# ExecC1Registered

Claim C1 observed exits for the REGISTERED round 55–59 gate-registry members, per contract § Claim C1.
Rows parsed from `SKILL.md` at base `97cdc122379711c2b02a8970752c8782da3ac81d`, lines 1233–1309
(13 member rows: c55×2, c56×2, c57×3, c58×3, c59×3 — the seat spec text says 12; the parenthetical
count is 13 and 13 rows hold population-counter paths, so all 13 were run). Clone:
`git clone -q --shared` of the lane detached at base, cwd = clone for every run; `GIT_*` scrubbed;
`TMPDIR` per run under scratch; inherited env otherwise. Evidence: `ExecC1Registered.files/`
(`runs.json`, `harness.py`, `stdout-stderr.tar.gz` with every run's captured stdout/stderr).

RUNS: (member, label, pin, e_T, e_P, seconds — summary = first/summary line of stdout)

| member | label | pin | e_T | e_P | s_T | s_P | T summary (first line) |
|---|---|---|---|---|---|---|---|
| c55_readme_index | historical | 64c0ce12…f6 | 1 | 0 | 0.2 | 0.2 | `index_mismatches=1 knowledge_files=58 met=False` (head_changed=1) |
| c55_quote_truth | historical | 64c0ce12…f6 | 1 | 0 | 0.1 | 0.1 | `C2 quote-truth 6/8 met=False` |
| c56_selftally | live | — | 0 | — | 25.5 | — | `tally_mismatches=0 rows_checked=10 met=True` |
| c56_quote_truth | historical | 4cb225fb…ec | 1 | 0 | 0.1 | 0.1 | `C2 quote-truth 6/8 met=False` |
| c57_receipt_pins | historical | 32754df7…1e | 1 | 1 | 0.4 | 0.3 | T:`new_unpinned=4 new_receipts=0 scorecard_pin=0 met=False`; P:`new_receipts=0 scorecard_pin=0 met=False` |
| c57_idresolver_gate | live | — | 0 | — | 2.2 | — | `C2 id-resolver 5/5 met=True` (run with `[--fleet <fleet root>]` kept → `--fleet /home/vgpnk/Projects/shokunin`) |
| c57_quote_truth | historical | 32754df7…1e | 1 | 0 | 0.1 | 0.1 | `C3 quote-truth 6/8 met=False` |
| c58_receipt_rewrites | live | — | 0 | — | 0.2 | — | `events=19 … new_receipts=2 met=True` |
| c58_resolver_cases | live | — | 0 | — | 0.9 | — | `C2 resolver-cases 14/14 met=True` (`--work <scratch>` kept, `[--seed N]` dropped) |
| c58_quote_truth | historical | 8d340c15…1f | 1 | 0 | 0.1 | 0.1 | `C3 quote-truth 6/8 met=False` |
| c59_axis_evidence | live | — | 1 | — | 0.1 | — | JSON `met:false` — `superseded_kept=0` (needs 3); `mismatches=0 scores_held=2` |
| c59_resolver_cases | live | — | 0 | — | 1.2 | — | `C2 resolver-cases 21/21 met=True` (`TMPDIR=` env + `--work` kept, `[--seed N]` dropped) |
| c59_quote_truth | live | — | 1 | — | 0.1 | — | JSON `conditions_passed:6` — C3, C8, C9 fail |

Extra runs (controls, not label runs):
- `c57_idresolver_gate` at base WITHOUT `--fleet`: exit 2 (1.1 s), `unevaluable: no sibling registries under the fleet or no sibling snapshot` — matches the contract § C1 "Before" note.
- `c59_axis_evidence` / `c59_quote_truth` at base with `--base` left at its frozen default `fd6303ce…` (i.e. the `[--base <rev>]` segment NOT kept): exit 0 / 0 (1.4 s / 1.0 s; `superseded_kept=3`, `conditions_passed=9`). The T-column exit 1 for these two is produced ONLY by keeping `[--base <rev>]` → `--base <measured rev>`, a self-comparison the frozen counters reject (C3 "already in the base registry", C9 "no inserted [r59-correction]", `superseded_kept=0`). Contract § C1 placeholder rules keep the segment (`<rev>` is a placeholder) → the T values above stand as the literal-Entry observation; this optional-argument sensitivity is flagged for the counter build.
- `c57_receipt_pins` probe: exit 1 at `31b61a4d…31` (`new_receipts=2`), exit 0 (met=True, `new_receipts=3 scorecard_pin=1`) at `20217f23…06` (0.4 s). The counter IS green — but only from the revision where the third after-receipt landed, not at its registry pin.

MISMATCHES AT BASE: (label-vs-observation under contract § C1 mismatch classes)

| member | class | detail |
|---|---|---|
| c57_receipt_pins | historical_not_green_at_pin | pin `32754df7…1e` (`measured.json` revision) predates the landing of the three after-receipts (`31b61a4d`, `20217f23`); counter exits 1 there (`new_receipts=0 scorecard_pin=0`). Green from `20217f23` on. e_T=1 at base is correct for `historical`. |
| c59_axis_evidence | live_not_green | e_T=1 under the literal `[--base <rev>]`→measured-rev substitution (self-compare defeats `superseded_kept`); green (exit 0) when `--base` is left at the frozen default. Ambiguous substitution, not a code failure — flag for `c60_gate_status.py` to decide. |
| c59_quote_truth | live_not_green | same mechanism: `conditions_passed=6` (C3, C8, C9 fail) under `--base=<measured>`; 9/9 with default `--base`. |

All other rows: label matches observation (historical rows e_T=1/e_P=0; live rows e_T=0).
No `unregistered`, `duplicate_row`, `row_incomplete`, `unpinned`, or `pin_not_ancestor` found:
all 13 rows have 8 cells, a `0=`/`1=` verdict map, one backtick span naming the member path;
all four pins are ancestors of base (verified `git merge-base --is-ancestor`).

ENV NOTES:
- `c57_idresolver_gate` is fleet-dependent: reads sibling lanes' registries under `--fleet /home/vgpnk/Projects/shokunin` at their CURRENT heads (observed green today 2026-10-27); without `--fleet` it is exit 2 unevaluable. Any change in live sibling ownership vs `sibling-snapshot.json` flips this live member red — it is not hermetic.
- `[--base <rev>]` substitution is ambiguous (default = frozen `fd6303ce`, not "revision under test"); the e_T for both c59 members inverts on that choice — the contract text keeps it, but the counter build should pin the interpretation down explicitly.
- `c56_selftally` is the slow member (25.5 s): it itself clones the revision and runs 10 documented selftests building sandbox repos under TMPDIR; needs the lane clone's shared object store reachable (kept `.git/objects/info/alternates` works).
- `c58_resolver_cases` / `c59_resolver_cases` `git init` fixtures under `--work`/TMPDIR — all under scratch, no lane mutation.
- No network use observed in any run (all "offline, committed bytes only" claims hold).
- Observation cwd was a shared clone, not the live lane; `--root .` resolved to the clone. `git -C` inside counters reads the same object store via alternates — fine for read-only counters.

VERDICT: 13 registered members observed at base — 2 mismatches firm (c57_receipt_pins pin is not green there; both c59 members red under the literal kept `--base <rev>` segment) + 1 flagged ambiguity (`--base` substitution flips the two c59 exits; id-resolver-gate needs the fleet to evaluate at all).
