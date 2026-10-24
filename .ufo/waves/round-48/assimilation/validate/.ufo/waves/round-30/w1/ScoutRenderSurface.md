# C2 recon — Render static-site facts beyond S049–S052 (seat KakeR30.ScoutRenderSurface)

Scope: read the four retained texts; open the pages they link that bear on publishing a static site
(deploys, blueprint spec for static sites, preview environments). One GET per page, render.com/docs only,
2026-10-22T12:03:55–56Z, status 200 all four. Sandbox: /fast/scratch/hyaku/kake-r30/w1/ScoutRenderSurface/
Exploratory source ids X01–X04 (deliberately not S0xx, so they cannot be mistaken for the declared C2 sources).

## Commands run (all in the sandbox; no lane writes except this report)
- `git clone` not needed; no repo mutation. `python3 -B fetch_extra.py` → exit 0 (4 GETs, receipts written).
- `python3` stdlib one-liners to extract `<article>` text and to decode the RSC payload from the saved X02 body → exit 0.
- Retained texts read from `.ufo/waves/round-30/sources/S049..S052.txt` (one line each; quote search by phrase).

## Sources opened
| id | URL | finalUrl | words (text) | body sha256 (receipts.json) |
|----|-----|----------|------|------------------|
| X01 | https://render.com/docs/deploys | same | 3403 | b714dd0f…994c295 |
| X02 | https://render.com/docs/blueprint-spec | same | 8223 | a5b18d81…40d40c2 |
| X03 | https://render.com/docs/service-previews | same | 1829 | 46b4cf27…5c64a3b |
| X04 | https://render.com/docs/preview-environments | same | 1989 | 20af08da…b311518 |

Artifacts: `sources/X0N.html.gz`, `sources/X0N.txt`, `sources/receipts.json` (sha256 7a311da8…dc1119f),
`article-X0N.txt` (article-only text; X02 sha256 c78c4a95…ac92a58b). Full hashes: `sha256sum` output in transcript.

