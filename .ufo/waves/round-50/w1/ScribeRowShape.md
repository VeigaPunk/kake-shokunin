# Round 50 wave 1 — S286 row shape: pre-append mirror vs staged append

Seat: leaf (read-only except this report). Axis: freshness.

Inputs (evidence anchors):

- Pre-append mirror row: `.ufo/waves/round-50/assimilation/pre-append/corpus/SOURCES.md:151`
- Staged append row: `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md:43` (read-only external)
- Table header, both files, identical: `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` (pre-append line 7, staged line 5) — 11 columns.
- Method: `python3` script (scratch at `/tmp/c50_s286_cells.py`); split on unescaped pipes (regex `(?<!\\)\|`), cells stripped, compared pairwise. All quoted strings below are script output verbatim.

## 1. Pre-append S286 row shape

- Pipe count in the line: 12. Blind split on `|`: 13 fields (first and last empty) → **11 pipe-separated content cells** between the leading and trailing pipe, matching the 11-column header.
- Requested cells, verbatim:
  - status: `mined`
  - opened: `2026-10-24`
  - recheck: `180d`
  - used-by: `corpus/knowledge/crawl-error-status-table.md`
- Literal/escaped pipe check: **no cell contains a literal or escaped pipe.** The line has zero `\|` sequences, and every `|` in the line is a cell delimiter; a blind split and an escaped-pipe-aware split agree (11 content cells either way).

## 2. Cell-by-cell diff vs the staged S286 row

Both rows have 11 cells (same count). 6 cells unchanged: id, source, kind, tier, status, used-by. 5 cells changed:

- **scope** (cell 5):
  - old: `How an error status is read by Googlebot, distinct from robots directives and crawl-budget levers`
  - new:
    ```
    The **crawl-error layer** — how availability, soft 404s and over-crawling change crawling. The lane's robots rows (S011–S013, S095–S100) and the wave-3 budget rows (S154, S155) state directive and budget semantics; neither states how an error status is read by the crawler
    ```
- **anchor** (cell 6):
  - old: `the sentence that Googlebot scales crawling back when servers are in trouble; opened 2026-10-24`
  - new: `§ "Hide URLs that you don't want in search results" → "soft 404 errors" (doc rev. Last updated 2025-12-18 UTC)`
- **teaches** (cell 7):
  - old: `Googlebot scales its crawling back when it detects the server is having trouble`
  - new: `soft 404 pages keep being crawled and waste budget while a real 404/410 stops the recrawl, and Googlebot scales its crawling back when the server is struggling`
- **opened** (cell 9): `2026-10-24` → `2026-10-23`
- **recheck** (cell 10): `180d` →
  ```
  180d — `curl -fsSL 'https://developers.google.com/search/docs/crawling-indexing/troubleshoot-crawling-errors' \| grep -c 'scale back its crawling'` -> 1 (ran 2026-10-23)
  ```

Parsing note on the staged row: its recheck cell contains **one escaped pipe** (`\|` inside the backtick curl pipeline). The staged line has 13 `|` characters; a blind split on `|` yields 12 content fields, while an escaped-pipe-aware split yields 11 — the header-consistent count. The staged row is shape-valid only under escaped-pipe-aware parsing; the pre-append row is shape-valid under either.

Observed fact, no verdict implied: the staged `opened` moves one day backward relative to the pre-append mirror (2026-10-24 → 2026-10-23).

## 3. Frozen counting commands (run; output recorded, not reasoned)

- `c50_quote_class.py --revision 9619af67c52939daac502ca7a24c9d714f3f51db` → `C1 classed 0/3 met=False`; FAIL S273 (class ledger absent, lesson absent), FAIL S274 (same), FAIL S286 (class ledger absent, retained blob absent, lesson absent, no live registry row, entry absent); exit 1.
- `c50_quote_class.py --revision 33eec7f2cecfdbb9c7a1f85c3d8efae8dacd7dd1` → `C1 classed 0/3 met=False`; FAIL S273 (lesson absent), FAIL S274 (lesson absent), FAIL S286 (lesson absent, no live registry row, entry absent); exit 1.
- `c50_durable.py --revision 9619af67c52939daac502ca7a24c9d714f3f51db` → `C2 durable 0/1 met=False`; order proof absent, wave-cite proof absent, LOG.md at measured revision does not cite the wave, settlement absent; exit 1.
