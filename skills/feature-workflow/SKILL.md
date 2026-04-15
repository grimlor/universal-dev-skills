---
name: feature-workflow
description: "Spec-before-code feature development workflow. Use when the user requests a new feature, enhancement, or non-trivial change -- anything that adds or modifies behavior, including requests phrased as add, implement, build, create, refactor, or start implementation."
---

# Feature Workflow -- Engineering Discipline

## When This Skill Applies

Whenever the user requests a new feature, enhancement, or non-trivial change -- anything
that adds or modifies behavior. This includes requests phrased as "add …", "implement …",
"build …", "create …", "refactor …", "I need …", or "Start implementation".

This skill does **NOT** apply to:
- Bug fixes with a clear cause and obvious one-line fix
- Typo corrections, formatting, or comment-only changes
- Pure refactoring that preserves existing behavior (tests already exist)
- Questions, explanations, or research tasks

---

## The Problem This Solves

AI agents default to writing code immediately. This produces rework, scope creep,
and implementations that solve *a* problem but not *the user's* problem. The user's
established workflow requires specification before implementation -- every time.

Software engineering is not feature development. Feature development asks "is the
code written?" Engineering asks "is the system understood, designed, verified, and
documented?" This workflow encodes the engineering discipline: define it, spec it,
design it, clean the workspace, test it, build it, verify it, record it.

---

## The Required Workflow

Every feature request MUST proceed through these phases in order.
**Do not skip phases. Do not combine phases. Do not start implementation before tests exist.**

### Phase 1 -- Feature Definition

**Goal:** "What are we building and why does it matter?"

The feature exists as an idea. This phase turns it into a defined, bounded thing.

1. **Name the feature.** A short, specific name -- not a verb phrase, not a
   sentence. This becomes the plan document title and the branch name root.
2. **State the goal.** One paragraph: what this feature achieves and why it matters.
   This is the motivating statement that survives context resets.
3. **Establish rough scope.** What does this feature touch? What does it NOT touch?
   Precision is not required yet -- that comes in Phase 2. This is the initial
   boundary that prevents scope creep before the spec exists.
4. **Initialize the plan document.** Locate or create the plan doc using the
   `plan-updates` decision tree. If creating a new plan, read the plan template
   from the `templates` skill (`references/plan.md`) and fill in: Goal from
   step 2, Context/Constraints with
   what is known so far (mark unknowns as TBD), and Open Questions with anything
   that must be resolved before implementation. Check off "Feature defined" under
   Phase 1.

**Present the feature definition to the user.** This is the "are we talking about
the same thing?" checkpoint. Wait for acknowledgment before proceeding.

### Phase 2 -- Spec Gate

**Goal:** "Does a reviewed behavioral spec exist for this feature?"

Given the defined feature, write (or locate) the behavioral specification.

1. **Does a spec document already exist?**
   Look in the project's spec location (BDD Specifications doc, architecture docs,
   or a feature spec file). A spec exists if it describes WHAT the feature does,
   WHO uses it, and what the public API surface looks like.

2. **Is the spec complete enough to implement against?**
   A minimum viable spec must include:
   - WHAT the feature does (behavior, not implementation)
   - WHAT it explicitly does NOT do (scope boundary)
   - The public API surface: method signatures, parameters, return types
   - At least one scenario per major behavior path (Given / When / Then)

3. **Has the human reviewed the spec?**
   A spec written in the same session as implementation has not been reviewed.
   If the spec was just created, stop and wait for human sign-off before
   proceeding.

**If the answer to any of these is no -- stop. Create or complete the spec first.**

#### If No Spec Exists

1. **Ask clarifying questions** -- Do not assume. Identify ambiguity and resolve it.
2. **Write user stories or scenarios** that describe the feature from the consumer's
   perspective (user, downstream module, AI agent -- whoever benefits).
3. **Create the spec** using the template from the `templates` skill
   (`references/spec.md`). Read the template file directly -- do not reproduce
   it from memory. Fill in every section: Overview,
   Out of Scope, Public API Surface, and at least one Behavior with its MOCK BOUNDARY
   and Scenarios.
4. **Present the spec to the user for review** and wait for explicit approval.
5. **Update the plan.** Check off "Spec created / located" and "Human review
   complete" under Phase 2. Update Context/Constraints with decisions made
   during spec creation. Resolve any Open Questions that were answered.

#### If the Spec Exists but Has Gaps

Gaps discovered during any phase:
1. Stop at the point where the gap was discovered
2. Add the missing behavior to the spec document
3. Present the gap and proposed spec addition to the human
4. Wait for approval before continuing

