#!/usr/bin/env python3
"""
setup.py

Configures AI coding agents to use universal-dev-skills.

Supported targets:
  vscode      — Merges settings into VS Code User settings.json
  claude      — Symlinks skills into ~/.claude/skills/
  windsurf    — Symlinks skills into ~/.codeium/windsurf/skills/
  copilot-cli — Symlinks skills, instructions, and hooks into ~/.copilot/
  cursor      — Converts skills to .cursor/rules/*.mdc (requires --workspace)
  all         — Runs all of the above (cursor excluded unless --workspace given)

Safe to run multiple times — only adds entries that are missing.

Usage:
    python3 scripts/setup.py --target vscode          # VS Code / Copilot
    python3 scripts/setup.py --target claude           # Claude Code
    python3 scripts/setup.py --target copilot-cli      # GitHub Copilot CLI
    python3 scripts/setup.py --target cursor --workspace /path/to/project
    python3 scripts/setup.py --target all              # all architectures
    python3 scripts/setup.py --target vscode --dry-run
"""

from __future__ import annotations

import json
import os
import platform
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

# ── Resolve the repo root ────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent


def parse_jsonc(text: str) -> dict[str, Any]:
    """Parse JSON with Comments (JSONC) as used by VS Code settings."""
    # Remove single-line comments (// ...) but not inside strings
    result: list[str] = []
    i = 0
    in_string = False
    escape_next = False
    while i < len(text):
        ch = text[i]
        if escape_next:
            result.append(ch)
            escape_next = False
            i += 1
            continue
        if ch == "\\" and in_string:
            result.append(ch)
            escape_next = True
            i += 1
            continue
        if ch == '"' and not in_string:
            in_string = True
            result.append(ch)
            i += 1
            continue
        if ch == '"' and in_string:
            in_string = False
            result.append(ch)
            i += 1
            continue
        if not in_string and ch == "/" and i + 1 < len(text):
            if text[i + 1] == "/":
                # Skip to end of line
                while i < len(text) and text[i] != "\n":
                    i += 1
                continue
            if text[i + 1] == "*":
                # Skip to closing */
                i += 2
                while i + 1 < len(text) and not (text[i] == "*" and text[i + 1] == "/"):
                    i += 1
                i += 2  # skip */
                continue
        result.append(ch)
        i += 1

    cleaned = "".join(result)
    # Remove trailing commas before } or ]
    cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
    return json.loads(cleaned)


def detect_settings_file() -> Path:
    """Detect the VS Code settings file path based on platform."""
    wsl = os.environ.get("WSL_DISTRO_NAME") or os.environ.get("WSLENV")

    if wsl:
        # WSL — try to find Windows VS Code User settings
        try:
            import subprocess

            appdata = (
                subprocess.check_output(
                    ["cmd.exe", "/C", "echo %APPDATA%"], stderr=subprocess.DEVNULL
                )
                .decode()
                .strip()
            )
            wsl_appdata = (
                subprocess.check_output(["wslpath", appdata], stderr=subprocess.DEVNULL)
                .decode()
                .strip()
            )
            path = Path(wsl_appdata) / "Code" / "User" / "settings.json"
            print(
                f"WSL detected — using Windows VS Code User settings: {path}",
                file=sys.stderr,
            )
            return path
        except Exception:
            pass
        # Fallback: VS Code Server machine settings
        path = Path.home() / ".vscode-server" / "data" / "Machine" / "settings.json"
        print(
            f"WSL detected — using VS Code Server Machine settings: {path}",
            file=sys.stderr,
        )
        return path

    system = platform.system()
    if system == "Darwin":
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / "Code"
            / "User"
            / "settings.json"
        )
    if system == "Linux":
        config = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
        return Path(config) / "Code" / "User" / "settings.json"
    if system == "Windows":
        appdata = os.environ.get("APPDATA", "")
        return Path(appdata) / "Code" / "User" / "settings.json"

    print(f"ERROR: Unsupported platform: {system}", file=sys.stderr)
    sys.exit(1)


