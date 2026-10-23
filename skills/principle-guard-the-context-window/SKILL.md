---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads."
---

<!-- codex-pstack adapter begin -->
Before following the upstream instructions below, resolve this file to its real path and read the [Codex adapter](../../docs/harness/codex.md). Apply its tool, model, path, and authorization mappings. Keep the original workflow and report unsupported steps; do not replace it with a shorter workflow.
<!-- codex-pstack adapter end -->

# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
