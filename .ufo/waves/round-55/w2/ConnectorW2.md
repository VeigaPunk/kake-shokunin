# ConnectorW2

ATTACKS: cross-claim and cross-source interactions at build a7a548e102b71bd16b0a6ddafa469393a2c98b69 — C1 coverage rows vs C2 entries (titles/ids/areas); frontier ground map Rows/Entries cells vs registry used-by; README/ground-map id currency (S372/S373 re-used this round); sibling-lane Yahoo-robots/prefix statements; repeats of earlier verifier spot-check patterns.

## INTERACTIONS:

1. C1 ↔ C2 (titles/ids/areas): no disagreement found. C1 rows name `knowledge/yahoo-japan-robots-txt-refusal-rules.md` (S372), `…pattern-syntax.md` (S373), `…txt-basics.md` (S418); each C2 entry's `source:` line names exactly that id and URL (`git show a7a548e:corpus/README.md` lines 67–69; `git show a7a548e:corpus/knowledge/yahoo-japan-robots-{txt-refusal-rules,pattern-syntax,txt-basics}.md` headers). Coverage cells (root placement / directory scope / absent-file negation / case-sensitive names / meta-tag fallback; prefix-vs-end marker / wildcard scope / trailing-wildcard equivalence; request channel two payloads / root-directory per-crawl lookup / absent=no restriction / present=follow) each map to real entry sections; each entry's H1 shares the cell's vocabulary (C1 `thin` term = 0 at rev). Registry `teaches` cells for S372/S373/S418 match the entries' scope. Area naming differs only in surface form ("Yahoo! JAPAN robots refusal rules (r55)" vs entry `ground:` "per-engine crawl hygiene" vs PROVINCE.md §Round-55 heading) — same frontier item, no contradiction.
2. Frontier ground map vs registry used-by: full bidirectional union check passes for all 21 rows at the attacked revision (see MAP-VS-REGISTRY CHECK). S372/S373 used-by extensions (S372 +refusal-rules; S373 +pattern-syntax; S418 new, exactly basics) are the only used-by diffs vs base fcaf4b85 and are exactly the contract-declared ones (`git show a7a548e:corpus/SOURCES.md` vs `git show fcaf4b85:corpus/SOURCES.md`; only row-set delta = +S418).
3. Id currency / sharing: S372 and S373 are now shared by multiple frontier rows (rel=nofollow row `S367 S372 S373 S374`; Baidu guidance row `S329 S373 S390 S409`; r55 row `S372 S373 S418`). Every sharing is consistent with the map's own definition (rows whose used-by names the row's entry); no row's set is missing or extra under that definition. One wording wrinkle, disclosed in the README itself: the map header says all cells are "at base fcaf4b85… (155 rows)", but the r55 row lists S418, which is not in the base registry (the map's own prose states "S418 is not in the base registry") — the header's "at base" invariant does not cover the last row, and S372/S373 base used-by did not include the new entries. Documented, so not a silent inconsistency.
4. No dangling ids: 0 distinct `S###` cited in corpus/knowledge prose fails to resolve in the 156-row registry at rev (`git show a7a548e:corpus/SOURCES.md` parse + citation scan); no leftover staged id S380 anywhere in corpus (README, lessons, QUALITY) — S380 appears only as an explicit staging discussion in lessons/round-55.md, not as a citation.

## MAP-VS-REGISTRY CHECK:

Script (python3, read-only over `git show`):
```
parse registry rows (11 cells; used-by=cell 11) from git show a7a548e:corpus/SOURCES.md
parse frontier-map rows from git show a7a548e:corpus/README.md (table under "### Frontier ground map (round 55)")
for each map row: expand id ranges (S###–S###, zero-padded);
  forward: every id exists in registry and its used-by names >=1 entry of the row;
  reverse: every registry row whose used-by names any of the row's entries is in the Rows cell.
```
Observed output: 21 real table rows, all `OK` in both directions. The only flagged line is the markdown separator row `|---|---|---|---|` (a table-format artifact, not a content row; excluding it → 21/21 OK). No `MISSING-IN-REGISTRY`, no `EXTRA` used-by cell, no `names NO entry` failures. Same check applied to the base registry for the 20 pre-round-55 rows: all pass (base used-by cells match the map's base claim; e.g. S373 base = [nofollow, baidu]).

## SIBLING CONFLICTS:

- Grep over `/home/vgpnk/Projects/shokunin/*/corpus/knowledge/` (all sibling lanes) for `Yahoo|yahoo|robots|プリフィクス|接頭辞|prefix|wildcard|Disallow|startsWith`: the only robots-matcher implementation in any sibling is tabi-shokunin/corpus/knowledge/external-class-fixture-v2.md lines 86–99 (`robotsDisallowMatches` uses `path.startsWith(p)` — RFC-style path-prefix match). It is explicitly scoped as a lane-authored loopback instrument, not a robots-semantics claim: the same entry states "It is **not**: … a robots-semantics study, a ToS reading" and U5 "Real robots semantics … are [not measured]". PROVINCE.md §Adjacent hands client-side/browser crawler discipline to tabi and publisher-side placement to kake, so no conflicting held statement exists.
- kasegi-shokunin's `yahoo` hits are bug-bounty program names (intigriti-yahoo), not robots rules. kotodama-shokunin's `Yahoo` hits are Bing SERP scratch HTML captures, not statements. kama's `接頭辞` hit is a fetched source artifact (`hosted-s346.html`), not a statement.
- Net: no sibling lane holds a conflicting statement about Yahoo! robots rules or about prefix matching.

## REPEATS:

Patterns flagged by earlier verifier spot-checks (rounds 48–54 lessons) vs this build:
- r48 "counters read the worktree, not the revision" → NOT repeated: both v2 counters read committed bytes only (`git show`/`git ls-tree`), verified in `c55_readme_index.py` and `c55_quote_truth.py` code.
- r52 defect 4 "dangling cross-registry citations (S367/S372/S373/S390/S409)" → NOT repeated: 0 dangling ids in knowledge prose at rev (measured above); S372/S373/S418 all registered.
- r52 defect 5 / r53 defect 5 "wrong gate locators" → NOT repeated for the new rows: each of the three gate quotes is a raw, unique substring of its retained body (verified: counts 1/1/1), and the S418 anchor `robots.txtとは？` exists in the body (count 3; `<title>` matches row source).
- r53 defect 5 / r54 defect 3 "S367/S372/S373 quotes 31/27/27 units > 25" → addressed for new material: this round's gate quotes are 24 (S372), 21 (S373), 22 (S418) units under the CJK-unit convention (≤25); S367 remains deliberately flagged at 31 per contract. The S372/S373 spans re-cut this round are within ceiling.
- r54 defect 1 "silent single wave" → NOT repeated: contract declares two v1 waves and W2 (this wave) exists and is running.
- r54 defect 2 "silent sub-axis ownership" → NOT repeated: contract names the calibration sub-axis deviation explicitly and the report must repeat that sentence.
- No installs were made (no tool/version/channel record); only python3/git/grep built-ins used.

VERDICT: no falsifying cross-claim interaction found — C1 rows ↔ C2 entries agree on titles/ids/areas, the frontier ground map is fully consistent with registry used-by in both directions at a7a548e, no dangling/stale ids were introduced by the S372/S373 re-use, no sibling lane holds a conflicting Yahoo-robots or prefix-matching statement, and none of the earlier verifier-flagged repeat patterns reoccurs; the only wrinkle (map header's "at base" wording vs the disclosed r55/S418 row) is self-documented, not a contradiction.
