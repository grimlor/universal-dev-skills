# Setup — Claude Code

Claude Code supports skills via `.claude/skills/`, instructions via `.claude/rules/`, and its own `CLAUDE.md` for always-on instructions. VS Code also reads Claude-format files when `chat.useClaudeMdFile` is enabled, so these formats work in both environments.

## What Works Directly

| UDS Component | Claude Code Support | Notes |
|---|---|---|
| Skills (`SKILL.md`) | Yes | Via `.claude/skills/` directory |
| `AGENTS.md` | Via `CLAUDE.md` | Claude Code uses `CLAUDE.md` as its equivalent |
| Instructions (`.instructions.md`) | Yes | Via `.claude/rules/` (uses `paths` instead of `applyTo`) |
| Agents (`.agent.md`) | Yes | Via `.claude/agents/` |

## Quick Start

### Option A — Copy skills into workspace

```bash
mkdir -p /path/to/your-repo/.claude/skills
cp -r skills/ /path/to/your-repo/.claude/skills/
```

### Option B — User-level skills

Claude Code reads user-level skills from `~/.claude/skills/`:

```bash
for skill in ~/universal-dev-skills/skills/*/; do
  ln -s "$skill" ~/.claude/skills/$(basename "$skill")
done
```

### Option C — CLAUDE.md as entry point

Create a `CLAUDE.md` in your project root as the always-on instruction equivalent:

```markdown
Before starting any task, read and follow the skill-compliance skill.
```

Claude Code discovers `CLAUDE.md` in these locations:
- Workspace root: `CLAUDE.md`
- `.claude` folder: `.claude/CLAUDE.md`
- User home: `~/.claude/CLAUDE.md`
- Local variant: `CLAUDE.local.md` (not committed to version control)

## Instructions as Claude Rules

Claude Code uses `.claude/rules/` for file-scoped instructions. These follow a format similar to VS Code's `.instructions.md` but use `paths` (an array of glob patterns) instead of `applyTo`:

```markdown
---
name: 'Python Standards'
description: 'Coding conventions for Python files'
paths:
  - '**/*.py'
---

# Python coding standards
- Follow PEP 8.
- Use type hints for all function signatures.
```

When `paths` is omitted, the rule defaults to `**` (all files).

## Claude Agent Files

Claude Code supports sub-agents via `.claude/agents/`. VS Code also detects these files when the Claude format is enabled. The Claude agent format uses slightly different frontmatter:

```markdown
---
name: Dev
description: Daily development agent
tools: "Read, Grep, Glob, Bash"
---

Agent instructions here...
```

Note that Claude uses comma-separated strings for the `tools` field, while VS Code uses YAML arrays. VS Code maps Claude-specific tool names to their VS Code equivalents automatically.

## Cross-Compatibility with VS Code

VS Code reads Claude-format files alongside its native formats:

| Claude Path | VS Code Equivalent | Setting |
|---|---|---|
| `.claude/skills/` | `.github/skills/` | Included in `chat.agentSkillsLocations` by default |
| `.claude/rules/` | `.github/instructions/` | Included in `chat.instructionsFilesLocations` by default |
| `.claude/agents/` | `.github/agents/` | Included in `chat.agentFilesLocations` by default |
| `CLAUDE.md` | `copilot-instructions.md` | Controlled by `chat.useClaudeMdFile` |

This means you can use Claude-format paths and have them work in both Claude Code and VS Code/Copilot.

## Limitations

- **Different entry point** — Claude Code uses `CLAUDE.md` rather than `copilot-instructions.md` or `AGENTS.md`. If you need both, create both files.
- **`paths` vs `applyTo`** — Claude rules use `paths` (array of globs) for file scoping; VS Code uses `applyTo` (single glob string). VS Code handles both formats, but Claude Code only reads `paths`.
- **Tool naming** — Claude Code uses its own tool names (`Read`, `Grep`, `Bash`, etc.) rather than VS Code tool identifiers. VS Code maps these automatically, but the reverse is not guaranteed.

## Skill Applicability Notes

The `tool-usage` skill is VS Code-specific. It references VS Code tools (`get_errors`, `runTests`, `replace_string_in_file`, Pylance, Ruff extensions, etc.) that do not exist in the Claude Code environment. Claude Code uses its own tool set (`Read`, `Write`, `Bash`, `Grep`, `Glob`, etc.).

When using these skills with Claude Code, the `tool-usage` skill should be **excluded** during the skill-compliance step. The underlying principles — prefer structured tools over raw shell commands, validate after edits, run type checks and linters — still apply, but the specific tool mappings do not transfer. Adapt the verification steps to use Claude Code's `Bash` tool with `pyright`, `pytest`, and your project's linter directly.
