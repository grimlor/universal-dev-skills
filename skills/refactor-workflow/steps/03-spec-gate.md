# Phase 3 -- Spec Gate

**Purpose:** Audit the existing test suite for BDD correctness, then analyze what needs to change to support the refactoring. The behavioral specification does not change -- the goal is to document how the mock boundary and fixture setup must adapt to the new interface.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started refactor-workflow 3 "Spec Gate"
```

---

## Iron Laws

1. **Audit before analysis.** Do not proceed to the adaptation analysis on tests that fail the BDD audit. Wrong-shaped tests adapted to a new interface are still wrong-shaped. Remediate first.
2. **Retreat to design when the analysis reveals gaps.** If analysis reveals that the design (Phase 2) does not specify how a particular behavior maps to the new interface, stop. Do not invent a mapping. Return to `steps/02-design.md`, update the design note with the gap and its resolution, then return here and continue. This iteration is expected.
3. **Behavioral claims do not change.** WHAT and WHY clauses in existing test classes describe behavior the system makes to its consumers. If you find yourself needing to rewrite them, you have found a behavioral change, not a structural one. Stop and surface it to the user -- this is a scope signal, not a spec update.

---

## Step 1 -- BDD Audit

For each test class in the existing suite that exercises code touched by this refactor, verify against the `bdd-testing` skill:

1. **Mock boundary is at the I/O boundary.** No mocking of internal code -- functions and classes that live in the codebase are not mocked. Mocks sit only at process boundaries, HTTP clients, database wire calls, process-level state.
2. **No assertions on mock internals.** No `assert_called_with`, `call_args`, call counts, or any assertion that would fail if the mock were swapped for a conforming real implementation.
3. **Three-part contract present.** Each class has REQUIREMENT/WHO/WHAT/WHY + MOCK BOUNDARY. Each test method has a Given/When/Then docstring and `# Given/# When/# Then` body comments.
4. **Assertions include diagnostic messages.** Bare asserts are a violation.
5. **WHAT count matches test count.** Every WHAT clause has exactly one implementing test method; every test method traces to exactly one WHAT clause.

### If Violations Are Found

Wrong-shaped tests are a prerequisite issue -- the same discipline as Phase 0's quality baseline, applied to the test layer. Do not proceed to Step 2 until violations are remediated:

1. Surface the violations to the user with a summary: which classes, which rules violated.
2. Remediate the violations per the `bdd-testing` and `code-quality-audit` skills.
3. Confirm the full suite still passes after remediation.
4. Then proceed to Step 2.

## Step 2 -- Adaptation Analysis

For each test class that passed the audit and exercises code touched by this refactor:

1. **Identify the current mock boundary.** Where does this test class mock? What concrete type or interface is being substituted?
2. **Identify the new mock boundary.** After the refactor, where should the mock boundary be? What new Protocol, port, or adapter shape does the fake need to conform to?
3. **Identify fixture changes.** What new fakes need to be created? What existing fixtures need to be updated to conform to the new interface?
4. **Check behavioral assertions.** Do the WHAT clauses and assertion bodies remain valid under the new interface? If yes -- they are untouched. If no -- stop and evaluate: this is a scope signal (Iron Law 3).
5. **Check for new failure modes.** Does the new interface expose failure modes the old interface could not produce? For example: a Protocol method that can return None where the concrete implementation always returned a value; a new boundary that can raise where the old one swallowed errors. These are the only legitimate source of new test methods in a refactor.

## Output

Produce a test adaptation plan using the `templates` skill (`references/refactor-adaptation-plan.md`). Read the template directly -- do not reproduce from memory. The plan documents, for each affected test class:

- Audit result (pass / remediated, with notes if remediated)
- Current mock boundary → new mock boundary
- Fixture changes: fakes to create or update with the new interface they must conform to
- Behavioral assertions: unchanged / needs wording update (rare) / new failure mode (exception case)
- New test methods needed for newly exposed failure modes, with their Given/When/Then scenario

Present the completed plan to the user and wait for acknowledgment before proceeding.

## Plan Update

Check off "Spec gate complete" under Phase 3. Append a session log entry noting the test class count, any audit violations found and remediated, boundary changes identified, and any design gaps that triggered a Phase 2 retreat.

## Proceed

Load `steps/04-test-gate.md` and begin Phase 4.

```bash
~/.agents/bin/emit-telemetry compliance.check refactor-workflow 3 "Spec Gate" bdd_audit_clean pass "All test classes passed BDD audit or were remediated before adaptation analysis."
~/.agents/bin/emit-telemetry phase.completed refactor-workflow 3 "Spec Gate" success "BDD audit complete; adaptation plan produced and user-reviewed."
```
