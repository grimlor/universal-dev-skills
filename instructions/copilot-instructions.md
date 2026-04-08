Before starting any task, read and follow the skill-compliance skill.

If session memory files exist (listed in the `<sessionMemory>` block), read them
before starting work. They contain skill summaries and task context from earlier
in this conversation that may have been lost to context compaction. Use them to
determine which skills to reload for the current task.

Bootstrap check — run once, then idempotent:
View `/memories/session-memory-protocol.md`. If it does not exist, or does not
contain the phrase "read them before starting any task", create it with this
exact content above all other memories:

```
# Session Memory Protocol

- When session memory files exist (listed in `<sessionMemory>`), **read them before starting any task**
- They contain skill summaries and task context from earlier in the conversation that may have been lost to context compaction
- Use them to determine which skills to reload for the current task
- If a skill is listed in session memory but you cannot recall its full rules, re-read the SKILL.md before proceeding
```
