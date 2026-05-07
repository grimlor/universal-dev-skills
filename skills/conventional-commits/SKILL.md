---
name: conventional-commits
description: "Commit message format rules. Use whenever staging, committing, or describing changes -- including when the user asks to commit, when preparing a PR, or when writing a changelog entry.
NOTE: Never commit autonomously. Always prepare a message and ask for user approval before committing."
---

# Conventional Commits -- Message Format

## Iron Laws

1. **Never commit autonomously.** Show the staged diff and the proposed message; wait for explicit user approval before executing the commit. Reformatting hooks may modify files mid-commit -- that is not approval to keep going on a different commit.
2. **Every commit gets a type.** No untyped commits. Subject line is `<type>[optional scope]: <description>`.
3. **One logical change per commit.** Don't bundle a feature with a refactor; don't sweep unrelated files in with `git add -u`. Stage the specific paths you intend to ship.
4. **`feat` and `fix` are the only version-bumping types.** Mark breaking changes with `!` after the type/scope or a `BREAKING CHANGE:` footer (equivalent; both trigger a major bump).
5. **Subject line is imperative, lowercase after the colon, no trailing period, ≤72 chars.** Body wraps at 72 and explains _what_ and _why_, not _how_.
6. **Re-stage after auto-formatting hooks; reuse the original message.** Hook reformat → reject → re-stage → retry is the normal workflow, not a new commit.

## When This Skill Applies

Whenever writing a commit message, PR title, or changelog entry. This includes interactive commits, automated commits, and squash-merge titles.

This skill defines **message format only.** For how to execute git operations (staging, committing, pushing), follow `tool-usage` -- it determines whether to use GitKraken MCP tools, GitHub MCP tools, or terminal commands based on what is available.

## Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | Meaning | Version bump |
| --- | --- | --- |
| `feat` | New feature or capability | **minor** (0.1.0 → 0.2.0) |
| `fix` | Bug fix | **patch** (0.1.0 → 0.1.1) |
| `docs` | Documentation only | none |
| `style` | Formatting, whitespace, semicolons | none |
| `refactor` | Code change that neither fixes nor adds | none |
| `perf` | Performance improvement | none |
| `test` | Adding or correcting tests | none |
| `build` | Build system, dependencies, CI config | none |
| `ci` | CI pipeline changes | none |
| `chore` | Maintenance tasks (tooling, config) | none |
| `revert` | Reverts a previous commit | depends on reverted type |

### Scope

Optional. Narrows the area of change to a module or subsystem name (`auth`, `api`, `models`, `cli`, `config`, `deps`, `release`). Scopes should be short, stable, and map to subsystems or directories.

### Description

Imperative mood ("add", "fix", "remove" -- not "added", "fixes", "removed"). Lowercase first letter after the colon. No trailing period. ≤72 chars including type and scope.

### Body

Optional. Wrap at 72. Explain _what_ and _why_, not _how_.

### Footers

- `BREAKING CHANGE: <description>` -- triggers major bump
- `Refs: #123` -- links to an issue
- `Co-authored-by: Name <email>` -- attribution

### Squash-merge PRs

The PR title becomes the squash commit message and must follow the same format.

For worked examples, read `references/examples.md`.

## Pre-Commit Hooks

Pre-commit hooks (or equivalent staged-file checks) may run before a commit is accepted. Commits can fail at the hook stage until staged files satisfy the configured quality gates.

### Auto-formatting and re-staging

Many hooks reformat staged files in place (Ruff, Black, Prettier, google-java-format). When this happens:

1. The hook modifies the working-tree copy of the file.
2. The commit is rejected because the staged content no longer matches.
3. **Re-stage the modified files** and retry with the same message.

This is normal workflow, not an error. Iron Law 6.

### Formatting a file on demand

To get a file formatted without making a real change:

1. Make a trivial edit (e.g., add a blank line).
2. Stage the file.
3. Attempt a commit -- the hooks reformat it.
4. Re-stage the reformatted file and commit (or reset the commit if the only purpose was formatting).

Useful when a file predates the hooks or was edited outside the project's toolchain.

### Persistent failures after re-staging

If the commit still fails after re-staging the auto-formatted output, the remaining violations are not auto-fixable -- typically lint or type-check errors requiring manual intervention. Read the hook output, fix each reported issue, re-stage, and retry.

### Activating hooks

Activation depends on the project's toolchain. Python projects using the canonical setup use:

```bash
uv run pre-commit install
```

This only needs to be run once per clone. See the language-specific standards skill for your active stack (e.g., `python-code-standards`).

## On Invocation

1. Stage exactly the files you intend to ship (Iron Law 3).
2. Draft the commit message in the format above.
3. Show the user the staged diff and the proposed message. Wait for explicit approval.
4. Execute the commit per `tool-usage`.
5. If a hook reformats files, re-stage and retry with the same message (Iron Law 6).
6. If the hook reports non-auto-fixable violations, fix them, re-stage, retry.

## Why This Exists

Semantic release tools (`semantic-release`, `python-semantic-release`, `release-please`) read commit messages to determine version bumps automatically. Without consistent conventional commits, the automation cannot tell whether a change is a feature, fix, or breaking change -- and either bumps incorrectly or not at all.
