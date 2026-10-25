# ReviewerLessonGate

ATTACKS: corpus/lessons/round-55.md @ a7a548e102b71bd16b0a6ddafa469393a2c98b69 — against /home/vgpnk/Projects/shokunin/CORPUS.md (SOURCES rule 1 Gate elements, rule 2 append-only + old→new logging, "A count carries its command", `## Mistakes` shape, corrections append-only) and /home/vgpnk/Projects/shokunin/LEARNING.md (Gate shape: candidates considered, admitted, rejected with reasons, spot-check result; outside discernment).

Method: all lane evidence read at REV=a7a548e102b71bd16b0a6ddafa469393a2c98b69 and BASE=fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d via `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show <rev>:<path>`; no path outside this report written; no git/jj mutation. Lesson is 70 lines (`git show $REV:corpus/lessons/round-55.md | wc -l` → 70). Line numbers below are that file's.

## CONFORMANCE TABLE:

| # | Requirement | Verdict | Command → observed output |
|---|---|---|---|
| 1 | SOURCES rule 1: new row S418 Gate line has URL, access date, ≤25-word located quote with location | PASS | lesson L15; `grep -c -F 'robots.txtとは？' S418.html`(from `git show $REV:.ufo/waves/round-55/sources/S418.html`) → 3; python `d.count("検索エンジンに対する要求を伝えるファイルです")` → 1; units below |
| 2 | Quote ceiling ≤25 units (unit rule L10) for all three Gate quotes | PASS | canonical `units()` copied from `$REV:.ufo/waves/round-55/c55_quote_truth.py` (CJK_RE excludes CJK punctuation; a token containing CJK contributes 0 non-CJK tokens): S372=24, S373=21, S418=22 — matches L13–15 claims exactly |
| 3 | Gate receipt claims: sha256, bytes, HTTP 200 | PASS | `git show $REV:.ufo/waves/round-55/sources/S{372,373,418}.html \| sha256sum \| wc -c` → ee8c9def…0111/10168, 3173d961…03885/9402, 2b146a72…312c/7559 — byte-equal to L13–15 and to receipts.json (`httpStatus: 200` ×3, fetchedAt 2026-10-25) |
| 4 | Quotes are raw substrings; anchors exist in bodies | PASS | python `in`/`count` on decoded bodies: quotes count=1 each; headings: S372 §サイト単位…拒否設定 ×4, S373 「$」記号 ×5, S418 robots.txtとは？ ×3 |
| 5 | SOURCES rule 2: only status/recheck/used-by change in place, logged old→new | PASS | cell-split diff of S372/S373 rows BASE→REV: only cell 12 changed, new values byte-equal to the L25–26 log; S418 row appended at line 164 (`NF=13`, status `mined`, opened `2026-10-25`, recheck `180d`, used-by `corpus/knowledge/yahoo-japan-robots-txt-basics.md`) |
| 6 | Registry rows 155 → 156 | PASS | `git show $BASE:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 155; same at $REV → 156; L29 carries the command + date (the only fully conformant count in the lesson) |
| 7 | "A count carries its command" | FAIL (partial) | only L29 conforms; every other count lacks the `<number> — <command> <date>` form — see UNCOUNTED NUMBERS |
| 8 | `## Mistakes` shape (class · evidence · captured-by · fix; classes from vocabulary) | PASS | L59–64: 4 rows; classes reference-drift/vacuous/landing/scope all in the CORPUS vocabulary list; evidence pointers exist at $REV (`controls/base-c1-readme-index-v2.txt` → `unindexed=21 knowledge_files=46 met=False … EXIT=1`; `controls/base-c2-quote-truth-v2.txt` → `0/8 met=False … EXIT=1`) |
| 9 | Fixes shipped: red-before committed, QUALITY criterion | PASS | both v2 base-control receipts above show exit 1 at BASE; `git show $REV:corpus/QUALITY.md \| grep -n round-55` → lines 1153–1169 criterion citing this lesson §Mistakes and ExecStagedQuoteAudit |
| 10 | Corrections append-only | PASS | `git log --format='%h %s' $REV -- corpus/lessons/round-55.md` → single commit `2bda8e4 round-55: build …` (new file, no rewrite of any lane lesson) |
| 11 | C2 counter/quality trend claims ("49 of 49", re-grounded quotes) | PASS | `python3 -B .ufo/waves/round-55/c55_readme_index.py --root <lane> --revision $REV` → `index_mismatches=0 knowledge_files=49 met=True`, exit 0; `…/c55_quote_truth.py …` → `8/8 met=True`, exit 0; `git ls-tree -r --name-only $REV corpus/knowledge \| wc -l` → 49 (BASE → 46) |
| 12 | L17–18 fresh-GET sha equality; L38–45 id/guard artifacts; L50 staged spans; L52 quarantine; L46–49 normalization | PASS (bytes) | ScoutFreshS372/S373 receipts: `sha256 (my fetch)` = retained sha256 (S372 ee8c9def…, S373 3173d961…), HTTP 200, bytes 10168/9402; `assimilation/reg-ids\|wc -l`=155, `staged-ids`=129, `collisions`=8 (S312 S329 S367 S372 S373 S374 S390 S409, matches L39), `quarantine-slice`=12; guard re-run on committed `guard-proof/fixture-reg.md`: 0–3-space pattern → 1, column-zero → 0; my probe `    \| S999 \|` vs 0–3 pattern → 0 (supports L44); ExecStagedQuoteAudit `SUMMARY spans=6 … over_25_units=6` (L50); anchor `§ 本文（クローラー…手順）` in S418 body → 0 hits; staged rows in /home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md: S372/S373/S380 `opened= 2026-10-24`, `recheck= 180d — curl -fsSL…` (matches L46–48) |
| 13 | LEARNING Gate shape: candidates, admitted, rejected (reasons), spot-check result | FAIL | Gate (L8–19) lists only admitted rows; zero rejected candidates with reasons; spot-check explicitly pending (L69–70) — see MISSING |
| 14 | No credential material / session tokens / op:// | PASS | read of all 70 committed lines — none present |
| 15 | Assimilation source pointer `merge/kake/` (L33) | NOTE | `git ls-tree --name-only $REV merge/kake/` → empty: not a lane path; resolves only in the shokuknow tree /home/vgpnk/Projects/shokuknow/merge/kake [INFERENCE]. Counts there: 129 staged rows, 104 manifest entries — see CONTRADICTIONS #2 |

