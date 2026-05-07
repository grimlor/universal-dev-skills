# Phase 4 -- Test Gate

**Purpose:** Write tests from the spec. Tests use fakes at the new interface boundary and assert on observable outputs only. Tests will fail at this point -- that is correct.

---

## Test File

Create the test file following the `bdd-testing` skill conventions. Group classes by consumer requirement, not by the internal module being refactored.

## Fakes at the Target Boundary

Tests are written against fakes that implement the target interface (the new Protocol, ABC, or adapter shape from Phase 2). The fakes are not the old concrete implementations -- they are purpose-built test doubles that conform to the new interface.

Fake design requirements:

- Conform to the target interface exactly (same method signatures, same return type shapes)
- Return configurable values so tests can exercise different scenarios
- Raise on demand so failure-mode scenarios can be tested
- Contain no production logic -- they are scaffolding, not implementations

## Outcome-Equivalence Check

Before writing each assertion, ask: _"If I swapped in the real implementation at this boundary, would this assertion still pass?"_

If the answer is no -- the assertion is on mock internals (`assert_called_with`, `call_args`, call counts) rather than on observable outputs. Rewrite it to assert on what the system returns, what state changes, or what error is raised.

See the `bdd-testing` skill, I/O Boundary section, for the substitution failure definition and examples.

## Expected Failure

Run the tests after writing them. They should fail because the production code still uses the old interface. If they pass:

- The test is a tautology (it would pass without any real implementation)
- The behavior already exists under the new interface (no implementation needed for this scenario -- note it and move on)

A passing test that is neither a tautology nor evidence of existing behavior is a red flag. Stop and investigate before proceeding.

## Plan Update

Check off "Test gate complete" under Phase 4. Record the test count per class. Append a session log entry.

## Proceed

Load `steps/05-implementation.md` and begin Phase 5.
