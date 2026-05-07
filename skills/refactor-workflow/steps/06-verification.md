# Phase 6 -- Verification

**Purpose:** Confirm the full suite is green, coverage is confirmed, the plan is closed, and the commit is clean.

---

## Full Suite

Run the complete test suite -- both the new refactor tests and the full pre-existing suite. Both must pass. Partial passage (new tests green, existing suite broken) is not done.

If the existing suite is broken: return to Phase 5 and diagnose before continuing here.

## Coverage

Run coverage on the production files modified by the refactor. Apply the coverage procedure from the `bdd-testing` skill:

- 100% statement and branch coverage is the only passing score
- Every uncovered line is an unspecified behavior -- write the spec or remove the code
- "Pre-existing" is not a disposition

If coverage reveals uncovered lines in the new interface code: return to Phase 3 (Spec Gate), add the missing scenario, then Phase 4 (Test Gate) to add the test, then return here.

## Old Interface Cleanup

If the refactor replaces an old interface rather than extending alongside it, confirm that the old interface is fully removed:

- No references to the old class, method signatures, or abstraction remain in production code
- Any old test fixtures or helpers that depended on the old interface are removed or updated
- The plan's caller enumeration table is fully checked off

## Plan Closure

- Check off all remaining plan items
- Mark the refactor phase heading with the completion marker
- Append a final session log entry: what was completed, any follow-up features or prerequisite tasks identified, next action if work continues

## Commit

Follow the `conventional-commits` skill for commit message format. The commit for a refactor typically uses `refactor:` as the type. If a prerequisite cleanup task was committed separately earlier, this commit covers only the main refactor.

## Done

The refactor is closed when:

- Full suite passes (new + pre-existing)
- Coverage is 100% on modified files
- Old interface is removed (if applicable)
- Plan is closed with session log entry
- Commit is clean and conventionally formatted
