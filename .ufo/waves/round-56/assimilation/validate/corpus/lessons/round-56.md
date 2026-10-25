# Round 56 — kake (calibration: SKILL.md registry self-test tallies; freshness: Yahoo! JAPAN crawl-handling assimilation)

lane: kake-shokunin · round 56 · base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`
claims: C1 calibration (the ten SKILL.md gate-registry rows that state a selftest tally, against what the documented
command prints), C2 freshness (three Yahoo! JAPAN crawl-handling entries on rows opened or re-opened this round). Contract,
frozen before any data: `.ufo/waves/round-56/contract.md` (with its appended counter-version sections). Round shape: two v1
waves, W1 build + pre-data attacks and W2 falsify; the L1 holds the canonical planner seat. Seat accounting:
`.ufo/waves/round-56/settlement.md`.

## Gate

Rows opened or re-opened this round. Unit rule (the counter's `units()`): one unit per kana/kanji/halfwidth-kana character,
one per non-CJK whitespace token; every quote below is at most 25 units under it, and at most 40 characters (version-2
character ceiling). The word-segmentation question of CORPUS.md rule 1 stays unresolved for older rows; new quotes avoid it.

- S367 — https://info-search.yahoo.co.jp/archives/002852.php — accessed 2026-10-25 — § リンク先のウェブページの巡回制限 ― ウェブページ内やサーバーでの設定 → メタタグを使用する方法 (更新日 2010年11月24日) — quote: "インデックスへの登録を許可する" (15 units; raw substring of the retained body, sha256 0188de9dae01e9088231098a9c6af3c8f5dc62a5982419a5f82fd98e86772a19, 8051 bytes, HTTP 200)
- S419 — https://info-search.yahoo.co.jp/archives/002856.php — accessed 2026-10-25 — § 削除したウェブページが巡回され続ける (更新日 2010年11月24日) — quote: "クローラーは削除されたウェブページと認識できず、" (23 units; raw substring of the retained body, sha256 6172d5d108d0c31d25244659516fc7fc81472c924ef35a51afc964cdd3a4a5c8, 7428 bytes, HTTP 200)
- S420 — https://info-search.yahoo.co.jp/archives/002857.php — accessed 2026-10-25 — § 存在しないウェブページが巡回される (更新日 2010年11月24日) — quote: "クローラーはエラーページとみなさず、" (17 units; raw substring of the retained body, sha256 a860d4f33181302d7ab467f5a0b21f2008916bb6dc6def69e69df5b54c630209, 7332 bytes, HTTP 200)

S367 is a held row (opened round 53, `used-by` extended only); this round re-opened it with a fresh GET equal to the round-53 body
(sha256 0188de9d…, `w1/ScoutFreshness.md`) and re-cut its overlong quote (31 units at round 53) into pieces of at most 24 units
inside the new entry. S419 and S420 are the two new rows (staged ids S375 and S376, renumbered by document). Page-printed
revision date of all three: 更新日 2010年11月24日; the site's own `robots.txt` (HTTP 200) does not mention `archives`.

Candidates considered, admitted, rejected:

- Admitted: `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md` (S367), `yahoo-japan-deleted-url-recrawl.md` (S419),
  `yahoo-japan-nonexistent-url-recrawl.md` (S420; the staged name `yahoo-japan-soft-404-recrawl` is not carried: the page never
  uses the words soft 404, so the term appears only as a tagged lane reading). Scope: `w1/ScoutScopeOverlap.md` — in scope as
  Frontier per-engine crawl hygiene, non-duplicative of the Google-side status entries, not tabi's client-side ground.
- Refused on merit or as staged (author-side seat evidence, for the non-author spot-check; each keeps reason and flip):
  - staged `yahoo-japan-canonical-notification` (S388, archives/003036.php) — REJECT as staged (`w1/ScoutRejectCanonical.md`):
    its `source:` section label does not occur in the body (0 hits), its only quote/recheck span is 98 units, one quoted span,
    S388 not in the lane registry, and "writing it once covers Google and Bing too" is an unsupported inference. Flip: a lane row
    for the page, the real h3 as locator, three page-unique spans of at most 25 units, the Google/Bing clause deleted or tagged.
  - staged `yahoo-japan-redirect-indexed-url` (S389, archives/002865.php) — REJECT as staged (`w1/ScoutRejectRedirect.md`):
    zero located quotes, the `本文（…）` wrapper of its label is not a heading in the body, one prose claim (the transfer rather
    than the crawler decides) contradicts the page, recheck grep string 84 units. No merit rejection of the page itself. Flip: seven
    fixes listed in the report plus a lane row.
  - staged `yahoo-japan-dynamic-page-indexing` (S387, archives/002867.php) — REJECT as staged (`w1/ScoutRejectDynamic.md`): zero
    quoted spans, a false statement that the lane holds the crawl-category page, an inference passed as operator wording. No merit
    rejection: the two operator statements are accurate and page-unique. Flip: a lane row, at least three page-unique quotes of
    at most 25 units, claims 5 and 7 corrected.
  - staged pre-renumber ids, `opened 2026-10-24` dates, the 46-unit (S375) and 29-unit (S376) quotes, the staged claim that a
    per-link-URL refusal is stated on the S367 page, and the staged S375/S376 "practical reading" prose — not carried
    (`w1/ScoutClaimsAudit.md`, `w1/ReviewerStaged.md`, `w1/ExecStagedQuoteAudit.md`).
- Spot-check: the non-author spot-check of these admits and rejects belongs to the closure; none is recorded here.

## Registry changes (old → new)

| row | cell | old | new |
|---|---|---|---|
| S367 | used-by | `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` | + `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md` |
| S419 | (new row) | — | status `mined`, opened 2026-10-25, recheck `180d`, used-by `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` |
| S420 | (new row) | — | status `mined`, opened 2026-10-25, recheck `180d`, used-by `corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` |

Registry rows 156 → 158 — `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at base
`e48354b7` and at the measured revision, 2026-10-25. `SKILL.md` gate-registry cells changed old → new are tabulated in
`.ufo/waves/round-56/w1/ScribeSkillRows.md` and recorded in LOG.md (seven Self-test cells).

