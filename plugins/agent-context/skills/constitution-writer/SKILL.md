---
name: constitution-writer
description: >-
  Write, refresh or review a project constitution: the short, high-level file of
  principles ("we believe", each with its why) that a coding agent reads every
  session and that Spec Kit plans against. Use it whenever someone wants to onboard
  a repo to AI agents or Spec Kit, run or replace /speckit.constitution, capture a
  team's engineering principles, turn tribal knowledge in senior engineers' heads
  into written principles, decide whether a rule belongs in the constitution or in
  CLAUDE.md, or asks "is our constitution any good" or "it's too long". Also use it
  for a brand-new repo where a manager or lead dictates the principles, and for an
  existing (brownfield) repo where nobody wrote them down.
---

# Writing a project constitution

A constitution is the team's DNA: a handful of general beliefs that steer decisions,
each with the reason behind it. An agent reads it at the start of every session (it
is `@`-imported into CLAUDE.md), and Spec Kit checks every plan against it.

**A principle leads the direction of decisions; it is not a rule about this code.**
"Fail fast", "simplicity over flexibility", "tests are the contract", "a lesson lives
in the repo, not in someone's head": each of these could hold for many of the team's
projects, and each helps choose between two reasonable options in a case nobody has
seen yet. "Every external call has a timeout", "order prices are whole cents",
"system tests gate the merge" are good rules, but they are *ways of living* a
principle in this codebase. They go in CLAUDE.md, a rules file or a folder's
CLAUDE.md, and the principle links to them as its mechanics.

Three things follow, and they drive everything below:

- **It steers, it doesn't specify.** Most candidates you collect will be specific
  rules. Your main job is to find the few beliefs behind them, not to list the rules.
- **It is paid for in every session.** Every line costs context forever, so it holds
  only what is still worth saying in a year, on any project of this team.
- **Its value is the why.** A rule without a reason gets followed literally, and
  broken the first time a case doesn't fit. A belief with its reason lets the agent
  make the right call in cases nobody listed.

The hard part is not the writing. It is getting the real reasons, which usually live
in the heads of the people who built the repo, not in any file.

## Pick the path

| Situation | Path |
|---|---|
| New repo; someone (manager, lead) can state the beliefs | **A. Dictated** |
| Existing repo; the beliefs were never written down | **B. Brownfield** |
| A constitution exists; review, shrink or refresh it | **C. Review** |

## A. Dictated (new repo)

1. Ask for the beliefs as the person would say them out loud. Short bullets are fine.
2. For each one, ask **why** until you have a reason in their words, and **how a
   violation would show up** (a review comment, a failing check, a crash). A belief
   whose violation nobody could notice is a wish; say so.
3. For the topics in "What a good one covers" that their list doesn't mention, walk
   through the recommended principles with them (see "Recommended principles"), and
   let them adopt, change, invert or skip each one.
4. Ask which belief wins when two conflict (speed vs. stability, simplicity vs.
   flexibility). The order of the principles records that answer.
5. Run every candidate through the boundary test (below), draft, get approval, wire it in.

## B. Brownfield (existing repo)

The code shows *what* the team does. It cannot show *why*, and a guessed why is worse
than none: it reads as authoritative. So the agent's job is to find the questions,
not to answer them.

1. **Survey.** Read the README, every CLAUDE.md / AGENTS.md, `.claude/rules/`, CI
   config, lint config, the test folder layout, and `git log` (look for patterns:
   reverts, "fix flaky", repeated review themes; `git log --grep` helps). If `gh` is
   available, skim recent PR review comments: they are the team's beliefs, enforced
   by hand. Note any existing written principles, even in a wiki dump.
2. **Turn patterns into questions.** For each pattern, write one observation with
   evidence and one question:
   > *Observed:* every module validates input at its public function and nowhere
   > inside (`orders/api.py`, `money/api.py`). *Ask:* is that a rule? Why?
   Aim for 8–15 questions. Include the topics in `references/question-bank.md` that
   the survey didn't already answer.
