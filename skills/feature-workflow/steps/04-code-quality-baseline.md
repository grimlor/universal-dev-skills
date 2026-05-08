# Phase 4 -- Code Quality Baseline

**Purpose:** Ensure the files this feature will modify are clean before changes begin. Quality fixes mixed into a feature PR obscure the functional change and make review harder.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started feature-workflow 4 "Code Quality Baseline"
```

---

## Scope

This phase covers only **existing files** the spec (Phase 2) and design (Phase 3) indicate will be modified. New files created by the feature are exempt -- they will be written to standard from the start. Files discovered later during implementation are handled by the late-discovery clause in Phase 7.

## Steps

1. Identify existing files that will be modified.
2. Run mechanical checks -- lint and type-check on those files using the project's configured toolchain (see the relevant language-specific standards skill).
3. Run the structural audit -- follow the `code-quality-audit` skill procedure (Steps 2-5) scoped to the identified files. This catches violations linters miss: mock boundary violations in test files, test-only production API pollution, unjustified suppression pragmas, BDD convention drift.
4. If all files are clean -- update the plan, check off "Code quality baseline verified" under Phase 4, and proceed to Phase 5.
5. If violations exist: a. Create a quality branch (e.g., `quality/<feature-name>`) and fix the violations. b. Commit the fixes using the `conventional-commits` skill and open a PR for review. c. Create the feature branch off the quality branch (e.g., `feat/<feature-name>` branched from `quality/<feature-name>`). d. Open a draft PR from the feature branch targeting the quality branch. This ensures the feature PR diff shows only functional changes. e. Proceed to Phase 5 on the feature branch.

## Checkpoint

Update the plan and load Phase 5.

```bash
~/.agents/bin/emit-telemetry compliance.check feature-workflow 4 "Code Quality Baseline" existing_files_clean pass "All files in scope are lint, type, and audit clean."
~/.agents/bin/emit-telemetry phase.completed feature-workflow 4 "Code Quality Baseline" success "Quality baseline established; feature or quality branch ready."
```