def repo_tilde_path() -> str:
    """Return the repo path with ~ prefix for portability in VS Code settings."""
    home = Path.home().resolve()
    repo = REPO_ROOT.resolve()
    try:
        relative = repo.relative_to(home)
        return f"~/{relative}"
    except ValueError:
        return str(repo)


def merge_object_setting(
    settings: dict[str, Any], key: str, entries: list[str]
) -> list[str]:
    """Merge entries into an object-valued setting. Returns list of actions taken."""
    actions: list[str] = []
    if key not in settings:
        settings[key] = {}

    for entry in entries:
        if entry not in settings[key]:
            settings[key][entry] = True
            actions.append(f'  + {key}: "{entry}"')
        else:
            actions.append(f'  ✓ {key}: "{entry}" (already set)')

    return actions


# ── Symlink helpers ──────────────────────────────────────────────────────


def ensure_symlinks(
    target_dir: Path, source_dirs: list[Path], *, dry_run: bool
) -> list[str]:
    """Create symlinks in target_dir pointing to each source directory.

    Each subdirectory of each source_dir gets a symlink like:
        target_dir/<name> -> source_dirs[i]/<name>

    Returns a list of human-readable action strings.
    """
    actions: list[str] = []
    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    for source in source_dirs:
        if not source.is_dir():
            actions.append(f"  ! Skipped (not found): {source}")
            continue
        for child in sorted(source.iterdir()):
            if not child.is_dir():
                continue
            link = target_dir / child.name
            if link.is_symlink():
                existing = link.resolve()
                if existing == child.resolve():
                    actions.append(f"  ✓ {link.name} → {child} (already linked)")
                else:
                    actions.append(
                        f"  ! {link.name} → {existing} (different target, skipped)"
                    )
            elif link.exists():
                actions.append(f"  ! {link.name} exists (not a symlink, skipped)")
            else:
                if not dry_run:
                    link.symlink_to(child.resolve())
                actions.append(f"  + {link.name} → {child}")
    return actions


def ensure_file_symlink(link: Path, target: Path, *, dry_run: bool) -> str:
    """Create a single file-level symlink. Returns a human-readable action string."""
    if not dry_run:
        link.parent.mkdir(parents=True, exist_ok=True)

    if link.is_symlink():
        existing = link.resolve()
        if existing == target.resolve():
            return f"  ✓ {link} → {target} (already linked)"
        return f"  ! {link} → {existing} (different target, skipped)"
    if link.exists():
        return f"  ! {link} exists (not a symlink, skipped)"
    if not dry_run:
        link.symlink_to(target.resolve())
    return f"  + {link} → {target}"


def write_hook_config(dest: Path, *, dry_run: bool) -> str:
    """Write enforce-tool-usage.json with an absolute path to the shell script.

    The JSON must contain an absolute path because VS Code resolves relative
    paths from the workspace root, not from the JSON file's directory.
    """
    script_path = str((REPO_ROOT / "hooks" / "enforce-tool-usage.sh").resolve())
    config: dict[str, Any] = {
        "hooks": {
            "PreToolUse": [
                {
                    "type": "command",
                    "command": script_path,
                    "timeout": 10,
                }
            ]
        }
    }
    content = json.dumps(config, indent=2) + "\n"

    # Remove existing symlink — writing through it would modify the repo file
    if not dry_run and dest.is_symlink():
        dest.unlink()

    if dest.exists() and not dest.is_symlink():
        existing = dest.read_text(encoding="utf-8")
        if existing == content:
            return f"  ✓ {dest.name} (up to date)"
        if not dry_run:
            dest.write_text(content, encoding="utf-8")
        return f"  ~ {dest.name} (updated)"

    if not dry_run:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    return f"  + {dest.name}"


# ── Target: VS Code ─────────────────────────────────────────────────────


