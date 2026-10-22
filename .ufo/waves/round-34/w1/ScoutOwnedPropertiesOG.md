# Open Graph state of owned properties — retained served bytes only (r34 w1)

Scope: every owned surface in the lane property map (SKILL.md:14-29) that has retained
served HTML in `.ufo/`. No live requests were made. Counter: `link_preview_probe.py`
(sandbox `/fast/scratch/hyaku/kake-r34/w1/ScoutOwnedPropertiesOG/link_preview_probe.py`),
HTMLParser-based, counts `meta[property]` with an exact lowercase og token and non-empty
stripped `content`, plus `link[rel~=canonical]` and `meta[name=twitter:card]`.

## Snapshot inventory (only served captures that exist)

- `.ufo/waves/round-23/live/*` — the lane's only served snapshot batch: capture times
  2026-10-21T06:33:03Z–06:33:20Z from each `fetch.json` `fetchedAt`; 8 HTML bodies retained,
  4 dead kimi slots metadata only; every `page.html` sha256 equals its `fetch.json` `sha256`.
- `.ufo/waves/round-29/real-input/sites/{plazir15,charter,lucario}-ghp/page.html` — byte-identical
  copies of the round-23 GHP bodies (same sha256), no capture time in their manifests, so no added freshness.
- `.ufo/waves/round-22/domain-snapshot/index.html` — local static source copy of the charter GHP
  page (`provenance.json` retrieved 2026-10-20, sourceCommit 31c465f1…, sha256 43d321f9…); not served.
- No other owned served capture exists in `.ufo` (rounds 26/27 `fetched/` hold external standards
  pages only); the round-23 batch is the newest owned served bytes.

## Per-site census

| surface | snapshot (lane-relative) | capture UTC | HTTP | og:title/type/image/url | all 4 | og:url | absolute | canonical | og:url==canonical | twitter:card |
|---|---|---|---|---|---|---|---|---|---|---|
| ds4cc.com | `.ufo/waves/round-23/live/ds4cc-primary/page.html` (ccb3f46eda1c) | 06:33:03Z | 200 | 1/1/**0**/1 | no | `https://ds4cc.com/` | yes | `https://ds4cc.com/` (`:496`) | yes | `summary` (`:12`) |
| ds4cc.kimi.page | `.ufo/waves/round-23/live/ds4cc-kimi/page.html` (108f5aca89b9) | 06:33:04Z | 200 | 1/1/**0**/1 | no | `./` (`:8`) | **no** | none | **no** | `summary` (`:10`) |
| burnerchrome.kimi.page | `.ufo/waves/round-23/live/burnerchrome-kimi/page.html` (44dc3491fbc6) | 06:33:06Z | 200 | 0/0/0/0 | no | — | — | none | — | none |
| veigapunk.kimi.page (vault) | `.ufo/waves/round-23/live/vault-index-kimi/page.html` (a0a7f33aba44) | 06:33:08Z | 200 | 0/0/0/0 | no | — | — | none | — | none |
| plazir-15-site (GHP) | `.ufo/waves/round-23/live/plazir15-ghp/page.html` (d82af77aee40) | 06:33:03Z | 200 | 1/1/1/1 | **yes** | `https://veigapunk.github.io/plazir-15-site/` (`:15`) | yes | same (`:10`) | yes | `summary_large_image` (`:17`) |
| charter-ufo-fsd (GHP) | `.ufo/waves/round-23/live/charter-ghp/page.html` (7c243a1d8135) | 06:33:04Z | 200 | 1/1/1/1 | **yes** | `https://veigapunk.github.io/charter-ufo-fsd/` (`:14`) | yes | same (`:8`) | yes | `summary_large_image` (`:18`) |
| lucario (GHP) | `.ufo/waves/round-23/live/lucario-ghp/page.html` (bee2d9f5b577) | 06:33:17Z | 200 | 0/0/0/0 | no | — | — | none | — | none |
| ufo-fsd.kimi.pro | `.ufo/waves/round-23/live/ufo-fsd-kimi-pro/page.html` (1df92e30ba5a) | 06:33:12Z | 200 | 0/0/0/0 (612 B SPA shell) | no | — | — | none | — | none |

