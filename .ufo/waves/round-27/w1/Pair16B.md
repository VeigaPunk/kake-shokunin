# Pair16B — adversarial critic: (S023, corpus/knowledge/static-canonical-preflight.md)

Seat `KakeR27.Pair16B` (critic, leaf, read-only). Axis: freshness. Milestone `r27-full-citing-set`. Checked 2026-10-21.
A report (Pair16A) NOT read. No network fetch, no r24 material read, no tool installed/updated, no source/ledger edits.
Measured file: `corpus/knowledge/static-canonical-preflight.md`, sha256 `833b28f26fa7309f7e31398275bae2f704969d8e6f095bc5bb96250da5c531bc` (working tree == blob at `be375d9`).

## Verdict: HOLD (artifact-kind) — attack failed; the pair is date metadata only

## 1. Citing lines (ranges expanded)

- `count_c1.py` regexes over the file: **no literal `S023`**. The pair exists only through the range on **line 2**:
  > `verified-at: 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029), documentation opened this round; local behavior has separate committed round22 receipts, not live website verification`
- Other ranges/literals in the file do not reach S023: `S001–S006` (line 54), `S028-S029` (line 2), and literal lists at lines 1, 98–101, 184, 186–203. `S0NN` (line 184) does not match `\bS(\d{3,})\b`.
- Frozen population membership: `.ufo/waves/round-27/frozen/population.json` row `"id": "S023"`. The pair is listed in `c1-before.json` (missing) and in `c2-oracle.json` (one of the 16 expected `unadjudicated_citing_pair`).

## 2. Claim scope

Line 2 claims one thing about S023: as part of S020–S027, its documentation was opened on 2026-10-20 in the authoring round, which is round 22. No body sentence in the entry cites S023. The `source:` header (line 1) lists only S020/S021/S026/S027. The round-22 lesson confirms that split: `corpus/lessons/round-22.md:55` says “C1's knowledge entry cites S020/S021/S026/S027; the remaining rows ground its implementation/rejection boundaries in this Gate.” Because of that, the range attributes **no knowledge claim** to S023. It is a verification-date stamp only. The r26 ledger handled S020's identical stamp the same way (`statements.json`: “R2 is a verification-date stamp only; content HOLD.”).

## 3. Falsification attempts

| # | Attack | Result |
|---|---|---|
| A1 | Date wrong: was S023 actually opened 2026-10-20? | **Failed.** `corpus/lessons/round-22.md` contains `### Sources opened for C1 (2026-10-20)`, followed by the S023 row (`| S023 | https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | Section 4.6.8.4:`). `.ufo/waves/round-22/w1/Case06.md` contains `Primary, opened this session, access date 2026-10-20` and the S023 row with digest `82a81f23…f6b7`. `corpus/SOURCES.md:31` says `opened 2026-10-20`. |
| A2 | Living-standard drift: did the date-labelled read capture different bytes? | **Failed.** The page has `last-modified: Tue, 20 Oct 2026 12:58:32 GMT` (r26 `fetched/manifest.json`). Round-22 Case06 was committed at `c0fd6d5` 2026-10-20T18:30:55-03:00 (21:30Z) and records sha256 `82a81f233583716daf76ce20938a399016dfd877a9368ea2cdb1a60bcd3df6b7`. I recomputed that digest: `zcat .ufo/waves/round-26/fetched/S023-1.raw.gz \| sha256sum` gives the same value. The r22 read therefore falls between 12:58Z and 21:30Z on 2026-10-20 and used byte-identical content. The date holds in both UTC and -03:00. |
| A3 | Retroactive range: the `(S020-S027)` qualifier was added later | **Partly true, but harmless.** Original `c0fd6d5` line 2 read `verified-at: 2026-10-20, documentation opened this round`. Round-22 recovery commit `b539cc1` (2026-10-21T03:16-03:00) added `(S020-S027)`. It is still round 22, and the date it attaches to S023 is correct per A1/A2. This adds precision; it does not misattribute anything. |
| A4 | Stale premise: the “2026-10-20 … opened this round” wording ignores later re-opens (r23 `corpus/lessons/round-23.md:37` “Re-opened without change: S021, S023…”; the r26 re-fetch on 2026-10-21) | **Not STALE.** The entry's own r26 EOF note (line 184) contains `Older verified-at/reopened dates in this entry remain the historical record of the earlier reading`. “this round” is round-22 history. Preserved date: 2026-10-20. |
| A5 | Unsupported scope: does the range imply S023 supports a body claim (for example rel keyword case-insensitivity, or canonical as the preferred URL)? | **Failed.** grep finds no `case-insens`, `ASCII`, `link type` or `keyword` claim in the entry. Its only `rel=` mention (line 18) is attributed to Google/S021. |
| A6 | Source content changed so that S023's row no longer holds | **Failed.** In the retained r26 text `.ufo/waves/round-26/fetched/text/S023-1.txt`, each of the following occurs exactly once: “The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document.” and “Keywords are always ASCII case-insensitive, and must be compared as such.” |
| A7 | r26 manifest-retry relevance | **Irrelevant boilerplate for S023.** `manifest-retry.json` has no S023 entry. Line 184's “S008 via `manifest-retry.json`” concerns S008 only. |

