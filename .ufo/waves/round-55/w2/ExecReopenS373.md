# ExecReopenS373
ATTACKS: freshness of row S373 and `corpus/knowledge/yahoo-japan-robots-pattern-syntax.md` at measured revision `a7a548e102b71bd16b0a6ddafa469393a2c98b69` (lane kake-shokunin), against a live plain GET of `https://info-search.yahoo.co.jp/archives/002850.php`.

All committed bytes below were read with
`git -C /home/vgpnk/Projects/shokunin/kake-shokunin show a7a548e102b71bd16b0a6ddafa469393a2c98b69:<path>`.
Scratch data dir `/tmp/s373work.yEYheb` (extracted committed copies, no git state), fetch dir
`/tmp/s373fresh.7ITDt4`. No lane path was written except this report.

## FETCH:

Command (one request):

```
curl -sSL -o "$D/S373.html" -w 'HTTPSTATUS:%{http_code}\nFINALURL:%{url_effective}\nSIZE:%{size_download}\n' \
  -D "$D/headers.txt" 'https://info-search.yahoo.co.jp/archives/002850.php'
```

Observed:

| field | observed now | receipts.json S373 | committed retained body |
|---|---|---|---|
| HTTP status | `HTTPSTATUS:200` | `httpStatus: 200` | — |
| final URL | `https://info-search.yahoo.co.jp/archives/002850.php` (no redirect) | same URL | same URL (row + entry `source:`) |
| byte length | `SIZE:9402` / `wc -c` = 9402 | `bytes: 9402` | `wc -c` = 9402 |
| sha256 | `3173d9613128e1aaa7cb55919fa52438602095bd7bc54d4437760ee8b1c03885` | `3173d961…c03885` | `3173d961…c03885` |

Response headers (`cat headers.txt`): `HTTP/2 200`; `content-type: text/html; charset=UTF-8`;
`date: Sun, 25 Oct 2026 21:13:29 GMT`; `vary: Accept-Encoding`;
`cache-control: private, no-cache, must-revalidate`; `pragma: no-cache`; `age: 0`;
`x-content-type-options: nosniff`; `x-frame-options: SAMEORIGIN`; `x-xss-protection: 1; mode=block`;
`permissions-policy` (2×, ch-ua-* and `unload=()`); `accept-ch: …`.
**`Last-Modified`: absent. `ETag`: absent.** Four `set-cookie` headers were returned; values are session
material and are deliberately not transcribed (shape only: `A`, `XA`, `B`, `XB` on `.yahoo.co.jp`).

Receipt-vs-live delta: receipt `fetchedAt` = `2026-10-25T20:40:14+00:00`, live `date` header =
`2026-10-25 21:13:29 GMT` — 33 min apart, byte-identical body. The receipt records
`userAgent: kake-shokunin-round55`; this fetch used curl's default UA and still produced the same
sha256, so the page bytes are UA-independent between those two requests.

## RECHECK COMMAND:

Line as committed (entry line 3, `cat -A` confirms it is one line ending `…2026-10-25)$`):

```
recheck: 180d — curl -fsSL 'https://info-search.yahoo.co.jp/archives/002850.php' | grep -F -c '記述された文字列を含むURLがすべてマッチします。' -> 1 (grep form run against the retained body, 2026-10-25)
```

1. Curl half run verbatim (`curl -fsSL '…/002850.php' | grep -F -c '…'`): printed **1**, exit 0 —
   matches the declared `-> 1`.
2. Same grep against the committed retained body
   (`grep -F -c '記述された文字列を含むURLがすべてマッチします。' /tmp/s373work.yEYheb/S373.committed.html`):
   printed **1**, exit 0.

Both counts = 1; the recheck's declared result reproduces on both surfaces (network and retained copy).

## SPAN TABLE:

Extraction: every straight double-quoted span `"…"` in the committed entry and in the committed lesson
Gate line (`corpus/lessons/round-55.md`, the single line starting `- S373 `), filtered to 6+ units.
Units computed with the round's own definition copied from the committed counter — `CJK_RE` at
`c55_quote_truth.py:104` and `units()` at `:167-169` (`len(CJK_RE.findall(t)) + len([tok for tok in t.split() if not CJK_RE.search(tok)])`).
Note that `。`/`、`/`「」` are outside that regex, hence the 21-unit totals below.
Test: `span in fresh_text` (python3, `-B`), fresh = `/tmp/s373fresh.7ITDt4/S373.html`.

