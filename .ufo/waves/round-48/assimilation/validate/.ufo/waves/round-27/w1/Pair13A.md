# Pair13A — reviewer: (S008, corpus/knowledge/ghp-etag-anatomy.md)

Seat: KakeR27.Pair13A (reviewer, read-only leaf). Axis judged: freshness. Milestone r27-full-citing-set.
Measured revision: `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (HEAD; base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`).
Read-only: no fetch, no corpus/ledger edit, no r24 material read, no tool install, no /tmp use.
Disclosure: while checking the report-trailer convention I opened the sibling critic file `.ufo/waves/round-27/w1/Pair13B.md` for the same pair. Every finding below was re-derived by me from git blobs at the measured revision (hashes, byte counts, receipts, manifests) before/independent of that file; I did not copy its reasoning. It reaches the same verdict by a different route, and I record one finding it missed (the count_c1 `kind` constraint).

## Verdict: **HOLD**, kind = **artifact**

At its own stated scope the S008 mention is a true round-level fetch-provenance pointer. It attributes no claim of this entry to S008 and makes no source assertion about S008's content, so no fresh S008 fetch could falsify it. Not a stale premise, not a source-date issue, not a drift: it is shared r26 EOF boilerplate that is true of the round and irrelevant to this entry's scope.

## Citing set for this pair (complete)

- Token census of the file at `be375d9` with the two regexes `count_c1.py` uses (`\bS(\d{3,})\b`, `\bS(\d{3,})\s*([-–—]|\.\.|to|through)\s*S(\d{3,})\b`): `S008`×1, `S009`×6, `S010`×9. **No range in the file matches at all**, so no range expands to S008. The receipt pattern `S0NN.json` has no digits and matches neither regex.
- The single S008 occurrence is **line 60**, inside `## Round-26 source recheck`. `git blame` at the measured revision: `e28312b (kake-shokunin 2026-10-21 13:08:15 -0300)`.
- Full citing line 60 (verbatim, complete):
  > "- Round-26 source recheck (2026-10-21, append-only; original lines unchanged). Rows S009 and S010 were re-fetched by one public GET each (`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`) and judged HOLD at their anchors against the retained bytes; receipts `.ufo/waves/round-26/rechecks/S0NN.json`, statement-level reviews `.ufo/waves/round-26/w1/Pair*.md`. Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten. Pointers labelled `at base cb807bc` stay base-scoped (QUALITY.md round-21 coordinate rule), so current-tree line movement is not a stale claim. Counting command: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`."
- Exact located support for the S008 fragment (≤25 words): **"S008 via `manifest-retry.json`"** — the only S008-bearing span in the file.
- File identity: sha256 `fa71ecd60370f81ec9d5ec596cc04483221392b9901068b4e92cef881a801d95`, byte-identical in the working tree, at `be375d9`, at `83528f7`, and at `.ufo/waves/round-27/frozen/corpus/knowledge/ghp-etag-anatomy.md` (frozen `expected.json` pins the same digest).
- Pair is one of the frozen 16 baseline-unadjudicated pairs: `c1-before.json` `missing[]` contains `{"row":"S008","file":"corpus/knowledge/ghp-etag-anatomy.md"}`; my run of `count_c1.py --revision be375d9` reproduces `citingPairs 57, decided 41, missing 16` with that pair listed.

## What the S008 fragment asserts, and its scope test

The grammatical subject of the sentence is "Rows S009 and S010"; S008 sits inside the provenance parenthetical naming where S008's r26 bytes live. The fragment's only assertion: S008's r26 retrieval is recorded in `manifest-retry.json` rather than `manifest.json`.

Evidence that this is true, all read from git blobs at `be375d9`:

