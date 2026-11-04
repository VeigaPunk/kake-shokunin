source: S421 — https://ziyuan.baidu.com/college/articleinfo?id=3458 — § 一、了解死链 (发布日期 2022-09-09), with quoted spans also from § 二 and § 三 — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL --compressed 'https://ziyuan.baidu.com/college/articleinfo?id=3458' | grep -F -c '协议死链和内容死链'` -> 1 (grep against the retained body 1, 2026-10-25)
ground: per-engine crawl hygiene — how Baidu's own page defines a dead link, which two kinds it says dead links include, and what the content kind answers with

# Baidu's page says dead links include protocol dead links and content dead links, and that the content kind answers 200

Baidu's college page prints a title that opens `搜索问答剧场 【六】` (with the space inside the printed title; then 死链 between curly quotation marks that this entry does not copy, then 常见问题解析 outside them) and answers developer questions about dead links (死链). The Q&A opens under the heading `一、了解死链` with the two kinds [S421] (`python3 -B .ufo/waves/round-57/span_tools.py check S421 '一、了解死链'` -> count_in_page 1, raw substring, 2026-10-25).

## The two kinds of dead link

The definition sentence names the criterion first, with the hedge 一般是指 (generally means) [S421]:

> "死链一般是指页面已经无效，"
> "无法对用户提供任何有价值信息的页面。包括"

(rendered: a dead link generally means a page that is already invalid, a page that cannot offer users any valuable information — 一般是指 is a general meaning, not a strict equivalence.)

The page's definition then names two kinds with 包括 (include), which introduces them rather than dividing the class exhaustively [S421]:

> "协议死链和内容死链"

(rendered: protocol dead links and content dead links.)

### Protocol dead link

> "的TCP协议状态/HTTP协议状态明确表示的死链，"

(rendered: a dead link clearly indicated by the page's TCP protocol status / HTTP protocol status — 明确表示 (clearly indicated) is inside the quoted span; 页面的 (of the page) sits in the text node before it, which ends 页面, and the span begins at its trailing 的, so 页面的 is the page's phrase but is inside no quotable span.)

> "常见的如403、404、503状态等"

(rendered: common ones such as the 403, 404 and 503 statuses — 常见的如 and 等 keep the list exemplary, not exhaustive.)

### Content dead link

> "服务器返回状态是正常的，但"
> "内容已经变更为不存在、"
> "已删除或需要权限"
> "等与原内容无关的信息页面"

