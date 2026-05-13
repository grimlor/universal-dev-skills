---
name: plan-updates
description: "Progress tracking in project artifacts -- plan, task, and BDD spec documents. Use after completing each phase of any workflow (feature, refactor, bug-fix), at checkpoints during audit passes, when adding or updating behavioral specs, or when the user asks to update project status."
---

# Plan Updates -- Tracking Progress in Project Artifacts

## Iron Laws

1. **Locate before writing.** Use the decision table below to find or create the right tracking document; never improvise a new format.
2. **Check off only when complete.** It is not complete until the HITL approves the phase. Implementation done AND tests pass against the real implementation -- not against fakes or mocks of system-internal code. No speculative checkoffs.
3. **Append-only Session Log.** Never edit or delete previous entries.
4. **Update at every checkpoint** -- after each completed phase of `feature-workflow`, `refactor-workflow`, or `bug-fix-workflow`, and at the end of each test class for audit passes (not just at the end of each file).
5. **Don't restructure plans without being asked.** Section ordering and narrative text are off-limits unless the user requests changes.

## When This Skill Applies

After completing each phase of `feature-workflow`, `refactor-workflow`, or `bug-fix-workflow`, at checkpoints during audit/remediation passes, or whenever progress status needs updating.

## Locating the Tracking Document

All tracking artifacts live in `.copilot/` (git-ignored). The user moves artifacts elsewhere manually before committing if they choose to keep them.

| Situation | Document | Notes |
| --- | --- | --- |
| `.copilot/plan.md` already exists | Use it | Markdown with phase-grouped checkboxes |
| Feature / non-trivial change, no plan yet | Create `.copilot/plan.md` | Read template from `templates` skill (`references/plan.md`) |
| Bug fix | Create `.copilot/plan.md` | Simpler plan: reproduction → failing test → fix → verification |
| Refactoring pass | Create `.copilot/plan.md` | Multi-phase plan: entry → design → spec/test gate → implementation → verification |
| Audit / remediation pass | Create or update `.copilot/task.md` | Update at every class checkpoint |

If `.copilot/` does not exist, create it and add `.copilot/` to `.gitignore` before writing files there. Never write plan, task, or spec artifacts to `docs/`, the project root, `specs/`, or `tests/` -- if the user wants to promote an artifact, they will move it themselves.

## Artifact Rules

Structure for each artifact lives in the `templates` skill. The behavioral rules below govern how to _populate and update_ them.

### 1. Project Plan -- `.copilot/plan.md`

Template: `templates` skill, `references/plan.md`.

- Check off (`- [x]`) only when implementation is complete AND tests pass.
- Add new line items when scope expands during implementation.
- Append `✅` to the phase heading when all items in that phase are checked.
- Test-related items record the BDD spec file and test count (e.g., `BDD specs: test_validation.py (18 tests)`).
- Brief descriptions explain WHAT was built and WHERE in the codebase.
- Open Questions are removed or marked resolved as work progresses -- they must not linger silently.

**Session Log** (append-only, at the bottom of `plan.md`):

- Append a new entry every session that advances the plan -- do not skip when context is running low.
- Never edit or delete previous entries.
- "Next action" must be specific enough to resume without re-reading the full plan (e.g., "Write test class for validation behavior in spec §3.2", not "Continue work").
- "Decisions made" captures choices not in the spec but affecting implementation (e.g., "Chose factory pattern for builder initialization" or "None").
- On context reset: re-read the plan from the top -- Goal and Context establish the big picture, the phase checklist shows progress, the last Session Log entry tells you exactly where to pick up.

### 2. Task Tracking -- `.copilot/task.md`

Template: `templates` skill, `references/task.md`.

- Track progress at the **class** (or equivalent REQUIREMENT-sized) level, not the file level.
- Update at the end of every class, not just every file.
- One-line finding per item: "clean" or a brief description of what was fixed.
- Do not mark an item complete until all violations are fixed and the unit compiles.
- On context reset, re-read this file first to establish where work left off.

### 3. BDD Specifications -- `.copilot/specs.md`

Template: `templates` skill, `references/spec.md` (plus the matching language reference under `references/spec/`).

- Initial spec classes are created during the Spec Gate phase of `feature-workflow` or `refactor-workflow`, or during the Failing Test phase of `bug-fix-workflow`.
- If implementation reveals requirements not in the spec, add them here -- do not let the test file drift ahead of the spec.
- Keep in sync with actual test files: if a test class exists in code, its spec must exist here.
- If the project splits specs by domain, use additional files under `.copilot/` (e.g., `.copilot/specs-parser.md`) following the same template.

## On Invocation

1. Locate or create the tracking document (table above).
2. Identify which items were completed.
3. Verify correctness before checking off items (tests pass, no violations remain).
4. Check off completed items with a one-line finding.
5. Add any new items discovered during the work.
6. Update BDD Specifications if specs were added or modified.
7. Briefly confirm to the user what was updated.
