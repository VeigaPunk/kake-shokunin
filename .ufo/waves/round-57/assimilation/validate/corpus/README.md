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
| Claim-count derivation (r43) | `knowledge/claim-count-derivation.md` | every count in a self-assessment document is a claim: it names its measured revision and re-derives from committed bytes with a recorded command at filing time; the able-to-fail gate is `.ufo/waves/round-43/registry_count_check.py` (red on the r42 claims, green on the r43 correction) |
| Probe-delta alerting | `knowledge/probe-delta-alerting.md` + `scripts/probe-delta.mjs` | phantom-suppressed history diffing (naive 42/40-phantom → 6/0), corrected r5 veigapunk bracket, coverage holes |
| Keeper-timer status | `knowledge/keeper-timer-inert.md` | r12: keeper timer loaded/disabled/never-fired; logs frozen 09-21; charter-ghp pin = config lag + human edit (scribe is the writer; no fleet.config writer in src/); scribe push-gate failing |
| Free-read verbs | `knowledge/free-read-verbs.md` | probe/status/reconcile/sync-check (r11) + status --json/grokbots --check/bots list/bots report (r12 live): exit contracts, gap/stale predicates, 18/21/20/21 universes, clobber + corrected merge patch |
| Handoffs (webzites owner) | `handoffs/cmdProbe-merge-fix.md` | verified one-line cmdProbe merge patch (r11 F1 guard refuted; `probe <id> --all` edge covered), owner test recipe |
| Citation-local absence | `lessons/round-20.md` + `QUALITY.md` | Baseline/candidate CLI proof, exact unannotated locations, frozen input digests; round admission blocked by host route bindings. |
| Commit-citation hygiene (round 47) | `knowledge/commit-citation-hygiene.md` + `scripts/citation_lint.py` | repository-scoped object-name resolution, exclusions, ledger reason fidelity and committed receipt identity; S136 grounds Git revision semantics only |
| GHP served-set semantics (r20) | `knowledge/ghp-served-set.md` | what an Actions artifact or branch build actually serves: .git/.github always excluded, dot paths from upload-pages-artifact v4.0.0, Jekyll skips; tar depth repro |
| GHP custom-domain source (r20) | `knowledge/ghp-custom-domain.md` | under Actions publishing the repo CNAME is ignored; the domain is the Pages setting (`cname`, `build_type` in the REST API) |
| ETag anatomy (r20) | `knowledge/ghp-etag-anatomy.md` | the recorded root ETag decodes to mtime-length (nginx format, backend identity [INFERENCE]); validator, never identity |
| Crawl scope per host (r20) | `knowledge/crawl-scope-per-host.md` | robots.txt only at the host root; sitemap scope by location; project sites share the user-site robots policy |
| Earlier round lessons (historical through r18) | core `round-{1,3,4,5,6,7,8,9,10,12,16,17,18}.md` plus named aggregator audits; later entries live in `lessons/` | Dated audit findings and source-era measurements, not current surface availability. |
| Static canonical preflight (r22) | `knowledge/static-canonical-preflight.md` | Source-backed publisher-policy comparison of a named static HTML population; canonical signals versus selection, parser/URL limits; local fixture proof under `.ufo/waves/round-22/` |
| Field performance (r28) | `knowledge/field-performance-cwv.md` (S036–S039) | LCP, INP and CLS good and poor bounds at the 75th percentile, CrUX discoverability and popularity eligibility, the CrUX API 28-day window; no property measured, no API call |
| WCAG 2.2 criterion review cards | `knowledge/accessibility-review-cards.json` | Preparation-only WCAG 2.2 success-criterion cards: a source quote, publisher check procedure, evidence needed, failure example and limitation per card; status is not-assessed and each names the shared handoff record. |
| WCAG 2.2 accessibility review packet | `knowledge/accessibility-review-packet.md` (S035) | Fixed Level A/AA WCAG 2.2 criterion population: one `not-assessed` card per criterion with located quote, publisher check, evidence needed, failure example, limitation; a local gate validates structure, metadata and quote binding, never website conformance |
| Baiduspider robots scope, wildcards and spider trap | `knowledge/baidu-friendly-crawl-guidance.md` (S329) | Baiduspider robots scope: a block on that agent binds the desktop and mobile crawlers; wildcard symbols `*` and `$`; the spider trap as a parameter-generated URL space with a robots remedy. |
| Baidu mobile-matching correspondence errors | `knowledge/baidu-mobile-matching-error-causes.md` (S312) | Baidu's mobile-matching correspondence-error list: an ajax-loaded mobile body and a Baiduspider robots block, both quoted raw; the five-item list also names an unusable mobile page, a rule-pattern format error and a wrong PC-mobile mapping; no matching algorithm or threshold stated. |
| Canonical selection vs declaration | `knowledge/canonical-selection.md` (S262) | Google's selection mechanism: a declared canonical is a hint, weighed against HTTPS, redirects and sitemap inclusion; four recognised variant classes; quotation rendering classes and the round-51 correction. |
| Per-host crawl hygiene | `knowledge/crawl-budget-consequences.md` (S273, S274) | Two admitted Google sentences: a robots block does not make Google shift the spared crawl budget to other pages unless the capacity limit is already hit (S273); emergency backoff reduces crawl rate across the whole hostname (S274); status codes unadmitted; no lane property measured. |
| Error-status crawl layer | `knowledge/crawl-error-status-table.md` (S286) | One admitted Googlebot sentence: crawling scales back when server trouble is detected; the admitted quote is a raw substring of the retained page, unlike S273's collapsed-only crawl-budget quote; no soft-404 remedy claimed. |
| Crawler identity (Googlebot subtypes) | `knowledge/crawler-identity.md` (S263) | Googlebot names two crawlers, Smartphone and Desktop; the HTTP user-agent header identifies the subtype, and both types obey the same robots.txt product token; it also lists what the entry does not establish. |
| Dynamic rendering workaround limits | `knowledge/dynamic-rendering-workaround-limits.md` (S249) | One engine's own account of dynamic rendering as a workaround, not a recommended solution: the cloaking boundary is a content condition, not a technique; error pages inherit the rendering-queue status-code rule; nothing was observed on a live crawl. |
| Local-path freshness sidecar | `knowledge/freshness-sidecar.json` | 30 entries dated 2026-10-21, each naming a cited file and line number, a `~/Projects/...` path token, the line SHA-256 as of that date, kind `absent` or `restored`, and a note carrying the `test -e` exit code and marking the citation historical. |
| Render queue status-code contract | `knowledge/js-rendering-queue.md` (S137–S139) | Status-code rule: 200 responses queue for rendering regardless of JavaScript, non-200 may skip; robots.txt check precedes the request; four publisher rules; zh-CN and ja locale restatements. |
| Link-preview metadata (r34) | `knowledge/link-preview-metadata.md` (S067–S070) | Four required Open Graph properties and what each preview field means; Facebook's undecorated canonical og:url, one og:type per URL, URL-keyed image caching and Sharing Debugger re-scrape; Slack's range-limited fetch and 30-minute global cache; Mastodon's PreviewCard entity; a source-byte census of 102 ds4cc pages. |
| Project-site base paths | `knowledge/pages-base-path.md` (S040–S043) | Publisher-side ground that a project site is published under a base path: two site kinds (S040), Liquid `relative_url`/`absolute_url` filters (S042), Vite's `base` option (S043), an offline audit over a frozen 30-case matrix; root-relative breakage is inference, no property measured. |
| Receipt integrity (round 45) | `knowledge/receipt-integrity.md` (S133) | Three receipt defect classes (counter-error, tool-absent, stale planted), the v2 binding rule's exit, note, counter-sha, mtime-window and seed gates plus a toolSha256 control binding, do-nothing reachability, 27-control and fixture counts, two named residual limits |
| Redirect/rewrite rule semantics (r46) | `knowledge/redirect-rewrite-rules.md` (S050, S135) | Render and Cloudflare Pages redirect/rewrite rule semantics: resource precedence, first-match order, dashboard versus `_redirects` placement, Cloudflare's status codes 301, 302, 303, 307, 308 with 302 default, splat and placeholder expansion; manifest fields declaring which precedence an offline audit applies. No live serving claim. |
| Render web services and Blueprint (r31) | `knowledge/render-web-services.md` (S057, S058, S059, S060) | Render's documentation for web services: the required 0.0.0.0 port bind, a Docker build context filtered by .dockerignore, health-check success at 2xx or 3xx within five seconds, and an offline key-by-key check of the lane's own render.yaml at ds4cc-marketplace commit 1fbdb8ed. |
| Render static-site deploy semantics (r30) | `knowledge/render-static-sites.md` (S049–S052) | Render Docs reading of a static site: build details and dependency install, redirect/rewrite rule matching order, dashboard response headers, custom domains and TLS, and contrasts with the GitHub Pages entries already held; four retained pages, no owned property measured |
| Offline robots.txt expectation rules | `knowledge/robots-txt-rules.md` (S011, S095, S096, S034, S098, S099, S100) | RFC 9309 robots.txt rules and this lane's offline expectation readings: access-result status handling, line and group parsing, rule matching with URL normalization, plus round-38 amendments (h) JSON numbers, (i) URL characters, (k) implicit /robots.txt allow. |
| security.txt publishing on GitHub Pages (r35) | `knowledge/security-txt-publishing.md` (S078–S080, S082–S086, S001–S002, S006) | Where `/.well-known/security.txt` lives and the duplicate rule, HTTPS and `text/plain` serving, the registered fields with cardinality, the `Expires` horizon, contact order, encryption and signing, host scope, two live files, and dot-directory handling for a Jekyll branch build versus an Actions artifact build |
| Vault PROPERTIES[] surface audit (r23) | `knowledge/vault-properties.md` (S019) | Static GET exposes the client-rendered PROPERTIES literal, so rot-checking needs no rendered DOM: 13 entries, 3 null URLs, seed-tag byte normalization, and round-23 HOLD/STALE corrections where URLs marked live are not 200. |
| Yahoo! JAPAN rel=nofollow semantics | `knowledge/yahoo-japan-rel-nofollow-semantics.md` (S374) | One operator's rel=nofollow reading: the phrase is a crawl qualifier on the link target's page, the URL may still be used to discover new pages, and the attribute is not weighed in result ordering; other operators and attribute values out of scope. |
| Yahoo! JAPAN robots refusal rules (r55) | `knowledge/yahoo-japan-robots-txt-refusal-rules.md` (S372) | root placement, directory scope, absent-file negation, case-sensitive names, meta-tag fallback |
| Yahoo! JAPAN robots pattern syntax (r55) | `knowledge/yahoo-japan-robots-pattern-syntax.md` (S373) | prefix versus end marker, wildcard scope, and the equivalence of a trailing wildcard |
| Yahoo! JAPAN robots.txt basics (r55) | `knowledge/yahoo-japan-robots-txt-basics.md` (S418) | request channel with two payloads (pages, sitemap location); root-directory lookup on each crawl, absent file = no restriction, present = follow contents |
| Yahoo! JAPAN link-target crawl restriction (r56) | `knowledge/yahoo-japan-link-target-crawl-restriction.md` (S367) | meta tag and server routes, page-vs-link-target indexing split, two glossed values |
| Yahoo! JAPAN deleted URL crawl handling (r56) | `knowledge/yahoo-japan-deleted-url-recrawl.md` (S419) | deleted URL status 200 OK vs 404 Not Found check, error-page head meta tag with unnamed value, possibility and cannot-be-configured qualifiers |
| Yahoo! JAPAN non-existent URL crawl handling (r56) | `knowledge/yahoo-japan-nonexistent-url-recrawl.md` (S420) | error page served with HTTP 200 OK is not read as an error page, the crawl continues; HTTP 404 Not Found requested instead; meta-tag index-refusal fallback where that setting cannot be made |
| Baidu dead-link types and handling (r57) | `knowledge/baidu-dead-link-types.md` (S421) | dead-link types (protocol and content kinds), the content kind's HTTP 200 answer, the 404 setting and submission workflow the page states, the crawler's periodic check; no crawl observed |
| Baidu Spider 3.0 dead-link recognition model (r57) | `knowledge/baidu-spider3-dead-link-model.md` (S422) | protocol dead links, most content dead links and redirect dead links named by the recognition model; a few-days processing statement; the best-choice preference; the index-display figure's real placement; no crawl observed |