def setup_vscode(*, dry_run: bool) -> None:
    """Merge universal-dev-skills paths into VS Code User settings."""
    settings_file = detect_settings_file()
    repo_path = repo_tilde_path()

    print()
    print("VS Code / GitHub Copilot")
    print("─" * 40)
    print(f"Settings: {settings_file}")
    print()

    # Read existing settings
    settings: dict[str, Any] = {}
    if settings_file.exists():
        try:
            text = settings_file.read_text(encoding="utf-8")
            settings = parse_jsonc(text)
        except (json.JSONDecodeError, ValueError) as e:
            backup = f"{settings_file}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
            print(f"WARNING: Could not parse existing settings ({e})", file=sys.stderr)
            if not dry_run:
                shutil.copy2(settings_file, backup)
                print(f"  Backup saved to: {backup}", file=sys.stderr)
            settings = {}

    all_actions: list[str] = []

    # Skills
    all_actions += merge_object_setting(
        settings,
        "chat.agentSkillsLocations",
        [
            ".github/skills",
            f"{repo_path}/skills",
        ],
    )

    # Instructions
    all_actions += merge_object_setting(
        settings,
        "chat.instructionsFilesLocations",
        [
            ".github/instructions",
            f"{repo_path}/instructions",
        ],
    )

    # Agents
    all_actions += merge_object_setting(
        settings,
        "chat.agentFilesLocations",
        [
            ".github/agents",
            f"{repo_path}/agents/vscode",
        ],
    )

    # Hooks — generate config with absolute path to the shell script
    # (VS Code resolves relative paths from the workspace root, not the JSON dir)
    managed_hooks_dir = Path.home() / ".vscode-copilot" / "hooks"
    hook_action = write_hook_config(
        managed_hooks_dir / "enforce-tool-usage.json", dry_run=dry_run
    )
    all_actions.append(hook_action)
    managed_hooks_tilde = "~/.vscode-copilot/hooks"
    all_actions += merge_object_setting(
        settings,
        "chat.hookFilesLocations",
        [
            ".github/hooks",
            managed_hooks_tilde,
        ],
    )

    # Enable agent-scoped hooks
    if settings.get("chat.useCustomAgentHooks") is not True:
        settings["chat.useCustomAgentHooks"] = True
        all_actions.append("  + chat.useCustomAgentHooks: true")
    else:
        all_actions.append("  ✓ chat.useCustomAgentHooks (already set)")

    for action in all_actions:
        print(action)
    print()

    formatted = json.dumps(settings, indent=4, ensure_ascii=False) + "\n"

    if dry_run:
        managed_keys = [
            "chat.agentSkillsLocations",
            "chat.instructionsFilesLocations",
            "chat.agentFilesLocations",
            "chat.hookFilesLocations",
            "chat.useCustomAgentHooks",
        ]
        preview = {k: settings[k] for k in managed_keys if k in settings}
        print("  Would write:")
        print(json.dumps(preview, indent=4))
    else:
        settings_file.parent.mkdir(parents=True, exist_ok=True)
        settings_file.write_text(formatted, encoding="utf-8")
        print(f"✓ Settings written to {settings_file}")


# ── Target: Claude Code ─────────────────────────────────────────────────


def setup_claude(*, dry_run: bool) -> None:
    """Symlink skills into ~/.claude/skills/ for Claude Code."""
    print()
    print("Claude Code")
    print("─" * 40)

    skills_dir = Path.home() / ".claude" / "skills"
    print(f"Skills:   {skills_dir}")
    print()

    actions = ensure_symlinks(skills_dir, [REPO_ROOT / "skills"], dry_run=dry_run)
    for action in actions:
        print(action)
    print()

    if not dry_run:
        print(f"✓ Skills linked in {skills_dir}")


# ── Target: Windsurf ────────────────────────────────────────────────────


