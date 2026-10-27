# EntryUnblocking

Seat EntryUnblocking (leaf, r58 w1, claim C3, page S424). Axes: verbatim fidelity (each quote a page-unique raw substring of one text node, under both ceilings); required coverage (symptoms, three block kinds, ordered check with the 200 rule, all three 【建议方案】 remedies); registry/gate conformance (11-cell row, gate line, unit counts, recheck, omitted); house style (header block, `[INFERENCE]` only where the page is silent, cross-links to existing entries only, closing scope note).

## What ran

- `span_tools.py window S424` (full article window incl. `发布日期：2020-07-23`), `spans S424` (31 text nodes with unit/char counts), `check S424 '<span>'` on 38 candidates (30 distinct): all 15 used returned `in_text_node: True, count_in_body: 1, unique: True, within_ceilings: True`.
- `grep -F -c` on `sources/S424.html`: recheck quote 1, locator heading 1, sweeps below. Title parse: `<title>开发者如何解除封禁百度蜘蛛_搜索学堂_百度搜索资源平台</title>` → cell-2 title `开发者如何解除封禁百度蜘蛛`. Post-write script re-checked all 15 `> "..."` lines (15/15 OK) and asserted the row at 11 cells.

## GATE LINE

- S424 — https://ziyuan.baidu.com/college/articleinfo?id=3028 — accessed 2026-10-26 — § 如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？ (发布日期 2020-07-23) — quote: "导致百度蜘蛛无法正常抓取" (12 units; raw substring of the retained body, sha256 3ef1275b730230f2cb9c14b28b1c4bd08dc363dc7941b63d06c507fb2729cad1, 22476 bytes, HTTP 200)

## REGISTRY ROW

| S424 | 百度搜索资源平台 — 开发者如何解除封禁百度蜘蛛 — https://ziyuan.baidu.com/college/articleinfo?id=3028 | docs | A | **Three block kinds a site can aim at Baiduspider — robots, Baidu UA, Baidu IP — and the ordered self-check the operator gives a site with no crawl record** — the symptoms it names, the check order robots.txt then the UA request then firewall IP blocks, and one 【建议方案】 remedy per kind | § 如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？ (发布日期 2020-07-23) | a site can block Baiduspider through robots.txt, through a rule on the Baidu UA, or at the firewall/IP level; the page orders the check robots.txt first, then the UA request whose 200 is normal and anything else abnormal, then IP-level firewall blocks, and gives one suggested remedy per kind | mined | 2026-10-26 | 180d | corpus/knowledge/baidu-spider-unblocking.md |

## UNIT COUNTS

- `"有些网站或智能小程序存在封禁百度蜘蛛的情况"` 21u/21c; `"导致百度蜘蛛无法正常抓取"` 12u/12c; `"无法在百度搜索中正常收录和展现"` 15u/15c; `"摘要展现为“存在robots封禁”字样"` 11u/19c; `"建议开发者及时根据以下内容自查，解除封禁问题"` 21u/22c
- `"并通过链接提交工具主动提交给我们"` 16u/16c; `"常见的封禁行为包括robots封禁、封禁百度UA、封禁百度IP等。"` 20u/33c; `"1、首先， 查看robots.txt文件，是否存在封禁记录"` 14u/29c; `"请检查robots.txt文件，及时修改"` 9u/20c; `"2、robots文件无异常，进一步排查是否存在封禁百度UA情况"` 20u/31c
- `"注：正常返回码是200，其他情况为异常。"` 14u/20c; `"或针对百度UA添加策略白名单"` 12u/14c; `"3、以上验证均无异常，最后进一步排查是否存在IP级别的封禁"` 24u/29c; `"常见的IP封禁，源自网站的防火墙系统配置"` 17u/20c; `"【建议方案】解除百度IP封禁：查看网站反爬虫策略，进行策略调整。"` 25u/32c
- Locator heading `如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？` — counter 25u/26c, count 1; **not quoted** (the seat spec calls it over 25 units; see Findings).

