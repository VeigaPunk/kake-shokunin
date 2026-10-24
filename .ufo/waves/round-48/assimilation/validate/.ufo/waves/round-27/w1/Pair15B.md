# Pair15B — critic: (S022, corpus/knowledge/static-canonical-preflight.md)

Seat: KakeR27.Pair15B (critic, leaf, read-only). Axis: freshness. Milestone: r27-full-citing-set.
Independent judgment; the Pair15A report was not read. No fetch, no r24 material, no ledger/source edits, no tool installs.

## Measured revision and hashes
- HEAD `be375d90afc6fc7aca369ab3cf5247bf460aeed2`; file blob identical at base `83528f7` and HEAD: `d86ddec6e6acc05b3c1f60da87a97a0f2645c8bf`.
- sha256 `corpus/knowledge/static-canonical-preflight.md` = 833b28f26fa7309f7e31398275bae2f704969d8e6f095bc5bb96250da5c531bc (203 lines)
- sha256 `corpus/SOURCES.md` = 5001eadee20c65c5df364a88430b6b0e76a99940afc282d72fecdd6d7c6be62d
- sha256 `corpus/lessons/round-22.md` = 30b5409808965c7704cfd2adb739d0c2f1b3ca8c07eeb5d16e4701057ecf5088
- sha256 `.ufo/waves/round-26/rechecks/S022.json` = 7b7e3129b002a5f01ac60d59b241631b518367a12184038e6b7f85c0f033eef3
- sha256 `.ufo/waves/round-26/fetched/text/S022-1.txt` = d35660665774bc03cba76afc6a7834f11a0873f37e1bb316fb3097c5f8f4aee8

## Citing-line enumeration (ranges expanded)
- There is no literal `S022` anywhere in the file (`grep -n S022` exit 1).
- The pair exists only through the range on **line 2** (metadata), which `count_c1.py` RANGE expands to S020..S027:
  `verified-at: 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029), documentation opened this round; local behavior has separate committed round22 receipts, not live website verification`
- Line 1 `source:` lists S020, S021, S026–S029 only. S022 is absent from it.
- The body (lines 5–203) never cites S022. The EOF r26 paragraph (line 184) lists S020, S021, S026–S034, and line 200 adds S024/S025. S022 is not named at EOF.
- Kind: **historical metadata** (verified-at provenance). This is neither a content attribution nor r26 EOF prose.

## Claim at its own stated scope
The claim is a date claim: the documentation for each of S020–S027 was opened on 2026-10-20, "this round". Line history confirms the scope:
- `c0fd6d5` (2026-10-20 18:30 -0300, "round-22: offline canonical publishing preflight") added `verified-at: 2026-10-20, documentation opened this round`. The same commit added SOURCES row S022 with `opened 2026-10-20`.
- `b539cc1` (2026-10-21, round-22 recovery) split the date by range into `2026-10-20 (S020-S027)` and `2026-10-21 (S028-S029)`.
- So "this round" means round 22. `corpus/lessons/round-22.md:3` contains `Date: 2026-10-20.`

