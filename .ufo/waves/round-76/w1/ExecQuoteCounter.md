# ExecQuoteCounter — delivered C1 counter (round 76, wave w1, attempt 1)

Seat: leaf executor. Scope: harden C1's counter into the delivered instrument under the frozen
contract and amendments 1–7. The lane checkout was read-only throughout; all fixtures were built
under `/fast/scratch/hyaku/kake-r76/ExecQuoteCounter` and removed after the receipts were copied.
No commit, push or tree mutation was made in the lane or the fleet repo. No tool was installed or
upgraded. No model was named or passed to a tool.

**Delivered:** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py`
— sha256 `e7f86d3aa0554f61330179f803fcc7624504b2ee63ea2d3e1a9ee5e3427f59ae`, 49,077 bytes, 1,135 lines.
Stdlib only; reads committed bytes only (`git show`, `git ls-tree -r -z`, one `git cat-file --batch`
per revision); no network, no `/tmp` literal, no write during evaluation; `--selftest` writes only
under `--work`. Interface: `--root`, `--revision`, `--rounds`, `--base` (required for evaluation),
`--json`, `--selftest`, `--work`; exit 0 met, 1 findings, 2 input fault, 64 usage.

`--json` keeps the contract field names `rows, receipt_files, spans_checked, spans_exempted,
corrections, append_only, findings, met` (plus `counter, revision, rounds, base, missing_files`).

## 1. Measured states

All commands below were run with cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`; receipts are under
`.ufo/waves/round-76/w1/ExecQuoteCounter/receipts/`.

### Base (required before-state)

```
$ python3 -B .ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py \
    --root . --revision a0491fcd041cbc3fff2c964ecf6268557e45a5c1 \
    --base a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --rounds 75,76
C1v2 revision=a0491fcd rows=16 receipt_files=7923 spans=25 exempted=0 corrections=0 findings=7 met=false
  T1 SCORECARD.md:4892 files=18 mismatches=0 append_only=true met=true missing_frozen=0
  T1 SCORECARD.md:4892 mismatches=3 classes=E3 append_only=false missing_frozen=1
  T1 SCORECARD.md:4893 population=18 bound=18 mismatches=0 met=true missing_frozen=0
  T1 SCORECARD.md:4893 receipt: source=committed declared_valid=true
  T1 SCORECARD.md:4904 mismatches=0 met=true missing_frozen=0
  T1 corpus/QUALITY.md:1499 files=15 append_only=false met=false
  T1 corpus/lessons/round-75.md:82 files=15 append_only=false met=false
  missing corpus/lessons/round-76.md
exit=1
```

Receipts: `receipts/base-c1-quote-truth-v2.txt` (command + output + exit), `receipts/base-json.txt`.
The plain-output copy requested by the L1 is at `.ufo/waves/round-76/controls/base-c1-quote-truth-v2.txt`
(written at the L1's direction; my seat's default write scope is the `w1/` tree only).

### Repaired tip

```
$ python3 -B .ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py \
    --root . --revision d2555766a1de6a5ccaa4458961e863a4aeccba6f \
    --base a0491fcd041cbc3fff2c964ecf6268557e45a5c1 --rounds 75,76
C1v2 revision=d2555766 rows=23 receipt_files=7925 spans=41 exempted=7 corrections=7 findings=0 met=true
  missing corpus/lessons/round-76.md
exit=0
```

The lane tip now contains the repair commit `442d36c6` (five SCORECARD correction rows, one QUALITY
criterion, one round-75 lesson correction). My counts match `ExecQuoteRepair`'s amended build exactly
(`w1/ExecQuoteRepair.md` Appendix A: `rows=23 … spans=41 exempted=7 corrections=7 findings=0 met=true`).
Receipts: `receipts/tip-after.txt`, `receipts/tip-json.txt`.

### No-repair controls (must stay red)

At the repair parent `f4f076ba`, the freeze commit `b758cb04` and `442d36c6^`, the same command prints
`findings=7 met=false`, exit 1 (`receipts/no-repair-controls.txt`). A green run at those revisions
without the repair rows is not reachable through the receipt universe.

