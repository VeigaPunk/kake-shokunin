#!/usr/bin/env python3
"""QUALITY (t), round 41: the final build was reviewed by a fresh seat, not only by the L1's reruns.
Usage: fresh_review_check.py --tool-sha <sha256> --reports <dir>... [--exclude-prefix <name prefix>]...
Exit 0: at least one report (a .md file under the dirs whose name starts with no excluded prefix, e.g.
the L1's own files) names the first 16 hex digits of the final tool's sha256; 1: none does; 2: unreadable
input. Weakness (wave-2 `ReviewLessonDraftCheck`): a report that only quotes the sha, or a rerun rather
than a review, passes; read the report too."""
import argparse
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--tool-sha", required=True)
ap.add_argument("--reports", nargs="+", required=True)
ap.add_argument("--exclude-prefix", action="append", default=[])
a = ap.parse_args()
key = a.tool_sha.lower()[:16]
if len(key) < 16:
    print("sha too short")
    sys.exit(2)
hits = []
try:
    for d in a.reports:
        for n in sorted(os.listdir(d)):
            if not n.endswith(".md") or any(n.startswith(x) for x in a.exclude_prefix):
                continue
            if key in open(os.path.join(d, n), encoding="utf-8", errors="replace").read().lower():
                hits.append(os.path.join(os.path.basename(d), n))
except OSError as ex:
    print("unreadable: %s" % ex)
    sys.exit(2)
print("final tool %s…: seat reports naming it: %d" % (key, len(hits)))
for h in hits:
    print("  " + h)
sys.exit(0 if hits else 1)
