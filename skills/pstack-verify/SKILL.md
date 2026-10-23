---
name: pstack-verify
description: "Verify observable software behavior and create or maintain repeatable verification recipes. Use to prove a change works, check a risky invariant, model concurrency, or update verification that has drifted from code."
---

# Verify

Read [the Codex adapter](../pstack/references/codex.md). Identify the exact claim, artifact revision, inputs, environment, and expected observation. Choose the cheapest check that reaches the behavior. A type check, unit test, live UI run, and benchmark support different claims.

Prefer existing project checks. Run through the consumer's interface and inspect actual values and effects. Derive expected results from the requirement. Confirm the check can detect the target failure, using a known regression or an isolated broken variant when useful. Never mutate a live system to demonstrate a failure without authorization.

Report the command or action, actual result, artifact revision, and coverage gap. A check that could not run is blocked. A failed assertion is failed. Neither is passed. Reassess receipts when the code, dependency, configuration, or environment changes.

## Reusable verification

When requested or justified by repeated complex work, create a project-local recipe or skill using the available skill creator. Include real commands, prerequisites, setup and cleanup, a feature-to-code map, observable pass criteria, and evidence locations. Keep language and platform choices tied to the project.

Run the recipe as a new user would. A recipe that was not executed is a draft. For maintenance, compare covered code and behavior with the recorded baseline, fix proven drift, and rerun affected checks. Separate a product defect from a stale verification expectation; do not weaken a valid assertion to make it green.

For races, retries, parsers, unsafe code, or state-machine properties beyond practical test coverage, read [formal verification](references/formal.md). For timing claims, read [measurement](../pstack-debug/references/measurement.md).
