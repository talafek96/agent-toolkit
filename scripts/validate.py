#!/usr/bin/env python3
"""Validate the marketplace: manifests parse, every plugin source exists and has a
plugin.json whose name matches, and every SKILL.md has name + description frontmatter
matching its folder. Exit 1 on any problem."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []

market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
for key in ("name", "owner", "plugins"):
    if key not in market:
        errors.append(f"marketplace.json: missing '{key}'")
for p in market.get("plugins", []):
    src = (ROOT / p["source"]).resolve()
    pj = src / ".claude-plugin/plugin.json"
    if not pj.is_file():
        errors.append(f"{p['name']}: no plugin.json at {pj.relative_to(ROOT)}")
        continue
    meta = json.loads(pj.read_text())
    if meta.get("name") != p["name"]:
        errors.append(f"{p['name']}: plugin.json name is {meta.get('name')!r}")
    skills = list(src.glob("skills/*/SKILL.md"))
    if not skills:
        errors.append(f"{p['name']}: no skills/*/SKILL.md")
    for s in skills:
        m = re.match(r"^---\n(.*?)\n---\n", s.read_text(), re.S)
        if not m:
            errors.append(f"{s.relative_to(ROOT)}: no frontmatter")
            continue
        fm = m.group(1)
        name = re.search(r"^name:\s*(\S+)", fm, re.M)
        if not name or name.group(1) != s.parent.name:
            errors.append(f"{s.relative_to(ROOT)}: name must match folder '{s.parent.name}'")
        if not re.search(r"^description:", fm, re.M):
            errors.append(f"{s.relative_to(ROOT)}: missing description")

for e in errors:
    print("ERROR:", e)
print(f"{len(market.get('plugins', []))} plugins checked, {len(errors)} errors")
sys.exit(1 if errors else 0)
