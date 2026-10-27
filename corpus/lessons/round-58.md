# Round 58 — lessons (kake)

Round date 2026-10-26. Base `044048597d62f3199494b63b36e90dd57825e350`; contract `.ufo/waves/round-58/contract.md` (version 1 frozen at `fff3eea6`,
version 2 at `1c0aa211` after wave 1, before any claim was measured). One v2 wave of 68 seats (`.ufo/waves/round-58/w1/`).

## Gate

Rows opened this round. Unit rule (the C3 counter's `units()`): one unit per CJK character, one per non-CJK whitespace token;
every quote below is at most 25 units and at most 40 characters. Both pages were opened 2026-10-26 UTC by
`.ufo/waves/round-58/fetch_sources.py` (GET, HTTP 200, userAgent `kake-shokunin-round58`) and retained under
`.ufo/waves/round-58/sources/` with sha256 receipts; a later live re-open (`w1/ExecSourceLive.md`, `w1/ProbeBodyStability.md`) found
the article text nodes byte-identical, only cache-buster tokens outside the article differing.

- S423 — https://ziyuan.baidu.com/college/articleinfo?id=3457 — accessed 2026-10-26 — § 2、Q：如何才能识别当前抓取是正确的百度蜘蛛？ (发布日期 2022-08-19) — quote: "A：有两个方式可以判断百度蜘蛛。" (13 units; raw substring of the retained body, sha256 8b8aef60bd7e315799e9a97dadfd02a5982f8c7e17b9d4064a6fc3913a0736ec, 29007 bytes, HTTP 200)
- S424 — https://ziyuan.baidu.com/college/articleinfo?id=3028 — accessed 2026-10-26 — § 如何验证网站和智能小程序是否存在封禁百度蜘蛛的情况？ (发布日期 2020-07-23) — quote: "导致百度蜘蛛无法正常抓取" (12 units; raw substring of the retained body, sha256 3ef1275b730230f2cb9c14b28b1c4bd08dc363dc7941b63d06c507fb2729cad1, 22476 bytes, HTTP 200)

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

Reject reasons were re-read against their pages before they were logged (QUALITY round-57 criterion 2): S378 by `w1/ScoutRejectS378.md`
and `w1/ScribeRegistryGate.md` (two independent curl re-opens), the staged S395 sentences by `w1/ScoutStagedS395.md`,
`w1/ScribeRegistryGate.md` and `w1/CriticEntryOverreach.md`.

Also opened this round, no row: https://ziyuan.baidu.com/college/articleinfo?id=2855 (the identification article S423 links;
`w1/ExecSourceLive.md`): it adds that the operator does not publish Baiduspider IP ranges (`IP地址范围动态变化不固定，我们无法对外公布`); no admitted
entry rests on it, so no row is written (CORPUS rule 4). Flip: an entry that states the no-published-ranges fact.

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

Guard: the collision extractor uses the 0–3-space pattern proven in round 57 (`.ufo/waves/round-57/assimilation/guard-proof/`); the
lists are `.ufo/waves/round-58/assimilation/reg-ids` (160), `staged-ids` (129), `collisions` (8). Scratch validation before the
append: `.ufo/waves/round-58/validate_append.sh` (receipts under `.ufo/waves/round-58/assimilation/validate/`).

## Search log (rule 5)

