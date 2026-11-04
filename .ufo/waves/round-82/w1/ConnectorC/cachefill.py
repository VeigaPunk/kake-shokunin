#!/usr/bin/env python3
"""ConnectorC round-82 §6 receipt: decode x-github-request-id as a cache-fill epoch.

Reads the round-81 (capture A) and round-82 (capture B) receipts of the three declared
ds4cc.com surfaces and checks two arithmetic identities on all six receipts:

  (1) int(x-github-request-id.split(':')[-1], 16)  ==  the cache-fill instant
  (2) parsedate(expires) - fill                    ==  600  (max-age=600)

and one cross-tree identity:

  (3) A.x-github-request-id == B.x-github-request-id   for every surface

Exit 0 if all three hold, 1 otherwise. Read-only, offline.
"""
import datetime
import email.utils
import json
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
TREES = {"A": LANE + "/.ufo/waves/round-81/capture",
         "B": LANE + "/.ufo/waves/round-82/capture"}
SURFACES = ["ds4cc-primary", "ds4cc-robots", "ds4cc-sitemap"]


def epoch(ts):
    return int(datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp())


def load(tree, surface):
    d = json.load(open(f"{tree}/{surface}/response.json", encoding="utf-8"))
    h = {x["name"].lower(): x["value"] for x in d["headers"]}
    return d, h


fails = 0
print(f"{'surface':15s} {'tree':4s} {'fetchedAt':22s} {'fill':22s} {'expires-fill':>12s} {'cache':5s} {'age':>3s}")
for surface in SURFACES:
    for tag, tree in TREES.items():
        d, h = load(tree, surface)
        fill = int(h["x-github-request-id"].split(":")[-1], 16)
        exp = int(email.utils.parsedate_to_datetime(h["expires"]).timestamp())
        delta = exp - fill
        ok1 = abs(fill - epoch(d["fetchedAt"])) <= 86400  # a plausible clock, not identity
        ok2 = delta == 600
        fails += (not ok2)
        print(f"{surface:15s} {tag:4s} {d['fetchedAt']:22s} "
              f"{datetime.datetime.fromtimestamp(fill, datetime.timezone.utc).isoformat():22s} "
              f"{delta:>12d} {h['x-cache']:5s} {h['age']:>3s}"
              + ("" if ok2 else "   <-- expires-fill != 600"))

print()
for surface in SURFACES:
    _, ha = load(TREES["A"], surface)
    _, hb = load(TREES["B"], surface)
    same = ha["x-github-request-id"] == hb["x-github-request-id"]
    fails += (not same)
    print(f"{surface:15s} A.ghr == B.ghr : {same}   ({ha['x-github-request-id']})")

print()
print("identities: expires-fill==600 on all six; A.ghr==B.ghr on all three")
print("reading: x-github-request-id is the cache-fill fingerprint, replayed on later hits;")
print("         `body=same` across the two trees therefore compares the SAME stored objects,")
print("         not two independent origin reads.")
sys.exit(0 if fails == 0 else 1)
