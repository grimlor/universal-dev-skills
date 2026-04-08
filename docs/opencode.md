# Setup — OpenCode

OpenCode has native support for the Agent Skills specification (`SKILL.md`), `AGENTS.md`, and Claude Code compatibility paths. It reads skills from multiple directories and supports global configuration at `~/.config/opencode/`.

## What Works Directly

| UDS Component | OpenCode Support | Notes |
|---|---|---|
| Skills (`SKILL.md`) | Yes | Native support, same spec as agentskills.io |
| `AGENTS.md` | Yes | Project root + global (`~/.config/opencode/AGENTS.md`) |
| Instructions (`.instructions.md`) | No | Use `AGENTS.md` or `opencode.json` `instructions` |
| Agents (`.agent.md`) | Yes | Via `.opencode/agents/` or `~/.config/opencode/agents/` |

## Quick Start

### Option A — Copy skills into workspace

```bash
mkdir -p /path/to/your-repo/.opencode/skills
cp -r skills/ /path/to/your-repo/.opencode/skills/
```

### Option B — Global skills directory

OpenCode reads global skills from `~/.config/opencode/skills/`. Symlink or copy:

```bash
for skill in ~/universal-dev-skills/skills/*/; do
  ln -s "$skill" ~/.config/opencode/skills/$(basename "$skill")
done
```

Global skills are available in all workspaces.

### Option C — Claude Code compatibility

OpenCode also scans Claude Code paths as fallbacks:

- `.claude/skills/` (workspace)
- `~/.claude/skills/` (global)

If you already have Claude Code set up, OpenCode will discover the same skills automatically.

## How Skills Work in OpenCode

OpenCode follows the same progressive disclosure model as the Agent Skills spec:

1. **Discovery** — Skill `name` and `description` from frontmatter are indexed at startup.
2. **Invocation** — The full `SKILL.md` content is loaded when the description matches the current task.
3. **Resources** — Supporting files (references, scripts) are loaded only when needed.

## Skill Locations

| Scope | Path | Notes |
|---|---|---|
| Workspace | `.opencode/skills/` | Committed with your repo |
| Claude compat | `.claude/skills/` | Fallback path, also scanned |
| Cross-agent compat | `.agents/skills/` | Also scanned automatically |
| Global | `~/.config/opencode/skills/` | All workspaces on your machine |
| Global (Claude) | `~/.claude/skills/` | Fallback, also scanned |

## AGENTS.md

OpenCode reads `AGENTS.md` from:
- **Project root** — always-on instructions for the workspace
- **`~/.config/opencode/AGENTS.md`** — global instructions for all workspaces

It also reads Claude Code's equivalent:
- **`CLAUDE.md`** and **`.claude/CLAUDE.md`** in the workspace root

## Custom Instructions via opencode.json

OpenCode supports custom instructions in its config file (`opencode.json` or `.opencode/config.json`):

```json
{
  "instructions": [
    "Before starting any task, read and follow the skill-compliance skill."
  ]
}
```

Each entry in the `instructions` array is prepended to every conversation.

## Agent Files

OpenCode supports custom agents as markdown files:

| Scope | Path |
|---|---|
| Workspace | `.opencode/agents/` |
| Global | `~/.config/opencode/agents/` |

Agent files follow the same markdown format with YAML frontmatter.

## Memory & Context Persistence

OpenCode does not have a built-in memory tool or persistent note system like VS Code Copilot. Context persistence relies on:

- **`AGENTS.md`** — Re-read from disk at the start of every session. The global `~/.config/opencode/AGENTS.md` is always loaded, making it the most reliable anchor for skill-recall instructions.
- **`opencode.json` instructions** — Loaded every session from config.
- **CLAUDE.md compatibility** — If you use Claude Code's memory paths (`.claude/CLAUDE.md`, `~/.claude/CLAUDE.md`), OpenCode reads those too.
- **No auto-memory** — Unlike Windsurf (which writes `~/.codeium/windsurf/memories/`) or Claude Code (which writes `~/.claude/projects/<proj>/memory/`), OpenCode does not automatically persist conversation insights.

### Skill-recall after context compaction

To ensure skills are re-read after context compaction, the global `AGENTS.md` should include:

```
Before starting any task, read and follow the skill-compliance skill.
```

The `skill-compliance` skill includes an unconditional reload instruction (Step 8) that forces re-reading of all active skills before starting work.

## Cross-Compatibility

OpenCode is designed for Claude Code compatibility. If you already have a Claude Code setup, most paths work out of the box:

| Claude Code Path | OpenCode Reads It? |
|---|---|
| `.claude/skills/` | Yes |
| `.claude/CLAUDE.md` | Yes |
| `~/.claude/skills/` | Yes |
| `~/.claude/CLAUDE.md` | Yes |
| `.claude/rules/` | No — use `AGENTS.md` instead |
| `.claude/agents/` | No — use `.opencode/agents/` |

## Limitations

- **No `.instructions.md` support** — Use `AGENTS.md` or `opencode.json` instructions.
- **No rules system** — Unlike Windsurf (rules with triggers) or Cursor (rules with globs), OpenCode relies on `AGENTS.md` and config-level instructions.
- **No persistent memory** — No built-in mechanism to save and recall notes across sessions.
- **No external directory setting** — Unlike VS Code's `chat.agentSkillsLocations`, discovery paths are fixed. Use global config directories or workspace-level copies.
