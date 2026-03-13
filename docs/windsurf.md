# Setup — Windsurf

Windsurf has native support for the Agent Skills specification (`SKILL.md`), `AGENTS.md`, and its own rules system. It also scans cross-agent compatibility paths (`.agents/skills/`), making it one of the most compatible targets for these skills.

## What Works Directly

| UDS Component | Windsurf Support | Notes |
|---|---|---|
| Skills (`SKILL.md`) | Yes | Native support, follows agentskills.io spec |
| `AGENTS.md` | Yes | Root = always-on, subdirectory = auto-glob scoping |
| Instructions (`.instructions.md`) | No | Use Windsurf rules instead |
| Agents (`.agent.md`) | No | Windsurf does not have custom agent modes |

## Quick Start

### Option A — Copy skills into workspace

```bash
mkdir -p /path/to/your-repo/.windsurf
cp -r skills/ /path/to/your-repo/.windsurf/skills/
```

Windsurf also scans `.agents/skills/` for cross-agent compatibility, so you can alternatively use:

```bash
mkdir -p /path/to/your-repo/.agents
cp -r skills/ /path/to/your-repo/.agents/skills/
```

### Option B — Global skills directory

Windsurf reads global skills from `~/.codeium/windsurf/skills/`. Symlink or copy:

```bash
for skill in ~/universal-dev-skills/skills/*/; do
  ln -s "$skill" ~/.codeium/windsurf/skills/$(basename "$skill")
done
```

Global skills are available in all workspaces on your machine.

### Option C — Use AGENTS.md

Create an `AGENTS.md` in your project root with the key instructions. Windsurf processes it through the same rules engine — root-level files are always-on, subdirectory files are auto-scoped.

## How Skills Work in Windsurf

Windsurf follows the progressive disclosure model from the Agent Skills spec:

1. **Discovery** — Only the skill's `name` and `description` are loaded at startup.
2. **Invocation** — Cascade reads the full `SKILL.md` content when it decides the description is relevant.
3. **Resources** — Supporting files (scripts, references) are loaded only when needed.

Skills can be invoked automatically (based on description matching) or manually via `@skill-name` in the Cascade input.

## Skill Locations

| Scope | Path | Notes |
|---|---|---|
| Workspace | `.windsurf/skills/` | Committed with your repo |
| Cross-agent compat | `.agents/skills/` | Also scanned automatically |
| Global | `~/.codeium/windsurf/skills/` | All workspaces on your machine |
| System (Enterprise) | OS-specific (see below) | Deployed by IT, read-only |

Enterprise system paths:
- macOS: `/Library/Application Support/Windsurf/skills/`
- Linux/WSL: `/etc/windsurf/skills/`
- Windows: `C:\ProgramData\Windsurf\skills\`

## Converting Instructions to Windsurf Rules

The `instructions/copilot-instructions.md` entry point is VS Code-specific. For Windsurf, the equivalent is a workspace rule:

Create `.windsurf/rules/skill-compliance.md`:

```markdown
---
trigger: always_on
---

Before starting any task, read and follow the skill-compliance skill.
```

### Windsurf rule activation modes

| Mode | `trigger` value | Behavior |
|---|---|---|
| Always On | `always_on` | Included in every message |
| Model Decision | `model_decision` | Description shown; full content loaded on demand |
| Glob | `glob` | Applied when matching files are touched |
| Manual | `manual` | Only when `@rule-name` is used |

## Windsurf vs VS Code Comparison

| Feature | VS Code / Copilot | Windsurf |
|---|---|---|
| Skills path | `.github/skills/` | `.windsurf/skills/` or `.agents/skills/` |
| Instructions | `.github/instructions/*.instructions.md` | `.windsurf/rules/*.md` |
| Custom agents | `.github/agents/*.agent.md` | Not supported |
| External dir config | `chat.agentSkillsLocations` setting | Global path only (`~/.codeium/windsurf/skills/`) |
| Always-on instructions | `.github/copilot-instructions.md` | Root `AGENTS.md` or `trigger: always_on` rule |
| AGENTS.md | Supported | Supported (same scoping behavior) |

## Limitations

- **No external directory setting** — Unlike VS Code, you cannot add arbitrary paths for skill discovery. Use the global directory or workspace copy.
- **No custom agents** — Windsurf does not have an equivalent to `.agent.md` files for defining custom personas with tool restrictions.
- **Rule size** — Workspace rules are limited to 12,000 characters per file. Global rules are limited to 6,000 characters.
- **No `.instructions.md` support** — Use Windsurf rules for the equivalent functionality.

## Skill Applicability Notes

The `tool-usage` skill references VS Code-specific tools (`get_errors`, `runTests`, `replace_string_in_file`, etc.). Windsurf is VS Code-based, and Cascade has access to equivalent file editing and terminal tools, so the tool-first principles apply. The specific tool names referenced in the skill should work in Windsurf's agent context.
