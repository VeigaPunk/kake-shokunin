# Round 98 — ReviewCapB (C1 row-review conjunct)

Scope: judge every row the C1 repair (4446ce219b4f0c9f5f4fc81f7f772e3a7f24c95a) added, renamed or moved in
SCORECARD.md `## Capabilities` (40 rows in the first table: 39 added + 1 renamed; 5 moved to
`### Capability rows without an admitted closure`) = 45 rows. Fleet record: MANIFEST.json at
f86740064229897f53212e03ae3b6474dac66de4. Base e51328b6. Read-only throughout; no lane or fleet file was
modified (outputs only in w1/ReviewCapB/ and this report). No subagents. No tools installed.

## Counter (step 4)

Command: `cd <scratch> && python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-98/c98_captable.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 4446ce219b4f0c9f5f4fc81f7f772e3a7f24c95a --fleet-revision f86740064229897f53212e03ae3b6474dac66de4` → rc=0

Line 1:
`entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true revision=4446ce219b4f0c9f5f4fc81f7f772e3a7f24c95a fleet-revision=f86740064229897f53212e03ae3b6474dac66de4`

Copy in `w1/ReviewCapB/c98_captable.stdout.txt`.

## Row verdicts

`w1/ReviewCapB/verdicts.tsv`: 45 lines, `<round>\t<capability>\t<agree|disagree>\t<reason>`.
Tally: agree 43, disagree 2.

Checks applied per row: (1) closure record in the pinned MANIFEST (kake, lane_round = round, admitted, verdict,
capabilities_added); for moved rows, admitted is false; (2) the "what it can now do" cell against the named
script's docstring/code and the closure spot-check lesson; (3) every evidence path against the 4446 tree
(`git cat-file -e`, round-prefixed where the cell gives a round-relative path); (4) for moved and renamed rows,
cell identity with the base row.

Evidence-path result: every path named in the 40 first-table rows exists at 4446ce21. Every moved-row path
resolves at 4446ce21 once round-relative fragments are prefixed with `.ufo/waves/round-<R>/` (the one
non-path token, `18/18`, is a count). Renamed row 195: what/evidence/round cells byte-identical to base.
Moved rows 34, 35, 61, 64: row text byte-identical to base. Moved row 37: NOT identical (see F1).

## Disagree (lands C1 unmet if they stand)

D1. Row 215 `selftest-tally-counter`: "Re-runs every registered instrument selftest". The counter's
population is the frozen POP list of 10 entries (`.ufo/waves/round-56/c56_selftally.py`; docstring: "ten rows of
the SKILL.md gate registry whose self-test cell states how many fixtures"). SKILL.md has about 100 gate rows
(`grep -c '^| .* | gate'` = 100). Scope overclaim.

D2. Row 218 `id_resolver.py`: "reporting dangling, ambiguous and resolved ids". `scripts/id_resolver.py`
contains zero occurrences of "ambiguous" (`grep -ci` = 0). Output is DANGLING lines plus
`ids_cited ids_resolved dangling owned_elsewhere unowned` (lines 505-513). The fence, non-ASCII and quoted-path
claims are supported; the "ambiguous" category is not.

Both are wording-level overclaims on otherwise-supported rows. Per the frozen rules I did not rewrite any row.

## Routed findings (not verdict flips)

F1. Moved row 37 (`Offline robots.txt expectation audit`) was edited, not just moved. The table note at
SCORECARD.md:246-249 says "Row text is unchanged; the closure verdict is the added first cell"; that is false for
this row. Base cell: "selftest 131/131 (`verification/robots-selftest-at-9dbc88bb-tool.json`) ... at most 20 for
the controls that skip rules". Moved cell: "at most 4 for the do-nothing, junk, constant, all-false and no-reader
controls, 20 for the stock `urllib.robotparser` and at most 24 for the 34 listed reference ablations ... 127/134 on
that control, 134/134 on the tool". The new numbers trace to the lane's round-37 record (SCORECARD.md ~1846, 1981,
2030, 2061, 2109-2113) and to receipts that exist (`verification/postfix/robots-selftest-134-on-*.json`; the
shortcut receipt has failed=7, i.e. 127/134). The accuracy of the moved cell is therefore agreed; the provenance
note is wrong. The repair should say the row was re-worded, or restore the base text.

F2. Receipt-pin record conflict. SKILL.md:1284 records receipt-pin-counter as red at its round-57 measured revision
32754df7 (new_receipts=0, scorecard_pin=0). `corpus/lessons/round-57-verifier-spotcheck.md` reports
`after-c1-receipt-pins.txt` at 32754df7 as `met=True`. Row 219 quotes the SKILL.md record and is consistent with
it; the two lane records disagree and should be reconciled.

F3. Row 234 (capture-once chain) evidence names header_audit.py, the round-81 manifest and the lesson, but not
`scripts/response_snapshot.py` (the GET-only capturer, present) or `.ufo/waves/round-81/c81_capture_audit.py` (the
re-derivation counter, present). Under-citation; the capability claim is supported. "Bytes under an allowlist"
refers to the manifest-level host allowlist, not to a byte filter in the capturer. The wording could be tightened.

F4. Row 213 describes only the unnamed-file half of the coverage-map counter (the counter also counts dangling
rows). Under-description; no verdict change.

## Verification gaps

- Did not re-run the per-instrument counters or selftests (not assigned). Judgments rest on committed receipts,
  the lane's spot-check lessons, the MANIFEST closure records, and reading the named scripts' docstrings and the
  specific code lines cited above.
- Rows 205, 228, 232, 236, 237 are judged from docstrings and closure text, not from line-by-line code audit.
- The round-57 receipts (F2) were not re-derived; the conflict is recorded, not resolved.
- The counter checks the first table only (as built); the moved table is judged here by hand.

## Verdict

REVIEW-CAP rows=45 agree=43 disagree=2 counter_exit=0
