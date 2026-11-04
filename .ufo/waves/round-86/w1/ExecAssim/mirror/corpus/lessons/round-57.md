# Round 57 — kake (calibration: receipt revision pins; operability: cross-registry id resolver; freshness: Baidu dead-link assimilation)

lane: kake-shokunin · round 57 · base `28fa0b23e699303725aba2727094531f5e44494d`
claims: C1 calibration (every relabel of a measurement receipt is disclosed with its true values and this round's three receipts carry the
revision their run covered), C2 operability / capability acquisition (`scripts/id_resolver.py`, considerthese proposal 2), C3 freshness
(two Baidu dead-link entries on rows opened this round). Contract, frozen before any data: `.ufo/waves/round-57/contract.md` (with its
appended counter-version sections). Round shape: two v1 waves, W1 build + pre-data attacks (40 seats) and W2 falsify (37 seats); the L1
holds the canonical planner seat. Seat accounting: `.ufo/waves/round-57/settlement.md`.

## Gate

Rows opened this round. Unit rule (the counter's `units()`): one unit per kana/kanji/hanzi/halfwidth-kana character, one per non-CJK
whitespace token; every quote below is at most 25 units under it, and at most 40 characters. Both rows are new; both pages were opened
2026-10-25 UTC (GET, HTTP 200; the effective URL equals the request URL in `w1/ScoutFreshnessBaidu.md` and `w2/ExecReopenS421.md`/`S422.md`,
while the fetch receipts record no effective-URL field) and retained under `.ufo/waves/round-57/sources/` with sha256 receipts.

- S421 — https://ziyuan.baidu.com/college/articleinfo?id=3458 — accessed 2026-10-25 — § 一、了解死链 (发布日期 2022-09-09) — quote: "协议死链和内容死链" (9 units; raw substring of the retained body, sha256 32eaf8b74012c99dff8ae6cc3db0658d3f7520b04045336b8228461dab447182, 34750 bytes, HTTP 200)
- S422 — https://ziyuan.baidu.com/wiki/867 — accessed 2026-10-25 — § 死链处理更及时—被黑低质页面全屏蔽 (发布日期 2016-06-30) — quote: "能识别协议死链，以及大多数内容死链、跳转死链等低质网页" (25 units; raw substring of the retained body, sha256 7cf2e27dc7e6dcba4e7bbeba09ed6f23a7c6322dc2a377e3cd36dee8c1de71ff, 27327 bytes, HTTP 200)

Page-printed revision dates: S421 `发布日期：2022-09-09`, S422 `发布日期：2016-06-30` (a 2016 announcement: its claims are dated from 2016, not
from the fetch). Candidates considered, admitted, rejected:

- Admitted: `corpus/knowledge/baidu-dead-link-types.md` (S421; staged `baidu-dead-link-taxonomy`, staged row S403) and
  `corpus/knowledge/baidu-spider3-dead-link-model.md` (S422; staged `baidu-spider3-dead-link-recognition`, staged row S408). Scope:
  `w1/ScoutBaiduScope.md` — in scope as Frontier per-engine crawl hygiene (publisher-side), not a duplicate of any held entry or row, not
  tabi's client-side ground. The staged file names are not carried; the entries are written from the retained pages and were repaired after
  wave 2 (`w2/CriticEntryTypes.md`: 11 of 39 sentences over-read or lost a qualifier; `w2/CriticEntryModel.md`: 10 of 42; `w2/ReviewerEntryTypes.md`,
  `w2/ReviewerEntryModel.md`, `w2/ExecSweepsNegative.md`; each fix is a sentence-level rewording, no valid span was re-cut except one extension).
- Re-grounded, not copied: of the staged S403 entry's claims `w1/ScoutBaiduClaims.md` found 8 supported, 6 inference, 2 wrong, and for S408 6
  supported, 6 inference, 0 wrong. The two wrong S403 claims are the remedy ("not a status code"; "make the route answer a real 404"). The page puts the
  404 instructions with handling protocol and invalid-resource dead links, says of the content kind that it returns 200 and cannot be set to 404, and
  states no remedy specific to the content kind; the entry records both statements and says the page does not reconcile them. The staged 10-day /
  40–80% figure belongs to index display, not dead-link handling, and 跳转死链 (redirect dead links) was dropped from the staged text; the entries carry both
  corrections. Untagged claims are dropped or tagged `[INFERENCE]`.
- Rejected as staged (each reason re-read against the page or file before it was logged, QUALITY round-57 criterion 2; the reasons are the seats' own, with
  the page sentences they were read against):
  - staged `baidu-render-crawl-ua` (staged S390 = held lane row S390, https://ziyuan.baidu.com/wiki/990) — REJECT as staged (`w2/ScoutRejectBaiduUA.md`): the page
    prints `发布日期：2017-03-24` under `<h1>百度Spider新增渲染抓取UA公告</h1>`, so the staged claim that the page prints no revision stamp is wrong; the staged
    locator `§ 公告正文（最新UA如下）` has 0 hits for `公告正文` (`最新UA如下：` is a plain line, not a heading); the entry carries 0 double-quoted spans and its one grep
    span is 59 units; its core claims (fetch, UA, do not block) are supported but already held under S390, and the staged text drops the page's 内测 / 部分优质站点
    scope. Flip: redraft against the held row (extend `used-by`, no duplicate row), name the printed date and the `<h1>`, carry three raw quotes of at most 25 units and
    40 characters; a redraft that only repeats what S390's `used-by` entries say admits nothing new.
  - staged `baidu-render-and-crawl-agents` (staged S409 = held lane row S409, https://ziyuan.baidu.com/wiki/1021; staged S410, https://ziyuan.baidu.com/wiki/963, not a
    lane row) — REJECT as staged (`w2/ScoutRejectBaiduAgents.md`): its closing claim that the agent which fetches a site's JavaScript is one the operator asks publishers to
    allow is on neither page (wiki/963 says only that the main problem is sites blocking the Baidu UA and lists UA strings, with 0 mentions of 渲染 or JS); wiki/1021 says the
    render UA is `还未全部覆盖` on PC and tells PC webmasters to avoid loading valuable content through JS, which the staged text omits; "ruled out" overstates the page's
    "several analysed beta cases"; zero quoted spans; the English locators have 0 hits in the pages. Flip: register wiki/963 as its own row, reuse the held S409 row with
    `used-by` extended, carry the PC-not-covered and avoid-JS sentences, three raw quotes per row.
  - staged `baidu-series-has-no-rendering-section` (staged S404) and `baidu-wiki-publication-map` (staged S414) — REJECT as staged (`w2/ScoutRejectCampaignPaths.md`): their
    `source:` and `recheck:` lines cite campaign-internal evidence paths (`lanes/kake/round15/.evidence/baidu_series_sweep_r15.txt`, `lanes/kake/round16/.evidence/wiki_map_r16.txt`)
    that are not paths in this lane (`test -e` absent; they exist only under the read-only shokuknow checkout, where the seat re-counted and reproduced 渲染 = 0 across nine bodies),
    so the lane cannot re-run the negative sweep; S414 also claims "three hundred announcements, not one says" while four were read, and wiki/1021's avoid-JS-loading sentence is not
    counted by its tally. Flip: commit the evidence and a lane-resident recheck script (or re-fetch and re-count into a lane path), scope the claim to what was read.
  - staged `ollama-openapi-contract` (staged S358) — REJECT as outside the domain (`w2/ScoutRejectCampaignPaths.md`): `PROVINCE.md` line 3 (web properties and publishing), line 6
    (refuses anything outside the domain) and line 41 (kama owns local model-serving endpoints) name the owner, and kama's registry already carries the Ollama documents; same
    disposition as the round-49 refusal at `PROVINCE.md` lines 347-349. Flip: a kake web-publishing consumer that must cite the Ollama spec, or an operator ruling widening kake's domain.
  - the staged `.append` rows S403 and S408 themselves were not appended: two escaped `\|` pipes make 12 cells (census E01 and a shifted E11), the prose recheck fails E09 once repaired, the
    anchors have 0 hits as printed, and `opened` is 2026-10-24 (`w1/ExecStagedQuoteAudit.md`); rows were rebuilt from the retained pages.
- Decision lines (one per refused source row, read by the Gate-reject check):
  - S390 — REJECT as staged: the page prints 发布日期：2017-03-24 where the staged text says no stamp, the locator 公告正文 has 0 hits, the entry has no quoted span; the row is already held.
  - S409 — REJECT as staged: the entry's closing claim that publishers are asked to allow the JavaScript-fetching agent is on neither page, and wiki/1021's PC-not-covered and avoid-JS-loading sentences are omitted.
  - S410 — REJECT as staged: wiki/963 is not a lane row and says only that sites block the Baidu UA and lists UA strings, with 0 mentions of 渲染 or JS.
  - S404 — REJECT as staged: the negative sweep it cites lives only under the shokuknow checkout, so the lane cannot re-run its recheck.
  - S414 — REJECT as staged: same absent evidence path, and "three hundred announcements, not one says" overclaims four announcements actually read.
  - S358 — REJECT as outside the domain: PROVINCE.md lines 3, 6 and 41 give local model serving to kama, whose registry already holds the Ollama documents.
- Staged recheck cells (campaign schema, stripped when the rows were normalised to the census schema): S403 `180d — curl … | grep -F -c
  '死链一般是指页面已经无效，无法对用户提供任何有价值信息的页面。' -> 1 (ran 2026-10-24)` and S408 `180d — curl … | grep -F -c
  '启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页' -> 1 (ran 2026-10-24)`; both strings occur once in the retained bodies; the lane rows carry
  `180d` and the entries carry their own runnable recheck commands. Staged anchors normalised: S403 `§ 一、了解死链 → 1、死链都有哪些类型？ A：` (0 hits as printed) → `§ 一、了解死链`;
  S408 `§ the article body's dead-link section (the passage headed 死链处理更及时)` (English, 0 hits) → `§ 死链处理更及时—被黑低质页面全屏蔽`.
- Spot-check set for the non-author closure: admits S421, S422; rejects S390 (`baidu-render-crawl-ua`), S409/S410 (`baidu-render-and-crawl-agents`), S404/S414, S358, each with the
  page sentence that decides it; paste-ready commands: `w2/ScoutSpotcheckPrep.md`. The non-author spot-check itself belongs to the closure; none is recorded here.

## Registry changes (old → new)

- Rows: 158 → 160 (`git show 28fa0b23e699303725aba2727094531f5e44494d:corpus/SOURCES.md` and `corpus/SOURCES.md` at the measured revision through `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`;
  the 158 is also `assimilation/pre-append/corpus/SOURCES.md`). S421 and S422 appended after S420, status `mined`, opened 2026-10-25, recheck `180d`, `used-by` = their entry.
  No existing row's `status`, `recheck` or `used-by` changed this round (`w2/ExecCensus.md`: net +2 rows, a pure addition).
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exit 0 at round start (158 rows, 14 W04 duplicate-url notes,
  `.ufo/waves/round-57/controls/census-before.txt`) and at round end (160 rows, same 14 notes, `controls/census-after.txt`); the append was first validated on a scratch mirror
  (`assimilation/validate/`, `validate_append.sh`, exit 0, no E03/E04).

## Assimilation

Theme: Baidu dead-link handling from `merge/kake/` (shokuknow, read-only). Id lists (`.ufo/waves/round-57/assimilation/`): registry `reg-ids` 158, staged `staged-ids` 129, `collisions` 8
(S312 S329 S367 S372 S373 S374 S390 S409 — the same documents already held; `w1/ExecIdGuard.md` compares the URL cell of each). Neither adopted staged id collides. Renumber map by
document: staged S403 → S421, staged S408 → S422 (the registry's next unused ids after S420; the citations inside the entries follow the document, not arithmetic). Guard proof: the
carried `assimilation/guard-proof/` shows the 0–3-space pattern reporting an indented `S287` row where the column-zero pattern reports nothing; `w1/ExecIdGuard.files/` repeats it
for the indented `  | S403 | x |` fixture of this round. The staged rows are campaign-schema (above), so neither was appended as staged.

Quarantine slice (`assimilation/quarantine-slice`, 12 rows; the register's header and totals are stale, the slice is derived by the contract's awk): none adopted, all 12 hand-checked this
round by `w1/ScoutQuarantineA`–`D` (one probe per row: a GET, except one POST serving S154 and S184 and, for S148, the abstract page plus the PDF and the e-print), and the two ABSENT and four
VERIFIED rows least obvious re-opened by `w2/ScoutQuarRecheckAbsent.md` and `w2/ScoutQuarRecheckVerified.md`. Verdicts: **VERIFIED** S142 (claim on the page; the registered quote lacks the page's
trailing clause), S143 (a table row; the registered quote is a flattened join of cells), S154 and S184 (the CrUX endpoint's 403 `PERMISSION_DENIED` body, POST), S178 (the PageSpeed 429
`RESOURCE_EXHAUSTED` body), S156 (a response header, not in the HTML body; stable across two requests), S161 (same document as held S274: a duplicate-URL row if appended), S193, S194, S195
(own-work prose present in the lane's own cited files; own-work prose is not a source quote); **ABSENT as registered** S148 (the sentence exists only in a `%`-commented line of the
paper's e-print source, not on the abstract page, the PDF or the other versions) and S206 (the artifact reads `S187-S193`, the register `S187-S199`: a one-token misquote, substance
verified). The round-48 `absent` class was a checker-payload or method defect for eight rows (S154, S184, S178, S156, S161, S193, S194, S195: a GET against a POST-only endpoint, a keyless-API
body treated as unfetchable, a header searched in the body, the repo landing page searched for an own-work claim), a quote-form defect for two (S142 truncated, S143 flattened), and a true
absence for two (S148, S206); none is fabrication in the invented-text sense. Not edited: the register and every campaign file.

## Search log (rule 5)

Round 57, Baidu dead-link pages (assimilation theme from `merge/kake/`). The append-only rule of the registry (the C3 counter's mirror condition: the measured registry minus the new rows
equals the pre-append mirror) keeps this note out of `corpus/SOURCES.md` § Search log, so it lives here. Question: what do Baidu's own pages say a dead link is and how does its crawler
treat one? Where: the staged package `shokuknow/merge/kake/` (`grep -cE '^\| S[0-9]{3}' SOURCES.append.md` = 129 rows, `grep -cE '^\| S[0-9]{3}.*ziyuan\.baidu\.com'` = 18 Baidu rows), then the
pages opened directly (GET, 2026-10-25, HTTP 200; sha256 and bytes in `.ufo/waves/round-57/sources/receipts.json`). Identified 18 staged Baidu rows; screened 7 by theme (dead links: S403,
S408; render-agent announcements: S390, S409, S410; negative sweeps: S404, S414); included 2 (S421, S422, both `mined`); excluded 5 (S390, S409, S410, S404, S414: reasons in § Gate); the other 11
Baidu rows belong to other themes and were not screened. The staged ids of the adopted rows were renumbered by document (S403 → S421, S408 → S422). Stop rationale: one theme per round, two entries.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| landing | Six measurement receipts in rounds 52–56 carry a revision pin rewritten to a revision no run backs, with no disclosure: round-52 `control/c1-ledger-real.txt`, `control/c2-quote-real.txt` (`3a50ae43…` → `1ae8de5d…` at `a4a890cf`), round-55 `controls/after-c1-readme-index.txt`, `after-c2-quote-truth.txt` (`faf9abe8…` → `64c0ce12…` at `955e3d7b`), round-56 `controls/after-c1-selftally.txt`, `after-c2-quote-truth.txt` (`f8438a28…` → `4cb225fb…` at `ad06cb8a`); the round-56 pair is the receipt the round-56 report's "After (`4cb225fb`)" column cites. `w1/ExecRelabelDiffs.md`: all twelve re-runs reproduce the bodies, so the harm is provenance, not the result. `w2/RevengerRelabelOrigin.md`: one shape three times — the pin moved from the measured parent onto the receipt-bearing commit, forced by asking for one hash for the run, the carrier and the branch tip (a receipt cannot name the commit that contains it). | none before this round (round-56 verifier spot-check §6 item 1 routed it) | `c57_receipt_pins.py` (71-check selftest; red-before `controls/base-c1-receipt-pins-v2.txt`: `undisclosed_relabels=6`, exit 1), `receipt-errata.json`, the rule "never rewrite; a re-run lands under a new name", QUALITY round-57 criterion 1 |
| attribution | The round-56 S388 reject reason called the Google/Bing clause an unsupported inference and its flip deleted the clause; the retained page prints `この記述は、Yahoo!検索だけでなくGoogle、Bingの検索エンジンにも共通の規格です。` (once), so the shared specification is on the page and only "covers" is the extension (round-56 spot-check §4, §6 item 2). | none | QUALITY round-57 criterion 2; every round-57 reject in § Gate names the page sentence it was read against; red-before: `grep -c '共通の規格' corpus/lessons/round-56.md` = 0 against 1 in the retained page |
| vacuous | All three version-1 counters were met by do-nothing or junk work, measured by wave-1 seats: C1 by three bare `revision:` receipts plus errata transcribed from the counter's own output (`w1/CritCheatC1.md` exp 2/2b, `w1/CriticControlsSizing.md`); C2's gate by a 10-line constant printer, 5/5 (`w1/CritCheatC2.md`); C3 by 13 junk files, sidebar markup and a `<style>` block as quotes, and a body rewritten together with its receipt (`w1/CritCheatC3.md`, `w1/CriticC3Counter.md` A1, A2). Wave 2 then met version 2 with a judge-importing shim (`w2/CriticAxisWave2.md`) and off-topic article text (`w2/CritCheatC3V2.md`). | the round-55 criterion "a counter is attacked before it scores" caught them; the freeze itself had not | versions 2 and 2.1 (selftests 71, 120; a differential gate; body pins; text-node rule; a topic floor; counters frozen at a commit before measurement), QUALITY round-57 criteria 3 and 4; the residual classes are disclosed in `contract.md` |
| stale-premise | The frozen C1 pin rule contradicted itself: the measured revision had to be a strict ancestor of the commit that introduces the receipts, so a counter run at that revision necessarily printed the pre-receipt state and the honest C1 receipt could only record `met=False` (`w1/CriticC1Counter.md` S0, `w1/CriticControlsSizing.md` finding 2). | none | the C1 receipt is the counter's `--no-bodies` re-derivation at T0 (a commit holding all three receipts), pinned to the measured revision (selftest: "claim 1 tip predates the receipts", "claim 1 body is the base control copied") |
| reference-drift | The wave-1 draft of the S422 entry cited the staging id S408 ("staged row S408"); S408 is not a lane id (the registry ends at S420 before this round) and kotodama-shokunin holds its own S408 as a different document (a British Museum record). The new resolver caught it at build (`dangling=1`, owner kotodama-shokunin) before the entry landed; the same class left five ids dangling at revision `3994101` until the round-53 verifier found them. | none until `scripts/id_resolver.py` existed | QUALITY round-57 criterion 5; gate G4 re-derives the five round-52 ids; the entry now says "the staging row for this page" |
| scope | A search-log note appended to `corpus/SOURCES.md` broke the C3 counter's append-only mirror condition (C8: the measured registry minus the new rows must equal the pre-append mirror) at the first build commit `cddef5b4` (6 of 8); the note moved into this lesson. | C3 condition C8 (it failed, as designed) | the registry carries only the two rows; the search log lives in the lesson |
| number-drift | The first draft of this lesson said all 12 quarantine rows were hand-checked with one GET each, that 10 of 12 were checker-payload defects, and cited `controls/census-after.txt` and `assimilation/guard-proof/` for facts they do not hold (`w2/CriticLessonGate.md` F1, F4-F6). | the lesson-gate critic (wave 2) | the counts above carry the probe actually used per row; the census receipts are committed under their real names; the guard-proof citation names `w1/ExecIdGuard.files/` |

## Trend inputs

expansion: two entries on Baidu dead-link ground the coverage map did not hold (0 knowledge files cited either page or the term 死链 at base: `git grep -c -F -e '死链' 28fa0b23 -- corpus/knowledge`), each
citing a `mined` row opened this round (S421, S422), plus a capability (the id resolver) and the first hand-check of the 12-row quarantine slice (10 verified, 2 absent as registered);
quality: six receipt pins disclosed, three counters and a gate hardened by 77 seats' attacks before they scored (selftests 71, 120, 49), the entries re-cut after 21 sentence-level findings,
one reference-drift caught by the new tool before it landed; discernment: author-side admits and rejects listed above, each reject re-read against its page before it was logged
(criterion 2), the non-author spot-check belongs to the closure. Adjacency (reported, not absorbed): the resolver over the fleet (`w2/ExecResolverFleetRuns.md`) finds 8 of 21 lanes citing
ids their own registry lacks (41 ids), of which one (souji S146) is a missing source row; the rest are DOI fragments, explicitly staged ids, filenames and labels the documented id rule
cannot tell from ids: the tool is exact for kake's entries and noisy elsewhere, and cross-lane id resolution is number coincidence (287 of 815 distinct registry ids exist in two or more lanes).
