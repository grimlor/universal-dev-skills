---
name: tool-usage
description: "Tool and terminal decisions for every task. Use for any request involving file reads or edits, running tests, executing searches, git commands, or terminal work -- even when the user does not mention tool choice. Determines whether to use VS Code integrations, MCP tools, or terminal commands."
---

# Tool Usage Guidelines

Standard tool-vs-terminal decision framework.

## Iron Laws

1. **Tool-first.** Use the tool listed in the routing table below; never the
   "Never This" column.
2. **Tests run via `runTests` only.** Never `pytest`, `jest`, `dotnet test`,
   `bun test`, etc. in the terminal -- no exceptions, including sanity checks
   and coverage runs.
3. **Scripts require user approval.** When a snippet-execution tool is needed,
   show the script and ask the user to enable the tool. Never run language
   runtimes in the terminal as a workaround.
4. **Verify after edits.** After completing edits, run language-native CLI
   type/lint checks in the terminal as final verification -- the Problems
   panel may not surface every diagnostic.

## Language References

For language/toolchain-specific verification details:

- `references/python.md`
- `references/typescript.md`
- `references/java.md`
- `references/csharp.md`

## Tool-First Routing

| Task | Use This Tool | Never This |
|------|--------------|----------|
| Read/edit files | `read_file`, `replace_string_in_file`, `create_file` | `cat`, `sed`, `awk`, `echo` |
| Run tests | `runTests` tool | `pytest` in terminal |
| Check errors | `get_errors` tool (Pylance/Pyright; partial Ruff) | -- |
| Search code | `semantic_search`, `grep_search` | `grep`, `find` in terminal |
| Find files | `file_search`, `list_dir` | `ls`, `find` in terminal |
| Git status/changes | `get_changed_files`, GitKraken `git_status` | `git status` in terminal |
| Git add/commit | GitKraken `git_add_or_commit` | `git add`, `git commit` in terminal |
| Git diff/log | GitKraken `git_log_or_diff` | `git log`, `git diff` in terminal |
| Git branch | GitKraken `git_branch`, `git_checkout` | `git branch`, `git checkout` in terminal |
| Git push | GitKraken `git_push` | `git push` in terminal |
| Git blame | GitKraken `git_blame` | `git blame` in terminal |
| Git stash | GitKraken `git_stash` | `git stash` in terminal |
| Run language snippets | Show script to user; ask them to enable snippet tool (see below) | ad-hoc shell one-liners; running scripts without user review |

## Platform-Dependent Operations

For platform-dependent tasks (GitHub vs ADO vs GitLab vs ...), do not hardcode
a tool. Probe the available tool list with the discovery pattern below; use
whatever matches; otherwise use the fallback.

| Task | Discovery Pattern | Fallback |
|------|------------------|----------|
| Code review | `review` | Manual review in diff view |
| Pull / merge requests | `pull_request\|merge_request` | Git provider web UI |
| Work items / issues | `issue\|work_item` | Project tracker web UI |
| CI / pipeline status | `pipeline\|build\|check` | CI provider web UI |

Example: in a GitHub workspace with GitKraken installed, searching `review`
finds `gitlens_start_review`. In an ADO workspace with `ado-workflows-mcp`,
searching `pull_request` finds ADO PR tools. With neither installed, fall back
to the web UI.

The git operations in the routing table above (status, commit, branch, push,
blame, stash) are platform-agnostic; only the tasks in this table vary.

## When Terminal Is Appropriate

- **Package installation**: `pip install`, `npm install`, `dotnet restore`, etc.
- **Build/compilation**: complex builds requiring environment setup
- **Background processes**: servers, long-running tasks (`isBackground=true`)
- **Environment setup**: virtual environments, cloud CLI auth
- **Type-check + lint sweep**: language-native analyzers after edits (Iron Law 4)
- **Commands with no tool equivalent**

For language-specific terminal commands (Bun coverage workflow, Ruff severity,
etc.), see the relevant reference file.

## Script Handling

Some language servers expose snippet-execution tools (e.g. Pylance
`RunCodeSnippet` for Python). These are **disabled by default** for security.
When a script needs to run:

1. Show the full script to the user in a code block.
2. Ask the user to enable the snippet tool and approve your running it.
3. Do not run language runtimes directly in the terminal as a workaround.

This ensures the user reviews every script before execution, preventing
jailbreak attacks through dynamically generated code.

For language-specific snippet details, see the relevant reference file.

## Git Branching Protocol

Branching strategy for feature work is defined in the `feature-workflow` skill,
Phase 4 (Code Quality Baseline) -- the quality-branch → feature-branch →
draft-PR workflow that keeps quality fixes separate from functional changes.

The `conventional-commits` skill covers commit message format only, not
branching.
