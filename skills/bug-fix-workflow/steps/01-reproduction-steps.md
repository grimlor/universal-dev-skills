# Phase 1 -- Reproduction Steps

**Purpose:** Gather a structured account of the bug from the user and translate it into a Given/When/Then scenario that can be directly encoded as a failing test.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started bug-fix-workflow 1 "Reproduction Steps"
```

---

## Intake

Ask the user for:

1. **What they did** -- the specific action, input, or condition that triggered the bug. Be precise: not "I ran the indexer" but "I called `indexer.index(documents=[])` with an empty list."
2. **What they expected** -- the intended behavior under those conditions.
3. **What actually happened** -- the observed behavior: wrong output, exception, silent failure, data corruption.
4. **Frequency and conditions** -- does it always happen? Only under specific conditions? First occurrence or recurring?

If the user's account is imprecise, ask clarifying questions. Do not proceed to Phase 2 with a vague scenario -- the test can only be as specific as the reproduction steps.

## Translate to Given/When/Then

Restate the reproduction steps as a Given/When/Then scenario:

- **Given** -- the system state and inputs that set up the bug condition
- **When** -- the specific action that triggers the defective behavior
- **Then** -- what the system should do (correct behavior), which is the opposite of what it currently does

Present the scenario to the user. Confirm it accurately captures the bug before proceeding.

## Plan

Locate or create the plan document using the `plan-updates` skill decision table. If creating a new plan, read the plan template from the `templates` skill (`references/plan.md`) directly. Populate:

- **Goal** -- fix the defect described by the reproduction scenario
- **Context/Constraints** -- the Given/When/Then scenario; any known constraints
- **Open Questions** -- anything unresolved

Check off "Reproduction steps captured" under Phase 1. Append a session log entry.

## Proceed

Load `steps/02-failing-test.md` and begin Phase 2.

```bash
~/.agents/bin/emit-telemetry phase.completed bug-fix-workflow 1 "Reproduction Steps" success "Reproduction scenario captured and confirmed with user."
```
