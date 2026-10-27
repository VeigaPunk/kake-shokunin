# ExecC1Selftest

## Scope and version drift (read first)

Deliverable: `.ufo/waves/round-59/w1/ExecC1Selftest.files/c59_axis_evidence.py` = the **frozen contract counter**
(`git show 45a92b64:.ufo/waves/round-59/c59_axis_evidence.py`, sha256 `95d23511…`, the `counterSha256v1` in contract.json)
with `selftest()` replaced by a 27-case fixture kill matrix. Pristine copy kept as `c59_axis_evidence_v1_frozen.py`.

Version drift observed while working: the lane counter at `.ufo/waves/round-59/c59_axis_evidence.py` is no longer the
frozen v1. It is an **uncommitted worktree rewrite** (v2; now 515 lines, sha256 `6df31e5f…`, L1-written selftest at 24/24).
I snapshotted it as `c59_axis_evidence_v2_landed.py` and gated it behind `KAKE_C1_SELFTEST_V2=1`; an earlier 377-line v2
(`1d04f19d…`) existed mid-wave and is what my v2 expectations were calibrated on. Facts for the L1:
contract.json still declares `counterSha256v1 = 95d23511…`; the file that will be measured is not that file — the C1
receipt must state which counter (and hash) produced the measured number.

## CASES

27 cases, each: scratch git repo (base commit + measured commit, `-c user.name=selftest -c user.email=selftest@local`),
`measure()` called directly, counters asserted, and one named mutant that the case must kill (mutant = patched source, or
an attribute override on the loaded module; patches are applied to the counter part only, never to `selftest()`).
"expectation" is the frozen-v1 docstring semantics (pointer/receipt/tally atoms).

| # | case | expectation (v1) | result | mutant it kills |
|---|------|------------------|--------|-----------------|
| 1 | base_shape_real | mismatches 16 = unresolved 11 + rows_no_receipt 3 + rows_no_tally 2; rows 3; scores_held 2; superseded_kept 0; met False — reproduces the contract base control exactly | PASS | `resolve` always ok (unresolved counted) |
| 2 | clean_minimal_true | mismatches 0, rows 3, scores_held 2, superseded_kept 3, met True | PASS | `HELD=()` (scores_held must be 2) |
| 3 | emptied_evidence_cells | rows_no_receipt 3, rows_no_tally 3, mismatches 6 | PASS | `pointers` phantom |
| 4 | tmp_pointer | unresolved 1 (absolute), tallies_unfound 1, rows_no_tally 1, mismatches 4 | PASS | absolute path made repo-relative |
| 5 | home_pointer | same shape as 4 for `~/x.md` | PASS | `~` stripped |
| 6 | absolute_home_pointer | same shape as 4 for `/home/u/x.md` | PASS | `/home/u/` stripped |
| 7 | bare_name_not_at_root | unresolved 1 (`notes.md` only under `docs/`), mismatches 4 | PASS | basename fallback to `docs/` |
| 8 | file_line_beyond_eof | unresolved 1 ("line beyond the file"), mismatches 4 | PASS | line-bound check dropped |
| 9 | line_continuation_after_unresolved | unresolved 2 (failed pointer + its `:12`), mismatches 5 | PASS | `last_file` not reset on failure |
| 10 | brace_expansion | unresolved 0 (two expanded pointers resolve), mismatches 3 | PASS | `expand` no-op |
| 11 | tree_pointer | tree resolves (unresolved 0) but is not a receipt: rows_no_receipt 1, mismatches 3 | PASS | tree treated as blob |
| 12 | off_axis_receipt | receipts_off_axis 1, rows_no_receipt 1, mismatches 2 | PASS | `on_axis` always True |
| 13 | tally_absent_from_cited_blob | tallies_unfound 1, rows_no_tally 1, mismatches 2 | PASS | `TALLY` never matches |
| 14 | tally_only_in_uncited_file | v1: tally found in a cited non-receipt blob → mismatches 0, met True (see defect D4) | PASS | bodies switched to receipts |
| 15 | score_change_on_operability | scores_held 1, met False (score moved) | PASS | score compare forced True |
| 16 | removed_calibration_row | rows 2, names_ok False, scores_held 2, superseded_kept 3 | PASS | `names_ok` forced True |
| 17 | reordered_rows | rows 3, names_ok False, mismatches 0 | PASS | order-insensitive `names_ok` |
| 18 | superseded_cell_missing | superseded_kept 2 | PASS | containment check forced True |
| 19 | superseded_cell_altered_one_byte | superseded_kept 2 (not verbatim) | PASS | 10-char prefix match |
| 20 | superseded_kept_only_inside_table | superseded_kept 0, met False (cell only inside the table) | PASS | `outside` = whole text |
| 21 | pipe_inside_code_span | cell truncated at the pipe: rows_no_receipt 2, rows_no_tally 2, mismatches 4 (see defect D1) | PASS | code-span-aware row split |
| 22 | duplicated_header_first_table_wins | first table wins: rows 3, names_ok True, met True | PASS | last header wins |
| 23 | crlf_line_endings | identical to the LF twin (met True) | PASS | `strip(" ")` instead of `strip()` |
| 24 | symlinked_receipt | symlink resolves as blob, receipt counted, tally NOT found (mismatches 2; see defect D2) | PASS | symlink (mode 120000) rejected |
| 25 | receipt_of_measured_round | v1 accepts a round-59 receipt (measured sections) → met True (v1 gap D5) | PASS | `on_axis` forced False |
| 26 | base_without_axis_table | `RuntimeError: base revision has no axis table` (CLI exit 2, not a silent miss) | PASS | raise replaced by `base_rows = rows` |
| 27 | row_with_fewer_than_four_cells | short row charged rows_no_receipt 1 + rows_no_tally 1 (mismatches 2) | PASS | short-row charge removed |

