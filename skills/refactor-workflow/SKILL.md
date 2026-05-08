---
name: refactor-workflow
description: "Structured workflow for refactoring existing code without changing observable behavior. Use when restructuring abstractions, extracting ports or adapters, converting inheritance to protocols, or adapting callers to new interfaces -- any change where the goal is structural improvement, not new capability. NOT for new features or enhancements (use feature-workflow). NOT for bug fixes."
---

# Refactor Workflow

Structured process for safely restructuring existing code. The goal is preserved behavior under a new structure -- not new capability.

## How This Differs from feature-workflow

`feature-workflow` and `refactor-workflow` are not interchangeable. Four differences are structural, not stylistic:

- **Caller enumeration is load-bearing.** You cannot scope a refactor without knowing what you are breaking. feature-workflow has no equivalent phase.
- **Tests prove preservation, not new behavior.** The spec and test gate prove that existing observable behavior holds under the new structure. New behavior belongs in a separate feature after the refactor closes.
- **Phase 3 to 4 iteration is expected.** Writing the spec against the new interface shape surfaces design gaps. Retreating to the design phase to fix them is correct, not failure. feature-workflow visits Phase 3 once.
- **The existing test suite is the regression gate.** After implementation, the full existing suite must pass alongside the new tests. Passing new tests alone are not sufficient evidence that behavior is preserved.

## Iron Laws

1. **Enumerate callers before starting.** The full caller list is the blast radius. Scope defined without it is guesswork.
2. **Preserve behavior, don't extend it.** New requirements discovered during the refactor belong in a separate feature. Stop, close the refactor at a stable intermediate state, open a feature branch.
3. **Volume is a planning condition, not a stopping condition.** If the caller list exceeds single-pass scope, decompose into sequenced sub-tasks with stated dependencies before starting. Do not refuse; do not fragment without a sequencing plan.
4. **Prerequisite cleanup first.** If the existing code has inconsistencies the refactor would expose -- mixed abstraction patterns, inheritance where protocols are the target boundary -- resolve them as a separate prior task. Do not absorb prerequisite cleanup into the main refactor.

## Phase Overview

Load the step file for the current phase. Do not load all steps at once.

| Phase | Step file | Purpose |
| --- | --- | --- |
| 0 -- Entry | `steps/00-entry.md` | Pre-flight, scope, plan |
| 1 -- Caller Enumeration | `steps/01-caller-enumeration.md` | Every caller, every adaptation needed |
| 2 -- Design | `steps/02-design.md` | Current to target interface; adapter map; decisions |
| 3 -- Spec Gate | `steps/03-spec-gate.md` | BDD spec of existing behavior to preserve |
| 4 -- Test Gate | `steps/04-test-gate.md` | Tests against new interface shape; outcome-equivalent |
| 5 -- Implementation | `steps/05-implementation.md` | Adapt callers; existing suite + new tests pass |
| 6 -- Verification | `steps/06-verification.md` | Full suite green; coverage confirmed; plan closed |

## Relationship to Other Skills
- `feature-workflow` -- for new capability; not interchangeable with this skill
- `bdd-testing` -- test quality standards; referenced from Phase 3 and Phase 4
- `plan-updates` -- progress tracking; used at Phase 0 (initialization) and Phase 6 (closure), and at every phase boundary
- `templates` -- canonical document structures; read templates directly, never from memory
- `tool-usage` -- cross-cutting; applies at every phase
- `code-quality-audit` -- if pre-existing files modified by the refactor have quality violations, follow the audit procedure before beginning implementation
- `_shared/telemetry.md` -- structured event logging; read before invoking this skill and emit `skill.invoked` before any phase begins

## On Invocation

Read `_shared/telemetry.md`, then emit `skill.invoked` before loading any phase step file:

```bash
~/.agents/bin/emit-telemetry skill.invoked refactor-workflow
```
