# CriticEntryModel

Claim C3, entry under attack: `corpus/knowledge/baidu-spider3-dead-link-model.md`, read at lane revision
`4b8c73050470ada9e6583f3b12d659d1bed6a17f` (`git show …:<path>` sha256 `40df6c8c…3029c`, identical to the working-tree file
as read; the L1's repairs since that revision were not in my copy). Retained body: `.ufo/waves/round-57/sources/S422.html`,
sha256 `7cf2e27d…e71ff`, 27327 bytes = 23676 decoded chars (offsets below are 0-based **char** offsets in the decoded body).
Page: https://ziyuan.baidu.com/wiki/867. Counterpart invoked by the entry: staged row `merge/kake/SOURCES.append.md:128` (S408)
and `merge/kake/knowledge/corpus/knowledge/baidu-spider3-dead-link-recognition.md` (read-only). Everything below marked
"confirmed by running" was executed; readings of prose are marked `[INFERENCE]`.

## FINDINGS

| # | entry line | class | entry says | page says | fix |
|---|---|---|---|---|---|
| F1 | 24 | WRONG-PLACE (false exclusivity) | "the paragraph under it speaks about dead-link recognition and processing time only [S422]" | the same `<p>` (chars 11050–11320) also carries "甚至快照在一段时间内仍然存在" and, in its final sentence, "当然，如果你要追求最佳处理效果，协议死链是最好的选择。" — the sentence the entry quotes in its own next-but-one section | FIX-1 |
| F2 | 18 | UNTAGGED-INFERENCE | "Two qualifiers decide how far the sentence reaches: 大多数 … scopes the group after 以及 … and 跳转死链 … is a third named kind of its own, not a restatement of either of the other two" | page gives one quantity word (大多数) and one open-ended marker (等); the entry names a second qualifier it never identifies. 大多数 directly precedes 内容死链, so binding only that item is also a permitted parse; the page does not settle which. The kind relations are nowhere stated (the page defines none) | FIX-2 |
| F3 | 37 | WRONG-PLACE (locational reason) | "[INFERENCE] the lane reads it as covering the kinds the model recognises, since it follows that scope sentence directly" | between the scope clause and "大约几天内就可以处理掉了" sit three clauses: "简单点说就是在之前的版本，站点通过站长平台提交死链，处理速度可能非常慢，甚至快照在一段时间内仍然存在，但是" (chars 11137–11224) | FIX-3 |
| F4 | 59 | WRONG-PLACE | "the article block's only 索引 occurrences are the two in the index-display sentence above" | two in-block occurrences, but in two sentences of one paragraph: char 10681 "索引展现时效性提升，原来是", and char 10772 **inside 搜索引擎** in the next sentence "我们都知道，搜索引擎从用户搜索到最终搜索结果展现的步骤是…" (`grep -o -F '索引' … \| wc -l` -> 3; 索引量 nav at 6786 is the third) | FIX-4 |
| F5 | 61 | OVERREAD | "the percentages on the page belong to the fetching, index-building and submission sections" | 90% and 80% sit in the unlabelled opening summary `<p>` (char 10086: "可以收录90%的网页，速度提升80%！"), before the first 『』 label at 10245; only 95%/40%~80% (10670/10749) and 60%--100% (12486) are in labelled sections | FIX-5 |
| F6 | 62 | OVERREAD | "the paragraph names no report, no tool and no status" | the paragraph names 站长平台 once ("站点通过站长平台提交死链", char 11162); 工具 occurs 0 times in the paragraph but 6 times on the page. The lane's own S421 entry names the discovery tool (抓取异常) for exactly this question | FIX-6 |
| F7 | 4 | MODAL-LOSS | "the processing time it states for a submitted dead link before and after the update" | submission through 站长平台 is stated only on the prior-version side; the post-update clause "更新后，大约几天内就可以处理掉了" names no channel and no submission | FIX-7 |
| F8 | 70 | OVERREAD (false completeness) | "Other Baidu statements held by the lane: … S329 … S312" | the lane also holds S421 (`corpus/knowledge/baidu-dead-link-types.md`, present at the same revision), opened from the same operator in the same round, which supplies the 403/404/503 vs 200 split and the 抓取异常 discovery tool this entry's silence list leaves open | FIX-8 |
| F9 | 33 | OVERREAD (count mismatch) | "Three qualifiers hold the prior-version account: 可能 … , 甚至 … , and the submission channel named is the platform, 站长平台" | the third listed item is a channel, as the entry itself says; only 可能 and 甚至 are qualifiers | FIX-9 |
| F10 | 74 | WRONG-PLACE (boundary) | "sits inside the article block (the container class `zz_dldes_content` through the page footer)" | the `zz_dldes_content` div closes at char 12884; the footer nav (投诉平台 13281, 联系我们 13862) and ©2026/京ICP证 (13972/14065) lie outside it. The contract's version-2 rule starts the block at the byline (发布日期：2016-06-30), before the container | FIX-10 |

No WRONG sentence was found in the four scope/timing/best-choice renderings themselves, and the title/label claim
("the label claims more than the paragraph develops") holds: 屏蔽 occurs once, in the label (char 10955), and the paragraph
supplies no blocking rule (confirmed by running).

## LOCATOR AND EVIDENCE GAPS (not sentence-truth defects)

- L47 locates the 10-day/40%~80% figure by paraphrase only, with no heading: the page's section label is
  『抓取、建库更快—提交的内容更容易被抓取』 (char 10245) and the figure sits in its **second** paragraph ("链接抓取和建库方面…",
  `<p>` at 10567); the only heading between that paragraph and the dead-link paragraph (11050) is
  『死链处理更及时—被黑低质页面全屏蔽』 (10955). Claim "a different paragraph" is otherwise confirmed. -> FIX-11
- L18 asserts "404 and 状态码 occur zero times" but cites a command for `404` only; the 状态码 count appears later in
  §Quote classes. Both are 0 (confirmed by running).
- L27's "the staged Gate quote is 37 units" checks out (37 units, 40 characters, present once in S422), but the span is the
  staged entry's front-matter recheck quote (the recognition sentence), and the staged tree defines "gate quote" only for
  own-work rows that name an artifact. The staged row words the misplacement itself as "indexing display timeliness …
  40–80% faster", so "attached … to dead-link handling" is the entry's gloss on a placement error that is real.
- Negatives in the entry that carry **no** command and rest on my sweeps: "the page states no per-kind rate"; "it does not say
  the other recognised kinds fail, are rejected, or go unhandled"; "It does not say how a publisher learns…"; "The page states
  neither half of that reading"; "the page attaches no dead-link handling time to it". All hold against the sweeps below.

## SUPPORTED COUNT

**32 of 42** factual sentences supported (front-matter lines 1–4 counted as 4; quote lines and headings excluded; the
English renderings counted individually). The 10 unsupported are F1–F10. Fully confirmed by running: every quoted span is a
raw substring, occurs once in S422 and 0 times in S421, lies in one text node, and respects both ceilings (max 25 units /
27 characters); sha256, byte count and HTTP 200 match `sources/receipts.json`; 40%~80% and 10 sit in `span lang=EN-US`;
the 10-day figure's paragraph and the dead-link paragraph are distinct `<p>` elements.

## NEGATIVE CLAIMS RECHECKED

| command (repo root) | count | entry claimed |
|---|---|---|
| `grep -o -F '删除' .ufo/waves/round-57/sources/S422.html \| wc -l` | 0 | 0 ✓ |
| `grep -o -F '移除' … \| wc -l` | 0 | 0 ✓ |
| `grep -o -F '下线' … \| wc -l` | 0 | 0 ✓ |
| `grep -o -F '状态码' … \| wc -l` | 0 | 0 ✓ |
| `grep -o -F '404' … \| wc -l` | 0 | 0 ✓ |
| `grep -o -F '屏蔽' … \| wc -l` | 1 | 1 ✓ |
| `grep -o -F '索引' … \| wc -l` | 3 | "two in block + 索引量" — count ✓, attribution ✗ (F4) |
| `grep -o -F '协议死链' … \| wc -l` | 2 | "only other mention is the preference" ✓ |
| `grep -o -F '站长平台' … \| wc -l` | 5 (1 in the dead-link paragraph) | "names no tool" ✗ (F6) |
| `grep -o -F '工具' … \| wc -l` | 6 page-wide, 0 in the dead-link paragraph | — |
| `grep -o -F '403' / '503' … \| wc -l` | 0 / 0 | "no status code" ✓ |
| `grep -o -F '失败' / '拒绝' / '无法' / '不处理' / '弃用' … \| wc -l` | 0 each | "do not fail/reject/go unhandled" ✓ |
| `grep -o -F '无需' / '不需要' / '不必' / '取消' … \| wc -l` | 0 each | "submission became unnecessary" not stated ✓ |
| `grep -o -F '通知' / '报告' … \| wc -l` | 0 / 0 | "no report, no notification" ✓ |
| `grep -F -c '能识别协议死链，以及大多数内容死链、跳转死链等低质网页' …` | 1 | 1 ✓ (curl arm honestly reported unrun) |
| `grep -n '死链\|Baidu\|Spider' crawl-error-status-table.md yahoo-japan-{deleted,url}…` | no match in all three | "None of those entries states what Baidu's crawler recognises" ✓ |

## FIXES THE L1 SHOULD APPLY

- FIX-1 (L24, replace "and the paragraph under it speaks about dead-link recognition and processing time only [S422]"):
  "and the paragraph under it says nothing about blocking: it gives the recognition model, the prior version's slow
  processing and lingering snapshot, the few-days handling time, and the best-choice preference [S422]".
- FIX-2 (L18): "[INFERENCE] The sentence's reach turns on two words. The lane reads 大多数 (most) as scoping the whole list
  after 以及 — content dead links, redirect dead links and the other low-quality kinds — so protocol dead links alone are named
  without a quantifier; the page's punctuation also permits 大多数 to bind only 内容死链, and the page does not settle which.
  等 (etc.) leaves that list open-ended, and the lane reads 跳转死链 (redirect dead links) as a third named kind, not a
  restatement of either of the other two, since the page defines none of them."
- FIX-3 (L37, replace "since it follows that scope sentence directly"): "since it sits in the same paragraph as that scope
  sentence, separated from it only by the prior-version account".
- FIX-4 (L59): "…and the article block's two 索引 occurrences are both in that earlier paragraph — 索引展现时效性提升 in the
  index-display clause and 索引 inside 搜索引擎 in the next sentence — while the body's third 索引 is the navigation link
  索引量, outside the article block."
- FIX-5 (L61): "It states no rate, no percentage and no measurement for dead-link handling; every percentage on the page sits
  outside this section — 90% and 80% in the opening upgrade summary, 95% and 40%~80% in the fetching-and-index-building
  section, 60%--100% in the link-submission section."
- FIX-6 (L62): "It does not say how a publisher learns that a dead link was recognised: the paragraph names no reporting tool,
  no report and no status — its one platform name, 站长平台, is the prior-version submission channel, not a notification
  path; the lane's S421 entry, which names the 抓取异常 tool, is where that question is answered."
- FIX-7 (L4): "…the processing time it states for dead links before and after the update (the submission channel 站长平台 is
  named only on the prior-version side)…".
