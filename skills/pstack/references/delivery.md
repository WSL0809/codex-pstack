# Delivery

Use only the actions included in the current task. Local implementation does not automatically request a commit, PR, merge, or deployment.

## Prepare a PR

Inspect the complete diff against the intended base, existing user edits, repository instructions, and checks. Keep changes scoped. Prefer small coherent commits when commits are requested; do not rewrite existing shared history for presentation. A PR description explains the concrete trigger, changed behavior, validation, and remaining limits. Respect the repository template.

When a GitHub connector is available, prefer it for supported operations. Otherwise use an authenticated forge CLI already available. Inspect its help if syntax is uncertain. Do not configure credentials or publish to a guessed remote. A multiline body should be a structured argument or a UTF-8 file, not an interpolated shell string.

## CI and review follow-up

Read the actual failing log and current head before editing. Distinguish a product defect, a test defect, and an infrastructure failure. Fix findings that are supported by evidence. Do not mechanically satisfy every reviewer suggestion or dismiss a lone finding by vote count. Rerun changed checks. A transient failure may justify a bounded retry, not an endless watcher.

## Authorized landing

Confirm the target branch, current artifact, required checks, and review state. A verification receipt for an older head needs a new check of the changed behavior and integration; default to re-verification rather than silently carrying it forward.

For a stack, maintain one topology owner. Land bottom-up into the intended trunk. After each merge, read the forge state back; queued or auto-merge-enabled is not merged. Re-evaluate base changes and resulting artifacts before the next merge. Stop on an unexplained check failure or loss of authorization. Report the verified landed range and any remaining unit separately.
