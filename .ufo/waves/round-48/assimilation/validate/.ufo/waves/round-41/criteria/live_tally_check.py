#!/usr/bin/env python3
"""QUALITY (s), round 41: a control tally counts live seats only.
Usage: live_tally_check.py --dispatch-log <log>... --receipts <dir>
Exit 0: no receipt in <dir> belongs to a seat the dispatch logs record as DEAD; 1: some do (listed);
2: unreadable input. A receipt belongs to seat S when its file name starts with S followed by '-' or '__'."""
import argparse
import os
import re
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--dispatch-log", nargs="+", required=True)
ap.add_argument("--receipts", required=True)
a = ap.parse_args()
dead = set()
try:
    for log in a.dispatch_log:
        for line in open(log, encoding="utf-8"):
            m = re.search(r"\bDEAD [A-Za-z0-9_-]+\.([A-Za-z0-9_]+)\b", line)
            if m:
                dead.add(m.group(1))
    names = sorted(n for n in os.listdir(a.receipts) if n.endswith(".json"))
except OSError as ex:
    print("unreadable: %s" % ex)
    sys.exit(2)
bad = [n for n in names for s in dead if n.startswith(s + "-") or n.startswith(s + "__")]
print("dead seats: %s; receipts: %d; dead-seat receipts in tally: %d" % (sorted(dead) or "none", len(names), len(bad)))
for n in bad:
    print("  " + n)
sys.exit(1 if bad else 0)
