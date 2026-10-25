# ExecLessonNumbers

Number audit of `corpus/lessons/round-56.md`, `PROVINCE.md` §Round-56 (`408-426`) and the round-56 edits in
`corpus/README.md`, against the number-drift class doc `corpus/knowledge/claim-count-derivation.md`.

Method: every number re-derived from the revision under attack `a450e43` (`git show a450e43:<path>`) or from base
`e48354b7` where the claim is about base; counters ran only inside `D=$(mktemp -d)` clone
(`git clone -q --no-checkout <lane> "$D" && git -C "$D" checkout -q <rev>`, `git -C "$D" rev-parse --show-toplevel`
== `$D`), using the counter blobs committed at `a450e43` (`c56_selftally.py` sha256 `591d2701…dda1d5dc1`,
`c56_quote_truth.py` `e874e300…2e2b37196`). Lane writes: this report only; no git/jj mutation; no tool installs.

Lane moved during the audit: HEAD `a450e43` → `7ad7db5` (19:52:22) → `f8438a2` (20:13:07, "wave-2 repairs …
C1 counter v2.1 …"). `corpus/README.md`, `settlement.md`, `LOG.md` and the w1 reports cited here are byte-identical
at `a450e43` and `f8438a2`; `PROVINCE.md` §Round-56 wording changed with no number change; `SKILL.md` tallies and the
lesson's S389 line changed (finding 1). Numbers below are the `a450e43` text unless a row says otherwise.

## NUMBER TABLE:

| # | claim (site) | command | measured | verdict |
|---|---|---|---|---|
| 1 | lesson:89 `7 of the 10` tally rows false at base | `python3 -B .ufo/waves/round-56/c56_selftally.py --root $D --revision e48354b7…` | `tally_mismatches=7 rows_checked=10 met=False`, EXIT=1 | agree |
| 2 | lesson:89 claimed `101/137/150/8/35/47` vs observed `106/204/235/9/44/54` | same run, per-row lines | source-recheck 101/106, robots 137/204, sitemap 150/235, commit-citation 8/9, readme-index 35/44, yahoo-robots 47/54 | agree |
| 3 | lesson:96-98 "the self-test tallies of ten gates now equal what their commands print" | same counter, `--revision a450e43…` | `tally_mismatches=0 rows_checked=10 met=True`, EXIT=0 (all ten `claim == observed`) | agree |
| 4 | lesson:90 r52 selftest prints `17/18` at base | in `$D`@`e48354b7`: `env -u KAKE_R52_SELFTEST_REV python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` | `17/18 (fixture revision e48354b7c26b)`, exit 1; FAIL lines name C5 S374 quote and C8 `156 != 145 + 3` | agree |
| 5 | lesson:90 same selftest passes only under pin `1ae8de5d4dee` | `KAKE_R52_SELFTEST_REV=1ae8de5d4dee … --selftest` | `18/18`, exit 0 | agree |
| 6 | C2 base `0/8` → after `8/8` (contract §C2) | `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root $D --revision e48354b7…` then `--revision a450e43…` | `0/8 met=False` EXIT=1 (all C1–C8 FAIL); `8/8 met=True` EXIT=0 (C1–C8 PASS) | agree |
| 7 | lesson:91 "six of 16 mutants survived its 20-check selftest" | `w1/MutC1Counter.md:5,6,85` | baseline `20/20`; "16 mutants run"; "10 killed, 6 survived" | agree |
| 8 | lesson:91 `A1–A9` attack ids | `grep -oE '\bA[0-9]+\b' w1/CriticC1Contract.md \| sort -u -V` | `A1 A2 A3 A4 A5 A6 A7 A8 A9 A10` | **disagree** (10, see D2) |
| 9 | lesson:91 C2 v1 "7 of 8" and "3-character body edit" | `w1/CriticC2Contract.md:19-20,28,154` | "7/8", "3-character edit … 3 chars net" (report text; v1 counter not re-run) | agree (text) |
| 10 | lesson:99 "6 critic/reviewer/mutation seats" | `w1-results.json` `agent` field + `settlement.md:5-7` | 7 attack seats (see D3) | **disagree** |
| 11 | lesson:16-18 Gate unit counts `15 / 23 / 17` | `python3 -B .ufo/waves/round-56/span_tools.py check S367 'インデックスへの登録を許可する'` (and S419, S420 quotes) | `units: 15 / 23 / 17`, `raw_substring True`, `in_content True`, `count_in_page 1` | agree |
| 12 | lesson:13-14 "at most 40 characters" | `len(q)` on the three Gate quotes | 15 / 24 / 18 chars | agree |
| 13 | lesson:12-13 unit rule (`units()`) | `span_tools.py:16-18`, `c56_quote_truth.py:160-162` | identical rule (CJK char + non-CJK whitespace token) | agree |
| 14 | lesson:21 round-53 S367 quote `31 units` | `units()` on `.ufo/waves/round-53/sources/gate-draft.md:15` quote | 31 units, raw substring of S367 body | agree |
| 15 | lesson:21-22 re-cut to pieces "at most 24 units" | 41 `> "…"` block quotes in the three entries; max `units()` | S367 max 24 (17 quotes), S419 max 23 (12), S420 max 24 (12); max chars 37; 0 non-substrings | agree |
| 16 | lesson:44 staged S375 quote `46 units`, S376 `29 units` | `units()` on the `grep -F -c '…'` strings of `SOURCES.append.md:95,96` | 46 units (47 chars), 29 units (47 chars), both raw, count 1 | agree |
| 17 | lesson:33 S388 recheck span `98 units` | `units()` on `SOURCES.append.md:108` string | 98 units (102 chars), raw, count 1 | agree |
| 18 | lesson:38 S389 recheck `90 units` | `units()` on `SOURCES.append.md:109` string | **84 units** (92 chars), raw, count 1 | **disagree** (D1) |
| 19 | lesson:16-18 sha256 + bytes + HTTP for S367/S419/S420 | `sha256sum`/`stat -c %s` on `.ufo/waves/round-56/sources/*.html` + `receipts.json` | `0188de9d…72a19` 8051; `6172d5d1…a5c8` 7428; `a860d4f3…209` 7332; `httpStatus 200` all; bytes/sha equal receipts | agree |
| 20 | lesson:23 "all three print 更新日 2010年11月24日" | `grep -o -F '更新日 2010年11月24日' <body> \| wc -l` | 1 / 1 / 1 | agree |
| 21 | lesson:33 S388 `source:` label "0 hits" | `body.count('本文（内容が重複する複数のURLをまとめる方法）')` and heading-only form | 0 and 0 | agree |
| 22 | lesson:77 S375/S376 labels "3 raw hits each" | `body.count('削除したウェブページが巡回され続ける')` / `'存在しないウェブページが巡回される'` | 3 / 3 | agree |
| 23 | lesson:76-77 S367 staged label "0 hits in the body as a whole label" | `S367.html.count('サーバーで設定する方法')`; composite `h2 → h3` label | bare string **1** (a real `<h3>` at 3194); composite label 0 | **disagree** (D4) |
| 24 | lesson:23 "site's own `robots.txt` (HTTP 200) does not mention `archives`" | none | not retained in `.ufo/waves/round-56/` (no receipt, network claim) | **unrun** |
| 25 | lesson:57 registry rows `156 → 158` | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | 156 (`e48354b7`), 158 (`a450e43`), 158 (`f8438a2`) | agree |
| 26 | lesson:53 S367 changes in `used-by` only | cell-wise diff of the S367 row, `e48354b7` vs `a450e43` | 11 cells, only cell 10 differs (prior path + `…/yahoo-japan-link-target-crawl-restriction.md`) | agree |
| 27 | lesson:54-55 S419/S420 `mined`, `2026-10-25`, `180d` | 11-cell split of both rows at `a450e43` and `f8438a2` | cells 7/8/9 = `mined` / `2026-10-25` / `180d`; 11 cells, no embedded pipe | agree |
| 28 | lesson:58-59 "seven Self-test cells" changed | cell-wise diff of `SKILL.md` base vs `a450e43`, column 4 | exactly 7 rows changed (source-recheck, robots, sitemap, commit-citation, quote-truth, readme-index, yahoo-robots); 2 rows added | agree |
| 29 | lesson:59 "recorded in LOG.md (seven Self-test cells)" | `grep -ciE 'round-56\|round 56\|r56' LOG.md` at `a450e43` and `f8438a2` | 0 and 0 (LOG's last entry is round 55) | **disagree** (D6) |
| 30 | lesson:68 ids `156` / `129` | `wc -l .ufo/waves/round-56/assimilation/{reg-ids,staged-ids}` | 156 / 129; bytes 780 / 645; sha256 `7f458d3d…`, `3938ec94…`; reproduction byte-identical | agree |
| 31 | lesson:69 collisions `8` (0–3-space pattern) | `comm -12` of registry ids (`e48354b7`) and staged ids | 8 (`S312 S329 S367 S372 S373 S374 S390 S409`), byte-identical to `assimilation/collisions` (40 B, `a443d89d…`) | agree |
| 32 | lesson:70 all eight are the same document | URL cell compare, both registries | 8/8 identical URLs; `w1/ExecIdGuard.md:86-95` table has 8 rows | agree |
| 33 | lesson:71-72 max lane id `S418`, S419/S420 not staged | `sort -V reg-ids \| tail -1`; `grep -E 'S(419\|420)' staged-ids` | `S418`; no match | agree |
| 34 | lesson:72-74 guard: indented row → `S287` under 0–3, nothing column-zero; 4-space outside both | `.ufo/waves/round-56/w1/ExecIdGuard.files/{fixture-*,guard-*}` + `scripts/sources-census.sh:541` (`^ {0,3}\|`) | `guard-0to3.out` = S287; `guard-col0.out` empty; `guard-0to3-on-4space.out` empty; `guard-unbounded-on-4space.out` = S287 | agree |
| 35 | lesson:80-81 quarantine `12` rows (9 payload-absent + 3 unreachable) | `wc -l …/quarantine-slice`; content | 12 (453 B, `6d92f440…`): 9 `payload-absent`, 3 "could not be fetched" | agree |
| 36 | lesson:82 package `104 knowledge entries` | `MERGE-REPORT.md:7`; `find knowledge -name '*.md' \| wc -l`; `find amendments -name '*.md' \| wc -l` | line 7 = 104; knowledge dir 98 `.md`; amendments 6; 98+6 = 104 | agree (composition) |
| 37 | lesson:68/82 staged rows `129` | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' SOURCES.append.md`; line 8 sum | 129; by-round sum = 129 | agree |
| 38 | lesson:82 "101 of 104 … and 126 of 129" not adopted | per-round `104-3`/`129-3`; package state: name-match + `used-by` | per-round 101/126 ✓; package state 7 entries have lane counterparts (6 same basename + `soft-404-recrawl` → `nonexistent-url-recrawl`), 10 staged ids are cited lane rows → 97 / 119 | **disagree** (D5) |
| 39 | lesson:79 dry run "census exit 0, 158 rows, three breaks E03/E01/E11" | `w1/ExecRowDryRun.md:70,100,118-119,133` | exit 0, `rows 158 (156 base + 2)`, b1 `E03`, b2 `E01`, b3 `E11` | agree (report evidence) |
| 40 | lesson:65-66 "10 cited hashes, 10 ancestors of `master`" | `w1/ExecLandedCheck.md:65,70-73,107` | `cited=10 landed=10 missing=0 unknown=0`, exit 0; 12 hash tokens → 10 distinct; selftest 14/14 | agree (report evidence) |
| 41 | lesson:66 "proposals 2 and 3 were not taken (at most one per round)" | `grep -cE '^[0-9]+\. ' considerthese/2026-10-25.md` | 4 proposals; 1 implemented, 4 was r55 | agree |
| 42 | `PROVINCE.md:408` = §Round-56 (lesson:59 via README) | `awk 'NR==408' PROVINCE.md` | `## Round-56 Yahoo! JAPAN crawl handling: …` | agree |
| 43 | README:137 cites `PROVINCE.md:408` | `awk 'NR==137' corpus/README.md` | line 137 names `PROVINCE.md:408` | agree (cite resolves; see D7) |
| 44 | README base `fcaf4b85…` `155 rows`; r55 `156`; r56 `158` | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\|…S[0-9]{3,}…'` | 155 / 156 / 158 | agree |
| 45 | README "nine per-engine entries" | `ls corpus/knowledge \| grep -E '^(baidu\|yahoo)'` | exactly 9 files, all named in README | agree |
| 46 | README line cites `22-30, 23, 29, 77-78, 120, 302-303, 335-336, 344, 361-362, 382, 397` | `awk 'NR==n' PROVINCE.md` for each | every line resolves to the item described (Frontier range, JS rendering, WCAG, deploy facts, sitemap/redirects, gzip/Sitemap, crawl budget, canonical/JS, r52 trio, r55 trio) | agree |
| 47 | `settlement.md`: 43 seats, roles 18/7/6/5/4/2/1, 43 reports, 0 misdirected | `w1-results.json` `agent` counts; `ls .ufo/waves/round-56/w1/*.md \| wc -l`; first-line check | 43 results, seats=43; executor 18, scout 7, critic 6, scribe 5, reviewer 4, connector 2, mutation-tester 1; 43 reports, all first lines `# <seat>` | agree |

## DISAGREEMENTS:

1. **S389 recheck span: 90 units stated, 84 measured** — attacks `corpus/lessons/round-56.md:38` (`a450e43`) and
   `w1/ScoutRejectRedirect.md:16,53,59`. Command: `units()` (span_tools/c56 rule) on the `grep -F -c '…'` string of
   `SOURCES.append.md:109` → **84 units, 92 characters** (84 CJK chars, no whitespace tokens), raw substring, count 1.
   The 90 also inflates the report's "3.6x the ceiling" (84/25 = 3.4x). The lesson line is already repaired at HEAD
   `f8438a2` ("recheck grep string 84 units", the only lesson change in that commit); the w1 report still says 90 at
   HEAD. The substantive point (over the 25-unit ceiling) survives at 84.

2. **`A1–A9` undercounts the attack list** — attacks `round-56.md:91` and `contract.md:98` ("`w1/CriticC1Contract.md`
   A1-A9"). `grep -oE '\bA[0-9]+\b' w1/CriticC1Contract.md | sort -u -V` → `A1 … A10`; A10 ("caller-chosen revision",
   line 61) is a real attack item and the contract's own header says "A1..A10 W1..W6". The cited range stops one short.

3. **"6 critic/reviewer/mutation seats" attacks, 7 measured** — attacks `round-56.md:99`. `w1-results.json` + `settlement.md:5-7`:
   `CriticC1Contract`, `CriticC2Contract`, `CriticControls`, `CritCheatC1`, `CritCheatC2` (critic), `ReviewerSelftallyCode`
   (reviewer), `MutC1Counter` (mutation-tester) = 7 seats, and `contract.md:100-101` folds `CriticControls` into C2 v2. Only
   by dropping `CriticControls` does the count become 6.

4. **S367 staged label "0 hits" misstates the measured count** — attacks `round-56.md:76-77`. The bare string
   `サーバーで設定する方法` occurs **once**, as the page's own `<h3>` (`S367.html`, offset 3194); what has 0 raw hits is the
   composite staged label `リンク先のウェブページの巡回制限 ― … → サーバーで設定する方法` (U+3000/`→` join), exactly as
   `w1/ExecStagedQuoteAudit.md:128` records ("`サーバーで設定する方法` raw 1"). The lesson's parenthetical says the bare
   string has 0 hits, contradicting its own cited evidence.

5. **"101 of the package's 104 … and 126 of its 129" is a per-round subtraction presented as a package state** —
   attacks `round-56.md:82-83`. Per-round it agrees (104−3, 129−3). Measured package state: 7 of the 104 entries have
   lane counterparts (6 same basename: `deleted-url-recrawl`, `link-target-crawl-restriction`, `rel-nofollow-semantics`,
   `robots-pattern-syntax`, `robots-txt-basics`, `robots-txt-refusal-rules`; plus `soft-404-recrawl` → `nonexistent-url-recrawl`),
   the 6 amendments are unapplied (`cmp` differs on all 6), and 10 staged ids now have cited lane rows (8 collision ids,
   all with non-empty `used-by`, + S375/S376 → S419/S420) → **97 of 104 and 119 of 129** not adopted. Round-55's lesson
   (`round-55.md:84`) carries the identical 101/126 although that round also adopted three, so the pair cannot both be
   package-state statements.

6. **"recorded in LOG.md" has no record** — attacks `round-56.md:59`. `grep -ciE 'round-56|round 56|r56' LOG.md` → 0 at
   `a450e43` and at HEAD `f8438a2`; LOG.md's last entry is round 55. The seven cells are tabulated
   (`w1/ScribeSkillRows.md`, 7 rows, verified) but not logged.

7. **README's round-56 trio cite does not land on the analogous sentence** — attacks `corpus/README.md:137`. `PROVINCE.md:408`
   is the §Round-56 heading, while the sibling cites `382` and `397` point at the "Frontier knowledge: no gate, no owned
   property audited" sentence of their sections; that sentence for round 56 is at `PROVINCE.md:422`. Not false, but the
   three cites are not the same kind of location.

8. **`assimilation/…` paths do not resolve from the lane root** — attacks `round-56.md:68,69,81`. `wc -l assimilation/reg-ids`
   at the lane root → `No such file or directory`; the files live at `.ufo/waves/round-56/assimilation/…` (numbers right:
   156/129/8/12). Inherited from `round-55.md:65-66,83`, which uses the same relative style.

Unrun: the `robots.txt` HTTP-200/no-`archives` sentence (`round-56.md:23`) — network claim, no retained receipt in
`.ufo/waves/round-56/`; not re-derived here.

Not re-run: the C2 version-1 counter (rows 9) and `scripts/landed_check.py` (row 40) — their numbers are taken from the
committed seat reports, which is stated in the row.

VERDICT: 47 numbers re-derived — 40 agree, 6 disagree (S389 90 vs 84 units; A1–A9 vs A1–A10; 6 vs 7 attack seats;
S367 label 0 vs 1 raw hit; 101/126 vs 97/119 package state; LOG.md has no round-56 record), 1 cite-style drift
(README `PROVINCE.md:408` vs the analogous 422), 1 path that does not resolve (`assimilation/…`), 1 unrun (robots.txt);
counters C1 7→0 of 10 and C2 0/8→8/8 reproduce exactly at base `e48354b7` and revision `a450e43`.
