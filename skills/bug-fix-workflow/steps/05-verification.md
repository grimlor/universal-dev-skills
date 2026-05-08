# Phase 5 -- Verification

**Purpose:** Confirm the fix is complete, the suite is fully green, and the plan is closed. This phase applies to Path A (minimal fix) only -- Path B is verified by refactor-workflow Phase 6.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started bug-fix-workflow 5 "Verification"
```

---

## Steps

1. **Full suite** -- run the complete test suite. Both the new regression test and the full pre-existing suite must pass. Partial passage is not done.
2. **Coverage** -- run coverage on the files modified by the fix. Apply the `bdd-testing` coverage procedure. If the fix introduced new production code paths (a new guard, a new branch), they must be covered. "The fix was small" is not a coverage exemption.
3. **Plan closure** -- check off all remaining plan items. Append a final session log entry: what was fixed, the regression test that guards it, any follow-up refactor-workflow work identified during Phase 4.

## Commit

Follow the `conventional-commits` skill. Bug fixes use the `fix:` type. The commit message body should reference the reproduction scenario and the regression test by name so the fix is traceable.

## Done

The fix is closed when:

- Failing test from Phase 2 now passes
- Full pre-existing suite passes
- Coverage holds on modified files
- Plan is closed with session log entry
- Commit is clean and conventionally formatted

```bash
~/.agents/bin/emit-telemetry compliance.check bug-fix-workflow 5 "Verification" full_suite_green pass "Regression test and full pre-existing suite both pass."
~/.agents/bin/emit-telemetry compliance.check bug-fix-workflow 5 "Verification" coverage_holds pass "Coverage maintained on modified files."
~/.agents/bin/emit-telemetry phase.completed bug-fix-workflow 5 "Verification" success "Fix verified; plan closed; commit complete."
~/.agents/bin/emit-telemetry skill.completed bug-fix-workflow success "Bug fix workflow complete. Failing test now passes; no regressions."
```
