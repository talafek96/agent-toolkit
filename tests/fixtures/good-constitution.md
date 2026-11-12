# Example Constitution

Read every session; wins over rules files and CLAUDE.md on conflict.

## Core Principles

### I. Tests Are the Contract
- Never change, skip or delete a test to make it pass; a human decides that.
- *Why: if the agent can edit the tests, a green run proves nothing.*

### II. Fail Fast
- On a broken invariant, stop with a trace instead of continuing.
- *Why: a process that limps on corrupts more state, far from the cause.*

## Governance
Changes are approved by the team lead in a reviewed pull request.
