---
name: templates
description: "Document templates for the feature workflow. Use when creating a plan, spec, or design note -- read the relevant template file from references/ rather than reproducing structure from memory."
---

# Templates -- Canonical Document Structures

## When This Skill Applies

Whenever you need to create a plan document, behavioral spec, or design note.
Other skills reference this skill as the source of truth for document structure.

Do not reproduce templates from memory. Read the template file directly.

---

## Available Templates

| Template | File | Created during |
|---|---|---|
| Plan document | `references/plan.md` | Phase 1 -- Feature Definition |
| Behavioral spec | `references/spec.md` | Phase 2 -- Spec Gate |
| Design note | `references/design-note.md` | Phase 3 -- Architecture |

### Language-Specific References

Some templates have language-specific reference files for code examples.
Read the language-agnostic template first, then read the relevant language
reference for code patterns.

| Template | Language references |
|---|---|
| Behavioral spec | `references/spec/python.md`, `references/spec/typescript.md`, `references/spec/java.md`, `references/spec/csharp.md` |

---

## Usage

1. Read the relevant template file from this skill's `references/` directory.
2. If the template has language-specific references, also read the reference
   matching your project's language.
3. Copy the template content into the target location.
4. Fill in all placeholders (marked with `<angle brackets>`), using the
   language-specific reference for code block patterns.
5. Follow the rules defined in the requesting skill (`feature-workflow` or
   `plan-updates`) for how to populate each section.

Templates define **structure**. Skills define **rules and workflow**.
