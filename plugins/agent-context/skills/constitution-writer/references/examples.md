# Good and bad principles

Each pair shows the same intent written two ways. The bad versions are all common
in real constitutions.

## No why

**Bad**
```markdown
### IV. Error Handling
- All errors must be handled appropriately.
```
Vague ("appropriately"), no reason, and no way to tell if it was broken.

**Good**
```markdown
### IV. Fail Fast
- On a broken invariant, stop immediately with a trace. Don't limp on.
- Return an error only for a normal outcome the caller branches on (not found,
  timeout). A real failure is never disguised as a return value.
- *Why: a process that limps on corrupts more state, and the bug surfaces far from
  its cause. A loud crash is cheaper to fix than a quiet wrong answer.*
```

## A convention dressed as a principle

**Bad** (in the constitution)
```markdown
### VI. Python Style
- Use type hints on all public functions. Use f-strings. Max line length 100.
```
Breaks the "swap the language" test. Belongs in `.claude/rules/python.md`, and the
line length belongs to the formatter, not to any document.

## A specific rule dressed as a principle

**Bad**
```markdown
### I. Money
- Order prices are stored as whole cents, never floats.
- *Why: float rounding once put wrong totals on invoices.*
```
It has a why, and it's still not a principle: it covers one field. The next exact
quantity (tax rates, stock counts, exchange rates) gets no guidance from it.

**Good**
```markdown
### I. Exact or Nothing
- Anything a customer pays, receives or is told is computed exactly, or the
  operation fails with an error. Never an approximate or default value.
- *Why: a total that's slightly wrong reaches invoices and costs trust; an error
  gets fixed the same day.*
- Mechanics: money is integer cents (`shop/money/CLAUDE.md`).
```
Ask "why?" once about the specific rule; the answer is usually the principle.

## A project fact dressed as a principle

**Bad**
```markdown
### VIII. Database
- We use PostgreSQL 15 on port 5432. Migrations are in db/migrations.
```
A fact about this project, true until the next migration. Belongs in root CLAUDE.md
(if the agent needs it at all).

## A wish, not a rule

**Bad**
```markdown
### II. Quality
- Strive for high quality and maintainable code.
```
Nobody could point at a violation. Ask the team what they actually reject in review;
that is the rule.

**Good**
```markdown
### II. Known Bugs Block New Work
- A known bug in a shipped feature is fixed before new feature work starts.
- *Why: bugs we live with become the behavior people rely on, and each new feature
  is built on top of them. Fixing first keeps the base trustworthy.*
```

## A why that only restates the rule

**Bad**
```markdown
- Never change a test to make it pass.
- *Why: tests should not be changed to make them pass.*
```

**Good**
```markdown
- *Why: tests are the only check on agent-written code we don't have to trust. If
  the agent can edit them, a green run proves nothing.*
```

## Everything non-negotiable

**Bad**: seven of nine principles marked `(NON-NEGOTIABLE)`. The marker then carries
no information. Keep it for the one or two things the team would stop a release for
(often: user data, privacy, safety).
