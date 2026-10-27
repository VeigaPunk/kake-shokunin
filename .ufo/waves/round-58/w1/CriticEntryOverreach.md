# CriticEntryOverreach

Pre-draft critique of C3's planned content (identification entry citing S423; unblocking entry citing S424).
Evidence read: contract.md C3; c58_quote_truth.py C1–C8; sources/receipts.json; `span_tools.py window/check` on S423 and S424 (checked on retained bodies, sha256 frozen at contract commit); staged entry `merge/kake/knowledge/corpus/knowledge/baidu-crawler-identification.md` (row S395 → S423); ScoutStagedS395.md. Unrun: live re-fetch (retained bodies only), S409 content (not read; registry row only). Checks run: `span_tools.py check` spans below; window term scan for 渲染/脚本/CSS/JavaScript/JS/2017/日本/IP段/天/小时/分钟 (zero hits in both article blocks).

## UNSUPPORTED TEMPTATIONS:
- **Render agent executes JavaScript / fetches CSS, JavaScript and images.** Neither article block contains 渲染, 脚本, CSS, JavaScript or JS; the only render trace is the UA token `Baiduspider-render/2.0` inside the channel UA strings. The pages never state what the render agent fetches or does. (S423 UA lists only.)
- **Baiduspider-render is only for mobile.** Contradicted by S423: the -render token appears in the 移动UA list, the PC UA list and the 小程序UA list. (See disagreements.)
- **Baidu publishes crawler IP ranges / address lists.** Neither page prints any IP range or address block. Identification is hostname-based: `方式二：双向DNS解析认证` (第一步 reverse, 第二步 forward). IP mentions on both pages are the *site's* firewall (`常见的IP封禁，源自网站的防火墙系统配置`).
- **robots changes take effect within N days.** S423 only: `搜索引擎需要逐渐完成更新，所以百度蜘蛛不是立即停止抓取网页，请耐心等待` — no number. S424 has no timing sentence.
- ***.baidu.jp is for Japan.** The page never explains the suffix; it appears only as a valid hostname form next to `*.baidu.com`. No geography anywhere.
- **UA match alone confirms it is Baiduspider.** UA (方式一) only permits positive *exclusion* on mismatch (`如果UA信息不对，可以直接判断为非百度搜索的蜘蛛`); confirmation is 方式二 (`IP地址一致可确认spider来自百度搜索引擎`).
- **Reverse DNS alone decides.** 方式二 is explicitly 双向: 第一步 reverse (`非*.baidu.com或*.baidu.jp即为冒充。`), 第二步 forward (`IP地址不一致即为冒充`). Reverse-only is not the page's verdict.
- **Blocking the UA removes pages from the index.** 封禁篇 Q2 lists these as possible symptoms across all block kinds: `没有查询到百度蜘蛛任何抓取记录` / `在百度搜索中没有得到收录和展现` / `流量异常下降` / `摘要展现为“存在robots封禁”字样` — not a UA-specific causal claim.
- **Unblocking restores indexing soon/guaranteed.** Page says `及时解除封禁…等待恢复`; no timeline or guarantee.
- **Baidu performs IP blocking.** Both pages locate IP blocking at the site: `常见的IP封禁，源自网站的防火墙系统配置`.
- **The curl check's 200 is Baidu's response.** The probe targets the operator's own site: `curl --head --user-agent '…Baiduspider/2.0…' --request GET 'xxxxxxx'`; `正常返回码是200` = the site answers 200 to the spider UA (else UA-blocked). The check tests UA only, not IP or DNS.
- **"A publisher blocking by UA must allow both" / "asks you not to block the render agent".** The only don't-block sentence is generic: `若网站需要百度蜘蛛抓取一定不要做任何封禁哦（封禁相关参考下文内容）`. No sentence names -render or JavaScript.
- **The same agent the platform's 2017 announcement introduced.** S423 contains no 2017; its only date is `发布日期：2022-08-19`. The 2017 render-UA introduction lives on another row (S409; registry only).
- **Crawl frequency is a section.** S423's two section headers are `【抓取篇】` and `【封禁篇】`; crawl frequency is Q4 inside 抓取篇 (`【抓取频次】工具调整频次`).
- **S424 covers identification.** S424 links out for identification (`正确识别和获取百度蜘蛛` https://ziyuan.baidu.com/college/articleinfo?id=2855); its own body is unblocking only.
- **Pages are current guidance as of 2026-10-26.** Publication dates are 2022-08-19 (S423) and 2020-07-23 (S424); quoting them as "Baidu's current procedure" must carry those dates.
- **Baiduspider-render is a separate crawler.** The page defines the *name* (`Baiduspider也叫百度蜘蛛，是百度搜索引擎的一个自动程序`); per-agent roles/separation are inference, not page text.
- **"QA7" is the unblocking reference.** 封禁篇 Q2 says `解除封禁参考QA7` but the page has only Q1–Q3 — dangling cross-reference. (Internal page defect; see disagreements.)

## PAGE DISAGREEMENTS:
- **Same sentence, different markup: `正常返回码是200`.** On S424 it is one text node (`注：正常返回码是200，其他情况为异常。`; check: unique, in_text_node True). On S423 the "200" sits in its own text node (window shows a bare `200` line), so `正常返回码是200` is *not* a substring of one text node there (check: count_in_body 0). A quote valid from S424 is invalid from S423; authors must pick the page whose node text matches.
- **Render agent appears in all three channels on S423** (移动UA second line, PC UA second line, 小程序UA only line). Any "render is mobile-only" phrasing contradicts S423 itself.
- **Publication dates differ and are inverted vs the link direction:** S423 2022-08-19, S424 2020-07-23 — S423 (newer) cites S424 (older) as its unblocking detail page (`详情可参考《开发者如何解除封禁百度蜘蛛》`). S424 must not be presented as the newer/latest guidance.
- **Timing language exists only on S423** (`不是立即停止抓取网页`, `逐渐完成更新`); S424 has none. An unblocking entry citing S424 for "gradual effect" mixes sources.
- **Terminology:** S423 says `小程序`; S424 says `智能小程序`.
- **Staged row/entry vs pages:** (a) staged anchor "no revision printed" is false — both pages print `发布日期` (2022-08-19 / 2020-07-23; neither prints a 更新/修订 date, so only "no update date" holds); (b) staged anchor `【抓取篇】→「第一步：DNS反查IP」段末句` is ambiguous — the clause `非*.baidu.com或*.baidu.jp即为冒充。` repeats in platform items ①–③ with `&nbsp;` separators and 第一步 continues past it; (c) staged "reverse lookup" framing omits 第二步, which is the actual deciding step; (d) staged scope's Yahoo clause is not on either page (lane history); (e) staged `verified-at 2026-10-24` vs contract round date and receipts `fetchedAt 2026-10-26T23:35Z`; (f) staged filename `baidu-crawler-identification.md` vs landed `baidu-spider-identification.md` / `baidu-spider-unblocking.md` (counter C1 expects the staged name absent); (g) staged `recheck: 180d` form is fine, but row `recheck` cell must match the counter's regex (ISO date / NNd / on-release).
- **Agreement to preserve (not a disagreement):** both pages give the same curl probe and the same 200 expectation and the same three block kinds (robots/UA/IP).
- **S423-internal defect:** `解除封禁参考QA7` — no Q7 exists on the page; an entry must not relay it as a working reference.

## MUST-NOT LIST:
- No "render agent fetches/executes CSS, JavaScript or images" (unsupported by both pages).
- No "Baiduspider-render is mobile-only" (contradicted by S423 PC/小程序 UA lists).
- No "Baidu publishes IP ranges/addresses" (neither page).
- No "*.baidu.jp is for Japan" (no geography on either page).
- No robots-effect time window (N days/hours) — only "not immediate; gradual".
- No immediate/guaranteed re-indexing after unblocking.
- No "UA matches ⇒ it is Baiduspider" — mismatch excludes; DNS confirms.
- No reverse-only DNS presentation — the forward-confirmation step is part of the page's verdict.
- No "asks you not to block the render agent" / "must allow both" (generic don't-block sentence only).
- No S409/2017 attribution to S423.
- No "crawl-frequency section" — it is Q4 under 抓取篇.
- No S424 as an identification source (it links out to id=2855).
- No reading the curl 200 as Baidu's own response — it probes the operator's site.
- No "Baidu blocks IPs" — the page says site firewalls do.
- No quoting `正常返回码是200` from S423 (text-node split) — use S424 if the sentence is needed.
- No "QA7" reference (dangling).
- No "latest as of 2026" without the publication dates 2022-08-19 / 2020-07-23.
- No lane/Yahoo history presented as page support.
- Quote discipline: ≤25 units and ≤40 characters, raw substring of one article text node, ASCII double quotes, page-unique; the S423 identification quote `非*.baidu.com或*.baidu.jp即为冒充。` (6u/28c, unique) and S423 `双向DNS解析认证` (6u/9c, unique) verify clean; `Baiduspider-render/2.0` is NOT usable as a quote (occurs 3× in S423).

VERDICT: The C3 drafts must drop the render-fetch/execute, IP-range, *.baidu.jp-is-Japan, robots-timing and UA-confirms temptations, fix the 200 text-node split and the QA7 reference, present identification as reverse+forward two-step, use S424 only for unblocking, and carry both publication dates.
