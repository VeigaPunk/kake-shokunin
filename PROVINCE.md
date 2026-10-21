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
- Field performance (Core Web Vitals, CrUX eligibility), accessibility
  conformance (WCAG 2.2), Jekyll/base-path build tooling, Render deploy
  semantics. Ground moves to Core only with source-backed entries and a gate.

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
