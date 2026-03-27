---
name: tool-usage
description: "Tool and terminal decisions for every task. Use for any request involving file reads or edits, running tests, executing searches, git commands, or terminal work — even when the user does not mention tool choice. Determines whether to use VS Code integrations, MCP tools, or terminal commands."
---

# Tool Usage Guidelines

Standard tool-vs-terminal decision framework.

## Language References

This file defines language-agnostic tool usage. For language/toolchain-specific
verification details, use:

- `references/python.md`

## Prerequisites

The tool-first approach depends on editor integrations feeding diagnostics into
the Problems panel (`get_errors`). Configure your language's analysis/lint
extensions so `get_errors` surfaces meaningful errors.

Regardless of language, the principle is:

- Use editor-integrated diagnostics first.
- After edits, run language-native CLI checks (type/lint/test) as final verification.

Python-specific extension, pragma, and Ruff severity notes are in
`references/python.md`.

## Tool-First Approach

Use specialized VS Code tools instead of terminal commands. This is not a preference — it is a requirement. Tools provide structured output, integrated error reporting, and correct path resolution that raw terminal commands do not.

| Task | Use This Tool | Never This |
|------|--------------|----------|
| Read/edit files | `read_file`, `replace_string_in_file`, `create_file` | `cat`, `sed`, `echo` |
| Run tests | `runTests` tool | `pytest` in terminal |
| Check errors | `get_errors` tool (Pylance/Pyright; partial Ruff) | — |
| Search code | `semantic_search`, `grep_search` | `grep`, `find` in terminal |
| Find files | `file_search`, `list_dir` | `ls`, `find` in terminal |
| Git status/changes | `get_changed_files`, GitKraken `git_status` | `git status` in terminal |
| Git add/commit | GitKraken `git_add_or_commit` | `git add`, `git commit` in terminal |
| Git diff/log | GitKraken `git_log_or_diff` | `git log`, `git diff` in terminal |
| Git branch | GitKraken `git_branch`, `git_checkout` | `git branch`, `git checkout` in terminal |
| Git push | GitKraken `git_push` | `git push` in terminal |
| Git blame | GitKraken `git_blame` | `git blame` in terminal |
| Git stash | GitKraken `git_stash` | `git stash` in terminal |
| Run language snippets | Language-server snippet tools when available | ad-hoc shell one-liners when a structured tool exists |

**Running tests via terminal is not permitted** except for the coverage exception below. The `runTests` tool handles test environment setup, path configuration, and output formatting that raw test commands will get wrong or miss entirely. Any session step that would otherwise run `pytest`, `jest`, `dotnet test`, etc. in the terminal must use `runTests` instead — no exceptions, including quick sanity checks.

**Coverage exception:** `runTests` is a VS Code Test Explorer integration and cannot pass arbitrary flags like `--cov` or `--cov-report`. When the explicit goal is generating a coverage report (not just running tests), use the terminal:

```bash
# Python example
pytest --cov=<package> --cov-report=term-missing tests/
```

This exception applies only to deliberate coverage reporting steps, not to routine test runs during development.

**Terminal verification:** The VS Code Problems panel may not surface every
diagnostic from every analyzer. After completing edits, run language-native CLI
checks in the terminal as a final verification step.

## Platform-Dependent Operations

Some operations depend on the git hosting platform (GitHub, Azure DevOps, GitLab, etc.) and have different tool implementations depending on what MCP servers or extensions are installed. **Do not hardcode a specific tool for these tasks.** Instead, discover what is available at runtime.

### Principle

When the task is platform-dependent, search the available tool list using the discovery pattern for that task category. Use whatever tool matches. If nothing matches, fall back to the terminal or web UI.

### Discovery procedure

1. Use the tool search capability to probe available tools with the pattern from the table below
2. If a matching tool is found, use it
3. If no match, use the documented fallback

### Platform-dependent task categories

| Task | Discovery Pattern | Fallback |
|------|------------------|----------|
| Code review | `review` | Manual review in diff view |
| Pull / merge requests | `pull_request\|merge_request` | Git provider web UI |
| Work items / issues | `issue\|work_item` | Project tracker web UI |
| CI / pipeline status | `pipeline\|build\|check` | CI provider web UI |

### Examples

- **GitHub workspace** with GitKraken installed: searching `review` finds `gitlens_start_review` → use it.
- **ADO workspace** with `ado-workflows-mcp` installed: searching `pull_request` finds ADO PR tools → use them.
- **Bare workspace** with neither: no match → tell the user to use the web UI or terminal.

The git operations in the tool-first table above (status, commit, branch, push, blame, stash) are platform-agnostic — they work the same regardless of the remote. Only the tasks in this section vary by platform.

## When Terminal Is Appropriate

- **Package installation**: `pip install`, `npm install`, `dotnet restore`, etc.
- **Build/compilation**: Complex build processes requiring environment setup
- **Background processes**: Servers, long-running tasks (`isBackground=true`)
- **Environment setup**: Virtual environments, cloud CLI auth
- **Coverage reporting**: Test coverage report generation (see above)
- **Type-check + lint sweep**: Running language-native analyzers and linters after edits to catch diagnostics invisible to `get_errors`
- **Commands with no tool equivalent**: When no specialized tool exists

General test runs are not on this list. They have a tool equivalent — `runTests` — and that tool must be used. Similarly, when snippet tools are available for a language, they should be preferred over ad-hoc terminal one-liners.

## Script Handling

When language-server snippet tools are available, prefer them over shell
one-liners for quick scripts because they avoid quoting issues and run against
the configured workspace environment.

For Python-specific `RunCodeSnippet` guidance, see `references/python.md`.

### Script file fallback

| Script Size | Approach |
|-------------|----------|
| ≤ 10 lines | Run directly in terminal |
| > 10 lines | Create a script file, then execute it |

**For long scripts:**
1. Store scripts in `.copilot/scripts/` (git-ignored)
2. Use `create_file` to write the script
3. Execute it — prefer a language-server snippet tool if available (see language references), otherwise use `run_in_terminal`
4. This prevents terminal buffer overflow and Pty failures

## Why This Matters

- **Faster execution**: Tools are optimized for VS Code integration
- **Better context**: Structured data instead of raw text parsing
- **Error handling**: Built-in validation catches issues early
- **Iteration speed**: Especially impactful for testing and file operations
