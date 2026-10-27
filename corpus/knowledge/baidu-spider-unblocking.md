source: S424 — https://ziyuan.baidu.com/college/articleinfo?id=3028 — § 如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？ (发布日期 2020-07-23) — fetched 2026-10-26
verified-at: 2026-10-26
recheck: 180d — `curl -fsSL --compressed 'https://ziyuan.baidu.com/college/articleinfo?id=3028' | grep -F -c '导致百度蜘蛛无法正常抓取'` -> 1 (grep against the retained body 1, 2026-10-26)
ground: per-engine crawl hygiene — the three block kinds the operator names (robots, Baidu UA, Baidu IP), the order it asks a publisher to check them in, and one 【建议方案】 remedy per kind

# Baidu's page names three ways a site can block Baiduspider and orders the self-check robots, then UA, then IP

Baidu's college page answers a publisher's complaint rather than stating a rule: it asks why a site or smart mini-program whose content is very high quality has no Baiduspider fetch record or is not included or displayed in Baidu search. Every quoted span below is an exact raw substring of one text node of the retained body (`python3 -B .ufo/waves/round-58/span_tools.py check S424 '<span>'` -> `in_text_node` true, `count_in_body` 1, within both ceilings for each span used as a quotation, 2026-10-26). Quoted spans come from the opening paragraphs above this entry's locator question line and from the three-step check printed under it.

## The symptoms the page names

The page says that after technical analysis it found some sites blocking Baiduspider [S424]:

> "有些网站或智能小程序存在封禁百度蜘蛛的情况"
> "导致百度蜘蛛无法正常抓取"

(rendered: some websites or smart mini-programs are in a situation where Baiduspider is blocked, so Baiduspider cannot fetch them normally — one paragraph, split here because the full sentence exceeds the 25-unit and 40-character ceilings.)

> "无法在百度搜索中正常收录和展现"

(rendered: so they cannot be normally included and displayed in Baidu search; 正常 (normally) is inside the span.)

The third symptom is what the search result shows:

> "或在搜索结果中的摘要展现为"

