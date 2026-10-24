# Pair05B — S004 / corpus/knowledge/publish-channels.md

Axes: freshness (assigned); operability (preserve complete expanded citing-set obligation; no implementation judgment).

## Finding

Suggested C1 disposition: **HOLD, artifact-scoped historical metadata only**. This is author-side evidence, not canonical admission or a current source re-verification.

The sole S004 citing occurrence is the expanded range `S001-S007` on `corpus/knowledge/publish-channels.md:2`. Expand it to S001, S002, S003, **S004**, S005, S006, S007. The pair must remain in the denominator despite the absence of a literal standalone S004 token. No new pair beyond this frozen obligation was discovered.

Full citing line read:

> verified-at: 2026-09-26 (kimi-webbridge "not supported on Linux" check) and 2026-09-28 (round-1 commit cd5b381 that introduced this entry; wz1-ds4cc emptied 2026-09-28T21:42-03:00); round-20 corrections 2026-10-19 (S001-S007 opened that day) — historical-not-live-reverified; no live domain recheck performed

Its S004-specific assertion is that the source was opened on 2026-10-19. It does not assert that S004 independently supports every round-20 correction or the historical platform/channel claims.

## Strongest counterexample and scope test

Attempted falsification: interpret the date-line range as attribution of all corrections to every source. S004 teaches artifact shape/deployment requirements, not custom-domain ownership or version-specific hidden-path behavior. Under that interpretation the attribution would be unsupported.

Local context defeats that interpretation:

- `publish-channels.md:1` explicitly attributes the EOF corrections to S001, S002, S003, S005 and S007, omitting S004/S006.
- Lines 58 and 60 cite only S001/S002 for packaging/hidden paths.
- Line 59 cites S005/S003/S007 and line 61 S003/S005 for CNAME/domain behavior.
- Line 84 explicitly repeats those five source identities and their separate contributions; S004 is absent.
- `corpus/SOURCES.md:12` records S004's historical fetched/opened date as 2026-10-19 and its own artifact-shape scope.

Thus no stale S004 premise was found at the actual citing scope. Replacing 2026-10-19 with 2026-10-21 would incorrectly rewrite historical provenance rather than improve freshness.

## Located evidence (support snippets each <=25 words)

1. `corpus/knowledge/publish-channels.md:2`: `round-20 corrections 2026-10-19 (S001-S007 opened that day)`.
2. `corpus/SOURCES.md:12`: `| mined | 2026-10-19 | 90d | corpus/knowledge/ghp-served-set.md |`.
3. `corpus/knowledge/publish-channels.md:1`: `S001, S002, S003, S005 and S007 in corpus/SOURCES.md support the EOF round-20 corrections`.
4. `corpus/knowledge/publish-channels.md:84`: `The round-20 correction lines in this entry cite S001, S002, S003, S005 and S007 (lines 58-61).`.
5. `.ufo/waves/round-26/fetched/manifest-retry.json:3`: `"row": "S008"`.
6. `.ufo/waves/round-26/rechecks/S004.json:5`: `The tar file must be under 10GB in size and should not contain any symbolic or hard links`.

The r26 retry artifact records only S008 attempt 2 on 2026-10-21, not an S004 retry. Its `first attempt TimeoutError at 60s; single retry with 240s timeout` is irrelevant to this pair's historical opened-date claim. No retry was performed here.

The S004 r26 manifest entry reports status 200, fetchedAt `2026-10-21T15:09:34.536589+00:00`, raw-byte SHA256 `5c15ef2d916a57a9877f75518968df2d644799f08630f9beb5ed8d699206a385`. This is later retained provenance, not proof of a new r27 opening or a reason to change the historical date. The r26 receipt is a scoped artifact, not an independently repeated observation by this seat.

## Suggested C1 ledger record

```json
{
  "row": "S004",
  "file": "corpus/knowledge/publish-channels.md",
  "kind": "artifact",
  "verdict": "HOLD",
  "reason": "Line 2 expands S001-S007 only for the historical statement that these sources were opened on 2026-10-19. SOURCES.md S004 records that date. Lines 1, 58-61 and 84 attribute the substantive corrections to other explicitly named sources; this is not S004 support for all platform claims or a fresh r27 source observation.",
  "evidence": "corpus/SOURCES.md",
  "contains": "| mined | 2026-10-19 | 90d | corpus/knowledge/ghp-served-set.md |"
}
```

Smallest safe correction: **none required**. Preserve the historical dates and explicit scope; do not append an `[r27-recheck S004 STALE]` marker without an actual unsupported claim. The evidence substring is not row-unique on its own; the located S004 row at SOURCES.md:12 supplies identity and date. That is an oracle-interface limitation, not grounds to inflate the finding into current-source verification.

## Evidence hashes and limits

SHA256 of observed working-file bytes:

- `corpus/knowledge/publish-channels.md`: `18042de41ae254a0e4138a6a1cfe6e4bdaa2bbf59b4c1de0181bca9f1bca73be`
- `corpus/SOURCES.md`: `5001eadee20c65c5df364a88430b6b0e76a99940afc282d72fecdd6d7c6be62d`
- `.ufo/waves/round-26/fetched/manifest-retry.json`: `84e83fb0cf5bf431eb029a9ab8cab69b661054e6e992b862e87b514786a65d1b`
- `.ufo/waves/round-26/fetched/manifest.json`: `28f9944d36db40b56362903d6ba1245ae54d26a0e612615b3174f45ea3c7cba8`
- `.ufo/waves/round-26/rechecks/S004.json`: `81233a452aac4393230e3678a6d628a91e328c59c7a6ae83f8f7fed9bb23aa5a`

Read frozen contract and both independent counting oracles; did not execute them. No A report read, external fetch, r24 work retrieval/retry, source/ledger edit, build, test, formatter, runtime invocation, or install. Historical opening is established only to the corpus-record scope; contemporaneous round-20 network logs were not supplied or claimed.
