#!/usr/bin/env python3
"""Install the status line: copy statusline.py next to the settings file and point
the settings' ``statusLine`` at the copy (never at the plugin folder, whose path
changes on every plugin update).

Usage:
  python install.py [--settings PATH] [--dry-run] [--replace]

--settings  settings file to change (default ~/.claude/settings.json)
--dry-run   print what would change; write nothing
--replace   allow replacing a different statusLine that is already set

Exit 0: installed (or would install). Exit 2: a different statusLine is set and
--replace was not given; nothing was written. Every other key in the settings file
is kept. A changed script or settings file is backed up as ``*.bak`` first.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "statusline.py"
REFRESH_SECONDS = 5  # redraw while idle, so task and git counts stay current


def command_for(target: Path) -> str:
    # uv runs the script in isolation from any nearby pyproject; plain python3 also works
    # (standard library only).
    if shutil.which("uv"):
        return f'uv run --script "{target}"'
    return f'python3 "{target}"'


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--settings", type=Path, default=Path.home() / ".claude" / "settings.json")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--replace", action="store_true")
    a = ap.parse_args()

    settings_path = a.settings.expanduser()
    target = settings_path.parent / "statusline.py"
    settings = {}
    if settings_path.is_file():
        text = settings_path.read_text(encoding="utf-8")
        settings = json.loads(text) if text.strip() else {}
        if not isinstance(settings, dict):
            print(f"ERROR {settings_path} is not a JSON object; not touching it")
            return 1

    wanted = {"type": "command", "command": command_for(target), "refreshInterval": REFRESH_SECONDS}
    current = settings.get("statusLine")
    # Already pointing at our copy (however the command is written): leave the setting alone.
    ours = isinstance(current, dict) and str(target) in str(current.get("command", ""))
    set_it = not ours
    if current is not None and set_it and not a.replace:
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
    if not plan:
        print("Already installed and up to date; nothing to do.")
        return 0
    for step in plan:
        print(("would " if a.dry_run else "") + step)
    if a.dry_run:
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
    print("Done. Claude Code reloads settings on its own; the status line appears on the next redraw.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
