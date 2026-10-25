# ScoutQuarantineSlice — kake quarantine slice, re-derived

Axes: operability, freshness. Read-only. This file is the only write.

## Verdict

The round-prompt awk, re-run against the absent-defect register at write time, prints **12 lines**. Every line carries an S-id.

The 12 ids, in slice order: **S142, S143, S148, S156, S161, S193, S194, S195, S206, S154, S178, S184**.

**S273 does not appear. S274 does not appear.** Neither token is in the slice, and neither is a substring anywhere in the register.

## Slice (awk stdout)

Command (prompt awk; stdout only — not redirected into `assimilation/quarantine-slice`):

```
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
awk -F'|' -v l='kake' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R"
```

`/usr/bin/awk` is GNU Awk 5.4.1. Exit 0. `wc -l` = 12. Stdout sha256 `6d92f4408c7482e59fb93c2085676f7d9c4fedb687bcfd501060f63c15d2d63a`.

```
 S142   `payload-absent` 
 S143   `payload-absent` 
 S148   `payload-absent` 
 S156   `payload-absent` 
 S161   `payload-absent` 
 S193   `payload-absent` 
 S194   `payload-absent` 
 S195   `payload-absent` 
 S206   `payload-absent` 
 S154`   the cited source could not be fetched, so no quote was checked 
 S178`   the cited source could not be fetched, so no quote was checked 
 S184`   the cited source could not be fetched, so no quote was checked 
```

`cmp` of that stdout against `.ufo/waves/round-49/assimilation/quarantine-slice` was identical (same sha256). The committed slice was not used as the source of the ids.

## Ids

| # | S-id | register line | round | raw `$4` after trim | `$5` |
|---|------|---------------|-------|---------------------|------|
| 1 | S142 | 83 | round1 | `S142` | `` `payload-absent` `` |
| 2 | S143 | 84 | round1 | `S143` | `` `payload-absent` `` |
| 3 | S148 | 85 | round1 | `S148` | `` `payload-absent` `` |
| 4 | S156 | 86 | round2 | `S156` | `` `payload-absent` `` |
| 5 | S161 | 87 | round3 | `S161` | `` `payload-absent` `` |
| 6 | S193 | 88 | round6 | `S193` | `` `payload-absent` `` |
| 7 | S194 | 89 | round6 | `S194` | `` `payload-absent` `` |
| 8 | S195 | 90 | round6 | `S195` | `` `payload-absent` `` |
| 9 | S206 | 91 | round7 | `S206` | `` `payload-absent` `` |
| 10 | S154 | 319 | round2 | `S154`` | prose: could not be fetched |
| 11 | S178 | 320 | round4 | `S178`` | prose: could not be fetched |
| 12 | S184 | 321 | round5 | `S184`` | prose: could not be fetched |

Rows 1–9 are under `## Rows`. Rows 10–12 are under `## Rows whose quotes were NEVER CHECKED` (register lines 319–321). Their id cells are written `S154`` / `S178`` / `S184`` — a trailing backtick is part of `$4`, so a consumer that treats the whole cell as the id does not get a bare `S154`. The S-id token still matches `/S[0-9]+/`, which is why the awk admits them. The prompt's own comment ("every line must carry an S-id") holds.

## S273 / S274

- Slice grep for `S273|S274`: no match.
- Whole-register grep for `S273|S274`: absent.
- `crawl-budget` does not occur in the register.
- One URL overlap, not an id hit: register line 87 cites `https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate` under **S161**, class `` `payload-absent` ``. That is the reduce-crawl-rate URL, not S274.

## Why the summary is not the slice

`## By lane` line 242 is `| `kake` | 9 |`. The awk drops it: `$3` is ` 9 `, not `round[0-9]+`, and `$4` is empty. That matches the prompt's warning that the header and By-lane totals are stale and the slice must be derived. The 9 counts only the `## Rows` payload-absent block. The awk also admits the 3 never-checked prose rows, which is the 12.

Other `` `kake` `` field-2 hits: the 9 payload-absent rows, the summary row, and the 3 prose rows. No further kake data row was dropped by the round/id filters.

## Freshness

- Register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
- mtime `2026-10-24 08:37:00.746072780 -0300`, 83621 bytes, 375 lines, sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`
- Re-derived `2026-10-24T21:37:16-03:00` from that file. Register not edited.

Not done: no fetch of the 12 cited sources, no hand-check, no append. Those are outside this seat.

Report: .ufo/waves/round-49/w1/ScoutQuarantineSlice.md
