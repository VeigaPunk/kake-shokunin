source: Historical entry-local evidence: webzites probe/sync/reconcile source, fleet snapshots and the 2026-09-28/29 observations cited in this entry; source trees absent after the 2026-10-12 prune. Metadata authority only: S019 in corpus/SOURCES.md, not platform verification.
verified-at: 2026-09-29 (latest original evidence: r16 read-only re-verification, 2026-09-29T02:2xZ; probe 2026-09-28T18:51Z; dedupe-report and sync-check record 2026-09-26) — historical-not-live-reverified; round 21 re-verified no domain or source tree.
recheck: local historical reading only: `git show 5009ecaa1cce10b895617a585ddd3f7c7c923a84:corpus/knowledge/drift-detection.md`; the webzites and plazir source trees remain absent after the 2026-10-12 prune. Operator must restore them and re-derive domain verdicts or retire the dependent recipes.

# Drift detection — live vs source

Source: `~/Projects/webzites/{bin/webzites.mjs, scripts/kimi-surface.mjs,
src/probe.mjs}` <!-- r18 re-census 2026-10-14: the webzites tree (bin/webzites.mjs · scripts/kimi-surface.mjs · src/probe.mjs) absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. --> + `state/probe-latest.json` (2026-09-28T18:51Z run) +
`fleet/fleet.dedupe-report.md`.

Commands (all under `~/Projects/webzites/`): <!-- r18 re-census 2026-10-14: ~/Projects/webzites absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->

```bash
webzites probe --all                          # tripwire: GET + expect{status,finalUrl,title,marker}; rc 1 on violation
webzites grokbot reconcile <id>               # live bytes vs sourceDir/index.html: match|in-sync|drift
node scripts/kimi-surface.mjs sync-check [id] # kimi rows: title+marker vs sourceDir, normalized digest
node scripts/kimi-surface.mjs kimi-map        # chat→domain truth: publishedUrl/publishState per chat+project
webzites grokbot tick                         # probe + reconcile + keeper log, one round
```

## Semantics that matter

- **`in-sync*` on kimi rows = identity OK, freshness unknown.** Kimi injects
  `sdk-seed.js` and rewrites cfemail/entities → bytes never equal (fixed
  ~+157B normalized delta). `data-cfemail` is the ONLY tolerated churn class.
  Decide republish on *vintage evidence*: embedded dates, keeper logs,
  kimi-map version timestamps — never digests.
- **`200` is not live.** `plazir27.kimi.pro` returns 200 with a 5,995B
  preview-404 body (x-fc-request-id, Function-Compute ingress). `ufo-fsd.kimi.pro`
  is a 612B React shell — GET it, don't HEAD (HEAD→403). Trust `expect`
  title+marker, never status alone.
- **`reconcile` covers only index.html** — subpath rot is invisible to it.
- **Probe blind spot:** content-level rot inside a passing marker (heading
  stays, paragraph rots, PROPERTIES links all 404 → still `ok`). Escape class
  documented in dedupe-report mutation section.
- **Marker equality ≠ byte equality** for byte-twin rows (vault vs
  veigapunk-page differ only by the 93B `WZ-CANARY-FIX` meta).

## Observed drift state (2026-09-26, dedupe-report + sync-check)

| Row | State |
|---|---|
| ds4cc.kimi.page | in-sync* but ~18+ revs stale (Aug-29 vintage; missing ss-plus section, stale agent-pip) |
| plazir27.kimi.page | in-sync* stale vs charter-ghp (09-18 vs 09-26 scribe beat) |
| plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path |
| plazir15-ghp | tree byte-identical to live (no commit step) — **FALSE since 2026-09-26 (r16)**: source is 5 commits ahead of `origin/main`, live serves the pre-push tree (r16 proof below) |
| charter-ghp | sha256 == source index.html |
| vault PROPERTIES[] | 5 stale rows internally (PQ-1) — body drift only visible from fetched bytes |

## Fresh probe — 2026-09-28 (this repo's own run)

`webzites probe --all` at 18:51Z: 12 OK, 6 fail/err. `sync-check` (kimi
rows): ds4cc-kimi-mirror + burnerchrome-kimi `in-sync`; ufofsd-charter,
plazir27-kimi-page, plazir27runs-on, plazir15, charter-ufo-fsd-kimi, lucario
`drift`.

