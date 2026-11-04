# Round 87 — bounded gate-agreement calibration and conservative current age

Author-side lesson candidate for L1 integration, not an admission or successful measurement receipt. Base: `86ca7803fd964db7ae2a628c7e9048741c78a45f`; freeze: `58fee726102aa89ad2c1fa9f697869de3a212510`. Authority: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/contract.md`. Only L1 integrates independent candidate files. Paths below are absolute.

## Axes

- **C1 calibration — lowest axis, 2 HOLD.** Target: eight missing/mismatched ledger decisions → zero, exactly one complete expected row per decision, no additional rows, with matching committed snapshot digests. This mines proposal 4, “Gate-agreement ledger”, in `/home/vgpnk/Projects/shokunin/kake-shokunin/considerthese/2026-10-26.md`. It is finite self-assessment, not universal calibration or closure of D84-2/3/4.
- **C2 freshness — 10 HOLD.** Target: absent reader 0/17 → 17/17 frozen cases. The corpus contains twelve valid cases and five rejection cases. All six output fields and all case exits matter. This is an offline integer-seconds JSON adapter implementing the conservative RFC9111 §4.2.3 max profile, not the RFC's only permitted algorithm.

The ledger's intended integration destination, `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/gate-agreement-ledger.json`, does not make it domain knowledge: it records calibration metadata about historical author/closure agreement. S462's age-arithmetic entry is the sourced domain candidate. Neither a ledger copy nor a green finite counter proves the historical decisions were sound. Independent table comparison remains necessary.

## Gate

Candidate decisions below are author-side; outside admission and this round's independent spot-check remain closure-owned. Both source quotes were located by this seat in its own public GET of RFC9111 on 2026-11-04, retained at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeLesson/receipts/rfc9111.txt` (84477 bytes; SHA256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`).

| Candidate | Decision | Source and location | Located quote, ≤25 whitespace-delimited words | Reason / flip condition |
|---|---|---|---|---|
| S462 — conservative age arithmetic | ADMIT candidate, bounded to §4.2.3 | https://www.rfc-editor.org/rfc/rfc9111.txt, §4.2.3, retained L775 | “corrected_initial_age = max(apparent_age, corrected_age_value);” (3 words) | The conservative maximum is expressly available; L765–782 provide apparent age, response delay, corrected age and residency. Admit this arithmetic scope, not storage/reuse approval. |
| Proposition: current_age alone proves response reuse | REJECT proposition | Same reopened URL, §4.2, retained L621; supporting conditions §4 L468–490 | “response_is_fresh = (freshness_lifetime > current_age)” (5 words) | Even freshness requires a lifetime comparison; §4 separately requires matching URI, method, nominated fields, validation/directive handling and an allowed freshness/staleness/validation state. Flip only for a separately bounded decision procedure supported by those applicable rules, never age alone. |

S462 is a new bounded slice rather than expansion of S461's duplicate/lifetime scope. The selected profile always takes max(apparent_age, corrected_age_value); §4.2.3 L770 also permits corrected_age_value alone. Optional Age defaults to zero (L731–734). Date is required by this adapter; no missing Date or synthetic timing may be relabelled as observed input. Inputs use one epoch clock, exact integer seconds, no bool values, nonnegative local times and age, and request_time ≤ response_time ≤ now; date_value may be negative. No clock, Date parser, network cache, Cache-Control interpreter, browser behavior or reuse authorization is implemented by the arithmetic tool.

## Calibration provenance

This seat compared all eight expected decisions with the frozen outside tables, not merely the expected JSON:

| Snapshot | Decisions observed | SHA256 observed |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/snapshots/round-84-verifier-spotcheck.md` | S457 admit/agree; §4.1 normalization reject/agree; §5.2.2.2 max-age anchor reject/agree | `80f48887b1e5f2e9d7d54adcce19d8b935f77fc0b236620abac3335b730dfda9` |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/snapshots/round-85-verifier-spotcheck.md` | S458 admit/agree; blanket response-policy reorder equivalence reject/agree | `948c316831d0c71927e6a29501f05037b3faa940a251984ed28ca8f0eee2ce71` |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/snapshots/round-86-verifier-spotcheck.md` | S459 admit/agree; S461 admit/agree; RFC7234 minimum-duplicate attribution reject/agree | `47499686bc976564c43174fdeeae2219e0db2351c571678ba35caff0a34de42b` |

All three measured digests match `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/expected-ledger.json`. These observations support transcription fidelity only. The historical closure verdicts remain their authors' judgments, and the sample does not certify other rounds or future Gates.

## Mistakes

Rows retain class · evidence · captured-by · fix/failing condition. Historical evidence is not rewritten.

| Class | Evidence | Captured-by | Fix and condition able to fail |
|---|---|---|---|
| Self-certifying / cross-claim predicate | r86 snapshot, §Per-axis verdicts: “R1 requires the counter's own green receipt after receipt plus C2's success — self-certifying and cross-claim dependent” | r86 non-author closure | r87 counter reads claim artifact and frozen inputs, never a success receipt or the other claim's result. A receipt-only repair must not satisfy C1. r86's honest red remains historical; no green is invented here. |
| Mutable live-fleet comparison | `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/QUALITY.md`, Round 86: “the same base's open=4 then open=3 is not a revision-pinned comparison” | r86 QUALITY record, read by ScribeLesson | r87 commits the source snapshots and checks their digests. A source tamper, empty ledger, altered row or duplicate must fail. Mutant execution evidence remains to be provided by its assigned owner; this seat has not run or credited it. |
| Scratch disposal — candidate disposition | r86 snapshot, §Routed defects item 1: untracked raw mirror `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-86/w1/ExecAssim/mirror/corpus/lessons/round-81-gate/rfc9110.html` | r86 closure; r87 L1 disposal record | `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/bindings-disposal.md` records exact rm, exit0, no tracked receipt removed. This seat's directory observation found rfc9110.txt but no HTML mirror; it did not execute the disposal. Retain the distinction between untracked scratch HTML and historical tracked source text. Closure must decide whether the routed debt is discharged. |
| Quarantine order — candidate rule | r86 snapshot, §Conformance and §Routed defects item 2: data-row quarantine sweep ran after SOURCES append | r86 closure | Quarantine and validate candidate registry data before an authorized append; reject a post-append sweep presented as prior authorization. Assimilation is none this round: no merge/kake row append or assimilation success is claimed. Any authorized new source append still requires its own applicable registry checks. |

## QUALITY candidate

The separate integration candidate at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-87/w1/ScribeLesson/QUALITY-criterion.md` grounds a receipt-independent, snapshot-bound finite comparison in the two predicate mistakes above, and preserves the distinction between agreement metadata and domain truth. It is proposed text, not a passed check.

## Findings still open at this seat's handoff

- C1/C2 integrated measurements, independent implementation/selftest, constant-zero and Age-only shortcuts, and ledger mutants have not been executed or consumed by this scribe. Their owners must provide revision-bound evidence; this draft assigns no success to them.
- An actual owned-property GET trial is executor-owned. This scribe performed only the RFC source GET. Missing Date must yield an honest could-not-evaluate trial, not fabricated input.
- D84-2 general instrument soundness, D84-3 general semantic/input-dependence debt and D84-4 planner/operator conflict stay open. L1 planner plus scout data-walk is mitigation, not an operator ruling.
- Frozen expected bytes, target population and claim predicate remain unchanged. C1's finite equality could still accept a faithfully copied false table; agreement metadata is not proof of universal Gate reliability.
- No blanket no-harm, score promotion or outside admission is claimed. This seat made no production edits and ran no lane counter, selftest, build, lint or product trial.
