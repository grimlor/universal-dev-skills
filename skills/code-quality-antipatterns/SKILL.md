---
name: code-quality-antipatterns
description: "Suppression pragma policy and common code quality antipatterns. Use whenever writing, editing, or reviewing production code or test code -- any task where the agent might add a suppression comment (type-ignore, noqa, pragma no-cover, eslint-disable, SuppressWarnings, etc.) or encounter one that should be fixed. Cross-cutting: applies alongside language-specific standards skills."
---

# Code Quality Antipatterns -- Suppression Pragmas and Common Evasions

## Iron Laws

### Suppression pragmas

1. **No suppression pragmas during implementation work.** While writing or
   modifying code, the answer to a diagnostic is always "fix the code", never
   "silence the warning".
2. **Pragmas are only considered post-implementation**, during a final lint
   or type-check pass when a diagnostic genuinely resists clean fixing.
3. **No suppression without explicit user approval in the current
   conversation.** The agent presents the diagnostic, the correct fix, why
   the fix is not viable, and the proposed pragma -- then waits.
4. **Approved suppressions are line-level, rule-specific, and commented.** No
   file-level disables, no anonymous `# type: ignore`, no
   `/* eslint-disable */` blocks.

### Antipattern hygiene

5. **Don't silence diagnostics through evasion.** Catch-all `except`,
   force-unwraps (`!`, `cast()`), and runtime `try`/`pass` blocks are
   pragmas in disguise. They escape the approval flow but produce the same
   silencing effect.
6. **Don't bend production APIs for test convenience.** Mock at the I/O
   boundary; never add a parameter, dependency, or branch to production
   code whose only caller is a test.
7. **An unapproved pragma or an unjustified evasion is a task failure.**
   Treat it like a lint error: the task is not complete until the
   suppression is removed, the evasion is replaced with a real fix, or the
   user has explicitly approved leaving it.

Coverage suppressions follow `bdd-testing`'s coverage rule: every uncovered
line is a spec gap, the disposition is write the spec or remove the code, and
the approval flow above gates any `pragma: no cover`.

## Cross-Cutting Note

This skill defines *whether* a suppression is allowed. The language-specific
standards skills (`python-code-standards`, `typescript-code-standards`,
`java-code-standards`, `csharp-code-standards`) define *how* to format one
when the user has approved it.

## Suppression Categories

The Iron Laws apply to every suppression mechanism:

| Category | Examples |
|---|---|
| **Coverage** | `# pragma: no cover`, `/* istanbul ignore next */`, `[ExcludeFromCodeCoverage]` |
| **Type checking** | `# type: ignore`, `# pyright: ignore`, `@ts-ignore`, `@ts-expect-error`, `// @ts-nocheck` |
| **Linting** | `# noqa`, `// eslint-disable-next-line`, `#pragma warning disable`, `@SuppressWarnings`, `// noinspection` |

## Approval Workflow

When a diagnostic survives the post-implementation pass and looks like a
suppression candidate, the agent must:

1. **Name the diagnostic.** Identify the exact rule and show the message.
   "The type checker complains" is not enough.
2. **Present the correct fix first** as the primary recommendation.
3. **Explain why the fix is not viable**, only if it genuinely is not.
   "Inconvenient" and "verbose" do not count.
4. **Propose the suppression as the second option** -- the exact pragma, the
   required justification comment, and the narrowest possible scope.
5. **Wait for the user to choose.** Do not default to the suppression.

## Antipattern Catalog

### Suppression Antipatterns

#### 1. Coverage Suppression Instead of Writing the Spec

**The antipattern:** A line is hard to reach in tests, so the agent marks it
`# pragma: no cover` instead of writing the spec or removing dead code.

**Why it's wrong:** Coverage = specification completeness. A suppressed line is
an unspecified line. The correct dispositions are:

- **Reachable requirement** → write the spec.
- **Dead code** → remove it.
- **Genuinely unreachable** (e.g., defensive `assert False` after exhaustive
  match) → propose the pragma with justification; wait for approval.

"Hard to test" is not "unreachable."

#### 2. Type-Ignore Instead of Type Stubs

**The antipattern:** A third-party library ships without type information.
Instead of creating a stub file, the agent sprinkles `# type: ignore` on every
call site.

**Why it's wrong:** Each `# type: ignore` silences *all* diagnostics on that
line -- not just the missing-stub error. Real type bugs on the same line become
invisible. The suppressions multiply as more call sites are added, and nobody
remembers which ones are still needed.

**The correct fix:**

- **Check for existing stubs first.** Many popular libraries have stubs on PyPI
  (`types-requests`, `types-pyyaml`, etc.) or in `typeshed`. Install the stub
  package.
