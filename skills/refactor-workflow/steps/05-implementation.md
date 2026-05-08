# Phase 5 -- Implementation

**Purpose:** Adapt production code to the new interface. Work through callers in enumeration order. After each caller: new tests pass, existing suite still passes.

---

## Iron Law

1. **The existing suite is the regression gate.** After each caller is adapted, both the new tests and the full pre-existing test suite must pass. New tests alone do not prove behavior is preserved. If the existing suite breaks, stop -- do not move to the next caller until the regression is diagnosed and resolved.

---

## Ordering

Work through the adapter map from Phase 2 in dependency order. If a decomposition was produced in Phase 1 (volume exceeded single-pass scope), work within the current sub-task's scope only.

Complete each caller fully before moving to the next. Partial adaptation across multiple callers simultaneously increases the window during which the codebase is incoherent.

## Per-Caller Procedure

For each caller in the enumeration:

1. Read the adapter map entry for this caller (Phase 2 design note).
2. Adapt the caller to use the new interface.
3. Run the new tests -- they should now pass for this caller's scenarios.
4. Run the full pre-existing test suite -- it must continue to pass. If it breaks, stop. Diagnose the regression before continuing. Iron Law 1 above.
5. Check off this caller in the plan.

## Volume Discovery During Implementation

If a caller turns out to require substantially more adaptation than the Phase 1 estimate indicated, surface the discovery, propose a decomposition or revised sequencing, and wait for acknowledgment before continuing. Do not silently absorb scope growth. Iron Law 3 from SKILL.md applies.

## No New Behavior

If adaptation of a caller surfaces a genuine new requirement (something the existing system does not do and the refactor spec does not cover), do not implement it. Record it in the plan's Open Questions or as a follow-up feature. Iron Law 2 from SKILL.md applies.

## Plan Update

After each caller is adapted and verified: check it off in the plan. Append a session log entry at natural stopping points (end of session, end of a sub-task group) with next action specific enough to resume without re-reading the full plan.

## Proceed

Load `steps/06-verification.md` and begin Phase 6 when all callers in scope are adapted.
