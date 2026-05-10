---
name: bug-fix-workflow
description: "Structured workflow for diagnosing and fixing defects -- cases where the system behaves differently from intent. Use when a bug has been reported or discovered. NOT for new features or enhancements (use feature-workflow). NOT for structural improvements to correct code (use refactor-workflow). NOT for typo corrections, formatting, or comment-only changes."
---

# Bug Fix Workflow

Structured process for diagnosing and correcting defective behavior. The goal is a verified fix with a permanent regression guard -- not just code that no longer exhibits the symptom.

## How This Differs from feature-workflow and refactor-workflow

- **feature-workflow** adds new behavior. Bug fixes correct existing behavior that diverges from intent -- no new capability.
- **refactor-workflow** restructures correct code. A bug fix may transition into a refactor when root cause is structural, but the motivation is correction, not improvement.
- The failing test written in Phase 2 is the acceptance criterion. The fix is done when that test passes and the full suite is green -- not before.

## Iron Laws

1. **Reproduce before diagnosing.** If you cannot reproduce the bug, you cannot verify the fix. Gather reproduction steps from the user before touching any code.
2. **Failing test before fix.** The reproduction steps are encoded as a failing BDD test before root cause analysis begins. The test tells you what "fixed" means. Diagnosing without it risks fixing the wrong thing.
3. **The failing test must fail for the right reason.** Run it, confirm it fails, understand why it fails -- before writing any fix. A test written and fixed in the same motion may never have caught the bug.
4. **Root cause, not symptom.** If the fix addresses the symptom without the root cause, the same bug surfaces elsewhere. Root cause must be identified before the fix is written.
5. **Minimal change for minimal fixes.** A targeted fix changes only what the root cause identifies. Opportunistic refactoring during a bug fix is scope creep -- note it and open a separate refactor-workflow.
6. **Full suite must pass.** The fix must not introduce regressions. Both the new test and the full pre-existing suite must be green at closure.

## Phase Overview

Load the step file for the current phase. Do not load all steps at once.

| Phase | Step file | Purpose |
| --- | --- | --- |
| 1 -- Reproduction Steps | `steps/01-reproduction-steps.md` | Structured intake; Given/When/Then scenario |
| 2 -- Failing Test | `steps/02-failing-test.md` | BDD test encoding the bug; confirmed failing |
| 3 -- Root Cause | `steps/03-root-cause.md` | Why; minimal vs. structural determination |
| 4 -- Fix | `steps/04-fix.md` | Minimal fix or transition to refactor-workflow |
| 5 -- Verification | `steps/05-verification.md` | Full suite green; plan closed |

## Workflow Composition

Bug fix workflow composes with refactor-workflow when root cause is structural:

- **bug-fix-workflow → refactor-workflow:** when Phase 3 determines the root cause is a structural defect, the bug fix transitions into refactor-workflow on the same branch. The failing test from Phase 2 travels with the branch as the acceptance criterion throughout the refactor. The branch does not become a PR candidate until the refactor closes and the failing test passes. bug-fix-workflow Phase 5 is superseded by refactor-workflow Phase 6 in this case.

If the bug fix reveals missing intended behavior -- something the system never did but should -- that is a feature, not a fix. Close the bug fix branch, open a feature-workflow on a new branch.

Transitioning to another workflow is not a failure of process -- it is the correct response when root cause analysis reveals that the work is larger or different in kind than the initial report suggested.

## Relationship to Other Skills

- `refactor-workflow` -- Phase 4 may transition into this skill when root cause is structural; the failing test from Phase 2 travels with the branch as the acceptance criterion
- `feature-workflow` -- not interchangeable; if the bug fix reveals missing intended behavior, close the bug fix branch and open a feature-workflow
- `bdd-testing` -- test quality standards; referenced from Phase 2
- `plan-updates` -- progress tracking; used at Phase 1 (initialization) and Phase 5 (closure)
- `templates` -- plan template at Phase 1; read directly, never from memory
- `tool-usage` -- cross-cutting; applies at every phase
- `conventional-commits` -- commit message format; `fix:` type for minimal fixes; `refactor:` type if the branch transitions to structural fix
- `_shared/telemetry.md` -- structured event logging; read before invoking this skill and emit `skill.invoked` before any phase begins

## On Invocation

Read `_shared/telemetry.md`, then emit `skill.invoked` before loading any phase step file:

```bash
~/.agents/bin/emit-telemetry skill.invoked bug-fix-workflow
```
