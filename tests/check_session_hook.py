#!/usr/bin/env python3
"""Check the repo-memory SessionStart hook: silent without opt-in; with it, emits the
branch's HANDOFF.md and the PITFALLS.md headings."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "plugins/repo-memory/hooks/session_start.py"


def run(root):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root))
    return subprocess.run([sys.executable, str(HOOK)], env=env, capture_output=True, text=True, check=True).stdout


with tempfile.TemporaryDirectory() as d:
    root = Path(d)
    subprocess.run(["git", "init", "-q", "-b", "usr/t/feat", str(root)], check=True)
    (root / "HANDOFF.md").write_text("# Handoff\nGoal: X\n")
    (root / "PITFALLS.md").write_text("# Pitfalls\n\n## Totals off by a cent\nCause: floats\n")
    assert run(root) == "", "hook must be silent without .claude/rules/memory.md"
    (root / ".claude/rules").mkdir(parents=True)
    (root / ".claude/rules/memory.md").write_text("rule")
    ctx = json.loads(run(root))["hookSpecificOutput"]["additionalContext"]
    assert "Goal: X" in ctx and "## Totals off by a cent" in ctx and "Cause: floats" not in ctx, ctx
    subprocess.run(["git", "-C", str(root), "checkout", "-q", "-b", "main"], check=True)
    ctx = json.loads(run(root))["hookSpecificOutput"]["additionalContext"]
    assert "WARNING: HANDOFF.md is on main" in ctx and "Goal: X" not in ctx, ctx
print("session hook: ok")
