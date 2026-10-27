# ReviewerNoHarm

RUNS:

| Gate | Base result (w1/ExecHistoricalGates.md) | Build `c1e39ef` result |
|---|---|---|
| `c55_readme_index.py` | exit 0, 0 mismatches / 54 files | exit 0, 0 mismatches / 56 files |
| `c57_receipt_pins.py` | exit 0, `met=True` (tip in w1 report) | exit 1, `met=False`; `new_unpinned=4`, `new_receipts=0`, `scorecard_pin=0` |
| `c57_idresolver_gate.py` | exit 0, 5/5 | exit 0, 5/5 |
| `c52_wave_ledger.py` | exit 0, 3/3 | exit 0, 3/3 |
| `c57_quote_truth.py` | exit 0, 8/8 | exit 1, 6/8; C7 and C8 fail |
| `c56_selftally.py` | Not measured in the cited w1 report (explicitly excluded there) | exit 0, `met=True`, 10/10 rows; zero tally mismatches |

The six build-revision runs used the counter scripts from the clone checked out at `c1e39ef`, with `--root` and `--revision c1e39ef3567542b2dc602cc235ed717d6dfbd915`; the resolver gate also used `--fleet /home/vgpnk/Projects/shokunin`. The gate-script files themselves had no diff between base `0440485` and the build.

NEW REDS:

- `c57_receipt_pins.py`: red against the w1 tip result (green). It reports four unpinned items: `round-57/measured.json` because `scripts/id_resolver.py` differs from the frozen counter baseline, and the three `after-c1/c2/c3` receipts introduced at `31b61a4` with `measured=None`. This is a concrete new gate regression at the assigned build.
- `c57_quote_truth.py`: red 6/8. The round-58 SKILL.md registry row explicitly says this gate is historical from round 58 and becomes red when later rows append; the observed failures are exactly its mirror-row condition: C7 scratch registry differs from landed registry, and C8 `162 != 158 + 2` plus the append-only mirror mismatch. This is the documented historical condition, not a new quote-truth defect.
- `c56_selftally.py` passed on the build. No base comparison is recorded for this gate in the cited w1 report; its build result alone establishes no newly introduced red.

VERDICT: One actionable new red versus the cited base/tip evidence: `c57_receipt_pins.py`; all other comparable gates are green or the documented round-58 mirror-row historical red. `c56_selftally` is green at the build; base result unavailable in the cited comparison.