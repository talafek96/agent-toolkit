
## HANDOFF.md: where your work stands (private, opted in)

`HANDOFF.md` is **yours**: git-ignored, never shared. It's your progress file: the
next session reads it first to pick up where you left off (the same idea as a
long-running agent's progress notes). It's loaded automatically at session start.

**Budget: 40 lines.** Only the first 40 lines are loaded; the rest is cut off.
You'll be told when you're near or over it. When that happens, rewrite it shorter
before anything else.

- **At the end of every session** ("wrap up", "let's stop", before a break),
  **rewrite it. Replace it; don't append.** It's a snapshot, not a log: yesterday's
  details are in `git log`.
- **Keep only what the next session needs and can't get elsewhere:**

  ```markdown
  # Handoff · <date>
  ## Now
  <one or two lines: what you're in the middle of>
  ## Next
  1. <first concrete step>
  ## Open decisions
  - <question> · I recommend <x> · <who decides>
  ## Careful
  - <something in flight that isn't obvious from the code>
  ```

- **Leave out** what's done (git has it), task lists (your `tasks.md` has them), and
  anything the team should know: a trap goes to a `PITFALLS.md`, a lasting decision
  to CLAUDE.md or a rule.