## 4. Findings that are not STALE (disclosed; parent decides)

- **F1: the r26 EOF row list omits S023 (and S022).** Line 184 lists the rows re-fetched in r26 as `S020, S021, S026…S034`. Line 200 later adds S024/S025. Yet r26 `fetched/manifest.json` re-fetched S023 (status 200, same sha256), and `.ufo/waves/round-26/rechecks/S023.json` records `"verdict": "HOLD"`. This is an omission in the r26 record, not a wrong attribution. Line 184 does not cite S023, so it is not part of this pair. Severity: low (record completeness).
- **F2: r26's FalsifyS023 found zero S023 mentions.** `.ufo/waves/round-26/w2/FalsifyS023.md` states that `corpus/knowledge/*` “contains zero S023 mentions”. That is literally true, but it is false once ranges are expanded. This is the C2 fail-open class. It is r26 historical debt and is not relabelled here.
- **F3: no r27 fresh observation exists for S023.** The r27 `fetched/manifest.json` rows are only S001–S006. A `kind:"source"` record would fail `count_c1.py` with `source_missing`, so the record below is `kind:"artifact"`. It rests on r22/r26 retained artifacts and is not presented as an r27 fresh source observation.

## 5. Suggested C1 ledger record

```json
{"row":"S023","file":"corpus/knowledge/static-canonical-preflight.md","kind":"artifact","verdict":"HOLD","reason":"Pair arises only from line 2 range 'verified-at: 2026-10-20 (S020-S027)'; S023 grounds no body claim (header and r22 lesson:55 list S020/S021/S026/S027 only), so scope is the historical opening date. Round-22 Case06 'Primary, opened this session, access date 2026-10-20' pins S023 to sha256 82a81f23...f6b7, equal to r26 retained S023-1.raw.gz and to page Last-Modified 2026-10-20T12:58:32Z, which precedes the Case06 commit at 21:30Z. Later reopenings (r23, r26 HOLD) do not rewrite the stamp (line 184). Carried from r22/r26 artifacts; not an r27 fresh fetch.","evidence":".ufo/waves/round-22/w1/Case06.md","contains":"| S023 | WHATWG HTML §4.6.8.4, https://html.spec.whatwg.org/multipage/links.html#link-type-canonical |"}
```

The `contains` substring was verified once in the `be375d9` blob. Alternative evidence that also verified once: `corpus/lessons/round-22.md` with `### Sources opened for C1 (2026-10-20)`, and `.ufo/waves/round-26/fetched/manifest.json` with `"sha256": "82a81f233583716daf76ce20938a399016dfd877a9368ea2cdb1a60bcd3df6b7"`.

## 6. Correction wording

**None required.** With HOLD, no `[r27-recheck S023 STALE]` marker is owed.

Optional precision note for F1, if L1 wants the record complete. It is not a STALE correction. It adds a literal S023 to the same file, so it creates no new pair:

> - r27 precision note (not STALE): S022 and S023 were also re-fetched in round 26 (`.ufo/waves/round-26/fetched/manifest.json`; receipts `rechecks/S022.json`, `rechecks/S023.json`) but are missing from the round-26 recheck row list above. In this entry S023 appears only through line 2's `(S020-S027)` verification-date range and grounds no body statement.

Before using that wording, L1 must separately confirm the S022 receipt verdict. I did not read `rechecks/S022.json`.

## 7. Uncertainties

- The date can be wall-clock dependent. Every bound I found is inside 2026-10-20 in both UTC and -03:00, so I see no residual uncertainty.
- I did not judge the pair-row or anchor quality of the round-22 Case06 text beyond the S023 row and date line.
- Discovered pairs: none added by this seat.
