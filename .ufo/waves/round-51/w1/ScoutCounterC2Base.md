# ScoutCounterC2Base — C2 do-nothing control at the base revision

Seat: `L1Kake51.ScoutCounterC2Base-2` (scout, leaf). Axis: freshness.
Question: at the frozen base revision, does the C2 counter score 0/8 for the right reasons, and is
that score evidence that the counter is a real oracle rather than a constant?

## 1. Command run and exact result

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/c51_quote_truth.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 007d66e4e8360a5f88d29a93eeedd8066dad4434
```

Full stdout (verbatim):

```
C2 quote-truth 0/8 met=False  (met: conditions_passed == 8 of 8)
  C1_entries_exist FAIL
    - S262: knowledge entry corpus/knowledge/canonical-selection.md absent at the measured revision
    - S263: knowledge entry corpus/knowledge/crawler-identity.md absent at the measured revision
  C2_entry_cites_id FAIL
    - S262: entry absent
    - S263: entry absent
  C3_row_shape FAIL
    - S262: no registry row at the measured revision
    - S263: no registry row at the measured revision
  C4_used_by FAIL
    - S262: no usable registry row
    - S263: no usable registry row
  C5_gate_quote_truth FAIL
    - S262: retained body .ufo/waves/round-51/sources/S262.html absent
    - S263: retained body .ufo/waves/round-51/sources/S263.html absent
  C6_receipt_pins FAIL
    - S262: no receipt in .ufo/waves/round-51/sources/receipts.json
    - S263: no receipt in .ufo/waves/round-51/sources/receipts.json
  C7_validate_before_append FAIL
    - pre-append census receipt is incomplete
  C8_append_after_mirror FAIL
    - no commit adds the pre-append mirror
  revision: 007d66e4e8360a5f88d29a93eeedd8066dad4434
```

**Exit code: 1.** (`--json` form agrees: `conditions_passed 0`, `met False`, and all eight flags
`False`.)

Run twice, byte-identical output, exit 1 both times (`cmp` clean) — deterministic.

## 2. Which conditions fail

All eight, i.e. **8 of 8 fail, 0 pass**:

| condition | verdict | base ground truth (independently checked) |
|---|---|---|
| C1 entries exist | FAIL | `corpus/knowledge/canonical-selection.md` and `crawler-identity.md` are ABSENT at base (`git cat-file -e`) |
| C2 entry cites id | FAIL | follows from C1 (no entry to cite) |
| C3 row shape | FAIL | rows `S262`/`S263` are absent inside the `## Registry` table at base |
| C4 used-by | FAIL | follows from C3 |
| C5 gate quote truth | FAIL | `.ufo/waves/round-51/sources/S262.html`, `S263.html` absent; `corpus/lessons/round-51.md` absent |
| C6 receipt pins | FAIL | `.ufo/waves/round-51/sources/receipts.json` absent |
| C7 validate before append | FAIL | no `assimilation/pre-append/census-{argv,stdout,exit}.txt` at base |
| C8 append after mirror | FAIL | no commit up to base adds `.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` |

This is exactly the C2 `before` field in `contract.json` ("0 of 8 at the base 007d66e (neither
entry, neither row, no retained source, no pre-append mirror)") and exactly the C2
`doNothingControl` prediction ("the base revision 007d66e scores 0 of 8").

## 3. Is the control non-vacuous? (the part that matters)

The base score alone proves nothing — a stub could print 0/8. I measured the other pole myself and
audited how the counter reaches its verdicts.

- **Tip pole measured by me**: `--revision 9d13768c4fdd0e9a2688d2ecf1616b539cf57658` prints
  `C2 quote-truth 8/8 met=True`, exit **0** (C7 and C8 both `pass`). So the counter is neither
  constant-false (base 0/8) nor constant-true (it distinguishes the two revisions by content).
- **Revision-pinned, worktree-blind**: the script contains no `open(`, `Path(`, `read_text`,
  `os.path` or `glob`; every read is `git show <rev>:<path>` plus `git log`/`merge-base`. Untracked
  worktree artifacts (`.ufo/waves/round-51/w1/`, `route-map.json`, …) therefore cannot leak into a
  measurement. Verified by grep: no filesystem-read call sites.
