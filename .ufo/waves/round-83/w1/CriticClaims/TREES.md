# Crafted trees (CriticClaims, round 83 w1) — reconstruction recipes

All trees were built read-only from the lane (`git -C <lane> archive <rev> | tar -x -C <dir>`) and
scored with the frozen counters; nothing in the lane or fleet was modified. Scratch was
`/fast/scratch/hyaku/kake-r83/CriticClaims/` and has been deleted after these artifacts were copied.

## records-only (C1)

```
D=<dir>; git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive \
  826b0061f233ce1dffb9bd6874abc1342a864247 | tar -x -C "$D"
# overlay the files in records-only-tree/ at the same relative paths, then append
# QUALITY-appended-line.txt to corpus/QUALITY.md
python3 -B .ufo/waves/round-83/c83_defect_queue.py --root "$D" \
  --fleet /home/vgpnk/Projects/shokunin --work <scratch>
```
Reads: `open=0 closed=6 met=true`, exit 0.

### sparse-seats (same tree, results/accounting replaced)

Keep `ReviewC1`, `CriticClaims`, `ScoutRecon`, `ScribeLesson` only, each with `output: "x"`;
`settled=4 settled_attack=2 settled_share=0.5`. Reads `D1 closed … met=true`, exit 0 — 10 of 14
seats dead.

## c2-base-records (C2)

```
D=<dir>; git -C <lane> archive 826b0061… | tar -x -C "$D"
cp <lane>/scripts/header_change_class.py "$D/scripts/"
cp <lane>/.ufo/waves/round-83/controls/after-c2-classes.txt "$D/.ufo/waves/round-83/controls/"
# control pair: copy .ufo/waves/round-82/capture to .ufo/waves/round-83/capture-control/{a,b};
# in b/, for each surface flip body.bin[0] ^= 0x01, refresh bytes and sha256, and on
# ds4cc-primary set the ETag header to "fabricated-v2" (no network anywhere)
python3 -B .ufo/waves/round-83/c83_drift_class.py --root "$D" --work <scratch>
```
Reads `… record_equal=1 determinism=1 control_ok=1 … met=true`, exit 0.

## c2-identical-captures (C2)

Same as above but `a/` and `b/` are identical copies. Reads `diffs=0 … record_equal=0 … met=false`,
exit 1.

## c2-tool-diverges (C2)

Same as `c2-base-records` (frozen tool + record + control pair) with one edit to the scratch copy of
`scripts/header_change_class.py`: the summary print's `verdict={overall}` is replaced by
`verdict=representation-changed`, and the record is regenerated from that tool. The tool's own
`--selftest` still prints `6/6 passed` (it never calls `run()`). Reads `… record_equal=1 …
selftest_ok=1 … met=true`, exit 0, while the tool's per-surface lines say `same-object`.

## fleet-drift-fixture (C1 D4)

A 3-commit fixture repo (`git init` in scratch, toplevel asserted) touching
`.ufo/reports/round-81/kake.md`: `filed` → `amended` (removes four lines) → `later touch` (adds a
line). Scoring `records-only` against it with `--fleet <fixture>` reads
`D4 open removed=0 quoted=0 amendment=ecdf37ba log=no` and `open=1 closed=5 met=false`, exit 1 —
the counter's `after` is the latest commit touching the path, not the contract's `7678247a`.
