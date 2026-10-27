# MutC1Counter — Round 63 C1 mutation probe

## Scope and method

Mutation-tested the frozen `.ufo/waves/round-63/c63_calibration.py` decision logic (relevant code: lines 121–166). Fleet counter remained untouched. Before/after SHA-256 of the fleet counter and scratch pristine copy: `bcd16f680da2594040a897803ddefa82ff13679ebe458dd6f6ff6c957ea3fc91` (matches the contract’s frozen digest).

Scratch: `/fast/scratch/hyaku/kake-r63/MutC1Counter/`. Marker fixture is a byte-identical copy of the committed round-62 false-green corpus, confirmed by `diff -r`; own scratch repo revision `5faf9fa0b7c5bce0212b7c7ed57a43ae02cceb1a`. Corpus-only junk fixture is copied from measured revision `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f` and has no `.ufo` blobs; own revision `03f0640d26984a52809692e91e5f36084073359a`. Both scratch repo top-levels were verified before committing, with throwaway identity configured per command. Existing fixture-receipt revision is `7833be888760bc7878857aa39362792b02e3ab07`; the scratch marker repo differs only in repo commit identity/history, not corpus bytes.

For every pristine/mutant invocation the command shape was:

`python3 -B <scratch-counter.py> --root <target-root> --revision <target-revision>`

Targets were: measured tree at `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`; base at `13d4519818db28cd0aa912e49020659140d7b9fa`; marker fixture at `5faf9fa0b7c5bce0212b7c7ed57a43ae02cceb1a`; and junk fixture at `03f0640d26984a52809692e91e5f36084073359a`. Same bounded detector for each: compare each target’s `met` and process exit status with pristine; a difference is a kill. Contract expectation is measured met=true/exit 0 and base, marker, junk met=false/exit 1.

Pristine outputs (all observed):

- Measured: `revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`; exit 0.
- Base: `revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=1 met=false`; exit 1.
- Marker: `revision=5faf9fa0b7c5bce0212b7c7ed57a43ae02cceb1a disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false`; exit 1.
- Junk: `revision=03f0640d26984a52809692e91e5f36084073359a disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false`; exit 1.

## Mutants and kill matrix

`K` = killed (a `met`/exit change on that target); `S` = survived (same `met`/exit as pristine). Other printed component fields can change without counting as a kill under this detector.

| Mutant (one change) | Measured | Base | Marker-only | Junk | Verdict |
|---|---:|---:|---:|---:|---|
| M01 `blobs_match` initial value forced 1 | S | S | S | S | Survived |
| M02 invert class-match condition | K | S | S | S | Killed |
| M03 correction quote test loosened to `"Content-Type" in knowledge` | S | S | S | S | Survived |
| M04 criterion reduced to `"substantive" in quality` | S | S | S | S | Survived |
| M05 lesson gate reduced to `"## Gate" in lesson` | S | S | S | S | Survived |
| M06 source-row regex loosened to `"S432" in sources` | S | S | S | S | Survived |
| M07 `met = True` | S | K | K | K | Killed |
| M08 `resolved` conjunction changed to disjunction | S | K | K | K | Killed |
| M09 swap raw-substring/collapsed-only return labels | K | S | S | S | Killed |
| M10 drop raw/text SHA equality checks from `blobs_match` | S | S | S | S | Survived |
| M11 `quote_correction = int(correction)` (drop blob/class gates) | S | S | S | K | Killed |
| M12 `unresolved = 0` | S | S | S | S | Survived |
| M13 require `disagreements == 0` for `met` | K | S | S | S | Killed |

Thus 6/13 were killed and 7/13 survived. M01 and M12 do alter printed fields (`blobs_match=1` on blobless targets; `unresolved=0`), but did not alter the detector’s `met`/exit pair. M08’s false green is detected by base, marker, and junk. M11 is specifically killed by junk, where planted corpus markers make `correction=1`, but the retained blobs are absent. M02/M09/M13 are killed by the measured real tree’s expected green.

### Exact mutant output evidence (changed-target results)

The following are the outputs on targets that killed the mutant; unlisted targets retained pristine `met` and exit:

- M02 measured, exit 1: `revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=0 blobs_match=1 derived=collapsed-only class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false`.
- M07 base/marker/junk, each exit 0 and `met=true`. Marker output: `revision=5faf9fa0b7c5bce0212b7c7ed57a43ae02cceb1a disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=true`.
- M08 base, exit 0: `revision=13d4519818db28cd0aa912e49020659140d7b9fa disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=0 source_row=1 unresolved=0 met=true`; marker, exit 0: `revision=5faf9fa0b7c5bce0212b7c7ed57a43ae02cceb1a disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=0 lesson_gate=0 source_row=1 unresolved=0 met=true`; junk, exit 0: `revision=03f0640d26984a52809692e91e5f36084073359a disagreements=1 quote_correction=0 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`.
- M09 measured, exit 1: `revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=0 blobs_match=1 derived=raw-substring class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=1 met=false`.
- M11 junk, exit 0: `revision=03f0640d26984a52809692e91e5f36084073359a disagreements=1 quote_correction=1 blobs_match=0 derived=unevaluable class_match=0 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true`.
- M13 measured, exit 1: `revision=05b0d7f4b4a23513390f7b92547e2b0f1fccb06f disagreements=1 quote_correction=1 blobs_match=1 derived=collapsed-only class_match=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false`.

## Findings and restoration

The bounded controls kill the explicit false-green mutations M07, M08, and M11, and catch false-red changes M02, M09, M13. The marker-only control does **not** exercise individual component gates because it fails multiple independent components at once (`quote_correction=0`, `criterion=0`, `lesson_gate=0`). Notably M10, which removes both ledger/blob digest equality checks, survives all four controls: the current negative controls contain no retained blobs/ledger, while the measured tree has matching digests. This is a coverage finding; it does not change the frozen claim or counter.

The frozen fleet counter was not edited or restored because it was never modified. Its post-probe hash remains the frozen hash above. Mutant files and fixture repos were confined to the assigned scratch directory. No git/jj mutation occurred in the fleet repository; scratch repo commits were the only Git writes. No tool was installed.
