# Phase 4 -- Test Gate

**Purpose:** Implement the test adaptation plan from Phase 3. Adapt mock boundaries and fixture setup to the new interface. Leave behavioral assertions untouched. Add new tests only for failure modes identified in Phase 3.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started refactor-workflow 4 "Test Gate"
```

---

## Iron Law

1. **Adapt the boundary, not the behavior.** Mock setup and fixture construction change to conform to the new interface. Behavioral assertions -- what the system returns, what state changes, what error is raised -- are untouched. If an assertion needs rewording to make sense under the new interface, it is a scope signal: stop and surface it before continuing.

---

## Procedure

Work through the test adaptation plan from Phase 3 class by class:

1. **Create or update fakes** to conform to the new interface (new Protocol, port, or adapter shape). Fakes must: conform to the target interface exactly; return configurable values; raise on demand; contain no production logic.
2. **Update fixture setup** in each affected test class to use the new fakes and new mock boundary location.
3. **Leave behavioral assertions untouched.** The WHAT clauses, Given/When/Then scenarios, and assertion bodies do not change unless Phase 3 explicitly identified a wording update. Any impulse to rewrite an assertion is a scope signal -- stop and evaluate.
4. **Add new test methods** only for failure modes identified in Phase 3. Follow the `bdd-testing` skill three-part contract. These are the only net-new tests a refactor produces.

## Expected State After Adaptation

Adapted tests will fail at this point because production code still uses the old interface -- that is correct. If an adapted test passes before implementation:

- The behavioral assertion was so loose it passes against anything -- tighten it.
- The behavior already exists under the new interface -- note it and move on.

## Plan Update

Check off "Test gate complete" under Phase 4. Record the count of adapted classes and any new test methods added. Append a session log entry.

## Proceed

Load `steps/05-implementation.md` and begin Phase 5.

```bash
~/.agents/bin/emit-telemetry compliance.check refactor-workflow 4 "Test Gate" adapted_tests_failing pass "Adapted tests fail because production code still uses the old interface -- correct pre-implementation state."
~/.agents/bin/emit-telemetry phase.completed refactor-workflow 4 "Test Gate" success "Test adaptation complete; boundaries adapted; behavioral assertions untouched."
```
