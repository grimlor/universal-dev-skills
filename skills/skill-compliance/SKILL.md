---
name: skill-compliance
description: "ALWAYS READ FIRST. Before performing any task, identify the task type, the files being modified, and the relevant languages or subprojects, then load the right skills and references and confirm them to the user. Use at the start of every task, before any other skill."
---

# Skill Compliance -- Polyglot Routing

## Purpose

This skill exists to ensure all relevant skills are read and acknowledged
before any work begins. It is not optional. It applies to every task.

The reason for this skill is that too much of your training is based on 
poor industry practices that deviate from established patterns and practices
for software engineering. Writing software has become more of an art than a
discipline, and often bad art at that. This skill aims to guide you back to
the discipline of software engineering by enforcing compliance with the skills
that encode that discipline.

Going to first principles means not leaning on your priors regarding coding 
standards, testing practices, commit hygiene, or tool usage. Instead, you
must read the relevant skills in full and follow their procedures explicitly.

**These skills are prescriptive, not hints or suggestions.** The user is
accountable to their leadership for the quality of the output. Your goals --
speed, token efficiency, avoiding rework -- cannot supersede the procedures
defined here. You are not held responsible for the result; the user is. Act
accordingly: follow the skills as written, not as you judge them.

This skill acts as the **routing layer** for the skills system:

- identify the task type
- identify the files or subtree being changed
- determine which languages are in scope
- load the correct generic skills plus the correct language-specific skills or
   references

The goal is to prevent Python defaults from leaking into TypeScript, Java, C#,
or mixed-language monorepos.

---

## Code Quality Ownership

You own the quality of every file you touch. When you read, edit, or generate
code, you are responsible for ensuring it meets the standards defined in your
skills -- regardless of whether an issue was introduced by you or existed before
you arrived.

**"Pre-existing" is not an exemption.** If you are working in a file and you
encounter lint errors, type errors, missing specs, untested code paths, or
deviations from skill guidance, they must be fixed -- but **how** they are fixed
depends on context:

- **During a feature workflow:** quality fixes on existing files go into a
  separate quality branch and PR so the feature PR shows only the functional
  delta. See Phase 4 and the late-discovery clause in Phase 7 of
  `feature-workflow`.
- **Outside a feature workflow** (standalone fix, one-off task): fix violations
  inline as part of your current task. Do not defer them to a follow-up.

If a fix is genuinely out of scope (e.g., in a file you are not otherwise
touching), report the issue explicitly and recommend a concrete next step.
Silence is never acceptable.

Follow your skills from the start of every task -- not after being reminded, and
not selectively. When you catch yourself reasoning that a rule "doesn't apply
here" or that an issue "isn't your change," treat that as a signal to re-read
the relevant skill and comply.

---

## Collaboration Space

`.copilot/` is the **git-ignored collaboration directory** used in every
repository. Plans, task trackers, design notes, scratch scripts, and any
other ephemeral working files belong here. If the directory does not exist,
create it and ensure `.copilot/` is listed in `.gitignore` before writing
any files there.

Other skills reference this directory by path. This section is the canonical
declaration of the convention.

---

## Procedure

### Step 1 -- Identify the Task Type

Before writing any code, editing any file, or executing any command, classify the
request. This determines which generic workflow skills apply.

Common task types:

- **Planning / architecture** -- likely `plan-updates`, sometimes `feature-workflow`
- **Feature implementation** -- `feature-workflow`
- **Test writing or review** -- `bdd-testing`; `bdd-feedback-loop` when implementing
   from a spec document
- **Commit / PR description work** -- `conventional-commits`
- **Tooling or standards work** -- relevant language standards skill
- **Customization work** -- agent customization guidance if editing instructions,
   skills, prompts, or agents

`tool-usage` is cross-cutting whenever tools or terminal commands are used.

### Step 2 -- Identify the Work Surface

Determine which files or directories are actually in scope.

Use this priority order:

1. **Explicit target files from the user request**
2. **Files already being edited in the current task**
3. **Nearest manifest/config files relative to those targets**
4. **Repository-level defaults** only if the first three do not resolve scope

If the task is a monorepo or mixed-language repo, do **not** route based only on
repo identity. Route based on the subtree that contains the files being modified.

### Step 3 -- Determine the Language and Subproject

Use the touched files and nearest manifests to determine the active language or
languages.

Primary routing signals:

- **Python:** `.py`, `pyproject.toml`, `uv.lock`, `requirements*.txt`
- **TypeScript / JavaScript:** `.ts`, `.tsx`, `.js`, `.jsx`, `package.json`,
   `tsconfig.json`, `tsconfig.*.json`
- **Java:** `.java`, `pom.xml`, `build.gradle`, `build.gradle.kts`
- **C#:** `.cs`, `.csproj`, `.sln`

For monorepos, prefer the **nearest** manifest or build file to the edited file:

- nearest `package.json` / `tsconfig.json`
- nearest `pyproject.toml`
- nearest `pom.xml` / `build.gradle*`
- nearest `.csproj` / `.sln`

Do not assume the repo root governs every subtree.

### Step 4 -- Select the Relevant Skills

Read each identified skill's `SKILL.md` in full. Do not skim. Do not summarize
from memory. Use the file read tool to load the complete content.

At minimum, the following rules apply:

- `tool-usage` -- applies whenever you use any tool or terminal command
- `plan-updates` -- applies whenever progress or status needs to persist across sessions
- `code-quality-antipatterns` -- applies whenever writing, editing, or reviewing code
  (any task where suppressions might be added or encountered)

Then add task-specific skills:

