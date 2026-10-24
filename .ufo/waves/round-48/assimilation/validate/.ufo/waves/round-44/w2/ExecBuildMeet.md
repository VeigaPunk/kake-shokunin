# ExecBuildMeet — round 44 wave 2

Axis: **operability** (lane axes: operability, freshness).

Seat item: attack the held build's 3/3 claim without editing the lane. Build a 1-row controls
TSV in the seat scratch dir (the `buildscheme-M5` row copied verbatim from
`.ufo/waves/round-44/controls-27.tsv`), run the frozen driver
`.ufo/waves/round-44/c44_audit.py` with `--classes v5 --expect blind --build-rev 020bc457
--build-runs 3 --workers 1 --out <scratch>/buildmeet.json`, three times, twice under CPU load
(three `yes > /dev/null &` hogs), and report every `build#` line verbatim plus whether any
timing ratio approaches the 2.0 bound.

**Verdict: the attack did not break the claim.** Across three invocations (9 build receipts)
plus two extra contention probes (6 more receipts) — 15 build receipts, 15 distinct random
seeds — every build run met the full v5 predicate: `met=True`, `equalRuns=21/21`. The highest
single timing ratio observed anywhere was **1.3684**, i.e. 68.4% of the 2.0 bound; the smallest
headroom to the bound was **0.6316**. No ratio comes near 2.0, under load or without.

The one non-zero exit (`audit-exit=1`) is **not** a build failure. It is the `--expect blind`
expectation interacting with the single control row: `blind` requires every control to be
`met == True` **and** `witnessed == 0`, but `buildscheme-M5` is a mutant that the v5 counter
catches via class `G2`, so `met=False` / `caughtBy=G2` / `witnessed=1`. A cross-check run of
the identical invocation with `--expect witnessed` (the expectation that matches a 1-row
class-caught control) exits **0** with `ok=True` and `build_met=3/3`. The build claim itself
is `build_met=3/3` in every single invocation.

## Lane state confirmed before running

```text
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && git rev-parse --verify '020bc457^{commit}'
020bc4574729ed674299f6cab02faac1582d9464
$ git log --oneline -1 020bc457
020bc45 round-42: build — URL check rewritten as a byte-table scanner (ExecBuildIndependent), comment corrected (routed defect 3), ten r42 guard fixtures (ExecBuildRegex); selftest 235
$ for r in 1ef7a0e95f6884dd113fe583a997c633fe330ddd 8eb121c81ffebada064eefcabcd94dd2303d646f 020bc457; do git rev-parse --verify "$r^{commit}"; done
1ef7a0e95f6884dd113fe583a997c633fe330ddd
8eb121c81ffebada064eefcabcd94dd2303d646f
020bc4574729ed674299f6cab02faac1582d9464
$ sha256sum .ufo/waves/round-44/controls-r43/buildscheme-M5-default-port-https80.py
0fc6091351c1e080b90df1f96ef2558d9f5ada2dce473109d0fe805d07fe5889  .ufo/waves/round-44/controls-r43/buildscheme-M5-default-port-https80.py
$ bwrap --ro-bind /usr /usr --symlink usr/lib /lib --symlink usr/lib64 /lib64 --symlink usr/bin /bin --unshare-all --die-with-parent --clearenv /usr/bin/true; echo "bwrap-exit=$?"
bwrap-exit=0
```

Both reference revisions the frozen counter hashes (`REF41_REV 1ef7a0e…`, `BASE40_REV 8eb121c…`)
resolve in this repo, so the counter's `CannotEvaluate` path was not taken. The 1-row TSV's
recorded sha256 matches the control file on disk byte-for-byte, so the control row was scored,
not skipped for a hash mismatch.

Build-byte identity (the receipt's `toolSha256` is the tool bytes the counter actually
measured, taken from the `git show` of the build rev):

```text
HEAD=18cb2c2
blob-at-rev: 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021  -
worktree:    914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021  scripts/sitemap_audit.py
receipt toolSha256: 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021
receipt counterSha256: 5cedaa3b9f918979 ratioLimit: 2.0 reps: 5
```

The tool bytes at `020bc457` are identical to the current worktree `scripts/sitemap_audit.py`,
and the receipts' `toolSha256` equals both — so the held build under attack is the build the
receipts claim. Counter sha `5cedaa3b9f91…` is identical across all invocations (frozen counter,
not edited).

