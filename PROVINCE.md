# kake-shokunin — Province

**Domain:** web properties & publishing — scopes ds4cc.com, kimi.page/pro mirrors, Pages deploys

**Owns:** the domain knowledge, playbooks, error patterns, and checklists above.
**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.

<!-- Sections below appended round 20 (2026-10-19); the four lines above are unchanged. -->

## Core

- Source-grounded audits, drift checks and source-fix guidance for the lane's
  web properties: GitHub Pages fronts, kimi.page/pro mirrors, sitemaps.
- Publishing-platform semantics the audits depend on: what a Pages deploy
  serves, where the custom domain lives, what an ETag can prove
  (`corpus/knowledge/ghp-*.md`, sources in `corpus/SOURCES.md`).
- The lane's own gates: `scripts/freshness-sweep.mjs`, `scripts/probe-delta.mjs`.
  Publishing itself stays operator-gated: kake prepares, verifies and hands off.

## Frontier

- Crawl hygiene per host (robots.txt, sitemap scope, canonical signals) — first
  entry `corpus/knowledge/crawl-scope-per-host.md`; canonical/JS rendering open.
- Field performance (Core Web Vitals, CrUX eligibility) — first entry
  `corpus/knowledge/field-performance-cwv.md` (round 28; knowledge only, no
  gate, no property measured); Jekyll/base-path build tooling — first entry
  `corpus/knowledge/pages-base-path.md` plus offline gate
  `scripts/base_path_audit.py` (round 29; no live property repaired);
  accessibility conformance (WCAG 2.2) and Render deploy semantics remain
  open. Ground moves to Core only with source-backed entries and a gate.

## Adjacent

- `tabi` drives browsers and owns client-side crawler discipline; kake owns
  publisher-side placement (robots/sitemap at the host it serves).
- `chousa` owns research method and source hierarchy; kake keeps only
  domain findings and its own `corpus/SOURCES.md` rows.
- `kagi` owns secrets and credential custody; kake records no secret values.
  The the-musketeer Chrome profile lease is contested scope (kagi/tabi/kake)
  and stays with the integrator.
- `kama` owns local model-serving endpoints; kake owns remote web properties.

## Surfaces (checked 2026-10-19 with `test -e`)

- Present: `SKILL.md`, `corpus/knowledge/`, `corpus/lessons/`,
  `scripts/freshness-sweep.mjs`, `scripts/probe-delta.mjs`.
- Absent since the 2026-10-12 `~/Projects` prune (r18 W7 annotations): the
  webzites tooling checkout, the ds4cc-marketplace source, the plazir-15-site
  source, the lucario checkout and the origin-work tree. Restore-or-retire is
  operator-owned; the corpus keeps their cites as historical records.
- Live web properties (ds4cc.com, veigapunk.github.io project sites,
  *.kimi.page/pro) were not probed in round 20 (documentation-only round).

## Round-22 publisher-side addition

`corpus/knowledge/static-canonical-preflight.md` covers the previously open
static canonical-signal ground: preferred relation semantics, explicit local
publisher policy and offline parser limits. The lane's local validator and
frozen fixtures are its operability artifact, not a claim that a live website
was repaired or a Google-selected canonical observed. The broader crawl and
JS-rendered-canonical frontier above remains open; browser execution stays tabi's
adjacent province and publication/account operations stay operator-owned.


## Round-23 live use

The publisher-side canonical tool now consumes saved GET-response HTML from owned public properties through `scripts/live_snapshot.py`; live capture is GET-only and separate from offline validation. This is not rendered-DOM observation, navigation/readiness approval or permission to publish. `corpus/lessons/round-23.md` records the outcomes; source repair and deployment stay operator-owned. A surviving burnerchrome source candidate at `~/Projects/burnerchrome` was found and read only; its mapped historical ds4cc-marketplace path remains absent.


## Round-24 restored source correction

The earlier Surfaces paragraph and round-23 burnerchrome note are historical local-state observations. On 2026-10-21 the ds4cc-marketplace checkout and its CNAME, burnerchrome, speedrun and apps-sdk subtrees are present again (checkout birth 05:19 -03; observed HEAD 1fbdb8ed). No restoration was performed by kake. Evidence: `.ufo/waves/round-24/c1-receipts/T16.json` through `T19.json` and `w1/R23ReceiptsDs4ccStale.md`. Presence enables later source rechecks; it does not establish live deployment or grant publication, browser-profile, DNS or account authority. The webzites, Plazir and Lucario observations remain separately dated.

## Round-25 accessibility preparation boundary

The WCAG frontier now has publisher-side review preparation: sourced criterion
cards and an offline inventory gate (`corpus/knowledge/accessibility-review-packet.md`,
S035). This moves preparation only into held ground, not WCAG conformance.
No actual website accessibility is evaluated. Browser/assistive-technology
execution stays separately authorized adjacent work; publishing stays with
the operator. The remaining field-performance, Jekyll and Render frontier
is unchanged. Round24's policy-stop disposition remains separate open debt.

## Round-29 base-path frontier step

The round-25 sentence above ("The remaining field-performance, Jekyll and
Render frontier is unchanged") is historical for its date. Round 28 added
field-performance knowledge, and round 29 added project-site base-path
knowledge (`corpus/knowledge/pages-base-path.md`, S040–S043) with an offline
gate (`scripts/base_path_audit.py`). The gate reads local files only; no live
property was fetched, measured or repaired, and publishing stays with the
operator. Render deploy semantics and accessibility conformance stay open.

## Round-30 Render static-site frontier step

The round-29 sentence above ("Render deploy semantics and accessibility
conformance stay open") is historical for its date. Round 30 added Render
static-site platform knowledge (`corpus/knowledge/render-static-sites.md`,
S049–S052): build and deploy on push, redirect and rewrite rule order,
dashboard response headers, custom domains and TLS. It is knowledge only, with
no gate, and no owned property recorded in local checkouts or the corpus is a
Render static site; Render web service deploys (the Docker service recorded
for `app.ds4cc.com`) and the Blueprint file stay open.
Accessibility conformance stays open. The lane's own citing-set gate
(`scripts/citing_set.py`) gained committed reason-code fixtures, repairs for the round-27 input
families that round 28 routed (duplicate keys, non-finite numbers, short ids,
repeated options) and for two round-28 residual findings (deep corpus,
`O_NOCTTY`). The round-27 identity-path, retention and unit-override families
stay open.
