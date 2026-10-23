#!/usr/bin/env python3
"""Check fidelity to the pinned source, Codex metadata, and package references."""

import json
from pathlib import Path
import re
import sys
import zipfile

from port_upstream import check as check_port, fields

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = check_port(root)
    def check(ok, message):
        if not ok:
            errors.append(message)

    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    compat = json.loads((root / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    check(manifest["name"] == compat["name"] == "codex-pstack", "plugin identities differ")
    check(manifest["version"] == compat["version"], "plugin versions differ")
    check(compat["skills"] == "./skills/", "invalid skills directory")
    migration = json.loads((root / "migration.json").read_text(encoding="utf-8"))
    expected = set(migration["top_level_skills"]) | {"pstack"}
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    check({p.parent.name for p in skills} == expected, "missing or extra skill entry points")
    check(len(migration["top_level_skills"]) == 57, "pinned upstream has 57 top-level skills")
    check(len(migration["dormant_skills"]) == 3, "pinned upstream has three dormant Benny skills")
    check(len(migration["playbooks"]) == 23, "pinned upstream has 23 playbooks")
    check(len(migration["files"]) == 184, "pinned upstream has 184 files")
    for skill in skills:
        front, body = fields(skill.read_text(encoding="utf-8"))
        check(front["name"] == skill.parent.name, f"name mismatch: {skill}")
        check(0 < len(front["description"]) <= 1024, f"invalid description: {skill}")
        check(set(front) == {"name", "description"}, f"unsupported frontmatter: {skill}")
        ui = (skill.parent / "agents/openai.yaml").read_text(encoding="utf-8")
        values = dict((k, json.loads(v)) for k, v in re.findall(r'^  ([a-z_]+): (".*")$', ui, re.M))
        check(25 <= len(values.get("short_description", "")) <= 64, f"invalid short description: {skill}")
        check("$" + skill.parent.name in values.get("default_prompt", ""), f"missing invocation: {skill}")

    with zipfile.ZipFile(root / "upstream/pstack.zip") as archive:
        for source, row in migration["files"].items():
            if source.endswith("/SKILL.md"):
                original = archive.read(source).decode("utf-8")
                original_front, original_body = fields(original)
                converted = (root / row["target"]).read_text(encoding="utf-8")
                check(converted.endswith(original_body), f"upstream skill body changed: {source}")
                if source.startswith("skills/"):
                    ui = (root / row["target"]).parent / "agents/openai.yaml"
                    implicit = "false" if original_front.get("disable-model-invocation") == "true" else "true"
                    check("allow_implicit_invocation: " + implicit in ui.read_text(), f"invocation policy changed: {source}")
        check((root / "LICENSE").read_bytes() == archive.read("LICENSE"), "upstream license changed")

    pages = [root / row["target"] for row in migration["files"].values() if row["target"].endswith(".md")]
    pages += [root / name for name in ("README.md", "docs/MIGRATION.md", "docs/VALIDATION.md", "docs/TLC.md", "docs/harness/codex.md", "docs/harness/codex-benny.md", "automations/benny/CODEX.md", "skills/pstack/SKILL.md")]
    for page in pages:
        for link in re.findall(r"\[[^\]]*\]\(([^)\n]+)\)", page.read_text(encoding="utf-8")):
            if re.match(r"[a-z]+://|#|mailto:", link):
                continue
            # This placeholder is part of the original report template, not a package reference.
            if link == "url" and page.relative_to(root).as_posix() == "skills/why/references/synthesizer-prompt.md":
                continue
            destination = (page.parent / link.split("#")[0]).resolve()
            check(destination.is_relative_to(root.resolve()), f"link leaves package: {page}: {link}")
            check(destination.exists(), f"broken link: {page}: {link}")
    return errors


if __name__ == "__main__":
    try:
        problems = validate()
    except (OSError, ValueError, KeyError) as error:
        problems = [str(error)]
    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)
    print("Validated 57 original skills + 1 alias, 3 dormant skills, 23 playbooks, and 184 source files.")
