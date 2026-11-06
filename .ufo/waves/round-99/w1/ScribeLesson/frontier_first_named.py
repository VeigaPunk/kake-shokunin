#!/usr/bin/env python3
"""Draft checker for QUALITY criterion R99-A (open-frontier first-named map).

Reads two committed lane files and decides one predicate:

  Every ground a `Planned -- after round N` section of `SCORECARD.md` names as
  still open is carried in `corpus/README.md`'s open-frontier map, with the round
  in which that ground was FIRST named open.

  met=true  when every named-open ground has a map row whose "first named"
             round is <= the round that named it open (a map may name it
             earlier; it may not name it later).
  met=false when a named-open ground has no map row, or its row names a first
             round later than the round that named it open.

A "ground" is an RFC section id, written either `§4.3.4` or `RFC 9111 4.3.4`
in the map row; both spellings canonicalise to the key `4.3.4`.

Usage:
  python3 -B frontier_first_named.py --root <lane dir> [--revision <commit>]
                                       [--json]

Everything is read from committed bytes: `git show <rev>:<path>` when
--revision is given, the working tree otherwise. Nothing is written.
"""
import argparse
import json
import os
import re
import subprocess
import sys

PLANNED = re.compile(r"(?m)^#{2,4}[^\n]*Planned\b[^\n]*?\bround[ -](\d+)")
OPEN_CLAUSE = re.compile(r"(?i)\bfrontier\b[^\n]*")
# An RFC section id: `§4.3.4` or `RFC 9111 4.3.4` (the RFC number is ignored).
GROUND = re.compile(r"§\s*(\d+(?:\.\d+)*)|RFC\s+\d+\s+(\d+(?:\.\d+)*)")
MAP_HEAD = re.compile(r"(?m)^##\s+Open frontier\b[^\n]*$")
MAP_ROW = re.compile(r"(?m)^\|\s*([^|\n]*?)\s*\|([^|\n]*?)\|([^|\n]*?)\|")
ROUND_IN_CELL = re.compile(r"r(?:ound)?\s*(\d+)", re.I)


def read(root, rev, path):
    if rev:
        out = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)],
                             capture_output=True)
        if out.returncode != 0:
            raise SystemExit("git show %s:%s failed: %s" % (
                rev, path, out.stderr.decode("utf-8", "replace").strip()))
        return out.stdout.decode("utf-8", "replace")
    with open(os.path.join(root, path), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def grounds_in(text):
    """Canonical section ids mentioned in a text, in order, de-duplicated."""
    out = []
    for a, b in GROUND.findall(text):
        gid = a or b
        if gid and gid not in out:
            out.append(gid)
    return out


def planned_sections(scorecard):
    """[(round, section_text)] for every `Planned -- after round N` section."""
    marks = [(m.start(), int(m.group(1))) for m in PLANNED.finditer(scorecard)]
    out = []
    for i, (pos, rnd) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(scorecard)
        out.append((rnd, scorecard[pos:end]))
    return out


def open_grounds(scorecard):
    """{ground_id: first round that named it open} over Planned sections."""
    first = {}
    for rnd, text in planned_sections(scorecard):
        for clause in OPEN_CLAUSE.findall(text):
            if not re.search(r"(?i)\bopen\b|\bremain", clause):
                continue
            for gid in grounds_in(clause):
                first.setdefault(gid, rnd)
    return first


def map_rows(readme):
    """{ground_id: first-named round} from the `## Open frontier` table, or None."""
    m = MAP_HEAD.search(readme)
    if not m:
        return None
    rows = {}
    for row in MAP_ROW.finditer(readme[m.end():]):
        cells = [c.strip() for c in row.groups()]
        if not cells[0] or set(cells[0]) <= set("-: "):
            continue
        hit = ROUND_IN_CELL.search(cells[2])
        if not hit:
            continue
        for gid in grounds_in(cells[0]):
            rows.setdefault(gid, int(hit.group(1)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        scorecard = read(a.root, a.revision, "SCORECARD.md")
        readme = read(a.root, a.revision, "corpus/README.md")
    except SystemExit as exc:
        print(str(exc), file=sys.stderr)
        return 2
    named = open_grounds(scorecard)
    rows = map_rows(readme)
    missing, wrong = [], []
    if rows is None:
        missing = sorted(named)
        detail = "corpus/README.md has no `## Open frontier` section"
    else:
        for gid, rnd in sorted(named.items(), key=lambda kv: kv[1]):
            if gid not in rows:
                missing.append(gid)
            elif rows[gid] > rnd:
                wrong.append((gid, rows[gid], rnd))
        detail = "map rows: %d" % len(rows)
    met = not missing and not wrong
    if a.json:
        print(json.dumps({"named_open": named, "map_rows": rows,
                          "missing": missing, "wrong": wrong,
                          "met": met}, indent=1, sort_keys=True))
    else:
        print("named_open=%d map_rows=%s missing=%d wrong=%d met=%s"
              % (len(named), "absent" if rows is None else len(rows),
                 len(missing), len(wrong), str(met).lower()))
        for gid in missing:
            print("missing_open_ground %s (named open in round %d)" % (gid, named[gid]))
        for gid, got, want in wrong:
            print("wrong_first_named %s map_says_r%d first_named_r%d" % (gid, got, want))
        print(detail)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
