#!/usr/bin/env python3
"""Round-36 criterion: every full 40-hex commit hash in a SCORECARD section resolves.

Mined from the round-36 declaration, whose "Base" line carried a full hash that names no object
(an L1 typing error). Usage:

  python3 -B hash_resolve_check.py --root REPO --revision REV --heading "## Round 36 — declared claims"

Reads SCORECARD.md at REV, takes the text from the heading to the next `## ` heading, and checks
each 40-hex word with `git cat-file -e <hash>^{commit}` in REPO. Hashes that resolve only from a
retained bundle are not accepted (fetch the bundle first). Exit 0 when all resolve, 1 when any
does not (each printed), 2 on a usage or read error.
"""
import argparse
import os
import re
import subprocess
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", required=True)
    ap.add_argument("--heading", required=True)
    a = ap.parse_args()
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    show = subprocess.run(["git", "-C", a.root, "show", f"{a.revision}:SCORECARD.md"], capture_output=True, env=env)
    if show.returncode != 0:
        print("cannot read SCORECARD.md at", a.revision, file=sys.stderr)
        return 2
    text = show.stdout.decode("utf-8", "replace")
    start = text.find(a.heading + "\n")
    if start < 0:
        print("heading not found:", a.heading, file=sys.stderr)
        return 2
    end = text.find("\n## ", start + len(a.heading))
    section = text[start:end if end > 0 else len(text)]
    bad = []
    hashes = sorted(set(re.findall(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", section)))
    for h in hashes:
        ok = subprocess.run(["git", "-C", a.root, "cat-file", "-e", f"{h}^{{commit}}"], capture_output=True, env=env)
        if ok.returncode != 0:
            bad.append(h)
            print("FAIL: does not resolve:", h)
    print(f"hashes {len(hashes)}, unresolved {len(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
