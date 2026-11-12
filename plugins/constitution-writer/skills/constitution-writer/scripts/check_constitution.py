#!/usr/bin/env python3
"""Mechanical checks for a project constitution.

Usage: python check_constitution.py <path/to/constitution.md>

Checks what a script can check; judgment (is the why real? does it pass the
boundary test?) stays with the reader. Exit code 1 if any ERROR was found.
"""
import re
import sys
from pathlib import Path

MAX_LINES = 250
MAX_PRINCIPLES = 12
MAX_NON_NEGOTIABLE = 2


def main(path: str) -> int:
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    findings = []

    def add(level, msg):
        findings.append((level, msg))

    if len(lines) > MAX_LINES:
        add("WARN", f"{len(lines)} lines (aim for under {MAX_LINES}): it is loaded every session")

    for m in re.finditer(r"\[ASK:[^\]]*\]|\(proposed\)|\bTODO\b|\bTBD\b", text, re.I):
        add("ERROR", f"open-question marker in the file: {m.group(0)[:40]!r}; questions belong in the response, the file reads as finished")
    for m in re.finditer(r"\[[A-Z][A-Z0-9_]{2,}\]", text):
        add("ERROR", f"template placeholder left in: {m.group(0)}")

    if re.search(r"sync impact report|^\s*version:\s*\d+\.\d+\.\d+\s*(→|->)", text, re.I | re.M):
        add("WARN", "embedded change log / sync-impact report: git already keeps history, and this costs tokens every session")
    if len(re.findall(r"^Previous\s+[—-]", text, re.M)) > 0:
        add("WARN", "version history entries inside the file")

    # principles = level-3 headings under a 'Principles' level-2 section, or roman-numbered h3s
    principles = []
    section = None
    cur = None
    for i, line in enumerate(lines):
        if line.startswith("## "):
            section = line[3:].strip().lower()
            cur = None
            continue
        if line.startswith("### ") and (section and "principle" in section or re.match(r"###\s+[IVXLC]+\.", line)):
            cur = {"title": line[4:].strip(), "line": i + 1, "body": []}
            principles.append(cur)
            continue
        if cur is not None:
            cur["body"].append(line)

    if not principles:
        add("ERROR", "no principles found (expected '### I. Name' headings under a '## Core Principles' section)")
    if len(principles) > MAX_PRINCIPLES:
        add("WARN", f"{len(principles)} principles (usually 6-10); merge or move some to rules files")

    nn = [p for p in principles if "NON-NEGOTIABLE" in p["title"].upper()]
    if len(nn) > MAX_NON_NEGOTIABLE:
        add("WARN", f"{len(nn)} principles marked NON-NEGOTIABLE: if everything is, nothing is")

    for p in principles:
        body = "\n".join(p["body"])
        has_why = re.search(r"\bwhy\b\s*[:\-—]", body, re.I)
        has_inline_reason = re.search(r" — |\bbecause\b|\bso that\b|\botherwise\b|\bwhich (?:lets|means|keeps)\b", body, re.I)
        if not body.strip() or not re.search(r"\S", body):
            add("ERROR", f"line {p['line']}: '{p['title']}' is empty")
        elif not has_why and not has_inline_reason:
            add("WARN", f"line {p['line']}: '{p['title']}' gives no reason (no 'Why:' line and none inline); a rule without its why gets followed literally")

        bullets = [ln for ln in p["body"] if re.match(r"\s*[-*]\s", ln) and not re.search(r"why\s*:", ln, re.I)]
        specific = [ln for ln in bullets if not re.search(r"mechanics\s*:", ln, re.I)
                    and (re.search(r"`[^`]*[/.][^`]*`", ln) or re.search(r"\b\d+(\.\d+)?\s*(%|ms|s|days?|hours?|lines?)\b", ln))]
        if specific:
            add("INFO", f"line {p['line']}: '{p['title']}' names a file, path or number; fine as an example, but the principle itself must hold for other projects too")
        if len(bullets) > 7:
            add("WARN", f"line {p['line']}: '{p['title']}' has {len(bullets)} rule bullets; mechanics belong in a rules file or folder CLAUDE.md")

    vague = re.findall(r"\b(appropriate(?:ly)?|as needed|where possible|strive to|best practices?|high[- ]quality)\b", text, re.I)
    if vague:
        add("WARN", f"vague words nobody can check: {', '.join(sorted(set(v.lower() for v in vague)))}")

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for level, msg in sorted(findings, key=lambda f: order[f[0]]):
        print(f"{level}: {msg}")
    print(f"\n{len(principles)} principles, {len(lines)} lines, "
          f"{sum(1 for f in findings if f[0] == 'ERROR')} errors, {sum(1 for f in findings if f[0] == 'WARN')} warnings")
    return 1 if any(f[0] == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
