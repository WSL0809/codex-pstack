---
name: pstack-design
description: "Design software data models, interfaces, and module boundaries before implementation. Use for architecture decisions, competing implementation shapes, or repeated workarounds that suggest a wrong abstraction."
---

# Design

Read [the Codex adapter](../pstack/references/codex.md). Establish whether the requested deliverable is a design or an implemented change. A design request alone does not authorize implementation.

Trace the existing caller, state, and failure paths. Read history when ownership or a compatibility choice needs explanation. Code shows behavior; it does not establish historical intent.

Write the caller's usage first. Derive the domain types, invariants, function signatures, ownership, and module boundaries from it. Keep internals private and external representations at the boundary. Use [the principles](../pstack/references/principles.md) for relevant decisions.

For a consequential or uncertain choice, compare at least two structurally distinct candidates. Name what evidence would choose between them. A small runnable prototype is useful for timing, concurrency, or interaction questions. Independent agents can explore alternatives when permitted; otherwise compare them in the current session. Do not claim multiple independent judgments.

Screen each candidate:

- Does its interface hide meaningful complexity, or merely forward calls?
- Does one fact require coordinated edits across multiple modules?
- Can a caller import internals or choose an obsolete alternative?
- Does state have one owner? Can concurrent writers avoid sharing?
- Can a new contributor make a locally plausible change that violates a distant rule?

Return the chosen shape, the alternative, the deciding reason, and the expected verification. During authorized implementation, track deviations. Repeated same-shaped deviations, casts, or caller coordination are evidence to revisit the design. One legitimate edge case is not enough to restart the architecture.
