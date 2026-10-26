# ReviewerEntryModel

Claim C3, independent fidelity review of `corpus/knowledge/baidu-spider3-dead-link-model.md`. Entry read at lane revision
`4b8c73050470ada9e6583f3b12d659d1bed6a17f` (`git show …:<path>` sha256 `40df6c8c07625b3f2d54a70392fbc24b8cd2daea2085f9f7519810007ad3029c`, identical to the
working-tree file: `git diff --stat 4b8c730 -- <entry> <counter> sources/` empty). Retained body
`.ufo/waves/round-57/sources/S422.html`, sha256 `7cf2e27d…e71ff`, 27327 bytes / 23676 decoded chars, `sources/receipts.json`
HTTP 200 fetched 2026-10-25T23:38:35Z. No LSP server answers this corpus and `xd://lsp` is not mounted, so caller/definition
checks below are text- and counter-level (span_tools, c57_quote_truth, grep on raw bytes), not semantic-LSP.

## DEFECTS:

| # | sev | line | defect | fix | evidence |
|---|---|---|---|---|---|
| D1 | MEDIUM | 59 | "the article block's only 索引 occurrences are the two in the index-display sentence above" — the block has two, but in **two sentences**: `索引展现时效性提升…` and `索引` inside 搜索引擎 in the next sentence (`我们都知道，搜索引擎从用户搜索到…`). | "…the article block's two 索引 occurrences are the 索引-display clause and 索引 inside 搜索引擎 in the following sentence; the body's third 索引 is the navigation link 索引量, outside the block." | confirmed by running: decoded-body char offsets 10681 (`索引展现时效性提升`) and 10772 (`搜索引擎` in the next sentence); `grep -o -F '索引' S422.html \| wc -l` -> 3; `索引量` at char 6786, before the block start 9242. |
| D2 | MEDIUM | 4 | ground promises "the processing time it states for a submitted dead link before and after the update": the page states no pre-update time (only `处理速度可能非常慢`, a modal speed), and submission through 站长平台 is named only on the prior-version side. | "…what it says about handling time after the update, the prior version's account (platform submission, possibly very slow processing, lingering snapshot), and the one kind it names as the best choice." | confirmed by running: the dead-link `<p>` contains `处理速度可能非常慢`, `快照在一段时间内仍然存在`, `更新后，大约几天内就可以处理掉了`; no duration on the prior side and no submission verb after 更新后; `无需`/`不需要`/`不必`/`取消` -> 0 each. |
| D3 | LOW | 24 | "the paragraph under it speaks about dead-link recognition and processing time only" is false exclusivity: the same `<p>` ends with `当然，如果你要追求最佳处理效果，协议死链是最好的选择。`, the sentence the entry itself quotes two sections later. | "…and the paragraph under it states no blocking rule: it gives the model, the prior version, the few-days handling and the best-choice preference." | confirmed by running: the dead-link `<p>` (char 11050–11308) contains the preference sentence at 11248; 屏蔽 -> 1 (label only). |
| D4 | LOW | 37 | "it follows that scope sentence directly" is locational overreach: the `更新后` clause is a 但是-clause of the **same** sentence, with the whole prior-version account between it and the `能识别…` clause. | "since it sits in the same sentence as that scope clause, separated from it by the prior-version account". | confirmed by running: one `<p>`/one sentence from `在死链处理方面` to `处理掉了。`; clause order as quoted. |
| D5 | LOW | 37, 55 | qualifier losses in the English: `处理掉` rendered "handled" (the resultative 掉, dispose-of, is dropped while the gloss says "the verb is 处理"); `就` in `就可以` dropped; `40%~80%不等` rendered "[40%~80%]" without 不等 (varying). | render `处理掉` as "can be dealt with (disposed of)" **and** keep the no-index-removal caveat; add "varying" for 不等. | confirmed by running: raw text `大约几天内就可以处理掉了`, `现在提升40%~80%不等`; 删除/移除/下线 -> 0 each, so the caveat survives the stronger gloss. |
| D6 | LOW | 18, 33 | self-description miscounts: "Two qualifiers … and 跳转死链 … is a third named kind" lists one qualifier (大多数) plus a parse; "Three qualifiers … and the submission channel named is the platform" lists two qualifiers (可能, 甚至) plus a channel. | "The reach turns on 大多数 and on how 跳转死链 is parsed"; "Two qualifiers and one channel hold the prior-version account". | confirmed by running: the two sentences' own items; no third quantifier exists in the span. |
| D7 | LOW | 62 | "the paragraph names no report, no tool and no status": the paragraph names 站长平台, which line 33 of the same entry calls the submission channel/platform. Intent (no notification path) holds, but "no tool" is overbroad. | "…names no reporting tool, no notification and no status; its one platform name, 站长平台, is the prior-version submission channel." | confirmed by running: paragraph slice counts 站长平台 1, 工具 0, 报告 0, 状态 0; page-wide 站长平台 5, 工具 6. |
| D8 | LOW | 8, 70 | cross-link gap: S421 (`corpus/knowledge/baidu-dead-link-types.md`, same operator, same round, same dead-link subject) is named nowhere, while the list of "Other Baidu statements held by the lane" carries S329 and S312. | add S421 and its scope (the protocol/content split, 403/404/503 vs 200). | confirmed by running: `grep -n 'S421\|baidu-dead-link-types'` on the entry exits 1; the file exists at the revision (7314 bytes) and is the C3 sibling in the counter's `ADOPTED`. |
| D9 | LOW | 74 | quote-class boundary wording "the container class `zz_dldes_content` through the page footer" matches neither the counter's block (byline `info-item-time` at 9199 → `wiki-foot-right` at 12939) nor the container extent (`zz_dldes_content` div 9242→12878, page `class="footer"` at 13056). | "sits inside the counter's article block (byline 发布日期：2016-06-30 through `wiki-foot-right`), within the `zz_dldes_content` container". | confirmed by running: div-depth walk from the `zz_dldes_content` div (char 9242–12878) and byte offsets above (page `class="footer"` at 13056); all 11 spans lie in the byline→wiki-foot-right window. |
| D10 | LOW | 55 | staged-artifact gloss is imprecise: the staged row says "indexing display timeliness improved from about ten days to 40–80% faster" (`shokuknow/merge/kake/SOURCES.append.md:128`), not that dead-link handling improved; the misplacement is the row's scope cell (`§ … 死链处理更及时…`) covering a figure from the earlier section. | "the staging row scopes itself to the dead-link section while its teaches cell carries the index-display figure — a figure the body puts in the earlier paragraph." | confirmed by running: row text at `merge/kake/SOURCES.append.md:128`; the staged entry `merge/kake/…/baidu-spider3-dead-link-recognition.md` carries no 10-day figure at all. The placement error and the 37-unit Gate span (37 units / 40 chars) are otherwise confirmed. |

