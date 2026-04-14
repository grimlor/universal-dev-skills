---
name: bdd-testing
description: "BDD test conventions for this repository. Use when writing, modifying, or reviewing test files, including creating tests for new features and adding coverage specs. ALSO use when running coverage checks, reporting coverage results, or auditing code coverage -- this skill defines the 100% coverage requirement and remediation procedure."
---

# BDD Testing -- How to Write Tests

## When This Skill Applies

Whenever writing, modifying, or reviewing test files. This includes
creating tests for new features (Phase 2 of the feature workflow) and adding coverage
specs (Phase 4).

## Role in the Skill System

`bdd-testing` is the **source of truth** for test-quality rules and conventions.

- If the question is "what is correct?", use this skill.
- If the question is "what steps do I run now?", use `bdd-feedback-loop`.

The feedback-loop skill is an execution runbook. It should reference this skill for
normative quality rules rather than duplicating them.

## Language References

This file defines language-agnostic BDD testing rules. For language/toolchain-specific
examples and commands, use:

- `references/python.md`
- `references/typescript.md`
- `references/java.md`
- `references/csharp.md`

---

## Foundational Principle -- System Specification, Not Unit Testing

We are not testing units in isolation. We are **specifying a system**.

The system under test is the full call chain from the public entry point down to the
I/O boundary. Every layer of the system runs for real -- Layer 3 composes Layer 2,
which composes Layer 1, all the way down to the process/network/hardware edge. The
only mock is at that edge.

This means:

- **Inter-layer interactions are the point.** If Layer 3 calls Layer 2 which calls
  Layer 1, all three run for real. Mocking Layer 1 from a Layer 3 test would hide
  integration defects -- the very bugs that matter most.
- **The mock boundary is where the system ends**, not where a module ends. A function
  in our codebase is part of the system regardless of which module or layer it lives
  in. `subprocess.run` is not part of our system. `discover_repositories` is, even
  though it calls `subprocess.run`.
- **The exception is foundational pure functions.** Functions with no system
  dependencies (e.g., URL parsers, math, config validation) can be tested directly
  with no mocks at all -- they have no I/O to mock and no layers to compose.

See `references/test-patterns.md` → *Mocking Rules* and *Tautology Tests* for
full examples of correct vs. tautological system specs.

### What counts as an I/O boundary?

The boundary is where the **system** ends and the **environment** begins:

| I/O boundary (mock these) | Part of the system (never mock) |
|---|---|
| `subprocess.run` -- spawns a process | `discover_repositories` -- our function that calls subprocess |
| `requests.get` -- HTTP call | `fetch_details` -- our function that calls requests |
| `Connection.query` -- database wire call | `RepoContext.get` -- our caching logic over discovery |
| `os.getcwd` -- process-level state | `os.path.exists` with `tmp_path` -- use real filesystem instead |

If you find yourself mocking a function in your own codebase, stop. Trace the call
chain to the actual I/O operation and mock that instead. Use `tmp_path` for real
filesystem structure so that `os.path.exists`, `os.listdir`, and `os.path.isdir` all
run against real directories.

---

## The Hierarchy

BDD in this repo has three levels. Each level answers a different question:

| Level | Form | Question Answered |
|---|---|---|
| **Test class** | REQUIREMENT / WHO / WHAT / WHY | What user story does this group prove? |
| **Test method** | Given / When / Then scenario | Under what specific conditions does the behavior occur? |
| **Test body** | Given / When / Then comments | How is the scenario implemented in code? |

The class captures the user story. The WHAT field enumerates which scenarios are needed
to prove it -- if WHAT is well-written, the list of required test methods should follow
from it directly. Each method then specifies one of those scenarios in full.

---

## Test Organization

Tests are organized by **consumer requirement**, not by code structure or persona.
Group by what the system promises (`TestPluginRegistration`, `TestScoreCalculation`),
not by module name or persona. A single file may contain multiple requirement classes
when they exercise the same module.

---

## The Three-Part Contract

Every test method requires all three of the following. None substitutes for the others:

