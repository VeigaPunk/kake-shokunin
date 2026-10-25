# ScoutSpotcheckPrep

Scope: a runnable non-author closure checklist for round 56 (kake), styled on `corpus/lessons/round-55-verifier-spotcheck.md`
(conformance table, claims re-check, discernment table, census). Everything below was *run by me* in `D=$(mktemp -d)` clone
checked out at the attacked tip `a450e43e696d032e3ac308383f6b3394e0c92860` (`git -C $D rev-parse --show-toplevel` = `$D`), 2026-10-25.
The lane's `master` = `origin/master` = `7ad7db5` (spec/dispatch commit, `git diff --stat a450e43 7ad7db5` = W2 spec files only), so the
report's *measured revision* is whatever the final commit names; the commands take `<rev>`; substitute it. Not run: anything needing the
network (see last section); C1 counter run exactly once (tip, 28 s wall on this host, not the 40-130 s the assignment warns of).

Setup (all steps): `L=/home/vgpnk/Projects/shokunin/kake-shokunin; B=e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6; T=<measured rev>;`
`D=$(mktemp -d) && git clone -q --no-checkout $L $D && git -C $D checkout -q $T && git -C $D rev-parse --show-toplevel` then `cd $D`.
At the tip as dispatched: `T=a450e43e696d032e3ac308383f6b3394e0c92860`. Never run in `$L`.

CHECKLIST:

1. Revision hygiene. `git -C $L merge-base --is-ancestor $B $T; echo $?` -> `0`; `git -C $L log --format='%an %H' -- .ufo/reports/round-56/kake.md`
   (fleet repo `/home/vgpnk/Projects/shokunin`, not the lane) -> author `kake-shokunin`. Proves the report landed under the lane identity and the
   measured revision descends from the frozen base. (Fleet report not present at my read: `ls /home/vgpnk/Projects/shokunin/.ufo/reports/round-56/` held
   kotoba/kotodama/kumitate only.)
2. C1 counter at tip (calibration). `python3 -B .ufo/waves/round-56/c56_selftally.py --root $D --revision $T; echo EXIT=$?`
   Observed at `a450e43`: `C1 selftest-tally tally_mismatches=0 rows_checked=10 met=True` + ten `OK` lines with claim = observed
   (45, 106, 204, 235, 23, 9, 19, 18, 44, 54), `EXIT=0`, 28 s. Proves the ten registry cells state what their documented commands print.
3. C1 counter at base (do-nothing control; do NOT rerun, read the committed receipt): `cat .ufo/waves/round-56/controls/base-c1-selftally-v2.txt`
   -> `tally_mismatches=7 rows_checked=10 met=False`, `EXIT=1`, revision `e48354b7…`; mismatches source-recheck 101/106, robots 137/204,
   sitemap 150/235, commit-citation 8/9, quote-truth-r52 18 claimed but `17/18` fails unpinned, readme-index 35/44, yahoo-robots-r55 47/54.
   Not re-run by me (the one-run cap): to re-measure, run the *tip* counter file with `--revision $B` (the counter file does not exist at base;
   the lane did the same), expect exit 1 with the same seven mismatches.
4. C2 counter at tip then base: `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root $D --revision $T; echo EXIT=$?` -> `C2 quote-truth 8/8
   met=True`, C1..C8 all PASS, `EXIT=0` (observed). Base: same command with `--revision $B` -> `0/8 met=False`, all eight FAIL (entries absent, no
   S419/S420 rows, S367 used-by lacks the new entry), exit 1 (matches `controls/base-c2-quote-truth.txt`). NOTE: pipe through `tee`, not `| head`
   — `echo EXIT=$?` after a pipe reports the pipe's last stage (I got a false `EXIT=0` at base that way; use `${PIPESTATUS[0]}`).
5. Counter selftests with their pins (all `cd $D`; observed at the tip):
   - C1: `python3 -B .ufo/waves/round-56/c56_selftally.py --selftest` -> `c56 selftally selftest: 47/47`, exit 0.
   - C2: `KAKE_R56_SELFTEST_REV=3691e9689a0358fc671d948d39dae3546ba5c01d python3 -B .ufo/waves/round-56/c56_quote_truth.py --selftest`
     -> `c56 quote-truth selftest: 67/67 (fixture revision 3691e9689a03)`, exit 0 (67 = 64 fixtures + 3 unit checks, per SKILL row 1254/contract).
   - Pin proof (r52 row): `KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` -> `18/18`, exit 0;
     WITHOUT the pin -> `17/18 (fixture revision a450e43e696d)`, exit 1 (FAIL `pass`, C5 on S374, C8 `158 != 145 + 3`). Proves the row must name the pin.
   - The other seven rows' selftests are run by step 2; to run one by hand take the command from its own `Self-test` cell
     (`awk -F'|' '$2 ~ /readme-index-counter/ {print $6}' SKILL.md`).
