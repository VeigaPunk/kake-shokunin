source: entry-specific evidence — /tmp/orphan-check.mjs baseline 2026-09-28 (103 sitemap locs), pages.yml deploy-graph reads for ds4cc-marketplace and plazir-15-site, fleet.config.json, live sitemap.xml fetches; S001, S002, S004, S006 (corpus/SOURCES.md) for the r20 artifact-membership corrections — https://raw.githubusercontent.com/actions/upload-pages-artifact/7b1f4a764d45c48632c6b24a0339c27f5614fb0b/action.yml §Archive artifact
verified-at: 2026-09-28 (orphan-check baseline ~20:20Z; r16 re-read 2026-09-29T02:2xZ as recorded; r20 S001-S006 quote corrections 2026-10-19, base cb807bc) — historical-not-live-reverified; no live sitemap or domain fetch this round
recheck: on pages.yml upload path, pinned action, or sitemap change — run from kake-shokunin: grep -nF 'include-hidden-files' corpus/knowledge/ghp-served-set.md corpus/SOURCES.md; source-vanished: /tmp/orphan-check.mjs, ds4cc-marketplace and plazir-15-site pages.yml, and fleet.config.json are absent from this workstation — operator must restore them at the cited paths or retire the 2026-09-28 baseline counts

# Live-only orphan audit — the direction the source walk can't see

Evidence: `/tmp/orphan-check.mjs` baseline 2026-09-28 (~20:20Z, 103
sitemap-listed URLs across the three GHP rows), `pages.yml` deploy-graph
reads (ds4cc + plazir15), `fleet.config.json`, live sitemap fetches.
Companion to `ghp-subpath-spotcheck.md` (which covers source→live).

## The coverage matrix — every file↔URL cell now has an owner

| direction | detector | baseline |
|---|---|---|
| source file → live URL (rot) | subpath spotcheck (round 6) | 2 352 paths, 0 rot |
| **URL listed → live** (dead listing) | sitemap `<loc>` GET sweep | 103 URLs, **0 dead listings** |
| **live path → source** (orphan) | sitemap sweep + membership check | 0 orphans; GHP-provable impossible, see below |
| live path not listed anywhere | — | invisible by definition; bounded, see below |
| kimi subpaths | — | still uncovered (title+marker per path, never sha) |

## GHP live-only orphans are impossible by construction

`actions/upload-pages-artifact` + `actions/deploy-pages` deploy a
**fresh snapshot of the entire checked-out tree** every push — both
workflows upload `path: ./ds4cc-marketplace` / `path: .`
(`ds4cc-marketplace/.github/workflows/pages.yml`,
`plazir-15-site/.github/workflows/pages.yml`, read 2026-09-28). A Page
deploy never retains files from the previous artifact, so a deleted
source file cannot linger live. The whole "file deleted from source
stays served until redeploy" class (README residual, round-6 lesson)
does not exist on GHP — the live tree IS the last-pushed `origin/main`
tree, modulo the push→deploy lag already captured by the origin/main
comparison in the spotcheck.

Residual live-only exposure on GHP is therefore **listing coverage**:
paths that exist but no sitemap/audit enumerates. That is a completeness
property of the URL list, not a deploy defect. The first sitemap sweep
found nothing, and every unlisted path is still inside the source-walk
coverage (round 6 covered ALL sourceDir paths, not just listed ones) —
so the only true blind cell left is "URL the world can guess but no
list names," which is undetectable by enumeration.

## Procedure (the wedge: a URL list independent of the source tree)

1. Get a URL list that isn't the source walk. Sources observed:
   - Live `sitemap.xml`: plazir15-ghp ✓ (8 locs), charter-ghp ✓ (2 locs).
     ds4cc.com/sitemap.xml → **404 live but exists at local HEAD** (93
     locs, unpushed — deploy-lag class, use the staged copy).
   - No live sitemap and no list → crawl same-origin `href`s (BFS, stay
     inside base path) or use `docs/FLEET-MAP.md` path tables.