Do not silently fill gaps with undocumented behavior.

### Phase 3 -- Architecture

**Goal:** "How should this be structured internally?"

Given the spec, design the internal structure before writing any code. This phase
prevents the agent from making architectural decisions implicitly during
implementation -- decisions that are hard to see in a diff and expensive to undo.

1. **Identify the architectural concerns.** Not every feature needs deep design.
   But if any of these apply, the design must be explicit:
   - New module or package boundaries
   - New interfaces, protocols, or abstract types
   - Dependency direction decisions (who depends on whom)
   - Port/adapter boundaries (where I/O meets domain logic)
   - Integration points with existing subsystems
   - Concurrency, caching, or state management patterns

2. **Write a design note** using the template from the `templates` skill
   (`references/design-note.md`). Read the template file directly -- do not
   reproduce it from memory. The design note can live in:
   - `docs/adr/` as an Architecture Decision Record (ADR)
   - The spec document as an appended `## Design` section
   - `.copilot/` as a standalone note for smaller features

3. **Present the design to the user for review.** Architectural decisions are
   the hardest to reverse. Wait for explicit approval.

4. **Update the plan.** Check off "Architecture reviewed" under Phase 3. Add any
   new constraints or decisions to Context/Constraints.

**When this phase is trivial:** If the feature is a straightforward addition to an
existing, well-structured module (e.g., adding a field, a new handler following an
established pattern), the design note can be a single sentence: "Follows existing
pattern in `<module>`." The phase still exists -- it just completes quickly.

### Phase 4 -- Code Quality Baseline

**Goal:** "Are the files we're about to change already clean?"

Legacy codebases often contain files with pre-existing lint errors, type errors,
formatting drift, and structural quality violations. Mixing quality fixes into a
feature PR obscures the functional change and makes review harder. This phase
isolates cleanup work into a separate PR so the feature PR shows only the
functional delta.

1. **Identify existing files** that the spec (Phase 2) and design (Phase 3)
   indicate will be modified. New files created by the feature are exempt --
   they will be written to standard from the start.
2. **Run the mechanical checks** -- lint and type-check on those files using the
   project's configured toolchain (see the relevant language-specific standards
   skill).
3. **Run the structural audit** -- follow the `code-quality-audit` skill procedure
   (Steps 2–5) scoped to the identified files. This catches violations that
   linters miss: mock boundary violations in test files, test-only production API
   pollution, unjustified suppression pragmas, and BDD convention drift.
4. **If all files are clean** -- proceed to Phase 5.
5. **If violations exist:**
   a. Create a branch (e.g., `quality/<feature-name>`) and fix the violations.
   b. Commit the fixes and open a PR for review.
   c. Create the **feature branch off the quality branch** (e.g.,
      `feat/<feature-name>` branched from `quality/<feature-name>`).
   d. Open a **draft PR** from the feature branch targeting the quality branch.
      This ensures the draft PR diff shows only the functional changes, not
      formatting and typing noise.
   e. Proceed to Phase 5 on the feature branch.

This gate only applies to **existing files** identified by the spec and design.
Files discovered later during implementation are handled by the late-discovery
clause in Phase 7.

### Phase 5 -- Prerequisite Validation

**Goal:** "Do our assumptions about external dependencies actually hold?"

If the spec depends on external API behavior -- SDK models, REST endpoints,
third-party service capabilities -- validate those assumptions before writing
BDD tests against them.

1. **Identify external premises.** Review the spec's MOCK BOUNDARY declarations
   and Scenarios. Any behavior that assumes a specific external API response,
   data shape, or capability is a premise that can be wrong.
2. **Write a smoke test against the real dependency.** This is NOT a BDD spec --
   it is a narrow integration test that calls the real service and asserts on the
   shape or behavior the spec assumes. Mark it with the project's integration
   test marker (e.g., `@pytest.mark.integration`, `describe.skip` for CI).
3. **Run it.** If the premise holds, proceed to Phase 6. If it fails, **stop** --
   the spec is built on a false assumption. Go back to Phase 2, update the spec
   to reflect reality, and get human review before continuing.
4. **Update the plan.** Check off "Premises validated" under Phase 5. Note which
   dependencies were tested and any surprises discovered.

**When this phase does not apply:** If the feature has no external dependencies
(pure domain logic, internal refactoring, UI-only changes), skip this phase and
note "No external premises" in the plan. The phase heading still exists in the
plan -- it just gets checked off immediately.

