# Round 55 — kake (calibration: coverage-map index; freshness: Yahoo! JAPAN robots.txt assimilation)

lane: kake-shokunin · round 55 · base `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`
claims: C1 calibration (the README coverage map against the knowledge tree), C2 freshness (three
Yahoo! JAPAN robots.txt entries on rows opened or re-opened this round). Contract, frozen before any
data: `.ufo/waves/round-55/contract.md` (with its appended counter-version sections).
Round shape: two v1 waves — W1 build (40 seats) and W2 falsify (36 seats), 76 in total; the L1 holds
the canonical planner seat. Seat accounting: `.ufo/waves/round-55/settlement.md`.

## Gate

Rows opened this round. Unit rule: one unit per CJK character, one per non-CJK whitespace token; every
quote is at most 25 units, so the CORPUS.md ≤25-word ceiling holds under any word segmentation.

- S372 — https://info-search.yahoo.co.jp/archives/002849.php — accessed 2026-10-25 — § サイト単位、ディレクトリ単位での巡回の拒否設定 1 (更新日 2010年11月24日) — quote: "サイトに対する巡回の制限はないものとみなされます" (24 units; raw substring of the retained body, sha256 ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111, 10168 bytes, HTTP 200)
- S373 — https://info-search.yahoo.co.jp/archives/002850.php — accessed 2026-10-25 — § 「$」記号 → 注意 (更新日 2010年11月24日) — quote: "記述された文字列を含むURLがすべてマッチします。" (21 units; raw substring of the retained body, sha256 3173d9613128e1aaa7cb55919fa52438602095bd7bc54d4437760ee8b1c03885, 9402 bytes, HTTP 200)
- S418 — https://info-search.yahoo.co.jp/archives/002885.php — accessed 2026-10-25 — § robots.txtとは？ (更新日 2010年11月24日) — quote: "検索エンジンに対する要求を伝えるファイルです" (22 units; raw substring of the retained body, sha256 2b146a723e5d417de24f7bc64ad7adda4efbf9c6251438d89cfa88839d69312c, 7559 bytes, HTTP 200)

S372 and S373 are held rows (opened round 53); this round re-opened both with fresh GETs (`w1/ScoutFreshS372.md`,
`w1/ScoutFreshS373.md`, and again `w2/ExecReopenS372.md`, `w2/ExecReopenS373.md`): sha256 equal to the retained
bodies, no drift. S418 is the one new row (staged id S380; `w2/ExecReopenS418.md`: live GET equals the retained body).
These are the sourced claim's rows: C2 rests on S418 (opened this round) and on S372/S373 (re-opened this round).

Candidates considered, admitted, rejected:

- Admitted: the three entries `yahoo-japan-robots-txt-refusal-rules`, `yahoo-japan-robots-pattern-syntax`,
  `yahoo-japan-robots-txt-basics` (scope: `w1/ScoutScopeOverlap.md` — in scope as Frontier per-engine crawl-hygiene
  knowledge, narrowed by stated flip conditions; every quote re-cut to at most 25 units and re-verified).
