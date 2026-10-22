#!/usr/bin/env python3
"""Witness for round-30 lesson mistake M3: a claim named a receipt that was
never committed.

Reads a lane report and the wave's committed verification receipts. Every
revision the report names as measured (or re-measured) must have a committed
receipt that names the same revision.

Usage: python3 -B witness_claim_receipt_backing.py --root <lane>
       --report <report path, relative to --root or absolute>
       --wave round-NN [--revision <commit>]
Exit 0 when every revision the report names has a committed receipt; 1 when
one does not (the criterion fails); 2 on bad input.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REV = re.compile(r"\b[0-9a-f]{7,40}\b")
# Words that put a hash in a measurement position, not an incidental mention.
MEASURE_CONTEXT = re.compile(
    r"(?:re-?measured at|measured at|re-?measured|re-?run at|rerun at|"
    r"counter at|grade[sd]? at|measured)", re.IGNORECASE)
REV_KEYS = ("revision", "commit", "rev")


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=env)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--report", required=True)
    ap.add_argument("--wave", required=True,
                    help="comma-separated wave names, or 'all' for every wave")
    ap.add_argument("--revision", default="HEAD")
    a = ap.parse_args()
    rev = git(a.root, "rev-parse", "--verify", "--quiet", a.revision + "^{commit}")
    if rev.returncode != 0:
        print("revision not found: %s" % a.revision)
        return 2
    commit = rev.stdout.decode().strip()

    report_path = Path(a.report)
    if not report_path.is_absolute():
        report_path = Path(a.root) / a.report
    try:
        report_text = report_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        print("report not readable: %s" % report_path)
        return 2

    named = []
    for lineno, line in enumerate(report_text.splitlines(), 1):
        if not MEASURE_CONTEXT.search(line):
            continue
        for m in REV.finditer(line):
            h = m.group(0)
            named.append({"hash": h, "line": lineno, "text": line.strip()[:200]})
    short = sorted({n["hash"] for n in named})

    listing = git(a.root, "ls-tree", "-r", "--name-only", commit, ".ufo/waves/")
    receipted = set()
    receipt_files = []
    for rel in listing.stdout.decode().splitlines():
        if not rel.endswith(".json") or "/verification/" not in rel:
            continue
        wave = rel.split("/")[2]
        if a.wave != "all" and wave not in a.wave.split(","):
            continue
        blob = git(a.root, "show", "%s:%s" % (commit, rel))
        if blob.returncode != 0:
            continue
        try:
            doc = json.loads(blob.stdout.decode("utf-8", "replace"))
        except ValueError:
            continue
        if not isinstance(doc, dict):
            continue
        for key in REV_KEYS:
            value = doc.get(key)
            if isinstance(value, str) and value:
                receipted.add(value)
                receipted.add(value[:7])
        receipt_files.append(rel)

    unbacked = []
    for h in short:
        if h in receipted:
            continue
        full = git(a.root, "rev-parse", "--verify", "--quiet", h + "^{commit}")
        if full.returncode == 0:
            full_hash = full.stdout.decode().strip()
            if full_hash in receipted or full_hash[:7] in receipted:
                continue
        unbacked.append(h)
    out = {"witness": "kake-r30-m3-claim-receipt-backing", "revision": commit,
           "report": str(report_path), "wave": a.wave,
           "receiptFilesCommitted": len(receipt_files),
           "namedRevisions": short, "receiptedRevisions": sorted(receipted),
           "unbackedRevisions": unbacked}
    print(json.dumps(out, indent=1))
    if unbacked:
        print("M3 FAILS: %d named revision(s) have no committed receipt: %s"
              % (len(unbacked), ", ".join(unbacked)), file=sys.stderr)
        return 1
    print("M3 holds: every named revision has a committed receipt", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
