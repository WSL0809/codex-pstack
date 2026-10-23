---
name: principle-subtract-before-you-add
description: "Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base."
---

<!-- codex-pstack adapter begin -->
Before following the upstream instructions below, resolve this file to its real path and read the [Codex adapter](../../docs/harness/codex.md). Apply its tool, model, path, and authorization mappings. Keep the original workflow and report unsupported steps; do not replace it with a shorter workflow.
<!-- codex-pstack adapter end -->

# Subtract Before You Add

When evolving a system, remove complexity first, then build. Default to subtraction.

Make simplification a continual investment. Leave the design slightly simpler and more capable behind the same or smaller surface than you found it.

- Sequence removal before construction
- Cut before you polish (get to the minimum before investing in quality)
- Design for observed usage, not speculative edge cases
- No speculative validators, parsers, or guards beyond what the spec demands
- Simplify prompts (remove redundant instructions, excessive templates)
- When a reference has no novel content, delete it rather than leaving a stub
