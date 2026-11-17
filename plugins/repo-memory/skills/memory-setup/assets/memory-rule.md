# Pitfalls: what this repo taught us

You start every session knowing nothing. `PITFALLS.md` files are the team's shared
memory of traps: committed, reviewed like code, and placed next to the code they're
about. Any folder can have one.

## How you'll see them

You get only headings, never whole files. At session start: the root `PITFALLS.md`.
When you read or edit a file: the headings of every `PITFALLS.md` from that file's
folder up to the root, each labelled with its file, once per session. **When a heading
touches what you're about to do, read that entry before you do it.**

## When to write one

- **In the same commit as the fix**, when the cause wasn't obvious from the error: a
  trap the next person would fall into too. Not for typos, and not for problems the
  error message already explains.
- **First ask: can a check make this impossible?** A test, a lint rule, a type, an
  assertion, an API that refuses the misuse. If yes, write the check instead. When a
  check later catches an existing trap, delete its entry.
- **Update, don't duplicate.** If an entry already covers it, improve that entry.

## Where it goes

1. List every place the mistake can be **made**, meaning where someone would be
   editing when they make it. Not where the symptom shows up.
2. Put the entry in the **nearest folder that contains all of those places**. Anyone
   who could make the mistake passes through that scope, so it can't be missed.
3. **Not higher.** A level too high loads it where it can't matter, and noise teaches
   readers to skim.
4. Follow the logical units: one component → its folder; two components → their
   shared parent; anywhere in the repo → the root. Keep the root short.
5. **One place only.** Never copy an entry into a second file.

If the mistake is misusing an API from anywhere, prefer making the API refuse the
misuse over parking the entry at the root.

## How to write it so it's found

Headings are all anyone sees, so the heading does the work.

- **Name the trigger, not only the symptom:** the action that causes it, in the words of
  the code someone would be touching. "Applying a discount anywhere but checkout doubles
  it (SAVE10 gave 19%)", not "Discount bug".
- **Use the names they'll be editing:** functions, config keys, commands, files.
- **One trap per heading, 15 words at most.** No "Note:", "Important", dates or ticket
  numbers. A heading that needs "and" is two pitfalls.
- **Short body:** *Cause*, *Fix*, and *Where it's fixed* (file, test or commit) or the
  check that now guards it. Longer explanations go in a doc the entry links to.

```markdown
## Applying a discount anywhere but checkout doubles it (SAVE10 gave 19%)
*Cause:* checkout recomputed from a cart total that already had the discount.
*Fix:* apply once, in `checkout()`. *Guarded by:* tests/comp/orders/test_checkout.py
```

## What stays private

Personal preferences about how *you* like to work go in `CLAUDE.local.md`
(git-ignored). Anything about the project and its traps goes where the team sees it.
