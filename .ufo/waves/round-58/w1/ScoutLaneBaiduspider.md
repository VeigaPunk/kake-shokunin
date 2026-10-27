# ScoutLaneBaiduspider

Read-only consistency scout, 2026-10-26. Greps over `corpus/knowledge/` (all 54 files) for `Baiduspider`, `baidu.com`, `reverse DNS`, `反查`, `UA`, `user agent`, plus `spoof|冒充|nslookup|rDNS|S395|S416|3457|3028` over corpus/ and `.ufo/waves/`. Full reads of `crawler-identity.md` and `baidu-friendly-crawl-guidance.md`. Spans of S423 / S424 read with `span_tools.py spans`. Nothing fetched live; nothing run on the network. Paths below are relative to the lane repo.

## EXISTING STATEMENTS:

Baidu crawler token / robots scope (`corpus/knowledge/baidu-friendly-crawl-guidance.md`, S329/S416):
- :11 `> "如果封禁的agent是Baiduspider，会对PC和移动同时生效"` — a robots block on Baiduspider binds PC and mobile at once.
- :33-38 "One token governs two crawlers … a single `User-agent: Baiduspider` block covers both". Line 36-38 ("the opposite consequence") is withdrawn by the :68 correction (parallel to Googlebot; clause sits under `如何正确识别Baiduspider移动ua`, header 最新更新章节 2019-09-18).
- :49-51 does not establish script execution; render agent is "named" in S390/S409.
- :52-53 does not state how long a blocked object stays unfetched after the block is lifted.
- :68 (round-53 correction, append-only): the S329 PC/mobile clause is under heading `如何正确识别Baiduspider移动ua`. This is the same heading family the new identification entry covers, so the identification entry cannot claim the lane has no Baiduspider-identification statement.

Baidu mobile matching (`baidu-mobile-matching-error-causes.md`): :16 quote "放开对Baiduspider的robots封禁…" (robots block withholds the PC-mobile correspondence); :31-33 restates that one Baiduspider block binds both; :34-35 the ajax cause is "a precondition for the lane's rendering rows" (S390, S409); :43-45 no script-execution claim.

Baidu render UA (`corpus/SOURCES.md`): :160 S390 — render UA `Baiduspider-render/2.0` from 2017-03-24, publishers asked not to block it; says it fetches CSS/JS/images, not that it executes. :161 S409 — render UA on full mobile traffic, not yet all PC traffic. The retained S390 body holds the same two UA strings as S423 (PC `Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)`; iPhone `… Mobile/13B143 Safari/601.1 (compatible; Baiduspider-render/2.0; …)`), spacing differs slightly.

Baidu dead-link entries (r57): `baidu-dead-link-types.md` :53-58 "Baiduspider periodically checks page content value" (S421); `baidu-spider3-dead-link-model.md` (S422). Neither mentions identification, DNS or UA strings.

Crawler identity, Google side (`corpus/knowledge/crawler-identity.md`, S263):
- :6 title `"Googlebot" is a family name, not one crawler`; :20-23 subtype is told apart by the HTTP user-agent request header; :27 both types obey the same product token.
- :31-34 **"A user-agent string is the only thing a server log records about the crawler."** — flagged in r51 as contradicted by S263's own "Verifying Googlebot" section (`.ufo/waves/round-51/w1/ScribeEntryAudit.md:223`: UA "is often spoofed by other crawlers"; best verification is reverse DNS on the source IP or an IP-range match). Still in the entry unrepaired; `corpus/lessons/round-51.md:135-140` routes it "not repaired this round".
- :52-53 "does not establish anything about how a specific crawler identifies itself on a specific lane property: no operator-owned property was fetched this round."
- :50-51 "does not enumerate the non-Google bots … the lane has no use for that list beyond identity."
- No file in `corpus/knowledge/` contains `spoof`, `冒充`, `反查`, `nslookup`, `host ip`, `dig`, `baidu.jp` or `reverse DNS` (grep, zero hits outside the r51 audit and the r55 reject notes). The Baidu DNS procedure is new ground.

Registry / README:
- `corpus/README.md:53` coverage row "Crawler identity (Googlebot subtypes) | crawler-identity.md (S263)"; `:94` frontier row "Crawler identity (Googlebot subtypes) | r51 | S263"; `:100` "Baidu crawl guidance | r52; locators superseded r53 | S329 S373 S390 S409"; `:101` Baidu mobile matching; `:104` r57 Baidu dead-link row. `:48-49` Baidu robots / mobile-matching coverage rows; `:73-74` dead-link rows.
- `corpus/SOURCES.md:153` S263; `:155` S329; `:156` S312; `:162` S416 (S329 superseder, W04 duplicate URL); `:163` S417; `:160-161` S390/S409; `:167-168` S421/S422. No row names `id=3457` or `id=3028` (S423/S424 are new).
- `.ufo/waves/round-58/contract.md:65-68` names the Crawler-identity frontier ground and the two entries.

