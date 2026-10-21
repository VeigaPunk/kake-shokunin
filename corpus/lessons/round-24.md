# Lesson — round 24 (2026-10-21): re-arm restored-source pins and parse receipt fields

## Claims

- C1 freshness: reconcile the frozen 19-target paths population (3 drift, 12 newly cited/pinned mismatches, 4 recovered) with dated current observations and correction registers. Lowest-axis duty applies: the two owned axes tie at legacy 10; no scalar rating increase is asserted.
- C2 operability: harden the existing receipt-replay instrument against the frozen malformed-record population while preserving accepted controls. Structural validation does not authenticate the originating observation.

`contract.json` and `contract-amendment.json` under `.ufo/waves/round-24/` define the scope. The latter rejects the original suffix-edit plan before any corpus correction was applied: QUALITY's round-20 non-author ruling requires byte-identical original lines.

## Gate

### Admitted candidates

- Dated re-observations for all 19 targets, with exact commands, state and evidence; 15 targets draw on author-side seat observations, four on coordinator observations after provider deaths. Source restoration is observed, never performed by this lane.
- Hash-bound sidecar corrections plus EOF blocks: 30 citation corrections, preserving original bytes and coordinates; non-author files remain entirely unchanged. This is the preservation-safe replacement for the rejected suffix plan.
- A 130-case, digest-pinned C2 population: 110 reject cases and 20 acceptance controls derived from actual committed sandbox observations. The selection register records deduplication and exclusions before measurement. Original round-23 counters remain byte-intact.
- S032/S033/S034: primary scoped sources for timestamp grammar, media-type grammar, and JSON interoperability, applied to the maintained replay script and knowledge entry.

### Rejected candidates and boundaries

- Suffix-append proposals from the frozen build prompts: rejected by QUALITY.md's round-20 post-review ruling. Original report drafts remain historical; no such suffix is integrated.
- Five heading/id cases needing companion Markdown and one synthetic finalUrl case needing companion fetch/audit changes: rejected as single-file population representations, not refuted observations. Retain their reports as supplemental evidence.
- Uppercase digest acceptance: not part of malformed-record hardening; the historical runner compares the producer's exact lowercase digest. Do not silently broaden unspecified encoding policy.
- A blanket string-only contentType rule: rejected because the producer permits null for an omitted header. A 404/null acceptance control is preserved. Likewise, c1 observedAt's historical full-date format remains accepted; c2 fetchedAt requires a date-time.
- RFC source assertions of universal MUST-accept/reject behaviour are scoped to the lane's documented profile: date-only acceptance, UTC observation floor/commit ceiling, unique-member policy, runtime numeric limits and unsupported leap-second handling are local choices, not extra RFC mandates. RFC9110 permits empty parameter occurrences after a semicolon; those controls stay accepted.

### Sources opened this round

| Row | URL / access | Located quote (≤25 words) | Scope / evidence |
|---|---|---|---|
| S032 | https://www.rfc-editor.org/rfc/rfc3339.txt — 2026-10-21 | §5.6: `full-time = partial-time time-offset` | Offset required in date-time; source bytes SHA256 9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a; w1/SourceRFC3339.md |
| S033 | https://www.rfc-editor.org/rfc/rfc9110.txt — 2026-10-21 | §8.3.1: `media-type = type "/" subtype parameters` | HTTP media-type grammar; source bytes SHA256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a; w1/SourceRFC9110MediaType.md |
| S034 | https://www.rfc-editor.org/rfc/rfc8259.txt — 2026-10-21 | §4: “The names within an object SHOULD be unique.” | Duplicate rejection is explicit receipt policy, not an RFC MUST; source bytes SHA256 61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7; w1/SourceRFC8259Json.md |

Rows added: A3. No earlier status/recheck/used-by cell is changed. The Python datetime documentation was also opened (w1/SourcePythonDatetime.md); it supplies a counterexample to using fromisoformat alone, not a separate registry row or additional claim.

