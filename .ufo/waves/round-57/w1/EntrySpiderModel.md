# EntrySpiderModel

Claim C3, new row **S422** (`https://ziyuan.baidu.com/wiki/867`, staged S408 → lane S422); entry drafted:
`corpus/knowledge/baidu-spider3-dead-link-model.md`. Every statement was re-grounded in the retained body
`.ufo/waves/round-57/sources/S422.html` (27327 bytes, sha256 `7cf2e27d…`, HTTP 200, `sources/receipts.json`); nothing is carried from the
shokuknow staging candidate and its file name is not reused. Page facts: `<h1>` = `百度搜索Spider3.0升级对站点有什么好处`; the page prints
`发布日期：2016-06-30` (count 1); the article block runs from container class `zz_dldes_content` to the page footer and contains **no
`<h2>`/`<h3>`/`<strong>`/`<b>`** — its section labels are the four `『…』` lines, so the anchor heading is the label
`死链处理更及时—被黑低质页面全屏蔽` (16 units, page-unique, occurs once).

## ENTRY:

```markdown
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

(rendered: about [10] days, now improved by [40%~80%]). The digits sit inside inline spans, so they are described here and not quoted [S422]. The figure is about how soon a page is displayed to a search user after fetching and index building; the page attaches no dead-link handling time to it. The staged candidate this entry replaces (shokuknow `merge/kake/`, staged row S408, whose file name is not reused here) attached a 10-day-to-40-80% improvement to dead-link handling; read against the retained body, that placement is wrong, and the staged Gate quote is 37 units, over the 25-unit ceiling.

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
```

## GATE LINE:

- S422 — https://ziyuan.baidu.com/wiki/867 — accessed 2026-10-25 — § 死链处理更及时—被黑低质页面全屏蔽 (发布日期 2016-06-30) — quote: "能识别协议死链，以及大多数内容死链、跳转死链等低质网页" (25 units; raw substring of the retained body, sha256 7cf2e27dc7e6dcba4e7bbeba09ed6f23a7c6322dc2a377e3cd36dee8c1de71ff, 27327 bytes, HTTP 200)

Checked with the counter's own extraction (`c57_quote_truth.py` C5): one double-quoted span, 25 units ≤ 25, 27 chars ≤ 40, raw substring, inside the
article block, `count_in_page == 1`, absent from S421, ASCII quotes only, URL and access date present.

## COVERAGE ROW:

| Baidu Spider3.0 dead-link recognition (r57) | `knowledge/baidu-spider3-dead-link-model.md` (S422) | recognition model scope, most-qualifier on content and redirect dead links, few-days processing timing, best-choice preference, index-display placement |

3 cells, no `|` inside a cell, 17 tokens in the Coverage cell; it shares seven 5+-letter words with the entry H1 (`recognition`, `model`, `scope`,
`processing`, `timing`, `preference`, `choice`).

## REGISTRY ROW:

| S422 | 百度搜索资源平台 — 百度搜索Spider3.0升级对站点有什么好处 — https://ziyuan.baidu.com/wiki/867 | docs | A | **Dead-link recognition scope and processing timing** — what the operator says its Spider3.0 dead-link model recognises (protocol dead links, and most content and redirect dead links and other low-quality pages), the processing time it states for a submitted dead link before and after the update, and the preference it states for protocol dead links | § 死链处理更及时—被黑低质页面全屏蔽 (发布日期 2016-06-30) | The operator states that Spider3.0 runs a new dead-link recognition model that recognises protocol dead links and most content, redirect and other low-quality pages, that a dead link submitted through the webmaster platform could take very long and leave a snapshot behind in the earlier version but is processed within about a few days after the update, and that a protocol dead link is the best choice for the best processing result | mined | 2026-10-25 | 180d | corpus/knowledge/baidu-spider3-dead-link-model.md |

Shape checked with the counter's `parse_registry`/`row_url`: 11 cells; `row_url` = the S422 URL; the text between the first and last ` — ` of cell 2 is
`百度搜索Spider3.0升级对站点有什么好处`, present in the retained body (`<h1>` and `<title>`); anchor extracted by
`row[5].split("§")[1].split(" (")[0]` = `死链处理更及时—被黑低质页面全屏蔽`, present; `发布日期 2016-06-30` present and the body prints
`发布日期：2016-06-30`; scope cell 350 chars, teaches cell 434 chars; no escaped pipe; status/opened/recheck as frozen.

## UNIT COUNTS:

Computed with `span_tools.py` (= the counter's `units()`: one unit per CJK character, one per non-CJK whitespace token; CJK punctuation costs 0).

units/chars per span: `启用了全新的死链识别模型` 12/12 · `能识别协议死链，以及大多数内容死链、跳转死链等低质网页` 25/27 ·
`死链处理更及时—被黑低质页面全屏蔽` 16/17 · `简单点说就是在之前的版本` 12/12 · `站点通过站长平台提交死链` 12/12 ·
`处理速度可能非常慢` 9/9 · `甚至快照在一段时间内仍然存在` 14/14 · `更新后，大约几天内就可以处理掉了` 15/16 ·
`当然，如果你要追求最佳处理效果，协议死链是最好的选择` 24/26 · `索引展现时效性提升，原来是` 12/13 · `天左右，现在提升` 7/8.

All ≤ 25 units and ≤ 40 characters. The staged Gate quote `启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页` is **37
units / 40 chars** — a raw substring, so only the unit ceiling fails.

## UNIQUE SPANS:

`python3 -B .ufo/waves/round-57/span_tools.py check S422 '<span>'` returned `{'raw_substring': True, 'in_content': True, 'count_in_page': 1,
'in_other_adopted_body': False}` for all eleven spans above; `grep -l -F` over `sources/*.html` matched S422 alone for each (only S421/S422 exist). The
`spans S422` lister supplied spans 1, 2, 3, 6, 7, 8, 9, 10, 11 and the label; spans 4, 5 and the label were confirmed individually with `check` because
the lister splits on `。`/`、`. The entry carries 11 page-unique quoted spans (C5 floor: 3).

## RECHECK RUN:

- `grep -F -c '能识别协议死链，以及大多数内容死链、跳转死链等低质网页' .ufo/waves/round-57/sources/S422.html` → **1** (2026-10-25, retained body).
- The `curl -fsSL --compressed` arm was **not run** (no live fetch was needed; the entry's recheck line labels that arm unrun).
- Sweeps actually run over the retained body: 删除 0, 移除 0, 下线 0, 状态码 0, 404 0, 屏蔽 1, 索引 3 (two inside the article block, one navigation
  link), 跳转死链 1.
- Entry-level replay of the counter's C5 extraction (double-quoted spans, units, chars, substring, content window, uniqueness, curly-quote refusal)
  and C2 header rules over the drafted file: 0 failures, 11 unique spans, 78 lines, 8911 bytes. The counter itself was not run (it needs the entry,
  both registry rows, the lesson Gate line and the census receipt at one revision).

## OMITTED:

- The fetching/index-building section beyond the index-display placement (90% of pages indexed, 80% faster, 500亿 daily discovered links, 95% recall,
  the ML quality ranking): different claim, and every figure sits inside an inline `span lang=EN-US` tag, so no raw span can carry it.
- The `时效性内容更多` section (2.0 versus 3.0 treatment of original articles against reprints): freshness of time-sensitive content, not dead links.
- The `链接提交更好用` / 主动推送 section (16-character token, ~10W sites, 5000W daily submissions, 4 hours earlier than crawler discovery,
  60%--100% same-day indexing): submission-channel performance, outside the row's scope; the channel is carried only where the dead-link paragraph
  names it.
- The off-page campaign link `http://bbs.zhanzhang.baidu.com/thread-113258-1-1.html` (an off-page URL, not a statement) and the navigation block's
  `死链提交` (`/badlink/index`) and `索引量` links (outside the article block; `索引量` is named in prose only to place the third `索引`).
- The `『抓取、建库更快—提交的内容更容易被抓取』` and `『时效性内容更多—有内容站点的更多机遇』` labels: they anchor sections this entry does not mine.
- The staged candidate's own H1, its untagged inference and its 10-day attachment: the inference is carried tagged `[INFERENCE]`, the attachment is
  corrected in the index-display section, and the H1 and staged file name are not reused (C1 refuses the staged names).
- Staged defects observed, not carried: id `S408` (pre-renumber; 0 hits in the body), `fetched 2026-10-24` (not the round date), anchor label
  `the article body's dead-link section` (0 hits in the body — an English description, not a heading), and the 37-unit Gate quote.
- Nothing about a live property: no URL served under test, no crawl observed, no Baidu behaviour measured.

Tool installs: none (`python3` and `grep` sufficed; no pacman transaction was attempted).

VERDICT: S422 entry drafted and quote-true (11 page-unique spans, all ≤25 units/≤40 chars; anchor, title and printed date present in the retained body), correcting the staged 37-unit quote, the dropped 跳转死链, the mistimed index-display figure and the untagged inference; Gate line, coverage row and 11-cell registry row produced and shape-checked.