1. `.ufo/waves/round-26/fetched/manifest-retry.json` (tracked) holds exactly one entry: `"row": "S008"`, `"attempt": 2`, `"status": 200`, `"fetchedAt": "2026-10-21T15:11:01.972009+00:00"`, `"bytes": 512359`, `"sha256": "93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084"`, `"file": "S008-1-retry.raw.gz"`, reason `"first attempt TimeoutError at 60s; single retry with 240s timeout"`.
2. `manifest.json` holds exactly one S008 entry, index 1, `"status": null`, `"error": "TimeoutError: The read operation timed out"`, 0 bytes, empty-content sha `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. So the successful S008 bytes really do live in the retry manifest.
3. I re-hashed both retained payloads from the revision blobs: `S008-1-retry.raw.gz` → 512,359 bytes, sha256 `93281a63…6084` (equals the manifest); `S008-1.raw.gz` → 0 bytes, sha256 `e3b0c442…b855`. Both match their recorded digests.
4. The r26 receipt `.ufo/waves/round-26/rechecks/S008.json` is `"verdict": "HOLD"`, `"fetchIndex": 1`, and its quote is present in the retained view `fetched/text/S008-1.txt` at the revision (checked: True). Its raw anchor lines are exact on the retry blob: 8587 `Default is @option{--no-anchored} for exclusion members`, 8588, 8602–8604 (the quoted wildcard-slash item), 8618 `Exclusion … --wildcards --no-anchored --wildcards-match-slash`.
5. "one public GET each" holds for the rows the clause quantifies over: `manifest.json` has exactly one entry each for S009 and S010, both `"status": 200`; their receipts `rechecks/S009.json` and `rechecks/S010.json` are both `HOLD`. S008's two attempts are exactly what the parenthetical distinguishes.
6. No false attribution: `corpus/SOURCES.md:16` (S008, GNU tar) has `opened 2026-10-19`, `recheck 365d`, used-by `corpus/knowledge/ghp-served-set.md` **only**. This entry's header (line 1) lists only `S009, S010`; `rechecks/S008.json` is not a source of any claim here. The r26 registry agrees: `.ufo/waves/round-26/statements.json` has pairs `S009/ghp-etag-anatomy.md` and `S010/ghp-etag-anatomy.md` and **no** S008 pair for this file.
7. Historical dates are preserved, not rewritten: line 2 keeps `verified-at: 2026-10-19`; line 60 itself says older dates "remain the historical record of the earlier reading". The only S008 date in play (2026-10-21 fetch) matches the manifest `fetchedAt` and the r26 receipt. This file contains no `1.35` occurrence, so the r20 label withdrawal (`corpus/lessons/round-20.md:309-311`, `.ufo/round-20/resume/sources-gate.md:140-143`) does not reach it.

## Stale premise vs source-date vs irrelevant retry boilerplate

- **Not a stale premise.** Nothing in this file depends on S008 content, so no S008 byte change could falsify line 60.
- **Not a source-date issue.** No S008 open/recheck date is restated here; the clause's date is the r26 round date and it is internally consistent with the artifacts.
- **It is irrelevant retry boilerplate.** The fragment `S008 via `manifest-retry.json`` is a shared r26 template appearing verbatim at `corpus/knowledge/crawl-scope-per-host.md:57`, `ghp-custom-domain.md:62`, `ghp-etag-anatomy.md:60`, `ghp-served-set.md:83`, `static-canonical-preflight.md:184`. The r26 falsify wave already ruled on the identical wording: `.ufo/waves/round-26/w2/Rejection07S013.md:70` — "It is true of the round but irrelevant to this entry. This is a provenance-precision nit, not staleness."
- **Reader ambiguity is a tradeoff, not a defect.** A hasty reader could take S008 for one of this entry's sources. That is a readability asymmetry only — `ghp-served-set.md:95` carries an explicit "name the round's retry, not a source of this entry" disclaimer and this file does not. A STALE verdict requires a wrong/unsupported attribution at the sentence's own scope; that is not met, so no `[r27-recheck S008 STALE]` marker is warranted and none should be appended.

## Ledger-mechanics finding the integrator must act on (not covered by the critic report)

`count_c1.py` validates a `kind:"source"` row by looking the row up in **this wave's** `.ufo/waves/round-27/fetched/manifest.json`. That manifest currently contains rows **S001–S006 only** (S008 absent — verified). Therefore a `kind:"source"` record for S008 would take the `StopIteration` branch → `errors.append('source_missing')` → the row lands in `findings[]` and the C1 count exits 1, no matter how good the quote is. **This pair must be recorded with `kind:"artifact"`**, `evidence` = a path tracked at the measured revision, `contains` = a byte-exact substring of that blob.

I verified the proposed record against the count_c1 artifact branch on the `be375d9` blobs: evidence `.ufo/waves/round-26/fetched/manifest-retry.json` is tracked (blob present, 902 bytes) and the substring `"file": "S008-1-retry.raw.gz"` occurs verbatim exactly once. Alternatives that also occur verbatim: `"row": "S008"`, `"attempt": 2`, `"reason": "first attempt TimeoutError at 60s; single retry with 240s timeout"`.

## Suggested C1 ledger record (r27 `pairs.json` → `pairs[]`)

```json
{"row":"S008","file":"corpus/knowledge/ghp-etag-anatomy.md","kind":"artifact","verdict":"HOLD","evidence":".ufo/waves/round-26/fetched/manifest-retry.json","contains":"\"file\": \"S008-1-retry.raw.gz\"","reason":"Only S008 token is r26 EOF provenance boilerplate at line 60 ('S008 via `manifest-retry.json`'); it locates S008's r26 retry (attempt 2, status 200, 512359 bytes, sha256 93281a63...6084 after the 60s TimeoutError recorded in manifest.json) and attributes no claim of this entry to S008 (SOURCES S008 usedBy = corpus/knowledge/ghp-served-set.md only). True at its own stated scope; carried r26 retrieval fact, not an r27 fresh source observation."}
```

Field-by-field check against the frozen contract's ledger spec: `row`/`file`/`kind`/`verdict`/`reason` present; artifact kind supplies `evidence` (repo path) + `contains` (substring) as required; HOLD needs no `[r27-recheck S008 STALE]` marker, and the marker is absent from the citing file at the measured revision (correct for HOLD).

## Correction wording

- **Required: none.** HOLD ⇒ no STALE marker, no appended correction. Appending `[r27-recheck S008 STALE]` would mislabel the pair and is explicitly not warranted here.
- **Optional, append-only, L1 discretion** (precision only, mirrors `ghp-served-set.md:95`; original line 60 and the 2026-10-19/2026-10-21 dates untouched):
  > `- Round-27 precision note (append-only; not a STALE correction): the words "S008 via manifest-retry.json" in the round-26 recheck paragraph name that round's single retried fetch (S008 attempt 2); S008 (GNU tar) is not a source of this entry, whose sources remain S009 and S010. HOLD (w1/Pair13A.md).`

