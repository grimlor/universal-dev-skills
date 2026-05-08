# Phase 2 -- Spec Gate

**Purpose:** Confirm a reviewed behavioral spec exists before any design or implementation begins.

---

## Iron Laws

1. **Spec gaps stop this phase.** When a gap is discovered -- here or in any later phase -- stop at the point of discovery, add the missing behavior to the spec, present it to the user, and wait for review before continuing.
2. **A spec written in the same turn as implementation has not been reviewed.** Stop and wait for human sign-off.
3. **Do not silently fill gaps with undocumented behavior.** If the right answer is unclear, ask.

---

## Gate Checks

Answer all three before proceeding:

1. **Does a spec document exist?** Look in the project's spec location (BDD Specifications doc, architecture docs, feature spec file). A spec exists if it describes WHAT the feature does, WHO uses it, and what the public API surface looks like.
2. **Is the spec complete enough to implement against?** A minimum viable spec includes: WHAT the feature does (behavior, not implementation); WHAT it explicitly does NOT do (scope boundary); the public API surface (method signatures, parameters, return types); at least one scenario per major behavior path (Given / When / Then).
3. **Has the human reviewed the spec?** A spec written in the same turn as implementation has not been reviewed.

If any answer is no -- stop. Create or complete the spec first.

## If No Spec Exists

1. Ask clarifying questions -- do not assume. Identify ambiguity and resolve it before writing.
2. Write user stories or scenarios from the consumer's perspective (user, downstream module, AI agent -- whoever benefits).
3. Create the spec using the `templates` skill (`references/feature-spec.md`). Read the template directly -- do not reproduce from memory. Fill in every section: Overview, Out of Scope, Public API Surface, and at least one Behavior with its MOCK BOUNDARY and Scenarios.
4. Present the spec to the user for review. Wait for explicit approval.
5. Update the plan: check off "Spec created / located" and "Human review complete" under Phase 2. Update Context/Constraints with decisions made. Resolve Open Questions that were answered.

## If the Spec Exists but Has Gaps

1. Stop at the point where the gap was discovered.
2. Add the missing behavior to the spec document.
3. Present the gap and proposed addition to the user.
4. Wait for approval before continuing.

## Checkpoint

Present the completed spec to the user and wait for explicit acknowledgment before loading Phase 3.
