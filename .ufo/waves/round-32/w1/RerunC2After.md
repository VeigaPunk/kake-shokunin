# RerunC2After — C2 after-measurement (wave 1, r32-build)

Seat: KakeR32.RerunC2After. Axis: freshness. Task: rerun the C2 counter at the
build revision and the lane tip, compare with the L1 receipt, verify the counter
script is unchanged, and independently count the pinned blob ids in the tree.

## Commands run (all in /home/vgpnk/Projects/shokunin/kake-shokunin, read-only git)

1. `python3 -B .ufo/waves/round-32/c2_retained_count.py --rev 2f2f12deb0fe33d8fa7d9bd14c75d855f005f71a` → exit 0
2. `python3 -B .ufo/waves/round-32/c2_retained_count.py --rev 285abcad632e3c1c57bb402232e7d218054db383` → exit 0
3. `git show <rev>:.ufo/waves/round-32/c2_retained_count.py | sha256sum` at 5b32cc7 and 285abcad; plus `sha256sum` of the working-tree file → all three equal `48126fc5b42db1e210bcc2c24c7cb699207ee79b0683bf47cb0c8f94c3f3e22c`
4. `git ls-tree -r 285abcad… | grep -c d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252` → `1`
5. `git ls-tree -r 285abcad… | grep -c ee0b63819a9ce71e51469796541b9075e9676ae9` → `1`
6. `diff <rerun @2f2f12d> .ufo/waves/round-32/verification/c2-after-2f2f12d.json` → no output; identical.

## Observed counter output

At 2f2f12d: c1 true, c2RowIds ["S062"], c2 true, c3Cites {S062: 2}, c3 true,
met 3 — byte-identical to `.ufo/waves/round-32/verification/c2-after-2f2f12d.json`.

At 285abcad (lane tip): identical fields — c1 true, c2 [S062], c2 true,
c3Cites {S062: 2}, c3 true, met 3. The tip recheck commit did not weaken or
inflate the measurement; met is still 3.

## Independent checks

- Both blob ids appear exactly once each in `git ls-tree -r 285abcad…`, at the
  declared paths:
  - `d17ab7e5…` → `.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/render.yaml`
  - `ee0b6381…` → `.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/apps-sdk/Dockerfile`
- Counter script sha256 is the same at the declaration commit 5b32cc7 and at the
  lane tip 285abcad (and at the current working tree): the measurement did not
  change between after-declaration and tip.

## Per-condition verdict

- c1 (both blob ids in tree at rev): TRUE at both revs; independent grep counts confirm 1+1.
- c2 (S062-style row in SOURCES.md Registry, opened 2026-10-22): TRUE at both revs; row S062.
- c3 (entry cites S062): TRUE at both revs; 2 occurrences counted by the counter.
- met: 3 at both revs. Declared "after 3" holds at build rev and persists at lane tip.
- Counter integrity: sha256 equal at 5b32cc7, 285abcad, and working tree.

## Findings

No defect found. The rerun reproduces the L1 after-receipt exactly, the counter
is byte-identical across the declared range, and independent ls-tree counts
agree with the counter's c1 claim. The lane-tip recheck commit (285abcad)
neither altered the measurement nor the result.

## Not verified / out of scope

- Byte-identity of the retained copies against the live ds4cc-marketplace
  checkout (the counter only checks blob ids in the lane tree; blob-id equality
  is itself byte-identity proof for git content, but I did not separately hash
  the source checkout — covered by other seats).
- S062 row prose and the appended entry section beyond the counter's regexes.

## Artifacts

- /fast/scratch/hyaku/kake-r32/w1/RerunC2After/rerun-2f2f12d.json
- /fast/scratch/hyaku/kake-r32/w1/RerunC2After/rerun-285abcad.json
- /fast/scratch/hyaku/kake-r32/w1/RerunC2After/clone (unused read-only clone)

No tools installed; system python3 and git sufficed.
