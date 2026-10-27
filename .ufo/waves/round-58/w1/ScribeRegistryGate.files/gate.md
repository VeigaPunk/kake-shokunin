## Gate

Rows opened this round. Unit rule (the C3 counter's `units()`): one unit per CJK character, one per non-CJK whitespace token;
every quote below is at most 25 units and at most 40 characters. Both pages were opened 2026-10-26 UTC per
`sources/receipts.json` (HTTP 200, userAgent `kake-shokunin-round58`, fetchedAt 23:35:45Z and 23:35:46Z; the receipts carry no
effective-URL field), and the retained bodies sit under `.ufo/waves/round-58/sources/`; this seat re-hashed them and did not
re-fetch them. Each span below was cut and tested with
`python3 -B .ufo/waves/round-58/span_tools.py check <id> <span>` (units, chars, one text node of the article block, page-unique).

- S423 — https://ziyuan.baidu.com/college/articleinfo?id=3457 — accessed 2026-10-26 — § 2、Q：如何才能识别当前抓取是正确的百度蜘蛛？ (发布日期 2022-08-19) — quote: "A：有两个方式可以判断百度蜘蛛。" (13 units; raw substring of one text node of the retained body, sha256 8b8aef60bd7e315799e9a97dadfd02a5982f8c7e17b9d4064a6fc3913a0736ec, 29007 bytes, HTTP 200)
- S424 — https://ziyuan.baidu.com/college/articleinfo?id=3028 — accessed 2026-10-26 — § 常见的封禁行为包括robots封禁、封禁百度UA、封禁百度IP等。 (发布日期 2020-07-23) — quote: "如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？" (25 units; raw substring of one text node of the retained body, sha256 3ef1275b730230f2cb9c14b28b1c4bd08dc363dc7941b63d06c507fb2729cad1, 22476 bytes, HTTP 200)

Page-printed revision dates: S423 prints `发布日期：2022-08-19`, S424 prints `发布日期：2020-07-23`. Candidates considered, admitted,
rejected:

- Admitted, theme `Baidu crawler identification`. Staged `baidu-crawler-identification.md` (staged row S395) re-grounded as **S423**
  (renumbered by document, not arithmetically — the registry's next unused id after S422); **S424** lane-found from S423's own
  outbound link 《开发者如何解除封禁百度蜘蛛》 (`href="https://ziyuan.baidu.com/college/articleinfo?id=3028"`, one occurrence in
  the retained body). Both rows are new; both `mined`, opened 2026-10-26, recheck `180d`. The entries
  `corpus/knowledge/baidu-spider-identification.md` (S423) and `corpus/knowledge/baidu-spider-unblocking.md` (S424) belong to the
  entry scribes; the staged file name is not carried, and the staged rows are not appended as staged.
- Staged S395 sentences refused, each read against the retained S423 body before it was logged (counts are `str.count` on the
  retained bytes):
  - "Baiduspider-render/2.0 … fetches a page's CSS, JavaScript and images" — `渲染` 0, `CSS` 0, `JavaScript` 0, `图片` 0; the page lists UA strings and says nothing about what the render agent fetches.
  - "the same agent the platform's 2017 announcement introduced" — `2017` has 0 occurrences; that announcement is already held as S390 and a row must not attribute across documents.
  - "A publisher blocking by user agent must allow both" — the page says `百度蜘蛛遵守互联网robots协议` and shows the UA self-check under `Baiduspider/2.0` only; no sentence states a must, so the modal is refused.
  - "It has a section on crawling and a section on crawl frequency" — the page's two section headings are `【抓取篇】` and `【封禁篇】`; crawl frequency is question 4 inside `【抓取篇】`, not a section.
  - "with two methods: … and a DNS reverse lookup" — the second method is `方式二：双向DNS解析认证`, reverse lookup then forward lookup (`第二步：对域名运行正向` + `DNS` + `查找。`); the one-step framing under-reads the page.
  - "`Baiduspider/2.0` is the ordinary crawler" — the page defines Baiduspider as `百度搜索引擎的一个自动程序` and never ranks the two agents; the gloss is an inference and is dropped.
  - the staged anchor `§ 【抓取篇】→「第一步：DNS反查IP」段末句` — `【抓取篇】` is 3 units and the arrow locator matches no text node; rebuilt as the page-unique h3 above.
  - the staged "no revision stamp" clause — false, the page prints `发布日期：2022-08-19`; the rebuilt anchor carries it.
  - the staged entry's lane-history opening and its Yahoo-unreadability paragraph — meta prose, not a page statement (the Yahoo side is the round-56 S388 refusal).
  - the one staged sentence kept, as a bounded negative: the page does not say whether the render agent executes what it fetches — `执行` occurs once, inside `方案一：执行` (the curl instruction), never of the render agent; an entry may state that check, not the absence alone.
- Decision lines (one per refused source row, read by the Gate-reject check):
  - S378 — REJECT as staged (`yahoo-japan-crawler-address-change-notice.md`, https://ads-developers.yahoo.co.jp/ja/ads-api/announcement/260514.html, re-opened 2026-10-26 by curl, HTTP 200, 19226 bytes, sha256 5cbac62802e149c8cdf2ccdcaafb8b16cfecad08394c37535a8ce06d9eda67b1, effective URL equal to the request URL): the notice's subject is the Display Ads (運用型) product-list crawler — page sentence `動的ディスプレイ広告の商品リストにおいて、定期更新（FTPによる定期巡回）でファイルを取得するクローラーのIPアドレスを追加しました。` — and the consequence it states for a stale allow-list is `動的ディスプレイ広告の配信が停止します`, i.e. ad delivery stops, not crawling or indexing; the notice names no search crawler, sits in an ads API developer center, and `PROVINCE.md` lines 3–6 put this lane on web properties and publishing, not on ad-platform delivery infrastructure. The staged entry also overcounts: its 更新履歴 holds four dated entries (2026年5月14日, 2026年7月6日, 2026年7月9日, 2026年9月2日; `grep -c` over the two 更新 phrases = 4), not five. Flip: the operator publishes the same address change for its search crawler (the notice's subject becomes 検索 rather than the product-list fetcher), or the operator rules ad-delivery crawler addresses into kake's province and the lane gains an ads service property.

## Registry changes (old → new)

- Rows: 160 → 162. S423 and S424 are appended after S422 in that order, both `mined`, opened 2026-10-26, recheck `180d`,
  `used-by` = their single entry. No existing row's `status`, `recheck` or `used-by` changed this round (a pure addition).
- Counts: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` = 160 at the base revision and in the
  pre-append mirror (`assimilation/mirror-pin.json`: 160 rows, sha256 57c83362…, 149028 bytes); the two ids are absent from the
  base (`grep -cE '^\|[[:space:]]*S42[34][[:space:]]*\|'` = 0).
- Draft-row census (run by this seat on a scratch copy `sources-copy.md` = the lane registry plus the two draft rows, with the
  frozen CORPUS.md awk formulas): rows 162, malformed rows (NF!=13) 0, duplicate ids none, tier/kind/status enum violations none,
  status histogram `mined=132 queued=8 rejected=22`. The `used-by` existence check prints the two entry paths as missing at the
  base revision — expected, the entries land with the entry scribes.

## Assimilation

Theme: `Baidu crawler identification` from `merge/kake/` (shokuknow, read-only). Id lists (`assimilation/`): registry `reg-ids` 160,
staged `staged-ids` 129 (`wc -l`), `collisions` 8 (S312 S329 S367 S372 S373 S374 S390 S409 — the same documents round 57 found);
neither S395 nor S378 collides. Renumber map by document: staged S395 → S423; S424 has no staged id (lane-found from S423); staged
S378 → none (rejected, no row). Quarantine slice (12 rows: S142 S143 S148 S154 S156 S161 S178 S184 S193 S194 S195 S206): none is
S395 or S378, none is adopted this round, and none was re-checked by this seat. The staged `.append` rows S395 and S378 are not
appended as staged — S395 is rebuilt from the retained page, S378 is refused above.
