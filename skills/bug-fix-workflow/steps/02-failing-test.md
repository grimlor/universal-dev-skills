# Phase 2 -- Failing Test

**Purpose:** Encode the reproduction steps as a BDD test that fails because of the bug. This test is the acceptance criterion for the fix and the permanent regression guard.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started bug-fix-workflow 2 "Failing Test"
```

---

## Iron Law

1. **Run the test and confirm it fails before proceeding.** A test written and fixed in the same motion may never have caught the bug. The failing run must be observed -- not assumed.

---

## Test Structure

Write the test following the `bdd-testing` skill conventions. The test class encodes the bug as a behavioral requirement:

- **REQUIREMENT** -- the behavior the system must exhibit (the correct behavior, not the buggy one)
- **WHO** -- the caller or consumer affected by the defect
- **WHAT** -- one clause: the system behaves correctly under the conditions that triggered the bug
- **WHY** -- what breaks downstream when this behavior is wrong
- **MOCK BOUNDARY** -- at the I/O boundary as always; not at internal code

The test method encodes the reproduction scenario directly:

- **Given** -- the system state and inputs from Phase 1
- **When** -- the triggering action from Phase 1
- **Then** -- the correct behavior from Phase 1 (what should happen, not what does happen)

The assertion tests for correct behavior. The test fails because the system currently produces incorrect behavior -- that is the expected and correct state at this point.

## Confirm Failure

Run the test. It must fail. Observe the failure output and confirm:

- It fails for the right reason -- the assertion on correct behavior fails because the system produces the bug behavior, not because of a setup error, import error, or test authoring mistake
- The failure message is diagnostic -- it shows what was expected vs. what was received

If the test passes: the behavior may already be correct (the bug was fixed elsewhere, or the reproduction steps don't match the actual defect). Surface this to the user before continuing.

If the test fails for the wrong reason (setup error, wrong mock boundary, authoring mistake): fix the test until it fails for the right reason. Do not proceed to Phase 3 until the failure is meaningful.

## Plan Update

Check off "Failing test written and confirmed" under Phase 2. Append a session log entry noting the test class and method name and the observed failure.

## Proceed

Load `steps/03-root-cause.md` and begin Phase 3.

```bash
~/.agents/bin/emit-telemetry compliance.check bug-fix-workflow 2 "Failing Test" test_fails_for_right_reason pass "Test confirmed failing for the right reason; failure message is diagnostic."
~/.agents/bin/emit-telemetry phase.completed bug-fix-workflow 2 "Failing Test" success "Failing test written and confirmed; regression guard in place."
```
