---
name: bdd-testing
description: "BDD test conventions for this repository. Use when writing, modifying, or reviewing test files, including creating tests for new features and adding coverage specs. ALSO use when running coverage checks, reporting coverage results, or auditing code coverage -- this skill defines the 100% coverage requirement and remediation procedure."
---

# BDD Testing -- How to Write Tests

## Iron Laws

1. **Specify the system, not units.** Mock only at the I/O boundary; never mock our own code. If a function lives in our codebase, it runs for real.
2. **Three-part contract on every test method.** Method name (the claim) + Given/When/Then docstring (the scenario) + `# Given/When/Then` body comments (the structure). All three required; none substitutes for the others.
3. **Class docstrings are REQUIREMENT/WHO/WHAT/WHY + MOCK BOUNDARY.** WHAT is enumerated, not summarized. WHAT count = test count.
4. **Public API only.** No imports of `_`-prefixed names. If a failure condition can't be induced through public inputs, it's dead code.
5. **Diagnostic message on every assertion.** Bare asserts are prohibited.
6. **100% coverage is the only passing score.** Sub-100% is a blocking failure -- write the spec or remove the code. "Pre-existing" is not a disposition.
7. **Failure-mode specs are mandatory.** Missing input, unavailable services, invalid config, boundary values, partial failures.

## Role in the Skill System

Source of truth for test-quality rules. Use this skill for "what is correct?" Use `bdd-feedback-loop` for "what steps do I run now?" The feedback loop cites this skill for normative rules; do not duplicate them there.

## Language References

This file is language-agnostic. For toolchain-specific examples and commands:

- `references/python.md`
- `references/typescript.md`
- `references/java.md`
- `references/csharp.md`

## I/O Boundary

The boundary is where the **system** ends and the **environment** begins. The system under test is the full call chain from public entry point down to that boundary -- every layer in between runs for real.

| I/O boundary (mock these) | Part of the system (never mock) |
| --- | --- |
| Process spawning (subprocess, exec, spawn) | Our function that wraps the process call |
| HTTP calls (client libraries, fetch) | Our function that calls the HTTP client |
| Database wire calls (connection/query) | Our caching/repository logic over the connection |
| Process-level state (cwd, env vars) | Filesystem operations against a test directory |

Assertions on mock internals -- call counts, specific arguments passed to the mock, `assert_called_with`, `call_args` -- are substitution failures. They couple the test to this specific implementation rather than to any conforming one at the boundary. Assert on observable outputs through the public API instead: what the system returned, what state changed, what error was raised. If a behavior cannot be observed through the public API, it either requires a port to be extracted or is not a testable requirement. Ask yourself: _"If I were to swap in the unmocked implementation, would the test still pass?_ If the answer is no, it is not a requirement and should not be asserted.

If you find yourself mocking a function in your own codebase, stop -- trace the call chain to the actual I/O operation and mock that instead. For filesystem interactions, use the test framework's temp directory facility.

Foundational pure functions (URL parsers, math, config validation) need no mocks at all -- they have no I/O and no layers to compose.

See `references/test-patterns.md` → _Mocking Rules_ and _Tautology Tests_ for correct vs. tautological system specs. Language references show concrete I/O boundaries and temp-directory patterns.

## The Hierarchy

| Level | Form | Question Answered |
| --- | --- | --- |
| **Test class** | REQUIREMENT / WHO / WHAT / WHY | What user story does this group prove? |
| **Test method** | Given / When / Then scenario | Under what specific conditions does the behavior occur? |
| **Test body** | Given / When / Then comments | How is the scenario implemented in code? |

The class captures the user story; WHAT enumerates the scenarios needed to prove it; each method specifies one scenario in full.

## Test Organization

Group by **consumer requirement**, not by code structure or persona. Names like `TestPluginRegistration` or `TestScoreCalculation` describe a promise the system makes. A single file may contain multiple requirement classes when they exercise the same module.

## Class Docstring -- REQUIREMENT / WHO / WHAT / WHY

| Field | Purpose | Question It Answers |
| --- | --- | --- |
| **REQUIREMENT** | One-line capability statement | What promise does this group verify? |
| **WHO** | Stakeholder or consumer | Who benefits when this is met? |
| **WHAT** | Enumerated testable behaviors | What observable behavior proves it? |
| **WHY** | Business/operational justification | What goes wrong if it's missing? |

**WHAT must enumerate, not summarize.** Write WHAT as a numbered list of claims, one per testable scenario. A test method that cannot trace to any WHAT clause is speculative; a WHAT clause with no implementing test is a coverage gap.

**WHAT count = test count.** Every WHAT clause maps to exactly one test method and every test method traces to exactly one WHAT clause.

See `references/test-patterns.md` → _Mock Boundary Contract -- Full Examples_.

## Mock Boundary Contract (required per class)

Every test class includes a MOCK BOUNDARY declaration immediately after the WHO/WHAT/WHY block. Three lines:

- **Mock** -- what is patched and which fixture to use
- **Real** -- what runs for real (computation, filesystem, embedded DB)
- **Never** -- what must not be constructed or mocked directly

For pure-computation classes, write `Mock: nothing -- this class tests pure computation`. The line is still required so the intent is explicit.

## Method Docstring, Body, and Naming

- **Docstring:** Given / When / Then scenario format. Always include Given; the only exception is when the precondition is the default state from conftest fixtures. Never user-story format ("As a … I want …").
- **Body:** `# Given:`, `# When:`, `# Then:` comments delineate setup, action, and assertion phases. Comments must be **descriptive**, not bare labels -- each names the concrete state, action, or expected outcome at that line (e.g., `# Given: a parser configured with the 2024 tax schedule`). The `# Given:` comment is always present even when the docstring elides it.
- **Name:** A behavior statement, not an implementation description. `test_parser_normalizes_hourly_to_annual` ✅ -- `test_multiply_by_2080` ❌.

