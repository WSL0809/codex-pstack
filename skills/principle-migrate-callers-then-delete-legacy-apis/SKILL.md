---
name: principle-migrate-callers-then-delete-legacy-apis
description: "Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers."
---

<!-- codex-pstack adapter begin -->
Before following the upstream instructions below, resolve this file to its real path and read the [Codex adapter](../../docs/harness/codex.md). Apply its tool, model, path, and authorization mappings. Keep the original workflow and report unsupported steps; do not replace it with a shorter workflow.
<!-- codex-pstack adapter end -->

# Migrate Callers Then Delete Legacy APIs

- Update tests to assert the new contract, and delete tests that only protect pre-refactor implementation details

**When this applies:**
- No external users depend on backward compatibility
- The project can absorb coordinated breaking changes
- The new API is part of a simplification or refactor initiative
