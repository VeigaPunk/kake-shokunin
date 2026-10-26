# CriticEntryTypes

Claim C3 (freshness, sourced), seat `CriticEntryTypes`. Artifact attacked: `corpus/knowledge/baidu-dead-link-types.md`
(row S421 in `corpus/SOURCES.md:167`), against the retained body `.ufo/waves/round-57/sources/S421.html`
(sha256 `32eaf8b7…`, 34750 bytes, `sources/receipts.json` httpStatus 200, page `…/college/articleinfo?id=3458`).

Build read: `git show 4b8c73050470ada9e6583f3b12d659d1bed6a17f:corpus/knowledge/baidu-dead-link-types.md` is
byte-identical to the working-tree file (empty diff, confirmed by running), so every line number here is a 4b8c730
line number. No file outside this report was touched.

Method (all run 2026-10-25, lane root): text nodes of the article block dumped with `span_tools.py window S421`
plus a tag-split (`re.split('<[^>]*>')`) to get node boundaries; every blockquote and every CJK inline span of the
entry checked with `span_tools.py check S421 '<span>'`; section offsets taken in the stripped article text
(`二、` at 928, `三、` at 1442); `grep -F` counts on the raw body and on the round-56 bodies; held entries
(`yahoo-japan-*.md`) greped; one live `curl` of the page. "ran" below = confirmed by running.

## FINDINGS

| # | entry line | class | entry text (as written) | page text at its locator | basis | smallest safe fix |
|---|---|---|---|---|---|---|
| F1 | L1 | WRONG-PLACE | `source: S421 — … — § 一、了解死链 (发布日期 2022-09-09) — fetched 2026-10-25` | 5 of the 23 spans (L80 `将需处理的页面设置404页面` off 1070, L81 `页面设置404，一定是404页面` off 1108, L85 `仅识别404，` off 1501, L86, L87) lie in §二 and §三, which begin at offsets 928 and 1442; §一 holds the other 18 | ran | name §二/§三 in the source line, keep the registry anchor string `§ 一、了解死链` unchanged |
| F2 | L6 (H1), L4, L19 | OVERREAD | "Baidu separates dead links into protocol dead links and content dead links"; "splits it into protocol and content kinds"; "The page then divides dead links into two kinds" | page node 10 ends `A：死链一般是指页面已经无效，无法对用户提供任何有价值信息的页面。包括` and node 11 is `协议死链和内容死链` — 包括 (include) introduces the kinds; the page never asserts a partition | ran | quote `。包括` and render "include", not "divide/separate" (L15, L19, L4, L6) |
| F3 | L8 s1 | WRONG-PLACE | "the title's remaining words, 死链 and 常见问题解析, sit between curly quotation marks that this entry does not copy" | `<title>` = `搜索问答剧场 【六】“死链”常见问题解析_搜索学堂_百度搜索资源平台`: only 死链 is between the curly quotes; 常见问题解析 follows the closing ” | ran | move 常见问题解析 outside the quotes |
| F4 | L29 | WRONG-PLACE | "the qualifiers are 明确表示 (clearly indicated) and 页面的 (of the page)" | the quoted span is node 16, which begins `的TCP协议状态/…`; 页面 closes node 15 (`：页面`); `页面的TCP协议状态` occurs 0 times in the raw body (tag boundary) | ran | keep 明确表示 as the quotable qualifier; say 页面的 is the preceding text node's phrase, not inside any span |
| F5 | L42 | OVERREAD | "或 (or) keeps the three reasons alternative" | node 21 = `内容已经变更为不存在、已删除或需要权限`: 、 separates 不存在 from the pair, 或 joins 已删除 and 需要权限 only | ran | name both separators (、 and 或) |
| F6 | L49 s2 | MODAL-LOSS | "This answers the staged candidate's assertion (b): the content dead link indeed returns HTTP 200 and cannot be set to 404" | the subject is right (page text `内容死链，` immediately precedes the quoted span, offset 373), but §一 Q2A(1) says `发现后需要及时做404处理` for internally added wrong content links (off 447) and §二 says `将需处理的页面设置404页面` (off 1070); 内容死链 never recurs after offset 928 (3 occurrences, all < 928) | ran | state the subject, then state that the page also orders 404 for that class, and that the entry does not reconcile the two |
| F7 | L55–L58 | MODAL-LOSS | two quote lines plus "the consequence is hedged with 可能会 (may)" | 可能会 is its own text node (node 55) between the two quoted nodes; the two lines joined without it (`…若存在大量死链，影响网站整体评价`) occur 0 times in the body | ran | keep both spans, say 可能会 sits between them and is inside neither, so the lines do not read continuously |
| F8 | L101 | MODAL-LOSS | "The page states the 1–2 week effect cycle of submissions" | `死链提交后一般` + `生效周期为1-2周`: the page hedges with 一般 (一般 occurs twice on the page, here and at 一般是指) | ran | add "generally (一般)" |
| F9 | L95 s3 | OVERREAD | "Both Yahoo pages concern a URL that answers `HTTP 200 OK`, and each asks that the server return 404" | S419: `…「HTTP 200 OK」のステータスを返すようにサーバーが設定されている場合…` and `…「HTTP 404 Not Found」のステータスを返すように設定されているかを確認してください` (confirm whether); S420: `…設定にしていると…` and `…返すように設定を行ってください` (make the setting). The held S419 entry says "The verb is 確認してください, please confirm" (L27/L29) and the S420 entry says "The request is to make the setting, not to check one" (L54) | ran | restore "configured to answer" and the check-vs-set split |
| F10 | L95 s3 | WRONG-PLACE + MODAL-LOSS | "states two things about 404 that sit side by side on the page: the content kind cannot be set to 404, and the submission tool recognises 404 only" / "The page does not reconcile the two statements" | the two named statements are 1111 characters apart (`无法设置为404` off 390 in §一; `仅识别404，` off 1501 in §三); the third, §二's 404 setting (off 1070/1108), is the one that conflicts with 无法设置为404, and it is not named | ran | name all three with their sections; the "does not reconcile" sentence stays true but must cover the §一/§二 pair |
| F11 | L95 s3 | UNTAGGED-INFERENCE | "[S421] states the same class for Baidu (a content dead link answers 200)" | neither page cross-references the other; the mapping is the lane's, and this entry tags a smaller inference at L68 | [INFERENCE] | prefix `[INFERENCE]` |
| F12 | L95 s1 | MODAL-LOSS | "Both sides are quoted from the held entries." | true for the Yahoo side; the Baidu side is this entry's own retained body S421 (not a held entry in the sense of L95's other citations) | ran | say "the Yahoo side from the held entries, the Baidu side from the retained body" |

