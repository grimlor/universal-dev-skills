---
name: skill-compliance
description: "ALWAYS READ FIRST. Before performing any task, read all relevant skills and confirm to the user which skills were loaded. Use at the start of every task, before any other skill."
---

# Skill Compliance — Pre-Task Checklist

## Purpose

This skill exists to ensure all relevant skills are read and acknowledged
before any work begins. It is not optional. It applies to every task.

---

## Procedure

### Step 1 — Identify Relevant Skills

Before writing any code, editing any file, or executing any command, scan
the task description and identify which skills apply. The available skills
are in the skills directory configured for your agent (e.g., `.github/skills/`,
`.windsurf/skills/`, or the location specified in your editor settings).
Read the directory listing first.

### Step 2 — Read Each Relevant Skill

Read each identified skill's `SKILL.md` in full. Do not skim. Do not
summarize from memory. Use the file read tool to load the complete content.

At minimum, the following skills apply to almost every task:
- `tool-usage` — applies whenever you use any tool or terminal command
- `bdd-testing` — applies whenever tests are involved
- `bdd-feedback-loop` — applies whenever implementing from a spec doc

### Step 3 — Confirm to the User

Before beginning any work, post a message to the user that includes:

1. The task as you understand it (one sentence)
2. The skills you loaded (list each by name)
3. Any skills you considered but determined were not relevant, with a
   one-line reason for exclusion

Example:

> **Task:** Implement test coverage for the validation module.
> **Skills loaded:** tool-usage, bdd-testing, bdd-feedback-loop
> **Skills excluded:** feature-workflow (no new feature being added),
> plan-updates (no plan doc changes required)

Do not begin work until this confirmation is posted.

### Step 4 — Locate or Create the Tracking Document

Before beginning work, locate or create the file that will track progress
for this session. Follow the decision tree in the `plan-updates` skill.

For refactoring, audit, or remediation passes where no plan doc exists,
this means creating `.copilot/task.md` before the first work item begins.
Do not use an in-session todo list as a substitute — it is invisible to
context restore and lost on session end.

### Step 5 — Proceed

After posting the confirmation, begin the task using the procedures
defined in the loaded skills.

If at any point during the task you realize an additional skill applies
that you did not load, stop, read it, and post an amended confirmation
before continuing.

### Step 6 — Protect Skills from Context Loss

Skill content loaded via file reads lives in conversation history. When
the context window fills, the system compresses older messages into
summaries — silently dropping procedural steps, weakening requirements,
and conflating distinct rules.

**The defense is prevention, not recovery.** Structure work around
natural checkpoints that externalize state before context pressure
builds:

1. **Pause for review after completing a logical unit of work.** For
   feature work, a logical unit is a phase of the feature workflow or a
   test module. For audit and remediation passes, a logical unit is a
   test class — update `.copilot/task.md` after every class, not every
   file. Present the result and wait for the user before continuing.

2. **Externalize before moving on.** When finishing a unit of work,
   update the tracking document (`.copilot/plan.md` or
   `.copilot/task.md`) with completed items, open items, and any
   decisions made. This ensures progress is recorded outside the
   conversation, not just in it.

3. **If the conversation is getting long, restore context — do not
   abandon it.** When significant depth has accumulated (many tool
   calls, large file reads, multiple implementation rounds), the
   correct response is to re-read, not restart. Re-read the agent
   instructions file (e.g., `copilot-instructions.md` or equivalent),
   re-read this skill, re-read the skills relevant to the current task,
   and re-read the tracking document to establish where work left off.
   Then confirm to the user what was re-loaded and continue. Starting a
   new session is a user decision, not an agent decision — suggest it
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
