# ScribeGroundMap

Seat scope: C3 support — (a) coverage-map rows for the two new entries, (b) the frontier ground-map
row and its dated preamble, (c) the PROVINCE question, plus the land ordering forced by the round-55
counter's dangling rule. Lane reads were read-only; every run used a shared scratch clone under
`/fast/scratch/hyaku/kake-r58/ScribeGroundMap/` (deleted at the end). No lane jj/git mutation, no
subagent dispatch, no tool install, no pacman.

State at report time: lane tip `cc8da16`; contract commit `fff3eea`; base revision `0440485`.
`corpus/knowledge/` holds 54 files and neither `baidu-spider-identification.md` nor
`baidu-spider-unblocking.md` exists yet; `corpus/SOURCES.md` holds 160 rows (`grep -c '^| S'` → 160)
with S423/S424 absent. The coverage-map first table has 56 rows; the frontier table 22 rows.

## CURRENT:

`corpus/README.md:74` (last index row of the first table):

```
| Baidu Spider 3.0 dead-link recognition model (r57) | `knowledge/baidu-spider3-dead-link-model.md` (S422) | protocol dead links, most content dead links and redirect dead links named by the recognition model; a few-days processing statement; the best-choice preference; the index-display figure's real placement; no crawl observed |
```

`corpus/README.md:76`: `### Frontier ground map (round 55; round-57 update)`

`corpus/README.md:78-85` (preamble; the clause to extend is :82-83):

```
One row per `PROVINCE.md` §Frontier ground that a held entry can be dated to
(`PROVINCE.md:22-30`): the round it entered, the entry, and the `used-by` rows
that entry names in `corpus/SOURCES.md` at base `fcaf4b85…` (155 rows); the round-55 row is
measured at the round's final revision (156 rows, S418 added) and the round-56 row at the round-56
final revision (158 rows, S419 and S420 added), not at base `e48354b7…`; the round-57 row at the
round-57 final revision (160 rows, S421 and S422 added), not at base `28fa0b23…`. Ranges
are inclusive and each id was checked individually; a row set is the entry's
`used-by` cells, not a re-adjudication of any source.
```

`corpus/README.md:104` (last round-grouped frontier row):

```
| Baidu dead-link handling (dead-link types, Spider 3.0 recognition model) | r57 (lands this round) | `knowledge/baidu-dead-link-types.md` `knowledge/baidu-spider3-dead-link-model.md` | S421 S422 |
```

`corpus/README.md:117-121` (post-table paragraph):

```
locators). The round-55 row's three entry paths are absent at base by design,
and S418 is not in the base registry; the round-56 row's three entry paths are
absent at its base `e48354b7…`, and S419 and S420 are not in that registry; the
round-57 row's two entry paths are absent at its base `28fa0b23…`, and S421 and
S422 are not in that registry.
```

`corpus/README.md:141-143` (held-but-ungated sentence; proposed unchanged, see PROVINCE):

```
`PROVINCE.md:344`, canonical selection and crawler identity `PROVINCE.md:361`,
the eleven per-engine entries (the round-52 trio `PROVINCE.md:382`, the round-55 Yahoo! robots trio
`PROVINCE.md:397`, the round-56 crawl-handling trio `PROVINCE.md:423`, the round-57 Baidu pair
```

`PROVINCE.md:22-23`:

```
- Crawl hygiene per host (robots.txt, sitemap scope, canonical signals) — first
  entry `corpus/knowledge/crawl-scope-per-host.md`; canonical/JS rendering open.
```

## PROPOSED EDITS:

Five anchored replacements; all measured green by the counter in a fixture (see ORDERING).

**E1 — two index rows, inserted after `corpus/README.md:74` (that line itself unchanged):**

```
| Baiduspider identification (r58) | `knowledge/baidu-spider-identification.md` (S423) | Baiduspider identification as the page states it: three UA channels (PC, mobile, mini-program) and a two-step DNS verification — a reverse lookup whose hostname must sit under baidu.com or baidu.jp, then a forward lookup whose address must match the logged IP; no crawl observed |
| Baiduspider unblocking (r58) | `knowledge/baidu-spider-unblocking.md` (S424) | Baiduspider unblocking: the three block classes the page names (robots.txt, the Baidu user agent, an IP-level firewall block), the curl head request under a Baiduspider user agent whose 200 answer it calls normal, and the remedies it names (strategy change, user-agent whitelist); no unblock observed |
```