### Frontier ground map (round 55; round-57 update)

One row per `PROVINCE.md` §Frontier ground that a held entry can be dated to
(`PROVINCE.md:22-30`): the round it entered, the entry, and the `used-by` rows
that entry names in `corpus/SOURCES.md` at base `fcaf4b85…` (155 rows); the round-55 row is
measured at the round's final revision (156 rows, S418 added) and the round-56 row at the round-56
final revision (158 rows, S419 and S420 added), not at base `e48354b7…`; the round-57 row at the
round-57 final revision (160 rows, S421 and S422 added), not at base `28fa0b23…`. Ranges
are inclusive and each id was checked individually; a row set is the entry's
`used-by` cells, not a re-adjudication of any source.

| Frontier ground | Entered in round | Entries | Rows |
|---|---|---|---|
| Crawl hygiene per host (robots.txt location, sitemap scope) | r20 | `knowledge/crawl-scope-per-host.md` | S011–S013 |
| robots.txt rule semantics, offline expectation audit | r37; repaired r38 | `knowledge/robots-txt-rules.md` | S011 S034 S095 S096 S098–S101 |
| Sitemap and orphan parity | r7; r33 source pin | `knowledge/sitemap-orphan-audit.md` | S001–S006 S065 S066 |
| Static canonical declaration | r22 | `knowledge/static-canonical-preflight.md` | S001–S006 S020 S021 S024–S034 |
| Canonical selection | r51 | `knowledge/canonical-selection.md` | S262 |
| Crawler identity (Googlebot subtypes) | r51 | `knowledge/crawler-identity.md` | S263 |
| JS rendering queue | r48 | `knowledge/js-rendering-queue.md` | S137–S139 |
| Dynamic rendering limits | r48 | `knowledge/dynamic-rendering-workaround-limits.md` | S249 |
| Crawl budget | r49 | `knowledge/crawl-budget-consequences.md` | S273 S274 |
| Crawl-error status | r50 | `knowledge/crawl-error-status-table.md` | S286 |
| Yahoo! JAPAN link attribute (`rel`) | r52; S374 re-read r54 | `knowledge/yahoo-japan-rel-nofollow-semantics.md` | S367 S372 S373 S374 |
| Baidu crawl guidance | r52; locators superseded r53 | `knowledge/baidu-friendly-crawl-guidance.md` | S329 S373 S390 S409 |
| Baidu mobile matching | r52; locators superseded r53 | `knowledge/baidu-mobile-matching-error-causes.md` | S312 S390 S409 |
| Yahoo! JAPAN robots refusal file, pattern syntax, basics | r55 (lands this round) | `knowledge/yahoo-japan-robots-txt-refusal-rules.md` `knowledge/yahoo-japan-robots-pattern-syntax.md` `knowledge/yahoo-japan-robots-txt-basics.md` | S372 S373 S418 |
| Yahoo! JAPAN crawl handling (link-target restriction, deleted URL, non-existent URL) | r56 (lands this round) | `knowledge/yahoo-japan-link-target-crawl-restriction.md` `knowledge/yahoo-japan-deleted-url-recrawl.md` `knowledge/yahoo-japan-nonexistent-url-recrawl.md` | S367 S419 S420 |
| Baidu dead-link handling (dead-link types, Spider 3.0 recognition model) | r57 (lands this round) | `knowledge/baidu-dead-link-types.md` `knowledge/baidu-spider3-dead-link-model.md` | S421 S422 |
| Field performance (CWV, CrUX) | r28 | `knowledge/field-performance-cwv.md` | S036–S039 |
| Jekyll/base-path build tooling | r29 | `knowledge/pages-base-path.md` | S040–S043 |
| Render static sites | r30 | `knowledge/render-static-sites.md` | S049–S052 S061 |
| Render web services and Blueprint | r31 | `knowledge/render-web-services.md` | S057–S060 S062 |
| Link-preview metadata | r34 | `knowledge/link-preview-metadata.md` | S067–S070 S073 |
| security.txt publishing | r35 | `knowledge/security-txt-publishing.md` | S001 S002 S006 S078–S080 S082–S086 |
| Accessibility review preparation | r25 | `knowledge/accessibility-review-packet.md` | S035 |