(rendered: the server's return state is normal, but the content has changed to nonexistent, deleted or requiring permission — an information page unrelated to the original content; the page separates the three with 、 (不存在、已删除) and 或 (已删除或需要权限), and 等 (etc.) keeps the list non-exhaustive.)

What the content kind answers — the page's own words [S421]:

> "服务器端返回HTTP状态码200"
> "无法设置为404"

(rendered: the server side returns HTTP status code 200, and it cannot be set to 404 — 无法设置为404 is a stated impossibility, not a recommendation.) The sentence's subject is the content kind, not dead links in general: the page's own 内容死链 (raw, immediately before the quoted span) precedes it. The same page then tells the publisher, for content links wrongly added internally, 发现后需要及时做404处理 (§ 一) and 将需处理的页面设置404页面 (§ 二); this entry records both and does not reconcile them with 无法设置为404. The assertion (b) of the staging row for this page read that the content kind returns HTTP 200 and cannot be set to 404; that is the page's sentence [S421].

## The crawler's own check, and how the page says dead links are found

The page states Baiduspider periodically checks page content value [S421]:

> "百度蜘蛛会定期检测网站页面内容价值，若存在大量死链，"
> "影响网站整体评价"

(rendered: Baiduspider regularly tests the site's page content value; if a large number of dead links exist, it may affect the site's overall evaluation — 定期 is regular and 大量 is a large number.) The modal is the page's own: 可能会 (may) is a separate text node between the two quoted nodes and is inside neither span, so the two lines above do not read as one continuous quotation.

The page's discovery methods are the 搜索资源平台 tool's 抓取异常 tool and crawler software [S421]:

> "搜索资源平台工具"
> "抓取异常工具"
> "可以查看最近产生的死链，且支持导出功能"

(rendered: the search-resource-platform tool's fetch-abnormality tool can view recently produced dead links and supports export; crawler software is named as the second method — the page does not describe either as status-code-only.)

[INFERENCE] Because the page states a content dead link answers HTTP 200 and cannot be set to 404 [S421], a reader that only reads status codes sees a normal page for it; that conclusion is the lane's inference, not a statement of the page. The page's own discovery tools are named above, not described as status-code-only.

## The remedies the page states

For a wrong content link added internally, actively or passively (主动或被动; the page's own example is malicious injection), the page says timely 404 handling is needed [S421]:

> "发现后需要及时做404处理"

(rendered: after discovery, timely 404 handling is needed.)

The handling section (§ 二、教你如何处理死链页面) tells the publisher to set the page to a 404 page and to be sure it is a 404 page [S421]:

> "将需处理的页面设置404页面"
> "页面设置404，一定是404页面"

(rendered: set the pages to be processed to a 404 page; setting a page to 404, it must be a 404 page — 一定是 is a must, not a suggestion. The page's own instruction to build a dead-link file from the hacked or invalid resources to be deleted sits between the two quoted spans and is not quoted here.) In § 三、使用【死链提交】工具的注意事项 the page says the 【死链提交】 tool only recognises 404, and non-404 resources can affect the whole file's effect [S421]:

> "仅识别404，"
> "请一定设置为404"
> "若存在非404资源，可能会影响整个文件生效情况"

(rendered: the tool only recognises 404 — please be sure to set it to 404; if non-404 resources exist, the whole file's effect may be affected.)

The assertion (c) of the staging row for this page (shokuknow `merge/kake/`) said the remedy is to remove the path from the internal links or to make the route answer a real 404 (the candidate's wording, not the page's). The page states the second half (set the page to 404) but states nothing about removing a path from internal links; that half is not carried [S421].

## Cross-engine contrast

The Yahoo side is quoted from the held entries and the Baidu side from the retained body. The Yahoo! JAPAN deletion entry holds `クローラーは削除されたウェブページと認識できず、` (rendered: the crawler cannot recognise the deleted web page) (S419); its nonexistent-URL sibling holds `巡回を続けます` (rendered: it continues the crawl) (S420). Both Yahoo pages concern a URL the server is configured to answer with `HTTP 200 OK`; S419 asks the publisher to confirm whether the server is configured to return 404, and S420 asks for the setting to be made. [INFERENCE] [S421] states the same shape for Baidu (a content dead link answers 200) and three things about 404 that are not adjacent: the content kind cannot be set to 404 (§ 一), the publisher is told to set the pages to be processed to 404 (§ 二), and the submission tool recognises 404 only (§ 三). The page does not reconcile them, and this entry does not. The Google-side entry `corpus/knowledge/crawl-error-status-table.md` (S286) admits one sentence (Googlebot scales back when servers are detected to have trouble); [S421] states no rate or backoff effect.

## What this entry does not establish

- No URL was served under test, no crawl was observed, and no Baidu behavior was measured; the entry states what the operator's page says (see Scope note).
- The page states no definition of a monitor or a link checker, and no claim that any tool cannot see a content dead link. Page-silence sweeps (2026-10-25, `grep -o -F '<word>' .ufo/waves/round-57/sources/S421.html | wc -l`): 监控 0, 链接检查 0, 速率 0, 频率 0, 退避 0, 移除 0, 删除链接 0.
- The page states that a submitted dead link's effect cycle is generally (一般) 1–2 weeks, and the file-placement steps; they are operational mechanics and are not carried here.
- The page is one page of the operator's info centre; its statements bind nothing beyond what is quoted.

Scope note: a claim about what the operator's page states on one page of its info centre; no URL served under test, no crawl observed, no Baidu behavior measured.