### Selftest and performance

```
$ python3 -B .../doc_quote_truth.py --selftest --work /fast/scratch/hyaku/kake-r76/ExecQuoteCounter/work
selftest: 63/63 passed
exit=0
```

Receipt: `receipts/selftest.txt` (63 cases, every line retained). Wall time, `/usr/bin/time -f 'wall=%e s'`,
three runs each (`receipts/perf.txt`): base `0.90, 0.88, 0.88 s`; two-universe tip `1.66, 1.63, 1.61 s`.
The receipt universe is read with one batch, not one subprocess per file.

## 2. Amendment implementation, one sentence per line

**B1 — revision citations vs digests.** A 7–40 char lowercase hex span is accepted when
`git cat-file -e <tok>^{commit}` resolves at the measured revision; a 41–63 char span is treated as a
digest, and a 64-char span is a digest, so both must be contiguous in a receipt
(`is_revision_citation`, `span_ok`).

**B2 — section identity and no duplicate rows.** Only level-two headings matching
`^Round[ -]?<N>` (SCORECARD), `^Round[- ]?<N>` (QUALITY) and the exact titles
`Mistakes|Gate|Claims|Corrections` (lessons) are sections; a section body ends at the next heading of
level ≤ 2, physical rows are deduplicated by `(file, line)`, and only 0–3 leading spaces start a table
row while 4+ is code (`sections`, `rows_for`, `TABLE_ROW_RE`).

**B3 — correction rows are checked too.** A correction is validated only when it quotes at least one
whole receipt line (exact equality after trimming both ends) and carries no fabricated claim-bearing
span; a fragment quote cannot close, and a correction that fails either test closes nothing
(`whole_line_quote`, `status`, `evaluate`).

**B3-bis — naming vs claiming.** A non-whole-line span on a correction row is allowed only when it is a
`T1`/`T2` span at `--base`; those base defects are computed first (`base_defect_spans`) and only a
validated correction that names the identical string exempts the defective occurrence. Names are
quotations, never new claims, so an invalid correction gets `T4` plus the still-open `T1` but is not
itself flagged for repeating the name.

**B4 — append-only compares exact text.** `row_ids` keys on `(file, exact row text)` with no whitespace
collapsing; a whitespace-only rewrite is `A1` (`row_ids`; selftest `whitespace_rewrite`).

**B5 — ready artifacts are never receipts.** Any basename matching `*.ready*` is excluded, alongside
`*-results.json`, `*-dispatch.json`, `*-spec.json` and `swarm-registry.json` (`ARTIFACT_GLOBS`,
`is_receipt`).

**B6 — the before-state.** The re-measured base is `findings=7` (the `SCORECARD.md:4904` physical row
yields one finding, and `6c10b433`/`ca1a2982` are revision citations); the line above is the receipt.

**Amendment 4 — own diagnostics are never receipts.** Files under
`.ufo/waves/round-76/controls/` whose basename matches `base-c1-quote-truth*.txt` or `ctl-*.txt` are
excluded on every revision (`is_receipt`).

**D1 — receipt directories only.** A receipt is a committed file inside `controls/`, `verification/`,
`resid/`, `receipts/`, `frozen/`, `fixtures/`, `cases/`, `sources/` or `live/` of any round;
data-extension files outside a receipt directory are not receipts (`is_receipt`).

**D2 — diagnostic lines are never evidence.** Each receipt body is stripped of lines matching
`^\s*(T1|T2|T4|A1)\s+\S+:\d+\s` before any matching (`strip_diagnostics`).

**D3 — amendment 4 stands.** The name exclusion runs before the directory rule and is not loosened by
D1 (`is_receipt`, selftest `amendment4_*`).

**D4 — base and target.** The base is `findings=7 met=false`, exit 1; the target is
`findings=0 append_only=true met=true`, exit 0; every measured no-repair control above stays red.

