# Phase 7 -- Implementation

**Purpose:** Write code that makes the failing tests pass. The tests are the specification -- implementation is done when all tests pass and coverage is verified in Phase 8.

---

## Iron Laws

1. **Do not deviate from the reviewed architecture.** If the design needs to change, return to Phase 3, update the design note, get user review, then resume here. Do not silently re-architect during implementation.
2. **Remove what the design replaces.** When the design calls for restructuring, the old structure is removed -- not left alongside the new. Adding new structure next to old is not restructuring; it is accumulation.
3. **Never suppress a failing test or lint error to make a phase pass.** Suppression pragmas are not fixes. A suppressed failure is an unspecified behavior and a coverage gap.
4. **Scope reduction requires explicit user acknowledgment.** If the full scope turns out to be larger than expected, surface it and replan (Iron Law 5 from SKILL.md). Do not quietly narrow what was asked.

---

## Steps

1. Write code to make the failing tests pass. The tests are the specification -- do not add behavior that isn't specified by a test. If you discover a need during implementation, return to Phase 6 and add the spec first.
2. Follow existing code patterns -- check neighboring modules for conventions (error handling, factory methods, async patterns, etc.).
3. Follow the architecture from Phase 3. Any deviation triggers Iron Law 1 above.

## Late-Discovery Structural Gate

If implementation reveals that existing code needs restructuring before the feature can proceed cleanly -- a structural problem not caught in Phase 3:

1. Stop at the point of discovery. Commit any in-progress work on the feature branch.
2. Return to Phase 3. Update the design note with the structural problem and its scope.
3. Present the finding to the user and determine: prerequisite refactor on a new branch, or adjusted feature approach.
4. If a prerequisite refactor is confirmed: open a refactor-workflow on a prerequisite branch off the same base. When the refactor closes and merges, rebase the feature branch and resume from Phase 3 with the corrected substrate.
5. If the user decides to adjust the feature's approach: update the spec and design note before resuming implementation. Do not continue on a design that depends on a structure that doesn't exist.

The late-discovery structural gate is the same exit as Phase 3's structural prerequisite gate -- the difference is that Phase 3 catches it early from design inspection, and Phase 7 catches it late from implementation contact. Both are valid; Phase 3 is cheaper.

## Late-Discovery Quality Gate

If implementation requires modifying existing files not identified in Phase 4 that have quality violations:

1. Commit any in-progress work on the feature branch.
2. Switch to the quality branch from Phase 4 (create one if Phase 4 found all files clean).
3. Fix violations in the newly discovered files and commit.
4. Switch back to the feature branch and merge the quality branch changes.
5. Continue implementation. The draft PR continues to show only functional changes.

## Checkpoint

When all tests pass, update the plan and load Phase 8.
