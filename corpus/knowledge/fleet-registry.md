# Fleet registry & tripwires

Source: `~/Projects/webzites/fleet/fleet.config.json` (schema
`webzites-fleet-v1`, updatedAt 2026-09-26) + `fleet/fleet.dedupe-report.md`.

**Freshness warning:** this table is a snapshot. Live probe 2026-09-28 found
`lucario` recorded `live/maintained` while `lucario.kimi.page` had **never
been published** (404; README: "first publish pending — gated") — its real
canonical is `veigapunk.github.io/lucario/` (live, Pages branch deploy).
Also 2026-09-28: `charter-ghp` FAIL on stale marker (09-26 pin vs live
09-28 beat). Always re-probe before trusting `status`.

## Schema per row

```json
{"id","name","class","owner","url","expect":{"status","title","marker"},
 "sourceDir","sourceNote","updatePath","notes","status","priority",
 "lastChecked","prunedFor?"}
```

- `expect` = tripwire: GET status + final URL + title regex + one literal
  substring of raw bytes (`src/probe.mjs`, `html.includes`, case-sensitive).
- `status`: `live` | `broken` | `pruned` | `queued`. Pruned rows are marked
  `prunedFor: <canonical-id>` and **never deleted**; `status:"pruned"` is inert
  in `probe.mjs` — pruned rows still get probed (tripwire value).
- `priority`: `high` (revenue/brand: veigapunk-page, ds4cc-com) · `maintained`
  (canonical mirrors + GHP fronts) · `dormant` (frozen/broken/pruned) ·
  `queued` (awaiting operator action).

## Row inventory (2026-09-26 probes)

| id | url | status | sourceDir |
|---|---|---|---|
| vault | ufo-fsd.kimi.page | pruned→veigapunk-page | none |
| veigapunk-page | veigapunk.kimi.page | live | none (Kimi account only) |
| ds4cc-com | ds4cc.com | live | `~/Projects/ds4cc-marketplace` |
| ds4cc-kimi-mirror | ds4cc.kimi.page | live, STALE (~Aug-29 DOM) | `~/Projects/ds4cc-marketplace` |
| burnerchrome-kimi | burnerchrome.kimi.page | live | `~/Projects/ds4cc-marketplace/burnerchrome` |
| ufofsd | ufofsd.kimi.page | live (frozen landing) | none |
| plazir27runson | plazir27runson.kimi.page | live (Night Trilogy) | none |
| ufofsd-charter | ufofsd-charter.kimi.page | pruned→plazir27-kimi-page | charter repo |
| plazir27-kimi-page | plazir27.kimi.page | live (canonical kimi charter) | charter repo |
| plazir27runs-on | plazir27runs-on.kimi.page | live (distinct 63KB build) | charter repo |
| plazir15 | plazir15.kimi.page | broken (404) | `~/Projects/plazir-15-site` |
| plazir15-ghp | veigapunk.github.io/plazir-15-site | live | `~/Projects/plazir-15-site` |
| charter-ufo-fsd-kimi | charter-ufo-fsd.kimi.page | broken (404) | charter repo |
| charter-ghp | veigapunk.github.io/charter-ufo-fsd | live (canonical doc) | `~/Projects/origin-work/charter-ufo-fsd` |
| plazir27-kimi-pro | plazir27.kimi.pro | broken (preview-404) | none |
| ufo-fsd-kimi-pro | ufo-fsd.kimi.pro | live (612B SPA shell) | none |
| xsnapshot-app | xsnapshot.app | queued (NXDOMAIN) | none |
| ds4cc-kimi-mirror-vault-row | null | pruned→ds4cc-kimi-mirror | `~/Projects/ds4cc-marketplace` |
| snapshot-kimi-pro | null | queued | none |
| burnerchrome-com | null | queued | `~/Projects/ds4cc-marketplace/burnerchrome` |
| lucario | lucario.kimi.page | **broken (404, never published — see warning)** | `~/Projects/lucario` (canonical: `veigapunk.github.io/lucario/`) |

## Marker quality (r2 tightening)

Weak markers killed by r2: `sdk-seed.js` (boilerplate), `ballot`
(misattributed), `PLAZIR-27` (title-redundant across 3 variants), `snapshot.`
(foreign hits). Pins now deployment-scoped (`WZ-CANARY-FIX-veigapunk`,
`data-kimi-website-id` UUID) or beat-dated (`2026-09-26 scribe beat`) — all
require re-pinning on republish. Source: dedupe-report r2 mutation table
(12 cross-body swaps killed by new markers, 0 by old).