## UNCOUNTED NUMBERS:

Sentences stating a number with no inline command (`<number> — <command> <date>`, CORPUS.md "A count carries its command"). Tier A = no command and no committed receipt pointer; Tier B = receipt/artifact pointer cited but no command in the sentence.

- Tier A — L54: "the package's remaining 100 knowledge entries and 126 staged rows" — no command, no artifact pointer; 100 also contradicted (CONTRADICTIONS #1). "126" is arithmetically 129−3 but carries nothing runnable.
- Tier A — L61: "selftest 32 fixtures" — no command, no pointer to the selftest fixture set.
- Tier A — L62: "version-1 selftests passed 10/10" — no command, no pointer (the v1 receipts named in the same row are base controls, not selftest runs).
- Tier B — L13–15: "24 units", "21 units", "22 units" — unit rule stated (L10) but no command; verified true only via the counter's `units()` (row 2).
- Tier B — L38: "(155 ids)" and "(129 ids)" — artifact names only, no command.
- Tier B — L39: "collisions …: 8" — artifact + w1 pointer only.
- Tier B — L43–44: "yields collisions `S287` … and 0 with a column-zero-only pattern" — pointer only (I re-ran: 1 and 0).
- Tier B — L48: "0 hits in the body" — pointer only (I re-ran: 0).
- Tier B — L50: "6 of 6 staged quoted spans exceed 25 units" — pointer only (audit SUMMARY confirms).
- Tier B — L52: "12 rows" — pointer only (file has 12 lines).
- Tier B — L61: "21 of 46 … (…base-c1-readme-index-v2.txt, exit 1)" — receipt cited (receipt embeds the command output) but not in `<number> — <command> <date>` form.
- Tier B — L62: "one mega-row naming 46 files", "9 of 16 mutants survived" — w1 pointers only.
- Tier B — L63: "one 33-seat v1 wave" — pointer to round-54-verifier-spotcheck.md only (contents not re-verified by this seat: unrun).
- Tier B — L69: "names 49 of 49 knowledge files … (C1 counter)" — names the counter but no date; I ran it: `index_mismatches=0 knowledge_files=49 met=True`, exit 0.

## CONTRADICTIONS:

1. L54 "remaining 100 knowledge entries" — contradicted by the package itself. `grep -cE '^\| `corpus/knowledge/' /home/vgpnk/Projects/shokuknow/merge/kake/MERGE-REPORT.md` → 104 table rows (98 `new-file` + 6 `amendment`; `yahoo-japan-robots` rows = 3); MERGE-REPORT.json `entries` list length 104; `find …/merge/kake/knowledge -type f -name '*.md' | wc -l` → 98. With the 3 Yahoo entries adopted this round: 104−3 = 101 remaining by the manifest, or 98−3 = 95 by files on disk. No derivation from committed/manifest bytes yields 100, and the sentence carries no command that would. ("126 staged rows" is consistent: `grep -cE '^ {0,3}\|…S[0-9]{3,}…\|' …/SOURCES.append.md` → 129, minus 3 = 126, but is likewise uncommanded.)
2. No other committed-byte contradiction found: every other number or byte claim I exercised (rows 1–6, 8–12, 15 above) reproduced exactly. Checks not exercised are marked unrun, not clean.

## MISSING:

1. No rejected candidate with reason and flip condition anywhere in the lesson. Gate (L8–19) contains only the three admitted rows; the `REJECTED: <reason>; flip: <what would change the verdict>` shape (CORPUS §SOURCES `teaches` rule) appears zero times; LEARNING "Files the path writes" requires the Gate to carry "rejected (with reasons)". The closest material — L52–55 quarantine and "not adopted" bullets — carries neither the REJECTED marker nor a flip condition.
2. No spot-check result. L69–70 records discernment as "pending at filing". LEARNING "Discernment is checked from outside" requires a non-author spot-check of "at least one admit and one reject" recorded as agree/disagree with a reason in the round's lesson. As filed, zero rejects are recorded anywhere, so even the required admit+reject sample shape cannot yet exist — the reject half needs materializing (candidates exist: the 12 quarantined rows, the unadopted entries) before closure can sample it.
3. Gate scoping wording vs rule 1: L10 header says "Rows opened this round" while L17 states "S372 and S373 are held rows (opened round 53)". SOURCES rule 1 attaches the Gate duty to every new row; two of the three Gate rows are not new. The header over-scopes (should read "opened or re-opened", or scope the rule-1 duty to S418) — the data itself is correct and correctly disambiguated at L17–19.
4. Non-author re-open sample not discharged or reserved: SOURCES rule 1 sentence 2 ("Non-author verification re-opens a sample") is nowhere recorded in the lesson. L17–18 cites `w1/ScoutFreshS372.md`/`ScoutFreshS373.md`, but LEARNING is explicit that "A subagent the lane dispatched is still the lane" — those W1 receipts cannot serve as the outside check; only the operator/fresh-reviewer closure of MISSING #2 can.

VERDICT: byte-true at a7a548e where it counts — quotes 24/21/22 units are raw substrings, hashes/bytes/HTTP-200 match receipts, append-only used-by-only registry change 155→156 verified, counters exit 0 (C1 49/49, C2 8/8) with committed red-before controls — but the lesson carries one contradicted uncommanded count (L54 "100 knowledge entries"; manifest arithmetic gives 101 remaining of 104) plus a dozen numbers without commands, and the LEARNING Gate shape is incomplete as filed: no rejected candidate with reason/flip and no spot-check result (both pending non-author closure).
