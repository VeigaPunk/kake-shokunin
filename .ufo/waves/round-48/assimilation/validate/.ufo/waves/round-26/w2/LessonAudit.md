# W2 LessonAudit — round-26 C1 freshness, author-side FALSIFY

Scope: `corpus/lessons/round-26.md`, SCORECARD.md round-26 section (L502–512), LOG.md round-26 entries (L988–1009), `.ufo/waves/round-26/statements.json`. Checked for count drift (276/22/8/14, 32 rows, 34 fetches), tense (no result asserted before execution), unsupported claims.

Candidate: e28312b14b076584fedd696fae2a684e460bd11e. Base: 97404de4ff73d6c8a4f87385cf5fdf36dca7f006.

## Verdict

DISAGREE, severity medium. Every count in the scope reconciles (276/22/8/14, 25 pairs, 32 receipts, 34 manifest fetches). Four things are wrong or unsupported as written:

1. Measured results exist but the lesson, SCORECARD and LOG still say they are pending (tense).
2. The statement ledger omits knowledge statements that cite S024 and S025, so "knowledge statements that rely on them rechecked" is not fully true.
3. The lesson's red/green selftest row is still future tense although both runs exist, and those runs were executed under /tmp without disclosure.
4. Smaller precision defects: fetch window and "once each" wording, an unretained RFC Editor source presented as a dated fact, an undisclosed SkillTails exclusion from the 22, an unrecorded UNVERIFIABLE-4 in LOG, and adjudicator attribution.

## Count reconciliation (all AGREE)

Commands: `python3 -B` read-only sums over `statements.json` pairs (L6–L240), `ls` of `rechecks/`, `fetched/manifest.json` + `manifest-retry.json`.

- Pairs: 25 (statements.json L7–L238, one object per `"row"` key). Distinct rows covered: 24.
- Statements: 28+5+13+7+4+17+6+20+12+13+9+20+11+14+13+12+13+8+6+7+8+8+7+6+9 = **276**.
- seatStale: 3+2+3+2+1+1+1+1+3+2+1+2 (S001, S003b, S005, S010, S011, S012, S013, S020, S021, S026, S027, S030) = **22**.
- stale: S003b 2, S010 2, S021 1, S026 1, S030 2 = **8**. Rejected = 22−8 = **14**.
- Lesson L60–L61 rejected list reconciles to 14: S001×3, S005×3, S011, S012, S013, S020, S021×2, S026 C1, S027.
- Lesson L53–L54 admitted list (S003×2, S010×2, S021×1, S026×1, S030×2) = 8, matching the 8 `[r26-recheck …STALE]` blocks: served-set L85+L87, etag L62+L64, static L186+L188+L190+L192.
- Receipts: 32 files `rechecks/S001..S034` minus S014, S019, with S035 excluded. All 32 `"verdict": "HOLD"`. Largest quote is 25 words (S003, S011), so the "≤25-word" claim (lesson L26) holds.
- Fetches: manifest.json has **34** entries (S001×2, S002×2, S008×1 timeout, others ×1). Each `sha256` matches the decompressed gzip body (35 of 35 incl. retry, 0 mismatch). Retry is a 35th GET.
- Measured: `verification/measure-candidate.json` L17 `decided 32, hold 32, statements 276, statementsStale 8, statementCorrections 8, unverifiable 0`, exit 0. `verification/measure-before.json` L17 `decided 0, receipts_absent`, exit 1.

## Defects

### D1 (medium, tense). Measured results are pending in the lesson, SCORECARD and LOG although they were executed.

- `corpus/lessons/round-26.md` L83–L84: "Results, revisions and no-harm checks are appended only after execution."
- `SCORECARD.md` L510: "Score stays 10→10 (HOLD); measured outcomes are appended only after execution."
- `LOG.md` L1008–L1009: "Measurements follow execution on a pushed revision."
- Also `round-26.md` L8–L9: "After is recorded only from the counter run." The counter has run, and the after value is not recorded in the lesson.

Evidence: `verification/measure-candidate.json` `executedAt` 2026-10-21T16:08:32Z, exit 0, stdout quoted above. `measure-before.json` exit 1. `measure-candidate-reverify.json` and `measure-before-reverify.json` at 16:28:35 in /tmp/kake-r26-verify, both matching.

Minimal correction: append the two measured outputs (revision, exit, decided/hold/statements/statementsStale) to lesson L83–L84, SCORECARD L510 and LOG L1008–L1009, and change "appended only after execution" to past tense.

