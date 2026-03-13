# Setup — Cursor

Cursor supports rules (`.cursor/rules/`) and `AGENTS.md`, but does **not** natively support the Agent Skills specification (`SKILL.md`). Skills need to be adapted into Cursor's rules format.

## What Works Directly

| UDS Component | Cursor Support | Notes |
|---|---|---|
| `AGENTS.md` | Yes | Root + subdirectories supported |
| Skills (`SKILL.md`) | No | Must be converted to Cursor rules |
| Instructions (`.instructions.md`) | No | Must be converted to Cursor rules |
| Agents (`.agent.md`) | No | Cursor has no custom agent concept |

## Quick Start with AGENTS.md

The simplest path is to use `AGENTS.md`, which Cursor supports natively:

1. Copy or create an `AGENTS.md` file in your project root with the key instructions from your skills.
2. Cursor treats root-level `AGENTS.md` as always-on instructions.
3. Subdirectory `AGENTS.md` files apply when working in those directories.

## Converting Skills to Cursor Rules

Each skill can be converted to a Cursor rule file in `.cursor/rules/`.

### Rule format

Cursor rules are Markdown files (`.md` or `.mdc`) in `.cursor/rules/`. The `.mdc` format supports frontmatter:

```markdown
---
description: "When to use this rule and what it covers."
globs: "**/*.py"
alwaysApply: false
---

# Rule content here...
```

### Activation modes

| Mode | Frontmatter | Behavior |
|---|---|---|
| Always Apply | `alwaysApply: true` | Applied to every chat session |
| Apply Intelligently | `alwaysApply: false` + `description` | Agent decides based on description |
| Specific Files | `globs: "**/*.py"` | Applied when matching files are in context |
| Manual | No `alwaysApply`, no `globs` | Only when `@rule-name` is mentioned |

### Recommended conversion

| UDS Skill | Cursor Rule | Activation |
|---|---|---|
| `skill-compliance` | `.cursor/rules/skill-compliance.mdc` | Always Apply |
| `tool-usage` | `.cursor/rules/tool-usage.mdc` | Always Apply |
| `bdd-testing` | `.cursor/rules/bdd-testing.mdc` | Apply Intelligently |
| `bdd-feedback-loop` | `.cursor/rules/bdd-feedback-loop.mdc` | Apply Intelligently |
| `feature-workflow` | `.cursor/rules/feature-workflow.mdc` | Apply Intelligently |
| `conventional-commits` | `.cursor/rules/conventional-commits.mdc` | Apply Intelligently |
| `plan-updates` | `.cursor/rules/plan-updates.mdc` | Apply Intelligently |

For each skill, copy the `SKILL.md` body into a `.mdc` file and adapt the frontmatter:

```markdown
---
description: "BDD test conventions — system specification, not unit testing. Use when writing, modifying, or reviewing test files."
alwaysApply: false
---

# BDD Testing Conventions
...
```

### Creating rules via chat

Cursor also supports generating rules via the `/create-rule` command in Agent mode.

## Remote Rules via GitHub

Cursor can import rules directly from a GitHub repository:

1. Open **Cursor Settings → Rules, Commands**
2. Click **+ Add Rule** → **Remote Rule (Github)**
3. Paste the repository URL

Imported rules auto-sync with the source repository. This could be a distribution path, but note that it imports rules — not SKILL.md files — so the skills would need to be restructured as rules in a separate branch or directory if you want to use this mechanism.

## User Rules

Cursor supports global user rules defined in **Cursor Settings → Rules**. These are plain text, applied to all projects. Use this for personal preferences that don't need the full skill structure.

## Team Rules

On Team and Enterprise plans, administrators can create and enforce rules from the Cursor dashboard. Team rules take precedence over project and user rules.

## Limitations

- **No SKILL.md support** — Cursor does not follow the Agent Skills specification or support progressive disclosure (loading name/description first, then full content on demand).
- **No external directory setting** — Unlike VS Code's `chat.agentSkillsLocations`, there is no way to point Cursor at an external cloned directory. Each project needs its own `.cursor/rules/` copy, or you can use remote GitHub rules.
- **No custom agents** — Cursor does not have an equivalent to VS Code's `.agent.md` custom agent definitions.
- **Rule size** — Rules should be kept under 500 lines for best results.

## Skill Applicability Notes

The `tool-usage` skill references VS Code-specific tools (`get_errors`, `runTests`, `replace_string_in_file`, etc.). Cursor is VS Code-based and provides equivalent tooling, so the principles apply — but the exact tool names and invocation patterns may differ. When converting `tool-usage` to a Cursor rule, adapt the tool references to match Cursor's agent capabilities.
