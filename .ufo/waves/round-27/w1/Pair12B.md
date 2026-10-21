# Pair12B — critic: (S008, corpus/knowledge/ghp-custom-domain.md)

Seat: KakeR27.Pair12B (B / adversarial critic, read-only). Axis judged: freshness. Milestone r27-full-citing-set.
Independence: Pair12A's report was not read. No network fetch was made; no r24 material was read.
Measured tree: HEAD `be375d90afc6fc7aca369ab3cf5247bf460aeed2`. The file's sha256 `65dd561af5cc7b189ae97caf67a52aa85ff794dc11c164cf07d2e0f91a7b19b6` is identical in the working tree, at be375d9, at base 83528f7, and in `frozen/expected.json`.

## Verdict
**HOLD (kind = artifact)**. This is r26 EOF provenance plus retry boilerplate. At its own scope, a retrieval-location pointer, the sentence is true. It makes no source attribution for any of this file's claims.

## Citing location (complete)
- The file has exactly one `S008` token (`rg -o` count = 1). It sits on line 62, inside `## Round-26 source recheck`.
- No range in the file expands to S008. The header (`source: S003, S005, S007`), line 1, the claim body, and the r20 correction (lines 50–58) never mention S008.
- Full surrounding claim, line 62: "Rows S003, S005 and S007 were re-fetched by one public GET each (`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`) and judged HOLD at their anchors …"
- Line 62 was introduced by commit e28312b (2026-10-21 13:08:15 -0300, "round-26: re-verify 32 cited sources…").

## What the S008 fragment actually asserts
Its only assertion is that S008's r26 retrieval is recorded in `manifest-retry.json`, alongside `manifest.json`. The grammatical subject of "judged HOLD at their anchors" is "Rows S003, S005 and S007". S008 is not one of those rows.

Evidence that the fragment is true:
- `.ufo/waves/round-26/fetched/manifest-retry.json` is tracked at be375d9 (blob 637e278d). Its only entry is `"row": "S008"`, `attempt: 2`, `status: 200`, fetchedAt `2026-10-21T15:11:01.972009+00:00`, sha256 `93281a63…6084`, with `"reason": "first attempt TimeoutError at 60s; single retry with 240s timeout"`.
- `manifest.json` records the first S008 attempt as `status: null`, `"error": "TimeoutError: The read operation timed out"`, and the empty-content sha `e3b0c442…b855`.
- I re-hashed both retained gz files locally. `S008-1-retry.raw.gz` decompresses to 512,359 bytes and its sha256 matches the manifest. `S008-1.raw.gz` decompresses to 0 bytes and matches the empty sha. Both observations are mine, from this run.
- The r26 receipt `.ufo/waves/round-26/rechecks/S008.json` is `verdict: HOLD`, `fetchIndex: 1`, and its reason states "attempt 2 after a 60s timeout". This agrees with the manifests.
- Freshness ordering is consistent. The retry was fetched at 15:11 UTC, before e28312b at 16:08 UTC. No date in line 62 conflicts with the artifacts.

## Counterexamples tested
1. **False attribution.** Does line 62 imply S008 supports a claim here? No. The `corpus/SOURCES.md:16` row for S008 is GNU tar (`tar.texi?id=cfdb891…`), with `usedBy: corpus/knowledge/ghp-served-set.md` only. The r26 population row agrees. `statements.json` has no (S008, ghp-custom-domain.md) pair. The line attributes nothing to S008. The only verdict it carries is HOLD for S003/S005/S007, and receipts `rechecks/S003.json`, `S005.json` and `S007.json` all read `verdict: HOLD`.
2. **"One public GET each."** S003, S005 and S007 each have exactly one manifest entry (index 1). S008 needed two GETs, and the parenthetical is exactly where that exception is noted. No contradiction.
3. **Stale premise vs. source date vs. retry boilerplate.**
   - Not a stale premise: nothing in the file depends on S008 content.
   - Not a source date: S008's `opened 2026-10-19` and `recheck 365d` are not restated here.
   - It is boilerplate: the identical fragment `S008 via \`manifest-retry.json\`` appears in crawl-scope-per-host.md:57, ghp-custom-domain.md:62, ghp-etag-anatomy.md:60, ghp-served-set.md:83 and :95, and static-canonical-preflight.md:184. It is a shared r26 pointer template.
4. **Historical dates.** `verified-at: 2026-10-19`, "quotes reopened 2026-10-19", "Recheck (2026-10-19)" and the r20 erratum date are left unchanged. Line 62 explicitly calls them the historical record and says it does not rewrite them. This is not a freshness defect.
5. **Pointer resolvability.** Bare `manifest-retry.json` resolves as a sibling of the path cited just before it (`.ufo/waves/round-26/fetched/`). That file exists and is tracked.

## Tradeoff (not a defect)
Mentioning S008 in a file that cites only S003/S005/S007 is irrelevant noise. A careless reader could take S008 to be one of this entry's sources. This is a readability tradeoff, not a wrong attribution at the sentence's own scope, so a STALE verdict would be unsupported. For the same reason, no `[r27-recheck S008 STALE]` marker is warranted.

## Suggested C1 ledger record (pairs.json → pairs[])
```json
{"row":"S008","file":"corpus/knowledge/ghp-custom-domain.md","kind":"artifact","verdict":"HOLD","evidence":".ufo/waves/round-26/fetched/manifest-retry.json","contains":"\"file\": \"S008-1-retry.raw.gz\"","reason":"Only S008 token is r26 EOF provenance boilerplate at line 62 ('S008 via `manifest-retry.json`'); it locates S008's r26 retry (attempt 2, status 200, sha256 93281a63…6084, after 60s timeout) and attributes no claim of this file to S008 (SOURCES S008 usedBy = ghp-served-set.md only). True at its own stated scope; carried r26 retrieval fact, not an r27 fresh source observation."}
```
I checked `contains` against the blob at be375d9 with `git show … | grep -cF`, which returned 1. An alternative substring that also returned 1 is `"reason": "first attempt TimeoutError at 60s; single retry with 240s timeout"`. Note: `count_c1.py` reads `evidence` from `--revision`, and this blob is committed, so the check passes at be375d9 and its descendants.

## Correction wording
None needed; the verdict is HOLD. If L1 decides to remove the reader ambiguity, append rather than edit (line 62 stays as it is). Optional wording:
> `[r27-recheck S008 HOLD]` (2026-10-21) The S008 mention on the round-26 line is a shared retrieval pointer (its r26 retry is in `manifest-retry.json`); S008 (GNU tar) is not a source for this entry, whose sources remain S003, S005 and S007.

## Denominator
No new citing pair was found in this file. The pairs present are S003, S005, S007 and S008, and each is already in the frozen/c1-before sets. The count stays the same.

## Uncertainty
- I did not open the S008 source text, because this pair's scope does not depend on its content. The S008 HOLD comes from the r26 receipt, not from a fresh r27 reading.
- Installs/updates: none. Scratch directories: none used.
