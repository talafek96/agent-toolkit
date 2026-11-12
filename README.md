# agent-toolkit

Plugins for making a repo work well with coding agents. Installable as a
[Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugin-marketplaces).

| Plugin | What it does |
|---|---|
| `claude-md-standards` | Write, lint and review `CLAUDE.md` / `AGENTS.md`. Keeps only what the agent wouldn't do untold. Ships a linter (`scripts/lint_claude_md.py`). |
| `orchestrate` | Lead a feature as the senior engineer: understand the design, brief cheaper subagents with how / what / why, review every deliverable against the design, and report at checkpoints. Raises to you only what truly needs you. Start it with `/orchestrate <feature or spec>`. |
| `constitution-writer` | Write or review a project constitution: the few principles the agent reads every session, each with its why. In an existing repo it interviews the people who built it instead of guessing the reasons, routes every rule to the right file, and wires the result into `CLAUDE.md`. |

## Install

In Claude Code:

```text
/plugin marketplace add talafek96/agent-toolkit
/plugin install claude-md-standards@agent-toolkit
/plugin install constitution-writer@agent-toolkit
/plugin install orchestrate@agent-toolkit
```

To give a whole team the plugins, install them with project scope inside the repo
(`claude plugin install <name>@agent-toolkit --scope project`), so they're recorded
in the repo's `.claude/settings.json`.

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
