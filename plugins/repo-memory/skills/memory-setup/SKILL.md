---
name: memory-setup
description: >-
  Set up shared, hierarchical PITFALLS.md memory in a repo: lessons live in a
  PITFALLS.md next to the code they're about, the agent sees only the headings in scope,
  and a rule teaches it where and how to write new ones. Optionally adds a private,
  git-ignored HANDOFF.md that's loaded at session start. Run once per repo, by hand.
  Also migrates existing lessons files (a single big PITFALLS.md, LESSONS.md, gotchas,
  untracked or git-ignored notes) into the shared, scoped layout.
disable-model-invocation: true
---

# Setting up repo memory (pitfalls)

An agent starts every session knowing nothing. Lessons kept on one laptop help one
person; a single growing lessons file loaded every session costs everyone context.
This sets up the middle path: `PITFALLS.md` files anywhere in the tree, committed and
shared, and the plugin's hooks show the agent only the **headings** of the files in
scope (root at session start; a folder's file when the agent works there), once per
session. The rule file teaches where and how to write entries so they're found.

## Steps

1. **Look first.** Find existing lessons: `PITFALLS.md`, `LESSONS.md`, `docs/*lesson*`,
   "gotchas" sections in CLAUDE.md files, untracked or git-ignored notes. Read them; they
   are material to keep, not to overwrite.

2. **Write the rule.** Copy `assets/memory-rule.md` to `.claude/rules/memory.md` (no
   `paths:` frontmatter: it applies everywhere). Its presence is also the opt-in that
   turns on the plugin's hooks in this repo.

3. **Create the root `PITFALLS.md`** if missing:

   ```markdown
   # Pitfalls

   Repo-wide traps only. Component traps live in that component's PITFALLS.md.
   ```

4. **Migrate existing lessons, entry by entry**, following the rule's "Where it goes"
   and "How to write it" sections:
   - Place each in the nearest folder containing every place the mistake can be made.
   - Rewrite its heading to name the trigger, in the words of the code (15 words max).
   - Give it *Cause* and *Fix* (or *Guarded by*). If you can't find the cause, keep the
     original wording and mark it in your report as unverified; don't invent one.
   - If a test or check already makes the trap impossible, don't migrate it; say so.
   - Don't invent entries from old commits unless the user asks; list candidates in
     the report instead.

5. **Un-hide them.** If `.gitignore` excludes any `PITFALLS.md` or lessons file, remove
   those lines and say why in one sentence (the team can't share what git doesn't
   track). Make sure `CLAUDE.local.md` *is* ignored, and move personal preferences found
   in old notes there.

6. **Point CLAUDE.md at it**, with one line, not a copy:
   `Pitfalls: see .claude/rules/memory.md (PITFALLS.md files, headings shown by scope).`

7. **Offer a private HANDOFF.md, and install it only if they say yes.** Ask once:
   "Do you want a private HANDOFF.md? It's your own note of where your work stands,
   on your machine only, rewritten at the end of each session and loaded when the next
   one starts." If yes:
   - add `HANDOFF.md` to `.gitignore` (if a HANDOFF.md is already tracked, ask before
     untracking it: `git rm --cached HANDOFF.md` keeps the file on disk);
   - append `assets/handoff-rule.md` to `.claude/rules/memory.md` (its heading is
     also what turns on loading HANDOFF.md at session start);
   - if an old HANDOFF.md exists, keep it as the starting point, and move anything in
     it the team should know to PITFALLS.md or CLAUDE.md.
   If no, install nothing about handoff.

8. **Run the checker** (`scripts/check_pitfalls.py`) on the result, fix what it flags,
   and **report**: what you created, moved (old place → new place), left alone, the
   candidates you didn't add, and whether the private handoff is on.

## Notes

- Runs once per repo, started by hand (`/repo-memory:memory-setup`); it costs nothing
  in other sessions. The daily work is done by the rule file and the hooks.
- The hooks are silent in repos without `.claude/rules/memory.md`. HANDOFF.md is
  loaded only when that rule has the handoff section.
