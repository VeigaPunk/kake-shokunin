# ExecC3Derive

## CHANGES:
- Added `ExecC3Derive.files/derive_c60_quote_truth.py`; it derives `ExecC3Derive.files/c60_quote_truth.py` from the round-59 v2 counter at base `97cdc122379711c2b02a8970752c8782da3ac81d`. Derivation `sub()` asserts each source replacement is unique; all three retained HTML files are checked against round-60 receipt SHA-256s.
- Retargeted rows/entries and C1–C4: S427/S428/S429 rows; only S428/S429 entries; staged `google-robots-txt-limits.md` absent; exact used-by sets and URLs; S427 supersession and scope precision. Added L1 T1's regex rejection for scope overclaim.
- C5: page title and body pins; page-unique 6–25-unit / <=160-character quote checks; S427/S428/S429 topics; footer-scoped `Last updated` limited to text nodes inside the footer and excluding template/script/style; positional nearest preceding article h1/h2/h3 heading for the subject-bearing Gate quote. S429's Search Central title, article marker, and footer form are handled.
- C6: receipt sha256, bytes, HTTP status, UTC access date, `round60` user-agent, URL and effective URL; `receipts.json` pinned to blob `b9b56713713523ed9bec1c769313fd9cb0d52e6d` (content SHA-256 `7367683d99aada9fa1b66fd76fbd5cf88d0fa3d65b8dd055fcd84ce587ae42ec`).
- C7: consumes `.ufo/waves/round-60/controls/validate-append.txt`, validates the base, census command/target, exit, E-codes, appended and final row counts, admitted missing used-by targets, and receipt-add commit as a strict ancestor of the earliest S427 registry commit.
- C8: uses the pinned 164-row mirror and checks strict ancestry plus append-only registry reconstruction.
- C9: checks append-only preservation of the base S426 sentence, the six-base-line window, one insertion run at a block boundary, and a single rendered-prose line containing the correction tag, S428, the exact stale wording, and a qualifying S428 quote carrying `generally ignore`. Fenced code, comments, inline code, and tag attributes are excluded from prose searches.
- Incorporated L1 2026-10-27 amendments T1–T8. The selftest includes red/green controls for each tightening, including heading-position, fence, receipt pin/effective URL, C7 ancestry, footer scope, and C9 line/run placement.

## SELFTEST:
`c60_quote_truth.py --selftest`: **140/140**; baseline fixture exit 0 with 9/9; 129 fixtures (125 red, 4 green). Ran with `TMPDIR=/fast/scratch/hyaku/kake-r60/ExecC3Derive`. No installed or updated tools.

## BASE RUN:
At `97cdc122379711c2b02a8970752c8782da3ac81d`: **0/9**, predicate false, **EXIT=1** (expected). The failures reflect the absent round-60 rows, entries, retained sources/receipts, validation receipt, mirror, and correction at the base revision.

## CONTRACT AMBIGUITIES:
No unresolved ambiguity after the L1 rulings. The C9 window is interpreted as insertion positions `s < i1 <= s + 7` (six following base lines); the added T3 ruling further requires a single insertion run at a block boundary. The T2 ruling requires the `was` wording and qualifying `now` quote on the same tagged/citing line.