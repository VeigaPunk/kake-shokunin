# RowCrawlErrors

Seat: leaf scribe, claim C1 (coverage-map calibration). Base revision fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d.
File read whole: `corpus/knowledge/crawl-error-status-table.md` (14 lines, no trailing content).
Format reference read: `corpus/README.md` header + `## Coverage map` rows at lines 17–45 (3-cell `| Area | Entry | Coverage |`).
No file edited. No subagent dispatched. No tool installed or upgraded (nothing needed).

## ROW:

```
| Error-status crawl layer | `knowledge/crawl-error-status-table.md` (S286) | One admitted Googlebot sentence: crawling scales back when server trouble is detected; the admitted quote is a raw substring of the retained page, unlike S273's collapsed-only crawl-budget quote; no soft-404 remedy claimed. |
```

Mechanical checks run (python, this seat):
- Coverage word count = 32 (window 10–45); no `|` character; does not start with `TBD`.
- 5+-letter words shared with H1 (`An error status is its own crawl layer`) or first 1500 chars: Googlebot, admitted, claimed, collapsed-only, crawl-budget, crawling, quote, remedy, retained, sentence, server, substring, trouble.
- Table line splits into exactly 3 cells; Entry cell is the backticked path plus `(S286)` copied verbatim from the file's `source:` line (line 1).
- No existing Coverage-map row names this file: `grep -n "crawl-error" corpus/README.md` returns nothing; no other `knowledge/*.md` mentions it.
- Area has no round tag because the file's own header (line 6) carries none; `(r55)` would not be traceable to the file.

## EVIDENCE:

All passages below are raw substrings of `corpus/knowledge/crawl-error-status-table.md` (verified with python `in`), each ≤ 25 units (no CJK present, so units = whitespace tokens).

1. `crawl-error-status-table.md:8` — "Only one sentence is admitted." (5 units) — grounds "One admitted Googlebot sentence".
2. `crawl-error-status-table.md:10` — "Googlebot will scale back its crawling if it detects that your servers are having trouble" (15 units) — grounds "crawling scales back when server trouble is detected".
3. `crawl-error-status-table.md:10` — "S273's crawl-budget quote is collapsed-only." (5 units) — grounds "unlike S273's collapsed-only crawl-budget quote".
4. `crawl-error-status-table.md:14` — "A soft-404 remedy is not claimed from this sentence." (9 units) — grounds "no soft-404 remedy claimed".

The "raw substring of the retained page" clause rests on line 10, "That sentence is a raw substring of the retained HTML." (9 units, also a substring of the file). Independently spot-checked against the retained body, read-only: `grep -o` of that 15-unit sentence in `.ufo/waves/round-50/sources/S286.raw.html` returns exactly one match; `.ufo/waves/round-50/sources/S286.headers` shows HTTP/2 200. The same probe reproduces the file's two cross-references: the S273 crawl-budget quote is absent from `round-49/sources/S273.raw.html` but present in `S273.txt` (collapsed-only), and the S274 crawl-rate quote is present in `round-49/sources/S274.raw.html` (raw substring). Both cross-reference labels in line 10 are accurate.

## RISKS:

- **Filename overpromises structure.** The file is named `…-status-table.md` but holds 14 lines of prose with no table, no status-code list and no per-status behaviour. The row's Area therefore says "crawl layer", not "table"; a reader who trusts the filename will expect a mapping that does not exist. The Entry cell must name the path as-is, so the row cannot signal this mismatch.
- **No round tag anywhere.** Line 8 says "One Google document opened this round" without naming the round; metadata is `verified-at: 2026-10-24` and `recheck: 180d`. Round date is 2026-10-25, so this file was verified the previous round and is inside its recheck window. The row carries no round tag and must not be read as r55 verification.
- **Single-sentence scope.** The file admits exactly one sentence and explicitly disclaims more ("What this entry does not establish", line 12). The row must not be widened to "error statuses", "status codes", or soft-404 handling; only the Googlebot scaling statement is supported.
- **Provenance lives outside r55.** The r55 retained bodies are Yahoo! JAPAN pages (S372/S373/S418) and are unrelated to this file. Its retained body is `.ufo/waves/round-50/sources/S286.raw.html`, so any future re-derivation must go there, not to the round's `sources/` directory.
- **Row placement is not mine to make.** The natural slot is after the last row, `corpus/README.md:45` (Field performance, r28). This report proposes the line only; the README is unedited, as instructed.
- **Unrun checks (reported as unrun, not as passes):** no check of whether the Coverage-map table stays well-formed after insertion (that is the integrator's edit); no re-fetch of the S286 URL this round (network fetch was out of scope); no verification of the file's `ground:` claim that robots-directive and crawl-budget entries exist in the lane beyond the two cross-references named above.

VERDICT: One coverage-map row drafted and mechanically validated against the file (32-word Coverage, 4 substring-verified evidence passages); file left unedited, cross-references and S286 raw-substring claim independently confirmed read-only.
