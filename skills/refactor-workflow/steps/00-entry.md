# Phase 0 -- Entry

**Purpose:** Establish scope, verify environment, locate or create the plan.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started refactor-workflow 0 "Entry"
```

---

## Pre-flight

1. Verify git repo is present and on the expected branch for this refactor.
2. Verify the target interface or module being refactored is identifiable -- name it explicitly before proceeding.
3. Verify the existing test suite is passing at baseline. If it is not, stop: do not begin a refactor against a broken baseline. Surface the failures to the user and wait for resolution.

## Scope Statement

Produce a one-paragraph scope statement covering:

- **Target:** what interface, class, module, or abstraction is being restructured
- **Goal:** what structural property the refactor achieves (e.g., "extract EmbedderPort as a Protocol so callers depend on the abstraction, not the concrete implementation")
- **Not in scope:** what will NOT change as part of this refactor

Present the scope statement to the user and wait for acknowledgment before proceeding to Phase 1.

## Plan

Locate or create `.copilot/plan.md` using the `plan-updates` skill decision table. If creating a new plan, read the plan template from the `templates` skill (`references/plan.md`) and populate:

- **Goal:** the scope statement from above
- **Context/Constraints:** known constraints (e.g., existing test suite must remain green; no new behavior; prerequisite tasks if any)
- **Open Questions:** anything unresolved before Phase 1 can begin

Check off "Entry complete" under Phase 0 and append a session log entry.

## Proceed

Load `steps/01-caller-enumeration.md` and begin Phase 1.

```bash
~/.agents/bin/emit-telemetry compliance.check refactor-workflow 0 "Entry" baseline_suite_passing pass "Existing test suite passing at baseline before refactor begins."
~/.agents/bin/emit-telemetry phase.completed refactor-workflow 0 "Entry" success "Scope defined, baseline verified, plan initialized."
```
