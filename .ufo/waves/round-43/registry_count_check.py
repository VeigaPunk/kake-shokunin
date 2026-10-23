#!/usr/bin/env python3
"""Able-to-fail check for the round-42 registry-arithmetic mistake (closure routed defect 1).

A claims file names the registry counts a report or SCORECARD section states for a base and a
tip revision; this checker re-derives rows/mined/queued/rejected from the committed bytes at
those revisions with the CORPUS.md census commands and exits 0 only when every stated count
matches its re-derivation. Exit 1 names each mismatch.

Usage: python3 registry_count_check.py --root <lane> --claims <json>
claims = {"base_rev": "...", "tip_rev": "...",
          "base": {"rows": N, "mined": N, "queued": N, "rejected": N},
          "tip":  {"rows": N, "mined": N, "queued": N, "rejected": N},
          "deltas": {"mined": N, "queued": N, "rejected": N}}
"""
import argparse
import json
import subprocess
import sys


def census(root, rev):
    def run(*args):
        return subprocess.run(["git", "-C", root] + list(args), check=True,
                              capture_output=True, stdin=subprocess.DEVNULL).stdout

    text = run("show", "%s:corpus/SOURCES.md" % rev).decode("utf-8")
    rows = mined = queued = rejected = 0
    for line in text.splitlines():
        cells = [c.strip() for c in line.split("|")]
        if len(cells) == 13 and len(cells) > 2 and cells[1].startswith("S") and cells[1][1:].isdigit():
            rows += 1
            status = cells[8]
            if status == "mined":
                mined += 1
            elif status == "queued":
                queued += 1
            elif status == "rejected":
                rejected += 1
    return {"rows": rows, "mined": mined, "queued": queued, "rejected": rejected}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--claims", required=True)
    a = ap.parse_args()
    claims = json.load(open(a.claims))
    bad = []
    derived = {}
    for side in ("base", "tip"):
        rev = claims[side + "_rev"]
        derived[side] = census(a.root, rev)
        for key, stated in claims[side].items():
            if stated != derived[side][key]:
                bad.append("%s.%s: stated %s, re-derived %s" %
                           (side, key, stated, derived[side][key]))
    for key, stated in claims.get("deltas", {}).items():
        delta = derived["tip"][key] - derived["base"][key]
        if stated != delta:
            bad.append("deltas.%s: stated %s, re-derived %s" % (key, stated, delta))
    print(json.dumps({"ok": not bad, "derived": derived, "mismatches": bad}, indent=1))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
