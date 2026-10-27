# ReviewerEntryFidelityPrep

Claim C3 fidelity reference, independent of the entry scribes. Method: `python3 -B .ufo/waves/round-58/span_tools.py window S423` and `window S424` (both ran, exit 0), article blocks read in full; frozen contract C3 section read. No counter runs (not this seat's check). Marking scheme: after each translated sentence, `〔…〕` lists the Chinese source tokens that are qualifiers (QUAL), modals (MOD), or scope words (SCO/conditionals COND/list-scope L-SCO/negation NEG), with glosses. Bold inside the translation marks the same words.

## REFERENCE S423:
Source: 搜索问答剧场【五】"百度蜘蛛"全面解析 ("Search Q&A Theater #5 — Comprehensive Analysis of the 'Baidu Spider'"), published 2022-08-19, page id=3457. Scope here: 【抓取篇】 (Crawling chapter) Q1–Q4 only. Note: the retained S423 body also contains a 【封禁篇】 (Blocking chapter; Q1–Q3) — quoted in TRAPS below, but not part of this reference's carried parts.

Q1. 什么是 Baiduspider？ — Q: What is Baiduspider?
A: Baiduspider, also called the Baidu spider (百度蜘蛛), is an automated program of the Baidu search engine; its role is to visit web pages on the Internet and build an index database, so that users can find site content in Baidu search.
〔是=is, copula, factive; 也=also, additive SCO; 一个=a, one-member SCO; 作用=role/purpose, functional SCO; 使…能=enable…can, MOD; 中=in, locative SCO〕

Q2. Q: How can one tell that an ongoing crawl is a genuine Baidu spider?
A: There are two ways to identify the Baidu spider.
〔两个=two, enumerative SCO; 可以=can, MOD〕

方式一：查看UA信息。/ Method 1: check the UA (user-agent) information.
如果UA信息不对，可以直接判断为非百度搜索的蜘蛛。/ If the UA information is wrong, it can be directly judged to be a spider that is not from Baidu search.
〔如果=if, COND; 不对=wrong, qualifier QUAL; 直接=directly, QUAL; 可以=can, MOD; 非=not, NEG〕

目前UA分为移动、PC、和小程序三个应用场景，这三个渠道UA分别如下：/ Currently, UAs fall into three application scenarios — mobile, PC, and mini-program — and the UA for each of these three channels is respectively as follows:
〔目前=currently, temporal SCO; 三个=three, enumerative SCO; 分别=respectively, distributive SCO; 这三=these three, referential SCO〕

移动UA：Mozilla/5.0 (Linux;u;Android 4.2.2;zh-cn;) AppleWebKit/534.46 (KHTML,like Gecko)Version/5.1 Mobile Safari/10600.6.3 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html) 或 Mozilla/5.0 (iPhone;CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko)Version/9.0 Mobile/13B143 Safari/601.1 (compatible; Baiduspider-render/2.0;+http://www.baidu.com/search/spider.html) / Mobile UA: … (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html) or … (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html). (Literal UA strings; distinguishing tokens: product `Baiduspider/2.0` / `Baiduspider-render/2.0`, comment syntax `+<verification-url>`.)
〔或=or, alternative list SCO〕

PC UA：Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html) 或 Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html) / PC UA: … (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html) or … (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html).
〔或=or, alternative list SCO〕

