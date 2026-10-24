# ProbeNoise — round-42 wave-1: counter ratio noise band under host load
Axes (godspeed): (a) counter measurement noise — per-shape ratio `median(cand CPU)/median(base40 CPU)` when the candidate is byte-identical to the round-40 tool; (b) load admissibility — that spread under a load the counter must tolerate; (c) predicate headroom — whether the 2.0 limit sits outside the noise.
Change: counter runs with `--tool-file`=round-40 tool on five seeds, =round-41 tool on two seeds; ≤3 concurrent; `uptime`/`/proc/loadavg` before each launch.

**Verdict: HELD.** All 25 byte-identical-candidate ratios (5 seeds × 5 shapes) are in **[0.970, 1.034]**, max |ratio−1| = **0.034**, zero outside [0.8, 1.25]. The 2.0 limit sits ~57× above the noise half-width.

## Commands / exits (all exit 1, stderr empty, no `note`)
```
timeout 900 prlimit --as=8000000000 -- python3 -B \
 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-42/c42_count.py \
 --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file <base40.py|tip41.py> \
 --label <ProbeNoise-B40|ProbeNoise-T41> --seed <seed> \
 --out /fast/scratch/hyaku/kake-r42w1/KakeR42.ProbeNoise/<label>-s<seed>.json
```
driver `run_batch.sh` (≤3 concurrent); receipts `*.json`, stdout `*.stdout`, exit `*.exit`, load log `log.txt`.

| label | tool | seed | exit | equalRuns | met |
|---|---|---|---|---|---|
| ProbeNoise-B40 | base40.py | 42001/42002/42003/42004/42005 | 1×5 | 3/8 each | false |
| ProbeNoise-T41 | tip41.py | 42001, 42002 | 1×2 | 8/8 each | false |

## Tool paths / sha256 (each receipt's `toolSha256` matches)
- `/fast/scratch/hyaku/kake-r42/shared/base40.py` — `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`
- `/fast/scratch/hyaku/kake-r42/shared/tip41.py` — `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`
- `.ufo/waves/round-42/c42_count.py` — `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`

## Ratios (every run)
base40 as candidate (pure noise), seed | T1 T2 T3 T4 T5:
42001 0.989 0.996 1.009 1.018 1.033 · 42002 1.011 1.003 1.021 0.985 1.034 · 42003 0.996 1.008 0.991 1.008 1.017
42004 1.010 0.997 0.994 1.003 0.970 · 42005 1.023 0.998 0.978 0.998 1.005 → min 0.970, max 1.034, 25/25 in [0.8,1.25].
Per-shape seed spread: T1 [.989,1.023] T2 [.996,1.008] T3 [.978,1.021] T4 [.985,1.018] T5 [.970,1.034].
tip41 as candidate (the priced cost): 42001 5.502 2.771 1.397 1.218 9.879 · 42002 5.316 2.819 1.340 1.200 10.718.

## Load averages before each launch (1/5/15-min, running/total)
B40 s42001-42003: 65.10/68.15/57.57 (65/3880, 66/3883, 69/3888) · B40 s42004-42005: 67.28/68.65/58.72 (59/3342, 61/3344) ·
T41 s42001: 67.28/68.65/58.72 (61/3347) · T41 s42002: 78.83/71.52/60.71 (78/3576) · after all done: 75.26/73.39/63.18 (75/3991).
1-min load 65.10→78.83 (mean ≈71.3), 8× CPU count busy: heavy contention throughout.

## Per checked statement
| statement | verdict | evidence |
|---|---|---|
| byte-identical round-40 candidate scores every ratio in [0.8,1.25] on five seeds | holds | 25/25 ratios in [0.970,1.034] |
| so the 2.0 budget is outside noise | holds | max \|r−1\|=0.034 vs limit 2.0 |
| measurement valid under current host load | holds | 7/7 exit 1, empty stderr, no `note`, ratios stable while load ran 65→79 |
| the round-41 tool is the cost the claim must remove | holds | T1 5.32–5.50, T2 2.77–2.82, T5 9.88–10.72 over round-40; equalRuns 8/8 (equality not the failing clause) |
| round-40 tool fails equality (3/8) | holds | 5/5 receipts equalRuns 3/8; failing shapes T1,T5 (`candRepsEqual` 0/5), T2/T3/T4 5/5 |
| a candidate judged "met" on the ratio clause from ratio ≤ 1.25 | overstated | ≤1.25 is inside the noise band (max 1.034); T3 (1.34–1.40) and T4 (1.20–1.22) are near-indistinguishable from noise, so "met" there rests on equality, not measured cost |
| T1/T5 absolute CPU small enough for a stable ratio | wrong | T5 median CPU 0.053–0.064 s/run vs 0.44–0.56 s for T1–T4; T5 carries the widest seed spread (0.970–1.034) and widest per-rep range (base 0.0580–0.0620 s) |

## Findings / risks for the L1
- `c42_count.py` alternating order per rep + 5 reps + median keeps the band tight; per-rep spread inside one shape (T1 s42001 base [0.5240,0.5438], ≈3.8 %) is as wide as the whole across-seed band.
- Operative discriminators are T1 and T5 (round-41 cost 5.3–10.7×, noise floor 0.034); T3/T4 cannot discriminate cost from noise on their own.
- Load 8× oversubscribed throughout, sibling seats running the same counter concurrently (`pgrep`: MutRegexNonAscii, MutRegexStructure, ReviewCounterCode) → upper bound on noise, not a quiet-host lower bound.
- Nothing installed or upgraded (no pacman/uv/npx/cargo); `/usr/bin/bwrap` already present. Writes confined to `/fast/scratch/hyaku/kake-r42w1/KakeR42.ProbeNoise/` (96K) plus this report; no mutating git/jj; no process of mine left running (`ALL DONE` in `log.txt`).
