# ScoutOperatorLessons

Read-only scout. Sources read: `corpus/lessons/` listing, `corpus/QUALITY.md` §Round-54..57 (lines 1118-1258), `corpus/lessons/round-57-verifier-spotcheck.md` (all, §5 D1-D5), `corpus/lessons/round-57.md` §Mistakes, `considerthese/2026-10-26.md`, round-58 `contract.md`/`contract.json`, docstrings of `c58_receipt_rewrites.py`, `c58_resolver_cases.py`, `c58_quote_truth.py`, `make_spec_w1.py`. No counter or gate run; no tool installed.

## OPERATOR LESSONS:

- `ls corpus/lessons/operator-*.md` → **no such files** (exit 1). Fleet-wide `find -maxdepth 4 -iname 'operator-*'` finds only unrelated lane artifacts (kasegi/tameshi/tabi/souji/game-dev-3d); none is a kake lesson. There is no inherited operator-authored lesson file for this lane.
- Operator-owned *open items* do exist and are carried in `considerthese/2026-10-26.md` Part 1 (open items) and Part 2 proposal 3: (a) the calibration sub-axis ownership ruling (r54-r57, "waiting on an operator ruling"); (b) the CJK quote-length rule (5 rounds; S367 at 31 units); (c) SHONEN promotion (four `[ ]`); (d) `wip/operator-save-20261023` / draft PR #1. QUALITY.md line 1109 (round 50) also holds "Operator-owned and inherited artifacts are not swept to zero a count".
- Honoured by round 58?
  - (a) Calibration ownership: **stated open, not decided** — contract.md line 18-19: "The ownership question (calibration vs operability) stays open for the operator, as in rounds 55–57." Honoured (not pre-empted); not resolved.
  - (b) CJK quote length: **tightened, not ruled** — contract.md line 8 of unit rule in the assignment ("every quote <= 25 units AND <= 40 characters") and counter C5 "each 6..25 units and at most 40 characters". This follows the round-55 criterion (stop the overrun growing); contract does not resolve S367/S372/S373 (31/27/27 units). Honoured as containment only.
  - (c) SHONEN boxes and (d) wip branch/PR: **not mentioned** in contract.md (grep for SHONEN → only none; line 87 area has no operator-queue text). Not handled, and correctly not claimed (status-neutral, operator-owned).
  - Operator-queue proposal (considerthese #3) asks the report to list waiting items with round counts: [INFERENCE] a round-58 report line should carry (a)-(d) with ages (a: now 5 rounds incl. r58; b: 6) — nothing in the contract requires it.

## QUALITY CRITERIA:

Round-54 criteria are listed because they feed the unit rule (C3). `HONOURS` = contract/counter text that carries it; quotes are verbatim.

| # | Criterion (QUALITY.md line) | Honoured? | Quote / where |
|---|---|---|---|
| r54-a | Translation keeps source qualifier (1120) | n/a to new entries by counter; reviewer duty | contract line 78: "whether the English rendering is faithful (reviewer/critic-checked)" — yes, delegated to critics |
| r54-b | CJK quote length names unit; units not "words" (1133) | **yes** | contract (assignment) "one unit per CJK character, one per non-CJK whitespace token"; counter C5 requires Gate line to state units (`Gate line does not state N units`, c58_quote_truth.py:409) |
| r55-1 | Entry lands with its README coverage-map row (1148) | **partial** | Not a claim, not named in contract.md. Only carried by seat spec `make_spec_w1.py:115-120` (README coverage map, `c55_readme_index.py` "treats a pointer to a missing file as dangling"). Contract line 63 names the README *frontier map* as the surface only. Gap: no frozen counter for it in r58 (the c55 counter exists; contract does not require it green at tip). |
| r55-2 | New quotes ≤25 units, raw substring in content block, ≥3 page-unique spans (1160) | **yes** | C5: "each 6..25 units and at most 40 characters, a raw substring of one text node of the retained body's article block, page-unique … at least 3 distinct page-unique spans" (c58_quote_truth.py docstring) |
| r55-3 | Held row reused → `used-by` only changes (1170) | n/a | both rows new: "S423 and S424 are new rows absent from the base registry" (C3); C4 "used-by: S423 = exactly entry 1" |
| r55-4 | Validated append block is the appended block (1174) | **yes** | C7 "scratch registry is byte-equal to the landed registry and the two scratch entries are byte-equal to the landed ones"; C8 pre-append mirror |
| r55-5 | Counter attacked before it scores (1181) | **yes** | contract line 7 ">= 25 % attack roles"; "Junk controls (selftest v1, 18 checks …)" for C1; but C3 counter selftest is a stub: contract line 72 "the selftest is a stub in version 1 and is ported by wave 1 before data" — honoured only if the port lands (c58_quote_truth.py:602-609 still prints "not ported yet" at read time) |
| r56-1 | Stated selftest tally = printed tally (1190) | **open obligation** | Contract says nothing on SKILL.md rows. Seat spec `ScribeSkillRows` drafts rows with placeholder `<N>/<N>` "the L1 fills the tally after the final selftest run". [INFERENCE] c56_selftally.py will go red if a row lands with a placeholder or a stale count; contract does not freeze a rule. |
| r56-2 | Selftest rebuilding from HEAD names its fixture revision (1199) | **not handled in contract** | c58 C3 selftest is to be a port of the r57 one (`KAKE_R57_SELFTEST_REV=b9a5d012f7fd`); contract does not require a `KAKE_R58_SELFTEST_REV` pin in the SKILL row. [INFERENCE] new row needs one. |
| r56-3 | Held row body pinned by sha256 (1203) | n/a / yes | new rows pinned: `BODY_SHA256 = {"S423": "8b8aef60…", "S424": "3ef1275b…"}` "frozen at the contract commit" |
| r56-4 | Sibling pages share phrases; Gate quote occurs once in its page (1207) | **yes (partial)** | C5 "page-unique" applies to Gate quote and 3 spans; S423/S424 are two retained bodies so the "unique across every retained body" reading is carried only if "page-unique" in the counter spans both bodies [INFERENCE: not verified in code] |
| r56-5 | Staged candidate re-derived, not renamed (1211) | **yes** | C1 "the staged candidate name `corpus/knowledge/baidu-crawler-identification.md` does not [exist]"; contract lines 85-86 gate the S378 reject against PROVINCE |
| r56-6 | No quote from a line holding a raw double quote (1215) | **not handled** | counter C5 refuses curly quotes only (`CURLY`, line 85); no check that the source line is free of ASCII `"`. Contract silent. Retained page text may carry `"` in code samples (the curl UA check in S424 is the likely site) — [INFERENCE]. |
| r57-1 | Receipt pin = revision covered; receipt never rewritten (1221) | **yes, widened** | contract line 11-13: "a receipt under `.ufo/waves/round-58/controls/` is committed once, after the run it records, and never rewritten; a re-run lands under a new file name. No placeholder receipt is committed." C1 `new_rewritten == 0`. Note: c57's `new_unpinned`/`scorecard_pin` terms are **dropped** from c58 C1 (grep `unpinned|scorecard` finds only a SCORECARD pointer regex, line 119); a new receipt without a `revision:` line would not fail C1. |
| r57-2 | Reject reason re-read against the page (1233) | **yes (spec-level)** | S378 reject "to be gated against PROVINCE.md in wave 1" (contract line 86); the criterion's sentence-quote duty lives in the lesson-gate seat spec, not in a counter [INFERENCE] |
| r57-3 | Gate vs tool uses reference + unseen inputs, not constants (1240) | **yes** | C2 junk controls (contract line 56-57): constant printer fails K1–K5, P3–P5; always-exit-1 fails P1/P2/P6/P7; fence-dropper fails P2. Weakness: fixtures are gate-fixed (K1–K5 literal ids S950-S952, S900, S901), not randomised per run — the r57 v2 gate randomised them. [INFERENCE from case table] |
| r57-4 | Counter pins page by digest, article text only (1246) | **yes** | BODY_SHA256 (above); "Article block: from `class="article-info"` … to 往期回顾 / 推荐阅读; text nodes only" |
| r57-5 | Entry cites only ids its registry holds (1253) | **yes** | C2 P7 "real lane at the revision green with ids_cited >= 106" (guards against drift) + K1–K5 now catch fenced/quoted-path ids. Staging ids: contract names "staged S395" only as renumber source; entries must say "the staging row for this page" (r57 criterion), not enforced by the counter. |

Summary: 2 not handled in the contract (r56-2 selftest pin, r56-6 raw-quote line), 2 partial (r55-1 README row not frozen; r57-1 pin line dropped from C1), tally criterion (r56-1) open.

## ROUTED DEFECTS:

Source: `round-57-verifier-spotcheck.md` §5.

| D | Defect | Round-58 status | Where |
|---|---|---|---|
| D1 | Receipt rewrite stated as absent (`after-c1-receipt-pins.txt` pending then filled) | **handled** | C1 whole claim; contract lines 11-13 (receipt rule); base `events=19 undisclosed=19` incl. the r57 fill; mined mistake line 87-88. Predicate terms `undisclosed/phantom/new_rewritten == 0`, `new_receipts == 2`. Limit stated: C1 receipt itself is written after the run and "covered by `new_rewritten` at every later tip" (contract line 35). Counter cannot prove a run happened (contract does not claim it). |
| D2 | Untracked leftover `round-57/w1/ExecPinsIndependent.files/relabels.json` | **resolved outside the contract** | `git ls-files` now lists `relabels.json`, `relabels.out.txt`, `relabels.py` (tracked at HEAD `cc8da16`). Not a contract item; no action needed. Current untracked: only round-58 `w1.ready*`, `w1/` (expected seat output). |
| D3 | `c56_quote_truth.py` red 6/8 on every later tree (mirror pins 158 rows) | **not in the contract**; handled only in seat specs | contract.md has no `historical`/c56 text. `make_spec_w1.py` ScribeLessonMistakes M3 ("register it as historical pinned to its measured revision (state the SKILL.md row change)") and ScribeSkillRows ("`historical` marking for c56_quote_truth.py"). No claim, counter or predicate covers it; considerthese proposal 5 (historical-gate list) asks for the same. Outcome is lane-edit only, unmeasured. |
| D4 | SHONEN boxes `[ ]`, operator-owned | **not handled, correctly** | contract silent; status-neutral per spot-check. |
| D5 | Carried limits: (i) fence-blind registry, (ii) non-ASCII path drop, (iii) C1 cannot prove a run, (iv) C2 G4 reads live sibling registries | (i) **handled** C2 K1–K3 (+P2/P3); (ii) **handled** C2 K4–K5 (note: K4 uses `中文.md`, K5 a `"` name); (iii) **stated limit, not fixed**: C7 "A receipt check, not proof that the run happened" and C1 "What the counter does not test"; (iv) **not handled**: contract line 59 lists "sibling ownership beyond P4" as untested; P4 uses a fixture sibling, so the live-sibling dependence of the r57 gate G4 is simply not scored again (c57 gate unchanged). |

Additional gap: the census stays fence-blind by design (contract line 58-59, stated divergence) — a fenced row counted by `sources-census.sh` but ignored by the tool means the two disagree on registry row count after the fix; the contract names this as a choice.

VERDICT: No operator-*.md lessons exist; round 58 honours most inherited criteria and handles D1 and D5(i)(ii) in claims, but leaves the r56 selftest-pin, r56 raw-quote-line, r55 README-row and D3 historical-gate items to seat specs/unfrozen, and C1 drops the r57 `revision:`-pin term.