Checked and supported (no finding):

- The content-kind attribution the assignment flags: the page sentence is `内容死链，` + node 23 `服务器端返回HTTP状态码200` + node 24 `，无法设置为404` — about the content kind, not about dead links in general. L44/L46/L47 are SUPPORTED; the quote block just starts after the subject (hence the fix in F6).
- 一般是指 (L12/L17), 等 in `常见的如403、404、503状态等` (L33) and 等 in `等与原内容无关的信息页面` (L42), 明确表示 (L29), 一定是 (L83), 定期/大量 (L58): all rendered with the page's qualifiers.
- Both Yahoo quotes are real and page-unique: `クローラーは削除されたウェブページと認識できず、` → `grep -c -F` = 1 in round-56 `S419.html`, 0 in `S420.html`, 2 in the held S419 entry, 0 in the S420 entry; `巡回を続けます` → 0/1 in the bodies, 0/2 in the entries.
- Every one of the 23 quoted spans is a raw substring inside a single text node of the article block, page-unique (count 1), absent from S422, ≤ 25 units and ≤ 40 characters (max 24 units / 26 characters, L55). The L8 command claim re-runs exactly: `check S421 '一、了解死链'` → `{'units': 5, 'raw_substring': True, 'in_content': True, 'count_in_page': 1, 'in_other_adopted_body': False}`.
- L68's [INFERENCE] is correctly tagged and its two sentences are supported; L100's negative holds (sweeps below); L91's "states nothing about removing a path from internal links" holds (sweeps below); L89 and L83's tool statements match §三; L95's Google sentence matches `corpus/knowledge/crawl-error-status-table.md:10` ("Googlebot will scale back its crawling if it detects that your servers are having trouble").

## SUPPORTED COUNT

28 of 39 prose sentences supported as written; 11 defective (F1 = L1, F2 = L4 and L19, F3 = L8 s1, F4 = L29, F5 = L42, F6 = L49 s2, F7 = L58, F12 = L95 s1, F9/F10/F11 = L95 s3, F8 = L101).
Inventory used (sentence count per line, headings and blockquotes excluded): L1 1, L3 1, L4 1, L8 2, L12 1, L17 1,
L19 1, L23 1, L29 1, L33 1, L42 1, L44 1, L49 2, L53 1, L58 1, L60 1, L66 1, L68 2, L72 1, L76 1, L78 1, L83 2,
L89 1, L91 2, L95 5, L99 1, L100 1, L101 1, L102 1, L104 1 = 39. Rendering fidelity is good overall; the defects are
boundary and quantifier defects, not invented page statements.

## NEGATIVE CLAIMS RECHECKED

| entry claim | command (lane root) | result |
|---|---|---|
| L100 "no definition of a monitor or a link checker" | `python3 -B .ufo/waves/round-57/span_tools.py window S421 > /tmp/w` then `grep -o -F` for 监控, 监测工具, 检测工具, 检查工具, `link checker`, 链接检查 | 0 each — holds |
| L91 "states nothing about removing a path from internal links" | same window: 移除, 去掉, 删除链接, 链接删除 | 0 each — holds |
| L66/L68 "not described as status-code-only" | same window: 状态码 = 1, at offset 383 (§一 Q1); the discovery paragraph starts at offset 840 → 0 there | holds |
| L95 "states no rate or backoff effect" | same window: 频率, 速率, 降频, `backoff` | 0 each — holds |
| L95 "does not reconcile" | 内容死链 = 3 (offsets 256, 318, 368, all before §二 at 928); 无法设置 = 1; `404处理` = 1 | true, but the named pair is the wrong pair (F10) |
| L3 recheck `curl …` piped to `grep -F -c '协议死链和内容死链'` -> 1 | `curl -fsSL --compressed` live GET, then `grep -F -c` on live body and on retained body | 200 / 34750 bytes / 1 live / 1 retained; live article block byte-identical to the retained block (sha `f905eedc…`); whole-file sha256 differs (`16be2f0d…` vs retained `32eaf8b7…`) — the recheck is a phrase check and holds |
| L8 `check S421 '一、了解死链'` -> count_in_page 1 | the command as written in the entry | matches exactly |
| L95 Yahoo spans | `grep -c -F` in `.ufo/waves/round-56/sources/S419.html`, `S420.html` and the two held entries | 1/0, 0/1 in bodies; 2/0, 0/2 in entries — real |