## Assimilation

Assimilation: one theme from `merge/kake/` (shokuknow, read-only) — Yahoo! JAPAN crawl handling — three entries, each re-grounded
in-round against a fresh retained body. Considerthese: proposal 1 of `considerthese/2026-10-25.md` (landed-vs-claimed check)
implemented as `scripts/landed_check.py` with a selftest and run on the round-55 report (10 cited hashes, 10 ancestors of
`master`); proposals 2 and 3 were not taken (at most one per round).

- Id lists: `assimilation/reg-ids` (156 ids — `wc -l`) and `assimilation/staged-ids` (129 ids — `wc -l`); collisions
  (`assimilation/collisions`, 0–3-space pattern): 8 — S312 S329 S367 S372 S373 S374 S390 S409. All eight are the same document in
  both registries (`w1/ExecIdGuard.md` SAME-DOCUMENT TABLE), so none is renumbered; only S367 is adopted here and resolves to the lane's
  own S367. Renumber map: staged S375 → lane S419, staged S376 → lane S420 (neither collides; both continue the lane registry,
  whose max id was S418, by document); staged S367 → lane S367. Guard proof (`w1/ExecIdGuard.files/`): a scratch registry with the
  indented row `  | S287 | x |` yields `S287` with the 0–3-space pattern and nothing with a column-zero-only pattern; a 4-space row is outside
  both the guard and the census.
