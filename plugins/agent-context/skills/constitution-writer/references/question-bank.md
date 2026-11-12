# Question bank

Topics most product teams hold a belief about. These are **questions to ask**, not
principles to copy: a team that answers "we don't care" has told you something too,
and that topic stays out. Skip any topic the survey already answered with evidence.

Ask each as an open question, then the two follow-ups that make a principle:
**"Why?"** and **"How would we notice someone broke it?"**

## Correctness and failure

- When something impossible happens at runtime, do we crash, log and continue, or
  return an error? Why that and not the others?
- Is a wrong answer worse than no answer here? (Shapes "refuse rather than guess".)
- What does a bug report need to contain for us to fix it fast? (Logs, traces, dumps.)

## Tests

- Can anyone (or any agent) change a test to make it pass? Who decides?
- Which test levels exist (unit, component, system, end-to-end), what does each
  prove, and which one is the gate before a merge?
- Is coverage a target, or do we fence behavior that matters? Why?
- What do we do with a flaky test?

## Simplicity and change

- Do we add a dependency easily or reluctantly? What made us that way?
- When we can reuse or write new, which wins by default?
- Are known bugs a backlog item or a blocker for new work?

## Design and planning

- Does a feature need a written spec or design before code? Who approves it?
- When the implementation finds the design is wrong, what happens: fix the design
  first, or fix forward?

## Knowledge

- Where does a lesson learned live, so the next person (or agent) doesn't repeat it?
- Where is the single source of truth for configuration, registries, constants?

## People and product

- Who is the product for, and what must never happen to them? (Data loss, privacy,
  surprise.) These often become the one or two NON-NEGOTIABLE principles.
- What does the user decide, and what may the software (or an agent) decide alone?

## Priority between principles

- When two of these conflict (shipping speed vs. stability, simplicity vs.
  flexibility), which wins? The answer sets the order of the principles.
