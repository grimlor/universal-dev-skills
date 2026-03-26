# Python Feedback Loop Reference

Language-specific guidance for applying `bdd-feedback-loop` in Python projects.

## Step 4 Validation Commands

1. Run editor diagnostics on the test file.
2. Run `pyright` on the test module or test package.
3. Run pytest for the targeted module.

## Common Python Remediation Issues

- Missing imports and undefined fixture names
- Async/sync mock mismatches (`AsyncMock` vs `MagicMock`)
- Type mismatches in constructor or method calls

## Step 5 Python-Specific Checks

- Use `pytest.approx` for floating-point comparisons where tolerance matters.
- Validate error message content, not only exception type.
- Avoid always-true assertions inside `pytest.raises` contexts.
