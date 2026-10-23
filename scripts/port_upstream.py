#!/usr/bin/env python3
"""Render the pinned upstream tree with a small, explicit Codex adapter."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def destination(source):
    return {
        "README.md": "docs/UPSTREAM_README.md",
        "plugin.json": "upstream/metadata/plugin.json",
        ".cursor-plugin/plugin.json": "upstream/metadata/cursor-plugin.json",
        ".gitignore": "upstream/metadata/gitignore",
    }.get(source, source)


def fields(content):
    match = re.match(r"\A---\n(.*?)\n---\n", content, re.S)
    if not match:
        raise ValueError("Missing upstream frontmatter")
    front = {}
    key = None
    for line in match[1].splitlines():
        entry = re.match(r"^([\w-]+): (.*)$", line)
        if entry:
            key = entry[1]
            front[key] = entry[2]
        elif key and (line.startswith((" ", "\t")) or not line):
            front[key] += "\n" + line
        else:
            raise ValueError("Unsupported upstream frontmatter line: " + line)
    if not front.get("name") or not front.get("description"):
        raise ValueError("Missing upstream name or description")
    return front, content[match.end():]


def adapter_notice(source):
    if source.startswith("automations/benny/"):
        reference = os.path.relpath("automations/benny/CODEX.md", str(PurePosixPath(source).parent))
    else:
        reference = os.path.relpath("docs/harness/codex.md", str(PurePosixPath(source).parent))
    return ("\n<!-- codex-pstack adapter begin -->\n"
            "Before following the upstream instructions below, resolve this file to its real path "
            "and read the [Codex adapter](" + reference + "). Apply its tool, model, path, and authorization mappings. "
            "Keep the original workflow and report unsupported steps; do not replace it with a shorter workflow.\n"
            "<!-- codex-pstack adapter end -->\n")


def rewrite_readme_links(text):
    def replace(match):
        link = match[1]
        if re.match(r"[a-z]+://|#|mailto:", link):
            return match[0]
        path, separator, anchor = link.partition("#")
        path = destination(str(PurePosixPath(path)))
        target = os.path.relpath(path, "docs").replace(os.sep, "/")
        return "](" + target + (separator + anchor if separator else "") + ")"
    return re.sub(r"\]\(([^)\n]+)\)", replace, text)


def render(source, data):
    if source == "skills/poteto-mode/scripts/worktree-audit.sh":
        text = data.decode("utf-8")
        original = '# Transcripts dir: ~/.cursor/projects/<slugified-repo-path>/agent-transcripts.\nslug=$(printf \'%s\' "$main_wt" | sed \'s#^/##; s#/#-#g\')\ntranscripts="$HOME/.cursor/projects/$slug/agent-transcripts"'
        replacement = '# Codex history must be supplied explicitly for this repository.\ntranscripts="${PSTACK_TRANSCRIPTS_DIR:-}"\n[ -n "$transcripts" ] || echo "warn: no transcript directory supplied; activity is unknown" >&2'
        if text.count(original) != 1:
            raise ValueError("Worktree transcript patch no longer matches upstream")
        text = text.replace(original, replacement)
        anchor = '\n\tprintf "%s\\t%s\\t%s\\t%s\\t%s\\t%s\\t%s\\t%s\\t%s\\n"'
        if text.count(anchor) != 1:
            raise ValueError("Worktree activity patch no longer matches upstream")
        text = text.replace(anchor, '\n\tif [ ! -d "$transcripts" ] && [ "$bucket" = safe ]; then bucket=review-no-history; fi\n' + anchor)
        return text.encode("utf-8")
    if source.endswith("/SKILL.md"):
        text = data.decode("utf-8")
        front, body = fields(text)
        if source.startswith("skills/"):
            header = "---\nname: " + front["name"] + "\ndescription: " + front["description"] + "\n---\n"
        else:
            header = text[:len(text) - len(body)]
        return (header + adapter_notice(source) + body).encode("utf-8")
    if source.startswith("agents/") and source.endswith(".md"):
        text = data.decode("utf-8")
        _, body = fields(text)
        return (text[:len(text) - len(body)] + adapter_notice(source) + body).encode("utf-8")
    if source == "automations/benny/FOR_AGENTS.md":
        return (adapter_notice(source) + data.decode("utf-8")).encode("utf-8")
    if source == "README.md":
        return rewrite_readme_links(data.decode("utf-8")).encode("utf-8")
    return data


def generated(root=ROOT):
    lock = json.loads((root / "upstream/lock.json").read_text(encoding="utf-8"))
    files = {}
    rows = {}
    with zipfile.ZipFile(root / "upstream/pstack.zip") as archive:
        if set(archive.namelist()) != {row["path"] for row in lock["files"]}:
            raise ValueError("Snapshot inventory differs from lock")
        for row in lock["files"]:
            source = row["path"]
            if PurePosixPath(source).is_absolute() or ".." in PurePosixPath(source).parts:
                raise ValueError("Unsafe snapshot path")
            data = archive.read(source)
            if hashlib.sha256(data).hexdigest() != row["sha256"]:
                raise ValueError("Snapshot digest differs: " + source)
            target = destination(source)
            converted = render(source, data)
            files[target] = (converted, row["mode"])
            rows[source] = {"target": target, "source_sha256": row["sha256"], "target_sha256": hashlib.sha256(converted).hexdigest(), "change": "verbatim" if converted == data else "codex-adapter"}
            if source.startswith("skills/") and source.endswith("/SKILL.md"):
                front, _ = fields(data.decode("utf-8"))
                name = front["name"]
                implicit = "false" if front.get("disable-model-invocation") == "true" else "true"
                ui = "interface:\n" + "".join("  " + key + ": " + json.dumps(value) + "\n" for key, value in [
                    ("display_name", name),
                    ("short_description", ("Original pstack workflow: " + name)[:64]),
                    ("default_prompt", "Use $" + name + " for this task, following the original pstack workflow.")])
                ui += "policy:\n  allow_implicit_invocation: " + implicit + "\n"
                files[str(PurePosixPath(target).parent / "agents/openai.yaml")] = (ui.encode("utf-8"), 0o644)
    migration = {"upstream": {k: lock[k] for k in ("repository", "commit", "path", "upstream_version")},
                 "top_level_skills": sorted(PurePosixPath(p).parent.name for p in rows if p.startswith("skills/") and p.endswith("/SKILL.md")),
                 "dormant_skills": sorted(p for p in rows if p.startswith("automations/") and p.endswith("/SKILL.md")),
                 "playbooks": sorted(p for p in rows if p.startswith("skills/poteto-mode/playbooks/") and p.endswith(".md")),
                 "files": rows}
    files["migration.json"] = ((json.dumps(migration, indent=2) + "\n").encode("utf-8"), 0o644)
    return files


def check(root=ROOT):
    errors = []
    for name, (expected, mode) in generated(root).items():
        path = root / name
        if not path.is_file() or path.read_bytes() != expected:
            errors.append("Generated file differs: " + name)
        elif bool(path.stat().st_mode & 0o111) != bool(mode & 0o111):
            errors.append("Executable mode differs: " + name)
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        problems = check()
        if problems:
            raise SystemExit("\n".join(problems))
        print("Pinned upstream files and all generated adaptations match.")
    else:
        for name, (content, mode) in generated().items():
            path = ROOT / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            path.chmod(mode)
        print("Restored all upstream files with only recorded compatibility changes.")
