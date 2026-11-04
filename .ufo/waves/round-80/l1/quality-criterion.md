## Round-80 criterion — a survivor mutant is killed by an isolated fixture, not by a neighbouring finding

Appended 2026-11-04 by the round-80 L1; every criterion above stands unchanged. Grounding: the round-79
non-author closure's R79-4 and R79-6 (`corpus/lessons/round-79-verifier-spotcheck.md` §6) record that
the frozen counter's fixture battery left three mutants alive — zeroing `wrong_kind` (k3), `malformed`
(k4) and `symlinks` (k5) — and that the cheap-note fixture stays red through `undisclosed=1` rather
than through a `malformed` finding, so a battery that only counts red fixtures cannot tell the two
mechanisms apart.

- **A survivor mutant is closed by a fixture that isolates its own mechanism.** A fixture row names the
  mutant class it kills, the single conjunct that flips it, and the counter output line that carries
  that conjunct — `undisclosed=1` for the cheap-note class (k4), a wrong `kind` for k3, a non-regular
  file for k5. A fixture that is red for any reason does not kill its mutant; the harness must report
  `killed == 3` only when each fixture is red through its own conjunct. Registered by
  `.ufo/waves/round-80/c80_ledger_fixtures.py`; evidence
  `.ufo/waves/round-80/controls/c80-cheap-note.txt`.
- **A gate's receipt is re-derived, never trusted.** A receipt that states a count (a selftest tally, a
  matrix total, an `undisclosed` value) is admitted only when the round's counter re-runs the producing
  command at the measured revision and gets the identical line; a mismatch is `open`, not `stale`.
  Able-to-fail: the round-80 C1 counter's R79-3 item re-runs `--selftest` and compares
  (`.ufo/waves/round-80/c80_defect_queue.py`), and the base receipt shows the item open for want of the
  receipt it later requires.
