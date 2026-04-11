#!/bin/bash
# enforce-tool-usage.sh
#
# PreToolUse hook that enforces tool-usage rules via a hybrid
# category-blocklist and command-allowlist model.
#
# Delegates all classification logic to enforce-tool-usage.py,
# which loads its configuration from tool-usage-rules.json.
#
# Receives JSON on stdin with tool_name and tool_input.
# Returns permissionDecision: "deny" when a blocked command is detected.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/enforce_tool_usage.py" "$SCRIPT_DIR/tool-usage-rules.json"
