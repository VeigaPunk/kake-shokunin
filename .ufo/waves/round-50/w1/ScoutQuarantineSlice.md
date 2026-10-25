# Scout quarantine slice — kake lane, round 50 wave 1

Read-only re-derivation of the lane's quarantine slice from
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.
No cited source was fetched. Nothing was appended anywhere. Scratch only; the
report file itself is the sole write.

## Filter

```
awk -F'|' -v l='kake' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'
```

Run verbatim against the register. `wc -l` on its output: **12 rows**.

## Rows (id → class cell, verbatim)

Nine rows carry the backticked class `` `payload-absent` `` in cell 5:

| id | round cell | class cell |
|---|---|---|
| S142 | round1 | `payload-absent` |
| S143 | round1 | `payload-absent` |
| S148 | round1 | `payload-absent` |
| S156 | round2 | `payload-absent` |
| S161 | round3 | `payload-absent` |
| S193 | round6 | `payload-absent` |
| S194 | round6 | `payload-absent` |
| S195 | round6 | `payload-absent` |
| S206 | round7 | `payload-absent` |

Three rows have a malformed cell layout: cell 4 holds the id **plus a stray
trailing backtick** (`S154\``, `S178\``, `S184\``), and cell 5 carries no class
token at all — it holds the free-text note `the cited source could not be
fetched, so no quote was checked`. By the register's own class table, that note
is the `unreachable` condition (source never fetched → quote never checked →
not a fabrication candidate), but the class cell is absent rather than
`` `unreachable` ``:

| id (as printed) | round cell | class cell (verbatim) |
|---|---|---|
| S154` | round2 | `the cited source could not be fetched, so no quote was checked` |
| S178` | round4 | `the cited source could not be fetched, so no quote was checked` |
| S184` | round5 | `the cited source could not be fetched, so no quote was checked` |

These sit at register lines 319–321, after the totals block; line 242
(`` | `kake` | 9 | ``) is a per-lane count row the filter rejects — consistent
with exactly nine `payload-absent` rows being counted for kake.

## Live-registry presence check

Registry: `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`
(143 unique `S\d+` ids present).

`grep -c "| <id> |"` for each of the 12 slice ids → **0 for every id**.
Cross-check with read-only git: `git grep -nE '\| (S142|…|S206) \|' HEAD --
corpus/SOURCES.md` → 0 matches.

**None of the 12 quarantine-slice ids is present in the lane's live registry.**

## Relation to the frozen round-50 claims (context only, no action taken)

- C1 declared ids are S273, S274, S286 — none overlaps this quarantine slice.
- `c50_quote_class.py` at base `9619af67`: `classed 0/3 met=False` (all three:
  class ledger absent, lesson absent; S286 additionally: retained blob absent,
  no live registry row, entry absent).
- `c50_quote_class.py` at pre-append `33eec7f2`: `classed 0/3 met=False`
  (S273/S274/S286: lesson absent; S286 also: no live registry row, entry
  absent — the mirror commit added the class ledger but not lessons/registry).
- `c50_durable.py` at base `9619af67`: `durable 0/1 met=False` (order proof
  absent, wave-cite proof absent, LOG.md does not cite the wave, settlement
  absent).

Report: .ufo/waves/round-50/w1/ScoutQuarantineSlice.md
