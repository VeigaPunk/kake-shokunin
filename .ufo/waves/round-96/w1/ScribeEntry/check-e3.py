#!/usr/bin/env python3
"""Simulate the C1 counter's E3 knowledge-entry audit on the round-96 draft.

Seat ScribeEntry, kake round 96 (hyaku run 15, attempt 1).

The frozen counter `.ufo/waves/round-96/c96_selfassess.py` audits each
`corpus/knowledge/*.md` (E3, lines ~348-374): the provenance trio must be present
and non-empty within the first 8 lines, exactly ONE `source:` line may appear there,
every `S###` id named in that line must resolve to a row id in `corpus/SOURCES.md`,
and the line must carry a citable locator (a URL or a path) that is not under /tmp.

This script re-implements that audit read-only, against:
  * the draft entry `knowledge-entry.md`, and
  * a prospective `corpus/SOURCES.md` = the lane's file with the finalized S480 row
    inserted after S479 (the row the L1 will land), so the id-resolution branch is
    measured as it will be after the round's integration, and also against the
    lane's CURRENT SOURCES.md (where S480 does not exist yet), so the landing-order
    dependency is shown rather than asserted.

Run:  python3 -B check-e3.py        (exit 0 iff the prospective state has no E3 finding)
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
DRAFT = os.path.join(HERE, "knowledge-entry.md")
SOURCES = os.path.join(LANE, "corpus/SOURCES.md")
ROWFILE = os.path.join(HERE, "s480-row.md")

ID_RE = re.compile(r"S\d{3,}")
ROW_ID_RE = re.compile(r"^\|[ \t]*(S[0-9]{3,})[ \t]*\|")
LOCATOR_RE = re.compile(
    r"https?://|~/|[A-Za-z0-9._/~\-]+\.(?:md|py|mjs|json|txt|html|yml|yaml)\b")
TMP_LOCATOR_RE = re.compile(r"(?:^|[\s`\"'])/(?:var/)?tmp/")


def extract_row():
    text = open(ROWFILE, encoding="utf-8").read()
    for b in text.split("```"):
        b = b.strip("\n")
        if b.startswith("| S480 |"):
            return b
    raise SystemExit("no S480 row block found")


def e3(text, row_ids):
    """Re-implementation of the counter's E3 knowledge-entry audit."""
    head = "\n".join(text.splitlines()[:8])
    problems = []
    for key in ("source", "verified-at", "recheck"):
        if not re.search(r"(?m)^" + key + r":\s*\S", head):
            problems.append("missing %s:" % key)
    source_lines = re.findall(r"(?m)^source:.*$", head)
    if len(source_lines) > 1:
        problems.append("multiple source: lines (%d)" % len(source_lines))
    for line in source_lines[:2]:
        ids_here = set(ID_RE.findall(line))
        unresolved = sorted(i for i in ids_here if i not in row_ids)
        if unresolved:
            problems.append("unresolved row id " + ", ".join(unresolved))
        elif not ids_here:
            if TMP_LOCATOR_RE.search(line):
                problems.append("non-citable locator: /tmp is never evidence")
            elif not LOCATOR_RE.search(line):
                problems.append("vacuous source: no row id, URL or path locator")
    return problems


def row_ids_of(sources_text):
    ids = set()
    for line in sources_text.splitlines():
        m = ROW_ID_RE.match(line)
        if m:
            ids.add(m.group(1))
    return ids


def main():
    draft = open(DRAFT, encoding="utf-8").read()
    sources = open(SOURCES, encoding="utf-8").read()
    row = extract_row()

    current_ids = row_ids_of(sources)
    prospective_text = sources
    lines = prospective_text.splitlines(True)
    idx = next(i for i, l in enumerate(lines) if l.startswith("| S479 "))
    lines.insert(idx + 1, row + "\n")
    prospective_text = "".join(lines)
    prospective_ids = row_ids_of(prospective_text)

    print("S480 in the lane's current SOURCES.md: %s"
          % ("yes" if "S480" in current_ids else "no (the row is not landed yet)"))
    print("S480 in the prospective SOURCES.md:    %s"
          % ("yes" if "S480" in prospective_ids else "no"))

    cur = e3(draft, current_ids)
    print("\nE3 against the CURRENT SOURCES.md (S480 not yet landed):")
    print("  problems: %s" % (cur or "none"))
    pro = e3(draft, prospective_ids)
    print("E3 against the PROSPECTIVE SOURCES.md (S480 landed):")
    print("  problems: %s" % (pro or "none"))
    print("head lines 1-5 of the draft:")
    for i, l in enumerate(draft.splitlines()[:5], 1):
        print("  %d %s" % (i, l))
    print("source: lines in the first 8 lines: %d"
          % len(re.findall(r"(?m)^source:.*$", "\n".join(draft.splitlines()[:8]))))
    if pro:
        print("VIOLATION the prospective state still has E3 findings")
        return 1
    print("violations=0 (prospective E3 clean)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
