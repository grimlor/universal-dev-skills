# Phase 3 -- Root Cause

**Purpose:** Identify why the bug exists, not just where it manifests. Determine whether the fix is minimal (targeted code change) or structural (requires refactor-workflow).

---

## Diagnosis Procedure

Using the failing test as the entry point, trace the defect:

1. Follow the call chain from the test's When step into the production code.
2. Identify the specific location where behavior diverges from intent -- the wrong value, missing guard, incorrect condition, or mishandled state.
3. Distinguish the manifestation site (where the symptom appears) from the root cause site (where the defect originates). These are often different locations.
4. Determine whether the root cause is a targeted defect or a structural problem.

## Targeted vs. Structural Determination

**Targeted defect** -- the root cause is a specific wrong value, missing guard, incorrect condition, or mishandled edge case. The fix is a change to one or a small number of lines without restructuring abstractions, interfaces, or caller relationships. Proceed to Phase 4 -- minimal fix path.

**Structural defect** -- the root cause is an abstraction problem: the bug exists because the wrong interface is in place, callers depend on the wrong thing, or the code cannot correctly handle the condition without restructuring. A targeted patch would suppress the symptom without addressing why the system is wrong-shaped. Proceed to Phase 4 -- structural fix path.

If the determination is unclear, surface it to the user with your analysis before proceeding. Do not guess.

## Present and Wait

Present the root cause analysis to the user:

- Root cause location (file, function, line range)
- Why the defect produces the observed behavior
- Determination: targeted or structural, with rationale

Wait for acknowledgment before loading Phase 4.

## Plan Update

Check off "Root cause identified" under Phase 3. Record the root cause location and determination in the plan. Append a session log entry.

## Proceed

Load `steps/04-fix.md` and begin Phase 4.
