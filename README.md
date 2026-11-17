# agent-toolkit

Plugins for making a repo work well with coding agents. Installable as a
[Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces).

| Plugin | Skills inside | What it does |
|---|---|---|
| `agent-context` | `claude-md-standards`, `constitution-writer` | Quality for the files the agent reads every session. **claude-md-standards** writes, lints and reviews `CLAUDE.md` / `AGENTS.md`, keeping only what the agent wouldn't do untold (ships a linter). **constitution-writer** writes or reviews a project constitution: a few general principles, each with its why. In an existing repo it asks the people who built it instead of guessing the reasons, routes every specific rule to the right file, and wires the result into `CLAUDE.md`. |
| `repo-memory` | `memory-setup` (once per repo) and `prune-pitfalls` (now and then), both started by hand | Shared lessons, kept where they're found: a `PITFALLS.md` in any folder, next to the code it's about. Hooks show the agent only the **headings** in scope (the root file at session start; a folder's file, and its parents', when the agent reads or edits there), once per session; it opens an entry when a heading is relevant. A rule teaches where an entry goes (the nearest folder containing every place the mistake can be made) and how to write a heading that's found. Includes a checker, and `prune-pitfalls`: deletes entries a check now guards or whose code is gone, merges duplicates, moves misplaced entries, with evidence for each, and commits only after you approve. Setup also offers a private, git-ignored `HANDOFF.md` (where your own work stands), loaded at session start if you opt in. Personal preferences go in git-ignored `CLAUDE.local.md`. |
| `orchestrate` | `orchestrate` | Lead a feature as the senior engineer: understand the design, brief cheaper subagents with how / what / why, review every deliverable against the design, and report at checkpoints. Raises to you only what truly needs you. Start it with `/orchestrate <feature or spec>`. |

## Install

In Claude Code:

```text
/plugin marketplace add talafek96/agent-toolkit
/plugin install agent-context@agent-toolkit
/plugin install repo-memory@agent-toolkit
/plugin install orchestrate@agent-toolkit
```

When asked for the scope, choose **project** to give the whole team the plugins: they're
recorded in the repo's `.claude/settings.json`, which you commit. Then run
`/repo-memory:memory-setup` once in the repo.

## Where they fit

1. **Today:** run `claude-md-standards` on your `CLAUDE.md`. Cut every line the agent
   would follow anyway.
2. **This week:** run `constitution-writer`. In a repo you already have, it reads the
   code and history, writes the questions, and you put them to the people who built
   it. Nothing goes in without a why.
3. **Afterwards:** run `claude-md-standards` again; the constitution is now
   `@`-imported, and rules have moved to their own files.
4. **For big features:** plan with Spec Kit, then `/orchestrate` the tasks. It works
   best once tests and a merge gate exist, because its review leans on them.

## Contributing

Branches: `usr/<name>/<topic>` for work, pull requests into `main`. CI runs
`scripts/validate.py` (manifests and skill frontmatter) and ruff.
