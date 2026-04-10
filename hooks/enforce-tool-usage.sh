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

# Parse JSON with python3 (avoids jq dependency)
json_field() {
  echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
keys = sys.argv[1].split('.')
v = d
for k in keys:
    v = v.get(k, '') if isinstance(v, dict) else ''
print(v if isinstance(v, str) else '')
" "$1" 2>/dev/null || echo ''
}

TOOL_NAME=$(json_field tool_name)

# Only inspect terminal execution tools
case "$TOOL_NAME" in
  runInTerminal|run_in_terminal|createAndRunTask|create_and_run_task) ;;
  *) echo '{}'; exit 0 ;;
esac

CMD=$(json_field tool_input.command)
if [[ -z "$CMD" ]]; then
  echo '{}'
  exit 0
fi

# Strip quoted strings so we never match against argument content
# (e.g. git commit -m "pytest --cov" must not trigger the pytest rule)
STRIPPED=$(echo "$CMD" | sed "s/'[^']*'//g" | sed 's/"[^"]*"//g')

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
# Only block subcommands that have a direct MCP equivalent.
# Allow through: fetch, pull, rebase, merge, tag, cherry-pick, revert,
#   remote, config, clean, rm, branch -d, reset, etc.
GIT_BLOCKED="status|add|commit|push|log|diff|show|branch|checkout|switch|blame|stash|worktree"
if echo "$STRIPPED" | grep -qE "\bgit ($GIT_BLOCKED)\b"; then
  deny "Use GitKraken MCP tools (git_status, git_add_or_commit, git_log_or_diff, git_branch, git_checkout, git_push, git_blame, git_stash, git_worktree) instead of git in the terminal. See the tool-usage skill."
fi

# --- File read/edit commands: use read_file, replace_string_in_file, create_file ---
if echo "$STRIPPED" | grep -qE '\b(cat|sed|head|tail|awk)\b'; then
  deny "Use read_file, replace_string_in_file, or create_file tools instead of $STRIPPED in the terminal. See the tool-usage skill."
fi

# --- Echo with redirect: use create_file or replace_string_in_file ---
if echo "$STRIPPED" | grep -qE '\becho\b.*>'; then
  deny "Use create_file or replace_string_in_file instead of echo with output redirection. See the tool-usage skill."
fi

# --- Search commands: use semantic_search, grep_search, file_search ---
# Match only as commands, not as flags (e.g. -fd in git clean -fd)
if echo "$STRIPPED" | grep -qE '(^|[;&|] *)(grep|rg|find|fd)\b'; then
  deny "Use semantic_search, grep_search, or file_search tools instead of $STRIPPED in the terminal. See the tool-usage skill."
fi

# --- Directory listing: use list_dir ---
if echo "$STRIPPED" | grep -qE '\bls\b'; then
  deny "Use the list_dir tool instead of ls in the terminal. See the tool-usage skill."
fi

# --- Privilege escalation and permission changes: never allowed ---
if echo "$STRIPPED" | grep -qE '\b(sudo|su|doas|chmod|chown|chgrp|setfacl)\b'; then
  deny "Do not use privilege escalation or permission/ownership commands (sudo, su, doas, chmod, chown, chgrp, setfacl) in the terminal. These should be managed outside the agent."
fi

# --- Test runners: use runTests tool (supports coverage) ---
if echo "$STRIPPED" | grep -qE '\b(npx jest|jest|yarn jest|pnpm jest)\b'; then
  deny "Use the runTests tool instead of jest in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '\b(dotnet test)\b'; then
  deny "Use the runTests tool instead of dotnet test in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '(\./gradlew test|\bgradle test|\bmvn test|\bmvn verify)\b'; then
  deny "Use the runTests tool instead of gradle/maven test in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '\b(npm|yarn|pnpm)( run)? test'; then
  deny "Use the runTests tool instead of npm/yarn/pnpm test in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '(\bnpx |\byarn |\bpnpm (exec )?)?\bvitest\b'; then
  deny "Use the runTests tool instead of vitest in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '(\bnpx |\byarn |\bpnpm (exec )?)?\bmocha\b'; then
  deny "Use the runTests tool instead of mocha in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '\b(pytest|python[0-9.]* -m pytest)\b'; then
  deny "Use the runTests tool instead of pytest in the terminal. See the tool-usage skill."
fi

if echo "$STRIPPED" | grep -qE '\bpython[0-9.]* -m unittest\b'; then
  deny "Use the runTests tool instead of python -m unittest in the terminal. See the tool-usage skill."
fi

# --- Python execution: show script to user and ask them to enable RunCodeSnippet ---
if echo "$STRIPPED" | grep -qE '\bpython[0-9.]*\b'; then
  deny "Do not run Python in the terminal. Show the script to the user and ask them to enable the Pylance RunCodeSnippet tool and approve running it. The tool is disabled by default for security. See the tool-usage skill (references/python.md)."
fi

# Command is allowed
echo '{}'
exit 0
