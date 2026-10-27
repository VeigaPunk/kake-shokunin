# Round 62 — lessons (kake)

Round opened 2026-10-27; base `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`. One frozen claim: calibration, correction of the round-61 S432 quote disagreement. Contract and base-control evidence: `.ufo/waves/round-62/contract.md`, `.ufo/waves/round-62/controls/base-c1.txt` (created after integration below). Source S432 was re-opened this round at https://fetch.spec.whatwg.org/ on 2026-10-27; the retained body is `.ufo/waves/round-61/sources/S432.html`.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| vacuous | `corpus/lessons/round-61-verifier-spotcheck.md:33` records that the admitted S432 span is a generic section lead-in; `corpus/knowledge/response-header-expectations.md` previously quoted that lead-in and a fragment ending mid-sentence. The existing quote-truth and locator criteria did not test whether a span actually supported the attached publishing claim. The quoted text exists at the cited location; the failure is that it does not substantiate the attached proposition. | none — no existing criterion caught this support failure; the non-author verifier caught it at round 61. | Add a source-support criterion that rejects a generic lead-in even when it is a raw quote at the correct location, and keep the correction held while the only complete S432 sentence fails the existing raw-substring rule. The criterion's concrete reject case is the verifier-disputed lead-in; the correction note does not claim the citation is repaired. The frozen counter was shown by the mutation probe to false-green with a marker-only fixture, so neither its `unresolved` output nor this single criterion establishes calibration or generalization. |

## Gate

Candidates considered: the round-61 S432 admission and its verifier-disputed quoted span; proposal 4 in `considerthese/2026-10-26.md` (a gate-agreement ledger). The latter was not implemented: the single existing spot-check verdict identifies this specific disagreement, and a second ledger would add bookkeeping without adjudicating the raw-quote constraint. Flip condition: repeated verifier/gate comparisons show a durable need to summarize more than the specific cases already recorded in spot-check reports.

- **S432 source row (lane assessment):** S432 was reopened this round: https://fetch.spec.whatwg.org/, accessed 2026-10-27; retained body `.ufo/waves/round-61/sources/S432.html`, sha256 `63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`. Its §3.6 opening sentence (body lines 6150–6156) contains the field-purpose proposition across inline markup, but the normalized rendering is not a raw substring of the retained HTML. Because existing `corpus/QUALITY.md` requires raw-substring quotes, this round does **not** admit it as a replacement quote and leaves the S432 knowledge citation unresolved. The already-mined S432 registry row stays unchanged; it also supports a separately scoped value rule.
- **Reject:** the earlier “Web developers and conformance checkers must use the following” lead-in and the truncated “can be used to require checking of a” fragment do not independently state the attributed field proposition. The verifier's S432 `Disagree` remains preserved at `corpus/lessons/round-61-verifier-spotcheck.md:33`; `corpus/knowledge/response-header-expectations.md:218-220` appends the correction-held status without claiming the citation repaired.
- **Agree (lane self-assessment only):** the verifier's rejection of those two old spans is correct under the existing quality bar. No round-62 independent non-author spot-check occurred; dispatched seats are author-side. Closure must not treat this self-assessment as an outside verdict.

Counter result after landing is recorded in the report and is not accepted as calibration evidence: the frozen counter's marker-only false-green is documented by the independent attack receipt `.ufo/waves/round-62/w1-results.json` (seat `ReviewerCounterControls`). The claim therefore remains unprovable; score stays 2.

## Sources census

Round-start census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → 171 rows, 16 W04 cross-scope duplicate-URL warnings, exit 0. Round-end census and exit are recorded in the round report after final tree integration. No SOURCES row was added or changed; the already-mined S432 row was opened again and cited by the claim.

Assimilation: none. The round-61 verifier finding, not a package, grounds the correction. No entry was adopted from `merge/kake/`.
