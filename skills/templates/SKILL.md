---
name: templates
description: "Document templates for the feature workflow. Use when creating a plan, spec, or design note -- read the relevant template file from references/ rather than reproducing structure from memory."
---

# Templates -- Canonical Document Structures

## Iron Laws

1. **Never reproduce templates from memory.** Always read the template file
   directly from `references/`.
2. **Read the language-agnostic template first**, then the matching language
   reference (when one exists for that template).
3. **Templates define structure only.** Population rules live in the requesting
   skill (`feature-workflow` or `plan-updates`).

## Available Templates

| Template | File | Created during |
|---|---|---|
| Plan document | `references/plan.md` | Phase 1 -- Feature Definition |
| Behavioral spec | `references/spec.md` | Phase 2 -- Spec Gate |
| Design note | `references/design-note.md` | Phase 3 -- Architecture |

### Language-Specific References

| Template | Language references |
|---|---|
| Behavioral spec | `references/spec/python.md`, `references/spec/typescript.md`, `references/spec/java.md`, `references/spec/csharp.md` |

## On Invocation

1. Read the template file from `references/`.
2. If a language-specific reference exists for that template, read the one
   matching your project's language.
3. Copy the template content into the target location.
4. Fill in all `<angle bracket>` placeholders, using the language reference
   for code block patterns.
5. Follow the requesting skill's rules for how to populate each section.
