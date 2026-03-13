---
name: tool-usage
description: "Development tool preferences and execution patterns. Use when choosing between VS Code tools and terminal commands, handling long scripts, deciding how to execute file operations, tests, searches, or git commands."
---

# Tool Usage Guidelines

Standard tool-vs-terminal decision framework.

## Prerequisites

The tool-first approach below depends on VS Code extensions feeding diagnostics into the Problems panel (surfaced by `get_errors`). For Python projects, the recommended stack is:

| Extension | ID | Purpose |
|---|---|---|
| Pylance | `ms-python.vscode-pylance` | Type-checking via Pyright (strict mode), unused imports, type-ignore validation |
| Ruff | `charliermarsh.ruff` | Lint rules from project config |

Pylance uses Pyright as its type-checking engine. Pyright is also available as a standalone CLI (`pyright` or `uv run pyright`). However, Pylance does not surface all Pyright diagnostics through `get_errors` — some issues only appear when running Pyright directly. After completing edits, run `pyright` in the terminal as a final verification step alongside the lint sweep.

**Recommended settings** (User or Workspace):

- `python.analysis.typeCheckingMode`: `"strict"`
- `python.analysis.diagnosticSeverityOverrides`: `reportUnusedImport: "error"`, `reportUnusedVariable: "error"`, `reportUnnecessaryTypeIgnoreComment: "error"`, `reportUnknownMemberType: "none"`
- `ruff.configurationPreference`: `"filesystemFirst"` (uses project-level config)
- `ruff.fixAll`: `true`

Without these extensions and settings, `get_errors` will not cover the full lint/type surface and terminal fallbacks become necessary.

Adapt these recommendations to your project's language and toolchain. The principle — use extensions that feed diagnostics into `get_errors` — is universal.

### Pyright / Pylance pragma policy

Pyright diagnostics must be fixed — not silenced. Pragmas (`# type: ignore`, `# pyright: ignore`) are a last resort, not a first response.

**File-level pragmas are never acceptable.** Do not add `# pyright: basic`, `# pyright: ignore`, `# type: ignore` (without a specific code), or any other directive at the top of a file to suppress type-checking wholesale. This hides an unknown number of real bugs and defeats strict mode entirely.

**Inline pragmas are rarely acceptable.** Use a narrow, code-specific comment (e.g., `# type: ignore[assignment]`) only when all of the following are true:

1. The issue is a **known Pyright limitation** — a dynamic pattern Pyright cannot model, or a third-party library ships incomplete stubs **and** creating a stub file (e.g., `stubs/<package>.pyi`) is not feasible (the library is too large, too volatile, or has no stable public API surface worth stubbing)
2. The code is **provably correct** — you have verified it manually or via tests
3. The suppression is **as narrow as possible** — targeting a single rule code, on a single line

When an inline pragma is added, include a comment on the same line explaining why:

```python
result = some_dynamic_call()  # type: ignore[no-any-return]  # third-party stub missing return type
```

If you find yourself adding more than one or two pragmas while fixing a file, stop. The volume indicates a structural problem — incorrect type annotations, a missing stub package, or code that needs to be restructured — not a pragma problem.

### Known gap — Ruff severity

The Ruff extension hardcodes diagnostic severity in `_get_severity()`: only `F821`, `E902`, and `E999` are reported as **Error**; every other rule is **Warning**. The `get_errors` tool only returns error-severity diagnostics — so most Ruff findings are invisible to it.

**Impact:** `get_errors` does **not** surface the full diagnostic set from either tool. Pylance omits some Pyright findings, and Ruff reports most rules as warnings (invisible to `get_errors`). After completing edits, run both `pyright` and your project's lint command in the terminal to catch what `get_errors` missed. This is the one accepted exception to the tool-first rule above.

## Tool-First Approach

Use specialized VS Code tools instead of terminal commands. This is not a preference — it is a requirement. Tools provide structured output, integrated error reporting, and correct path resolution that raw terminal commands do not.

