# ScribeRegistryGate

Claim C3 / frontier step. Drafted the two registry rows (S423, S424) and the round-58 Gate block independently of the entry
scribes. Paste-ready block also at `.ufo/waves/round-58/w1/ScribeRegistryGate.files/gate.md`; the rejected page's fetched body is
retained at `.ufo/waves/round-58/w1/ScribeRegistryGate.files/yahoo-260514.html`. Nothing else in the lane was written; no git/jj
mutation; all work in `/fast/scratch/hyaku/kake-r58/ScribeRegistryGate/` (deleted at the end).

Inputs read: `CORPUS.md` § SOURCES.md (11-column table, status vocabulary, recheck forms), `corpus/SOURCES.md` rows S421/S422 as
the model and the row census, `corpus/lessons/round-57.md` § Gate / § Assimilation, round-58 `contract.md`, `assimilation/`
(reg-ids, staged-ids, collisions, quarantine-slice, mirror-pin.json), `sources/receipts.json`, `sources/S423.html`,
`sources/S424.html`, `span_tools.py`, `c58_quote_truth.py` (C3/C5 code), `SOURCES.append.md` rows S395 and S378,
`merge/kake/knowledge/corpus/knowledge/{baidu-crawler-identification,yahoo-japan-crawler-address-change-notice}.md`,
`PROVINCE.md` lines 3–6.

ROWS: (append after S422; no pipe inside any cell; both new, `mined`, opened 2026-10-26, recheck `180d`)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S423 | 百度搜索资源平台 — 搜索问答剧场 【五】“百度蜘蛛”全面解析 — https://ziyuan.baidu.com/college/articleinfo?id=3457 | docs | A | **The operator's own crawler inventory and its two-step identification procedure** — the agent names it publishes per channel (mobile, PC, mini-program) and the user-agent plus two-way DNS test that separates a real Baiduspider from an impostor | § 2、Q：如何才能识别当前抓取是正确的百度蜘蛛？ (发布日期 2022-08-19) | Telling a genuine Baiduspider from an impostor is done two ways: the request user agent, where the page lists the mobile, PC and mini-program strings for Baiduspider/2.0 and Baiduspider-render/2.0, and a two-way DNS check whose hostname must be under *.baidu.com or *.baidu.jp — anything else is an impersonation | mined | 2026-10-26 | 180d | corpus/knowledge/baidu-spider-identification.md |
| S424 | 百度搜索资源平台 — 开发者如何解除封禁百度蜘蛛 — https://ziyuan.baidu.com/college/articleinfo?id=3028 | docs | A | **The operator's unblocking checklist for its own crawler** — the three block kinds it names (robots, its user agent, its IP ranges), the order it checks them in, and the request whose status code tells a publisher whether the block is still there | § 常见的封禁行为包括robots封禁、封禁百度UA、封禁百度IP等。 (发布日期 2020-07-23) | The page names three common blocks on Baiduspider — robots, its user agent and its addresses — and walks them in that order: read robots.txt, then request the site under the Baiduspider user agent where a 200 is normal and anything else abnormal, then the firewall for address-level blocks, lifting each block found | mined | 2026-10-26 | 180d | corpus/knowledge/baidu-spider-unblocking.md |

GATE:

