#!/usr/bin/env python3
"""Install the status line: copy statusline.py next to the settings file and point
the settings' ``statusLine`` at the copy (never at the plugin folder, whose path
changes on every plugin update). The setting is always the same shape:

  {"type": "command", "command": "uv run --script <dir>/statusline.py", "refreshInterval": 5}

Usage:
  python install.py [--settings PATH] [--dry-run] [--replace]

--settings  settings file to change (default ~/.claude/settings.json)
--dry-run   print what would change; write nothing
--replace   allow replacing a different statusLine that is already set

Exit 0: installed and verified (or would install). Exit 2: a different statusLine is
set and --replace was not given; nothing written. Exit 3: uv not found; nothing
written. Exit 4: installed, but the command didn't render in a shell. Every other key
in the settings file is kept. A changed script or settings file is backed up as *.bak.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "statusline.py"
REFRESH_SECONDS = 5  # redraw while idle, so task and git counts stay current
UV_PLACES = ("~/.local/bin/uv", "~/.cargo/bin/uv", "/opt/homebrew/bin/uv", "/usr/local/bin/uv")
SAMPLE = json.dumps({"model": {"display_name": "check"}, "context_window": {"used_percentage": 1}})


def find_uv() -> str | None:
    """'uv' if the shell finds it by name; else an absolute path to it; else None."""
    if shutil.which("uv"):
        return "uv"
    for p in UV_PLACES:
        full = Path(p).expanduser()
        if full.is_file() and os.access(full, os.X_OK):
            return str(full)
    return None


def quote(path: Path) -> str:
    s = str(path)
    return f'"{s}"' if any(c in s for c in " '\"$`\\") else s


def renders(command: str) -> tuple[bool, str]:
    """Run the command the way Claude Code does (through a shell, JSON on stdin)."""
    try:
        r = subprocess.run(command, shell=True, input=SAMPLE, capture_output=True,
                           text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return False, "timed out"
    ok = r.returncode == 0 and "check" in r.stdout
    return ok, (r.stdout + r.stderr).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--settings", type=Path, default=Path.home() / ".claude" / "settings.json")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--replace", action="store_true")
    a = ap.parse_args()

    uv = find_uv()
    if uv is None:
        print("uv not found. This status line runs with uv. Install it, then run setup again:")
        print("  curl -LsSf https://astral.sh/uv/install.sh | sh     (or: brew install uv)")
        return 3

    settings_path = a.settings.expanduser()
    target = settings_path.parent / "statusline.py"
    settings = {}
    if settings_path.is_file():
        text = settings_path.read_text(encoding="utf-8")
        settings = json.loads(text) if text.strip() else {}
        if not isinstance(settings, dict):
            print(f"ERROR {settings_path} is not a JSON object; not touching it")
            return 1

    wanted = {"type": "command", "command": f"{uv} run --script {quote(target)}",
              "refreshInterval": REFRESH_SECONDS}
    current = settings.get("statusLine")
    # A status line that already runs our copy is ours: bring it to the exact shape
    # without asking. Anyone else's needs --replace.
    ours = isinstance(current, dict) and str(target) in str(current.get("command", ""))
    set_it = current != wanted
    if current is not None and set_it and not ours and not a.replace:
        print(f"A different statusLine is already set in {settings_path}:")
        print(json.dumps(current, indent=2))
        print("Nothing written. Re-run with --replace to replace it (the old file is backed up).")
        return 2

    script_same = target.is_file() and target.read_bytes() == SOURCE.read_bytes()
    plan = []
    if not script_same:
        plan.append(f"{'replace' if target.exists() else 'create'} {target}"
                    + (f" (backup {target}.bak)" if target.exists() else ""))
    if set_it:
        plan.append(f"set statusLine in {settings_path}: {json.dumps(wanted)}"
                    + (f" (backup {settings_path}.bak)" if settings_path.exists() else ""))
    for step in plan:
        print(("would " if a.dry_run else "") + step)
    if a.dry_run:
        if not plan:
            print("Already installed and up to date; nothing to do.")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    if not script_same:
        if target.exists():
            shutil.copy2(target, target.with_name(target.name + ".bak"))
        shutil.copyfile(SOURCE, target)
    if set_it:
        if settings_path.exists():
            shutil.copy2(settings_path, settings_path.with_name(settings_path.name + ".bak"))
        settings["statusLine"] = wanted
        settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    ok, out = renders(wanted["command"])
    if not ok:
        print(f"Installed, but the command did not render: {wanted['command']}")
        print(out[-800:] or "(no output)")
        return 4
    print("Verified: the command renders. " + ("Done." if plan else "Already installed and up to date."))
    print("Claude Code reloads settings on its own; the status line appears on the next redraw.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