def setup_windsurf(*, dry_run: bool) -> None:
    """Symlink skills into ~/.codeium/windsurf/skills/ for Windsurf."""
    print()
    print("Windsurf")
    print("─" * 40)

    skills_dir = Path.home() / ".codeium" / "windsurf" / "skills"
    print(f"Skills:   {skills_dir}")
    print()

    actions = ensure_symlinks(skills_dir, [REPO_ROOT / "skills"], dry_run=dry_run)
    for action in actions:
        print(action)
    print()

    if not dry_run:
        print(f"✓ Skills linked in {skills_dir}")


# ── Target: Copilot CLI ─────────────────────────────────────────────────


def setup_copilot_cli(*, dry_run: bool) -> None:
    """Symlink skills, instructions, and hooks into ~/.copilot/ for Copilot CLI."""
    print()
    print("GitHub Copilot CLI")
    print("─" * 40)

    copilot_home = Path(os.environ.get("COPILOT_HOME", str(Path.home() / ".copilot")))

    skills_dir = copilot_home / "skills"
    instructions_link = copilot_home / "copilot-instructions.md"
    instructions_source = REPO_ROOT / "instructions" / "copilot-instructions.md"
    hooks_dir = copilot_home / "hooks"

    print(f"Home:     {copilot_home}")
    print()

    # Skills
    print("Skills:")
    actions = ensure_symlinks(skills_dir, [REPO_ROOT / "skills"], dry_run=dry_run)
    for action in actions:
        print(action)
    print()

    # Instructions entry point
    print("Instructions:")
    print(ensure_file_symlink(instructions_link, instructions_source, dry_run=dry_run))
    print()

    # Hooks
    print("Hooks:")
    print(write_hook_config(hooks_dir / "enforce-tool-usage.json", dry_run=dry_run))
    hook_actions2 = ensure_file_symlink(
        hooks_dir / "enforce-tool-usage.sh",
        REPO_ROOT / "hooks" / "enforce-tool-usage.sh",
        dry_run=dry_run,
    )
    print(hook_actions2)
    print()

    if not dry_run:
        print(f"✓ Copilot CLI configured in {copilot_home}")


# ── Target: Cursor ──────────────────────────────────────────────────────

# Mapping from skill name to Cursor activation mode.
# - True means alwaysApply: true
# - A glob string means globs: "<pattern>"
# - None means alwaysApply: false (Apply Intelligently, agent decides)
CURSOR_ACTIVATION: dict[str, str | bool | None] = {
    "skill-compliance": True,
    "tool-usage": True,
    "python-code-standards": "**/*.py",
    "typescript-code-standards": "**/*.ts,**/*.tsx",
    "java-code-standards": "**/*.java",
    "csharp-code-standards": "**/*.cs",
}


def convert_skill_to_cursor_rule(skill_dir: Path) -> str:
    """Read a SKILL.md and return Cursor .mdc content with adapted frontmatter."""
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")

    # Extract YAML frontmatter
    if not text.startswith("---"):
        return text  # No frontmatter — return as-is

    end = text.index("---", 3)
    frontmatter = text[3:end].strip()
    body = text[end + 3:].lstrip("\n")

    # Parse description from frontmatter
    description = ""
    for line in frontmatter.splitlines():
        if line.startswith("description:"):
            description = line.split(":", 1)[1].strip().strip('"').strip("'")
            break

    skill_name = skill_dir.name
    activation = CURSOR_ACTIVATION.get(skill_name)

    # Build Cursor frontmatter
    lines: list[str] = ["---"]
    lines.append(f'description: "{description}"')
    if activation is True:
        lines.append("alwaysApply: true")
    elif isinstance(activation, str):
        lines.append(f'globs: "{activation}"')
        lines.append("alwaysApply: false")
    else:
        lines.append("alwaysApply: false")
    lines.append("---")

    return "\n".join(lines) + "\n" + body


