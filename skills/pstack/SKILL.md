---
name: pstack
description: "Apply pstack engineering workflows to a software task: establish evidence, choose the data model, implement a bounded change, and verify observable behavior. Use when the user asks for pstack, an engineering workflow, or a rigorous end-to-end implementation."
---

# Pstack for Codex

Carry the requested software task through to a verifiable result. Scale the process to the uncertainty and impact. A small local edit needs a small local check, not an architecture panel.

## Start

Read applicable AGENTS.md files. Inspect the working tree and the relevant code before changing it. Preserve edits owned by the user or other workers. State the requested outcome and the observable acceptance condition. Ask only for missing choices that materially affect the result and cannot be learned from the repository or an experiment.

Read [the Codex adapter](references/codex.md) on first use. It governs capability discovery, collaboration, permissions, and portable paths. Read only the route needed below. Links are relative to this skill's installed directory, not the user's current directory.

| Task | Read next |
|---|---|
| New behavior, refactor, migration, prototype, visual parity | [Development](references/development.md) |
| Bug, runtime symptom, captured trace, performance regression | [Debug](../pstack-debug/SKILL.md) |
| Data model, interface, module boundary, design alternatives | [Design](../pstack-design/SKILL.md) |
| Review a diff or assess its impact | [Review](../pstack-review/SKILL.md) |
| Prove behavior, build a verification recipe, formal verification | [Verify](../pstack-verify/SKILL.md) |
| Understand code, explain historical intent, teach a subsystem | [Explain](../pstack-explain/SKILL.md) |
| Long task, multiple units, handoff, pause or resume | [Orchestrate](../pstack-orchestrate/SKILL.md) |
| Repeated mistakes, lessons, skill authoring or evaluation | [Improve](../pstack-improve/SKILL.md) |
| PR preparation, CI repair, review follow-up, authorized landing | [Delivery](references/delivery.md) |
| Prompt refinement, restatement, docs or clear writing | [Communication](references/communication.md) |

For an unfamiliar task, define a short workflow from its outcome, constraints, uncertainties, acceptance checks, and stop conditions. Reuse relevant routes. Do not force an unrelated playbook.

## Engineering decisions

Use [the principles](references/principles.md) when a design or implementation decision needs them. Keep these checks active:

- Identify the domain shape and the owner of mutable state before adding logic.
- Remove obsolete paths before adding new ones. Do not generalize from an imagined future requirement.
- Put validation at real trust boundaries. Trust internal types only when those boundaries and invariants hold.
- If two attempted fixes share a failed premise, test that premise before the next fix.
- Break large changes into units with explicit verification exits. Declare any temporary breakage inside a unit.
- Prefer a small rerunnable script when it makes nontrivial work easier to inspect or reproduce. Do not build an automation framework for a short edit.
- Verify the real behavior and the current artifact. An agent's report, a successful build, and a queued merge each prove different things.

## Finish

Report the user-visible outcome, the material design choice, the evidence actually obtained, and any remaining gap. Link files or artifacts that the user can inspect. Distinguish a failed check from an unavailable check. Do not claim a review was independent when you performed it yourself.

Commit, push, open a PR, send messages, merge, or deploy only within the user's task and existing authorization. Selecting this skill does not request those actions.