### Phase 6 -- BDD Test Specification

**Goal:** "How do we know it works?"

1. **Create test classes** from the specs written in Phase 2, informed by the
   architecture from Phase 3.
2. **Follow BDD testing principles** -- see the `bdd-testing` skill for conventions.
3. **Tests must fail** -- Run the tests to confirm they fail. Refer to tool-usage skill.
   If they pass, either the behavior already exists or the tests aren't testing anything.
4. **Include failure-mode specs** -- An unspecified failure is an unhandled failure.
   Test error paths, edge cases, and boundary conditions.

### Phase 7 -- Implementation

**Goal:** "Build it."

1. **Write code to make the failing tests pass.** The tests are the specification --
   implementation is done when all tests pass.
2. **Follow existing code patterns** -- Check existing modules for conventions
   (error handling patterns, factory methods, async patterns, etc.).
3. **Follow the architecture from Phase 3** -- Do not deviate from the reviewed
   design. If the design needs to change, go back to Phase 3 and update it first.
4. **Do not add behavior that isn't specified by a test.** If you discover a need
   during implementation, go back to Phase 6 and add the spec first.
5. **Late-discovery quality gate.** If implementation requires modifying existing
   files that were **not** identified in Phase 4 and those files have quality
   violations:
   a. Commit any in-progress work on the feature branch.
   b. Switch to the quality branch (from Phase 4 -- create one if Phase 4
      was skipped because all originally-identified files were clean).
   c. Fix the violations in the newly-discovered files and commit.
   d. Switch back to the feature branch and merge in the quality branch changes.
   e. Continue implementation. The draft PR continues to show only functional
      changes.

### Phase 8 -- Coverage Verification

**Goal:** "Is the specification complete?"

1. **Run tests with coverage** for the project's source package.
2. **Every uncovered line is an unspecified requirement.** For each:
   - Is this a real requirement? → Write the spec, then keep the code.
   - Is this dead code? → Remove it.
   - Is this over-engineering? → Remove it and simplify.
3. **Target: 100% coverage.** Not as a vanity metric -- as proof that every line of
   code has a specification justifying its existence.

Three categories routinely surface only at coverage time:
- **Defensive guard code** -- misuse protection
- **Graceful degradation paths** -- soft failures the system absorbs
- **Conditional formatting branches** -- display logic that varies by state

**"Pre-existing" is not a category.** Whether a line existed before your changes is irrelevant -- if it is uncovered after your work, it is uncovered. The only valid dispositions are: real requirement (write the spec), dead code (remove it), or over-engineering (remove it). "It was already there" is not a disposition.

### Phase 9 -- Plan Status Update

**Goal:** "Record what was done."

1. **Update the project's plan document** -- check off completed items, add new
   line items if scope expanded.
2. **Update BDD Specifications** if any specs were added or modified during
   implementation (Phase 7 discoveries).
3. **Append a session log entry** -- record the stopping point, next action, and
   any decisions made. See the `plan-updates` skill for the session log format.
4. See the `plan-updates` skill for detailed rules on tracking progress.

---

## Critical Rules

- **NEVER start writing production code before test specs exist and fail.**
- **NEVER treat "Start implementation" as permission to skip planning.** If the
  user says "Start implementation" and no feature definition exists, Phase 1 is
  the starting point. If the feature is defined but no spec exists, Phase 2.
  If specs exist but no architecture review, Phase 3. If specs and architecture
  exist but tests don't, Phase 6.
- **Present each phase's output to the user** before moving to the next phase.
- **Use the todo list** to track progress through phases -- this gives the user
  visibility into where you are in the workflow.

---

## Relationship to Other Skills

- `feature-workflow` (this skill) governs the full lifecycle -- definition through plan update
- `code-quality-audit` governs the structural inspection in Phase 4 -- mock boundaries,
  test-only APIs, suppression pragmas, BDD conventions
- `bdd-testing` governs test quality -- referenced from Phase 6 and the `bdd-feedback-loop`
- `bdd-feedback-loop` governs per-module test implementation -- used during Phase 6
- `plan-updates` governs progress tracking -- used during Phase 1 (initialization) and
  Phase 9 (final update), and at any phase boundary where progress should be recorded
- `templates` provides canonical document structures -- plan (Phase 1), spec (Phase 2),
  design note (Phase 3). Read templates from this skill, do not reproduce from memory
- `tool-usage` is cross-cutting -- applies at every phase

The flow: **define → spec → architecture → quality baseline → prerequisite validation → tests → implementation → coverage → plan update**