17 spans of 6+ units (16 distinct; the Gate quote repeats entry span #14). Curly double quotes: 0 in entry, 0 in Gate line.

| # | src | units | in fresh | in committed body | span |
|---|---|---|---|---|---|
| 1 | entry | 18 | True | True | `robots.txtでは、以下のパターン記号が使用できます。` |
| 2 | entry | 15 | True | True | `ワイルドカードのパターンマッチ` |
| 3 | entry | 13 | True | True | `URLの末尾文字のパターンマッチ` |
| 4 | entry | 16 | True | True | `任意の長さの、任意のURL文字列にマッチ` |
| 5 | entry | 16 | True | True | `URL文字列のいずれの部分にも使えます。` |
| 6 | entry | 21 | True | True | `「public」で始まるすべてのディレクトリへの巡回を許可` |
| 7 | entry | 12 | True | True | `robots.txtが設置されたサイト以下で` |
| 8 | entry | 19 | True | True | `「.gif」で終わるすべてのファイルへの巡回を拒否` |
| 9 | entry | 10 | True | True | `ファイルパスに「.gif」を含む` |
| 10 | entry | 19 | True | True | `「$」記号は、文字列の末尾でのみ意味をなします。` |
| 11 | entry | 21 | True | True | `末尾であると判断し、以降の文字列を無視します。` |
| 12 | entry | 7 | True | True | `「$」記号がない場合、` |
| 13 | entry | 20 | True | True | `クローラーはプリフィクス（接頭辞）として扱い` |
| 14 | entry | 21 | True | True | `記述された文字列を含むURLがすべてマッチします。` |
| 15 | entry | 14 | True | True | `以下のように書かれていた場合、` |
| 16 | entry | 15 | True | True | `2つの「Disallow」の指示は、同等とみなされます。` |
| 17 | gate | 21 | True | True | `記述された文字列を含むURLがすべてマッチします。` |

Aggregate: `all_in_fresh = True`, `all_in_retained = True`, `max_units = 21`, `min_units = 7`,
`distinct_spans = 16`. Ceiling check: 21 <= 25 for every span, so the entry's own claim
("The longest span is 21 units") and the Gate's `(21 units; …)` both hold. Spans below the 6-unit
floor were excluded by the probe and are not scored here (`"$"`, `"*"`, `"Disallow: /*.gif$"`,
`"Disallow: /private*"`, `"Disallow: /private"`, `"robots.txt-rules.md"`-class identifiers).

## DRIFT:

`cmp /tmp/s373fresh.7ITDt4/S373.html /tmp/s373work.yEYheb/S373.committed.html` → identical, no output;
`diff -u committed fresh` → no hunks, `diff_exit=0`. **No byte change** between the round-55 receipt
(`2026-10-25T20:40:14Z`), the committed retained body at `a7a548e`, and the live page at
`2026-10-25 21:13:29 GMT`.

Cross-surface consistency (read-only, not a check of the lane's claims): the entry's `source:` header
line states `sha256 3173d961…c03885, 9402 bytes, HTTP 200` and the lesson Gate repeats the same pair;
both agree with the live fetch. Also `git diff --stat a7a548e -- <S373.html> <receipts.json>
<entry> <lesson>` printed nothing (`exit 0`), i.e. the worktree copies of these four paths still equal
the measured revision — the worktree has not moved under them.

Risk/limit: one GET, no conditional request (`If-None-Match`/`If-Modified-Since` unusable — the origin
sends neither `ETag` nor `Last-Modified`), so "no drift" is established only for this instant; the
`cache-control: private, no-cache` header means no intermediary copy was served, which strengthens the
single observation but does not extend it. `[INFERENCE]` the page's own `更新日 2010年11月24日` and the
absence of validators are consistent with a static archive page, so a 180d recheck interval is plausible
but unverified beyond this sample.

VERDICT: S373 freshness holds — live GET is 200, 9402 bytes, sha256 `3173d961…c03885`, byte-identical to receipt and retained body; recheck reproduces 1 on both network and retained surfaces; all 17 quoted spans (max 21 units) are exact substrings of the fresh text; no drift.
