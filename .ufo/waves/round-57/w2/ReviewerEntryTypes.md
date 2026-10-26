# ReviewerEntryTypes

Scope: C3 freshness, fidelity lens on `corpus/knowledge/baidu-dead-link-types.md`. Entry read at revision
**4b8c73050470ada9e6583f3b12d659d1bed6a17f** (`git show`); the working tree is byte-identical for it, the registry and the
counter (`git diff --quiet 4b8c730… -- corpus` -> 0; `… -- .ufo/waves/round-57/c57_quote_truth.py` -> 0). Body read:
`.ufo/waves/round-57/sources/S421.html`, 34750 B, sha256 `32eaf8b7…7182`, = `sources/receipts.json` (HTTP 200,
fetchedAt 2026-10-25T23:38:33Z, url `…/articleinfo?id=3458`). No tool installed; nothing outside this file written.

## Span gate (item 1)

`python3 -B .ufo/waves/round-57/c57_quote_truth.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision
4b8c73050470ada9e6583f3b12d659d1bed6a17f` -> `C3 quote-truth 8/8 met=True`, C1–C8 all PASS, exit 0. **The run prints no
C5 notes, so there are no notes to quote.** The assignment's premise (6/8 fail at that revision, since repaired) does not
reproduce: the entry, registry and lesson bytes *at that revision* pass all eight checks, and the counter bytes are the
same at that revision and in the tree — so this is not a working-tree artefact. Treat the premise as stale; nothing in C5
is left for this seat to confirm.

Independent gate (confirmed by running, counter's own `units()`, `in_content()`, `text_segments()` over the article block
of S421): all **22** verbatim blockquote spans (L14–L87) are raw substrings inside *one* text node of the article block,
occur once in S421, occur in no other adopted body (`S422.html`: 0 hits), and are **≤24 units / ≤26 characters** (worst:
L55, 24 u / 26 ch). Inline page quotes (`搜索问答剧场 【六】`, `一、了解死链`, `HTTP 200 OK`, the two Japanese peers) also
check out. The helper call claimed on L9 reproduces exactly: `span_tools.py check S421 '一、了解死链'` ->
`{'units': 5, 'raw_substring': True, 'in_content': True, 'count_in_page': 1, 'in_other_adopted_body': False}`.

## DEFECTS:

**D1 — MEDIUM — L4 (`ground:`), L6 (H1), L19 — exhaustiveness asserted where the page says "includes". (confirmed by
running)** Raw at offset 10211 of `S421.html`: `…无法对用户提供任何有价值信息的页面。包括<span …><b>协议死链和内容死链</b>`.
The page's word is 包括 (includes), i.e. a non-exhaustive enumeration. The entry upgrades it three times: `ground:` "splits
it into protocol and content kinds", H1 "separates dead links into protocol dead links and content dead links", L19 "The
page then divides dead links into two kinds". This is the one qualifier-drop that changes claim strength (contrast L32 and
L42, where 常见的如/等 are correctly preserved). No third kind is named on S421, so the fix is wording only: "names two
kinds — 包括 (including) …" / H1 "…names protocol dead links and content dead links". A span cannot carry the word:
`包括协议死链 in body` -> False (a `<span>` splits 包括 from 协议死链), so it must be prose, on L19.

**D2 — MEDIUM — L8 — the title-typography sentence is false about the page. (confirmed by running)** L8: "the title's
remaining words, 死链 and 常见问题解析, sit between curly quotation marks". Raw title (both `<title>` and the printed
`<h3 class="info-title">`): `搜索问答剧场 【六】“死链”常见问题解析`. Only 死链 sits inside the curly quotes;
`常见问题解析` sits **outside** the closing `”` (`'“死链”常见问题解析' in body` -> True; `'“死链常见问题解析”'`,
`'“死链和常见问题解析”'`, `'“死链、常见问题解析”'`, `'“死链”“常见问题解析”'` -> 0 each). Fix: "死链 inside curly
quotation marks and 常见问题解析 outside them". This sentence is the entry's opening precision claim, so a reader who
trusts it is misled at line 8.

