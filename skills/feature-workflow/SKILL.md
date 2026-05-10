---
name: feature-workflow
description: "Spec-before-code feature development workflow. Use when the user requests a new feature, enhancement, or non-trivial change -- anything that adds or modifies behavior, including requests phrased as add, implement, build, or create. NOT for pure refactoring that preserves existing behavior (use refactor-workflow). NOT for defects where the system diverges from intent (use bug-fix-workflow). NOT for typo corrections, formatting, or comment-only changes."
---

# Feature Workflow -- Engineering Discipline

## The Problem This Solves

AI agents default to writing code immediately. This produces rework, scope creep, and implementations that solve _a_ problem but not _the user's_ problem. Software engineering asks "is the system understood, designed, verified, and documented?" -- not just "is the code written?" This workflow encodes that discipline: define it, spec it, design it, clean the workspace, test it, build it, verify it, record it.

## When This Skill Applies

Whenever the user requests a new feature, enhancement, or non-trivial change -- anything that adds or modifies behavior.

This skill does NOT apply to:

- Pure refactoring that preserves existing behavior (use `refactor-workflow`)
- Defects where the system diverges from intent (use `bug-fix-workflow`)
- Typo corrections, formatting, or comment-only changes

If the request is ambiguous -- "fix this so it works better" could be a feature or a bug fix -- ask the user whether the system is behaving wrongly (bug) or whether new capability is wanted (feature) before selecting a workflow.

## Iron Laws

1. **Never write production code before tests exist and fail.** No exceptions, no sub-phases, no "just a quick scaffold."
2. **Never skip or combine phases.** Each phase gate exists because the next phase depends on its output.
3. **Present each phase output before proceeding.** The user checkpoint is the gate, not your confidence in the output.
4. **"Start implementation" routes to the earliest incomplete phase.** If no feature definition exists, start at Phase 1. If no spec, Phase 2. If no architecture review, Phase 3. If no tests, Phase 6. Never jump to Phase 7 directly.
5. **Volume is a planning condition, not a stopping condition.** If scope is larger than expected, decompose and replan. Do not refuse; do not quietly narrow.

## Phase Overview

Load the step file for the current phase. Do not load all steps at once.

| Phase | Step file | Purpose |
| --- | --- | --- |
| 1 -- Feature Definition | `steps/01-feature-definition.md` | Name, goal, scope, plan initialized |
| 2 -- Spec Gate | `steps/02-spec-gate.md` | Behavioral spec exists and is reviewed |
| 3 -- Architecture | `steps/03-architecture.md` | Internal structure designed and reviewed; structural prerequisites identified |
| 4 -- Code Quality Baseline | `steps/04-code-quality-baseline.md` | Existing files clean before changes begin |
| 5 -- Prerequisite Validation | `steps/05-prerequisite-validation.md` | External API assumptions verified |
| 6 -- BDD Test Specification | `steps/06-bdd-test-specification.md` | Tests written, failing, covering failure modes |
| 7 -- Implementation | `steps/07-implementation.md` | Tests pass; architecture followed; no extras |
| 8 -- Coverage Verification | `steps/08-coverage-verification.md` | 100% coverage; every line specified |
| 9 -- Plan Status Update | `steps/09-plan-status-update.md` | Plan closed; session log appended |

## Workflow Composition

These workflows are composable -- a feature can spawn a prerequisite refactor, and the workflows hand off rather than compete:

- **feature-workflow → refactor-workflow:** if Phase 3 or Phase 7 reveals that existing code needs restructuring before the feature can be built cleanly, refactor-workflow executes as a prerequisite on a separate branch. The feature resumes after the refactor merges.
- **bug-fix-workflow → refactor-workflow:** if a bug fix reveals a structural root cause, bug-fix-workflow transitions into refactor-workflow on the same branch. The failing test from bug-fix-workflow Phase 2 travels with the branch as the acceptance criterion.

Spawning a prerequisite workflow is not a failure of process -- it is the correct response to discovering that the substrate needs preparation before the primary work can proceed cleanly.

## Relationship to Other Skills

- `refactor-workflow` -- for structural changes that preserve behavior; can be spawned as a prerequisite by this skill
- `bug-fix-workflow` -- for defects where the system diverges from intent; not interchangeable with this skill
- `code-quality-audit` -- structural inspection used in Phase 4; mock boundaries, suppression pragmas, BDD conventions
- `bdd-testing` -- test quality standards; referenced from Phase 6
- `bdd-feedback-loop` -- per-module test implementation; used during Phase 6
- `plan-updates` -- progress tracking; used at Phase 1 (initialization), Phase 9 (closure), and every phase boundary
- `templates` -- canonical document structures; plan (Phase 1), feature-spec (Phase 2), design note (Phase 3); read templates directly, never from memory
- `tool-usage` -- cross-cutting; applies at every phase
- `conventional-commits` -- commit message format; used at Phase 4 (quality branch) and after Phase 9
- `_shared/telemetry.md` -- structured event logging; read before invoking this skill and emit `skill.invoked` before any phase begins

## On Invocation

Read `_shared/telemetry.md`, then emit `skill.invoked` before loading any phase step file:

```bash
~/.agents/bin/emit-telemetry skill.invoked feature-workflow
```

## Content Routing -- Where Information Lives

When migrating content from existing documents into the template system:

| Source content | Destination |
| --- | --- |
| Motivation / Why | Plan → Goal |
| Approach / Solution | Design Note, or Plan → Context/Constraints |
| Root Cause / Current State | Spec → Overview, or Plan → Context/Constraints |
| Alternative Considered | Design Note → Key Decisions, or Plan → Context/Constraints |
| Tasks / Implementation Steps | Plan → Implementation Tasks |
| Behavioral requirements | Spec → Behaviors (one per test class) |
| API surface | Spec → Public API Surface |

When in doubt: "Is this _what_ to build (spec), _why/how_ to build it (design note), or _project state_ (plan)?" Content lives in exactly one place.
