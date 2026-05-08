# Phase 6 -- BDD Test Specification

**Purpose:** Write tests from the spec. Tests must fail before implementation begins. Failing tests are the specification -- passing tests before implementation are either tautologies or evidence the behavior already exists.

---

## Steps

1. Create test classes from the spec (Phase 2), informed by the architecture (Phase 3). Follow the `bdd-testing` skill for all conventions -- class structure, REQUIREMENT/WHO/WHAT/WHY, MOCK BOUNDARY, three-part contract per method, assertion quality.
2. Include failure-mode specs. An unspecified failure is an unhandled failure. Test error paths, edge cases, and boundary conditions.
3. Run the tests and confirm they fail. If a test passes before implementation:
   - **Tautology:** the test would pass without any real implementation. Rewrite it to assert on actual system behavior.
   - **Behavior already exists:** the system already satisfies this requirement. Note it in the plan as already green; proceed to Phase 8 for coverage verification on that behavior.
   - Any other passing test is a red flag -- stop and investigate before proceeding.

## BDD Ordering Is Recursive

If implementation will be broken into sub-tasks (A, B, C within Phase 7), the BDD constraint applies at every level. Test specs for each sub-task must exist and fail before that sub-task's implementation begins. Sub-tasks do not get a free pass on ordering because their parent is Phase 7.

## Checkpoint

Present the test file to the user. Confirm tests are failing. Wait for acknowledgment before loading Phase 7.
