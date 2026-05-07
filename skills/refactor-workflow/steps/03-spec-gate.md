# Phase 3 -- Spec Gate

**Purpose:** Write a BDD spec that proves existing observable behavior is preserved under the new structure. The spec is not about what the refactor adds -- it is about what it must not break.

---

## Spec Shape for Refactors

Create `.copilot/specs.md` using the template from the `templates` skill (`references/spec.md`). Read the template directly.

A refactor spec differs from a feature spec in scope: every scenario describes a behavior that currently exists and must continue to exist after the refactor. The spec is evidence of preservation, not specification of new capability.

For each behavior to preserve:

- Write a REQUIREMENT class named for the consumer requirement being preserved (not for the internal class or module being restructured)
- WHO is the caller or consumer that depends on this behavior continuing
- WHAT enumerates the observable outcomes that prove the behavior still holds
- WHY states what breaks downstream if this behavior is lost

MOCK BOUNDARY is set at the NEW interface boundary -- the target interface from Phase 2, not the current one. The tests will run against fakes that implement the target interface, and against the real implementation once it exists.

## Design Gap Protocol

If writing scenarios reveals that the design (Phase 2) does not specify how a particular behavior maps to the new interface, stop. Do not invent a mapping. Return to `steps/02-design.md`, update the design note with the gap and its resolution, then return here and continue.

This iteration is expected. Iron Law 6 applies.

## Coverage of Failure Modes

The spec must cover failure modes, not just happy paths. For every interaction at the target boundary:

- What happens when the boundary returns an empty result?
- What happens when it raises?
- What happens at volume limits or boundary values?

An unspecified failure mode in the refactor spec is a behavior the refactor is not required to preserve. That is a risk, not an acceptable gap.

## Present and Wait

Present the spec to the user. Wait for explicit acknowledgment before proceeding to Phase 4.

## Plan Update

Check off "Spec gate complete" under Phase 3. Append a session log entry noting the scenario count and any design gaps that triggered a Phase 2 retreat.

## Proceed

Load `steps/04-test-gate.md` and begin Phase 4.
