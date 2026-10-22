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
| Field performance (r28) | `knowledge/field-performance-cwv.md` (S036–S039) | LCP, INP and CLS good and poor bounds at the 75th percentile, CrUX discoverability and popularity eligibility, the CrUX API 28-day window; no property measured, no API call |

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

## Round-26 source recheck

All 32 prior external SOURCES rows were re-fetched 2026-10-21 and hold at
their anchors (`.ufo/waves/round-26/rechecks/`). The five platform/canonical
knowledge entries citing them carry an appended "Round-26 source recheck"
section: dated HOLD record plus 8 `[r26-recheck S0NN STALE]` statement
corrections. No coverage-map ground was added; this is quality maintenance.

Falsify-wave final: nine knowledge entries were rechecked (the five above plus
the round-20 correction tails in publish-channels, sitemap-orphan-audit,
ghp-subpath-spotcheck and speedrun-pipeline). Final ledger: 313 row-statement
units, 7 STALE corrections and 4 earlier tags reclassified as precision notes.
The 8-correction figure above is the pre-falsify candidate. S024/S025 `used-by`
now also names static-canonical-preflight; the round-26 lesson logs old→new.

## Round27 repair-first source adjudication

Round26 remains **rejected-honest-stop**, not admitted: its32/32 row receipts
are real, but its full knowledge-entry citing-set clause omitted the grouped
S001–S006 recommendation at `knowledge/static-canonical-preflight.md:53–54`.
The non-author verifier records that gap; a structural green counter did not
complete the claim.

Round27 separately records the complete finite knowledge-file obligation in
`.ufo/waves/round-27/{c1-before,pairs,discovered-pairs}.json`:57 original pairs
and one conservatively included embedded evidence-report reference. The six
grouped sources are individually source-grounded, the recommendation is labelled
local synthesis, and unsupported attributions receive append-only corrections.
Historical metadata and retry-provenance pairs are judged, not discarded or
marketed as fresh platform observations.

The new range-aware gate checks pair presence against a derived current input;
it does not prove semantic source support, every statement true, perpetual
freshness or website conformance. Lesson: `lessons/round-27.md`. The broader
outside-knowledge corpus policy and excluded-source populations remain explicit
scope debt, not a secretly reduced denominator. Domain frontier/ownership and
round24's unresolved policy-stop are unchanged.

Strict acceptance note: full review coverage is not full C1 success. Its
frozen after-clause requires HOLD/supported STALE, never UNVERIFIABLE counted
decided. Six inherited unknown statement units in two pairs remain explicit;
C1 is unprovable if they are unresolved. The lesson/disposition and stricter
counter distinguish reviewed from decided. No structural green, new C2
capability or source-group repair silently lowers that bar.

Final carry-audit qualification: raw r26 sum(statements)=313 remains unchanged
but mixes counting conventions; it is not a semantic unit denominator.
Known unresolved units are7 across3 pairs after the lost S007 historical
representation unit is disclosed in round27 carry-errata.json. The earlier
six-unit description is the old field sum only. C1 remains unprovable while
these unknowns persist; complete review coverage is not strict support.

Round27 closes author-side as an honest stop, **not admitted**: review58/58
is distinct from strict55/58, and the full C2 input/interface claim is
unprovable despite its exact16/16 finite result, real29/Git30 tests and killed
mutants. The scripts are candidate evidence, not production admission or
general sanitization guarantees. Current interpretation, measured receipts
and explicit failures are under round27 current-interpretation.json,
counter-version-chain.json, verification/ and unresolved-acceptance.json.
No new frontier/capability/rank is admitted here; Main owns independent closure.

Round27 independent non-author closure (hyaku): **rejected-honest-stop, admitted false** —
C1 freshness and C2 operability both stay unprovable; finite16/16 is a bounded component,
not an admission predicate. No capability, promotion or scalar change is granted.
Bounded no-harm covers26knowledge prefixes,7older scripts and279r26 wave files;
original targets, conformance exceptions, r24 policy-stop and18out-of-population pairs
remain unchanged. Decision, revisions and routed defects:
`lessons/round-27-verifier-spotcheck.md`. The round closes negatively; its full claims
remain unproved and its scripts remain unadmitted candidate evidence.

