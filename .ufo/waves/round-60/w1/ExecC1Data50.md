# ExecC1Data50

Claim C1 data seat, round-60 w1. Members: the four round-50/51 counters. Method: `git clone -q
--shared` of the lane detached at base `97cdc122379711c2b02a8970752c8782da3ac81d` under the seat
scratch; each counter run as `python3 -B <path> --root . --revision <rev>`, `GIT_*` scrubbed,
`TMPDIR`=scratch, `timeout 1800`. All four counter blobs are byte-identical at base, at their
measured revisions, at measured-parent and at their round's final tip (verified by `git ls-tree`
blob sha), so the base-tree script is the same code every tree carries — no later hardening.
Ever-green probe = measured revision, measured-parent, round-final tip.

## MEMBERS:

### `.ufo/waves/round-50/c50_durable.py` (round-50 C2, operability)

- Measured revision `ff3f6ecff5caf579fdc76216aa9cb82fa146a30e`. Sources: SCORECARD.md line 4143-4144
  measured-results table (`Measured commit` column); `corpus/lessons/round-50-verifier-spotcheck.md`
  line 10 `Measured claim commit: ff3f6ecff5caf579fdc76216aa9cb82fa146a30e.`; fleet
  `.ufo/reports/round-50/kake.md` line 4 `Measured commit: ff3f6ecff5caf579fdc76216aa9cb82fa146a30e.`
- exit@base(97cdc12)=0 `C2 durable 1/1 met=True`; exit@measured=0 `C2 durable 1/1 met=True`;
  measured-parent (dfb4a3f)=1 `C2 durable 0/1 met=False` (do-nothing red: proofs absent);
  round-50 tip (1c7f076)=0 `C2 durable 1/1 met=True`.
- **Label: live** (green at base; green everywhere except the pre-evidence parent).
- Code facts for the row: exits `0=met`/`1=not met`/`2=exception`/`64=usage` (code matches docstring);
  no selftest flag — unknown arg exits 64.

### `.ufo/waves/round-50/c50_quote_class.py` (round-50 C1, freshness)

- Measured revision `ff3f6ecff5caf579fdc76216aa9cb82fa146a30e`; same source lines as above
  (SCORECARD.md:4143, kake.md:4, spotcheck line 10).
- exit@base=0 `C1 classed 3/3 met=True`; exit@measured=0 `C1 classed 3/3 met=True`;
  measured-parent=1 `C1 classed 0/3 met=False`; tip=0 `C1 classed 3/3 met=True`.
- **Label: live.**
- Code facts: exits `0`/`1`/`2=exception`/`64=usage` (code matches docstring); no selftest flag.

### `.ufo/waves/round-51/c51_wave_ledger.py` (round-51 C1, operability)

- Measured revision `842c1b44a590104cff4c06ef84726cac19475d0a`. Sources: fleet
  `.ufo/reports/round-51/kake.md` line 4 `Measured lane commit: 842c1b44a590104cff4c06ef84726cac19475d0a.`;
  `corpus/lessons/round-51-verifier-spotcheck.md` line 7 `measured lane tip (after):
  842c1b44a590104cff4c06ef84726cac19475d0a (= master, pushed)`; SCORECARD.md:4187 names it
  descriptively (`the lane commit that carries this section and the wave evidence`).
- exit@base=0 `C1 ledger 3/3 met=True`; exit@measured=0 `C1 ledger 3/3 met=True`;
  measured-parent (907790c)=0; round-51 tip (93d7fdbd45b0e5698927e7f9cb3dafca24ace416)=0.
- **Label: live** (green at base and everywhere probed; the counter is retrospective — it re-derives
  round-51 evidence that is committed forever).
- Code facts: `0=met`/`1=not met`; argparse errors exit 2; docstring claims `2=could-not-evaluate`
  and `64=usage` — neither is in the code (nothing returns 2 or 64; uncaught exceptions traceback
  to exit 1). No selftest flag.

### `.ufo/waves/round-51/c51_quote_truth.py` (round-51 C2, freshness)

- Measured revision `842c1b44a590104cff4c06ef84726cac19475d0a`; same source lines as above.
- exit@base=0 `C2 quote-truth 8/8 met=True`; exit@measured=0 `C2 quote-truth 8/8 met=True`;
  measured-parent=0; tip (93d7fdb)=0.
- **Label: live.**
- Code facts: `0=met`/`1=not met`; argparse exits 2; same docstring/code exit-code drift as the
  ledger counter (docstring says `2=could-not-evaluate`, `64=usage`; code has neither). No selftest
  flag. Two commits touched the file (19a99bd create, 9d13768 receipt-lookup fix) — blob at base
  equals blob at measured.

## ROWS:

Complete 8-cell draft rows for all four members (each `gate (live; ...)`, entry commands the real
CLIs, verdict maps read from the code, self-test cells `none (no selftest mode)`, Owner `kake`):
`.ufo/waves/round-60/w1/ExecC1Data50.files/rows.md`. Note for the integrator: none of the four is
registered in SKILL.md today — they are part of C1's 12 unregistered members at base; the round-52
`wave-evidence-ledger` row (SKILL.md:1215) is the hardened round-52 counter, not c51_wave_ledger.

## NOTES:

- Raw outputs (16 runs): retained at `ExecC1Data50.files/run-outputs/<tag>.txt`
  (stdout+stderr of each invocation); last summary lines quoted above.
- Round-51 "final tip" taken as `93d7fdbd45b0e5698927e7f9cb3dafca24ace416` (the round-51 spot-check
  commit, first child of the measured commit and round-52's declared base `93d7fdb`); spot-check
  calls `842c1b4` "measured lane tip (after) (= master, pushed)" — either reading gives exit 0.
- Interesting detail: the c50 counters are red at measured-parent `dfb4a3f` — their evidence
  (order/wave-cite proofs, lesson, S286 row) lands only at the measured commit itself. That is
  do-nothing behaviour working as designed, not fragility: both are stable green on every later tree.
- c51 docstring/code exit-code drift is a real (cosmetic) defect worth a lesson note: c60's gate
  only requires `0=`/`1=` in the Verdict map cell, so the rows state `2=usage (argparse)` per the
  code, with the docstring discrepancy named inside the cell.
- [INFERENCE] C1's population regex requires committed path `^\.ufo/waves/round-(N)/...` with
  matching N — all four members qualify (`c50_*` under round-50, `c51_*` under round-51).
- Tool installs: none. Scratch: `/fast/scratch/hyaku/kake-r60/ExecC1Data50` (deleted on exit via
  the seat cleanup step).

VERDICT: all four members measured green at base — live, live, live, live; 8-cell rows drafted in ExecC1Data50.files/rows.md.