## RECHECK RUN

- `grep -F -c '导致百度蜘蛛无法正常抓取' /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/sources/S424.html` -> 1; the locator heading -> 1. The `curl` half was **not run** (no network fetch in this seat). Sweeps (`grep -o -F '<word>' ... | wc -l`): sitemap 0, Google 0, Bing 0, 403 0, 503 0, 日志 0, 压力 0, 申诉 0; 抓取频次 1 and 站长平台 1 (navigation/footer only, article block 0/0); 移动 1 (navigation 移动适配, article block 0); 反馈 1 (article opening 收到一些开发者反馈).

## OMITTED

- Link targets named in prose but not carried: robots-file explanation (articleinfo id=1516), crawler identification (id=2855). `方案二` (change browser UA) is named without steps and is not page-unique → prose. The `curl` command (142-char node) and the 81-char `Baiduspider/2.0` UA string exceed the 40-character ceiling → code. The domain example after `xxxxxxx为网站域名,如：` is split across three text nodes → prose.
- The sibling page named in this round's claim statement has no registry row and contributes nothing: its 【封禁篇】 and its gradual-effect statement (不是立即) are not quoted; the entry names the sibling entry `baidu-spider-identification.md` being drafted this round and asserts nothing from that page. Crawl rate, block duration, removal procedure, sitemap/log advice and other engines are absent from the page (sweeps), so unwritten.

## ENTRY

```markdown
source: S424 — https://ziyuan.baidu.com/college/articleinfo?id=3028 — § 如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？ (发布日期 2020-07-23) — fetched 2026-10-26
verified-at: 2026-10-26
recheck: 180d — `curl -fsSL --compressed 'https://ziyuan.baidu.com/college/articleinfo?id=3028' | grep -F -c '导致百度蜘蛛无法正常抓取'` -> 1 (grep against the retained body 1, 2026-10-26)
ground: per-engine crawl hygiene — the three block kinds the operator names (robots, Baidu UA, Baidu IP), the order it asks a publisher to check them in, and one 【建议方案】 remedy per kind

# Baidu's page names three ways a site can block Baiduspider and orders the self-check robots, then UA, then IP

Baidu's college page answers a publisher's complaint rather than stating a rule: it asks why a site or smart mini-program whose content is very high quality has no Baiduspider fetch record and is not included or displayed in Baidu search. Every quoted span below is an exact raw substring of one text node of the retained body (`python3 -B .ufo/waves/round-58/span_tools.py check S424 '<span>'` -> `in_text_node` true, `count_in_body` 1, within both ceilings for each span used as a quotation, 2026-10-26). Quoted spans come from the opening paragraphs above this entry's locator question line and from the three-step check printed under it.

## The symptoms the page names

The page says that after technical analysis it found some sites blocking Baiduspider [S424]:

> "有些网站或智能小程序存在封禁百度蜘蛛的情况"
> "导致百度蜘蛛无法正常抓取"

(rendered: some websites or smart mini-programs are in a situation where Baiduspider is blocked, so Baiduspider cannot fetch them normally — one paragraph, split here because the full sentence exceeds the 25-unit and 40-character ceilings.)

> "无法在百度搜索中正常收录和展现"

(rendered: so they cannot be normally included and displayed in Baidu search; 正常 (normally) is inside the span.)

The third symptom is what the search result shows:

> "摘要展现为“存在robots封禁”字样"

(rendered: or what the summary in the search result displays is the wording “存在robots封禁” — literally "a robots block exists"; the curly quotation marks are the page's and sit inside the quoted span, which is why the span is wrapped in ASCII quotes here.)

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

- [INFERENCE] The remedies are publisher-side: change robots.txt, adjust the anti-crawler policy, or clear the firewall's IP block. The article block states no appeal route (sweep `申诉` 0); `反馈` occurs once in it, inside the opening 收到一些开发者反馈 (the page received feedback from some developers), not as a route. The submission step it names is the link submission tool quoted above.
- The file whose step 1 reads is the host-root robots file; `robots-txt-rules.md` holds that location and refusal semantics — [INFERENCE] this page assumes that semantics instead of explaining it.
- The page links the operator's own page on correctly identifying and obtaining Baiduspider (articleinfo id=2855); `crawler-identity.md` holds the lane's identification material and this entry does not restate it.
- A robots block aimed at Baiduspider binds PC and mobile together per `baidu-friendly-crawl-guidance.md`; step 1 here states no such scope.
- The gradual effect of a robots.txt change (the change is not immediately (不是立即) a stop to fetching) is stated on the sibling page whose entry `baidu-spider-identification.md` is being drafted in this same round; it is not on this page and is not asserted here as this page's statement, and no span of that sibling page is quoted in this entry.

## What this entry does not establish

- No request was issued, no crawl was observed and no Baidu behaviour was measured; the 200 rule is the page's stated reading, not a test result.
- The page states no crawl rate, no block duration, no removal procedure, no sitemap or log-analysis advice; Google and Bing do not occur in the retained body (sweep `grep -o -F '<word>' .ufo/waves/round-58/sources/S424.html | wc -l`): sitemap 0, Google 0, Bing 0, 403 0, 503 0, 日志 0, 压力 0; 抓取频次 1 and 站长平台 1 occur only in site navigation and footer links (article block sweep 0 and 0).
- The page does not say how a UA block is implemented; it points at the site's anti-crawler policy and at a UA whitelist.
- 方案二 is named without steps, and the 方案一 placeholder is described only as the site domain plus an example.
- The 【建议方案】 labels are guidance (建议), not enforcement statements.

Scope note: a claim about what the operator's page states on one page of its info centre; no URL served under test, no crawl observed, no Baiduspider request made, no Baidu behaviour measured.
```

