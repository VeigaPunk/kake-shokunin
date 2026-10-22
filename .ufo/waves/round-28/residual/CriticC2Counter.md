# CriticC2Counter — round 28 attempt 3 residual review of the C2 counter

Seat: KakeR28a3.CriticC2Counter (leaf critic, advisory only). Axis: freshness (C2).
Target: `.ufo/waves/round-28/c2_source_count.py`, blob 1d386368f523, committed only in 84ea5b1
(the declaration commit, before e57f601), so the counter was fixed before the landing it measures.
Sandbox: /fast/scratch/hyaku/kake-r28a3/res/CriticC2Counter/ (clone, counter.py copy sha256 a415dd79…,
mutate.py driver, mutants.json, base-*.json). TMPDIR set there. No lane file written except this report.
Tools: Python 3.14.8, git. No installs or updates.

## Baseline runs (`python3 -B ../counter.py --root . --revision <rev>` in the clone)

| Revision | Exit | Passed | Note |
|---|---|---|---|
| 22c1669c1fec | 1 | 0/4 | every row: no registry row, entry missing, no Gate line |
| b5d423fc0205 | 1 | 0/4 | same as 22c1669 (C1 commit does not touch C2 surfaces) |
| e57f601bd014 | 0 | 4/4 | matches the declared after value |
| 8ecbefe (tip) | 0 | 4/4 | C1 follow-up does not disturb C2 |
| deadbeef | 2 | — | `{"error": "revision not found"}` |

Declared before 0/4 and after 4/4 both reproduce.

## Mutants (each one commit on top of e57f601 in the sandbox, driver `mutate.py`)

| Mutant | Commit | Exit | Passed | Verdict | Failing row: reason |
|---|---|---|---|---|---|
| M1 drop S036 Gate line | 580c787056cc | 1 | 3/4 | killed | S036: no Gate line |
| M2 S037 status mined → queued | d2ba215fc583 | 1 | 3/4 | killed | S037: status 'queued' |
| M3 remove entry `verified-at:` line | 31fc261f0b7a | 1 | 0/4 | killed | all: entry header |
| M4 second curly-quoted excerpt on S038 Gate line | 8635726fb476 | 1 | 3/4 | killed | S038: no Gate line |
| M5 remove every S038 token from entry | 50cf697ee5b3 | 1 | 3/4 | killed | S038: entry does not cite id |
| P1 remove S038 from entry body only, header kept | 79b4fcaf2811 | 0 | 4/4 | survived | — |
| P2 S039 Gate quote replaced by invented text | 3a77e7280809 | 0 | 4/4 | survived | — |
| P3 S039 Gate quote swapped for an S038 sentence | b2f9320e8963 | 0 | 4/4 | survived | — |
| P4 S038 Gate line wrapped in an HTML comment | 3d593298fc2e | 0 | 4/4 | survived | — |
| P5 delete a3/S036.txt and receipts-a3.json | 228e23ca6d21 | 0 | 4/4 | survived | — |
| P6 S036 URL changed to `…/vitals.evil` in row and Gate line | 30a8e89e93f6 | 0 | 4/4 | survived | — |
| P7 S036 quote stretched to 26 words | c5d61f7ec4f3 | 1 | 3/4 | killed | S036: no Gate line |
| P8 straight quotes instead of curly on S036 line | 0db71f3d1da9 | 1 | 3/4 | killed | S036: no Gate line |
| P9 heading `## Gate` renamed `## Gates` | bf5ba267226e | 1 | 0/4 | killed | all: no Gate line |
| P10 entry body emptied below the 3 header lines | 3478e28d83d2 | 0 | 4/4 | survived | — |

All five assigned mutants (M1–M5) are killed, each on the expected row and reason.

## Named gaps (what the counter does not check)

1. Quote truth (P2, P3). It checks quote shape (one curly pair, 1–25 words) only, not that the quote is an
   exact substring of the source text, or of the right source. Closed for e57f601 by my own check:
   all 15 Gate quotes (4 bullets + 11 table cells in round-28.md:33-52) are exact substrings of
   both `sources/a3/<id>.txt` and `sources/<id>.txt` at e57f601, and the sha256 of each a3 text equals
   `visibleSha256` in receipts-a3.json (4/4). Matters for the claim "grounded in four primary sources";
   it does not change the 4/4 value at e57f601.
2. Opening provenance (P5). Retained texts and receipts are not read. Deleting them keeps 4/4. Whether
   the pages were opened this round rests on receipts-a3.json, which the counter ignores.
3. Citation strength (P1, P10). Header line 1 (`source: S036, S037, S038, S039 …`) alone satisfies
   "cites the id", so an entry with no body citation, or no body at all, passes. At e57f601 S038 has 9
   body citations (field-performance-cwv.md:63-107); the other ids were not counted by me.
4. Rendering (P4). A Gate line hidden in an HTML comment (or a code fence) still counts. Cosmetic.
5. URL boundary (P6). `url_in` allows a trailing `.`, `?` or `#`, so `…/vitals.evil` passes when both
   places agree. Low risk: an author would have to edit both cells consistently.
6. Not checked at all: entry claims against sources (thresholds, 28-day window, 150 queries/minute),
   `recheck:` content, registry columns other than tier/status/opened/used-by, duplicate registry rows
   (first match wins), and the other new surfaces (QUALITY.md, SKILL.md, README, PROVINCE.md).

## Assessment for the declared claim

The scorecard value is "4/4 declared rows meet every check" and that is true and reproducible. The
claim text adds "grounded in four primary sources opened this round", which gaps 1 and 2 leave to
evidence outside the counter. That evidence holds today (quote substrings and digests above). These
are fixable defects of the counter, not a reason to reject the value. Smallest safe correction for a
future counter: for each Gate quote, require it to be a substring of the committed
`sources/a3/<id>.txt` whose sha256 matches receipts-a3.json, and require one id token outside the
first 3 header lines of the entry. Kills P1, P2, P3, P5, P10.

## Not verified

- I made no network fetch, so I did not compare retained texts against the live pages.
- Facts in the entry body were not checked against the sources, apart from the quoted sentences.
- No other new surface (QUALITY.md, SKILL.md, README, PROVINCE.md) was reviewed.
