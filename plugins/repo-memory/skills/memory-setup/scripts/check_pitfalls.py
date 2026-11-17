#!/usr/bin/env python3
"""Check every PITFALLS.md in a repo for entries that won't be found or can't be used.

Usage: python check_pitfalls.py [repo_root]

Errors: a heading over 15 words; an entry with no cause or no fix; the same heading in
two files. Warnings: vague headings ("bug", "issue", "careful", "note"); headings with
"and" (probably two traps); long entries. Exit 1 on errors.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

MAX_WORDS = 15
MAX_BODY_LINES = 12
VAGUE = re.compile(r"\b(bug|issue|problem|careful|note|important|gotcha|misc|todo)\b", re.I)
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}


def entries(f: Path):
    out, cur = [], None
    for i, ln in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if ln.startswith("## "):
            cur = {"heading": ln[3:].strip(), "line": i, "body": []}
            out.append(cur)
        elif cur is not None and not ln.startswith("# "):
            cur["body"].append(ln)
    return out


def main(root: Path) -> int:
    files = [p for p in root.rglob("PITFALLS.md") if not SKIP_DIRS & set(p.relative_to(root).parts)]
    seen = defaultdict(list)
    errors = warns = 0
    for f in sorted(files):
        rel = f.relative_to(root).as_posix()
        for e in entries(f):
            h, body = e["heading"], "\n".join(e["body"])
            where = f"{rel}:{e['line']}"
            seen[h.lower()].append(where)
            if len(h.split()) > MAX_WORDS:
                print(f"ERROR {where}: heading over {MAX_WORDS} words; name the trigger, short")
                errors += 1
            if not re.search(r"\bcause\b", body, re.I):
                print(f"ERROR {where}: no cause")
                errors += 1
            if not re.search(r"\b(fix|guarded by)\b", body, re.I):
                print(f"ERROR {where}: no fix (or 'Guarded by')")
                errors += 1
            if VAGUE.search(h):
                print(f"WARN  {where}: vague word in heading: {VAGUE.search(h).group(0)!r}")
                warns += 1
            if re.search(r"\band\b", h, re.I):
                print(f"WARN  {where}: 'and' in heading; is this two pitfalls?")
                warns += 1
            if len([b for b in e["body"] if b.strip()]) > MAX_BODY_LINES:
                print(f"WARN  {where}: long entry; move detail to a linked doc")
                warns += 1
    for where in seen.values():
        if len(where) > 1:
            print(f"ERROR same heading in {len(where)} places: {', '.join(where)}; keep one")
            errors += 1
    total = sum(len(v) for v in seen.values())
    print(f"\n{len(files)} PITFALLS.md files, {total} entries, {errors} errors, {warns} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()))
