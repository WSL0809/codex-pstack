# Measurement and hillclimbing

State the intended claim, workload, unit, baseline revision, and acceptance threshold before changing code. Read the harness to establish what it includes and ignores.

- Confirm correct outputs, error counts, and that the expected work actually occurs inside the timed region.
- Compare equivalent versions, production settings, data, concurrency, and cache conditions. An untuned side measures configuration as well as implementation.
- Profile separately from reported timing. Identify the limiting resource or path, including a saturated load generator. Map it to source.
- Repeat and interleave baseline and treatment. Start with five runs per side for a comparison, then adjust to variability and cost. Report the median, spread, run count, and machine conditions. Label a requested one-run estimate as an estimate.
- Check physical and end-to-end limits. A change cannot save more total time than its original share of the path. A microbenchmark win needs a realistic user-path measurement before making a product claim.

For sustained improvement, freeze a correct harness and guardrails, record one hypothesis at a time, measure, and keep or revert based on evidence. Keep accepted changes separate when commits are part of the task. Stop at the requested target or budget, an unreliable harness, or a blocker that needs external change. Do not optimize away required work to improve the metric. A result smaller than measurement noise is inconclusive.
