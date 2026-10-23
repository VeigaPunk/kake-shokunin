# RerunBuildV2 — counter v2 rerun at the landed build (falsify, wave 2)

Seat: `KakeR41.RerunBuildV2` (fresh leaf; did not participate in wave 1).

## Checked statement

SCORECARD "Round 41 — kill rule (1) fired" section, "Counter v2 (information for
the next round, not C1's instrument)": "Build `0b485431…`, the reference and the
independent build score 1434 on seeds 41101–41103 under v2"
(SCORECARD.md:2809–2817). Scoped claim: the build scores 1434 under counter v2.

## Commands (each with `prlimit --as=4000000000 timeout 900`, run in parallel, ≤3 processes)

```
python3 -B .ufo/waves/round-41/c1_count_v2.py --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6 \
  --out /fast/scratch/hyaku/kake-r41w2/RerunBuildV2/v2-<n>.json    # n = 1,2,3; no --seed (random each run)
```

## Results

| run | receipt | seed | passed | cases | met | counter exit | tool exit |
|-----|---------|------|--------|-------|-----|--------------|-----------|
| 1 | /fast/scratch/hyaku/kake-r41w2/RerunBuildV2/v2-1.json | 269799941353973 | 1434 | 1434 | true | 0 | 2 |
| 2 | /fast/scratch/hyaku/kake-r41w2/RerunBuildV2/v2-2.json | 233879230613843 | 1434 | 1434 | true | 0 | 2 |
| 3 | /fast/scratch/hyaku/kake-r41w2/RerunBuildV2/v2-3.json | 34226982901002 | 1434 | 1434 | true | 0 | 2 |

- `toolSha256` in every receipt: `0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf`
  — exactly the build tool sha256 named in the SCORECARD/goal. The revision
  argument resolves to the landed build commit `eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6`.
- `byField` (all three runs): `loc` 630/630, `sitemapUrl` 804/804.
- `byComponent` (all three runs): userinfo, host, port, path, query, fragment each 239/239.
- `misses`: 0 in every receipt; `oracleInvalid` 608–624 per seed (fresh case mix each run).
- `counterSha256` `53a0ec1b…a45f8d`, `oracleSha256` `cdcac127…0917` (matches the pinned
  PyPI abnf 2.9.1 digest; wheel hash verified locally, sha256sum agrees).
- stderr empty on all runs; wall time ≈2 s per run.
- `toolExit` 2 is expected: the tool exits 2 when any check has findings, and the
  generated manifest deliberately contains oracle-invalid cases.

## Findings

None — no defect found in scope.

## Verdicts on checked statements

- "the build scores 1434 under counter v2 (information)" — **holds**: three fresh
  random-seed runs at the landed revision each pass 1434/1434, `met: true`, exit 0.
- SCORECARD "score 1434 on seeds 41101–41103" — **holds** (my seeds differ; the
  claim is the score, and it reproduces on independent seeds).
- SCORECARD "it is not frozen and decides nothing this round" — consistent; this
  rerun is information only, as is this report.

## Environment / installs

No installs. Prereqs verified: `bwrap` at /usr/bin/bwrap; oracle wheel sha256
`cdcac127…0917` matches `ORACLE_SHA256`; git rev-parse of the revision succeeds.
Lane repo untouched (read-only `git` used by the counter itself).

## Residual risk / verification gaps

- Counter v2 is declared non-frozen; a high score is evidence, not admission — by design.
- Three seeds is a sample; the generator's component buckets are fixed (239 each), so
  coverage breadth is stable, but within-bucket byte placement varies by seed.
- `toolExit` 2 is interpreted, not independently re-derived from the contract here.
