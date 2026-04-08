---
name: code-quality-antipatterns
description: "Suppression pragma policy and common code quality antipatterns. Use whenever writing, editing, or reviewing production code or test code — any task where the agent might add a suppression comment (type-ignore, noqa, pragma no-cover, eslint-disable, SuppressWarnings, etc.) or encounter one that should be fixed. Cross-cutting: applies alongside language-specific standards skills."
---

# Code Quality Antipatterns — Suppression Pragmas and Common Evasions

## When This Skill Applies

Whenever writing, editing, or reviewing code — production or test. If the task
could result in a suppression pragma being added, or if the agent encounters an
existing one while working, this skill applies.

This is a **cross-cutting** skill. It does not replace the language-specific
standards skills (which define *how* to format a suppression when one is
justified). It defines *when* a suppression is allowed and what the correct
alternative is.

---

## Core Rule — No Suppression Without Approval

Suppression pragmas — in any language, for any tool — are **never added
autonomously**. The agent must not add a suppression without explicit user
approval in the current conversation.

This includes, but is not limited to:

| Category | Examples |
|---|---|
| **Coverage** | `# pragma: no cover`, `/* istanbul ignore next */`, `[ExcludeFromCodeCoverage]` |
| **Type checking** | `# type: ignore`, `# pyright: ignore`, `@ts-ignore`, `@ts-expect-error`, `// @ts-nocheck` |
| **Linting** | `# noqa`, `// eslint-disable-next-line`, `#pragma warning disable`, `@SuppressWarnings`, `// noinspection` |

### Before Proposing a Suppression

The agent must:

1. **Explain precisely what the diagnostic is and why it fires.** Not "the type
   checker complains" — name the rule, show the error, explain the root cause.
2. **Present the correct fix first.** There is almost always a real fix. Present
   it as the primary recommendation.
3. **Explain why the fix is not viable** only if that is genuinely the case.
   "Inconvenient" and "verbose" are not reasons.
4. **Present the suppression as a second option** with the exact pragma, the
   required justification comment, and the narrowest possible scope.
5. **Wait for the user to choose.** Do not default to the suppression.

**Violation of this rule is treated the same as a lint error or coverage gap.**
A pragma added without approval means the task is not complete.

---

## Antipattern Catalog

### 1. Coverage Suppression Instead of Writing the Spec

**The antipattern:** A line is hard to reach in tests, so the agent marks it
`# pragma: no cover` instead of writing the spec or removing dead code.

**Why it's wrong:** Coverage = specification completeness. A suppressed line is
an unspecified line. The correct dispositions are:

- **Reachable requirement** → write the spec.
- **Dead code** → remove it.
- **Genuinely unreachable** (e.g., defensive `assert False` after exhaustive
  match) → propose the pragma with justification; wait for approval.

"Hard to test" is not "unreachable."

### 2. Type-Ignore Instead of Type Stubs

**The antipattern:** A third-party library ships without type information.
Instead of creating a stub file, the agent sprinkles `# type: ignore` on every
call site.

**Why it's wrong:** Each `# type: ignore` silences *all* diagnostics on that
line — not just the missing-stub error. Real type bugs on the same line become
invisible. The suppressions multiply as more call sites are added, and nobody
remembers which ones are still needed.

**The correct fix:**

- **Check for existing stubs first.** Many popular libraries have stubs on PyPI
  (`types-requests`, `types-pyyaml`, etc.) or in `typeshed`. Install the stub
  package.
- **If no published stubs exist,** create a minimal stub file in the project's
  `typings/` directory (or equivalent). The stub only needs to cover the
  symbols actually used — not the entire library.
- **If the library is tiny or the usage is a single call,** a one-file stub is
  still better than `# type: ignore` because it documents the expected types
  and catches real misuse.

Language-specific equivalents:

| Language | Antipattern | Correct fix |
|---|---|---|
| Python | `# type: ignore[import-untyped]` | Install `types-*` package or add `typings/<lib>.pyi` |
| TypeScript | `@ts-expect-error -- no types` | Install `@types/*` package or add `typings/<lib>.d.ts` |
| Java | `@SuppressWarnings("unchecked")` | Add proper generic bounds or cast through a checked method |
| C# | `#pragma warning disable CS8600` | Use nullable annotations and proper null guards |