**D5 — the selftest must run.** The fixture helper was written once per case with a distinct
second-commit payload (`_commit_payload`); the suite executes all 63 cases (`selftest: 63/63 passed`,
exit 0), so no case is skipped by an aborted harness.

**F1 — seat-tree exclusion is the newest round only.** `rounds` is sorted; only
`.ufo/waves/round-<rounds[-1]>/w1/` is never a receipt; an older measured round's seat tree is a
receipt source (`is_receipt`).

**F2 — before-state restored.** With F1 the base digest `cbe684a1…` at `corpus/lessons/round-75.md:56`
and `source=uncommitted` at line 103 are receipt-backed again, so the base reads `findings=7`.

## 3. Selftest coverage (63 cases, all green)

Every finding id is exercised red and green: `T1` (`t1_absent`, `t1_noncontiguous`, `t1_ratio`,
`t1_hex_absent_noncommit`, `t1_seat_prose_results_json`, `ready_marker`, `single_letter_assignment`,
`t1_pipe_span`, `t1_newline_escape`, `indented_row`), `T2` (`t2_elision_bad`, `t2_elision_split_files`)
and green elisions; `T4` and its green counterpart; `A1` (`a1_deleted_row`, `whitespace_rewrite`) and
`append_only_green`. Also covered: the four receipt-universe closures (seat tree, data-extension outside
a directory, `*.ready*`, `*-results.json`), the diagnostic-line strip, the amendment-4 name exclusion,
indented rows at 3 vs 4 spaces, `## Round 7` prefix rejection, level-three heading rejection, duplicate
valid corrections, the whole-line closure, the partial-line/fabricated-span attacks, and the input-fault
and usage exits.

Reviewer-1 held-outs named by the L1, mapped to cases:

| Held-out | Case | Expected |
|---|---|---|
| `single_letter_assignment` (`x=9`) | `single_letter_assignment` | `T1`, exit 1 |
| `correction_extra_false_claim` | `correction_extra_false_claim` | `T1` ×2, `corrections=0` |
| `correction_partial_line` | `correction_partial_line` | `T1` + `T4`, 2 findings |
| `commit_without_receipt` | `commit_without_receipt_B1_citation` | green (B1 citation) |
| `ready_marker` | `ready_marker` | `T1`, `receipt_files=1` |
| `whitespace_rewrite` | `whitespace_rewrite` | `A1`, `append_only=false` |
| `wrong_heading_level` | `wrong_heading_level` | green, `rows` excludes it |
| `disjoint_canonical` | `disjoint_canonical_whole_line_closes` | green, `corrections=1`, `spans_exempted=1` |
| `indented_row` | `indented_row` / `indented_code_row_excluded` | `T1` at 3 spaces; excluded at 4 |
| `round7_prefix` | `round7_prefix` | green, `rows` excludes it |
| `duplicate_correction` | `duplicate_correction` | green, `corrections=2` |

Additional Reviewer-1 cases retained: `unrelated_round`, `seat_prose` via
`amendment7_closed_seat_prose_excluded`, `dispatcher_prose` via `t1_seat_prose_results_json`,
`elision_split`, `different_span` via `correction_names_other_span`, `nonreceipt_correction` via
`correction_quotes_seat_prose`, `fabricated_digest` via `digest_64_requires_receipt`, `pipe_span`,
`newline_escape`.

## 4. Decisions and divergences the L1 should ratify

1. **`findings=8` → `findings=7`.** My seat text demanded reproduction of the v1 receipt's
   `findings=8`. Amendments 3 §B6, 4 and 7 F2 supersede that number; the delivered base is `7`. The
   v1 eight were: the `SCORECARD.md:4904` row counted twice (one physical row under two overlapping
   headings) and six real non-contiguous spans, while `6c10b433`/`ca1a2982` are revision citations
   under B1. Receipt: `receipts/base-c1-quote-truth-v2.txt`.

