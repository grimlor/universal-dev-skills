# Phase 4 -- Fix

**Purpose:** Apply the fix determined by root cause analysis. Two paths: minimal fix (stays in this workflow) or structural fix (transitions to refactor-workflow on the same branch).

---

## Path A -- Minimal Fix

Root cause is a targeted defect. Apply the smallest change that makes the failing test pass without restructuring abstractions or caller relationships.

### Iron Laws

1. **Change only what the root cause identifies.** No opportunistic refactoring, no cleanup, no "while I'm here" changes. If structural problems are noticed, record them in the plan as follow-up refactor-workflow work.
2. **The fix must not suppress the symptom.** If the change makes the test pass by catching and swallowing the error rather than correcting the behavior, it is a symptom fix, not a root cause fix. Identify and apply the correct change.

### Steps

1. Apply the targeted change at the root cause site.
2. Run the failing test -- it must now pass.
3. Run the full pre-existing test suite -- it must continue to pass.
4. If any existing test breaks: stop. The fix introduced a regression. Diagnose before continuing.
5. Load `steps/05-verification.md` and proceed to Phase 5.

---

## Path B -- Structural Fix

Root cause is a structural defect. A targeted patch would suppress the symptom without correcting the underlying abstraction problem.

### Steps

1. The failing test from Phase 2 remains on the branch in its failing state. It is the acceptance criterion -- the branch is not a merge candidate until it passes. No skip marker is needed; the branch does not enter a PR queue until the work is complete.
2. Transition to `refactor-workflow` on this same branch. The failing test travels with the branch and serves as the acceptance criterion throughout the refactor.
3. Run refactor-workflow from Phase 0 (pre-flight and scope) through Phase 6 (verification). The refactor's scope is the structural change the root cause requires.
4. At refactor-workflow Phase 3 (Spec Gate), the failing test is the first input to the BDD audit. It should be correctly shaped from Phase 2 -- if the audit finds violations, remediate before the adaptation analysis.
5. The refactor is complete when the failing test passes alongside the full suite. This is the verification that the bug is fixed. The branch becomes a PR candidate at that point.
6. bug-fix-workflow Phase 5 is superseded by refactor-workflow Phase 6 -- no separate verification step is needed.
