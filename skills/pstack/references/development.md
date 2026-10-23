# Development routes

## Feature

Trace the relevant consumer path and state ownership. State acceptance in observable terms. If the change introduces a meaningful interface or state model, read [design](../../pstack-design/SKILL.md); a function boundary alone does not justify a large design exercise.

Implement the smallest coherent increment. Delegate only when allowed and useful, with disjoint write ownership. Check the behavior on its actual surface. Use [verify](../../pstack-verify/SKILL.md) for unclear or broad verification. Review the diff for unintended changes. Use [delivery](delivery.md) when the task includes delivery.

## Refactor and migration

Identify behavior that must remain stable and capture its baseline. Map callers, serialization, external consumers, and deployment constraints. Remove dead code first. Establish a target shape and explicit verification units. Prefer a codemod when the transformation repeats or manual inspection is unreliable.

Migrate internal callers and delete obsolete entry points in one bounded wave when compatibility allows it. Do not impose this on external APIs or mixed-version deployments. Record expected intermediate failures within a unit. Verify each unit's exit before depending on it. At completion search for old callers, run relevant static and runtime checks, and inspect the final diff.

## Prototype

Name the question the prototype should answer and the observation that decides it. Build the cheapest runnable slice, using isolated files when useful. For a contested interaction or architecture, compare distinct shapes with the same input. Report what was observed and what remains untested. Carry code into production only after inspecting assumptions and adding the required integration checks.

## Visual parity

Capture both surfaces under the same viewport, state, font, data, and timing. Compare screenshots and interactions. Fix the first material mismatch and recapture. Do not infer visual equivalence from source or a successful build. If the target cannot be opened, state which reference was available and which claims remain unverified.
