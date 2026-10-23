# ExecLedgerCheck — round 44 wave 1

Axis: **freshness** (lane-owned axes: operability and freshness).

Implemented the L1-refined three-figure C2 checker. It reads the declared JSON contract, takes the last `re.S` match in each ledger file, reports the match's 1-based line, and compares each captured number to its committed receipt-derived value rounded half-up to the same decimal precision. The three derivations are distinct `toolSha256` values from committed L1-rescore JSONs, T1/T5 from the committed `ref41-base.json`, and per-field min/max across committed `build-1..3.json`. Receipt bytes are read through `git show master:<path>`; a ledger's worktree copy is preferred, falling back to `git show master:<path>` only when absent. The checker pins the exact three-figure contract so spec edits cannot silently drop or reroute a check. Wave composition was excluded by the L1 refinement; no ledger or receipt was edited.

## Commands and evidence

Synthetic selftest:

```text
$ python3 -B kake-shokunin/scripts/ledger_latest_check.py --selftest
ledger_latest_check --selftest
  PASS matching fixture MATCH quoted=14 derived=14
  RED MISMATCH mismatching fixture quoted=18 derived=14
selftest: 2/2 passed
exit=0
```

Before run, before any ledger repair:

```text
$ python3 -B kake-shokunin/scripts/ledger_latest_check.py
rescore-tally MISMATCH quoted=18 derived=14 SCORECARD.md:3393
donothing-ratios MISMATCH quoted=T1 4.27, T5 8.68 derived=T1 4.21, T5 7.05 LOG.md:1661
build-ratio-range MISMATCH quoted=T1 1.00–1.02, T5 1.13–1.18 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1660
ledger-quotes: 3 figures, 3 mismatches
exit=1
```

Verbatim checker stdout is recorded at `.ufo/waves/round-44/verification/ledger-before.txt`; `.ufo/waves/round-44/verification/ledger-before.txt.exit` contains `1`.

Other shell commands run:

```text
$ printf '%s\\n' kake-shokunin/.ufo/waves/round-43/w1/*.md | wc -l
51
$ mkdir -p /fast/scratch/hyaku/kake-r44/ExecLedgerCheck /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/verification /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w1
(no output)
```

The report-count probe was exploratory only; the final L1 scope excludes wave composition. No tools were installed. No build, lint, format, or unrelated tests were run.

## Files written

- `scripts/ledger_latest_check.py`
- `.ufo/waves/round-44/ledger-quotes.json`
- `.ufo/waves/round-44/verification/ledger-before.txt`
- `.ufo/waves/round-44/verification/ledger-before.txt.exit`
- `.ufo/waves/round-44/w1/ExecLedgerCheck.md`

Scratch directory created: `/fast/scratch/hyaku/kake-r44/ExecLedgerCheck/` (no temporary files).

## Risks / blockers

No blocker. The three declared regex/receipt bindings are deliberately duplicated in the checker as a fixed contract; changing the scope requires a coordinated checker and spec update. `master` must remain the committed receipt ref for normal runs and the ledger fallback.
