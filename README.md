# Universal Dev Skills

Standardized, repo-agnostic GitHub Copilot skills for consistent AI-assisted development workflows.

## What This Is

A portable collection of `.github/skills/` that can be copied into any repository to establish consistent development practices with GitHub Copilot. Each skill encodes domain knowledge that guides Copilot's behavior — from how to write tests to how to format commit messages.

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

## Usage

### Copy into a repository

```bash
cp -r .github/ /path/to/your-repo/.github/
```

### Add the entry point

The `.github/copilot-instructions.md` file tells Copilot to read the skill-compliance skill first, which then orchestrates loading the other skills as needed.

### Add repo-specific skills

These universal skills cover general development workflow. For domain-specific knowledge (e.g., project-specific scoring models, config schemas, pipeline architectures), create additional skills in your repo's `.github/skills/` directory following the same YAML frontmatter + Markdown format.

## Skill Format

Each skill is a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: my-skill
description: "When to use this skill and what it covers."
---

# Skill Title

## When This Skill Applies
...
```

Skills may include a `references/` subdirectory with detailed examples and supplementary documentation.

## Design Principles

- **Universal** — No references to specific repos, packages, or domain objects
- **Opinionated** — Encodes a specific workflow (spec → test → implement → verify)
- **Self-reinforcing** — Skills cross-reference each other to form a coherent system
- **Portable** — Drop into any Python project using pytest; adaptable to other stacks

## License

[MIT](LICENSE)
