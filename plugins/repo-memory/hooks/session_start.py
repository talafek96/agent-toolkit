#!/usr/bin/env python3
"""SessionStart hook for repo-memory.

Does nothing unless the repo opted in (has .claude/rules/memory.md). Then it hands the
agent: the branch's HANDOFF.md (the state of this piece of work) and the list of
PITFALLS.md headings (so it knows which traps exist and can read the one it needs).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

MAX_HANDOFF_CHARS = 8000
MAX_HEADINGS = 200


def main() -> int:
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    if not (root / ".claude/rules/memory.md").is_file():
        return 0

    parts = []
    try:
        branch = subprocess.run(["git", "-C", str(root), "branch", "--show-current"],
                                capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        branch = ""

    handoff = root / "HANDOFF.md"
    if handoff.is_file() and branch in ("main", "master"):
        parts.append(f"WARNING: HANDOFF.md is on {branch}. A handoff belongs on its work's branch. "
                     "Before other work, tell the user and offer to move it to its branch, or close it "
                     "(lessons to PITFALLS.md / CLAUDE.md / rules, personal lines to CLAUDE.local.md, then delete it).")
    elif handoff.is_file():
        text = handoff.read_text(encoding="utf-8", errors="replace")
        if len(text) > MAX_HANDOFF_CHARS:
            text = text[:MAX_HANDOFF_CHARS] + "\n[... HANDOFF.md truncated; read the file for the rest]"
        parts.append(f"## HANDOFF.md (branch: {branch or 'unknown'})\n"
                     "The state of the work on this branch, written at the end of the last session.\n\n" + text)
    elif branch and branch not in ("main", "master"):
        parts.append(f"No HANDOFF.md on branch '{branch}' yet: this is a fresh piece of work.")

    pitfalls = root / "PITFALLS.md"
    if pitfalls.is_file():
        heads = [ln.strip() for ln in pitfalls.read_text(encoding="utf-8", errors="replace").splitlines()
                 if re.match(r"^#{2,3} ", ln)]
        if heads:
            shown = heads[:MAX_HEADINGS]
            more = f"\n(+{len(heads) - len(shown)} more)" if len(heads) > len(shown) else ""
            parts.append("## PITFALLS.md headings\nKnown traps. Before working in an area, read the "
                         "matching entry in full.\n" + "\n".join(shown) + more)

    if parts:
        context = "# Repo memory (loaded by the repo-memory plugin)\n\n" + "\n\n".join(parts)
        json.dump({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}},
                  sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
