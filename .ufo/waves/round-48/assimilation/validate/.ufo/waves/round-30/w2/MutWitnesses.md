# Round 30, wave 2 — MutWitnesses: can the four witnesses fail when they should?

Axes: operability (evidence identity) and freshness (live-mode bound).
Target: the four witnesses under `.ufo/waves/round-30/witness/` (M1 live-mode
scan, M2 receipt identity, M3 claim/receipt backing, M4 C2 field comparison).
Method: plant one defect per witness in a throwaway clone, then mutate the
witness's key comparison and see whether the planted defect survives.
All work stayed in `/fast/scratch/hyaku/kake-r30/w2/MutWitnesses/`; the lane
was read only. No live-capable lane script was invoked in any mode.

## Ledger: planted defect -> witness exit before and after mutation

| Witness | Planted defect (sandbox clone, commit) | Pristine witness | Mutated witness | Verdict |
|---|---|---|---|---|
| M1 `witness_sweep_live_mode.py` | seat report line with a bare live-mode freshness-sweep invocation, no offline flag after it (`clone-m1` @ `cd2cc77`, `.ufo/waves/round-30/w2/SeatReport-plant.md:5`) | **exit 1**, names the file and line | **exit 0** | defect survives the mutation |
| M2 `witness_receipt_identity.py` | receipt naming a digest but no revision (`clone-m2` @ `23238c0`, `.ufo/waves/round-30/verification/plant-partial-receipt.json`) | **exit 1**, bucket `partial` | **exit 0** | defect survives the mutation |
| M3 `witness_claim_receipt_backing.py` | SCORECARD names `deadbee1deadbee2deadbee3deadbee4deadbee5` with no committed receipt (`clone-m3` @ `19e8e73`) | **exit 1**, names that hash | **exit 0** | defect survives the mutation |
| M4 `witness_c2_field_comparison.py` | frozen round-29 counter never compares `id`, `page`, `resolved`, `pagesChecked`, `referencesChecked` (present in the lane) | **exit 1** | **exit 0** ("M4 holds") while its own JSON still shows a wrong-field tool scoring 30/30 | defect survives the mutation |

Clean bases (so no baseline failure hides the effect): M1 base `clone` @ `451e98f`
exit 0; M2 base `clone-m2` @ `0d6c281` exit 0 (the committed anonymous summary
given a revision and a tool digest); M3 base `clone-m3` @ `f8973d1` exit 0
(identity receipts added for the ten older hashes).

## Mutations (one line each; `mutants/` vs `pristine/`)

| File | Edit | sha256 of mutant |
|---|---|---|
| `mutants/m1.py` | drop `freshness-sweep\.mjs` from `TOOL_PATH` | `b48ad31f4f04ee9d2e38fb5eea52e80f08936e829ce8b2e0c9acad264220bd6c` |
| `mutants/m2.py` | `has_rev = any(...)` -> `has_rev = True` | `53a972a4eb45249a480b3e6bde8c82fa81e5d9b7fd9bff9a1858c645a70e2f5f` |
| `mutants/m3.py` | `REV` bounds `{7,40}` -> `{41,}` (no hash ever named) | `df25290beee9848d12ff3e8bff74de294ea038f2c603fc718e5496e18d10d89a` |
| `mutants/m4.py` | `gaps = []` and mutant-A survival test flipped to `exit == 1` | `256e65b3299e6001481c21797bbe264471a79c396a952eef151c0276bdbc803c` |

The M1 mutation is not scope creep: on the known round-29 breach it turns the
pristine exit 1 into exit 0. M4 needed two edits because its verdict is the
disjunction of two comparisons (coverage gaps, mutant survival); one edit on
the verdict line would have been a no-op.

## What the pristine witnesses say on the lane tip `1c7773e` (read only)

- M1 `witness_sweep_live_mode.py --root <lane> --round round-30 --revision HEAD` -> **exit 0**.
- M2 `witness_receipt_identity.py --root <lane> --wave round-30 --revision HEAD` -> **exit 1**,
  naming `.ufo/waves/round-30/r29-rerun/real-input/summary.json` (bucket `anonymous`:
  a tally with `sites`/`totals`, no revision, no digest). Its digest sits in
  `r29-rerun/receipt.json`, which the witness does not scan.