| Task | Use This Tool | Never This |
|------|--------------|----------|
| Read/edit files | `read_file`, `replace_string_in_file`, `create_file` | `cat`, `sed`, `echo` |
| Run tests | `runTests` tool | `pytest` in terminal |
| Check errors | `get_errors` tool (Pylance/Pyright; partial Ruff) | — |
| Search code | `semantic_search`, `grep_search` | `grep`, `find` in terminal |
| Find files | `file_search`, `list_dir` | `ls`, `find` in terminal |
| Git status | `get_changed_files` | `git status`, `git diff` |
| Run Python snippets | Pylance `RunCodeSnippet` MCP tool | `python -c "..."` in terminal |

**Running tests via terminal is not permitted** except for the coverage exception below. The `runTests` tool handles test environment setup, path configuration, and output formatting that raw test commands will get wrong or miss entirely. Any session step that would otherwise run `pytest`, `jest`, `dotnet test`, etc. in the terminal must use `runTests` instead — no exceptions, including quick sanity checks.

**Coverage exception:** `runTests` is a VS Code Test Explorer integration and cannot pass arbitrary flags like `--cov` or `--cov-report`. When the explicit goal is generating a coverage report (not just running tests), use the terminal:

```bash
# Python example
pytest --cov=<package> --cov-report=term-missing tests/
```

This exception applies only to deliberate coverage reporting steps, not to routine test runs during development.

**Terminal verification:** The VS Code Problems panel aggregates diagnostics from configured extensions, but `get_errors` does not surface everything. Pylance omits some Pyright diagnostics, and Ruff reports most rules as warnings (invisible to `get_errors`). After completing edits, run both `pyright` and your project's lint command in the terminal as a final verification step.

## When Terminal Is Appropriate

- **Package installation**: `pip install`, `npm install`, `dotnet restore`, etc.
- **Build/compilation**: Complex build processes requiring environment setup
- **Background processes**: Servers, long-running tasks (`isBackground=true`)
- **Environment setup**: Virtual environments, cloud CLI auth
- **Coverage reporting**: Test coverage report generation (see above)
- **Type-check + lint sweep**: Running `pyright` and linters after edits to catch diagnostics invisible to `get_errors`
- **Commands with no tool equivalent**: When no specialized tool exists

General test runs are not on this list. They have a tool equivalent — `runTests` — and that tool must be used. Similarly, ad-hoc Python execution has a tool equivalent — Pylance `RunCodeSnippet` — which should be preferred over terminal `python` invocations.

## Script Handling

### Python scripts — Pylance RunCodeSnippet (preferred)

For Python projects, the Pylance MCP server exposes a `RunCodeSnippet` tool that
executes Python directly using the workspace's configured interpreter. Prefer it
over terminal execution for scripts of any size:

- **No shell escaping.** Heredocs and `python -c` require careful quoting of
  quotes, backslashes, and dollar signs. `RunCodeSnippet` accepts raw Python —
  the code you write is the code that runs.
- **Correct interpreter.** The tool automatically uses the Python environment
  configured for the workspace, matching what Pylance and `runTests` use. No
  risk of hitting the system Python or a stale venv.
- **Clean output.** stdout and stderr are returned as structured data, not
  interleaved with shell prompts and ANSI escape sequences.

Use `RunCodeSnippet` for: audit/analysis scripts, code generation helpers,
data transformation one-offs, import validation, and any ad-hoc Python
execution during a session. No temporary files needed — code runs directly
in memory.

```python
# Example: audit every test file for bare assertions
# Passed directly to RunCodeSnippet — no quoting gymnastics required
import ast, os
for root, _, files in os.walk("tests"):
    for f in files:
        if not f.endswith(".py"):
            continue
        path = os.path.join(root, f)
        tree = ast.parse(open(path).read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert) and node.msg is None:
                print(f"BARE_ASSERT: {path}:{node.lineno}")
```

### Non-Python scripts and fallback

| Script Size | Approach |
|-------------|----------|
| ≤ 10 lines | Run directly in terminal |
| > 10 lines | Create a script file, then execute it |

**For long scripts:**
1. Store scripts in `.copilot/scripts/` (git-ignored)
2. Use `create_file` to write the script
3. Use `run_in_terminal` to execute it
4. This prevents terminal buffer overflow and Pty failures

## Why This Matters

- **Faster execution**: Tools are optimized for VS Code integration
- **Better context**: Structured data instead of raw text parsing
- **Error handling**: Built-in validation catches issues early
- **Iteration speed**: Especially impactful for testing and file operations
