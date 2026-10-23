# Formal checks and statecharts

Choose one consequential property from the actual code. State the property and the harm of violating it in plain words. Select the least costly suitable tool: a model checker for event ordering, a code verifier for language-supported properties, or a proof assistant when a finite bound is insufficient. Discover installed tools; do not assume one exists.

Map model states and transitions to source. An atomic model step must correspond to an atomic step in the implementation. Document bounds, fairness, environmental assumptions, excluded behavior, covered files, and the revision at which correspondence was checked.

Prove the check can fail on an isolated broken variant. Report real counterexamples in the code's terms. Do not weaken a property to silence a defect or modify production code during a verification-only task. Generated property tests can be a useful fallback, but are not a formal proof.

For a statechart, show user-observable states and transitions with Mermaid or the project's existing notation. Mark observed working, observed failing, and unverified behavior separately. Derive from an existing model when available. A chart alone does not prove that code matches it. Translate a checker counterexample into a numbered transition path.

On maintenance, inspect changes since the recorded revision, update the model or harness only where behavior legitimately changed, rerun, and distinguish model drift from a product defect. Advance the correspondence revision only after that check. Hand off one reproducible command and state exactly what a pass covers.