Two dated row sets hold no entry of their own: the round-39 sitemap-file audit
(S102–S109, `used-by` only `corpus/lessons/round-39.md`; tool
`scripts/sitemap_audit.py`) and the round-53 superseding rows S416/S417
(`used-by` only `corpus/lessons/round-53.md`, correcting the S329/S312
locators). The round-55 row's three entry paths are absent at base by design,
and S418 is not in the base registry; the round-56 row's three entry paths are
absent at its base `e48354b7…`, and S419 and S420 are not in that registry; the
round-57 row's two entry paths are absent at its base `28fa0b23…`, and S421 and
S422 are not in that registry.

**Untouched ground** — PROVINCE frontier items no entry holds yet:

- Accessibility conformance (WCAG 2.2) — `PROVINCE.md:29`. Only the round-25
  preparation packet exists, its cards are `not-assessed`, and
  `PROVINCE.md:77-78` says the packet is not conformance and no website was
  evaluated.
- JS-rendered canonical and rendered-DOM observation — `PROVINCE.md:23`
  ("canonical/JS rendering open"); `PROVINCE.md:361-362` keeps JS rendering open
  and leaves anything that executes a browser to tabi.
- Render live deploy facts (plan, region, domains, deploy trigger) —
  `PROVINCE.md:29`; `PROVINCE.md:120` records they stay unknown from the file.
