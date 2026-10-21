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

## Recovery closure — policy interruption, not falsification success

Replacement coordinator KakeR24R inherits the same claimed round24 attempt1.
The original coordinator's final model error at 2026-10-21T12:22:15.004Z was:
`Codex error event: This content was flagged for possible cybersecurity risk.`
Its code was `cyber_policy`. The recovery does not adopt the provider's
suggestion to rephrase or change an access tier. No refused probe is retried,
rephrased, rerouted or replaced; no host/provider configuration is changed.

The original implementation at `faace82dcf50e1c563d437f2caecb77a9a865880`
had already run both counters before that error: C1 accepted19/19, paths0;
C2 correct130/130 (reject110/110, accept20/20), both commands exit0.
Original stdout/stderr/argv remain in `measure-c1-after.json`,
`measure-c2-after.json` and `implementation-suite.json`. Recovery
`recovery/provenance-audit.json` audits those receipt digests, the three
committed revisions and identical counter bytes. It is documentary
verification, not a newly executed gate result.

The retained implementation suite also records replay controls17/17 and12/12,
replay selftest129, C1selftest53 assertions, matrix selftest7, sweep35,
canonical matrix32 and clean corpus-contract. These are inherited local
checks, not a completed independent falsify wave or outside admission.

### Corrected wave accounting

- Wave1:72 seats;55 completed reports;17 deaths (16 Haiku429,1 connector
  Antigravity429). No dead seat is credited for recovered candidate code.
- Wave2:64 spawned;0 completed report files. Terminal JSONL projections:
  62 `Request was aborted`,1 connector429,1 interrupted without a final
  result. The coordinator's policy error is separate from those seat errors.
- Two new recovery seats inspect documentation/evidence only, not the
  refused assignments. Round total138 seats. All are author-side.
- Evidence: `recovery/interruption-inventory.json`; original wave registries
  and specs are retained. Wave reservations released through the host helper.
  No source checkout, publishing/account surface or driver state is changed.

### Sources & frontier census

Original start output, command
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`:
`kake ok /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`;
exit0 (`census-before.txt`). Recovery end output for the identical argv:
`kake W04 S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes`
then `kake ok /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`;
exit0. Full tab-separated output and Git-derived before/after row histograms:
`recovery/source-census.json`. Rows31→34, A29→32, C2 unchanged;
mined27→30, queued2 and rejected2 unchanged. Old31 rows unchanged.
S032–S034 used-by evolution is recorded above; no prior row cell is changed.
The added source search-log note records the original build readings, not a
new independent source reopening.

### Additional mistake record

| Class | Evidence pointer | Captured-by | Fix / limit |
|---|---|---|---|
| provider | recovery/interruption-inventory.json: coordinator cyber_policy plus incomplete wave2 | explicit no-reroute/no-replacement user instruction | Preserve measurements and interruption evidence; stop refused work, withhold admission/progression, file the L0 Policy-stop disposition question. This is disposition, not a claimed code repair. |

The fleet-root `git status --porcelain` sweep on recovery showed only
tracked sibling/driver state changes and no untracked file; no owned misroot
copy was found or moved. No operator-* lesson exists in the lane at this
sweep; round23's outside ruling is MANIFEST rounds[394] (no standalone
round-23-verifier-spotcheck.md file exists here).

### Final author-side verdicts

C1 and C2 show bounded local measured improvements; full falsification and
independent no-harm/admission remain incomplete. Expansion unchanged (no new
uncovered knowledge entry/capability); quality improved locally on the
recorded repaired populations; discernment unchanged pending the outside
admit/reject spot-check. The earlier Gate “admitted candidates” heading is
local curation, never full-round admission. “Independent C1 measurement”
above means causal separation only. No SHONEN promotion or next round starts.

### Documentary-audit dispositions

- `recovery/docs-audit.md` confirms distinct units:19 path targets with101
  frozen original citation coordinates;30 sidecar corrections (4 absent,
  26 restored);130 malformed-matrix cases (110 rejects,20 accepts).
  The pristine17/17 and12/12 replay controls are separate denominators.
- **Retained conformance defect:** `implementation-suite.json` and
  `sweep-selftest.json` expose concrete temporary/home-resolved selftest
  paths, while their recorded argv omits the override-variable/isolation
  shape. This fails QUALITY's shape-only probe-environment criterion.
  Neither output is rewritten or represented as fully redacted/isolated
  evidence. It does not by itself falsify the reported test tally; the
  conformance defect and broader admission hold remain.
- Frozen contract `count` strings are shorthand, not exact argv.
  The measurement receipts carry `python3 -B ... --json` and the complete
  root/revision arguments; use those for reproduction. The frozen contract
  is not rewritten to hide this abbreviation.
- Timestamp clarification: the first displayed round-open paths run was
  11:33:15Z; `paths-before.json` was generated at11:35:35Z by a separate
  capture. Neither is a Git commit timestamp. After-measurement receipts
  have no `executedAt` member; the original coordinator's tool event spans
  12:18:27.711Z–12:19:08.152Z and contains both after-counter exits0,
  before the12:22:15.004Z policy error. The event projection is appended in
  `recovery/provenance-audit.json`, not inferred from the commit time.
- `recovery/evidence-audit.md` identifies one build-seat interpreter install:
  CPython3.10.22 and3.15.0 via `uv python install 3.10 3.15`, uv0.13.0,
  uv-managed channel, for pre-3.11/current-doc datetime comparisons
  (`w1/SourcePythonDatetime.md:72`). No package/system upgrade is reported;
  neither replacement coordinator nor documentary recovery seat installed
  a tool. The original build's interpreter installs remain disclosed.
