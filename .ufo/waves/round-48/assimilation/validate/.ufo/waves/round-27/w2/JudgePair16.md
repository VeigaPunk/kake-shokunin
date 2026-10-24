# JudgePair16 — fresh falsification of (S023, corpus/knowledge/static-canonical-preflight.md), HOLD kind=artifact

Seat `KakeR27.JudgePair16` (reviewer, leaf — no dispatch). Axis: **freshness**. Milestone `r27-fresh-falsification`.
Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`. Measured candidate `ac46a7472d945a6d7ff135e4d7f07b0b6913d835` (all Git reads by full hash).
Read-only: no corpus/ledger/script/registry/Git mutation. Scratch only: `/fast/scratch/hyaku/kake-r27/judgepair16/`. **No tool installed or upgraded** (python3 stdlib, curl, git only). No r24 material read/retried.

## 0. Item attacked

`pairs.json` row: `{"row":"S023","file":"corpus/knowledge/static-canonical-preflight.md","kind":"artifact","verdict":"HOLD","evidence":"corpus/SOURCES.md","contains":"| S023 | WHATWG HTML: Link type canonical — … | Living Standard accessed 2026-10-20 | … | mined | 2026-10-20 | 90d |"}`.
Full citing text at the candidate (file = 247 lines):
- **line 2** `verified-at: 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029), documentation opened this round; …`
- **lines 241–243 (r27 appended adjudication)** “The line2 S020–S027 metadata band records historical opening dates, including S022 and S023, not fresh round27 observations or individual support for every body claim. Their registry/round22 records support the dates.” → line 245 “All three pairs are explicitly adjudicated.”

## 1. Independent expectation vs. actual (each expectation stated before the probe)

| # | Expected before running | Actual command / exit | Result |
|---|---|---|---|
| P1 | The counter accepts the record (valid, HOLD, not undecided); strict C1 = 55/58 decided with 3 carried-UNVERIFIABLE pairs, S023 not among them | `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision ac46a747…` → **exit 1** | `citingPairs 58, reviewedPairs 58, decided 55, knownUnverifiableUnits 7, knownUnverifiablePairs 3`; missing/findings = S001/ghp-served-set, S007/ghp-custom-domain, S033/preflight (`carried_unverifiable`); `S023 outcome {'verdict':'HOLD','valid':True}` |
| P2 | `contains` occurs in `corpus/SOURCES.md` at the candidate exactly once; evidence path is not self-support | python blob count | present, count **1**; evidence `corpus/SOURCES.md` ≠ knowledge file; candidate blob sha == working-tree sha for SOURCES.md, preflight.md, pairs.json |
| P3 | No S023-derived body statement exists (relevance test) | `git show ac46a74…:corpus/knowledge/static-canonical-preflight.md \| grep -n` | literal `S023` only at **line 242**; no “canonical keyword / preferred URL / case-insensitive” claim from S023 (line 174 “case-insensitive” = Content-Type, S033). S023 is absent from the `source:` header (line 1) and from SOURCES.md `used-by` (row 31 → `corpus/lessons/round-22.md` only) |
| P4 | The 2026-10-20 stamp is true | `grep` over candidate blobs | SOURCES.md:31 `opened 2026-10-20`, anchor “Living Standard accessed 2026-10-20”; `corpus/lessons/round-22.md:36` “### Sources opened for C1 (2026-10-20)” with the S023 row at :46; `.ufo/waves/round-22/w1/Case06.md:382` “opened this session, access date 2026-10-20”, :387 digest pin `82a81f23…f6b7`; SOURCES.md:69 “the fixed eight official sources listed in S020–S027 on 2026-10-20” |
| P5 | Zero drift: live document digest == r26 retained raw == r22 pin; both anchor sentences still present exactly once | `curl https://html.spec.whatwg.org/multipage/links.html \| sha256sum` → HTTP 200, 381019 B | live sha256 **82a81f233583716daf76ce20938a399016dfd877a9368ea2cdb1a60bcd3df6b7** == `git show ac46a74…:.ufo/waves/round-26/fetched/S023-1.raw.gz \| gunzip \| sha256sum` == r22 pin. Flattened live text (lane `source_text.py`, in memory, nothing retained): “The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document.” ×1, “Keywords are always ASCII case-insensitive, and must be compared as such.” ×1; committed r26 text view == live flattened **+ trailing '\n'** (single-char diff); headings “4.6.8 Link types”, “4.6.8.4 Link type \" canonical \"" present |
| P6 | No fresh r27 observation for S022/S023 (so `kind:artifact` is the honest shape) | read r27 `fetched/manifest.json` | rows = S001×2, S002×2, S003, S004, S005, S006 — **no S022/S023** |
| P7 | “All three pairs are explicitly adjudicated” is true (S022, S023, S008 of this file) | pairs.json + P1 outcomes | all three present, all `valid:True`; S023 is not one of the 3 UNVERIFIABLE pairs (r26 `statements.json` has **no** S023 row → no inherited credit; `decided.discard` path irrelevant) |
| P8 | The grouped block does not repeat the S004-step misattribution that dissent found in `ghp-served-set.md` | flatten r27 retained S003/S004 text views | S003 quote ×1 **only in S003 view**; S004 quote ×1 **only in S004 view** (dissent C respected: numbered flow steps = S003, artifact configuration = S004) |

