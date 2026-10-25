# ExecReopenS418
ATTACKS: freshness of S418 (`corpus/knowledge/yahoo-japan-robots-txt-basics.md`) and its retained body
`.ufo/waves/round-55/sources/S418.html` + `sources/receipts.json` at revision
a7a548e102b71bd16b0a6ddafa469393a2c98b69; live re-GET of `https://info-search.yahoo.co.jp/archives/002885.php`.

Read-only seat. All committed bytes read via
`git -C /home/vgpnk/Projects/shokunin/kake-shokunin show a7a548e102b71bd16b0a6ddafa469393a2c98b69:<path>`.
Scratch dir `D=/tmp/tmp.m6uJCuk1lt` (`git -C "$D" init -q`; `git -C "$D" rev-parse --show-toplevel` → `/tmp/tmp.m6uJCuk1lt`).
Lane worktree HEAD observed `78963ae28e1c6a409a1a1322230c5671cd2efcbe`; nothing in the lane was written except this report.
Tooling: curl 8.23.0, Python 3.14.8, `grep` builtin pi-uu-grep 0.2.0 and `/usr/bin/grep` GNU 3.12-modified. No installs, no pacman.

## FETCH:

Command (one request; 2026-10-25T21:13:30Z per response `date:` header):
```
curl -sSL -o fresh.html -D headers.txt -w 'HTTPSTATUS:%{http_code}\nFINALURL:%{url_effective}\nSIZE:%{size_download}\nNUMREDIRECTS:%{num_redirects}\n' \
  'https://info-search.yahoo.co.jp/archives/002885.php'
```
Observed output:
```
HTTPSTATUS:200
FINALURL:https://info-search.yahoo.co.jp/archives/002885.php
SIZE:7559
NUMREDIRECTS:0
EXIT=0
```
`wc -c fresh.html` → `7559`; `sha256sum fresh.html` →
`2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c`.

Response headers (`headers.txt`): `HTTP/2 200`; `content-type: text/html; charset=UTF-8`;
`date: Sun, 25 Oct 2026 21:13:30 GMT`; `cache-control: private, no-cache, must-revalidate`; `age: 0`.
**`Last-Modified` and `ETag` are both absent** — `grep -iE 'last-modified|etag' headers.txt` printed nothing
(`NEITHER PRESENT`), so no validator-based freshness signal exists for this URL; byte identity is the only
usable comparison. (Response also set `A`/`XA`/`B`/`XB` cookies — not reproduced here, not used.)

Byte/hash comparison of the same URL across four observations:

| observation | bytes | sha256 | status |
|---|---|---|---|
| `receipts.json` S418 (fetchedAt 2026-10-25T20:40:14+00:00, UA `kake-shokunin-round55`) | 7559 | `2b146a72…d69312c` | 200 |
| retained body at rev a7a548e (`git show …:sources/S418.html`) | 7559 | `2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c` | — |
| retained body in worktree (`sha256sum .ufo/waves/round-55/sources/S418.html`) | 7559 | `2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c` | — |
| **fresh GET now** (`fresh.html`) | 7559 | `2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c` | 200 |

All four are byte-identical. Receipt fields `url`, `httpStatus`, `bytes`, `sha256` match the fresh response exactly;
`fetchedAt` 20:40:14Z is ~33 min before this GET. `receipts.json` is itself identical at rev and in the worktree
(sha256 `c85a7d18585ae330f935d337afbd08f03c386ce8037fd5161bc401a53151b18e` both), as is the entry
(`bc5a3098eccc870a1e9e15bb1b81d4009a3be3484c0cfc565826b5b5da2f7062` both), so the comparison target did not drift
under me. Caveat: my GET used curl's default User-Agent, not the receipt's `kake-shokunin-round55`; the response was
byte-identical regardless. Total origin requests made by this seat: 2 (the plain GET above and the recheck curl below).

## RECHECK COMMAND:

Entry trailer, run exactly as written (curl half; second origin request):
```
curl -fsSL 'https://info-search.yahoo.co.jp/archives/002885.php' | grep -F -c '検索エンジンに対する要求を伝えるファイルです'
```
Observed: `1` (pipeline `EXIT=0`).

Same grep against the retained body at rev a7a548e (`/tmp/S418_rev.html`):
```
grep -F -c '検索エンジンに対する要求を伝えるファイルです' /tmp/S418_rev.html
```
Observed: `1` (`EXIT=0`).

**Counts: live = 1, retained = 1.** Cross-implementation check (the shell `grep` here is a builtin, so I ran both):
`/usr/bin/grep` (GNU 3.12-modified) → `1` live, `1` retained; builtin `grep` (pi-uu-grep 0.2.0) → `1` live, `1` retained.
The entry states no expected count, so the recheck is consistent rather than confirmed-by-assertion.