3. **Interview the people who built the repo.** Ideally a short meeting with the
   veterans and the manager (the beliefs are the team's, not one person's). Ask one
   question at a time. Record answers in their words. If the user is alone, ask them,
   and mark answers that need the team's confirmation.
4. **Every principle needs a source, and you are never the source.** A principle
   goes into the file only if its belief *and* its reason come from the evidence
   (cite the commit, file or review comment) or from the person you're talking to.
   For each topic in "What a good one covers" that the evidence doesn't settle,
   **ask the person** (one topic at a time, see "Recommended principles" below):
   show the recommended principle and why it's recommended, then ask how they work.
   Their answer decides: write it as recommended, write their version, write the
   *opposite* if that's what they believe (a team that prefers "degrade gracefully"
   over "fail fast" should say so, with its reason), or leave the topic out.
   Write the reason in the file as they gave it.
5. **When nobody can answer right now** (a non-interactive run, or the person is
   away), the file holds only what the evidence supports. Everything else goes in the
   response as **recommended principles to discuss**: each one with the recommended
   wording, why it's recommended, and the question to settle it. Never put
   `(proposed)`, `[ASK]`, TODOs or any other open-question marker in the file itself:
   it must read as the finished document. And never label a reason as "evidenced"
   unless the evidence states that reason, not just the rule.
   One exception keeps the draft usable: when a belief is sourced (the person stated
   it, or the evidence shows it) but its reason isn't, and the belief matches a
   recommended principle, you may write the recommended reason in the file and list
   it in the response as "reason to confirm". Anything you put in quotation marks
   must be copied exactly from its source.
6. **Find the beliefs behind the answers.** Most answers will be specific rules
   ("we always validate at the public function"). Group them and ask what they have
   in common; that shared belief is the principle, and the rules become its
   mechanics. A brownfield constitution usually ends up with fewer principles than
   the survey produced questions.
7. **Write the belief, not the habit.** Where the code and the answers disagree
   (they say "fail fast", the code swallows errors), the constitution states what the
   team wants. List the gap separately as known work (see output). Don't weaken the
   principle to match today's code.

## C. Review an existing constitution

Run `python scripts/check_constitution.py <file>` for the mechanical checks (missing
whys, length, leftover template placeholders, embedded change logs). Then judge:

- Does each principle have a why in the team's words, not a restatement of the rule?
- Does each pass the boundary test, or is it a project fact, a language convention,
  or something the agent does anyway?
- Is anything stated twice, or contradicted by CLAUDE.md or a rules file?
- Would cutting it change any decision? If not, cut it.

Propose a diff with the reason per change; don't rewrite silently. If the review
leaves topics uncovered, handle them as in path B steps 4–5: ask, or list them as
recommended principles in the response. Don't add sections (a testing table, new
principles) that neither the file, the repo nor the person supports.

## The boundary test: where does each rule go?

Run every candidate through this, top to bottom; the first match wins.

| If the candidate is… | It goes to |
|---|---|
| Something the agent already does without being told | **nowhere** (delete it) |
| Enforced by a tool (formatter, linter, type checker, CI gate) | **nowhere**; the tool is the rule. At most, one line in CLAUDE.md naming the command |
| A specific rule about one thing: a field, a data type, a module, a format ("order prices are whole cents") | **not a principle**. Find the belief it comes from and make *that* the principle; the specific rule goes in a rules file or the folder's CLAUDE.md, linked as the principle's mechanics |
| A belief that holds across the whole project and would survive a change of language or framework | **constitution** |
| A convention for one language or tool (style, naming, git message format) | **a rules file**, e.g. `.claude/rules/python.md`, path-scoped where the tool supports it |
| Mechanics local to one folder (how tests are laid out, how a subsystem is wired) | **that folder's CLAUDE.md**, e.g. `tests/CLAUDE.md` |
| A project fact or decision (commands, where things live, a specific choice made once) | **root CLAUDE.md** |

