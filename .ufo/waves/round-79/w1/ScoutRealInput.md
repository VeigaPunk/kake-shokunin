# ScoutRealInput — round 79, wave w1

**Verdict:** the real-input surface is a **negative population** — 12 recorded surfaces, **0 carry any
`x-robots-tag` field** (0/12), 207 recorded field lines total — so a clean audit run over it proves only
that the tool accepts real-shaped header lists and reports empty sets, never that a positive
X-Robots-Tag grammar path works on real data. Of the 12, **4 are GitHub Pages** (no author-defined
response-header mechanism) and **8 are third-party Kimi-hosted origins behind Cloudflare** (no
declaration file in any local checkout); the one **Render** property in `ds4cc-marketplace`
(`render.yaml`, Docker web service) is **not** among the 12 and is the only owned surface whose code
could set the header (Express middleware, `apps-sdk/src/server.ts:184-189`, currently three other
security fields).

## 1. Method and commands

Read-only only; no network fetch, no clone, no fixture, no scratch tree created (nothing owed to
cleanup). Lane worktree `/home/vgpnk/Projects/shokunin/kake-shokunin` untouched.

| command (cwd) | exit |
|---|---|
| `python3 - <<'PY' …` over `.ufo/waves/round-61/capture/*/response.json` (inventory + sha256; cwd `.../capture`) | 0 |
| same, second script: `headerCount == len(headers)`, ASCII names, duplicate-name count, `fetchedAt`, total field lines | 0 |
| `python3 - <<'PY'` over `.ufo/waves/round-79/cases/c*/manifest.json` (zero-XRT path census) | 0 on the first 23 dirs; 1 at `c24` because `c24/manifest.json` is deliberately malformed JSON (9 bytes) — handled as the fault case it is, scan re-run with a per-case `try` → 0 |
| `cd /home/vgpnk/Projects/ds4cc-marketplace && git rev-parse HEAD` | 0 → `24991e44c74d1061db55652be4a27db56efc8791` |
| `git status --porcelain` | 0, 0 lines (clean worktree) |
| `git grep -in 'x-robots-tag' -- .` | **1** (no match anywhere in tracked bytes) |
| `find . -path ./.git -prune -o -name '_headers' -print` | 0, no output |
| `find . -path ./.git -prune -o -name 'netlify.toml' -print` | 0, no output |
| `grep -in 'header' .github/workflows/*.yml` | **1** (no match) |
| `find . -path ./.git -prune -o \( -iname '*cloudflare*' -o -iname 'wrangler*' -o -iname '*netlify*' \) -print` | 0, no output |
| `find /home/vgpnk/Projects -maxdepth 3 … \( -name '_headers' -o -name CNAME -o -name netlify.toml -o -name render.yaml \) -print` (bounded cross-check, read-only) | 0 → only `./ds4cc-marketplace/CNAME`, `./ds4cc-marketplace/render.yaml` |

## 2. Inventory — 12 recorded surfaces

Requested URL == final URL and `redirects: []` on all 12; `fetchedAt` span `2026-10-27T09:15:53Z` …
`09:16:02Z`; `headerCount` equals `len(headers)` on all 12 (12/12 true); every recorded field name is
ASCII (12/12 true). Names are listed in wire order.

