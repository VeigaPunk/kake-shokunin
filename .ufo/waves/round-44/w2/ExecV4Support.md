# ExecV4Support — re-produce the v4 supporting control

Seat: `kake-r44.ExecV4Support` (executor, wave 2, lane kake-shokunin, axis operability).
Lane repo: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Scratch: `/fast/scratch/hyaku/kake-r44/ExecV4Support/`.

## Axes

- **operability (target):** does the frozen v4 supporting control reproduce, and what is the v4 met count j/27?
- **freshness (secondary):** do the two attempt-1 divergences (`buildscope-m5` on run D, `repeat-depth-deep` on run C) reproduce under fresh seeds, or are they seed-luck?

## Decisive command output (verbatim)

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes v4 --expect blind --workers 4 --out .ufo/waves/round-44/verification/claim/v4-support.json > .ufo/waves/round-44/verification/claim/v4-support.txt 2>&1; echo exit=$?

real	3m13.488s
user	15m22.862s
sys	1m25.195s
exit=1
```

`claim/v4-support.txt` (the audit's own stdout, verbatim):

```
AUDIT kake-r44 classes=v4 classKeys=- witnessed=0/27 (no class runs; witnessed=0 by construction) notMet=1 build_met=0/0 ok=False counter=5cedaa3b9f91
  portlen-v1           G1         met=True  caught=-
  portlen-v5           G1         met=True  caught=-
  buildscheme-M5       G2         met=True  caught=-
  buildscope-m5        G3         met=True  caught=-
  buildscope-m4        G4         met=True  caught=-
  headtail-V1          G5         met=True  caught=-
  headtail-V2          G5         met=True  caught=-
  headtail-V7          G5         met=True  caught=-
  prefixcache-p48      G5         met=True  caught=-
  casememo-v3          G6         met=True  caught=-
  casememo-v4          G6         met=True  caught=-
  casememo-v7          G6         met=True  caught=-
  casememo-v8          G6         met=True  caught=-
  repeat-len-band      G7         met=False caught=T5
  repeat-depth-band    G7         met=True  caught=-
  repeat-defpos-band   G7         met=True  caught=-
  repeat-depth-deep    G7         met=True  caught=-
  repeat-defpos-late   G7         met=True  caught=-
  hosttable-A          G8         met=True  caught=-
  hosttable-B          G8         met=True  caught=-
  hosttable-F          G8         met=True  caught=-
  portvalue-digits     G9         met=True  caught=-
  portvalue-digits-67  G9         met=True  caught=-
  portlen-v4           G9         met=True  caught=-
  buildport-m6         G2         met=True  caught=-
  headtail-V4          G10        met=True  caught=-
  headtail-V8          G10        met=True  caught=-
```

Counter identity in that receipt: `counterSha256 = 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc` — the same bytes as attempt 1's
`verification/freeze/control-v4blind.json` (`counterSha256 5cedaa3b9f91…`). `build: []`, `errors: []`,
`classKeys: []`, `witnessed: 0`, `witnessedNames: []`, `notMet: 1`, `ok: false`.

## Answer to the named attack

### 1. v4 met count j/27

**j = 26/27 met** in the decisive run (`metNames` = 26, `notMetNames` = `["repeat-len-band"]`). The audit's
`--expect blind` therefore **fails** (`ok=false`, exit 1): blindness requires *every* control met, and one row is not met.

### 2. Which rows diverge, on which v4 runs

Decisive run (fresh, unseeded — 27 distinct random seeds, one per row):

| row | class | met | diverging v4 run(s) | equalRuns | seed |
|---|---|---|---|---|---|
| `repeat-len-band` | G7 | **False** | **T5** (timing shape, `candRepsEqual 0/5`) | 10/11 | 170775818202126 |

All other 26 rows: `met=True`, `caughtBy=[]`, `equalRuns 11/11`. Every diverging key is a **v4/legacy** key
(`legacyCaught`), never a class key (`classCaught` empty on every row) — consistent with `c44_audit.py`'s
documented v4 semantics ("no class runs; witnessed=0 by construction").

A **second** fresh-seed cohort of the same command (identical flags, `--out` redirected to scratch so the
lane's `claim/` cohort was not clobbered) gives a **different** divergence set:

```
AUDIT kake-r44 classes=v4 classKeys=- witnessed=0/27 (no class runs; witnessed=0 by construction) notMet=2 build_met=0/0 ok=False counter=5cedaa3b9f91
  buildscope-m5        G3         met=False caught=A
  headtail-V8          G10        met=False caught=F
