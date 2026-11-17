# Repo memory

You start every session knowing nothing. These two files are the memory, and they
live in the repo so the whole team (and every agent) shares them.

## PITFALLS.md: what we learned (shared, on main)

- **Write an entry in the same commit as the fix**, when the cause was not obvious
  from the error: a trap the next person would fall into too. Not for typos or for
  bugs the error message explains.
- **Format:** `## <the symptom, as someone would search for it>`, then *Cause*,
  *Fix*, and *Where it's fixed* (file, test or commit). A few lines, not a story.
- **Before working in an area, read the entries whose headings match it.** The
  headings are loaded at session start; read the full entry you need.
- **When a check makes the trap impossible** (a test, a lint rule, a type), shrink the
  entry to one line naming that check, or delete it. The best pitfall is one a check
  now catches.

## HANDOFF.md: where this work stands (on its branch, never on main)

- **It belongs to the piece of work, not to a person.** It lives on the work's
  branch, is committed and pushed, and anyone continuing the work reads it first.
- **At the end of every session** ("wrap up", "let's stop", "hand this off", before a
  break), **rewrite it. Replace it; don't append.** Write for a
  fresh agent that has the repo but not this conversation: the goal; what's done and
  *how each item was verified* (a test name, a manual check, or "not verified"); what's
  next, in order; open decisions with your recommendation and who decides; anything in
  flight that isn't obvious from the code. Point to specs or tasks; don't copy them, and
  don't narrate the session.
- **A decision is recorded only once someone made it.** If you need a choice nobody
  made, put it under open decisions with your recommendation. Never write it into
  CLAUDE.md, a rule or the code as if it were policy.
- **Before the branch merges, close it.** Closing is bookkeeping, not implementation:
  - Check each "done" item against the code and its tests. A placeholder test or an
    unused constant is not done.
  - Lessons and decisions that are already final move to their homes now, either way
    (a pitfall that was fixed, a decision someone made). Don't hold them back.
  - If anything is unfinished, don't delete HANDOFF.md and don't build the rest unasked:
    rewrite it with what blocks the merge, and report.
  - If everything is done and every lasting lesson is in its home (PITFALLS.md,
    CLAUDE.md, a rules file, a spec), delete HANDOFF.md in the last commit.
    `main` never carries a handoff.
- **Commit memory files by name** (`git add HANDOFF.md PITFALLS.md …`), never everything
  at once.

## What stays private

Personal preferences about how *you* like to work go in `CLAUDE.local.md`
(git-ignored). Anything about the project, its traps or its work goes in the files
above, where the team can see it.
