# ReviewHistoricalMarkings — round-33 wave-2 falsify

Seat: KakeR33.ReviewHistoricalMarkings. Rev reviewed: 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0
(sandbox clone `/fast/scratch/hyaku/kake-r33/w2/ReviewHistoricalMarkings/clone`; upstream
read-only clone `/fast/scratch/hyaku/kake-r33/ds4cc-upstream`, no fetch).

## Pointer checks — "Round-33 wave-1 additions" marking (sitemap-orphan-audit.md:239-244)

All four pointers resolve at the pinned rev; qualifiers accurate.

1. `kimi-subpath-audit.md:24` → resolves. Line reads "ds4cc.com's `sitemap.xml` (93 locs) is
   the 'should-serve' set for ds4cc.kimi.page" — matches "93 locs" / "should-serve set"
   exactly. Historical at `7fc6aa2f`: retained `sitemap.xml` parses to 100 `<loc>` (7,810 B,
   sha256 `55cb947f…`). Nuance: the count was already stale at `1fbdb8ed` (97 locs), so
   "become historical at `7fc6aa2f`" is loose but directionally correct.
2. `sitemap-orphan-audit.md:48-49` → resolves: "ds4cc.com/sitemap.xml → 404 live but exists
   at local HEAD (93 locs, unpushed — deploy-lag class…)". Same 93 count, same conclusion.
   Adjacent clause "exists at local HEAD" was separately corrected by c4 (:136, file absent
   2026-10-21) and restored per round-24 section — not part of the count claim.
3. Round-24 section = "## Round-24 local-source restoration correction" (:143-149); "97
   parsed loc elements" is verbatim at :145. "Stays exact for `1fbdb8ed`" re-derived true:
   `git -C ds4cc-upstream show 1fbdb8ed:sitemap.xml` → 7,614 B, sha256
   `18c51c45d62dd1cea99f9d88e7e19c0e9bd00c75f7e2ccf36e002a702823e53d`, `grep -c '<loc>'` = 97.
   At `7fc6aa2f` the count is 100, so the marking is accurate.
4. Round-23 "96 locs" readings → resolve at `sitemap-orphan-audit.md:135` (c3: GET 200,
   "listed 96 <loc> entries") and `kimi-subpath-audit.md:96-97` (c1/c2: live sitemap 96 locs,
   96 mapped GETs). All three are dated 2026-10-21 live HTTP observations; no source commit
   has 96 locs (`1fbdb8ed` = 97). "A live vintage, not a source state" is accurate.

## Caveats on the marking

- `:209` "93 locs at `f3d2ecd`" cannot be re-derived: `f3d2ecd` is not an object in the
  public upstream repo (`git cat-file -t` → fatal), consistent with c5's recorded 404
  (kimi-subpath-audit.md:100). The count remains supported by local/receipt evidence.
- The section cites reports under `.ufo/waves/round-33/w1/` (:220) and names
  `ScoutCorpusDs4ccPinClaims.md`, `ExecSitemapTreeParity.md` etc., but `w1/` is absent at
  `0a0acfb` (`git ls-files` shows only counters/criteria/sources/verification). The
  marking text is self-contained; the cited evidence is uncommitted working-tree output.

## Other ds4cc count statements left unqualified in corpus/

- **corpus/README.md:29** — "ds4cc mirror 75/93 canonical locs missing all post-vintage
  (0 rot)": undated standing summary in the coverage map; no vintage token. Both numbers
  superseded (source sitemap 100 locs at `7fc6aa2f`; live re-measure 2026-10-21: 96 locs /
  77 missing, kimi-subpath-audit.md:97). Primary miss.
- corpus/README.md:62-63 — "round-7 sitemap sweep (103 locs live-side; 102 source-side
  from r16…)": vintage-tagged, so partially qualified; totals stale under the new pin.
- corpus/knowledge/publish-queue.md:26 (PQ-2) — "75 missing canonical paths", "19/93
  served", "20 commits unpushed", "remote `e6bd071`": carries in-row vintage tags
  (f3d2ecd, r13-r15) but stands as the ledger's operative gate size; remote is now
  `7fc6aa2f` and the live delta is 77 (c2). Entry front-matter says
  "historical-not-live-reverified" — partial qualifier only.
- corpus/knowledge/ghp-subpath-spotcheck.md:89 — "ds4cc: 2 614 files, ~1 874 text":
  matches neither `1fbdb8ed` (2,630 files, `git ls-tree -r | wc -l`) nor `7fc6aa2f`
  (2,639); older vintage, only the entry-level "Historical-not-live-reverified" note.
- corpus/knowledge/freshness-sweep.md:61,90,121 — detector rows carry pinned
  `sitemapStatus` 404 / `pq2Remote e6bd071` / `pq2Unpushed` 20; the wave-1 section flags
  the underlying pins stale (:245-249) but the sweep table itself is unnoted. Borderline.

Adequately qualified (checked, not missed): kimi-subpath-audit.md:1,24,30-47 (dated
baseline + c1/c2/c5 corrections + :208-210 blanket qualifier naming the file);
sitemap-orphan-audit.md:70,74-79 (dated baseline + r16 re-read + same qualifier);
free-read-verbs.md:465 (inline "live 2026-09-28"); drift-detection.md:87 (r16 correction
arithmetic); corpus/lessons/* counts (round records, preserved-unchanged convention,
round-8.md:74); freshness-pins.json (flagged stale at :245-249).

## Commands (all exit 0 unless noted)

- `git clone -q <lane> … && git checkout -q 0a0acfb` → HEAD = 0a0acfb.
- ElementTree parse of retained sitemap → 100 locs; sha256/bytes as above.
- `git -C ds4cc-upstream show 1fbdb8ed:sitemap.xml | sha256sum` → `18c51c45…`; `grep -c
  '<loc>'` → 97. `git ls-tree -r --name-only <rev> | wc -l` → 2639 (`7fc6aa2f`), 2630
  (`1fbdb8ed`). `git cat-file -t f3d2ecd` → fatal (exit 128), object absent.
- `git ls-files .ufo/ | grep round-33` → no `w1/` entries; `git check-ignore` exit 1.
- greps for `93|96|97|100|102|103|74|75|77|locs|canonical paths` across corpus/ as above.

Not verified: live ds4cc.com sitemap (owned-site GETs prohibited); whether the w1 reports
exist in the lane working tree (bounds: work from own clone only). No tools installed.
