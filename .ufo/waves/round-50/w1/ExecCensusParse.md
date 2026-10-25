# ExecCensusParse — round 50, wave 1 leaf seat

Scope: re-derive the registry id list with the census parser's own pattern, compare against the staged ids of `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md`, then re-test with a column-zero-only pattern. Read-only; writes only this report.

## Claim-instrument baselines (run; not reasoned about)

`c50_quote_class.py` at base `9619af67` → `classed 0/3 met=False` (S273, S274, S286: class ledger absent + lesson absent; S286 also lacks retained blob, live registry row, entry).
`c50_quote_class.py` at pre-append `33eec7f2` → `classed 0/3 met=False` (S273, S274: lesson absent only; S286: lesson absent, no live registry row, entry absent). The mirror commit moves S273/S274 to near-pass — only the lesson file is missing — but S286 still lacks the live registry row it needs.
`c50_durable.py` at base `9619af67` → `durable 0/1 met=False` (order proof absent, wave-cite proof absent, LOG.md does not cite the wave, settlement absent).

## Id census — census pattern `^ {0,3}\|[[:space:]]*S[0-9]{3,}`

| set | count | duplicates |
|---|---|---|
| live registry `corpus/SOURCES.md` | 142 | none |
| staged append `SOURCES.append.md` | 121 | none |

Intersection (`comm -12`): **S273, S274** — two collisions. Both are already live rows at `corpus/SOURCES.md:149-150`, and the staged append re-declares them at its lines 30-31 with longer class text. The third declared claim id, S286, exists only in the staged append (its line 43) and has no live row — matching the instrument's "no live registry row" fail at pre-append.

## Column-zero pattern `^\|` retest

Counts: registry 142, staged 121 — identical to the 0–3-space run. Intersection: S273, S274 — identical.

Missed collisions: **none**. The set difference between the two intersections is empty. Reason on this corpus: `grep -cE '^ +\|'` returns 0 for both files — no registry or staged row is indented at all, so the looser pattern has nothing extra to catch. The `^ {0,3}` allowance is dead headroom today; it only matters if a future row arrives indented (e.g. nested inside a list item), which neither file currently contains.

## Freshness-relevant note

S273 and S274 are the freshness frontier ids — they already exist as live rows, so the staged append re-stages them rather than adding them. Whether the re-stage counts as a collision (drop) or a refresh (replace with the longer class text) is an L1 call; mechanically, the registry and the staged file agree on the ids, differ in the row text.
