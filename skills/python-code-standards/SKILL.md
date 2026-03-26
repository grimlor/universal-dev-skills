---
name: python-code-standards
description: "Ruff and Pyright configuration standards for Python projects. Use when setting up a new Python project, auditing an existing project's tooling config, or applying linting/type-checking fixes. Covers pyproject.toml settings, taskipy tasks, and pre-commit hooks."
---

# Python Code Standards

## When This Skill Applies

Whenever:
- Setting up tooling in a new Python project
- Auditing or updating `pyproject.toml` lint/type configuration
- Running ruff or pyright to find and fix issues
- Adding or updating the pre-commit hook configuration
- Applying the standard taskipy task aliases

---

## Scope — Personal vs. Team Projects

**This standard applies in full only to projects where you control the toolchain**
(personal projects, greenfield repos, repos where you are the sole or primary author).

### How to determine if you control the toolchain

Use these signals — AI models vary in capability, so explicit heuristics here are
more reliable than expecting a model to infer context from the workspace alone:

1. **GitHub owner is `grimlor`** → personal repo → full standard applies.
2. **Forked repo** (different owner, contributor commits from `grimlor`) → apply
   the higher bar of your personal standard and the upstream's standard to your
   contributions. Don't rewrite the upstream's existing configs — the upstream
   project's conventions (type checker, lint rules, coverage thresholds) are
   theirs to own.
3. **Repo lives under a work org path or an ADO workspace** → team repo → follow
   team conventions for shared config, but apply the higher bar of your personal
   standard and the team's standard to your own contributions. You may not be
   able to reduce existing tech debt, but don't add to it.
4. **`pyproject.toml` already has `[tool.mypy]`** → someone else owns the type
   checker; don't replace it without team agreement.
5. **`CODEOWNERS` file exists or git log shows multiple authors** → shared
   codebase; don't commit toolchain changes unilaterally.
6. **A `.pre-commit-config.yaml` is already present with different hooks** → adapt
   to what's there rather than overwriting.

When in doubt, ask the user which category the repo falls into before applying the
full standard.

**Important:** Do not treat configs from forked projects as canonical examples of
this standard. Forked project configs reflect the original author's choices, not
necessarily yours.

At work, team repos may follow different conventions — and that's expected. The key
differences to watch for in shared codebases:

- **Type checker:** team repos may use `mypy` instead of `pyright`. Do not replace
  mypy with pyright unilaterally — see [Pyright vs. mypy](#pyright-vs-mypy) below.
- **Ruff config:** teams may not have ruff at all, or may have a narrower `select`
  list. You can still run ruff locally with `--config` pointing to your personal
  settings, but don't commit a config the team hasn't agreed to.
- **Pre-commit hooks:** a team repo may have its own hook setup. Don't overwrite it
  with the personal standard — extend or adapt to what's already there.
- **Docstring rules (D):** pydocstyle is strict. Enabling it on a legacy codebase
  generates hundreds of violations. Only add `"D"` to `select` in repos where you
  intend to fix all violations immediately.

In team contexts, apply what you can personally (running ruff locally, using pyright
in your editor via Pylance) without imposing changes on shared config files. Your
contributed code should still meet your personal quality bar even when the team's
bar is lower.

---

## Pyright vs. mypy

**Prefer pyright for all projects you control.** For team projects, use whatever the
team uses — do not replace mypy with pyright unilaterally.

### Why pyright, not mypy

Pylance (the VS Code Python language server) uses pyright internally as its
type-checking engine. Running mypy in the same project creates a **two-checker split**:

- Pylance/pyright surfaces errors in the editor Problems panel and inline squiggles
- mypy surfaces different errors in the terminal (different inference, different
  strictness model, different plugin ecosystem)
- The two disagree on some valid code, meaning you end up either suppressing one or
  chasing false positives in the other

Using pyright for both the CLI check and the editor gives a **single consistent
type surface** — what the editor shows is exactly what `uv run pyright` reports,
and vice versa.

### If a team repo uses mypy

- Keep mypy — don't change the team's CI
- Pylance will still type-check in the editor using pyright internally; editor
  errors won't match `mypy` output exactly, and that's acceptable
- Do not add a `[tool.pyright]` section to a repo that uses mypy — having both
  configured creates confusion about which is authoritative
- If you add new code to a mypy repo, write it to satisfy mypy's rules (which are
  stricter in some areas, looser in others)

