# Round 55 — kake (calibration: coverage-map index; freshness: Yahoo! JAPAN robots.txt assimilation)

lane: kake-shokunin · round 55 · base `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`
claims: C1 calibration (the README coverage map against the knowledge tree), C2 freshness (three
Yahoo! JAPAN robots.txt entries on rows opened or re-opened this round). Contract, frozen before any
data: `.ufo/waves/round-55/contract.md` (+ the appended counter-version-2 section).

## Gate

Rows opened this round. Unit rule: one unit per CJK character, one per non-CJK whitespace token; every
quote is at most 25 units, so the CORPUS.md ≤25-word ceiling holds under any word segmentation.

- S372 — https://info-search.yahoo.co.jp/archives/002849.php — accessed 2026-10-25 — § サイト単位、ディレクトリ単位での巡回の拒否設定 1 (更新日 2010年11月24日) — quote: "サイトに対する巡回の制限はないものとみなされます" (24 units; raw substring of the retained body, sha256 ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111, 10168 bytes, HTTP 200)
- S373 — https://info-search.yahoo.co.jp/archives/002850.php — accessed 2026-10-25 — § 「$」記号 → 注意 (更新日 2010年11月24日) — quote: "記述された文字列を含むURLがすべてマッチします。" (21 units; raw substring of the retained body, sha256 3173d9613128e1aaa7cb55919fa52438602095bd7bc54d4437760ee8b1c03885, 9402 bytes, HTTP 200)
- S418 — https://info-search.yahoo.co.jp/archives/002885.php — accessed 2026-10-25 — § robots.txtとは？ (更新日 2010年11月24日) — quote: "検索エンジンに対する要求を伝えるファイルです" (22 units; raw substring of the retained body, sha256 2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c, 7559 bytes, HTTP 200)

S372 and S373 are held rows (opened round 53); this round re-opened both against fresh GETs
(`w1/ScoutFreshS372.md`, `w1/ScoutFreshS373.md`: sha256 equal to the retained bodies, no drift). Their only
registry change is `used-by`, logged old→new below. S418 is the one new row (staged id S380).

## Registry changes (old → new)

| row | cell | old | new |
|---|---|---|---|
| S372 | used-by | `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` | + `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md` |
| S373 | used-by | `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md, corpus/knowledge/baidu-friendly-crawl-guidance.md` | + `corpus/knowledge/yahoo-japan-robots-pattern-syntax.md` |
| S418 | (new row) | — | `queued`→`mined` at append (status `mined`, opened 2026-10-25, recheck `180d`) |

Registry rows 155 → 156 (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`, 2026-10-25).

## Assimilation

Assimilation: one theme from `merge/kake/` (shokuknow, read-only) — Yahoo! JAPAN robots.txt — three entries
(`yahoo-japan-robots-txt-refusal-rules`, `yahoo-japan-robots-pattern-syntax`, `yahoo-japan-robots-txt-basics`), each
re-grounded in-round against a fresh retained body. Considerthese: proposal 4 of `considerthese/2026-10-25.md`
("Frontier ground map") implemented as a README section under the coverage map.

- Id lists: `assimilation/reg-ids` (155 ids) and `assimilation/staged-ids` (129 ids); collisions
  (`assimilation/collisions`, 0–3-space pattern): 8 — S312 S329 S367 S372 S373 S374 S390 S409. All eight are the same
  document in both registries (URL cells byte-equal, `w1/ExecIdGuard.md`), so none is renumbered: staged S372/S373 resolve
  to the lane's own S372/S373. Renumber map: staged S380 → lane S418 (the only adopted staged row the lane lacked; S380 itself
  does not collide, S418 continues the lane registry by document). Guard proof: a scratch registry with the indented row
  `  | S287 |` yields collisions `S287` with the 0–3-space pattern and 0 with a column-zero-only pattern
  (`assimilation/guard-proof/`); the guard stops at 3 leading spaces — a 4-space or tab-indented row is outside both the guard
  and the census (`w1/ExecIdGuard.md`).
- Normalization of the appended row: staged recheck `180d — curl -fsSL '…'…` → `180d`; the stripped prose (the grep recheck
  command and its printed count) is carried by each entry's own `recheck:` line; staged `opened 2026-10-24` → this round's
  2026-10-25; staged anchor `§ 本文（クローラーによる巡回時の robots.txt の参照手順）` refused — 0 hits in the body
  (`w1/ExecStagedQuoteAudit.md`) — replaced by the page's real heading `robots.txtとは？`; no cell holds a pipe.
- Staged quote ceiling: 6 of 6 staged quoted spans exceed 25 units (`w1/ExecStagedQuoteAudit.md`); none was carried — every
  quote in the three entries was re-cut and re-verified against the retained body.
- Quarantine slice (12 rows: S142 S143 S148 S156 S161 S193 S194 S195 S206 payload-absent; S154 S178 S184 unreachable):
  not adopted, not appended, not hand-checked this round — they stay quarantined.
- Not adopted this round (single-theme limit): the package's remaining 100 knowledge entries and 126 staged rows; no row
  is appended that no admitted entry cites (CORPUS.md rule 4).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| reference-drift | 21 of 46 `corpus/knowledge/` files were named by no row of the README coverage map across rounds 21–54 (`.ufo/waves/round-55/controls/base-c1-readme-index-v2.txt`, exit 1) | none | C1 counter + QUALITY round-55 criterion 1; red-before: base control exit 1, selftest 32 fixtures |
| vacuous | The version-1 counters met their frozen predicates under junk: one mega-row naming 46 files, a constant coverage cell, a skip-navigation string as every quote, an `[INFERENCE]` escape, a swapped retained body, a forged census receipt (`w1/CriticC1Contract.md` A1–A10, `w1/CriticC2Contract.md` A1–A8, `w1/MutC1Counter.md` 9 of 16 mutants survived) | none (version-1 selftests passed 10/10) | counter version 2 committed before any build, with the junk cases as selftest fixtures |
| landing | Round 54 ran one 33-seat v1 wave with no falsify wave (`corpus/lessons/round-54-verifier-spotcheck.md` routed defect 1) | PROTOCOL round-shape text only | this round runs W1 (build) and W2 (falsify) as two v1 waves |
| scope | The staged package's three entries could not land as written: every quoted span over the ceiling, a section label with 0 body hits, `source:` naming the pre-renumber id (`w1/ExecStagedQuoteAudit.md`) | none (the package's own gate recorded no unit ceiling) | re-cut quotes; C5 enforces the ceiling, the located heading and the row id |

## Trend inputs

expansion: three entries on per-engine crawl-hygiene ground held only as one rel=nofollow entry before (Yahoo! robots rules);
quality: the coverage map names 49 of 49 knowledge files at the final revision (C1 counter); discernment: the spot-check of
this round's admits and rejects belongs to the non-author closure (pending at filing).
