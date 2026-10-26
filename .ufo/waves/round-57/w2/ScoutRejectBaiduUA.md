# ScoutRejectBaiduUA

Artifacts attacked: staged `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/baidu-render-crawl-ua.md` (26 lines, read-only); retained body `.ufo/waves/round-53/sources/S390.html` (22141 B, sha256 a8f9ae70…1506, equals `round-53/sources/receipts.json` S390 `bytes`/`sha256`, confirmed by running); `corpus/SOURCES.md:160`; `w1/ReviewerPlan.md:33-34`. Fresh GET: HTTP 200, 22141 B, saved `ScoutRejectBaiduUA.files/S390.fresh.html`, sha256 0f44b040…65aa2. The two hashes differ ONLY in 3 lines (`diff`, confirmed by running): two `passport.baidu.com` script `?cdnversion=` nonces (l.318-319) and the `ziyuan.baidu.com:8054`→`:8087` port in a login-config line (l.333). All text nodes identical; the page content is unchanged since round 53. Tools installed: none.

## CLAUSE CHECKS:

| # | clause | command | count | page text |
|---|---|---|---|---|
| 1 | "page prints no update stamp" is false; page prints `发布日期：2017-03-24` | `grep -o '发布日期[^<]*' S390.html` (both bodies); line 274 | 1 | `<p class="info-item-time">发布日期：2017-03-24</p>` under `<h1>百度Spider新增渲染抓取UA公告</h1>`. Also `grep -o '更新[^<]\{0,20\}'` → only `更新到高版本浏览器` (nav banner), no revision/update stamp. |
| 2 | clause 1 nuance | same | — | `发布日期` is a PUBLISH date, not an "update stamp". Literal "no update stamp" is true (0 revision stamp); but the staged line says the only date is the one "inside the quoted clause", hiding the printed header date. The misleading framing stands; the proposed reason must say "prints a publish date", not "prints an update stamp". |
| 3 | date sentence inside the body | `grep -o '[^<>]*从3月24日[^<>]*' S390.html` (l.276) | 1 | `…百度搜索会全面启用最新UA来访问站点的上述资源。从3月24日（2017）开始，百度搜索抽取了部分优质站点进行抓取内测，可能会对站点服务器造成一定压力影响，请尽量不要对UA进行封禁，以免造成不可逆转的损失。` |
| 4 | "`从3月24日（2017）开始` stands inside the quoted clause" | read staged `recheck:` line | — | FALSE: the only span in the entry is the `recheck:` grep string, which ends at `…上述资源。` (first sentence). `从3月24日` is NOT in it. Extra defect not in the planner's reason. |
| 5 | `最新UA如下` sentence | `grep -o '[^<>]*最新UA如下[^<>]*' S390.html` | 1 (`最新UA如下：`) | `最新UA如下：` is a plain text line after the `</p>` (l.276-277), not a heading. Followed by `PC：Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)` and `移动：Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) … Mobile/13B143 Safari/601.1 (compatible; Baiduspider-render/2.0; …)`. |
| 6 | `公告正文` count | `grep -o '公告正文' S390.html \| wc -l` | **0** (both bodies) | no such heading. The page's only headings are `<h1>百度Spider新增渲染抓取UA公告</h1>` plus nav `<h4>`s. Staged `§ 公告正文（最新UA如下）` is a fabricated locator. |
| 7 | `"` in staged file | `grep -o '"' staged.md \| wc -l` | **0** (curly `“”` also 0) | entry body has no source span at all; the sole page-text span is a 59-unit/79-char grep string in `recheck:` (> 25 units / 40 chars ceiling) — per `ReviewerPlan.md:33(c)`, not re-measured by me. |
| 8 | held row | `grep -n 'S390' corpus/SOURCES.md` | 2 lines (160 row, 222 round-53 note) | `160: \| S390 \| 百度搜索资源平台 — 百度Spider新增渲染抓取UA公告 — https://ziyuan.baidu.com/wiki/990 \| docs \| A \| … (发布日期 2017-03-24, printed on the page) … \| mined \| 2026-10-25 \| … 180d \| baidu-friendly-crawl-guidance.md, baidu-mobile-matching-error-causes.md`. Held: true; same URL; `used-by` already cites the render facts (`baidu-friendly-crawl-guidance.md:50`, `baidu-mobile-matching-error-causes.md:35` cite S390). The staged entry itself is not in `corpus/knowledge/`. |

Planner-text slip: `ReviewerPlan.md:33` says the body is 20,626 bytes; receipt and `wc -c` say 22,141 (confirmed by running). Correct before logging.

## WHAT THE PAGE SAYS:

Page `https://ziyuan.baidu.com/wiki/990`, title 百度Spider新增渲染抓取UA公告, publish date 2017-03-24. One body paragraph + two agent strings:
- Purpose: 为了…更好地索引和呈现，百度搜索需要访问网站的CSS、Javascript和图片信息，以便更精准地理解页面内容，实现搜索结果最优排名，百度搜索会全面启用最新UA来访问站点的上述资源。
- Scope/date: 从3月24日（2017）开始，百度搜索抽取了部分优质站点进行抓取内测 — a test on a SAMPLE of quality sites, with possible load on servers.
- Instruction: 请尽量不要对UA进行封禁，以免造成不可逆转的损失。
- Strings: PC and 移动 variants, both containing `Baiduspider-render/2.0`.

Staged claims vs page:
- SUPPORTED: fetches CSS/JS/images; purpose (understand page more precisely, rank better); UA `Baiduspider-render/2.0` in PC and mobile forms; asks not to block, losses irreversible; the page says 访问 (access/fetch) and nowhere says 执行/渲染 the script (the "does not say it executes" restraint is correct).
- OVERSTATED: "from 24 March 2017 Baidu started fetching a site's CSS, JavaScript and images with a dedicated user agent" — the page says the 3-24 start was an 内测 on a 部分优质站点 sample, while 全面启用 is stated as intent. The staged body drops "internal test / some quality sites" and "尽量" (please, as far as possible) hardens to an instruction. Held row S390 already has the correct reading.
- NOT SUPPORTED / unverifiable on this page: "The lane's ledger said there was no published Baidu source on rendering … The sweep looked in the course pages" (lane-internal narrative, not page content); `§ 公告正文`; "inside the quoted clause".

Is the reject on merit or form? Mixed, mostly form-plus-two-real-defects. Form: no double-quoted spans, over-ceiling recheck span, duplicate row already held. Merit (page-grounded): a locator that does not exist on the page, a date-provenance statement that is false (date sits in the header, and `从3月24日` is outside the quoted string), and the 内测/sample scope dropped. The core facts (fetch resources, agent string, do-not-block) ARE correct, and are already carried by the held row and two admitted entries, so no page fact is lost by rejecting.

## DECISION:

**Reject** (as staged). Agree with L1, with corrections.

Exact reason text the lesson may log:
"Rejected baidu-render-crawl-ua.md (staged S390 → held kake S390, https://ziyuan.baidu.com/wiki/990): against the retained body (22141 B, sha256 a8f9ae70…1506; fresh GET 2026-10-25 identical text) the page prints `发布日期：2017-03-24` (1 hit) under `<h1>百度Spider新增渲染抓取UA公告</h1>`, so the staged claim that the date lives only inside the quoted clause is wrong, and `从3月24日（2017）开始` is not inside the entry's only quoted span (its `recheck:` string stops at `…上述资源。`); the locator `§ 公告正文（最新UA如下）` has 0 hits for `公告正文` (`最新UA如下：` is a plain line before the PC and 移动 strings, not a heading); the entry carries 0 double-quoted spans and its one grep span is 59 units; the staged text drops that the page says `抽取了部分优质站点进行抓取内测` and states the 3-24 start as a sample test. The page's actual claims — Baidu fetches CSS, JavaScript and images (`访问网站的CSS、Javascript和图片信息`) with `Baiduspider-render/2.0` (PC and mobile) and asks `请尽量不要对UA进行封禁，以免造成不可逆转的损失` — are already held in row S390 and cited in baidu-friendly-crawl-guidance.md and baidu-mobile-matching-error-causes.md."
(Do not call the date an "update stamp"; call it the printed publish date. Use 22,141 B, not 20,626.)

Flip condition (to admit): redraft against held row S390 (extend `used-by`, no duplicate row); name `发布日期：2017-03-24` and `<h1>百度Spider新增渲染抓取UA公告</h1>` / `最新UA如下：` as locators; carry >= 3 raw-substring quotes <= 25 units / 40 chars (e.g. `请尽量不要对UA进行封禁`, `抽取了部分优质站点进行抓取内测`, `Baiduspider-render/2.0` — each is a raw substring of l.276/the UA lines; lengths not machine-checked by me); restate the 3-24 start as a sample test; keep the no-script-execution restraint. If the redraft only repeats what S390 `used-by` entries already say, admit nothing new.

VERDICT: Reject confirmed — 0 `公告正文`, 0 `"`, `发布日期：2017-03-24` printed, row S390 held at SOURCES.md:160; core fetch/UA/do-not-block claims are supported but already held, and the staged text drops the page's 内测/部分优质站点 scope.