## Denominator

No new citing pair was discovered in this file. Its citing set is exactly {S008, S009, S010}; S009 and S010 for this file are already carried from r26 `statements.json`, and S008 for this file is already in the frozen 16. C1 denominator stays 57 for this file; the wave denominator grows only via the predeclared monotone `discovered-pairs.json` (which already holds one entry, S013/ghp-served-set.md).

## Residual risk and verification gaps

1. **Judgment call is interpretive.** Whether a provenance parenthetical counts as "attribution" is the only soft point. I resolved it at the clause's own stated scope; r26's falsify wave reached the same reading on the identical wording. If L1 rules the other way, the marker is `[r27-recheck S008 STALE]` and the appended correction above becomes mandatory, not optional.
2. **No r27 fresh S008 fetch exists**, and none is needed: r27 `fetched/manifest.json` covers S001–S006 only. The HOLD rests on committed r26 artifacts whose hashes I re-derived at the measured revision, not on any r27 observation. Do not relabel it as an r27 fresh source observation.
3. **Adjacent debt, out of my pair's scope:** `ghp-served-set.md:83` puts S008 inside the quantified subject list ("Rows S001, S002, S004, S006 and S008 were re-fetched by one public GET each") while S008 in fact needed two attempts — a precision gap in that file's wording, on the already r26-decided pair (S008, ghp-served-set.md). I flag it for L1; I do not adjudicate it.
4. **Adjacent debt:** `.ufo/waves/round-26/rechecks/S008.json` `anchorObserved` still contains the clause "all inside the cited 8478-8617 range" while raw 8618–8619 lie outside it. r26 recorded the correction in `.ufo/waves/round-26/receipt-locator-errata.json` (S008 entry) with "receipts stay as committed". It does not propagate to this file, which states no S008 anchor range, so it does not bear on this verdict.
5. **Adjacent observation on the S009/S010 pairs of this same file (not my pair):** line 60 says rows S009 and S010 were "judged HOLD at their anchors against the retained bytes", while lines 62 and 64 append two `[r26-recheck S010 STALE]` statement-level corrections to this entry (the §8.8.1 paraphrase). Those are statement-level findings inside the entry, not anchor failures, and the row-level receipts are HOLD — so line 60 remains true at its own scope. Noted for the parent; not judged here.
6. **Historical metadata preserved.** No 2026-10-19 date was rewritten to 2026-10-21, and no r26 date was rewritten to today.

## Tooling

None installed, upgraded or removed; no pacman transaction (host-wide pacman pause respected). Python 3 standard library only, all in-memory over `git show` blobs (`gzip`, `hashlib`, `json`, `re`); plus `git ls-tree`, `git blame`, `git show`, `grep`. No network GET. No writes outside this report; no /tmp or /dev/shm use. No build, lint, test or formatter run mid-flight.

Report: .ufo/waves/round-27/w1/Pair13A.md