| Part | Purpose | Serves |
|---|---|---|
| **Method name** | The claim -- behavior stated as a fact | Scanability; test output |
| **Given / When / Then docstring** | The scenario -- explicit conditions and observable outcome | Precision; review; spec traceability |
| **Given / When / Then body comments** | The structure -- setup, action, assertion delineated | Readability; maintenance |

A good name without a docstring leaves the scenario ambiguous. A docstring without
body comments buries the structure in undifferentiated code. All three are required
on every test method.

Note that the method docstring and the body comments serve different purposes even
though they share the Given/When/Then form. The docstring is the *specification* --
legible in isolation in test output, spec reports, and code review. The body comments
are the *structure* -- they delineate setup, action, and assertion for the reader
inside the code. The docstring captures semantic intent; the body comments map that
intent to concrete lines. Both are required; neither substitutes for the other.

---

## Class-Level Docstrings -- REQUIREMENT / WHO / WHAT / WHY

Every test class MUST have a structured docstring with these four fields:

| Field | Purpose | Question It Answers |
|-------|---------|---------------------|
| **REQUIREMENT** | One-line capability statement | What promise does this group verify? |
| **WHO** | Stakeholder or consumer | Who benefits when this is met? |
| **WHAT** | Enumerated testable behaviors | What observable behavior proves it? |
| **WHY** | Business/operational justification | What goes wrong if it's missing? |

**WHAT must enumerate, not summarize.** Write WHAT as a numbered list of claims --
one per testable scenario. A test method that cannot trace to any WHAT clause is
speculative or WHAT is incomplete. A WHAT clause with no implementing test method
is a coverage gap.

**WHAT count = test count.** Every WHAT clause maps to exactly one test method and
every test method traces to exactly one WHAT clause. If the counts diverge, either
WHAT is missing a clause or the test suite has speculative/undocumented tests.

See `references/test-patterns.md` → *Mock Boundary Contract -- Full Examples* for
complete class docstring examples.

---

## Mock Boundary Contract (REQUIRED per class)

Every test class must include a MOCK BOUNDARY declaration immediately after the
WHO/WHAT/WHY block. The three lines answer:

- **Mock** -- what is patched and which fixture to use
- **Real** -- what runs for real (computation, filesystem, embedded DB)
- **Never** -- what must not be constructed or mocked directly

If a test class has no I/O, the Mock line reads `Mock: nothing -- this class tests
pure computation`. This is still required so the intent is explicit.

---

## Method-Level Docstrings -- Given / When / Then (REQUIRED)

Every test method MUST have a Given / When / Then docstring.

**Always include Given in the docstring.** The only exception is when the
precondition is the default state established by conftest fixtures and adds no
distinguishing information. Even then, the `# Given:` body comment is always present.

Use scenario format only -- never user-story format ("As a … I want …").
See `references/test-patterns.md` → *The Three-Part Contract* for full examples.

---

## Method Naming

Names read as **behavior statements**, not implementation descriptions.
`test_parser_normalizes_hourly_to_annual` ✅ -- `test_multiply_by_2080` ❌.

---

## Test Body Structure -- Given / When / Then (REQUIRED)

Every test method body MUST use `# Given:`, `# When:`, `# Then:` comments to
delineate setup, action, and assertion phases. See `references/test-patterns.md`
for full examples.

---

## Assertion Quality (REQUIRED on every assertion)

Every assertion MUST include a diagnostic message. Bare assertions (`assert x`,
`assert len(items) == 3`) are prohibited. Messages must show expected vs. actual
and enough context to diagnose without a debugger. See `references/test-patterns.md`
→ *Assertion Quality* for examples.

---

## Test Data

Test data should be **representative** -- close enough to real-world values that
failures mean something. Placeholder strings like `"t"` for title produce opaque
failures. Magic numbers are acceptable when their meaning is stated in a comment
or assertion message. See `references/test-patterns.md` → *Test Data* for examples.

---

## Coverage = Complete Specification

100% coverage means every line of production code has a spec justifying it.
**100% is the only passing score.** Any value below 100% -- including 99% -- is a
specification gap that must be remediated before the task is complete.

After all spec tests pass, run the language-appropriate coverage command from the
language reference file.

