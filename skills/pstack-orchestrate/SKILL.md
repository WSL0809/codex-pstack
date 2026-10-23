---
name: pstack-orchestrate
description: "Plan and carry out a long software task as bounded, verifiable units with durable handoffs. Use for migrations, several dependent changes, permitted parallel work, or pausing and resuming an engineering task."
---

# Orchestrate

Read [the Codex adapter](../pstack/references/codex.md). This workflow works in one session and does not require subagents. Use a normal task list for short work. Use durable records only when the work outlives the current context or involves several owners.

## Frame and pilot

Define a countable done condition, scope, dependency order, verification exits, budget if supplied, and stop conditions. Separate independent units from shared writes. For an unfamiliar repeated unit, complete one through implementation, verification, and integration before scaling. Use the pilot to revise the brief and check recipe.

For each unit record its goal, allowed paths, forbidden paths, baseline, acceptance, check command, owner, and result location. Scope a unit so another worker can complete it without guessing at unstated intent. Keep upstream context available to dependent units.

## Execute and integrate

Run sequentially by default. If delegation is allowed and beneficial, assign disjoint ownership and bounded concurrency using the session's tools. Preserve others' edits. Separate implementation and independent verification when warranted. Do not add a verifier whose entire useful work is a cheap command the worker can run.

Integrate from the first verified unit, not only at the end. One owner changes branch topology. Before accepting late or retried output, compare its baseline with current code. Bound retries by failure type and evidence; replan after repeated failure instead of looping blindly.

## Durable state

Use the project's existing tracker, or a task-specific directory. Keep these facts in a compact file or small tables:

- Task outcome, scope, constraints, decisions, and open questions.
- Units with owner, dependency, state, branch, revision, and output pointer.
- Evidence with revision, check, result, environment, and artifact path.
- Next action and exact resume command where applicable.

An append-only JSONL or TSV receipt is adequate for a single writer. If several actors need to publish facts, give each its own file and aggregate on read. Use structural synchronization only when one shared mutable object is essential. Derive status counts from records. Do not keep parallel hand-edited copies.

## Pause and resume

On an explicit pause, start no new work. Stop active work at a safe boundary and preserve files. Do not commit, push, or cancel unrelated processes solely to pause. Record uncommitted changes, live process handles, known failures, and the next step. Do not claim work continues after the session ends unless an actual authorized background capability is running.

On resume, read the handoff and current Git state. Reconcile the plan with what exists. Reuse valid evidence; recheck changed artifacts and material unsupported claims. Resume from the first pending unit.

For delivery read [delivery](../pstack/references/delivery.md). For worktree cleanup, read [cleanup](references/cleanup.md). At close, account for every unit as complete, blocked, or deliberately excluded. Confirm the done condition against the actual artifacts.
