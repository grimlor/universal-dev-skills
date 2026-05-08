---
name: templates
description: "Document templates for various workflows, including feature and refactor workflows. Use when creating a plan, spec, or design note -- read the relevant template file from references/ rather than reproducing structure from memory."
---

# Templates -- Canonical Document Structures

## Iron Laws

1. **Never reproduce templates from memory.** Always read the template file directly from `references/`.
2. **Read the language-agnostic template first**, then the matching language reference (when one exists for that template).
3. **Templates define structure only.** Population rules live in the requesting skill (`feature-workflow` or `plan-updates`).

## Available Templates
| Template | File | Created during | Target path |
|---|---|---|---|
| Plan document | `references/feature-plan.md` | Phase 1 -- Feature Definition | `.copilot/<feature name>-plan.md` |
| Feature spec | `references/feature-spec.md` | Phase 2 -- Spec Gate (feature-workflow) | `.copilot/<feature name>-specs.md` |
| Refactor adaptation plan | `references/refactor-adaptation-plan.md` | Phase 3 -- Spec Gate (refactor-workflow) | `.copilot/<refactor name>-adaptation-plan.md` |
| Design note | `references/design-note.md` | Phase 3 -- Architecture (feature) / Phase 2 -- Design (refactor) | `.copilot/<feature/refactor name>-design-note.md` |
| Task tracking | `references/task.md` | Start of refactor / audit / remediation pass | `.copilot/<task name>.md` |

### Language-Specific References

| Template | Language references |
|---|---|
| Feature spec | `references/spec/python.md`, `references/spec/typescript.md`, `references/spec/java.md`, `references/spec/csharp.md` |

## On Invocation

1. Read the template file from `references/`.
2. If a language-specific reference exists for that template, read the one matching your project's language.
3. Copy the template content into the target location.
4. Fill in all `<angle bracket>` placeholders, using the language reference for code block patterns.
5. Follow the requesting skill's rules for how to populate each section.
