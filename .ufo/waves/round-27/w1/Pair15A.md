# Pair15A — (S022, corpus/knowledge/static-canonical-preflight.md) adjudication, round 27 C1

Scope: one C1 citing pair. Read-only seat: no ledger, source, SOURCES, manifest or index edits were made.
Measured revision used for every blob read: `be375d90afc6fc7aca369ab3cf5247bf460aeed2` (declarations landed), tree `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`.
No network action, no fetch, no build/test/lint/selftest run (mid-flight prohibition); no r24 work read or retried.

## 1. Where the citation is (exact located support)

The pair exists **only** through a range in the entry's metadata prefix. There is no literal `S022` anywhere in the file.

- `corpus/knowledge/static-canonical-preflight.md:2` (full citing line, verbatim):

  > `verified-at: 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029), documentation opened this round; local behavior has separate committed round22 receipts, not live website verification`

- The range `S020-S027` at line 2 is the only citing form that reaches S022. Independent read-only scan of every `corpus/knowledge` blob at `be375d9` (same regexes as `.ufo/waves/round-27/count_c1.py`: `LITERAL \bS(\d{3,})\b`, `RANGE \bS(\d{3,})\s*(?:[-–—]|\.\.|to|through)\s*S(\d{3,})\b`) yields exactly one S022 pair: `corpus/knowledge/static-canonical-preflight.md`. The file's other ranges are `S028-S029` (line 2) and `S001–S006` (line 54, en dash; no S022). **No new citing pair is discovered; the denominator (57) does not grow.**
- Coordinate sanity: the r26 block's line references are *current* coordinates, not pre-prefix ones (`corpus/QUALITY.md:69-73` round-21 rule requires +4 for pre-round-21 literal pointers). Check: the `[r26-recheck S021 STALE]` block names "Line 25", and current line 25 is `Cross-domain canonical is likewise not intrinsically invalid.` — consistent, so line 2 is unambiguously the S022 citing line.
- Corpus index cross-check: `corpus/SOURCES.md:30` S022 `usedBy` = `corpus/lessons/round-22.md` only — the knowledge entry is **not** listed there (see note N1).

## 2. Claim decomposition at the citing line's own scope

The citation asserts two things about S022, and nothing else: (a) S022's documentation was opened on **2026-10-20** ("this round" = round 22, the authoring round of this entry); (b) the consulted documentation set spans rows S020–S027. It asserts **no** substantive claim about S022's content: the entry's body never cites S022, and `source:` (line 1) enumerates only S020, S021, S026, S027, S028, S029.

## 3. Evidence for each sub-claim