## TALLY

```
python3 -B .ufo/waves/round-59/w1/ExecC1Selftest.files/c59_axis_evidence.py --selftest
TALLY cases=27 passed=27 failed=0 mutants_killed=27      exit=0
```
Run under `KAKE_C1_SELFTEST_TMP=/fast/scratch/hyaku/kake-r59/ExecC1Selftest` (fixtures removed on exit).
With `KAKE_C1_SELFTEST_V2=1` the same matrix runs against the landed v2 snapshot and **does not hold**: v2 renames
`names_ok`→`axes_ordered`, adds `rows_no_passing_receipt`, and on my clean fixture reports `rows_no_receipt 3`
(measured `clean_minimal_true`: mismatches 12 instead of 0) while the mutant for that case still dies. So the matrix is
evidence for the frozen v1 semantics only; the landed v2 has its own 24/24 selftest and my fixtures would need
re-basing to it (not done: L1 asked for a stop). No after-state is scored here.

## COUNTER DEFECTS FOUND (frozen v1; D4/D5 are fixed in the landed v2)

- **D1 pipe inside a code span truncates the evidence cell.** `cells = line.strip().strip("|").split("|")` splits on every
  pipe, including one inside a backticked path: the cell becomes "`docs/a.md" (no closing backtick), so pointer and tally
  silently vanish and the row is charged a no-tally mismatch. Fix: split on pipes outside code spans (mutant 21 shows the
  corrected result: unresolved 0, tallies_unfound 1, mismatches 5).
- **D2 a symlinked receipt always fails its tally.** Git stores a symlink as a blob (mode 120000) whose content is the
  target path, so `cat-file -t` says "blob" and the receipt resolves, but `show()` returns "docs/real.md" and no tally can
  ever be found in it (case 24: guaranteed false `tallies_unfound`). Fix: refuse symlink receipts (ls-tree mode 120000) or
  dereference the target blob before scanning.
- **D3 `superseded_kept` is a substring test over the whole outside text** (`bc[2] in outside`): a base cell that is a
  prefix of a longer, different cell counts as "kept"; conversely an unchanged cell that lives only inside the axis table
  can never be kept (case 20 → `superseded_kept 0`), so `met` is unreachable unless old cells are duplicated outside the
  table. Fix: compare cell-to-cell with boundaries (or exact cell strings from a parsed table) and count a byte-identical
  measured cell as kept.
- **D4 (fixed in v2) a tally is satisfied by any resolved blob of the cell**, not only by the cited on-axis receipt: in
  case 14 a tally that occurs only in a cited non-receipt file makes the claim `met True` with `tallies_unfound 0`.
  v2 searches receipts only.
- **D5 (fixed in v2) receipts and on-axis rounds are read from the measured SCORECARD**, so the measured revision can
  self-attest its own round (case 25: a round-59 receipt is accepted; any pipe row mentioning the axis anywhere in a
  `## Round N` section makes it on-axis). v2 uses base-revision sections kept verbatim and requires an axis-column table.
- Observation (not a defect): one broken pointer chain is charged once per failed `:LINE` continuation (base shape:
  `cli.mjs:935` + 3 continuations = 4 of the 11 unresolved), and a short row is charged both `rows_no_receipt` and
  `rows_no_tally` — both inflate `mismatches` for a single defect.

## DIFF

`git diff --no-index -U0 c59_axis_evidence_v1_frozen.py c59_axis_evidence.py` → **592 insertions, 2 deletions, one hunk**
(`@@ -260,2 +260,592 @@ def selftest()`): the stub body is replaced by the matrix, everything else in the counter is
byte-identical to the frozen v1. Full diff saved at
`.ufo/waves/round-59/w1/ExecC1Selftest.files/c59_axis_evidence.selftest.diff` (601 lines).

```
-    print("c59 axis-evidence selftest: version 1 stub (wave 1 writes the fixture kill matrix); exit 2")
-    return 2
+    """C1 axis-evidence kill matrix: fixture cases over the counter, each case paired with a mutant it must kill.
...
```

Files written (only my own paths): `.ufo/waves/round-59/w1/ExecC1Selftest.md`,
`.ufo/waves/round-59/w1/ExecC1Selftest.files/{c59_axis_evidence.py, c59_axis_evidence_v1_frozen.py,
c59_axis_evidence_v2_landed.py (515-line v2 snapshot, sha256 6df31e5f…, reference only), c59_axis_evidence.selftest.diff}`.
No lane git/index/jj mutation; no pacman; scratch dir deleted.

VERDICT: 27/27 fixture cases pass and 27/27 targeted mutants are killed on the frozen v1 counter; five v1 defects
documented (D1 pipe-in-code-span, D2 symlink receipt, D3 substring superseded test, D4/D5 fixed by the landed v2).
