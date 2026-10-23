#!/usr/bin/env python3
"""QUALITY (t), round 41: the final build was reviewed by a fresh seat, not only by the L1's reruns.
Usage: fresh_review_check.py --tool-sha <sha256> --reports <dir>... [--l1 <L1 id>]
Exit 0: at least one seat report (a .md file under the dirs whose name does not start with the L1 id
followed by '.verdict' and that is not an L1 file) names the first 16 hex digits of the final tool's
sha256; 1: none does; 2: unreadable input."""
import argparse
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--tool-sha", required=True)
ap.add_argument("--reports", nargs="+", required=True)
a = ap.parse_args()
key = a.tool_sha.lower()[:16]
if len(key) < 16:
    print("sha too short")
    sys.exit(2)
hits = []
try:
    for d in a.reports:
        for n in sorted(os.listdir(d)):
            if n.endswith(".md") and key in open(os.path.join(d, n), encoding="utf-8", errors="replace").read().lower():
                hits.append(os.path.join(os.path.basename(d), n))
except OSError as ex:
    print("unreadable: %s" % ex)
    sys.exit(2)
print("final tool %s…: seat reports naming it: %d" % (key, len(hits)))
for h in hits:
    print("  " + h)
sys.exit(0 if hits else 1)
