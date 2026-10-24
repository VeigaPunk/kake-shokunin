# Round 47 — lesson

## Mistakes

1. **class:** population unit misstated in filed counts (calibration) ·
   **evidence:** the round-46 report and LOG entry filed the adjudication
   ledger as "12 rows"; the ledger holds **20 data rows** (12 naming LOG.md +
   8 naming SCORECARD.md) — caught by the round-46 closure as routed defect
   R3 · **captured-by:** QUALITY "Population unit named" should have caught
   it (the count mixed two units, ledger-rows and per-file rows, under one
   number) · **fix:** every round-47 filed count names its unit and
   population split (the C1/C2 counters print `2/2 tools`, `4/4 defects`
   with per-item detail); the LOG and SCORECARD carry the append-only
   correction naming the 12+8 split; the fix is shown able to fail — both
   counters at base read not-met (the do-nothing control), and the c47
   receipts re-derive the units from committed bytes.
2. **class:** reason prose drifted from the citing line it adjudicates
   (freshness) · **evidence:** five ledger reason cells named
   ds4cc-marketplace where the citing lines name the charter repo's
   2026-09-28 push series (`b74190e`, `d69dd22`, `0c767c2`, `b9db4b1`), and
   `dc8e1adf` named `CriticC2Sufficiency` where the provenance is
   `CriticProbeLeniency` — classes stayed correct, so the gate could not see
   it (round-46 closure routed defect R4) · **captured-by:** none — the
   citation gate checks token resolution and class only · **fix:** the
   round-47 QUALITY criterion "Citation reason fidelity" + the append-only
   §Round-47 corrections block naming each old line; the fix is shown able
   to fail — the corrections name the exact citing lines, and a future
   closure can re-read citing line vs reason the same way.
3. **class:** verdict filed without a committed receipt (operability) ·
   **evidence:** the round-46 report filed "freshness-sweep --offline exit 0
   at verdict time" with no committed output (round-46 closure routed defect
   R6) · **captured-by:** QUALITY "Replayable claim" in spirit (exact argv +
   full verdict + exit), but nothing required the output file itself ·
   **fix:** withdraw the unreceipted r46 verdict-time claim append-only in
   LOG.md; retain `.ufo/waves/round-47/verification/offline-sweep-r47-rerun.txt`
   solely as a contemporaneous r47 rerun, explicitly not retroactive evidence.
   The "Verdicts carry committed receipts" criterion and counter prove a
   prose tally is not a receipt; C1's base measurement read 0/2 selftest
   receipts despite the tallies existing in LOG prose, while C2's base
   measurement read 4/4 routed defects outstanding.

## Gate

- **S136 — gitrevisions (git-scm.com/docs/gitrevisions):**
  opened 2026-10-24T06:31:20Z by the L1 with one public GET (HTTP 200,
  74,526 bytes, retained text sha256 `33a99ba2…2d2da8c` at
  `.ufo/waves/round-47/sources/S136.txt`, receipt
  `.ufo/waves/round-47/sources/receipts.log`). Located quote (18 words):
  "The full SHA-1 object name (40-byte hexadecimal string), or a leading
  substring that is unique within the repository." ADMITTED (mined, tier A):
  git's own documentation of its revision-token semantics; grounds
  `corpus/knowledge/commit-citation-hygiene.md` (resolution semantics) and
  the R4 corrections (repo-scoped resolution). Second quote verified present:
  "E.g. dae86e1950b1277e545cee180551750029cfe735 and dae86e both name the
  same commit object if there is no other object in your repository whose
  object name starts with dae86e."
- Re-opened this round (recheck only, no cell change): none.
- Rejections this round: none.
- Bounded source search: question was Git's documented abbreviation/resolution rule; direct official Git documentation URL, one GET. Identified 1, screened 1, included 1 (S136), excluded 0; stop because the vendor-primary paragraph directly answers the narrow question.
- Non-author spot-check: not run in this seat; the L2 wave is prepared but undispatched under the host mapping. S136's quote and admitted scope were author-checked only; there is no rejected source candidate to sample. Independent admit+reject spot-check remains owed to closure.


## Registry changes

- rows 135 → 136 (S136 added, mined, tier A). No status / recheck / used-by
  cell changed on any existing row. Census exit 0 at round start and end.
- Sourced claim: C2 (the routed-prose repair claim) rests on S136 opened this
  round — the knowledge entry its evidence lands
  (`corpus/knowledge/commit-citation-hygiene.md`) cites S136 for the
  resolution semantics the R4 corrections rely on.

## Wave note

Round shape per the host mapping: the L1 holds the canonical planner seat
(frozen-topology ruling) and prepares waves; the orchestrator dispatches.
`.ufo/waves/round-47/w47-spec.json` (v1, 32 seats) was validated under
policy v1 and committed as prepared-but-undispatched evidence, together with
its validator taskCall. The lane-scope build and repairs were executed by the
L1 as integration owner (round-46 lesson, mistake 2's fix).
