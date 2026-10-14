# kake-shokunin corpus

Memory for the web-properties & publishing domain (ds4cc.com, kimi.page/pro
mirrors, Pages deploys).

## Layout

- `knowledge/` — domain facts with citations (file path, command output, URL).
- `lessons/` — per-round lessons citing LOG.md round + evidence.

## Coverage map

| Area | Entry | Coverage |
|---|---|---|
| Fleet registry & tripwires | `knowledge/fleet-registry.md` | all 21 rows, expect semantics, pruning rules |
| Publish channels | `knowledge/publish-channels.md` | GHP push-to-main, Render apps-sdk, kimi surface verbs |
| Drift detection | `knowledge/drift-detection.md` | probe / sync-check / reconcile / kimi-map; byte-vs-marker semantics |
| Mirror pitfalls | `knowledge/mirror-pitfalls.md` | kimi byte rewriting, no dir indexes, one-chat-one-slot, dead slots |
| Fire journals & exit codes | `knowledge/fire-journal-codes.md` | state/*.json journal anatomy, exit codes 1–8/64, meter-consumption truth |
| Ops automation | `knowledge/ops-automation.md` | systemd 6h probe + daily keeper timers, probe-history semantics, full CLI verb table, bots fleet |
| Origin repos | `knowledge/origin-repos.md` | 50-clone canonical-source map, byte-verified writers, 5 sourceless artifacts |
| Speedrun pipeline | `knowledge/speedrun-pipeline.md` | record→report→prep→operator-push→X-draft; redaction + fail-closed rules |
| GHP subpath spotcheck | `knowledge/ghp-subpath-spotcheck.md` | probe/reconcile coverage math, `in-sync` masking, origin/main classification, first baseline (2 352 paths, 0 rot) |
| Sitemap/orphan audit | `knowledge/sitemap-orphan-audit.md` | URL-list→live sweep, GHP orphan impossibility proof (deploy = full-tree artifact), first baseline (103 locs live-side / 102 source-side at r16 — the delta is the unpushed plazir gate PQ-14), charter marker day-2 churn |
| kimi subpath audit | `knowledge/kimi-subpath-audit.md` | link sweep + sitemap parity; ds4cc mirror 75/93 canonical locs missing all post-vintage (0 rot); `dir/` hrefs live-dead on kimi |
| Publish-queue ledger | `knowledge/publish-queue.md` | PQ-1..PQ-14 readiness: gate class, bound chats, source freshness, cheapest wins, ordering DAG (r9 baseline; PQ-14 = the plazir15-ghp 5-commit push gate found r16) |
| Freshness sweep (instrument) | `scripts/freshness-sweep.mjs` + `knowledge/freshness-sweep.md` + `knowledge/freshness-pins.json` | one read-only command re-derives the lane's whole standing-claim battery (cited paths, probe-history shape, detector deltas, PQ-12/PQ-5/PQ-2/plazir gates) against pinned baselines with exit 0/1/2/64 — pinned values live in the JSON, never copied into prose |
| Probe-delta alerting | `knowledge/probe-delta-alerting.md` + `scripts/probe-delta.mjs` | phantom-suppressed history diffing (naive 42/40-phantom → 6/0), corrected r5 veigapunk bracket, coverage holes |
| Keeper-timer status | `knowledge/keeper-timer-inert.md` | r12: keeper timer loaded/disabled/never-fired; logs frozen 09-21; charter-ghp pin = config lag + human edit (scribe is the writer; no fleet.config writer in src/); scribe push-gate failing |
| Free-read verbs | `knowledge/free-read-verbs.md` | probe/status/reconcile/sync-check (r11) + status --json/grokbots --check/bots list/bots report (r12 live): exit contracts, gap/stale predicates, 18/21/20/21 universes, clobber + corrected merge patch |
| Handoffs (webzites owner) | `handoffs/cmdProbe-merge-fix.md` | verified one-line cmdProbe merge patch (r11 F1 guard refuted; `probe <id> --all` edge covered), owner test recipe |
| Round lessons | 20 files: core `round-{1,3,4,5,6,7,8,9,10,12,16,17,18}.md` + 7 named aggregator audits | audit findings; fresh-probe corrections; journal decoder; automation+repo layer; subpath spotcheck; orphan audit; kimi subpath audit; PQ readiness; probe-delta + checklist audit; free-read suite; r12 automation-myth falsification; r16 claim-class instrument; r17 W6 catch + inert-pin hazards; r18 W7 mega-prune re-census + suspended-source semantics |

## Known gaps

- **Claim-class drift (r16).** The r16 sweep enumerated 160 quantified
  standing claims and found 15 stale; the classes it needs again each round
  (verb-outcome samples, journal shape, ETag literals, fire counts) have
  recipes in `/tmp/kake-r16/scout-claims.md` but no standing gate —
  `scripts/freshness-sweep.mjs` gates only the pinned sets. Re-run the
  inventory sweep per freshness round; **PQ-14** (plazir15-ghp push) is an
  open gate the instrument reports as `LIVE-SOURCE-GAP`, exit 1.
- The sourceless kimi artifacts now have an **extraction recipe**
  (`knowledge/vault-properties.md`): body→`index.html`→`sourceDir`→`update`;
  `ufo-fsd.kimi.page` additionally needs `recreate --new-chat --canonical=`
  (no bound chat); `plazir27runson` needs `--zip-exclude='assets/*.mp4'`;
  `ufo-fsd.kimi.pro` needs html+assets zipped. Execution remains
  operator-gated; no Origin repo, unchanged since 2026-09-21.
- Live-only orphan paths: **closed 2026-09-28** — GHP Pages deploys are
  full-tree artifacts, so the served set ≡ `origin/main` tree; the round-7
  sitemap sweep (103 locs live-side; 102 source-side from r16 — the delta is
  the unpushed plazir gate, PQ-14) found 0 orphans/dead listings. kimi subpaths:
  **closed 2026-09-28 round 8** — link sweep + sitemap parity baseline
  (`kimi-subpath-audit.md`). JS-rendered link surfaces: **closed 2026-09-28
  round 9** — PROPERTIES[] is a static literal; rot baseline landed
  (`knowledge/vault-properties.md`).
- kimi `apiv2` authenticated ops are capability-recorded but intentionally
- `webzites-probe.timer` nominally provides 6h coverage, but
  probe-history is bursty (median gap 0.45h, 42.7h hole 09-21→09-22) —
  **detection closed 2026-09-28 round 10**: `scripts/probe-delta.mjs`
  (read-only, spot/bootstrap-phantom-suppressed; runbook
  `knowledge/probe-delta-alerting.md`). Alert *delivery* (notify/systemd
  fan-out) stays with the webzites owner — not this repo.
- Operator-decision queue (r12, all filed to L0 — none are kake-executable):
  keeper timer enable-vs-retire (disabled, never fired —
  `knowledge/keeper-timer-inert.md`); lucario registry mint-or-prune
  (grokbots --check exit 1); `ufo-fsd-kimi-pro` marker collision (website-id
  2/18), `plazir27runson` marker case `Nightcall`→`NIGHTCALL`, charter-ghp
  pin `2026-09-26`→current live literal (human config edit —
  `fleet.config.json:256`; diff in `~/Projects/webzites/reports/r9-stale-markers.md`; <!-- r18 re-census 2026-10-14: ~/Projects/webzites/reports/r9-stale-markers.md absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. -->
  scribe push-gate failing since 06:05Z so churn is paused),
  plazir15 chat-binding ambiguity (vessel `1a0c2186` vs emergent `1a0de2ed`),
  bare `webzites` not on PATH (invoke `node ~/Projects/webzites/bin/webzites.mjs`),
  cmdProbe merge patch for the webzites owner (`handoffs/cmdProbe-merge-fix.md`).
