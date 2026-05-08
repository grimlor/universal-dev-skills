# Phase 5 -- Prerequisite Validation

**Purpose:** Validate external API assumptions before writing BDD tests against them. A spec built on a false premise produces tests that pass in isolation and fail in production.

---

## When This Phase Applies

If the spec depends on external API behavior -- SDK models, REST endpoints, third-party service capabilities -- validate those assumptions now. Any behavior that assumes a specific external API response, data shape, or capability is a premise that can be wrong.

## When This Phase Does Not Apply

If the feature has no external dependencies (pure domain logic, UI-only changes, internal restructuring), note "No external premises" in the plan and check off Phase 5 immediately. The phase heading still exists in the plan.

## Steps

1. Review the spec's MOCK BOUNDARY declarations and Scenarios. Identify every assumed external behavior.
2. For each assumption, write a narrow smoke test against the real dependency. This is NOT a BDD spec -- it is an integration test that calls the real service and asserts on the shape or behavior the spec assumes. Mark it with the project's integration test marker (e.g., `@pytest.mark.integration`, `describe.skip` for CI).
3. Run the smoke tests.
   - If all premises hold -- proceed to Phase 6.
   - If any premise fails -- stop. The spec is built on a false assumption. Return to Phase 2, update the spec to reflect reality, and get human review before continuing.
4. Update the plan: check off "Premises validated" under Phase 5. Note which dependencies were tested and any surprises discovered.

## Checkpoint

Update the plan and load Phase 6.
