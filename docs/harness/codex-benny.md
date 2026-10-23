# Benny in Codex

The entire original pack is present at `<pstack>/automations/benny/`, including its three dormant skills, references, configuration examples, and prompt templates. Preserve its install, configuration, source-thread safety, evidence, deduplication, and bounded-fix procedures.

Read `FOR_AGENTS.md` and `CODEX.md` before setup. Copy the complete pack to the target project's `.agents/automations/benny/`, preserving user-owned configuration as the original instructs. Interpret `.cursor/automations/benny/` as that path and `.cursor/benny/` as `.agents/benny/`. The copied pack includes CODEX.md so its dormant skills keep a local adapter pointer.

Instead of editing `.cursor/settings.json`, install this complete package for the target project with `python3 <pstack>/scripts/manage.py install --project <target-project>`. Verify original skill names at repo scope in a fresh session. Do not count an existing user-scoped copy as proof of a project installation. Do not auto-commit merely because setup requires committed artifacts before activation.

Use a documented automation-authoring skill only if the current Codex environment provides one and the user requested setup. Preserve the original editor review and approval boundary. If no compatible automation editor and trigger service exists, prepare the configuration and copied pack, report the missing capability, and leave both automations disabled. Do not replace the original service with an invented webhook, direct backend request, or polling daemon.

Use actual configured Slack and tracker tools. Preserve immutable channel/thread coordinates, trusted triage identity, one thread-only verdict, and the restriction that delegated workers cannot post. Missing required isolation or a missing source parent must fail closed. Installing this package alone grants no messaging, ticket, PR, or automation permission.

All secret, identity, control-adapter, model availability, and thread-safety checks in the original remain required. A configuration draft is not an enabled or tested automation.