### D2 (medium, coverage). Knowledge statements citing S024 and S025 are not in the 276-statement ledger.

- `corpus/knowledge/static-canonical-preflight.md` L98–L101: "Sources: … S024 (the first base in tree order wins), S026."
- Same file L117: "…a body base is still the document's first base in tree order (S024)…"
- Same file L144: "…'template descendants cannot supply a document-head canonical' rests on S025…" (an r23-correction block, L143–L146).
- The round-26 block at L182–L184 lists rows "S020, S021, S026, S027, S028, S029, S030, S031, S032, S033 and S034". S024 and S025 are not listed.
- `.ufo/waves/round-26/statements.json` pairs: no S022, S023, S024 or S025 entry. Pair rows at lines 7–238 contain 24 distinct rows.
- `.ufo/waves/round-26/population.json` row S024 (L528) and S025 (L552) list `usedBy: corpus/lessons/round-22.md` only. The knowledge file is missing from `usedBy`, so the used-by cell does not reflect the citation.

Contract `claim.after` requires "knowledge-entry claims citing the rows rechecked". Three knowledge statements citing S024/S025 were not rechecked, and the lesson (L47–L48: "25 pair seats judged 276 knowledge statements") and LOG (L1001–L1005) do not disclose the gap. The corrections (L143–L146) are r23 text, not round-26 judgments.

Minimal correction: either add pair/statement entries for S024/S025 at static-canonical-preflight.md L98–L101, L117, L144 (updating the 276/25 totals), or disclose in lesson L47 and LOG L1001 that rows S015–S018 and S022–S025 had no round-26 statement review and why; and add `static-canonical-preflight.md` to population.json `usedBy` for S024/S025.

### D3 (medium, tense and /tmp disclosure). The red/green selftest row is still future tense, and the runs were executed under /tmp.

- `corpus/lessons/round-26.md` L74 (Mistakes, class `survivor`): "…`text_selftest.py` checks synthetic `&amp;lt;` cases; red-before/green-after recorded after execution".
- Records now exist: `verification/text-selftest-before-extractor.json` (exit 1, `failed` includes `entities_amp_lt_decoded_once`, `entities_amp_amp_decoded_once`, `normalize_square_bracket_spacing_as_accessibility_packet`), and `verification/text-selftest-after.json` (exit 0, `passed: true`).
- Both records and `measure-selftest.json` carry `cwd: /tmp/kake-r26-red` or `/tmp/kake-r26-verify`. The lesson's /tmp row (L79, "scope"/"attribution (routed, r25)") only addresses seat writes and says nothing about these L1 runs.

Minimal correction: change L74 to past tense and cite the two JSON records by path; add to L79 or the Measurement section that the L1 verification clones ran under /tmp (`measure-*-reverify.json`, `text-selftest-*.json`), outside the seat rule.

### D4 (low, precision). Fetch window and "once each".

- `corpus/lessons/round-26.md` L22–L23: "34 fetches for 32 rows, 2026-10-21 15:09–15:10 UTC; S008 first timed out at 60 s and was retried once…". The retry ran at 15:11:01 UTC (`fetched/manifest-retry.json` L10), outside the stated window. The total is 35 GET attempts; the lesson does not say so.
- `LOG.md` L994: "Re-fetched 34 recorded URLs once each (S008 retried once after a timeout…)". S008's URL was requested twice, so "once each" is inaccurate.

Minimal correction: "34 manifest entries (35 GET attempts: S008 timed out at 15:09:36 and succeeded at 15:11:01)"; LOG L994 "once each, except S008 (timeout, then one retry)".

### D5 (low, unretained source). RFC 9557 version note rests on live RFC Editor info pages.

- `corpus/lessons/round-26.md` L63–L64: "Version note: RFC 3339 is updated by RFC 9557 per the RFC Editor info page (PairS032)".
- `.ufo/waves/round-26/w1/PairS032StaticCanonicalPrefl.md` L55: "Superseded-status checks used RFC Editor info pages (public documentation), not retained bytes."
- `corpus/knowledge/static-canonical-preflight.md` L194 repeats it as a dated fact.

The lesson does not say the info page is unretained, while the contract's `boundaries` and `appendOnly` clauses require retained bytes for new evidence.

Minimal correction: add "(live read 2026-10-21, not retained under fetched/)" at round-26.md L63–L64.

