# Pair12A — S008 × corpus/knowledge/ghp-custom-domain.md (r27 C1 freshness)

- Seat: `KakeR27.Pair12A` (reviewer, leaf; no dispatch). Axis judged: **freshness**.
- Obligation source: `.ufo/waves/round-27/c1-before.json` → `missing[11]` = `{row: S008, file: corpus/knowledge/ghp-custom-domain.md}` (16 missing; 41/57 decided at base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`).
- Read-only seat: no corpus/ledger/source edit, no fetch, no build/test/lint. Python stdlib only, in-memory; no `/tmp`, no `/dev/shm` (nothing written outside this report).
- **Verdict: HOLD** (kind `artifact`). No appended correction wording is necessary.

## 1. Citing line, located exactly

`corpus/knowledge/ghp-custom-domain.md` has **62 lines** (EOF at 62); file sha256 `65dd561af5cc7b189ae97caf67a52aa85ff794dc11c164cf07d2e0f91a7b19b6`. The **only** S-id literal for S008 is line **62** (single line; no range expansion applies — the file contains no `SNNN-SNNN` / `SNNN to SNNN` form).

Exact substrings of line 62 (located, verbatim, ≤25 words each):

- `S008 via \`manifest-retry.json\`` — 4 words — line 62.
- `Rows S003, S005 and S007 were re-fetched by one public GET each` — 13 words — line 62.
- `judged HOLD at their anchors against the retained bytes` — 9 words — line 62.

Full citing line (751 chars) is the r26 EOF block under `## Round-26 source recheck`; it also carries the counting command `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`.

**Pair enumeration for this file (independent, read-only):** population = 32 rows from `.ufo/waves/round-26/population.json`; S-literals/ranges in this file yield exactly `S003, S005, S007, S008`. `S003/S005/S007` are already decided in r26 (`.ufo/waves/round-26/statements.json:27-28,54-55,73-74`); `S008` is the assigned new obligation. **No additional citing pair discovered in this file** (the `S0NN` placeholder is not an S+3-digits literal). Denominator unchanged by this seat.

## 2. What the S008 mention claims at its own stated scope

Line 62 attributes to S008 **only** r26 round fetch provenance: S008's r26 fetch record is in `manifest-retry.json` rather than `manifest.json`, because attempt 1 timed out. It is **not** a source-support citation of S008 for this entry:

- Entry header `source:` lists `S003, S005, S007` only (`corpus/knowledge/ghp-custom-domain.md:1`).
- `corpus/SOURCES.md:16` (S008 row) `used-by` cell = `corpus/knowledge/ghp-served-set.md` only; `opened` = `2026-10-19`, `status` = `mined`, `recheck` = `365d`.
- Grammatically, `one public GET each` is scoped to "Rows S003, S005 and S007"; S008 is introduced only inside the parenthetical as an aside about which manifest holds its record.

## 3. Evidence (repo path + exact contains substring)

| # | Evidence path (repo-relative) | Exact contains substring (verified present) |
|---|---|---|
| E1 | `.ufo/waves/round-26/fetched/manifest-retry.json` | `"row": "S008"` (occurs 1×) |
| E2 | same | `"file": "S008-1-retry.raw.gz"` (1×) |
| E3 | same | `first attempt TimeoutError at 60s; single retry with 240s timeout` (1×) |
| E4 | same | `"sha256": "93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084"` (1×) |
| E5 | `.ufo/waves/round-26/w2/Rejection07S013.md:70` | `It is true of the round but irrelevant to this entry. This is a provenance-precision nit, not staleness.` (20 words) |
| E6 | `.ufo/waves/round-26/w2/Correction3S010.md:47` | `S008 is not cited by this file, so this looks like boilerplate carried over from \`ghp-served-set.md\`.` (19 words) |
| E7 | `corpus/knowledge/ghp-served-set.md:95` (r26 note) | `name the round's retry, not a source of this entry` (10 words) |
| E8 | `.ufo/waves/round-26/w2/CensusRerun.md:185-186` | `consistent with the paragraph under the natural reading; no correction needed` (12 words) |

E5 full-line context (same file, line 70, preceding the quoted substring): `That same appended bullet includes "(S008 via \`manifest-retry.json\`)", but this entry cites only S011, S012 and S013.` and `The same wording appears in 5 knowledge files` — followed by the enumeration `crawl-scope-per-host, ghp-custom-domain, ghp-etag-anatomy, ghp-served-set, static-canonical-preflight`. So the r26 ruling names `ghp-custom-domain` explicitly.

E5/E6/E7 are the **r26 wave's own adjudication of this identical boilerplate** in the sibling entries (`crawl-scope-per-host.md:57`, `ghp-etag-anatomy.md:60`, `ghp-served-set.md:83`, `static-canonical-preflight.md:184` all carry the same sentence). E5 states the rule verbatim for the same phrase in the same template.

**Independent local check (read-only, recomputed here):** `gzip.decompress(.ufo/waves/round-26/fetched/S008-1-retry.raw.gz)` → sha256 `93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084`, length **512,359 bytes** — matches E4 and `.ufo/waves/round-26/rechecks/S008.json` (`verdict: HOLD`, `fetchIndex: 1`).

**Counter-record for the pointer's precision:** `.ufo/waves/round-26/fetched/manifest.json:173-185` holds S008 attempt 1 (`status: null`, `TimeoutError`, sha256 `e3b0c442…b855` = sha of empty, file `S008-1.raw.gz`, 20-byte gzip on disk). So "S008 via `manifest-retry.json`" is the accurate pointer to the *successful* fetch; the failed attempt remains recorded in `manifest.json` and is not what the citing line points at. No inconsistency.

## 4. Freshness discipline: stale premise vs. source-date vs. irrelevant retry boilerplate

- **Not a stale premise.** Every assertion line 62 makes about S008 is true of the r26 round and verifiable in the tree: S008's successful r26 fetch is recorded in `manifest-retry.json` (E1–E4), with the retry reason and digest matching the retained bytes (local recompute above).
- **Not a source-date staleness.** Historical dates are preserved, not restated as current: S008 `opened 2026-10-19` (`corpus/SOURCES.md:16`), r26 fetch `2026-10-21T15:11:01Z` (`manifest-retry.json` `fetchedAt`), and line 62 self-labels as a `2026-10-21, append-only` block whose "original lines unchanged". No live-domain re-claim is made for S008 in this entry.
- **It is retry boilerplate, and irrelevant to this entry — which is not staleness.** The r26 falsify wave already ruled on this exact phrase and this exact template: E5 ("a provenance-precision nit, not staleness"), E6 ("boilerplate carried over from `ghp-served-set.md`"), E7 (the words "name the round's retry, not a source of this entry"). The line 62 text here is byte-identical to the ruled sibling instances except for the row list (S003/S005/S007), so the same ruling applies to this pair.
- **Adjacent r26 erratum does not touch this pair.** `.ufo/waves/round-26/receipt-locator-errata.json` (S008 entry) corrects `rechecks/S008.json` `anchorObserved`: `'all inside the cited 8478-8617 range'` → `teaching lines 8587-8588 and 8602-8604 are inside 8478-8617; summary lines 8618-8619 lie just outside`. That correction concerns the S008 receipt's anchor prose; line 62 asserts no anchor range and no S008 verdict for this entry, so it changes nothing here. (S008's own row verdict stays `HOLD`, `correction: null`.)
- **No source-kind adjudication is available or needed.** `.ufo/waves/round-27/fetched/manifest.json` (r27 fetch group) covers **S001–S006 only** (`fetch_group.py`), so a `kind: "source"` ledger row for S008 would fail `count_c1.py`'s `source_missing` gate. The claim in question is provenance, not source content → `kind: "artifact"`.