小程序UA：Mozilla/5.0 (iPhone;CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko)Version/9.0 Mobile/13B143 Safari/601.1 (compatible; Baiduspider-render/2.0;Smartapp; +http://www.baidu.com/search/spider.html) / Mini-program UA: … (compatible; Baiduspider-render/2.0; Smartapp; +http://www.baidu.com/search/spider.html). (Extra `Smartapp` token distinguishes the mini-program channel.)

方式二：双向DNS解析认证 / Method 2: two-way DNS resolution verification.
第一步：DNS反查IP，开发者通过对日志中访问服务器的IP地址运行反向DNS查找，判断某只spider是否来自百度搜索引擎，Baiduspider的hostname以*.baidu.com或*.baidu.jp的格式命名，非*.baidu.com或*.baidu.jp即为冒充。/ Step 1: reverse-DNS lookup of the IP. The developer runs a reverse-DNS lookup on the IP addresses that accessed the server, as recorded in the logs, to judge whether a particular spider comes from the Baidu search engine. Baiduspider hostnames are named in the format *.baidu.com or *.baidu.jp; anything not of the form *.baidu.com or *.baidu.jp is an impostor.
〔第一步=step 1, ordering SCO; 是否=whether, yes/no SCO; 某=particular, indefinite SCO; 以…格式=in the format, mode SCO; 或=or, alternative SCO; 非…即=not … is, NEG equivalence; 冒充=impostor, judgment term〕

根据平台不同验证方法不同，如linux/windows/os三种平台下的验证方法分别如下：/ The verification method differs by platform; for example, the methods on the three platforms linux/windows/os are respectively as follows:
〔不同=differ, comparative QUAL; 如=for example, exemplification SCO; 三种=three, enumerative SCO; 分别=respectively, distributive SCO〕

①在linux平台下，可以使用host ip命令反解ip来判断是否来自Baiduspider的抓取。/ ① On Linux, you can use the `host ip` command to reverse-resolve the IP and judge whether the crawl comes from Baiduspider.
②在windows平台或者IBM OS/2平台下，可以使用nslookup ip命令反解ip来判断是否来自Baiduspider的抓取。/ ② On Windows or IBM OS/2, you can use the `nslookup ip` command to reverse-resolve the IP and judge whether the crawl comes from Baiduspider.
③在mac os平台下，可以使用dig命令反解ip来判断是否来自Baiduspider的抓取。/ ③ On macOS, you can use the `dig` command to reverse-resolve the IP and judge whether the crawl comes from Baiduspider.
〔可以=can, MOD (×3); 是否=whether (×3); 或者=or, alternative SCO〕

第二步：对域名运行正向DNS查找。对第1步中通过命令检索到的域名运行正向DNS查找，验证该域名与您日志中访问服务器的原始IP地址是否一致，IP地址一致可确认spider来自百度搜索引擎，IP地址不一致即为冒充。/ Step 2: run a forward-DNS lookup on the domain. Take the domain retrieved by the command in step 1, run a forward-DNS lookup on it, and verify whether that domain matches the original IP address that accessed your server in your logs. If the IP addresses match, the spider can be confirmed to come from the Baidu search engine; if they do not match, it is an impostor.
〔第1步=step 1, referential SCO; 是否=whether; 一致=match, equivalence; 可确认=can be confirmed, MOD; 即=is/nothing but, equivalence〕

详情可参考文档：《轻松两步，教你快速识别百度蜘蛛》/ For details, you may refer to the document: «Two Easy Steps to Quickly Identify the Baidu Spider».
〔可=may, MOD; 详情=details, scope delimitation〕

Q3. Q：百度蜘蛛会一直抓我的网站吗？/ Q: Will the Baidu spider keep crawling my website forever?
〔会=will, future/habitual MOD; 一直=continuously/forever, durative SCO; 吗=question particle, interrogative〕

A：一般会的，若网站持续生产新资源、更新内容等，蜘蛛会持续抓取的。/ A: Generally yes — if a site keeps producing new resources and updating content, and so on, the spider will keep crawling it.
〔一般=generally, QUAL (NOT “always”); 会=will, habitual MOD (×2); 若=if, COND; 持续=continuously, durative QUAL (×2); 等=etc., open-list L-SCO〕

需要提醒的是，若网站需要百度蜘蛛抓取一定不要做任何封禁哦。（封禁相关参考下文内容）/ It should be noted that if you need the Baidu spider to crawl your site, you must not impose any blocking at all. (See below for blocking-related content.)
〔需要提醒=should be noted, recommendation framing; 若=if, COND; 需要=need, MOD; 一定不要=must not, strong prohibition MOD; 任何=any, total-universal SCO; 哦=sentence particle, informal assertiveness; 下文=below, referential SCO〕

此外，您也可以检查网站访问日志，及时判断正确的百度蜘蛛，以防止有人恶意冒充百度蜘蛛来频繁抓取您的网站。/ In addition, you can also check your site access logs to promptly identify the genuine Baidu spider, so as to prevent someone from maliciously impersonating the Baidu spider to crawl your site frequently.
〔此外=in addition, additive SCO; 也=also, additive SCO; 可以=can, MOD; 及时=promptly, QUAL; 正确=genuine/correct, QUAL; 防止=prevent, purpose; 恶意=maliciously, QUAL; 频繁=frequently, frequency QUAL〕

Q4. Q：百度蜘蛛频繁光顾网站，导致网站服务器压力大，怎么办？/ Q: The Baidu spider frequently visits my site, putting heavy pressure on the site server — what should I do?
〔频繁=frequently, frequency QUAL; 大=heavy, degree QUAL; 怎么办=what to do, question〕

A：若发现百度蜘蛛频繁抓取，可能是因为①网站存在新生产资源、更新内容待抓取更新；②可能存在恶意冒充百度蜘蛛，可以通过上文Q2"如何识别正常百度蜘蛛"的方法排查问题；/ A: If you find the Baidu spider crawling frequently, the cause may be ① the site has new resources or updated content awaiting crawl/refresh; or ② there may be a malicious impersonator of the Baidu spider — you can troubleshoot using the method in Q2 above, “how to identify a normal Baidu spider”;
〔若=if, COND; 可能=may, epistemic MOD (×2); 或=or, disjunctive SCO; 待=pending, aspect; 上文=above, referential SCO; 正常=normal, QUAL; 可以=can, MOD〕

若百度蜘蛛抓取频次过高，造成网站服务异常，可以通过搜索资源平台-【抓取频次】工具调整频次。/ If the Baidu spider's crawl frequency is too high and is causing abnormal service on your site, you can adjust the frequency via the Search Resource Platform's [Crawl Frequency] tool.
〔若=if, COND; 过高=too high, degree QUAL; 异常=abnormal, QUAL (NOT “blocked”); 可以=can, MOD; 工具=tool, instrument SCO〕

## REFERENCE S424:
Source: 开发者如何解除封禁百度蜘蛛 ("How Developers Unblock the Baidu Spider"), published 2020-07-23, page id=3028. Scope: whole article.

Title: How developers unblock the Baidu spider.

近期收到一些开发者反馈，为什么网站或智能小程序资源的内容非常优质，但是没有查询到百度蜘蛛抓取记录，或在百度搜索中没有得到收录和展现？/ Recently, we received feedback from some developers asking why the content of their websites or smart mini-programs is very good, yet no Baidu-spider crawl records can be found, or the content is not indexed or displayed in Baidu search.
〔近期=recently, temporal SCO; 一些=some, quantifier SCO; 或=or, alternation SCO; 非常=very, degree QUAL; 没有=not, NEG〕

在技术分析后发现，有些网站或智能小程序存在封禁百度蜘蛛的情况，导致百度蜘蛛无法正常抓取，所以无法在百度搜索中正常收录和展现，或在搜索结果中的摘要展现为"存在robots封禁"字样。/ After technical analysis, we found that some websites or smart mini-programs have the condition of blocking the Baidu spider, which causes the Baidu spider to be unable to crawl normally; therefore it is unable to be normally indexed and displayed in Baidu search, or the summary shown in search results reads “存在robots封禁” ("robots blocking exists").
〔有些=some, quantifier SCO; 存在=exists, factive; 导致=causes, causal; 无法=unable to, negated MOD (×2); 所以=therefore, inference; 正常=normally, QUAL (×2); 或=or, alternation SCO〕

为了让广大开发者的网站或小程序，在百度搜索中得到正常的收录和展现，建议开发者及时根据以下内容自查，解除封禁问题，并通过链接提交工具主动提交给我们。/ To let developers' websites or mini-programs get normally indexed and displayed in Baidu search, we recommend that developers promptly self-check against the following content, resolve the blocking problem, and proactively submit to us via the link-submission tool.
〔建议=recommend, recommendation MOD (NOT mandatory); 及时=promptly, QUAL; 以下=following, referential SCO; 主动=proactively, QUAL; 通过=via, instrument; 为了=in order to, purpose〕

常见的封禁行为包括robots封禁、封禁百度UA、封禁百度IP等。/ Common blocking behaviors include robots blocking, Baidu-UA blocking, and Baidu-IP blocking, among others.
〔常见=common, QUAL; 包括=include, non-exhaustive L-SCO; 等=etc., open-list L-SCO〕

如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？/ How do you verify whether a website or smart mini-program has the condition of blocking the Baidu spider?
〔如何=how, question; 是否=whether, yes/no SCO; 存在=exists, factive〕

1、首先，查看robots.txt文件，是否存在封禁记录。（一般robots.txt文件放置在网站根目录下。）/ 1. First, check the robots.txt file for whether blocking records exist. (Generally, the robots.txt file is placed in the site root directory.)
〔首先=first, ordering SCO; 是否=whether; 一般=generally, QUAL (NOT always)〕

【建议方案】解除robots封禁：robots封禁情况，请检查robots.txt文件，及时修改。robots文件说明：https://ziyuan.baidu.com/college/articleinfo?id=1516 / [Suggested approach] Removing robots blocking: for a robots-blocking situation, please check the robots.txt file and fix it promptly. robots file documentation: https://ziyuan.baidu.com/college/articleinfo?id=1516.
〔建议=suggested, recommendation MOD; 请=please, polite directive; 及时=promptly, QUAL〕

2、robots文件无异常，进一步排查是否存在封禁百度UA情况；/ 2. If the robots file has nothing abnormal, further check whether there is Baidu-UA blocking.
〔无异常=nothing abnormal, negated QUAL; 进一步=further, sequence SCO; 是否=whether〕

方案一：执行 curl --head --user-agent 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)' --request GET 'xxxxxxx' / Option 1: run `curl --head --user-agent '<Baiduspider UA>' --request GET 'xxxxxxx'`.
注：正常返回码是200，其他情况为异常。/ Note: a normal return code is 200; other cases are abnormal.
〔正常=normal, QUAL; 其他情况=other cases, residual SCO — “abnormal”, NOT “blocked”〕
xxxxxxx为网站域名,如：http://abc.com.cn。/ xxxxxxx is your website domain, e.g., http://abc.com.cn.
〔如=e.g., exemplification SCO; 为=is, copula〕

