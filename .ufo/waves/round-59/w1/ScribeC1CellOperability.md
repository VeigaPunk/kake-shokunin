# ScribeC1CellOperability

Claim C1, operability row (score cell 10, unchanged). Surface read: `SCORECARD.md` lines 14-17 (axis table) and the
`## Round 41/46/47/48/49/50/51/52/54/57/58` sections at base fd6303ce5c14b3f892dec586297a942ab6e4193b, plus
`.ufo/waves/round-59/c59_axis_evidence.py` (v1, pointer/receipt/tally rules) and `/home/vgpnk/Projects/shokunin/AXES.md`
("SCORECARD entries match observed repo state"). All repo paths below are relative to the lane toplevel.

## CELL

```text
Operability now rests on committed instruments, not the round-12 and round-17 live-execution narrative this cell used to carry: the cross-registry source-id resolver `scripts/id_resolver.py` and its differential gate, whose round-58 after-receipt `.ufo/waves/round-58/controls/after-c2-resolver-cases.txt` records 14/14 met over the fence, non-ASCII path, git-quoted path and newline-path cases, against 6/14 in that round's red-before receipt `.ufo/waves/round-58/controls/base-c2-resolver-cases-v2.txt`, and whose round-57 receipts `.ufo/waves/round-57/controls/after-c2-idresolver.txt` (gate 5/5) and `.ufo/waves/round-57/controls/tool-selftest-final.txt` (tool selftest 49/49) carry that round's capability entry; the counters themselves are committed at `.ufo/waves/round-58/c58_resolver_cases.py` and `.ufo/waves/round-57/c57_idresolver_gate.py`. The 10 is a legacy rating (round 12 and round 17 by this row's history, round 17 and round 18 by this file's preamble) with no re-derivation in this round: the cell claims the instruments exist, pass a differential gate and are receipted at those rounds, not that the score was re-measured.
```

1143 characters, zero `|` characters, no bare `/tmp`, `~` or `/home` token. Same text in
`.ufo/waves/round-59/w1/ScribeC1CellOperability.files/cell.txt`.

## POINTERS

Every backticked token resolved at the base revision (`git -C <lane> cat-file -e fd6303ce:<path>`); both cited receipt
rounds are on-axis (their `## Round N` section carries a table row naming operability).

| pointer | exists | role |
|---|---|---|
| `scripts/id_resolver.py` | yes (1026 lines at base) | the tool the row is about |
| `.ufo/waves/round-58/controls/after-c2-resolver-cases.txt` | yes | round-58 after-receipt (operability) |
| `.ufo/waves/round-58/controls/base-c2-resolver-cases-v2.txt` | yes | round-58 red-before receipt (operability) |
| `.ufo/waves/round-57/controls/after-c2-idresolver.txt` | yes | round-57 after-receipt (operability) |
| `.ufo/waves/round-57/controls/tool-selftest-final.txt` | yes | round-57 tool selftest receipt |
| `.ufo/waves/round-58/c58_resolver_cases.py` | yes | the counter that produced the 14/14 |
| `.ufo/waves/round-57/c57_idresolver_gate.py` | yes | the counter that produced the 5/5 |

On-axis evidence: round 57's section row `| \`scripts/id_resolver.py\` lists cited \`S###\` ids the lane registry lacks and
names the sibling owner | operability (capability acquisition) |`; round 58's row `| \`scripts/id_resolver.py\` fence-aware
registry and revision-mode NUL path reading eliminate the round-57 fence and git-quoted-path false greens | operability |`.

## TALLIES

Each `A/B` in the cell occurs verbatim in a blob the same cell cites (`git show <rev>:<path> | grep -n`).