### 3. Type-Ignore Instead of Narrowing

**The antipattern:** A value has type `T | None`. Instead of narrowing with a
guard, the agent adds `# type: ignore` or uses a force-unwrap (`!` in TS,
`cast()` in Python).

**Why it's wrong:** The type checker is telling you the None case is unhandled.
Silencing it doesn't handle it — it hides a potential `NoneType` crash at
runtime.

**The correct fix:**

```python
# ❌ Suppress the symptom
value = maybe_none.strip()  # type: ignore[union-attr]

# ❌ Force-cast — hides the None case
value = cast(str, maybe_none).strip()

# ✅ Narrow — handle the None case explicitly
if maybe_none is None:
    raise ValueError("Expected a value but got None")
value = maybe_none.strip()

# ✅ Or provide a default
value = (maybe_none or "").strip()
```

```typescript
// ❌ Non-null assertion — hides the undefined case
const name = user!.name;

// ✅ Narrow — handle the undefined case
if (!user) {
    throw new Error("Expected user to be defined");
}
const name = user.name;
```

### 4. Broad Suppressions Instead of Narrow Ones

**The antipattern:** When a suppression is justified, the agent uses the broadest
form available — file-level `# noqa`, `/* eslint-disable */`, `@ts-nocheck`,
`#pragma warning disable` without a matching `restore`.

**Why it's wrong:** Broad suppressions silence diagnostics beyond the one that
triggered them. New code added to the same file inherits the suppression
silently. The original reason becomes invisible.

**When a suppression is approved, it must be:**

- **Line-level**, not file-level or block-level.
- **Rule-specific** — name the exact diagnostic being suppressed.
- **Commented** — include a justification that explains *why*.

```python
# ❌ Broad
# type: ignore

# ✅ Narrow with reason
# type: ignore[import-untyped]  # no published stubs for this lib; stub in typings/
```

### 5. Catch-All Exception Handling as a Pragma Equivalent

**The antipattern:** Instead of handling specific failure modes, the agent wraps
code in `except Exception` (or equivalent) to suppress errors at runtime rather
than at the type-checker level — achieving the same silencing effect through
different means.

**Why it's wrong:** The broad catch hides bugs, swallows unexpected errors, and
makes debugging impossible. It's a runtime pragma.

**The correct fix:** Catch the specific exception types that represent known
failure modes. Let unexpected exceptions propagate.

### 6. Test-Only Parameters on Production APIs

**The antipattern:** A production function is hard to test because it calls
another function internally (e.g., `load_settings()`). Instead of mocking at
the I/O boundary where the dependency reads from disk or network, the agent adds
a parameter to the production function so tests can inject the dependency
directly.

**Why it's wrong:** The parameter exists solely for test convenience — no
production caller uses it. This pollutes the public API with test concerns,
hides the real I/O boundary from the test suite, and skips exercising the
production code path in every test that uses the shortcut.

**How to detect it:**

- A parameter has a default of `None` and the only non-`None` callers are tests.
- Other functions with the same dependency don't have the parameter — they call
  the dependency internally and their tests already mock at the I/O boundary.
- Removing the parameter would not break any production code path.

**The correct fix:** Find the I/O boundary the dependency uses (file read,
network call, environment variable) and mock *that*. For file-based config,
write a real config file to `tmp_path` and `chdir` into it. For environment
variables, use `monkeypatch.setenv`. For network calls, mock the HTTP client.

The test should exercise the same code path production uses. If every other
handler calls `load_settings()` internally and the tests supply a real config
file, the odd one out with an injected `settings` parameter is the antipattern.

---

## Relationship to Other Skills

- **Language-specific standards** (`python-code-standards`, `typescript-code-standards`,
  etc.) define *how* to format a suppression when one has been approved (scope,
  syntax, required comments). This skill defines *whether* a suppression is
  allowed.
- **`bdd-testing`** defines the coverage requirement (100%) and the disposition
  for uncovered lines (spec or remove). This skill extends that principle: a
  `# pragma: no cover` counts as an uncovered line unless approved.
- **`skill-compliance`** routes to this skill via the "cross-cutting" rule — it
  applies alongside whatever task-specific skills are active.
