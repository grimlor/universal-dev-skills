# Phase 1 -- Caller Enumeration

**Purpose:** Find every caller of the target interface. The caller list is the blast radius. Work without it is guesswork.

---

## Enumeration Procedure

Use `semantic_search` and `grep_search` to find every location in the codebase that references the target interface, class, or module being refactored. Cast wide: imports, instantiations, subclasses, type annotations, and test fixtures all count.

For each caller, record:

| Caller | File | Line | What it calls | Adaptation needed |
| --- | --- | --- | --- | --- |
| (name) | (path) | (line) | (method / attribute / constructor) | (brief description) |

"Adaptation needed" should be specific enough to estimate scope -- not "update it" but "change constructor call from `VectorStore(path)` to inject `VectorStorePort` via parameter."

## Volume Check

After enumeration is complete, assess total adaptation scope:

- **Single-pass:** all callers can be adapted in one implementation session. Proceed to Phase 2.
- **Exceeds single-pass:** apply Iron Law 3. Before proceeding, produce a decomposition:
  - Group callers into sequenced sub-tasks
  - State the dependency between sub-tasks (e.g., "Sub-task B requires Sub-task A's port definition to exist")
  - Record the decomposition in the plan under Implementation Tasks
  - Present the decomposition to the user and wait for acknowledgment

Do not begin Phase 2 until the decomposition is accepted, if one is needed.

## Prerequisite Check

Review the caller list for signs that prerequisite cleanup is needed before the main refactor (Iron Law 5). Signals:

- The target boundary has mixed abstraction patterns (some callers use inheritance, others duck-typing, others concrete construction)
- A caller at the boundary uses a pattern that would be inconsistent with the target interface (e.g., ABC inheritance where the target is Protocol)

If prerequisite cleanup is needed:

1. Name it explicitly in the plan as a prerequisite task
2. Note that the main refactor begins only after the prerequisite task closes
3. Present this to the user before proceeding

## Plan Update

Record the full caller table in the plan. Check off "Caller enumeration complete" under Phase 1. Append a session log entry noting the caller count and any volume or prerequisite findings.

## Proceed

Load `steps/02-design.md` and begin Phase 2.
