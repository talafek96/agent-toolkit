#!/usr/bin/env python3
"""Check the statusline plugin: the script renders a sample payload, and the installer
sets exactly `uv run --script <copy>` with refreshInterval 5, verifies it renders,
is idempotent, upgrades its own older command, refuses to replace someone else's
statusLine, replaces with backups on --replace, keeps every other settings key, and
stops when uv is missing. Exit 1 on any failure."""
import json
import os
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


def run(*args, stdin=None, path="", home="/nonexistent"):
    return subprocess.run([sys.executable, *map(str, args)], input=stdin, capture_output=True,
                          text=True, env={"PATH": path, "HOME": home, "NO_COLOR": "1"})


payload = (ROOT / "tests/fixtures/statusline/payload.json").read_text()
r = run(SCRIPTS / "statusline.py", stdin=payload)
out = r.stdout
check(r.returncode == 0, "statusline.py exits 0 on a sample payload")
for part in ("Opus", "62K/200K (31%)", "5h: 40%", "edits +120/−8", "uptime 12m"):
    check(part in out, f"output shows {part!r}")
check(run(SCRIPTS / "statusline.py", stdin="not json").returncode == 1, "invalid JSON exits 1")

with tempfile.TemporaryDirectory() as d:
    # A stand-in uv: `uv run --script X` -> python X.
    fakebin = Path(d) / "bin"
    fakebin.mkdir()
    (fakebin / "uv").write_text(f'#!/bin/sh\nshift 2\nexec "{sys.executable}" "$@"\n')
    (fakebin / "uv").chmod(0o755)
    PATH = f"{fakebin}{os.pathsep}/usr/bin{os.pathsep}/bin"
    settings = Path(d) / "settings.json"
    settings.write_text(json.dumps({"model": "opus", "permissions": {"allow": ["Bash(ls)"]}}))
    inst = SCRIPTS / "install.py"
    copy = Path(d) / "statusline.py"

    def install(*args, path=PATH):
        return run(inst, "--settings", *args, path=path)

    r = install(settings, "--dry-run")
    check(r.returncode == 0 and "would" in r.stdout, "dry run plans changes")
    check(not copy.exists(), "dry run writes nothing")

    r = install(settings)
    s = json.loads(settings.read_text())
    check(r.returncode == 0 and "Verified" in r.stdout, "install exits 0 and verifies it renders")
    check(copy.read_bytes() == (SCRIPTS / "statusline.py").read_bytes(), "script copied next to settings")
    check(s.get("statusLine") == {"type": "command", "command": f"uv run --script {copy}",
                                  "refreshInterval": 5},
          "statusLine is exactly `uv run --script <copy>`, refreshInterval 5")
    check(s.get("model") == "opus" and s.get("permissions") == {"allow": ["Bash(ls)"]},
          "other settings kept")

    r = install(settings)
    check(r.returncode == 0 and "up to date" in r.stdout, "second run changes nothing")

    s["statusLine"] = {"type": "command", "command": f'python3 "{copy}"'}
    settings.write_text(json.dumps(s))
    r = install(settings)
    check(r.returncode == 0 and json.loads(settings.read_text())["statusLine"]["command"].startswith("uv run --script"),
          "its own older python3 command is upgraded to uv without asking")

    s["statusLine"] = {"type": "command", "command": "echo mine"}
    settings.write_text(json.dumps(s))
    r = install(settings)
    check(r.returncode == 2, "someone else's statusLine: exits 2")
    check(json.loads(settings.read_text())["statusLine"]["command"] == "echo mine",
          "someone else's statusLine: left untouched")

    r = install(settings, "--replace")
    check(r.returncode == 0 and "echo mine" in (Path(d) / "settings.json.bak").read_text(),
          "--replace replaces and backs up the old settings")

    fresh = Path(d) / "new" / "settings.json"
    r = install(fresh)
    check(r.returncode == 0 and "statusLine" in json.loads(fresh.read_text()),
          "creates a settings file that doesn't exist yet")

    broken = Path(d) / "broken"
    broken.mkdir()
    (broken / "uv").write_text("#!/bin/sh\nexit 1\n")
    (broken / "uv").chmod(0o755)
    r = install(Path(d) / "b" / "settings.json", path=f"{broken}{os.pathsep}/usr/bin{os.pathsep}/bin")
    check(r.returncode == 4, "a command that doesn't render: exits 4")

    nouv = Path(d) / "n" / "settings.json"
    r = install(nouv, path=f"/usr/bin{os.pathsep}/bin")
    if r.returncode != 3 and any(Path(p).is_file() for p in ("/opt/homebrew/bin/uv", "/usr/local/bin/uv", "/usr/bin/uv")):
        print("skip uv-missing check: a system uv exists here")
    else:
        check(r.returncode == 3 and not nouv.exists(), "uv missing: exits 3, writes nothing")

print(f"\n{len(fails)} failures")
sys.exit(1 if fails else 0)
