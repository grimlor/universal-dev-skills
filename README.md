# Universal Dev Skills

Portable, agent-agnostic skills that enforce development discipline — spec-before-code, BDD testing, plan-first workflows — across any project and any AI coding agent.

## What This Is

A collection of [Agent Skills](https://agentskills.io/) that establish consistent development practices with AI coding agents. Each skill encodes domain knowledge — from how to write tests to how to format commit messages — using the open Agent Skills standard (`SKILL.md` + YAML frontmatter + Markdown).

The enforcement model is the key design choice: the `skill-compliance` skill makes the agent explicitly acknowledge which skills it loaded before touching anything, making non-compliance observable rather than silent.

## Skills Included

### Workflow Skills (language-agnostic)

These skills define processes and decision rules. They apply regardless of language and delegate language-specific details to `references/` files.

| Skill | Purpose |
|-------|---------|
| **skill-compliance** | Pre-task routing — identifies the task type, work surface, and languages in scope, then loads the right skills and references |
| **tool-usage** | VS Code tool-first approach — when to use tools vs. terminal commands |
| **bdd-testing** | BDD test conventions — system specification, not unit testing |
| **bdd-feedback-loop** | Per-module test implementation procedure — spec to clean output |
| **feature-workflow** | Spec-before-code development — 5-phase lifecycle from planning to status update |
| **conventional-commits** | Commit message format following Conventional Commits v1.0.0 |
| **plan-updates** | Progress tracking in project plan and BDD specification artifacts |
| **code-quality-antipatterns** | Suppression pragma policy — prevents autonomous type-ignore, noqa, pragma no-cover (cross-cutting) |

### Language Standards Skills

These skills define toolchain configuration, linting, formatting, coverage thresholds, and documentation standards for a specific language ecosystem.

| Skill | Ecosystem |
|-------|-----------|
| **python-code-standards** | Ruff, Pyright, pytest, pyproject.toml |
| **typescript-code-standards** | ESLint (flat config), TypeScript strict mode, Jest |
| **java-code-standards** | Checkstyle, SpotBugs, Spotless, Gradle, JUnit 5 |
| **csharp-code-standards** | Roslyn analyzers, .editorconfig, dotnet CLI, xUnit |

Java and C# standards are forward-looking — authored before live projects exist in the workspace. They will be refined when real project usage begins.

### Language References

Workflow skills use a `references/` subdirectory for language-specific details. The agent loads the right reference based on the files being edited.

| Skill | References |
|-------|------------|
| **bdd-testing** | `python.md`, `typescript.md`, `java.md`, `csharp.md`, `test-patterns.md` |
| **bdd-feedback-loop** | `python.md`, `typescript.md`, `java.md`, `csharp.md` |
| **tool-usage** | `python.md`, `typescript.md`, `java.md`, `csharp.md` |

`skill-compliance` routes by file extension and nearest manifest file (`pyproject.toml`, `package.json`, `pom.xml`, `build.gradle*`, `.csproj`) to determine which language skills and references to load.

## Agent Compatibility

These skills work with multiple AI coding agents. The skill content (Markdown + YAML frontmatter) follows the [Agent Skills specification](https://agentskills.io/specification) and is fully portable. What differs is how each agent discovers and loads them.

| Agent | Skills (SKILL.md) | AGENTS.md | Setup Guide |
|-------|-------------------|-----------|-------------|
| **GitHub Copilot** (VS Code) | Native support | Native support | [Setup guide](docs/vscode-copilot.md) |
| **GitHub Copilot CLI** | Native support | Native support | [Setup guide](docs/vscode-copilot.md) |
| **Cursor** | Via rules conversion | Native support | [Setup guide](docs/cursor.md) |
| **Windsurf** | Native support | Native support | [Setup guide](docs/windsurf.md) |
| **Claude Code** | Native support | Via CLAUDE.md | [Setup guide](docs/claude-code.md) |
| **OpenCode** | Native support | Native support | [Setup guide](docs/opencode.md) |

**AGENTS.md** is the one format recognized by all six agents. If you need a single-file approach that works everywhere, start there.

## Quick Start

### Option 1 — Clone and run the setup script (recommended)

Clone this repo once, then run the setup script for your agent:

```bash
git clone https://github.com/grimlor/universal-dev-skills.git ~/universal-dev-skills
cd ~/universal-dev-skills

# Pick your target (or use "all" for everything)
python3 scripts/setup.py --target vscode       # VS Code / GitHub Copilot
python3 scripts/setup.py --target copilot-cli   # GitHub Copilot CLI
python3 scripts/setup.py --target claude        # Claude Code
python3 scripts/setup.py --target windsurf      # Windsurf
python3 scripts/setup.py --target opencode      # OpenCode
python3 scripts/setup.py --target cursor \       # Cursor (per-workspace)
  --workspace /path/to/your-project
python3 scripts/setup.py --target all           # all of the above (except cursor)
```

Use `--dry-run` to preview changes without writing anything. Run `--help` for full usage.

The Cursor target converts SKILL.md files to `.cursor/rules/*.mdc` and requires `--workspace` to specify the project directory. The `all` target includes Cursor only when `--workspace` is provided.

For manual setup, see the per-agent guides: [VS Code/Copilot](docs/vscode-copilot.md) · [Cursor](docs/cursor.md) · [Windsurf](docs/windsurf.md) · [Claude Code](docs/claude-code.md) · [OpenCode](docs/opencode.md)

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

## Updating

If you cloned the repo and ran the setup script (Option 1), pull the latest changes:

```bash
cd ~/universal-dev-skills
git pull
```

Whether `git pull` is sufficient depends on how your agent was set up:

| Agent | `git pull` sufficient? | Notes |
|-------|------------------------|-------|
| **VS Code / Copilot** | ✅ Yes | Symlinks point at repo; changes flow through automatically |
| **Copilot CLI** | ✅ Yes | Symlinks point at repo |
| **Claude Code** | ✅ Skills only | New entry points (e.g., `CLAUDE.md`) require re-running setup |
| **Windsurf** | ✅ Skills only | Workspace rules (`.windsurf/rules/`) are manual per-workspace |
| **OpenCode** | ✅ Skills only | New entry points (e.g., `AGENTS.md`) require re-running setup |
| **Cursor** | ❌ Re-run setup | Rules are copied and converted, not symlinked |

For agents that need a re-run, use the same command as initial setup:

```bash
python3 scripts/setup.py --target <agent>         # re-run for your agent
python3 scripts/setup.py --target <agent> --dry-run  # preview first
```

The setup script is idempotent — it will skip existing symlinks and only create missing files.

## Repo Structure

```
universal-dev-skills/
├── instructions/                    # Entry-point instruction files
│   └── copilot-instructions.md
├── skills/                          # Agent Skills (SKILL.md per skill)
│   ├── skill-compliance/            # Polyglot routing — always loaded first
│   ├── tool-usage/                  # Tool-vs-terminal decisions
│   │   └── references/              #   python.md, typescript.md, java.md, csharp.md
│   ├── bdd-testing/                 # Test quality conventions
│   │   └── references/              #   python.md, typescript.md, java.md, csharp.md
│   ├── bdd-feedback-loop/           # Per-module test implementation loop
│   │   └── references/              #   python.md
│   ├── feature-workflow/            # Spec-before-code lifecycle
│   ├── conventional-commits/        # Commit message format
│   ├── plan-updates/                # Progress tracking
│   ├── code-quality-antipatterns/   # Suppression pragma policy (cross-cutting)
│   ├── python-code-standards/       # Ruff + Pyright + pytest config
│   ├── typescript-code-standards/   # ESLint + tsc + Jest config
│   ├── java-code-standards/         # Checkstyle + SpotBugs + Gradle config
│   └── csharp-code-standards/       # Roslyn + .editorconfig + dotnet config
├── hooks/                           # PreToolUse hooks enforcing tool-usage skill
│   ├── enforce-tool-usage.json      #   Hook configuration (VS Code / Copilot CLI)
│   └── enforce-tool-usage.sh        #   Shell script matching blocked commands
├── scripts/                         # Setup automation
│   └── setup.py                     #   Multi-target installer (vscode, claude, windsurf, copilot-cli, cursor, opencode)
├── agents/                          # Custom agent definitions — one folder per platform
│   └── vscode/
│       └── dev.agent.md
└── docs/                            # Per-agent setup guides
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

### Language references

Skills that apply across multiple languages use a `references/` subdirectory for language-specific details:

```
skills/bdd-testing/
├── SKILL.md                  # Language-agnostic test conventions
└── references/
    ├── python.md             # pytest / coverage patterns
    ├── typescript.md         # Jest / ts-jest patterns
    ├── java.md               # JUnit 5 / AssertJ / Mockito patterns
    └── csharp.md             # xUnit / FluentAssertions / Moq patterns
```

The agent loads the `name` and `description` at startup (lightweight), then loads the full `SKILL.md` body only when it decides the skill is relevant (progressive disclosure). Language references are loaded based on which files are being edited — `skill-compliance` handles this routing.

## Adding Repo-Specific Skills

These universal skills cover general development workflow. For domain-specific knowledge (e.g., project-specific scoring models, config schemas, pipeline architectures), create additional skills in your project's skills directory following the same format.

## Design Principles

- **Polyglot** — Workflow skills are language-agnostic; language-specific details live in references and standards skills (Python, TypeScript, Java, C#)
- **Opinionated** — Encodes a specific workflow (spec → test → implement → verify) with strict toolchain defaults (100% coverage, warnings-as-errors)
- **Self-reinforcing** — Skills cross-reference each other to form a coherent system; `skill-compliance` routes to the right combination
- **Portable** — Works across multiple AI agents via the Agent Skills standard
- **Observable** — `skill-compliance` makes the agent declare what it loaded, so you can verify before work begins

## License

[MIT](LICENSE)