2. **D1 vs F1/F2 needs one explicit ruling.** Literal D1 (exclude every measured round's seat tree)
   produced `findings=9` at base, because the only base copies of
   `cbe684a1…` (`corpus/lessons/round-75.md:56`) and `source=uncommitted` (line 103) are under
   `.ufo/waves/round-75/w1/` (`receipts/f1-span-locations.txt`,
   `receipts/universe-literal-d1-run.txt`, `receipts/universe-notes.txt`). Amendment 7 F1 scopes the
   exclusion to `rounds[-1]`, and F2 pins the base at 7. To satisfy both, the delivered rule treats a
   **closed** round's seat tree as a receipt source for its receipt-directory files **and its
   data-extension files** (the digest's only copy is
   `.ufo/waves/round-75/w1/ScoutSources/fetch-intoto.txt`, outside every receipt directory), while
   never admitting that round's prose/scripts. This is the one place the implementation goes beyond a
   literal sentence of D1; if the L1 prefers strict D1, the base becomes 9 and F2 must be amended.

3. **B3-bis on invalid corrections.** I read a base-defect name on a correction row as a quotation,
   not a fabricated claim, so `correction_partial_line` yields `T1` (the unclosed defect) + `T4`
   (no whole-line quote) and does not additionally flag the repeated name. If the L1 intends names to
   be `T1` on a non-validated correction, that is a one-line change in the fabricated-span test; the
   frozen controls do not exercise the distinction.

4. **`spans_checked` includes correction-row spans.** At the repaired tip it is 41, matching the
   repaired build's own tally; the contract fixes the field name, not this counting rule. `rows`,
   `spans_exempted`, `corrections`, `append_only`, `findings` and `met` are unaffected.

5. **Input-fault hardening beyond v1.** Unresolved `--revision`/`--base`, a non-work-tree `--root`,
   a `--root` that is not the work-tree toplevel, and missing required `SCORECARD.md` /
   `corpus/QUALITY.md` now exit 2 (v1 silently measured an empty population and could return
   `met=true`). No frozen control changes state because of this.

6. **No-repair tip.** The lane tip `d2555766` already carries the repair commit `442d36c6`, so the
   no-repair control is measured at `442d36c6^` / `f4f076ba` / `b758cb04`; all are red with
   `findings=7`.

## 5. Risks and limits

- Whole-line quotes are textual after trimming, not semantic; B3 defines nothing stronger.
- Correction closure is by exact span string: one validated correction naming a defect closes every
  occurrence of that identical string in the population (span identity, per B3-bis).
- D2 strips whole receipt lines; a legitimate observation line that happens to begin with the
  diagnostic prefix is dropped by design.
- Only committed bytes are visible; uncommitted working-tree receipts cannot launder or rescue a span.
- A closed round's seat data files are receipt sources by the F1/F2 reconciliation above; its `.md`
  and `.py` files are not.
- An internal crash (not an input fault) exits 1 with a traceback rather than a contract code; the
  contract defines no internal-error exit.

## 6. Files written

- `.ufo/waves/round-76/w1/ExecQuoteCounter/doc_quote_truth.py` (delivered tool).
- `.ufo/waves/round-76/w1/ExecQuoteCounter.md` (this report).
- `.ufo/waves/round-76/w1/ExecQuoteCounter/receipts/`: `base-c1-quote-truth-v2.txt`, `base-json.txt`,
  `tip-after.txt`, `tip-json.txt`, `no-repair-controls.txt`, `selftest.txt`, `perf.txt`, `sha256.txt`,
  `tool.txt`, `f1-span-locations.txt`, `universe-literal-d1-run.txt`, `universe-notes.txt`.
- `.ufo/waves/round-76/controls/base-c1-quote-truth-v2.txt` (plain-output copy requested by the L1;
  this path is outside my default write scope, written on explicit instruction).

Scratch `/fast/scratch/hyaku/kake-r76/ExecQuoteCounter` was removed after the receipts were copied.
No other file was created or modified.

Report: .ufo/waves/round-76/w1/ExecQuoteCounter.md