| tally | file | grep line |
|---|---|---|
| 14/14 | `.ufo/waves/round-58/controls/after-c2-resolver-cases.txt` | line 1: `C2 resolver-cases 14/14 met=True  (met: cases_passed == 14 of 14)` |
| 6/14 | `.ufo/waves/round-58/controls/base-c2-resolver-cases-v2.txt` | line 1: `C2 resolver-cases 6/14 met=False  (met: cases_passed == 14 of 14)` |
| 5/5 | `.ufo/waves/round-57/controls/after-c2-idresolver.txt` | line 1: `C2 id-resolver 5/5 met=True  (met: gate_conditions_passed == 5 of 5)` |
| 49/49 | `.ufo/waves/round-57/controls/tool-selftest-final.txt` | line 1: `selftest: 49/49` (also line 4 of the same round's after-receipt: `- selftest: 49/49`) |

No other `A/B` shape occurs in the cell.

## COUNTER ROW DETAIL

Method: `git clone -q --shared` into my scratch dir, `checkout -q fd6303ce…` (measured lineage on the contract base;
`SCORECARD.md` is byte-identical at base and at lane tip cb68527, `git diff --stat` empty), replaced the operability
row's third cell, appended the old cell verbatim under `## Superseded axis-table evidence` at EOF, committed as
`dfc6006694863cf382a258fea797ccaece548524` (selftest identity) and ran
`python3 -B .ufo/waves/round-59/c59_axis_evidence.py --root <scratch>/c --revision HEAD --json` → **exit 1** (expected:
the other two rows are untouched at base).

Operability row, after my replacement: 7 pointers, 0 unresolved (each `"ok"`); tallies 14/14 found, 6/14 found, 5/5
found, 49/49 found; no `off_axis` entries; row contributes 0 to `rows_no_receipt` and 0 to `rows_no_tally`.

Aggregate at HEAD `dfc6006`: rows=3, row_names=[operability, freshness, calibration], names_ok=true, unresolved=7,
rows_no_receipt=2, receipts_off_axis=0, tallies_unfound=0, rows_no_tally=1, mismatches=10, scores_held=2,
superseded_kept=1, met=false, exit 1. The 7 unresolved and the 2/1 row counters all belong to the untouched rows:
freshness (7 unresolved pointers = six `/tmp/kake-r17/...` receipts plus `corpus/claims`) and calibration (zero pointers, so
`rows_no_receipt` + `rows_no_tally`).

Base run for the before-state (`--revision fd6303ce --base fd6303ce`, same tree): mismatches=16, unresolved=11,
rows_no_receipt=3, rows_no_tally=2, superseded_kept=0, exit 1; the operability row alone held 4 unresolved
(`cli.mjs:935`, `:836-839`, `:932`, `:393`) + no receipt + no tally = 6 of those 16. My replacement clears exactly
those 6 (16 → 10), nothing else.

`superseded_kept` is 1, not 3, in my run — because the block I appended carries only the operability base cell.
The field counts base cells found in the text outside the axis-table span (header line through last row), so one
superseded block holding all three base cells yields 3 whether or not the rows are replaced; row replacement is
what clears `unresolved` / `rows_no_receipt` / `rows_no_tally`. The single-block case was measured by the
`ScribeC1Superseded` seat (base text plus its `> `-prefixed block, table untouched: superseded_kept 0→3, every
other field unchanged); I did not run it, and I earlier predicted it wrongly as 1. Reaching `met` still needs the
freshness and calibration rows replaced, since their mismatches come from the rows themselves.

Receipts copied to `.ufo/waves/round-59/w1/ScribeC1CellOperability.files/`: `cell.txt`, `old_cell.txt`,
`counter.json` (JSON run above), `base.txt`, `scratch-diff.patch` (the SCORECARD hunk). `old_cell.txt` holds the
raw third cell as it sat between pipes — 1058 characters / 1062 UTF-8 bytes, i.e. the stripped 1056-character /
1060-byte cell plus one padding space at each end; the copy actually appended to the scratch SCORECARD was the
stripped form (the counter counted it, superseded_kept 1, and `old_cell.txt.strip() == base stripped cell`).
My new `cell.txt` is pure ASCII, so its 1143 characters are also 1143 bytes.

## HONESTY NOTES

- The cell does not claim the score 10 is measured. It says the 10 is legacy and states what the evidence does support:
  that a committed tool exists, passes a differential gate at round 58 and a gate at round 57, and that those runs are
  receipted. No score movement is proposed.
- The evidence is instrument-level (case matrix, gate, tool selftest), not a re-execution of "every free-read verb" the
  old cell asserted. That older assertion is not reproducible here: `cli.mjs` does not exist at base (the counter reports
  `cli.mjs:935` as "not a committed path at the revision") and the six `/tmp/kake-r17/...` files are gone.
- Counter limit, from its own docstring: it does not test whether a cited receipt *supports* the score, nor whether a
  stated tally is the receipt's own result — only that the `A/B` string occurs somewhere in a cited blob. My four tallies
  are each the receipt's headline verdict line (line 1 of four different receipts, one of them repeated at line 4), but
  that correspondence is my reading, not the counter's check.
- Provenance of the legacy rating is stated two ways in the cell because the lane says it two ways: the assignment and the
  row history give round 12 and round 17; `SCORECARD.md`'s preamble calls the numeric ratings "legacy round-17/18
  assessments". I did not try to settle which is right.
- Per the assignment I changed the third cell only. The fourth cell still reads "12" while the row now cites round-57/58
  receipts — an inconsistency I left in place for the integrator (a "last change" of 12 would understate the row's
  evidence turnover).
- Unrun, therefore unclaimed: whether the round-57/58 runs themselves happened (I read receipts, I did not re-run those
  counters or the resolver — no after-state of any claim is scored here, per the wave rule); whether the retained receipts
  are the values git shows (receipt-pin checking is another claim's surface); whether the resolver is correct beyond the
  14 cases its counter encodes.
- Known-by-design gaps in the cited instruments are not restated in the cell (round-58 discloses that P6 trusts a printed
  selftest tally, so a zero-test stub can print 59/59): the cell cites receipts, it does not certify the tools are
  unspoofable.
- No tool installs, no pacman, no host service touched. No lane mutation: I wrote only this report and my
  `.files/` directory; all git mutation happened in `/fast/scratch/hyaku/kake-r59/ScribeC1CellOperability/`, which is
  deleted after copying the receipts.

VERDICT: operability evidence cell replaced with 7/7 committed pointers and 4/4 receipt-backed tallies — the row's 6 base mismatches drop to 0 (aggregate 16 → 10); `met` still needs the freshness and calibration rows plus the other two superseded cells.