- Sitemap parsing/scope, crawler-specific extensions, live fetch, redirects and
  caching — `PROVINCE.md:302-303`.
- Sitemap gzip, text/RSS sitemaps, robots `Sitemap:` cross-submission —
  `PROVINCE.md:335-336`.

Held, but ungated or unmeasured (an entry exists; no gate, no owned property
observed): field performance `PROVINCE.md:25-26`, crawl budget
`PROVINCE.md:344`, canonical selection and crawler identity `PROVINCE.md:361`,
the eleven per-engine entries (the round-52 trio `PROVINCE.md:382`, the round-55 Yahoo! robots trio
`PROVINCE.md:397`, the round-56 crawl-handling trio `PROVINCE.md:423`, the round-57 Baidu pair
`PROVINCE.md:441`). The "Untouched ground" lines about
crawler-specific extensions and robots `Sitemap:` cross-submission predate round 55: one operator's own
pattern-syntax and sitemap-location statements are now held
(`knowledge/yahoo-japan-robots-pattern-syntax.md`,
`knowledge/yahoo-japan-robots-txt-basics.md`), as documentation only, not observed crawler behaviour.

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

- Round-47 S136 admit and a rejected-source-candidate spot-check remains owed to a non-author: this seat recorded no rejection and its prepared L2 wave was undispatched (`lessons/round-47.md` §Gate).

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


