---
name: memory-setup
description: >-
  Set up shared, in-repo memory for coding agents: a PITFALLS.md of lessons on main,
  a HANDOFF.md of work state on each branch, and the rule that tells the agent how to
  keep both. Use it when someone wants the agent to "remember" across sessions, keep
  lessons or pitfalls, write handoffs, stop repeating the same mistakes, onboard a
  repo to AI, or asks where HANDOFF.md / PITFALLS.md should live and whether they
  should be committed, gitignored or private. Also use it to migrate a repo whose
  handoff and pitfalls files are untracked or personal into the shared model.
disable-model-invocation: true
---

# Setting up repo memory

An agent starts every session knowing nothing. Memory that lives on one laptop, or
in a file nobody commits, helps one person and nobody else. This sets up memory the
whole team shares, split by what it holds:

| | Holds | Lives | Ends |
|---|---|---|---|
| `PITFALLS.md` | Knowledge: a trap, its cause, its fix | Committed on `main` | Shrinks when a check makes the trap impossible |
| `HANDOFF.md` | State: where one piece of work stands | Committed on that work's branch | Deleted before the branch merges, after its lessons move to their homes |
| `CLAUDE.local.md` | One person's preferences | Git-ignored | Never shared |

The split is what makes sharing safe: knowledge is true for everyone, so it's on
`main`; state belongs to one piece of work, so it travels with that branch and never
collides with anyone else's.

## Steps

1. **Look first.** Check for existing `HANDOFF.md`, `PITFALLS.md`, `docs/lessons*`,
   `CLAUDE.local.md`, and whether `.gitignore` excludes any of them. Read what's
   there; it's material to keep, not to overwrite.

2. **Write the rule.** Copy `assets/memory-rule.md` to `.claude/rules/memory.md`.
   Adjust wording to the repo if needed, but keep the three sections. This file is
   also what turns on the plugin's session-start hook for this repo, so its presence
   is the opt-in.

3. **Create `PITFALLS.md`** if it doesn't exist:

   ```markdown
   # Pitfalls

   Traps we hit, their cause and fix. Headings are the symptom, as you'd search for it.
   ```

   If lessons exist elsewhere (an untracked file, a wiki page, old commit messages
   the user points to), offer to move them in using the entry format, one per trap.
   Don't invent entries.

4. **HANDOFF.md:** create one only if the user is on a work branch and there's work
   in flight; otherwise leave it for the first end of session. If a `HANDOFF.md` sits
   on `main`, don't leave it there, tracked or not (someone will commit it): move it to
   the branch it describes (create the branch if needed), or close it (lessons to
   PITFALLS.md, personal lines to `CLAUDE.local.md`, then delete it).

5. **Un-hide them.** If `.gitignore` excludes `HANDOFF.md` or `PITFALLS.md`, remove
   those lines and explain why in one sentence (the team can't share what git
   doesn't track). Make sure `CLAUDE.local.md` *is* ignored.

6. **Point CLAUDE.md at it,** with one line, not a copy:
   `Memory: see .claude/rules/memory.md (PITFALLS.md on main, HANDOFF.md per branch).`

7. **Guard the merge (offer, don't force).** Suggest a line in the PR template:
   `- [ ] HANDOFF.md closed (lessons moved, file deleted)`. If the repo uses CI, offer
   a check that fails a pull request into `main` while `HANDOFF.md` is present.

8. **Report** what you created, changed and left alone, and the one habit that
   matters: end each session by saying "wrap up"; the rule file tells the agent what
   that means.

## Notes

- This skill runs once per repo, started by hand (`/repo-memory:memory-setup`); it
  costs nothing in other sessions. Everything that must happen every session lives in
  the rule file it writes and in the plugin's hook.

- The plugin's SessionStart hook loads the branch's HANDOFF.md and the PITFALLS.md
  headings automatically in repos that have `.claude/rules/memory.md`. Nobody has to
  remember to "read it first".
- Keep PITFALLS.md searchable as it grows: headings are symptoms, entries are short.
  A long PITFALLS.md is fine; a long entry is not.
