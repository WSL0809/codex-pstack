---
name: pstack-review
description: "Review a code change for concrete correctness, compatibility, and maintainability risks. Use for adversarial review, blast-radius analysis, or checking a small diff with hidden downstream effects."
---

# Review

Read [the Codex adapter](../pstack/references/codex.md). Review is read-only unless the user also requests fixes. Use isolated temporary files for executable probes. Do not create production side effects to prove a finding.

Establish the change's intent, base revision, full diff, and relevant consumer contracts. Read beyond changed lines. Follow wire formats, persistence, pinned library behavior, callbacks, lifecycle ordering, and external consumers that symbol search misses.

Find the fact each safety argument depends on. Verify the most consequential facts by source inspection and, when practical, an executable probe against the real code. Do not invent callers, assign unsupported probabilities, or treat a search with no matches as proof of absence.

When independent review is permitted and worthwhile, provide the same intent and artifacts to each reviewer without the author's preferred verdict. Model diversity is useful only when available and authorized. Do not dismiss a valid minority finding or treat consensus as a proof. Without agents, use a separate self-review pass and label it.

For each finding provide the trigger, observed or traced consequence, file and line, severity, and the check that supports it. Prioritize real contract violations and structural mistakes over style preferences. Classify uncertain concerns separately. Explain rejected findings when that prevents repeated work.

Return actionable findings first, then material open questions and checks performed. If there are no findings, say so and state coverage limits. Do not automatically modify code, post review comments, or open follow-up issues.
