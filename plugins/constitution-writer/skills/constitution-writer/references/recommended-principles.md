# Recommended principles

One recommended principle per topic, with why it's recommended and the question that
settles it. These are proven defaults from teams that build products with agents,
not facts about any particular repo. Present one at a time, explain the reason, and
let the person adopt it, reword it, invert it or skip it. Write only what they chose,
with the reason they gave (or the reason below, if they adopt it as is).

---

## Fail Fast

- **Make bugs shout.** On a broken invariant, stop immediately with a trace rather
  than continue in an undefined state.
- **Never disguise a failure as a normal result.** Return a value only for an outcome
  the caller expects to branch on (not found, timeout); a real failure stops.
- **Every failure carries enough to triage** without reproducing it live.

**Why recommended:** a process that limps on corrupts more state, and the bug shows up
far from its cause. A wrong answer that looks right is the most expensive kind of bug.
Agents in particular tend to "handle" errors by returning a default; this principle
stops that.
**Ask:** "When something impossible happens at runtime, do you want it to stop, or to
keep going? Is there anything that must stay up even when parts fail?"
**Common alternative:** degrade gracefully at the edges (a UI keeps rendering), but
never with a wrong value. If they choose it, write where degrading is allowed.

## Power of Simplicity

- **The simplest path that works.** Don't build structure the code doesn't need yet.
- **Reuse before writing.** Look for an existing primitive or pattern first; no second
  way to do the same thing.
- **Fewest types, files and layers that work.** A new abstraction must earn its place.
- **No speculative generality, and no cleverness a reader has to decode.**

**Why recommended:** agents happily generate abstractions, wrappers and new files;
every one is something the next reader (or agent) must load and understand.
Simplicity is what keeps a codebase small enough to fit in context.
**Ask:** "When the agent can either reuse something or write a cleaner new version,
which do you want by default?"

## Stability First

- **Stability outranks new features.**
- **Known bugs block new work;** they are not backlog.
- **Design first:** settle boundaries, data flow and interfaces before code.
- **Build on a tested base,** in increments; no throw-away code.

**Why recommended:** bugs that are lived with become behavior people depend on, and
each new feature is built on top of them. Design-first is also what gives an agent a
fixed target, so its fixes can't quietly drift from the plan.
**Ask:** "If a known bug and a new feature compete for the same week, which wins?
Does a feature need an agreed design before code?"

## The Author Owns Quality

- **You are the first line of defense, not CI or QA.** Fix fragile or tangled code
  the moment you notice it.
- **Review your own diff end to end** before asking anyone else to.
- **"Done" means validated:** the relevant tests and checks ran and passed.

**Why recommended:** when quality is "CI's job", everyone (and every agent) ships the
first thing that compiles. An agent told it owns "done" verifies before it reports.
**Ask:** "What does 'done' mean on this team? What must have run before a change is
handed over?"

## Tests Are the Contract

- **A failing test, lint or type check is a red alert,** never a nuisance to silence.
- **Never change, skip or delete a test to make it pass.** A test change means the
  intended behavior changed, and a human must agree to that, in writing.
- **Tests fence agent-written code:** they are the durable contract for what it must
  do.
- **A change is fenced at every level it touches** (its units, its composition, the
  merge gate), and **a defect adds the test that would have caught it.**
- **No flaky tests.** A test that sometimes fails is fixed or removed, not retried.

**Why recommended:** tests are the only check on agent-written code that you don't
have to take on trust. If the agent can edit them, a green run proves nothing.
**Ask:** "Who may change what a test expects? Which test levels do you use, and which
one gates a merge? What do you do with a flaky test today?"
**Also ask** about anything explicitly avoided (TDD, coverage targets) and why; write
it in the testing section.

## Diagnosable From the Evidence

- **Debuggable from logs and artifacts, not a live debugger.**
- **Instrumentation is part of "done".**
- **Act on observed state, never on sleeps or timing.**

**Why recommended:** production and CI failures can't be stepped through. And
sleep-based waits are the most common source of flaky tests and agent "fixes" that
only pass sometimes.
**Ask:** "When something fails in production or CI, how do you find out why?"

## Knowledge Lives in the Repo

- **The repo is the single source of truth.** Decisions and lessons are written where
  the next person, or agent, will find them.
- **Decisions live next to the code they govern;** docs hold only the slow-changing
  concepts.
- **A lesson is recorded in the same change as its fix.**

**Why recommended:** an agent starts every session knowing nothing. What isn't in the
repo doesn't exist for it, and what lives only in someone's head leaves with them.
**Ask:** "Where does a lesson learned live today, so it isn't learned twice?"

## Flow

- **Never block others:** unblock with stubs, fakes or mocks against the agreed
  interface.
- **Blockers first.**
- **Batch by area:** fix adjacent issues in place; group work by functional area.

**Why recommended:** parallel work, human or agent, only pays off when nobody waits.
**Ask:** "When you're blocked on someone else's piece, what do you do?"

## One Source of Truth for Configuration

- **One authoritative place per registry or setting;** a change is a one-place edit.
- **Derive, don't duplicate:** generate dependent lists and tables from that source.
- **No scattered magic constants.**

**Why recommended:** scattered configuration breeds "changed X, forgot Y" bugs, and an
agent editing one copy has no way to know the others exist.
**Ask:** "When you add an entry to a list the system uses in several places, how many
places do you edit?"

## The Product's Non-Negotiable

Many products have one thing they'd stop a release for: the user's data, privacy,
money, safety. If so, it's usually principle I, marked `(NON-NEGOTIABLE)`.

**Why recommended:** it settles every conflict with the other principles in advance.
**Ask:** "What must never happen to the people who use this?"