- Refused on merit (author-side seat evidence, for the non-author spot-check; each keeps reason and flip):
  - staged `yahoo-japan-sitemap-constraints` (S382) — REJECT as staged (`w2/ScoutRejectSitemap.md`): one claim ("updated
    or new pages are crawled sooner") is on a sub-page, not the cited index page; the "one mechanism, the operator's own
    design" closure is an unmarked inference; one located span only. Flip: delete the clause or re-anchor to
    `archives/002859.php`/`002863.php`, tag the inference, carry 3+ located spans.
  - staged `yahoo-japan-crawler-identification-by-dns` (S386) — REJECT as staged (`w2/ScoutRejectDnsId.md`): the
    load-bearing DNS-versus-name mechanism is a fact about `archives/002855.php`, which the lane does not hold, not the
    cited index; "the lane already holds the ten pages in full" is false (4 of 10 rows held); S386 names no lane row.
    Flip: adopt 002855 as a lane row, cite it, withdraw the two unsupported assertions.
  - staged `yahoo-japan-user-agent-list-unreadable` (S364) — REJECT as staged (`w2/ScoutRejectUaList.md`): client-rendered
    body, only chrome quotable, unresolved S192/S193/S195/S200 premises. Flip: restate as a pinned measurement or
    re-ground on the server-rendered 002855 page with corrected citations.
  - staged section label `§ 本文（クローラーによる巡回時の robots.txt の参照手順）` for S418 — refused: 0 hits in the
    retained body (`w1/ExecStagedQuoteAudit.md`); replaced by the page's h2 `robots.txtとは？`.
- Spot-check: the non-author spot-check of these admits and rejects belongs to the closure; none is recorded here.

## Registry changes (old → new)

| row | cell | old | new |
|---|---|---|---|
| S372 | used-by | `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` | + `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md` |
| S373 | used-by | `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md, corpus/knowledge/baidu-friendly-crawl-guidance.md` | + `corpus/knowledge/yahoo-japan-robots-pattern-syntax.md` |
| S418 | (new row) | — | status `mined`, opened 2026-10-25, recheck `180d`, used-by `corpus/knowledge/yahoo-japan-robots-txt-basics.md` |

Registry rows 155 → 156 — `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
at base `fcaf4b85` and at the measured revision, 2026-10-25.

## Assimilation

Assimilation: one theme from `merge/kake/` (shokuknow, read-only) — Yahoo! JAPAN robots.txt — three entries, each
re-grounded in-round against a fresh retained body. Considerthese: proposal 4 of `considerthese/2026-10-25.md`
("Frontier ground map") implemented as a README section under the coverage map (proposal 3, a CJK locator sample, was not
taken; at most one per round).

- Id lists: `assimilation/reg-ids` (155 ids — `wc -l`) and `assimilation/staged-ids` (129 ids — `wc -l`); collisions
  (`assimilation/collisions`, 0–3-space pattern): 8 — S312 S329 S367 S372 S373 S374 S390 S409 (`wc -l`). All eight are
  the same document in both registries (URL cells byte-equal, `w1/ExecIdGuard.md`), so none is renumbered: staged S372 and
  S373 resolve to the lane's own S372 and S373. Renumber map: staged S380 → lane S418 (the only adopted staged row the lane
  lacked; S380 does not collide, S418 continues the lane registry by document). Guard proof: a scratch registry with the
  indented row `  | S287 |` yields collisions `S287` with the 0–3-space pattern and 0 with a column-zero-only pattern
  (`assimilation/guard-proof/`); the guard stops at 3 leading spaces — a 4-space or tab-indented row is outside both the
  guard and the census (`w1/ExecIdGuard.md`).
- Normalization of the appended row: staged recheck `180d — curl -fsSL '…'…` → `180d`; the stripped prose (the grep
  recheck command and its printed count) is carried by each entry's own `recheck:` line; staged `opened 2026-10-24` →
  2026-10-25; staged anchor refused (above) and replaced; no cell holds a pipe.
- Staged quote ceiling: the audit of the three staged entries found 3 of 3 quoted spans and 3 of 3 `recheck` grep strings
  over 25 units (`w1/ExecStagedQuoteAudit.md`, `SUMMARY spans=6 (quotes=3 recheck_greps=3)`); none was carried.
- Staged claims dropped or restored: `w2/RevengerStaged.md` tabulates 17 staged observations the landed entries omit
  (most dropped on purpose: unsupported by the page, over the ceiling, pre-renumber id, 2026-10-24 dates) and lists 5
  page-stated points as lost; all 5 were restored from the retained bodies in this round: the three S373 examples
  (`Allow: /*?$`, `Disallow: /*_print*.html`, `Disallow: /*?sessionid`), S418's third link, and the S372 case-rule subject.
- Quarantine slice (12 rows: S142 S143 S148 S156 S161 S193 S194 S195 S206 payload-absent; S154 S178 S184 unreachable —
  `wc -l assimilation/quarantine-slice`): not adopted, not appended, not hand-checked this round.
- Not adopted (single-theme limit): 101 of the package's 104 knowledge entries (`MERGE-REPORT.md` line 7 minus 3) and 126
  of its 129 staged rows; no row is appended that no admitted entry cites (CORPUS.md rule 4).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| reference-drift | 21 of 46 `corpus/knowledge/` files were named by no row of the README coverage map at the round base — `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision fcaf4b85…` → `unindexed=21`, exit 1, 2026-10-25 (a snapshot at the base, not a count over earlier rounds) | none | C1 counter + QUALITY round-55 criterion 1; red-before: `controls/base-c1-readme-index-v2.txt` exit 1 |
| vacuous | The version-1 counters met their frozen predicates under junk: one mega-row naming 46 files, a constant coverage cell, a skip-navigation string as every quote, an `[INFERENCE]` escape, a swapped retained body, a forged census receipt (`w1/CriticC1Contract.md` A1–A10, `w1/CriticC2Contract.md` A1c A2 A3 A4 A6 A7 A8 A9, `w1/MutC1Counter.md` 9 of 16 mutants survived the 10-fixture selftest); a second attack round on version 2 (`w2/CriticJunkC1.md`, `w2/CriticJunkC2.md`, `w2/MutC1V2Counter.md`) found 10 C1 junk variants and 8 C2 blind spots still passing | none (version-1 selftest passed 10/10) | counter versions 2 and 2.1, each junk case a selftest fixture; what stays outside any counter is named in the report (row truth and entry fidelity are reviewers' terms) |
| landing | Round 54 ran one 33-seat v1 wave with no falsify wave (`corpus/lessons/round-54-verifier-spotcheck.md` routed defect 1) | PROTOCOL round-shape text only | this round runs W1 (build) and W2 (falsify) as two v1 waves, 76 seats |
| scope | The staged package's three entries could not land as written: every quoted span over the ceiling, a section label with 0 body hits, `source:` naming the pre-renumber id (`w1/ExecStagedQuoteAudit.md`) | none (the package's own gate recorded no unit ceiling) | re-cut quotes; C5 enforces the ceiling, the located heading and the row id |
| attribution | Seat `ScribeQuality` (W1) returned a draft for another lane's round (round 45, criteria 85–86, a 1150-line QUALITY.md) and wrote no report in this lane (`w1-results.json`, `settlement.md`) | settlement check `w2/ExecSeatSettlement.md` | the draft was discarded; the QUALITY criteria were written by the L1 from this round's evidence; the dead report is recorded, not replaced |
| number-drift | This lesson's first draft stated a count of 100 remaining entries, "6 of 6" quoted spans, a 32-fixture selftest and "rounds 21–54" without commands (`w2/CriticClaimsAdmission.md`, `w2/ReviewerLessonGate.md`) | `corpus/knowledge/claim-count-derivation.md` (not followed while drafting) | numbers above carry commands and were re-derived at the measured revision; the contract's "before any build edit" was wrong by commit graph (version 2 landed with the build, before any measurement) and is corrected in `contract.md` |

## Trend inputs

expansion: three entries on per-engine crawl-hygiene ground that held only the rel=nofollow entry before; quality: the
coverage map names every knowledge file at the measured revision (C1 counter), and 7 executor row-checks found one stale
statement (`freshness-sidecar.json` line↔SHA correspondence, corrected) and 1 entry overread (S418 "per crawl", corrected);
discernment: the author-side seats' admits and rejects are listed above and await the non-author spot-check.