Four quick checks. A real principle passes all of them:

- **Another project.** Would it hold, word for word, for a different project of the
  same team (a different product, another language)? If it names a module, a field,
  a tool, a service or a number, it's a rule for this repo, not a principle.
- **A decision.** Name a real choice between two reasonable options that this
  principle settles. If you can't, it's a wish or a procedure.
- **Swap the language.** If the rule breaks when you name another language ("use
  RAII", "type hints on public functions"), it's a convention.
- **Ask "why?" once.** If the answer is a more general belief, that belief is the
  principle and the rule is one way of living it. "Order prices are whole cents"
  → why? → "a total that's slightly wrong is worse than an error" → the principle is
  *Exact or Nothing*, and the cents rule lives in `money/CLAUDE.md`. A principle
  names a belief; it should apply to cases nobody has thought of yet.

Expect the numbers to come out lopsided: a team's list of ten "beliefs" often holds
three or four principles and six or seven rules. That's the right result, not a
loss. Show it in the routing table, so nobody thinks their rule was dropped.

The *principle* (its name and its belief) must be general. Its bullets then say
what the belief means in practice, and may use concrete examples ("e.g. an X-macro
list", "would-block, timeout, not-found") to make it unambiguous. The test is that
the principle still holds on the team's next project, even if an example changes.
Lists of product details (every network call, every file, every command) and
operating rules for agents (how to share a working tree, how long reports are) are
not examples; they go in CLAUDE.md or a rules file, linked as Mechanics.

## Recommended principles

`references/recommended-principles.md` holds a recommended principle for each topic,
with why it's recommended. Use it to make the conversation concrete: "Here's what we
recommend for failures, and why. How does your team handle them?" It is a starting
point for the person's decision, never content to paste in unasked. When you present
one, give the reason it's recommended in a sentence or two, so the person can judge
it rather than just accept it.

## Principle format

Model it on strong real constitutions: a general name, then several bullets, each
opening with a **bold, imperative headline** and a short clarification. The reason
is carried either inline in a bullet ("…rather than limp on — a limping process
silently corrupts more state") or in a closing `*Why:*` line. Every principle needs
its reason *somewhere*; a separate Why line is best where the reason isn't obvious
from the bullets.

```markdown
### I. Fail Fast

- **Make bugs shout.** On a broken invariant, stop immediately with a trace rather
  than continue in an undefined state — a process that limps on corrupts more state.
- **Never disguise a failure as a normal result.** Return a value only for an
  outcome the caller branches on (not found, timeout); a real failure stops.
- **Every failure carries enough to triage** without a live debugger.
- *Why: a wrong answer that looks right is the most expensive bug there is; a loud
  failure gets fixed the same day.* Mechanics: `src/errors/CLAUDE.md`.
```

- **Name**: a belief, short and memorable ("Fail Fast", "Power of Simplicity",
  "Stability First", "Organizational Memory"), never a topic ("Error Handling").
- **Bullets**: 2–6. Each something a reviewer could point at. "Do X", not
  "consider X".
- **Mechanics**: link to the rules file or folder CLAUDE.md that holds the how.
- Mark at most one or two principles `(NON-NEGOTIABLE)`: the things the team would
  stop a release for (often the user's data, privacy, money).

Order the principles so that the one that should win a conflict comes first.

## What a good one covers

Strong constitutions cover how the team *works*, not only how the code looks. Go
through each topic. Include it when the evidence or the person supports it; otherwise
ask, or list it in the response as a recommended principle to discuss. The recommended
wording and its reasoning for each topic are in `references/recommended-principles.md`.

- **Failure**: fail fast vs. degrade; no plausible wrong answers.
- **Simplicity**: simplest path that works; reuse before writing; fewest types and
  files; no speculative generality.
- **Stability and bugs**: stability before features; known bugs block new work;
  design before code; build on a tested base.
- **Ownership of quality**: the developer (or agent) is the first line of defense,
  not CI; self-review; what "done" means.
- **Tests**: tests are the contract on agent-written code; a failing test, lint or
  type check is a red alert, never weakened to pass; a defect adds a test; no flaky
  tests; a change is fenced at every level it touches (unit, composition, merge gate).
- **Debuggability**: diagnosable from logs and artifacts; act on observed state,
  never on sleeps.
- **Knowledge**: the repo is the source of truth; decisions inline; lessons recorded.
- **Flow**: never block others; blockers first; batch by area.
- **Configuration**: one source per registry; derive, don't duplicate.
- **The product's non-negotiable** (privacy, the user's data, money), if it has one.

## File shape and size

```markdown
# <Project> Constitution

<2–4 lines: the project's durable standards, its DNA; read every session; the how
lives in .claude/rules/ and folder CLAUDE.md files; on conflict, this file wins.>

## Core Principles
### I. … through ### N. …     (usually 6–10)

## Testing Discipline
| Level | Used | Notes |       (every level, including the ones the team does NOT use, and why;
                                 notes say each level's purpose and when it runs, no repo paths:
                                 the folder layout belongs in tests/CLAUDE.md)
Explicitly avoided: … (e.g. TDD, coverage targets), with the reason.

## <Optional cross-cutting standards: e.g. logging and defect levels, scripting>

## Governance
- This file supersedes ad-hoc practice; deviations are justified in writing where made.
- Relationship to rules files and CLAUDE.md: they hold the how, must not restate
  this file, and must stay consistent with it.
- Who approves an amendment (reviewed like code).
```

- Usually 120–220 lines. Dense is fine; padding and repetition are not. It's loaded
  every session, so every line must change a decision.
- **No change log, sync-impact report or version history inside the file.** Git
  keeps history, and the log costs tokens in every session forever. One version
  footer line is enough if the tooling wants it.
- No placeholders left from the template (`[PRINCIPLE_1_NAME]`, `[DATE]`).

## Approve, then wire it in

1. Show the user the draft **and** a routing table: every candidate that did *not*
   go into the constitution, with where it went (CLAUDE.md, a rules file, nowhere)
   and why. This is where most of the value of the review is; people often expect
   their favorite style rule in the constitution.
2. Write files only after approval. Location:
   - Spec Kit present (`.specify/`): `.specify/memory/constitution.md`.
   - Otherwise: `.claude/constitution.md` (or wherever the team keeps agent docs).
3. Make sure root CLAUDE.md imports it: a line `@.specify/memory/constitution.md`
   (adjust the path). Without the import, the agent never sees it; Claude Code
   doesn't load a constitution on its own.
4. Move routed items to their homes (rules files, folder CLAUDE.md files) if the
   user agrees. If the claude-md-standards skill is available, suggest running it on
   CLAUDE.md afterwards.

## What to hand back

Always end with these sections, in this order:

1. **The constitution draft** (or the diff, in review mode).
2. **Routing table**: candidate → where it went → why.
3. **Recommended principles to discuss and open questions**: each topic the file
   doesn't cover yet, with the recommended wording, why it's recommended, and the
   question to settle it; plus any reason you need confirmed. Grouped by who should
   answer.
4. **Known gaps**: places where today's code doesn't follow a principle yet, with
   evidence (file paths). This is work, not a reason to soften the principle.
5. **Next step**: the one thing to do now (usually "hold the 30-minute interview" or
   "approve and I'll wire it in").

## References

- `references/question-bank.md`: topics worth asking about, with sample questions.
  Read it in path B step 2 and path A step 2.
- `references/examples.md`: good and bad principles, side by side. Read it when
  drafting or reviewing wording.
- `scripts/check_constitution.py`: mechanical checks for path C and before handing
  back any draft.
