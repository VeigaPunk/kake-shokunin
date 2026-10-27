# MutationC2Probe

## SETUP
- Target: the C2 `scripts/header_audit.py` expected semantics as frozen in
  `.ufo/waves/round-61/contract.md` §Claim C2 (manifest v1, six expectation
  classes, could-not-evaluate and exit rules), probed through the contract's
  18-case table H1–H18 **before** the L1 freeze.
- Harness (scratch-built, copied to `MutationC2Probe.files/`): one engine
  `audit.py` implements the expected semantics (default variant `ref`);
  `MUTANT=m01..m12` env-switch flips exactly one semantic point each —
  mutants therefore never touch the bytes (restoration trivial: file sha256
  `412f43a3…` unchanged between ref and mutant runs).
  `gen_fixtures.py` emits the 18 fixture shapes + 3 proposed additions;
  `run_matrix.py` runs every variant over every case and diffs
  (exit, findings) against the contract's expected column.
- Kill criterion: a mutant's (exit code, findings count) differs from the
  contract-expected verdict on that case.
- **Validation**: the reference variant reproduces all 18 contract-expected
  verdicts exactly — fixtures are faithful encodings of the table
  (`results.json`, `ref_mismatch: []`).
- Scope: R3/R4 are counter-level (real manifest, base-absence), not
  tool semantics — excluded. No lane files, no sibling seats touched.
- Deliberate fixture encodings: H1 uses canonical-cased header names (a
  case-sensitive-name lookup misses them); H9's two `Content-Type` fields
  differ in case (a case-sensitive count sees one each); H6 carries
  case+OWS, H17 carries OWS-only.
- Ambiguity surfaced: contract text says exit 2 "only when NO check is
  evaluable" yet H13 (single check, missing receipt) expects exit 1. The
  reference follows the table (H13→exit 1). Worth pinning before freeze
  (see ADDITIONS A4).

## MUTANTS:
| mutant | semantics flipped | killed by (frozen 18) |
|---|---|---|
| m01 | singleton fires at count ≥1 (off-by-one) | H1, H10 |
| m02 | header names matched case-sensitively | H1, H2, H3, H4, H5, H6, H8, H9, H10, H12, H16, H17 |
| m03 | OWS not trimmed before value compare | H6, H17 |
| m04 | `content_type_present` only when status == 200 (not full 2xx) | SURVIVES |
| m05 | `content_type_present` requires a valued field (value-based, not name-based) | SURVIVES |
| m06 | `nosniff` compared case-sensitively | H6 |
| m07 | any manifest fault → exit 2 immediately (not per-check cne) | H13 |
| m08 | `hsts_present` gate ignores the `https` flag | SURVIVES |
| m09 | `Set-Cookie` honored as an ordinary singleton | H10 |
| m10 | `field_name_syntax` check disabled | H12 |
| m11 | `could_not_evaluate` does not force exit 1 | H13 |
| m12 | singleton counted case-sensitively | H9 |

Kill matrix: 9/12 mutants killed by the frozen 18; every killing case's
mutant verdict differs from the contract-expected verdict in exit code
and/or finding count (`results.json`, `raw` map). Representative raw
verdicts (exit,findings): m02|H1 (1,3) vs expected (0,0); m12|H9 (0,0)
vs (1,1); m07|H13 exit 2 vs 1; m11|H13 (0,0) vs (1,0).

## SURVIVORS:
- **m04** — 2xx boundary narrowed to `status == 200`. No frozen case
  carries a non-200 2xx status: H1 is 200 (both behave), H11 is 404
  (both skip). Verdicts identical on all 18.
- **m05** — `content_type_present` judged on the field's *value*
  (non-empty required) instead of field-name presence. Every frozen case
  with a `Content-Type` field has a non-empty value; H2 (no field) fires
  under both. Identical on all 18.
- **m08** — `hsts_present` expectation checked without the `https: true`
  gate. Every frozen hsts-expecting check is https (H3, H4); no
  `https: false` + `hsts_present: true` case exists. Identical on all 18.

## ADDITIONS:
Verified: each addition below, run in the same harness, kills exactly the
named survivor and nothing else (ref reproduces the proposed verdict):
- **A1** — status `204` (or 201), no `Content-Type` field,
  `content_type_present: true` → expect 1 `content_type_present`.
  ref yields (1,1); m04 yields (0,0). Kills m04.
- **A2** — status 200 with `Content-Type:` present but an empty value,
  `content_type_present: true` → expect 0 (field present).
  ref yields (0,0); m05 yields (1,1). Kills m05.
- **A3** — `https: false` + `expect.hsts_present: true`, no STS field →
  expect 0. ref yields (0,0); m08 yields (1,1). Kills m08.
- **A4 (spec-pinning, recommended)** — a manifest with two checks, one
  evaluable-clean + one missing-receipt, plus an all-cne manifest, would
  pin the contract's "exit 2 only when NO check is evaluable"
  parenthetical against H13's explicit "exit 1" (single cne check).
  [INFERENCE]: the parenthetical and the table are in tension for a
  single-cne-check manifest; the freeze should pick one.

## EVIDENCE
- `MutationC2Probe.files/`: `audit.py` (engine + 12 env mutants,
  sha256 `412f43a3…e487d`), `gen_fixtures.py` (`f9796312…da`),
  `run_matrix.py` (`4c03e32f…e0`), `expected.json` (`c649d9e3…4e`),
  `results.json` (full 13×21 matrix), `fixtures/` (18 contract cases +
  A1–A3, tar sha256 `c8dd8fd5…e7`), `hashes.txt`.
- Reproduce: `MUTANT=<id> python3 -B audit.py fixtures/<case>/manifest.json`;
  `python3 run_matrix.py` regenerates the kill matrix.
- No tools installed or modified; no credentials/URLs beyond the fixture
  hostname `pub.test`; lane repo untouched (report + .files only).
- Scratch `/fast/scratch/hyaku/kake-r61/MutationC2Probe` removed after
  copy-out; restoration = identical audit.py bytes before/after each
  mutant run (env-switch only), verified by the recorded sha256.

VERDICT: 9/12 cheap semantic mutants killed by the frozen H1–H18 table; survivors m04/m05/m08 are each killed by one proposed addition (A1/A2/A3) and one spec ambiguity (exit-2 vs H13) is surfaced for pinning before freeze.
