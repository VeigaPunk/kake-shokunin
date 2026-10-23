# RerunC2Evidence — round 37 wave 2 (falsify), axis operability

Attacked: the non-claim C2 evidence (27 → 32 of 32, `verification/c2-at-621fb528.json` →
`c2-evidence-at-528a6d02.json`) and the C2 snapshot control receipt that withdrew C2
(`retained/controls/c2/c2-snapshot.json`, "32 of 32, met, 398 valid", SCORECARD round-37 control call
lines 38-42 of that section; `corpus/lessons/round-37.md:21-23,114-117,157`).

Sandbox: `/fast/scratch/hyaku/kake-r37w2/RerunC2Evidence/clone`, cloned from the lane, checked out at
`79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c`; TMPDIR in the sandbox; GIT_* unset. Counter sha256
`d72e232e…5cb6` in the clone and in the lane (identical). Outputs in `/fast/scratch/hyaku/kake-r37w2/RerunC2Evidence/out/`.

## Runs

| run | command tail | exit | fixtures | valid | killed | survivors | receipt match |
|---|---|---:|---:|---:|---:|---|---|
| 528a6d02 | `--revision 528a6d02 --jobs 8` | 0 | 106 | 106 | 32 | none | yes, byte-identical to `verification/c2-evidence-at-528a6d02.json` (receipt `.exit` 0) |
| 528a6d02 | `--revision 528a6d02 --jobs 1` | 0 | 106 | 106 | 32 | none | yes, byte-identical to the `--jobs 8` run |
| 621fb528 | `--revision 621fb528 --jobs 8` | 1 | 101 | 101 | 27 | M07,M08,M09,M11,M24 | yes, byte-identical to `verification/c2-at-621fb528.json` (receipt `.exit` 1) |
| snapshot rebuild | `--revision snapctl --jobs 8` (x3) | 0, 0, 0 | 400 | 398 | 32 | none | yes, identical to `retained/controls/c2/c2-snapshot.json` except `revision` (key order too); 3 runs byte-identical |

Full command: `timeout 900 python3 -B .ufo/waves/round-37/c2_mutkill.py --root /fast/scratch/hyaku/kake-r37w2/RerunC2Evidence/clone --revision <rev> --jobs <n>`, cwd the clone.
Output sha256: 528a6d02 `5d637cd2…f041`, 621fb528 `cf1a8861…c03c`, snapshot `e5089f0a…e435`.

Snapshot rebuild: `git checkout -q -b snapctl 202d625a && cp .../retained/controls/c2/selftest-snapshot.py scripts/source_recheck_selftest.py && git commit -qam …` (exit 0), giving
commit `4908ebcec3ca39ef2dc041818da469181a048836` (parent `202d625a`, blob `2c94c4a2…`, file sha256
`73239541…7e54` = `variants.json` pin = receipt `selftestSha256`). The diff against 202d625a is 10672
insertions, 0 deletions (101 fixtures from the base kept, 299 appended, as `ctl/CtlC2FixtureSets.md` says).
Invalid fixtures in both the rebuild and the receipt: `random-259` and `random-273` fail on E2 and pass on E1.

## Verdicts

- "C2 counter 27 → 32 of 32 at 621fb528 → 528a6d02; 106 fixtures, all valid on E1 and E2" (lesson
  :114-117, SCORECARD measured-results): **holds**. Both receipts reproduce byte-for-byte, and the result is the same at `--jobs 1` and `--jobs 8`.
  The five previous survivors are each killed by exactly one fixture, and each fixture is named for its contract rule:
  M07 `b12-relative-redirect-resolved-against-previous-hop`, M08 `b13-dot-segments-in-relative-location-removed`,
  M09 `c11-comment-with-inner-greater-than-removed-whole`, M11 `c12-tag-between-text-removed-before-match`,
  M24 `f17-utf8-bom-mark-dropped-from-text`. The selftest diff 621fb528..528a6d02 is +35 lines, 0 deletions.
- "Snapshot control met 32 of 32 with 398 valid fixtures, so C2 is withdrawn" (SCORECARD control call;
  `CtlC2FixtureSets.md` table): **holds**. The result is reproduced from the retained variant file, and the exit is 0 (met).
- The committed retained receipts have the sha256 values listed in `ctl/CtlC2FixtureSets.md`
  (c2-snapshot `2a363842…a904`, c2-pristine = c2-restored `f187453a…aa57`, initial `064d7caa…a1da`): **holds**.

## Findings (by severity)

1. Low, operability/reproducibility: the snapshot receipt's `revision` `da09e6c737a2…` is not
   in the lane repo (`git cat-file -t da09e6c7…` → "could not get object info"). It lived only in the
   L1's private bundle. Re-running the receipt's own command fails to resolve that revision. The only way to reproduce it is to rebuild from the retained file on `202d625a` as above, and that rebuild agrees with the receipt.
   SCORECARD calls this commit "in the seat's sandbox", which is accurate, but the receipt gives no rebuild recipe.
2. Low, operability: `c2_mutkill.py:237-252` reads the mutants and their manifest from the `--root`
   worktree, not from `--revision`. `.ufo/waves/round-37/c2/mutants` is absent at 621fb528 (`git rev-parse
   621fb528:.ufo/waves/round-37/c2/mutants` fails), so the 621fb528 result depends on the clone's checkout
   (79d3c780, tree `51b43d7c…`, the same tree as at 202d625a and 528a6d02). The pinned manifest sha256 makes the counter exit 2
   on a wrong checkout; it does not return a wrong count. This is [INFERENCE] from the code, not run.
3. Info: each new kill depends on a single fixture (killerCount 1). Removing any one of the five fixtures brings back its survivor.
   This is not a defect in the evidence.

## Not checked

- Snapshot-initial (`5ee6bb05`, 27 killed, 396 valid): not rebuilt. Its source is only in the L1 bundle,
  which this seat may not read. The retained receipt hash matches the control report, and that is the only check.
- The all-failing, junk and keyed controls were not re-scored. That was out of this item's scope.
Installs/updates: none. Lane and fleet writes: only this report. All processes this seat started have exited (`pgrep -f RerunC2Evidence` → 0).