2. GET every `<loc>`; classify:
   | status | in sourceDir? | class |
   |---|---|---|
   | 200 | yes | healthy |
   | 200 | no | ORPHAN — foreign live content (GHP: shouldn't exist; flags deploy-source drift) |
   | 404 | yes | listed-but-404 = stale sitemap entry |
   | 404 | no | dead listing — prune the sitemap |
3. `in-sourceDir` check must try `rel`, `rel/index.html`, and `index.html`
   for the root — `/` resolves to `index.html` on all three sourceDirs
   (baseline script burned one iteration on this false positive).
4. Same normalize-against-`origin/main` rule as the spotcheck: a
   listed-but-404 that exists at local HEAD but not `origin/main` is
   deploy lag, not a defect.

## Baseline 2026-09-28 (~20:20Z)

| row | loc source | locs | healthy | orphan | dead listing | in-source-404 |
|---|---|---|---|---|---|---|
| ds4cc-com | staged `sitemap.xml` (HEAD, unpushed) | 93 | 92 | 0 | 0 | 0 (`/` = index.html edge) |
| plazir15-ghp | live sitemap.xml | 8 | 7 | 0 | 0 | 0 (same edge) |
| charter-ghp | live sitemap.xml | 2 | 1 | 0 | 0 | 0 (same edge) |

The staged sitemap doubles as a **pre-push drift preview**: all 93
listed paths already serve 200, so pushing adds a sitemap listing
what's already there — zero new-path risk in that direction.

**r16 re-read (2026-09-29T02:2xZ) — the 103 decomposes, and one term moved:**
`93 (ds4cc staged) + 8 (plazir15-ghp live) + 2 (charter) = 103` **live**;
source-side the same sum is now **102**, because `plazir-15-site` dropped its
`/tetris/` loc in `0de5eb9` (2026-09-26) while live still serves the 8-loc
pre-push tree — that row is **5 commits ahead of `origin/main`** (r16
discovery, now ledgered as **PQ-14**). plazir live `/tetris/` = 200/1,650B, so
this is stale-listing-through-deploy-lag, not a dead listing. Both numbers are
correct *for their surface*: never compare a live loc count against a
source-side one without naming which side (r16 rule).

## Charter marker churn — second consecutive day

`probe-latest.json` (18:51Z): `charter-ghp` FAILED again on
`marker: absent (expected 2026-09-26 scribe beat)`; live literal is now
`2026-09-28 scribe beat (the-scribe via local-fallback)`. The pin was
extracted as 2026-09-28 in round 3 but the config was never re-pinned —
beat pins churn ~daily when the daily scribe lands, so a <48h re-pin
only holds until the next beat. The re-pin edit is a publish-queue item
(webzites keeper owns `fleet.config.json`); this round records the
current literal for it.

Also standing (unchanged, correctly recorded): `plazir15`,
`charter-ufo-fsd-kimi`, `lucario` = dead 404 rows; `plazir27-kimi-pro` =
preview-404; `xsnapshot-app` = armed NXDOMAIN; `lucario` config
`status:"live"` still contradicted by the 404 probe (round-3 staleness
lesson still live).

## Limits

- kimi rows: a kimi publish replaces the whole bundle too (update verb
  = full-site fire), so live-only orphans are equally unlikely — but
  unverifiable without per-path title+marker probes; sync-check covers
  the root only.
- `lucario` GHP canonical (`veigapunk.github.io/lucario/`): no sitemap;
  site is 2 files (`index.html`, `engine.py`) — the row URL probe is
  already total coverage.
- A live orphan could exist only via a non-workflow Pages deploy
  (branch deploy) or a manual upload — neither is in the observed
  deploy graph; if a row ever switches deploy modes, re-derive this.

## Round-20 corrections (append-only; base `cb807bc`)

- Base `corpus/knowledge/sitemap-orphan-audit.md:14`: **[r20-correction 2026-10-19: a zero-orphan result must be checked against the actual deployed artifact/build output; the checkout alone does not establish the live→source set — S001, S004]**
- Base `corpus/knowledge/sitemap-orphan-audit.md:18`: **[r20-correction 2026-10-19: the no-orphan conclusion is conditional on comparing live paths with the actual uploaded/deployed artifact or build output, not the checkout — S001, S004]**
- Base `corpus/knowledge/sitemap-orphan-audit.md:21`: **[r20-correction 2026-10-19: upload-pages-artifact excludes .git/.github and v4 excludes hidden paths by default (v5 adds include-hidden-files); check the deployed artifact/build output rather than assuming full-tree coverage — S001, S002, S004, S006]**
- Base `corpus/knowledge/sitemap-orphan-audit.md:25`: **[r20-correction 2026-10-19: whether deleted paths remain served depends on the actual deployed artifact/build output; verify that output rather than infer from the checkout — S001, S004]**
- Base `corpus/knowledge/sitemap-orphan-audit.md:28`: **[r20-correction 2026-10-19: an artifact can be a subset or build output, so the served set is not equivalent to origin/main; compare the actual artifact/build output — S001, S002, S004, S006]**
- Base `corpus/knowledge/sitemap-orphan-audit.md:32`: **[r20-correction 2026-10-19: [INFERENCE] listing-only residual is not established until live→source membership is checked against actual deployed artifact/build output — corpus/knowledge/ghp-served-set.md (S001, S004)]**
- Base `corpus/knowledge/sitemap-orphan-audit.md:38`: **[r20-correction 2026-10-19: [INFERENCE] generated artifact/build output can include paths not in sourceDir, so listing coverage is not the only possible blind spot; compare actual deployed output — corpus/knowledge/ghp-served-set.md (S001, S004)]**
- Base `corpus/knowledge/sitemap-orphan-audit.md:112`: **[r20-correction 2026-10-19: [INFERENCE] workflow build output may also differ from the checkout; test actual artifact/build membership before declaring live-only paths impossible — corpus/knowledge/ghp-served-set.md (S001, S004)]**

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/sitemap-orphan-audit.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [sitemap-orphan-audit:c1] **STALE** — The live plazir sitemap currently lists 8 <loc> URLs. Surface: `https://veigapunk.github.io/plazir-15-site/sitemap.xml`. Correction: On 2026-10-21, the live plazir-15-site sitemap returned HTTP 200 with 7 <loc> entries, not 8.
- [sitemap-orphan-audit:c2] **HOLD** — The live charter sitemap currently lists 2 <loc> URLs. Surface: `https://veigapunk.github.io/charter-ufo-fsd/sitemap.xml`.
- [sitemap-orphan-audit:c3] **STALE** — The public ds4cc.com sitemap endpoint returns HTTP 404. Surface: `https://ds4cc.com/sitemap.xml`. Correction: On 2026-10-21, https://ds4cc.com/sitemap.xml returned HTTP 200 and listed 96 <loc> entries, not HTTP 404.
- [sitemap-orphan-audit:c4] **STALE** — The staged 93-loc ds4cc sitemap exists at local HEAD. Surface: `/home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml`. Correction: On 2026-10-21, the cited local /home/vgpnk/Projects/ds4cc-marketplace/sitemap.xml file was absent, so the 93-loc staged-copy presence claim does not hold at that path.
- [sitemap-orphan-audit:c5] **HOLD** — The direct live plazir /tetris/ route returns HTTP 200 and 1,650 bytes. Surface: `https://veigapunk.github.io/plazir-15-site/tetris/`.
- [sitemap-orphan-audit:c6] **STALE** — The current charter homepage marker is 2026-09-28 scribe beat (the-scribe via local-fallback). Surface: `https://veigapunk.github.io/charter-ufo-fsd/`. Correction: On 2026-10-21, the charter homepage contained `2026-09-30 scribe beat (the-scribe via local-fallback)`, not the `2026-09-28` literal.
- [sitemap-orphan-audit:c7] **STALE** — The plazir15, charter-ufo-fsd-kimi, and lucario rows each return HTTP 404. Surface: `https://plazir15.kimi.page/; https://charter-ufo-fsd.kimi.page/; https://veigapunk.github.io/lucario/`. Correction: On 2026-10-21, plazir15.kimi.page and charter-ufo-fsd.kimi.page still returned HTTP 404, but https://veigapunk.github.io/lucario/ returned HTTP 200, so lucario is no longer in the dead-404 set.
- [sitemap-orphan-audit:c8] **HOLD** — plazir27-kimi-pro redirects to the preview-404 page. Surface: `https://plazir27.kimi.pro/`.


## Round-24 local-source restoration correction

The local-state rationale at line136 [sitemap-orphan-audit:c4] is historical. On 2026-10-21 the local sitemap is present and byte-identical to checkout HEAD 1fbdb8ed: 7,614 bytes, SHA256 18c51c45d62dd1cea99f9d88e7e19c0e9bd00c75f7e2ccf36e002a702823e53d, 97 parsed loc elements (w1/R23ReceiptsDs4ccStale.md, exact commands/output). This does not verify the earlier 93-entry count or refresh the separate round-23 HTTP observation. No publication or source change occurred.

## Round-26 source recheck

- Round-26 source recheck (2026-10-21, append-only; original lines unchanged). The round-20 correction lines in this entry cite S001, S002, S004 and S006 (lines 120-127). Each was judged against bytes re-fetched 2026-10-21 (`.ufo/waves/round-26/fetched/`, receipts `.ufo/waves/round-26/rechecks/S0NN.json`) and holds: S001 and S002 as above; S004 uploads the configured path as a gzip-compressed tar; S006 lists the files Jekyll does not build. The conclusions that the served set is the deployed artifact or build output, not the checkout, follow from these and stay marked [INFERENCE] where they were. Ledger pairs in `.ufo/waves/round-26/statements.json`; found by the falsify wave (w2/CounterCritic.md).

## Round-27 provenance-range clarification (2026-10-21)

Line2's historical `S001-S006` band is expanded, not silently reduced to
its endpoints. The inline round20 corrections at lines120–127 use exactly
S001, S002, S004 and S006, as their original disposition records confirm.
The date2026-10-19 and base`cb807bc` remain historical and are not rewritten.

- S003 HOLD at the contextual batch scope: round20 lesson A2 explicitly
  connects this entry's served-set misconception with the S003-containing
  mechanism group. This does not attribute every inline correction to S003.
  Pair03A's evidence is admitted; Pair03B's stronger “no historical linkage”
  conclusion is rejected. The narrower inline source set above governs.
- [r27-recheck S005 STALE] The band over-attributes this entry's quote
  corrections to S005. None of its eight round20 correction records uses
  S005; the mechanism row A2 also omits it, while A3 applies it to other
  entries' custom-domain errors. Correct support for the inline corrections
  is S001, S002, S004 and S006. This is a partial attribution correction,
  not stale dating, source drift, a new sitemap observation or a changed base.
  The min/max-band alternative is preserved in both reviewers' reports;
  the explicit entry-specific support set is chosen here.

Evidence: `.ufo/round-20/resume/citation-disposition.json` platformCorrections;
`corpus/lessons/round-20.md:261–262`; `.ufo/waves/round-27/pairs.json`,
`w1/Pair03A.md`, `Pair03B.md`, `Pair07A.md`, `Pair07B.md` (wave-relative).

Round27 disclosure correction: the earlier “both reviewers” wording conflated
two alternatives. Pair07A records the min/max-interval interpretation;
Pair07B records a consulted-batch/opened-date reading. Both proposed STALE,
but their alternatives are not identical. The chosen relevance/support rule
and exact inline support set remain as stated; date/base and original bytes
are preserved. The strengthened S003 artifact witness includes A2's pointer
to this entry, not merely the adjacent fix-group cell.

## Round-33 ds4cc source pin 7fc6aa2f

The corpus' ds4cc-marketplace reads were pinned at `1fbdb8ed` (S062, and the
local clone `~/Projects/ds4cc-marketplace`, which is still at that commit). The
upstream repository moved one commit to
`7fc6aa2fc12451dd451fed5a9ee7125f3a90e884` (2026-10-21T17:32:55Z, "magga:
Frostbite — Classic & Remastered at /magga/frostbite/"), read on 2026-10-22
through a sandbox clone of the public repository (S065). The commit adds
three pages under `/magga/frostbite/` (hub, `classic/`, `remastered/`) with
their scripts and covers, links them from `magga/index.html`, and adds three
locs to `sitemap.xml` (lines 15–17). It changes none of the four files S062
retains (`render.yaml`, `apps-sdk/Dockerfile`, `apps-sdk/src/server.ts`,
`.dockerignore`).

Measured from the retained bytes (`.ufo/waves/round-33/sources/ds4cc-7fc6aa2f/`;
blob ids in S065). The sitemap count is the number of `<loc>` elements
parsed as XML; each canonical verdict is `scripts/canonical_audit.py` run on
one page with `expectedCanonical` equal to that page's sitemap loc:

sitemap-locs: 100
canonical https://ds4cc.com/magga/frostbite/: clean
canonical https://ds4cc.com/magga/frostbite/classic/: clean
canonical https://ds4cc.com/magga/frostbite/remastered/: clean

At `1fbdb8ed` the same file had 97 locs. Count statements earlier in this
entry and in `kimi-subpath-audit.md` (93 locs at `f3d2ecd`, 103 across three
GHP rows on 2026-09-28) are historical for their dates and commits; this
section does not re-measure them. Limits: source-side only. Nothing was
fetched from ds4cc.com, so whether this commit is deployed, and what the
live sitemap lists, is not known from this section; a `clean` verdict is the
lane's offline canonical policy on the page's explicit head link, not a
search-engine selection.

## Round-33 wave-1 additions (append-only)

Checked by round-33 wave-1 seats against `7fc6aa2f` and the lane at
`bc6c4a8`; reports under `.ufo/waves/round-33/w1/`.

- Sitemap to tree parity (`ExecSitemapTreeParity.md`): at `7fc6aa2f` all 100
  locs map to a tracked file (86 directory locs to `index.html`, 14 explicit
  file locs), 0 unmapped; one tracked page,
  `benchmarks/benxshitter-frontier.html`, is in no loc (also so at
  `1fbdb8ed`, 97 of 97 mapped). The three new pages' 21 relative or
  same-host references all resolve to tracked files, and
  `scripts/base_path_audit.py` with base path `/` is clean on them
  (`ExecNewPagesRefIntegrity.md`). Static source parity only.
- Publishing record (S066): GitHub's Pages deploy workflow run 39644779773
  for `7fc6aa2f` concluded `success` (started 17:32:59Z, updated 17:33:42Z
  on 2026-10-21). That is GitHub's record of the workflow, not an
  observation of what ds4cc.com serves now. The same push's "Test Apps SDK
  wrapper" run 39644779805 concluded `failure`, and the six most recent
  main-branch runs of that workflow (`7fc6aa2f` back to `480dd05f`,
  2026-10-14) all concluded `failure` (S066; second response retained at
  `.ufo/waves/round-33/sources/gh-actions-apps-sdk-runs-main.json`, read
  2026-10-22T20:06:32Z). The cause was not examined.
- Statements that become historical at `7fc6aa2f`: "93 locs" as the
  should-serve set (`kimi-subpath-audit.md:24`, this entry's lines 48–49)
  and the round-24 "97 parsed loc elements" (this entry's round-24 section),
  which stays exact for `1fbdb8ed` (7,614 bytes, sha256 `18c51c45…`); the
  round-23 "96 locs" readings are a live vintage, not a source state
  (`ScoutCorpusDs4ccPinClaims.md`).
- Not repaired, flagged: `corpus/knowledge/freshness-pins.json` still pins
  `pq2Remote` `e6bd0718` (29 commits behind `7fc6aa2f`) and `sitemapStatus`
  404, which round-23 live observations already contradicted. Re-pinning
  needs the sweep's armed section, which fetches owned sites; it was not
  run this round.
- One page attribute mismatch, source-side: `magga/frostbite/index.html:208`
  declares `width="1280" height="960"` for `covers/classic.png`, whose bytes
  are 960×768 (`ScoutUpstreamCommitAnatomy.md` F1). Rendering is governed
  by CSS `aspect-ratio` per that report; not verified in a browser.

## Round-33 wave-2 corrections (append-only)

- The stale-pin flag above names two values; a third is stale too:
  `pq2Unpushed` 20, where the local checkout now has 0 unpushed commits
  (`w2/ScoutPinsFlagAccuracy.md`). "Which round-23 live observations already
  contradicted" applies to `sitemapStatus` only; `pq2Remote` and
  `pq2Unpushed` are settled by public `git ls-remote` and the read-only
  checkout, with no owned-site request. An armed sweep on this host would
  still not be green (`fleet.config.json` and `probe-history.jsonl` are
  absent).
- Other ds4cc count statements in the corpus not qualified by the section
  above, all historical for their dates (`w2/ReviewHistoricalMarkings.md`):
  `corpus/README.md:29` ("75/93 canonical locs missing"), `corpus/README.md:62-63`
  (103 live / 102 source locs), `publish-queue.md:26` (PQ-2: 19/93, 20
  unpushed, remote `e6bd071`), `ghp-subpath-spotcheck.md:89` ("2 614 files";
  the tree has 2,630 files at `1fbdb8ed` and 2,639 at `7fc6aa2f`), and the
  detector pins quoted in `freshness-sweep.md:61,90,121`.
- `7fc6aa2f` was still the upstream head at 2026-10-22T20:14:58Z, and the
  retained run listing was byte-identical to a fresh read
  (`w2/ScoutUpstreamHeadNow.md`, `w2/ReviewS066RowTruth.md`).
