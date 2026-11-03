#!/usr/bin/env python3
"""Round-71 C1 calibration counter. Frozen before data; any change is a new file.

Predicate (the same sentence as contract.md section C1 and the receipt label):
  C1 met iff mismatches == 0 and the append-only guard holds, at --revision.
  mismatches = stale_planned + attack_share_mismatch.

  stale_planned: active SCORECARD.md `## Planned` headings naming a round < 72. The round is
    the heading's `— round N`, else the first `**Round N**` in the section body; a section with
    no parseable round counts as stale (fail-closed).
  attack_share_mismatch: the stated `attack share K/N` (exactly one, on a line that does not
    start with `Correction (round 71)`) differs from the strict count over
    .ufo/waves/round-70/w1-results.json (agent in reviewer, critic, mutation-tester, labrat),
    unless the revision carries a line `Correction (round 71): ... attack share <k>/<n>` with
    the recomputed value.
  guard: every removed base line is a `## Planned` heading whose round R is replaced in the tip
    by a line `## Superseded plan — round R`; all other base lines survive. Deleting a planned
    section without its superseded replacement fails the guard.

Usage: c71_calibration.py [--lane DIR] [--revision REV]   (REV default HEAD)
Exit: 0 met · 1 not met · 2 unevaluable · 64 usage. Reads committed bytes only (git show).
"""
import collections
import json
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
NEXT_ROUND = 72
STRICT_ROLES = {"reviewer", "critic", "mutation-tester", "labrat"}
RESULTS = ".ufo/waves/round-70/w1-results.json"
PLANNED_RE = re.compile(r"^## Planned(?:\s+—\s+round\s+(\d+))?\s*$")
SUPERSEDED_RE = re.compile(r"^## Superseded plan — round (\d+)\b")
ATTACK_RE = re.compile(r"attack share (\d+)/(\d+)")


def show(lane, rev, path):
    p = subprocess.run(["git", "-C", lane, "show", f"{rev}:{path}"], capture_output=True, text=True)
    if p.returncode != 0:
        print(f"C1 unevaluable: git show {rev}:{path} exit {p.returncode}", file=sys.stderr)
        sys.exit(2)
    return p.stdout


def planned_round(lines, i):
    m = PLANNED_RE.match(lines[i])
    if m and m.group(1):
        return int(m.group(1))
    for j in range(i + 1, len(lines)):
        if lines[j].startswith("## "):
            break
        b = re.search(r"\*\*Round (\d+)\*\*", lines[j])
        if b:
            return int(b.group(1))
    return None


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
    base_text = show(lane, "cc6b4e0b8c35e72dfb02c6184b847f68c1262153", "SCORECARD.md")
    tip_text = show(lane, rev, "SCORECARD.md")
    base, tip = base_text.splitlines(), tip_text.splitlines()

    stale = []
    for i, line in enumerate(tip):
        if PLANNED_RE.match(line):
            r = planned_round(tip, i)
            if r is None or r < NEXT_ROUND:
                stale.append((i + 1, r))

    stated = []
    correction_lines = []
    for n, line in enumerate(tip, 1):
        if line.startswith("Correction (round 71)"):
            correction_lines.append(line)
            continue
        for m in ATTACK_RE.finditer(line):
            stated.append((n, int(m.group(1)), int(m.group(2))))
    if len(stated) != 1:
        print(f"C1 unevaluable: stated attack-share population is {len(stated)}, frozen population is 1", file=sys.stderr)
        return 2
    _, K, N = stated[0]

    results = json.loads(show(lane, rev, RESULTS))["results"]
    if len(results) != N and N <= 0:
        print("C1 unevaluable: results population", file=sys.stderr)
        return 2
    k = sum(1 for x in results if x.get("agent") in STRICT_ROLES)
    n = len(results)
    corrected = any(re.match(rf"^Correction \(round 71\):.*attack share {k}/{n}\b", c) for c in correction_lines)
    attack_mismatch = 0 if ((K, N) == (k, n) or corrected) else 1

    base_counter = collections.Counter(base)
    tip_counter = collections.Counter(tip)
    removed = base_counter - tip_counter
    guard_ok = True
    for line, count in removed.items():
        m = PLANNED_RE.match(line)
        if not m:
            guard_ok = False
            continue
        bi = base.index(line)
        r = planned_round(base, bi)
        if r is None or not any((SUPERSEDED_RE.match(t) and int(SUPERSEDED_RE.match(t).group(1)) == r) for t in tip):
            guard_ok = False

    mismatches = len(stale) + attack_mismatch
    met = mismatches == 0 and guard_ok
    print(
        f"C1 revision={rev} stale_planned={len(stale)} stale_at={[s[0] for s in stale]} "
        f"attack_stated={K}/{N} attack_strict={k}/{n} attack_mismatch={attack_mismatch} "
        f"guard={'ok' if guard_ok else 'fail'} mismatches={mismatches} met={met}"
    )
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
