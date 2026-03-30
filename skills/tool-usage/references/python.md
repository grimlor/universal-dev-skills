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

Use Pylance `RunCodeSnippet` for Python execution. It avoids quoting issues
and runs against the configured workspace Python environment.
