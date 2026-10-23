# Engineering principles

Read the section relevant to a decision. These are decision criteria, not a checklist that every task must expand.

## Shape and ownership

- **Foundational thinking.** Trace dominant reads and writes before choosing the data shape. Build the small shared foundation that later units require. Remove obsolete code before scaffolding replacement code.
- **Model the domain.** Use explicit states, discriminated variants, tables, indexes, or queues where they remove invalid combinations or duplicated rules. Group a module around the knowledge it owns, rather than merely load/validate/save phases.
- **Type discipline.** Distinguish semantic identifiers. Parse external inputs into domain values. Derive types from the authoritative schema. Do not use casts to hide a missing invariant.
- **Boundary discipline.** Validate untrusted input at actual boundaries. Keep business transformations independent of framework wiring. A cast, mutable alias, stale database row, or unchecked plugin can invalidate the assumption that internal values are trustworthy.
- **Separate before serializing.** First remove unnecessary shared write targets. If sharing is essential, use a single writer, transaction, lock, or compare-and-swap. A prose instruction is not a lock.
- **Idempotence.** Inspect existing state and apply the difference. Consider repeated runs and crashes between steps. Make incomplete artifacts recognizable and recoverable.

## Simplicity and experience

- **Laziness protocol.** Keep one source of truth for each decision. Choose the smallest complete change, not the shortest incomplete patch.
- **Subtract before adding.** Remove dead paths and redundant representations. Do not add speculative compatibility or validators without a contract that needs them.
- **Reader load.** Reduce both layers a reader must trace and mutable state they must remember. A useful module hides substantial complexity behind a small interface.
- **Experience first.** Judge the result from the consumer's and maintainer's perspective. Polish the core path and failure feedback before adding options.
- **Explore alternatives.** Compare structurally different designs when uncertainty is material. Use a small prototype for a question about feel or measured behavior. One obvious local edit does not need competing implementations.
- **Redesign from first principles.** Consider what the design would be if the new constraint existed from the start. Repeated same-shaped workarounds justify revisiting it. Deliver the warranted change in bounded units.
- **Migrate then delete.** For an internal API with no compatibility obligation, migrate its callers and remove the old API together. Public consumers and rolling deployments require an explicit compatibility plan.
- **Outcome-oriented execution.** Planned, reversible breakage may occur within a migration unit. Define its exit checks and keep unrelated paths working. Do not leave the final state partially migrated.

## Evidence and delivery

- **Prove it works.** Observe the real artifact on the relevant surface. State the exact claim each check supports.
- **Fix root causes.** Find the first wrong decision. Handling a state locally is correct when that state is legitimate; hiding an impossible state conceals the source fault.
- **Attack the premise.** After two failed fixes that share a premise, write and test that premise before adding a third fix.
- **Test behavior.** The test should fail when the public contract breaks and survive a change confined to internals. Derive expected results from the requirement.
- **Explain the number.** Validate output and work counts, noise, configuration fairness, and the limiting resource before interpreting a measurement.
- **Verifiable units.** Start from an understood baseline, change one coherent unit, check its exit condition, then advance. Review history should explain the result. Use a failing-before check where practical without forcing a broken main branch.
- **Build the lever.** When a script makes work repeatable or reviewable, do one unit to learn the recipe, then automate it. Validate the tool against that first unit and make reruns safe.

## Agent work

- **Guard context.** Read relevant sections, retain compact decisions, and keep large evidence in referenced artifacts. Delegate bulk only when delegation is permitted and actually helps.
- **Avoid unnecessary blocking.** Execute authorized reversible work. Ask for product intent that cannot be observed. An experiment can settle a factual question; it cannot grant permission.
- **Encode lessons.** Prefer eliminating a recurring mistake through ownership, types, lint, or a test. Use written guidance for judgments that cannot be enforced. Remove obsolete instructions after the structural fix.
