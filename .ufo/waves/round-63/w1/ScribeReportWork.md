# ScribeReportWork — round-63 report `## Work performed` draft

Seat: `ScribeReportWork` (scribe, leaf; no subagent dispatch). Item: draft the report's
Work-performed section — open by naming the two declared claims and their axes, then one bullet
per work item with an evidence pointer; facts from committed files only.

Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`; base `13d4519818db28cd0aa912e49020659140d7b9fa`,
measured commit `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`, lane `HEAD` at read time
`15eb965c1d0f23ce2a522c651e9306a0952da7d3`.

Advisory draft only. Nothing was written outside this report path; no commit, no counter run, no
receipt edited, no scratch directory created. No tool installed, no `pacman` invocation.

## Read-only provenance checks behind the draft

| # | Check | Command | Observed |
|---|---|---|---|
| 1 | Frozen C1 counter | `sha256sum .ufo/waves/round-63/c63_calibration.py` | `bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91` — contract's value |
| 2 | Frozen C2 counter | `sha256sum .ufo/waves/round-63/c63_quote_tool.py` | `9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e` — contract's value |
| 3 | Frozen ledger | `sha256sum .ufo/waves/round-63/quote-class/quote-classes.json` | `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d` — contract's value |
| 4 | Frozen tool | `sha256sum scripts/quote_class.py` | `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14` — post-freeze-note value |
| 5 | Admitted span class, self-re-derived | Python `count()` of the ledger quote against the two blobs | `in_text=1 in_raw=0` → `collapsed-only` |
| 6 | Live body identity | `sha256sum` both blobs; `cmp -s` | both `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`; `IDENTICAL`; 1,854,393 bytes |
| 7 | Append-only corpus edits | `git diff --numstat 13d45198..05b0d7f4 -- <file>` | `corpus/knowledge/response-header-expectations.md` `29 0`; `corpus/QUALITY.md` `4 0`; `corpus/SOURCES.md` no output (untouched) |
| 8 | Receipt commits | `git log --format='%h %s' -- .ufo/waves/round-63/controls/<f>.txt` | `base-c1`, `base-c2`, `control-marker-fixture`, `control-junk-fixture` → `6d8c52a6`; `after-c1`, `after-c2` → `7f77d12b` |
| 9 | Wave shape | `w1-spec.json` items / `w1-dispatch.json` `counts` | 64 items (scout 10, executor 15, scribe 8, reviewer 15, critic 6, mutation-tester 5, connector 2, sentinel 1, simplifier 1, revenger 1); `counts.spawn=64`; `policy.maxLanes=64` |
| 10 | S432 row invariance | `git show 05b0d7f4:corpus/SOURCES.md \| sed -n '178p'` | row present, `status` cell `mined`, `recheck` `2026-10-27`, `used-by` `corpus/knowledge/response-header-expectations.md` |

The committed counter receipts (`base-c1`, `base-c2`, `after-c1`, `after-c2`,
`control-marker-fixture`, `control-junk-fixture`) were read, not re-executed; their printed values
below are quoted from those committed files. Measurement values belong to the sibling
`ScribeReportMeasurements` section and are not restated here beyond their use as work evidence.

## Draft — `## Work performed`

```markdown
## Work performed

Two claims, frozen in `.ufo/waves/round-63/contract.md` against base
`13d4519818db28cd0aa912e49020659140d7b9fa` (round-62 tip, `contract.md:3`):

- **C1 — calibration (lowest owned axis, 2/10):** repair the round-62 falsified calibration
  counter family and resolve the round-61 S432 disagreement by admitting the Fetch §3.6
  field-purpose span as `collapsed-only` (`contract.md:8-47`).
- **C2 — operability (HOLD 10):** land the committed quote-class tool
  `scripts/quote_class.py` and count it (`contract.md:49-73`).

Work items, each with its evidence pointer:

- **Froze the contract before any after-state measurement.** Base revision, both predicates, all
  four artifact sha256s, the control list and the kill rules are committed in
  `.ufo/waves/round-63/contract.md:3,17,22-29,37-44,51,64-71` (commit `6d8c52a6`); the
  freeze-note/tool-binding amendment is `contract.md:57-63` (commit `05b0d7f4`).
- **Built the semantics-binding C1 counter.** `.ufo/waves/round-63/c63_calibration.py`
  (sha256 `bcd16f68…3fc91`) re-derives every `resolved` component from committed bytes fetched
  with `git show` at the measured revision — retained blobs and ledger at `:107-109`; the
  `[r63-correction]`-block requirement at `:121-124`; ledger sha256 comparison against the two
  blob digests at `:127-142`; inline class derivation at `:139-144`; `quote_correction` conjunction
  at `:145`; `criterion` at `:149-150`; `lesson_gate` at `:153-159`; `source_row` at `:162`;
  `resolved` at `:164`.
- **Kept C1 independent of C2.** The counter classifies the span with its own
  `classify()` (`c63_calibration.py:59-67`) and never invokes `scripts/quote_class.py`
  (contract `Separability`, `contract.md:75-83`); the only `quote_class` occurrences in the counter
  are its two comments (`c63_calibration.py:15,61`), not a call.
- **Committed the class ledger that resolves the disagreement.**
  `.ufo/waves/round-63/quote-class/quote-classes.json` (sha256 `5f48e26b…0c42d`) records id
  `S432`, `matchClass` `collapsed-only`, `textSha256` `8b90d096…2a69`, `rawSha256`
  `63b0a018…911b`, `locatedRawLines` `6150-6154` (`quote-classes.json:7-15`), with the extraction
  recipe named at `:4`.
- **Committed the flat-text rendering and its extractor.** `.ufo/waves/round-63/quote-class/S432.txt`
  (sha256 `8b90d096…2a69`, 290,480 bytes) produced by
  `.ufo/waves/round-63/quote-class/extract_text.py`; re-checked this seat: the ledger quote occurs
  once in the flat text and zero times in the retained HTML, which is exactly the `collapsed-only`
  class.
- **Re-opened the source live and retained the body.** One GET of
  https://fetch.spec.whatwg.org/ retained as `.ufo/waves/round-63/sources/S432.live.html`
  (sha256 `63b0a018…911b`, 1,854,393 bytes), byte-identical to the round-61 retained body
  (`cmp` returns identical); recorded in `corpus/lessons/round-63.md:53-59` and
  `corpus/knowledge/response-header-expectations.md:247-249`.
- **Appended the knowledge correction (append-only).** `corpus/knowledge/response-header-expectations.md:222-250`
  (`## Round-63 correction` at `:222`, `[r63-correction 2026-10-27]` at `:224`, the admitted span at
  `:230`, digests at `:234` (flat text), `:236` (retained HTML) and `:249` (live re-open)); `git diff --numstat 13d45198..05b0d7f4` = `29 0`, no base
  line changed or removed. The span grounds the entry's `xcto_nosniff_value` section as a
  field-purpose statement, with the earlier fragment and lead-in left historical (`:245-246`).
