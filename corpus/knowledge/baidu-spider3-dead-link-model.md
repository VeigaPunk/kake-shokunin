source: S422 — https://ziyuan.baidu.com/wiki/867 — § 死链处理更及时—被黑低质页面全屏蔽 (发布日期 2016-06-30) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — curl -fsSL --compressed 'https://ziyuan.baidu.com/wiki/867' | grep -F -c '能识别协议死链，以及大多数内容死链、跳转死链等低质网页' -> 1 (curl arm unrun this round; the same grep against the retained round-57 body prints 1, 2026-10-25)
ground: per-engine crawl hygiene — what the operator says its Spider3.0 dead-link recognition model recognises, the processing time it states for a submitted dead link before and after the update, and the one kind it names as the best choice

# Baidu's Spider3.0 dead-link recognition model: scope, processing timing and the best-choice preference

The lane holds what an error status does to a crawl on Googlebot's side (`corpus/knowledge/crawl-error-status-table.md`, S286), and what another operator's pages say about a deleted URL and about a URL that never existed (`corpus/knowledge/yahoo-japan-deleted-url-recrawl.md`, S419; `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md`, S420). None of those entries states what Baidu's crawler recognises as a dead link. This page states it in one paragraph under a labelled section, and the label claims more than the paragraph develops [S422].

## The model, and the exact scope it claims

> "启用了全新的死链识别模型"

(rendered: it has enabled a brand-new dead-link recognition model; the subject is Spider3.0, named immediately before this run of text, and 全新 is new, not merely newer). The page prints its publication date as 2016-06-30, so the claim is dated from 2016, not from the fetch [S422].

> "能识别协议死链，以及大多数内容死链、跳转死链等低质网页"

(rendered: it can recognise protocol dead links, and most content dead links, redirect dead links and other low-quality pages). Two qualifiers decide how far the sentence reaches: 大多数 (most) scopes the group after 以及, so protocol dead links are named without a quantifier while content dead links, redirect dead links and the other low-quality kinds are named only in the majority; and 跳转死链 (redirect dead links) is a third named kind of its own, not a restatement of either of the other two. The page names all three kinds and defines none of them here: 404 and 状态码 occur zero times in the retained body (`grep -o -F '404' .ufo/waves/round-57/sources/S422.html | wc -l` -> 0, 2026-10-25), and the only other mention of 协议死链 on the page is the preference quoted below.

## The label states two things; the paragraph develops one

> "死链处理更及时—被黑低质页面全屏蔽"

(rendered: dead-link handling is more timely — hacked low-quality pages are fully blocked). The second half is not developed: 屏蔽 (block) occurs once in the whole body, inside this label (`grep -o -F '屏蔽' .ufo/waves/round-57/sources/S422.html | wc -l` -> 1, 2026-10-25), and the paragraph under it speaks about dead-link recognition and processing time only [S422]. This entry therefore carries the label as the section anchor and claims no blocking rule from it.

## The timing, and the version it is compared against

> "简单点说就是在之前的版本"
> "站点通过站长平台提交死链"
> "处理速度可能非常慢"
> "甚至快照在一段时间内仍然存在"

(rendered: to put it simply, in the earlier version a site submitted dead links through the webmaster platform, the processing speed could be very slow, and the snapshot might even remain for a period of time). Three qualifiers hold the prior-version account: 可能 (could) makes the slow processing a possibility, 甚至 (even) makes the lingering snapshot an extreme case, and the submission channel named is the platform, 站长平台.

> "更新后，大约几天内就可以处理掉了"

(rendered: after the update, they can be handled within about a few days). 大约 (about) qualifies the few days, and the verb is 处理 (handle), not a removal from an index and not a deletion. The page does not say the platform submission became unnecessary, and it does not restate the majority qualifier in this sentence, so the few-days statement is not scoped per kind [S422]; [INFERENCE] the lane reads it as covering the kinds the model recognises, since it follows that scope sentence directly, and the page states no per-kind rate.