6. SKILL.md row tallies (the C1 population). Seven Self-test cells changed: `git diff -U0 $B $T -- SKILL.md | grep -E '^[-+]\| (source-recheck|robots-exp|sitemap-file|commit-cit|quote-truth-counter|readme-index|yahoo-robots)'`
   -> seven `-`/`+` pairs (`git diff --stat` = SKILL.md 34 lines); the three agreeing rows (base-path 45, redirect 23, wave-ledger 19) untouched.
   Cell values at tip (SKILL.md lines): 1067 `106`, 1093 `204`, 1128 `235`, 1199 `9/9`, 1216 `KAKE_R52_SELFTEST_REV=1ae8de5d4dee … 18`, 1233 `44`, 1234
   `KAKE_R55_SELFTEST_REV=64c0ce12ffe3… 54`. Out of scope and disclosed: the link-preview-audit row (45 dirs vs 46 cases), other prose mentions, helper files
   outside the pinned script's directory.
7. Registry 156 -> 158: `for r in $B $T; do git -C $D show $r:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'; done`
   -> `156` then `158` (observed). `diff <(git show $B:corpus/SOURCES.md) <(git show $T:corpus/SOURCES.md)` -> `157c157`, `164a165,166`: exactly S367
   changed, S419 and S420 added. Proves the append-only shape.
8. S367 cell-level diff (python, split rows on ` | ` over the 11 cells): only cell index 10 (`used-by`) differs; old
   `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`, new the same + `, corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md`
   (observed: `len 11 11, differing cells [10]`). Proves "S367 changed in used-by only". Also: S419/S420 rows are `docs | A`, status `mined`, opened
   `2026-10-25`, recheck `180d`, used-by their own entry, anchor `§ <h2> (更新日 2010年11月24日)`.
9. Retained bodies vs receipts: `sha256sum .ufo/waves/round-56/sources/S{367,419,420}.html` -> `0188de9d…`, `6172d5d1…`, `a860d4f3…` equal to
   `receipts.json` (bytes 8051/7428/7332); S367 equals the round-53 body. (Observed; also S388 `115b4353…` 9681, S389 `ef304c4d…` 6440, S387 `0a954ff0…` 6272 for
   the rejects.) Live re-fetch is the only network step (below).
10. The three entries' quotes (offline, against retained bodies; NB `span_tools.py` hardcodes `SRC=` to the lane's `sources/` dir, not the clone's, so after a later commit re-point `SRC` or use `grep` on `$D/.ufo/waves/round-56/sources/`):
    `python3 -B .ufo/waves/round-56/span_tools.py check S419 'クローラーは削除されたウェブページと認識できず、'` -> `units 23, raw_substring True, in_content True,
    count_in_page 1`; S367 `インデックスへの登録を許可する` -> 15 units, count 1; S420 `クローラーはエラーページとみなさず、` -> 17 units, count 1.
    `grep -F -c` of each entry's own `recheck:` string against `sources/<id>.html` -> `1` each (S367 `サーバーの設定で指定する方法があります`). Then, per entry,
    spot-read two or three `> "…"` blocks: `python3 -B .ufo/waves/round-56/span_tools.py window S367` prints the article text; the entry's locator must name
    its heading (S367 h2 `リンク先のウェブページの巡回制限 ― ウェブページ内やサーバーでの設定` → `メタタグを使用する方法`/`サーバーで設定する方法`; S419 h2 `削除した
    ウェブページが巡回され続ける`; S420 h2 `存在しないウェブページが巡回される`). Caveat: S367 meta-tag lines with raw `"` cannot be quoted whole (contract); the entry
    quotes the `&quot;`-bearing span `rel=&quot;nofollow&quot;属性を使った指定方法` verbatim as HTML entities.
11. Ceilings (25 units / 40 chars): the Gate quotes are 15/23/17 units (observed above). For the entry blocks: C5 of the counter enforces both ceilings
    (passes 8/8); a non-author hand check: a short python snippet importing `span_tools.units` over every `^> "…"` line of the three entries (the counter's `units()` is
    the same function).
12. Entry headers and README rows: first lines `source:`/`verified-at: 2026-10-25`/`recheck: 180d — \`curl … | grep -F -c '…'\` -> 1` are on every entry (observed
    line 1-3 in all three); `corpus/README.md` has 2 matching rows per entry (coverage map + ground map); `python3 -B .ufo/waves/round-55/c55_readme_index.py --root $D --revision $T`
    -> `index_mismatches=0 knowledge_files=52 met=True coverage_rows=54` (52 = 49 + 3). Proves nothing new is unindexed.
