# Python Tool Usage Reference

Python-specific details for applying `tool-usage`.

## Recommended VS Code Extensions

| Extension | ID | Purpose |
|---|---|---|
| Pylance | `ms-python.vscode-pylance` | Type-checking via Pyright, unused-import and type-ignore diagnostics |
| Ruff | `charliermarsh.ruff` | Lint and format integration from project config |

## Recommended Settings

- `python.analysis.typeCheckingMode`: `"strict"`
- `python.analysis.diagnosticSeverityOverrides`: `reportUnusedImport: "error"`, `reportUnusedVariable: "error"`, `reportUnnecessaryTypeIgnoreComment: "error"`, `reportUnknownMemberType: "none"`
- `ruff.configurationPreference`: `"filesystemFirst"`
- `ruff.fixAll`: `true`

## Pyright/Pylance Pragmas

File-level suppression pragmas are not acceptable. Use narrow inline ignores only
when unavoidable and include a reason.

```python
result = some_dynamic_call()  # type: ignore[no-any-return]  # third-party stub missing return type
```

## Known Ruff Severity Gap

Most Ruff diagnostics surface as warnings in the extension and may not appear via
`get_errors`. Run terminal lint and type checks (`ruff` and `pyright`) as final
verification after edits.

## Python Snippet Execution

Pylance `RunCodeSnippet` is **disabled by default** for security. When the
agent needs to run a Python script:

1. **Show the full script** to the user in a fenced code block.
2. **Ask the user to enable** the `RunCodeSnippet` tool and get the approval to run it.
3. **Do not** run `python` directly in the terminal as a workaround.

This prevents jailbreak attacks through dynamically generated code while
still allowing legitimate script execution under user supervision.
