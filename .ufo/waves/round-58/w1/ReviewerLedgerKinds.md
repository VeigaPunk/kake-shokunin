# ReviewerLedgerKinds

C1 classifier review (before data): 19 base events enumerated with `events()` imported from
`.ufo/waves/round-58/c58_receipt_rewrites.py` at tip `044048597d62f3199494b63b36e90dd57825e350`
(lane `/home/vgpnk/Projects/shokunin/kake-shokunin`). Per event: `_text()` of from/to blobs,
`classify(status, old, new)` result, and `git diff <fromBlob> <toBlob>` (same syntax as the
counter's own keying). Event count matches the claim's base 19 undisclosed events.

## TABLE:

| # | path | commit | auto kind | diff summary | verdict |
|---|------|--------|-----------|--------------|---------|
| 0 | .ufo/waves/round-52/control/c1-mutation-ladder.json | 1ae8de5 | relabel | 36 changed lines, all `"old_tail": "  revision: <hex>",` re-pinned; same length 4945 B; no result lines | OK |
| 1 | .ufo/waves/round-52/control/c1-ledger-real.txt | a4a890c | relabel | 1 line pair `revision: <hex>` re-pinned; rest identical | OK |
| 2 | .ufo/waves/round-52/control/c1-mutation-ladder.json | a4a890c | relabel | same 36-pin pattern, length-preserving | OK |
| 3 | .ufo/waves/round-52/control/c2-quote-real.txt | a4a890c | relabel | 1 line pair `revision: <hex>` re-pinned | OK |
| 4 | .ufo/waves/round-52/control/c2-quote-selftest.txt | a4a890c | relabel | 1 line pair: `18/18` constant, `fixture revision <hex>` pin changes | OK |
| 5 | .ufo/waves/round-52/control/c1-mutation-ladder.json | fd91527 | relabel | same 36-pin pattern | OK |
| 6 | .ufo/waves/round-54/controls/c1-selftest.txt | 8e408e0 | rerun | 2 result lines inserted mid-file (not tail; `startswith=False`): `ok correction_wrong_polarity: exit 1 (met=False) expected 1`, `ok correction_before_render ...`; no pins | OK |
| 7 | .ufo/waves/round-54/controls/base-c1-s374.txt | a0a4fd4 | rerun | 6 changed lines: PASS/FAIL messages and counts updated (`suspect_cells=1` -> `+base_render_count=1`, FAIL rewording); one line relocated identically; no pins | OK |
| 8 | .ufo/waves/round-54/controls/base-c2-ops-debt.txt | a0a4fd4 | rerun | 8 changed lines: `uncovered=4 -> 7`, `cited`/`uncovered_names` lists extended, one relocated identical line; no pins | OK |
| 9 | .ufo/waves/round-54/controls/c1-selftest.txt | a631cc0 | rerun | 2 result lines inserted mid-file: `ok unrelated_marker ...`, `ok correction_removed_render ...` | OK |
| 10 | .ufo/waves/round-54/controls/sources-census.txt | 5826682 | rerun | 1 line pair: After-header gains `measured against lane tip <hex>`; `-` side is pinless so relabel gate can't fire; no numeric rows changed (rows/warnings identical) | MISCLASSIFIED (true relabel) |
| 11 | .ufo/waves/round-55/controls/c1-selftest-v2.txt | 64c0ce1 | rerun | 1 line pair: `32/32 -> 44/44`; no pins; re-run tally change | OK |
| 12 | .ufo/waves/round-55/controls/after-c1-readme-index.txt | 955e3d7 | relabel | 1 line pair `revision: <hex>` re-pinned | OK |
| 13 | .ufo/waves/round-55/controls/after-c2-quote-truth.txt | 955e3d7 | relabel | 1 line pair `revision: <hex>` re-pinned | OK |
| 14 | .ufo/waves/round-55/controls/c2-selftest.txt | 955e3d7 | relabel | 1 line pair: `54/54` constant, `fixture revision <hex>` pin changes | OK |
| 15 | .ufo/waves/round-56/controls/after-c1-selftally.txt | ad06cb8 | relabel | 1 line pair `revision: <hex>` re-pinned | OK |
| 16 | .ufo/waves/round-56/controls/after-c2-quote-truth.txt | ad06cb8 | relabel | 1 line pair `revision: <hex>` re-pinned | OK |
| 17 | .ufo/waves/round-56/controls/c2-selftest.txt | ad06cb8 | relabel | 1 line pair: pin `f8438a282d59` IDENTICAL on both sides, score `67/67 -> 86/86`; line passes relabel only via the word "revision" | MISCLASSIFIED (true rerun) |
| 18 | .ufo/waves/round-57/controls/after-c1-receipt-pins.txt | 20217f2 | fill | `pending` placeholder replaced by full receipt (68 -> 430 B, `len(new)>len(old)`, old contains "pending") incl. `tip: <hex>` | OK |

17/19 events correctly auto-classified. No base event was classified `append`; the ladder-JSON
rewrites (0/2/5) are interior pin replacements, not prefix-preserving appends, so `append` never
legitimately applies to them (the `new.startswith(old)` test would only fire for tail-appends).

## MISCLASSIFIED:

1. **[17] round-56/controls/c2-selftest.txt @ ad06cb8 — auto `relabel`, true `rerun` (high severity).**
   `git diff f96bb110a3d31dcc42ada9139ca321e803f10b42 1cfd5667817ebafb4deda77ef7ae24cd1fc6415f`:
   only one line pair changes, and it is a RESULT line: `c56 quote-truth selftest: 67/67
   (fixture revision f8438a282d59)` -> `... 86/86 (fixture revision f8438a282d59)`. The pin is
   unchanged; the score changed. The classifier returns `relabel` solely because the line text
   contains the word "revision". This is exactly the false-green trap: a genuine re-run result
   change would be silently masked as relabel, and the ledger would bless it as a label-only edit.

2. **[10] round-54/controls/sources-census.txt @ 5826682 — auto `rerun`, true `relabel` (low/medium severity).**
   `git diff 350215f3013cf42528fc098c6906effab1799408 9fadd501bfb39591f627165e8e69ad48902d2bd4`:
   one line pair, both `Before`/`After` header lines: `After (round-end run): ...` ->
   `After (round-end run, measured against lane tip <hex>): ...`. No measurement rows changed
   (155 rows / 14 warnings identical). This is a provenance-pin annotation, not a re-run with
   different output, so `rerun` mislabels it. The relabel rule cannot fire because the removed
   line carries no pin, so "every changed line carries a pin" is unsatisfiable for pin-adding edits.

## RULE FIXES:

Replace the relabel block in `classify` (currently `if changed and all(REVLINE_RE.search(l) ...)`
-> `return "relabel"`) with a residue-invariance check: a pure relabel must survive masking every
40-hex id — the removed and added lines must then be identical as multisets. Add a module-level
`PIN_RE = re.compile(r"\b[0-9a-f]{40}\b")`.

```python
    import difflib
    hunk = [(l[0], l[1:]) for l in difflib.unified_diff(
        old.splitlines(), new.splitlines(), lineterm="", n=0)
        if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    if hunk and all(REVLINE_RE.search(t) for s, t in hunk if t.strip()):
        del_l = sorted(PIN_RE.sub("<HEX>", t) for s, t in hunk if s == "-")
        add_l = sorted(PIN_RE.sub("<HEX>", t) for s, t in hunk if s == "+")
        if del_l == add_l:
            return "relabel"
        # Optional looser branch for pin-annotation edits (issue 10): a single
        # added line that is the removed line with a pin-bearing annotation added.
        if len(del_l) == 1 and len(add_l) == 1 and del_l[0] in add_l[0]:
            raw_add = [t for s, t in hunk if s == "+"]
            if len(raw_add) == 1 and PIN_RE.search(raw_add[0]):
                return "relabel"
```

Verification against the 19 events:
- [17]: masked removed `67/67` residue != masked added `86/86` residue -> multiset equality fails;
  substring branch also fails (`...67/67...` not in `...86/86...`) -> falls through to `rerun`. FIXED.
- [10]: multiset equality fails (extra words), but removed line is a substring of the added line
  and the added line carries a real pin -> `relabel`. FIXED.
- [0][1][2][3][4][5][12][13][14][15][16]: masked residues equal -> still `relabel`. UNCHANGED.
- [6][7][8][9][11]: changed lines pinless -> outer gate fails -> `rerun` (correct).
- [18]: `pending` line pinless -> gate fails -> `fill` (correct; length gate unchanged).

Optional hardening (no base-event impact): `append` is structurally unsound for JSON receipts
(re-serialization never keeps old bytes as a prefix); no base event hits it, so no change is
required — if desired, guard `append` to non-`.json` paths.
VERDICT: 17/19 base events auto-classified correctly; 2 misclassifications found — [17] relabel masks a real rerun score change (high severity, fixed by pin-residue equality), [10] rerun mislabels a pin-annotation edit (fixed by optional substring branch); exact rule fixes provided above.
