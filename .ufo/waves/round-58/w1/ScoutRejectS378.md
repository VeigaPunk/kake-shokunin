# ScoutRejectS378

Method: one curl GET of the page at 2026-10-26 (body kept only in scratch, now deleted); staged entry, row S378 and PROVINCE.md read from disk. No span_tools run (it only serves S423/S424); unit counts below are by hand and marked approximate.

PAGE:
- HTTP 200, text/html; charset=UTF-8, 19226 bytes, redirects followed with -L (final URL not recorded; `%{url_effective}` was not requested). [observed]
- Title: 【ディスプレイ広告（運用型）】商品リスト定期更新クローラーのIPアドレス追加について │ LINEヤフー広告 API │ Developer Center - LINEヤフー広告. Host is the LINEヤフー広告 API Developer Center (LY Corporation), not the Yahoo!検索 インフォセンター (info-search.yahoo.co.jp).
- Date shown: 2026/09/02 (last update). The history has FOUR `<li>` items: 2026年9月2日, 2026年7月9日, 2026年7月6日, 2026年5月14日 (掲載開始).
- 対象サービス: LINEヤフー広告 ディスプレイ広告（運用型）. 実施日: new-IP crawling from 2026年7月8日, old-IP crawling stopped from 2026年9月1日 (the page's own history shows 7/6 "開始日変更" and 7/9 "開始" updates).
- Answer to the question: the page is about the Display Ads product-list FTP fetcher, not a search crawler. The words "検索" and "search" appear only in a navigation link (検索広告 APIリファレンス), never in the article body. The notice is also not about a crawler fetching a publisher's web host: the crawler fetches an advertiser's product-list file by FTP for dynamic display ads. [observed]

STAGED CLAIMS: (entry file yahoo-japan-crawler-address-change-notice.md; row S378 in SOURCES.append.md line 98)
- L5 `ground: per-host crawl hygiene — how the operator publishes changes to its crawler addresses`: UNSUPPORTED. The page covers one crawler of one ads product; "the operator ... its crawler addresses" is a generalisation. "Per-host crawl hygiene" does not fit an FTP feed fetch.
- L9-10 "The operator does not publish a standing list of the addresses its crawlers come from. It publishes changes, as dated notices": UNSUPPORTED. This is an absence claim about every crawler of the operator, taken from a single page. The page says nothing about other crawlers or lists.
- L13 quote `2026年9月2日：旧IPアドレスからの巡回を停止し、記事を更新しました`: SUPPORTED as a raw substring (count 1 in the body; 36 characters). It is the 更新履歴 line of the product-list crawler notice, not evidence of the operator's practice in general.
- L15 "The history holds five entries": UNSUPPORTED. The page has four. "start date was changed 7/6", "start recorded 7/9", "stop recorded 9/2": supported.
- L17-20 new ranges 7/8, old range stopped from 9/1, overlap window, old range droppable afterwards, table with one old range (203.216.252.128/26) and three new addresses: SUPPORTED, for the product-list crawler.
- L22-23 "the operator's address is not a constant: the same crawler's range has moved before": UNSUPPORTED. The page records one move (old to new). The earlier history entries move dates, not ranges.
- L24-27 "An allow-list that pins an address is pinned to a date", and a publisher whose allow-list holds only the old range loses delivery: PARTLY. The page says an advertiser whose whitelist holds only the old IPs loses 動的ディスプレイ広告 delivery (旧IPアドレスのみを登録している場合、動的ディスプレイ広告の配信が停止します). The staged text recasts this as "a publisher", which is a different party. Lines 24-26 are the entry's own inference.
- L30-31 scope note "concerns the advertising service's product-list fetcher, not the search crawler ... not a current list of every address the operator uses": SUPPORTED, and it contradicts L5, L9, L22 and the title "Crawler addresses are published as dated changes, not as a list". The body generalises and the scope note retracts it; this is a self-inconsistent entry.
- Row S378: bold gloss "How the operator publishes changes to its crawler addresses" and body "the operator adds and retires crawler address ranges by notice rather than by list": same generalisation; the row never says "ads / FTP / product list" outside the page title. The row's recheck command (grep -c = 1) proves the string exists, not that the generalisation holds.
- The page's retained facts are not wrong; the unsupported items are the generalisations (L5, L9-10, L15, L22-23, row gloss).

PROVINCE: (/home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md)
- L3 domain: "web properties & publishing — scopes ds4cc.com, kimi.page/pro mirrors, Pages deploys". L6 "Refuses: anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it."
- L22-23 Frontier: "Crawl hygiene per host (robots.txt, sitemap scope, canonical signals)". L34-36 Adjacent: kake owns "publisher-side placement (robots/sitemap at the host it serves)"; client-side crawler discipline belongs to tabi.
- L398-399 (Round-55): "Yahoo! JAPAN crawler-address, user-agent-list and deleted-URL pages in the staging package are not adopted this round." This is round-55 history, dated; deleted-URL was adopted in round 56 (S419). The crawler-address page has not been adopted in any section I read (the Round-56 and Round-57 sections listed above only name robots/link-target/deleted/nonexistent-URL entries).
- The product-list FTP fetcher is advertiser-feed operations for a paid ads product. It is not publisher-side placement at a host the lane serves, so it is outside L22-23/L34-36 and falls under the L6 refusal.

REJECT REASON:
- The adoption rests on the staged entry being a claim about "the operator" and "its crawlers". The page is only about 商品リスト定期更新クローラー, a Display Ads FTP fetcher.
- Page sentence 1 (概要, one text node; located by the raw-HTML `<p>` after `<h3>概要`): "定期更新（FTPによる定期巡回）でファイルを取得するクローラー". By hand: 31 characters, units about 25 with FTP counted as one token; this is over or at the 25-unit limit, so use the shorter pair below for quoting.
- Shorter, safe quotes: "定期更新（FTPによる定期巡回）" (16 characters, count 1, in the 概要 `<p>`); "商品リスト定期更新クローラー" (14 characters, in the `<h2>` title and also the page `<title>`, so it is not unique in the body; count 3 in text).
- Page sentence 2 (対象サービス, `<p>` after `<h3>対象サービス`): "LINEヤフー広告 ディスプレイ広告（運用型）" is 23 characters; unit counting of the mixed LINEヤフー広告 token is ambiguous, so alternatively "動的ディスプレイ広告の商品リスト" (16 characters, start of the 概要 `<p>`).
- The page has no search crawler, no robots.txt, no user-agent, no per-host statement. L5/L9/L22 generalise a one-product notice to the whole operator; L15 miscounts history (5 vs 4); L22-23 "moved before" is not on the page. The entry's own scope note (L30-31) concedes the page is not the search crawler, so the entry as titled cannot stand, and the PROVINCE L6 refusal plus the L398-399 round-55 non-adoption apply.
- Citation note: the title/row say Yahoo! JAPAN's crawler; the page is LINEヤフー広告 API Developer Center. [INFERENCE] the lane's other yahoo-japan-* entries all cite info-search.yahoo.co.jp search-crawler pages, so this one is the only entry from the ads-API host.

FLIP:
Adopt S378 only if all hold:
1. Retitle and rescope to the product-list FTP crawler of LINEヤフー広告 Display Ads, with "the operator" and "its crawlers" replaced by that crawler, and the row gloss reworded likewise.
2. Fix the history count to four, and drop "moved before" and "does not publish a standing list".
3. PROVINCE or the orchestrator records why advertiser-feed crawler addresses are inside the web-publishing domain, for example a lane property that submits a product feed to this service. [INFERENCE] no such property is recorded in the PROVINCE sections read.
Alternatively, adopt it as a single non-generalised scope-bounded row with "not search crawler" in the title. Without (3) the default is REJECT per L6.

VERDICT: REJECT S378 as staged — the page is the Display Ads product-list FTP crawler notice (HTTP 200), the entry generalises it to "the operator/its crawlers", miscounts history (5 vs 4) and falls outside the PROVINCE publisher-side crawl domain (L6, L22-23, L398-399); flips only on rescoping to that one crawler plus a recorded domain reason.