正确识别和获取百度蜘蛛，https://ziyuan.baidu.com/college/articleinfo?id=2855 / For correctly identifying and obtaining the Baidu spider, see https://ziyuan.baidu.com/college/articleinfo?id=2855.
〔正确=correctly, QUAL — note: this cross-reference is where IP-range details live; not on S423/S424〕

方案二：变更浏览器UA验证；/ Option 2: change the browser UA to verify.
〔变更=change, action SCO〕

【建议方案】解除百度UA封禁：查看网站反爬虫策略，进行策略调整。或针对百度UA添加策略白名单。/ [Suggested approach] Removing Baidu-UA blocking: review your site's anti-crawler policy and adjust the policy. Or add a policy whitelist for the Baidu UA.
〔建议=suggested, recommendation MOD; 或=or, alternation SCO; 针对=specifically for, target SCO〕

3、以上验证均无异常，最后进一步排查是否存在IP级别的封禁；/ 3. If all the above checks have nothing abnormal, finally check further whether there is IP-level blocking.
〔以上=above, referential SCO; 均=all, universal SCO; 无异常=nothing abnormal; 最后=finally, ordering SCO; 进一步=further; 是否=whether; 级别=level, scope-type〕

常见的IP封禁，源自网站的防火墙系统配置，需要查看防火墙配置系统后台，检查是否存在百度蜘蛛的IP级别封禁措施。/ Common IP blocking originates from the site's firewall system configuration; you need to look at the firewall configuration backend and check whether there are Baidu-spider IP-level blocking measures.
〔常见=common, QUAL; 源自=originates from, causal; 需要=need, MOD; 是否=whether〕

