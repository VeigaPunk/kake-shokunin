# Round 43 W1 — MutBuildPct: percent-triplet mutants of the build (counter v4)

KILLED: 7/7 single-member mutants in the build's percent-triplet validation were killed by counter v4 (equality half), pristine and restored bytes both met 11/11.

## Setup
- Pristine copy: `git -C <lane> show 020bc4574729ed674299f6cab02faac1582d9464:scripts/sitemap_audit.py` -> `/fast/scratch/hyaku/kake-r43/MutBuildPct/build.py`, sha256 `914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021` (matches required).
- Mutants are separate copies in that directory; `build.py` was never edited, so no restore was needed (hash re-checked after all runs: `914ebdee...cd021`).
- Counter: `timeout 900 prlimit --as=8000000000 -- python3 -B <lane>/.ufo/waves/round-43/c43_count_v4.py --root <lane> --tool-file <mutant> --label MutBuildPct-<n> --out <n>.json` (no `--seed`). 7 mutants scored 3-at-a-time; each run 30-42 s wall.

## Baseline / restored (pristine bytes)
- `baseline.json` label MutBuildPct-baseline: equalRuns 11/11, met true, exit 0, ratios T1 1.041 T2 1.226 T3 1.263 T4 1.195 T5 1.128.
- `restored.json` (same bytes re-scored after the mutation batch): 11/11, met true, exit 0, ratios T1 0.998 T2 1.187 T3 1.240 T4 1.237 T5 1.154.
- Baseline passes => each kill below is attributable to the mutant, not detector failure.

## Mutants (all in /fast/scratch/hyaku/kake-r43/MutBuildPct/, all against build.py:134 unless noted)
| # | file | sha256 | one-member change | receipt | verdict |
|---|---|---|---|---|---|
| m1 | m1_lowerhex.py | de2b85fc5db0f8de1e94417ab78f057a56caa693a80c8a67384ddcc86c22894d | `_BAD_PCT_RE` hex class `[0-9A-Fa-f]` -> `[0-9A-F]` (lowercase hex dropped) | 1/11, met false | KILLED |
| m2 | m2_upperhex.py | 773a6613082cc28456036a8aea25e6660730285d5a1010f4195a73de416e89bc | `_BAD_PCT_RE` hex class `[0-9A-Fa-f]` -> `[0-9a-f]` (uppercase dropped) | 1/11, met false | KILLED |
| m3 | m3_short.py | 6a6ac372679ebb8952df839087578faccae50b7cee3c471462bfc87f8a312181 | `_BAD_PCT_RE` count `{2}` -> `{1}` (short percent form accepted) | 2/11, met false | KILLED |
| m4 | m4_long.py | 6218ecbbd48e8bae5a3d9eb2f12a7926322dd73ebf985fe74ba8b542a9cb94ab | `_BAD_PCT_RE` count `{2}` -> `{3}` (valid triplet rejected; long form) | 1/11, met false | KILLED |
| m5 | m5_fragend.py | 308f04d17840c3785b066729858ffbe07c364d1510288ea5f0b2c7940c2eab0f | build.py:206 fragment span `size` -> `size - 1` (last byte unvalidated: triplet at value end) | 4/11, met false | KILLED |
| m6 | m6_runcut.py | 4152177c0e7f771fa165547aa0277a9c7d992bcdc90d797c9bd71a6d3724e988 | build.py:167 `_path_ok` malformed-triplet branch body `return False` -> `pass` | 2/11, met false | KILLED |
| m7 | m7_pathskip.py | d9356ce20376bd18bcafc1bafb90dcd9c2c5de253355d61d9b91e4f2180cd16c | build.py:159 `_region_ok` malformed-triplet branch body `return False` -> `pass` (query/fragment) | 3/11, met false | KILLED |

All 7 exit 1. Every mutant's five timing ratios lay in 0.787-1.300, i.e. every kill came from the equality half (`equalRuns`), not the 2.0x timing clause. Each mutant differs from the pristine copy by exactly one line (`diff build.py <mutant>` shown; every other byte identical).

## Witnesses (pristine -> mutant, direct probe of `_uri_ok`; no survivor needs one, but each kill's defect is pinned)
- m1: `http://h/x%7ey` True -> False (lowercase triplet wrongly rejected).
- m2: `http://h/a%2Fb` True -> False (uppercase triplet wrongly rejected).
- m3: `http://h/x%4Gy` False -> True; `http://h/x%2` False -> True (truncated form accepted).
- m4: `http://h/x%41y` True -> False; `http://h/%41` True -> False (valid triplet requires 3 hex).
- m5: `http://h/p#q%41` True -> False (valid triplet at fragment end rejected); `http://h/p#q%` False -> True (bare `%` as last byte accepted).
- m6: `http://h/x%4Gy` False -> True (malformed path triplet accepted).
- m7: `http://h/p#q%` False -> True (malformed fragment triplet accepted).
Probe source `/fast/scratch/hyaku/kake-r43/MutBuildPct/probe.py`, `timeout 120 python3 -B probe.py` exit 0.

## Failing equality runs per mutant (from each receipt's `runs[].equal`)
- m1, m2, m4: A B C D E F T1 T2 T3 T5 (only T4 equal).
- m3: A C D E F T1 T2 T3 T5. m6: A C D E F T1 T2 T3 T5.
- m5: A C D E F T1 T3. m7: A C D E F T1 T3 T5.

## Statement checks
- "Counter v4's equality half detects percent-triplet defects of the hex-case class": holds (m1, m2).
- "Counter v4 detects short and long percent forms": holds (m3, m4).
- "Counter v4 detects a triplet validation defect at the end of the value": holds (m5; the fragment slot at end-of-value is exercised, E and F failed).
- "Percent-triplet rejection branches in `_path_ok`/`_region_ok` are load-bearing": holds (m6, m7) — neither is dead code.
- "The frozen build at b49cba9 meets the C1 predicate in this sandbox": holds for this seat's two pristine scans (11/11 twice, exit 0), consistent with the freeze receipts.

## Notes / bounds
- No tool installs or upgrades were made. No network access used. No writes outside the sandbox and this report; lane `jj`/git state untouched; `build.py` byte-identical to the extracted revision.
- No surviving mutant, so no coverage gap in this area was demonstrated by this probe; this is not evidence about other areas.
