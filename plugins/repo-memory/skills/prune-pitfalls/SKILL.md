---
name: prune-pitfalls
description: >-
  Prune every PITFALLS.md in the repo: delete entries a check now guards or whose code
  is gone, merge duplicates, move misplaced entries to the right folder, and sharpen
  headings that won't be found. Shows the plan, then commits on approval. Run by hand,
  now and then (monthly, or when the files feel noisy).
disable-model-invocation: true
---

# Prune pitfalls

`PITFALLS.md` files should hold only traps no check can catch, each in the right place,
each with a heading that gets found. Daily work keeps them mostly right; this pass
catches what drifted. Follow `.claude/rules/memory.md` for what a good entry is and
where it goes. If the repo has no such rule, stop and suggest `/repo-memory:memory-setup`.

## 1. Inventory

Run `python "${CLAUDE_PLUGIN_ROOT}/skills/memory-setup/scripts/check_pitfalls.py" .`
(or the repo's copy of the checker), then list every entry: file, heading, and the
names it mentions (functions, files, config keys, commands).

## 2. Judge each entry against the code, not from memory

For each entry, check the repo and give it one verdict:

| Verdict | When | Evidence you need |
|---|---|---|
| **Delete: guarded** | A test, lint rule, type or assertion now makes the trap impossible | The check's file and name; read it and confirm it would fail on the mistake |
| **Delete: gone** | The code it's about no longer exists (function, file, feature removed) | A search that finds nothing, or the commit that removed it |
| **Merge** | Two entries describe the same trap | Both locations; keep one, in the right place, with the better heading |
| **Move** | The entry isn't in the nearest folder that contains every place the mistake can be made | Where the mistake can be made today, and the folder that should own it |
| **Rewrite heading** | The heading names a symptom only, is vague, too long, or uses old names | The current names in the code |
| **Keep** | Still a live trap, well placed, well named | Nothing to change |

Never delete an entry because it *looks* old or unimportant. Without evidence, keep it,
and list it under "couldn't verify" in the plan.

If an entry describes a trap that could be made impossible cheaply (a one-line
assertion, a missing test), list it as a **suggestion**; don't write the check yourself
as part of pruning.

## 3. Show the plan before changing anything

One table: entry → verdict → evidence. Then the totals (entries before → after). Ask
the user to approve, adjust or skip items. If nobody can answer (a non-interactive
run), stop here and leave the plan in your reply: pruning without approval deletes
the team's memory.

## 4. Apply and commit

Apply only the approved items. Run the checker again; it must report no errors. Commit
only the `PITFALLS.md` files you changed, with a message that lists what was deleted,
merged and moved, and why, so `git log` explains every removal.