## Round-28 field-performance frontier step

New entry `knowledge/field-performance-cwv.md` holds the Core Web Vitals good
and poor thresholds, the 75th-percentile rule, the metric lifecycle, CrUX
eligibility and the CrUX API data window, from S036–S039 opened 2026-10-22.
It is knowledge without a gate: field performance stays in the Frontier, no
property was measured and no API call was made. Round-27 routed defect 1 (the
citing-set gate interface) is repaired in `scripts/citing_set.py` at
`b5d423f`; defects 2–4 are carried as `QUALITY.md` criteria in "Counters and
field evidence — round 28". Lesson: `lessons/round-28.md`.

## Round-29 base-path frontier step

| Area | Entry | Coverage |
|---|---|---|
| Project-site base paths (r29) | `knowledge/pages-base-path.md` (S040–S043) + `scripts/base_path_audit.py` | A GitHub Pages project site is served under `https://<owner>.github.io/<repo>/`, so a root-relative reference such as `/style.css` leaves the site; the source-backed parts are the two site kinds and the project-site default location `http(s)://<owner>.github.io/<repositoryname>` (S040), the `username.github.io` repository-naming rule, project pages in a `gh-pages` branch or `docs` folder, and the local `jekyll serve --baseurl ""` override (S041), the Liquid `relative_url` and `absolute_url` filters that prepend the `baseurl` (S042), and the Vite `base` option, which defaults to `/` and must be `/<REPO>/` for a project site (S043). The gate part is an offline, manifest-driven audit of page references against a declared base path, with its 30-case frozen matrix and tool contract at `.ufo/waves/round-29/c2-matrix.json` (relative to the lane root); no live property was fetched, measured or repaired |

This moves the Jekyll/base-path build-tooling ground from the open list to held Frontier ground (PROVINCE.md: first entry plus offline gate; not Core). The
entry is grounded in four primary sources opened with one public GET each on
2026-10-22 (HTTP 200); retained bodies, visible text and receipts are at
`.ufo/waves/round-29/sources/` (lane root: `S040.txt` … `S043.txt`,
`receipts.json`). The gate is offline by contract: it reads a local manifest
and local HTML files and never contacts a property, so the round repaired
nothing live and published nothing. Counters:
`.ufo/waves/round-29/c1_quote_truth.py` (a quote must be an exact substring of
the retained visible text, at most 25 words) and
`.ufo/waves/round-29/c2_matrix_count.py` (the 30 frozen matrix cases, compared
on exit, verdict and finding tuples).

Still open: Jekyll and Liquid base-path handling on a real Pages build, Render
deploy semantics, accessibility conformance, and the operator-authorized reads
named in the Frontier above. The round-25 statement "the remaining
field-performance, Jekyll and Render frontier is unchanged" is historical as
of 2026-10-21 and now carries the base-path step above.

## Coverage — round 30 (2026-10-22)

| Area | Entry | Coverage |
|---|---|---|
| Render static sites (r30) | `knowledge/render-static-sites.md` (S049–S052) | Render's own documentation for static sites: every push to the deployed branch rebuilds the site, each build is atomic, and a build that succeeds is deployed and the CDN caches are invalidated; redirect and rewrite rules apply only where no resource exists at the path, first matching rule wins, otherwise 404; custom response headers are set per relative path in the dashboard and match every attached custom domain; custom domains get automatic TLS and an HTTP to HTTPS redirect and keep the onrender.com host unless it is disabled. Knowledge only: no gate, nothing live was measured, and no owned property recorded in local checkouts or this lane's corpus is a Render static site (a site set up only in the Render dashboard would leave no local trace). |

