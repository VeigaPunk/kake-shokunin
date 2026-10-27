#!/usr/bin/env python3
"""Round-62 calibration counter over committed Git blobs only."""
from __future__ import annotations
import argparse
import subprocess
import sys

BASE = "c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13"
PATHS = {
    "spot": "corpus/lessons/round-61-verifier-spotcheck.md",
    "knowledge": "corpus/knowledge/response-header-expectations.md",
    "quality": "corpus/QUALITY.md",
    "lesson": "corpus/lessons/round-62.md",
    "sources": "corpus/SOURCES.md",
}
QUOTE = "response header can be used to require checking of a response’s Content-Type header against the destination of a request"
CRITERION = "substantive located quote"

def blob(root: str, rev: str, path: str) -> str:
    p = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if p.returncode:
        return ""
    return p.stdout.decode("utf-8", errors="replace")

def measure(root: str, rev: str) -> int:
    data = {k: blob(root, rev, p) for k, p in PATHS.items()}
    if not data["spot"]:
        print("could-not-evaluate: missing verifier spot-check", file=sys.stderr)
        return 2
    disagreements = sum("S432" in line and "Disagree" in line
                        for line in data["spot"].splitlines())
    correction = int(QUOTE in data["knowledge"] and "S432 §3.6" in data["knowledge"]
                     and "Round-62 correction" in data["knowledge"])
    criterion = int(CRITERION in data["quality"] and "round-61-verifier-spotcheck.md" in data["quality"])
    lesson_gate = int("## Gate" in data["lesson"] and "S432" in data["lesson"]
                      and "Agree" in data["lesson"] and "Reject" in data["lesson"])
    source_row = int("| S432 |" in data["sources"])
    resolved = correction == 1 and criterion == 1 and lesson_gate == 1 and source_row == 1
    unresolved = disagreements if not resolved else 0
    met = unresolved == 0 and resolved
    print(f"revision={rev} disagreements={disagreements} unresolved={unresolved} quote_correction={correction} criterion={criterion} lesson_gate={lesson_gate} source_row={source_row} met={str(met).lower()}")
    return 0 if met else 1

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", default=BASE)
    args = ap.parse_args()
    return measure(args.root, args.revision)

if __name__ == "__main__":
    raise SystemExit(main())