### Common mypy → pyright migration signals

When a team repo is ready to migrate (not your call to make unilaterally):
- mypy errors that are false positives due to missing stubs or dynamic patterns
- `# type: ignore` comments accumulating without a clear reason
- Pylance editor errors that mypy doesn't catch (or vice versa)
- Team interest in strict mode with fewer suppressions

---

## Canonical `pyproject.toml` Configuration

The following sections must be present in every Python project. Substitute
`<package_name>` with the project's importable package name (e.g. `ado_workflows`).

### Dev Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pyright>=1.1,<2",
    "pre-commit>=4,<5",
    "pytest>=8,<9",
    "pytest-asyncio>=0.24,<1",
    "pytest-cov>=6,<7",
    "ruff>=0.8,<1",
    "taskipy>=1.14,<2",
]
```

### Taskipy Tasks

```toml
[tool.taskipy.tasks]
lint   = "uv run ruff check --fix src/ tests/"
format = "uv run ruff format src/ tests/"
type   = "uv run pyright src/ tests/"
test   = "uv run pytest tests/ -v"
cov    = "uv run pytest tests/ --cov=<package_name> --cov-report=term-missing"
check  = "task format && task lint && task type && task test"
```

The `check` task runs the full quality gate: format → lint → type → test.
Run `uv run task check` before committing when not using pre-commit hooks for
all four checks (pre-commit hooks cover format/lint/type but not tests).

### Ruff

```toml
[tool.ruff]
target-version = "py311"   # match project's minimum Python version
line-length = 99
src = ["src", "tests"]

[tool.ruff.lint]
preview = true
explicit-preview-rules = true
select = [
    "E",        # pycodestyle errors
    "W",        # pycodestyle warnings
    "F",        # pyflakes
    "I",        # isort
    "N",        # pep8-naming
    "UP",       # pyupgrade
    "B",        # flake8-bugbear
    "SIM",      # flake8-simplify
    "TCH",      # flake8-type-checking
    "RUF",      # ruff-specific rules
    "D",        # pydocstyle
    "PLC0415",  # import-outside-top-level
    "PLC2701",  # import-private-name (preview)
]
ignore = [
    "E501",   # line length (handled by formatter)
    "D212",   # multi-line-summary-first-line (conflicts with D213)
    "D203",   # one-blank-line-before-class (conflicts with D211)
]

[tool.ruff.lint.isort]
known-first-party = ["<package_name>"]
combine-as-imports = true

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "PLC0415",  # import-outside-top-level — tests may import inside functions
    "PLC2701",  # import-private-name — testing internal state is intentional
    "D205",     # BDD Given/When/Then blocks aren't summary+body
    "D400",     # BDD steps don't end with periods
    "D415",     # same as D400
    "D401",     # fixture docstrings are descriptive, not imperative
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

**Why D212/D203 are ignored:** ruff enforces only one convention at a time. `D213`
(summary on second line) conflicts with `D212`; `D211` (no blank line before class)
conflicts with `D203`. The ignored rule in each conflicting pair is the less-common
one; the enforced rule is the project default.

**Additional per-file-ignores:** Some projects need extra ignores for specific
subdirectories. Example — MCP tool files that require runtime imports:

```toml
"src/<package>/tools/*.py" = [
    "TCH002",  # runtime imports required for @mcp.tool() outputSchema generation
]
```

Add these below the `tests/**/*.py` block as needed.

### Pyright

```toml
[tool.pyright]
pythonVersion = "3.11"   # match project's minimum Python version
typeCheckingMode = "strict"
venvPath = "."
venv = ".venv"
```

For projects that include hand-written stubs:

