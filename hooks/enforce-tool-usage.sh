#!/bin/bash
# enforce-tool-usage.sh
#
# PreToolUse hook that denies terminal commands which have dedicated
# VS Code tool equivalents, as defined in the tool-usage skill.
#
# Receives JSON on stdin with tool_name and tool_input.
# Returns permissionDecision: "deny" when a blocked command is detected.

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Only inspect terminal execution tools
case "$TOOL_NAME" in
  runInTerminal|run_in_terminal|createAndRunTask|create_and_run_task) ;;
  *) echo '{}'; exit 0 ;;
esac

CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
if [[ -z "$CMD" ]]; then
  echo '{}'
  exit 0
fi

# Strip leading whitespace and environment variable assignments for matching
STRIPPED=$(echo "$CMD" | sed 's/^[[:space:]]*//' | sed 's/^[A-Z_]*=[^ ]* //')

deny() {
  local reason="$1"
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "$reason"
  }
}
EOF
  exit 0
}

# --- Git commands: use GitKraken MCP tools ---
if echo "$STRIPPED" | grep -qE '^\s*(git)\b'; then
  deny "Use GitKraken MCP tools (git_status, git_add_or_commit, git_log_or_diff, git_branch, git_checkout, git_push, git_blame, git_stash) instead of git in the terminal. See the tool-usage skill."
fi

# --- File read/edit commands: use read_file, replace_string_in_file, create_file ---
if echo "$STRIPPED" | grep -qE '^\s*(cat|sed|head|tail)\b'; then
  deny "Use read_file, replace_string_in_file, or create_file tools instead of $STRIPPED in the terminal. See the tool-usage skill."
fi

# --- Echo with redirect: use create_file or replace_string_in_file ---
if echo "$STRIPPED" | grep -qE '^\s*echo\b.*>'; then
  deny "Use create_file or replace_string_in_file instead of echo with output redirection. See the tool-usage skill."
fi

# --- Search commands: use semantic_search, grep_search, file_search ---
if echo "$STRIPPED" | grep -qE '^\s*(grep|rg|find|fd)\b'; then
  deny "Use semantic_search, grep_search, or file_search tools instead of $STRIPPED in the terminal. See the tool-usage skill."
fi

# --- Directory listing: use list_dir ---
if echo "$STRIPPED" | grep -qE '^\s*(ls)\b'; then
  deny "Use the list_dir tool instead of ls in the terminal. See the tool-usage skill."
fi

# --- Test runners: use runTests tool (supports coverage) ---
if echo "$STRIPPED" | grep -qE '^\s*(npx jest|jest|yarn jest|pnpm jest)\b'; then
  deny "Use the runTests tool instead of jest in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '^\s*(dotnet test)\b'; then
  deny "Use the runTests tool instead of dotnet test in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '^\s*(\./gradlew test|gradle test|mvn test|mvn verify)\b'; then
  deny "Use the runTests tool instead of gradle/maven test in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '^\s*(npm|yarn|pnpm)( run)? test'; then
  deny "Use the runTests tool instead of npm/yarn/pnpm test in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '^\s*(npx |yarn |pnpm (exec )?)?vitest\b'; then
  deny "Use the runTests tool instead of vitest in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '^\s*(npx |yarn |pnpm (exec )?)?mocha\b'; then
  deny "Use the runTests tool instead of mocha in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '^\s*(pytest|python[0-9.]* -m pytest)\b'; then
  deny "Use the runTests tool instead of pytest in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '^\s*python[0-9.]* -m unittest\b'; then
  deny "Use the runTests tool instead of python -m unittest in the terminal. See the tool-usage skill."
fi

# --- Python execution: use Pylance RunCodeSnippet ---
if echo "$STRIPPED" | grep -qE '^\s*python[0-9.]*\b'; then
  deny "Use Pylance RunCodeSnippet instead of running Python in the terminal. See the tool-usage skill (references/python.md)."
fi

# Command is allowed
echo '{}'
exit 0