## Coverage — round 35 (2026-10-22)

| Area | Entry | Coverage |
|---|---|---|
| security.txt publishing on GitHub Pages (r35) | `knowledge/security-txt-publishing.md` (S078–S080, S082–S085, plus S006 re-opened) | RFC 9116's placement rule — the file belongs under the domain's `/.well-known/` path, a legacy top-level copy may exist or redirect, and the well-known copy wins when both exist — on the reserved well-known prefix of RFC 8615 and the registry's permanent `security.txt` entry; the fields a publisher must or may carry: `Contact` always present, a single `Expires` in RFC 3339 form with the recommendation to keep it under a year ahead, an https-only `Canonical` naming the retrieval URI and the rule that a file not listing its own URI should not be trusted, `Encryption`, `Acknowledgments`, `Policy`, `Hiring` and `Preferred-Languages`; `text/plain` with default `utf-8`, HTTPS serving, domain-only scope and the recommended OpenPGP cleartext signature (S078). The publisher-facing generator's step that creates the file under the `.well-known` directory of the project (S079), and the GitHub Pages build path: Jekyll branch builds skip dot-leading paths by default (S006) with `include:` forcing them back in (S080), while Actions artifact uploads exclude dotfiles at v4.0.0 and expose `include-hidden-files` at v5.0.0 (S001, S002). Two published files, `github.com` and `www.google.com`, are recorded as body text only (S084, S085) |

