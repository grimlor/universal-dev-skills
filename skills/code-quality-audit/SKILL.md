---
name: code-quality-audit
description: "Systematic audit of code against structural quality rules -- mock boundaries, test-only API pollution, suppression pragmas, and BDD conventions. Use when auditing a codebase or set of files for quality violations, during Phase 1.5 of the feature workflow, or as a standalone quality review task."
---

# Code Quality Audit -- Structural Inspection Procedure

## When This Skill Applies

- **During Phase 1.5 of the feature workflow** -- scoped to the files the spec
  identifies for modification.
- **As a standalone task** -- when the user requests a quality audit, code review,
  or codebase health check.
- **During remediation passes** -- when working through findings from a prior audit.

This skill defines the **procedure** for conducting an audit. The **rules** being
audited against live in other skills:

| Rule source | What it defines |
|---|---|
| `bdd-testing` | Mock boundary discipline, BDD conventions, coverage requirements |
| `code-quality-antipatterns` | Suppression pragma policy, test-only API pollution |
| Language-specific standards | Lint, type-check, and formatting rules |

Read those skills before auditing. This skill tells you *how to inspect*; they
tell you *what to inspect for*.

---

## Audit Scope

### Feature workflow (Phase 1.5)

Scope the audit to **existing files** that the spec indicates will be modified.
New files created by the feature are exempt -- they will be written to standard
from the start.

### Standalone audit

Scope is determined by the user's request. Default to the full source and test
trees unless the user narrows it.

---

## Procedure

### Step 1 -- Mechanical Checks

Run the project's configured lint and type-check toolchain on the scoped files.
These are the same checks as Phase 1.5's original scope:

