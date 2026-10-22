#!/usr/bin/env python3
"""Witness for round-30 lesson mistake M1: a falsify seat reached owned sites.

Scans committed wave seat reports for a *reported run* of a lane tool that
reaches the operator's owned web properties in a live mode.

Owned-surface tools and their live/offline modes (read from the tool source):
  scripts/freshness-sweep.mjs
      --offline          skip every fetch/ls-remote
      --section=paths    local citation scan only
      --section=history  local history analysis only
      --selftest, --help hermetic / text
      (no flag, or --section=armed, or --section=plazir)  LIVE
  scripts/probe-delta.mjs   any mode reaches pinned repositories
  scripts/live_snapshot.py  any mode fetches owned sites

A line counts when it carries a past-tense run verb (ran, executed, invoked,
launched) directly in front of the tool path, the verb is not negated, and
the command window after the tool path carries no offline flag. Present
tense ("the integrating seat runs ..."), negations ("Did not run ...") and
bare mentions are excluded by construction.

Usage: python3 -B witness_sweep_live_mode.py --root <lane> [--revision <commit>]
Exit 0 when no live-mode run is reported; 1 when one is (the criterion fails);
2 on bad input.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

TOOL_PATH = r"scripts/(?:freshness-sweep\.mjs|probe-delta\.mjs|live_snapshot\.py)"
RUN_VERB = r"(?:ran|executed|invoked|launched)"
NEGATION = r"(?:did\s+not|didn'?t|not|never|no|without|avoided|skipped|refused|declined)\s+"
COMMAND = re.compile(
    r"(?P<neg>" + NEGATION + r")?"
    r"(?P<verb>\b" + RUN_VERB + r"\b)"
    r"(?:\s+the)?(?:\s+full)?(?:\s+\w+){0,2}?\s+`?(?:node\s+)?" + TOOL_PATH,
    re.IGNORECASE,
)
OFFLINE_FLAG = re.compile(r"--offline|--section=(?:paths|history)|--selftest|--help")
WINDOW = 160


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=env)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", default="HEAD")
    ap.add_argument("--round", default=None,
                    help="limit the scan to .ufo/waves/<round>/ (default: all waves)")
    a = ap.parse_args()
    rev = git(a.root, "rev-parse", "--verify", "--quiet", a.revision + "^{commit}")
    if rev.returncode != 0:
        print("revision not found: %s" % a.revision)
        return 2
    commit = rev.stdout.decode().strip()
    files = git(a.root, "ls-tree", "-r", "--name-only", commit)
    if files.returncode != 0:
        print("ls-tree failed")
        return 2
    hits = []
    scanned = 0
    for rel in files.stdout.decode().splitlines():
        if not (rel.startswith(".ufo/waves/") and rel.endswith(".md")):
            continue
        if a.round and not rel.startswith(".ufo/waves/%s/" % a.round):
            continue
        blob = git(a.root, "show", "%s:%s" % (commit, rel))
        if blob.returncode != 0:
            continue
        scanned += 1
        text = blob.stdout.decode("utf-8", "replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in COMMAND.finditer(line):
                if m.group("neg"):
                    continue
                if OFFLINE_FLAG.search(line[m.end():m.end() + WINDOW]):
                    continue
                hits.append({"file": rel, "line": lineno, "text": line.strip()[:240]})
    out = {"witness": "kake-r30-m1-live-mode-scan", "revision": commit,
           "scannedFiles": scanned,
           "scannedPattern": ".ufo/waves/%s/**/*.md" % a.round if a.round else ".ufo/waves/**/*.md",
           "liveModeRuns": len(hits), "hits": hits}
    print(json.dumps(out, indent=1))
    if hits:
        print("M1 FAILS: %d live-mode run(s) reported" % len(hits), file=sys.stderr)
        return 1
    print("M1 holds: no live-mode run reported", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
