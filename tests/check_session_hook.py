#!/usr/bin/env python3
"""Check the repo-memory pitfalls hooks end to end on a temp repo."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = Path(__file__).resolve().parent.parent / "plugins/repo-memory/hooks/pitfalls.py"


def run(root, mode, payload):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(root))
    out = subprocess.run([sys.executable, str(HOOK), mode], input=json.dumps(payload), env=env,
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out else ""


with tempfile.TemporaryDirectory() as d:
    root = Path(d)
    (root / "shop/orders").mkdir(parents=True)
    (root / "shop/orders/api.py").write_text("x = 1\n")
    (root / "shop/orders/totals.py").write_text("y = 1\n")
    (root / "PITFALLS.md").write_text("# Pitfalls\n\n## Floats for money round wrong on invoices\n*Cause:* x *Fix:* y\n")
    (root / "shop/PITFALLS.md").write_text("# P\n\n## charge() returns None on failure, looks like success\n*Cause:* x\n")
    (root / "shop/orders/PITFALLS.md").write_text("# P\n\n## Applying a discount twice gives 19%\n*Cause:* body text\n")
    s = {"session_id": "t", "cwd": str(root)}
    tool = dict(s, hook_event_name="PostToolUse", tool_input={"file_path": str(root / "shop/orders/api.py")})

    assert run(root, "session-start", s) == "", "silent without opt-in"
    assert run(root, "tool", tool) == "", "silent without opt-in"
    (root / ".claude/rules").mkdir(parents=True)
    (root / ".claude/rules/memory.md").write_text("rule")

    ctx = run(root, "session-start", s)
    assert "Floats for money" in ctx and "discount" not in ctx, ctx
    ctx = run(root, "tool", tool)
    assert "shop/PITFALLS.md" in ctx and "shop/orders/PITFALLS.md" in ctx, ctx
    assert "Floats for money" not in ctx and "body text" not in ctx, ctx
    assert ctx.index("shop/PITFALLS.md") < ctx.index("shop/orders/PITFALLS.md"), "outermost first"
    tool2 = dict(tool, tool_input={"file_path": str(root / "shop/orders/totals.py")})
    assert run(root, "tool", tool2) == "", "each heading once per session"
    with open(root / "shop/orders/PITFALLS.md", "a") as f:
        f.write("\n## Empty order totals 0 instead of failing\n*Cause:* x\n")
    ctx = run(root, "tool", tool2)
    assert "Empty order" in ctx and "Applying a discount" not in ctx, "only the new heading"
    run(root, "session-start", s)  # compact/clear: start over
    assert "Applying a discount" in run(root, "tool", tool), "shown again after compaction"
print("pitfalls hooks: ok")
