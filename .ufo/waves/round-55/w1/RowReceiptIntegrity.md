# RowReceiptIntegrity

Claim C1 — coverage-map calibration for `knowledge/receipt-integrity.md`. Read in full:
`corpus/knowledge/receipt-integrity.md` (124 lines) and `corpus/README.md` header + `## Coverage map`
(`:15-45`, header row `| Area | Entry | Coverage |` at `:17`). The README carries no existing row for
this file (`grep -n receipt-integrity corpus/README.md` → no match, exit 1), so exactly one new row is
drafted. No file was edited; only this report was written.

ROW:

```markdown
| Receipt integrity (round 45) | `knowledge/receipt-integrity.md` (S133) | Three receipt defect classes (counter-error, tool-absent, stale planted), the v2 binding rule's exit, note, counter-sha, mtime-window and seed gates plus a toolSha256 control binding, do-nothing reachability, 27-control and fixture counts, two named residual limits |
```

Format checks (all run): 3 cells, no `|` inside any cell; Area = 4 words (≤ 8) carrying the round tag
from the file's own header (`verified-at: 2026-10-24 (kake round 45)`, `:2`); Entry = backticked
`knowledge/receipt-integrity.md` followed by `(S133)`, an id copied from the file's own `source:` line
(`:1`); Coverage = 34 words (10-45), does not start with `TBD`, and shares the 5+-letter word
`receipt` with the H1 (`:5`).

EVIDENCE:

- `corpus/knowledge/receipt-integrity.md:12` — "## Three defect classes, each reachable in the round-44 instrument" (10 units). Anchors "Three receipt defect classes".
- `:56-61` — the five bulleted gates; passages: "- **exit gate** — counter exit in `{0, 1}`; anything else is class `counter_error`;" (14 units) and "- **run window** — receipt `st_mtime_ns` inside `[started_ns − 1 s, finish_ns + 1 s]`" (15 units). Anchors the exit / note / counter-sha / mtime-window / seed gate list; "toolSha256 control binding" rests on ":94" — "the toolSha256 binding closes the receipt→control leg" (7 units), which the on-disk predicate also implements (`c45_audit.py:83-84`, `expected_tool_sha` clause).
- `:110-113` — "- 27 controls in the round-44 claim cohort —" (9 units) and "- 4 invalid/stale fixture classes plus 1 honest control — `ls .ufo/waves/round-45/fixtures` →" (13 units). Anchors "27-control and fixture counts"; read-only re-check matched: `ls .ufo/waves/round-44/verification/claim/after-final/tools/ | wc -l` → 27, `ls .ufo/waves/round-45/fixtures` → `counter-error honest stale-backdate stale-planted tool-absent`.
- `:76` and `:92` — "The cheapest control that skips the claimed work is exactly these three receipt shapes: never run the" (17 units); "limits stay open after the wave-2 repairs, and both are named rather than closed: the" (15 units). Anchors "do-nothing reachability" and "two named residual limits".

Every quoted passage was verified as a raw substring with python `in` against the retained file bytes
(all True) and its unit count computed as one unit per CJK character / one per non-CJK whitespace
token; all are ≤ 25 units. Quotes use ASCII double quotes only; no CJK occurs in this file, so every
unit count equals its token count.

RISKS:

- **The row cannot claim provenance is proven.** The file's own named residual limit says the run
  window plus self-reported shas "cannot prove causal provenance" (`:94-96`) and that the manifest
  nonce "the frozen counter never echoes" (`:104-106`); the row therefore says "named residual limits",
  not "closed".
- **"27-control" is cohort-scoped, not a current round number.** The 27 is the round-44 claim cohort
  (`:110-111`); the row deliberately does not imply a round-55 measurement. The counts will go stale
  with any counter/driver/receipt-format change — the file's own `recheck:` line (`:3`) names
  `c45_matrix.py --stage before|after` as the trigger.
- **Digest and line-pointer drift in the entry itself (noticed, not edited).** `:51` gives the driver
  digest truncated as `f3c3171b658abccd…0a076` "at landing", so it cannot be matched to current bytes:
  HEAD `dc7f03e` `.ufo/waves/round-45/c45_audit.py` is sha256
  `9b824d958d1494471f45ad84d6ae38ce600518311b1fb95af51b1098aac8a400`. The same entry cites
  `build_build_row()` at `:131-146` and `_selftest_cohort` at `:223` onward, while current bytes place
  them at `:132` and `:235`; `receipt_validity()` still starts at `:68`, matching. The entry describes
  the landing version and does not say a later round-45 revision exists, so its pointers are not
  re-verifiable against HEAD without naming the version.
- **Source id scope.** S133 grounds only the `Popen.returncode` exit-status semantics (`:41-46`); it
  does not ground the three defect classes, the gate list or the counts. The Entry cell copies it
  because the file's `source:` line names it first, but a reader should not read `(S133)` as covering
  the whole entry.
- **Domain-fit caveat.** The file is instrument-integrity material (a verification driver's receipt
  gate), not a web-property fact; the row states what the file holds and makes no domain-surface claim.
- **Unrun:** `python3 -B .ufo/waves/round-45/c45_matrix.py --stage before|after` and the shipped
  `--selftest` were NOT executed in this seat (they write cohort receipts, outside a scribe's write
  scope); their exit-0 status is reported only as the file's own recorded claim (`:2`).
- **Also noticed, unresolved:** two receipts named `after-v5.json` exist with different verdicts
  (`:117` → `22 1 4`, `ok=False`; `:118-119` → `26 1 0`, `ok=True`); the file flags this itself
  (`:121-124`), so the row avoids any "27/27 witnessed" phrasing.

VERDICT: One traceable coverage-map row drafted for `knowledge/receipt-integrity.md` (Area 4 words, Entry `knowledge/receipt-integrity.md` (S133), Coverage 34 words, all passages verified as raw substrings ≤ 25 units); no file edited, residual-limit and digest-drift caveats reported.