Not defects, checked and supported: every blockquote is a raw substring, page-unique (count 1 in S422, 0 in S421), inside the
counter's text-node block, ≤25 units / ≤40 chars (max 25 units, 27 characters — quote at line 16 is exactly at the unit
ceiling); sha256/byte count/HTTP 200 match `receipts.json`; `10` and `40%~80%` really sit in `span lang="EN-US"`; `404`/`状态码`
are 0; `屏蔽` 1 (label only); `协议死链` 2 (scope + preference); `索引量` outside the block; H1's three promises (scope,
timing, preference) are each proven by the body.

## RECHECK RUN:

- Executed: `grep -F -c '能识别协议死链，以及大多数内容死链、跳转死链等低质网页' .ufo/waves/round-57/sources/S422.html` -> **1**. The `recheck:` grep is runnable as written and its `-> 1` matches the retained body; the curl arm is honestly marked unrun.
- Counter: `python3 -B .ufo/waves/round-57/c57_quote_truth.py --root . --revision 4b8c73050470ada9e6583f3b12d659d1bed6a17f` ->
  **`C3 quote-truth 8/8 met=True`, `C5_quote_truth PASS`, EXIT=0, zero C5 notes.** C5 reads the entry and registry with
  `git show <rev>:<path>` (counter lines 246, 332), so this is a revision read, not a worktree read; the entry and counter
  blobs at that revision equal the worktree copies, so no unrepaired copy exists for S422.