Every uncovered line triggers the question: *"Which requirement is this line serving?"*

### Coverage check procedure (REQUIRED)

When asked to run, check, or report coverage -- or when coverage results appear
during any workflow -- apply these steps **in order**:

1. **Run coverage.** Use the language-appropriate coverage command.
2. **If 100% statement AND branch coverage: report and stop.** The system is
   fully specified.
3. **If below 100%: this is a blocking failure.** Do not summarize and move on.
   Instead:
   a. Identify every uncovered line and partial branch.
   b. For each, determine the disposition: **write the spec** (real requirement),
      or **remove the code** (dead code / over-engineering).
   c. Implement the disposition immediately -- write the missing specs or remove
      the unjustified code.
   d. Re-run coverage to confirm 100%.
   e. Repeat until 100% is achieved.

**Do not report sub-100% coverage as acceptable.** Do not describe uncovered lines
as "backfill candidates", "pre-existing gaps", "low-priority", or "known issues".
There are no categories of acceptable incompleteness. Every uncovered line is a
current obligation, regardless of when it was introduced.

### What surfaces at coverage time

Three categories of requirements surface only at coverage time -- they are real
requirements, not optional extras:

| Category | Description | Example |
|---|---|---|
| **Defensive guard code** | Protects against misuse -- empty input, wrong types, boundary values | `if not full_text.strip(): raise ValidationError(...)` |
| **Graceful degradation** | Soft failures the system absorbs rather than raising | Missing `history` collection returns empty list, not error |
| **Conditional formatting** | Display logic that varies by state | Warning line only appears when `is_flagged=True` |

**"Pre-existing" is not a category.** Whether a line existed before your changes is irrelevant -- if it is uncovered after your work, it is uncovered. The only valid dispositions are: real requirement (write the spec), dead code (remove it), or over-engineering (remove it). "It was already there" is not a disposition.

For each uncovered line: keep it and write the spec, or remove it if it has no
justifying requirement.

---

## Reading `src/` -- Public API Discovery Only

Before writing any test for a module, read the relevant `src/` files to discover
the real public API: method signatures, return types, constructor parameters,
and which names are public vs. private (`_` prefix).

**This is the only permitted reason to read `src/` during test writing.** Do not
use `src/` knowledge to find internal functions to mock. If a failure condition
cannot be induced through public API inputs alone, flag it as potential dead code.

---

## Public APIs Only -- No Private Imports

Tests must exercise internal logic **through the public API**, not by importing
private (`_`-prefixed) names directly. When a private function "seems worth
testing directly":

1. **Default -- test it through the public API.** Find the public entry point
   that exercises the private logic.
2. **Override, don't import.** Overriding a private *variable* or injecting a
   dependency is acceptable; importing private *functions* is not.
3. **Promote only when production code needs it.** Test convenience alone is
   never a reason to promote.

See `references/test-patterns.md` → *No Private-Function Imports* for examples.
For suppression rules when legacy private imports exist, see the
`code-quality-antipatterns` skill.

---

## Error Testing -- Messages, Not Just Types

When testing error paths, verify message content, not just that an exception was raised:

- ✅ Assert both exception type and meaningful message content.
- ❌ Do not only assert that "some exception" occurred.

Use language-specific assertion syntax from the reference files.

Errors should include enough context for the operator to diagnose the problem
without consulting source code.

---

## Failure-Mode Specs Are Mandatory

Failure-mode specs are as important as happy-path specs. An unspecified failure is
an unhandled failure. For every feature, the spec must cover:

- Missing or malformed input
- External service unavailable
- Invalid configuration
- Boundary values
- Partial failure (one item in a batch fails, others continue)

---

## Reference Documents

For detailed implementation examples including mock boundary contracts, tautology
anti-patterns, assertion quality, and test data:
- `references/test-patterns.md`

Language-specific references:
- `skills/bdd-testing/references/python.md`
- `skills/bdd-testing/references/typescript.md`
- `skills/bdd-testing/references/java.md`
- `skills/bdd-testing/references/csharp.md`

For maintenance scripts (WHAT clause rewriting, audits):
- `skills/bdd-testing/scripts/` -- see each script's `--help` for usage