(a) opened 2026-10-20, round-22 provenance:
- `corpus/SOURCES.md:30`: `| S022 | Google Search Central: Fix canonicalization issues — https://developers.google.com/search/docs/crawling-indexing/canonicalization-troubleshooting | docs | A | Declared canonical versus Google-selected canonical | Opening paragraph, updated 2026-08-21; opened 2026-10-20 | Google may choose a different canonical even when the publisher explicitly designates one | mined | 2026-10-20 | 90d | corpus/lessons/round-22.md |`
  Located substring (anchor + opened date, the citing line's scope): `Opening paragraph, updated 2026-08-21; opened 2026-10-20`
- `corpus/SOURCES.md:69` round-22 search log: "Searched the fixed eight official sources listed in S020–S027 on 2026-10-20: RFC Editor, Google Search Central, WHATWG HTML and Python docs. Identified 8, screened 8, included 8, excluded 0" — S022 was among the eight opened on 2026-10-20, i.e. the range's date bracket is exactly the round-22 consultation set.

(b) content unchanged at the anchor (freshness of the cited row):
- Retained r26 fetch, `.ufo/waves/round-26/fetched/manifest.json` (row S022, index 1): `fetchedAt 2026-10-21T15:10:44.344595+00:00`, `status 200`, `bytes 178056`, `sha256 4d42dd82db74b81329deaa0e46fc4bfdf08548894d1e437a1a2634009b173e47`, `last-modified: Fri, 21 Aug 2026 11:28:27 GMT`, `file S022-1.raw.gz`.
- Receipt `.ufo/waves/round-26/rechecks/S022.json`: `"verdict": "HOLD"`, quote (17 words, verbatim, present in the retained text at `.ufo/waves/round-26/fetched/text/S022-1.txt`): `Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons`; `anchorObserved` "Main-content opening paragraph under H1 \"Fix canonicalization issues\" … footer \"Last updated 2026-08-21 UTC\"" — footer string present in the retained text; matches the SOURCES anchor "updated 2026-08-21".
- Statement-level review `.ufo/waves/round-26/w1/RowS022.md` caveat 4: the row's usedBy lesson quote `corpus/lessons/round-22.md:45` still matches the re-fetched bytes word-for-word (verified here: line 45 carries that exact quote).
- Cadence: SOURCES cadence `90d`, opened 2026-10-20 → not due (≈2027-01-18); the 2026-10-21 r26 recheck is already fresher than the cadence.

## 4. Proposed judgment: **HOLD** (recommendation; parent judges)

HOLD at the citing line's stated scope. Reason: the only assertion the pair carries is S022's documentation-open date within the round-22 consultation bracket, and that assertion is fully supported by `corpus/SOURCES.md:30` (opened 2026-10-20) plus the round-22 search log (`corpus/SOURCES.md:69`, S020–S027 searched 2026-10-20, 8 included); the row's content at its anchor is unchanged in the freshest retained observation (r26 fetch 2026-10-21, sha256 `4d42dd82…b173e47`, HOLD receipt). No attribution is wrong or unsupported, so STALE does not apply; the assertion is decidable from committed bytes, so UNVERIFIABLE does not apply. Precedent: r26 judged the identical metadata range HOLD for S020 (`stale=0`, `.ufo/waves/round-26/statements.json`) and for S021 the only stale was a body claim, never the metadata.

Not-STALE rationale for the range over-sweep (see N1): `source:` line 1 is demonstrably not an exhaustive source list — S024 and S025 are body-cited (lines 101, 117, 144, 198-200) yet absent from it — so the line-2 range is a date bracket over the round-22 consulted set, not an exhaustive enumeration of the entry's sources.

Not-STALE rationale for the r26 omission (see N2): the omission is an incompleteness in a *different* line (184) that cites no S022 row; it cannot retroactively falsify line 2's date assertion, and the r26 paragraph itself states older `verified-at` dates "remain the historical record of the earlier reading; they are not rewritten".

## 5. Precision notes (non-STALE; no `[r27-recheck S022 STALE]` marker required)

- **N1 — range over-sweep.** `S020-S027` covers S022 and S023, which the entry never uses in the body and which line 1's `source:` list omits; SOURCES `usedBy` for S022 lists only `corpus/lessons/round-22.md`. Real but cosmetic; no statement is mis-attributed. Suggested optional note appended by the executor (wording in §6).
- **N2 — r26 provenance paragraph under-reports S022.** Line 184 lists re-fetched rows "S020, S021, S026, S027, S028, S029, S030, S031, S032, S033 and S034" and omits S022 — although `.ufo/waves/round-26/fetched/manifest.json` holds S022 index 1 (sha256 `4d42dd82…b173e47`) and `.ufo/waves/round-26/rechecks/S022.json` holds a HOLD receipt. The file already flags the identical omission for S024/S025 ("S024 and S025 were re-fetched this round (receipts HOLD) but were missing from the recheck paragraph's row list above"), so the file's own convention is to note it. S023 has the same omission. This is the actionable freshness gap for this pair.
- **N3 — irrelevant retry boilerplate excluded.** "S008 via `manifest-retry.json`" in line 184 concerns S008 only; it plays no part in the S022 scope test and was not used as support.
- **N4 — pointer/command pointers still resolve at the measured revision (existence only, not executed).** `scripts/canonical_audit.py` and `.ufo/waves/round-22/matrix.py` both exist in the tree at `be375d9` (git `cat-file -e` on both). The `recheck:` line (line 3) therefore names live paths.
- **N5 — historical dates preserved, not rewritten.** 2026-10-20 / 2026-08-21 / 2026-10-21 values above are reported as the corpus records them; no date was normalised.

## 6. Suggested C1 ledger record (`.ufo/waves/round-27/pairs.json`, `pairs` array)

`count_c1.py` source-kind rows require an entry in `.ufo/waves/round-27/fetched/manifest.json` for that row; S022 was **not** fetched in round 27 (`fetch_group.py` restricts to S001–S006), so a `kind:"source"` row would fail with `source_missing`. Use `kind:"artifact"`:

```json
{
  "row": "S022",
  "file": "corpus/knowledge/static-canonical-preflight.md",
  "kind": "artifact",
  "verdict": "HOLD",
  "reason": "Citing form is the metadata range S020-S027 at line 2 (no literal S022 in the file). At that line's own scope the pair asserts only S022's documentation-open date inside the round-22 consultation bracket. Supported: corpus/SOURCES.md row S022 (anchor 'Opening paragraph, updated 2026-08-21; opened 2026-10-20', mined 2026-10-20) and corpus/SOURCES.md round-22 log (fixed eight sources S020-S027 searched 2026-10-20, 8 identified/8 included). Content at the anchor unchanged in the freshest retained observation: r26 fetch 2026-10-21T15:10:44Z, HTTP 200, 178056 bytes, sha256 4d42dd82db74b81329deaa0e46fc4bfdf08548894d1e437a1a2634009b173e47, Last-Modified Fri, 21 Aug 2026 11:28:27 GMT, judged HOLD at .ufo/waves/round-26/rechecks/S022.json; usedBy quote corpus/lessons/round-22.md:45 matches the re-fetched bytes word-for-word. No body claim in this entry depends on S022, so no mis-attribution and no STALE; range over-sweep and r26 row-list omission are precision notes, not stale premises.",
  "evidence": "corpus/SOURCES.md",
  "contains": "Opening paragraph, updated 2026-08-21; opened 2026-10-20"
}
```

Alternative if L1 prefers the r26 receipt as the supporting artifact (verified substring present in the blob at `be375d9`):

```json
{
  "row": "S022",
  "file": "corpus/knowledge/static-canonical-preflight.md",
  "kind": "artifact",
  "verdict": "HOLD",
  "reason": "Same adjudication as the SOURCES.md variant; the retained r26 receipt is the observation of record for the row's anchor.",
  "evidence": ".ufo/waves/round-26/rechecks/S022.json",
  "contains": "Even if you explicitly designate a canonical page, Google might choose a different canonical for various reasons"
}
```

Optional (requires a round-27 fetch of S022 — an executor action, not this seat's): adding S022 to `fetch_group.py`'s row filter would permit a `kind:"source"` row with `fetchIndex` 1, `quote` (17 words, verbatim in the fetched text) and `anchor` "opening paragraph under H1 'Fix canonicalization issues'; footer 'Last updated 2026-08-21 UTC'". Not required for HOLD.

## 7. Suggested appended wording (executor/L1 action; NOT written by this seat)

No `[r27-recheck S022 STALE]` marker: the pair is HOLD. Optional append-only precision note, mirroring the file's existing convention for S024/S025:

```
- [r27-precision S022] The verified-at range at line 2 (S020-S027) is a date bracket over the
  round-22 consulted set, not an exhaustive source list: S022 is used in
  corpus/lessons/round-22.md, not in this entry. S022 was also re-fetched on 2026-10-21
  (.ufo/waves/round-26/fetched/manifest.json row S022 index 1, sha256 4d42dd82…b173e47) and judged
  HOLD at its anchor (.ufo/waves/round-26/rechecks/S022.json); the round-26 row list above omits it,
  as it also omitted S024 and S025. Historical dates are preserved and not rewritten.
```

## 8. Effect on the C1 count, uncertainties, residual risk

- If this HOLD is recorded: `citingPairs` stays 57, `decided` 41 → 42, `missing` 16 → 15 (the list in `.ufo/waves/round-27/c1-before.json` loses the `{row: S022, file: corpus/knowledge/static-canonical-preflight.md}` entry). No pair is added, removed or re-scoped; the denominator is unchanged.
- Uncertainties: (i) S022 was not re-fetched in round 27, so the freshness support for this pair is the 2026-10-21 r26 retained bytes rather than a round-27 observation — one day older than this round; (ii) I did not execute `count_c1.py`/`c2_count.py` or any selftest (mid-flight prohibition); the citing-set enumeration in §1 is an independent read-only blob scan using the frozen counter's own regexes; (iii) the "range is a date bracket, not an exhaustive source list" reading is an inference from `source:` omitting body-cited S024/S025 — it is labelled as such and is not needed for the HOLD, which rests on the date/anchor facts alone.
- Residual risk: N2 leaves the file's r26 provenance paragraph incomplete for S022 (and S023) until an executor appends the note; that gap is a completeness defect in a different line, not a false statement, so it cannot invert this HOLD.
- No tool install or update was performed this seat (no install needed); nothing was written outside this report. Scratch: `/fast/scratch/hyaku/kake-r27/Pair15A/` (empty; reads only).

Report: .ufo/waves/round-27/w1/Pair15A.md