- M3 `witness_claim_receipt_backing.py --root <lane> --report SCORECARD.md --wave all --revision HEAD`
  -> **exit 1**, ten names, all from rounds 17-25 history.
- M4 `witness_c2_field_comparison.py --root <lane> --revision HEAD` -> **exit 1** by design
  (it documents the frozen round-29 counter and cannot pass).

## Blind spots found with cheap probes (false negatives)

1. M1 scans only `.ufo/waves/**/*.md`. A run line in `.ufo/reports/round-30/kake.md`
   or in a `.txt` seat report is invisible: `clone-fn` @ `c9c52ea` -> **exit 0**.
2. M1's regex allows at most two words between the verb and the tool path
   (`.ufo/waves/round-30/w2/SeatReport-wide-words.md:3`): **exit 0**, not flagged.
3. M2 scans only `*.json` under a `verification/` directory plus files named
   `summary.json`. A tally at `.ufo/waves/round-30/evidence/anon-receipt.json`
   with no identity is invisible: **exit 0**.
4. M3 needs a measurement word on the same line as the hash. A report row
   `revision: <hash>` is never named: `clone-fn3` -> **exit 0**.
5. M3 knows only the keys `revision`/`commit`/`rev` and only receipts under a
   `verification/` directory, so it reports older hashes as unbacked even where
   a committed receipt exists: `.ufo/waves/round-22/measure-after-v2.json`
   carries `sourceCommit: b539cc17c25e...`, `.ufo/waves/round-25/final-measurement.json`
   carries `measuredSourceRevision: be362b7808ea...`. Both are invisible to M3.

## Commands and exit codes (sandbox root `/fast/scratch/hyaku/kake-r30/w2/MutWitnesses`)

```
python3 -B pristine/witness_sweep_live_mode.py --root clone-m1 --round round-30 --revision HEAD      # exit 1
python3 -B mutants/m1.py            --root clone-m1 --round round-30 --revision HEAD                 # exit 0
python3 -B pristine/witness_sweep_live_mode.py --root clone --round round-29 --revision 234524c       # exit 1
python3 -B mutants/m1.py            --root clone --round round-29 --revision 234524c                 # exit 0
python3 -B pristine/witness_receipt_identity.py --root clone-m2 --wave round-30 --revision HEAD      # exit 1
python3 -B mutants/m2.py            --root clone-m2 --wave round-30 --revision HEAD                  # exit 0
python3 -B pristine/witness_claim_receipt_backing.py --root clone-m3 --report SCORECARD.md --wave all --revision HEAD  # exit 1
python3 -B mutants/m3.py            --root clone-m3 --report SCORECARD.md --wave all --revision HEAD # exit 0
python3 -B pristine/witness_c2_field_comparison.py --root clone --revision HEAD                       # exit 1
python3 -B mutants/m4.py            --root clone --revision HEAD                                     # exit 0
python3 -B pristine/witness_sweep_live_mode.py --root clone-fn --round round-30 --revision HEAD       # exit 0 (blind)
python3 -B pristine/witness_receipt_identity.py --root clone-fn --wave round-30 --revision HEAD       # exit 0 (blind)
python3 -B pristine/witness_claim_receipt_backing.py --root clone-fn3 --report SCORECARD.md --wave all --revision HEAD # exit 0 (blind)
```
Outputs: `out/*.json`, `out/*.err` in the sandbox; clones `clone-m1`, `clone-m2`,
`clone-m3`, `clone-fn`, `clone-fn3` hold every planted byte.

## Restoration

The lane's four witness files are byte-identical to my pristine copies
(`sha256sum` equal: `1724ba60…`, `b21b129d…`, `fc79e6fe…`, `938c0f4d…`), and
`git status --short` in the lane shows only untracked files from other seats.
Every mutated copy lives only in the sandbox `mutants/`.

## Not verified

The exit-2 (bad input) paths of the four witnesses were not exercised. The
M3 hash-scoped mutation is blunt (it names no hash at all) rather than a
minimal semantic change. I did not re-run the round-29 counter by hand against
a wrong-field tool; the mutant-A run inside the M4 witness output is that
evidence. No live requests were made and the three live-capable scripts were
never invoked, in any mode.
