# ReopenFlagS008 — S008 `quote_missing` re-opened by hand

Seat KakeR36.ReopenFlagS008 (wave 2, falsify). Lane master f3a38bf8. Sandbox
`/fast/scratch/hyaku/kake-r36w2/ReopenFlagS008/`. No tool installed or upgraded.

## Verdict
**Not real drift — input artifact (paraphrase class): the Gate quote carries two markdown
code-span backticks absent from the source.** Page unchanged, words verbatim, tool implements
its frozen rule, extractor faithful to the markdown line it read. `real=false`,
`tool miss=false`, `extraction miss=false`.

Item: `realrun/input.json` S008, url `…/cgit/tar.git/plain/doc/tar.texi?id=cfdb891bbd68c920ea75210977593f3cd08f0418`,
quote ``Default is `@option{--no-anchored}` for exclusion members``, `from: round-20.md`; manifest
identical (one hop 200, `text/plain; charset=UTF-8`, body `S008.body`); row `corpus/SOURCES.md:16`,
anchor 8478-8617.

## Live fetch (mine, not the tool's)
1. `curl -sS --max-redirs 0 -o body-noredir.html -D hdr-noredir.txt <url>` (exit 0) →
   `HTTP/1.1 502 Bad Gateway`, nginx/1.30.5, Savannah load page: "The service is unavailable.
   This is due to the high rate of AI scraping proxies which are overwhelming the system." — transient.
2. `curl -sS -L --max-redirs 5 -o body-retry -D hdr-retry.txt <url>` (exit 0) → `HTTP/2 200`,
   `content-type: text/plain; charset=UTF-8`, `content-length: 512359`. No redirect hop, so the
   row URL is current and `moved` is correctly absent.
3. `body-retry` sha256 `93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084` (512359 B).
   `cmp -s snap/S008.body body-retry` → identical to the body the real run scored
   (`realrun/snap-bodies.tar.xz:./S008.body`). Same sha256 dated 2026-10-21 in
   `.ufo/waves/round-26/rechecks/S008.json`: **unchanged across 10-21 → 10-23**. Raw `text/plain`
   Texinfo, so no JavaScript or rendering involvement.

## The quote in the live text (`body-retry:8584-8588`)
```
@itemx --no-anchored
If anchored, a pattern must match an initial subsequence
of the name's components.  Otherwise, the pattern can match any
subsequence.  Default is @option{--no-anchored} for exclusion members
and @option{--anchored} inclusion members.
```
Line 8587 sits inside the cited 8478-8617 and says exactly what the row teaches; summary table
8618 still reads `@item Exclusion @tab @option{--wildcards --no-anchored --wildcards-match-slash}`.
Body has 43 backticks in total, none at 8587.

## Why `quote_missing` (not a tool bug)
Bullet (d) (SCORECARD.md:1628-1631) is literal and case-sensitive after NFKC + `isspace()`
deletion; NFKC does not remove U+0060. Using the tool's own functions on the live body:
`as-recorded in text: False` / `backticks-stripped in text: True` (normalized index 263730).
Full reproduction, tool unmodified, real-run body:
`python3 -B scripts/source_recheck.py --manifest repro/manifest.json` → exit 1,
`{"version":1,"verdict":"failed-policy","checksEvaluated":1,"findings":[{"check":"S008","reason":"quote_missing","target":null}]}`
— same finding as `realrun/audit.json`. Media type `text/plain` takes bullet (e)'s raw path, so
no HTML rule could have stripped anything.

## Lineage of the backticks
`corpus/lessons/round-20.md:210` cell: `"Default is `@option{--no-anchored}` for exclusion
members"; "When wildcards match slash (the default for exclusion members)"`. The lesson wrapped
the Texinfo form in a markdown code span inside curly quotes; the wave-1 extractor took the cell
verbatim and states `.ufo/waves/round-36/w1/ExecGateQuoteExtractor.md:74` "every extracted quote
is verbatim from its recorded line" — true of the `.md` line, false of the source. The defect is
upstream of both the extractor contract and the recheck tool: the Gate quote is a
markdown-emphasized transcription, not a verbatim source span.

## Positive controls (row still supported)
- Round-20's second span is verbatim live: "When wildcards match slash (the default for
  exclusion members), a wildcard like @samp{*} in the pattern can match a @samp{/} in the name."
  → normalize-match True.
- Contiguous source sentence "Default is @option{--no-anchored} for exclusion members and
  @option{--anchored} inclusion members" → True.

## Advisory (outside S008)
- Same class explains siblings: manifest quotes for S004-S007 also carry markdown backticks; S004
  probe (`html_text`+`normalize` on its snapshot body) gives as-recorded False, stripped True. If
  that holds, the real run's `failed-policy` is quote contamination, not page drift.
- cgit answered 502 once under scraping load; contract (a) turns that into `http_error` →
  non-blocking → `failed-policy` with no retry, so a throttled host can read as a document policy
  failure. Did not affect S008 (recorded hop 200).

## Artifacts / not verified
`/fast/scratch/hyaku/kake-r36w2/ReopenFlagS008/{body-retry, body-noredir.html, hdr-retry.txt,
hdr-noredir.txt, snap/S008.body, repro/manifest.json}`. Not verified: sealed counter, 28 cases,
SCORECARD counts, the other 13 findings beyond the S004 probe.
