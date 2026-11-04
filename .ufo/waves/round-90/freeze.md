# Round 90 freeze — kake (L1 KakeR90)

Frozen before any after-state data. Base `209027f49959e2e2f0e16867a90a7bb38bbcd3f4`
(lane `master` at round start; `ls-remote` equal). No gate, correction, relocation or
superseding row existed when the controls below ran.

## Claims (2; distinct axes; causally separable)

### C1 — calibration (lowest owned non-retired axis, 2 HOLD)

The three defects the round-89 outside spot-check routed
(`corpus/lessons/round-89-verifier-spotcheck.md` §Routed defects D89-1, D89-2, D89-3)
close on committed bytes.

- Counter: `.ufo/waves/round-90/c90_defects.py` (sha256
  `462224f630d4369138af1bf38783b16695b712b85bb46b7b9d2d3c35f05d519b`).
- Command: `python3 -B .ufo/waves/round-90/c90_defects.py --root . --revision <REV> --work <scratch>`
- Predicate (same sentence as the counter's `met`): **met ⇔ open == 0 over items D1, D2, D3.**
- Before (base): `open=3 closed=0 met=false`, exit 1 (`controls/base-c1.txt`).
- Target after: `open=0 closed=3 met=true`, exit 0, at the measured carrier.
- Kill rule: any item open at the carrier → C1 not met; reported as an honest stop,
  never narrowed.
- D1 carries one LIVE conjunct (no untracked lane-root entry in the lane working tree);
  it is labelled `live` in the counter output and is not revision-bound.

### C2 — operability, capability acquisition: a behavioural cache-key conformance gate

The lane holds `scripts/cache_key_conformance.py`, a gate that refuses the committed
non-conforming cache-key population (57 subjects: 15 round-89 ExecControls stubs,
5 round-89 shortcut controls, 35 non-equivalent MutKey mutants, 2 round-90 sandbox
negatives) and admits the conforming one (4 subjects), under nonce renaming, with no
subject hash or stem in its source. Sourced: the CR/LF every-header refusal clause is
grounded on a RFC 9110 §5.5 row opened this round.

- Counter: `.ufo/waves/round-90/c90_gate.py` (sha256
  `703b00580391d8546ce238099d8fdba46358797af307cad02169c3828d70ccfa`); population pins
  `frozen/c2-population.sha256` (sha256
  `a57f8985e69ac01bb0d9f0d21f95a2007dad5396421c7cf46d0b0f57c614850c`); round-90 sandbox
  negatives `frozen/neg-oracle-path-import.py` (`3621e359…`) and
  `frozen/neg-exec-source.py` (`ad251e4a…`).
- Command: `python3 -B .ufo/waves/round-90/c90_gate.py --root . --revision <REV> --work <scratch>`
- Predicate: **met ⇔ gate present ∧ population=ok ∧ positives 4/4 admitted ∧
  negatives 57/57 refused (false_admits=0, errors=0) ∧ anti_table=ok.**
- Before (base): `gate=absent … met=false`, exit 1 (`controls/base-c2.txt`). The
  round-89 instrument's own reading on the 15 stubs is 7 false admits
  (`.ufo/waves/round-89/w1/ExecControls/scoring-receipt.txt`).
- Target after: `positives=4/4 negatives_refused=57/57 false_admits=0 errors=0
  anti_table=ok population=ok met=true`, exit 0, at the carrier.
- Kill rule: any positive refused, any negative admitted or errored → not met; reported.

## Controls executed before this freeze (`controls/run_controls.sh`)

`controls/ctl-c1.txt`: do-nothing (lane at base) open=3; forgeries D1a (copy committed,
root file left), D1b (wrong bytes), D2a (numbers disagree with receipt), D2b (fabricated
receipt agreeing with its correction — killed by the c89 re-run), D2c (filed row
rewritten in place), D3a (fabricated quote), D3b (S463 edited in place): each leaves its
item open; positive fixture with all three fixed: `open=0 closed=3 met=true`.
`controls/ctl-c1-v0-before-parse-fix.txt`: the first run, in which the positive control
stayed open because the counter read the quoted superseded `open=5 closed=1` as the
reading; fixed before freeze (last reading after `f62e7954`), disclosed in the lesson.

`controls/ctl-c2.txt`: do-nothing (no gate) met=false; blanket-refuse gate positives 0/4;
blanket-admit gate false_admits 57; hash-table gate (refuses pinned hashes) and
name-table gate both false_admits 57 under nonce renaming. Each met=false.

No positive control exists for C2 before the gate is written (a correct gate is the
claimed work); C2 reachability is shown only by the carrier measurement.

## Separability

C1 reads `SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md` S463 and the superseding row,
the round-90 lesson Gate and the relocated file; C2 reads only `scripts/` and the
frozen subject population. Neither counter reads the other's outputs or receipts.
