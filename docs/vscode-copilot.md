# Setup — VS Code / GitHub Copilot

GitHub Copilot in VS Code has native support for Agent Skills, custom instructions, and custom agents. This is the primary platform these skills were built for.

## Concepts

| VS Code Concept | UDS Equivalent | Location |
|---|---|---|
| Agent Skills (`SKILL.md`) | `skills/` directory | `.github/skills/` or custom path |
| Custom Instructions (`.instructions.md`) | `instructions/` directory | `.github/instructions/` or custom path |
| Custom Agents (`.agent.md`) | `agents/` directory | `.github/agents/` or custom path |
| Always-on instructions | `copilot-instructions.md` | `.github/copilot-instructions.md` |

## Option A — Global Settings (Recommended)

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

## Option B — Copy into a Workspace

Copy the files into a project's `.github/` directory:

```bash
mkdir -p /path/to/your-repo/.github
cp -r skills/ /path/to/your-repo/.github/skills/
cp -r instructions/ /path/to/your-repo/.github/instructions/
cp -r agents/ /path/to/your-repo/.github/agents/
```

This makes the skills version-controlled with the project and available to all contributors.

## Option C — User Profile Directory

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
4. **Never overwrite existing files** — only copy missing items, preserving user customizations.

This creates a zero-interaction install path: `pip install your-mcp-server` → skills appear in the workspace on next server start.

### Key design decisions

- `importlib.resources` over `__file__`-relative paths — works in all install modes including wheels and zip imports
- `Path.cwd()` detection — VS Code launches MCP servers with the workspace root as cwd
- Startup-time install — no CLI command or manual step required
- INFO-level logging for installs, DEBUG for skips — observable without being noisy

## How the Entry Point Works

The `instructions/copilot-instructions.md` file contains a single line that directs the agent to read the `skill-compliance` skill before doing anything else. `skill-compliance` then orchestrates loading all relevant skills for the current task.

This chain — entry point → skill-compliance → relevant skills — is what makes the system self-enforcing rather than advisory.

## Memory & Context Persistence

VS Code Copilot has the richest memory system of any supported platform:

| Scope | Location | Loaded | Survives Compaction? |
|---|---|---|---|
| User memory | `/memories/` (memory tool) | First 200 lines auto-loaded every turn | Yes — persists across all workspaces and conversations |
| Session memory | `/memories/session/` (memory tool) | Filenames listed every turn; content on demand | Until conversation ends |
| Repository memory | `/memories/repo/` (memory tool) | Create-only; stored locally in workspace | Yes — persists across conversations in the same workspace |

The memory tool is a VS Code extension feature (`github.copilot-chat`) — it is not filesystem-accessible and is not available in Copilot CLI or VS Code Cloud.

### Skill-recall after context compaction

Three layers ensure skills are re-read after compaction:

1. **User memory note** (`/memories/session-memory-protocol.md`) — auto-loaded every turn, instructs the agent to check session memory and reload skills if in doubt.
2. **`copilot-instructions.md` trigger** — always-on instruction that checks for session memory files.
3. **Skill-compliance Step 8** — writes active skill summaries to session memory with an unconditional reload instruction.

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

- `github.copilot.chat.organizationInstructions.enabled` — organization-level instructions
- `github.copilot.chat.organizationCustomAgents.enabled` — organization-level agents

See [GitHub's documentation](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-organization-instructions) for setup.
