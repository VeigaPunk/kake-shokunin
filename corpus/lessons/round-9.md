# Lesson — round 9 (2026-09-28)

Cites: LOG.md round-9 entry; evidence = 10 delegated read-only probes
(`~/Projects/webzites/reports/r9-publish-queue.md`, `r9-stale-markers.md`,
`dead-slot-recreate-readiness-r9.md`, `sentinel-sourceless-extract-r9.md`) +
self-verified curl GETs on the vault + dead slots. Commit `round-9`. Zero
publishes, zero metered fires, zero browser ops.

## The gap closed

Two coupled residuals: (a) no consolidated publish-queue readiness view — the
dedupe report named PQ-1..PQ-13 but nobody had mapped each item to gate class,
bound chat, and source freshness; (b) README residual "JS-rendered link
surfaces need rendered DOM" — false premise: the vault's link surface is a
static `const PROPERTIES = [...]` literal in the served body.

## What the baseline found

- **PQ-5 is the shortest path to green.** charter-ufo-fsd-kimi's `rebuild`
  already produced a verified version card (`efc1830`, preview 8,323B
  markerPresent, `liveAfter.stillDead:true`) — only the human Publish + slug
  click remains. Journals carry no `error.code`; the pipeline exited clean.
- **PQ-1-class vault rot is real and quantified without a browser.** 3 of 10
  live-claimed PROPERTIES[] links are dead (charter-ufo-fsd + plazir15 → 404
  sentinel sha `93ddca9a`; plazir27.kimi.pro → preview-404 redirect);
  `lucario` isn't in the array at all. `fleet/vault-properties.json` (09-20
  snapshot) still matches the live literal — the drift is upstream claims
  vs live fleet state, not page churn.
- **`sourceDir:null` is the single hard blocker for sourceless rows** —
  `cmdUpdate` refuses at `kimi-surface.mjs:483`, `cmdRecreate` refuses at
  `:845-849` on any live-200 slot. Extraction recipe landed
  (`vault-properties.md`); plazir27runson needs `--zip-exclude='assets/*.mp4'`
  (147MB of films exceed the 32MB `fetchLive` maxBuffer at `:339`).
- **Two platform shifts since 09-26:** the injected `sdk-seed.js` tag grew
  exactly +157B on every kimi-surface row (digest checks must normalize it —
  byte deltas now carry zero freshness signal), and website-id `1a0acf59…`
  serves on BOTH `ufo-fsd.kimi.pro` and `ufo-fsd.kimi.page` (the config's
  "fleet-unique 1/17" note is stale; an update fire may co-write both).
- **Citation review landed:** ops-automation's "6h cadence" is the timer's,
  not the file's (median gap 0.45h, one 42.7h hole); the "74 missing paths"
  figure is 75 in-repo (commit `f3d2ecd` adds 75 locs); `webzites` is not on
  PATH — canonical invocation `node ~/Projects/webzites/bin/webzites.mjs`.
- **25 unpushed source commits** are the GHP publish bottleneck:
  ds4cc-marketplace +20 (incl. the sitemap commit), plazir-15-site +5;
  charter is *behind* 2 (pull before any publish).
- **Fleet state unchanged**: probe-latest 18:51Z (12 ok / 5 violated / 1
  error), all FAILs match known-stale markers or documented dead slots —
  0 new failures. charter-ghp pin is the sole marker miss; ready diff sits
  in `reports/r9-stale-markers.md` (keeper owns the edit).

## Learned

- **The publish queue's binding truth lives in `state/kimi-map.json`, not the
  config.** Bound chats verified by `publishedUrl` matching, not hosts[] text —
  plazir15 came out ambiguous (vessel `1a0c2186` pristine vs emergent `1a0de2ed`
  with an unpublished version): a fired-orphan artifact, resolve before refire.
- **Read-only sweeps produce publish-ready diffs.** The charter-ghp re-pin is
  a one-line config edit handed to the keeper with exact line + live literal;
  prepare-the-diff beats flag-the-drift.
- **Live-404 sentinels are uniform**: all three dead slots serve the same
  13,409B body (sha `93ddca9a021664d5…`) — `liveBefore` journals pin this hash;
  any non-sentinel 404 on a kimi slot is a different failure class.
- **Cross-lane sweep found no contradictions**, one boundary note: the shared
  burner-chrome lease (CDP 9222) ownership between kake and kagi is unresolved
  — reported up, not absorbed.
