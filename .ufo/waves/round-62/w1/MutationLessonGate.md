# MutationLessonGate

**Mutant:** the committed lesson-gate predicate in frozen `c62_calibration.py` (lines 36–37) checks only for `## Gate`, `S432`, `Agree`, and `Reject`; it does not require an agreement/disagreement decision or a resolvable verifier/source pointer. For isolation, each test commit was based on a scratch fixture commit adding only `corpus/lessons/round-62.md`; the frozen counter remained unchanged (SHA-256 `ba7b77376c18d3abf72c3522a1cb46df7ab53395847f980e13a7128e7878548d`).

**Expected detector:** stripping required lesson evidence should set `lesson_gate=0`; a complete gate-shaped text without actual agreement evidence or pointer should be rejected. A *killed* mutant here means the measured gate flag is zero, not that the overall claim is met (other frozen predicates intentionally remain false in the fixture).

**Commands / outputs:**

- Baseline counter, `python3 -B .ufo/waves/round-62/c62_calibration.py --root . --revision c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`:
  `revision=c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false` (exit 1). This is the contract's known base control, not evidence of mutant detection.
- Fixture setup validated root with `git -C /fast/scratch/hyaku/kake-r62/MutationLessonGate/fixture rev-parse --show-toplevel` → `/fast/scratch/hyaku/kake-r62/MutationLessonGate/fixture`. Added a gate-only lesson containing `## Gate`, `S432`, `Agree`, `Reject`, `Agreement`; counter on `HEAD` output: `revision=HEAD disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=1 source_row=1 met=false` (exit 1). No verifier pointer or meaningful agreement/disagreement evidence was present: **survived**.
- Omit `Agree`, retain `## Gate`, `S432`, `Reject`, `Agreement`: output `revision=HEAD disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false`; **killed**.
- Omit `Reject`, retain `## Gate`, `S432`, `Agree`, `Agreement`: output `revision=HEAD disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false`; **killed**.
- Omit `S432`, retain `## Gate`, `Agree`, `Reject`, `Agreement`: output `revision=HEAD disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=0 source_row=1 met=false`; **killed**.
- Omit agreement evidence, retain `## Gate`, `S432`, `Agree`, `Reject` only: output `revision=HEAD disagreements=1 unresolved=1 quote_correction=0 criterion=0 lesson_gate=1 source_row=1 met=false`; **survived**.

**Verdict:** mixed coverage. Counter detects absence of the literal Admit-side token (`Agree`), Reject token, and S432 token in the tested variants. It does **not** detect absence of actual agreement/disagreement evidence, nor lack of a resolvable verifier/source pointer. The full-form-token mutant survives as `lesson_gate=1`. These runs do not change or adjudicate the frozen claim.

**Restoration evidence:** all fixture commits/files were confined to `/fast/scratch/hyaku/kake-r62/MutationLessonGate/fixture`; the attempted final baseline re-run/counter comparison did not complete because the fixture's untracked wave counter is absent from the base Git revision (`fatal: path '.ufo/waves/round-62/c62_calibration.py' exists on disk, but not in 'c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13'`). Therefore restored-control verification is **inconclusive**. The scratch cleanup command was after the failed command in an `&&` chain, so cleanup did not execute; no claim of scratch removal/restoration is made.