## 2. Verdict

**HOLD confirmed at its own scope — the attack fails.** The pair’s only assertions about S023 are (a) that S023 was among the S020–S027 batch whose documentation was opened 2026-10-20, and (b) that this is historical metadata, not a fresh r27 observation nor support for any body claim. Both are true: the registry row records `opened 2026-10-20` / “Living Standard accessed 2026-10-20”, the r22 lesson/Case06 records agree, the r27 manifest contains no S022/S023, and the document itself has **zero drift** (live bytes identical to the r26 raw and the r22 pin; both anchor sentences still present exactly once). No `[r27-recheck S023 STALE]` marker is owed; none exists in the candidate.

## 3. Dissent addressed (S005 preflight, S005/S003 sitemap, S004 ghp steps)

- **S005 preflight STALE (Pair08B) does not transfer.** Line 54’s band attributes a *substantive premise* (“which built HTML populates a manifest”) to S001–S006; S005 teaches CNAME/custom-domain only → wrong attribution → STALE. Line 2’s band attributes only *opening dates*, and `corpus/SOURCES.md` records that date for **every** row in S020–S027 (S022, S023 both 2026-10-20; S028/S029 both 2026-10-21, matching line 2’s split exactly). Bookkeeping-true bands and premise-attributing bands are different claims; the two verdicts in the same file are consistent, not contradictory. Even under Pair08B’s alternative “related rows” reading, the S023 band has no ambiguity: the one claim made about S023 is verifiably true.
- **S005/S003 sitemap (STALE / HOLD-with-dissent)** concern `corpus/knowledge/sitemap-orphan-audit.md`’s own band; they do not touch this file’s S022/S023 sentence.
- **S004 ghp steps STALE** (numbered items 4–5 belong to S003, not S004) is a locator-attribution defect in `ghp-served-set.md:29–30`. The r27 grouped block does **not** repeat it (P8), so the paragraph that carries my S023 sentence is not tainted by it.

## 4. Findings (author-side; none changes the HOLD verdict)

- **F1 — low, evidence-binding gap (ledger `reason` unbound half).** The record’s reason asserts “The registry **and historical lesson records** agree”, but the bound artifact is `corpus/SOURCES.md` only; the counter validates just `contains ∈ blob(evidence)` (count_c1.py:113–115) and cannot detect a false clause in `reason`. The unbound half is **true** (round-22.md:36/46; Case06:382/387 — verified above), so this is a completeness nit, not a falsification. Same shape as the S022 record (not a one-off).
- **F2 — low, review-premise one generation behind the measured revision.** w1 Pair16A/B were measured at declarations `be375d9` and both assert the file has **zero literal `S023`** and that the pair arises only from line 2’s range. At the candidate the file contains a literal `S023` at line 242 (the r27 adjudication prose that *is* the S023 adjudication), and the ledger reason names no line and does not mention that literal. I adjudicated that sentence’s three claims separately (historical date ✓, not a fresh r27 observation ✓, registry/round22 records support the dates ✓) → HOLD survives; only the evidence-to-sentence mapping is stale.
- **F3 — informational, registry completeness.** SOURCES.md S023 `used-by` omits this knowledge file although the C1 band admits the pair; the file discloses the metadata-only status at line 242. Registry-side edit is a writer-seat question, not this seat’s.
- **F4 — informational, scope of the HOLD.** S023’s registry row is `90d` recheck from 2026-10-20 (≈2027-01-18). The HOLD is date-anchored (corpus policy: “Living Standard citations are date-anchored, not immutable revision pins”, round-22.md) and does not assert perpetual freshness.

## 5. Residual risk / verification gaps

- The counter’s artifact branch validates only substring presence; F1/F2 (prose of `reason`, and the mismatch between w1 evidence base and measured revision) are outside machine reach.
- P5 is one GET today; the Living Standard is a moving target, so drift-freedom is an observation, not a guarantee.
- No r27 fresh source observation exists for S023 (P6); a `kind:"source"` variant would fail `source_missing` — the artifact shape is the honest one.
- I did not adjudicate S022’s own record beyond confirming the r22 lesson rows exist (out of scope).

## 6. Bottom line

The proposed HOLD for (S023, `corpus/knowledge/static-canonical-preflight.md`) is **independently confirmed** at the citing sentence’s own scope: metadata-level only, supported by the named historical artifact (`corpus/SOURCES.md` S023 row, opened 2026-10-20), with zero drift in the underlying document and no S023-derived body claim to falsify. F1–F4 are disclosure/completeness notes for L1; none is a STALE condition, so no `[r27-recheck S023 STALE]` correction is owed.

Report: .ufo/waves/round-27/w2/JudgePair16.md
