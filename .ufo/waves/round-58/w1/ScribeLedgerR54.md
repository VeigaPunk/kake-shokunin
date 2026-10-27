# ScribeLedgerR54

Claim C1 ledger notes for the five round-54 receipt events. Read-only on the lane: no git mutation, no jj, no product-code edit; nothing written outside this report file and scratch `/fast/scratch/hyaku/kake-r58/ScribeLedgerR54` (removed at exit).

## Counter state observed

Command (as assigned), run from scratch with absolute paths:

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/c58_receipt_rewrites.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 044048597d62f3199494b63b36e90dd57825e350
```

Observed output (first line, verbatim):

`C1 receipt-rewrites events=19 undisclosed=19 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=0 met=False  (met: undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0 AND unpointed == 0 AND new_rewritten == 0 AND new_receipts == 2)` — `EXIT=1`; ledger `.ufo/waves/round-58/receipt-rewrites.json absent (0 entries)`. Lane tip read as `cc8da1674d6e590ae2d05e1f48944ac7939e9ecd`; measured revision `0440485…` resolves.

Kinds below were produced by importing the counter's own `classify(status, old, new)` on the two blobs of each event (`git cat-file -p`), so they are the counter's classification, not my reading. My five note strings were then fed to the counter's `pointed()` (root `.`, tip `0440485…`) and all five return `True`.

## EVENTS:

| path | commit | kind (counter) | what happened | disclosed at the time? |
|---|---|---|---|---|
| `.ufo/waves/round-54/controls/c1-selftest.txt` | `8e408e00fbe1c5908df62ba79e78c944bda479e2` (`round-54: repair S374 calibration and settle r53 ops debt`) | rerun | Same commit rewrote `c54_s374_calib.py` (+62/-… lines) adding cases `correction_wrong_polarity` and `correction_before_render`; the receipt was regenerated and its `ok` lines went 5 → 7 before `EXIT=0`. Not a relabel (no `revision:` line in the file) and not a fill (no `pending`). | Generic only: `LOG.md:2138-2145` "Intermediate drafts were not treated as passing results; both base controls and the final C1 selftest were rerun after repair." No per-file or blob-pair disclosure anywhere. |
| `.ufo/waves/round-54/controls/base-c1-s374.txt` | `a0a4fd482700110600b0327c2fce1a270b272136` (`round-54: bind counters to source and settlement evidence`) | rerun | Counter `c54_s374_calib.py` changed in the same commit; the base receipt was re-run **at the unchanged base revision `68228b2d…`**. Its messages changed: `PASS C1.2_cells` gained `base_render_count=1`, the `FAIL C1.3_correction` text was reworded, the qualifier line gained a trailing period. Verdict lines are unchanged (`mismatches=1 met=False`, `EXIT=1`). | Generic only, same `LOG.md:2138-2145` sentence; the change of message text with unchanged verdicts is not itself disclosed. |
| `.ufo/waves/round-54/controls/base-c2-ops-debt.txt` | `a0a4fd482700110600b0327c2fce1a270b272136` | rerun | Counter `c54_ops_debt.py` (+76 lines) widened cited-name extraction (`cited_names()` now also scans the wave spec and parenthesised `…/w1/*.md` groups, and the manifest regex accepts backticks); re-run at the same base revision moved `uncovered=4 → 7` and added `CriticLocators.md`, `ScoutS312.md`, `ScribeGate.md` to `cited`/`uncovered_names`. This is a real recompute with a changed (more red) result, not a cosmetic edit. | Generic only, same `LOG.md:2138-2145` sentence; the 4 → 7 base-hardening is not called out. |
| `.ufo/waves/round-54/controls/c1-selftest.txt` | `a631cc0246b97f2a949d61186c7466468faf94d6` (`round-54: bind calibration and settlement counters to evidence`) | rerun | Counters changed (+7 lines each) with cases `unrelated_marker` and `correction_removed_render` added; receipt regenerated, `ok` lines 7 → 9, `EXIT=0` — the 9/9 later quoted at `LOG.md:2130` ("final selftest 9/9, exit 0"). | Generic only, `LOG.md:2138-2145`; the 9/9 number is stated at `LOG.md:2130` without saying the receipt file had been rewritten. |
| `.ufo/waves/round-54/controls/sources-census.txt` | `5826682b37811470980b3f263e148dd5292d8026` (`round-54: record measurements, wave findings, and learning`) | rerun (counter) | **Hand annotation, not a re-run.** The only change is the "After" header line, which gained the parenthetical `, measured against lane tip a631cc0246b97f2a949d61186c7466468faf94d6`. The `rows: 155; warnings: 14 W04 …; result \`kake ok\`; EXIT=0` lines are byte-identical to the previous blob (full-blob ids `350215f3…` → `9fadd501…`, diff `@@ -1,7 +1,7 @@` with one `-`/`+` pair). `grep -rn "measured against" scripts/` in the fleet root returns no hit, so the parenthetical is not tool output. | **Not disclosed.** `LOG.md:2155-2156` reads "The census remained 155 rows, 14 W04 warnings, exit 0 before and after (`.ufo/waves/round-54/controls/sources-census.txt`)" and the report cites the receipt at `.ufo/reports/round-54/kake.md:34`; neither mentions the header annotation. |

## NOTES JSON:

```json
[
  {"path": ".ufo/waves/round-54/controls/c1-selftest.txt", "commit": "8e408e00fbe1c5908df62ba79e78c944bda479e2", "note": "Selftest re-run after c54_s374_calib.py gained the correction_wrong_polarity and correction_before_render cases, moving the receipt from 5 to 7 ok lines with EXIT=0; the rerun is stated only generically at LOG.md:2138-2145."},
  {"path": ".ufo/waves/round-54/controls/base-c1-s374.txt", "commit": "a0a4fd482700110600b0327c2fce1a270b272136", "note": "Base control re-run at the unchanged base revision 68228b2d after c54_s374_calib.py reworded its FAIL line and added base_render_count=1 to the PASS line, leaving the verdict lines mismatches=1 met=False unchanged; disclosed generically at LOG.md:2138-2145."},
  {"path": ".ufo/waves/round-54/controls/base-c2-ops-debt.txt", "commit": "a0a4fd482700110600b0327c2fce1a270b272136", "note": "Base control re-run at the unchanged base revision 68228b2d after c54_ops_debt.py widened cited-name extraction to parenthesised and spec-listed names, raising uncovered from 4 to 7 and adding CriticLocators.md, ScoutS312.md and ScribeGate.md; disclosed generically at LOG.md:2138-2145."},
  {"path": ".ufo/waves/round-54/controls/c1-selftest.txt", "commit": "a631cc0246b97f2a949d61186c7466468faf94d6", "note": "Selftest re-run after c54_s374_calib.py gained the unrelated_marker and correction_removed_render cases, moving the receipt from 7 to 9 ok lines with EXIT=0, the 9/9 value quoted at LOG.md:2130; the rerun is stated only generically at LOG.md:2138-2145."},
  {"path": ".ufo/waves/round-54/controls/sources-census.txt", "commit": "5826682b37811470980b3f263e148dd5292d8026", "note": "Only the After header line changed, gaining the hand-written parenthetical 'measured against lane tip a631cc0246b97f2a949d61186c7466468faf94d6' while the rows=155 and EXIT=0 measurement lines stayed byte-identical, so no re-run is evidenced and LOG.md:2155-2156 cites the receipt without disclosing the annotation."}
]
```

Ledger mechanics the integrator must apply: the counter compares `path`, `commit`, `status`, `fromBlob`, `toBlob`, `kind`, `note`; the entries above give only `{path, commit, note}`, so add `status: "M"` and the blob pairs observed (from the counter listing and `git rev-parse`):

- `812bc1caf3d24212e03e89ff2b4801eadba83b19` → `3f66acc2a744bc06653d57dd563bbbba56d5d175`
- `f4cf6d5e334fb437dc3c9c69e8b58db706c78c04` → `661b6bd740b08d42734dd8c1b4bd1b0a21cfe407`
- `559bf9ba22ab5fee698afc3897d0e013feb5aa11` → `67a6902af5d611155cc6d8fdcbdcc94a031ebdc7`
- `3f66acc2a744bc06653d57dd563bbbba56d5d175` → `15d76dc6e17dbcf59e1c7d5a8952e1607d6ddb70`
- `350215f3013cf42528fc098c6906effab1799408` → `9fadd501bfb39591f627165e8e69ad48902d2bd4`

## KIND DISAGREEMENTS:

1. `.ufo/waves/round-54/controls/sources-census.txt` @ `5826682b3781` — counter says **rerun**, WRONG. The event is a hand-inserted provenance clause in the run header; the measured lines are byte-identical, and no tool emits the string (`grep -rn "measured against" /home/vgpnk/Projects/shokunin/scripts/` → no hit). The honest descriptor is "annotation" (nearest enum member would be `format`, which does not apply either, because the text is not whitespace-equal). Because `kind` must equal `classify()`'s output for `wrong_kind` to stay 0, the ledger entry has to carry `rerun`; its `note` above states the truth so the disclosure is not itself misleading. Planner decision needed only if a truthful kind is preferred over `met`.
2. No other disagreement. Events 1 and 4 (`c1-selftest.txt`) are pure line additions, which reads like `append`, but `classify`'s `append` requires the new bytes to *start with* the old bytes and these insert before the trailing `EXIT=0`; since the counter was edited and the selftest genuinely re-run, `rerun` is accurate, not wrong.
3. Not a kind issue but worth recording: three of five events (`base-c1-s374`, `base-c2-ops-debt` ×1 commit, `c1-selftest` ×2) were rewritten **within the same round, after their first commit**, always in the direction of a wider counter at the same base revision. The lane's only contemporaneous statement is the generic sentence at `LOG.md:2138-2145` / `.ufo/reports/round-54/kake.md:11`; no blob pair, per-file list or before/after diff was ever stated. Events 2 and 3 also prove the base receipt was re-measured at `68228b2d…` without a `revision:` bump — the `revision=` line stayed correct, which is exactly why the round-57 revision-line-only counter missed this class.

## Gates and limits

- Ran: the C1 counter at the base revision; `classify()` on all five blob pairs; `pointed()` on all five notes (5/5 True); diff/`--stat`/`log -1` reads for the four commits; `git ls-tree` presence checks for `LOG.md`, `SCORECARD.md`, `.ufo/waves/round-54/c54_s374_calib.py`, `c54_ops_debt.py`, `contract.md`, `controls/base-c1-s374.txt` at `0440485…`.
- Not run (and not claimed): no ledger was written (`.ufo/waves/round-58/receipt-rewrites.json` absent by design at base), so no post-ledger counter run exists — the effect of these notes on `undisclosed`/`unpointed` is [INFERENCE] from `classify`/`pointed` returning the expected values, not from a met run.
- Determinism: single run per command; the counter's output line, blob ids and diff hunks are recorded above verbatim enough to re-derive.
- Out of scope per assignment: the other 14 undisclosed events (rounds 52, 55, 56, 57) and the two `new_receipts` (`after-c2-*`, `after-c3-*`); no product code, counters, lane git/jj state or fleet files touched; no tools installed or updated.

VERDICT: Five round-54 events classified — four are genuine post-commit re-runs of a widened counter (disclosed only by the generic LOG.md:2138-2145 sentence), the fifth (`sources-census.txt` @ `5826682b`) is an undisclosed hand-annotated header line that the counter mislabels `rerun`; five pointer-verified notes supplied.
