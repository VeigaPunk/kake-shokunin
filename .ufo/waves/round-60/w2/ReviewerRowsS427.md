# ReviewerRowsS427

ATTACKS:
- Checked B1 registry rows S427–S429 cell-by-cell against the retained S427–S429 bodies and receipts; compared S425 at base; checked Gate quotes/anchors, S427 scope and supersedes; ran the registry census on a full B1 scratch tree.

ROWS:
- All three rows have 11 non-empty cells, valid `docs` kind / tier `A`, `mined` status, opened `2026-10-27`, normalized `180d` recheck, exact expected used-by paths, and title prefixes/URLs matching their retained body / receipt. All three source bodies match their receipt SHA-256 and byte count; receipts state HTTP 200, access date 2026-10-27, `round60` user-agent, and matching URL/effectiveUrl. The receipts blob at B1 is `b9b56713713523ed9bec1c769313fd9cb0d52e6d`.
- Gate quotes: all six checked spans are 6–25 whitespace units, <=160 characters, each occurs in one whitespace-collapsed article text node and exactly once in its own body (zero in the other two). Each quote's nearest preceding article heading and section match its row anchor under A1: S427 h1 “Overview of Google crawlers and fetchers (user agents)”; S428 h1 “List of Google user-triggered fetchers”; S429 h2 “Understand the limitations of a robots.txt file”. Embedded Last-updated dates match the respective footer: 2026-06-12, 2026-08-19, 2025-12-10.
- S427 scope is precise: it includes common and special-case crawlers; its A9 regex is clean; the retained body states the common-crawler automatic-crawl rule and AdsBot example, while its user-triggered category cell gives no robots.txt posture. `teaches` begins exactly `supersedes S425 — `; S425 has the same URL and remains unchanged. S427–S429 are absent at base; the registry diff is exactly three added rows and no removals.
- S428's body supports the lead “generally ignore” statement, general technical-properties qualifier, three named JSON objects, two reverse-DNS masks, and non-exhaustive list note. S429 supports the cannot-enforce / crawler-obeys statement and the disallowed-but-indexed statement.
- One precision note: S429 scope ends “not a crawl-rate or crawl-delay rule.” The retained article block has no crawl-rate/delay statement (the only full-file “crawl rate” hit is a navigation link). This is an accurate negative description of the article's scope, not a contradicted claim; it is not a defect warranting a finding.

CENSUS:
- Command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-27 --root <full B1 archive tree> --file <full B1 archive tree>/corpus/SOURCES.md`.
- Output: exit 0; 167 rows; `file ok`; 15 W04 warnings, including exactly one new warning for S427 sharing the overview URL with S425 across scopes. The round-start control has 164 rows and 14 W04; no E-code is reported for S427–S429. A preliminary corpus-only archive produced unrelated E11s for used-by paths outside `corpus/`; it was discarded and is not the census result reported here.

FINDINGS:
| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| none | — | No actionable row/census defect found. | See `.files/rows-and-census.txt`; full-tree validate output in `.files/census-validate-b1.out`. | — |

VERDICT: No actionable falsification found in S427–S429; registry validation is clean with the expected S427/S425 W04 warning.
