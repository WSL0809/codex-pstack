#!/usr/bin/env python3
"""Validate the package's metadata, installed references, and migration coverage."""

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)

    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    compat = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    check(manifest["name"] == compat["name"] == "codex-pstack", "plugin identities differ")
    check(manifest["version"] == compat["version"], "plugin versions differ")
    check(compat["skills"] == "./skills/", "invalid skills directory")
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    check(len(skills) == 8, "expected eight skills")
    license_text = (root / "LICENSE").read_text(encoding="utf-8")
    for skill in skills:
        body = skill.read_text(encoding="utf-8")
        front = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: (\"[^\n]+\")\n---\n", body)
        check(front is not None, f"invalid frontmatter: {skill}")
        if front:
            check(front[1] == skill.parent.name, f"name mismatch: {skill}")
            description = json.loads(front[2])
            check(0 < len(description) <= 1024, f"invalid description: {skill}")
        ui = (skill.parent / "agents/openai.yaml").read_text(encoding="utf-8")
        fields = dict((k, json.loads(v)) for k, v in re.findall(r'^  ([a-z_]+): (".*")$', ui, re.M))
        check(25 <= len(fields.get("short_description", "")) <= 64, f"invalid short description: {skill}")
        check("$" + skill.parent.name in fields.get("default_prompt", ""), f"missing skill invocation: {skill}")
        check((skill.parent / "LICENSE").read_text(encoding="utf-8") == license_text, f"missing attribution: {skill}")

    for page in root.rglob("*.md"):
        text = page.read_text(encoding="utf-8")
        if "skills" in page.relative_to(root).parts:
            check(not re.search(r"\.cursor/|subagent_type:|run_in_background:|/loop\b|claude-opus-|grok-4", text), f"unadapted runtime requirement: {page}")
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
            if re.match(r"[a-z]+://|#|mailto:", link):
                continue
            destination = (page.parent / link.split("#")[0]).resolve()
            check(destination.is_relative_to(root.resolve()), f"link leaves package: {page}: {link}")
            check(destination.exists(), f"broken link: {page}: {link}")
            if "skills" in page.relative_to(root).parts:
                check(destination.is_relative_to((root / "skills").resolve()), f"installed skill depends on uninstalled file: {page}: {link}")

    migration = json.loads((root / "migration.json").read_text(encoding="utf-8"))
    for group in ("skills", "playbooks"):
        for name, row in migration[group].items():
            check((root / row["target"]).is_file(), f"missing migration target: {name}")
    upstream = root.parent / "pstack"
    if upstream.is_dir():
        actual = {p.parent.name for p in (upstream / "skills").glob("*/SKILL.md")}
        check(actual == set(migration["skills"]), "upstream skill coverage differs")
        actual_plays = {p.stem for p in (upstream / "skills/poteto-mode/playbooks").glob("*.md")}
        check(actual_plays == set(migration["playbooks"]), "upstream playbook coverage differs")
    return errors


if __name__ == "__main__":
    try:
        problems = validate()
    except (OSError, ValueError, KeyError) as error:
        problems = [str(error)]
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)
    print("Validated 8 skills, plugin metadata, references, licenses, and migration targets.")
