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

---

## Usage

1. Read the relevant template file from this skill's `references/` directory.
2. Copy the template content into the target location.
3. Fill in all placeholders (marked with `<angle brackets>`).
4. Follow the rules defined in the requesting skill (`feature-workflow` or
   `plan-updates`) for how to populate each section.

Templates define **structure**. Skills define **rules and workflow**.