13. Census before/after. Before = committed `.ufo/waves/round-56/controls/census-before.txt` (14 `W04 duplicate url` + final `ok …/corpus/SOURCES.md` + `EXIT=0`).
    After (run by me, tip): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate $D; echo EXIT=$?` -> same 14 W04 lines, final `ok $D/corpus/SOURCES.md`, exit 0.
    `…/sources-census.sh census $D | head -7` -> `rows 158 / tier.A 135 / tier.B 6 / tier.C 17 / status.mined 128 / queued 8 / rejected 22`; at `$B` -> `rows 156 / tier.A 133`
    (so +2 rows, +2 tier-A, +2 mined). WARNING: the round-55 form `--root <fleet> kake` resolves the *fleet* lane, not the clone; with `--root $D kake` it errors
    (`config not found … shokunin.conf`, exit 2). Use the explicit-directory form above, or `--file $D/corpus/SOURCES.md` as `validate_append.sh` does.
    The committed C7 receipt `.ufo/waves/round-56/assimilation/validate/census-exit.txt` = `exit=0`. Note: no `controls/census-after.txt` exists at `a450e43`; the L1 must commit one, or the verifier cites its own run. Census passing at base is a no-harm check, not part of C2 (contract §After-state correction).
14. `landed_check` on the final report. Tool selftest: `python3 -B scripts/landed_check.py --selftest` -> `selftest 14/14`, exit 0 (observed).
    Previous-round use (observed, exit 0): `python3 -B scripts/landed_check.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-55/kake.md --repo $L --branch master`
    -> `cited=10 landed=10 missing=0 unknown=0` (3 digest tokens suppressed). On the final report: same command with `…/round-56/kake.md` -> expect `missing=0 unknown=0`,
    exit 0; exit 1 = a cited commit is not an ancestor of `master` (check BEFORE the last amend/rebase), exit 2 = unevaluable. Fleet-repo hashes cited in the report (e.g. the
    report's own landing commit) resolve to UNKNOWN in the lane repo and count against `unknown`; a lane-only hash list is what round 55 used.
    On the lane lesson: `--report corpus/lessons/round-56.md --repo $D --branch HEAD` -> `cited=2 landed=2 missing=0 unknown=0` (observed).
15. Lane state (round-55 style): `git -C $L status --porcelain` empty and `git -C $L ls-remote origin refs/heads/master` equals the report's tip; fleet watchdog digest
    for the launch/complete pair is not in the lane (cite from the fleet if present).
16. Defect hunt the previous closure found (so repeat it): number drift between lesson/report/SKILL and a re-derived count. Derive, don't copy: counter lines come from steps 2/4/5; the S389 figure below.
    Observed drift (informational, not a gate): `corpus/lessons/round-56.md` Gate says the S389 staged recheck string is **90 units**, as does `w1/ScoutRejectRedirect.md`;
    `span_tools.units` and `c56_quote_truth.units` both give **84** (92 characters) on the staged file's `grep -F -c '…'` string — still ≫ 25 so the reject stands, but cite 84.

ADMIT/REJECT TABLE:

Method: `L/…/w1/` reports are the author-side evidence; the closure re-opens the retained body and the staged file (`K=/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/`, read-only).
Where the reason lives: `corpus/lessons/round-56.md` § Gate ("Candidates considered, admitted, rejected", with reason + flip each) and the seat report named.

| Item | Decision | Reason lives in | Offline re-check (observed) | Live re-open (not run) |
|---|---|---|---|---|
| ADMIT `yahoo-japan-link-target-crawl-restriction` (S367, held row re-opened) | admit | lesson § Gate S367 line; `w1/ScoutFreshness.md` (fresh GET = round-53 body); `w1/EntryLinkTarget.md` | body sha `0188de9d…` 8051 B = receipt; gate quote `インデックスへの登録を許可する` 15 u, count 1; row diff = `used-by` only | `curl https://info-search.yahoo.co.jp/archives/002852.php \| sha256sum` must equal `0188de9d…` |
| ADMIT `yahoo-japan-deleted-url-recrawl` (S419, new row) | admit | lesson § Gate S419; `w1/EntryDeletedUrl.md` | sha `6172d5d1…` 7428 B; `クローラーは削除されたウェブページと認識できず、` 23 u, count 1; the page says 可能性があります (possibility) — entry heading says "possibility rather than a certainty" | `…/archives/002856.php` |
| ADMIT `yahoo-japan-nonexistent-url-recrawl` (S420, staged name `…soft-404-recrawl` dropped) | admit | lesson § Gate S420 + the name note (page never says soft 404; term only as tagged lane reading); `w1/EntryNonexistentUrl.md` | sha `a860d4f3…` 7332 B; `クローラーはエラーページとみなさず、` 17 u, count 1; `grep -c 'soft' corpus/knowledge/yahoo-japan-nonexistent-url-recrawl.md` to confirm the term is tagged | `…/archives/002857.php` |
| REJECT staged `yahoo-japan-canonical-notification` (S388, `archives/003036.php`) | reject as staged | lesson § Gate S388 bullet; `w1/ScoutRejectCanonical.md` (§ DECISION, flip) | label `本文（内容が重複する複数のURLをまとめる方法）` 0 hits in `sources/S388.html` (real h3 is `<link rel="canonical" href="">の記述方法と機能`); staged file has 0 `> "` spans; recheck string **98 units**; `S388` absent from `corpus/SOURCES.md` (0 rows); "covers Google and Bing too" is inference (page says shared 規格/format only) | `curl …/archives/003036.php` sha `115b4353…` 9681 B |
| REJECT staged `yahoo-japan-redirect-indexed-url` (S389, `archives/002865.php`) | reject as staged | lesson § Gate S389 bullet; `w1/ScoutRejectRedirect.md` | label `本文（リダイレクトの設定とインデックスに登録されるURL）` 0 hits in `S389.html` (real h2 `リダイレクトの設定とインデックスに登録されるURL`); 0 quoted spans; claim "the transfer decides" contradicts the page; recheck string 84 u (lesson/report say 90); no S389 row | `…/archives/002865.php` sha `ef304c4d…` 6440 B |
| REJECT staged `yahoo-japan-dynamic-page-indexing` (S387, `archives/002867.php`) | reject as staged | lesson § Gate S387 bullet; `w1/ScoutRejectDynamic.md` (§ DECISION, claim 7) | label `本文（動的に生成されるウェブページのインデックス）` 0 hits in `S387.html`; 0 quoted spans; `grep -c 002854 corpus/SOURCES.md` = **0** (so "the lane holds the crawl-category page" is false); recheck string 63 u; no S387 row; no merit rejection of the page | `…/archives/002867.php` sha `0a954ff0…` 6272 B |

