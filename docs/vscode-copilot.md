# Setup -- VS Code / GitHub Copilot

GitHub Copilot in VS Code has native support for Agent Skills, custom instructions, and custom agents. This is the primary platform these skills were built for.

## Concepts

| VS Code Concept | UDS Equivalent | Location |
|---|---|---|
| Agent Skills (`SKILL.md`) | `skills/` directory | `.github/skills/` or custom path |
| Custom Instructions (`.instructions.md`) | `instructions/` directory | `.github/instructions/` or custom path |
| Custom Agents (`.agent.md`) | `agents/` directory | `.github/agents/` or custom path |
| Always-on instructions | `copilot-instructions.md` | `.github/copilot-instructions.md` |

## Option A -- Global Settings (Recommended)

Clone this repo once and configure VS Code to read from it across all workspaces. Zero per-project setup.

### 1. Clone the repo

```bash
git clone https://github.com/grimlor/universal-dev-skills.git ~/universal-dev-skills
```

### 2. Add to VS Code User Settings

Open VS Code Settings (JSON) and add:

```json
{
  "chat.agentSkillsLocations": {
    ".github/skills": true,
    "~/universal-dev-skills/skills": true
  },
  "chat.instructionsFilesLocations": {
    ".github/instructions": true,
    "~/universal-dev-skills/instructions": true
  },
  "chat.agentFilesLocations": {
    ".github/agents": true,
    "~/universal-dev-skills/agents/vscode": true
  }
}
```

This keeps the default `.github/` paths active (so per-project customizations still work) and adds the cloned directory as an additional source.

### 3. Verify

1. Open any workspace in VS Code.
2. Open the Chat view and right-click → **Diagnostics** to see loaded customizations.
3. You should see the skills, instructions, and agents from the cloned directory listed alongside any workspace-specific ones.

Alternatively, type `/` in chat to see available skills, or check **Configure Chat** (gear icon) → **Instructions & Rules** to see loaded instruction files.

## Option B -- Copy into a Workspace

Copy the files into a project's `.github/` directory:

```bash
mkdir -p /path/to/your-repo/.github
cp -r skills/ /path/to/your-repo/.github/skills/
cp -r instructions/ /path/to/your-repo/.github/instructions/
cp -r agents/ /path/to/your-repo/.github/agents/
```

This makes the skills version-controlled with the project and available to all contributors.

## Option C -- User Profile Directory

VS Code also reads from user profile directories that persist across all workspaces:

| Type | User Profile Path |
|---|---|
| Skills | `~/.copilot/skills/` |
| Instructions | `~/.copilot/instructions/` |
| Agents | `~/.copilot/agents/` |

You can symlink or copy into these locations as an alternative to the settings approach:

```bash
ln -s ~/universal-dev-skills/skills/* ~/.copilot/skills/
ln -s ~/universal-dev-skills/instructions/* ~/.copilot/instructions/
ln -s ~/universal-dev-skills/agents/* ~/.copilot/agents/
```

## MCP Package Distribution

For team distribution, skills can be bundled inside an MCP server Python package and auto-installed on startup. The pattern:

1. Bundle skills as package data under `_bundled_skills/` in the wheel.
2. On server startup, before the MCP transport starts, run an `install_skills()` function.
3. `install_skills()` uses `importlib.resources.files()` to read the bundled files and copies any missing ones into `.github/skills/` in the workspace root.
4. **Never overwrite existing files** -- only copy missing items, preserving user customizations.

This creates a zero-interaction install path: `pip install your-mcp-server` → skills appear in the workspace on next server start.

### Key design decisions

- `importlib.resources` over `__file__`-relative paths -- works in all install modes including wheels and zip imports
- `Path.cwd()` detection -- VS Code launches MCP servers with the workspace root as cwd
- Startup-time install -- no CLI command or manual step required
- INFO-level logging for installs, DEBUG for skips -- observable without being noisy

## How the Entry Point Works

The `instructions/copilot-instructions.md` file contains a single line that directs the agent to read the `skill-compliance` skill before doing anything else. `skill-compliance` then orchestrates loading all relevant skills for the current task.

This chain -- entry point → skill-compliance → relevant skills -- is what makes the system self-enforcing rather than advisory.

## Memory & Context Persistence

VS Code Copilot has the richest memory system of any supported platform:

| Scope | Location | Loaded | Survives Compaction? |
|---|---|---|---|
| User memory | `/memories/` (memory tool) | First 200 lines auto-loaded every turn | Yes -- persists across all workspaces and conversations |
| Session memory | `/memories/session/` (memory tool) | Filenames listed every turn; content on demand | Until conversation ends |
| Repository memory | `/memories/repo/` (memory tool) | Create-only; stored locally in workspace | Yes -- persists across conversations in the same workspace |

