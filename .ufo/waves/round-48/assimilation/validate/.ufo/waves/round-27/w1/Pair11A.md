# Pair11A — S008 / corpus/knowledge/crawl-scope-per-host.md

Axes: **freshness** (assigned, judged here); operability (preserve the complete expanded citing-set
denominator; no gate/implementation judgment). Author-side evidence only — not canonical admission.

Measured revision for all observations: `be375d90afc6fc7aca369ab3cf5247bf460aeed2`
(round-27 declarations) on frozen base `83528f7c486fd1b9a85e6c0bb643b25fa4fb9fba`.

## Citing occurrence (exact)

Repo path: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/crawl-scope-per-host.md`
Line **57** (last line; section `## Round-26 source recheck`, added by round-26 commit
`e28312b14b076584fedd696fae2a684e460bd11e`). The token `S008` occurs **exactly once** in this file
(grep count at the measured revision = 1); it is not produced by any range expansion.

Full citing line (verbatim):

> - Round-26 source recheck (2026-10-21, append-only; original lines unchanged). Rows S011, S012 and S013 were re-fetched by one public GET each (`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`) and judged HOLD at their anchors against the retained bytes; receipts `.ufo/waves/round-26/rechecks/S0NN.json`, statement-level reviews `.ufo/waves/round-26/w1/Pair*.md`. Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten. Pointers labelled `at base cb807bc` stay base-scoped (QUALITY.md round-21 coordinate rule), so current-tree line movement is not a stale claim. Counting command: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`.

## Scope of the S008 token at its own scope

The token sits in a **parenthetical pointer**, not in a claim: it states where S008's round-26 fetch
record lives (`manifest-retry.json`), because the entry's own re-fetched rows S011–S013 are recorded
in `manifest.json`. **S008 supports no statement in this entry.** The entry's header
`source:` (line 1) is `S011, S012, S013 (corpus/SOURCES.md)`; every body claim (robots-root scope,
sitemap location, parent-directory scope) maps to those three rows, each already r26-adjudicated
HOLD (`.ufo/waves/round-26/rechecks/S011.json`, `S012.json`, `S013.json`, each `"verdict": "HOLD"`,
`"correction": null`).

Contrast that keeps this pair distinct from the substantive S008 use: `corpus/knowledge/ghp-served-set.md`
uses S008 as a real citation (line 34 claim, line 73 erratum) — that pair is r26-adjudicated
(`.ufo/waves/round-26/statements.json` → `{"row": "S008", "file": "corpus/knowledge/ghp-served-set.md", ...}`).

## Judgment: **HOLD** (artifact-scoped, provenance-only)

The citing pointer is factually correct and byte-checkable:

1. `.ufo/waves/round-26/fetched/manifest-retry.json` holds exactly one record, row `S008`,
   `"index": 1, "attempt": 2`, `"status": 200`, `"bytes": 512359`,
   `"sha256": "93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084"`,
   `"file": "S008-1-retry.raw.gz"`, `"fetchedAt": "2026-10-21T15:11:01.972009+00:00"`,
   `"reason": "first attempt TimeoutError at 60s; single retry with 240s timeout"`.
   **Contains substring used as evidence: `"file": "S008-1-retry.raw.gz",`**
2. `.ufo/waves/round-26/fetched/manifest.json` holds the failed **first** attempt for the same URL
   (`"status": null`, `"error": "TimeoutError: The read operation timed out"`, `"bytes": 0`,
   `"sha256": "e3b0c44…"`), which is precisely why S008 lives in the separate retry manifest.
   The pointer is therefore complete, not misleading.
3. Decompressed `.ufo/waves/round-26/fetched/S008-1-retry.raw.gz` → sha256
   `93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084`, identical to the manifest
   record and to the r26 receipt's stated digest; the text view
   `.ufo/waves/round-26/fetched/text/S008-1.txt` contains the r26 receipt quote verbatim
   ("When wildcards match slash (the default for exclusion members), a wildcard like @samp{*} …").
4. `.ufo/waves/round-26/rechecks/S008.json` → `"verdict": "HOLD"`, matching the citation's
   "judged HOLD" wording for the rechecked rows, and `.ufo/waves/round-26/w2/FalsifyS008.md`
   independently reproduced the same bytes and anchors ("AGREE with the row-level HOLD").
5. `corpus/QUALITY.md:231-233` (round-26 recheck adjudication): "A recheck covers every corpus
   statement that cites a rechecked row, not only files listed in `usedBy`" — so this pair must be
   adjudicated even though `corpus/SOURCES.md:16` records S008 `usedBy` as
   `corpus/knowledge/ghp-served-set.md` only.

## Stale premise vs source-date vs retry boilerplate (the required discrimination)

- **Stale premise: none found at the citing scope.** The manifest pointer is byte-accurate; S008's
  own row verdict is HOLD and survives the r26 falsify wave. The one open wording defect in the
  r26 S008 receipt — `.ufo/waves/round-26/receipt-locator-errata.json` entry `S008`: stale
  "'all inside the cited 8478-8617 range'" → corrected "teaching lines 8587-8588 and 8602-8604 are
  inside 8478-8617; summary lines 8618-8619 lie just outside" — concerns the *receipt's* locator
  phrasing, not the citing line in `crawl-scope-per-host.md`. It does not make this pair stale.
- **Source-date: not stale, do not rewrite.** `corpus/SOURCES.md:16` records S008 opened
  **2026-10-19**; the round-26 re-fetch is **2026-10-21**; the entry's own header keeps
  `verified-at: 2026-10-19`. Per QUALITY round-26, "A historical verified-at date … is not a stale
  claim; record it as a note." The 2-day gap is retained provenance, not an unsupported attribution.
- **Irrelevant retry boilerplate: present, true, and non-substantive.** The clause "S008 via
  `manifest-retry.json`" is boilerplate from the standardized r26 EOF template, repeated verbatim
  at `corpus/knowledge/ghp-custom-domain.md:62`, `corpus/knowledge/ghp-etag-anatomy.md:60`,
  `corpus/knowledge/static-canonical-preflight.md:184` and `corpus/knowledge/ghp-served-set.md:83`.
  Its factual content (which manifest holds S008's bytes) is correct and checkable; it attaches no
  source-support obligation to this entry's crawl-scope claims. It must stay in the denominator
  (contract C1 denominator explicitly INCLUDES "historical metadata/r26 EOF prose"), and it is
  adjudicated as a **provenance-only** HOLD, not as S008 support for the entry.

## Suggested C1 ledger record

```json
{
  "row": "S008",
  "file": "corpus/knowledge/crawl-scope-per-host.md",
  "kind": "artifact",
  "verdict": "HOLD",
  "reason": "Line 57 mentions S008 only inside the standard round-26 EOF parenthetical pointer 'S008 via manifest-retry.json'. manifest-retry.json holds S008's successful attempt-2 record (status 200, sha256 93281a63…, file S008-1-retry.raw.gz); manifest.json holds the failed attempt-1 TimeoutError, so the pointer is exact. S008 supports no statement in this entry (header source: S011,S012,S013; body claims map to those rows, r26 HOLD). No fresh r27 opening of S008 is claimed; r26 retained bytes are the authority.",
  "evidence": ".ufo/waves/round-26/fetched/manifest-retry.json",
  "contains": "\"file\": \"S008-1-retry.raw.gz\","
}
```

Why `kind: artifact` and not `source`: `.ufo/waves/round-27/fetched/manifest.json` currently contains
S001–S006 only and no r27 S008 fetch seat was assigned; a `source` row would require inventing an
r27 fresh observation, which the contract forbids ("r26 … not retroactively relabelled r27 fresh
source observations"). If L1 later opens S008 in r27, a `source` variant is admissible with
`fetchIndex`, the ≤25-word quote "When wildcards match slash (the default for exclusion members)" and
anchor "Controlling Pattern-Matching, 8602-8604" — but that would be a *new* observation, not this
pair's basis.

## Appended correction wording

**None required.** The verdict is HOLD, so `count_c1.py`'s STALE-only rule (no `[r27-recheck S008 STALE]`
marker) does not apply and no citing-file edit is needed. Optional, L1-owned, **not recommended**:
an EOF provenance note to remove the reader's possible misreading of the parenthetical, e.g.

> - r27 note: the S008 mention above records only the round-26 retry manifest location for that
>   row; S008 supports no statement in this entry (`usedBy` remains
>   `corpus/knowledge/ghp-served-set.md`).

Appending it would move EOF line numbers and require pointer accounting; the ledger record alone
carries the adjudication, so I recommend no corpus mutation for this pair.

## Denominator effect

No new citing pair discovered by this seat: this pair is already enumerated by the frozen count at the
measured revision (57 citing pairs, 41 decided, 16 missing, including
`(S008, corpus/knowledge/crawl-scope-per-host.md)`). S008 occurs in exactly five knowledge files at
that revision — `ghp-served-set.md` (6 tokens, r26-adjudicated) and one boilerplate token each in
`crawl-scope-per-host.md`, `ghp-custom-domain.md`, `ghp-etag-anatomy.md`,
`static-canonical-preflight.md` (all four already in the frozen missing-16). Monotone growth since
that snapshot: `.ufo/waves/round-27/discovered-pairs.json` adds one pair from another seat
(`S013` × `corpus/knowledge/ghp-served-set.md`, `w1/CritFailOpen.md`), taking the C1 obligation
count 57→58; my pair is unaffected and remains inside the frozen 57. Denominator never shrinks.

## Evidence hashes (SHA256 of observed bytes)

- `corpus/knowledge/crawl-scope-per-host.md`: `aea5d1579b1cec8ccefb30de600cce710f885bfddfd33c60a8809b7a609af691` (git blob `a05625c9dad9282a3905dad8b957342c0c4a5c2d`, clean working tree)
- `corpus/SOURCES.md`: `5001eadee20c65c5df364a88430b6b0e76a99940afc282d72fecdd6d7c6be62d`
- `.ufo/waves/round-26/fetched/manifest-retry.json`: `84e83fb0cf5bf431eb029a9ab8cab69b661054e6e992b862e87b514786a65d1b`
- `.ufo/waves/round-26/rechecks/S008.json`: `9e39e7da3099c442b4789919b1690339d74d776050ab5bd4536b242c22efe6ab`
- `.ufo/waves/round-26/fetched/text/S008-1.txt`: `5f12a7aa82fa1fbf51b03ca03708642739f3cd2955206a7fac634efed64ed1cb`
- `.ufo/waves/round-26/population.json`: `16330e1effd5ee52665f8f31738e9423c6ec387e5d4a1404c5bcc35f69d01b03` (S008 row: opened 2026-10-19, recheck 365d, usedBy `corpus/knowledge/ghp-served-set.md`)
- Retained S008 bytes (decompressed `S008-1-retry.raw.gz`): `93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084`

## Verification performed, uncertainties, gaps

- Executed the frozen, read-only measuring command
  `python3 -B .ufo/waves/round-27/count_c1.py --root . --revision be375d90…` to enumerate the
  denominator (git-show reads only; it writes nothing). No gate, selftest, build, test, formatter
  or smoke run was performed.
- Note for L1: the working tree's `count_c1.py` has since been amended (baseline-pair preservation
  from `c1-before.json`, `group_source_required` for `static-canonical-preflight.md` S001–S006, and a
  `--selftest` hook). Those changes do not touch this pair: the artifact/source record validity
  check is unchanged, S008 is inside the frozen 32-row population, and the grouped-source rule is
  scoped to a different file. My pair's obligation and record stand under the amended counter.
- No live network fetch was made for S008 this round. Byte identity was checked against the
  committed r26 retained bytes only, so this adjudication verifies the **historical provenance
  pointer** (what the citing line asserts), not that the GNU tar manual still says the same thing
  today. That re-opening, if wanted, is a separate r27 source seat.
- The `contains` substring is not globally row-unique across the corpus; row identity comes from
  `evidence` + `reason` (manifest-retry.json contains a single record, row S008).
- Not read: any sibling seat's A/B report for this pair; any r24 assignment, probe or counter
  (r24 work is not read, retried, rephrased or rerouted). No source, ledger, SOURCES, manifest,
  gate or Git mutation was performed; the only file written is this report.

Report: .ufo/waves/round-27/w1/Pair11A.md
