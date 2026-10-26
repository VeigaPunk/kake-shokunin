# EntryDeadLinkTypes

## ENTRY:

```markdown
source: S421 — https://ziyuan.baidu.com/college/articleinfo?id=3458 — § 一、了解死链 (发布日期 2022-09-09) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL --compressed 'https://ziyuan.baidu.com/college/articleinfo?id=3458' | grep -F -c '协议死链和内容死链'` -> 1 (grep against the retained body 1, 2026-10-25)
ground: per-engine crawl hygiene — how Baidu's own page defines a dead link, splits it into protocol and content kinds, and what the content kind answers with

# Baidu separates dead links into protocol dead links and content dead links; the content kind answers 200

Baidu's college page prints the title `搜索问答剧场 【六】“死链”常见问题解析` (with the space inside the printed title) and answers developer questions about dead links (死链). The Q&A opens under the heading `一、了解死链` with the two kinds [S421] (`python3 -B .ufo/waves/round-57/span_tools.py check S421 '一、了解死链'` -> count_in_page 1, raw substring, 2026-10-25).

## The two kinds of dead link

The definition sentence names the criterion first, with the hedge 一般是指 (generally means) [S421]:

> "死链一般是指页面已经无效，"
> "无法对用户提供任何有价值信息的页面"

(rendered: a dead link generally means a page that is already invalid, a page that cannot offer users any valuable information — 一般是指 is a general meaning, not a strict equivalence.)

The page then divides dead links into two kinds [S421]:

> "协议死链和内容死链"

(rendered: protocol dead links and content dead links.)

### Protocol dead link

> "的TCP协议状态/HTTP协议状态明确表示的死链，"

