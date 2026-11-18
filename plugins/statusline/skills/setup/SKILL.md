---
name: setup
description: >-
  Install the agent-toolkit status line: copies the script next to your Claude Code
  settings and sets statusLine to it. Run by hand once, and again after a plugin update
  to pick up the new version.
disable-model-invocation: true
---

# Install the status line

The script is `${CLAUDE_PLUGIN_ROOT}/scripts/statusline.py` (standard-library Python,
no dependencies). The installer copies it next to the settings file and points
`statusLine` at the copy, because the plugin folder's path changes on every update.

1. **Preview.** Run
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/install.py" --dry-run`
   and show the user what it would change. The default target is the user settings
   (`~/.claude/settings.json`): the status line is personal, not a team setting. Use
   `--settings <path>` only if the user asks for another file.

2. **If it exits 2**, a different status line is already set. Show the user the
   current one and ask whether to replace it. Only on a yes, add `--replace`. The old
   settings file and script are kept as `*.bak`.

3. **Install.** Run the same command without `--dry-run`. Settings reload on their
   own; no restart.

4. **Report** in two lines: what changed, and what the rows show:
   session and tasks · project and git status · model, thinking and context used ·
   cost estimate, time, edits and rate limits, then the transcript path.
