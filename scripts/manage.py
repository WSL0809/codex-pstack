#!/usr/bin/env python3
"""Install a complete pstack runtime and expose its original skill directories."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parents[1]
RECEIPT = ".pstack-install.json"
LOCK = ".pstack-install.lock"
PACKAGE_ID = "codex-pstack"
IGNORED = {".git", "__pycache__", "node_modules", ".venv", "dist", "build", ".DS_Store"}


def safe_name(name):
    return isinstance(name, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) is not None and len(name) <= 64


def fingerprint(directory, source=False):
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"Expected a real directory: {directory}")
    result = {}
    for base, dirs, names in os.walk(directory, followlinks=False):
        if source:
            dirs[:] = [name for name in dirs if name not in IGNORED]
            names = [name for name in names if name not in IGNORED and not name.endswith((".pyc", ".pyo"))]
        for name in dirs + names:
            if (Path(base) / name).is_symlink():
                raise ValueError(f"Refusing symlink inside managed package: {Path(base) / name}")
        for name in names:
            path = Path(base) / name
            if not path.is_file():
                raise ValueError(f"Unsupported file: {path}")
            result[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(sorted(result.items()))


def source_receipt(package):
    manifest = json.loads((package / "plugin.json").read_text(encoding="utf-8"))
    files = fingerprint(package, source=True)
    names = sorted(p.name for p in (package / "skills").iterdir() if p.is_dir())
    skills = {}
    for name in names:
        prefix = f"skills/{name}/"
        contents = {path[len(prefix):]: digest for path, digest in files.items() if path.startswith(prefix)}
        if not safe_name(name) or "SKILL.md" not in contents:
            raise ValueError(f"Invalid skill: {name}")
        skills[name] = contents
    if "pstack" not in skills:
        raise ValueError("Package has no pstack entry point")
    identity = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    return {"package": PACKAGE_ID, "version": manifest["version"], "skills": skills,
            "runtime": {"path": "../.pstack-packages/" + identity, "files": files}}


def validate_hashes(files):
    if not isinstance(files, dict) or not files:
        raise ValueError("Invalid fingerprint map")
    for file, digest in files.items():
        if not isinstance(file, str) or not Path(file).parts or Path(file).is_absolute() or ".." in Path(file).parts or "\\" in file:
            raise ValueError(f"Invalid fingerprint path: {file}")
        if not isinstance(digest, str) or re.fullmatch(r"[a-f0-9]{64}", digest) is None:
            raise ValueError(f"Invalid fingerprint: {file}")


def read_receipt(target):
    path = target / RECEIPT
    if path.is_symlink():
        raise ValueError(f"Refusing symlink receipt: {path}")
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("package") != PACKAGE_ID:
        raise ValueError(f"Unknown installation receipt: {path}")
    skills = value.get("skills")
    if not isinstance(skills, dict) or not skills:
        raise ValueError(f"Invalid installation receipt: {path}")
    for name, files in skills.items():
        if not safe_name(name) or not isinstance(files, dict) or "SKILL.md" not in files:
            raise ValueError(f"Invalid skill in receipt: {name}")
        validate_hashes(files)
    if "runtime" in value:
        runtime = value["runtime"]
        if not isinstance(runtime, dict) or not isinstance(runtime.get("path"), str) or re.fullmatch(r"\.\./\.pstack-packages/[a-f0-9]{64}", runtime["path"]) is None:
            raise ValueError("Invalid runtime path in receipt")
        validate_hashes(runtime.get("files"))
    return value


def runtime_path(target, receipt):
    store = target.parent / ".pstack-packages"
    if store.is_symlink():
        raise ValueError(f"Refusing symlink runtime store: {store}")
    return store / receipt["runtime"]["path"].rsplit("/", 1)[1]


def entry_state(target, receipt, name):
    path = target / name
    if "runtime" in receipt:
        expected = runtime_path(target, receipt) / "skills" / name
        if not path.is_symlink():
            return "modified" if path.exists() else "missing"
        if path.resolve() != expected.resolve():
            return "modified"
        path = expected
    if not path.exists() and not path.is_symlink():
        return "missing"
    try:
        return "ok" if fingerprint(path) == receipt["skills"][name] else "modified"
    except ValueError:
        return "modified"


def inspect(target, receipt):
    if receipt is None:
        return {"installed": False, "skills": {}}
    result = {"installed": True, "version": receipt["version"],
              "skills": {name: entry_state(target, receipt, name) for name in receipt["skills"]}}
    if "runtime" in receipt:
        path = runtime_path(target, receipt)
        try:
            result["runtime"] = "ok" if fingerprint(path) == receipt["runtime"]["files"] else "modified"
        except ValueError:
            result["runtime"] = "modified" if path.exists() or path.is_symlink() else "missing"
    return result


def require_clean(target, old, new):
    old_names = set(old["skills"]) if old else set()
    new_names = set(new["skills"]) if new else set()
    for name in sorted(old_names | new_names):
        path = target / name
        if name in old_names:
            if entry_state(target, old, name) == "modified":
                raise ValueError(f"Local changes in {path}; preserve or move them before updating/removing")
        elif path.exists() or path.is_symlink():
            raise ValueError(f"Name collision at {path}; no files changed")
    if old and "runtime" in old and inspect(target, old)["runtime"] == "modified":
        raise ValueError("Local changes in the installed runtime; preserve them before updating/removing")


def prepare_runtime(target, new, package):
    path = runtime_path(target, new)
    if path.exists() or path.is_symlink():
        if fingerprint(path) != new["runtime"]["files"]:
            raise ValueError(f"Existing runtime has local changes: {path}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".stage-", dir=path.parent))
    try:
        for name in new["runtime"]["files"]:
            dest = stage / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(package / name, dest)
        if fingerprint(stage) != new["runtime"]["files"]:
            raise ValueError("Source changed during copy")
        stage.rename(path)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return True


def remove_entry(path):
    if path.is_symlink():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def cleanup_runtime(target, receipt):
    if receipt and "runtime" in receipt:
        path = runtime_path(target, receipt)
        if path.exists() and not path.is_symlink() and fingerprint(path) == receipt["runtime"]["files"]:
            shutil.rmtree(path)
            try:
                path.parent.rmdir()
            except OSError:
                pass


def transact(target, old, new, package):
    require_clean(target, old, new)
    old_names = set(old["skills"]) if old else set()
    new_names = set(new["skills"]) if new else set()
    created = prepare_runtime(target, new, package) if new else False
    stage = Path(tempfile.mkdtemp(prefix=".pstack-stage-", dir=target))
    completed = []
    receipt_path = target / RECEIPT
    old_bytes = receipt_path.read_bytes() if receipt_path.exists() else None
    try:
        (stage / "new").mkdir()
        (stage / "old").mkdir()
        for name in sorted(new_names):
            destination = runtime_path(target, new) / "skills" / name
            (stage / "new" / name).symlink_to(os.path.relpath(destination, target), target_is_directory=True)
        for name in sorted(old_names | new_names):
            live = target / name
            if live.exists() or live.is_symlink():
                live.rename(stage / "old" / name)
            completed.append(name)
            if name in new_names:
                (stage / "new" / name).rename(live)
        if new:
            temporary = stage / "receipt.json"
            temporary.write_text(json.dumps(new, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            os.replace(temporary, receipt_path)
        elif receipt_path.exists():
            receipt_path.unlink()
    except BaseException:
        for name in reversed(completed):
            remove_entry(target / name)
            backup = stage / "old" / name
            if backup.exists() or backup.is_symlink():
                backup.rename(target / name)
        if old_bytes is not None:
            receipt_path.write_bytes(old_bytes)
        elif receipt_path.exists():
            receipt_path.unlink()
        if created:
            cleanup_runtime(target, new)
        raise
    finally:
        shutil.rmtree(stage)
    if old and old.get("runtime") != (new or {}).get("runtime"):
        cleanup_runtime(target, old)


def manage(action, target, package=PACKAGE):
    target = Path(target).expanduser().resolve()
    package = Path(package).resolve()
    if target == package or package in target.parents or target in package.parents:
        raise ValueError("Installation target must be outside the package tree")
    if action == "status":
        return inspect(target, read_receipt(target))
    target.mkdir(parents=True, exist_ok=True)
    lock = target / LOCK
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise ValueError(f"Install lock exists: {lock}. Check for a running installer before removing a stale lock.") from None
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "action": action}, stream)
        old = read_receipt(target)
        if action == "uninstall":
            if old:
                transact(target, old, None, package)
            return {"action": "uninstalled" if old else "not-installed", "target": str(target)}
        new = source_receipt(package)
        state = inspect(target, old)
        if old == new and state.get("runtime") == "ok" and all(s == "ok" for s in state["skills"].values()):
            return {"action": "unchanged", "target": str(target), "version": new["version"]}
        transact(target, old, new, package)
        return {"action": "updated" if old else "installed", "target": str(target), "version": new["version"], "skills": sorted(new["skills"])}
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "update", "status", "uninstall"])
    location = parser.add_mutually_exclusive_group()
    location.add_argument("--project", type=Path, help="Install in PROJECT/.agents/skills with a complete runtime beside it")
    location.add_argument("--target", type=Path, help="Explicit skills directory")
    args = parser.parse_args()
    target = args.target or (args.project / ".agents" / "skills" if args.project else Path.home() / ".agents" / "skills")
    try:
        result = manage(args.action, target)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        failed = args.action == "status" and (not result["installed"] or result.get("runtime", "ok") != "ok" or any(s != "ok" for s in result["skills"].values()))
        return 1 if failed else 0
    except (OSError, ValueError, KeyError) as error:
        print(f"pstack: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
