# ReRunLedgerGate — round-44 C2 no-harm

Axes: operability and freshness.

## Attack

Re-ran the round-44 ledger gate at the current checkout, targeting whether round-45 SCORECARD/LOG edits harmed the three-figure check, then ran its selftest.

Command:
```sh
python3 -B scripts/ledger_latest_check.py --root .
```
Decisive output (verbatim):
```text
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3581
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1703
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1705
ledger-quotes: 3 figures, 0 mismatches
```

Command:
```sh
python3 -B scripts/ledger_latest_check.py --selftest
```
Decisive output (verbatim):
```text
ledger_latest_check --selftest
  PASS matching fixture MATCH quoted=14 derived=14
  RED MISMATCH mismatching fixture quoted=18 derived=14
selftest: 2/2 passed
```

## Verdict

**PASS — the named no-harm attack found no harm:** the gate reports 3 figures, 0 mismatches and exits successfully; the selftest reports 2/2 passed. The mismatching fixture is the expected negative selftest case, not a ledger-check mismatch.

Files written: `.ufo/waves/round-45/w2/ReRunLedgerGate.md` only. No tools installed.
