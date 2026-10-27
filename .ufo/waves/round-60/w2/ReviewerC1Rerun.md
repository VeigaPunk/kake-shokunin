# ReviewerC1Rerun

ATTACKS: Re-ran frozen C1 gate-status counter against B1 in a `git clone --shared` and against the lane root directly; compared all member lines and summaries across runs and to the base receipt; ran the counter selftest and recorded elapsed time.

RUNS:
- Clone was detached at `8b33fd248d126b48d838af5c38bc175850f41a09`; `git rev-parse --show-toplevel` matched the clone path. For `c60_gate_status.py`, `c60_guard_cases.py`, `c60_quote_truth.py`, and `derive_c60_quote_truth.py`, B1 blob IDs equalled both the frozen `1ea305904933ac0f57e84ac1e7a8207e486f577d` blob IDs and the lane worktree hashes.
- Clone run A command: `python3 -B .ufo/waves/round-60/c60_gate_status.py --root . --revision 8b33fd248d126b48d838af5c38bc175850f41a09 --jobs 4 --work <seat-scratch>/work-a`. Exit 0, 125.154 s; summary `members=28 mismatches=0 scores_held=3/3 met=True`.
- Clone run B used the same command with `--work <seat-scratch>/work-b`. Exit 0, 94.947 s; same summary.
- Direct-root command: `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/c60_gate_status.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 8b33fd248d126b48d838af5c38bc175850f41a09 --jobs 4 --work <seat-scratch>/work-c`. Exit 0, 70.455 s; same summary.
- Selftest: `python3 -B .ufo/waves/round-60/c60_gate_status.py --selftest --work <seat-scratch>/work-selftest`; exit 0, `selftest 76/76 passed`.
- Full stdout for each run and selftest, exit codes, and the pinned base receipt are preserved under `ReviewerC1Rerun.files/`.

DIFF:
- Clone A and B stdout were byte-identical (`diff -s`: “Files .../a.out and .../b.out are identical”); all 28 per-member lines matched. Direct-root output also matches those lines and summary.
- Base receipt reports `members=28 mismatches=14 scores_held=3/3 met=False`; B1 runs report 28/0/3 and met true. The base's 12 unregistered members and c53 live mismatch are corrected at B1; c57 idresolver is `live e_T=0` in the base receipt and all three B1 observations.
- The specifically disclosed live dependency remains: `.ufo/waves/round-57/c57_idresolver_gate.py:192-207` enumerates sibling directories under `/home/vgpnk/Projects/shokunin` and reads each sibling repository's current `HEAD:corpus/SOURCES.md`. It did not cause an observed flip in these runs. Thus no nondeterminism was demonstrated; this is a residual hermeticity risk, not a measured counter failure.

FINDINGS:

| severity | target file:line | issue | evidence command | fix |
|---|---|---|---|---|
| — | — | No actionable defect observed in the assigned rerun attack. C1 predicate, per-member output, and selftest reproduced successfully. | See `RUNS:` and preserved outputs. | None indicated by this rerun. |

VERDICT: C1 passes the specified B1 rerun and selftest; outputs were deterministic across the three observations, with the disclosed live-sibling dependency still a residual risk.