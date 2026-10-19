# Fleet registry & tripwires

Source: `~/Projects/webzites/fleet/fleet.config.json` (schema <!-- r18 re-census 2026-10-14: ~/Projects/webzites/fleet/fleet.config.json absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
`webzites-fleet-v1`, updatedAt 2026-09-26) + `fleet/fleet.dedupe-report.md`.
Verified 2026-09-28: `len(sites)` = **21 rows** — status: 12 live / 3 pruned /
3 broken / 3 queued; updatePath: 14 kimi-websites-surface / 4 git-push-main /
2 kimi-pro-slot / 1 operator-registration. (Audit correction: round-1 said
"20 rows" — the registry has 21; the inventory below already lists all 21
ids. `app.ds4cc.com` is NOT a registry row — it exists only in SKILL.md's
property map as a Render service; do not add it here.)

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
  `prunedFor: <canonical-id>` and **never deleted**. `probe.mjs` has NO
  `pruned` handling at all — every row with `url` + `expect` is probed
  equally; pruning is a registry-level label invisible to the prober
  (audit correction 2026-09-28: round-1 said "inert in probe.mjs",
  implying a code path that does not exist).
- `priority`: `high` (revenue/brand: veigapunk-page, ds4cc-com) · `maintained`
  (canonical mirrors + GHP fronts) · `dormant` (frozen/broken/pruned) ·
  `queued` (awaiting operator action).

## Row inventory (21 rows; counts verified 2026-09-28 via `len(sites)`)

| id | url | status | sourceDir |
|---|---|---|---|
| vault | ufo-fsd.kimi.page | pruned→veigapunk-page | none |
| veigapunk-page | veigapunk.kimi.page | live | none (Kimi account only) |
| ds4cc-com | ds4cc.com | live | `~/Projects/ds4cc-marketplace` | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
| ds4cc-kimi-mirror | ds4cc.kimi.page | live, STALE (~Aug-29 DOM) | `~/Projects/ds4cc-marketplace` | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
| burnerchrome-kimi | burnerchrome.kimi.page | live | `~/Projects/ds4cc-marketplace/burnerchrome` |
| ufofsd | ufofsd.kimi.page | live (frozen landing) | none |
| plazir27runson | plazir27runson.kimi.page | live (Night Trilogy) | none |
| ufofsd-charter | ufofsd-charter.kimi.page | pruned→plazir27-kimi-page | charter repo |
| plazir27-kimi-page | plazir27.kimi.page | live (canonical kimi charter) | charter repo |
| plazir27runs-on | plazir27runs-on.kimi.page | live (distinct 63KB build) | charter repo |
| plazir15 | plazir15.kimi.page | broken (404) | `~/Projects/plazir-15-site` *[r20 citation-local 2026-10-19: `~/Projects/plazir-15-site` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]* |
| plazir15-ghp | veigapunk.github.io/plazir-15-site | live | `~/Projects/plazir-15-site` |
| charter-ufo-fsd-kimi | charter-ufo-fsd.kimi.page | broken (404) | charter repo |
| charter-ghp | veigapunk.github.io/charter-ufo-fsd | live (canonical doc) | `~/Projects/origin-work/charter-ufo-fsd` | <!-- r18 re-census 2026-10-14: ~/Projects/origin-work/charter-ufo-fsd absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
| plazir27-kimi-pro | plazir27.kimi.pro | broken (preview-404) | none |
| ufo-fsd-kimi-pro | ufo-fsd.kimi.pro | live (612B SPA shell) | none |
| xsnapshot-app | xsnapshot.app | queued (NXDOMAIN) | none |
| ds4cc-kimi-mirror-vault-row | null | pruned→ds4cc-kimi-mirror | `~/Projects/ds4cc-marketplace` | <!-- r18 re-census 2026-10-14: ~/Projects/ds4cc-marketplace absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
| snapshot-kimi-pro | null | queued | none |
| burnerchrome-com | null | queued | `~/Projects/ds4cc-marketplace/burnerchrome` |
| lucario | lucario.kimi.page | **broken (404, never published — see warning)** | `~/Projects/lucario` (canonical: `veigapunk.github.io/lucario/`) |

**Counting rule:** "21 rows" = raw `sites[]` length (inventory above lists
all 21). "14 kimi rows" = `updatePath == "kimi-websites-surface"`. Print the
command beside any count cited — audit round-1 found "20" propagated through
five files from one stale snapshot.

## Marker quality (r2 tightening)

Weak markers killed by r2: `sdk-seed.js` (boilerplate), `ballot`
(misattributed), `PLAZIR-27` (title-redundant across 3 variants), `snapshot.`
(foreign hits). Pins now deployment-scoped (`WZ-CANARY-FIX-veigapunk`,
`data-kimi-website-id` UUID) or beat-dated (`2026-09-26 scribe beat`) — all
require re-pinning on republish. Source: dedupe-report r2 mutation table
(12 cross-body swaps killed by new markers, 0 by old).
