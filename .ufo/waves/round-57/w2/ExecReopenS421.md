# ExecReopenS421

Seat: ExecReopenS421 — claim **C3 freshness** (re-open the source, re-run the recheck, re-run every quote, re-derive the row).
Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`. Build under attack, read as named revision:
`4b8c73050470ada9e6583f3b12d659d1bed6a17f` (`git show 4b8c730…:corpus/SOURCES.md`, `…:corpus/knowledge/baidu-dead-link-types.md`;
the working tree was not read for any row/entry fact). Date of run: 2026-10-25 UTC.
Evidence written (only path I wrote besides this report): `.ufo/waves/round-57/w2/ExecReopenS421.files/{S421.refetch.html,S421.refetch.diff.txt}`.
No credential material, token, `op://` ref or private URL is reproduced here.

## FETCH:

```
curl -sS -L --compressed -A kake-shokunin-round57-w2 -o .ufo/waves/round-57/w2/ExecReopenS421.files/S421.refetch.html \
     -w '%{http_code} %{url_effective} %{size_download}' 'https://ziyuan.baidu.com/college/articleinfo?id=3458'
-> 200 https://ziyuan.baidu.com/college/articleinfo?id=3458 10543      (10543 = compressed transfer bytes)
```

- `200`, effective URL identical to the requested URL (no redirect tail).
- Retained body: `.ufo/waves/round-57/sources/S421.html`, 34750 bytes, 450 lines.
- Refetch body: `…/ExecReopenS421.files/S421.refetch.html`, 34750 bytes, 450 lines.
- `receipts.json` S421 claim re-checked: `httpStatus 200`, `bytes 34750`, `sha256 32eaf8b7…447182`,
  `fetchedAt 2026-10-25T23:38:33+00:00`, `userAgent kake-shokunin-round57`. The retained file's own sha256 is
  `32eaf8b74012c99dff8ae6cc3db0658d3f7520b04045336b8228461dab447182` — **the receipt pin matches the retained file** (confirmed by running).

## EQUAL TO RETAINED:

- Not byte-identical. sha256 retained `32eaf8b7…447182` vs refetch `5a4edefe…5ca42d8`; both 34750 bytes; `cmp -l` reports 8 differing bytes.
- `diff -u` → exactly **3 changed lines: 346, 347, 361** (full unified diff at `…/ExecReopenS421.files/S421.refetch.diff.txt`).
- Region of every difference — **header/footer script block, not the article block**:
  - L346/L347: `passport.baidu.com/passApi/js/{uni_login_wrapper,wrapper}.js?cdnversion=…` cache-buster timestamps
    (`202610260738→202610260825`, `1792971513→1792974318`).
  - L361: the `passreg` JS config's passport port (`ziyuan.baidu.com%3A8054` → `…%3A8098`) inside a `<script>` block.
- Article block (span_tools v1 window, `class="article-info"` → `class="footer"`): retained `[9346,21828)`, refetch `[9346,21828)`;
  `retained[9346:21828] == refetch[9346:21828]` → **True** (byte-identical, confirmed by running). All three diffs sit at offsets
  23604/23734/24195, i.e. after the article block ends.
- Consequence for C3: the pinned digests are not reproducible byte-for-byte by a later fetch (dynamic CDN cache-busters + a session
  port), so a "refetch must equal the pin" reading would fail; the *content* the entry quotes is unchanged. This is a property of the
  page, not a defect in the entry. `[INFERENCE]` if `c57_quote_truth.py` were ever re-pinned from a live fetch rather than frozen at the
  contract commit, it would immediately mismatch.

## RECHECK RUNS:

Entry `corpus/knowledge/baidu-dead-link-types.md` line 3, command executed verbatim (live):

```
curl -fsSL --compressed 'https://ziyuan.baidu.com/college/articleinfo?id=3458' | grep -F -c '协议死链和内容死链'
-> 1        (exit 0)
```

Grep form against the retained body:

```
grep -F -c '协议死链和内容死链' .ufo/waves/round-57/sources/S421.html   -> 1   (exit 0)
grep -F -c '协议死链和内容死链' …/S421.refetch.html                      -> 1   (exit 0)
```

