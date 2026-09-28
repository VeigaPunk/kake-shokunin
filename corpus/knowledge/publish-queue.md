# Publish-queue readiness ledger (PQ-1..PQ-13)

Source queue: `~/Projects/webzites/fleet/fleet.dedupe-report.md` (r1 lines
46–57, r2 lines 89–106). Config of record: `fleet/fleet.config.json` (21 rows,
`schema:webzites-fleet-v1`; `fleet/fleet.json` is a generated 2026-09-20
snapshot of the vault's *claimed* PROPERTIES[] — the audited input for PQ-1,
NOT a second config). Baseline evidence: `reports/r9-publish-queue.md`,
`reports/r9-stale-markers.md`, `reports/dead-slot-recreate-readiness-r9.md`,
`reports/sentinel-sourceless-extract-r9.md` (all 2026-09-28, read-only).

Gate classes: `metered-fire` (one metered chat fire must be spent),
`human-click` (operator Publish/Share→Update or external action), `missing-chat`
(no chat owns the host per `state/kimi-map.json`), `missing-source`,
`none` (config/policy only). Every publish ends in `human-click` — the
version-card click is never automatable.

## Ledger

| PQ | target | what it fixes | gate class | pre-publish checks | post-publish free reads | residuals / notes |
|---|---|---|---|---|---|---|
| PQ-1 | vault `ufo-fsd.kimi.page` (+ veigapunk-page index, ds4cc-mirror-vault-row) | PROPERTIES[] drift: **3 of 10 live links dead** (charter-ufo-fsd.kimi.page, plazir15.kimi.page → 404; plazir27.kimi.pro → preview-404) + ds4cc row `url:null` while live | `missing-chat` + `missing-source` + human | vault unbound after 200-chat sweep; sourceDir:null — extraction recipe in `vault-properties.md` | live GET + `kimi-map` refresh | blocked hardest: needs source bytes + chat + fire + click |
| PQ-2 | `ds4cc-kimi-mirror` (chat `1a073c43-bf42-874a-8000-0907bd80b9dc`) | stale ~Aug-29 mirror; **75 missing canonical paths** (sitemap f3d2ecd: 18→93 locs — "74" in dedupe is off by one); live mirror 404s `/speedrun/ /iqrunway/ /burnerchrome/` | `metered-fire` + human | `sync-check ds4cc-kimi-mirror` (in-sync* = identity only); bound chat verified | live URL 200 → `GetWebsiteByChatID` PUBLISHED → `sync-check` → `kimi-map` | `update` verb ships index.html-only (kimi-surface.mjs:459-466) — subpath restore needs recreate-class zip; source `ds4cc-marketplace` is **20 commits unpushed** — pushing GHP first also advances canonical |
| PQ-3 | `plazir27-kimi-page` (chat `1a0b5f08-fb32-87ba-8000-0907192544b0`) | 09-18-vintage charter mirror vs 09-28 canonical beat | `metered-fire` + human | local charter checkout is **behind 2** (`git pull` first); mirror embedded max date 09-18 | marker re-pin (PQ-12) after publish; `kimi-map` | sequences into PQ-12 |
| PQ-4 | `plazir15` (vessel `1a0c2186-fa12…` 0 versions; emergent `1a0de2ed…` 1 version unpublished — binding UNRESOLVED) | dead slot restore; tree md5-identical to plazir15-ghp (200, 38,337B) | `metered-fire` + human (Publish + SetWebsiteSlug) | journals: last `recreate` exit code 6 post-`fired` — a fire was consumed 09-26T14:46Z with no landed card; resolve chat ambiguity via `kimi-map` before refire | live 404→200 + slug resolve | orphan fire risk documented in `fire-journal-codes.md` |
| PQ-5 | `charter-ufo-fsd-kimi` (rebuild chat `1a0de32f-3f12-8611-8000-0907d06bd2f2`, 2 versions) | dead slot — **fire already done**: version `efc1830` + preview 8,323B markerPresent, `liveAfter.stillDead` | `human-click` only | none — shortest path to a green row; staged zip 1 day stale vs HEAD `61d0ce6` (acceptable for publish; re-stage if restoring from source) | click Publish on version card + set slug `charter-ufo-fsd` → live 200 + slugStatus | operator decision restore-vs-retire precedes the click |
| PQ-6 | `plazir27-kimi-pro` | slot never served; `ballot` marker misattributed (r2: 0 hits in plazir27, 35 on plazir15-ghp); provisional `PLAZIR-27` pin + `finalUrlNot:preview-404` already armed | `missing-chat` + `missing-source` + human | 302→`statics.kimi.ai/pages/preview-404-en.html` (5,995B) confirmed 09-28; `kimi-pro-slot` updatePath undocumented (kimi-surface-ops.md:189) | n/a until restored | extraction impossible — no artifact bytes anywhere |
| PQ-7 | `xsnapshot-app` | DNS registration (armed NXDOMAIN tripwire; curl exit 6 since 09-21) | `human-click` (external registration) | none | row leaves `errors[]` in probe-history | constant errors[] is intended baseline until then |
| PQ-8 | vault + `veigapunk-page` canary | decide vault canary treatment; veigapunk carries `WZ-CANARY-FIX-veigapunk` (keeper publish 09-21T03:47Z) | `none` — decision | — | — | execution path feeds PQ-13 verification |
| PQ-9 | fleet-wide | policy: should `probe.mjs` skip `status:"pruned"` rows? — it currently has **no** pruned branch (grep: 0 hits); pruned rows probed equally | `none` — policy | — | — | code change in `src/probe.mjs`, not a publish |
| PQ-10 | ufo-fsd-kimi-pro, xsnapshot-app, snapshot-kimi-pro, plazir27-kimi-pro, charter set | weak/misattributed marker tightening — r2 applied 13 field edits on 11 rows, killed 12 swap-mutations | `none` — config done | — | — | residual: content-level assertions are a probe.mjs feature; **new collision**: `ufo-fsd-kimi-pro` pin `data-kimi-website-id="1a0acf59…"` regressed 1/17 → 2/18 — same site-id serves on `ufo-fsd.kimi.page` AND `.kimi.pro` (keeper re-pin needed); `plazir27runson` marker `Nightcall` case-mismatches served `NIGHTCALL` — passes today only via title regex |
| PQ-11 | `plazir27runs-on` (chat `1a049cb5-47d2-89cb-8000-0907da6e778e`) | extract 63KB doctrine build to Origin repo OR accept surface-only | `missing-source` | config points sourceDir at charter repo but content is a distinct frozen 09-02 artifact — provenance unresolved | — | extraction feasible (self-contained body per sentinel audit) |
| PQ-12 | `charter-ghp` (+ plazir27-kimi-page after PQ-3) | re-pin beat-churn marker: config `2026-09-26 scribe beat` vs live **`2026-09-28 scribe beat (`** (verified r7 + r12 live GET; fleet.config.json:256) | `human` — **operator config edit** (r12 relabel: no webzites code writes `fleet.config.json`, only the `loadFleetConfig` reader `src/fleet.mjs:7-11`; the active scribe, not any keeper, churns the marker — and the scribe push-gate is currently failing, 3 beats `pushed:false` since 06:05Z, so churn is paused) | diff in `reports/r9-stale-markers.md` | next probe run flips row ok; procedure `SKILL.md:148-159` | beats churn ~daily while scribe pushes land — see SKILL.md re-pin procedure; keeper-timer dead ≠ the blocker (`keeper-timer-inert.md`) |
| PQ-13 | `veigapunk-page` | conditional verify only — canary row-id pin discriminates by design | `none` — conditional | — | re-GET after any PQ-8 action | only if PQ-8 executes |

## Ordering DAG (evidenced edges only)

- **PQ-3 → PQ-12**: re-pin the kimi charter beat marker after the mirror republish.
- **PQ-8 → PQ-13**: canary verification is conditional on the vault decision.
- **PQ-2 ↔ ds4cc GHP push**: independent queue items but one lever — the 20
  unpushed `ds4cc-marketplace` commits advance BOTH the canonical site and the
  mirror source payload.
- All other items independent; never invent edges between PQ-1/PQ-8 (both
  mention the vault but have no shared precondition).

## Cheapest wins

1. **PQ-12** — one config line (`fleet.config.json:256`), diff supplied.
2. **PQ-5** — version card `efc1830` already built and preview-verified; only
   the human Publish + slug click remains.
3. **PQ-10 residue** — re-pin `ufo-fsd-kimi-pro` marker to a non-colliding
   literal + fix `Nightcall`→`NIGHTCALL` casing (keeper edits).

## What publishes do NOT fix

- `dir/` href rot on kimi mirrors — needs href rewrite at source (permanent
  until republish-with-rewrite; `kimi-subpath-audit.md`).
- Vault PROPERTIES[] rot — needs the extraction+chat path of PQ-1.
- Beat-dated pins — will re-churn ~daily while the scribe beats land.