Round 58, Baidu crawler identification (assimilation theme from `merge/kake/`). Question: how does Baidu's own operator tell a
publisher to recognise a genuine Baiduspider request, and what does it say about a site that blocks it? Where: the staged package
(staged entry `baidu-crawler-identification.md`, row S395; staged `yahoo-japan-crawler-address-change-notice.md`, row S378, screened
as the other crawler-identity candidate), then the pages opened directly (articleinfo id=3457; its outbound links id=3028 and
id=2855). Included 2 (S423 from staged S395 by document; S424 lane-found); excluded staged S378 (reason in § Gate) and id=2855
(no entry rests on it). Stop rationale: one theme per round, two entries.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| landing | `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` landed at `31b61a4` as three lines — `pending`, `  revision: 32754df75774dd38e8a96fcda375fc93adf97f1e`, `EXIT=0` — and was filled at `20217f2` (blob `417ca0c615ba -> b514c80d7f36` at `20217f23eca1`; `git log -- .ufo/waves/round-57/controls/after-c1-receipt-pins.txt` lists exactly those two commits), while the round-57 report said no receipt carrying a `revision:` line was rewritten. This is the shape C1 exists to forbid: a pre-written receipt with a pin and an exit code. The report half is quoted through `corpus/lessons/round-57-verifier-spotcheck.md` §5 D1 only — `.ufo/reports/round-57/kake.md` and its commit `bdfe1efd6ceecc8632508c47e8be2630e7289bd4` do not resolve in this repo (`git cat-file -t` → bad object; `git ls-tree -r 20217f23 -- .ufo/reports` → `round-20` alone). | `c57_receipt_pins.py` missed it by construction: it watched `revision:` lines, and the fill kept the same pin (`32754df7…` in both blobs), so no relabel was visible; QUALITY round-57 criterion 1 stated the rule but its counter could not see a fill. | C1 counter `.ufo/waves/round-58/c58_receipt_rewrites.py` — predicate carries `new_rewritten == 0`, the ledger vocabulary has a `pending-fill` kind (version 2 name), and the contract's receipt rule forbids a placeholder (committed once after the run; a re-run lands under a new name). Shown able to fail: `controls/base-c1-receipt-rewrites.txt` prints `undisclosed=19 … met=False`, `EXIT=1`, and its last event is this file (`UNDISCLOSED M … after-c1-receipt-pins.txt at 20217f23eca1 417ca0c615ba -> b514c80d7f36`). |
| landing | Post-commit edits to measurement receipts in rounds 52–56 disclosed nowhere: round-52 ×4 (`control/c1-mutation-ladder.json` three times, `old_tail` revision strings, at `1ae8de5d4dee`/`a4a890cf1381`/`fd91527a2860`; `control/c2-quote-selftest.txt` fixture revision `3a50ae4321e6` → `1ae8de5d4dee`), round-54 ×5 (`controls/c1-selftest.txt` +2 checks at `8e408e00fbe1` and again at `a631cc0246b9`; `controls/base-c1-s374.txt` PASS/FAIL lines at `a0a4fd482700`; `controls/base-c2-ops-debt.txt` `uncovered=4` → `uncovered=7` at `a0a4fd482700`; `controls/sources-census.txt` measured-tip note at `5826682b3781`), round-55 ×2 (`controls/c1-selftest-v2.txt` `32/32` → `44/44` at `64c0ce12ffe3`; `controls/c2-selftest.txt` fixture revision at `955e3d7bd6d1`), round-56 ×1 (`controls/c2-selftest.txt` `67/67` → `86/86` at `ad06cb8a17bd`). Counter kinds over the 13 undisclosed events (version-1 names; version 2 reclassifies two, `contract.md` § Counter versions): 6 `relabel`, 6 `rerun`, 1 `fill`. Derived from `controls/base-c1-receipt-rewrites.txt`: `events=19` − 6 disclosed by `receipt-errata.json` (all `relabel`) − 1 round-57 fill (row above) = 12 here. Harm: the two round-54 base controls had their *before* values rewritten, so no reader can tell what the round-54 counter measured. | none: the round-57 counter's population was revision lines only, and the round-57 landing table listed neither the `rerun` edits nor the rewritten base controls; the round-57 spot-check §2 C1 re-derived the 6 relabels only. | C1 ledger `.ufo/waves/round-58/receipt-rewrites.json`: one entry per event with path, commit, status, from/to blob ids, the counter's kind and a note whose pointer resolves at the tip. History is not rewritten — the receipts stay as committed, the disclosure is additive. Shown able to fail: base control prints the 19 events and `undisclosed=19` while the ledger is absent (`ledger: … absent (0 entries)`). |
| stale-premise | `c56_quote_truth.py` measured 2026-10-26: `8/8 met=True` exit 0 at its measured revision `4cb225fb032b04166fb0232bc98a7bcce72675ec`, and `6/8 met=False` exit 1 at the round-57 tip `20217f23eca1` and at the round-58 base `044048597d62f3199494b63b36e90dd57825e350` (`C8_mirror_bytes FAIL`, `registry rows 160 != mirror rows 156 + 2`). Its mirror is pinned to the 158-row registry, so the red is by design and the SKILL.md row `yahoo-crawl-handling-quote-truth-counter` (§Round 56 gate registry additions) advertises `0=met` for any `<commit>` that no later tree can reach; round-57 spot-check D3 carried the same item. | none: the round-56 criterion "a selftest that rebuilds from `HEAD` names its fixture revision in its row" covered selftests; nothing required a gate whose population moves to name its measured revision or leave the live set. | Register the row as historical, pinned: Name → `yahoo-crawl-handling-quote-truth-counter (historical, measured at 4cb225fb032b)`; Kind → `gate (historical — green only at its measured revision; a later tree fails C8 by design)`; Pinned values gains the pinned entry command `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision 4cb225fb032b04166fb0232bc98a7bcce72675ec` → `8/8` and the divergence `registry rows 160 != mirror rows 156 + 2`. No round-58 claim rests on it (C1/C2/C3 are the round-58 counters). Shown able to fail: the pinned form exits 0 while the same command at `cc8da16` exits 1 with `6/8`. |
| vacuous | Version-1 counters were met by wrong work, measured by wave-1 seats before data: C1 by a rename-with-edit, a subdirectory relocation, a symlink and pointer-only notes (`w1/CriticC1Cheat.md` CH1, CH2, CH4, CH7); C2 by id-magnitude and id-literal masks and canned per-fixture output (`w1/CriticC2Cheat.md`, 12/12); C3 by promo-trailer spans inside the S423 article window (`w1/ExecC3BaseControls.md` H1, 8/8). The C1 version-1 kind names (`relabel`/`rerun`) misnamed 13 of 19 events (`w1/RevengerReceiptIntent.md`). | the round's own attack items (prompt §6 item 9: build the cheapest control before freezing) | counters version 2 (`contract.md` § Counter versions): each cheat is a selftest case or a closed rule; red-before: the version-1 receipts and the seats' tallies above |

