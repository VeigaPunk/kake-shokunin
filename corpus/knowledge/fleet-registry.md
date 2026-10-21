source: Historical entry-local evidence: webzites fleet.config.json (updatedAt 2026-09-26), fleet.dedupe-report.md, src/probe.mjs and the 2026-09-28 probe cited below. Metadata authority only: S019 in corpus/SOURCES.md, not platform verification.
verified-at: 2026-09-28 (`len(sites)` = 21 and live probe of 2026-09-28 — original evidence; historical-not-live-reverified, not re-probed or re-read this round; source absent since the 2026-10-12 `~/Projects` prune per r18 re-census 2026-10-14)
recheck: on fleet source restore or retirement — `test -f "$HOME/Projects/webzites/fleet/fleet.config.json" && node -p 'const c=require(process.env.HOME+"/Projects/webzites/fleet/fleet.config.json"); [c.schema,c.updatedAt,c.sites.length].join(" ")' || echo "absent: operator must restore the fleet source or retire this entry"` (expect `webzites-fleet-v1 2026-09-26 21` when present)

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
| plazir15 | plazir15.kimi.page | broken (404) | `~/Projects/plazir-15-site` |
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

## Round-20 citation-local note (base `cb807bc`)

> *[r20 citation-local 2026-10-19: `~/Projects/plazir-15-site` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*

## Live re-verification — round 23 (2026-10-21)

Read-only live checks; receipt `.ufo/waves/round-23/receipts/fleet-registry.json` (claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. Where this section and earlier text disagree, this section is newer.

- [fleet-registry:c1] **HOLD** — The canonical fleet configuration is currently absent at its recorded source path. Surface: `test -e /home/vgpnk/Projects/webzites/fleet/fleet.config.json`.
- [fleet-registry:c2] **UNVERIFIABLE** — The current raw sites[] array contains 21 rows. Surface: `test -f "/home/vgpnk/Projects/webzites/fleet/fleet.config.json" && node -p 'const c=require("/home/vgpnk/Projects/webzites/fleet/fleet.config.json"); [c.schema,c.updatedAt,c.sites.length].join(" ")' || echo "absent: operator must restore the fleet source or retire this entry"`. Unverifiable: The canonical fleet.config.json is absent, so there is no current sites[] array to count; the command took its absent-file branch and the 21-row value remains historical evidence only.
- [fleet-registry:c3] **HOLD** — Both named high-priority endpoints remain publicly reachable at their listed URLs. Surface: `GET https://veigapunk.kimi.page/; GET https://ds4cc.com/`.
- [fleet-registry:c4] **HOLD** — The current endpoint split remains a 404 at the Kimi alias and a live GitHub Pages canonical; this does not re-prove the historical ‘never published’ wording. Surface: `GET https://lucario.kimi.page/; GET https://veigapunk.github.io/lucario/`.
- [fleet-registry:c5] **STALE** — The plazir27.kimi.page row remains live as the canonical Kimi charter. Surface: `GET https://plazir27.kimi.page/`. Correction: As of 2026-10-21, https://plazir27.kimi.page/ returns HTTP 404 (404 Page Not Found) rather than serving a live canonical Kimi charter.
- [fleet-registry:c6] **STALE** — The plazir27runson.kimi.page row is live (Night Trilogy). Surface: `GET https://plazir27runson.kimi.page/`. Correction: As of 2026-10-21, https://plazir27runson.kimi.page/ returns HTTP 404 (404 Page Not Found), so its live (Night Trilogy) status is stale.
- [fleet-registry:c7] **STALE** — The xsnapshot-app row is queued because xsnapshot.app is NXDOMAIN. Surface: `GET https://xsnapshot.app/`. Correction: As of 2026-10-21, https://xsnapshot.app/ resolves and returns HTTP 200 with a page stating domain live · build in progress, so NXDOMAIN is no longer an accurate basis for its queued status.
- [fleet-registry:c8] **HOLD** — The listed GitHub Pages canonical charter document is currently live. Surface: `GET https://veigapunk.github.io/charter-ufo-fsd/`.
