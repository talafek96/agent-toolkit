#!/usr/bin/env python3
"""repo-memory hooks: hierarchical PITFALLS.md, headings only.

session-start: show the root PITFALLS.md headings; forget what was shown (startup,
               clear and compact all start from a clean slate, like nested CLAUDE.md).
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
        emit("SessionStart", [f'PITFALLS.md: "{h}"' for h in headings(root_file)])
        return 0

    path = (data.get("tool_input") or {}).get("file_path") or (data.get("tool_input") or {}).get("notebook_path")
    if not path:
        return 0
    p = Path(path)
    p = (root / p if not p.is_absolute() else p).resolve()
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
