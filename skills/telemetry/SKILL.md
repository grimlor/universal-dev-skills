---
name: telemetry
description: "Read FIRST, before skill-compliance and all other skills. Defines the emission protocol for all skill activity. Every skill loaded in a session must emit skill.invoked immediately after being read. Every completed skill must emit skill.completed. Timestamps are reviewed for compliance."
---

# Telemetry -- Structured Event Logging

This skill must be read before any other skill, including skill-compliance. Its Iron Laws apply for the remainder of the session without exception.

---

## Iron Laws

1. **Emit `skill.invoked <skill-name>` immediately after reading each skill — before executing any procedure step from it.** This applies to every skill: workflow skills, cross-cutting skills, language standards skills, skill-compliance, and this skill itself. Run:
   ```bash
   ~/.agents/bin/emit-telemetry skill.invoked <skill-name>
   ```
2. **Never batch emissions.** Each emission must fire immediately after the triggering event. Batching all emissions at session end is a compliance violation regardless of whether the correct events eventually appear. Timestamps are recorded in the log and **will be reviewed**.
3. **Emit `skill.completed <skill-name>` when a skill's full procedure has been followed to completion.** Do not emit this event if the skill was only partially read or its steps were not executed.
4. **If the binary is unavailable, stop and report before continuing.** A missing binary is not a reason to skip telemetry — it is a reason to halt. Do not proceed with an incomplete telemetry record.

---

## Emission Command

All events are emitted via the `emit-telemetry` binary:

```bash
~/.agents/bin/emit-telemetry <event_type> <skill> [additional fields...]
```

This path is target-independent — the same path works for VS Code, Claude Code, Cursor, and Windsurf regardless of working directory.

---

## Event Schema

### `skill.invoked`

Emitted each time a skill is read and invoked, immediately before executing any procedure step. Re-reads within a session emit again — repeated emissions are valid data, not noise.

```bash
~/.agents/bin/emit-telemetry skill.invoked <skill-name>
```

Examples:
```bash
~/.agents/bin/emit-telemetry skill.invoked telemetry
~/.agents/bin/emit-telemetry skill.invoked skill-compliance
~/.agents/bin/emit-telemetry skill.invoked refactor-workflow
~/.agents/bin/emit-telemetry skill.invoked python-code-standards
```

---

### `skill.completed`

Emitted when a skill's full procedure has been followed to completion.

```bash
~/.agents/bin/emit-telemetry skill.completed <skill-name> <outcome> "<detail>"
```

Outcome values: `success`, `partial`, `blocked`

Example:
```bash
~/.agents/bin/emit-telemetry skill.completed refactor-workflow success "All phases passed."
```

---

### `phase.started`

Emitted at the top of each workflow step file, before any work begins.

```bash
~/.agents/bin/emit-telemetry phase.started <skill> <phase> "<phase_name>"
```

Example:
```bash
~/.agents/bin/emit-telemetry phase.started refactor-workflow 1 "Caller Enumeration"
```

---

### `phase.completed`

Emitted at the end of each workflow step file, after the checkpoint, before loading the next step.

```bash
~/.agents/bin/emit-telemetry phase.completed <skill> <phase> "<phase_name>" <outcome> "<detail>"
```

Outcome values: `success`, `partial`, `blocked`

Example:
```bash
~/.agents/bin/emit-telemetry phase.completed refactor-workflow 1 "Caller Enumeration" success "All callers identified and documented."
```

---

### `compliance.check`

Emitted when a specific rule or gate condition is evaluated.

```bash
~/.agents/bin/emit-telemetry compliance.check <skill> <phase> "<phase_name>" <rule> <outcome> "<detail>"
```

Outcome values: `pass`, `fail`

Example:
```bash
~/.agents/bin/emit-telemetry compliance.check refactor-workflow 3 "Spec Gate" spec_exists_and_reviewed pass "Spec exists, complete, and reviewed."
```

---

## When to Emit

| Event | When |
|---|---|
| `skill.invoked` | Each time a skill is read, immediately after the read and before any procedure step — applies to every skill including this one; re-reads within a session emit again |
| `phase.started` | Top of every workflow step file, before reading any plan or writing any content |
| `phase.completed` | End of every workflow step file, after the checkpoint, before loading the next step |
| `compliance.check` | Any step that explicitly evaluates a rule, gate condition, coverage result, or audit outcome |
| `skill.completed` | After a skill's full procedure has been followed to completion |

---

## Relationship to ACMCP

When the Adversarial Compliance MCP is implemented, it will produce a richer event stream as a structural product of the gate chain. At that point this advisory telemetry layer will be superseded for gated workflows. It will continue to apply for skills and phases running outside the ACMCP gate.
