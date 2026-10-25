# ExecReopenS420

Scope: freshness re-opening of row S420 only — live GET of `https://info-search.yahoo.co.jp/archives/002857.php`, the
knowledge entry's `recheck:` command run as written, the Gate quote of `corpus/lessons/round-56.md` located in the live body,
drift. Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`, revision under attack `a450e43e696d032e3ac308383f6b3394e0c92860`
(read-only; no counter was run in this seat). Fetch executed in `$(mktemp -d)`, no lane file touched.

## FETCH:

Command, run exactly once (2026-10-25):

```
curl -sS -L -A kake-shokunin-round56-w2 -o "$T/S420.live.html" -w '%{http_code}' \
  https://info-search.yahoo.co.jp/archives/002857.php
```

| | live GET | retained `sources/S420.html` | `receipts.json` S420 |
|---|---|---|---|
| HTTP | `200` | — | `httpStatus: 200` |
| bytes | `7332` | `7332` | `bytes: 7332` |
| sha256 | `a860d4f33181302d7ab467f5a0b21f2008916bb6dc6def69e69df5b54c630209` | `a860d4f3…c630209` (same) | `a860d4f33181302d7ab467f5a0b21f2008916bb6dc6def69e69df5b54c630209` |

- `cmp -s` live vs retained → identical; `diff` live vs retained → empty (no output, exit 0).
- Receipt metadata not re-asserted: `fetchedAt: 2026-10-25T22:02:42+00:00`, `userAgent: kake-shokunin-round56` are the
  round-56 receipt's own values; this GET used UA `kake-shokunin-round56-w2` and did not rewrite them.
- Byte-identity of a 7332-byte page fetched twice is the only freshness evidence here; no header other than the status code
  was captured (`-w '%{http_code}'` only).

## RECHECK RUN:

`corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md`, `recheck:` line, both arms run as written (2026-10-25):

```
curl -fsSL 'https://info-search.yahoo.co.jp/archives/002857.php' | grep -F -c 'クローラーはエラーページとみなさず、'
```

- curl arm printed **1**, exit 0.
- grep arm against the retained body, `grep -F -c 'クローラーはエラーページとみなさず、' .ufo/waves/round-56/sources/S420.html`
  → printed **1**, exit 0.

Both printed counts equal the counts the entry claims (`curl arm 1 and the same grep against the retained round-56 body 1,
2026-10-25`). The recheck's `180d` window and `verified-at: 2026-10-25` are unchanged by this run; the entry is not edited by
this seat.

## GATE QUOTE:

Gate line for S420: `corpus/lessons/round-56.md:18`, quote `クローラーはエラーページとみなさず、` (declared 17 units).

- Count in the live body: **1**. Count in the retained body: **1** (single occurrence, line 104).
- `span_tools.py check S420 'クローラーはエラーページとみなさず、'` →
  `{'units': 17, 'raw_substring': True, 'in_content': True, 'count_in_page': 1, 'in_other_adopted_body': False}` — the
  declared 17 units reproduce and the span is page-unique among adopted bodies (C2 v2's Gate-uniqueness condition holds).
- Heading cited by the Gate, `§ 存在しないウェブページが巡回される`, is present in the live body and matches the article's own
  `<h2>存在しないウェブページが巡回される</h2>` (retained line 100), immediately followed by
  `<p class="update">更新日 2010年11月24日</p>` (line 101) — the page-printed date the Gate cites.
- The heading string occurs **3** times in the live body: `<title>` (line 33), the `<h2>` (line 100), and a sidebar
  `<li><strong>` link (line 286). Only the `<h2>` is the section heading; the Gate names the section, so the locator is
  unambiguous, but the 3 occurrences mean a bare heading-substring count would not be a uniqueness proof.
- Quote sits inside the article block: `#contents-body`/`#main` open at lines 85–86, `#contents-footer` closes at line 388;
  line 104 is the paragraph carrying the 200-OK/error-page sentence.

## DRIFT:

- **No drift.** Live body is byte-identical to `sources/S420.html` (same sha256, same 7332 bytes, empty `diff`), so there is no
  differing region to name — not the header, not the article block, not the sidebar.
- Therefore the Gate quote, the entry's eight quoted spans and the `recheck:` counts are all still true of the live page as of
  2026-10-25; nothing in the row's provenance (`sha256 a860d4f3…`, 7332 bytes, HTTP 200) is stale.
- Limit of this finding: one GET, one instant. Byte-identity today says nothing about the next `180d` window, and no
  `Last-Modified`/`ETag`/`Age` header was captured, so caching or an edge copy serving identical bytes cannot be excluded.

No lane file, jj state or Git index was modified; the only write is this report.

VERDICT: S420 no drift — live GET 200 / 7332 bytes / sha256 a860d4f3…c630209 byte-identical to the retained body, recheck arms print 1 and 1 as claimed, Gate quote count 1 under h2 § 存在しないウェブページが巡回される.