## 5. Uncertainties / residual risk (recorded, not decided against the verdict)

1. **Mis-derivable reading.** A reader could stretch "one public GET each" to cover S008, which would be inaccurate (S008's URL was requested twice: 60 s timeout then one retry; r26 `corpus/lessons/round-26.md:25-26` and `LOG.md` were corrected for the same count elsewhere — `.ufo/waves/round-26/w2/LessonAudit.md:66-68`). The r26 census already recorded this reading hazard: E8 "no correction needed, but a reader could mis-derive request counts". Under the natural reading (S008 = parenthetical aside) this pair is unaffected; the phrase is scoped to the named rows. **Not counted as a defect of this pair.**
2. **Provenance of the retry script.** `.ufo/waves/round-26/contract-amendment.json` records `fetch_retry.py` as a committed post-hoc copy that "did not produce manifest-retry.json"; the committed `fetch_retry.py:5-8` says the same. The citing line points at the *manifest*, not at a producing script, so the claim is unaffected; but the reproducing script's provenance is not claimed and was not re-run here.
3. **No live re-verification.** S008's source bytes were not re-fetched in r27 and I did not fetch them (out of this seat's scope and the r27 fetch group's range). Freshness for the *source content* of S008 rests on r26's pinned-commit fetch and its receipt; this pair's verdict does not depend on it.
4. **Historical r24 work not touched.** No r24 file, assignment, probe or counter was read, retried, rephrased or rerouted for this judgment.

## 6. Suggested C1 ledger record (for L1 integration into `.ufo/waves/round-27/pairs.json`)

```json
{
  "row": "S008",
  "file": "corpus/knowledge/ghp-custom-domain.md",
  "kind": "artifact",
  "verdict": "HOLD",
  "reason": "Line 62 is the r26 append-only recheck block; its only S008 assertion is round fetch provenance ('S008 via `manifest-retry.json`'). The pointer resolves: .ufo/waves/round-26/fetched/manifest-retry.json holds the S008 attempt-2 record (status 200, fetchedAt 2026-10-21T15:11:01Z, sha256 93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084, file S008-1-retry.raw.gz), and the retained gzip recomputes to that digest and 512359 bytes locally. S008 is not a source of this entry (header cites S003/S005/S007; SOURCES.md:16 used-by = ghp-served-set.md only), so the phrase is round provenance, not an attribution; the r26 falsify wave ruled the same words in the same template 'true of the round but irrelevant to this entry ... not staleness' (w2/Rejection07S013.md:70). Historical dates (S008 opened 2026-10-19; r26 fetch 2026-10-21) are preserved, not restated as current.",
  "evidence": ".ufo/waves/round-26/fetched/manifest-retry.json",
  "contains": "\"row\": \"S008\""
}
```

Gate-facing checks against `count_c1.py`: `kind` = `artifact` ✔; `evidence` and `contains` present, and `contains` occurs exactly once in `evidence` ✔; `verdict` ∈ {HOLD, STALE, UNVERIFIABLE} ✔; `reason` non-empty ✔; `verdict != STALE` → no `[r27-recheck S008 STALE]` marker required in the citing file ✔; `not_cited` → the pair must exist in the enumerated set (it does: literal `S008` in `corpus/knowledge/ghp-custom-domain.md` at base `83528f7`) ✔.

## 7. Appended correction wording

**None necessary.** The contract requires an appended `[r27-recheck S0NN STALE]` correction only for STALE verdicts; this pair is HOLD at its own stated scope, and the historical metadata is accurate and append-only-safe. The r26 sibling note at `corpus/knowledge/ghp-served-set.md:95` is a *rationale* note, not a required correction.

Optional (L1 discretion only — **do not append unless provenance precision is wanted**; if appended it must be EOF/append-only, must not move any cited line, and must not be counted as a C1 correction):

> Rejection rationale note (r27 C1): the words "S008 via `manifest-retry.json`" in the round-26 recheck paragraph above name that round's retry record for S008, not a source of this entry; this entry's sources are S003, S005 and S007 (`corpus/SOURCES.md:16` lists S008 `used-by` as `corpus/knowledge/ghp-served-set.md`). The pointer is accurate: `.ufo/waves/round-26/fetched/manifest-retry.json` holds the S008 attempt-2 record.

## 8. Corroboration, cross-checks and one observation for L1

- **Line 62 provenance:** introduced by `e28312b14b076584fedd696fae2a684e460bd11e` ("round-26: re-verify 32 cited sources and append adjudicated corrections", 2026-10-21 13:08:15 -0300) — i.e. the r26 wave's own append, after the r26 fetch at 2026-10-21T15:11:01Z. Chronology is consistent (retry precedes the append).
- **Independent critic sibling** `KakeR27.Pair12B` (`.ufo/waves/round-27/w1/Pair12B.md`, read after my report was written) reached the same verdict independently — HOLD, `kind: artifact`, evidence `.ufo/waves/round-26/fetched/manifest-retry.json` — using the alternative `contains` substring `"file": "S008-1-retry.raw.gz"` (verified present exactly once by me as well). Either substring satisfies `count_c1.py`; L1 needs only one row per pair, so the two must be merged to a single record, not two.
- **Marker convention:** the contract reserves the appended `[r27-recheck S0NN STALE]` marker for STALE rows only. A `[r27-recheck S008 HOLD]` marker (as proposed in the sibling's optional wording) is not required by C1 and risks being read as a correction; if any note is appended, plain prose without a `[r27-recheck …]` tag is safer. Nothing needs appending for this pair.
- **Observation for L1 (outside my pair, reported not judged):** the frozen measurement instruments were modified in the working tree after the declarations commit `be375d90afc6fc7aca369ab3cf5247bf460aeed2` — `git status` shows `M .ufo/waves/round-27/count_c1.py` and `M .ufo/waves/round-27/c2_count.py` (uncommitted). The `count_c1.py` delta adds (a) a `--selftest` dispatch to `oracle_selftest.py` (file now present, 5324 bytes, 17:03) and (b) a baseline clause that unions the 16 `c1-before.json` obligations and the r26 decided pairs into the enumerated pair set, raising `citing obligation outside frozen population` otherwise. Both changes are obligation-monotone and leave the standard `--root/--revision` semantics for enumeration intact; my pair's obligation exists under either the frozen or the modified counter (the literal `S008` is present in the file). Disclosure is still warranted because the contract names `count_c1.py` as the independently written C1 measure frozen before adjudication.

## 9. Tools

No tools installed or upgraded (nothing needed; no pacman/uv/cargo/npm transaction performed, none pending the operator gate). Read-only tools used: repo file reads, grep, `git show`/`ls-tree` at the frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba` and declarations commit `be375d90afc6fc7aca369ab3cf5247bf460aeed2`, and Python stdlib (regex enumeration, gzip+sha256 recompute) in memory.

Report: `.ufo/waves/round-27/w1/Pair12A.md`