| id | status | requested URL | final URL | #hdr | header names | `x-robots-tag`? |
|---|---|---|---|---|---|---|
| `burnerchrome-kimi` | 200 | `https://burnerchrome.kimi.page/` | `https://burnerchrome.kimi.page/` | 16 | `Date; Content-Type; Transfer-Encoding; Connection; Server; vary; vary; x-internal-adhoc-canary; access-control-allow-headers; access-control-allow-methods; access-control-allow-origin; Cache-Control; x-content-type-options; strict-transport-security; cf-cache-status; CF-RAY` | no |
| `charter-ghp` | 200 | `https://veigapunk.github.io/charter-ufo-fsd/` | `https://veigapunk.github.io/charter-ufo-fsd/` | 23 | `Connection; Content-Length; Server; Content-Type; Last-Modified; Access-Control-Allow-Origin; Strict-Transport-Security; ETag; expires; Cache-Control; x-proxy-cache; X-GitHub-Request-Id; x-github-edge-region; Accept-Ranges; Date; Via; Age; X-Served-By; X-Cache; X-Cache-Hits; X-Timer; Vary; X-Fastly-Request-ID` | no |
| `charter-kimi` | 404 | `https://charter-ufo-fsd.kimi.page/` | `https://charter-ufo-fsd.kimi.page/` | 14 | `Date; Content-Type; Transfer-Encoding; Connection; Server; vary; vary; x-internal-adhoc-canary; access-control-allow-headers; access-control-allow-methods; access-control-allow-origin; strict-transport-security; cf-cache-status; CF-RAY` | no |
| `ds4cc-kimi` | 200 | `https://ds4cc.kimi.page/` | `https://ds4cc.kimi.page/` | 16 | `Date; Content-Type; Transfer-Encoding; Connection; Server; vary; vary; x-internal-adhoc-canary; access-control-allow-headers; access-control-allow-methods; access-control-allow-origin; Cache-Control; x-content-type-options; strict-transport-security; cf-cache-status; CF-RAY` | no |
| `ds4cc-primary` | 200 | `https://ds4cc.com/` | `https://ds4cc.com/` | 22 | `Connection; Content-Length; Server; Content-Type; Last-Modified; Access-Control-Allow-Origin; ETag; expires; Cache-Control; x-proxy-cache; X-GitHub-Request-Id; x-github-edge-region; Accept-Ranges; Date; Via; Age; X-Served-By; X-Cache; X-Cache-Hits; X-Timer; Vary; X-Fastly-Request-ID` | no |
| `lucario-ghp` | 200 | `https://veigapunk.github.io/lucario/` | `https://veigapunk.github.io/lucario/` | 23 | `Connection; Content-Length; Server; Content-Type; Last-Modified; Access-Control-Allow-Origin; Strict-Transport-Security; ETag; expires; Cache-Control; x-proxy-cache; X-GitHub-Request-Id; x-github-edge-region; Accept-Ranges; Date; Via; Age; X-Served-By; X-Cache; X-Cache-Hits; X-Timer; Vary; X-Fastly-Request-ID` | no |
| `lucario-kimi` | 404 | `https://lucario.kimi.page/` | `https://lucario.kimi.page/` | 14 | `Date; Content-Type; Transfer-Encoding; Connection; Server; vary; vary; x-internal-adhoc-canary; access-control-allow-headers; access-control-allow-methods; access-control-allow-origin; strict-transport-security; cf-cache-status; CF-RAY` | no |
| `plazir15-ghp` | 200 | `https://veigapunk.github.io/plazir-15-site/` | `https://veigapunk.github.io/plazir-15-site/` | 23 | `Connection; Content-Length; Server; Content-Type; Last-Modified; Access-Control-Allow-Origin; Strict-Transport-Security; ETag; expires; Cache-Control; x-proxy-cache; X-GitHub-Request-Id; x-github-edge-region; Accept-Ranges; Date; Via; Age; X-Served-By; X-Cache; X-Cache-Hits; X-Timer; Vary; X-Fastly-Request-ID` | no |
| `plazir15-kimi` | 404 | `https://plazir15.kimi.page/` | `https://plazir15.kimi.page/` | 14 | `Date; Content-Type; Transfer-Encoding; Connection; Server; vary; vary; x-internal-adhoc-canary; access-control-allow-headers; access-control-allow-methods; access-control-allow-origin; strict-transport-security; cf-cache-status; CF-RAY` | no |
| `plazir27-kimi` | 404 | `https://plazir27.kimi.page/` | `https://plazir27.kimi.page/` | 14 | `Date; Content-Type; Transfer-Encoding; Connection; Server; vary; vary; x-internal-adhoc-canary; access-control-allow-headers; access-control-allow-methods; access-control-allow-origin; strict-transport-security; cf-cache-status; CF-RAY` | no |
| `ufo-fsd-kimi-pro` | 200 | `https://ufo-fsd.kimi.pro/` | `https://ufo-fsd.kimi.pro/` | 12 | `Date; Content-Type; Transfer-Encoding; Connection; Server; access-control-expose-headers; Cache-Control; x-fc-request-id; x-proxy-by; strict-transport-security; cf-cache-status; CF-RAY` | no |
| `vault-index-kimi` | 200 | `https://veigapunk.kimi.page/` | `https://veigapunk.kimi.page/` | 16 | `Date; Content-Type; Transfer-Encoding; Connection; Server; vary; vary; x-internal-adhoc-canary; access-control-allow-headers; access-control-allow-methods; access-control-allow-origin; Cache-Control; x-content-type-options; strict-transport-security; cf-cache-status; CF-RAY` | no |

