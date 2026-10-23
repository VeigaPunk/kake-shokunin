# RerunBuildA — attack on L1 build receipts (round 42, wave 2)

Verdict: **L1's build receipts HOLD.** Both reruns of the counter on the lane tip
reproduce every receipt component; nothing overstated, no defect found in scope.

## What I ran
Two independent counter runs, `--revision 721310b19af88d3c43c01647d3ce29d51e6e3b96`
(lane tip), no `--seed` (random seed recorded), into
`/fast/scratch/hyaku/kake-r42w2/RerunBuildA/`:

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-42/c42_count_v3.py \
    --root /home/vgpnk/Projects/shokunin/kake-shokunin \
    --revision 721310b19af88d3c43c01647d3ce29d51e6e3b96 \
    --label RerunBuildA-1 --out /fast/scratch/hyaku/kake-r42w2/RerunBuildA/rr1.json
$ # same with --label RerunBuildA-2 --out .../rr2.json
```
Exit codes: **0** and **0** (runs ran concurrently; ~56 s wall).

## Artifacts (sha256)
- Counter `c42_count_v3.py`: `ce2d5a0ca2c3768ce2b1d7b9a57592817d7f16616ee7fb25989e580a70160acc`
- Tool `scripts/sitemap_audit.py` at both 721310b1 and 020bc457
  (`git show rev:scripts/sitemap_audit.py | sha256sum`): `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021`
- `tip41.py`: `50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d`
- `base40.py`: `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e`

## Results vs L1 receipts (verification/build/c1-v3-020bc457-{1,2,3}.json)
| field | L1 (3 receipts) | rr1 | rr2 |
|---|---|---|---|
| met | true x3 | **true** | **true** |
| counterSha256 | ce2d5a0c… | ce2d5a0c… ✓ | ce2d5a0c… ✓ |
| toolSha256 | 914ebdee… | 914ebdee… ✓ | 914ebdee… ✓ |
| ref41Sha256 | 50287ac6… | 50287ac6… ✓ | 50287ac6… ✓ |
| base40Sha256 | 4de35f8c… | 4de35f8c… ✓ | 4de35f8c… ✓ |
| equalRuns | 10/10 x3 | **10/10** | **10/10** |
| equalValues | 10218/10229/10229 | 10229 | 10229 |
| max ratioExact | 1.396/1.390/1.427 | 1.456 | 1.412 |
| all 10 runs equal | yes | yes | yes |
| candRepsEqual | 5/5 (T1–T5) | 5/5 | 5/5 |
| exit-code pattern A–E/T1–4/T5 | 2/1/2 | 2/1/2 | 2/1/2 |

Per-run output hashes agree between candidate and ref41 on every run (equal=true);
A–E value counts (1434/1200/656/2000) match L1 receipt 1; E varies with seed
(4928 vs 4939) as generated content, consistent with equalValues sums.

## Checks performed / statements
- Median-ratio honesty: for each T shape, `median(candCpu)/median(base40Cpu)` equals the
  recorded `ratiosExact` to 1e-9 (verified on rr1 and L1 receipt 1) — **holds**.
- Tool byte identity across build rev (020bc457) and lane tip (721310b1):
  identical sha256 — **holds**; so rerunning on the tip is a faithful build check.
- All five timing-shape medians ≤ 2.0x base40; max observed across L1+my 5 runs:
  1.456 (well under 2.0) — **holds**.
- Predicate text, ratioLimit 2.0, reps 5 recorded identically — **holds**.

## Residual risk / gaps
- Timing ratios are machine-state dependent; my runs were concurrent (2 processes),
  L1's were sequential — medians still consistent (1.0–1.46 band).
- I did not re-run H1–H5 or the selftest (out of my attack scope); unrun checks
  have not passed here.
- Seeds differ (random by protocol); equal-runs generate from the seed, so exact
  output hashes across receipts are not expected to match — equality is by
  candidate-vs-ref41 within each run, which is 10/10 in all five receipts.

No tool installed (no installs needed).
