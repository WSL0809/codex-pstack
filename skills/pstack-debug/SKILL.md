---
name: pstack-debug
description: "Diagnose reproducible defects, runtime symptoms, captured traces, and measured performance regressions using evidence. Use for root-cause analysis, a bug fix, benchmarking, or sustained metric improvement."
---

# Debug

Read [the Codex adapter](../pstack/references/codex.md). Respect a diagnosis-only request. For performance work read [measurement](references/measurement.md).

1. State expected behavior, observed behavior, environment, and the smallest reproduction. Run it on the matching surface. If unavailable, state the missing access or condition and collect the nearest useful evidence.
2. Trace the affected path. Form competing causes and choose an observation that separates them. Add focused instrumentation when state is unclear. For a trace, inspect its format, capture conditions, thread or process attribution, and missing intervals before interpreting a hot spot.
3. Locate the first wrong decision. Determine whether the triggering state is legitimate. A valid external failure needs handling; an impossible internal state needs its producer fixed.
4. If two fixes fail under one premise, write that premise and test it directly. Remove changes supported only by rejected hypotheses.
5. When fixing is requested, use the smallest change justified by the evidence. For an inexpensive existing test path, establish a failing-before regression test, then fix and rerun it. Do not create a brittle harness merely to satisfy TDD.
6. Repeat the original reproduction and relevant nearby checks. Trace a shared primitive through its actual consumers. Treat an unavailable or inconclusive check as a gap, not a pass.

Report the symptom, mechanism, source evidence, change if any, and failing-before/passing-after results. If no reproduction was possible, qualify the diagnosis and verification explicitly.
