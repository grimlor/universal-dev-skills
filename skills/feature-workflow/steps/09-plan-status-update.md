# Phase 9 -- Plan Status Update

**Purpose:** Close the plan, record what was done, and leave the project in a state that survives a context reset.

---

## Steps

1. Update the project's plan document -- check off all completed items. If scope expanded during implementation, add the new items before checking them off so the record is accurate.
2. Update BDD Specifications if any specs were added or modified during Phase 7 discoveries.
3. Append a session log entry -- record the stopping point, next action, and any decisions made. The session log entry must be specific enough to resume without re-reading the full plan. See the `plan-updates` skill for the session log format.

## Done

The feature is closed when:

- All tests pass
- Coverage is 100% on modified and new files
- Plan is fully checked off with session log entry
- Commit is clean and conventionally formatted per `conventional-commits`

## If Work Is Incomplete

If the session ends before the feature is fully done, the session log entry is still required. Record exactly where work stopped, what the next action is, and any open decisions. An incomplete plan with a clear session log is recoverable; an incomplete plan without one is not.