- The stated 6/8 does reproduce, but only at the earlier W1 build commit: at `cddef5b` the run gives **6/8 met=False** with
  exactly two note groups — `S421: entry line 91 quotes 72 characters, character ceiling 40` / `…not a raw substring…` and
  `C8: append-only: measured registry minus new rows … != mirror bytes`. **No S422 note at either revision**; both failures are
  S421/registry-side and are cleared at 4b8c730.

## CROSS-LINK CHECKS:

| named entry | exists | S-id | sentence the entry attributes | confirmed |
|---|---|---|---|---|
| `crawl-error-status-table.md` | yes | S286 | "what an error status does to a crawl on Googlebot's side" | H1 "An error status is its own crawl layer"; body: Googlebot scales back crawling |
| `yahoo-japan-deleted-url-recrawl.md` | yes | S419 | "what another operator's pages say about a deleted URL" | H1 "A deleted URL that still answers 200 OK may keep being crawled" |
| `yahoo-japan-nonexistent-url-recrawl.md` | yes | S420 | "and about a URL that never existed" | H1 "The crawler does not treat a 200 OK error page for a nonexistent URL as an error page" |
| `baidu-friendly-crawl-guidance.md` | yes | S329 | "Other Baidu statements held by the lane" | H1 "A Baiduspider robots block binds the desktop and mobile crawlers at once" |
| `baidu-mobile-matching-error-causes.md` | yes | S312 | same | H1 "A mobile page that loads its main body with ajax cannot be matched to its desktop page" |
| staged `merge/kake/SOURCES.append.md` row | yes (shokuknow, read-only) | S408 | "the staging row for this page, whose id and file name are not reused here" | row URL is `wiki/867`; S408 absent from `corpus/SOURCES.md`; new row S422, new file name |

"None of those entries states what Baidu's crawler recognises as a dead link" holds: no 死链 / dead-link / デッドリンク match in
S286, S419, S420. The one gap is D8: S421, the direct same-operator sibling, is not linked at all.

## STYLE:

- Length: 78 lines against 64 (`yahoo-japan-deleted-url-recrawl.md`) and 68 (`baidu-friendly-crawl-guidance.md`); comparable,
  slightly long, no padding found.
- Structure: header trio, H1, sectioned body, `## Quote classes`, page-silence sweeps, `Scope note` — present and
  sibling-shaped. Two deviations: (a) the H1 is a colon topic title ("Baidu's Spider3.0 …: scope, processing timing and the
  best-choice preference"), while all six sibling H1s are declarative sentences (S419/S420/S421/S286/S329/S312); (b) the entry
  has no `## What this entry does not establish` section, which both reference files and the S421 sibling carry (`## What the
  page does not say` plus the tagged-inference section cover part of that duty). Also INFO: the `recheck:` command is not in
  backticks as the sibling entries write it.
- Scope note: present, one sentence, same shape as siblings ("a claim about what the operator's page states; no URL was served
  under test for this lane, no crawl was observed and no Baidu behaviour was measured").

## ADMIT OR REPAIR:

REPAIR — the quote layer is sound (11/11 spans, 8/8 counter, runnable recheck), but D1 and D2 are factual promise/sweep
defects and D8 leaves out the S421 sibling; fix D1–D3 and D8 at least, then re-run the counter.

VERDICT: quote-true and largely faithful at 4b8c730/C5 8/8, but the 索引 sweep is misattributed and the ground and paragraph-exclusivity claims overreach — repair before admission.
