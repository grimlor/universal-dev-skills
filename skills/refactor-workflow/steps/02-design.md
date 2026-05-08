# Phase 2 -- Design

**Purpose:** Document the current interface, the target interface, and the adapter map. Every architectural decision made here is a decision the implementation phase does not get to re-make silently.

---

Emit `phase.started` before any work begins:

```bash
~/.agents/bin/emit-telemetry phase.started refactor-workflow 2 "Design"
```

---

## Design Note

Create `.copilot/design-note.md` using the template from the `templates` skill (`references/design-note.md`). Read the template directly.

The design note for a refactor must cover:

### Current Interface

Document what exists now:

- Public API surface (method signatures, constructor parameters, return types)
- What callers depend on (the stable surface vs. implementation details)
- What abstraction mechanism is currently in use (inheritance, duck typing, concrete class, ABC, Protocol)

### Target Interface

Document what the refactor produces:

- New public API surface at the target boundary
- Abstraction mechanism after the refactor (Protocol, ABC, dependency injection)
- What callers will depend on instead

### Adapter Map

For each caller from Phase 1, state the specific adaptation:

| Caller | Current usage | Target usage | Notes |
| --- | --- | --- | --- |
| (name) | (what it does now) | (what it will do) | (any risk or ordering dependency) |

### Key Decisions

Record every non-obvious design choice as a Key Decision (KD):

- KD-N: [decision] because [rationale]. Alternatives considered: [X] (rejected because [Y]).

Decisions that seem obvious to you now will not be obvious to a future reader or to an agent resuming after a context reset.

## Spec Reveals Gaps -- Iteration Protocol

If writing the spec in Phase 3 reveals that the design is under-specified, return here. Update the design note with the gap and its resolution. Do not patch the gap silently in the spec or test. Iron Law 2 (retreat to design) applies.

## Present and Wait

Present the design note to the user. Wait for explicit acknowledgment before proceeding to Phase 3. Architectural decisions are the hardest to reverse.

## Plan Update

Check off "Design complete" under Phase 2. Append a session log entry summarizing the key decisions made.

## Proceed

Load `steps/03-spec-gate.md` and begin Phase 3.

```bash
~/.agents/bin/emit-telemetry phase.completed refactor-workflow 2 "Design" success "Design note complete with current interface, target interface, adapter map, and KDs. User reviewed."
```