All: no duplicate `og:type` (max count 1), zero case-variant near-misses, zero `name="og:*"`
misuse. og:image tag present only on the two GHP pages above; asset reachability not tested.

## No retained bytes

- `charter-ufo-fsd.kimi.page`, `lucario.kimi.page`, `plazir15.kimi.page`, `plazir27.kimi.page`
  — 404 at 2026-10-21T06:33Z, 13409 B bodies not retained (live_snapshot stores `page.html`
  only for 2xx text/html; dirs hold `fetch.json`/`audit.json` only). Digest 93ddca9a… of that
  404 body exists only as a recorded hash; `find .ufo -size 13409c | sha256sum | grep ^93ddca`
  matched no stored file. Their OG state is unknown.
- `app.ds4cc.com/mcp` (Render) — no retained HTTP body of any kind in `.ufo`; not an HTML page
  and absent from the r23 population (`.ufo/waves/round-23/c2-population.json` lists 12 HTML
  surfaces, no Render row).
- Subpaths (`ds4cc.com/speedrun/`, `plazir-15-site/speedrun/`, any ds4cc sub-page) — no
  retained snapshots; every census row above is a site root.

## Findings (advisory)

1. Only 2 of 8 retained served pages carry all four required tags, and both are GitHub Pages.
   The primary `ds4cc.com` root is missing `og:image` — the same omission exists in current
   upstream source at 7fc6aa2f (`src/index.html`, 77625 B, commit 2026-10-21T17:32:55Z,
   og:title/type/url present, no og:image), so it is not a snapshot artifact.
2. `ds4cc.kimi.page` emits `og:url="./"` — relative, and the page carries no canonical link at
   all. This is the exact defect class C1 reports (non-absolute og:url; og:url cannot be
   compared to a page canonical). Its manifest declares expectedCanonical `https://ds4cc.com/`.
3. The four Kimi properties that serve 200 (`burnerchrome`, vault index, `ufo-fsd.kimi.pro`)
   plus `lucario` GHP ship zero Open Graph and zero `twitter:card`, so shares of those URLs
   fall back to platform scraping.
4. Freshness ceiling: no owned served bytes newer than 2026-10-21T06:33Z exist in the lane, so
   any "current" OG claim is ~1 day stale, and the four dead slots have no served evidence.

## Commands (all in sandbox; exit codes observed; no installs/updates, no network calls)

- `python3 -B link_preview_probe.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --json out/og-census.json` → exit 0 (census above; first run exit 0 but under-counted `twitter:card` because name-metas were not stored; fixed, reran, exit 0).
- inline sha256 vs `fetch.json` check over the 12 r23 dirs → exit 0; 8 `body=match`, 4 `no-html`, 0 mismatch.
- `find .ufo -type f -size 13409c | xargs -0 sha256sum | grep '^93ddca'` → no output (`grep` exit 1): no retained 404 body.
- `sha256sum .ufo/waves/round-23/live/*/page.html .ufo/waves/round-29/real-input/sites/*/page.html` → exit 0; the three r29 GHP bodies equal r23 (7c243a1d…, bee2d9f5…, d82af77a…).
- `tar -xJf .ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz -C src index.html burnerchrome/index.html` → exit 0; source census as in finding 1 (burnerchrome source has no OG and canonical `https://ds4cc.com/burnerchrome/`, which the served kimi copy lacks — source/served divergence, not resolved here).
- `git -C /fast/scratch/hyaku/kake-r33/ds4cc-upstream show -s --format='%H %cI' 7fc6aa2f…` → exit 0, `7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 2026-10-21T17:32:55Z`.

## Not verified

Live state today (out of bounds here), OG tags inside the four 404 bodies, whether the four
`og:image` asset URLs resolve, non-root page metadata, platform card rendering, and any
source-vs-served difference for ds4cc (served page likely predates 7fc6aa2f).
