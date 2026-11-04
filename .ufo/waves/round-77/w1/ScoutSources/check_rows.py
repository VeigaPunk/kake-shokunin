#!/usr/bin/env python3
"""Mechanical checks for the three drafted registry rows (round-77 ScoutSources).

* extracts the drafted S012/S447/S448 rows from the report's fenced block,
* asserts each row yields exactly the 11 registry columns and no escaped pipe,
* diffs the drafted S012 row against corpus/SOURCES.md's current S012 row cell by
  cell and prints which columns changed (expected: used-by only).

Prints `rows=<n> cells=<n> s012_changed=<names>`; exits 1 on any failure.
"""
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
REPORT = LANE / ".ufo/waves/round-77/w1/ScoutSources.md"
REGISTRY = LANE / "corpus/SOURCES.md"
COLS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
        "status", "opened", "recheck", "used-by"]
IDS = ["S012", "S447", "S448"]


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def registry_row(rows, rid):
    for line in rows:
        if line.startswith(f"| {rid} |"):
            return cells(line)
    return None


def main():
    report = REPORT.read_text(encoding="utf-8")
    drafted = {}
    for line in report.split("\n"):
        for rid in IDS:
            if line.startswith(f"| {rid} |"):
                drafted.setdefault(rid, line)
    failures = 0
    if sorted(drafted) != sorted(IDS):
        print(f"FAIL drafted rows found: {sorted(drafted)}")
        failures += 1
    registry_rows = REGISTRY.read_text(encoding="utf-8").split("\n")
    changed = []
    for rid in IDS:
        line = drafted.get(rid)
        if line is None:
            continue
        if "\\|" in line:
            print(f"FAIL {rid} contains an escaped pipe")
            failures += 1
        got = cells(line)
        if len(got) != len(COLS):
            print(f"FAIL {rid} cells={len(got)} want={len(COLS)}")
            failures += 1
            continue
        empty = [COLS[i] for i, c in enumerate(got) if c == ""]
        if empty:
            print(f"FAIL {rid} empty columns {empty}")
            failures += 1
        if rid == "S012":
            current = registry_row(registry_rows, rid)
            if current is None or len(current) != len(COLS):
                print("FAIL registry S012 row not found or malformed")
                failures += 1
                continue
            changed = [COLS[i] for i in range(len(COLS)) if current[i] != got[i]]
            print(f"S012 changed columns: {changed}")
            print(f"S012 old used-by: {current[10]}")
            print(f"S012 new used-by: {got[10]}")
        else:
            print(f"{rid} anchor cell: {got[5][:80]}…")
    print(f"rows={len(drafted)} cells={len(COLS)} s012_changed={','.join(changed)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
