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
   §Round-47 corrections block with the corrected phrase per row. The fix is
   shown able to fail: `python3 -B .ufo/waves/round-47/c47_r4_mutation_check.py
   --root . --revision 714e7074110469a9ed2a3594677197baa0890905` reports
   `R4_REASON_FIDELITY base=pass mutants=5/5_rejected PASS`, exit 0; receipt
   `.ufo/waves/round-47/verification/c2-r4-mutation.txt` sha256
   `1e7636ecb023b2d2fa61d5bb6904166ebe84337514beed175c8010675cd507c3`.
3. **class:** verdict filed without a committed receipt (operability) ·
   **evidence:** the round-46 report filed "freshness-sweep --offline exit 0
   at verdict time" with no committed output (round-46 closure routed defect
   R6) · **captured-by:** QUALITY "Replayable claim" in spirit (exact argv +
   full verdict + exit), but nothing required the output file itself ·
   **fix:** withdraw the unreceipted r46 verdict-time claim append-only in
   LOG.md; retain `.ufo/waves/round-47/verification/offline-sweep-r47-rerun.txt`
   (sha256 `b86bc45992aa4f93c2c6d55d972a7d1a84ac0ffb46bedb7a674afd4a9822a717`)
   solely as a contemporaneous r47 rerun, explicitly not retroactive evidence.
   The "Verdicts carry committed receipts" criterion and counter prove a
   prose tally is not a receipt; C1's base measurement read 0/2 selftest
   receipts despite the tallies existing in LOG prose, while C2's base
   measurement read 4/4 routed defects outstanding.

4. **class:** C2 counter misread the offline receipt's explicit exit label
   (operability) · **evidence:** first after run at build commit
   `846138c99043505592adc9a7cbffcc31e044cd35` left R6 false and
   `outstanding=1/4` in `verification/c2-after-846138c.json` (sha256
   `af6fcdbfd48927dab3662b420ef1dd2e967d1238d271c77e0b2553f693fb1674`),
   while the committed r47 rerun receipt ended `OFFLINE_EXIT=0` ·
   **captured-by:** none — the counter matched only the literal `exit=0`,
   not the receipt's actual explicit label · **fix:** accept either
   `exit=0` or `OFFLINE_EXIT=0` while still requiring the `--offline` argv
   and the non-retroactive r47 label. Shown able to fail: the same receipt is
   `C2_NOT_MET` under `846138c` and `C2_MET` under counter-fix commit
   `714e7074110469a9ed2a3594677197baa0890905`; after receipt
   `verification/c2-after-714e707.json` sha256
   `141ede64f4539481557c946dfc40fa5af574771b3a15a1cc58a0a2299d1b5dba`.

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

## Inherited R46 residual scope (advisory, not a closure verdict)

Re-opened the five orchestrator-owned reports under `.ufo/waves/round-46/residual/` after the parent steer. `CriticCitationOverreach.md` found false-green paths for dead full-40-hex tokens, capitalized `Base` context, and coarse `(token,file)` ledger suppression; `ReviewWitnessOracle.md` found the redirect fixtures mirror tool selftest data and W12 expects unsupported redirect status 200; `CriticMatrixBlindness.md` showed basename-matcher and doctored-index shortcuts can pass; `MutationSemanticsGap.md` found 3 decision-logic mutants survive both detectors; `ReviewReceiptIdentity.md` raised an alternate, stricter receipt-internal binding reading. These findings are advisory, not closure verdicts. R47 does not change the tools or fixtures and makes no semantic-completeness claim: C1 is registry/receipt delivery and C2 repairs the routed records. The eight residual reports are untracked orchestrator-owned files and were left untouched.