Rows opened this round. Unit rule (the C3 counter's `units()`): one unit per CJK character, one per non-CJK whitespace token; every
quote below is at most 25 units and at most 40 characters. Both pages were opened 2026-10-26 UTC per `sources/receipts.json` (HTTP
200, userAgent `kake-shokunin-round58`); this seat re-hashed the retained bodies and did not re-fetch them. Each span was tested with
`python3 -B .ufo/waves/round-58/span_tools.py check <id> <span>`.

- S423 — https://ziyuan.baidu.com/college/articleinfo?id=3457 — accessed 2026-10-26 — § 2、Q：如何才能识别当前抓取是正确的百度蜘蛛？ (发布日期 2022-08-19) — quote: "A：有两个方式可以判断百度蜘蛛。" (13 units; raw substring of one text node of the retained body, sha256 8b8aef60bd7e315799e9a97dadfd02a5982f8c7e17b9d4064a6fc3913a0736ec, 29007 bytes, HTTP 200)
- S424 — https://ziyuan.baidu.com/college/articleinfo?id=3028 — accessed 2026-10-26 — § 常见的封禁行为包括robots封禁、封禁百度UA、封禁百度IP等。 (发布日期 2020-07-23) — quote: "如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？" (25 units; raw substring of one text node of the retained body, sha256 3ef1275b730230f2cb9c14b28b1c4bd08dc363dc7941b63d06c507fb2729cad1, 22476 bytes, HTTP 200)

Page-printed revision dates: S423 `发布日期：2022-08-19`, S424 `发布日期：2020-07-23`.

- Admitted, theme `Baidu crawler identification`: staged `baidu-crawler-identification.md` (staged row S395) re-grounded as **S423**
  (renumbered by document; the registry's next unused id after S422); **S424** lane-found from S423's own outbound link
  《开发者如何解除封禁百度蜘蛛》 (`href="https://ziyuan.baidu.com/college/articleinfo?id=3028"`, one occurrence). Entries
  `corpus/knowledge/baidu-spider-identification.md` / `baidu-spider-unblocking.md` belong to the entry scribes; the staged file name
  is not carried and the staged rows are not appended as staged.
- Staged S395 sentences refused, each read against the retained S423 body (`str.count` on the retained bytes) before logging:
  - "Baiduspider-render/2.0 … fetches a page's CSS, JavaScript and images" — `渲染` 0, `CSS` 0, `JavaScript` 0, `图片` 0; the page lists UA strings only.
  - "the same agent the platform's 2017 announcement introduced" — `2017` 0 occurrences; that announcement is held as S390, and a row must not attribute across documents.
  - "A publisher blocking by user agent must allow both" — the page says `百度蜘蛛遵守互联网robots协议` and shows the UA self-check under `Baiduspider/2.0` only; no sentence states a must, so the modal is refused.
  - "It has a section on crawling and a section on crawl frequency" — the two section headings are `【抓取篇】` and `【封禁篇】`; crawl frequency is question 4 inside `【抓取篇】`, not a section.
  - "with two methods: … and a DNS reverse lookup" — the second method is `方式二：双向DNS解析认证`, reverse then forward lookup (`第二步：对域名运行正向` / `DNS` / `查找。`); the one-step framing under-reads the page.
  - "`Baiduspider/2.0` is the ordinary crawler" — the page defines Baiduspider as `百度搜索引擎的一个自动程序` and never ranks the two agents; the gloss is an inference and is dropped.
  - the staged anchor `§ 【抓取篇】→「第一步：DNS反查IP」段末句` — `【抓取篇】` is 3 units and the arrow locator matches no text node; rebuilt as the page-unique h3 used above.
  - the staged "no revision stamp" clause — false: the page prints `发布日期：2022-08-19`; the rebuilt anchor carries it.
  - the staged entry's lane-history opening and its Yahoo-unreadability paragraph — meta prose, not a page statement (the Yahoo side is the round-56 S388 refusal).
  - the one staged sentence kept, as a bounded negative: the page does not say whether the render agent executes what it fetches — `执行` occurs once, inside `方案一：执行` (the curl instruction); an entry may state that check, not the absence alone.
- Decision lines (one per refused source row):
  - S378 — REJECT as staged (`yahoo-japan-crawler-address-change-notice.md`, https://ads-developers.yahoo.co.jp/ja/ads-api/announcement/260514.html, re-opened 2026-10-26 by curl, HTTP 200, 19226 bytes, sha256 5cbac62802e149c8cdf2ccdcaafb8b16cfecad08394c37535a8ce06d9eda67b1, effective URL = request URL): the notice's subject is the Display Ads (運用型) product-list crawler — page sentence `動的ディスプレイ広告の商品リストにおいて、定期更新（FTPによる定期巡回）でファイルを取得するクローラーのIPアドレスを追加しました。` — and the consequence it states for a stale allow-list is `動的ディスプレイ広告の配信が停止します`, i.e. ad delivery stops, not crawling or indexing; no search crawler is named, the page sits in an ads API developer center, and `PROVINCE.md` lines 3–6 put this lane on web properties and publishing, not on ad-platform delivery infrastructure. The staged entry also overcounts: its 更新履歴 holds four dated entries (2026年5月14日, 2026年7月6日, 2026年7月9日, 2026年9月2日), not five. Flip: the operator publishes the same address change for its search crawler (the notice's subject becomes 検索 rather than the product-list fetcher), or the operator rules ad-delivery crawler addresses into kake's province and the lane gains an ads service property.

ASSIMILATION:

Id lists (`assimilation/`, `wc -l`): registry `reg-ids` 160, staged `staged-ids` 129, `collisions` 8 (S312 S329 S367 S372 S373 S374
S390 S409 — the same documents round 57 found); neither S395 nor S378 collides. Renumber map by document: staged S395 → S423; S424 has
no staged id (lane-found from S423); staged S378 → none (rejected, no row). Quarantine slice: 12 rows (S142 S143 S148 S154 S156 S161
S178 S184 S193 S194 S195 S206), none is S395 or S378, none adopted this round, none re-checked by this seat. Staged `.append` rows S395
and S378 are not appended as staged — S395 is rebuilt from the retained page, S378 is refused above.

REGISTRY CHANGES:

- Rows 160 → 162: S423, S424 appended in that order after S422, both `mined`, opened 2026-10-26, recheck `180d`, `used-by` = their
  single entry. No existing row's `status`, `recheck` or `used-by` changes this round (a pure addition).
- Base counts: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` = 160 (lane tree and
  `assimilation/pre-append/corpus/SOURCES.md`, pinned 149028 bytes / sha256 57c83362… by `mirror-pin.json`); the two ids are absent
  from the base (`grep -cE '^\|[[:space:]]*S42[34][[:space:]]*\|'` = 0).
- Draft-row census on a scratch copy (lane registry + the two draft rows, frozen CORPUS.md awk formulas): rows 162, malformed (NF!=13)
  0, duplicate ids none, tier/kind/status enum violations none, status histogram `mined=132 queued=8 rejected=22`. The mined `used-by`
  existence check prints the two entry paths as missing at the base revision — expected until the entry scribes land them.

Checks run (all by this seat, this round):

- `span_tools.py check` on both Gate quotes: S423 13 units / 16 chars / in one text node / body count 1 / page-unique; S424 25 units /
  26 chars / one text node / count 1 / page-unique.
- `sha256sum` + `wc -c` on both retained bodies: 8b8aef60… 29007 bytes and 3ef1275b… 22476 bytes, equal to `sources/receipts.json`.
- `str.count` on the retained bodies for every refused-sentence term above and for both anchor candidates (each 1, so page-unique).
- Title/anchor/date pre-flight against the counter's C5 code: row titles equal each page's `<title>` text before `_`
  (`搜索问答剧场 【五】“百度蜘蛛”全面解析`, `开发者如何解除封禁百度蜘蛛`); both anchors 4+ units, page-unique, inside a text node;
  both printed dates present.
- Full pre-flight of the draft rows and both Gate lines against the counter's own code (`preflight.py`, retained at
  `w1/ScribeRegistryGate.files/preflight.py`; imports `c58_quote_truth.py` and calls its `parse_registry`, `units`, `in_content`,
  `gate_line`, `CURLY`, `ROW_URL`, `BODY_SHA256`): the ROWS table above parses to ids S423 and S424 with **0 notes** — 11 cells,
  status/opened/recheck/kind/tier, row URL, title against `<title>`, anchor form/units/page-uniqueness/text-node, printed date,
  retained-body digest equal to the frozen one, and per Gate line: digest, `NNNNN bytes`, `NN units` labels, the row's anchor cell,
  the URL, the round date, no curly quotes, every quoted span ≤25 units and ≤40 characters, a substring of one article text node,
  page-unique against both bodies, at least one span carrying 百度蜘蛛. Not exercised by that pre-flight: the base-revision row
  comparison (C3 base branch) and the entry-side conditions C1, C2, C4, C6, C7, C8.
- Yahoo re-open: `curl -sS -L` → HTTP 200, 19226 bytes, sha256 5cbac628…, effective URL = request URL; the 更新履歴 entry count = 4.
- Census on the scratch copy (above); `wc -l` on the four id lists.

Findings and limits:

- The staged S395 row's `teaches` is re-grounded, not copied: two of its clauses are false or absent from the page (CSS/JS/images
  function of the render agent; the 2017 attribution) and one is false about the page itself ("no revision stamp").
- Anchor choices deviate from the staged locator on purpose: `【抓取篇】` is 3 units, so S423's anchor is the page-unique h3; S424 has
  no sub-headings, so its anchor is the page-unique sentence that names the three block kinds, and its Gate quote is the
  page-unique question that opens the self-check (the only page-unique S424 span carrying 百度蜘蛛).
- [INFERENCE] The S424 anchor is a body sentence rather than a heading; the counter accepts it (4+ units, page-unique, in a text
  node), but a reviewer may prefer the title line, which is not page-unique in the retained bytes.
- Not run by this seat, therefore unverified here: the lane's `c58_quote_truth.py` C1–C8 (needs the two entries and the appended
  registry), the census validator `scripts/sources-census.sh`, and any non-author spot-check.
- `PROVINCE.md` lines 3–6 were read for the S378 refusal; no PROVINCE edit was made (out of seat and append-only by another hand).
- Lead, not evidence: S423 links 《轻松两步，教你快速识别百度蜘蛛》 (`articleinfo?id=2855`) and four 搜索问答剧场 back issues
  (3386, 3389, 3426); none was opened this round.
- Tooling: no install or upgrade was needed; no pacman transaction was run.

VERDICT: Rows S423 (staged S395 re-grounded) and S424 (lane-found) drafted and Gate-grounded with page-unique ≤25-unit quotes; staged S378 refused as an ad-delivery product-list FTP crawler outside the lane's province; registry 160 → 162, census clean on the draft.
