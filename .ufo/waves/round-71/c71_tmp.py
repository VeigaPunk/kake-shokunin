#!/usr/bin/env python3
"""Round-71 C2 freshness counter (stale /tmp citations in SKILL.md). Frozen before data.

Predicate (the same sentence as contract.md section C2 and the receipt label):
  C2 met iff unannotated_tokens == 0 and the replacement guard holds, at --revision.
  A /tmp token is a path starting with the scratch root (built below so this file carries no
  literal). Its line is annotated iff the line carries the phrase
  `not an executable instruction` (the QUALITY absence-annotation phrase) or the line is a
  mktemp-based replacement that contains no /tmp token.
  guard: the removed base lines all carry a /tmp token; the added tip lines each carry the
  annotation phrase or `mktemp`; the number of removed lines equals the number of added lines
  (a deletion without replacement fails).

Usage: c71_tmp.py [--lane DIR] [--revision REV]   (REV default HEAD)
Exit: 0 met · 1 not met · 2 unevaluable · 64 usage. Reads committed bytes only (git show).
"""
import collections
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
BASE = "cc6b4e0b8c35e72dfb02c6184b847f68c1262153"
PATH = "SKILL.md"
PHRASE = "not an executable instruction"
TMP_ROOT = "/" + "tmp" + "/"
TOKEN_RE = re.compile(re.escape(TMP_ROOT) + r"[A-Za-z0-9_.\-/]*")


def show(lane, rev):
    p = subprocess.run(["git", "-C", lane, "show", f"{rev}:{PATH}"], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"C2 unevaluable: git show {rev}:{PATH} exit {p.returncode}", file=sys.stderr)
        sys.exit(2)
    return p.stdout.splitlines()


def main(argv):
    lane, rev = LANE, "HEAD"
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--lane" and args:
            lane = args.pop(0)
        elif a == "--revision" and args:
            rev = args.pop(0)
        else:
            print(__doc__, file=sys.stderr)
            return 64
    base = show(lane, BASE)
    tip = show(lane, rev)

    total = 0
    unannotated = 0
    unannotated_lines = []
    for n, line in enumerate(tip, 1):
        toks = TOKEN_RE.findall(line)
        total += len(toks)
        if toks and PHRASE not in line:
            unannotated += len(toks)
            unannotated_lines.append(n)

    base_c = collections.Counter(base)
    tip_c = collections.Counter(tip)
    removed = base_c - tip_c
    added = tip_c - base_c
    guard_ok = (
        all(TOKEN_RE.search(line) for line in removed.elements())
        and all((PHRASE in line) or ("mktemp" in line and not TOKEN_RE.search(line)) for line in added.elements())
        and sum(removed.values()) == sum(added.values())
    )
    met = unannotated == 0 and guard_ok
    print(
        f"C2 revision={rev} tokens_total={total} unannotated_tokens={unannotated} "
        f"unannotated_lines={unannotated_lines} removed={sum(removed.values())} "
        f"added={sum(added.values())} guard={'ok' if guard_ok else 'fail'} met={met}"
    )
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