- **Appended the round-63 criterion (append-only).** `corpus/QUALITY.md:1414-1416`
  (`## Round-63 criteria` at `:1414`); diff `4 0` against base; the round-62 criteria block at
  `:1410` is preserved above it.
- **Landed the C2 tool with its four frozen selftest cases.** `scripts/quote_class.py`
  (sha256 `431e75e8…1f14`) — `classify()` at `:32-38` returning `raw-substring` /
  `collapsed-only` / `absent`, case ids `inline_raw_substring`, `markup_collapsed_only`,
  `absent_everywhere`, `s432_real` at `:40-73`; fixtures bound to the invoking cwd
  (`LANE_ROOT = Path.cwd()` at `:24`) in commit `05b0d7f4` (`scripts/quote_class.py` only).
- **Built the C2 counter with the frozen case-set check.** `.ufo/waves/round-63/c63_quote_tool.py`
  (sha256 `9fcbfad0…7f01e`); `FROZEN_CASE_IDS` at `:25-30`; selftest invoked from the lane root at
  `:65`; case-set and pass-count conjunction at `:80-85`; emitted line at `:86`.
- **Committed the red-before and adversarial controls before measurement.** `base-c1.txt`,
  `base-c2.txt`, `control-marker-fixture.txt` (old c62 `met=true` defect line at `:4`, repaired c63
  `met=false` at `:7`), `control-junk-fixture.txt` — all added in `6d8c52a6`, i.e. before the
  measured commit; the after receipts `after-c1.txt`, `after-c2.txt` were committed separately in
  `7f77d12b` ("green-after receipts at measured commit `05b0d7f4`"). The attacked defect itself is
  the round-62 falsifier `.ufo/waves/round-62/controls/counter-false-green-l1.txt:8`.
- **Recorded the lesson gate and its outside verdict.** `corpus/lessons/round-63.md:61-65` labels
  the round-61 non-author `Disagree` as the outside verdict (`:61-63`) and this round's admits as
  author-side self-assessment (`:64-65`); the gate itself is at `:24-51` (admit (a) `:32-39`,
  reject (b) `:40-42`, reject (c) `:43-48`, assimilation none `:49-51`).
- **Left the registry row untouched.** S432 stays `mined` with its existing scope;
  `git diff 13d45198..05b0d7f4 -- corpus/SOURCES.md` is empty and the row at `corpus/SOURCES.md:178`
  is byte-identical at base and at the measured commit (`status` `mined`, `recheck` `2026-10-27`,
  `used-by` `corpus/knowledge/response-header-expectations.md`).
- **Dispatched the wave as one 64-seat v2 build+attack wave.**
  `.ufo/waves/round-63/w1-spec.json` holds 64 items (scout 10, executor 15, scribe 8, reviewer 15,
  critic 6, mutation-tester 5, connector 2, sentinel 1, simplifier 1, revenger 1) and
  `.ufo/waves/round-63/w1-dispatch.json` records `counts.spawn=64`, `policy.maxLanes=64`
  (commit `15eb965c`, post-dating the measured commit — dispatch metadata, not a claim receipt).
```

## Facts this seat could not verify from committed files

- The counter outputs quoted in the receipts were not re-executed here (seat instruction: do not
  rerun work to decorate the report); their values are asserted only as committed receipt content.
- The scratch-fixture revisions named inside the two control receipts (`7833be88…` for the
  marker-only fixture, `7da479c2…` for the junk fixture) are ephemeral and cannot be re-derived
  from the fleet repo; only the receipts record them.
- `w1-spec.json`/`w1-dispatch.json` commit `15eb965c` is `HEAD` and post-dates measured commit
  `05b0d7f4`; the wave-shape bullet above is therefore explicitly labelled dispatch metadata.
