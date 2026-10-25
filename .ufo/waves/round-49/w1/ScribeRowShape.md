# ScribeRowShape — round 49 / w1

Axes: operability, freshness.
Milestone: Round 49 v1 wave: attack the frozen order proof and crawl-budget quote truth.

Registry was not edited. Read-only parse of live `corpus/SOURCES.md`. That file is byte-identical to `1c846ed2d67b1692ea966be064f0fc04542763c6:corpus/SOURCES.md` (133241 bytes). `git status --porcelain -- corpus/SOURCES.md` printed nothing. HEAD is `1c846ed2d67b1692ea966be064f0fc04542763c6`.

## Verdict

Both rows are 11 data columns. Census field count is `NF=13` (`fields=NF-2=11`), which is the SOURCES-CONTRACT-v1 width (`scripts/sources-census.sh` header: 11 columns => NF=13; E01 fires when `NF!=13`). Recheck is the bare cell `180d` on both rows. No cell contains a pipe.

## Header

Line 7:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
```

`gawk -F'|'` on that line: `NF=13 fields=11`. Recheck is data column 10, awk `$11`.

## Rows

Same splitter on the live file (`gawk -F'|'`, trim of `$2` and `$11`):

```
NR=149 NF=13 fields=11 id=[S273] recheck=[180d] pipe_in_any_field=0
NR=150 NF=13 fields=11 id=[S274] recheck=[180d] pipe_in_any_field=0
```

Python split on U+007C, cells = fields[1:-1], strip:

| id | line | data columns | U+007C count | escaped-pipe count | pipe inside a trimmed cell | recheck |
|---|---|---|---|---|---|---|
| S273 | 149 | 11 | 12 | 0 | no | `180d` |
| S274 | 150 | 11 | 12 | 0 | no | `180d` |

Twelve pipes is the separator count for 11 cells (leading empty field, 11 cells, trailing empty field). Leading and trailing fields were empty on both rows. No trimmed cell contains `|`. No cell contains `\|`, U+FF5C `｜`, U+2502 `│`, U+00A6 `¦`, U+2223 `∣`, or U+01C0 `ǀ`. Source-cell em dashes are not pipes.

Recheck cells, exact:

- S273 column 10: `180d` (length 4). Not `180d — curl …` and not an ISO date.
- S274 column 10: `180d` (length 4). Same.

Other cells, pipe=false on every one:

- S273: id `S273`; kind `docs`; tier `A`; status `mined`; opened `2026-10-24`; used-by `corpus/knowledge/crawl-budget-consequences.md`.
- S274: id `S274`; kind `docs`; tier `A`; status `mined`; opened `2026-10-24`; used-by `corpus/knowledge/crawl-budget-consequences.md`.

Line sha256 (line bytes plus a trailing newline, as `splitlines` dropped it):

- L149 `b72736ccab28cb4c2c7fe77b105154db3d76b16b702c0730716168195432a534` (616 bytes)
- L150 `118a08d1a098bfc8fc2402240734ca0ab7ed0a2a22083f2358fb1811e0ffd36d` (493 bytes)

S273 and S274 each occur once, each as a single pipe-row. No continuation line.

## What this does not say

This seat did not run `sources-census.sh`. The measured `NF=13` and bare `180d` are the inputs that contract uses for E01 and E09 (`recheck ~ /^[0-9]+d$/`). A prose recheck cell would both fail that pattern and, if it contained `|`, inflate `NF`. Neither defect is in these two rows.

Report: .ufo/waves/round-49/w1/ScribeRowShape.md
