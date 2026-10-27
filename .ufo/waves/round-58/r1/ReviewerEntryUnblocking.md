# ReviewerEntryUnblocking

Scope: sentence-level fidelity of `corpus/knowledge/baidu-spider-unblocking.md` at the assigned build `c1e39ef3567542b2dc602cc235ed717d6dfbd915` (file unchanged from there to current worktree, `git diff --stat` empty) against the retained body `.ufo/waves/round-58/sources/S424.html` (sha256 `3ef1275b…`, fetched 2026-10-26T23:35:46+00:00, HTTP 200 per `sources/receipts.json`). References used: `w1/ReviewerEntryFidelityPrep.md` (S424 marked reference) and `w1/CriticEntryOverreach.md`. Read-only seat: no lane file mutated; scratch under `/fast/scratch/hyaku/kake-r58/ReviewerEntryUnblocking` (deleted after; no receipts needed — all evidence inline below). Method: `span_tools.py check S424 '<span>'` (the C5 counter's own code) for every quotation, raw-HTML text-node reads, sweep counts re-run on the raw body and on the article block (`span_tools.py window S424` saved to scratch).

## FINDINGS:

1. **LOW — intro paraphrase joins the page's two alternative symptoms with "and" (line 8).**
   Entry: "it asks why a site or smart mini-program whose content is very high quality has no Baiduspider fetch record **and** is not included or displayed in Baidu search."
   Page: "为什么网站或智能小程序资源的内容非常优质，但是没有查询到百度蜘蛛抓取记录，**或**在百度搜索中没有得到收录和展现？" — 或 is an alternation between "no crawl record found" and "not indexed/displayed"; "and" asserts both jointly.
   Fix: "...has no Baiduspider fetch record **or** is not included or displayed in Baidu search."

2. **LOW — lane bullet substitutes an inferred IP remedy for the page's stated one (line 98, [INFERENCE]-marked).**
   Entry: "The remedies are publisher-side: change robots.txt, adjust the anti-crawler policy, **or clear the firewall's IP block**."
   Page: the IP remedy is the same sentence as the UA remedy — "【建议方案】解除百度IP封禁：查看网站反爬虫策略，进行策略调整。" (policy adjustment, quoted correctly later in the entry); the firewall backend is named as the place to **check** ("需要查看防火墙配置系统后台，检查是否存在百度蜘蛛的IP级别封禁措施"), not a remedy the page gives.
   Fix: "...adjust the anti-crawler policy (the page repeats the policy-adjustment remedy for the IP kind and names the firewall configuration backend as the place to check)."

No MEDIUM/HIGH findings. Checked and clean:

- **All 15 blockquote spans verify** with `span_tools.py check S424`: `in_text_node` True, `count_in_body` 1, `unique` True (also absent from S423), within both ceilings each — 21u/21c, 12u/12c, 15u/15c, 13u/13c, 21u/22c, 16u/16c, 20u/33c, 14u/29c, 9u/20c, 20u/31c, 14u/20c, 12u/14c, 24u/29c, 17u/20c, 25u/32c. The entry's own claim ("`in_text_node` true, `count_in_body` 1, within both ceilings for each span used as a quotation") is exactly true.
- **Over-ceiling prose computations verify**: labelled robots sentence 21u/**49c** ("over the 40-character ceiling" ✓); IP paragraph **47u/55c** ("over both ceilings" ✓); opening symptom sentence 77u/90c (split justified ✓).
- **curl command text matches the page char-for-char**: raw node is `执行&nbsp;curl --head --user-agent 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)' --request GET 'xxxxxxx'` — the entry's inline code is identical, the literal `&nbsp;` entity is correctly disclosed, the command alone is one text node (`in_content` True, count 1), and `xxxxxxx` (7 x's) matches.
- **Renderings faithful** against the W1 reference: 存在/导致/无法…正常 chain kept; 或-in-list, 等 and 包括 non-exhaustive markers kept; 建议/及时/主动 modalities annotated ("neither a requirement"); 无异常 as "nothing abnormal"; 200 rule kept as "abnormal", never "blocked" (trap 6); 最后/进一步/均 kept; 需要 glossed; 智能小程序 as "smart mini-program"; publication date 2020-07-23 carried in the header.
- **Cross-link claims verified**: id=1516 and id=2855 links exist in the page (line 275, href+label) and neither is carried as a row (grep over `corpus/`: 1516 nowhere; 2855 only in `lessons/round-58.md`, which records "no row is written"); `baidu-friendly-crawl-guidance.md` does state the PC+mobile binding ("如果封禁的agent是Baiduspider，会对PC和移动同时生效" [S329]); `baidu-spider-identification.md` carries the UA strings and the two-step reverse/forward DNS check, and its own 【封禁篇】 pointer matches; `robots-txt-rules.md` holds the host-root location and 4xx refusal semantics (§§2.3.x); `crawler-identity.md` exists as the general identity entry; registry bindings consistent (`corpus/README.md` line 76, `corpus/SOURCES.md` S424 row, `used-by` = this single entry).
- **Gradual-effect attribution (line 102) is true**: retained S423 contains 搜索引擎需要逐渐完成更新，所以百度蜘蛛不…是立即停止抓取网页 (the contiguous string 不是立即 is split across two spans in the raw bytes — the entry uses it as a gloss, not a quote, which is honest), and the sentence sits in the page's single 【封禁篇】; the entry correctly says it is not on S424 and quotes nothing from S423.
- **MUST-NOT list clean**: no render/JS/CSS claims, no IP-range or .baidu.jp geography, no robots timing on S424, no UA-confirms-identity, no reverse-only DNS, no QA7, no "latest guidance", curl 200 never read as Baidu's own response, IP blocking located at the site's firewall. Quote hygiene: 15 blockquotes, zero curly quotes in the file, zero ASCII quotes in prose outside blockquotes.

## SWEEPS RE-RUN:

All counts re-run 2026-10-26 on the retained body (`grep -o -F` on `S424.html`, whole file / article block via `span_tools.py window S424`); every stated number matches.

- sitemap 0/0; Google 0/0; Bing 0/0; 403 0/0; 503 0/0; 日志 0/0; 压力 0/0 — entry states 0 ✓
- 申诉 0/0 ✓ (entry: "sweep `申诉` 0")
- 反馈 4 raw / **1 article block** ✓ (entry says "occurs once in it" — article block, precise; the other 3 are nav/JS, outside the block)
- 抓取频次 **1/0** and 站长平台 **1/0** ✓ — locations confirmed: 抓取频次 is a nav `<li>` link to `/pressure/index`; 站长平台 is a footer link to `developer.baidu.com` ("only in site navigation and footer links" is exact)
- 存在robots封禁 1/1 ✓ (entry: wording named once, inside the page's own curly quotes)
- locator heading 如何验证…封禁百度蜘蛛的情况 1 raw / 1 block ✓ ("occurs verbatim once in the retained body")
- 查看网站反爬虫策略，进行策略调整 **2**/2 ✓ (`count_in_body` 2, not page-unique — entry's stated reason for not quoting it)
- recheck line: `grep -F -c '导致百度蜘蛛无法正常抓取'` on the retained body = **1** ✓
- sha256 of retained body matches `sources/receipts.json` (S424, 22476 bytes) — entry header `source:`/`verified-at:`/`fetched` lines all match receipts

VERDICT: Entry is faithful to S424 — all 15 quotes, the curl command text, every stated sweep count and every cross-link verify against the retained body; only two LOW paraphrase fixes (或→"and" at line 8; inferred firewall IP remedy at line 98), neither touching a quoted span.