Red-before for the first two rows: `.ufo/waves/round-58/controls/base-c1-receipt-rewrites-v2.txt` (exit 1, `undisclosed=19`);
for the third: `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision 044048597d62f3199494b63b36e90dd57825e350`
prints `6/8 met=False` (`w1/ExecHistoricalGates.md`, `w1/ScribeLessonMistakes.md`). Count note: of the 13 events outside the
round-57 errata, `w1/CriticC1Before.md` finds two disclosed in prose at the time (11 disclosed nowhere) and
`w1/ScribeLessonMistakes.md` counts 12; the seats read "disclosed" differently (a generic LOG sentence vs a named receipt), and
the machine before-value (19 events, no ledger) does not depend on it.

## Considerthese

`considerthese/2026-10-26.md` (2026-10-26) proposal 2 (receipt-rewrite watch) is implemented as claim C1, grounded through the lane's
bar by `w1/ScribeConsiderthese.md`: the proposal's file-level watch ("more than one commit touching them", `git log --follow`) names
16 paths, not the 19 events (one path carries several), and misses deletions and renames; the counter's event definition replaces
it. Proposals 1 (landed_check, id_resolver, frontier map) are already landed tools; 3 (operator-decision queue), 4
(gate-agreement ledger) not taken this round (one per round); 5 (historical-gate list) overlaps routed defect D3 and is handled as
the SKILL.md `historical` marking, not as a claim.

## Routed defects (round-57 spot-check §5)

- D1 placeholder receipt: claim C1 and the round-58 receipt rule (receipts committed once, after the run; C1 `new_rewritten`).
- D2 untracked `relabels.json`: committed by the orchestrator salvage `0440485` (the round-58 base); nothing left.
- D3 `c56_quote_truth.py` red on later trees: SKILL.md rows marked historical with their measured revisions (`w1/ExecHistoricalGates.md`).
- D4 SHONEN: untouched (operator-owned promotion).
- D5 resolver limits: fence-blindness and quoted paths closed by claim C2; new limits found (`w1/ReviewerResolverOther.md`: HTML-comment rows,
  setext section end, symlinked knowledge dir) are reported, not targets.

## Trend inputs

expansion: two entries on Baidu crawler-identity ground the coverage map did not hold (the frontier map's `Crawler identity` ground held only
Googlebot subtypes), each citing a `mined` row opened this round (S423, S424); quality: 19 receipt events disclosed with git's values, two
false-green defects of the resolver closed, three counters hardened by a 68-seat wave before data; discernment: one staged entry
re-grounded with nine refused sentences, one staged entry rejected on scope with the page sentence, the non-author spot-check belongs to the closure.
Adjacency (reported, not absorbed; `w1/ConnSiblingOverlap.md`): no sibling owns the three surfaces; tabi splits crawler material and the DNS half is
unowned; kumitate keeps a prose receipt-change file (`w1/ScoutFleetReceipts.md`).