### Outside spot-check

Pending the separate non-author closure. Every dispatched seat remains author-side; none grants promotion or outside discernment. Round-23's closure (fleet MANIFEST rounds[394]) is the motivating outside review, not an admission of this round.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix / fail-capable witness |
|---|---|---|---|
| survivor | round-23 closure lexical observedAt and untyped contentType defects; w1/ReviewQualityCriteria.md | none: prior malformed-neighbour criterion was scoped to URL branches | Parse fields and types; same frozen matrix at before revision accepts/crashes on 49 expected rejects; maintain accepted controls |
| stale-premise | paths-before.json: four recovered pinned misses after ds4cc checkout reappeared | standing setDelta.recovered reports it, but recovery is intentionally informational | Remove recovered tokens from pathsMissSet only after dated observations, so disappearance is armed again; before/after C1 counter and recovered selftest control |
| reference-drift | original round-24 suffix plan versus QUALITY.md:31-39 | existing round-20 non-author ruling, caught by L1 before integration | Reject suffix proposals; original line hash must match and the correction note must exist in a separate EOF block; c1_selftest.py exercises binding/block failures |
| survivor | w1/ScoutMistakeSweep.md: delayed pipe receives 65536 of 70840 JSON bytes | none | Let stdout drain via process.exitCode instead of process.exit; the retained delayed-reader probe is red-before; wave-2 attacks the corrected path |
| provider | w1-deaths.json / host terminal notices | no replacement rule | Dead seats remain dead and uncredited; coordinator executes residual work, not replacement dispatch |

## Measurement

Frozen artifact revision: `ab85dbdba4499f35f7dab9c9635b9b605679dbe5`; source corpus and historical replay runners unchanged there.

- `python3 -B .ufo/waves/round-24/measure_c1.py --root . --revision ab85dbdba4499f35f7dab9c9635b9b605679dbe5 --json`: accepted 0/19, sweep exit1; command exit1, retained measure-c1-before.json.
- Same revision with measure_c2.py: correct 81/130 (reject61/110, accept20/20), exit1; retained measure-c2-before.json. Case population SHA256 16da1936f30e2e7bfa405d9b51dfc18ab686edbd9f1d36f65d76626b0cab7b8f.

After measurements are appended only after execution. Claims are not admitted by their declaration or by this baseline.

## Round-24 path reconciliation

The two immutable non-author cites are corrected here; their original files are not edited. Sidecar line hashes bind these notes to the earlier lines. Evidence: `.ufo/waves/round-24/c1-receipts/T03.json` and `T17.json`.

- 2026-10-21: ~/Projects/webzites/scripts/kimi-surface.mjs absent (test -e exit 1); exact removal time and cause unknown, earlier W7 attribution historical. Citation corpus/lessons/round-6-aggregator-audit.md:48 is a historical record, not an executable instruction.
- 2026-10-21: ~/Projects/ds4cc-marketplace/CNAME present (test -e exit 0; checkout 1fbdb8ed); prior local-state annotations at corpus/lessons/round-1-aggregator-audit.md:30 are historical. Deployment, chat binding and byte continuity with the historical checkout remain unverified.


### Source usage changes and independent C1 measurement

S032/S033/S034 used-by cells changed from `corpus/lessons/round-24.md` to `corpus/knowledge/static-canonical-preflight.md, corpus/lessons/round-24.md` when that knowledge section landed; status mined→mined and recheck365d→365d. The original31 rows remain unchanged.

C1-only landing `3d07733b482f88c42cb008397188237c80e42b67`: same C1 counting command accepted19/19, sweep exit0, command exit0 (`measure-c1-c1-only.json`). At that revision C2 still uses the historical readers and remains81/130, exit1 (`measure-c2-c1-only.json`). This is observed causal separation in the C1→C2 direction, not just two axis names.