### D6 (low, disclosure). SkillTails exclusion and UNVERIFIABLE statements not stated.

- `statements.json` L245 `staleAlreadyCorrected: 4` and `skillTails` (L241–L247: 11 statements, 7 hold, 4 stale already corrected). These are outside the 276 and outside the 22. The lesson L47–L48 does not say so.
- `statements.json` L12 `seatUnverifiable: 4` for S001. Lesson L61–L62 records this. LOG L1001–L1005 says nothing, and reports only `unverifiable: 0` at row level (SOURCES.md L79 likewise).

Minimal correction: one sentence at round-26.md L47 ("excludes the 11 SKILL-tail statements, 4 already corrected under r20; 4 UNVERIFIABLE v3.0.1 statements are not counted decided") and the same in LOG L1001.

### D7 (low, attribution). Adjudicator name is inconsistent.

- `statements.json` L3: `"adjudicatedBy": "L1 KakeR25 (author-side)"`.
- Lesson L47–L48 "L1 admitted 8 and rejected 14".
- `verification/*-reverify.json` and `census-end.json`: `executedBy: KakeR26-2 (L1 replacement)`.

The round-26 adjudication is attributed to a round-25 identity. This is an author-side attribution, not a correctness error, but a reader cannot tell who adjudicated the 8/14 split.

Minimal correction: state at statements.json L3 and round-26.md L47 the identity actually used for round 26, or say "L1 (round-26 replacement; statements.json originally attributed to KakeR25)".

## Checked and holding (no defect)

- Quotes: S005 (`If you are publishing from a custom GitHub Actions workflow, no CNAME file is created`), S013, S029, S034 are present verbatim in `fetched/text/*-1.txt` and match `rechecks/*.json`. Anchors (S029 §3, S034 §4, S013 footer 2026-07-08) match receipts.
- Byte identity: manifest sha for S028 and S033 is `21c1cdce…232a`; S029 `3102dae4…b2d683`; S030 `04b65bf0…`; S031 `a11dcf17…`; S034 `61a5378f…`. These agree with the appended register at `round-23.md:206–212` and `round-24.md` references in receipts. Note only: `round-23.md:60–61` pairs S030/S031 digests in the opposite order (ClaimCritic item 11); the lesson's claim is true but does not cite a line, so a reader following 60–61 would be misled.
- Mistake rows: `fetch_retry.py` exists; `misroot-RowS012.txt` exists; `RowS012.md` absent at the fleet root; `measure.py` contains `quote_not_row_specific` (L422) and `boilerplate_quote` selftest case (L708); `text_selftest.py` L45–L46 has `&amp;lt;` cases; `before/source_text.py` L32 has the `]` rule and current `source_text.py` L31 does not.
- SOURCES.md: `git --no-optional-locks diff 97404de -- corpus/SOURCES.md` shows 2 insertions, 0 deletions, so "no SOURCES cell changed" (lesson L29) holds. No S036 in SOURCES.md.
- MANIFEST rounds[420] quote in lesson L10–L11 matches the note text.
- W1 seat count: `w1-dispatch-attempts.json` try 6 "Spawned 64 background agents"; 32+25+1+2+2+1+1 = 64 (lesson L997 list agrees). Five job-cap refusals (tries 1–5) match.
- `census-before.txt` L1 `W04 S033 duplicate url …` and `exit=0`, matching LOG L996.

## Incidental exposure (disclosure)

While checking digest prefixes I ran one repo-wide `grep` over the lane. It returned lines from `.ufo/waves/round-24/w1/ScribeSourcesRows.md`, `SourceRFC8259Json.md` and `SourceRFC9110MediaType.md`, plus round-22/23 files. I did not open the round-24 files and did not use anything from them as evidence; every digest cited above comes from round-26 manifests or round-23 register lines.

## Tools and commands

- Installed/upgraded: none. Used `python3 -B` (stdlib: json, gzip, hashlib, re, glob, os), `grep`, `git --no-optional-locks diff --stat/diff` (read-only), `ls`/`glob`. No writes except this report.
- No network GETs in this audit.
- Read-only: `read` of statements.json, measure.py, manifests, verification JSON, SCORECARD L500–520, LOG L986–1015, lesson, KakeR contract, census-before.txt, w1 reports.

```json
{"target":"corpus/lessons/round-26.md; SCORECARD.md L502-512; LOG.md L988-1009; .ufo/waves/round-26/statements.json","verdict":"DISAGREE","severity":"medium"}
```
