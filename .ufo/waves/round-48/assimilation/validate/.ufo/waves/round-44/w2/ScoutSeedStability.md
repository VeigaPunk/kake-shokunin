# ScoutSeedStability — G6 seed-luck probe

Axes: operability (per-control witness rate over seeds 1..30), freshness (sha256 of the G6 bytes actually probed).

## Result

**BLOCKED.** `classes/g6_fold_pairs.py` is still the pre-fix module (witnesses 0/4). The named attack — a *correct* G6 witnesses each casememo control on fewer than 90% of seeds — was not scored against a landed fix. Before-data on the current module is below.

**Attack vs before-data: not seed-luck.** Witness rate is 0/30 (0%) on every casememo control, not a flaky mix of witnesses. The open 0/4 gap is uniform across seeds 1..30.

No tools installed. No lane class file edited. LSP was not in this seat's tool inventory; the measurement is probe exit codes, not a symbol graph.

## Bytes probed

sha256 stayed `f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d` from the snapshot through all 120 probes and a post-sweep rehash. Source shape matches the wave-1 non-witness (case swap in the *second* path segment; 50 Kelvin + 50 long-s `foldpair`s). Claim receipt `.ufo/waves/round-44/verification/claim/after-v5.json` still has empty `caughtBy` on casememo-v3/v4/v7/v8.

```
f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d  .ufo/waves/round-44/classes/g6_fold_pairs.py
f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d  /fast/scratch/hyaku/kake-r44/ScoutSeedStability/g6_fold_pairs.py.snapshot
```

Post-sweep confirmation:

```
rows 120
exits [0]
equals [True]
shas ['f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d']
unstable 0
('casememo-v3-validity-lower.py', 0) 30
('casememo-v4-validity-lower-short.py', 0) 30
('casememo-v7-value-lower-nonascii.py', 0) 30
('casememo-v8-value-casefold-nonascii.py', 0) 30
```

## Commands

Working directory: `/home/vgpnk/Projects/shokunin/kake-shokunin`. `TMPDIR=/fast/scratch/hyaku/kake-r44/ScoutSeedStability`.

Single probe (seed 1, casememo-v3), wall 0.166s, exit 0:

```
python3 -B .ufo/waves/round-44/c44_probe.py --root . --class G6 --tool-file .ufo/waves/round-44/controls-r43/casememo-v3-validity-lower.py --seed 1
```

```json
{
 "probe": "G6",
 "seed": 1,
 "units": 100,
 "values": 200,
 "ref41Exit": 0,
 "candExit": 0,
 "ref41OutSha256": "67ef7c1ddb222df5a8d5e4defee48e64d7c9cd34310611c2db7f19e390314031",
 "candOutSha256": "67ef7c1ddb222df5a8d5e4defee48e64d7c9cd34310611c2db7f19e390314031",
 "equal": true
}
```

Sweep (same probe, four controls, seeds 1..30, 8 workers). Probe exit 1 = witness; exit 0 = no witness.

```
python3 -B /fast/scratch/hyaku/kake-r44/ScoutSeedStability/sweep_seeds.py f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d
```

Per-seed line form (all 120 identical in exit/equal/stable; full log in scratch `sweep.jsonl`, sha256 `6ee64739568bc2fcee87ed4c18259b3455cd34b8daf68aedf4c551929a9788d0`):

```
<control> seed=<1..30> exit=0 equal=True stable=True
```

Decisive summary (verbatim):

```
WROTE /fast/scratch/hyaku/kake-r44/ScoutSeedStability/sweep.jsonl N 120
ENDSHA f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d
RATE casememo-v3-validity-lower.py witnessed=0/30 nowitness=30 probe_error=0 unstable=0 rate=0.0000
RATE casememo-v4-validity-lower-short.py witnessed=0/30 nowitness=30 probe_error=0 unstable=0 rate=0.0000
RATE casememo-v7-value-lower-nonascii.py witnessed=0/30 nowitness=30 probe_error=0 unstable=0 rate=0.0000
RATE casememo-v8-value-casefold-nonascii.py witnessed=0/30 nowitness=30 probe_error=0 unstable=0 rate=0.0000
```

## Before-data witness rates

| control | witnesses | rate | vs 90% |
|---|---|---|---|
| casememo-v3 | 0/30 | 0% | below, but zero witnesses not a flaky witness |
| casememo-v4 | 0/30 | 0% | same |
| casememo-v7 | 0/30 | 0% | same |
| casememo-v8 | 0/30 | 0% | same |

Fixed-G6 sweep over seeds 1..30: **unrun** (fix had not landed; hash unchanged).

## Files written

- `.ufo/waves/round-44/w2/ScoutSeedStability.md` (this report)
- `/fast/scratch/hyaku/kake-r44/ScoutSeedStability/g6_fold_pairs.py.snapshot`
- `/fast/scratch/hyaku/kake-r44/ScoutSeedStability/sweep_seeds.py`
- `/fast/scratch/hyaku/kake-r44/ScoutSeedStability/sweep.jsonl`

## Blockers

Correct-G6 seed-luck attack blocked: pre-fix sha256 `f4f13a7682ad27117e398f8b987aab68c92f34ccfa82813c0dd3636b8d2a536d` still witnesses 0/4 (measured 0/30 per control).
