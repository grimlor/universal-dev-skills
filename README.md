# Universal Dev Skills

Portable, agent-agnostic skills that enforce development discipline — spec-before-code, BDD testing, plan-first workflows — across any project and any AI coding agent.

## What This Is

A collection of [Agent Skills](https://agentskills.io/) that establish consistent development practices with AI coding agents. Each skill encodes domain knowledge — from how to write tests to how to format commit messages — using the open Agent Skills standard (`SKILL.md` + YAML frontmatter + Markdown).

The enforcement model is the key design choice: the `skill-compliance` skill makes the agent explicitly acknowledge which skills it loaded before touching anything, making non-compliance observable rather than silent.

## Skills Included

| Skill | Purpose |
|-------|---------|
| **skill-compliance** | Pre-task checklist — ensures all relevant skills are loaded before work begins |
| **tool-usage** | VS Code tool-first approach — when to use tools vs. terminal commands |
| **bdd-testing** | BDD test conventions — system specification, not unit testing |
| **bdd-feedback-loop** | Per-module test implementation procedure — spec to clean output |
| **feature-workflow** | Spec-before-code development — 5-phase lifecycle from planning to status update |
| **conventional-commits** | Commit message format following Conventional Commits v1.0.0 |
| **plan-updates** | Progress tracking in project plan and BDD specification artifacts |

## Agent Compatibility

These skills work with multiple AI coding agents. The skill content (Markdown + YAML frontmatter) follows the [Agent Skills specification](https://agentskills.io/specification) and is fully portable. What differs is how each agent discovers and loads them.

| Agent | Skills (SKILL.md) | AGENTS.md | Setup Guide |
|-------|-------------------|-----------|-------------|
| **GitHub Copilot** (VS Code) | Native support | Native support | [Setup guide](docs/vscode-copilot.md) |
| **Cursor** | Via rules conversion | Native support | [Setup guide](docs/cursor.md) |
| **Windsurf** | Native support | Native support | [Setup guide](docs/windsurf.md) |
| **Claude Code** | Native support | Via CLAUDE.md | [Setup guide](docs/claude-code.md) |

**AGENTS.md** is the one format recognized by all four agents. If you need a single-file approach that works everywhere, start there.

## Quick Start

### Option 1 — Clone and point your editor to it (recommended)

Clone this repo once, then configure your editor to read skills from the cloned directory. This means every workspace automatically gets the skills with zero per-project setup.

See the setup guide for your agent: [VS Code/Copilot](docs/vscode-copilot.md) · [Cursor](docs/cursor.md) · [Windsurf](docs/windsurf.md) · [Claude Code](docs/claude-code.md)

### Option 2 — Copy into a repository

Copy the skills and instructions into a project's expected directory:

```bash
# For VS Code / GitHub Copilot
mkdir -p /path/to/your-repo/.github
cp -r skills/ /path/to/your-repo/.github/skills/
cp -r instructions/ /path/to/your-repo/.github/instructions/
cp -r agents/vscode/ /path/to/your-repo/.github/agents/

# For Windsurf
mkdir -p /path/to/your-repo/.windsurf
cp -r skills/ /path/to/your-repo/.windsurf/skills/

# For Cursor (see setup guide for rules conversion)
```

### Option 3 — MCP package distribution

Skills can be bundled inside an MCP server package and auto-installed into workspaces on server startup. See the [VS Code/Copilot setup guide](docs/vscode-copilot.md#mcp-package-distribution) for the pattern.

## Repo Structure

```
universal-dev-skills/
├── instructions/           # Entry-point instruction files
│   └── copilot-instructions.md
├── skills/                 # Agent Skills (SKILL.md per skill)
│   ├── skill-compliance/
│   ├── tool-usage/
│   ├── bdd-testing/
│   ├── bdd-feedback-loop/
│   ├── feature-workflow/
│   ├── conventional-commits/
│   └── plan-updates/
├── agents/                 # Custom agent definitions — one folder per platform
│   └── vscode/
│       └── dev.agent.md
└── docs/                   # Per-agent setup guides
```

The `agents/` directory is organized by platform so that editor settings can point to a specific subdirectory (e.g., `agents/vscode/`) without picking up agents meant for other tools. Contributions for other IDEs are welcome — add a new subdirectory (e.g., `agents/cursor/`, `agents/windsurf/`).

## Skill Format

Each skill follows the [Agent Skills specification](https://agentskills.io/specification). At minimum, a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-skill
description: "When to use this skill and what it covers."
---

# Skill Title

## When This Skill Applies
...
```

Skills may include a `references/` subdirectory with detailed examples and supplementary documentation. The agent loads the `name` and `description` at startup (lightweight), then loads the full `SKILL.md` body only when it decides the skill is relevant (progressive disclosure).

## Adding Repo-Specific Skills

These universal skills cover general development workflow. For domain-specific knowledge (e.g., project-specific scoring models, config schemas, pipeline architectures), create additional skills in your project's skills directory following the same format.

## Design Principles

- **Universal** — No references to specific repos, packages, or domain objects
- **Opinionated** — Encodes a specific workflow (spec → test → implement → verify)
- **Self-reinforcing** — Skills cross-reference each other to form a coherent system
- **Portable** — Works across multiple AI agents via the Agent Skills standard
- **Observable** — `skill-compliance` makes the agent declare what it loaded, so you can verify before work begins

## License

[MIT](LICENSE)
