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
