#!/usr/bin/env python3
"""Criterion check: every contract bullet must be load-bearing (ablation floor).

A capability target is only worth declaring when no contract bullet can be
skipped and the target still met (round-35 routed defect 3: "C1 target slack.
22/24 is reachable with bullet (c) skipped"). This check takes the declared
predicate target and the ablation receipts scored against it, and fails when

  1. an ablation receipt reports ``met`` true (the ablated tool met the target),
  2. an ablation receipt reports ``passed >= T`` (the ablated tool reached the
     target on the score alone), or
  3. a required contract bullet letter has no ablation receipt at all (the
     bullet is untested, so nothing says it moves the target).

Receipts are the JSON files a counter writes per scored variant; a receipt
counts as an ablation when its name has the shape ``ablation-<bullet>_<rule>.json``.
Files with any other name in the same directory (for example the reference
receipt ``reference-private.json``, which is the tool itself and not an
ablation) are skipped and reported on stderr.

Usage:
  ablation_floor_check.py --target 25 --receipts DIR [--receipts FILE ...] \\
      [--bullets a,b,c,d,e,f,g]

Exit 0: no failure (every ablation is below the target and every required
bullet has a receipt). Exit 1: at least one failure, one line printed per
failure. Exit 2: usage or read error.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

# An ablation receipt names the contract bullet it ablates and the rule it drops.
NAME_RE = re.compile(r"^ablation-(?P<bullet>[^-_]+)_(?P<rule>.+)\.json$")

# The round-36 C1 contract has seven bullets: (a) final status, (b) redirects,
# (c) HTML text, (d) quote match, (e) media types, (f) decoding, (g) input faults.
DEFAULT_BULLETS = "a,b,c,d,e,f,g"


def collect(paths: list[str]) -> list[str]:
    """Expand receipt directories into the JSON files they hold, sorted."""
    files: list[str] = []
    for p in paths:
        if os.path.isdir(p):
            for name in sorted(os.listdir(p)):
                if name.endswith(".json"):
                    files.append(os.path.join(p, name))
        elif os.path.isfile(p):
            files.append(p)
        else:
            print(f"cannot read receipt path: {p}", file=sys.stderr)
            raise SystemExit(2)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="ablation floor check")
    ap.add_argument("--target", type=int, required=True,
                    help="declared predicate target T (passed count that meets the claim)")
    ap.add_argument("--receipts", action="append", required=True, metavar="PATH",
                    help="receipt file or directory of receipts (repeatable)")
    ap.add_argument("--bullets", default=DEFAULT_BULLETS,
                    help="comma separated contract bullet letters that each need a receipt")
    args = ap.parse_args()

    required = [b.strip() for b in args.bullets.split(",") if b.strip()]
    if not required:
        print("no bullet letter named", file=sys.stderr)
        return 2

    failures: list[str] = []
    seen_bullets: set[str] = set()
    scored = 0
    skipped: list[tuple[str, str]] = []

    for path in collect(args.receipts):
        name = os.path.basename(path)
        m = NAME_RE.match(name)
        if not m:
            skipped.append((path, name))
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError) as exc:
            failures.append(f"FAIL: receipt {name} cannot be read ({exc.__class__.__name__})")
            continue
        if not isinstance(data, dict):
            failures.append(f"FAIL: receipt {name} is not a JSON object")
            continue
        passed = data.get("passed")
        met = data.get("met")
        if not isinstance(passed, int) or isinstance(passed, bool) or not isinstance(met, bool):
            failures.append(f"FAIL: receipt {name} lacks an integer 'passed' and a boolean 'met'")
            continue
        scored += 1
        seen_bullets.add(m.group("bullet"))
        cases = data.get("cases", "?")
        if met:
            failures.append(
                f"FAIL: ablation {name} met the target (met=true, passed={passed} of {cases})")
        if passed >= args.target:
            failures.append(
                f"FAIL: ablation {name} reaches the target (passed={passed} of {cases} >= {args.target})")
        rt = data.get("target")
        if isinstance(rt, int) and rt != args.target:
            print(f"warning: receipt {name} was scored against target {rt}, not {args.target}",
                  file=sys.stderr)

    for bullet in required:
        if bullet not in seen_bullets:
            failures.append(f"FAIL: no ablation receipt for bullet ({bullet})")

    for path, name in skipped:
        note = f"note: not an ablation receipt, skipped: {name}"
        try:
            with open(path, encoding="utf-8") as fh:
                other = json.load(fh)
            if isinstance(other, dict) and other.get("met") is True:
                note += f" (met=true, passed={other.get('passed')})"
        except (OSError, ValueError):
            pass
        print(note, file=sys.stderr)

    if failures:
        for line in failures:
            print(line)
        print(f"FAIL: {len(failures)} failure(s), {scored} ablation receipts scored")
        return 1
    print(f"PASS: {scored} ablation receipts scored, all below target {args.target}, "
          f"bullets {''.join(required)} each covered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
