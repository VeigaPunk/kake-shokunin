# KakeR40.ReviewRoutedDefects — round-39 routed defects 1–5 + report corrections

Scope: round-39 spot-check (`corpus/lessons/round-39-verifier-spotcheck.md:160-180`) vs round-40 commits
f043c721 → 12211cc5 → 56d57ee4 → 6d5cd54 (tip). Read-only git; no installs.

## Routed defects
| # | Defect | Round-40 action (path:line / commit) | Verdict |
|---|---|---|---|
| 1 | SOURCES append-only corrections | S112/S113/S114 rows appended carrying supersedes cells with wave-2 corrections (`corpus/SOURCES.md:120-122`); S115 supersedes S111 (:123); existing S106/S107/S109 untouched (append-only, lesson `round-40.md:21-23`). S112's cell explicitly corrects the refuted "ignored" reading ("neither this source nor S102 says foreign elements are 'ignored'"). Committed in f043c721 | addressed |
| 2 | Build deviations D2/D1/D4/D5/D3 | Build 56d57ee4 (`scripts/sitemap_audit.py`, sha 03a8fba4…): D2 NUL check before parse (`:189`, `xml_malformed`); D4 `_parse_url` rejects leading C0/space + TAB/CR/LF anywhere (`:70-71` → `loc_not_absolute`/`check_invalid`); D5 duplicate string id → `check_invalid` (`:337-344`). Selftest 150→179, red on round-39 bytes (`verification/build/selftest-new-on-base.txt` PASS 156/179 exit 1) green on build (PASS 179/179 exit 0). D1 rejected with source reason (S110 §2.8; lesson `round-40.md:26-29`); D3 not changed, recorded as contract reading (lesson `:30-32`; `w1/ReviewD3Reading.md`) | partly — D2/D4/D5 fixed; D1 reject+D3 recorded per intent |
| 3 | SCORECARD correction for round-39 row | `SCORECARD.md:2539-2546`: appended closure correction — row admitted `unprovable-but-better`, reviewer pointer = spot-check file, "pending closure" superseded | addressed |
| 4 | QUALITY (o) gate for countable claims | `QUALITY.md:993-1000` (o) amended: every counter public/sealed, non-author receipts committed at/before declaration; executable `criteria/preseal_order_check.py`; receipts: fail at f043c721 (0 independent) and ceecb1b1, pass at 12211cc5 (76 independent) | addressed |
| 5 | Carried items stay open | No round-40 commit changes M06 survivor, `MutRecheckOversize` M4/M8, or round-38 defect-6 items 2–10; `w1/ScoutCarriedItems.md` (committed) verifies each still open at f043c721. Not re-carried in round-40 lesson/report | not addressed — status verified open; no fix, no carry-forward |

## Report-correction checks (against committed bytes)
1. Surface count: `git ls-tree -r --name-only 565ef4c9 scripts/ | grep -c sitemap_audit` → **2** (exit 0); `grep -cx 'scripts/sitemap_audit.py'` → **1** (exit 0). Lesson correction 1 holds.
2. Critic seats: round-39 commit holds 3 materialized sources (`a3-controls/w1a3/Ctl{EngineLenient,HtmlParserReader,StdlibConvenience}.py`) + 3 materialized diffs (`w1a3-materialized/Ctl{GuessTweak,RegexTweak,XsdTweak}.diff`) = **6**. Lesson correction 2 holds.
3. Criterion-o adversarial: `round-39/w2a3/MutCriterionO.md` table = 7 negatives; 5 false accepts (code_only, after_declaration, no_summary_revision, comment_only, quoted_policy), 2 correct rejects → **5 of 7** (not 15). Lesson correction 3 holds.

## Other verified claims
- Tally: `ls .ufo/waves/round-40/verification/w1/*.json | wc -l` → 76; `jq -s 'map(select(.met))|length'` → 27. Kill rule commit 12211cc5 precedes build 56d57ee4.
- Counter frozen: `c1_count.py` sha256 prefix 6d73b8f4… identical at f043c721/12211cc5/56d57ee4/6d5cd54; predicate = "passed >= 30 of 30 … selftest 150/150".
- Tool unchanged after build: sha at tip = 03a8fba4… = build. Real-run JSON byte-equal to round-39 (sha 2ffbea3a… both).
- No installs needed; no findings beyond the table.

Residual risk: D1 rejection and D3 reading rest on source interpretation (S110 §2.8 note; sentence-9 precedence) — recorded, not machine-checked beyond `d1_check.py`; counter 30/30 at build is information only (per kill rule).