- Both counts **1**, matching the entry's recorded `-> 1 (grep against the retained body 1, 2026-10-25)`.
- `-fsSL` (fail-on-HTTP-error) did not trip: the live page is served with 200 today, so the recheck signal is not a swallowed error.
  (The entry's `recheck:` line records the date but not the HTTP status; the count alone cannot distinguish "phrase present" from
  "page replaced by an error page that still contains the phrase" — not observed here.)

## SPAN TABLE:

Helper: `python3 -B .ufo/waves/round-57/span_tools.py check S421 '<span>'` (v1 window). Because the assignment notes the v2 text-node rule
is stricter, each row also records whether the occurrence lies inside a tag / `<script>`/`<style>` (my own mask over the retained body).
All 22 blockquoted spans plus the cited heading, **re-run now**:

| units | chars | raw | in_content | count | tag/script | span |
|---|---|---|---|---|---|---|
| 12 | 13 | True | True | 1 | no | 死链一般是指页面已经无效， |
| 17 | 17 | True | True | 1 | no | 无法对用户提供任何有价值信息的页面 |
| 9 | 9 | True | True | 1 | no | 协议死链和内容死链 |
| 16 | 25 | True | True | 1 | no | 的TCP协议状态/HTTP协议状态明确表示的死链， |
| 7 | 18 | True | True | 1 | no | 常见的如403、404、503状态等 |
| 12 | 13 | True | True | 1 | no | 服务器返回状态是正常的，但 |
| 10 | 11 | True | True | 1 | no | 内容已经变更为不存在、 |
| 8 | 8 | True | True | 1 | no | 已删除或需要权限 |
| 12 | 12 | True | True | 1 | no | 等与原内容无关的信息页面 |
| 9 | 16 | True | True | 1 | no | 服务器端返回HTTP状态码200 |
| 5 | 8 | True | True | 1 | no | 无法设置为404 |
| 24 | 26 | True | True | 1 | no | 百度蜘蛛会定期检测网站页面内容价值，若存在大量死链， |
| 8 | 8 | True | True | 1 | no | 影响网站整体评价 |
| 8 | 8 | True | True | 1 | no | 搜索资源平台工具 |
| 6 | 6 | True | True | 1 | no | 抓取异常工具 |
| 18 | 19 | True | True | 1 | no | 可以查看最近产生的死链，且支持导出功能 |
| 10 | 13 | True | True | 1 | no | 发现后需要及时做404处理 |
| 11 | 14 | True | True | 1 | no | 将需处理的页面设置404页面 |
| 9 | 16 | True | True | 1 | no | 页面设置404，一定是404页面 |
| 3 | 7 | True | True | 1 | no | 仅识别404， |
| 6 | 9 | True | True | 1 | no | 请一定设置为404 |
| 19 | 23 | True | True | 1 | no | 若存在非404资源，可能会影响整个文件生效情况 |
| 5 | 5 | True | True | 1 | no | 一、了解死链 (cited at entry line 8 as `check S421 '一、了解死链'` -> count 1) |

- **Violations: none.** Every span is a raw substring, occurs exactly once in the page, sits inside the article block, is in a text node
  (never in a tag, `<script>` or `<style>`), is absent from S422, is ≤ 25 units (max 24) and ≤ 40 characters (max 26).
- Weakest margin: `百度蜘蛛会定期检测网站页面内容价值，若存在大量死链，` = 24 units / 26 chars — one unit under the ceiling.
- Entry-internal emphases re-checked as substrings too (not quotes, for completeness): `一般是指` 4u/1 occurrence, `明确表示` 4u/1,
  `页面的` 3u/1, `常见的如` 4u/1, `定期` 2, `大量` 2, `可能会` 3, `一定是` 3, `【死链提交】` 8 — all raw, all in the article block.
  `抓取异常` (4u) occurs twice in the page, so it would not be page-unique as a span; the entry quotes `抓取异常工具` (6u, 1 occurrence)
  instead — the counter's page-uniqueness rule is satisfied by the form actually used.

## ROW CHECK:

Re-derived from `git show 4b8c73050470ada9e6583f3b12d659d1bed6a17f:corpus/SOURCES.md` (row at line 167; 160 `| S###` rows in the file;
exactly one `| S421 ` row):

- **Cells: 11** — `S421` · source · `docs` · `A` · scope · anchor · teaches · `mined` · `2026-10-25` · `180d` ·
  `corpus/knowledge/baidu-dead-link-types.md`.
- **Title between first and last ` — `**: first ` — ` at index 8, last at index 31 → `搜索问答剧场 【六】“死链”常见问题解析`.
  Page `<title>` = `搜索问答剧场 【六】“死链”常见问题解析_搜索学堂_百度搜索资源平台`; text before the first `_` =
  `搜索问答剧场 【六】“死链”常见问题解析` (15 units, raw substring, at offset 322 in `<title>` and again inside the article `<h3>` at 9391).
  Equality: **True** (confirmed by running).
- **`发布日期：<date>` printed in the page**: page text node at offset 9443 (inside the article block, not in a tag) prints
  `发布日期：2022-09-09`. Row anchor cell: `§ 一、了解死链 (发布日期 2022-09-09)` — date equal; the row renders the page's fullwidth
  colon `：` as a space, which the contract's C3 note explicitly accepts ("the page's own fullwidth-colon form is accepted in the row").
- **Anchor heading occurs once**: `一、了解死链` count in body = **1** (offset 10037, inside `<h2>` text node inside the article block;
  not inside any tag). Entry line 8's recorded `count_in_page 1` reproduces.
- Row `recheck` `180d` equals the entry's `recheck: 180d`; row `used-by` names exactly the entry; row `status` `mined`;
  row `opened` `2026-10-25` equals the entry's `verified-at`.

## Findings (freshness lens, each names its artifact)

1. **Confirmed by running — no freshness failure found.** Live GET 200, article block byte-identical, recheck count 1 live and 1 over the
   retained body, all 23 checked spans raw/unique/in-content/text-node/under both ceilings, row re-derives to 11 cells with a matching
   title, date and single anchor heading.
2. **Confirmed by running — pins are not refetch-reproducible** (`.ufo/waves/round-57/w2/ExecReopenS421.files/S421.refetch.diff.txt`
   vs `.ufo/waves/round-57/sources/receipts.json`): the 3 differing lines are CDN cache-busters and a passport port in the script region.
   Anyone treating `receipts.json`'s sha256 as "the page's digest" will see a false mismatch; it is a digest of one fetch.
3. **Confirmed by running — entry line 8 prose nit** (`corpus/knowledge/baidu-dead-link-types.md:8`): it says "the title's remaining
   words, 死链 and 常见问题解析, sit between curly quotation marks". The printed title is `“死链”常见问题解析` — only `死链` is between the
   curly quotes; `常见问题解析` follows the closing quote. The row's title cell is unaffected (it reproduces the title exactly, quotes included).
   This is outside what C3's counter tests (it compares the row title to the page title, not the prose), so it is a drafting-accuracy note,
   not a counter hole.
4. **Not run:** `c57_quote_truth.py` itself (C3's counter — other seats own the measurement), and any second GET for stability. `[INFERENCE]`
   a second GET would very likely differ in the same script lines again; I did not measure that.

## Risks / limits of this seat

- One GET only; today's page could differ from the contract-day page in ways both fetches share (both are post-contract fetches) — the
  retained body is itself a fetch, so "unchanged since retention" is all that is shown.
- The `发布日期` render `(发布日期 2022-09-09)` depends on the counter's documented acceptance; if that acceptance were tightened to a
  literal `发布日期：2022-09-09`, the row would need a one-character edit. Read as accepted, per contract § Counter versions (C3 v2).
- span_tools is the v1 window helper; the stricter v2 text-node rule I approximated with my own tag/`<script>` mask over the retained
  body. No span fell in a tag or script under that mask.

VERDICT: C3 freshness holds at 4b8c730 for S421 — live GET 200, article block byte-identical to the retained body, recheck counts 1/1, all 23 spans raw/unique/text-node/≤25u/≤40ch, row re-derives to 11 cells with matching title, printed date and a page-unique anchor heading; only script-region cache-busters differ.