Offline commands (observed; run from `$D`, `S=.ufo/waves/round-56/sources`): `grep -o -F -- '<label>' $S/S388.html | wc -l` -> 0 (same for 389 and 387);
`grep -cE '^ {0,3}\|[[:space:]]*S(387|388|389)[[:space:]]*\|' corpus/SOURCES.md` -> 0; `grep -c '^> "' $K/yahoo-japan-{canonical-notification,redirect-indexed-url,dynamic-page-indexing}.md` -> 0 each.
The discernment criterion: admit iff every quote is a raw page-unique substring ≤25 u under a located heading and the row is registered; reject iff the locator is false, the quote
count is 0/1, or a claim exceeds the page. Note S387/S388/S389 are rejected *as staged*, with a flip each; two of the three (S387, S389) have "no merit rejection of the page".
Suggested minimum spot-check (≥1 admit + ≥1 reject, matching round 55): re-open S419 live and S388 body; add S387's `002854` grep (the one reject reason that rests on the lane registry rather than a page).

COMMANDS NOT RUNNABLE OFFLINE:

- Live page re-fetch for the six pages (needs network, UA `kake-shokunin-round56`-style GET): `curl -fsSL https://info-search.yahoo.co.jp/archives/00{2852,2856,2857,3036,2865,2867}.php | sha256sum`
  to compare with `receipts.json`; the entry `recheck:` lines `curl -fsSL '<url>' | grep -F -c '<string>'` -> 1 for each of the three entries. Not run by me (no network use in this seat).
- `python3 -B scripts/source_recheck.py` against live pages (rechecks of rows older than `180d`; none due at 2026-10-25 — all three new rows opened today).
- The fleet report and watchdog digest: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-56/kake.md` did not exist at my read; `landed_check` on it, the fleet-commit author check (step 1) and
  the digest comparison run only after the report lands. `git ls-remote origin` needs the remote reachable (I used local refs; `origin/master` = `7ad7db5` locally).
- Closure of the `jj-lane.sh state` check needs the lane's jj workspace; the lane is detached (`git branch` shows `(no branch)`), read it in the lane, never mutate.
- `sudo`/pacman: nothing installed or upgraded; all tools already present.

VERDICT: closure checklist ready — both counters re-measured at a450e43 (C1 0/10 mismatches, 10 rows; C2 8/8), registry 156→158 with S367 diffed used-by-only, selftests 47/47 + 67/67 + r52 pin proof, census exit 0 with the same 14 W04, landed_check selftest 14/14; one drift found (S389 recheck string 84 units, lesson says 90).