The memory tool is a VS Code extension feature (`github.copilot-chat`) -- it is not filesystem-accessible and is not available in Copilot CLI or VS Code Cloud.

### Skill-recall after context compaction

Three layers ensure skills are re-read after compaction:

1. **User memory note** (`/memories/session-memory-protocol.md`) -- auto-loaded every turn, instructs the agent to check session memory and reload skills if in doubt.
2. **`copilot-instructions.md` trigger** -- always-on instruction that checks for session memory files.
3. **Skill-compliance Step 8** -- writes active skill summaries to session memory with an unconditional reload instruction.

## Relevant VS Code Settings

| Setting | Purpose |
|---|---|
| `chat.agentSkillsLocations` | Directories to search for skills |
| `chat.instructionsFilesLocations` | Directories to search for instruction files |
| `chat.agentFilesLocations` | Directories to search for agent files |
| `chat.useAgentsMdFile` | Enable/disable AGENTS.md support |
| `chat.useNestedAgentsMdFiles` | Enable AGENTS.md in subdirectories (experimental) |
| `chat.useClaudeMdFile` | Enable/disable CLAUDE.md support |
| `chat.includeApplyingInstructions` | Enable pattern-based instruction matching |

## Organization-Level Distribution

For GitHub organizations, custom instructions and agents can be defined at the organization level and automatically discovered by all members:

- `github.copilot.chat.organizationInstructions.enabled` -- organization-level instructions
- `github.copilot.chat.organizationCustomAgents.enabled` -- organization-level agents

See [GitHub's documentation](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-organization-instructions) for setup.

## Security Hardening -- Tool Approval Policy

The hooks in this repo (`hooks/enforce-tool-usage.sh` + `tool-usage-rules.json`) enforce tool-usage rules by denying terminal commands that should use VS Code tools instead. However, hooks alone are not sufficient -- they only gate the `run_in_terminal` tool. An agent that wants to circumvent them can launder operations through other tools that execute code, such as MCP server tools with code execution capabilities (e.g., Pylance's `runCodeSnippet`), `subprocess` calls inside Python snippets, or script interpreters like `perl -e`.

This is not a theoretical risk. It has been observed in practice.

### Recommended tool approval settings

Reset to strict approvals and only auto-approve operations you trust:

1. **Reset all tool approvals.** Run `Chat: Reset Tool Confirmations` from the Command Palette (`⇧⌘P`). This reverts every tool to requiring explicit approval.

2. **Disable dangerous MCP tools.** Any MCP tool that can execute arbitrary code should be disabled entirely. Use the Configure Tools picker in the Chat view to toggle off tools like `runCodeSnippet`. Disabling is stronger than requiring approval -- a disabled tool cannot be invoked at all. Enable it at your own risk.

3. **Auto-approve only read-only operations.** Use `Chat: Manage Tool Approval` from the Command Palette to selectively pre-approve tools that are strictly read-only (e.g., `grep_search`, `file_search`, `read_file`, `list_dir`, `semantic_search`). Leave everything else requiring manual approval.

4. **Review terminal auto-approvals.** Audit your `chat.tools.terminal.autoApprove` setting. Only allow commands you are certain cannot be used to bypass hooks. For example, `task` and `pre-commit` are safe because they run the project's own configured commands.

5. **Restrict URL auto-approvals.** Audit your `chat.tools.urls.autoApprove` setting. Use the granular `{ "approveRequest": bool, "approveResponse": bool }` form to separate request approval from response content review, especially for sites with user-generated content.

### Why hooks are necessary but not sufficient

The PreToolUse hook intercepts `run_in_terminal` calls and denies commands that violate the tool-usage rules (e.g., `git commit` instead of the GitKraken MCP tool, `grep` instead of `grep_search`). This works well for its scope, but:

- **Hooks only gate tools they are configured for.** A tool the hook doesn't intercept (like a code execution MCP tool) bypasses the hook entirely.
- **Code execution is command injection.** Any tool that accepts and runs code -- Python snippets, shell eval, script interpreters -- can be used to perform the same operations the hook blocks, just through a different channel.
- **Defense in depth requires both layers.** Hooks enforce discipline for the normal path (terminal commands). Tool approval settings enforce the perimeter (which tools can run at all).

### Quick reference

| Layer | What it controls | How to configure |
|---|---|---|
| PreToolUse hooks | Terminal command allowlist/blocklist | `hooks/tool-usage-rules.json` |
| Tool approval | Which tools can run and whether they need confirmation | `Chat: Manage Tool Approval` command |
| Tool disable | Remove tools from availability entirely | Configure Tools picker in Chat view |
| Permission level | Session-wide approval mode (Default / Bypass / Autopilot) | Permissions picker in Chat input |
| `chat.tools.eligibleForAutoApproval` | Prevent specific tools from ever being auto-approved | VS Code settings (org-managed) |