| Row | 09-26 record | 09-28 live | Delta |
|---|---|---|---|
| lucario | live/maintained | **404, never published** | config status wrong; canonical = `veigapunk.github.io/lucario/` (live) |
| charter-ghp | marker `2026-09-26 scribe beat` OK | marker absent — live rolled to `2026-09-28 scribe beat` | daily beat churns beat-dated pins in <48h → PQ-12 keeper fix |
| plazir15, charter-ufo-fsd-kimi | broken | still 404 | none |
| plazir27-kimi-pro | broken | still preview-404 (`finalUrlNot` trip) | none |
| ds4cc-kimi-mirror | stale Aug-29 | `in-sync` by markers — still stale (PQ-2 open) | none (marker can't see freshness) |
| xsnapshot-app | NXDOMAIN | fetch failed | none |

**Lesson encoded:** probe-verdict semantics — `in-sync` = identity+markers,
never freshness; `live` in config ≠ URL published. Snapshot config deltas at
`/tmp/sync-check.json` (transient); durable state in
`webzites/state/probe-latest.json` + `probe-history.jsonl`.

## r16 re-verification — plazir15-ghp live-vs-source drift (2026-09-29T02:2xZ, read-only)

Caught by the r16 quantified-claim sweep, not by any probe verb (`probe`
checks `expect` on the root URL; `reconcile` scores one `index.html`; neither
sees `sitemap.xml`):

| evidence | live | source (`~/Projects/plazir-15-site`) | `origin/main` |
|---|---|---|---|
| `sitemap.xml` `<loc>` count | **8** (incl. `/tetris/`, 1,293B, sha `3eb1722c…`) | **7** (sha `8e162356…`; `/tetris/` dropped in `0de5eb9`, 2026-09-26) | 8 |
| `snake/index.html` `og:url` | 0 hits | 1 hit (`3059bf0`) | 0 |
| `speedrun/` `rel=canonical` | `…/plazir-15-site/speedrun/` | `https://ds4cc.com/speedrun/` (`0de5eb9`) | self |

`git rev-list --count origin/main..HEAD` = **5** (HEAD `c814526`, remote
`bd02d10`, all five dated 2026-09-26); every one of the 8 live locs is HTTP
200, so this is **stale-vs-source, not rot** — a second unpushed publish gate
alongside ds4cc (PQ-14, `publish-queue.md`). Also corrects the r7 baseline
arithmetic carried in `sitemap-orphan-audit.md`: 93 (ds4cc staged) + 8
(plazir *live*) + 2 (charter) = 103 live locs; source-side re-derivation at
r16 = 93 + 7 + 2 = **102** — the two numbers differ *because* of this gate.
`reconcile plazir15-ghp` still reports `in-sync` (root index.html path is not
in the lag set) — the blind-spot class named above, live-proven.

## Round-20 citation-local note (base `cb807bc`)

> *[r20 citation-local 2026-10-19: `~/Projects/plazir-15-site` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/drift-detection.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [drift-detection:c1] **HOLD** — The documented webzites and plazir-15-site source trees are absent locally. Surface: `/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site`.
- [drift-detection:c2] **HOLD** — GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML. Surface: `GET https://ufo-fsd.kimi.pro`.
- [drift-detection:c3] **HOLD** — HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page. Surface: `HEAD https://ufo-fsd.kimi.pro`.
- [drift-detection:c4] **STALE** — The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header. Surface: `GET https://plazir27.kimi.pro`. Correction: As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.
- [drift-detection:c5] **HOLD** — The cited canonical GitHub Pages Lucario URL still serves the page. Surface: `GET https://veigapunk.github.io/lucario/`.
- [drift-detection:c6] **HOLD** — Both explicitly named dead-slot Kimi pages still return HTTP 404. Surface: `GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page`.

- [drift-detection:c7] **STALE** — The r16 live Plazir sitemap contained eight locations including tetris. Surface: `https://veigapunk.github.io/plazir-15-site/sitemap.xml`. Correction: As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.
- [drift-detection:c8] **STALE** — The r16 live snake page had no og:url and speedrun had a Plazir self-canonical. Surface: `https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/`. Correction: As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.


## Round-24 path reconciliation

These dated corrections supersede only current local-state readings of the cited lines; original bytes and coordinates are preserved. Evidence: `.ufo/waves/round-24/c1-receipts/` and `corpus/knowledge/freshness-sidecar.json` (lane-relative).

- 2026-10-21: ~/Projects/plazir-15-site absent (test -e exit 1); exact removal time and cause unknown, earlier W7 attribution historical. Citation corpus/knowledge/drift-detection.md:77 is a historical record, not an executable instruction.
