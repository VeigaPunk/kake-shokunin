# Pair13B — critic: (S008, corpus/knowledge/ghp-etag-anatomy.md)

Seat: KakeR27.Pair13B (critic, read-only, leaf). Axis: freshness. Milestone: r27-full-citing-set.
Pair A report NOT read (independent judgment). No fetches, no r24 material, no edits outside this report, no tool installs.

## Verdict: HOLD (kind: artifact) — r26 EOF retry-provenance boilerplate; true at its own scope, irrelevant to this entry's sources; no correction required.

## Citing set for this pair
- `rg -o '\bS\d{3,}\b'` on the file: S008 ×1, S009 ×6, S010 ×9. No `S0NN–S0MM`-style range anywhere in the file expands to S008 (the `S0NN` receipt pattern has no digits, so neither regex matches it).
- The only S008 occurrence is **line 60**, the "Round-26 source recheck" bullet (append-only EOF prose; `git blame` → e28312b, 2026-10-21, "round-26: re-verify 32 cited sources…").
- Full citing clause (line 60): "Rows S009 and S010 were re-fetched by one public GET each (`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`) and judged HOLD at their anchors against the retained bytes"
- File identity: sha256 `fa71ecd60370f81ec9d5ec596cc04483221392b9901068b4e92cef881a801d95`. This is identical at working tree, `be375d9`, `83528f7`, and `.ufo/waves/round-27/frozen/corpus/knowledge/ghp-etag-anatomy.md`.
- c1-before.json (rev 83528f7) lists `{row:S008,file:corpus/knowledge/ghp-etag-anatomy.md}` under `missing`. This confirms the pair is one of the 16 baseline-unadjudicated pairs.

## What the citation claims (its own scope)
The line makes no claim about S008's content. It also does not say S008 supports, or is used by, this entry. It asserts only one fact: the round-26 S008 retrieval is recorded in `manifest-retry.json`, not `manifest.json`. That's a historical fetch-provenance statement about the round, dated 2026-10-21.

## Tests against artifacts (all local, committed at r26)
1. **Retry record exists and is S008-only.** `.ufo/waves/round-26/fetched/manifest-retry.json` (sha256 `84e83fb0…5d1b`, tracked) has exactly one entry. Its fields are: `"row": "S008"`, `"attempt": 2`, `"status": 200`, `"fetchedAt": "2026-10-21T15:11:01.972009+00:00"`, and `"file": "S008-1-retry.raw.gz"`. The reason is `"first attempt TimeoutError at 60s; single retry with 240s timeout"`.
2. **Failed first attempt is in manifest.json.** S008 index 1 there has `"status": null`, `"error": "TimeoutError: The read operation timed out"`, bytes 0, and the empty-string sha256 `e3b0c442…b855`. So the successful S008 bytes really do come via the retry manifest, not manifest.json.
3. **Retry bytes match their recorded hash.** `gzip.decompress(S008-1-retry.raw.gz)` has sha256 `93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084`. That equals `manifest-retry.json` `sha256` and the r26 receipt `.ufo/waves/round-26/rechecks/S008.json`, which records verdict HOLD with "re-fetched 2026-10-21 (attempt 2 after a 60s timeout)".
4. **Clause's other rows.** In manifest.json, S009 and S010 are both `status 200`, each with a single entry, fetchedAt 2026-10-21T15:10:38Z. "One public GET each … manifest.json" holds for the rows that the clause actually quantifies over.
5. **Dates preserved.** The bullet's "2026-10-21" matches every fetchedAt. Line 60 itself states that the older `verified-at`/`reopened` 2026-10-19 dates remain the historical record. Nothing is rewritten, and no stale date premise is present.
6. **No unsupported scope expansion.** SOURCES.md:16 (S008) has `opened 2026-10-19` and used-by `corpus/knowledge/ghp-served-set.md` only. ghp-etag-anatomy's header (line 1) lists only `S009, S010`. So the file never claims S008 as a source, and SOURCES doesn't either. The registry and the entry are consistent.

## Strongest counterexamples tried
- **"Implies S008 was re-fetched for / supports this entry."** Rejected. The clause's subject is "Rows S009 and S010". S008 sits inside the provenance parenthetical as the round's single retry. The r26 w2 critic reached the same reading: `.ufo/waves/round-26/w2/Rejection07S013.md:70` says "It is true of the round but irrelevant to this entry. This is a provenance-precision nit, not staleness." It names ghp-etag-anatomy among the 5 files carrying the identical wording.
- **"One public GET each" is false for S008 (two GETs).** Rejected for this pair. "each" ranges over S009/S010, and the clause never asserts a GET count for S008. (Cross-pair note, not mine to adjudicate: in `ghp-served-set.md:83`, S008 *is* inside "Rows … S008 were re-fetched by one public GET each". There, the two-attempt history is arguably a precision gap. That pair is already r26-decided, so I'm only flagging it.)
- **Stale vs. retry-boilerplate distinction.** This is irrelevant retry boilerplate, not a stale premise and not a source-date issue. No S008 source text is quoted or paraphrased in this file, so a fresh S008 fetch could not change the verdict. An artifact verdict is therefore the right kind; a source verdict would claim content support that the line never asserts.
- **Unlike ghp-served-set.md:95**, this file has no explicit "names the round's retry, not a source of this entry" disclaimer. That's a readability asymmetry, not wrong attribution, so it doesn't make the pair STALE.

## Suggested C1 ledger record (pairs.json)
```json
{"row":"S008","file":"corpus/knowledge/ghp-etag-anatomy.md","kind":"artifact","verdict":"HOLD","reason":"Only occurrence is line-60 r26 EOF provenance boilerplate '(…manifest.json, S008 via manifest-retry.json)'; the entry cites S009/S010 only and claims no S008 content. Committed r26 retry manifest records S008 attempt 2 status 200 (2026-10-21, after 60s timeout in manifest.json), retry bytes sha256 93281a63…6084 match. True of the round, irrelevant to entry scope; not stale (cf. r26 w2/Rejection07S013.md:70).","evidence":".ufo/waves/round-26/fetched/manifest-retry.json","contains":"\"file\": \"S008-1-retry.raw.gz\""}
```
The `contains` check is byte-exact against the committed blob: the substring `"file": "S008-1-retry.raw.gz"` appears verbatim, including spacing, in `manifest-retry.json`. As an alternative that is also single-line, unique, and verbatim, `contains` could be `"reason": "first attempt TimeoutError at 60s; single retry with 240s timeout"`.

## Correction wording
- **Required: none.** The verdict is HOLD, so no `[r27-recheck S008 STALE]` marker is warranted. Adding one would wrongly mark the pair STALE.
- **Optional precision note (non-STALE, parity with ghp-served-set.md:95)**, if L1 wants it. It should be append-only and leave the original line-60 bytes and the 2026-10-21/2026-10-19 dates untouched:
  `- Round-27 precision note (append-only): the words "S008 via `manifest-retry.json`" in the round-26 recheck bullet name that round's single retried fetch (S008 attempt 2), not a source of this entry; this entry cites S009 and S010 only. HOLD (w1/Pair13B.md).`

## Uncertainties
- None on the facts: all the evidence is committed r26 artifacts with matching hashes. The only judgment call is interpretive, namely whether a provenance parenthetical counts as "attribution". I resolved it at the clause's own stated scope, and the r26 w2 critic reached the same reading independently.
- I didn't re-fetch S008 bytes in r27 (r27 `fetched/manifest.json` covers only S001–S006). That isn't needed for an artifact-kind verdict.