(rendered: or the summary in the search results displays — the page continues, inside its own curly quotation marks, with the wording 存在robots封禁, literally: a robots block exists. The marked phrase is named here in prose, not quoted, because this entry's quotations use ASCII quote marks only.)

The page's ask and the submission step [S424]:

> "建议开发者及时根据以下内容自查，解除封禁问题"
> "并通过链接提交工具主动提交给我们"

(rendered: the page suggests developers promptly self-check against the following content, resolve the block, and, through the link submission tool, proactively submit to the operator — 建议 is a suggestion and 及时 is prompt, neither a requirement. The two lines are consecutive clauses of one sentence.)

## The three block kinds, as the page lists them

> "常见的封禁行为包括robots封禁、封禁百度UA、封禁百度IP等。"

(rendered: common blocking behaviours include a robots block, blocking the Baidu UA and blocking Baidu IPs, etc. — 常见的 and 等 keep the list exemplary and 包括 introduces rather than exhausts it.)

## The check order the page gives

The locator heading is the question line printed before the three numbered steps; it occurs verbatim once in the retained body and is reproduced in the header line above rather than quoted here.

### Step 1 — robots.txt first

> "1、首先， 查看robots.txt文件，是否存在封禁记录"

(rendered: first, look at the robots.txt file for whether a block record exists — the space after the comma is the page's own raw spacing. The sentence's parenthetical, which this entry does not quote, says a robots.txt file is generally (一般) placed in the site root directory.)

Its 【建议方案】 is labelled 解除robots封禁 and states [S424]:

> "请检查robots.txt文件，及时修改"

(rendered: check the robots.txt file and modify it promptly. The label and the colon before this span are outside it, which is why they are named in prose here; the whole labelled sentence is 49 characters, over the 40-character ceiling.)

The page links its own robots-file explanation (articleinfo id=1516); the link and its target are not carried.

### Step 2 — the Baidu UA check

> "2、robots文件无异常，进一步排查是否存在封禁百度UA情况"

(rendered: if the robots file shows nothing abnormal, further check whether the Baidu UA is blocked — 进一步 is a further step and the step is conditional on step 1.)

The page's 方案一 prints a request command and one reading rule:

> "注：正常返回码是200，其他情况为异常。"

(rendered: note: a normal return code is 200; any other situation is abnormal — 其他情况为异常 is the page's binary reading, so anything other than 200 counts as abnormal here.)

The command, exactly as printed in the same text node (the page writes it as `执行&nbsp;curl …`, with the entity in the raw body): `curl --head --user-agent 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)' --request GET 'xxxxxxx'`. The page says the placeholder is the site domain and gives a domain example; both the command and the UA string exceed the character ceiling, so they are given as code and not as quotations. The page's 方案二 is named only — verify by changing the browser UA — and gives no steps.

Its 【建议方案】 解除百度UA封禁 offers two moves; this is the page-unique second one:

> "或针对百度UA添加策略白名单"

(rendered: or add a strategy whitelist for the Baidu UA — 或 offers it as the alternative to the policy adjustment named immediately before it, which this entry does not quote because that phrase 查看网站反爬虫策略，进行策略调整 occurs twice on the page.)

### Step 3 — IP-level blocks last

> "3、以上验证均无异常，最后进一步排查是否存在IP级别的封禁"

(rendered: if all of the above checks show nothing abnormal, last, further check whether an IP-level block exists — 最后 is last and 进一步 is further.)

> "常见的IP封禁，源自网站的防火墙系统配置"

(rendered: common IP blocks originate in the site's firewall system configuration; the same paragraph adds that the firewall configuration backend needs (需要) checking for an IP-level block on Baiduspider, which is stated in prose here because the whole paragraph is 47 units / 55 characters, over both ceilings.)

Its 【建议方案】:

> "【建议方案】解除百度IP封禁：查看网站反爬虫策略，进行策略调整。"

(rendered: 【suggested remedy】 lift the Baidu IP block: look at the site's anti-crawler policy and adjust the policy — 建议方案 is a suggested plan, not an operator-enforced requirement.)

## How this sits against the lane

- [INFERENCE] The remedies are publisher-side: change robots.txt or adjust the anti-crawler policy. For an IP block, the page repeats the policy-adjustment remedy and names the firewall configuration backend as the place to check. The article block states no appeal route (sweep `申诉` 0); `反馈` occurs once in it, inside the opening 收到一些开发者反馈 (the page received feedback from some developers), not as a route. The submission step it names is the link submission tool quoted above.
- The file whose step 1 reads is the host-root robots file; `robots-txt-rules.md` holds that location and refusal semantics — [INFERENCE] this page assumes that semantics instead of explaining it.
- The page links the operator's own page on correctly identifying and obtaining Baiduspider (articleinfo id=2855, not carried); the lane's Baidu identification material is `baidu-spider-identification.md` (the UA strings and the two-step DNS check), and `crawler-identity.md` holds the general crawler-identity material; this entry does not restate either.
- A robots block aimed at Baiduspider binds PC and mobile together per `baidu-friendly-crawl-guidance.md`; step 1 here states no such scope.
- The gradual effect of a robots.txt change (fetching does not stop immediately, 不是立即) is stated on the operator's Q&A page that `baidu-spider-identification.md` carries, in that page's 【封禁篇】; it is not on this page, is not asserted here as this page's statement, and no span of that page is quoted in this entry.

## What this entry does not establish

- No request was issued, no crawl was observed and no Baidu behaviour was measured; the 200 rule is the page's stated reading, not a test result.
- The page states no crawl rate, no block duration, no removal procedure, no sitemap or log-analysis advice; Google and Bing do not occur in the retained body (sweep `grep -o -F '<word>' .ufo/waves/round-58/sources/S424.html | wc -l`): sitemap 0, Google 0, Bing 0, 403 0, 503 0, 日志 0, 压力 0; 抓取频次 1 and 站长平台 1 occur only in site navigation and footer links (article block sweep 0 and 0).
- The page does not say how a UA block is implemented; it points at the site's anti-crawler policy and at a UA whitelist.
- 方案二 is named without steps, and the 方案一 placeholder is described only as the site domain plus an example.
- The 【建议方案】 labels are guidance (建议), not enforcement statements.

Scope note: a claim about what the operator's page states on one page of its info centre; no URL served under test, no crawl observed, no Baiduspider request made, no Baidu behaviour measured.