## Findings

- **Locator is a paragraph, not a heading element**: the body has `<p>如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？</p>`; the `§` carries it because the spec names it and it occurs verbatim once.
- **Unit-count disagreement, verbatim**: the spec calls that line "over 25 units"; `check` reports 25u/26c. It is the anchor only, so no quotation depends on either count.
- **Ceiling collisions force splits**: `【建议方案】解除robots封禁…` is 49 characters and the IP-cause node is 47u/55c; each became a page-unique sub-span plus prose that names the label and keeps 需要.
- **Not page-unique** (prose/code only): `没有查询到百度蜘蛛抓取记录` (2), `查看网站反爬虫策略，进行策略调整` (2, both remedies), `一般robots.txt文件放置在网站根目录下` (body 1, `unique: False`), `变更浏览器UA验证` (`unique: False`), `curl --head --user-agent` / `--user-agent` (`unique: False`).
- **Forward reference**: `ls corpus/knowledge` shows `crawler-identity.md`, `robots-txt-rules.md`, `baidu-friendly-crawl-guidance.md` but no `baidu-spider-identification.md`; the entry calls it the sibling entry drafted this round, with no S-id and no quotation — confirm it lands.
- **Registry**: rows run to S422; the round's two new rows are absent, so this is an append. No S-id outside the registry is cited; `[S424]` is valid once the row lands.

Limits: no request issued and no crawl or Baidu behaviour observed; no lane git/jj command run; no lane file written beyond the two artifact paths; scratch `/fast/scratch/hyaku/kake-r58/EntryUnblocking/`; no tool installed, no pacman transaction attempted.

Artifacts: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/w1/EntryUnblocking.files/baidu-spider-unblocking.md` (entry, 9368 bytes, 112 newlines) and `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/w1/EntryUnblocking.md` (this report).

VERDICT: S424 entry drafted and self-verified — 15/15 quoted spans page-unique, one text node, within ceilings; symptoms, three block kinds, ordered check with the 200 rule and all three 【建议方案】 remedies carried; no sibling-page quotation; registry row and gate line emitted for the integrator.
