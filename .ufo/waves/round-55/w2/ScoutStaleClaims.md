# ScoutStaleClaims

ATTACKS: stale/false claims in corpus/README.md, PROVINCE.md, SKILL.md, corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md, corpus/knowledge/robots-txt-rules.md, corpus/knowledge/crawl-scope-per-host.md, as of commit a7a548e102b71bd16b0a6ddafa469393a2c98b69.

Measured anchors (commands run): `git show a7a548e:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} \|'` → 156 rows at revision, 155 at base fcaf4b85 (`git show fcaf4b85:corpus/SOURCES.md`). `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision fcaf4b85...` → `index_mismatches=21 knowledge_files=46 coverage_rows=27`; at a7a548e → `index_mismatches=0 knowledge_files=49 coverage_rows=51`. Coverage-map row diff (base vs rev) → 24 new rows naming 24 files (21 base-unindexed + 3 new Yahoo entries). `git show a7a548e:.ufo/waves/round-55/controls/c1-selftest-v2.txt` → "32/32"; `git show a7a548e:.ufo/waves/round-55/c55_readme_index.py` run via scratch clone `--selftest` → "35/35". `git cat-file -e a7a548e:.ufo/waves/round-55/controls/c2-selftest.txt` → fatal (file absent); `git ls-tree -r --name-only a7a548e .ufo/waves/round-55/controls/` lists no `c2-selftest.txt`. Verified `git diff a7a548e -- <six scoped files>` → empty (worktree equal).

## STALE:

| File:line | Stale text | Correction proposal (append-only) |
|---|---|---|
| corpus/README.md:129 | "Held, but ungated or unmeasured … the three per-engine entries `PROVINCE.md:382`." | Lane now holds SIX per-engine entries: the three round-52 ones (S374 rel=nofollow, S329 Baidu, S312 Baidu mobile) plus the three round-55 Yahoo robots entries (S372, S373, S418), all "Frontier knowledge: no gate, no owned property audited, no publish action" (PROVINCE.md:397). Append a note that the count is six and that PROVINCE.md:382 describes the round-52 trio only; PROVINCE.md:397 describes the round-55 trio. |
| PROVINCE.md:403 | "a row for each of the 24 knowledge files the map did not name" | Measured base count of knowledge files named by no coverage-map row is **21** (C1 base receipt `index_mismatches=21`; contract.md "21 of them named by no coverage-map row"). 24 is the number of coverage rows added (21 previously-unindexed + 3 new entries). Append a disambiguation note stating 21 base-unnamed files and 24 rows added (21+3). |
| SKILL.md:1233 | C1 selftest "(35 fixtures, generated sandbox repos; receipt `.ufo/waves/round-55/controls/c1-selftest-v2.txt`)" | The committed receipt content says `c55 readme-index selftest: 32/32`, but the counter at the same revision outputs 35/35. Append/refresh a receipt that actually records the 35-fixture run (or correct the attestation). |
| SKILL.md:1234 | C2 selftest "(47 sandbox-repo fixtures … plus 3 unit-rule checks; receipt `.ufo/waves/round-55/controls/c2-selftest.txt`)" | No file `controls/c2-selftest.txt` exists at the revision (nor in the worktree). The receipt pointer is dangling; name an existing receipt or add one. (The 47+3=50 fixture count itself matches the counter output `50/50`.) |
| corpus/README.md:75 | "(155 rows)" as the row-set scope for the whole ground-map table | Base-scoped, so historically true for 155 rows — but the table's round-55 row (line 94) lists S372/S373/S418, which are not the base used-by cells (S418 does not exist at base; S372/S373's base used-by did not name the new entries). Line 108 discloses S418's absence. Append a scoping note that the round-55 row is measured at the revision, not at base. |

## CROSS-REFERENCES DUE:

- **corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md:26-27** — "the lane's robots-refusal ground (S372, S373)". Pre-round-55, S372/S373 were registry rows with no knowledge entry (the round-52 verifier flagged this cross-registry citation; the rows only became held ground when the three Yahoo robots entries landed). Append a note naming the new entries that now hold that ground: `yahoo-japan-robots-txt-refusal-rules.md` (S372), `yahoo-japan-robots-pattern-syntax.md` (S373), and the basics entry (S418), instead of only the row ids.
- **corpus/knowledge/robots-txt-rules.md** — the new refusal-rules/pattern-syntax/basics entries repeatedly "Contrast with the RFC side" against this entry (e.g., refusal-rules.md:28, 51, 65, 76, 91). This entry has no pointer to the operator-specific Yahoo robots entries; append a note that Yahoo! JAPAN's own robots syntax/rules are held separately.
- **corpus/knowledge/crawl-scope-per-host.md** — the new entries cite it as the host-root scope rule (pattern-syntax.md:15; basics.md:17). It should cross-reference the three new entries (append-only note), and its "Named debt" section could note the Yahoo-specific placement statements now held.
- **corpus/README.md:121-124** ("Untouched ground" list) — items "crawler-specific extensions" (PROVINCE.md:302) and "robots `Sitemap:` cross-submission" (PROVINCE.md:336) are listed as ground no entry holds; the new S373 entry now holds one operator's own extended robots pattern syntax (documentation, not observed behavior) and S418 records the operator's statement that robots.txt carries the sitemap location. [INFERENCE] These lines deserve an appended qualifier that the Yahoo operator's documented extension/sitemap-channel statements are now held for that operator, while the audit-tool gaps at PROVINCE.md:302/336 remain open.
- **corpus/README.md:67-69** — coverage rows for the three new entries exist; no change needed, but row 66 (Yahoo rel=nofollow) could cross-reference its three sibling entries.

## HISTORICAL-OK:

- corpus/README.md:75 "at base fcaf4b85… (155 rows)" — true for base (155 rows measured); base-scoped.
- corpus/README.md:59 receipt-integrity "27-control and fixture counts" — verified: `ls .ufo/waves/round-44/verification/claim/after-final/tools/ | wc -l` → 27; round-44-dated.
- corpus/README.md:103-108 "Two dated row sets hold no entry of their own: S102–S109 … S416/S417" — verified used-by only `corpus/lessons/round-39.md` / `round-53.md` at the revision.
- corpus/README.md:19 "all 21 rows" (fleet-registry) — table has 21 data rows.
- corpus/README.md:55 "30 entries" (freshness-sidecar.json) — measured 30 entries.
- corpus/README.md:42/63 "Crawl scope per host" and "Offline robots.txt expectation rules" coverage cells — still accurate at the revision.
- corpus/README.md:73-77 ground-map intro's used-by row sets — each verified against base SOURCES.md used-by cells (S011–S013, S011/S034/S095/S096/S098–S101, S001–S006/S020/S021/S024–S034, S001–S006/S065/S066, S262, S263, S137–S139, S249, S273/S274, S286, S367/S372/S373/S374, S329/S373/S390/S409, S312/S390/S409, S036–S039, S040–S043, S049–S052/S061, S057–S060/S062, S067–S070/S073, S001/S002/S006/S078–S080/S082–S086, S035).
- PROVINCE.md round-52/55 dated paragraphs (e.g., :373-383 "All three are Frontier knowledge") and the round-55 section (:385-405) — round-dated prose, kept as history.
- SKILL.md:1233/1234 base controls `base-c1-readme-index-v2.txt` (`index_mismatches=21`, exit 1) and `base-c2-quote-truth-v2.txt` (`0/8`, exit 1) — exist and match measured base state.
- SKILL.md:1239-1241 "No round-55 gate-completeness counter exists" — verified (no such counter in the round-55 tree).

VERDICT: The round-55 build lands false/stale counts on the per-engine "held, ungated" list (README.md:129, six entries now), PROVINCE.md:403 (24 vs measured 21), and SKILL.md's selftest receipt claims (c1 & v2 receipt records 32/32 while the counter outputs 35/35; c2-selftest.txt does not exist); plus append-only cross-references are due in the three older knowledge entries for the Yahoo robots ground.
