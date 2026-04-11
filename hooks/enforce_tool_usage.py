"""
PreToolUse hook engine for enforce-tool-usage.

Reads hook input from stdin, loads category and allowlist rules from a
JSON config file, and returns a deny decision when a terminal command
violates tool-usage rules.

Each segment of a chained/piped command is scanned independently against
categories (in priority order, most specific first). If no category
matches, the segment's leading command must appear on the allowed list.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, TypedDict, cast


class Category(TypedDict, total=False):
    """Type definition for a category configuration."""

    name: str
    guidance: str
    patterns: list[str]
    commands: list[str]
    subcommands: list[str]
    match: str


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------


def load_config(config_path: str) -> dict[str, Any]:
    """Load and parse the JSON rules configuration file."""
    with Path(config_path).open() as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Command parsing
# ---------------------------------------------------------------------------


def strip_quotes(cmd: str) -> str:
    """Remove single- and double-quoted strings to avoid matching argument content."""
    cmd = re.sub(r"'[^']*'", "", cmd)
    cmd = re.sub(r'"[^"]*"', "", cmd)
    return cmd


def split_segments(cmd: str) -> list[str]:
    """
    Split a command string into individual segments.

    Handles &&, ||, ;, |, and $()/ backtick subshells by treating
    subshell delimiters as segment separators.
    """
    # Treat subshell markers as segment separators
    cmd = re.sub(r"\$\(", " ; ", cmd)
    cmd = re.sub(r"`", " ; ", cmd)
    cmd = cmd.replace(")", " ")
    # Split on &&, ||, ;, |
    segments = re.split(r"&&|\|\||[;|]", cmd)
    return [s.strip() for s in segments if s.strip()]


def leading_command(segment: str) -> str:
    """
    Extract the leading command name from a segment.

    Strips ``env`` prefixes (with optional VAR=val assignments) and
    path prefixes so ``/usr/bin/env FOO=1 perl`` → ``perl``.
    """
    tokens = segment.split()
    if not tokens:
        return ""

    i = 0
    # Skip 'env' and any VAR=val assignments after it
    while i < len(tokens):
        if tokens[i] == "env" or tokens[i].endswith("/env"):
            i += 1
            while i < len(tokens) and "=" in tokens[i] and not tokens[i].startswith("-"):
                i += 1
            continue
        break

    if i >= len(tokens):
        return ""

    cmd = tokens[i]
    # Strip path: /usr/bin/perl → perl
    cmd = cmd.rsplit("/", 1)[-1]
    return cmd


def words_in_segment(segment: str) -> list[str]:
    """Extract all word tokens from a segment with paths stripped."""
    result: list[str] = []
    for token in segment.split():
        token = token.rsplit("/", 1)[-1]
        result.append(token)
    return result


# ---------------------------------------------------------------------------
# Category matching
# ---------------------------------------------------------------------------


def _matches_cmd(word: str, commands: set[str]) -> bool:
    """Check if a word matches a command, including versioned variants."""
    if word in commands:
        return True
    # Versioned variants: python3.12, node18, etc.
    return any(re.match(rf"^{re.escape(cmd)}[0-9.]+$", word) for cmd in commands)


def check_category(segment: str, category: Category) -> bool:
    """
    Check if a segment matches a category's rules.

    Evaluation order within a category:
      1. Regex patterns (always checked against the full segment text)
      2. Subcommand matching (e.g. ``git status``)
      3. Command list (respecting the ``match`` mode)
    """
    lead = leading_command(segment)
    all_words = words_in_segment(segment)
    match_mode = category.get("match", "anywhere")
    commands = set(category.get("commands", []))

    # 1. Regex patterns (always full-segment)
    for pat in category.get("patterns", []):
        if re.search(pat, segment):
            return True

    # 2. Subcommand matching
    if "subcommands" in category:
        subcommands = set(category["subcommands"])
        for cmd in commands:
            if cmd == lead or (match_mode == "anywhere" and cmd in all_words):
                for sub in subcommands:
                    if re.search(rf"\b{re.escape(cmd)}\s+{re.escape(sub)}\b", segment):
                        return True
        # Subcommand categories only match via subcommands — don't fall through
        return False

    # 3. Command list
    if match_mode == "leading_only":
        return _matches_cmd(lead, commands)
    else:
        return any(_matches_cmd(w, commands) for w in all_words)


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------


def classify(cmd: str, config: dict[str, Any]) -> dict[str, str] | None:
    """
    Classify a command against categories and the allowlist.

    Returns a dict with ``category`` and ``guidance`` if blocked,
    or ``None`` if allowed.
    """
    stripped = strip_quotes(cmd)
    segments = split_segments(stripped)
    categories = config.get("categories", [])
    allowed = set(config.get("allowed", []))

    for segment in segments:
        # Check categories in priority order (most specific first)
        for category in categories:
            if check_category(segment, category):
                return {
                    "category": category["name"],
                    "guidance": category["guidance"],
                }

        # No category matched — check the allowlist
        lead = leading_command(segment)
        if not lead:
            continue
        if lead in allowed:
            continue
        # Check versioned variants against allowlist
        if any(re.match(rf"^{re.escape(a)}[0-9.]+$", lead) for a in allowed):
            continue

        return {
            "category": "unlisted",
            "guidance": (
                f"Command '{lead}' is not on the approved list. "
                "Use a VS Code tool or ask the user to run it manually. "
                "See the tool-usage skill."
            ),
        }

    return None


# ---------------------------------------------------------------------------
# Hook response
# ---------------------------------------------------------------------------

TERMINAL_TOOLS = frozenset(
    {
        "runInTerminal",
        "run_in_terminal",
        "createAndRunTask",
        "create_and_run_task",
    }
)


def deny_response(reason: str) -> dict[str, Any]:
    """Build a deny hook response with the given reason."""
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


def main() -> None:
    """Entry point: read hook input from stdin and emit a JSON decision."""
    if len(sys.argv) < 2:
        # No config path — allow (fail open for safety during misconfiguration)
        print(json.dumps({}))
        sys.exit(0)

    config_path = sys.argv[1]
    try:
        config = load_config(config_path)
    except (OSError, json.JSONDecodeError) as exc:
        # Config unreadable — fail open with a warning on stderr
        print(json.dumps({}))
        print(f"enforce-tool-usage: config error: {exc}", file=sys.stderr)
        sys.exit(0)

    try:
        hook_input = json.load(sys.stdin)
    except json.JSONDecodeError:
        print(json.dumps({}))
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    if tool_name not in TERMINAL_TOOLS:
        print(json.dumps({}))
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    cmd = (
        cast("dict[str, Any]", tool_input).get("command", "")
        if isinstance(tool_input, dict)
        else ""
    )
    if not cmd:
        print(json.dumps({}))
        sys.exit(0)

    result = classify(cmd, config)
    if result:
        print(json.dumps(deny_response(result["guidance"])))
    else:
        print(json.dumps({}))


if __name__ == "__main__":
    main()