**Counts.** Surfaces total **12**; with an `x-robots-tag` field (ASCII case-insensitive name match)
**0**; without **12** (`burnerchrome-kimi`, `charter-ghp`, `charter-kimi`, `ds4cc-kimi`,
`ds4cc-primary`, `lucario-ghp`, `lucario-kimi`, `plazir15-ghp`, `plazir15-kimi`, `plazir27-kimi`,
`ufo-fsd-kimi-pro`, `vault-index-kimi`). Field lines **207**; duplicate-name surfaces **7/12** (the
two `vary` lines on every `.kimi.page` surface except `ufo-fsd-kimi-pro`); statuses **8×200, 4×404**.

**Receipt pins** (sha256 of each `response.json`, for the executor's manifest provenance):

| id | sha256(`response.json`) | fetchedAt |
|---|---|---|
| `burnerchrome-kimi` | `3b2e6530699f82b04d5e44e77c8bb0749656ace45e9b0bd3c847dd185dbef81f` | 2026-10-27T09:15:53Z |
| `charter-ghp` | `cf721dfd1a4ef1a2d141833dacf2ba922054682f8f55992d25094563622da08a` | 2026-10-27T09:15:55Z |
| `charter-kimi` | `d9e10c72d222b75121eecdd7fe4d3a6af90376139d4f4dd8f5686ebfc4bd1809` | 2026-10-27T09:15:55Z |
| `ds4cc-kimi` | `45d1f10f53ede3d2f59b25a5a623f0db927ae88f089bdfa58d56e6efeb170fde` | 2026-10-27T09:15:57Z |
| `ds4cc-primary` | `103e3013c3fdca20f0b3f374c3dc8c32430c4c23bbe02be4e56d009356661040` | 2026-10-27T09:15:57Z |
| `lucario-ghp` | `aad28be25c0518d6e049a4d9627686c6afd5b5f7a42548e8321d9eb883a041e6` | 2026-10-27T09:15:57Z |
| `lucario-kimi` | `a28350d59cbc37ac9583b1459de5c00b4e1af5d0210de03e68ecf3cd2f2df278` | 2026-10-27T09:15:58Z |
| `plazir15-ghp` | `1603e62d0b5f73f7e4a389aad02722a4170eda37d6621940c7f190fb89e71e35` | 2026-10-27T09:15:58Z |
| `plazir15-kimi` | `0390704f5a3a654789e88b1312daa2d4ca3b5b52f19ff12b03da27d010b2622e` | 2026-10-27T09:15:58Z |
| `plazir27-kimi` | `244c419e8a38a2820f3f8a765814a0e3d20fbcbf378c5b8cb38aab0fe273be10` | 2026-10-27T09:16:00Z |
| `ufo-fsd-kimi-pro` | `1de9733b26fdc3424e6e4e968d54c2a807828adaa187b7bd2416417dec4821d7` | 2026-10-27T09:16:00Z |
| `vault-index-kimi` | `6c3b5eac246303f25359bfcb1936be4ce0544db210f9510e4292be78bd44a99b` | 2026-10-27T09:16:02Z |

Cross-check: the 207 field-line total matches the round-61 `ExecC2HeaderRecon` census, so these are
the same bytes that report described.

## 3. `ds4cc-marketplace` scan (read-only, HEAD `24991e44`, clean worktree)

Header-declaration files found in the whole repository (`find` over all depths, `.git` pruned):
**`CNAME`** (content `ds4cc.com`, no trailing newline; sha256
`361e8a3fcefb55b19525ecd9f1e69fbe3c33cfddb2a45b538bcc8c16ff977437`) and **`render.yaml`** (sha256
`83e0ead9c360d1c315f0ad8774550e7da1fbe6be8ddc5ab52ef0edddb437920b`). **No `_headers`, no
`netlify.toml`, no `vercel.json`/`firebase.json`/`staticwebapp.config.json`, no `wrangler`/Cloudflare
config.** Zero tracked bytes mention `x-robots-tag` (`git grep -in` → exit 1). `.nojekyll` is present
(sha256 `f50e364d659135d77207a91b53e69b3596077974062db02769a2336c949269ea`); `robots.txt` exists
(sha256 `70f9ea2885def1b2d2117946b6e6256e666f970f018189d8f5414b1ad0264c05`) and declares only
`User-agent: * / Allow: / / Sitemap`.

**GitHub Pages path.** `.github/workflows/pages.yml:1` deploys on push to `main`;
`:64` `actions/upload-pages-artifact@v3` with `:66 path: ./ds4cc-marketplace` (the whole repo tree),
`:68-69` `actions/deploy-pages@v4`. No workflow step touches response headers
(`grep -in header .github/workflows/*.yml` → exit 1; the other two workflows are `validate.yml` and
`apps-sdk.yml`, both test-only). GitHub Pages offers no author-defined response-header mechanism: the
Pages documentation set covers publishing sources, Jekyll, custom domains, HTTPS and limits
(`corpus/SOURCES.md` S003/S004/S005/S006/S007/S040), and a `_headers` file is not interpreted by the
Pages backend. **Caveat for the record:** the lane corpus itself does *not* settle this —
`corpus/knowledge/render-static-sites.md:95-97` says "The corpus holds no author-defined per-path
response-header mechanism for GitHub Pages … Whether GitHub Pages has such a mechanism is not settled
by this corpus." The "cannot" in the seat brief is therefore docs-absence + repo-absence evidence, not
a corpus row; if C2's knowledge prose needs it, a source row must be mined first.

**Render path.** `render.yaml:2-5` declares one `type: web`, `runtime: docker` service
(`ds4cc-marketplace-app`, `dockerfilePath: ./apps-sdk/Dockerfile`); it is **not** a Render static
site, so Render's dashboard static-site header feature (S051) does not apply, and `render.yaml` has no
`headers:` block. The service's own process can set response headers: `apps-sdk/src/server.ts:184-189`
disables `x-powered-by` and sets `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`,
`Permissions-Policy: camera=(), microphone=(), geolocation=()`; no `X-Robots-Tag`. Its hosts are
`ds4cc-marketplace-app.onrender.com` (`ALLOWED_HOSTS`) and `app.ds4cc.com` (`APP_ORIGIN`) —
**neither is one of the 12 captured surfaces**.

**Surface split (from the recorded server signatures, not from any file in this repo):**

| platform | surfaces | evidence |
|---|---|---|
| GitHub Pages | `ds4cc-primary` (custom domain `ds4cc.com`), `charter-ghp`, `lucario-ghp`, `plazir15-ghp` | recorded `Server: GitHub.com`, `Via: 1.1 varnish`, `X-Served-By: cache-gig*`, `X-GitHub-Request-Id`; `CNAME`+`pages.yml` in `ds4cc-marketplace` |
| third-party Kimi host behind Cloudflare | `burnerchrome-kimi`, `ds4cc-kimi`, `vault-index-kimi`, `charter-kimi`, `lucario-kimi`, `plazir15-kimi`, `plazir27-kimi`, `ufo-fsd-kimi-pro` | recorded `Server: cloudflare`, `cf-cache-status: DYNAMIC`, `CF-RAY`; the seven `.kimi.page` surfaces additionally share platform canary `x-internal-adhoc-canary: 586427312`; `ufo-fsd.kimi.pro` shows `x-proxy-by: appproxy` + `x-fc-request-id`. No deployment or header file for any of these exists in `ds4cc-marketplace` or in any repo at `/home/vgpnk/Projects` depth ≤3 (bounded find → only the two `ds4cc-marketplace` files) |
| Render | **none of the 12**; `ds4cc-marketplace`'s Docker service is the only Render property in scope | `render.yaml:2-5`, `apps-sdk/src/server.ts:184-189` |

So: **no captured surface is a Render surface**, **4 are Pages** (where the platform, not the
publisher, decides the header set), and **8 are a third-party host** with no header declaration in any
scanned repo. The only owned property that *could* declare `X-Robots-Tag` through a path this repo
controls is the Render app, and it is outside the 12.

## 4. What a clean real run proves — and what it does not

Proves, if `scripts/x_robots_tag_audit.py --manifest …/realrun/manifest.json` exits 0 with
`checks=12 findings=0`:

- the tool accepts a 12-check `x-robots-tag-manifest/v1` document built from the recorded 2026-10-27
  header sets (207 field lines, names mixed-case, 7/12 with duplicate `vary`, `url` = recorded
  `finalUrl`), fetches nothing, and emits one report object with `checks=12`;
- every check carries zero `x-robots-tag` fields, so each check's `directives`, `effective` and
  `bots` sets are empty and the finding union is empty — exit 0.

Does **not** prove:

- anything about the live hosts today: the receipts are from **2026-10-27**, eight days before the
  round open; no network call is made by the tool or the seat;
- that any property *could not* declare `X-Robots-Tag`: the population is 0/12 positive, so it is a
  negative sample. Four of the twelve records are **404 pages**, and the manifest schema has no status
  field (extra keys ignored), so their emptiness means only "no such field was recorded", not
  "indexable page with no restriction";
- any positive grammar path: multi-field line merging, `<bot-name>:` scopes, invalid-value and
  duplicate-directive findings are exercised **only** by the frozen synthetic cases (contract §2
  mechanics; case set `c01–c31`), never by real data;
- crawler behaviour, effective per-bot resolution (a stated lane limit), or that the headers observed
  are the headers a browser would see.

Coverage anchors for the zero-field outcome the real run hits: `cases/c31/manifest.json` (a check whose
`headers` list holds only `X-Frame-Options`) expects `exit 0`, `directives []`, `effective []`,
`bots {}` (`expect/expect.json` → `cases.c31`) — so the all-empty result is oracled, not invented.
`cases/c23/manifest.json` (a string where a list is required) expects `xrt_input_check_shape` / exit 2,
and `cases/c07` holds two `X-Robots-Tag` field lines; no frozen case carries a *duplicate foreign*
field name, so duplicate-`vary` tolerance in the real manifest is unoracled (it must be tolerated per
the schema's list-of-`{name,value}` shape, but only c31's single foreign field is scored).

## 5. Routed notes (no frozen artifact touched)

1. **Real-input run is a negative population.** Its value is acceptance + empty-set rendering on real
   shapes; it cannot stand as evidence that the header grammar works on publisher ground. Any prose
   that cites it must say "recorded 2026-10-27 header sets", not "live hosts".
2. **"GitHub Pages cannot set custom headers" is not a corpus row.** The corpus explicitly leaves it
   unsettled (`corpus/knowledge/render-static-sites.md:95-97`); mine a GitHub Pages source row before
   the C2 knowledge entry asserts it.
3. **`ufo-fsd-kimi-pro` is a different host** (`kimi.pro`, `x-proxy-by: appproxy`) with the same
   Cloudflare front; grouping it with `*.kimi.page` is by host family, not by identity.
4. **No manifest written** (executor `ExecC2RealRun` owns `realrun/manifest.json`); no case, const,
   receipt, counter or contract byte was modified. No tools installed.

Scratch: none created — no clone, fixture, `--work` dir or `$HYAKU_SCRATCH` tree exists for this seat,
so no cleanup is owed.
