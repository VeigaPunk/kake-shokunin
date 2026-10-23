# Round 42 wave 2 — MutBuildPercent (mutation tester, falsify)

Verdict: NOT MET — no mutant met the predicate. All 6 single-member percent-rule mutants of the landed build were killed by counter v3; the pristine build met (baseline). Counter's power to catch one-member changes of the percent rule HOLDS on the exercised set. No witness searched (no meeting tool).

## Baseline (pristine build)
- Tool: /fast/scratch/hyaku/kake-r42w2/MutBuildPercent/build.py, sha256 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021 (copy of scripts/sitemap_audit.py; restored after mutants, hash unchanged).
- Command: `timeout 900 prlimit --as=8000000000 -- python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-42/c42_count_v3.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --tool-file build.py --label MutBuildPercent-build --out build.json`
- Exit 0 (met). Receipt: seed 200939442614690, equalRuns 10/10, ratios T1 1.051 T2 1.383 T3 1.419 T4 1.219 T5 1.158 (all ≤2.0x base40), met true.

## Mutants (all scratch copies in /fast/scratch/hyaku/kake-r42w2/MutBuildPercent/, each one single-member change in the percent rule area)
| mutant | sha256 | one-line change | result | first unequal run | seed | equalRuns | ratios (T1..T5) |
|---|---|---|---|---|---|---|---|---|
| m1.py | de2b85fc5db0f8de1e94417ab78f057a56caa693a80c8a67384ddcc86c22894d | `_BAD_PCT_RE` hex class drops `a-f` (line 134) | exit 1, NOT met (killed) | A | 236637158054267 | 1/10 | 0.911 0.828 0.972 1.216 0.782 |
| m2.py | 835412de2b47440dffaade671e4ba03965aa1af6bcbe806c66c0cdfc45e6b174 | `_REGNAME_ASCII` drops `%` table byte (line 121) | exit 1, NOT met (killed) | A | 273271736285484 | 7/10 | 1.024 1.35 1.312 1.289 1.053 |
| m3.py | aa246008548896c5cdcaebba154a4652b9fffbc7e40c0a10c76fe2842dcde9fd | `_path_ok` bad-percent guard removed (lines 166-167) | exit 1, NOT met (killed) | A | 130395364097987 | 2/10 | 0.994 1.315 1.276 1.168 0.9 |
| m4.py | 6a6ac372679ebb8952df839087578faccae50b7cee3c471462bfc87f8a312181 | `_BAD_PCT_RE` quantifier `{2}`→`{1}` (line 134) | exit 1, NOT met (killed) | A | 175090146506297 | 2/10 | 1.07 1.271 1.366 1.329 1.242 |
| m5.py | 4ddaa6da4ccd6452061849d4f43fe116eb4bf4ed650e788671be05468e1175a3 | `_run_end` bad-percent cut block removed (lines 146-150) | exit 1, NOT met (killed) | A | 210250386697545 | 7/10 | 1.066 1.314 1.532 1.034 1.052 |
| m6.py | 11eb988ff546f961cbf415a46ef2e0cb79a2f631028d07d3e9a252f810da6d3f | `_region_ok` guard flipped to return True on broken triplet (line 159) | exit 1, NOT met (killed) | A | 14813549075080 | 2/10 | 1.057 1.225 1.477 1.142 1.541 |

For m1-m6 command identical to baseline with `--tool-file mN.py --label MutBuildPercent-mN --out mN.json`; all exit 1 (predicate not met), checked at ≤3 concurrent per seat, each under `timeout 900` + `prlimit --as=8000000000`.

## Detector sanity
- Local differential probe (`_parse_url` vs tip41, 18 percent-bearing values): build diffs 0; every mutant showed ≥1 divergence, e.g. m1 on "http://h.com/a%7eb/" (valid lowercase triplet rejected), m2 on "http://h%41.com/", m3 on "http://h.com/a%4Gb/", m4 on "http://h.com/a%4Gb/", m5 on "http://u%zb@h.com/", m6 on "http://h.com/?q=%G". Every mutant is a real behavioral change, so its kill count is a genuine kill, not a no-op.
- Run A (counter-v2 case shapes with inserted ASCII/percent units) caught all six first; T-run equality also failed for m1/m3/m4/m6.

## Claims checked
- "Counter v3 catches one-member changes of the landed build's percent rule (_BAD_PCT_RE hex case, application sites, table bytes)": HOLDS — 6/6 mutants killed, baseline met. No surviving mutant found; no witness value exists for any tool here (none met).
- Restoration: build.py hash identical before/after; only sandbox files mutated; no lane repo file touched (read-only git); no tools installed (no installs needed).

## Files
- Receipts: /fast/scratch/hyaku/kake-r42w2/MutBuildPercent/{build,m1..m6}.json; run logs *.run.log.