## The best-choice preference

> "当然，如果你要追求最佳处理效果，协议死链是最好的选择"

(rendered: of course, if you want to pursue the best processing result, a protocol dead link is the best choice). The page frames this as a preference under a stated goal (最佳处理效果, the best processing result); it does not say the other recognised kinds fail, are rejected, or go unhandled.

## Where the index-display figure sits

The 10-day and 40%~80% numbers on this page are not in the dead-link section: they sit in the earlier paragraph on link fetching and index building, in the sentence whose head is

> "索引展现时效性提升，原来是"

(rendered: index display timeliness has improved; previously it was) and whose continuation is

> "天左右，现在提升"

(rendered: about [10] days, now improved by [40%~80%]). The digits sit inside inline spans, so they are described here and not quoted [S422]. The figure is about how soon a page is displayed to a search user after fetching and index building; the page attaches no dead-link handling time to it. The staged candidate this entry replaces (shokuknow `merge/kake/`, the staging row for this page, whose id and file name are not reused here) attached a 10-day-to-40-80% improvement to dead-link handling; read against the retained body, that placement is wrong, and the staged Gate quote is 37 units, over the 25-unit ceiling.

## What the page does not say

- It does not say a recognised dead link is removed from the index: 删除, 移除 and 下线 occur zero times in the retained body, and the article block's only 索引 occurrences are the two in the index-display sentence above (the body's third 索引 is the navigation link 索引量, which sits outside the article block).
- It prints no status code and no HTTP term for any of the three kinds; the recognition claim is a model claim, not a response-code claim.
- It states no rate, no percentage and no measurement for dead-link handling; the percentages on the page belong to the fetching, index-building and submission sections.
- It does not say how a publisher learns that a dead link was recognised: the paragraph names no report, no tool and no status.

## The lane's inference, tagged

[INFERENCE] A page the model recognises is not thereby visible to a status-code check: the lane reads the model claim and the absence of any status-code claim as two separate statements, so a content or redirect dead link can answer normally and still be recognised. The page states neither half of that reading. The staged candidate asserted it untagged; this entry tags it.

## Cross-links, and the contrast this entry does not state

Status-code layer: `corpus/knowledge/crawl-error-status-table.md` (S286). Other operator, deleted URL and never-existent URL: `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` (S419) and `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` (S420). Other Baidu statements held by the lane: `corpus/knowledge/baidu-friendly-crawl-guidance.md` (S329) and `corpus/knowledge/baidu-mobile-matching-error-causes.md` (S312). No cross-engine contrast is stated here: the lane admits one only where both sides are quoted from the held entries, and this entry quotes S422 alone, so the comparison belongs to a reading that quotes both.

## Quote classes

Each quotation is a raw substring of `.ufo/waves/round-57/sources/S422.html` (sha256 7cf2e27dc7e6dcba4e7bbeba09ed6f23a7c6322dc2a377e3cd36dee8c1de71ff, 27327 bytes, HTTP 200 in `.ufo/waves/round-57/sources/receipts.json`), occurs once in that body and in no other retained body, sits inside the article block (the container class `zz_dldes_content` through the page footer), and is at most 25 units under the round-57 rule (one unit per CJK character, so CJK punctuation costs 0, plus one per non-CJK whitespace token) and at most 40 characters (the longest span quoted here is 27 characters). No quoted span crosses an inline `span lang=EN-US` tag.

Page-silence sweeps (2026-10-25, over `.ufo/waves/round-57/sources/S422.html`): `grep -o -F '删除' | wc -l` -> 0, `grep -o -F '移除' | wc -l` -> 0, `grep -o -F '下线' | wc -l` -> 0, `grep -o -F '状态码' | wc -l` -> 0, `grep -o -F '404' | wc -l` -> 0, `grep -o -F '屏蔽' | wc -l` -> 1.

Scope note: a claim about what the operator's page states; no URL was served under test for this lane, no crawl was observed and no Baidu behaviour was measured.
