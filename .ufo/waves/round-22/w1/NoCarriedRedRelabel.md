# NoCarriedRedRelabel — critic report (C1, operability)

Seat: critic, wave 1, read-only. Scope: attack claim C1 ("Offline static
canonical publishing preflight") specifically on the carried-red axis: the
frozen 32-case count must not be obtained by relabeling a still-red condition
(policy violation, unmeasurable baseline, or inherited lane debt) as accepted,
clean, or resolved. Contract:
`.ufo/waves/round-22/contract.json`; base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.

## Carried red at base (observed this session)

| Surface | Observed | Source |
|---|---|---|
| `node scripts/freshness-sweep.mjs --section=paths` | exit 1, `VERDICT: DRIFT — §paths: 3 unannotated miss · 0 NOT in pins.pathsMissSet` | run 2026-10-20 at base |
| `node .ufo/waves/round-21/anchor-census.mjs` | exit 1, out-of-range diagnostics present | run 2026-10-20 at base |
| `scripts/canonical_audit.py` | absent at base | `test -f` |
| `.ufo/waves/round-22/measure.py` | absent at base | `test -f` |

The r21 non-author verifier (`corpus/lessons/round-21-verifier-spotcheck.md`)
routes both red surfaces as honest carried debt and explicitly credited the
lane for refusing to weaken the paths pin-set for green. `SCORECARD.md`
records saturation line 10/10 + stagnation window N=1; C1 is a capability
move, not a numeric move — any score-row change or "paths gate resolved"
wording inside round-22 evidence is a relabel.

## Falsifiable acceptance constraints for C1

1. **Baseline measured, not inferred.** `measure.py --root . --revision 7c61c8c…`
   must produce archived output reporting **0/32 with reason
   artifacts-absent** (validator+matrix files not in that tree). A baseline run
   that crashes, exits 64, or is simply not run leaves the before-number
   asserted, and the claim's "0 accepted" is then unverifiable, not measured.
2. **Per-case verdicts, not a scalar.** An "accepted case" must require BOTH
   the frozen expected exit AND the frozen expected finding id to match, and
   the report must publish all 32 (case, expected, observed) rows. A single
   32/32 scalar hides swapped or absent ids.
3. **Exit separation is the anti-relabel line.** Policy-violation negatives
   must exit 1, not 2 (`could-not-evaluate`). If an author fixture is malformed
   or unsupported and the validator exits 2, pinning `2` as that case's
   expectation relabels a policy red as an input error while still counting the
   case as accepted. Only `manifest_traversal`, `symlink_html`, `html_unsupported`
   class, and genuinely-bad-input cases may carry expected exit 2; every named
   policy negative (`duplicate_*`, `body_link`, `wrong_*`, `fragment_url`,
   `javascript_url`, `data_url`, `base_invalid`, decoys, `missing_*`,
   `href_*`, `invalid_url`) must be expected exit 1 with its contract finding
   id, and positives exit 0 with an empty findings array (there is no "clean"
   id in `findingIds`).
4. **Expectations frozen independent of the validator.** `cases.json` expected
   ids/exits must be written by the Matrix seat from the contract policy and
   committed *before or independent of* observing validator output; every
   expected id must be a member of the contract's ten `findingIds`. An
   expectation table tuned to whatever the validator emits is the
   red→green relabel in its purest form.
5. **Revision pin is a commit SHA, observed.** `--revision <master-tip>` must
   resolve to a full hash recorded in the measurement artifact, and the
   measured revision must equal the tree the report cites. A moving ref or a
   measurement taken on an uncommitted clone state is unreviewed-state-as-evidence.
6. **Carried debts stay red in round-22 text.** The paths gate (3 targets /
   missSet 55), anchor-census (not a gate; 78 baseline-inapplicable
   diagnostics), and reconstructed-Gate chronology must appear unchanged or
   explicitly carried. Any phrasing that folds them into the new capability's
   "clean" verdict is a carried-red relabel.
7. **Selftest does not substitute for the frozen matrix.** `--selftest` proves
   the binary runs; it is not the 32-case count. Do not let a 14/14-style
   selftest number stand in for matrix acceptance.

## Overclaim to reject

- "proves clean positive controls" — controls are demonstrated by author-side
  measurement, not proven; the r21 standard requires non-author re-measurement
  over committed blobs before admission. Reject any wording that promotes
  author output to proof or admission.
- Any claim that C1 changes freshness, clears citation/path debt, validates
  publishing readiness, or approximates Google canonical selection — all
  outside the frozen limits and already rejected in `corpus/lessons/round-22.md`
  §Gate; reject if it reappears in wave-2/integrator text.
- A 32/32 "accepted" count where expected ids were chosen after running the
  validator, where a scalar replaces per-case evidence, or where exit-2
  could-not-evaluate rows are counted as negative-case passes.

## Distinct wave-2 attack — the could-not-evaluate relabel

My siblings probe wrong ids and markup edge cases; this attack targets the
exit-map boundary, the cheapest way to launder a red into a green count:

1. Take the integrated tree. Pick a policy negative, e.g. `body_link` or
   `second_base_ignored`.
2. Mutate the fixture so it is *barely* malformed for the author's parser
   (e.g. drop the closing `</head>` so the head/body boundary the policy
   depends on becomes undecidable, or give `second_base_ignored` a base whose
   href is a scheme the URL resolver rejects).
3. The validator now exits 2 (`could-not-evaluate`) on a case the contract
   intends as a policy verdict (1 + `canonical_outside_head` /
   `base_url_invalid`-vs-clean).
4. If `cases.json` was pinned to observed output, the expectation silently
   becomes `2`, `measure.py` reports 32/32, and the frozen matrix now counts
   a parser-limitation red as accepted — a carried red relabeled green with a
   perfect count.

Detection required from the integrator: diff `cases.json` expected
exits/ids against the contract's exitMap and findingIds; any expected exit 2
on a policy-named case, or any expectation file whose git history shows it
was edited after validator output existed, fails constraint 3/4. Also require
the measure report to emit per-case `expected` vs `observed` — a mismatch
hidden behind an aggregate cannot be audited.

## Smallest safe correction

None of this requires redesign. Require, before L1 integrates:

- `cases.json` carrying, per case, `expectedExit` and `expectedFindings` drawn
  only from contract vocabulary, with exit-2 expectations restricted to the
  input/unsupported class;
- `measure.py` output including the resolved revision SHA and a 32-row
  expected/observed table, plus a baseline-revision run archived as
  0/32-artifacts-absent;
- a line in the round-22 evidence naming the two still-red gates as carried,
  unchanged.

Fixable defect if caught now (author-side ordering + report shape); if
integrated as a scalar 32/32 with post-hoc expectations, it is a
judge-must-reject false-green, same class the r21 verifier already credited
this lane for refusing.
