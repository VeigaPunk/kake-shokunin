# Round-24 documentary audit

## Axes checked

- Claim populations and denominator integrity.
- Timestamp and revision chronology.
- Preservation of earlier historical wording.
- S032–S034 used-by evolution and source census.
- Author-side evidence, interrupted seats, and non-author admission limits.

## Findings, by severity

### Medium — retained selftest receipts are not shape-only compliant

`corpus/QUALITY.md` §“Shape-only probe environment” requires variable names and isolation shape, symbolic placeholders in captured output, and rejects serializing assigned environment values or env-derived paths. In `.ufo/waves/round-24/implementation-suite.json` (sweep-selftest entry, `argv`/`stdout`) and the matching `sweep-selftest.json`, the recorded argv is only `node scripts/freshness-sweep.mjs --selftest`; it does not record `HOME`, `TMPDIR`, or `KAKE_SELFTEST_DIR` overrides. The captured stdout nevertheless contains concrete temporary-directory and home-resolved selftest paths. This is a documentary conformance defect in the retained evidence, not evidence that the test result itself is false.

Other wave-1 reports record explicit environment assignments for their own runs, but those are different scratch locations and do not establish the isolation values for the suite run. Do not rewrite the inherited receipts. For honest final bookkeeping, add an append-only disposition that identifies the retained selftest output as nonconforming to the shape-only criterion and avoids claiming that its environment was fully recorded or redacted.

### Low — frozen contract `count` fields are abbreviated relative to actual argv

`.ufo/waves/round-24/contract.json` gives C1/C2 count strings without `-B` and `--json`. The inherited before/after receipt argv records include both flags; the round-24 Scorecard/lesson measurement commands also include them. The outcome and denominators agree, and the exact receipts are retained, but the frozen contract strings should be labelled shorthand (or explicitly cross-referenced to receipt argv) rather than represented as the exact executed commands. Preserve the frozen contract; an append-only clarification is sufficient.

## Confirmed bookkeeping

### Denominators and results

- **C1** is 19 path targets, not 19 citations: 3 drift + 12 new-missing + 4 recovered = 19. The frozen target population separately preserves 101 original citation coordinates. The sidecar has 30 correction records (4 `absent`, 26 `restored`); these are a third, distinct unit. The before receipt is 0/19 with paths exit 1; the final receipt is 19/19 with paths exit 0. The miss-set change is 55→63, consistent with 12 observed misses added and 4 recovered tokens removed; the current pin contains 63 entries.
- **C2** is 130 frozen cases: 110 expected rejects and 20 acceptance controls. The recorded result is 81/130 (61/110 rejects, 20/20 accepts), exit 1, at `ab85dbd…`; it is 130/130 (110/110, 20/20), exit 0, at `faace82…`. The C1-only revision `3d07733…` measures C1 at 19/19 while C2 remains 81/130. The C2 population digest is the same across the measured revisions. The separate pristine replay controls (C1 17/17 and C2 12/12) and replay selftest tally are not part of the 130-case denominator.

### Revisions and clocks

The contract distinguishes base `f7de3ab…` from frozen measurement revision `ab85dbd…`; these are not interchangeable. The provenance audit records `ab85dbd…` at 2026-10-21 09:11:40/41 -03, C1-only `3d07733…` with committer time 09:16:07 -03, and implementation `faace82…` at 09:18:12 -03 (12:18:12Z). The recovery inventory records coordinator termination at 12:22:15.004Z. These commit and termination times are mutually consistent with the report’s chronology, but the measurement JSON records revision/argv/output, not an `executedAt` timestamp; the “ran before termination” statement is therefore carried from the coordinator’s record, not independently timestamped by those receipts. Do not present a Git commit time as a measurement time.

The contract records the round-open paths gate at 11:33:15Z; `paths-before.json` records `generatedAt` 11:35:35Z. **[INFERENCE]** These can coexist if the former is the invocation/round-open time and the latter is output generation, but the receipt does not encode that relationship. Keep them labelled separately. The T03/T17 observations are later dated receipts (11:50:05Z and 11:50:15Z). T03 preserves unknown removal time/cause and historical W7 attribution; T17 establishes current presence/value in the fresh clone only, not historical checkout continuity, deployment, or chat binding.

### Historical wording and source chronology

The inspected diff from the frozen artifact to `faace82…` adds, rather than deletes, lines in the round-24 lesson, QUALITY, SCORECARD, and LOG; current post-implementation recovery bookkeeping is likewise insertion-only. The pin JSON is intentionally different (30 additions/6 deletions), so this is not a claim that every corpus byte is unchanged. The two cited non-author lesson files (`round-1-aggregator-audit.md` and `round-6-aggregator-audit.md`) are unchanged in the inspected revision range. The T03/T17 corrections remain sidecar/EOF records and do not rewrite their original citation lines.

The registry chronology is consistent: at the C1-only revision, S032–S034 point to the round-24 lesson; at the final implementation revision, their `used-by` cells also name `corpus/knowledge/static-canonical-preflight.md`. Their status (`mined`) and recheck (`365d`) did not change. The census reports 31→34 rows, A29→32, C2 unchanged, `oldRowsChanged: []`, exit 0; its W04 duplicate-RFC9110-URL-across-scopes warning is retained. The current SOURCES search log adds the bounded round-24 question and explicitly says the policy-interrupted wave-2 source-reopening seats produced no completed reports. The existing replay capability’s maintenance pointer now names `scripts/receipt_replay.py`; SCORECARD still says first-working round 23 and claims no new capability.

### Admission limits

The current Scorecard, LOG, and lesson correctly withhold admission/progression: wave 1 has 55 reports from 72 seats (17 deaths); wave 2 has 0 completed reports from 64 seats (62 aborted, one connector quota error, one interruption without a final result). The two recovery seats are documentary audits, not replacement falsifiers; the record totals 138 author-side seats. The outside admit/reject spot-check remains pending, full-round no-harm is not established, no SHONEN promotion or new capability is claimed, and no next round or retry of the refused work is authorized.

## Residual risk and verification gaps

- The shape-only issue above should remain visible; inherited raw outputs were not modified.
- The C1/C2 after receipts lack wall-clock execution timestamps. Their revision binding, argv, output, and exit are present; independent non-author admission is not.
- No LSP device/server was exposed in this session, so no LSP status/reference/definition/diagnostics queries were available. Text search was used only to locate records, not as semantic proof.
- No tests, builds, linters, formatters, probes, or new measurements were run. This audit is documentary and does not independently verify the runtime implementation or remote push state.

## Bookkeeping correction summary

Keep the measured C1/C2 results and the current admission hold as recorded. Add an append-only shape-only conformance disposition for the retained selftest paths, label the frozen contract count strings as shorthand against exact receipt argv, and preserve the distinction between round-open and receipt-generation timestamps. No inherited artifact or historical citation was rewritten by this audit.