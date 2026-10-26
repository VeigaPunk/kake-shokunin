# Round 56 — verifier spot-check (kake)

author: hyaku closure (non-author integrator, @m_sonnet)
date: 2026-10-25 · lane `kake-shokunin` · lane-round 56 · base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6` · tip `413c3b4a5eb52202ae20fc7212ceaf87a75f613d`
driver digest (`.ufo/watchdog.log`, mutable): `2026-10-25T18:56:32-03:00 launch kake round=56 pgid=85773 driver=hyaku-inline attempt=1` ·
`2026-10-25T20:28:53-03:00 complete kake round=56; hyaku-inline attempt=1`.
Method: plain measurements over committed bytes plus live GETs. No lane gate or selftest was executed (PROTOCOL §Gate standard, Closure
consequence); lane-owned gate claims are marked *evidence-verified*, plain re-counts *re-measured*.

## 1. Step-1 conformance

| check | command / observation | result |
|---|---|---|
| report filed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-56/kake.md` | `kake-shokunin 9732bd29…` (final tip) and `kake-shokunin 2fe0478c…` — landed by the lane |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` → 1; `grep -c '^- \[' SHONEN.md` → 4; report has 4 lines, all `[ ]` | conformant |
| cited lane commits exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for `2d308e808bfd 6b3df99d694f d5afc48acd72 3691e9689a03 a450e43e696d 7ad7db51dfcf f8438a282d59 4cb225fb032b ad06cb8a17bd 413c3b4a5eb5` | 10 of 10 `ok` |
| pushed, no leftovers | `jj-lane.sh state` → `ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty; `rev-parse HEAD` = `413c3b4a…` = remote | clean |
| prompt carries the template contract | `.ufo/prompts/kake-round-56.md` (545 lines): axes binding §1, claims §2, frontier §2b, L2 floor §3, report §4 (SHONEN, commit-hash rule), commit/push scope/L0 §5, write scope item 3 | present |
| marker vs report | real report: work, 10 landed commits tied to LOG entries, before→after tables | status `ok` |

Conformance defects (status-neutral): none beyond those in §5.

## 2. Claims

### C1 calibration — ten SKILL.md registry rows state the tally their selftest prints (7 → 0)

Re-measured (plain):
- Base claims, `git show e48354b7:SKILL.md | grep -oE …`: source-recheck 101, robots 137, sitemap 150, citation-lint 8/8, readme-index 35, yahoo-robots
  47, plus the r52 quote-truth row (18, documented without its pin). Tip: 106, 204, 235, 9/9, 44, 54, and the r52 row names
  `KAKE_R52_SELFTEST_REV=1ae8de5d4dee`. The three unchanged rows (base-path 45, redirect 23, ledger 19) were already right.
- The ten tools are byte-unchanged: `git diff --quiet e48354b7 413c3b4a -- scripts/{citation_lint,source_recheck,robots_audit,sitemap_audit,redirect_audit,base_path_audit}.py .ufo/waves/round-52 .ufo/waves/round-55` → exit 0.
- Committed receipts that predate the round agree with the new tallies: `git grep` finds `"passedOverTotal": "106/106"` (round-39 `recheck-selftest-after.txt`),
  `204/204` (round-39 `robots-selftest-after.txt`), `PASS 235/235` (round-42 `selftest-build-py310.txt`), `selftest: 23/23 passed` (round-47), `44/44`
  (round-55 `c1-selftest-v2.txt`), `54/54` (round-55 `c2-selftest.txt`), `19/19` (round-52), `18/18` pinned (round-52).
- The ten cells did not change after the counter run under attack: `git diff a450e43e 413c3b4a -- SKILL.md` touches only the freshness-sweep row, one citing-set sentence and the two
  round-56 registry rows.