Measured with the counter's `words()`/`norm()`: 44 and 45 whitespace tokens (floor 5); no `|` in any
cell; both normalized cells unique against the 56 existing cells (`duplicate=0`); H1 overlap with the
lines the entry scribes reported — S423 `# Baidu's own page gives two tests for a genuine Baiduspider
request, and names three UA channels` → `{baidu, baiduspider, channels, three}`; S424 `# Baidu's page
names three ways a site can block Baiduspider and orders the self-check robots, then UA, then IP` →
`{baidu, baiduspider, block, names, robots, three}`. Each row names one knowledge file.
**E2 — heading:** `### Frontier ground map (round 55; round-57 update)` →
`### Frontier ground map (round 55; round-58 update)`
**E3 — preamble, old (end of :83 through :84):** ``not at base `28fa0b23…`. Ranges\nare inclusive`` →
```
not at base `28fa0b23…`; the round-58 row
at the round-58 final revision (162 rows, S423 and S424 added), not at base `0440485…`. Ranges
are inclusive
```
**E4 — post-table paragraph, old (:120-121):** ``S421 and\nS422 are not in that registry.`` →
```
S421 and
S422 are not in that registry; the
round-58 row's two entry paths are absent at its base `0440485…`, and S423 and S424 are not in
that registry.
```
**E5 — frontier row, inserted after :104:**

```
| Crawler identity (Baidu: UA + two-step DNS; unblocking) | r58 (lands this round) | `knowledge/baidu-spider-identification.md` `knowledge/baidu-spider-unblocking.md` | S423 S424 |
```

A new row beats extending the r51 `Crawler identity (Googlebot subtypes)` row (one round, one set per
cell); after :104 it keeps round-group order, and the frontier table is not an index table.

## ORDERING:

`c55_readme_index.py` (round-55 v2, `--root <lane> --revision <rev>`) fails `dangling` on any
backticked path token in the whole `## Coverage map` section, frontier subsection included, that does
not resolve at the measured revision (`resolves()` over `corpus/`, `corpus/knowledge/`,
`corpus/lessons/`, lane root); `unindexed` fires on any knowledge file the first table omits. Fixture
runs (shared clone, `selftest` commits, toplevel verified as the fixture dir):

- base tip, neither edit: `index_mismatches=0 … met=True`, EXIT=0 (56 rows / 54 files)
- both edits (two entry stubs + E1–E5): `index_mismatches=0 knowledge_files=56 … coverage_rows=58`, EXIT=0
- entries only, README reverted: `index_mismatches=2 … unindexed=2` (`baidu-spider-identification.md`,
  `baidu-spider-unblocking.md`), EXIT=1
- README only, entries absent: `index_mismatches=2 … dangling=2`
  (`knowledge/baidu-spider-identification.md`, `knowledge/baidu-spider-unblocking.md`), EXIT=1

So the L1 must: (1) land the two entries with the S423/S424 registry rows and the
`corpus/lessons/round-58.md` `## Gate` lines; (2) land the README edit in the same commit as the
entries or later — never earlier; (3) run `c55_readme_index.py` and take any receipt only at a
revision that already contains both entries and the README edit, since an intermediate revision is
red in either order and C1 forbids rewriting a committed receipt; (4) treat E3's "162 rows" claim as
true only once the registry append is in the same measured revision (the counter does not read
`SOURCES.md`; this is claim fidelity, not a counter condition).

## PROVINCE:

No existing PROVINCE line changes. `PROVINCE.md:22-23` (quoted above) already carries the ground, and
the round-51 block (`PROVINCE.md:352`) reads crawler identity into it; the round-58 entries extend
that reading, so no byte of :22-23 moves and :23's "canonical/JS rendering open" stays true. Rounds
51–57 recorded themselves as appended `## Round-NN …` sections (`:352`, `:367`, `:385`, `:408`, `:429`;
file ends at :447); a round-58 section is the same pattern — new lines after :447, optional for C3 —
and appended lines do not shift earlier ones. Any README citation of its line number (e.g. adding the
pair to the held list at `corpus/README.md:141-143`) must be written and checked after the append
lands. The "eleven per-engine entries" count stays untouched (the r58 pair sits on the already-named
`Crawler identity` ground); per-engine reclassification makes it thirteen and needs a measured
`PROVINCE.md:<line>` reference.

## Limits

- Neither entry exists at the tip I read; fixture stubs (reported H1 + `source:` / `verified-at:` /
  `recheck:` + one sentence) exercise index rules only, not quote truth. If a landed H1 differs,
  re-run the counter: the thin rule reads H1 + 1500 characters, so `Baiduspider` overlap survives most
  rewrites, but the seat rule names the H1.
- `c58_quote_truth.py` was not run by this seat (C3's 8 conditions belong to the build seats).
- No lane path other than this report was written; scratch removed.

VERDICT: The two index rows, the r58 frontier row and the preamble/paragraph updates validate green against the round-55 counter in a fixture; entries and the README edit must land in the same revision (entries-only → unindexed=2, README-only → dangling=2), and PROVINCE needs no existing-line change.