- Normalization of the appended rows: staged recheck `180d — curl …` → `180d`; the grep command each row's entry carries in its own
  `recheck:` line; staged `opened 2026-10-24` → 2026-10-25; the staged S367 section label (`サーバーで設定する方法` alone, 0 hits in the
  body as a whole label, `w1/ExecStagedQuoteAudit.md`) is replaced by the page's h2 plus both sub-headings, and the S375/S376 labels
  (3 raw hits each) are kept as the pages' own h2; no cell holds a pipe. Dry run before the append:
  `w1/ExecRowDryRun.md` (census exit 0, 158 rows, three deliberate breaks caught as E03/E01/E11).
- Quarantine slice (12 rows: S142 S143 S148 S156 S161 S193 S194 S195 S206 payload-absent; S154 S178 S184 unreachable —
  `wc -l assimilation/quarantine-slice`): not adopted, not appended, not hand-checked this round.
- Not adopted (single-theme limit): 101 of the package's 104 knowledge entries and 126 of its 129 staged rows; no row is appended that
  no admitted entry cites (CORPUS.md rule 4).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| number-drift | 7 of the 10 `SKILL.md` gate-registry rows that state a selftest tally disagreed with what their documented command prints at the round base (claimed 101/137/150/8/35/47 against observed 106/204/235/9/44/54; the r52 row's selftest printed 17/18) — `python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision e48354b7…` → `tally_mismatches=7`, exit 1, 2026-10-25 (a snapshot at the base, not a count over earlier rounds); the round-55 spot-check routed two of them (defect 1) | `corpus/knowledge/claim-count-derivation.md` (written for entry counts; not applied to registry rows, and the same class recurred inside round 55's own report) | C1 counter + QUALITY round-56 criterion 1; red-before: `controls/base-c1-selftally-v2.txt` exit 1; cells rewritten from the printed tallies |
| stale-premise | The r52 quote-truth selftest is documented as 18 fixtures with a passing receipt, but its fixtures rebuild from the checked-out `HEAD`; at the round base it prints 17/18 (C5: S374 quote edited after round 52; C8: registry grew) and passes only under the pin `KAKE_R52_SELFTEST_REV=1ae8de5d4dee` that the registry row never named (`w1/ExecPinProof.md`) | none | the row names the pin; the counter runs the documented command under a fixed environment, so a host-exported pin cannot rescue a row that omits it (selftest case `env_pin_removed`); QUALITY round-56 criterion 2 |
| vacuous | The version-1 C1 counter met its frozen predicate under a fake `python3 -c` command in the row (script blob untouched), a duplicate earlier row, a host-exported pin, two junk claims summing to the tally, and a rewritten helper beside the script (`w1/CriticC1Contract.md` A1–A9); six of 16 mutants survived its 20-check selftest (`w1/MutC1Counter.md`); the C2 counter at version 1 rejected a truthful build (7 of 8: the held S367 row's title is not a substring of the page) and accepted a 3-character body edit (`w1/CriticC2Contract.md` A1, WR-1) | QUALITY round-55 criterion "A counter is attacked before it scores" (it caught these: the attacks ran before any data) | counters version 2 (documented command pinned exactly, fixed environment, duplicate rows counted, helpers pinned, one claim per cell, rows_checked counts valid rows; C2: held-row body pinned by sha256, character ceiling 40, verified-at/recheck/kind/tier checks, staged name absence) |
| attribution | See `settlement.md` for any W1/W2 seat whose output named another lane or round; the misroot sweep result is recorded there | settlement check | seat output not used when it names another lane's evidence |

## Trend inputs

expansion: three entries on per-engine crawl-hygiene ground (server status answers and link-target refusal), each citing a `mined`
row (S367 re-opened, S419 and S420 new), on ground the coverage map did not hold for Yahoo! JAPAN; quality: the self-test tallies of ten
gates now equal what their commands print (C1 counter) and one selftest that rotted with the tree is pinned in its row; counters
attacked by 6 critic/reviewer/mutation seats before they scored; discernment: author-side admits and rejects listed above, the
non-author spot-check belongs to the closure.