## Falsification attempts
1. **Wrong date?** No. SOURCES.md:30 (S022) contains `Opening paragraph, updated 2026-08-21; opened 2026-10-20` and last-verified `2026-10-20`. The row was born in the same round-22 commit as line 2. All eight S020–S027 rows carry 2026-10-20 dates, so the range has no outlier.
2. **Was it actually opened then, or only dated?** Round-22 contemporaneous evidence quotes it. `corpus/lessons/round-22.md:45` contains `Opening paragraph: “Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons”`. `.ufo/waves/round-22/w1/SourceHierarchy.md:40` contains `S022 Google troubleshooting — declared versus selected`. I found no round-22 raw-byte fetch receipt for S022. The opening is evidenced by the quote plus commit date, not by retained bytes. This is a residual uncertainty, not a counterexample.
3. **Stale premise now?** No. r26 re-fetched S022 on 2026-10-21T15:10:44Z (`.ufo/waves/round-26/fetched/manifest.json`, index 1, status 200, sha256 4d42dd82…3e47, Last-Modified Fri, 21 Aug 2026). The receipt verdict is HOLD with the same quote. The retained `S022-1.txt` contains the opening sentence (count 1). The page date 2026-08-21 predates the 2026-10-20 opening, so the premise has not drifted. The 2026-10-20 date is a preserved historical source date, not a stale claim. Line 184 states: `Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten.`
4. **Retry boilerplate?** Irrelevant here. S022 is absent from `.ufo/waves/round-26/fetched/manifest-retry.json` (`[]`), and line 184's `S008 via manifest-retry.json` does not concern S022. S022 is also absent from the r27 fetch manifest (`[]`), so no r27 fresh source observation exists. The r26 receipt is carried as r26 and is not relabelled as r27.
5. **Unsupported scope (strongest counterexample).** The range puts S022 into this entry's provenance even though S022 grounds no statement here. Line 1 `source:` omits it, the body never cites it, and SOURCES.md:30 used-by lists only `corpus/lessons/round-22.md`. A reader could infer S022 supports content in this file. At the line's own stated scope, a verified-at date, nothing false is asserted. Line 2 claims no content support. SOURCES.md:51 also places S022 in the "Static canonical preflight" reading order (`S020 → S021 → S022 → S023 …`), so including it in the entry's opened-documentation set is consistent with the corpus's own topic map.
   - [INFERENCE] Lines 21–23 ("not guarantees that it chooses the publisher's preference") restate S022's teaching but attribute it to Google's annotation guidance (S021) without an id. That is a possible under-attribution elsewhere in the entry, not a defect of this pair.
6. **EOF completeness analogue.** Line 200 records S024/S025 as "re-fetched this round (receipts HOLD) but … missing from the recheck paragraph's row list above". S022 and S023 are in the same position: range-cited on line 2, r26 receipts `S022.json`/`S023.json` both HOLD, and neither is named on lines 184/200. This is a provenance-completeness gap in r26 EOF prose, not a wrong attribution. It does not make this pair STALE.

## Verdict
**HOLD** (artifact kind). The metadata date claim (S022 documentation opened 2026-10-20 in round 22) is supported at its stated scope by SOURCES.md and the round-22 lesson. r26's HOLD re-fetch shows the premise is not stale. There is no STALE, so no `[r27-recheck S022 STALE]` correction is required.

Impacted axis: freshness only. There is no identity change and no duplicate authority. The denominator is unchanged: no new citing form was found for S022 in this file, and no discovered pair is added.

## Suggested C1 ledger record (pairs.json)
```json
{"row":"S022","file":"corpus/knowledge/static-canonical-preflight.md","kind":"artifact","verdict":"HOLD","reason":"Only citation is line-2 verified-at range S020-S027 (historical round-22 metadata). Date claim matches SOURCES S022 opened 2026-10-20 and the round-22 lesson quote; r26 re-fetch 2026-10-21 HOLD, page date 2026-08-21 unchanged. No content claim attributed to S022 here; historical date preserved, not relabelled r27.","evidence":"corpus/SOURCES.md","contains":"Opening paragraph, updated 2026-08-21; opened 2026-10-20"}
```
Alternate evidence (also verified present): `corpus/lessons/round-22.md` contains `Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons`.

## Optional append (not a STALE correction; L1 discretion, append-only)
> - r27 provenance note (not STALE): line 2's `(S020-S027)` range also covers S022 and S023, which ground no statement in this entry (SOURCES used-by for S022 is `corpus/lessons/round-22.md`). Their 2026-10-20 opened dates hold; r26 receipts `.ufo/waves/round-26/rechecks/S022.json` and `S023.json` are HOLD but were not named on lines 184/200.

## Uncertainties
- There are no round-22 retained raw bytes for S022. The 2026-10-20 opening rests on the commit date plus the contemporaneous quote.
- The S023 statement above relies only on its receipt verdict and the absence of an S023 citation in the file. S023's own pair is not adjudicated here.