- **If no published stubs exist,** create a minimal stub file in the project's
  `typings/` directory (or equivalent). The stub only needs to cover the
  symbols actually used -- not the entire library.
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

#### 3. Type-Ignore Instead of Narrowing

**The antipattern:** A value has type `T | None`. Instead of narrowing with a
guard, the agent adds `# type: ignore` or uses a force-unwrap (`!` in TS,
`cast()` in Python).

**Why it's wrong:** The type checker is telling you the None case is unhandled.
Silencing it doesn't handle it -- it hides a potential `NoneType` crash at
runtime.

**The correct fix:**

```python
# ❌ Suppress the symptom
value = maybe_none.strip()  # type: ignore[union-attr]

# ❌ Force-cast -- hides the None case
value = cast(str, maybe_none).strip()

# ✅ Narrow -- handle the None case explicitly
if maybe_none is None:
    raise ValueError("Expected a value but got None")
value = maybe_none.strip()

# ✅ Or provide a default
value = (maybe_none or "").strip()
```

```typescript
// ❌ Non-null assertion -- hides the undefined case
const name = user!.name;

// ✅ Narrow -- handle the undefined case
if (!user) {
    throw new Error("Expected user to be defined");
}
const name = user.name;
```

#### 4. Broad Suppressions Instead of Narrow Ones

**The antipattern:** When a suppression is justified, the agent uses the broadest
form available -- file-level `# noqa`, `/* eslint-disable */`, `@ts-nocheck`,
`#pragma warning disable` without a matching `restore`.

**Why it's wrong:** Broad suppressions silence diagnostics beyond the one that
triggered them. New code added to the same file inherits the suppression
silently. The original reason becomes invisible.

**When a suppression is approved, it must be:**

- **Line-level**, not file-level or block-level.
- **Rule-specific** -- name the exact diagnostic being suppressed.
- **Commented** -- include a justification that explains *why*.

```python
# ❌ Broad
# type: ignore

# ✅ Narrow with reason
# type: ignore[import-untyped]  # no published stubs for this lib; stub in typings/
```

### Evasion Antipatterns

#### 5. Catch-All Exception Handling as a Runtime Pragma

**The antipattern:** Instead of handling specific failure modes, the agent wraps
code in `except Exception` (or equivalent) to suppress errors at runtime --
achieving the same silencing effect through different means.

**Why it's wrong:** The broad catch hides bugs, swallows unexpected errors, and
makes debugging impossible. It's a runtime pragma.

**The correct fix:** Catch the specific exception types that represent known
failure modes. Let unexpected exceptions propagate.

#### 6. Test-Only Parameters on Production APIs

**The antipattern:** A production function is hard to test because it calls
another function internally (e.g., `load_settings()`). Instead of mocking at
the I/O boundary, the agent adds a parameter to the production function so
tests can inject the dependency directly.

**Why it's wrong:** The parameter exists solely for test convenience -- no
production caller uses it. This pollutes the public API with test concerns,
hides the real I/O boundary from the test suite, and skips exercising the
production code path in every test that uses the shortcut.

**How to detect it:**

- A parameter has a default of `None` and the only non-`None` callers are tests.
- Other functions with the same dependency don't have the parameter -- they call
  the dependency internally and their tests already mock at the I/O boundary.
- Removing the parameter would not break any production code path.

**The correct fix:** Find the I/O boundary the dependency uses (file read,
network call, environment variable) and mock *that*. For file-based config,
write a real config file to `tmp_path` and `chdir` into it. For environment
variables, use `monkeypatch.setenv`. For network calls, mock the HTTP client.
The test should exercise the same code path production uses.

## Relationship to Other Skills

- **Language-specific standards** (`python-code-standards`, etc.) define *how*
  to format an approved suppression (scope, syntax, required comments).
- **`bdd-testing`** owns the 100% coverage rule and uncovered-line dispositions.
  This skill enforces the same rule against `pragma: no cover`.
- **`code-quality-audit`** operationalizes these antipatterns into a systematic
  inspection procedure with structured output.
- **`skill-compliance`** routes to this skill via the cross-cutting rule -- it
  applies alongside whatever task-specific skills are active.

## On Invocation

1. **Writing or modifying code?** Pragmas are off the table. Fix the code.
2. **Running a final lint or type-check pass?** If a diagnostic resists clean
   fixing, follow the Approval Workflow before adding any suppression.
3. **Reviewing code?** Flag any uncommented, broad, or unapproved pragma as a
   violation.
4. **Encountered an existing pragma while editing?** Do not propagate the
   pattern. If the cause is now fixable, remove the pragma; otherwise leave it
   and note it.
