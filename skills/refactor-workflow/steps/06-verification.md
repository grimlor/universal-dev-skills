# Phase 6 -- Verification

**Purpose:** Confirm the full suite is green, coverage is confirmed, the plan is closed, and the commit is clean.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started refactor-workflow 6 "Verification"
```

---

## Full Check

Run the full pre-commit gate. The canonical command is:

```bash
uv run task check
```

This runs `format`, `lint`, `type` (full project), and `test` in sequence. All must pass. If the project uses `task cov` in place of `task test`, substitute accordingly — check `pyproject.toml` for the project's task definitions.

**Do not substitute individual file-scoped commands for `task check`.** File-scoped type checking passes when full project analysis does not, because type errors can only manifest when pyright resolves the complete import graph. `task check` is the only valid pre-commit gate.

If any step fails: fix the issue and re-run `task check` in full before proceeding. Do not commit with a partial pass.

## Coverage

If the project uses `task cov` as the test step (i.e., `task check` was run with coverage), confirm 100% statement and branch coverage on modified production files. Apply the coverage procedure from the `bdd-testing` skill:

- 100% is the only passing score
- Every uncovered line is an unspecified behavior -- write the spec or remove the code
- "Pre-existing" is not a disposition

If coverage reveals uncovered lines: return to Phase 3 (Spec Gate), add the missing scenario, then Phase 4 (Test Gate) to add the test, then return here.

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

Show the staged diff and proposed commit message to HITL and wait for explicit approval before executing the commit. Do not commit autonomously.

## Done

The refactor is closed when:

- `task check` passes in full (format, lint, full-project type check, tests)
- Coverage is 100% on modified files (if using `task cov`)
- Old interface is removed (if applicable)
- Plan is closed with session log entry
- Commit approved by HITL and executed

```bash
~/.agents/bin/emit-telemetry compliance.check refactor-workflow 6 "Verification" task_check_pass pass "task check: format, lint, type, test all passed."
~/.agents/bin/emit-telemetry compliance.check refactor-workflow 6 "Verification" coverage_100 pass "100% statement and branch coverage on modified files."
~/.agents/bin/emit-telemetry phase.completed refactor-workflow 6 "Verification" success "task check clean; coverage confirmed; old interface removed; plan closed; commit approved."
~/.agents/bin/emit-telemetry skill.completed refactor-workflow success "Refactor workflow complete. All phases passed."
```
