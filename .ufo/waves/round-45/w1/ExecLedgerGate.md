# Round-44 C2 ledger gate baseline

Axes: operability, freshness.

## Result

I captured the required pre-integration baseline before any round-45 instrument was visible in the initial round-45 listing (which contained wave setup files and the w1 registry). Both checker invocations passed. The ledger check reports three matches and zero mismatches; its selftest reports 2/2 passed. This passes the named no-harm baseline attack: the current three declared ledger figures agree with the committed receipts, and the checker correctly selects the later correction in its matching/mismatching fixtures. This is baseline evidence only; it does not certify later SCORECARD/LOG edits.

## The three figures (read from `scripts/ledger_latest_check.py`)

The checker hard-codes these three definitions in `contract_spec()` and compares the latest matching occurrence in each ledger file against receipt-derived values (the latest selection is `matches[-1]`):

1. `rescore-tally`: the latest `re-scored N of the 27` in `SCORECARD.md`; `N` is the number of distinct non-empty `toolSha256` values across committed `master` JSON receipts at `.ufo/waves/round-43/verification/l1-rescores/*.json`.
2. `donothing-ratios`: the latest `not met (T1 x, T5 y)` in `LOG.md`; values are the `T1` and `T5` ratios from the committed `master` receipt `.ufo/waves/round-43/verification/freeze/ref41-base.json`.
3. `build-ratio-range`: the latest `T1 x–y, T5 a–b` in `LOG.md`; endpoints are the min/max `T1` and `T5` ratios derived from the three committed `master` receipts `build-1.json`, `build-2.json`, and `build-3.json` in `.ufo/waves/round-43/verification/freeze/`.

Derived decimals are rendered to the precision of the corresponding quote before equality comparison. At baseline the exact quoted and derived values were, respectively, `14`, `T1 4.21 / T5 7.05`, and `T1 1.00–1.01 / T5 1.11–1.22`.

## Round-45 edits that can harm the gate

The only quoted ledger values this checker reads are the latest matching statements in these paths:

- `SCORECARD.md`: an edit to the `rescore-tally` statement (`re-scored N of the 27`).
- `LOG.md`: an edit to the `donothing-ratios` statement (`not met (T1 ..., T5 ...)`).
- `LOG.md`: an edit to the `build-ratio-range` statement (`T1 ...–..., T5 ...–...`).

Round-45 writes to other paths do not change those local quoted statements. The receipt inputs are round-43 committed-`master` bytes. L1 or a wave-2 seat should rerun the checker after integration if any of the three quoted statements was edited; the after-run is not part of this assignment.

## Exact retained command output

The same output is retained at `.ufo/waves/round-45/verification/ledger-gate/before.txt`:

```text
$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/ledger_latest_check.py --root .
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3581
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1703
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1705
ledger-quotes: 3 figures, 0 mismatches
exit status: 0

$ python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/ledger_latest_check.py --selftest
ledger_latest_check --selftest
  PASS matching fixture MATCH quoted=14 derived=14
  RED MISMATCH mismatching fixture quoted=18 derived=14
selftest: 2/2 passed
exit status: 0
```

## Files written / blockers

- `.ufo/waves/round-45/verification/ledger-gate/before.txt` — baseline command output.
- `.ufo/waves/round-45/w1/ExecLedgerGate.md` — this report.

No tools were installed. No blockers. No post-integration check was run.