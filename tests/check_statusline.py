#!/usr/bin/env python3
"""Check the statusline plugin: the script renders a sample payload, and the installer
creates, is idempotent, refuses to replace a different statusLine, replaces with
backups on --replace, and keeps every other settings key. Exit 1 on any failure."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "plugins/statusline/scripts"
fails = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        fails.append(what)


def run(*args, stdin=None):
    return subprocess.run([sys.executable, *map(str, args)], input=stdin,
                          capture_output=True, text=True, env={"PATH": "", "NO_COLOR": "1"})


payload = (ROOT / "tests/fixtures/statusline/payload.json").read_text()
r = run(SCRIPTS / "statusline.py", stdin=payload)
out = r.stdout
check(r.returncode == 0, "statusline.py exits 0 on a sample payload")
for part in ("Opus", "62K/200K (31%)", "5h: 40%", "edits +120/−8", "uptime 12m"):
    check(part in out, f"output shows {part!r}")
check(run(SCRIPTS / "statusline.py", stdin="not json").returncode == 1, "invalid JSON exits 1")

with tempfile.TemporaryDirectory() as d:
    settings = Path(d) / "settings.json"
    settings.write_text(json.dumps({"model": "opus", "permissions": {"allow": ["Bash(ls)"]}}))
    inst = SCRIPTS / "install.py"

    r = run(inst, "--settings", settings, "--dry-run")
    check(r.returncode == 0 and "would" in r.stdout, "dry run plans changes")
    check(not (Path(d) / "statusline.py").exists(), "dry run writes nothing")

    r = run(inst, "--settings", settings)
    s = json.loads(settings.read_text())
    check(r.returncode == 0, "install exits 0")
    check((Path(d) / "statusline.py").read_bytes() == (SCRIPTS / "statusline.py").read_bytes(),
          "script copied next to settings")
    check(str(Path(d) / "statusline.py") in s.get("statusLine", {}).get("command", ""),
          "statusLine points at the copy, not the plugin folder")
    check(s.get("model") == "opus" and s.get("permissions") == {"allow": ["Bash(ls)"]},
          "other settings kept")

    r = run(inst, "--settings", settings)
    check(r.returncode == 0 and "nothing to do" in r.stdout, "second run is a no-op")

    s["statusLine"] = {"type": "command", "command": "echo mine"}
    settings.write_text(json.dumps(s))
    r = run(inst, "--settings", settings)
    check(r.returncode == 2, "different statusLine: exits 2")
    check(json.loads(settings.read_text())["statusLine"]["command"] == "echo mine",
          "different statusLine: left untouched")

    r = run(inst, "--settings", settings, "--replace")
    check(r.returncode == 0 and "echo mine" in (Path(d) / "settings.json.bak").read_text(),
          "--replace replaces and backs up the old settings")

    fresh = Path(d) / "new" / "settings.json"
    r = run(inst, "--settings", fresh)
    check(r.returncode == 0 and "statusLine" in json.loads(fresh.read_text()),
          "creates a settings file that doesn't exist yet")

print(f"\n{len(fails)} failures")
sys.exit(1 if fails else 0)
