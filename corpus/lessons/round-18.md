# Lesson — round 18 (2026-10-14): OMP/ufo-fsd re-census — W7 mega-prune caught standing

Cites: LOG.md round-18; `scripts/freshness-sweep.mjs`;
`corpus/knowledge/freshness-pins.json`; run artifacts `/tmp/kake-r18/`
(`before.json`, `before.out`, `after.out`, `after-offline.out`, `p.json`).

## The catch

The standing sweep was run at round open (2026-10-14T12:40Z) and exited 2 —
its biggest catch yet. Sometime between r17 (2026-09-29) and today the
`~/Projects` tree was pruned/migrated ("W7"): **33 of 36 pinned children
removed, 11 added.** Gone: `webzites` (the lane's instrument host — CLI,
fleet registry, probe history, keeper reports), `ds4cc-marketplace`,
`plazir-15-site`, `lucario`, `origin-work` wholesale (charter-ufo-fsd,
open-bug-bounties, and the ufo-fsd-alpha copy the corpus cited), plus the
`webzites-{probe,keeper}` systemd units, `~/DIRMAP.md` <!-- r18 re-census 2026-10-14: ~/DIRMAP.md absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->, and every keeper
report. `ufo-fsd-alpha` now lives directly at `~/Projects/ufo-fsd-alpha`
(same repo, HEAD `964f443e`) — but **without** `.ufo/charter-scribe/` or a
`ledger.jsonl`, so the scribe-ledger cite is dead, not moved.

## What the instrument proved before any repair

- `§paths`: 36 unannotated misses + 45 beyond the pinned miss set — the
  set-delta gate caught the class it was built for.
- `§history`: unreadable `probe-history.jsonl` failed closed at exit 2.
- `§armed` still ran the parts that can run: PQ-12's armed watch FIRED —
  live marker moved `2026-09-26` → `2026-09-30 scribe beat` (sha
  `7c243a1d…`, 53 660 B) with `fleet.config.json` gone, so the CHURN-AGAIN
  reading is "edit landed while the registry file was unverifiable". PQ-5
  still `PENDING` 404/13 409B/`93ddca9a…`; ds4cc sitemap still `PRE-PUSH`
  404/9 379B.
- `--selftest` regressed 10/10 → 8/10: fixture A cited `~/Projects/ *[r20 citation-local 2026-10-19: `~/Projects/webzites` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; historical record, not an executable instruction.]*
  webzites/fleet` as its guaranteed-resolving path — a fixture that
  trusted the world, which is exactly what fixtures must not do.

## Repairs (this commit)

- 63 cite lines across 22 files carry an inline `<!-- r18 re-census … -->`
  erratum marking each gone path absent and keeping the cite as a
  historical record (append-only; no claim deleted). Three multi-token /
  multi-line cites were repaired by hand after the blanket annotation
  broke brace-list grammar.
- `freshness-pins.json` re-measured in one pass: `pathsMissSet` 10 → 55,
  `projectsChildrenSet` 36 → 14, `charterGhpPin`/`-LiveSha`/`-ChurnAfter`
  re-baselined to the observed 2026-09-30 marker; new
  `probeHistoryAbsent: true` declares the suspended §history source.
- `freshness-sweep.mjs`: `pins.probeHistoryAbsent` turns a pin-declared
  absent history source into `SUSPENDED` (loud skip, listed under
  `skipped(...)`, never counted as pass) instead of unreadable-input
  exit 2. Selftest re-anchored to `~/Projects/ufo-fsd-alpha`.

## Carried debt (named, per term)

- **PQ-2** — `~/Projects/ds4cc-marketplace` gone; gate reads `ANOMALY`,
  exit 1 by design. Unblock: repo restored or PQ-2 declared dead.
- **PQ-14** — `~/Projects/plazir-15-site` gone; gate `ANOMALY` +
  sitemap `NOT-EVALUATED`. Unblock: source repo restored.
- **§history** — suspended; needs a re-anchored probe-history source or a
  declared end of the timer era. Unblock: webzites tree restored or
  `KAKE_PROBE_HISTORY` pointed at a surviving copy.

Final state: bare run exit 1 (DRIFT = the two unresolvable armed gates,
correct and loud), `--offline` exit 0, `--selftest` 10/10.
