# Phase 8 -- Coverage Verification

**Purpose:** Confirm every line of production code has a specification justifying its existence. 100% coverage is proof of specification completeness, not a vanity metric.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started feature-workflow 8 "Coverage Verification"
```

---

## Steps

1. Run tests with coverage for the project's source package (see the language-specific standards skill for the exact command).
2. If 100% statement AND branch coverage -- report results, update the plan, and proceed to Phase 9.
3. If below 100% -- this is a blocking failure. Do not summarize and move on. For each uncovered line or partial branch:
    a. Identify the disposition: **write the spec** (real requirement the spec missed) or **remove the code** (dead code or over-engineering).
    b. Implement the disposition immediately.
    c. Re-run coverage. Repeat until 100% is achieved.

## Valid Dispositions

There are exactly two:

- **Real requirement** -- write the spec (return to Phase 6, add the test, return here).
- **Dead code or over-engineering** -- remove it.

"Pre-existing" is not a disposition. "Low priority" is not a disposition. "It was already there" is not a disposition. Whether a line existed before your changes is irrelevant -- if it is uncovered after your work, it is uncovered.

## What Surfaces at Coverage Time

Three categories routinely appear only at coverage time:

| Category | Description | Example |
| --- | --- | --- |
| Defensive guard code | Protects against misuse -- empty input, wrong types, boundary values | `if not text.strip(): raise ValidationError(...)` |
| Graceful degradation | Soft failures the system absorbs rather than raising | Missing collection returns empty list, not error |
| Conditional formatting | Display logic that varies by state | Warning line only appears when `is_flagged=True` |

## Checkpoint

Report final coverage results to the user. Load Phase 9.

```bash
~/.agents/bin/emit-telemetry compliance.check feature-workflow 8 "Coverage Verification" coverage_100 pass "100% statement and branch coverage confirmed."
~/.agents/bin/emit-telemetry phase.completed feature-workflow 8 "Coverage Verification" success "100% coverage achieved; all uncovered lines dispositioned."
```