(rendered: a dead link clearly indicated by the page's TCP protocol status / HTTP protocol status — the qualifiers are 明确表示 (clearly indicated) and 页面的 (of the page).)

> "常见的如403、404、503状态等"

(rendered: common ones such as the 403, 404 and 503 statuses — 常见的如 and 等 keep the list exemplary, not exhaustive.)

### Content dead link

> "服务器返回状态是正常的，但"
> "内容已经变更为不存在、"
> "已删除或需要权限"
> "等与原内容无关的信息页面"

(rendered: the server's return state is normal, but the content has changed to nonexistent, deleted or requiring permission — an information page unrelated to the original content; 或 (or) keeps the three reasons alternative, and 等 (etc.) keeps the list non-exhaustive.)

What the content kind answers — the page's own words [S421]:

> "服务器端返回HTTP状态码200"
> "无法设置为404"

(rendered: the server side returns HTTP status code 200, and it cannot be set to 404 — 无法设置为404 is a stated impossibility, not a recommendation.) This answers the staged candidate's assertion (b): the content dead link indeed returns HTTP 200 and cannot be set to 404 [S421].

## The crawler's own check, and how the page says dead links are found

The page states Baiduspider periodically checks page content value [S421]:

> "百度蜘蛛会定期检测网站页面内容价值，若存在大量死链，"
> "影响网站整体评价"

(rendered: Baiduspider regularly tests the site's page content value; if a large number of dead links exist, it may affect the site's overall evaluation — 定期 is regular, 大量 is a large number, and the consequence is hedged with 可能会 (may).)

The page's discovery methods are the 搜索资源平台 tool's 抓取异常 tool and crawler software [S421]:

> "搜索资源平台工具"
> "抓取异常工具"
> "可以查看最近产生的死链，且支持导出功能"

(rendered: the search-resource-platform tool's fetch-abnormality tool can view recently produced dead links and supports export; crawler software is named as the second method — the page does not describe either as status-code-only.)

[INFERENCE] Because the page states a content dead link answers HTTP 200 and cannot be set to 404 [S421], a reader that only reads status codes sees a normal page for it; that conclusion is the lane's inference, not a statement of the page. The page's own discovery tools are named above, not described as status-code-only.

## The remedies the page states

For a wrong content link added internally, the page says timely 404 handling is needed [S421]:

> "发现后需要及时做404处理"

(rendered: after discovery, timely 404 handling is needed.)

The handling section tells the publisher to set the page to a 404 page and to be sure it is a 404 page [S421]:

> "将需处理的页面设置404页面"
> "页面设置404，一定是404页面"

(rendered: set the pages to be processed to a 404 page; setting a page to 404, it must be a 404 page — 一定是 is a must, not a suggestion.) The 【死链提交】 tool only recognises 404, and non-404 resources can affect the whole file's effect [S421]:

> "仅识别404，"
> "请一定设置为404"
> "若存在非404资源，可能会影响整个文件生效情况"

(rendered: the tool only recognises 404 — please be sure to set it to 404; if non-404 resources exist, the whole file's effect may be affected.)

The staged candidate's assertion (c) said the remedy is "remove the path from internal links, or make the route answer a real 404". The page states the second half (set the page to 404) but states nothing about removing a path from internal links; that half is not carried [S421].

## Cross-engine contrast

Both sides are quoted from the held entries. The Yahoo! JAPAN deletion entry holds `クローラーは削除されたウェブページと認識できず、` (rendered: the crawler cannot recognise the deleted web page) and asks the publisher to confirm a 404 setting (S419); its nonexistent-URL sibling holds `巡回を続けます` (rendered: it continues the crawl) when a nonexistent URL answers 200 (S420). [S421] states the content dead link answers 200 and cannot be set to 404, and its remedy is the 【死链提交】 workflow — so where the Yahoo pages remedy a 200-returning page by a server-status or meta-tag change, the Baidu page states that change is unavailable for the content kind and routes handling through the submission tool. The Google-side entry `corpus/knowledge/crawl-error-status-table.md` (S286) admits one sentence (Googlebot scales back when servers are detected to have trouble); [S421] states no rate or backoff effect.

## What this entry does not establish

- No URL was served under test, no crawl was observed, and no Baidu behavior was measured; the entry states what the operator's page says (see Scope note).
- The page states no definition of a “monitor” or “link checker”, and no claim that any tool cannot see a content dead link.
- The page states the 1–2 week effect cycle of submissions and the file-placement steps; they are operational mechanics and are not carried here.
- The page is one page of the operator's info centre; its statements bind nothing beyond what is quoted.

Scope note: a claim about what the operator's page states on one page of its info centre; no URL served under test, no crawl observed, no Baidu behavior measured.
```
## GATE LINE:
`- S421 — https://ziyuan.baidu.com/college/articleinfo?id=3458 — accessed 2026-10-25 — § 一、了解死链 (发布日期 2022-09-09) — quote: "协议死链和内容死链" (9 units; raw substring of the retained body, sha256 32eaf8b74012c99dff8ae6cc3db0658d3f7520b04045336b8228461dab447182, 34750 bytes, HTTP 200)`
## COVERAGE ROW:

`| Baidu dead-link types | `knowledge/baidu-dead-link-types.md` (S421) | protocol/content kinds, 200 answer, 404 submission workflow, Baiduspider periodic check |`
## REGISTRY ROW:

`| S421 | 百度搜索资源平台 — 搜索问答剧场 【六】“死链”常见问题解析 — https://ziyuan.baidu.com/college/articleinfo?id=3458 | docs | A | **Two dead-link kinds: protocol shows 403/404/503, content answers 200** — the operator's split of dead links and the content kind's characteristic answer, plus the 404-set submission workflow | § 一、了解死链 (发布日期 2022-09-09) | a content dead link answers HTTP 200 and cannot be set to 404, so finding and handling dead links goes through the operator's dead-link submission workflow | mined | 2026-10-25 | 180d | corpus/knowledge/baidu-dead-link-types.md |`
## UNIT COUNTS:
Units per quote (unit rule: one unit per CJK character, one per non-CJK whitespace token), from `span_tools.py check`; all spans <= 25 units and <= 40 characters (longest 24 units / 26 chars):

| quote | u | c | quote | u | c |
|---|---|---|---|---|---|
| 死链一般是指页面已经无效， | 12 | 13 | 无法对用户提供任何有价值信息的页面 | 17 | 17 |
| 协议死链和内容死链 | 9 | 9 | 的TCP协议状态/HTTP协议状态明确表示的死链， | 16 | 25 |
| 常见的如403、404、503状态等 | 7 | 18 | 服务器返回状态是正常的，但 | 12 | 13 |
| 内容已经变更为不存在、 | 10 | 11 | 已删除或需要权限 | 8 | 8 |
| 等与原内容无关的信息页面 | 12 | 12 | 服务器端返回HTTP状态码200 | 9 | 16 |
| 无法设置为404 | 5 | 8 | 发现后需要及时做404处理 | 10 | 13 |
| 将需处理的页面设置404页面 | 11 | 14 | 页面设置404，一定是404页面 | 9 | 16 |
| 仅识别404， | 3 | 7 | 请一定设置为404 | 6 | 9 |
| 若存在非404资源，可能会影响整个文件生效情况 | 19 | 23 | 百度蜘蛛会定期检测网站页面内容价值，若存在大量死链， | 24 | 26 |
| 影响网站整体评价 | 8 | 8 | 搜索资源平台工具 | 8 | 8 |
| 抓取异常工具 | 6 | 6 | 可以查看最近产生的死链，且支持导出功能 | 18 | 19 |
## UNIQUE SPANS:
Page-unique spans used (all `count_in_page: 1`, `raw_substring: True`, `in_content: True`, from `span_tools.py check S421`):

`死链一般是指页面已经无效，` `无法对用户提供任何有价值信息的页面` `协议死链和内容死链` `的TCP协议状态/HTTP协议状态明确表示的死链，` `常见的如403、404、503状态等` `服务器返回状态是正常的，但` `内容已经变更为不存在、` `已删除或需要权限` `等与原内容无关的信息页面` `服务器端返回HTTP状态码200` `无法设置为404` `发现后需要及时做404处理` `将需处理的页面设置404页面` `页面设置404，一定是404页面` `仅识别404，` `请一定设置为404` `若存在非404资源，可能会影响整个文件生效情况` `百度蜘蛛会定期检测网站页面内容价值，若存在大量死链，` `影响网站整体评价` `搜索资源平台工具` `抓取异常工具` `可以查看最近产生的死链，且支持导出功能`

Also verified, not used as quotes: `一、了解死链` (5 units, count 1); printed title `搜索问答剧场 【六】“死链”常见问题解析` (15 units, count 3, raw substring); heading `搜索问答剧场 【六】“死链”常见问题解析_搜索学堂_百度搜索资源平台` is in `<title>` only and NOT in the retained body content (`in_content: False`), which is why the registry cell uses the printed title.
## RECHECK RUN:
Command (grep form against the RETAINED body): `grep -F -c '协议死链和内容死链' .ufo/waves/round-57/sources/S421.html` -> printed `1`. The 180d form for the header is `curl -fsSL --compressed 'https://ziyuan.baidu.com/college/articleinfo?id=3458' | grep -F -c '协议死链和内容死链'`; the curl arm was not run (no fetch required this lane; the retained body is the evidence).
## OMITTED:
- Staged candidate (c)'s first half "remove the path from internal links": the page states the 404-page setting and the 【死链提交】 workflow, but no statement about removing a path from internal links; dropped as ungrounded (the second half is carried).
- Q2 genesis details (server instability, external wrong URLs, incomplete URLs extracted by crawlers, site-redesign legacy-domain deletion): about how dead links arise, not the types or the content kind's answer; only `发现后需要及时做404处理` is carried.
- Tool workflow steps beyond the 404 setting (placing the dead-link file in the site root, site verification, submission, status monitoring, the 1–2 week effect cycle, indexing-type files): operational mechanics, out of the types/answers scope.
- "Why handle" items other than the crawler check (management cost; exposure in search results affecting the visit experience): rationale beyond the crawler statement; omitted.
- The `<title>` suffix `_搜索学堂_百度搜索资源平台` and the `推荐阅读` sidebar / 往期回顾 navigation: boilerplate not in the body's article content.
- Staged file name `baidu-dead-link-taxonomy.md` deliberately not reused; the lane entry is `baidu-dead-link-types.md`.
VERDICT: S421 entry drafted — two-type taxonomy, content-kind 200 answer, 404 submission workflow, Baiduspider check, all 22 quotes raw unique spans <= 25 units; gate/coverage/registry rows verified; inference (d) tagged; staged "remove path" remedy dropped.
