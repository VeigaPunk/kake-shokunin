# Pair14B — critic: (S008, corpus/knowledge/static-canonical-preflight.md)

Axis: freshness. Milestone: r27-full-citing-set. Read-only seat; the only write is this report. I did not read the A-side report.
Measured at HEAD `be375d90afc6fc7aca369ab3cf5247bf460aeed2`. The target file is byte-identical to frozen base `83528f7c`:
sha256 `833b28f26fa7309f7e31398275bae2f704969d8e6f095bc5bb96250da5c531bc` at both.

## Verdict: HOLD (kind artifact). No correction needed.

## Citing set for this pair (ranges expanded)
- I ran `rg -n 'S[0-9]{3}'` over the 203-line file. **Line 184 is the only line that cites S008.**
- No range in the file covers 8:
  - line 2 `S020-S027` expands to 20–27;
  - line 54 `S001–S006` expands to 1–6;
  - line 159 `§5.6–5.7` is not an S-range.
- The file has no content reliance on S008. It has no tar, `1.35`, pattern-matching or wildcard statement (checked with `rg -i 'tar|1\.35|pattern-matching|wildcard'`). Every hit is unrelated canonical or HTML wording.
- In SOURCES.md:16, the S008 used-by cell lists only `corpus/knowledge/ghp-served-set.md`. This file is not a consumer.
- No new citing form was found, so no discovered pair is added. The denominator is unchanged.

## The citing claim (line 184, full)
"Round-26 source recheck (2026-10-21, append-only; original lines unchanged). Rows S020, S021, S026, S027, S028, S029, S030, S031, S032, S033 and S034 were re-fetched by one public GET each (`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`) and judged HOLD …; Counting command: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`."

- **Its own scope:** a provenance pointer saying that the round-26 retained bytes are in `manifest.json`, with S008's bytes in `manifest-retry.json`.
- **What it does not claim:**
  - S008 is not in this entry's row list;
  - S008 is not called a source of the entry;
  - S008 is not said to have taken one GET.
- **Classification:** this is r26 end-of-file retry boilerplate, not a stale premise. The same parenthetical appears word for word in four other recheck paragraphs:
  - `crawl-scope-per-host.md:57`
  - `ghp-custom-domain.md:62`
  - `ghp-etag-anatomy.md:60`
  - `ghp-served-set.md:83`
- **Line origin:** `git blame` gives commit `e28312b` (2026-10-21, "round-26: re-verify 32 cited sources…").

## Adversarial tests (each tried to falsify; all failed to falsify)
1. **Does `manifest-retry.json` actually hold S008?** Yes. HEAD blob sha256 is `84e83fb0cf5bf431eb029a9ab8cab69b661054e6e992b862e87b514786a65d1b`. It has a single record:
   - row `S008`, index 1, attempt 2, status 200;
   - `fetchedAt` `2026-10-21T15:11:01.972009+00:00`;
   - file `S008-1-retry.raw.gz`, 512359 bytes;
   - sha256 `93281a63…81606084`;
   - reason "first attempt TimeoutError at 60s; single retry with 240s timeout".
2. **Do the retained bytes match?** Yes. Gunzipping `S008-1-retry.raw.gz` gives 512359 bytes whose sha256 equals the manifest value. The bytes contain the receipt quote "When wildcards match slash (the default for exclusion members)".
3. **Is the pointer needed, i.e. is the `manifest.json` S008 slot unusable?** Yes:
   - the `manifest.json` S008 slot has status null, error "TimeoutError: The read operation timed out", `fetchedAt` 15:09:36;
   - its sha256 is `e3b0c442…b855`, the hash of empty input.

   So "S008 via manifest-retry.json" is accurate and not cosmetic. The `round-26-verifier-spotcheck.md:38` line agrees: "The S008 retry supersedes only its failed first slot."
4. **Could "one public GET each" falsely cover S008?** No. The sentence lists only S020–S034 rows (11 IDs), and each has exactly one status-200 entry in `manifest.json` (all at 15:10:43–15:10:52). The S008 parenthetical itself signals a separate retry.
   - [INFERENCE] A reader could still misread S008 as one of this entry's rows. That is an ambiguity, not a wrong attribution at its stated scope.
5. **Has the r26 S008 recheck held up?** Yes. `.ufo/waves/round-26/rechecks/S008.json` records verdict HOLD and fetchIndex 1, with this reason: "Commit-pinned texi re-fetched 2026-10-21 (attempt 2 after a 60s timeout), status 200, 512,359 bytes". It is consistent with the retry manifest.
6. **Precedent for the same words:** `ghp-served-set.md:95` (r26 w2) says "The words “S008 via `manifest-retry.json`” in the recheck paragraph name the round's retry, not a source of this entry". My reading of line 184 matches. This is peer evidence only; I verified it independently in tests 1–5.

## Freshness and dates (all preserved; none rewritten)
| Date | What it is | Status |
|---|---|---|
| 2026-10-19 | S008 opened/mined date (SOURCES.md:16, status `mined`, 365d) | Historical source date, not a stale premise |
| r20 | The `1.35` label erratum (round-20.md:310) | Applies to ghp-served-set and crawl-scope, not this file; irrelevant here |
| 2026-10-21 | r26 dated provenance (15:09:36 failed, 15:11:01 retry) | Correct as written |

- round-26.md:23 gives a "15:09–15:10 UTC" window for the 34 fetches. The 15:11:01 retry falls outside it, but round-26.md:23 is not this citing line, so it does not affect this pair.
- These are r26 observations carried forward. They are not relabelled as fresh r27 source observations.
- No r24 artifact was read or retried.

## Suggested C1 ledger record (pairs.json top-level `pairs`)
```json
{"row":"S008","file":"corpus/knowledge/static-canonical-preflight.md","kind":"artifact","verdict":"HOLD","evidence":".ufo/waves/round-26/fetched/manifest-retry.json","contains":"first attempt TimeoutError at 60s; single retry with 240s timeout","reason":"Line 184 only (no range covers S008): r26 EOF provenance pointer naming where S008's retry bytes live, not a source of this entry. manifest.json S008 slot failed (TimeoutError, empty sha256); manifest-retry.json holds S008 attempt 2, status 200, 512359 bytes, sha256 verified against S008-1-retry.raw.gz. Carried r26 observation (2026-10-21), not an r27 fresh fetch."}
```
- The `contains` substring is present exactly once in the HEAD blob (checked with `git show HEAD:… | grep -c` → 1). This satisfies `count_c1.py`'s `p['contains'] in blob(p['evidence'])` check.

## Correction wording
None required: the verdict is HOLD, so no `[r27-recheck S008 STALE]` tag is needed.

Optional precision note for the integrator, not STALE and not required: "S008 in line 184 names the round-26 retry manifest only; S008 is not a source of this entry."

## Uncertainties
- The ledger record is for the r27 `pairs.json`, which does not exist yet. I did not run `count_c1.py` or validate the record end to end (no checks mid-flight).
- The S028/S033 shared-sha256 note (identical `21c1cdce…` digest, one URL per LOG.md:1026) is outside this pair and not judged here.

## Tool installs
None.
