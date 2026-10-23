KILLED — 8/8 one-member mutants of the round-42 build's query/fragment/path URL validation were killed by counter v4 (met=false, behavioural equality failure; every timing ratio <=1.37, so no kill rests on speed).

Base artifacts (all read-only git extraction, exit 0)
- build: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 020bc4574729ed674299f6cab02faac1582d9464:scripts/sitemap_audit.py` -> /fast/scratch/hyaku/kake-r43/MutBuildQF/build.py, sha256 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021 (= C1 target).
- ref41: `git show 1ef7a0e95f6884dd113fe583a997c633fe330ddd:scripts/sitemap_audit.py` -> ref41.py, sha256 50287ac6de5600ab1fca5a4cb77d9f3b8a170ad0a63f287512f9403bdb1dde7d (= counter REF41_SHA).
- counter v4 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-43/c43_count_v4.py sha256 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab.

Scoring command per mutant (no --seed; exit 1 each; ~30-41 s; max 3 concurrent):
`timeout 900 prlimit --as=8000000000 -- python3 -B .ufo/waves/round-43/c43_count_v4.py --root . --tool-file /fast/scratch/hyaku/kake-r43/MutBuildQF/<mutant>.py --label MutBuildQF-<mutant> --out /fast/scratch/hyaku/kake-r43/MutBuildQF/receipts/<mutant>.json`
Differential pre-check (exit 0): `timeout 300 python3 -B diffprobe.py` — 10,325 values (fixed + counter cases_a/cases_d, seeds 0-2); build.py vs ref41 disagreements = 0; every mutant below differs from ref41 on counter-shaped values. `python3 -B -c py_compile` ok for all 8.

| mutant | line | one-member change | sha256 | receipt equalRuns / met | witness (_parse_url: ref41 vs mutant) |
|---|---|---|---|---|---|
| M1pathskip | 175 | `_path_ok`: `masked.find(b"\x01", at)` -> `at + 1` (skips first byte after "/") | 42cc770f…5d04d1 | 3/11, false | `http://example.com/ a/b` reject vs accept |
| M2fragstart | 206 | `_scan` fragment region `fragment_start + 1` -> `fragment_start` ("#" enters fragment class) | 4fe7b00c…aab44d | 3/11, false | `http://example.com/?a#b` accept vs reject |
| M3qclass | 204 | `_scan` query class `_TABLE_QUERY` -> `_TABLE_PCHAR` (drops "/" and "?") | 54bef894…381656 | 5/11, false | `http://example.com/?a/b` accept vs reject |
| M4qendsteal | 253 | path branch `query_end = size if fragment_start < 0 else fragment_start` -> `query_end = size` | ab32e600…15cd29 | 6/11, false | `http://example.com/?a#b` accept vs reject |
| M5nfrag | 260 | question branch `fragment_start = mark if mark >= 0 else -1` -> `-1` (query swallows "#") | a273f2d1…74a9b3 | 8/11, false | `http://example.com?q#f` accept vs reject |
| M6pathlead | 172 | `_path_ok` `if segment[at] != 0x2F` -> `== 0x2F` | 07e79a7a…83dbc52 | 0/11, false | `http://example.com/a` accept vs reject |
| M7pctarity | 134 | `_BAD_PCT_RE` `%(?![0-9A-Fa-f]{2})` -> `{1}` (percent triplet arity) | 5cb7df93…0354fa | 2/11, false | `http://example.com/?a%4` reject vs accept |
| M8pctaccept | 159 | `_region_ok` malformed-pct early `return False` -> `return True` | 11eb988f…da6d3f | 3/11, false | `http://example.com/?a%4` reject vs accept |

All witnesses verified by importing ref41.py and the mutant and calling `_parse_url` (exit 0); mutants M1-M6 are line 175/206/204/253/260/172 of build.py, M7/M8 line 134/159. Receipts: /fast/scratch/hyaku/kake-r43/MutBuildQF/receipts/{M1pathskip,M2fragstart,M3qclass,M4qendsteal,M5nfrag,M6pathlead,M7pctarity,M8pctaccept}.json; each records seed, equalRuns, equalValues, ratios, met.

Findings
- Kills are behavioural, not timing: all eight receipts have 5 ratiosExact keys with max 1.37 (<2.0), so `met=false` comes only from equalRuns<11 (counter line 1062 predicate).
- Runs that differed: M1 A,C,D,E,F,T1,T2,T3; M2 A,C,D,E,F,T1,T3,T5; M3 A,C,D,E,F,T1; M4 A,D,E,F,T3; M5 A,D,E (closest survivor, 8/11); M6 all 11; M7 A,C,D,E,F,T1,T2,T3,T5; M8 A,C,D,E,F,T1,T3,T5. Query/fragment shapes in run A and whole-value edits in run D carry the load; run B (brackets) never detects a query/fragment mutant, as expected.
- My receipt runs show ref41Exit=2 for A-F because each equality manifest carries at least one deliberately invalid sitemapUrl (build.py:557-559 check_invalid; exit 2). Equality is still over the full per-check JSON + exit (counter 1022-1032), so a URL-grammar difference changes output; this is an observation about the equality surface, not a counter defect.
- No survivor: no coverage gap demonstrated for one-member defects in this area; C1's v4 strength in the query/fragment/path class is CONFORMANT with 8 independent mutants (incl. the percent-triplet branch and two fragment/query boundary conditions).

Per checked statement
- "counter v4 sha256 1c3b9661…fe8eab" — holds (sha256sum of the frozen path).
- "target build 020bc457… tool sha256 914ebdee…cd021" — holds (git show + sha256sum).
- Freeze "build-1..3 met 11/11" — holds (verification/freeze/build-{1,2,3}.json: equalRuns 11/11, met true).
- Freeze "ref41-base not met" — holds: equal 11/11, met false, ratios T1 4.21, T5 7.05 (receipts read; the wave brief's 4.27/8.68 figures differ, same not-met verdict).
- Live-seat controls, freshness sweep, registry count — not exercised by this item.

Restoration / bounds evidence
- build.py sha256 before and after all work: 914ebdee7bcb25e877bed2bc19cd15642d0373f1526a9535123e3e0fc02cd021 (unchanged); mutants are sandbox copies, so no bytes needed restoring.
- Writes only in /fast/scratch/hyaku/kake-r43/MutBuildQF/ (8 mutants, ref41.py, build.py, diffprobe.py, 8 receipts) and this report; no lane file, git index, jj state, or sibling lane touched; no subagents; no tool installs (none needed).