## Facts the entry would need (fact → source → in S049–S052? → located quote)
| # | Fact | Source | In S049–S052 | Quote |
|---|------|--------|--------------|-------|
| 1 | Static-site zero downtime is CDN-backed, no service instances | /docs/deploys | partial (S049 has zero-downtime + immediate cache invalidation only) | "Static sites also update with zero downtime, but they're backed by a CDN and don't involve service instances." |
| 2 | Deploy command timeouts 120/30/15 min; start command N/A for static sites | /docs/deploys | no | "Build command 120 minutes Pre-deploy command 30 minutes Start command 15 minutes" |
| 3 | Auto-deploy modes: On Commit (default) / After CI Checks Pass / Off; pass = success, neutral, skipped | /docs/deploys | no | "Render considers a check \"passed\" if its conclusion is any of success , neutral , or skipped ." |
| 4 | Skip phrases [skip render] / [render skip] (render also replaceable by deploy, cd) | /docs/deploys | no | "The skip phrase is one of [skip render] or [render skip] ." |
| 5 | Build filters: auto-deploy only on changes to particular files | /docs/deploys, /docs/blueprint-spec | no | "File paths in the service's repo to include or ignore when determining whether to trigger an automatic build." |
| 6 | Manual deploys incl. deploy-hook GET/POST; "Deploy a specific commit" disables auto-deploys from Dashboard and hook, not CLI/API | /docs/deploys | no | "You can trigger a manual deploy by sending an HTTP GET or POST request to this URL." |
| 7 | Clear build cache & deploy refreshes stale static assets | /docs/deploys | no | "or to refresh stale static assets" |
| 8 | Overlapping deploys: Wait (default for workspaces created on/after 2025-07-14) vs Override | /docs/deploys | no — dated/account-dependent | "This is the default policy for workspaces created on or after 2025-07-14 ." |
| 9 | Static site = `type: web` + `runtime: static`; runtime immutable after creation | /docs/blueprint-spec | no | "web for a web service or static site For a static site, you also set runtime: static ." / "except for static sites" |
| 10 | `staticPublishPath` required, relative to repo root | /docs/blueprint-spec | no | "staticPublishPath Required. The path to the directory that contains the static files to publish, relative to the repo root." |
| 11 | Blueprint `headers` (path/name/value); existing rules not in the file are preserved | /docs/blueprint-spec | no | "Render preserves any existing header rules that are not included in the Blueprint file." |
| 12 | Blueprint `routes` (type redirect/rewrite, source/destination); same preserve rule | /docs/blueprint-spec | no | "Configuration details for a static site's redirect and rewrite routes ." |
| 13 | `plan` not supported for static sites; `region` unsupported (global CDN); `startCommand` unsupported | /docs/blueprint-spec | no | "Not supported for: Static sites (which don't have a compute plan)" / "Unsupported for static sites (which are hosted on a global CDN)." |
| 14 | `preDeployCommand` for static sites runs after build, before deployment — but /docs/deploys lists pre-deploy as paid web/private/worker only | /docs/blueprint-spec vs /docs/deploys | no — cross-page conflict, entry should not assert either | "For static sites , it runs after the build completes and before deployment." vs "available for paid web services , private services , and background workers ." |
| 15 | `ipAllowList` on static sites requires Scale or Enterprise | /docs/blueprint-spec | no | "ipAllowList Web services and static sites only. Requires a Scale or Enterprise plan ." |
| 16 | Per-service `previews.generation` manual/automatic (omit = previews off); deprecated `pullRequestPreviewsEnabled: true` | /docs/blueprint-spec | no | "Setting the deprecated field pullRequestPreviewsEnabled: true is equivalent to setting this subfield to automatic ." |
| 17 | Blueprint-level `previews.generation` off/manual/automatic; `previews.expireAfterDays`; deprecated `previewsEnabled: true` | /docs/blueprint-spec | no | "Supported values include: off manual automatic" / "previews.expireAfterDays The number of days to retain a preview environment that receives no updates." |
| 18 | `buildFilter` on sync fully replaces existing settings | /docs/blueprint-spec | no | "When synced, this value fully replaces an existing service's build filter settings." |
| 19 | Example render.yaml static block (headers, routes, previews, buildFilter, ipAllowList) | /docs/blueprint-spec | no | payload: "staticPublishPath: ./build … previews: generation: automatic … headers: - path: /* name: X-Frame-Options value: sameorigin … routes: - type: redirect source: /old destination: /new" |
| 20 | PR preview = separate temporary instance with its own onrender.com URL, HTTP/2 + full TLS | /docs/service-previews | partial (S049: "its own URL"; onrender.com/HTTP-2/TLS absent) | "a separate, temporary instance of your service with its own onrender.com URL (served over HTTP/2 with full TLS)" |
| 21 | Preview instances get `X-Robots-Tag: noindex` automatically | /docs/service-previews | no | "Render automatically sets the HTTP response header X-Robots-Tag: noindex for all preview instances." |
| 22 | Preview triggers: label render-preview, title [render preview]; skips: render-preview-skip, [skip preview]/[preview skip]/[skip render]/[render skip] | /docs/service-previews | no | "Include the string [render preview] in your PR's title (not the commit message)." |
| 23 | `IS_PULL_REQUEST` env var; settings copied at creation; later base-service changes not applied; preview deleted on PR merge/close | /docs/service-previews | no | "checking the value of the IS_PULL_REQUEST environment variable ( true for a PR preview, false otherwise)" |
| 24 | Preview billing prorated by second; free static site → free previews | /docs/service-previews | no | "If your base service is a free static site, its PR previews are also free." |
| 25 | Preview environments: Pro plan required; Blueprint-driven; datastore copies carry no data; `previewValue`, `previewPlan`/`previews.plan`, `initialDeployHook`; `sync: false` vars not copied; workflows skipped | /docs/preview-environments | no | "Preview environments require a Pro workspace plan or higher." / "Copies of datastores and persistent disks do not include data" |
| 26 | Domains in YAML auto-add www/root counterpart; `renderSubdomainPolicy` disables the onrender.com subdomain (404) | /docs/blueprint-spec | yes — S052 states the same www/root rule and the 404 behavior, and names renderSubdomainPolicy | "Requests to the subdomain receive a 404 response." |

