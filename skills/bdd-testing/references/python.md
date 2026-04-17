# Python BDD Reference

Language-specific guidance for applying `bdd-testing` in Python projects.

## I/O Boundary Examples

| I/O boundary (mock these) | Part of the system (never mock) |
|---|---|
| `subprocess.run` -- spawns a process | `discover_repositories` -- our function that calls subprocess |
| `requests.get` -- HTTP call | `fetch_details` -- our function that calls requests |
| `Connection.query` -- database wire call | `RepoContext.get` -- our caching logic over discovery |
| `os.getcwd` -- process-level state | `os.path.exists` with `tmp_path` -- use real filesystem instead |

Use `tmp_path` (pytest fixture) for real filesystem structure so that
`os.path.exists`, `os.listdir`, and `os.path.isdir` all run against real
directories.

## Coverage Command

```bash
pytest --cov=<package> --cov-report=term-missing tests/
```

## Exception Assertions

```python
with pytest.raises(ValueError) as exc_info:
    registry.get("nonexistent")

assert "nonexistent" in str(exc_info.value), (
    f"Error should name the missing item. Got: {exc_info.value}"
)
```

## Static Analysis Suppressions

Avoid file-level pragmas like `# pyright: reportPrivateUsage=false`.
If a suppression is unavoidable, use a narrow inline suppression with reason,
for example `# pyright: ignore[reportPrivateUsage]`.

See `tool-usage` for the full pragma policy.