## Exact commands

The 1-row controls TSV (scratch, header row kept so the driver's parser sees the same shape):

```text
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && mkdir -p /fast/scratch/hyaku/kake-r44/ExecBuildMeet/{run1,run2,run3} && \
  { head -1 .ufo/waves/round-44/controls-27.tsv; grep -P '^buildscheme-M5\t' .ufo/waves/round-44/controls-27.tsv; } \
  > /fast/scratch/hyaku/kake-r44/ExecBuildMeet/buildscheme-M5.tsv
```

`cat -A` of the resulting TSV (tab-separated, exactly one data row plus the frozen header):

```text
# name^Ifamily^Iclass^Icontrol file (repo-relative)^Isha256^Iround-43 seat report$
buildscheme-M5^Idefault_port^IG2^I.ufo/waves/round-44/controls-r43/buildscheme-M5-default-port-https80.py^I0fc6091351c1e080b90df1f96ef2558d9f5ada2dce473109d0fe805d07fe5889^Iw1/MutBuildScheme.md$
```

The audit command (run verbatim from the repo root, three times — run 1 with no load, runs 2 and
3 with three `yes > /dev/null &` hogs):

```text
$ python3 -B .ufo/waves/round-44/c44_audit.py \
    --root . \
    --controls /fast/scratch/hyaku/kake-r44/ExecBuildMeet/buildscheme-M5.tsv \
    --counter .ufo/waves/round-44/c44_count_v5.py \
    --classes v5 \
    --expect blind \
    --build-rev 020bc457 \
    --build-runs 3 \
    --workers 1 \
    --out /fast/scratch/hyaku/kake-r44/ExecBuildMeet/buildmeet.json
```

The three-invocation driver (`/fast/scratch/hyaku/kake-r44/ExecBuildMeet/run_attack.sh`) spawns
the hogs for runs 2 and 3 (`for i in 1 2 3; do yes > /dev/null & HOGS="$HOGS $!"; done`),
kills them after each run, and copies each run's `buildmeet.json` + `build-{1,2,3}.json` into
`run-N/` so receipts are not overwritten by the next invocation (the driver writes
`build-N.json` beside `--out`).

## Decisive output — all three runs, verbatim

Full driver log: `/fast/scratch/hyaku/kake-r44/ExecBuildMeet/driver.log`.

```text
=== RUN 1 (load=none) start 2026-10-23T23:02:40-03:00 ===
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=False counter=5cedaa3b9f91
  buildscheme-M5       G2         met=False caught=G2
  witnessed-by-class buildscheme-M5 caughtBy=G2
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
audit-exit=1
=== RUN 1 end 2026-10-23T23:03:40-03:00 ===
=== RUN 2 (load=3-hogs) start 2026-10-23T23:03:41-03:00 ===
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=False counter=5cedaa3b9f91
  buildscheme-M5       G2         met=False caught=G2
  witnessed-by-class buildscheme-M5 caughtBy=G2
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
audit-exit=1
=== RUN 2 end 2026-10-23T23:04:41-03:00 ===
=== RUN 3 (load=3-hogs) start 2026-10-23T23:04:42-03:00 ===
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=False counter=5cedaa3b9f91
  buildscheme-M5       G2         met=False caught=G2
  witnessed-by-class buildscheme-M5 caughtBy=G2
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
audit-exit=1
=== RUN 3 end 2026-10-23T23:05:36-03:00 ===
ALL RUNS DONE
```

Every `build#` line across the three runs is `met=True equal=21/21`. The summary line reads
`build_met=3/3` in every run.

### `--expect witnessed` cross-check (identical invocation, expectation matched to a 1-row class-caught control, under 3 hogs)

```text
AUDIT kake-r44 classes=v5 classKeys=G1,G2,G3,G4,G5,G6,G7,G8,G9,G10 witnessed=1/1 notMet=1 build_met=3/3 ok=True counter=5cedaa3b9f91
  buildscheme-M5       G2         met=False caught=G2
  witnessed-by-class buildscheme-M5 caughtBy=G2
  build#1 met=True equal=21/21
  build#2 met=True equal=21/21
  build#3 met=True equal=21/21
audit-exit=0
```

`ok=True`, exit 0. This isolates the `audit-exit=1` in the `--expect blind` runs to the
expectation mismatch (a caught mutant cannot satisfy `blind`), not to the build.

## Timing ratios against the 2.0 bound

`ratio = median(candidate CPU) / median(round-40 CPU)` per timing shape; the predicate requires
all five ratios `<= 2.0` (counter `RATIO_LIMIT = 2.0`). Values below are the exact
`ratiosExact` from each build receipt, with the run's maximum ratio and its headroom to 2.0.

```text
receipt               met    equal    max ratio  headroom to 2.0   per-shape (T1,T2,T3,T4,T5)
run-1/build-1.json    True   21/21    1.2796     0.7204             1.025, 1.1863, 1.2796, 1.2379, 1.1140
run-1/build-2.json    True   21/21    1.2885     0.7115             1.0092, 1.1534, 1.2540, 1.2885, 1.1490
run-1/build-3.json    True   21/21    1.2774     0.7226             0.9930, 1.2126, 1.2554, 1.2774, 1.1544
run-2/build-1.json    True   21/21    1.3494     0.6506             0.9425, 1.2577, 1.3494, 1.1658, 1.1144
run-2/build-2.json    True   21/21    1.3173     0.6827             0.8881, 1.1480, 1.2183, 1.3173, 1.1097
run-2/build-3.json    True   21/21    1.3014     0.6986             0.9502, 1.0666, 1.1993, 1.3014, 1.1744
run-3/build-1.json    True   21/21    1.3027     0.6973             1.0303, 1.1678, 1.3027, 1.2704, 1.1420
run-3/build-2.json    True   21/21    1.3163     0.6837             1.0226, 1.2087, 1.3163, 1.2539, 1.1514
run-3/build-3.json    True   21/21    1.3684     0.6316             0.9840, 1.1469, 1.3684, 1.2540, 1.1110
```

**No ratio approaches the 2.0 bound.** The worst ratio anywhere in the three required runs is
**1.3684** (run 3, build#3, shape T3) — 68.4% of the bound, headroom **0.6316**. The worst
shape is consistently **T3** (the largest adversarial `loc` set), which is the shape already
known to be the build's slow case.

### Extra contention probes (beyond the three required runs)

To push the bound harder than the specified 3 hogs, two more instrumented invocations were run
and their receipts preserved (`loadprobe2/` and the 12-hog stress run):

```text
loadprobe2/build-1.json  (3 hogs)   met=True equal=21/21  max=1.3647  headroom=0.6353
loadprobe2/build-2.json  (3 hogs)   met=True equal=21/21  max=1.3540  headroom=0.6460
loadprobe2/build-3.json  (3 hogs)   met=True equal=21/21  max=1.3428  headroom=0.6572
build-1.json (12-hog stress)        met=True equal=21/21  max=1.3473  headroom=0.6527
build-2.json (12-hog stress)        met=True equal=21/21  max=1.2793  headroom=0.7207
build-3.json (12-hog stress)        met=True equal=21/21  max=1.2539  headroom=0.7461
```

Aggregate over all 15 build receipts (9 required + 6 probes):

```text
receipts=15  unique_seeds=15  all_met=True  all_equal_21_21=True
overall_max_ratio=1.3684  headroom_to_2.0=0.6316  pct_of_bound=68.4%
```

Load was demonstrably real during the loaded runs (the counter measures **CPU time**, not wall
clock, so the hogs contend rather than merely delay):

```text
hogs= 267720 267721 267722
loadavg-before: 14.44 10.86 5.15 24/11986 268429
nproc=32
...
loadavg-after: 19.26 12.67 6.09 16/11992 294164
hogs killed
```

and the 12-hog stress probe:

```text
hogs=12 nproc=32 loadavg-before: 19.40 13.02 6.31 28/12045 297825
...
loadavg-after: 26.98 16.76 8.13 24/11727 324081
hogs killed
```

Ratios did **not** scale with load: the 12-hog run produced *lower* maxima (1.2539–1.3473) than
the lightly loaded runs (up to 1.3684). The ratio is a median-of-five CPU-time quotient measured
alternately for candidate and round-40 base within the same process, so contention inflates both
sides; the observed spread (1.2539–1.3684 across 15 receipts, ~9% band) is run-to-run noise, not
load pressure. The gap to 2.0 (≥0.63, ≥31%) is an order of magnitude larger than that noise band.

### Seed independence

All 15 build receipts carry distinct random seeds (the counter draws `os.urandom` per run and
records it):

```text
run-1/build-1.json  seed=128003007208871   run-2/build-1.json  seed=246424414511758
run-1/build-2.json  seed=230036935438099   run-2/build-2.json  seed=26368873820354
run-1/build-3.json  seed=170576357116830   run-2/build-3.json  seed=246894392236458
run-3/build-1.json  seed=261057614705395   loadprobe2/build-1.json  seed=(distinct)
run-3/build-2.json  seed=233569521489448   loadprobe2/build-2.json  seed=(distinct)
run-3/build-3.json  seed=46174296171731    loadprobe2/build-3.json  seed=(distinct)
build-1.json (stress) seed=184932013406751
build-2.json (stress) seed=89510727534133
build-3.json (stress) seed=170937920614963
unique_seeds=15
```

So the 3/3 is not a seed artifact of one lucky draw; it holds across 15 independent draws, each
covering 21 runs (A–F, G1–G10, T1–T5) for a total of 315 scored run-pairs, all equal.

## Files written

Lane (this seat's exclusive report path only — no lane source, no frozen file, no `MANIFEST.json`,
no templates, no fleet scripts, no route tables):

- `.ufo/waves/round-44/w2/ExecBuildMeet.md` (this report)

Scratch (`/fast/scratch/hyaku/kake-r44/ExecBuildMeet/`):

- `buildscheme-M5.tsv` — the 1-row controls TSV (frozen header + verbatim `buildscheme-M5` row)
- `run_attack.sh` — three-invocation driver (load on runs 2 and 3, per-run receipt copies)
- `loadprobe.sh`, `loadprobe2.sh`, `stress.sh` — instrumented contention probes (3-hog, 3-hog
  with preserved receipts, 12-hog)
- `driver.log` — full verbatim stdout of the three required runs
- `run-1.txt`, `run-2.txt`, `run-3.txt` — per-run stdout
- `run-1/`, `run-2/`, `run-3/` — per-run `buildmeet.json`, `build-{1,2,3}.json`, `stdout.txt`
- `loadprobe2/` — `buildmeet.json`, `build-{1,2,3}.json`, `stdout.txt`
- `build-1.json`, `build-2.json`, `build-3.json`, `buildmeet.json`, `buildmeet-loadprobe.json`,
  `buildmeet-stress.json`, `loadprobe.txt`, `stress.txt` — top-level probe outputs
- `tools/` — the driver's per-control receipt directory (side effect of `--out`'s dirname)

No file in `.ufo/waves/round-44/` was modified except the new `w2/ExecBuildMeet.md`. The frozen
artifacts (`c44_count_v5.py`, `c44_audit.py`, `controls-27.tsv`, `controls-r43/*`, `c44_placebo.py`)
were read only; the counter sha `5cedaa3b9f91…` is byte-identical before and after all runs.
No tools were installed. No build, lint, or format commands were run (the wave's gate is the
parent's); the only commands executed were the audit invocations and read-only inspection.

## Risks / blockers

No blocker. Two observations the parent may want to weigh:

1. **`--expect blind` cannot succeed with a class-caught control row.** `blind` requires
   `met == True` for every control and `witnessed == 0`; `buildscheme-M5` is caught by class
   `G2`, so the exit code is 1 regardless of the build. The build signal is the `build_met=3/3`
   field and the `build#` lines, both clean in every invocation; the `--expect witnessed`
   cross-check exits 0. Anyone reading only the exit code of a `--expect blind` run would
   misread it as a build failure.
2. **Timing headroom is wide but the margin is not shape-independent.** All 15 receipts peak on
   shape **T3** (1.2539–1.3684) while T1 stays ≤1.098. If T3's workload grows, the 2.0 bound
   is the constraint that would bind first; today the worst observed value uses 68.4% of it.

Dead ends: the first load probe's `build-{1,2,3}.json` receipts were overwritten by the
subsequent stress run, because the driver writes `build-N.json` beside `--out` and both probes
used the same scratch root. Fixed by re-running the 3-hog probe with `--out` in its own
subdirectory (`loadprobe2/`); the stress receipts were the ones preserved at top level. The
overwritten probe's *stdout* was already captured verbatim in the transcript above
(max ratios 1.3621 / 1.4681 / 1.2650, all `met=True`), and its re-run reproduced the same
values within the observed noise band (1.3647 / 1.3540 / 1.3428).