## Statements in the retained texts that look plan-dependent or dated (flag for the entry)
- S049 and S052, same table: "Plan Included domains Hobby 2 Pro 15 Scale 25 Each custom domain you add beyond this amount costs $0.25 per month." — plan- and price-dependent; will date.
- S049: "Static sites are fast and free to deploy." and "Static sites count against your workspace's monthly included amounts of outbound bandwidth and pipeline minutes ." — plan-dependent (free tier + workspace allowances).
- S050: "You can't apply redirect/rewrite rules to your domain root. Each Source requires at least one URL path component (such as /blog , or even / )." — internally tensioned; the entry should not paraphrase it as "root not matchable".
- S050: Redirect action documented only as "a 301 Moved Permanently response code" — no other status code is offered; treat as documented behavior, not a configurable knob.
- None of the four pages carries a last-updated date; the only freshness mark is the footer "© Render 2026" (all four). C2's freshness evidence therefore rests on the receipt timestamps, not on page metadata.
- Same applies to X01–X04: no dateModified/datePublished in the saved bodies (checked in HTML).

## Text-rule caveat for the entry (fidelity)
The retained-text rule (HTML minus script/style) drops the docs' code examples: on X02 the full example render.yaml and the
headers/routes examples live in the RSC payload inside a `<script>` (offsets 519848, 414837, 1136900 in `sources/X02.html.gz`).
A quote taken from an example block cannot be sourced from any `.txt`; cite the `.html.gz` body or re-extract.
Rows 11, 12, 19 above were recovered by decoding that payload from the saved snapshot (no extra GET).

## Cross-checks against the landed entry (corpus/knowledge/render-static-sites.md, read 2026-10-22)
- The entry says "The publish directory, root directory or output path of a Render static site is not stated by S049–S052 and is
  therefore not claimed here." Row 10 answers the gap for Blueprint-managed sites: `/docs/blueprint-spec` states
  "staticPublishPath Required. The path to the directory that contains the static files to publish, relative to the repo root."
- The entry's GitHub-Pages contrast says "[INFERENCE] on Render there is no repository file that names the domain, so a domain
  change is a dashboard change." That inference does not hold for Blueprint-managed services: `/docs/blueprint-spec` documents a
  repository `render.yaml` field "domains Web services and static sites only. A list of custom domains for the service." with the
  same auto www/root rule S052 states. Advisory for the L1/closure: qualify the inference or cite the Blueprint path.
- The entry's build section is consistent with X01: X01 adds that a static site's zero downtime is CDN-backed with no service
  instances, and that auto-deploy skip phrases, build filters and build-cache clearing exist (rows 3, 4, 5, 7).

## Not opened (linked from the retained pages, outside the named families)
/docs/quickstarts (deploy-nextjs-app, deploy-hugo, …), /docs/ddos-protection, /docs/configure-{cloudflare,namecheap,other}-dns,
/docs/build-pipeline, /docs/troubleshooting-deploys, /docs/rollbacks, /docs/monorepo-support, /docs/deploy-hooks, /docs/api.
They bear on adjacent concerns (generator-specific build settings, DNS setup, build internals, failure modes); the named
deploys/blueprint/previews surface above is complete for this seat.

## Confidence and unknowns
- High: rows 1–26 as quotes above are verbatim from the saved bodies at the stated URLs (status 200, sha256 recorded).
- Open: whether `buildCommand` is truly required for a build-less static site (spec: "Required for non-Docker-based services",
  not restated for static sites); whether pre-deploy commands run for static sites in practice (row 14 conflict); whether
  redirect rules can target the domain root (S050 wording). Each is a documentation ambiguity, not resolved by further GETs here.
