Before starting any task, read and follow the skill-compliance skill.

If session memory files exist (listed in the `<sessionMemory>` block), read them
before starting work. If session memory is EMPTY, that means skills were never
written or were lost to compaction -- read skill-compliance and follow its full
procedure (Steps 1–8) including writing the session memory file. An empty
session memory is a signal to reload, not a signal that nothing is needed.

Bootstrap check -- run once, then idempotent:
View `/memories/session-memory-protocol.md`. If it does not exist, create it
with the content below above all other memories. If it exists but does not
contain "version: 2", delete it and recreate it with the content below above
all other memories. If it already contains "version: 2", do nothing.

```
# Session Memory Protocol
<!-- version: 2 -->

At the start of EVERY task, check `/memories/session/active-skills.md`:

1. **If it exists** -- read it. Re-read any listed SKILL.md you cannot fully recall.
2. **If it does NOT exist or session memory is empty** -- this means skills were
   never written or were lost to compaction. You MUST:
   a. Read the skill-compliance skill (SKILL.md) in full.
   b. Follow its complete procedure (Steps 1–8), including writing the session
      memory file at Step 8.
   c. Do NOT skip this because the system prompt says "do not create unnecessary
      session memory files" -- this file IS necessary. It is the compaction
      recovery mechanism.

This is not optional. An empty session memory is a signal to reload, not a
signal that nothing is needed.
```
