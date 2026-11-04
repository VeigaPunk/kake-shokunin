# MutCounters — round 86 w1

Axes: detector sensitivity, isolated attribution, exact restoration, reproducible receipts. Author-side mutation probe only; no independent closure or production edits.

## Results

| Mutation | Expected detector | Actual output | Verdict |
|---|---|---|---|
| C2 comparator accepts any string for `basis`, keeping all other comparisons | Frozen `--selftest`; basis-only corrupt lookup fixture | Selftest **10/10, exit 0** unchanged. Wrong-basis fixture changes **0/15 met=false, exit 1 → 15/15 met=true, exit 0 → 0/15 met=false, exit 1** after restoration | **Survives frozen selftest**; killed by added basis-only behavioral discriminator |
| R4 drops only `flip:` conjunct | Frozen `c1-mut-r4`; hand-built README containing every other conjunct | Selftest **10/10, exit 0** unchanged. Hand-built missing-flip fixture changes **ok=false → ok=true → ok=false** | **Survives frozen selftest**; killed by isolated missing-flip discriminator |
| First-occurrence → last-occurrence, lookup-fixture outputs | Frozen C2 cases 5 and 15 | **13/15 met=false, exit 1**; case 5 becomes 200 rather than 100, case 15 becomes 100 rather than 200 | **Killed** |
| Drop no-store behavior, lookup-fixture outputs | Frozen C2 case 4 (also 13/14) | **12/15 met=false, exit 1** | **Killed** |
| Shared always true, lookup-fixture outputs | Frozen C2 case 3 | **14/15 met=false, exit 1** | **Killed** |

Every C2 fixture run reports `selftest_ok=1 tool_offline=1 tool_absent=0`. Each reader-output mutation was also exercised on the same active scratch filename in a before/mutated/restored cycle: **15/15 exit 0 → failing count exit 1 → 15/15 exit 0**, with exact restored fixture hashes. No failed baseline is counted as a kill.

The R4 selftest fixture removes D84-3 and the lesson citation together with flip:, so retaining those remaining checks masks this single-conjunct regression. The C2 green/constant/minmost fixtures do not isolate basis corruption. These are disclosed **selftest coverage weaknesses**, not proposed changes to the frozen contract or evidence that the actual frozen predicates are wrong. No counter was edited in the repo. D84-2/3 remain retained-open; no whole-queue closure claim.

## Scope and receipts

At initial discovery, the executor reader directory did not exist. Per assignment, no polling: used `FIXTURE_C2_TOOL` from the frozen counter instead. These are canned selftest fixtures with explicit output mutations, **not parser-branch mutations of the executor's reader** and not validation of a production implementation. The minimum/last distinction is preserved: this probe chose last, which fails both order witnesses.

All paths below are under `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/MutCounters/`:

- `pristine.json`, `mutant-basis.json`, `restored-basis.json`, `mutant-r4.json`, `restored.json`: literal commands, exits, stdout/stderr, counter SHA-256, targeted outcomes; pristine/restored include all expected/actual field differences by case.
- `fixture-cycles.json`: same-filename before/mutated/restored commands, outputs and fixture hashes.
- `restoration.json`: source/scratch exact-byte equality and hashes.
- `count.py`: restored instrument receipt; `fixture-{green,last-occurrence,no-store-dropped,shared-always}.py`: exact exercised fixture bytes.
- `probe.py`, `cycles.py`: exercised receipt drivers, retained for reproducibility; their execution paths refer to the now-deleted assigned scratch and must be re-created deliberately for replay.

Executed commands were `python3 -B /fast/scratch/hyaku/kake-r86/MutCounters/probe.py PHASE` for `pristine`, `mutant-basis`, `restored-basis`, `mutant-r4`, `restored`, then `python3 -B /fast/scratch/hyaku/kake-r86/MutCounters/cycles.py`. All drivers exited 0; enclosed detector exits are recorded above and in JSON. TMPDIR and every counter `--work` stayed in the assigned scratch. No VCS commands, network, installs, background jobs or delegation.

## Exact restoration

Counter SHA-256:

- Before and both restores: `f21c3a73f82c053d9a45257a245c92fec35973bb56d7c98c4985eb6e1c2af421`.
- Basis mutant: `982cf73c3b684a3d4c6c297c72b348508877e68cfd4bb4812830bf5338a39d4d`.
- R4 mutant: `f39d4212dcd4cae2c613dc592690d6c63381b8b8c736db118572944dab8f40dd`.

Lookup-fixture baseline/restored SHA-256: `c351fc542fb1133e7044368032f52162e03907ec04cc063bd3420264f02cb536`. Each mutant hash is preserved in `fixture-cycles.json`. Scratch cleanup is required before this seat yields; receipts were copied first.

Self-evaluation: accuracy 4 (fixture results do not generalize to real parser branches); completeness 4 (authorized absent-candidate fallback used); clarity 4 (raw JSON intentionally retains duplicate restore outputs); actionability 4 (replay requires reconstructing deleted scratch); conciseness 4 (hashes repeated for direct restoration audit). Overall 4.0. Highest-value downstream action: preserve these two selftest coverage findings without retrofitting frozen expectations. User should agree within the disclosed fallback scope.

Report: .ufo/waves/round-86/w1/MutCounters.md
