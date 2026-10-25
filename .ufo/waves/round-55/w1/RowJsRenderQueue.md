# RowJsRenderQueue

Claim C1 (coverage-map calibration), round 55 / W1, lane `kake-shokunin`.

Read set (read-only, no file edited): `corpus/knowledge/js-rendering-queue.md`
(all 78 lines) and `corpus/README.md` lines 1–47 (`## Layout` header, the
`| Area | Entry | Coverage |` table lines 14–38, `## Known gaps` start).
No git/jj command, no write outside this report.

Verification run (local python over the file bytes, `python3 - <<'PY'` heredoc):
each quoted passage below tested with `in` against its cited line (all True);
unit counts computed per the unit rule (one per CJK char, one per non-CJK
whitespace token); row split into exactly 3 cells; Coverage 26 words/26 units,
no `|`, does not start with `TBD`; shared 5+-letter words with the H1
(line 6) = `Status`, `queue`, `JavaScript`.

## ROW:

```markdown
| Render queue status-code contract | `knowledge/js-rendering-queue.md` (S137–S139) | Status-code rule: 200 responses queue for rendering regardless of JavaScript, non-200 may skip; robots.txt check precedes the request; four publisher rules; zh-CN and ja locale restatements. |
```

Placement: append as the last row of the `## Coverage map` table, after the
`Field performance (r28)` row (README line 38), before `## Known gaps`.

## EVIDENCE:

- `corpus/knowledge/js-rendering-queue.md:13-14` — "All pages with a 200 HTTP
  status code are sent to the rendering queue" (14 units; line 14 continues
  "matter whether JavaScript is present on the page"). Backs "200 responses
  queue for rendering regardless of JavaScript".
- `corpus/knowledge/js-rendering-queue.md:18-19` — "If the HTTP status code is
  non- 200 (for example, on error pages with 404" (15 units) and "rendering
  might be skipped." (4 units). Backs "non-200 may skip".
- `corpus/knowledge/js-rendering-queue.md:28,31-33` — "The crawl phase fixes
  the other boundary, and it sits *before* the fetch" (14 units) and "it first
  checks if you allow crawling. Googlebot reads the" (10 units; line 33 is
  "robots.txt file."). Backs "robots.txt check precedes the request".
- `corpus/knowledge/js-rendering-queue.md:39` — "A publisher reading that order
  gets four rules:" (8 units); `:54-56` — "The Simplified-Chinese edition
  states the same rule in that language" (10 units; line 57 names the Japanese
  edition). Backs "four publisher rules" and "zh-CN and ja locale restatements".

## RISKS:

- **No round tag in the file header.** Lines 1–4 are `source:`, `verified-at:`,
  `recheck:`, `ground:`; the only "round" match in the file is inside the word
  "ground" (line 4). The Area cell therefore carries no `(rNN)` tag, unlike the
  r20/r22/r28 rows. If the planner wants a tag it must come from the wave
  contract, not from this file — I did not add one.
- **Entry ids are compressed.** The `source:` line names three ids (S137 EN,
  S138 `?hl=zh-cn`, S139 `?hl=ja`); `(S137–S139)` is a range over them, matching
  the existing `knowledge/field-performance-cwv.md` (S036–S039) precedent.
- **Scope the row must not widen.** The file's `## Boundary` (lines 70–78)
  states it "does not say which canonical Google selects among duplicates" and
  "says nothing about any other engine"; browser execution and client-side
  crawler discipline are assigned to `tabi` (PROVINCE.md, Adjacent). A row
  claiming canonical or cross-engine rules would overreach.
- **Counts not restated.** The `recheck:` line (line 3) records grep counts
  1 / 3 / 2 for the English and locale editions; the row says "restatements"
  without a count, because the file quotes one sentence per locale and the
  counts are recheck artifacts, not body content.
- **Freshness.** `verified-at: 2026-10-24`, `recheck: 180d`; source doc revs
  2026-03-04 (EN) and 2026-03-05 (locale), all `opened 2026-10-24`. The recheck
  command was **not** re-run by me (read-only seat; no network fetch attempted),
  so the recorded counts are the file's claim, not my observation. No stale or
  self-contradictory statement found in the body.
- **Quoted artifact preserved.** Line 18 reads "non- 200" with an internal
  space; the row says "non-200" in prose, outside quotes, and no quote in
  EVIDENCE was altered.

VERDICT: One new coverage-map row drafted and machine-checked against the file's own lines; nothing edited, no claim beyond the file's text.
