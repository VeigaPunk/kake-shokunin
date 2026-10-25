# CriticOpenedDate — opened cell is the access date, not the campaign date

**Seat:** CriticOpenedDate (critic)
**Axes:** operability, freshness
**Attack:** both new registry rows must have opened `2026-10-24`. Copying the campaign opened date `2026-10-23` would fail C2 R1.

No production file was edited. The campaign-date probe was an in-memory rewrite of `git show` bytes and was not written back.

## What "both new rows" are

Registry ids at pre-append `99fa9d3fcaafbdb6bb1a2518c21e27698199b4c9`: 140.
Registry ids at scoring tip `1c846ed2d67b1692ea966be064f0fc04542763c6`: 142.
Added: `S273`, `S274`. Removed: none. No already-held row changed its opened cell.

`git merge-base --is-ancestor 1c846ed2d67b1692ea966be064f0fc04542763c6 HEAD` exited 0. `git rev-parse HEAD` is that same hash. `git status --porcelain -- corpus/SOURCES.md` printed nothing, so the worktree registry is not a second opened date.

## Committed opened cells

Parsed with the same rule as `c49_quote_truth.py` `registry_rows` (`git show <rev>:corpus/SOURCES.md`, `## Registry` only, opened = cell index 7 after the id). `git show` exit 0, blob 133241 bytes.

| id | line | status | opened | recheck | R1 |
|---|---|---|---|---|---|
| S273 | 149 | mined | 2026-10-24 | 180d | PASS |
| S274 | 150 | mined | 2026-10-24 | 180d | PASS |

A full-line split agrees: opened is field 9 (`| id | … | status | opened | recheck | used-by |`), and that field is `2026-10-24`, not `2026-10-23`.

R1 at that revision (`c49_quote_truth.py:13` and `:42`) is equality with the literal `OPENED = "2026-10-24"`. A mismatch appends `opened=<cell>` (`:156-157`) and the id fails.

## Campaign date, and why it would fail R1

Campaign rows, read-only, `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md`:

- line 30, S273, status `mined`, opened `2026-10-23`
- line 31, S274, status `mined`, opened `2026-10-23`

Those are the dates the lesson calls the campaign opened dates (`corpus/lessons/round-49.md:12`). They were not copied into the landed opened cells.

In-memory only: the two committed opened cells were replaced with `2026-10-23` and re-parsed. Result:

- S273 mutated_opened `2026-10-23` → R1 FAIL `opened=2026-10-23`
- S274 mutated_opened `2026-10-23` → R1 FAIL `opened=2026-10-23`

That mutation was not applied to the tree. A campaign date on either new row would drop that id, so C2 could not stay at 2/2.

## Verdict

Confirmed. Both new rows opened `2026-10-24`. The campaign date `2026-10-23` is still the opened cell in the campaign append file, and it is not the opened cell in the committed registry. R1 holds on the landed rows and would fail if the campaign date had been copied.

Freshness: the opened cell is the round access date named in the lesson, not the campaign day. Operability: R1 is a literal equality check, so the wrong day is a hard fail, not prose.

**Not a defect on this attack.** Receipt `accessed` fields are also `2026-10-24`, but R1 does not read them; the registry opened cell is the check. Local calendar at the read was `2026-10-24` (`date +%Y-%m-%d`); UTC was already `2026-10-25T00:37:22Z`. R1 pins the literal `2026-10-24`, not UTC now.

Report: .ufo/waves/round-49/w1/CriticOpenedDate.md