Evidence-verified (not executed): `controls/base-c1-selftally-v2.txt` (`tally_mismatches=7 rows_checked=10 met=False`, exit 1, revision `e48354b7`),
`controls/after-c1-selftally.txt` (`0 / 10 met=True`, exit 0), `controls/c1-selftest.txt` (`59/59`), and `w2/ExecRunC1.md` (hand-run documented commands, 10 of 10 agree,
base byte-identical to the control). Verdict: **verified**.

### C2 freshness (sourced) — three Yahoo! JAPAN crawl-handling entries on opened/re-opened rows (0/8 → 8/8)

Re-measured (plain):
- Registry rows: `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → base 156, tip 158; S419 and S420 present as `mined`, opened 2026-10-25, used-by their entries.
- Knowledge files 46 → 49 md (49 → 52 files incl. json; README map names 49 → 52). No file at base cited `00285[67].php` (0); the tip has 2 (new ground).
- Live re-open today (`curl -sL`, HTTP 200): `archives/002852.php` 8051 bytes sha256 `0188de9d…86772a19`, `002856.php` 7428 bytes `6172d5d1…cdd3a4a5c8`, `002857.php` 7332 bytes `a860d4f3…4c630209`
  — all three equal the sha256 values the lesson records (no drift). `robots.txt` (200) has no `archives` rule.
- Each Gate quote occurs exactly once in its page and in no sibling page (`grep -o … | wc -l`): `インデックスへの登録を許可する` 1 (002852), `クローラーは削除されたウェブページと認識できず、` 1 (002856),
  `クローラーはエラーページとみなさず、` 1 (002857); the page never says soft 404 (`grep -ioE 'soft ?404|ソフト ?404'` → 0), so the staged name rename is correct.
- The S419 entry's rendering (hedge 可能性があります, 確認してください vs 設定を行ってください, unnamed meta tag) matches the page text read line by line.
- Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, only the 14 W04 duplicate-url notes (same S033…S417 ids as the lane's `census-before.txt`).

Evidence-verified (not executed): `controls/after-c2-quote-truth.txt` (8/8, exit 0), `base-c2-quote-truth.txt` (0/8, exit 1), `controls/c2-selftest.txt` (86/86 at the tip).
Limit the lane itself states and I confirm: the counter certifies quote literals, not support; it has no drift condition. Verdict: **verified**; the freshness content is the re-open of S367/S419/S420, which I reproduced.

No exploratory claim; no claim relied on my judgment of taste.

## 3. Axis verdicts

| axis | verdict | basis |
|---|---|---|
| calibration | improved | C1 verified, 7 mismatches → 0 on a registry whose cells are self-assessment of selftest state; score stays 1/10, no inflation. Axis ownership (calibration vs operability, `CriticAxisClaim`) is left to the operator: the move is real either way |
| freshness | improved | C2 verified; held row S367 re-opened and the two new rows opened, bodies hash-equal to retained today; modest because the counter has no drift condition |
| operability | unchanged | 10/10 untouched; a selftest-tally gate and `landed_check.py` entered the capability table, not scored |
| coverage | improved | 46 → 49 knowledge md files on Yahoo! JAPAN status-answer ground; not a declared claim, reported as side effect |
| depth, adjacency | unchanged | no change |

`git diff e48354b7 413c3b4a -- SCORECARD.md` = 28 insertions, 0 deletions: no score was lowered or rewritten. **No axis harmed.**

## 4. Discernment spot-check

| item · decision | re-opened source | agree/disagree | reason |
|---|---|---|---|
| S419 deleted-URL entry · admit | `archives/002856.php` live GET, sha256 equal to lesson | agree | quote occurs once; 可能性があります and the 確認 vs 設定 split are on the page; entry's page-silence sweeps hold (no noindex/redirect/rate text in the article) |
| S420 non-existent-URL entry · admit | `archives/002857.php` live GET | agree | quote once; page says "エラーページとみなさず、巡回を続けます", no "soft 404" wording, so the staged soft-404 name is rightly dropped |
| S367 link-target entry · admit (re-open) | `archives/002852.php` live GET, sha256 = round-53 body | agree | held row; quote once; re-cut quotes are in the retained body |
| S388 canonical-notification · reject as staged | `archives/003036.php` + staged file `shokuknow/merge/kake/knowledge/corpus/knowledge/yahoo-japan-canonical-notification.md` | agree on decision, disagree with one reason | the staged `§ 本文（…）` label occurs 0 times in the body (confirmed) and the quote is one long span; but the page does say (line 23) "この記述は、Yahoo!検索だけでなくGoogle、Bingの検索エンジンにも共通の規格です", so the lane's "unsupported inference" overstates: the page supports "shared specification", only "covers" is the extension. The flip should say "tag as a shared spec", not delete the clause |
| S389 redirect-indexed-url · reject as staged | `archives/002865.php` + staged file | agree | page: "クローラーは、次のステータスコードをもとに…判定します" (crawler decides by status code) contradicts staged "the transfer decides for itself"; `本文（リダイレクトの設定…）` label occurs 0 times |
| S387 dynamic-page-indexing · reject as staged | `archives/002867.php` live GET (HTTP 200, 6272 bytes) + staged file | agree | staged file has no quoted span (`grep -c '"'` → 1, the frontmatter command only); its "A dynamic page needs a static path into it … the operator's own wording rather than an inference" is the lane's reading, while the page (002867) says only that the crawler mostly follows static links and that dynamic pages can be indexed; the page's two statements are accurate, so no merit rejection, as the lane says |

New SOURCES row check: S419/S420 rows (`git show 413c3b4a:corpus/SOURCES.md`) carry anchor `§ <page h2> (更新日 2010年11月24日)` and teaches cells without a quote; the ≤25-unit quote lives in the lesson Gate
(S419 23 units, S420 17 units by the lane's unit rule, 1 Japanese span of 23/17 CJK characters, ≤ 25 words under any counting) and is located in the pages as above.

Discernment verdict: **improved** — the spot-check agrees with the gate on 3 admits and 3 rejects; the one reasoning disagreement (S388 Google/Bing clause) is routed below as a lesson-to-be, not left silent.

## 5. Trends

- expansion: **improved** — three entries on ground the map did not hold (0 prior files citing 002856/002857), each citing a `mined` row; map 49 → 52.
- quality: **improved** — ten tallies equal the printed ones; the stale r52 pin is documented; S367 re-verified. Bounded as the lane says: entry fidelity is reviewer-evidenced, not counter-proved.
- discernment: **improved** — 6 of 6 decisions agree (see §4).

## 6. Defects routed to the lane (status-neutral)

1. **Receipt relabel without re-run evidence.** `controls/after-c1-selftally.txt` and `after-c2-quote-truth.txt` were committed in `4cb225f` with `revision: f8438a282d59…`; `ad06cb8`
   edited that line to `4cb225fb…` (`@R@` placeholders in LOG/SCORECARD likewise), and `c2-selftest.txt` read `67/67` at the "measured content commit" `4cb225fb`
   (fixed to `86/86` only in `ad06cb8`). `c56_quote_truth.py` and one SKILL pin changed between `f8438a28` and `4cb225fb`. The report's "After (`4cb225fb`)" column is therefore not a run over
   that revision. Next round: re-run both counters at the revision named and commit the unedited outputs. My plain re-counts above hold at the tip, so this does not move the verdicts.
2. **S388 reject reason.** State what the page does say (shared specification for Yahoo!, Google and Bing) when writing the flip; add to QUALITY a falsifier "a rejection reason is re-read against the page before it is logged".
3. **Disclosed limits stand:** C1 pins ten rows only (two further stale tallies corrected unclaimed, 8 mentions unmeasured); `used-by` of five reused held rows not extended; quarantine slice (12 rows) not hand-checked.
4. **SHONEN promotion:** all four boxes are `[ ]` and several remain untouched (e.g. an end-to-end task logged); nothing here is fully checkable by a non-author — no operator promotion note.