## FIXES THE L1 SHOULD APPLY

1. L1 → `source: S421 — https://ziyuan.baidu.com/college/articleinfo?id=3458 — § 一、了解死链 (发布日期 2022-09-09), with quoted spans also from § 二 and § 三 — fetched 2026-10-25`
2. L4 → `ground: per-engine crawl hygiene — how Baidu's own page defines a dead link, which two kinds it says dead links include, and what the content kind answers with`
3. L6 → `# Baidu's page says dead links include protocol dead links and content dead links, and that the content kind answers 200`
4. L15 → `> "无法对用户提供任何有价值信息的页面。包括"` (19 units, raw, count 1 — checked)
5. L19 → `The page's definition then names two kinds with 包括 (include), which introduces them rather than dividing the class exhaustively [S421]:`
6. L8 s1 → Baidu's college page prints a title that opens `搜索问答剧场 【六】` (with the space inside the printed title), then 死链 between curly quotation marks that this entry does not copy, then 常见问题解析, and answers developer questions about dead links (死链).
7. L29 → `(rendered: a dead link clearly indicated by the page's TCP protocol status / HTTP protocol status — 明确表示 (clearly indicated) is inside the quoted span; 页面的 (of the page) sits in the text node before it, which ends 页面, and the span begins at its trailing 的, so 页面的 is the page's phrase but is inside no quotable span.)`
8. L42 → `(rendered: the server's return state is normal, but the content has changed to nonexistent, deleted or requiring permission — an information page unrelated to the original content; the page separates the three with 、 (不存在、已删除) and 或 (已删除或需要权限), and 等 (etc.) keeps the list non-exhaustive.)`
9. L49 → (rendered: the content dead link's server side returns HTTP status code 200 and it cannot be set to 404 — 无法设置为404 is a stated impossibility, not a recommendation.) The sentence's subject is the content kind, not dead links in general: the page's own 内容死链， (raw, one occurrence) immediately precedes the quoted span. The same page then tells the publisher, for content links wrongly added internally, 发现后需要及时做404处理 (§ 一) and 将需处理的页面设置404页面 (§ 二); this entry records both and does not reconcile them with 无法设置为404. The staged candidate's assertion (b) read "the content kind returns HTTP 200 and cannot be set to 404" (staged l.33, quoted at `w1/ReviewerStagedBaidu.md:33`), so the page answers (b) and then sets it aside in § 二.
10. L58 → `(rendered: Baiduspider regularly tests the site's page content value; if a large number of dead links exist, it may affect the site's overall evaluation — 定期 is regular and 大量 is a large number.) The modal is the page's own: 可能会 (may) is a separate text node between the two quoted nodes and is inside neither span, so the two lines above do not read as one continuous quotation.`
11. L95 s3 → `Both Yahoo pages concern a URL the server is configured to answer with HTTP 200 OK; S419 asks the publisher to confirm whether the server is configured to return 404 (確認してください), S420 asks for the setting to be made (設定を行ってください). [INFERENCE] [S421] states the same shape for Baidu (a content dead link answers 200) and three things about 404 that are not adjacent: the content kind cannot be set to 404 (§ 一), the publisher is told to set 处理 pages to 404 (§ 二), and the submission tool recognises 404 only (§ 三). The page does not reconcile them, and this entry does not.`
12. L95 s1 → `The Yahoo side is quoted from the held entries and the Baidu side from the retained body.`
13. L101 → `- The page states that a submitted dead link's effect cycle is generally (一般) 1–2 weeks, and the file-placement steps; they are operational mechanics and are not carried here.`

None of these fixes removes or re-spans an existing valid span; fixes 4 and 11 add only spans that are raw, single
text node, page-unique, ≤ 25 units and ≤ 40 characters (checked). Fix 1 keeps the registry anchor string intact, so
C3's C5 anchor check (which reads the registry row, not the entry header) is unaffected.

VERDICT: C3's S421 entry is quote-true at the span level (23/23 spans valid, both Yahoo quotes real) but not rendering-true: 11 of 39 sentences over-read, drop a qualifier, or attach a page phrase to the wrong span or section — chiefly the 包括 partition, the §一 "cannot be set to 404" vs §二 "set it to 404" pair, the spliced 可能会, and "each Yahoo page asks that the server return 404" (S419 only asks to confirm).
