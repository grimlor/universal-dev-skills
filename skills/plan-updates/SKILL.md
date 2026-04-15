---
name: plan-updates
description: "Progress tracking in project artifacts. Use after completing implementation work (Phase 9 of the feature workflow), at checkpoints during refactoring or audit passes, or when the user asks to update project status."
---

# Plan Updates -- Tracking Progress in Project Artifacts

## When This Skill Applies

After completing implementation work (Phase 9 of the feature workflow), at checkpoints
during refactoring, audit, or remediation passes, or whenever the user asks to update
project status. Also applies when reviewing what has been done vs. what remains.

---

## Locating or Creating the Tracking Document

Use this decision tree every time before updating progress:

1. **Is there an established plan document for this project?**
   Check `docs/`, the project root, and `.copilot/` for a Markdown file with
   checkbox lists organized by phase. If found, use it.

2. **Is this a feature or non-trivial change?**
   If yes and no plan doc exists, create one at `.copilot/plan.md` (git-ignored).
   Read the plan template from the `templates` skill (`references/plan.md`) and
   fill in the placeholders. Then apply the plan document rules below for ongoing
   changes.

3. **Is this a refactoring, audit, or remediation pass?**
   Create or update `.copilot/task.md` (git-ignored). Follow the task tracking
   format below. This file is the session state for the current pass -- update it
   at every checkpoint and re-read it when resuming after context loss.

`.copilot/` is git-ignored by convention. If the directory does not exist, create it
and add `.copilot/` to `.gitignore` before writing any files there.

---

## Plan Document Rules

**Preamble:**
- Goal must be a single paragraph, not a bullet list
- Context/Constraints captures decisions made during Phases 1–3 that future sessions
  need without re-reading the full spec
- Open Questions are removed or marked resolved as work progresses -- they must
  not linger silently

**Session Log:**

The Session Log section at the bottom of `plan.md` is an append-only, datestamped
record of handoff state. It answers: "Where did we stop, and what should happen next?"

Each entry has three fields: **Stopped after**, **Next action**, and **Decisions made**.
See the Session Log section in the `templates` skill (`references/plan.md`)
for the exact format.

**Rules:**
- Append a new entry at the end of every session that advances the plan -- do not
  skip this when context is running low
- Never edit or delete previous entries
- "Next action" must be specific enough to resume without re-reading the full plan
  (e.g., "Write test class for validation behavior in spec §3.2", not "Continue work")
- "Decisions made" captures choices that are not in the spec but affect implementation
  (e.g., "Chose to use factory pattern for builder initialization" or "None")
- When resuming after a context reset, re-read the plan from the top -- Goal and
  Context establish the big picture, the phase checklist shows progress, the last
  Session Log entry tells you exactly where to pick up

---

## Artifacts to Update

### 1. Project Plan (feature work)

**Location:** `.copilot/plan.md`, or an existing plan document found in `docs/` or
the project root.

Each phase has a heading like `### Phase N -- Description` followed by checkboxes:

```markdown
### Phase 4c -- Operational Resilience
- [x] File logging -- persist logs alongside stderr output
- [x] Throttle detection -- recognize rate limiting signals
- [ ] Some future item not yet implemented
```

**Rules:**
- Check off items (`- [x]`) only when implementation is complete AND tests pass
- Add new line items when scope expands during implementation
- Append the phase marker (e.g., `✅`) to the phase heading when all items are checked
- If a new phase is needed, follow the existing naming convention (`Phase Na`, `Phase Nb`, etc.)
- Include the BDD spec file and test count when checking off test-related items
  (e.g., `BDD specs: test_validation.py (18 tests), test_processing.py (12 tests)`)
- Brief descriptions should explain WHAT was built and WHERE in the codebase

### 2. Task Tracking (refactoring, audit, and remediation passes)

**Location:** `.copilot/task.md`

For work that touches existing test or source files rather than adding new features,
track progress at the **test class** level -- not the file level. Files are too large
to be a meaningful completion unit; a class maps to one REQUIREMENT and can be
completed without context pressure building mid-work.

Group classes by file for orientation, but make each class its own checkable item.
Record findings inline so that context can be restored from this file alone:

```markdown
# Task -- BDD Test Remediation

## Goal
Audit all test files against the current bdd-testing skill. Fix violations in place.

## Status
Started: 2026-01-15

## Files

### tools/code_review/prescriptive_io_test.py
- [x] TestPrescriptiveIOParsing -- WHAT enumeration added; Given elision fixed in 3 methods
- [x] TestPrescriptiveIOValidation -- clean
- [ ] TestPrescriptiveIOErrorHandling
- [ ] TestPrescriptiveIOFormatting

### tools/code_review/static_analysis_test.py
- [ ] TestStaticAnalysisSignals
- [ ] TestStaticAnalysisThresholds
```

**Rules:**
- Update this file at the end of every test class, not just at the end of every file
- Record a one-line finding per class: either "clean" or a brief description of what was fixed
- When resuming after a context reset, re-read this file first to establish where work left off
- Do not mark a class complete until all violations are fixed and the class compiles

### 3. BDD Specifications

**Location:** The project's BDD specifications document -- a canonical listing of all
behavioral contracts. Look for it alongside the project plan, or in a `specs/` or
`tests/` directory.

The BDD Specifications document contains `TestClass` definitions with method signatures
(no bodies -- just `...`).

**Rules:**
- Add new spec classes during Phase 2 (Spec Gate) of the feature workflow
- If implementation reveals requirements not in the spec, add them here
- Keep the document in sync with actual test files -- if a test class exists in code,
  its spec should exist here
- Follow the existing format: class docstring with REQUIREMENT/WHO/WHAT/WHY,
  then method signatures with `...` bodies
- Group specs under the appropriate section heading for the project's structure

---

## When NOT to Update

- Do not update plan status for work that is still in progress
- Do not check off items speculatively ("this should work")
- Do not modify the plan structure (section ordering, narrative text) unless asked
- Do not update the plan for trivial changes that don't correspond to plan items

---

## Update Workflow

1. Locate or create the tracking document using the decision tree above
2. Identify which items were completed
3. Verify correctness before checking off items (tests pass, no violations remain)
4. Check off completed items with a one-line finding
5. Add any new items discovered during the work
6. Update BDD Specifications if specs were added or modified
7. Briefly confirm to the user what was updated
