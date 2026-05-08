# Phase 3 -- Architecture

**Purpose:** Design the internal structure before writing any code. Architectural decisions made here are decisions Phase 7 does not get to re-make silently. This phase is also the earliest point at which a structural prerequisite can be identified -- if the existing code needs restructuring before the feature can be built cleanly, that determination belongs here, not in Phase 7.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started feature-workflow 3 "Architecture"
```

---

## Iron Laws

1. **Architectural decisions require explicit user review before proceeding.** They are the hardest to reverse. Do not move to Phase 4 without acknowledgment.
2. **Structural prerequisites are identified here, not discovered in Phase 7.** If the design reveals that existing code needs restructuring to cleanly accommodate the feature, stop and surface it now. Do not absorb the refactor into Phase 7 implementation.

---

## When This Phase Requires Depth

Not every feature needs deep design. If any of these apply, the design must be explicit:

- New module or package boundaries
- New interfaces, protocols, or abstract types
- Dependency direction decisions (who depends on whom)
- Port/adapter boundaries (where I/O meets domain logic)
- Integration points with existing subsystems
- Concurrency, caching, or state management patterns

If none apply -- the feature is a straightforward addition to a well-structured module following an established pattern -- the design note can be a single sentence: "Follows existing pattern in `<module>`." The phase still exists; it just completes quickly.

## Steps

1. Identify the architectural concerns from the list above.
2. Inspect the existing code the feature will build on. Assess whether it is structured to receive the feature cleanly -- correct abstraction boundaries, no mixed patterns, no inheritance where protocols are the target shape.
3. Write a design note using the `templates` skill (`references/design-note.md`). Read the template directly -- do not reproduce from memory. The design note can live in: `docs/adr/` as an ADR; the spec document as an appended `## Design` section; `.copilot/` as a standalone note for smaller features.
4. Record every non-obvious design choice as a Key Decision (KD): what was decided, why, and what alternatives were rejected and why. Decisions that seem obvious now will not be obvious after a context reset.
5. Update the plan: check off "Architecture reviewed" under Phase 3. Add new constraints or decisions to Context/Constraints.

## Structural Prerequisite Gate

If step 2 reveals that existing code needs restructuring before the feature can be built cleanly:

1. Record the structural problem and its scope in the design note as a Key Decision: what needs restructuring, why it blocks the feature, and what the target structure is.
2. Present the finding to the user. This is a scope and sequencing decision -- the user decides whether to proceed with the prerequisite refactor now or adjust the feature's approach.
3. If a prerequisite refactor is confirmed: the feature branch pauses. Open a refactor-workflow on a prerequisite branch off the same base. When the refactor closes and merges, rebase the feature branch and resume from Phase 3 with the corrected substrate.
4. If the user decides to adjust the feature's approach to avoid the prerequisite: update the spec (Phase 2) and design note to reflect the adjusted approach before proceeding. Do not carry forward a design that depends on a structure that doesn't exist.

## Checkpoint

Present the design note to the user. Wait for explicit acknowledgment before loading Phase 4.

```bash
~/.agents/bin/emit-telemetry phase.completed feature-workflow 3 "Architecture" success "Design note complete and reviewed by user."
```