**D3 — MEDIUM — L1 (`source:`), L78, L80–L81, L85–L87 — 5 of 22 spans are quoted from sections the locator does not
name. (confirmed by running)** h2 offsets in the article block: 一、了解死链 10033, 二、教你如何处理死链页面 14632,
三、使用【死链提交】工具的注意事项 17881. Span→section map: L14…L74 -> § 一; **L80, L81 -> § 二**; **L85, L86, L87 ->
§ 三**. `source:` (L1) and the registry anchor cell (`corpus/SOURCES.md:167`, "§ 一、了解死链 (发布日期 2022-09-09)")
name § 一 only, and the two later sections are called "The handling section" (L78) and "The 【死链提交】 tool" (L83) —
never by heading. The sibling states the convention and obeys it: `baidu-spider3-dead-link-model.md` puts its
off-anchor quote in a named place ("The 10-day and 40%~80% numbers on this page are not in the dead-link section: they
sit in the earlier paragraph on link fetching and index building"). Fix: name `§ 二、教你如何处理死链页面` at L78 and
`§ 三、使用【死链提交】工具的注意事项` at L83; L1 may stay narrow if the row scope cell ("the 404-set submission
workflow", `SOURCES.md:167`) is read as covering them, but each quote site must name its section.

**D4 — MEDIUM — L80–L81 — a full clause is elided between two quoted spans with no marker. (confirmed by running)** Raw
at offset 15987: `将需处理的页面设置404页面，生成死链文件整理被黑、无效等需要被删除的资源，<b>页面设置404，一定是404页面</b>。`
The entry prints the two spans as consecutive blockquote lines; between them the page carries the step-1 instruction to
build the dead-link file from the hacked/invalid resources to be deleted. L83's rendering hides it behind a semicolon
("… to a 404 page; setting a page to 404 …"), and the silence bullets (L99–L102) cover only "the 1–2 week effect cycle …
and the file-placement steps" (L101), not this clause. Two lesser instances of the same gap: at L55–L56 the word 可能会
sits between the two spans (text nodes 57/58/59) — disclosed in the rendering but not marked as inter-span text — and
L27's span opens with a dangling `的` because 页面 is split off by `<span>` (`'页面的TCP协议状态' in body` -> False;
`'的TCP协议状态'` -> 1), while L28 cites 页面的 as a qualifier the quote cannot show. Peer convention marks this
exactly: `yahoo-japan-nonexistent-url-recrawl.md` — "The verb sits between this span and the next, outside both quotes."
Fix: one clause at L82 naming the dropped `生成死链文件…` instruction (and the split of 页面 / the position of 可能会).

**D5 — MEDIUM — L95 — cross-link overclaim: "each asks that the server return 404". (confirmed by running)** The cited
peer entry this claim rests on says the opposite for S419: `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md:29` — "The
verb is 確認してください, please confirm: [S419] asks the publisher to check whether that setting exists", with the
check/set division tagged [INFERENCE] on the same line; its quoted span is `設定されているかを確認してください` (L27).
Only S420 asks for the status (`yahoo-japan-nonexistent-url-recrawl.md:40`, "The status the page asks for instead").
Fix: "S419 asks the publisher to confirm the 404 setting exists; S420 asks for that status instead."

**D6 — LOW — L72 — 主动或被动 dropped from the remedy's scope. (confirmed by running)** Page text (text node 32):
`网站内部主动或被动添加了错误内容链接，发现后需要及时做404处理，如网站被恶意添加大量黄反内容等` (`grep -o -F '主动或被动'
S421.html | wc -l` -> 1). The entry compresses this to "For a wrong content link added internally", losing that the link
may be added passively (the page's own example is malicious injection). Fix: "added internally, actively or passively
(主动或被动; the page's example is malicious injection)".

**D7 — LOW — L93 –L104 — three page-silence claims carry no sweep. (confirmed by running)** L95 "states no rate or
backoff effect" and L100 "states no definition of a monitor or a link checker". The claims are **true** — my sweeps over
`S421.html`: 监控 0, 链接检查 0, 速率 0, 频率 0, 退避 0, 移除 0, 删除链接 0 — but the entry prints no command, while both
comparators do (`baidu-spider3-dead-link-model.md`, "Page-silence sweeps (2026-10-25 …)"; `yahoo-japan-deleted-url-recrawl.md`,
same). Fix: one sweep line, as the sibling has. Related: L55's quote stops before the page's own crawl consequence
`从而不能更好的进行网站抓取和展现` (text node 60); "no rate or backoff effect" stays true, but the page does state a
crawl effect, so say so where the omission is made.

**D8 — LOW — L49, L91, L95 — unlocatable cross-references. [INFERENCE]** L95 identifies the Yahoo peers by id only
("(S419)", "(S420)") while the Google peer on the same sentence carries a path; the sibling lists all three with paths
(`baidu-spider3-dead-link-model.md`, "Cross-links" section). L49 and L91 cite "the staged candidate's assertion (b)/(c)"
with no artifact, where the sibling names its staging row ("shokuknow `merge/kake/`, the staging row for this page"). Not
a fidelity error; it costs a reader the ability to check either half.

Renderings otherwise audited clean (item 2): each of L16, L22, L28, L32, L42, L48, L57, L65, L75, L82, L89 preserves its
span's qualifiers (一般是指, 明确表示, 常见的如/等, 或/等, 无法, 定期/大量/可能会, 最近/导出, 及时, 需处理/一定是, 仅/请一定/可能会/
整个文件). H1 and `ground:` promise nothing the body does not prove, apart from D1's "splits/separates".

## RECHECK RUN:

Command as printed on L3, grep arm against the **retained** body (curl arm **unrun** — no live fetch this seat):

`grep -F -c '协议死链和内容死链' .ufo/waves/round-57/sources/S421.html` -> **1** — matches the header's `-> 1` and its
parenthetical "(grep against the retained body 1, 2026-10-25)". Header trio is well-formed and runnable: `source:` names
S421 and the URL that `receipts.json` records for it; `verified-at: 2026-10-25`; `recheck: 180d` (an accepted token form);
page prints `发布日期：2022-09-09`, matching L1. Only D3 limits the locator.

## CROSS-LINK CHECKS:

- `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` — exists (`ls`); L18 holds the quoted span
  `クローラーは削除されたウェブページと認識できず、` and renders it "the crawler cannot recognise the deleted web page",
  the same rendering L95 gives. Its condition quote is `「HTTP 200 OK」` (L18–L20), so "concern a URL that answers
  `HTTP 200 OK`" holds. **"each asks that the server return 404" fails here** — see D5.
- `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` — exists; L36 holds `巡回を続けます`, rendered "it continues
  the crawl"; its section L40 "The status the page asks for instead" carries the 404 request. Holds.
- `corpus/knowledge/crawl-error-status-table.md` (S286) — exists, 14 lines; states "Google's crawl-errors page says
  Googlebot will scale back its crawling if it detects that your servers are having trouble (S286)" and "Only one
  sentence is admitted". L95's "admits one sentence (Googlebot scales back …)" is exact. Holds.
- Registry identity of the peers checked against `corpus/SOURCES.md:165-166`: S419 = 002856.php (削除したウェブページが
  巡回され続ける), S420 = 002857.php (存在しないウェブページが巡回される) — matches "deletion entry" / "nonexistent-URL
  sibling".

## STYLE:

Comparators: `yahoo-japan-deleted-url-recrawl.md` (64 lines / 9109 B, 6 `##`, Quote classes + Scope note),
`baidu-friendly-crawl-guidance.md` (68 / 4596, 4 `##`, Quote classes, no Scope note line), same-round sibling
`baidu-spider3-dead-link-model.md` (78 / 8933, 9 `##`, Quote classes + Scope note + page-silence sweeps). This entry:
104 lines / 7314 B, 5 `##`, **no `## Quote classes`**, Scope note present (L104).

- Length and the "What this entry does not establish" + `Scope note:` shape are in family; the scope note (L104) is
  parallel to the peers' and correctly restricts the claim to the page's text.
- Structure diverges twice. (a) **No `## Quote classes`**: 3 of 4 comparators, including the same-round sibling, state
  raw-substring / single-occurrence / article-block / ≤25-unit / ≤40-character / sha256 provenance there; this entry
  leaves the whole span-provenance claim unstated even though it carries 14 `[S421]` citations. (b) It opens on
  title typography (L8) where every peer opens on what the lane already holds and what this page adds — and L8 is the
  line that is wrong (D2). Also, peers cite the section for each off-anchor quote; see D3.
- Evidence density: peers carry page-silence sweeps with printed counts; this entry asserts silence without them (D7).

## ADMIT OR REPAIR:

**REPAIR** — small, wording-only edits: D1 (drop "splits/separates/divides", keep 包括), D2 (fix the title sentence),
D3 (name § 二 and § 三 at L78/L83), D4 (one clause for the dropped `生成死链文件…` instruction), D5 (S419 confirms, S420
asks); add the `## Quote classes` line and one silence-sweep line (D7) and the peer paths (D8). Span, unit, length,
recheck and cross-link *content* all hold at revision 4b8c730; nothing here disputes 8/8 on the counter.

VERDICT: REPAIR-before-admit — spans, ceilings, recheck and cross-link quotes all verify at 4b8c730, but five wording defects (including-claim upgraded to exhaustive partition; false title-typography claim; two unnamed quoted sections plus one unmarked elision; S419 misdescribed as asking for 404) and two style gaps (no Quote classes, no silence sweeps) need fixing.