- FIX-8 (L70): append "and S421 `corpus/knowledge/baidu-dead-link-types.md`, the dead-link taxonomy and discovery tools the
  same operator published, opened in the same round."
- FIX-9 (L33): "Two qualifiers and one channel hold the prior-version account: 可能 … , 甚至 … , and the submission channel
  named is the platform, 站长平台."
- FIX-10 (L74): "sits inside the article block the counter reads (S422's block starting at the byline 发布日期：2016-06-30;
  the `zz_dldes_content` container ends before the footer nav and copyright line)".
- FIX-11 (L47): "…they sit in the second paragraph of the earlier section 『抓取、建库更快—提交的内容更容易被抓取』 (the paragraph
  headed 链接抓取和建库方面), in the sentence whose head is …; the only heading between that paragraph and the dead-link
  paragraph is 『死链处理更及时—被黑低质页面全屏蔽』."

No report file other than this one was written; no lane state, index or sibling lane was touched; no tool was installed.
The page-silence sweeps were re-run with the entry's own commands; the two `curl` arms were not run and are not claimed.

VERDICT: entry S422 is quote-true and mostly faithful, but 10 of 42 sentences need repair — the dead-link paragraph is claimed to develop only recognition and timing while it carries the best-choice sentence, the 索引 sweep is attributed to the wrong sentence, and four silence/cross-link claims overreach; four of these are structural enough to fix before the row is scored.
