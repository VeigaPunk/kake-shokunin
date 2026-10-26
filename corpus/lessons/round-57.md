# Round 57 — kake (calibration: receipt revision pins; operability: cross-registry id resolver; freshness: Baidu dead-link assimilation)

lane: kake-shokunin · round 57 · base `28fa0b23e699303725aba2727094531f5e44494d`
claims: C1 calibration (every relabel of a measurement receipt is disclosed with its true values and this round's three receipts carry the
revision their run covered), C2 operability / capability acquisition (`scripts/id_resolver.py`, considerthese proposal 2), C3 freshness
(two Baidu dead-link entries on rows opened this round). Contract, frozen before any data: `.ufo/waves/round-57/contract.md` (with its
appended counter-version section). Round shape: two v1 waves, W1 build + pre-data attacks (40 seats) and W2 falsify; the L1 holds the
canonical planner seat. Seat accounting: `.ufo/waves/round-57/settlement.md`.

## Gate

Rows opened this round. Unit rule (the counter's `units()`): one unit per kana/kanji/hanzi/halfwidth-kana character, one per non-CJK
whitespace token; every quote below is at most 25 units under it, and at most 40 characters. Both rows are new; both pages were opened
2026-10-25 UTC (GET, HTTP 200, no redirect) and retained under `.ufo/waves/round-57/sources/` with sha256 receipts.

- S421 — https://ziyuan.baidu.com/college/articleinfo?id=3458 — accessed 2026-10-25 — § 一、了解死链 (发布日期 2022-09-09) — quote: "协议死链和内容死链" (9 units; raw substring of the retained body, sha256 32eaf8b74012c99dff8ae6cc3db0658d3f7520b04045336b8228461dab447182, 34750 bytes, HTTP 200)
- S422 — https://ziyuan.baidu.com/wiki/867 — accessed 2026-10-25 — § 死链处理更及时—被黑低质页面全屏蔽 (发布日期 2016-06-30) — quote: "能识别协议死链，以及大多数内容死链、跳转死链等低质网页" (25 units; raw substring of the retained body, sha256 7cf2e27dc7e6dcba4e7bbeba09ed6f23a7c6322dc2a377e3cd36dee8c1de71ff, 27327 bytes, HTTP 200)

Page-printed revision dates: S421 `发布日期：2022-09-09`, S422 `发布日期：2016-06-30` (a 2016 announcement: its claims are dated from 2016, not
from the fetch). Candidates considered, admitted, rejected:

- Admitted: `corpus/knowledge/baidu-dead-link-types.md` (S421; staged `baidu-dead-link-taxonomy`, staged row S403) and
  `corpus/knowledge/baidu-spider3-dead-link-model.md` (S422; staged `baidu-spider3-dead-link-recognition`, staged row S408). Scope:
  `w1/ScoutBaiduScope.md` — in scope as Frontier per-engine crawl hygiene (publisher-side), not a duplicate of any held entry or row, not
  tabi's client-side ground. The staged file names are not carried; the entries are written from the retained pages.
- Re-grounded, not copied: of the staged S403 entry's claims `w1/ScoutBaiduClaims.md` found 8 supported, 6 inference, 2 wrong (a remedy
  stated as "not a status code" and "make the route answer 404" contradict the page: the page's remedy is to set the page to 404 and to
  submit through the dead-link tool, which recognises 404 only), and for S408 6 supported, 6 inference, 0 wrong (the 10-day / 40–80%
  figure belongs to index display, not to dead-link handling; 跳转死链, redirect dead links, was dropped from the staged text). Wrong or
  untagged claims are dropped or tagged `[INFERENCE]` in the entries.
- Rejected as staged (reason re-read against the page before it was logged; see § Rejects below for the page sentences and flips).
- Staged `recheck` cells (campaign schema, stripped when the rows were normalised to the census schema): S403 `180d — curl … | grep -F -c
  '死链一般是指页面已经无效，无法对用户提供任何有价值信息的页面。' -> 1 (ran 2026-10-24)` and S408 `180d — curl … | grep -F -c
  '启用了全新的死链识别模型，能识别协议死链，以及大多数内容死链、跳转死链等低质网页' -> 1 (ran 2026-10-24)` (two escaped `\|` inside; both
  strings occur once in the retained bodies, `w1/ExecStagedQuoteAudit.md`, `w1/ScoutFreshnessBaidu.md`); the lane rows carry `180d` and the
  entries carry their own runnable recheck commands. Staged anchors normalised: S403 `§ 一、了解死链 → 1、死链都有哪些类型？ A：` (0 hits as
  printed) → `§ 一、了解死链`; S408 `§ the article body's dead-link section (the passage headed 死链处理更及时)` (English, 0 hits) → `§ 死链处理更及时—被黑低质页面全屏蔽`.