- Lint errors (Ruff, ESLint, Checkstyle, Roslyn analyzers)
- Type errors (Pyright, TypeScript compiler, javac, C# compiler)
- Formatting drift (if the project enforces a formatter)

Record all findings. These are the easy wins -- tools catch them automatically.

### Step 2 -- Mock Boundary Audit

For each test file in scope, check whether mocks target I/O boundaries or
internal code:

| Finding type | Rule reference |
|---|---|
| Patching a private attribute of our own class | `bdd-testing` → Mock boundary |
| `patch.object(OurClass, "our_method")` | `bdd-testing` → Mock boundary |
| `monkeypatch.setattr(OurClass, "our_method")` | `bdd-testing` → Mock boundary |
| `patch("our_module.our_function")` | `bdd-testing` → Mock boundary |

For each violation, record:

1. **File and line(s)**
2. **What it accomplishes** -- the test intent the mock serves
3. **Why it violates** -- which boundary rule it breaks
4. **The alternative** -- how to achieve the same test intent by mocking at the
   actual I/O boundary

### Step 3 -- Test-Only Production API Audit

For each production file in scope, look for symbols that have **zero production
callers** but are used by tests:

- Parameters with test-only defaults (default `None`, only tests pass non-`None`)
- Properties that expose internal state for test assertions
- Context managers or methods that exist solely for test setup/teardown
- Factory methods whose only consumers are test fixtures

For each finding, record:

1. **Symbol name, file, and line**
2. **Production callers** (should be zero -- verify with usage search)
3. **Test callers** (list the test files and approximate count)
4. **What it accomplishes** -- the test need it serves
5. **Why it violates** -- `code-quality-antipatterns` §6 (test-only production APIs)
6. **The alternative** -- how tests can achieve the same goal using only the
   public API and I/O boundary mocks

### Step 4 -- Suppression Pragma Audit

Scan the scoped files for all suppression pragmas:

| Category | Patterns to search |
|---|---|
| Coverage | `pragma: no cover`, `istanbul ignore`, `ExcludeFromCodeCoverage` |
| Type checking | `type: ignore`, `pyright: ignore`, `ts-ignore`, `ts-expect-error`, `ts-nocheck` |
| Linting | `noqa`, `eslint-disable`, `pragma warning disable`, `SuppressWarnings`, `noinspection` |

For each suppression found, classify it:

- **Removable** -- a real fix exists (type narrowing, stub file, code restructuring).
  Record the fix.
- **External** -- caused by a third-party library's missing stubs. Record whether
  local stubs could replace it.
- **Justified** -- genuinely unavoidable, has an explanation comment, and is narrowly
  scoped. Record as "no action needed" with the justification.

### Step 5 -- BDD Convention Audit

For each test file in scope, check compliance with BDD conventions from the
`bdd-testing` skill:

- **Class-level docstrings** -- REQUIREMENT / WHO / WHAT / WHY present and meaningful
- **Method-level docstrings** -- Given / When / Then in title-case (not ALL-CAPS)
- **Method body comments** -- `# Given`, `# When`, `# Then` structuring the test body
- **Test organization** -- grouped by consumer requirement, not by code structure
- **Assertion quality** -- no bare assertions without context; no tautology tests

---

## Output Format

The audit produces a findings document organized by category. Each finding must
include:

1. **The violation** -- what the code does and where
2. **What it accomplishes** -- the intent behind the code (charitable reading)
3. **The recommended alternative** -- how to achieve the same intent correctly

### Document Structure

```markdown
# Code Quality Audit

> Scope: <files or directories audited>
> Audit date: <date>
> Rules applied: bdd-testing, code-quality-antipatterns, <language>-code-standards

---

## 1. Mock Boundary Violations
### 1a. <Pattern Name>
| File | Lines | Count |
|------|-------|-------|
| ... | ... | ... |
**What it accomplishes:** ...
**Why it violates:** ...
**Alternative:** ...

## 2. Test-Only Production API Pollution
### 2a. <Symbol Name>
| Location | File | Line |
|----------|------|------|
| ... | ... | ... |
**What it accomplishes:** ...
**Why it violates:** ...
**Alternative:** ...

## 3. Suppression Pragma Violations
### 3a. Removable Suppressions -- <category>
### 3b. External Library Stub Gaps
### 3c. Justified Suppressions (No Action Required)

## 4. BDD Convention Violations

## Summary
| Category | Count | Severity | Effort |
|----------|-------|----------|--------|
| ... | ... | ... | ... |
```

### Severity Classification

| Severity | Meaning |
|---|---|
| **Critical** | Violates a core testing principle (mock boundary, coverage). Tests may pass but prove nothing. |
| **High** | Pollutes the production API or hides real diagnostics. Requires test rewrites. |
| **Medium** | Avoidable suppressions. Real fix exists but requires moderate effort. |
| **Low** | Convention or style issues. Mechanical fix, no logic changes. |

### Effort Classification

| Effort | Meaning |
|---|---|
| **High** | Requires rethinking test setup patterns across many files. |
| **Medium** | Targeted changes to specific files or classes. |
| **Low** | Find-and-replace or single-function changes. |

---

## Tracking Remediation

When remediating audit findings, track progress in `.copilot/CODE_QUALITY_AUDIT.md`
(or the location where the audit document was written). Use the task tracking
format from the `plan-updates` skill:

```markdown
## Remediation Progress

### Mock Boundary Violations
- [x] 1a. Direct `embedder._client` assignment -- patched at ollama.AsyncClient boundary
- [ ] 1b. `patch.object(embedder, "_client")` -- 20 instances in test_embedder.py
- [ ] 1c. `patch.object(PipelineRunner, "run")` -- extract pure functions
```

Update at each checkpoint to maintain resumability across sessions.

---

## Relationship to Other Skills

- **`feature-workflow`** Phase 1.5 invokes this skill's procedure (Steps 1–5)
  scoped to files identified by the spec.
- **`bdd-testing`** provides the mock boundary and BDD convention rules
  audited in Steps 2 and 5.
- **`code-quality-antipatterns`** provides the suppression pragma and test-only
  API rules audited in Steps 3 and 4.
- **`plan-updates`** provides the tracking format used during remediation.
- **Language-specific standards** provide the lint/type-check rules for Step 1.
