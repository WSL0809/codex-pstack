---
name: pstack-explain
description: "Explain how a codebase works or why a design exists using source and historical evidence. Use for subsystem walkthroughs, teaching, architectural rationale, or rebuilding the current task context."
---

# Explain

Read [the Codex adapter](../pstack/references/codex.md). Keep investigation read-only. Determine whether the user wants mechanism, historical rationale, teaching, or a status reconstruction.

For mechanism, start at the real entry point. Trace data, state ownership, control flow, failures, and relevant side effects. Explain one concrete input through the path. Cite files and lines that were actually read. Use a small diagram when it clarifies boundaries or transitions.

For rationale, inspect relevant commits, PR descriptions, design records, and available connected sources. Search only the relevant project context. Distinguish direct statements, converging indirect evidence, inference, speculation, and unknowns. Code can prove what happens, but not why its author chose it. Treat the user's suggested reason as a hypothesis. Include contradictory evidence rather than constructing a tidier history.

For teaching, establish the reader's starting point from the conversation. Build an explanation from behavior to mechanism to tradeoffs. Introduce terminology when the reader needs it. A small worked example is often clearer than a file inventory.

For recall or status, use the current conversation, a supplied handoff, and current repository state. Do not search unrelated private transcripts. Separate completed, verified, pending, and changed assumptions. Verify material inherited claims against the current artifact without repeating already valid work gratuitously.

Return the answer first, supporting source pointers, and the uncertainty that matters to the question. Do not modify or publish documentation unless requested.