This takes the static-site part of the "Render deploy semantics" ground from
the open list to held Frontier knowledge (no gate, so not Core). Render web
service deploys (the lane's one recorded Render property is the Docker web service
`ds4cc-marketplace-app`, recorded for `app.ds4cc.com`; `knowledge/publish-channels.md`) and the Blueprint file
(`render.yaml` fields such as `staticPublishPath`, `routes`, `headers`,
`domains`) stay open: wave-1 scouts read those pages but the round retained
them as leads, not registry rows. The round-29 sentence above ("Still open: …
Render deploy semantics …") is historical for its date.

## Coverage — round 31 (2026-10-22)

| Area | Entry | Coverage |
|---|---|---|
| Render web services and Blueprint (r31) | `knowledge/render-web-services.md` (S057–S060) | Render's own documentation for web services: deploy on push, bind host 0.0.0.0 and default port 10000; Docker builds from the repository Dockerfile with build arguments and `.dockerignore`; health checks (2xx or 3xx within five seconds, deploy cancel after 15 minutes, routing stop at 15 seconds and restart at 60 seconds, Host header); Blueprint file location, the keys the lane's `render.yaml` uses, `sync: false` and the values an existing service keeps. Includes an offline check of `render.yaml` blob `d17ab7e5` at ds4cc-marketplace `1fbdb8ed`. Knowledge only: no gate, nothing live measured. |

Render DNS records for root domains (S061) are added to
`knowledge/render-static-sites.md` as a round-31 correction. Accessibility
conformance and crawl or JS-rendered canonical signals stay open.

Round-31 wave-2 narrowing (`ReviewProvinceReadme` F3): the health-check
routing stop and restart apply after an instance "fails consecutive health
checks" for 15 and 60 seconds (S060), not at a fixed time; "nothing live
measured" means no operator-owned property was measured.

## Coverage — round 33 (2026-10-22)

| Area | Entry | Coverage |
|---|---|---|
| ds4cc source pin advance | `knowledge/sitemap-orphan-audit.md` "Round-33 ds4cc source pin 7fc6aa2f" and "Round-33 wave-1 additions" (S065, S066) | Upstream `7fc6aa2f`: sitemap 100 locs re-derived from retained bytes, three new pages' canonicals clean under the offline policy, sitemap-to-tree parity, the Pages deploy run and a failing apps-sdk test workflow; older counts marked historical; live serving not observed |
| Citing-set runner | `SKILL.md` "Citing-set runner — round 33" | Structured refusal codes and `reason_code`; per-run default scratch; routed low items repaired; Git-pin mutants still open |

`freshness-pins.json` `pq2Remote` and `sitemapStatus` are flagged stale, not
re-pinned (needs the sweep's armed section).

## Coverage — round 34 (2026-10-22)

| Area | Entry | Coverage |
|---|---|---|
| Link-preview metadata (r34) | `knowledge/link-preview-metadata.md` (S067–S070) | The Open Graph properties a platform reads to build a card for a shared URL: the four required properties and their meanings (S067); each URL is a single object, so multiple `og:type` values are not possible, and `og:url` is the canonical URL without session variables or counters (S068); Slack's link-expanding robot reads oEmbed and Twitter Card / Open Graph tags with HTTP Range requests and fetches referenced media to check validity (S069); Mastodon's PreviewCard is generated from Open Graph tags (S070). States the ds4cc census of the retained `7fc6aa2f` tree: 102 pages, `og:title` 87, `og:type` 87, `og:url` 87, `og:image` 1, all four 1, `og:url` equal to canonical 87. Platform rendering, X card tags and image validity are not covered |
| Offline link-preview audit (r34) | `scripts/link_preview_audit.py` and `.ufo/waves/round-34/c1-matrix.json` | A version-1 manifest of local HTML pages and absolute page URLs is audited network-free for a missing required property, more than one `og:type`, a non-absolute `og:url` and an `og:url` differing from the first canonical link resolved against the page URL; clean exits 0, policy findings 1, input findings 2, usage 64. 28 frozen cases, four constants each required to fail at least one case; counters `c1_matrix_count.py` and `c2_source_census.py` |

`corpus/SOURCES.md` gains rows S067–S077 opened 2026-10-22: S067–S070 and
S073 (Discord link previews) mined; S071 (X card markup, now a redirect to a
generic documentation index), S072 (GitHub repository social preview), S074
(Telegram Bot API) and S075 (LinkedIn Post Inspector shell) rejected; S076
(oEmbed) and S077 (jekyll-seo-tag) queued. X card tagging stays open. The census is
source-side: no operator-owned property was fetched, no card was rendered and
no page was repaired.
