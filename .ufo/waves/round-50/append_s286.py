#!/usr/bin/env python3
"""Append the validated S286 row to the live lane registry.

The row is taken byte-exact from the pre-append mirror that the census validated
(`--file`, exit 0), so the live row and the validated row cannot drift. The live
registry is append-only: the row is inserted after the last registry row and no
existing cell is touched. Usage: append_s286.py <lane-root>
"""
from __future__ import annotations

import sys

LANE = sys.argv[1] if len(sys.argv) > 1 else "/home/vgpnk/Projects/shokunin/kake-shokunin"
MIRROR = f"{LANE}/.ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md"
LIVE = f"{LANE}/corpus/SOURCES.md"
ROW_ID = "S286"


def main() -> int:
    mirror_lines = open(MIRROR, encoding="utf-8").read().splitlines()
    row = next((l for l in mirror_lines if l.startswith(f"| {ROW_ID} |")), None)
    if row is None:
        print("append_s286: mirror carries no S286 row")
        return 1
    live = open(LIVE, encoding="utf-8").read().splitlines()
    if any(l.startswith(f"| {ROW_ID} |") for l in live):
        print("append_s286: live registry already carries S286")
        return 1
    last = max(i for i, l in enumerate(live) if l.startswith("| S"))
    live.insert(last + 1, row)
    with open(LIVE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(live) + "\n")
    print(f"append_s286: inserted {ROW_ID} after line {last + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
