# Drift detection — live vs source

Source: `~/Projects/webzites/{bin/webzites.mjs, scripts/kimi-surface.mjs,
src/probe.mjs}` + `state/probe-latest.json` (2026-09-28T18:51Z run) +
`fleet/fleet.dedupe-report.md`.

Commands (all under `~/Projects/webzites/`):

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
| plazir15-ghp | tree byte-identical to live (no commit step) |
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