def setup_cursor(*, dry_run: bool, workspace: Path) -> None:
    """Convert skills to Cursor rules in <workspace>/.cursor/rules/."""
    print()
    print("Cursor")
    print("─" * 40)

    rules_dir = workspace / ".cursor" / "rules"
    print(f"Rules:    {rules_dir}")
    print()

    if not dry_run:
        rules_dir.mkdir(parents=True, exist_ok=True)

    skills_dir = REPO_ROOT / "skills"
    for skill in sorted(skills_dir.iterdir()):
        if not skill.is_dir() or not (skill / "SKILL.md").exists():
            continue

        rule_file = rules_dir / f"{skill.name}.mdc"
        content = convert_skill_to_cursor_rule(skill)

        if rule_file.exists():
            existing = rule_file.read_text(encoding="utf-8")
            if existing == content:
                print(f"  ✓ {rule_file.name} (up to date)")
            else:
                if not dry_run:
                    rule_file.write_text(content, encoding="utf-8")
                print(f"  ~ {rule_file.name} (updated)")
        else:
            if not dry_run:
                rule_file.write_text(content, encoding="utf-8")
            print(f"  + {rule_file.name}")

    print()
    if not dry_run:
        print(f"✓ Cursor rules written to {rules_dir}")


# ── CLI entry point ─────────────────────────────────────────────────────

USAGE = """\
usage: setup.py --target TARGET [--workspace PATH] [--dry-run] [--help]

Configure AI coding agents to use universal-dev-skills.

options:
  --target TARGET    Agent architecture to configure (required)
                     Choices: vscode, claude, windsurf, copilot-cli, cursor, all
  --workspace PATH   Target workspace directory (required for cursor)
  --dry-run          Show what would change without writing anything
  --help, -h         Show this message and exit
"""

TARGETS: dict[str, Callable[..., None]] = {
    "vscode": setup_vscode,
    "claude": setup_claude,
    "windsurf": setup_windsurf,
    "copilot-cli": setup_copilot_cli,
    "cursor": setup_cursor,
}


def main() -> None:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(USAGE)
        sys.exit(0)

    dry_run = "--dry-run" in sys.argv

    # Parse --target (required — show help if missing)
    target = None
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--target" and i + 1 < len(sys.argv):
            target = sys.argv[i + 1]
            break
        if arg.startswith("--target="):
            target = arg.split("=", 1)[1]
            break

    if target is None:
        print("ERROR: --target is required\n", file=sys.stderr)
        print(f"Supported targets: {', '.join(TARGETS)}, all\n")
        print(USAGE)
        sys.exit(1)

    # Parse --workspace
    workspace: Path | None = None
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--workspace" and i + 1 < len(sys.argv):
            workspace = Path(sys.argv[i + 1]).resolve()
            break
        if arg.startswith("--workspace="):
            workspace = Path(arg.split("=", 1)[1]).resolve()
            break

    # Validate target name
    if target != "all" and target not in TARGETS:
        print(
            f"ERROR: Unknown target '{target}'.\n",
            file=sys.stderr,
        )
        print(f"Supported targets: {', '.join(TARGETS)}, all\n")
        print(USAGE)
        sys.exit(1)

    # Validate --workspace requirement
    if target == "cursor" and workspace is None:
        print("ERROR: --workspace is required for --target cursor\n", file=sys.stderr)
        print(USAGE)
        sys.exit(1)

    print()
    print("universal-dev-skills setup")
    print("━" * 40)
    print(f"Repo:   {REPO_ROOT}")
    if workspace:
        print(f"Target: {workspace}")
    if dry_run:
        print("Mode:   DRY RUN")

    if target == "all":
        # Run global targets; include cursor only if --workspace was provided
        for name, setup_fn in TARGETS.items():
            if name == "cursor":
                if workspace is not None:
                    setup_cursor(dry_run=dry_run, workspace=workspace)
            else:
                setup_fn(dry_run=dry_run)
    elif target == "cursor":
        assert workspace is not None  # validated above
        setup_cursor(dry_run=dry_run, workspace=workspace)
    elif target in TARGETS:
        TARGETS[target](dry_run=dry_run)

    print()
    if dry_run:
        print("Run without --dry-run to apply changes.")
    else:
        print("Done. Restart your editor for changes to take effect.")


if __name__ == "__main__":
    main()
