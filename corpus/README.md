# kake-shokunin corpus

Memory for the web-properties & publishing domain (ds4cc.com, kimi.page/pro
mirrors, Pages deploys).

## Layout

- `knowledge/` — domain facts with citations (file path, command output, URL).
- `lessons/` — per-round lessons citing LOG.md round + evidence.
- `QUALITY.md` — publishing-evidence admission criteria grounded in the
  round-20 citation-locality lesson; independent spot-check still owed.
- `SOURCES.md` — where kake learns: scoped-tier source registry (contract v1),
  study paths, search log and unopened leads (round 20 resume).

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
| Sitemap/orphan audit | `knowledge/sitemap-orphan-audit.md` | URL-list→live sweep, GHP orphan impossibility proof (deploy = full-tree artifact), first baseline (103 locs live-side / 102 source-side at r16 — the delta is the unpushed plazir gate PQ-14), charter marker day-2 churn **[r20-correction 2026-10-19: the orphan direction must be checked against the actual uploaded/deployed artifact or build output, not inferred from the checkout; upload-pages-artifact excludes .git/.github and v4 excludes hidden paths by default (v5 adds include-hidden-files); branch builds also apply Jekyll's default exclusions — S001, S002, S004, S006]** |
| kimi subpath audit | `knowledge/kimi-subpath-audit.md` | link sweep + sitemap parity; ds4cc mirror 75/93 canonical locs missing all post-vintage (0 rot); `dir/` hrefs live-dead on kimi |
| Publish-queue ledger | `knowledge/publish-queue.md` | PQ-1..PQ-14 readiness: gate class, bound chats, source freshness, cheapest wins, ordering DAG (r9 baseline; PQ-14 = the plazir15-ghp 5-commit push gate found r16) |
| Freshness sweep (instrument) | `scripts/freshness-sweep.mjs` + `knowledge/freshness-sweep.md` + `knowledge/freshness-pins.json` | one read-only command re-derives the lane's whole standing-claim battery (cited paths, probe-history shape, detector deltas, PQ-12/PQ-5/PQ-2/plazir gates) against pinned baselines with exit 0/1/2/64 — pinned values live in the JSON, never copied into prose |
| Probe-delta alerting | `knowledge/probe-delta-alerting.md` + `scripts/probe-delta.mjs` | phantom-suppressed history diffing (naive 42/40-phantom → 6/0), corrected r5 veigapunk bracket, coverage holes |
| Keeper-timer status | `knowledge/keeper-timer-inert.md` | r12: keeper timer loaded/disabled/never-fired; logs frozen 09-21; charter-ghp pin = config lag + human edit (scribe is the writer; no fleet.config writer in src/); scribe push-gate failing |
| Free-read verbs | `knowledge/free-read-verbs.md` | probe/status/reconcile/sync-check (r11) + status --json/grokbots --check/bots list/bots report (r12 live): exit contracts, gap/stale predicates, 18/21/20/21 universes, clobber + corrected merge patch |
| Handoffs (webzites owner) | `handoffs/cmdProbe-merge-fix.md` | verified one-line cmdProbe merge patch (r11 F1 guard refuted; `probe <id> --all` edge covered), owner test recipe |
| Citation-local absence | `lessons/round-20.md` + `QUALITY.md` | Baseline/candidate CLI proof, exact unannotated locations, frozen input digests; round admission blocked by host route bindings. |
| GHP served-set semantics (r20) | `knowledge/ghp-served-set.md` | what an Actions artifact or branch build actually serves: .git/.github always excluded, dot paths from upload-pages-artifact v4.0.0, Jekyll skips; tar depth repro |
| GHP custom-domain source (r20) | `knowledge/ghp-custom-domain.md` | under Actions publishing the repo CNAME is ignored; the domain is the Pages setting (`cname`, `build_type` in the REST API) |
| ETag anatomy (r20) | `knowledge/ghp-etag-anatomy.md` | the recorded root ETag decodes to mtime-length (nginx format, backend identity [INFERENCE]); validator, never identity |
| Crawl scope per host (r20) | `knowledge/crawl-scope-per-host.md` | robots.txt only at the host root; sitemap scope by location; project sites share the user-site robots policy |
| Earlier round lessons (historical through r18) | core `round-{1,3,4,5,6,7,8,9,10,12,16,17,18}.md` plus named aggregator audits; later entries live in `lessons/` | Dated audit findings and source-era measurements, not current surface availability. |
| Static canonical preflight (r22) | `knowledge/static-canonical-preflight.md` | Source-backed publisher-policy comparison of a named static HTML population; canonical signals versus selection, parser/URL limits; local fixture proof under `.ufo/waves/round-22/` |

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
  full-tree artifacts, so the served set ≡ `origin/main` tree; the round-7 **[r20-correction 2026-10-19: the orphan direction must be checked against the actual uploaded/deployed artifact or build output, not inferred from the checkout; upload-pages-artifact excludes .git/.github and v4 excludes hidden paths by default (v5 adds include-hidden-files); branch builds also apply Jekyll's default exclusions — S001, S002, S004, S006]**
  sitemap sweep (103 locs live-side; 102 source-side from r16 — the delta is
  the unpushed plazir gate, PQ-14) found 0 orphans/dead listings. kimi subpaths:
  **closed 2026-09-28 round 8** — link sweep + sitemap parity baseline
  (`kimi-subpath-audit.md`). JS-rendered link surfaces: **closed 2026-09-28
  round 9** — PROPERTIES[] is a static literal; rot baseline landed
  (`knowledge/vault-properties.md`).
- kimi `apiv2` authenticated ops are capability-recorded but intentionally
  unwired; any change there is a new round's work. *(r20 correction
  2026-10-19: continuation restored from `cd5b381`; it was dropped in
  `dd4eabf`.)*
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
  bare `webzites` not on PATH (invoke `node ~/Projects/webzites/bin/webzites.mjs`), *[r20 citation-local 2026-10-19: `~/Projects/webzites/bin/webzites.mjs` absent — gone in W7, the 2026-10-12 `~/Projects` prune/migration; this citing command is a historical record, not an executable instruction; it is not executable until restored and re-checked.]*
  cmdProbe merge patch for the webzites owner (`handoffs/cmdProbe-merge-fix.md`).

## Frontier

- Complete the round-20 audit only after the host owner supplies the required
  existing alias bindings; the validated 32-scope wave is not dispatched.
  See `lessons/round-20.md` and `.ufo/round-20/routing-blocker.json`.
- Repair or locally qualify the individual deleted-source citations exposed
  by P1; a target-wide historical marker is not enough. Existing publishing
  source restoration and history restoration/retirement remain operator-owned.
- Obtain a non-author spot-check of at least one admitted and rejected
  round-20 candidate; self-review does not close discernment or promotion.
- *(r20 resume 2026-10-19)* The first bullet is now carried by the kaika
  campaign swarm (`.ufo/round-20/resume/swarm-dispatch.json`); the second is
  done for the 26 measured locations
  (`.ufo/round-20/resume/citation-disposition.json`). Open ground: canonical
  signals and JS-rendered canonicals; field performance (CWV/CrUX); WCAG 2.2;
  Jekyll/base-path tooling; Render deploys (`../PROVINCE.md` §Frontier). Named
  checks needing an operator-authorized free read: each Pages repo's
  `build_type` and workflow action pins; whether `/CNAME` is served under
  Actions; the user-site robots.txt.

## Round-21 corpus maintenance

- `lessons/round-21.md`: historical provenance and decision-log repair,
  source S019, and the inbound line-pointer correction register.
- `../scripts/corpus-contract.mjs`: runnable structural census of provenance
  fields and exact lesson Gate headings; registry in `../SKILL.md`.
- `../.ufo/waves/round-21/`: frozen red-before inputs, measured outputs,
  author-side swarm reports and pure-addition/pointer proofs.

This adds no new publishing-domain coverage. Original observations keep
their own dates, missing source trees remain operator restore-or-retire
debt, and round admission still requires the independent closure reviewer.
Round-20 outside review is now recorded in
`lessons/round-20-verifier-spotcheck.md`; older Frontier bullets are historical,
not a denial of that later review. The remaining citation/confinement bounds
are retained in the round-21 lesson.

## Round-22 frontier step

Canonical signals now have a source-backed knowledge entry
`knowledge/static-canonical-preflight.md` (S020/S021/S026/S027), and a local
publisher-policy capability is measured in the round22 report. This is
uncovered ground from the round20/21 Frontier, not another corpus-metadata
claim. JS-rendered canonicals, Google-selected canonical, live delivery,
HTTP headers, content duplication and actual operator publication remain open.
Historical Frontier and Known gaps paragraphs above retain their chronology;
the round21 verifier and correction register govern their current reading.


## Round-23 re-verification and live canonical use

Seventeen frozen units (16 historical knowledge entries and the property map) carry claim-level dated HOLD/STALE/UNVERIFIABLE rechecks; original observations remain intact. See `lessons/round-23.md` and `.ufo/waves/round-23/receipts/` (relative to the lane root). Twelve owned public surfaces were captured GET-only and preflighted: three clean, five missing a canonical under the local policy, four not-served (404). Rendering and live publishing remain outside this workflow. The formerly open static-canonical ground is in use, not a search-engine-selection claim.


## Round-24 frontier maintenance

The restored ds4cc source changes the local-state premise, not the domain boundary. Nineteen paths-gate targets now have dated reconciliation evidence (30 hash-bound citation corrections); source-tree observations remain read-only. The individual citation frontier advances through preservation-safe sidecar/EOF corrections; no original observation is relabelled live. `lessons/round-24.md` records the gate decisions and exact counters. Rendering, deployment, accounts and operator restore-or-retire decisions for the other trees remain open.

## Round-25 accessibility frontier preparation

| Area | Entry | Coverage |
|---|---|---|
| Publisher accessibility review preparation | `knowledge/accessibility-review-packet.md`, `knowledge/accessibility-review-cards.json` (S035) | Fixed WCAG 2.2 A/AA criterion cards: publisher checks, manual evidence needs and limits; packet-structure gate only, no website evaluated |

This is new publisher-side preparation ground from the WCAG frontier.
Actual accessibility evaluation, browser/assistive-technology execution,
conformance claims and publication remain open or operator/adjacent-owned.
Round24's interrupted reconciliation/replay falsification remains held and
is not repeated or satisfied by this unrelated documentation capability.

Round-25 concrete preparation handoff:
`handoffs/accessibility-preparation.md`, received by the operator.
`knowledge/accessibility-review-cards.json` carries criterion-specific
instructions and the shared authorization/evaluation-record boundary.
The corrected finite snapshot is `.ufo/waves/round-25/frozen-final/` relative
to the lane root; the original frozen/ remains historical evidence only.
No card stores an actual website result.
