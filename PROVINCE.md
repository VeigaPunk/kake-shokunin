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

## Round-31 Render web-service frontier step

The round-30 sentence above ("Render web service deploys … and the Blueprint
file stay open") is historical for its date. Round 31 added Render
web-service and Blueprint knowledge (`corpus/knowledge/render-web-services.md`,
S057–S060): port binding, Docker builds, health-check rules and the
Blueprint keys, with an offline key-by-key check of the lane's own
`render.yaml` at ds4cc-marketplace `1fbdb8ed`. It is knowledge only, with no
gate; nothing live was fetched and no deploy was made. The live service's
plan, region, domains and deploy trigger stay unknown from the file.
Accessibility conformance stays open. The citing-set fixture runner gained
containment for five hostile fixture shapes (`scripts/citing_set_hostile_selftest.py`);
the round-27 families listed in round 30 stay open.

Round-31 wave-2 narrowing (`.ufo/waves/round-31/a2-w2/ReviewProvinceReadme.md`
F1, F2, F4): "nothing live was fetched" above means no operator-owned property
was fetched or measured and no deploy was made; the round's only live fetches
were the public Render Docs pages S057–S061 (one GET each, 15:41:23–29Z). The
refusals live in the runner `scripts/citing_set_selftest.py`;
`scripts/citing_set_hostile_selftest.py` is the committed check of them. S061
also corrected `render-static-sites.md` (its "Round-31 corrections").

## Round-33 frontier step

Correction (round-32 routed item 5): line 122 above says "five hostile
fixture shapes"; the committed hostile-spec set has six since round 32
(P1–P6 under `scripts/fixtures/citing-set-hostile/`). Round 33 keyed P6 on the
runner's structured refusal `code` (`reason_code`) instead of message text.

The ds4cc-marketplace source the corpus reads moved upstream from `1fbdb8ed`
to `7fc6aa2f` (one commit, three `/magga/frostbite/` pages, sitemap 97 → 100
locs). The corpus now records that commit's sitemap, page canonicals and the
forge's deploy-run record (S065, S066;
`corpus/knowledge/sitemap-orphan-audit.md` round-33 sections). Source-side
and forge-record only: no operator-owned property was fetched and nothing
was deployed. The round's only network reads were the public GitHub
repository clone and two GitHub API run listings.

Correction (round-33 wave-2 `CriticC2Verdict`): "The round's only network
reads were the public GitHub repository clone and two GitHub API run
listings" above is too narrow. The L1 also ran `git ls-remote`, and wave
seats made further public github.com reads (other clones, `ls-remote`, the
commit page, `gh api` run, deployment and workflow listings, two refused
unauthenticated API requests; `.ufo/waves/round-33/w1/*.md`,
`w2/ScoutUpstreamHeadNow.md`). All went to public GitHub; none reached an
operator-owned property.

## Round-34 link-preview frontier step

Link-preview metadata — the Open Graph properties a platform reads to build a
card for a shared URL — enters the Frontier as held ground with a source-backed
entry and an offline gate. The entry,
`corpus/knowledge/link-preview-metadata.md`, is grounded in S067 ogp.me, S068
Meta's sharing guide for webmasters, S069 Slack's robots page and S070
Mastodon's PreviewCard entity, and states the ds4cc Open Graph census of the
retained upstream tree at `7fc6aa2f`: 102 pages, 87 with `og:title`, 87 with
`og:type`, 87 with `og:url`, 1 with `og:image`, 1 with all four, and 87 whose
`og:url` equals the page canonical. The gate, `scripts/link_preview_audit.py`,
reads a version-1 manifest of local HTML pages and absolute page URLs and,
network-free, reports a missing one of the four required properties (S067),
more than one `og:type` (S068), a non-absolute `og:url`, and an `og:url`
differing from the first `<link rel=canonical>` resolved against the page URL.
Exit, verdict and finding shapes and the 28 frozen cases are in
`.ufo/waves/round-34/c1-matrix.json`; the counters are
`.ufo/waves/round-34/c1_matrix_count.py` and `c2_source_census.py`.

The Frontier paragraph at line 30 says ground moves to Core only with
source-backed entries and a gate. Both conditions are supplied: the entry's
quotes are exact substrings of the retained text, and the gate has a frozen
case matrix and a counter that rejects four constant implementations (although a
lookup-table tool also scores it; `corpus/lessons/round-34.md` mistake row 4), plus a
29-fixture selftest `scripts/link_preview_selftest.py`. The
round takes this ground from open to held Frontier ground, not Core; no Core
line is added and no older line is rewritten.

Nothing live was observed: the gate reads local files only, and the sources
were opened with one public GET each at 20:57Z (S067–S072) and 21:08–21:09Z
(S073–S077) (`.ufo/waves/round-34/sources/receipts.json`); wave-1 seats made further
ordinary GETs of public documentation and the public ds4cc-marketplace repository, listed
in their reports. No
operator-owned property was fetched. Open: live platform rendering (no card
was requested or observed; Slack's link robot reads tags over HTTP Range and
fetches referenced media, S069; Mastodon generates a PreviewCard from Open
Graph tags, S070); X card tags, whose markup URL S071 now redirects to a
generic documentation index and so grounds nothing; image checks beyond a
non-empty `og:image` (no fetch, MIME, dimension, HTTPS or reachability test);
`name=` meta forms, the other `og:*` properties and per-type extra required
properties (S067). The census observes source bytes and repairs nothing: 101
of 102 pages carry no non-empty `og:image`.
