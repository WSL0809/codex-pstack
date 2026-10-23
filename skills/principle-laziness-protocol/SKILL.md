---
name: principle-laziness-protocol
description: "Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem."
---

<!-- codex-pstack adapter begin -->
Before following the upstream instructions below, resolve this file to its real path and read the [Codex adapter](../../docs/harness/codex.md). Apply its tool, model, path, and authorization mappings. Keep the original workflow and report unsupported steps; do not replace it with a shorter workflow.
<!-- codex-pstack adapter end -->

# Laziness Protocol

- **Consolidate decisions.** Do not repeat the same choice in several places. Put it behind one source of truth and pass the result as a simple flag.
- **Minimize the diff.** Make the smallest change that solves the problem. Fewer lines beat "elegant" boilerplate.
