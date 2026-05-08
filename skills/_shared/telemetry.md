# Telemetry -- Structured Event Logging

Shared reference for skill telemetry. All workflow skills and procedural skills emit structured events to a local log file. The log provides diagnostic visibility into skill execution without requiring the ACMCP enforcement layer.

This is the pre-ACMCP telemetry mechanism. When the ACMCP exists, it will provide a richer event stream as a natural product of the gate chain. Until then, this file defines the advisory telemetry layer.

---

## Log Location

```
~/.agents/events.log
```

JSON Lines format -- one JSON object per line, append-only. The directory is created automatically on first emit.

---

## Emission Command

All events are emitted via the `emit-telemetry` binary installed at `~/.agents/bin/emit-telemetry`. This location is target-independent -- the same path works for VS Code, Claude Code, Cursor, Windsurf, and OpenCode regardless of working directory.

```bash
~/.agents/bin/emit-telemetry <event_type> <skill> [additional fields...]
```

Install the binary by running `python3 scripts/setup.py --target <your-target>` from the universal-dev-skills repo root. The setup script symlinks the binary into `~/.agents/bin/` automatically.

**If emission fails (non-zero exit), stop and diagnose before continuing.** A failed emission means the diagnostic record for Experiment 2 is incomplete. Telemetry is not optional and failure is not silent -- the binary writes to stderr and exits non-zero on any write error.

---

## Event Schema and Calling Convention

### `skill.invoked`

Emitted at the start of skill execution, before any phase begins.

```bash
~/.agents/bin/emit-telemetry skill.invoked <skill>
```

Example:
```bash
~/.agents/bin/emit-telemetry skill.invoked feature-workflow
```

---

### `phase.started`

Emitted at the top of each step file, before any work begins.

```bash
~/.agents/bin/emit-telemetry phase.started <skill> <phase> "<phase_name>"
```

Example:
```bash
~/.agents/bin/emit-telemetry phase.started feature-workflow 1 "Feature Definition"
```

---

### `phase.completed`

Emitted at the end of each step file, after the checkpoint, before loading the next step.

```bash
~/.agents/bin/emit-telemetry phase.completed <skill> <phase> "<phase_name>" <outcome> "<detail>"
```

Outcome values: `success`, `partial`, `blocked`

`blocked` is used when a gate check fails and work cannot proceed.

Example:
```bash
~/.agents/bin/emit-telemetry phase.completed feature-workflow 1 "Feature Definition" success "Feature named, goal stated, scope established, plan initialized."
```

---

### `compliance.check`

Emitted when a specific rule or gate condition is evaluated. Use for Iron Law checks, audit results, and coverage verification.

```bash
~/.agents/bin/emit-telemetry compliance.check <skill> <phase> "<phase_name>" <rule> <outcome> "<detail>"
```

Outcome values: `pass`, `fail`

Example:
```bash
~/.agents/bin/emit-telemetry compliance.check feature-workflow 2 "Spec Gate" spec_exists_and_reviewed pass "Spec exists, complete, and human-reviewed."
```

---

### `skill.completed`

Emitted at the final phase of the skill, after all phases are done and the plan is closed.

```bash
~/.agents/bin/emit-telemetry skill.completed <skill> <outcome> "<detail>"
```

Example:
```bash
~/.agents/bin/emit-telemetry skill.completed feature-workflow success "All phases passed."
```

---

## When to Emit

| Event | When |
|---|---|
| `skill.invoked` | SKILL.md On Invocation section, before loading any phase step file |
| `phase.started` | Top of every step file, first action before reading any plan or writing any content |
| `phase.completed` | End of every step file, after the checkpoint, before loading the next step |
| `compliance.check` | Any step file that explicitly evaluates a rule: Iron Law checks, gate conditions, coverage results, audit outcomes |
| `skill.completed` | Final step file only, after plan closure and commit |

---

## Emission Is Mandatory

Telemetry emission is not optional and is not skipped for short or simple phases. The value of the log comes from completeness -- a missing event is indistinguishable from a phase that was skipped.

**If emission fails, stop and diagnose before continuing.** Do not proceed with the next step until the emission failure is resolved. A telemetry gap in Experiment 2 data degrades the diagnostic value of the entire run.

---

## Relationship to ACMCP

When the Adversarial Compliance MCP is implemented, it will produce a richer event stream as a structural product of the gate chain -- `begin_workflow_step` and `audit_workflow_step` will emit events directly, with full artifact and violation detail. At that point this advisory telemetry layer will be superseded for gated workflows. It will continue to apply for skills and workflow phases that run outside the ACMCP gate.
