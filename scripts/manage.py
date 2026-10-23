#!/usr/bin/env python3
"""Install the complete skill set without changing Codex or project configuration."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parents[1]
RECEIPT = ".pstack-install.json"
LOCK = ".pstack-install.lock"
PACKAGE_ID = "codex-pstack"


def fingerprint(directory):
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"Expected a real directory: {directory}")
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Refusing symlink inside managed skill: {path}")
        if path.is_file():
            result[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        elif not path.is_dir():
            raise ValueError(f"Unsupported file: {path}")
    return result


def source_receipt(package):
    manifest = json.loads((package / "plugin.json").read_text(encoding="utf-8"))
    skills = {p.name: fingerprint(p) for p in sorted((package / "skills").iterdir()) if p.is_dir()}
    if not skills or "pstack" not in skills:
        raise ValueError("Package has no pstack entry point")
    for name, files in skills.items():
        if not safe_name(name) or "SKILL.md" not in files:
            raise ValueError(f"Invalid skill: {name}")
    return {"package": PACKAGE_ID, "version": manifest["version"], "skills": skills}


def safe_name(name):
    return isinstance(name, str) and (name == "pstack" or name.startswith("pstack-")) and all(c in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name)


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
        for file, digest in files.items():
            parts = Path(file).parts
            if not parts or Path(file).is_absolute() or ".." in parts or not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                raise ValueError(f"Invalid fingerprint in receipt: {file}")
    return value


def inspect(target, receipt):
    if receipt is None:
        return {"installed": False, "skills": {}}
    states = {}
    for name, expected in receipt["skills"].items():
        path = target / name
        if not path.exists() and not path.is_symlink():
            states[name] = "missing"
        else:
            try:
                states[name] = "ok" if fingerprint(path) == expected else "modified"
            except ValueError:
                states[name] = "modified"
    return {"installed": True, "version": receipt["version"], "skills": states}


def transact(target, old, new, package):
    old_names = set(old["skills"]) if old else set()
    new_names = set(new["skills"]) if new else set()
    for name in sorted(old_names | new_names):
        path = target / name
        exists = path.exists() or path.is_symlink()
        if name in old_names:
            if exists and fingerprint(path) != old["skills"][name]:
                raise ValueError(f"Local changes in {path}; preserve or move them before updating/removing")
        elif exists:
            raise ValueError(f"Name collision at {path}; no files changed")

    stage = Path(tempfile.mkdtemp(prefix=".pstack-stage-", dir=target))
    completed = []
    receipt_path = target / RECEIPT
    old_bytes = receipt_path.read_bytes() if receipt_path.exists() else None
    try:
        for name in sorted(new_names):
            shutil.copytree(package / "skills" / name, stage / "new" / name)
            if fingerprint(stage / "new" / name) != new["skills"][name]:
                raise ValueError(f"Source changed during copy: {name}")
        (stage / "old").mkdir()
        for name in sorted(old_names | new_names):
            live = target / name
            backup = stage / "old" / name
            if live.exists():
                live.rename(backup)
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
            live, backup = target / name, stage / "old" / name
            if live.exists():
                shutil.rmtree(live)
            if backup.exists():
                backup.rename(live)
        if old_bytes is not None:
            receipt_path.write_bytes(old_bytes)
        elif receipt_path.exists():
            receipt_path.unlink()
        raise
    finally:
        shutil.rmtree(stage)


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
        if old == new and all(state == "ok" for state in inspect(target, old)["skills"].values()):
            return {"action": "unchanged", "target": str(target), "version": new["version"]}
        transact(target, old, new, package)
        return {"action": "updated" if old else "installed", "target": str(target), "version": new["version"], "skills": sorted(new["skills"])}
    finally:
        lock.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "update", "status", "uninstall"])
    location = parser.add_mutually_exclusive_group()
    location.add_argument("--project", type=Path, help="Install only in PROJECT/.agents/skills")
    location.add_argument("--target", type=Path, help="Explicit skills directory for testing or legacy clients")
    args = parser.parse_args()
    target = args.target or (args.project / ".agents" / "skills" if args.project else Path.home() / ".agents" / "skills")
    try:
        result = manage(args.action, target)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1 if args.action == "status" and (not result["installed"] or any(s != "ok" for s in result["skills"].values())) else 0
    except (OSError, ValueError, KeyError) as error:
        print(f"pstack: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
