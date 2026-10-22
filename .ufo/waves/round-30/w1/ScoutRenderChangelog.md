# Round 30 wave 1 scout — Render changelog, freshness check for C2

Seat: KakeR30.ScoutRenderChangelog. Question: which Render changelog entries of the last 12
months touch static sites, redirects, headers, custom domains or TLS, and does any contradict
the S049–S052 text held in `.ufo/waves/round-30/sources/`?

**Answer: none found inside the 12-month window (2025-10-22 .. 2026-10-22). No contradiction of
S049–S052, and two in-window entries corroborate the docs.**

## Method (all GET only, ordinary curl, no browser, no challenge encountered)

Sandbox `/fast/scratch/hyaku/kake-r30/w1/ScoutRenderChangelog/`.

1. `mkdir -p …/ScoutRenderChangelog` — exit 0.
2. `curl -sS -L --max-time 45 -A '<Chrome UA>' -o changelog.html -w … https://render.com/changelog`
   → `http=200 size=739984 url=https://render.com/changelog`, exit 0, 2026-10-22T12:03:29Z
   (sha256 `cfc4e4be6c0ff556f9ae63cb3112ff221e2fd6863c27a1200708aff53123634f`).
   The index is a server-rendered list of 166 entries, 2026-10-01 back to 2023-03-31, with no
   pagination control (`?page=`, "load more" absent), so the 12-month window is covered
   continuously: 44 entries, newest 2026-10-01, oldest 2025-10-27.
3. Fetched the page's advertised feeds (`<link rel=alternate>` in the head):
   `feed.json` → `http=200 size=14583` (10 newest items, sha256 `92cf8e289e8799d945b84e6b3f29544e287023018cda67b4fb7fa8528f38260f`),
   `feed.xml` → `http=200 size=15079`. A guessed sibling `feed.js` → 404, not linked, unused.
4. Fetched every index entry page since 2025-04-01 (window plus five months of margin), 77 URLs,
   `xargs -P 8` over curl: `awk` tally `77 200`, exit 0, 12:04–12:05Z. Saved under `pages/`.
   Parsed article bodies (`.prose-docs` region) to `bodies.json`; index dates re-derived from each
   page matched the index for 77/77 pages, so the date parser is validated.
5. Keyword scan over the 44 in-window bodies (footer navigation stripped) for
   `static site|static-site|redirect|rewrite|response header|custom domain|TLS|certificate|apex|www\.|edge cach|CDN|prune|invalidate|CNAME|DNS|header`.
   Zero semantic hits other than the two corroborations below; every other "Static Sites" string
   was site-footer navigation.

## Findings — entries since 2025-10-22

* **Static sites, redirects, rewrites, response headers, TLS certificates: no entries.** The whole
  166-entry index contains no title mentioning redirect, rewrite, response header, TLS or
  certificate changes at all.
* **Custom domains (pricing only), 2026-04-23, "Updated plans for Render workspaces"**
  <https://render.com/changelog/updated-plans-for-render-workspaces> — saved
  `pages/updated-plans-for-render-workspaces.html` (sha256 `c16c5c01ba0a74c5163ced604fe08fc3a4155a88706370202fcb2bd4d6f04bb5`).
  Quote at body offset 823: "Each workspace plan includes baseline usage for: Custom domains
  ($0.25/month for each additional domain) Build pipeline minutes ($5 for each additional 1000
  minutes) Bandwidth ($0.15 for each additional GB)". Corroborates S052.txt:1 @off 2975 ("Each
  custom domain you add beyond this amount costs $0.25 per month"); it states no included-domain
  counts, so the S052 table "Hobby 2 Pro 15 Scale 25" (@off 2858) is not contradicted.
* **Static site build UI, 2026-05-11, "Change your service's backing repo or image in the Render
  Dashboard"** — quote at body offset 550: "(For static sites, you specify your content's
  Publish Directory instead of a start command.)" and "you cannot change an existing service's
  type (between web service, static site, and so on)". Dashboard workflow only; S049–S052 say
  nothing about changing a backing repo, so no conflict.

## Nearest entries, just outside the window (report these if the claim is stated as a year)

* 2025-10-17 "Web service edge caching now supports all file types" (5 days before the cutoff)
  <https://render.com/changelog/web-service-edge-caching-now-supports-all-file-types> — saved
  `pages/web-service-edge-caching-now-supports-all-file-types.html` (sha256 `b0a5d11530010c6d32ea7152a290fc353a3c048914f76e2c9a0b433e7389689e`).
  Offset 34: "Edge caching for web services now includes the option to cache response data for all
  file types—not just for a predefined list of common static file types (like images and PDFs)."
  Offset 466: "make sure to set proper Cache-Control headers for all of your service's dynamic
  responses before enabling this option." Web services only; it does not change the static-site
  header semantics in S051, nor S049's CDN behaviour.
* 2025-10-02 "Enterprise orgs can set inbound IP rules for web services and static sites" (20 days
  before the cutoff) — offset 34: "Enterprise orgs on Render can now set inbound IP rules for the
  following: Individual web services and static sites An entire environment An entire workspace".
  This is a new enterprise control over an otherwise-uncovered topic; it adds a feature rather
  than altering anything S049–S052 assert.
* 2025-08-13 edge caching GA and 2025-07-16 early access (both web services, "similar to static
  sites"): the GA text reads "You can now enable edge caching for any paid web service … Backed by
  a global CDN". 2024-04-09 "Static site assets now built and persisted in the same region as
  other services" predates the window.

## Contradiction check against the held docs (no contradiction found)

Docs statements checked: S049.txt:1 @3894 "Render serves your site over a blazing-fast, reliable,
and secure global CDN"; @4875 "immediately invalidate our CDN caches so your users always see the
latest working version of your site"; @5412 "Render uses Let's Encrypt and Google Trust Services to
automatically issue and renew TLS certificates for every site and service"; S052.txt:1 @3044
"Render automatically creates and renews TLS certificates for all custom domains, including
wildcard domains." Nothing in the window's 44 entries touches issuance, renewal, CAA, wildcard
handling, redirect ordering, header precedence or CDN invalidation, so no held quote is stale or
falsified by the changelog.

## What I did not verify

* Whether the changelog index lists every post Render publishes: the JSON feed carries only the 10
  newest, the index has no pagination, and no sitemap or archive page was opened (neither is
  linked from the changelog page).
* Docs-side editorial updates that never get a changelog post, incidents/status history, and the
  Render support or feedback sites.
* Entry pages older than 2025-04-01 were not fetched (title-only evidence for the 2024 entry).
* No live request to any owned property, no freshness-sweep/probe-delta/live_snapshot run, no jj or
  git mutation. No tool installed.

## Delivered artefacts (sandbox, absolute)

* `/fast/scratch/hyaku/kake-r30/w1/ScoutRenderChangelog/changelog.html`, `feed.json`, `feed.xml`
* `/fast/scratch/hyaku/kake-r30/w1/ScoutRenderChangelog/pages/` — 77 entry pages, all HTTP 200
* `/fast/scratch/hyaku/kake-r30/w1/ScoutRenderChangelog/{entries.json,sel.json,urls.txt,fetchlog.txt,bodies.json,page_texts.json,summary.json}`
  — `summary.json` holds the 44 in-window entries and the 5 topic-adjacent entries with URLs.