Yahoo precedent (r55, `corpus/lessons/round-55.md:36-37`; verifier `round-55-verifier-spotcheck.md:62`): staged `yahoo-japan-crawler-identification-by-dns` (S386) REJECTED because its load-bearing DNS-vs-name mechanism is a fact about `info-search.yahoo.co.jp/archives/002855.php`, a page the lane does not hold. `yahoo-japan-nonexistent-url-recrawl.md:81` also records that a ユーザーエージェント mention was only a sidebar anchor. So the lane has NO held identification procedure for any operator other than the Googlebot UA-subtype text.

Retained-body facts the entries must stay inside (from `span_tools.py spans`):
- S423 (发布日期 2022-08-19, 搜索问答剧场 第五集): Q2 offers two ways to judge a real Baiduspider — (1) UA (three scenarios: 移动 two strings, PC two strings, 小程序 one string; `Baiduspider/2.0` and `Baiduspider-render/2.0`, the Smartapp string carries `Baiduspider-render/2.0;Smartapp;`); wrong UA ⇒ "可以直接判断为非百度搜索的蜘蛛"; (2) two-step bidirectional DNS — reverse lookup hostname `*.baidu.com` or `*.baidu.jp`, otherwise 冒充, via `host` (linux), `nslookup` (windows/OS2), `dig` (mac), then forward lookup must return the original IP. The same page's 封禁篇 repeats the robots/UA/IP unblocking list and the curl UA check (so S423 already contains S424's substance; S424 is a longer standalone version). It links `id=2855` (《轻松两步，教你快速识别百度蜘蛛》) and `id=3028` (S424), both inside the article block.
- S424 (发布日期 2020-07-23): symptom (no crawl records / not indexed / 摘要 "存在robots封禁"); three block kinds "robots封禁、封禁百度UA、封禁百度IP"; step order robots.txt → UA (`curl --head --user-agent 'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)' --request GET`, normal code 200) → IP-level firewall; links `id=1516` (robots doc) and `id=2855`.

## CONFLICT RISKS:

1. **Duplication of S329/S416's "PC and mobile" clause.** The new identification entry must not re-quote or restate `如果封禁的agent是Baiduspider，会对PC和移动同时生效` (already quoted raw at baidu-friendly-crawl-guidance.md:11 under the same heading family). S423's three UA scenarios (移动 / PC / 小程序) are a third class beyond the "two crawlers" frame at :6, :33-35; do not write "Baidu has two crawlers" or "one token covers all UAs". Whether a `User-agent: Baiduspider` block also binds `Baiduspider-render` is stated by neither S329 nor S423 [INFERENCE: not covered by any held page; S390 only says don't block the render UA] — say nothing.
2. **Parallel-to-Google overreach.** :36-38 "opposite consequence" is withdrawn (:68); the new entry must not revive it or cast Baidu's UA/DNS as a counterpart "with the opposite consequence". Cross-engine framing is safe only as "S263 and S423 each give a UA route and a DNS route" — S263's DNS route is NOT quoted in `crawler-identity.md` (line 31 even denies a log has more than the UA), so do not write "like the Googlebot entry says".
3. **Direct contradiction with `crawler-identity.md:31-34`.** S423 says a wrong UA means not-Baidu AND that UA-correct requests may still be 冒充 and need DNS confirmation (and its Q3/Q4 tell publishers to check access logs against 恶意冒充 traffic). A new entry saying "UA alone is insufficient" contradicts the unrepaired sentence on the Google entry. Either carry a cross-link noting the Google entry's sentence is the r51-audited known defect, or do not touch crawler-identity.md and keep the Baidu entry self-contained. Do not state "UA is the only thing logged".
4. **"Not established" collisions.** `crawler-identity.md:52-53` says no operator-owned property was fetched — keep that true: the new entries describe a documentation reading, not a verified hostname/IP of any real Baiduspider request. No claim that `*.baidu.com`/`*.baidu.jp` is current, complete, or sufficient beyond what S423 says; no list of IP ranges (S423 gives none). `baidu-friendly-crawl-guidance.md:49-53` "does not establish script execution / crawl rate / unfetched time after lifting": S423's "百度蜘蛛不是立即停止抓取网页" is about the delay after a robots update (a block added), not lifting — do not use it to fill the :52-53 gap [INFERENCE: S423 sentence reads as about updating robots to disallow; the unblocking page S424 states no recovery timing].
5. **Duplication between the two new entries.** S423's 封禁篇 Q3 (robots / UA / IP blocks; curl UA check) is the same content as S424. The unblocking entry must quote S424 spans (≤25 units, ≤40 chars, raw, in the article block) and may not be justified by "S423 says it too". Use distinct spans: S423 for UA table + two-step DNS + 冒充; S424 for the three block kinds and the curl-based check plus return-code note.
6. **Numeric-id collision hazard.** `id=2855` on ziyuan.baidu.com (linked from both pages) shares its number with Yahoo `archives/002855.php` (the page the lane rejected the S386 staged DNS entry over). The lane holds neither. Never write "2855" bare in a registry cell, README row, or entry; always the full URL, and never imply the Yahoo reject applies. Note id=1516 (robots doc) and id=2855 are NOT held rows; any claim about their content is out of scope.
7. **Span-quality traps in the retained bodies (not contradictions, but they affect stated units).** The longest identification spans exceed the unit/character bounds: the key DNS spans are 30u/107c, 32u/165c, 68u/88c, 27u/45c — only short fragments qualify; UA lines are 83-219 chars (over 40c). Spans contain `&nbsp;`: a raw substring must keep the bytes `&nbsp;`, not a space. Do not quote the UA strings as spans; name `Baiduspider/2.0`, `Baiduspider-render/2.0` in backticks and anchor on short spans instead.
8. **Dating.** S423 prints 2022-08-19, S424 2020-07-23, S329/S416 header 2019-09-18; S421 2022-09-09. The unblocking page predates identification by two years and its curl UA is the unrendered `Baiduspider/2.0` PC string only — not a statement that mobile or render UAs need the same check. Do not generalise.
9. **Source URL / row duplication.** S423's URL is new (no W04 added). S424 is `used-by` only the unblocking entry and must not be used by the identification entry (contract: "S424 … linked from S423" is a lane-found link, not a staged row); census currently 14 W04 warnings from S416/S417 — the new rows must keep that at 14.
10. **Staged S395 text is not authority.** The staged entry `merge/kake/baidu-crawler-identification.md` (not read; `<lane>/merge/kake` does not exist — `ls` error; a `baidu` grep of `<fleet>/merge/kake` listing returned nothing) may carry r-staged quotes; anything from it must be re-verified against `sources/S423.html` before use.

## CROSS-LINKS:

For `baidu-spider-identification.md` (S423):
- `corpus/knowledge/crawler-identity.md` (S263) — sibling ground; link with an explicit scope note: that entry's UA-subtype and "family name" framing differs; do not import its :31 sentence.
- `corpus/knowledge/baidu-friendly-crawl-guidance.md` (S329/S416) — PC-and-mobile robots scope, and the :68 locator correction; point to it instead of restating the clause.
- S390 / S409 rows (`SOURCES.md:160-161`) — `Baiduspider-render/2.0` is the same UA token that S423's UA table lists; link by id, state only that both name it, not that S423 covers the rendering question.
- `corpus/knowledge/baidu-spider-unblocking.md` — the S424 sibling (blocks / curl UA check); reciprocal link.
- `corpus/knowledge/baidu-mobile-matching-error-causes.md` (S312/S417) — optional: the robots-block cause for matching failure is another face of "Baiduspider is being refused".
- `corpus/knowledge/robots-txt-rules.md` (S011/S095) — robots product-token reading (`:39`); S423 states Baiduspider "遵守互联网robots协议".
- Do NOT link `yahoo-japan-*` entries as support; only mention the r55 reject if a dated note is needed (`corpus/lessons/round-55.md:36-37`).

For `baidu-spider-unblocking.md` (S424):
- `baidu-spider-identification.md` (reciprocal; S423's 封禁篇 states the same three blocks).
- `baidu-friendly-crawl-guidance.md` and `baidu-mobile-matching-error-causes.md` (robots-block cause), `robots-txt-rules.md`, `crawl-scope-per-host.md` (host-root robots location; its :10 4xx/5xx robots statuses), `crawl-error-status-table.md` (200 as the "normal code" the curl check expects — verify before linking; not read).
- `baidu-dead-link-types.md` — note only that `200` here is the normal return of a UA check, not a content dead-link answer (S421 :content kind answers 200); a possible confusion for readers [INFERENCE].

Registry/README rows to add (names only; owned by the integrator): `corpus/README.md` coverage rows near `:53` and `:48-49`; frontier row near `:94` (Crawler identity) widened to name both Baidu entries and rows S423 S424; do not reuse "Googlebot subtypes" in the row label. SOURCES rows S423/S424 must carry `used-by` with exactly one entry path each (counter condition in contract). Retained bodies `sources/S423.html`, `sources/S424.html` + `receipts.json`.

Unrun/unread: live fetch of any page (unrun); `merge/kake/` staged entry (absent); `corpus/knowledge/crawl-error-status-table.md` body (not opened); whether S423's 简体 body is byte-identical to the staged copy (unrun).

VERDICT: no statement in the lane forbids the two entries, but crawler-identity.md:31-34 (unrepaired r51 "UA is the only thing logged") contradicts S423's DNS-verify point and the PC/mobile/render/小程序 UA classes must not be folded into baidu-friendly-crawl-guidance.md's "one token, two crawlers" frame.
