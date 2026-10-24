#!/usr/bin/env python3
"""Witness for round-30 lesson mistake M2: a receipt named no revision or digest.

Scans committed evidence receipts under a wave's verification directory and
its run summaries, and reports every receipt that does not say which bytes it
measured.

A receipt counts as identifying its subject when it carries:
  * a revision field (revision / commit / rev), and
  * a digest field for the tool or counter it ran
    (toolSha256 / counterSha256 / gateSha256 / runnerSha256 / sha256), or
    an explicit "tool" path that is pinned by a sibling digest field.

Receipts whose subject is a registry diff (no revision is meaningful, e.g.
a saved "old teaches" cell file) are reported separately as "not a
measurement receipt" and do not fail the criterion.

Usage: python3 -B witness_receipt_identity.py --root <lane> --wave round-29
       [--revision <commit>]
Exit 0 when every measurement receipt names its revision and digest; 1 when
one does not (the criterion fails); 2 on bad input.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

REV_KEYS = ("revision", "commit", "rev")
DIGEST_KEYS = ("toolSha256", "counterSha256", "gateSha256", "runnerSha256",
               "scriptSha256", "sha256")
# A receipt is a measurement receipt when it records a tally or a verdict.
MEASURE_MARKERS = ("passed", "total", "verdict", "cases", "passedOverTotal",
                    "totals", "sites", "exit", "byKind")


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=env)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--wave", required=True)
    ap.add_argument("--revision", default="HEAD")
    a = ap.parse_args()
    rev = git(a.root, "rev-parse", "--verify", "--quiet", a.revision + "^{commit}")
    if rev.returncode != 0:
        print("revision not found: %s" % a.revision)
        return 2
    commit = rev.stdout.decode().strip()
    listing = git(a.root, "ls-tree", "-r", "--name-only", commit,
                  ".ufo/waves/%s/" % a.wave)
    if listing.returncode != 0:
        print("wave not found: %s" % a.wave)
        return 2
    paths = [p for p in listing.stdout.decode().splitlines()
             if p.endswith(".json") and "/verification/" in p]
    # summaries live beside the verification dir
    for p in listing.stdout.decode().splitlines():
        if p.endswith("summary.json") and p not in paths:
            paths.append(p)
    unidentified, non_measurement = [], []
    for rel in sorted(set(paths)):
        blob = git(a.root, "show", "%s:%s" % (commit, rel))
        if blob.returncode != 0:
            continue
        try:
            doc = json.loads(blob.stdout.decode("utf-8", "replace"))
        except ValueError:
            non_measurement.append({"file": rel, "why": "not JSON"})
            continue
        if not isinstance(doc, dict):
            non_measurement.append({"file": rel, "why": "not an object"})
            continue
        keys = set(doc)
        if not any(k in keys for k in MEASURE_MARKERS):
            non_measurement.append({"file": rel, "why": "no measurement marker"})
            continue
        has_rev = any(k in keys for k in REV_KEYS)
        has_dig = any(k in keys for k in DIGEST_KEYS)
        if not (has_rev and has_dig):
            bucket = "anonymous" if not (has_rev or has_dig) else "partial"
            unidentified.append({"file": rel, "bucket": bucket,
                                  "namesRevision": has_rev,
                                  "namesDigest": has_dig,
                                  "keys": sorted(keys)[:10]})
    anonymous = [r for r in unidentified if r["bucket"] == "anonymous"]
    partial = [r for r in unidentified if r["bucket"] == "partial"]
    out = {"witness": "kake-r30-m2-receipt-identity", "revision": commit,
           "wave": a.wave, "receiptsScanned": len(set(paths)),
           "unidentified": len(unidentified),
           "anonymousCount": len(anonymous), "partialCount": len(partial),
           "receipts": unidentified,
           "notMeasurementReceipts": non_measurement}
    print(json.dumps(out, indent=1))
    if unidentified:
        print("M2 FAILS: %d receipt(s) do not name both a revision and a digest "
              "(%d anonymous, %d partial)" % (len(unidentified), len(anonymous),
                                              len(partial)), file=sys.stderr)
        return 1
    print("M2 holds: every measurement receipt names a revision and a digest",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
