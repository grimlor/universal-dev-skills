# Python BDD Reference

Language-specific guidance for applying `bdd-testing` in Python projects.

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