exit=1
```

i.e. **25/27 met**, with `buildscope-m5` diverging on run **A** and `headtail-V8` on run **F** — both v4
equality runs, both stdout-hash differences (`ref41Exit 2` vs `candExit 2`, different output bytes), not timing-only.

So the divergence set is **seed-dependent, not fixed**: cohort 1 → {repeat-len-band/T5}; cohort 2 →
{buildscope-m5/A, headtail-V8/F}; attempt 1 → {buildscope-m5/D, repeat-depth-deep/C}.

### 3. Do the two attempt-1 divergences reproduce with fresh seeds?

Attempt 1's exact seeds were re-run first, then fresh seeds. Both attempt-1 divergences reproduce **exactly at
their recorded seeds** (byte-identical output hashes), and **both also occur under fresh seeds — but on a
different v4 run than attempt 1 recorded**, which is the decisive point.

Attempt-1 seeds (from `verification/freeze/control-v4blind.json`):

```
A1SEED buildscope-m5      attempt1 seed=181346457990762 met=False equalRuns=10/11   caught=D      {"D": {"refExit": 2, "candExit": 2, "refSha": "7bdf3ebd80c57e7e", "candSha": "3406aa7462b7a76d", "reps": null, "values": 2000}}
A1SEED repeat-depth-deep  attempt1 seed=5994504518804  met=False equalRuns=10/11   caught=C      {"C": {"refExit": 2, "candExit": 2, "refSha": "665f50f04fa3c6db", "candSha": "8b0791818af0feba", "reps": null, "values": 656}}
```

These match attempt 1's receipt byte for byte (`freeze/tools/buildscope-m5.json` run D: ref
`7bdf3ebd80c57e7e…` / cand `3406aa7462b7a76d…`; `freeze/tools/repeat-depth-deep.json` run C: ref
`665f50f04fa3c6db…` / cand `8b0791818af0feba…`). So the counter is **deterministic given the seed**.

Fresh-seed sweep, same three rows, seeds 1–10 (`c44_count_v5.py --classes v4 --tool-file … --seed N`):

```
SWEEP buildscope-m5      seed=1    met=False equalRuns=10/11   caught=D
SWEEP buildscope-m5      seed=2    met=True  equalRuns=11/11   caught=-
SWEEP buildscope-m5      seed=3    met=True  equalRuns=11/11   caught=-
SWEEP buildscope-m5      seed=4    met=False equalRuns=9/11    caught=A,D
SWEEP buildscope-m5      seed=5    met=True  equalRuns=11/11   caught=-
SWEEP buildscope-m5      seed=6    met=True  equalRuns=11/11   caught=-
SWEEP buildscope-m5      seed=7    met=True  equalRuns=11/11   caught=-
SWEEP buildscope-m5      seed=8    met=True  equalRuns=11/11   caught=-
SWEEP buildscope-m5      seed=9    met=False equalRuns=9/11    caught=D,E
SWEEP buildscope-m5      seed=10   met=False equalRuns=10/11   caught=D
SWEEP repeat-depth-deep  seed=1    met=True  equalRuns=11/11   caught=-
SWEEP repeat-depth-deep  seed=2    met=True  equalRuns=11/11   caught=-
SWEEP repeat-depth-deep  seed=3    met=True  equalRuns=11/11   caught=-
SWEEP repeat-depth-deep  seed=4    met=True  equalRuns=11/11   caught=-
SWEEP repeat-depth-deep  seed=5    met=True  equalRuns=11/11   caught=-
SWEEP repeat-depth-deep  seed=6    met=True  equalRuns=11/11   caught=-
SWEEP repeat-depth-deep  seed=7    met=False equalRuns=10/11   caught=C
SWEEP repeat-depth-deep  seed=8    met=True  equalRuns=11/11   caught=-
SWEEP repeat-depth-deep  seed=9    met=True  equalRuns=11/11   caught=-
SWEEP repeat-depth-deep  seed=10   met=True  equalRuns=11/11   caught=-
SWEEP repeat-len-band    seed=1    met=True  equalRuns=11/11   caught=-
SWEEP repeat-len-band    seed=2    met=True  equalRuns=11/11   caught=-
SWEEP repeat-len-band    seed=3    met=False equalRuns=10/11   caught=T5
SWEEP repeat-len-band    seed=4    met=False equalRuns=9/11    caught=C,T5
SWEEP repeat-len-band    seed=5    met=True  equalRuns=11/11   caught=-
SWEEP repeat-len-band    seed=6    met=True  equalRuns=11/11   caught=-
```

**Verdict on the two attempt-1 rows:**

- `buildscope-m5` on run **D**: **reproduces** with fresh seeds (seeds 1, 4, 9, 10 — 4 of 10 fresh seeds) and
  exactly at attempt 1's seed 181346457990762. It is therefore **not** seed-luck; the row genuinely diverges
  from the round-41 reference on the v4 corpus at a nontrivial rate (≈40 % of fresh seeds in this sample).
- `repeat-depth-deep` on run **C**: **reproduces** at attempt 1's exact seed 5994504518804 and at fresh seed 7
  (run C, same run key, different byte hashes since the corpus differs). 1 of 10 fresh seeds. It is **rare but
  real**, not a one-off artifact.
- Additionally, `repeat-len-band` diverges on **T5** (a timing shape) at fresh seeds 3 and 4, and on **C** at
  seed 4 — a row attempt 1 never flagged. `headtail-V8` (run F) and `buildscope-m5` (run A) appear in cohort 2.

Determinism check (same seed, separate processes → identical hashes):

```
DET repeat-len-band    rep0 seed=3 met=False equalRuns=10/11 caught=T5 {"T5": {"ref": "ac5773182e329eba", "cand": "cb6722e7000af56a"}}
DET buildscope-m5      rep1 seed=1 met=False equalRuns=10/11 caught=D {"D": {"ref": "e07f4d9492bd5647", "cand": "ff481f643f645ccf"}}
DET repeat-len-band    rep2 seed=3 met=False equalRuns=10/11 caught=T5 {"T5": {"ref": "ac5773182e329eba", "cand": "cb6722e7000af56a"}}
```

and the three cohort seeds re-scored in isolation reproduce their cohort's divergence and hashes exactly:

```
COHORT repeat-len-band    seed=170775818202126 met=False equalRuns=10/11 caught=T5 {"T5": {"ref": "364a9be6d52f8b1d", "cand": "474fe6a79df86660", "reps": "0/5"}}
COHORT buildscope-m5      seed=239945707555883 met=False equalRuns=10/11 caught=A {"A": {"ref": "7499758b216ec25e", "cand": "41759b34c6084fb1", "reps": null}}
COHORT headtail-V8        seed=201002865057097 met=False equalRuns=10/11 caught=F {"F": {"ref": "ce57f20f6be7d3b3", "cand": "fd7643f296b08a27", "reps": null}}
```

### Interpretation the L1 must carry (fact, not adjudication)

The v4 corpus is **not** deterministically blind to these controls. The observed v4 divergence set is
seed-dependent (attempt 1: 2 rows; this wave cohort 1: 1 row; cohort 2: 2 rows), and the attempt-1 rows
reproduce on their own seeds and on fresh seeds. Therefore "the 27 controls are 27/27 met under v4" is **not a
stable property** of this counter/control set — the honest bound is **"j met of 27, j varying with the seed"**,
with `buildscope-m5` and `repeat-depth-deep` known to diverge on v4 runs D and C at the seeds recorded. The
existing `control-v4blind.json` (2/27 witnessed, 25 met, `ok:false`) is therefore not stale evidence but one
sample of a seed-dependent process.

## Pass/fail against the item's named attack

**PASS** — the decisive command was executed verbatim, its exit code and stdout are pasted above, and the
attack's three questions are answered with receipts:

- v4 met count j/27: **26/27** in the decisive run (`repeat-len-band` not met, caught on run T5); **25/27** in a
  second fresh-seed cohort (`buildscope-m5` on A, `headtail-V8` on F).
- Rows diverging on which v4 runs: **all divergence keys observed are legacy v4 keys (A, C, D, E, F, T5)**, never a
  class key; `classCaught` is empty on every row and `witnessed` is 0 by construction in v4 mode.
- Attempt-1 divergences reproduce with fresh seeds: **yes for both**, at their exact recorded seeds with identical
  hashes, and at fresh seeds 1/4/9/10 (`buildscope-m5`→D) and 7 (`repeat-depth-deep`→C).

The audit's own `--expect blind` verdict is **FAIL** (`ok=false`, exit 1) in both cohorts — the v4 blindness
expectation does not hold on these seeds. That is the reproduced result, not a defect in my execution.

## Files written

In the lane repo (`/home/vgpnk/Projects/shokunin/kake-shokunin`):

1. `.ufo/waves/round-44/verification/claim/v4-support.json` — decisive audit receipt (the `--out` of the named command).
2. `.ufo/waves/round-44/verification/claim/v4-support.txt` — decisive audit stdout (the redirect target of the named command).
3. `.ufo/waves/round-44/verification/claim/tools/*.json` — 27 per-row counter receipts written by `c44_audit.py` as a side
   effect of the `--out` path (`claim/`), i.e. the `tools/` sibling directory the driver always populates. **Cohort note:**
   the `claim/tools/` directory is shared with the sibling `after-v5` cohort; the L1 has since re-separated the cohorts into
   `.ufo/waves/round-44/verification/claim/w2-baseline/l1-cohort-recovered/v4-support/tools/` (27/27 of my receipts verified
   there by seed + `classesMode`) and restored `claim/tools/` to the v5 `after-v5` receipts (verified: 27/27 rows of
   `after-v5.json` still match their `claim/tools/<row>.json` seed). My own run's v4 receipts are also copied verbatim to
   `/fast/scratch/hyaku/kake-r44/ExecV4Support/cohort-v4-run1/` (27/27 self-consistent with `v4-support.json`).
4. `.ufo/waves/round-44/w2/ExecV4Support.md` — this report.

In scratch (`/fast/scratch/hyaku/kake-r44/ExecV4Support/`, temp only):

`seed_sweep.py`, `attempt1_seed.py`, `sweep.txt`, `sweep-summary.json`, `sweep-receipts/*.json`,
`a1seed.txt`, `attempt1-seed-summary.json`, `attempt1-seed-receipts/*.json`, `det.txt`, `determinism-receipts/*.json`,
`cohort-seed.txt`, `cohort-seed-repro/*.json`, `v4-support-run2.json`, `v4-support-run2.txt`, `tools/*.json` (cohort 2
receipts), `cohort-v4-run1/` (bundle), `claim-tools-snapshot/`, `run2.nohup`.

Nothing under `.ufo/waves/round-44/` was edited except the receipts the named command itself writes. No frozen file
(`c44_count_v5.py`, `c44_audit.py`, `controls-27.tsv`, `controls-r43/*`, `c44_placebo.py`, `classes/gN_*.py`) was
touched. No commit, no push.

## Blockers / risks

- **None blocking.** One risk to flag: because `c44_audit.py` writes per-row receipts into `<outdir>/tools/`, any two
  seats whose `--out` shares a parent directory clobber each other's receipts. My run's `--out` was the mandated
  `claim/v4-support.json`, so it wrote `claim/tools/`; I have verified the sibling `after-v5` cohort is intact and that
  my own v4 receipts are preserved in the L1's re-separated directory and in scratch. Any future cohort must use a
  distinct `--out` parent.
- Determinism caveat: each control row is scored under its **own** fresh random seed (`c44_audit.py` does not pass
  `--seed`), so a whole-cohort re-run never reproduces a previous cohort's divergence set. The per-row sweep above is
  the only way to compare seeds.

## Commands run (all from the lane repo root, unless a path is given)

```sh
python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv \
  --counter .ufo/waves/round-44/c44_count_v5.py --classes v4 --expect blind --workers 4 \
  --out .ufo/waves/round-44/verification/claim/v4-support.json \
  > .ufo/waves/round-44/verification/claim/v4-support.txt 2>&1; echo exit=$?

# cohort 2 (scratch out, same flags)
python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv \
  --counter .ufo/waves/round-44/c44_count_v5.py --classes v4 --expect blind --workers 4 \
  --out /fast/scratch/hyaku/kake-r44/ExecV4Support/v4-support-run2.json \
  > /fast/scratch/hyaku/kake-r44/ExecV4Support/v4-support-run2.txt 2>&1; echo exit=$?

# per-row fresh-seed sweeps (scratch)
python3 -B /fast/scratch/hyaku/kake-r44/ExecV4Support/seed_sweep.py 1 2 3 4 5 6
python3 -B /fast/scratch/hyaku/kake-r44/ExecV4Support/attempt1_seed.py 7 8 9 10

# single control, single seed (frozen counter, v4 mode)
python3 -B .ufo/waves/round-44/c44_count_v5.py --root . --classes v4 \
  --tool-file .ufo/waves/round-44/controls-r43/buildscope-m5-empty-path.py --seed N --out <receipt>
```

No builds, linters, or tests were run (the wave is still in flight; the parent owns the post-integration gate).