- Spot-check set for the non-author closure: admits S421, S422; rejects as logged in § Rejects.

## Registry changes (old → new)

- Rows: 158 → 160 (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`, 2026-10-25). S421 and S422 appended after S420, status
  `mined`, opened 2026-10-25, recheck `180d`, `used-by` = their entry. No existing row's `status`, `recheck` or `used-by` changed this round.
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` exit 0 at round start (158 rows,
  `.ufo/waves/round-57/controls/census-before.txt`) and at round end (160 rows, `controls/census-after.txt`); the append was first validated on
  a scratch mirror (`assimilation/validate/`, `validate_append.sh`, exit 0, no E03/E04).

## Assimilation

Theme: Baidu dead-link handling from `merge/kake/` (shokuknow, read-only). Id lists (`.ufo/waves/round-57/assimilation/`): registry `reg-ids` 158,
staged `staged-ids` 129, `collisions` 8 (S312 S329 S367 S372 S373 S374 S390 S409 — the same documents already held; `w1/ExecIdGuard.md` compares
the URL cell of each). Neither adopted staged id collides. Renumber map by document: staged S403 → S421, staged S408 → S422 (the registry's next
unused ids after S420; the citations inside the entries follow the document, not arithmetic). Guard proof: a scratch registry with the indented
row `  | S403 | x |` — the 0–3-space pattern reports S403 and the column-zero pattern reports nothing (`assimilation/guard-proof/`,
re-proved by `w1/ExecIdGuard.md`). Staged rows are campaign-schema: both carry an escaped `\|` (12 cells, census E01 and a shifted E11 as-is, E09
on the prose recheck once the pipe is repaired — `w1/ExecStagedQuoteAudit.md`), so neither was appended as staged.

Quarantine slice (`assimilation/quarantine-slice`, 12 rows; the register's header and totals are stale, the slice is derived by the contract's
awk): none adopted, all 12 hand-checked this round by `w1/ScoutQuarantineA`–`D` (one GET each, 2026-10-25). Verdicts: **VERIFIED** S142
(claim on the page; the registered quote lacks the page's trailing clause), S143 (a table row; the registered quote is a flattened join of
cells), S154 and S184 (the CrUX endpoint's 403 `PERMISSION_DENIED` body, POST), S178 (the PageSpeed 429 `RESOURCE_EXHAUSTED` body), S156 (a
response header, not in the HTML body), S161 (same document as held S274: a duplicate-URL row if appended), S193, S194, S195 (own-work prose
present in the lane's own cited files; own-work prose is not a source quote); **ABSENT as registered** S148 (the sentence exists only in
commented-out LaTeX in the paper's e-print source, not on the abstract page or in the PDF) and S206 (the artifact reads `S187-S193`, the
register `S187-S199`: a one-token misquote, substance verified). The round-48 `absent` class was, for 10 of 12 rows, a checker-payload
defect (body-only search for a header quote, a GET against a POST-only endpoint, the repo landing page for an own-work claim, markdown
backticks against rendered `<code>`), not fabrication; none is fabrication in the invented-text sense. Not edited: the register and every
campaign file.

## Search log

Round 57, Baidu dead-link pages (assimilation theme from `merge/kake/`). The append-only rule of the registry (the C3 counter's mirror condition: the measured registry minus the new rows equals the pre-append mirror) keeps this note out of `corpus/SOURCES.md` § Search log, so it lives here. Question: what do Baidu's own pages say a dead link is and how does its crawler treat one? Where: the staged package `shokuknow/merge/kake/` (two staged rows, S403 and S408, both Baidu 搜索资源平台 pages), then each page opened directly (GET, 2026-10-25, HTTP 200, no redirect; sha256 and bytes in `.ufo/waves/round-57/sources/receipts.json`). Identified 2, screened 2, included 2 (S421, S422, both `mined`), excluded 0; the staged ids were renumbered by document (S403 -> S421, S408 -> S422; the registry's next unused ids). Stop rationale: one theme per round, two entries. The staged `S390`, `S409` and `S410` Baidu rows belong to other themes and stay refused as staged (reasons in `corpus/lessons/round-57.md` § Gate).

## Rejects

(filled after wave 2 re-reads each reason against the page)

## Mistakes

(filled below)

## Trend inputs

(filled below)