The docstring proves _what scenario_ is being verified; the body comments show _how_ each step is realized in code. Both are required.

See `references/test-patterns.md` → _The Three-Part Contract_.

## Assertion Quality

Every assertion includes a diagnostic message showing expected vs. actual and enough context to diagnose without a debugger. Bare `assert x` or `assert len(items) == 3` are prohibited. See `references/test-patterns.md` → _Assertion Quality_.

## Test Data

Use **representative** data -- close enough to real-world values that failures mean something. Placeholder strings like `"t"` for title produce opaque failures. Magic numbers are acceptable when their meaning is stated in a comment or assertion message. See `references/test-patterns.md` → _Test Data_.

## Coverage Procedure

100% coverage means every line of production code has a spec justifying it. Every uncovered line triggers the question: _"Which requirement is this line serving?"_

When running, checking, or reporting coverage, apply these steps **in order**:

1. **Run coverage.** Use the language-appropriate command.
2. **If 100% statement AND branch coverage:** report and stop.
3. **If below 100%:** this is a blocking failure. Do not summarize and move on. Instead: a. Identify every uncovered line and partial branch. b. For each, determine the disposition: **write the spec** (real requirement) or **remove the code** (dead code / over-engineering). c. Implement the disposition immediately. d. Re-run coverage to confirm 100%. Repeat until 100% is achieved.

Never describe uncovered lines as "backfill candidates", "pre-existing gaps", "low-priority", or "known issues". There are no categories of acceptable incompleteness. **"Pre-existing" is not a disposition** -- whether a line existed before your changes is irrelevant. The only valid dispositions are real requirement (spec it), dead code (remove it), or over-engineering (remove it).

### What surfaces at coverage time

Three categories of real requirements typically surface only at coverage time:

| Category | Description | Example |
| --- | --- | --- |
| **Defensive guard code** | Protects against misuse -- empty input, wrong types, boundary values | `if not full_text.strip(): raise ValidationError(...)` |
| **Graceful degradation** | Soft failures the system absorbs rather than raising | Missing `history` collection returns empty list, not error |
| **Conditional formatting** | Display logic that varies by state | Warning line only appears when `is_flagged=True` |

## Reading `src/` and Public APIs

Specs and tests **define** the public API; they do not reverse-engineer it from existing code. The default flow is spec-first: tests assert on observable behavior through the public API, and implementation follows. Reading `src/` is therefore a context-dependent activity:

- **New code (spec-first, the default).** No `src/` exists yet for the unit under test. The public API is defined by the spec and the design note; mock boundaries are chosen from the design's predicted I/O surface (process spawn, HTTP, DB wire, env). Tests are drafted before implementation, fail, then drive the implementation. Reading neighboring `src/` modules to discover _existing_ public APIs they expose is fine and expected.
- **Backfilling tests on existing code.** When tests are being added to code that already exists (legacy coverage work, refactors, audits), read `src/` in two passes:
  1. **Public API discovery.** Signatures, return types, constructor parameters, public vs. private names.
  2. **I/O boundary identification.** After specs are drafted from the public API, trace each call chain to its actual I/O boundary so the mock contract is set at the correct edge.

**No other reason to read `src/` is valid.** Do not mine it for internal functions to mock, branches to enumerate, or implementation shapes to mirror in tests -- in either flow.

Tests exercise internal logic **through the public API**. When a private function seems worth testing directly:

1. **Default -- test it through the public API.** Find the public entry point.
2. **Override, don't import.** Overriding a private _variable_ or injecting a dependency is acceptable; importing private _functions_ is not.
3. **Promote only when production code needs it.** Test convenience alone is never a reason to promote.

If a failure condition cannot be induced through public API inputs alone, flag it as potential dead code. See `references/test-patterns.md` → _No Private-Function Imports_. For suppression rules when legacy private imports exist, see `code-quality-antipatterns`.

## Error Testing and Failure-Mode Specs

When testing error paths, assert both exception type AND meaningful message content -- not just "some exception occurred". Errors must include enough context for an operator to diagnose without consulting source code.

An unspecified failure is an unhandled failure. Every feature's spec covers:

- Missing or malformed input
- External service unavailable
- Invalid configuration
- Boundary values
- Partial failure (one item in a batch fails, others continue)

## On Invocation

1. Read this skill and the language reference for your project.
2. Locate or create the test file; group classes by consumer requirement.
3. For each class: write REQUIREMENT/WHO/WHAT/WHY + MOCK BOUNDARY.
   - **New code:** derive the mock boundary from the design note's predicted I/O surface.
   - **Backfilling tests:** read `src/` for public API discovery first, then trace call chains to their I/O boundaries.
4. For each WHAT clause: draft a test method with the three-part contract, asserting on observable behavior through the public API only.
5. Verify mocks sit only at the I/O boundary. For new code, the tests fail at this point and drive the implementation; for backfill work, run against existing code.
6. Run tests and coverage; remediate any sub-100% per the coverage procedure.

## Reference Documents

- `references/test-patterns.md` -- mock boundary contracts, tautology anti-patterns, assertion quality, test data
- `references/python.md`, `references/typescript.md`, `references/java.md`, `references/csharp.md` -- language-specific examples and commands
- `scripts/` -- maintenance scripts (WHAT clause rewriting, audits); see each script's `--help` for usage