- **Same oracle at both poles**: `.ufo/waves/round-51/` does not exist at the base revision at all
  (`git ls-tree` count 0), including the counter itself. The base control therefore necessarily runs
  the current counter. That is acceptable here only because the counter bytes are identical across
  worktree, HEAD and tip (`git diff HEAD -- <script>` and `git diff <tip> -- <script>` both empty) —
  i.e. the oracle was not rewritten between the two measurements.
- **"No registry row" is a row absence, not a parse failure**: `corpus/SOURCES.md` is PRESENT at base
  with a `## Registry` heading at line 5 and 143 data rows (145 table lines with header and
  separator), and `parse_registry` accepts the same `^ {0,3}\|` shape those rows use. My independent
  grep for `^\s{0,3}\|\s*S26[23]` finds nothing at base and finds both rows at tip (lines 152–153).
  The registry's ids at base run up to a numeric max of `S286` (the only ids in the 250–299 range are
  `S273`, `S274`, `S286`), so the missing ids are interior gaps in an existing id space, not rows cut
  off the end of the table.
- **No duplicate-id collision for the two adopted ids**: at base, the strings `S262`/`S263` appear
  nowhere in `corpus/` or `.ufo/waves/` except the reserved pools
  `.ufo/waves/round-49/assimilation/staged-ids` and `.ufo/waves/round-50/assimilation/staged-ids`
  (those files are a contiguous reserved block `S250`–`S370`). So S262/S263 were reserved ids being
  consumed, not ids that had already been minted elsewhere.
- **Robustness caveat on the predicate, not a base-result defect**: C1–C4 are `passed = not notes`
  over the fixed two-key `ADOPTED` dict, so they are non-vacuous only because `ADOPTED` is non-empty
  (it has exactly 2 keys, read from the source). An empty `ADOPTED` would make C1–C4 and C5–C6 pass
  vacuously. Observed as a property of the instrument; it does not affect either measured pole.

## 4. Freshness findings that survive the control (evidence from committed bytes at the tip)

The judged axis is freshness, so I checked whether the tip's "re-grounded this round" claim rests on
this round's bytes rather than recycled ones. All read-only from `git show <tip>:<path>`:

- Retained body digests: `S262.html` = `792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b`,
  `S263.html` = `6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de` — these equal the
  `sha256` values in `sources/receipts.json`.
- Sizes agree: `wc -c` gives 174926 and 175561, matching `bytes`/`declaredBytes` and the Gate line
  annotations.
- **Not recycled**: I hashed all 43 retained `.html` bodies that exist at the base revision; neither
  digest appears among them.
- The `docRevision` values in the receipts are present inside the retained bodies themselves
  (`Last updated 2026-08-20 UTC` for S262, `Last updated 2026-02-03 UTC` for S263), so the receipt's
  revision pin is byte-backed, not asserted.
- Rows at tip read `status=mined opened=2026-10-24 recheck=180d used-by=<the one entry>` for both
  ids; the opened date is the round date, and the fetch timestamp is
  `2026-10-24T23:16:49-03:00`.
- **Limitation, stated as such**: S263's source document was last updated 2026-02-03, ~9 months
  before the fetch. The freshness claim is therefore about the *fetch and pin*, not about the
  underlying doc's recency; that is consistent with the declared 180d recheck cadence but should not
  be read as "the Googlebot page is new".

## 5. Remaining unknowns / out of scope for this seat

- C7 and C8 are process conditions; at base they fail because every receipt and the mirror are
  absent by definition, so the base control cannot distinguish "process skipped" from "process
  artifact not yet created". Only the tip pole discriminates those, and it passes there — measured by
  me, not inherited.
- C1 (wave-evidence ledger) is `0/3` at the tip per the dispatch's measured state; I did not re-run
  it (not this seat's question, and the dispatch states the L1 writes that evidence after the wave
  settles).
- Not in my lane, deliberately unexamined here: quote-class completeness inside the two entries
  ("each entry marks the class of every other quote it carries"), append-only proof for the
  `SOURCES.md` diff, and entry prose quality. Sibling seats own those.

## 6. Tooling

No installs, no upgrades, no pacman/uv/npm/cargo transactions. Read-only git only (`show`,
`ls-tree`, `cat-file`, `grep`, `log`, `merge-base`, `diff --stat`, `rev-parse`); scratch output in
`/tmp/c2base.{1,2}.txt`. The only file written in the lane is this report.
