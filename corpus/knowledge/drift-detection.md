# Drift detection — live vs source

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