## SPAN TABLE:

Extraction: every `"…"` span (same-line, non-empty) in the committed entry and in the Gate line
(`git show …:corpus/lessons/round-55.md | sed -n '15p'`), unit count = CJK chars + non-CJK whitespace tokens,
test `span in fresh_text` plus `fresh_text.count(span)`.
Inventory is complete: the entry holds **13** double-quoted spans total, the Gate line **1**; the smallest span is
7 units, so no span was dropped by the 6+ filter.

| # | src | units | `in fresh_text` | occurrences in fresh | span |
|---|---|---|---|---|---|
| 1 | entry | 22 | True | 1 | 検索エンジンに対する要求を伝えるファイルです |
| 2 | entry | 21 | True | 1 | クローラーに巡回してほしくないウェブページ |
| 3 | entry | 7 | True | 1 | やディレクトリ |
| 4 | entry | 9 | True | 1 | サイトマップの位置 |
| 5 | entry | 14 | True | 1 | クローラーはrobots.txtの記述に従って |
| 6 | entry | 17 | True | 1 | サイト内のウェブページを巡回します |
| 7 | entry | 13 | True | 1 | クローラーによる巡回の際は |
| 8 | entry | 15 | True | 1 | まずサイトのルートディレクトリ |
| 9 | entry | 21 | True | 1 | （サイトの一番上の階層）にあるrobots.txtを探します |
| 10 | entry | 16 | True | 1 | robots.txtが設置されていなかった場合には |
| 11 | entry | 23 | True | 1 | そのサイトに対する巡回制限はないものとみなして |
| 12 | entry | 13 | True | 1 | robots.txtが設置されていた場合には |
| 13 | entry | 13 | True | 1 | その内容に従って巡回します |
| 14 | gate | 22 | True | 1 | 検索エンジンに対する要求を伝えるファイルです |

14/14 spans present in the fresh body, each exactly once (matching the entry's "occurs once" claim, re-checked against
the retained body: all 14 also `True`, occurrence 1). Max span = 23 units, under the 25-unit ceiling. The Gate line's
own `(22 units; …)` parenthetical recomputes to 22 under the stated unit rule.

Unquoted claim probes on the fresh body (`grep -F -c`): `サイト管理者` 1, `更新日` 1, `2010年11月24日` 1,
`<p class="update">更新日 2010年11月24日</p>` present, `<h2>robots.txtとは？</h2>` present;
directive tokens `User-agent` 0, `Disallow` 0, `Allow:` 0, `Crawl-delay` 0; `404` 0, `403` 0, `301` 0 —
consistent with the entry's "no directive token / no status code" claims. Cited sibling titles present:
`archives/002849.php">サイト単位、ディレクトリ単位での巡回の拒否設定 1` and `…002850.php">… 2`.

## DRIFT:

No byte change.
```
diff -q fresh.html /tmp/S418_rev.html   → no output, exit 0  ("IDENTICAL")
cmp fresh.html /tmp/S418_rev.html       → no output, exit 0  ("cmp: same")
```
Diff summary: 0 changed lines, 0 added, 0 removed; 7559 bytes on both sides; single sha256
`2b146a72…d69312c` across receipt, rev body, worktree body and live body. Freshness of S418 and of the entry's
quoted material is intact at rev a7a548e.

Observations (non-drift, low severity, no action claimed by this seat):
- The page still self-dates `更新日 2010年11月24日`, so a 180-day recheck cannot detect editorial change through a
  date field; only the sha256 receipt can. With no `Last-Modified`/`ETag`, drift detection for this row rests entirely
  on re-hashing the body. [INFERENCE] from the two absent headers plus the 2010 date stamp.
- The page's sidebar lists 11 `archives/*.php` links, not just the two refusal pages; one of them is
  `HTTPステータスコードとは？` (002844), which is the single `HTTP` hit in the body (line 268). It is a navigation link
  to a different article, not a status code stated in this page's prose, so the entry's "the page states no status code"
  claim is not falsified; the entry also does not claim its enumeration of cited pages is exhaustive.
- `rel="nofollow"` count 0 on this page — irrelevant to S418's claims (the entry explicitly leaves the link-level
  attribute to S374) and consistent with it.
- unrun: none. Everything the assignment named was executed; the only non-executed item is a UA-matched re-GET, which
  the byte-identical result makes unnecessary.

VERDICT: S418 is fresh — live GET returns 200 at the same final URL, 7559 bytes, sha256 `2b146a72…d69312c`, byte-identical to the receipt and retained body (zero drift); recheck count 1 live / 1 retained; 14/14 quoted spans (13 entry + 1 Gate, max 23 units) are raw substrings of the fresh text; no `Last-Modified`/`ETag` exists, so freshness rests on the hash receipt alone.
