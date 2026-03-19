#!/usr/bin/env python3
"""Rewrite WHAT sections in test class docstrings using Copilot CLI.

For each test class, extracts the GWT docstrings from all test methods,
then asks Copilot to produce accurate, numbered WHAT clauses — one per
test method — and patches the result back into the file.

Usage:
    # Dry run (default) — prints proposed rewrites, touches nothing
    python rewrite_what_clauses.py

    # Apply rewrites to files
    python rewrite_what_clauses.py --apply

    # Limit to specific files (substring match)
    python rewrite_what_clauses.py --filter test_browser

    # Limit to specific classes (substring match)
    python rewrite_what_clauses.py --class TestAuthenticationFailures

    # Show skipped classes
    python rewrite_what_clauses.py --verbose

    # Specify a custom tests directory
    python rewrite_what_clauses.py --tests-dir path/to/tests

Requirements:
    - GitHub Copilot CLI installed and authenticated (`copilot` in PATH)
    - Run from any repo root that follows the bdd-testing convention,
      or pass --tests-dir to point at the test directory explicitly
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

COPILOT_TIMEOUT = 120  # seconds per class


# ---------------------------------------------------------------------------
# Repo discovery
# ---------------------------------------------------------------------------

def find_tests_dir(explicit: str | None) -> Path:
    """Resolve the tests directory from explicit arg, env var, or cwd convention."""
    if explicit:
        p = Path(explicit)
        if not p.is_dir():
            print(f"ERROR: --tests-dir {p} is not a directory")
            sys.exit(1)
        return p

    repo_root = Path(os.environ.get("REPO_ROOT", Path.cwd()))
    tests = repo_root / "tests"
    if tests.is_dir():
        return tests

    print(f"ERROR: tests/ not found at {tests}")
    print("Run from a repo root, set REPO_ROOT, or pass --tests-dir")
    sys.exit(1)


# ---------------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------------

def get_class_docstring_node(class_node: ast.ClassDef) -> ast.Constant | None:
    """Return the docstring AST node for a class, or None."""
    if (
        class_node.body
        and isinstance(class_node.body[0], ast.Expr)
        and isinstance(class_node.body[0].value, ast.Constant)
        and isinstance(class_node.body[0].value.value, str)
    ):
        return class_node.body[0].value
    return None


def extract_what_block(docstring: str) -> tuple[int, int] | None:
    """Return (start_line, end_line) of WHAT: section within the docstring.

    Line numbers are relative to the docstring content (0-indexed).
    Returns None if no WHAT section found.
    """
    lines = docstring.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.match(r"\s*WHAT:", ln):
            start = i
        if start is not None and i > start and re.match(r"\s*(WHY|MOCK BOUNDARY):", ln):
            return start, i
    if start is not None:
        return start, len(lines)
    return None


def extract_test_methods(
    class_node: ast.ClassDef,
    source_lines: list[str],
) -> list[dict[str, str]]:
    """Return list of {name, docstring, first_assert} for each test method."""
    methods: list[dict[str, str]] = []
    for node in ast.iter_child_nodes(class_node):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not node.name.startswith("test_"):
            continue

        docstring = ast.get_docstring(node, clean=True) or ""

        first_assert = ""
        for i in range(node.lineno - 1, min((node.end_lineno or node.lineno), len(source_lines))):
            stripped = source_lines[i].strip()
            if stripped.startswith("assert "):
                first_assert = stripped[:120]
                break

        methods.append({
            "name": node.name,
            "docstring": docstring,
            "first_assert": first_assert,
        })
    return methods


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def build_prompt(class_name: str, methods: list[dict[str, str]]) -> str:
    """Build the prompt to send to Copilot."""
    method_block = ""
    for i, m in enumerate(methods, 1):
        method_block += f"\n--- Test {i}: {m['name']} ---\n"
        if m["docstring"]:
            method_block += textwrap.indent(m["docstring"].strip(), "  ") + "\n"
        if m["first_assert"]:
            method_block += f"  Key assertion: {m['first_assert']}\n"

    n = len(methods)
    return (
        f"You are rewriting the WHAT section of a BDD test class docstring.\n\n"
        f"Class: {class_name}\n"
        f"Number of test methods: {n}\n\n"
        f"IMPORTANT: Delete and completely disregard any existing WHAT clauses -- "
        f"they are inaccurate or incorrectly numbered and must not influence your output. "
        f"Derive all clauses solely from the test methods listed below.\n\n"
        f"Each test method has a GWT (Given/When/Then) docstring describing what it proves. "
        f"Your job: write exactly {n} numbered WHAT clauses, one per test, in the same order.\n\n"
        f"Rules:\n"
        f"- Output ONLY the numbered clauses -- no explanation, no intro, no markdown, nothing else\n"
        f"- Format exactly: (1) first clause text\n"
        f"                  (2) second clause text\n"
        f"                  ... continuing through ({n})\n"
        f"- Each clause must be a single sentence with no semicolons splitting sub-clauses\n"
        f"- Each clause must accurately describe what ITS test proves, derived from its THEN line\n"
        f"- Write in present tense, active voice, from the system's perspective\n"
        f"- Do not duplicate clauses -- even if two tests cover similar ground, describe each distinctly\n"
        f"- There must be exactly {n} clauses numbered (1) through ({n}) -- no more, no fewer\n\n"
        f"Tests:\n"
        f"{method_block}\n"
        f"Output the {n} numbered WHAT clauses now:"
    )


# ---------------------------------------------------------------------------
# Copilot CLI call
# ---------------------------------------------------------------------------

def call_copilot(prompt: str) -> str:
    """Send prompt to Copilot CLI non-interactively and return response text."""
    cmd = ["copilot", "-p", prompt, "--silent", "--allow-all-tools"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=COPILOT_TIMEOUT,
        )
        output = result.stdout.strip()
        if result.returncode != 0 and not output:
            raise RuntimeError(
                f"copilot exited {result.returncode}: {result.stderr.strip()[:300]}"
            )
        return output
    except subprocess.TimeoutExpired as e:
        raise RuntimeError(f"copilot timed out after {COPILOT_TIMEOUT}s") from e
    except FileNotFoundError as e:
        raise RuntimeError("copilot not found in PATH -- is Copilot CLI installed?") from e


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def parse_what_clauses(response: str, expected: int) -> list[str] | None:
    """Parse numbered clauses from Copilot response.

    Returns list of full clause strings like '(1) clause text', or None
    if parsing fails or clause count doesn't match expected.
    """
    clauses: list[str] = []
    current: str | None = None

    for line in response.splitlines():
        stripped = line.strip()
        m = re.match(r"^\((\d+)\)\s+(.+)", stripped)
        if m:
            if current is not None:
                clauses.append(current)
            current = f"({m.group(1)}) {m.group(2)}"
        elif current is not None and stripped and not stripped.startswith("("):
            # Continuation line
            current += " " + stripped

    if current is not None:
        clauses.append(current)

    if len(clauses) != expected:
        return None

    return clauses


# ---------------------------------------------------------------------------
# Docstring patching
# ---------------------------------------------------------------------------

def build_new_what_block(clauses: list[str], indent: str) -> list[str]:
    """Build replacement WHAT block lines with correct indentation."""
    if not clauses:
        return []
    lines = [f"{indent}WHAT: {clauses[0]}"]
    for clause in clauses[1:]:
        lines.append(f"{indent}      {clause}")
    return lines


def patch_docstring(
    source: str,
    class_node: ast.ClassDef,
    new_clauses: list[str],
) -> str | None:
    """Return patched source with WHAT section replaced, or None on failure."""
    doc_node = get_class_docstring_node(class_node)
    if doc_node is None:
        return None

    docstring = doc_node.value
    if docstring is None:
        return None
    assert isinstance(docstring, str)
    what_range = extract_what_block(docstring)
    if what_range is None:
        return None

    what_start, what_end = what_range
    doc_lines = docstring.splitlines()

    # Determine indent from the WHAT: line
    what_line = doc_lines[what_start]
    indent_match = re.match(r"^(\s*)", what_line)
    indent = indent_match.group(1) if indent_match else "    "

    new_what_lines = build_new_what_block(new_clauses, indent)
    patched_doc_lines = doc_lines[:what_start] + new_what_lines + doc_lines[what_end:]
    new_docstring = "\n".join(patched_doc_lines)

    old_escaped = re.escape(docstring)
    new_source = re.sub(old_escaped, lambda _: new_docstring, source, count=1)

    if new_source == source:
        return None

    return new_source


# ---------------------------------------------------------------------------
# Per-class processing
# ---------------------------------------------------------------------------

def process_class(
    class_node: ast.ClassDef,
    source: str,
    source_lines: list[str],
    apply: bool,
    verbose: bool,
) -> str | None:
    """Process one test class. Returns new source if changed, else None."""
    class_name = class_node.name

    doc_node = get_class_docstring_node(class_node)
    if doc_node is None:
        if verbose:
            print(f"  SKIP {class_name} -- no docstring")
        return None

    what_range = extract_what_block(str(doc_node.value))
    if what_range is None:
        if verbose:
            print(f"  SKIP {class_name} -- no WHAT block")
        return None

    methods = extract_test_methods(class_node, source_lines)
    if not methods:
        if verbose:
            print(f"  SKIP {class_name} -- no test methods")
        return None

    print(f"  -> {class_name} ({len(methods)} tests) ... ", end="", flush=True)

    prompt = build_prompt(class_name, methods)

    try:
        response = call_copilot(prompt)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        return None

    clauses = parse_what_clauses(response, len(methods))
    if clauses is None:
        print("PARSE ERROR -- unexpected clause count")
        if verbose:
            print(f"    Response:\n{textwrap.indent(response, '      ')}")
        return None

    new_source = patch_docstring(source, class_node, clauses)
    if new_source is None:
        print("PATCH ERROR -- could not apply replacement")
        return None

    if apply:
        print("REWRITTEN")
    else:
        print("DRY RUN")
        print("    Proposed WHAT clauses:")
        for c in clauses:
            print(f"      {c}")

    return new_source


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write changes to files")
    parser.add_argument("--filter", default="", help="Only process files matching this substring")
    parser.add_argument(
        "--class", dest="class_filter", default="",
        help="Only process classes matching this substring",
    )
    parser.add_argument(
        "--tests-dir", default=None,
        help="Path to tests directory (default: $REPO_ROOT/tests or ./tests)",
    )
    parser.add_argument("--verbose", action="store_true", help="Show skipped classes and error detail")
    args = parser.parse_args()

    tests_dir = find_tests_dir(args.tests_dir)
    repo_root = tests_dir.parent

    test_files = sorted(tests_dir.glob("test_*.py"))
    if args.filter:
        test_files = [f for f in test_files if args.filter in f.name]

    if not test_files:
        print("No test files matched.")
        sys.exit(0)

    mode = "APPLYING" if args.apply else "DRY RUN"
    print(f"\n{'='*60}")
    print(f"rewrite_what_clauses.py  --  {mode}")
    print(f"Repo:  {repo_root}")
    print(f"Tests: {tests_dir}")
    print(f"Files: {len(test_files)}")
    print(f"{'='*60}\n")

    total_classes = 0
    rewritten = 0
    errors = 0

    for path in test_files:
        source = path.read_text(encoding="utf-8")
        source_lines = source.splitlines()

        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as e:
            print(f"\n{path.name}: SYNTAX ERROR -- {e}")
            errors += 1
            continue

        classes = [
            n for n in ast.iter_child_nodes(tree)
            if isinstance(n, ast.ClassDef)
            and n.name.startswith("Test")
            and (not args.class_filter or args.class_filter in n.name)
        ]

        if not classes:
            continue

        print(f"\n{path.name} ({len(classes)} classes)")

        current_source = source
        file_changed = False

        for class_node in classes:
            total_classes += 1
            new_source = process_class(
                class_node,
                current_source,
                source_lines,
                apply=args.apply,
                verbose=args.verbose,
            )
            if new_source is None:
                continue

            if new_source != current_source:
                current_source = new_source
                file_changed = True
                rewritten += 1

        if file_changed and args.apply:
            path.write_text(current_source, encoding="utf-8")
            print(f"  wrote {path.name}")

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"  Classes processed: {total_classes}")
    print(f"  Rewritten:         {rewritten}")
    print(f"  Errors:            {errors}")
    if not args.apply:
        print("\n  Run with --apply to write changes.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
