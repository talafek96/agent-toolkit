#!/usr/bin/env python3
"""repo-memory hooks: hierarchical PITFALLS.md, headings only.

session-start: show the root PITFALLS.md headings, and the private HANDOFF.md if the
               repo opted in; forget what was shown (startup, clear and compact all
               start from a clean slate, like nested CLAUDE.md).
tool:          after Read/Edit/Write on a file, show the headings of every PITFALLS.md
               from that file's folder up to the repo root that weren't shown yet.

Silent unless the repo has .claude/rules/memory.md (the opt-in). Never blocks a tool.
"""
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

HEADER = "Pitfalls in scope (headings only; read the file when one is relevant):"
HANDOFF_BUDGET = 40  # lines loaded at session start; like auto memory's MEMORY.md cap
HANDOFF_NEAR = 32


def headings(f: Path):
    try:
        return [ln[3:].strip() for ln in f.read_text(encoding="utf-8", errors="replace").splitlines()
                if ln.startswith("## ")]
    except OSError:
        return []


def state_file(session: str) -> Path:
    key = hashlib.sha1(session.encode()).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / f"repo-memory-pitfalls-{key}.json"


def emit(event: str, lines):
    if lines:
        ctx = HEADER + "\n" + "\n".join(lines)
        json.dump({"hookSpecificOutput": {"hookEventName": event, "additionalContext": ctx}}, sys.stdout)


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "tool"
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()).resolve()
    if not (root / ".claude/rules/memory.md").is_file():
        return 0
    state = state_file(str(data.get("session_id", "default")))
    root_file = root / "PITFALLS.md"

    if mode == "session-start":
        seen = {f"PITFALLS.md\t{h}" for h in headings(root_file)}
        state.write_text(json.dumps(sorted(seen)))
        parts = []
        rule = (root / ".claude/rules/memory.md").read_text(encoding="utf-8", errors="replace")
        handoff = root / "HANDOFF.md"
        if "## HANDOFF.md" in rule and handoff.is_file():
            lines = handoff.read_text(encoding="utf-8", errors="replace").strip().splitlines()
            if lines:
                text = "\n".join(lines[:HANDOFF_BUDGET])
                note = ""
                if len(lines) > HANDOFF_BUDGET:
                    note = (f"\n[HANDOFF.md is {len(lines)} lines; only the first {HANDOFF_BUDGET} were loaded. "
                            "Rewrite it under the budget before other work: keep Now, Next, Open decisions, "
                            "Careful; drop what git log or tasks.md already hold.]")
                parts.append("Your HANDOFF.md (private; where your work stood at the end of the last session):\n"
                             + text + note)
        heads = [f'PITFALLS.md: "{h}"' for h in headings(root_file)]
        if heads:
            parts.append(HEADER + "\n" + "\n".join(heads))
        if parts:
            json.dump({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                              "additionalContext": "\n\n".join(parts)}}, sys.stdout)
        return 0

    path = (data.get("tool_input") or {}).get("file_path") or (data.get("tool_input") or {}).get("notebook_path")
    if not path:
        return 0
    p = Path(path)
    p = (root / p if not p.is_absolute() else p).resolve()
    if p == (root / "HANDOFF.md").resolve() and data.get("tool_name") in ("Write", "Edit", "MultiEdit"):
        try:
            n = len(p.read_text(encoding="utf-8", errors="replace").strip().splitlines())
        except OSError:
            n = 0
        if n > HANDOFF_BUDGET:
            msg = (f"HANDOFF.md is now {n} lines, over its {HANDOFF_BUDGET}-line budget: the next session "
                   f"only sees the first {HANDOFF_BUDGET}. Rewrite it shorter now (replace, don't append; "
                   "drop what git log or tasks.md hold; move lessons to PITFALLS.md).")
        elif n >= HANDOFF_NEAR:
            msg = f"HANDOFF.md is {n} of {HANDOFF_BUDGET} lines. Keep it a snapshot: tighten it on the next rewrite."
        else:
            msg = ""
        if msg:
            json.dump({"hookSpecificOutput": {"hookEventName": data.get("hook_event_name", "PostToolUse"),
                                              "additionalContext": msg}}, sys.stdout)
        return 0
    try:
        p.relative_to(root)
    except ValueError:
        return 0  # outside the repo
    seen = set(json.loads(state.read_text())) if state.exists() else set()
    lines, d = [], (p if p.is_dir() else p.parent)
    chain = []
    while True:
        chain.append(d / "PITFALLS.md")
        if d == root or d.parent == d:
            break
        d = d.parent
    for f in reversed(chain):  # outermost first
        if not f.is_file():
            continue
        rel = f.relative_to(root).as_posix()
        for h in headings(f):
            key = f"{rel}\t{h}"
            if key not in seen:
                seen.add(key)
                lines.append(f'{rel}: "{h}"')
    if lines:
        state.write_text(json.dumps(sorted(seen)))
        emit(data.get("hook_event_name", "PostToolUse"), lines)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:  # a memory hint must never break a tool call
        sys.exit(0)