【建议方案】解除百度IP封禁：查看网站反爬虫策略，进行策略调整。/ [Suggested approach] Removing Baidu-IP blocking: review your site's anti-crawler policy and adjust the policy.
〔建议=suggested, recommendation MOD〕

## TRAPS:
The 10 most likely mistranslation/overreach traps for these entries:

1. 一般会的 → “generally yes” (habitual: it usually does, under the stated condition), NOT “always” / unconditional. The Q3 answer is conditional on 持续生产新资源、更新内容 (continuing to produce new resources/updated content).
2. 可以 → “can / may” (capability or permission), never “will / must”. E.g. 可以使用host ip命令 = “you can use the host ip command”, not “you must use”.
3. 会 (future/habitual marker) → translates as “will/keep …ing” as a predictive or habitual modal, not as a categorical promise; 百度蜘蛛会一直抓我的网站吗 is an open question, not an assertion.
4. 一定不要做任何封禁 → “must not impose any blocking” (strong prohibition; 任何 = any at all), NOT “you do not need to block” and NOT merely a weak “avoid blocking”.
5. 百度蜘蛛不是立即停止抓取网页 (in S423 封禁篇 Q1) → “the Baidu spider does not immediately stop crawling pages”: a gradual transition (robots updates take effect progressively — 搜索引擎需要逐渐完成更新), NOT “never stops” and NOT an instantaneous stop.
6. 正常返回码是200，其他情况为异常 → 200 is the normal code; every other case is “abnormal” (异常). Do NOT translate 异常 as “blocked” (封禁): a 403/500/redirect is abnormal but is not asserted to be a block, and a block is not asserted to be the only abnormal case.
7. IP-range (IP段) specifics are NOT on S423/S424: S424 only cross-references the page id=2855 (“正确识别和获取百度蜘蛛”) for how to identify/obtain Baiduspider. Do not claim these two pages publish Baidu IP ranges.
8. The identification test is a strict binary: hostname must be of the form *.baidu.com or *.baidu.jp, else “impostor” (冒充); and forward-DNS IP mismatch also = impostor. Keep the “if not … then impostor” equivalence; don't soften it to “probably fake”.
9. 目前UA分为移动、PC、小程序三个应用场景 ( “currently”, exactly three channels) — an exhaustive, time-scoped enumeration as of the 2022-08-19 publication. Do not expand it to future channels or claim UA examples are exhaustive within a channel (或 = alternatives are shown).
10. 建议/请 + “recommend/please” (polite directive), NOT a requirement or an obligation; e.g. 建议开发者及时…自查 = “we recommend developers self-check”, not “developers must self-check”. Also 需要 = “need” (instrumental necessity), not “must” in the sense of an external mandate.

VERDICT: Reference translations for S423 (抓取篇 Q1–Q4) and S424 (whole article) produced with qualifier/modal/scope marking; 10 traps listed — entries should be checked against these readings.
