# Mutation — swap the S262/S263 `used-by` cells (C2 counter)

Seat: `L1Kake51.MutationSwapIds-2` (mutation-tester, wave 1, round 51).
Claim attacked: **C2** (freshness, assimilated entries), predicate `met: conditions_passed == 8 of 8`,
counter `.ufo/waves/round-51/c51_quote_truth.py`.
Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`, measured tip
`9d13768c4fdd0e9a2688d2ecf1616b539cf57658`.

## Mutant

Smallest behaviour-bearing point: the `used-by` cell (cell 11, `row[10]`) of the two adopted registry
rows in `corpus/SOURCES.md`. The two cells were **swapped**, nothing else changed:

| id | used-by pristine | used-by mutant |
|---|---|---|
| S262 | `corpus/knowledge/canonical-selection.md` | `corpus/knowledge/crawler-identity.md` |
| S263 | `corpus/knowledge/crawler-identity.md` | `corpus/knowledge/canonical-selection.md` |

Scratch (never the lane): `git clone --shared /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/mut51-swapids`
(clone HEAD equal to the lane tip, and its `corpus/SOURCES.md` sha256 already equal to the lane's
`4ea81a5a…`). The mutation was committed in the scratch clone as
`777bafc715a3f65d2bce7bc5398ef7d08e0de456`, so the counter's `git show <rev>:<path>` reads mutated
bytes. Diff scope confirmed to exactly two lines:

```
-| S262 | … | corpus/knowledge/canonical-selection.md |
-| S263 | … | corpus/knowledge/crawler-identity.md |
+| S262 | … | corpus/knowledge/crawler-identity.md |
+| S263 | … | corpus/knowledge/canonical-selection.md |
 corpus/SOURCES.md | 4 ++--   (2 insertions, 2 deletions)
```

Byte hashes of the measured file: pristine `4ea81a5ae79029cbb7ec424a51ec1d31e06650f5072d8c58cea878f558449fe3`,
mutant `4f20521d3859c80542def8240511f6ce278e2b5121184ac728848519b57c4769`.

## Detector runs (same command, three byte-states)

Counting command, unchanged:
`python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-51/c51_quote_truth.py --root <root> --revision <rev>`

| state | root / revision | stdout headline | exit |
|---|---|---|---|
| pristine | lane / `9d13768c…` | `C2 quote-truth 8/8 met=True` | 0 |
| **mutant** | `/tmp/mut51-swapids` / `777bafc715…` | `C2 quote-truth 7/8 met=False` | **1** |
| restored | `/tmp/mut51-swapids` / `848e53f3c5…` (revert of the mutant) | `C2 quote-truth 8/8 met=True` | 0 |

The counter never opened a worktree file of the measured revision; every read was
`git show`/`git log` against the `--root`/`--revision` pair, so the pristine run is a valid baseline
and the mutant run differs only by the two committed cells.

## Which condition fails, and its note

**`C4_used_by`** — the only failing condition (7 of 8 passed). Actual notes printed by the counter:

```
  C4_used_by FAIL
    - S262: used-by is ['corpus/knowledge/crawler-identity.md'], expected exactly ['corpus/knowledge/canonical-selection.md']
    - S263: used-by is ['corpus/knowledge/canonical-selection.md'], expected exactly ['corpus/knowledge/crawler-identity.md']
```

`--json` on the mutant revision confirms the machine record: `conditions_passed: 7`, `met: false`,
and every other check `true` with empty notes —
`C1_entries_exist`, `C2_entry_cites_id`, `C3_row_shape`, `C5_gate_quote_truth`,
`C6_receipt_pins`, `C7_validate_before_append`, `C8_append_after_mirror`.

Verdict: **killed**. The mutant is rejected by the frozen predicate (7/8 → `met=False`, exit 1).
Because C3 still passes, the swapped rows remain well formed (11 cells, status `mined`, opened
`2026-10-24`, recheck `180d`); C4's exact-list comparison `used_by != [path]` is the sole gate that
pins each row's `used-by` to its own admitted entry, and it fires on both ids. C5–C8 are indifferent
to cell 11 by construction, so no second condition corroborates the kill — that is the mutation's
coverage boundary, not a defect in the claim.

## Restoration evidence

- No lane bytes were ever mutated: the swap was applied and committed only inside `/tmp/mut51-swapids`.
- Lane `git rev-parse HEAD` before and after the probe: `9d13768c4fdd0e9a2688d2ecf1616b539cf57658` (unchanged).
- Lane `git status --porcelain corpus/SOURCES.md`: empty (clean).
- Lane worktree `sha256sum corpus/SOURCES.md` = `4ea81a5a…`, identical to
  `git show 9d13768c…:corpus/SOURCES.md | sha256sum` = `4ea81a5a…`.
- Detector integrity: lane `.ufo/waves/round-51/c51_quote_truth.py` sha256
  `29a899a0345d36b457e8381e0f611b00cda920f741d3e52cbf3ba88df156f99f`, identical to its blob at
  `9d13768c…` — the counter was not edited for the probe.
- Scratch restored to the pristine bytes by `git revert` (`848e53f3c5…`), file sha256 back to
  `4ea81a5a…`, and the re-run returned to 8/8 exit 0, so the detector's 7/8 is attributable to the
  mutation alone. The scratch clone under `/tmp/mut51-swapids` is disposable and left in place for
  auditability only; nothing under the lane references it.
- Only file written in the lane: this report.

## Tooling

No installs or upgrades. Python 3 and git from the host were sufficient; no pacman, `uv tool`,
`npx` or binary fetch was performed.
