---
name: setup
description: >-
  Install the agent-toolkit status line: copies the script next to your Claude Code
  settings and sets statusLine to run it with uv. Run by hand once, and again after a
  plugin update to pick up the new version.
disable-model-invocation: true
---

# Install the status line

The installer does the whole job; don't edit settings or write a status line command
yourself. It sets exactly this (the path is the user's):

```json
"statusLine": {"type": "command", "command": "uv run --script ~/.claude/statusline.py", "refreshInterval": 5}
```

The script is copied next to the settings file because the plugin folder's path
changes on every update.

1. **Preview.** Run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/install.py" --dry-run`
   and show the user what it would change. Default target: the user settings
   (`~/.claude/settings.json`); use `--settings <path>` only if the user asks.

2. **Exit 3: uv is missing.** Show the install command it printed and ask the user
   whether to run it. After uv is installed, start again from step 1.

3. **Exit 2: someone else's status line is set.** Show it and ask whether to replace
   it. Only on a yes, add `--replace`. The old file is kept as `*.bak`.

4. **Install.** Run the same command without `--dry-run`. It runs the new command
   through a shell with a sample session and checks it renders.
   - **Exit 0:** done. Settings reload on their own; no restart.
   - **Exit 4:** it didn't render. Show the error it printed. Don't hand-write a
     different command; fix the cause (usually uv can't download Python: no network),
     then run the installer again.

5. **Report** in two lines: what changed, and what the rows show:
   session and tasks · project and git status · model, thinking and context used ·
   cost estimate, time, edits and rate limits, then the transcript path.
