#!/usr/bin/env python3
"""Round-35 criterion (e): a knowledge counter must refuse the cheap entries that skip the study.

Run a frozen counter on each named control revision. Every control must score below target
(counter exit 1). The controls this criterion asks for are an entry whose stated facts are
inverted, and an entry written without opening any retained source text.

Usage:
  knowledge_control_check.py --root REPO --counter PATH --claim c2 --key-revision KREV \
      --control REV [--control REV ...]

Exit 0: every control is refused (counter exit 1). Exit 1: at least one control meets the
target (counter exit 0), so the counter cannot tell study from its absence. Exit 2: a counter
run could not evaluate (any other exit), or no control was named.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--counter", required=True)
    ap.add_argument("--claim", required=True)
    ap.add_argument("--key-revision", required=True)
    ap.add_argument("--control", action="append", default=[])
    args = ap.parse_args()
    if not args.control:
        print("no control named")
        return 2
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    met, broken = [], []
    for rev in args.control:
        proc = subprocess.run([sys.executable, "-B", args.counter, args.claim, "--root", args.root,
                               "--revision", rev, "--key-revision", args.key_revision],
                              capture_output=True, text=True, env=env)
        try:
            out = json.loads(proc.stdout)
        except ValueError:
            out = {}
        summary = {k: out.get(k) for k in ("revision", "met", "passed", "probesPassed", "goodCites")}
        print(f"control {rev}: counter exit {proc.returncode} {json.dumps(summary, sort_keys=True)}")
        if proc.returncode == 0:
            met.append(rev)
        elif proc.returncode != 1:
            broken.append(rev)
    if broken:
        print("FAIL: could not evaluate " + ", ".join(broken))
        return 2
    if met:
        print("FAIL: control meets the target: " + ", ".join(met))
        return 1
    print("PASS: every control is refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