```toml
[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
stubPath = "typings"
venvPath = "."
venv = ".venv"
```

---

## Canonical `.pre-commit-config.yaml`

Every **personal project** must have a `.pre-commit-config.yaml` in the repo root
that runs ruff and pyright on every commit. For team repos, check what's already
there before adding or replacing hooks.

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.1
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: local
    hooks:
      - id: pyright
        name: pyright
        entry: uv run pyright
        language: system
        types: [python]
        args: [src/, tests/]
```

Update `rev` to the latest ruff release when setting up a new project. Check
[github.com/astral-sh/ruff-pre-commit/releases](https://github.com/astral-sh/ruff-pre-commit/releases).

Activate pre-commit in the virtual environment after `.pre-commit-config.yaml` is
in place:

```bash
uv run pre-commit install
```

---

## Docstring Standards (pydocstyle / D rules)

All public symbols must have docstrings — classes, functions, methods, and packages.
The `D` ruleset enforces this. Key requirements:

| Rule enforced | Meaning |
|---|---|
| `D100` | Public module docstring |
| `D101` | Public class docstring |
| `D102` | Public method docstring |
| `D103` | Public function docstring |
| `D104` | Public package docstring (`__init__.py`) |
| `D105` | Magic method docstring (`__post_init__`, etc.) |
| `D107` | `__init__` docstring |
| `D213` | Summary on second line (multi-line docstrings) |
| `D211` | No blank line before class docstring |
| `D401` | First line in imperative mood ("Return …", not "Returns …") |
| `D400`/`D415` | Summary line ends with punctuation |

### Common Fix Patterns

**D104 — empty `__init__.py`:**
```python
"""Test suite for <package>."""
```

**D107 — `__init__` method with class-level docstring:**
```python
def __init__(self, credential: TokenCredential | None = None) -> None:
    """Initialize with an optional credential; defaults to DefaultAzureCredential."""
```

**D105 — `__post_init__`:**
```python
def __post_init__(self) -> None:
    """Initialize computed fields after dataclass construction."""
```

**D401 — imperative mood (ruff can't auto-fix all cases):**
```python
# ❌  "Convenience wrapper for RepositoryContext.set."
# ✅  "Delegate to RepositoryContext.set."
# ✅  "Return the current workflow state."
```

**D400/D415 — missing terminal punctuation:**
```python
# ❌  """Common utilities for demo-assistant-mcp"""
# ✅  """Common utilities for demo-assistant-mcp."""
```

**D205 — blank line between summary and body (multi-line docstrings that start
immediately with text on the first line after `"""`):**
```python
# ❌
"""Present the next prompt for confirmation without executing it.
Advances the current_step pointer …
"""

# ✅
"""Present the next prompt for confirmation without executing it.

Advances the current_step pointer …
"""
```

---

## Workflow for Applying Standards to an Existing Project

**For personal projects:** apply the full standard below.
**For team projects:** see [Scope](#scope--personal-vs-team-projects) first — only
apply what the team has agreed to, or what doesn't affect shared config.

1. **Update `pyproject.toml`** — add/replace `[tool.ruff]`, `[tool.ruff.lint]`,
   `[tool.ruff.lint.isort]`, `[tool.ruff.lint.per-file-ignores]`, `[tool.ruff.format]`,
   `[tool.pyright]`, and taskipy tasks per the canonical config above.

2. **Run format:** `uv run task format` (or `uv run ruff format src/ tests/`)

3. **Run lint with auto-fix:** `uv run task lint` (or `uv run ruff check --fix src/ tests/`)

4. **Fix remaining issues manually** — ruff reports unfixable violations with file +
   line. Common unfixable rules: `D401` (imperative mood), `D107`/`D105`/`D102`
   (missing docstrings).

5. **Verify clean:** `uv run ruff check src/ tests/` should print `All checks passed!`

6. **Run type check:** `uv run task type` — fix any Pyright errors introduced.

7. **Commit:** `chore(lint): add pydocstyle rules and fix docstring issues`
