# ExecC1Predict

Claim C1 collision forecast. Mock = scratch `git clone --shared` of base `97cdc122379711c2b02a8970752c8782da3ac81d`
plus one selftest-identity commit `e1ecc4309764e17b6fcaf991443a265b42a117cc` carrying the spec's round-60 changes:
3 appended `## Registry` rows S427/S428/S429 (contract URLs, plausible cells), `corpus/knowledge/google-user-triggered-fetchers.md`
and `robots-txt-limits.md` (provenance trio + paragraph), a 3-line `  **[r60-correction 2026-10-27]**` run after
`googlebot-verification.md:38`, appended `## Round 60` sections in SCORECARD.md/LOG.md, a `### Round 60 gate registry additions`
table (one complete row) in SKILL.md, and a `scripts/append_guard.py` stub. 8 files, +54 lines, nothing else.
Runner + logs: `ExecC1Predict.files/{run_pop.py,run_variant.py,make_mock.py,results-*.json,logs/{base,mock}/}`.

Command resolution per the C1 contract: registered entry commands where a `Name|Kind|Entry command|…` row's
Entry-command cell contains the member path (16 registered, 12 unregistered — matches the L1 probe's 12);
unregistered members ran `python3 -B <path> --root . --revision <rev>`. For the 5 members whose Entry command
carries a `[...]` segment (`--fleet`, `--work`, `--base`, `--json`), the contract text says keep the segment when
every `<…>` inside is a placeholder, but the L1 probe observed `c57` exit 2 *without* `--fleet` — so both readings
were run. Columns below: `bk` = brackets kept per contract text, `bd` = brackets dropped (probe-consistent).

## RUNS:

| member | registered | exit@base bk | exit@base bd | exit@mock bk | exit@mock bd |
|---|---|---|---|---|---|
| c48_lint_count | no | 0 | — | 0 | — |
| c48_quote_truth | no | 0 | — | 0 | — |
| c49_order | no | 0 | — | 0 | — |
| c49_quote_truth | no | 0 | — | 0 | — |
| c50_durable | no | 0 | — | 0 | — |
| c50_quote_class | no | 0 | — | 0 | — |
| c51_quote_truth | no | 0 | — | 0 | — |
| c51_wave_ledger | no | 0 | — | 0 | — |
| c52_gate_registry | no | 1 | — | 1 | — |
| c52_mutation_ladder | no | 0 | — | 0 | — |
| c52_quote_truth | yes (historical @1ae8de5d) | 1 | — | 1 | — |
| c52_wave_ledger | yes (live) | 0 | — | 0 | — |
| c53_gate_truth | yes (live) | 1 | — | 1 | — |
| c54_ops_debt | no | 0 | — | 0 | — |
| c54_s374_calib | no | 0 | — | 0 | — |
| c55_quote_truth | yes (historical @64c0ce12) | 1 | — | 1 | — |
| c55_readme_index | yes (historical @64c0ce12) | 1 | — | 1 | — |
| c56_quote_truth | yes (historical @4cb225fb) | 1 | — | 1 | — |
| c56_selftally | yes (live) | 0 | — | 0 | — |
| c57_idresolver_gate | yes (live) | 0 | 2 | 0 | 2 |
| c57_quote_truth | yes (historical @32754df7) | 1 | — | 1 | — |
| c57_receipt_pins | yes (historical @32754df7) | 1 | — | 1 | — |
| c58_quote_truth | yes (historical @8d340c15) | 1 | — | 1 | — |
| c58_receipt_rewrites | yes (live) | 0 | — | 0 | — |
| c58_resolver_cases | yes (live) | 0 | 0 | 0 | 0 |
| c59_axis_evidence | yes (live) | 1 | 0 | 1 | 0 |
| c59_quote_truth | yes (live) | 1 | 0 | 1 | 1 |
| c59_resolver_cases | yes (live) | 0 | 0 | 0 | 0 |

`—` = member has no bracketed segment; one reading only. 56 timed runs total, all real exits, no timeouts.

Base reconciliation vs the L1 probe: 12 unregistered + `c53_gate_truth` live-red + `c57_idresolver_gate`
exit 2-without-fleet = >=13 mismatches, matching the probe under the `bd` reading. Under `bk`, `c57` is green
at base and the count drops to 12 live/structural + scores (still >=13). All 7 `historical` rows are red at
base and mock as labelled.

## PREDICTED RED:

- **`c59_quote_truth` (crawler-identity-quote-truth-counter) — the R59-D1 collision, unavoidable, both readings.**
  Under `bd` (default `--base fd6303ce`): mock exits 1, `conditions_passed 6/9`; three independent conditions fail —
  - C8 `mirror_bytes`: "registry rows 167 != mirror rows 162 + 2" — any registry append this round trips the
    frozen 162+2 mirror; the real tree fails identically (167 vs 162+2).
  - C7 `validate_before_append`: "validated scratch registry is not byte-equal to the landed registry" —
    the pinned round-59 validate scratch cannot equal a registry with three new rows.
  - C5 `quote_truth`: the `[r60-correction 2026-10-27]` run must quote S428 carrying `generally ignore`
    (round-60 C9), but c59's C5 checks every quoted span of the S426 entry against the **S426** retained body;
    "generally ignore" occurs in `sources/S428.html` and nowhere in `sources/S426.html` (greps run), so no
    compliant correction quote can pass. Any wording of the planned correction trips C5.
  Under `bk` (`--base` resolves to the measured revision): exit 1 at **both** base and mock — C3 reports
  "S425/S426 already in the base registry; not a new row". Always-red; the row can never satisfy
  `historical_not_green_at_pin`, i.e. the registered command is self-defeating and `never-met`/`historical`
  labels are unreachable without an entry-command fix.
- **`c59_axis_evidence` — red iff the counter keeps brackets** (mock bk exit 1: `superseded_kept 0`, `scores_held`
  collapses because `--base`==measured). Under `bd`: green at base and mock (0). No round-60-caused red; the
  `## Round 60` SCORECARD section and the mock's claim table do not touch the axis table, superseded cells, or
  scores (10/10/2 held).
- **`c57_idresolver_gate` — already red at base under `bd`** (exit 2: "no sibling registries under the fleet or
  no sibling snapshot"), unchanged by round 60; green 5/5 under `bk` with `--fleet <fleet root>` resolved.
- Not predicted red: `c52_wave_ledger`, `c56_selftally` (pinned selftests, new SKILL row not in its population),
  `c58_receipt_rewrites` (round-60 receipts are first-additions — `events()` skips first `A`; `new_receipts`
  counts only `round-58/controls/after-c{2,3}-*.txt`; verified in code), `c58_resolver_cases`,
  `c59_resolver_cases` (P7 real-lane ids all resolve: S427–S429 registered), `c55_readme_index` stays red
  (googlebot-verification.md is not a round-55-base knowledge file, so no new `head_changed`).
- Pre-existing base reds (not caused by round 60): `c53_gate_truth` (2/7 — stale S329/S312 locator/revision
  checks), `c52_gate_registry` under the generic command (frozen LOG.md pin), all historical rows.

## RELABEL NEEDED:

- **`c59_quote_truth` row → `historical`, pin `97cdc122379711c2b02a8970752c8782da3ac81d`** — verified green
  there (exit 0, 9/9, `bd` log) and an ancestor of any round-60 measured revision. The round-60 gate-registry
  addition table must carry this relabel note (row cell holds a 40-hex pin → e_P=0, e_T=1 → consistent).
  Under the `bk` reading no pin works — flag to the c60 counter author / L1: either drop `--base`/brackets in
  resolution or the row's Entry command needs repair (same for `c59_axis_evidence`, whose `--base <rev>` under
  `bk` is also always-red and unlabelable).
- **`c53_gate_truth` row → `never met`, pin `3994101dba28896830604fd0b08c7f00faca8ed6`** (its own recorded
  measured revision, `real-round52-tip.txt`): verified exit 1 at that pin, at round-53 tip `fd91527a`, and at
  base/mock — never observed green. `historical` is *not* honest (e_P=1 → `historical_not_green_at_pin`).
- **`c57_idresolver_gate` — label defect, resolution-dependent**: under `bd` its live label fails
  `live_not_green` (exit 2 without `--fleet`); fix = make `--fleet` non-optional in the Entry-command cell
  (one complete resolvable command) or relabel `historical` with a pin where it was green — candidate
  `32754df75774dd38e8a96fcda375fc93adf97f1e` (row's own stated round-57 measured revision; green there
  [INFERENCE] — not re-run, its G4/G5 revision pins are inside the counter). Under `bk` no action needed.
- The 12 unregistered members need registry rows (8 non-empty cells, `Verdict map` with `0=`/`1=`), not
  relabels — unchanged by round 60.
- scores_held: mock holds 10/10/2 → round-60 axis-table edits must keep them or C1's own `scores_held` term
  adds a third mismatch (mock verified no-op).

VERDICT: round-60's own changes turn exactly one population counter red — `c59_quote_truth` (C5+C7+C8, unavoidable by design) — which must be relabelled `historical` pinned at `97cdc122379711c2b02a8970752c8782da3ac81d`; pre-existing label debts `c53_gate_truth` (never met @3994101) and `c57_idresolver_gate` (command defect) also stand, and a brackets-kept command reading additionally makes `c59_axis_evidence`/`c59_quote_truth` permanently unlabelable.
