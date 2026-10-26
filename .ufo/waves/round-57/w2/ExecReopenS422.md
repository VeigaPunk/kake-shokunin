# ExecReopenS422

Claim C3 (freshness: the row's source is re-opened and the recheck runs). Build under attack: lane revision
`4b8c73050470ada9e6583f3b12d659d1bed6a17f`. The working-tree entry is byte-identical to that revision
(`git show 4b8c730…:corpus/knowledge/baidu-spider3-dead-link-model.md` vs the working file, sha256
`40df6c8c…` both, `diff` empty), so every line quoted below is the revision's text. All checks below were run by
this seat unless marked `[INFERENCE]` or `unrun`.

## FETCH:

Command, exactly as assigned (one GET), 2026-10-25 21:25 local:
`curl -sS -L --compressed -A kake-shokunin-round57-w2 -o <tmp> -w '%{http_code} %{url_effective} %{size_download}' https://ziyuan.baidu.com/wiki/867`

- stdout: `200 https://ziyuan.baidu.com/wiki/867 9944` — confirmed by running.
- The `9944` is the *transferred* (gzip) size; `%{size_download}` counts wire bytes under `--compressed`. The
  decoded body written to disk is **27327 bytes**, identical in size to the retained body and to `receipts.json`'s
  `bytes: 27327` — confirmed by running (`wc -c`, `ls -l`).
- Saved at `.ufo/waves/round-57/w2/ExecReopenS422.files/S422.live.html` (27327 bytes).
- sha256 live `66440e1518d2ea9c834dedf13c45976472a6a12cd52943dbdfc5660c8b844a19`;
  retained `.ufo/waves/round-57/sources/S422.html` `7cf2e27dc7e6dcba4e7bbeba09ed6f23a7c6322dc2a377e3cd36dee8c1de71ff`
  (= `receipts.json` `S422.sha256`, = the counter's frozen `BODY_SHA256`) — confirmed by running.

## EQUAL TO RETAINED:

**Not equal byte-for-byte.** `cmp` reports first difference at char 18275 (line 318); `diff -u` yields 6 changed
lines in 2 hunks, and the whole of it is in the page-level script / login-config region, *below* the footer:

| line | offset | retained | live |
|---|---|---|---|
| 318 | 14912 | `uni_login_wrapper.js?cdnversion=202610260738` | `…?cdnversion=202610260825` |
| 319 | 15019 | `wrapper.js?cdnversion=1792971515` | `…?cdnversion=1792974343` |
| 333 | 15437 | `passreg` … `ziyuan.baidu.com%3A8087%2F` | … `ziyuan.baidu.com%3A8054%2F` |

Region named: **header/footer script block, not the article block.** Anchors: `class="info-item-time"` at 9199
(line 274), `class="zz_dldes_content` at 9247 (line 275), `class="footer"` at 13061 (line 290);
`wiki-foot-right` at 12939. All three differing lines sit at offsets > 13061, i.e. after the page footer.

- Article block, counter v2 bounds `[info-item-time .. wiki-foot-right)` = offsets 9199–12939, 3740 bytes:
  **byte-identical** in both bodies (sha256 `a4d6bbe55a8fbfee…`) — confirmed by running.
- Article container `zz_dldes_content .. footer` = 9247–13061: sha256 `a4d6bbe55a8fbfee…`, **6272 bytes, identical**
  in both — confirmed by running.
- `class="article-info"` does not occur in S422 (S421 locator only), as the counter's locator table states.

Consequence for the freshness claim: the *content* the entry quotes is unchanged after re-opening; only rotating
CDN cache-buster tokens and one login-form port moved. Practical risk (finding, `[INFERENCE]` — not measured by me):
the counter's `BODY_SHA256` pin at `c57_quote_truth.py:94` is satisfied only by the retained artifact. A future
re-fetch cannot reproduce `7cf2e27d…` while the passport script tokens rotate, so a whole-body byte pin is not
reproducible live; the entry's *grep* recheck is stable because it targets the article block.

## RECHECK RUNS:

1. Entry line 3, curl arm, run verbatim:
   `curl -fsSL --compressed 'https://ziyuan.baidu.com/wiki/867' | grep -F -c '能识别协议死链，以及大多数内容死链、跳转死链等低质网页'`
   → **1**, curl exit status 0 — confirmed by running. (The entry's line-3 parenthetical says "curl arm unrun
   this round"; it is run here and agrees.)
2. grep arm against the retained body: `grep -F -c '<same span>' .ufo/waves/round-57/sources/S422.html` → **1**.
3. Same grep against today's live body (`…w2/ExecReopenS422.files/S422.live.html`) → **1**.

Both counts printed: **1 and 1**. The recheck predicate (`-> 1`) holds today.

## SPAN TABLE:

All 11 quoted CJK spans in `corpus/knowledge/baidu-spider3-dead-link-model.md` were re-run through
`python3 -B .ufo/waves/round-57/span_tools.py check S422 <span>`. Columns: helper output
(`units`/`raw_substring`/`in_content`/`count_in_page`) plus a v2 cross-check I ran myself (span inside the v2
block 9199–12939 and inside a text node, i.e. not inside a tag/attribute/`<style>`/`<script>`).

| entry line | units | chars | raw | in_content | count | v2 text-node | span |
|---|---|---|---|---|---|---|---|
| 12 | 12 | 12 | True | True | 1 | True | 启用了全新的死链识别模型 |
| 16 | **25** | 27 | True | True | 1 | True | 能识别协议死链，以及大多数内容死链、跳转死链等低质网页 |
| 22 | 16 | 17 | True | True | 1 | True | 死链处理更及时—被黑低质页面全屏蔽 |
| 28 | 12 | 12 | True | True | 1 | True | 简单点说就是在之前的版本 |
| 29 | 12 | 12 | True | True | 1 | True | 站点通过站长平台提交死链 |
| 30 | 9 | 9 | True | True | 1 | True | 处理速度可能非常慢 |
| 31 | 14 | 14 | True | True | 1 | True | 甚至快照在一段时间内仍然存在 |
| 35 | 15 | 16 | True | True | 1 | True | 更新后，大约几天内就可以处理掉了 |
| 41 | 24 | 26 | True | True | 1 | True | 当然，如果你要追求最佳处理效果，协议死链是最好的选择 |
| 49 | 12 | 13 | True | True | 1 | True | 索引展现时效性提升，原来是 |
| 53 | 7 | 8 | True | True | 1 | True | 天左右，现在提升 |

- Every span: helper `in_other_adopted_body` False (unique against S421) — confirmed by running.
- Ceilings: max 25 units (line 16, exactly at the ceiling, not over), max 27 characters — the entry's own
  "longest span quoted here is 27 characters" is accurate. All ≤ 25 units and ≤ 40 chars.
- No span contains `<`, so none crosses an inline `<span lang=EN-US>` tag (entry's claim) — confirmed by running.
- Nothing unrun in this table: all 11 spans checked.

## ROW CHECK:

Row re-derived read-only from `git show 4b8c73050470ada9e6583f3b12d659d1bed6a17f:corpus/SOURCES.md`
(`grep -n 'S422'` → line 168, exactly one such row; the registry holds 160 `| S…` rows at that revision).

- **11 cells** — confirmed by running: `S422 | 百度搜索资源平台 — 百度搜索Spider3.0升级对站点有什么好处 — https://ziyuan.baidu.com/wiki/867 | docs | A | <scope> | § 死链处理更及时—被黑低质页面全屏蔽 (发布日期 2016-06-30) | <teaches> | mined | 2026-10-25 | 180d | corpus/knowledge/baidu-spider3-dead-link-model.md`.
- **Title**: text between the first and the last ` — ` of cell 2 = `百度搜索Spider3.0升级对站点有什么好处`;
  page `<title>` = `百度搜索Spider3.0升级对站点有什么好处_搜索资讯_百度搜索资源平台`, text before the `_`
  suffix is the same string — **match** (confirmed by running).
- **Date**: the page prints `发布日期：2016-06-30` exactly once, in a text node (offset not inside any
  `<script>`/`<style>`, outside a tag) — confirmed by running. The row records the date as
  `(发布日期 2016-06-30)` (ASCII space instead of the page's fullwidth colon); date value equal, form not
  byte-identical to the page — noted, matches the contract's "fullwidth-colon form is accepted in the row" wording.
- **Anchor heading**: `死链处理更及时—被黑低质页面全屏蔽` occurs **once** in the retained body, in a text node, and
  0 times in S421; the row's `§` cell carries exactly that heading — confirmed by running.
- Also consistent: `status=mined`, `opened=2026-10-25`, `recheck=180d` = entry line 3's `180d`, `used-by` = the
  entry path (C4's one-to-one mapping).

## Notes, risks, blockers

- Files written: this report and `.ufo/waves/round-57/w2/ExecReopenS422.files/S422.live.html` only. No git/index/jj
  mutation, no pacman, no tool installs (none needed).
- Not run (out of assignment scope, reported as unrun): `c57_quote_truth.py` itself; the counter's `BODY_SHA256`
  behaviour against a fresh body was inferred from code reading, not measured.
- Risk to hand to L1: source drift on re-fetch is confined to rotating passport CDN versions and a login port, so
  C3's quote truth is stable while its whole-body digest pin is not reproducible from the live URL. If a later
  wave re-fetches and pins `receipts.json`, expect the 3-line delta, not content change.
- No blocker.

VERDICT: S422 re-opens (HTTP 200), differs from the retained body only in 3 non-article script/port lines, its recheck prints 1 vs 1, all 11 quoted spans pass units/raw/in_content/count and the v2 text-node rule, and the registry row re-derives correctly (11 cells, title/date/anchor match).