`corpus/SOURCES.md` gains rows S078–S085 opened 2026-10-22T22:00:48–22:02:20Z
with one public GET each (`.ufo/waves/round-35/sources/receipts.json`): S078
(RFC 9116), S079 (securitytxt.org), S080 (Jekyll configuration options), S082
(RFC 8615), S083 (IANA well-known URIs registry), S084 and S085 (the two
published files) ground the entry; S081 (Wikipedia's security.txt article) is
rejected as secondary and grounds no claim. S006 is a re-open of an existing
row, not a new one. Each of the nine retained rows carries a body sha256 and a
visible-text sha256 in the round-35 receipts, so a later re-open compares
digests instead of re-reading prose. The entry is offline publisher knowledge
and carries no gate: the round-35 counter for it reads the entry text, its
cites, its size and the retained source texts, so it cannot observe a served
file. A wave-1 source-side census of the public ds4cc-marketplace tree at
`7fc6aa2f` reports no `.well-known` path, no `security.txt` and no
`_config.yml`, with a root `.nojekyll` and a single Pages workflow pinned to
`upload-pages-artifact@v3`
(`.ufo/waves/round-35/w1/ScoutDs4ccWellKnown.md`). Wave-1 seats also read
public documentation, the RFC-Editor errata and a ten-host public
`/.well-known/security.txt` census (their reports under
`.ufo/waves/round-35/w1/`); none of those reads reached an operator-owned
property, and no security.txt was authored, added to a site, built or
deployed. S084/S085 were retained as body text, so their
response headers, TLS and redirects are unobserved and no conformance to the
RFC's serving requirements is claimed for them. Vulnerability handling itself
(report intake, triage, remediation, disclosure timing, bounty and policy
operation) stays outside this province, and writing, building or deploying the
file on an owned site is an operator-owned publishing action.

## Coverage — round 37 (2026-10-23)

| Area | Entry | Coverage |
|---|---|---|
| Offline robots.txt expectation audit (r37) | `scripts/robots_audit.py` (S011, S095) | A local manifest supplies each check's URL, user agent, expected decision, status and (for 2xx) local robots file; the offline audit compares the expected decision with RFC 9309 access rules and reports policy or input findings. |
| Offline robots.txt expectation audit repair (r38) | `scripts/robots_audit.py` (S011, S034, S098, S099, S100) | Round-37 C1 was not admitted; round 38 re-claims the tool as C2: (h) non-JSON constants and any-length integers, (i) RFC 3986 ASCII character set in `url`, (k) implicit `/robots.txt` allow on the normalized path. Counter v3 (20 of 20) puts every stdlib-delegating control at or below 13; measured 8 → 20 at `3ed8e15c`. Synthetic, offline; no fetch, redirect, cache or crawler-extension claim. |

The contract reads local inputs only and makes no network requests or writes; its cases are synthetic, not live fetch observations. Live fetch/redirect behavior, caching, crawler-specific extension behavior and sitemap handling remain open; unknown records including `Sitemap` and `crawl-delay` are ignored. Browser-driven/client-side crawler discipline remains tabi's province; kake's boundary is publisher-side robots/sitemap placement (Round-37 C1 contract; PROVINCE.md, Adjacent; S012–S013).

Knowledge entry: `corpus/knowledge/robots-txt-rules.md`.

## Round-39 frontier step

Sitemap files moved from Frontier to an exploratory capability: `scripts/sitemap_audit.py` (round 39,
not counter-admitted; `../SCORECARD.md` "Round 39 — C1 verdict"). Sources S102–S109 (protocol, XSDs,
W3C Datetime, XML 1.0, Namespaces, XSD Datatypes, sitemaps.org FAQ, Yandex). Still frontier: a sealed
key that kills the 15 round-39 single-sentence breaks and the regex reader; gzip; live fetch; text and
RSS sitemaps; robots `Sitemap:` cross-submission; the five build deviations in the round-39 SCORECARD
corrections.