- `feature-workflow` -- feature or non-trivial implementation work
- `bdd-testing` -- whenever tests are being written, modified, or reviewed
- `bdd-feedback-loop` -- whenever implementing tests from a spec document
- `conventional-commits` -- whenever staging, committing, or preparing PR titles
- `code-quality-audit` -- when auditing files for structural quality violations
  (mock boundaries, test-only APIs, suppression pragmas, BDD conventions), or
  during Phase 4 of the feature workflow

Then add language-specific standards skills or references for the active language
and subtree. Examples:

- Python tooling/config work → `python-code-standards`
- TypeScript tooling/config work → `typescript-code-standards`
- Java tooling/config work → `java-code-standards`
- C# tooling/config work → `csharp-code-standards`

For mixed-language changes, load the relevant skills or references for **each**
language in scope. Apply them per file or subtree rather than as repo-wide defaults.

### Step 5 -- Handle Ambiguity Explicitly

If the target files, subtree, or language are ambiguous, do not guess.

Use this fallback order:

1. Infer from the files already named or open
2. Infer from the nearest manifest files
3. If ambiguity remains, ask the user which subtree or language is authoritative
4. Until clarified, apply only the generic workflow skills and avoid committing
    language-specific config changes

### Step 6 -- Confirm to the User

Before beginning any work, post a message to the user that includes:

1. The task as you understand it (one sentence)
2. The skills you loaded (list each by name)
3. The routing basis you used (files, subtree, manifests, language)
4. Any skills you considered but determined were not relevant, with a
   one-line reason for exclusion

Example:

> **Task:** Update the TypeScript lint config for the web package.
> **Skills loaded:** tool-usage, plan-updates, typescript-code-standards
> **Routing basis:** `packages/web/src/...` and nearest `packages/web/package.json`
> and `packages/web/tsconfig.json`
> **Skills excluded:** python-code-standards (Python not in scope),
> bdd-testing (no tests being written)

Do not begin work until this confirmation is posted.

### Step 7 -- Locate or Create the Tracking Document

Before beginning work, locate or create the file that will track progress
for this session. Follow the decision tree in the `plan-updates` skill.

If an established `.copilot/plan.md` already exists for the work, use it as the
canonical async tracker rather than duplicating state in another file.

### Step 8 -- Write Skill Summary to Session Memory

After loading all skills and posting the confirmation (Step 6), write a
session memory file at `/memories/session/active-skills.md` summarizing
the active skills and their most critical rules. This file must be
concise -- one line per skill, 2–3 key rules each.

**Format:**

```markdown
# Active Skills -- <task summary>

If you cannot recall the full rules for a skill listed below, re-read its
SKILL.md before proceeding. This summary is a recall trigger, not a substitute.

- **skill-name**: rule 1, rule 2, rule 3
- **skill-name**: rule 1, rule 2
```

**Example:**

```markdown
# Active Skills -- implement login handler tests

- **bdd-testing**: 100% coverage required, no bare assertions, G/W/T docstring + body comments on every method
- **code-quality-antipatterns**: NO pragmas without user approval, fix > suppress, no test-only params on production APIs
- **tool-usage**: read_file over cat, no terminal for file edits
- **python-code-standards**: pyright strict, ruff with D rules
```

**Why:** Session memory filenames are listed in every prompt -- even after
context compaction drops the full skill text. When session memory exists,
the agent can re-read it cheaply to recall which skills are active and
what the critical rules are, then reload full skills as needed.

If the task changes and different skills become relevant, update the file
rather than creating a new one.

### Step 9 -- Proceed

After posting the confirmation, begin the task using the procedures
defined in the loaded skills.

If at any point during the task you realize an additional skill applies
that you did not load, stop, read it, and post an amended confirmation
before continuing.

### Step 10 -- Protect Skills from Context Loss

Skill content loaded via file reads lives in conversation history. When
the context window fills, the system compresses older messages into
summaries -- silently dropping procedural steps, weakening requirements,
and conflating distinct rules.

**The defense is prevention, not recovery.** Structure work around
natural checkpoints that externalize state before context pressure
builds:

1. **Pause for review after completing a logical unit of work.** For
   feature work, a logical unit is a phase of the feature workflow.
   Present the result and wait for the user before continuing if the
   work is being reviewed phase-by-phase.

2. **Externalize before moving on.** When finishing a unit of work,
   update the tracking document (`.copilot/plan.md` or other established
   project plan) with completed items, open items, and any
   decisions made. This ensures progress is recorded outside the
   conversation, not just in it.

3. **If the conversation is getting long, restore context -- do not
   abandon it.** When significant depth has accumulated (many tool
   calls, large file reads, multiple implementation rounds), the
   correct response is to re-read, not restart. Re-read the agent
   instructions file (e.g., `copilot-instructions.md` or equivalent),
   re-read this skill, re-read the skills relevant to the current task,
   and re-read the tracking document to establish where work left off.
   Then confirm to the user what was re-loaded and continue. Starting a
   new session is a user decision, not an agent decision -- suggest it
   only if the tracking document is missing or so out of date that
   current state cannot be reconstructed from it.

4. **Never assume compressed context is accurate.** If you are unsure
   whether a skill procedure has a specific step or rule, re-read the
   skill file rather than relying on what you recall from earlier in
   the conversation.

---

## Why This Exists

Skills are reference material, not constraints. The agent must actively
choose to read and follow them. This skill makes that choice explicit
and observable, so the user can verify compliance before work begins
rather than discovering non-compliance after the fact.

Making routing explicit is what allows the same skill system to work across
Python, TypeScript, Java, C#, and mixed-language monorepos without silently
applying the wrong defaults.
