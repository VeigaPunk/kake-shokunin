# C2 relevance: does any operator property or local checkout deploy on Render?

Seat: KakeR30.ScoutLocalRenderUse (leaf, read-only). Sandbox: `/fast/scratch/hyaku/kake-r30/w1/ScoutLocalRenderUse/` (unused; no clone needed).
No network, no pacman, no installs, no lane writes except this file.

## Answer

Yes for one owned property, and it is **not a static site**: `app.ds4cc.com` deploys as a Render **Docker
web service** from `/home/vgpnk/Projects/ds4cc-marketplace/render.yaml`. No local checkout of an operator
property deploys a Render **static site**. The lane's apex property `ds4cc.com` is GitHub Pages, not Render.
So the C2 entry stays platform knowledge; its static-site rules must not be read as describing the local
Render deployment, and its custom-domain text must stay service-neutral because S052 covers web services too.

## Hits, with exact coordinates

Deployment config (the only Render blueprint on this host):

- `/home/vgpnk/Projects/ds4cc-marketplace/render.yaml:2` `- type: web`; `:3` `name: ds4cc-marketplace-app`;
  `:4` `runtime: docker`; `:5` `dockerfilePath: ./apps-sdk/Dockerfile`; `:6` `dockerContext: .`;
  `:7` `healthCheckPath: /health`; `:9-10` `APP_ORIGIN=https://app.ds4cc.com`;
  `:11-12` `ALLOWED_HOSTS=ds4cc-marketplace-app.onrender.com`; `:13-14` `ALLOWED_ORIGINS=https://chatgpt.com`.
  File is 20 lines; keys `routes`, `headers`, `publishPath`, `staticSite`, `renderSubdomainPolicy`,
  `previews`, `disk` are absent (grep exit 1).
- `/home/vgpnk/Projects/ds4cc-marketplace/README.md:233` — "Deploy with the root `render.yaml` blueprint or
  `apps-sdk/Dockerfile`, attach `app.ds4cc.com`".
- `/home/vgpnk/Projects/ds4cc-marketplace/apps-sdk/README.md:18` — "The included `Dockerfile` runs on any
  container host; the repository-root `render.yaml` supplies a Render blueprint. Deploy the repository, add
  `app.ds4cc.com` as the service custom domain". Render is the chosen host for a host-portable server, so
  the app's behaviour is not Render semantics.
- `/home/vgpnk/Projects/ds4cc-marketplace/apps-sdk/SUBMISSION.md:72` — "[ ] Authenticate to Render,
  create/update the service from `render.yaml`, and inspect build/start logs". The deploy is a human
  dashboard step driven by the blueprint; no workflow or deploy hook performs it.
- `/home/vgpnk/Projects/ds4cc-marketplace/apps-sdk/Dockerfile:1-16` — node:22-alpine build, `EXPOSE 3000`,
  `CMD ["node", "dist/server.js"]`; a long-running server, not a static publish.
- `/home/vgpnk/Projects/ds4cc-marketplace/apps-sdk/src/server.ts:15-20` — the app allowlists
  `new URL(APP_ORIGIN).hostname`, `localhost`, `127.0.0.1` plus `ALLOWED_HOSTS`; `:142`
  `createMcpExpressApp({ host: "0.0.0.0", allowedHosts: [...] })`, so the onrender hostname is a
  deliberately accepted Host value, not incidental text.
- `/home/vgpnk/Projects/ds4cc-marketplace/CNAME` = `ds4cc.com`; `.github/workflows/pages.yml:1-26` deploys
  the repo root to GitHub Pages with `environment.url: https://ds4cc.com/` (`:20-22`). Apex is Pages;
  only the `app.` subdomain is Render.
- `/home/vgpnk/Projects/burnerchrome/vercel.json:1-18` — the other local static property configures
  headers for **Vercel**, not Render (`cleanUrls`, `trailingSlash`, cache headers on `/fonts/` and
  `/assets/`). Relevant contrast for S051: Render static-site header rules do not supersede this file.

Lane corpus (prose, not deployment):

- `corpus/knowledge/publish-channels.md:1` names `render.yaml` as a historical local source;
  `:24` `## Render — app.ds4cc.com`; `:28` `ALLOWED_ORIGINS` sentence; `:72` [publish-channels:c6] HOLD.
- `corpus/lessons/round-1-aggregator-audit.md:31` — historical check row (`ds4cc-marketplace-app`,
  `APP_ORIGIN=https://app.ds4cc.com`).
- Round-30 sources and sibling w1 reports (`CriticLearningClaim.md`, `ConnectSiblingOverlap.md`) mention
  `render.com`/`onrender` as documentation text only; `shokunin/.ufo/waves/kaika-w1/kake-art.md:118` is a
  fleet artifact holding a Render deploys page back (H9), not a deployment.

False positives: `grep -rIl 'onrender|render.com|render.yaml' ~/.local/bin ~/.config` returns only Chromium
extension filter lists and Codex `ActorSafetyLists`; `burnerchrome/burner.html:79` matches "renderer
accessibility" text.

## Scope recommendation for `corpus/knowledge/render-static-sites.md`

1. **Stay platform knowledge.** Do not name `ds4cc.com`, `app.ds4cc.com` or `ds4cc-marketplace` as an
   example deployment of the entry's rules. The one local Render artifact is a Docker web service; any
   sentence implying a static site would be false at `render.yaml:2-4`, and `apps-sdk/README.md:18` records
   the app as host-portable ("runs on any container host"), so Render supplies only the blueprint and the
   custom domain, not the application's semantics.
2. **One boundary sentence, not a property block**: the lane's only Render deployment is a Docker web
   service recorded at `publish-channels.md:24-28`, so static-site-only rules (publish path, static
   asset/CDN behaviour, `_redirects`/rewrite files, static-site header rules) do not describe it, and the
   web-service-only rules (health check, Docker runtime, server process) do not describe static sites.
   This is the cheapest guard against a future seat applying S049-S051 to `render.yaml`.
3. **Keep the custom-domain section service-neutral.** S052 says verbatim (spacing as retained): "You can
   apply your own custom domains to Render web services and static sites . Services with a custom domain
   also keep their onrender.com subdomain." The local blueprint matches that default: it attaches
   `app.ds4cc.com` and still names `ds4cc-marketplace-app.onrender.com` in `ALLOWED_HOSTS`, with no
   `renderSubdomainPolicy: disabled`. If the entry narrows that sentence to static sites, it becomes wrong
   for the one local service.
4. **Do not duplicate or extend the property facts here.** `publish-channels.md:24-28` owns them; an
   append-only deepening belongs there (it currently omits `ALLOWED_HOSTS`, `render.yaml:11-12`), and
   `app.ds4cc.com` must stay out of `fleet-registry.md` and `freshness-pins.json`.

## Audit of the landed entry (it appeared during this seat)

`corpus/knowledge/render-static-sites.md` did not exist when this seat started and landed while it ran
(111 lines). It already satisfies points 1-4 above, on the evidence checked here:

- `:4` `scope: Render platform documentation for static sites only. This entry makes no live request to any
  operator-owned property and asserts nothing about any owned site.` — platform knowledge, no property named.
- `:109-111` explicitly bounds the entry: "the Render row the lane holds is a Docker web service, not a
  static site (corpus/knowledge/publish-channels.md, `app.ds4cc.com`)." That is the counter-example
  sentence, and it is attributed to the owning entry rather than duplicated.
- `:57` and `:64` keep the custom-domain facts service-neutral, quoting "Only web services and static sites
  support custom domains" and "Services with a custom domain also keep their onrender.com subdomain". Both
  are true substrings of `S052.txt` (verified: the first occurs exactly once).
- `:31-32` carries the S049 split ("create a web service instead of a static site"), which is the boundary
  that keeps S049-S051 from being applied to `render.yaml`.

One bounded caution for the closure, not a defect proven here: `:86` infers "[INFERENCE] on Render there is
no repository file that names the domain". The retained bodies never mention a `domains:` blueprint key
(`grep -o -i 'domains:' S052.txt` → no output), so the sources do not contradict the inference; and the
local blueprint is consistent with it — `render.yaml` names `app.ds4cc.com` only as the `APP_ORIGIN` env
var value (`:9-10`) and has no `domains:` key. Local evidence is consistent but not decisive, so the
inference should stay labelled as an inference rather than be promoted to a fact.

Additional corpus hits found after the entry landed: `corpus/SOURCES.md:57-60` (the four rows, each scoped
"not a statement about … any other host"), `SKILL.md:28` (property row: Render web service, Docker),
`SKILL.md:366` (path inventory), `SKILL.md:427` ([property-map:c6] HOLD). All correct for the Docker
service; none calls it a static site.

## Freshness datums (all read locally)

- `ds4cc-marketplace` HEAD `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` (2026-10-21), matching the checkout
  recorded in the round-24 reconciliation of `publish-channels.md` ("checkout 1fbdb8ed").
- `render.yaml` blob at HEAD `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252`; working file sha256
  `83e0ead9c360d1c315f0ad8774550e7da1fbe6be8ddc5ab52ef0edddb437920b`; `git diff --stat HEAD -- render.yaml`
  is empty (0 lines), so working bytes equal the recorded blob.
- Last commit touching `render.yaml`: `3cd3534739b623fa55a614da0e35d7186c094e1b`, 2026-07-19T13:39:41-03:00
  "feat(marketplace): curate OpenAI submission". The blueprint has been byte-stable for ~3 months, while
  the checkout around it moved to 2026-10-21 — the Render fact in the lane is old, the repo is fresh.

## Commands (exit codes as observed)

1. `grep -rIl -E 'onrender\.com|render\.com|render\.yaml' corpus/` → 2 files, exit 0.
2. `find /home/vgpnk/Projects -maxdepth 6 -name 'render*.yaml' -not -path '*/node_modules/*'` →
   `./ds4cc-marketplace/render.yaml`, exit 0. Repeated at `-maxdepth 12` under the `render*.y*ml` pattern →
   same single hit, exit 0.
3. `grep -rIn -E 'render|onrender' .github/ apps-sdk/Dockerfile` in `ds4cc-marketplace` → no output, exit 1;
   the Render deploy is blueprint-driven only, no workflow step and no `api.render.com` hook
   (`grep -rIn --exclude-dir=.git -E 'api\.render\.com'` over `Projects` → no hit in any checkout).
4. `grep -rIn -i -E 'deploy(s|ed)? (on|to) render|render (web )?service|render\.com' xsnapshot
   audio-shokunin-publish kimi-shokunin the-kimiraikkoner ds4cc-marketplace docs` → only
   `ds4cc-marketplace/render.yaml:12`, exit 0.
5. `cat -n render.yaml` → 20 lines; `grep -n 'routes|headers|publishPath|staticSite|renderSubdomainPolicy'`
   → no match, exit 1.
6. `git -C ds4cc-marketplace rev-parse HEAD HEAD:render.yaml` → `1fbdb8ed…`, `d17ab7e5…`; `sha256sum` as above;
   `git log -3 --format='%H %cI %s' -- render.yaml` → two commits, newest `3cd3534` 2026-07-19.
7. `grep -n '## Render|publish-channels:c6|ALLOWED_ORIGINS' corpus/knowledge/publish-channels.md` → lines
   24, 28, 72, exit 0.
8. S052 sentence extraction (read-only Python over the retained body) → the "web services and static sites"
   sentence quoted above; the `renderSubdomainPolicy: disabled` knob and the "404 after disabling" rule.
9. `cat CNAME` → `ds4cc.com`; `head -50 .github/workflows/pages.yml` → Pages deploy with
   `environment.url: https://ds4cc.com/`.

One earlier whole-tree grep (`grep -rIl 'onrender\.com|render\.com' Projects`) hit its 300 s limit
(`bg_5350`, "interrupted") and is superseded by the targeted runs above; its partial output contained only
lane/fleet artifacts. Three later broad greps also capped at 300 s (`bg_5410` for `api\.render\.com|staticSite|type: static`,
`bg_5412` for `onrender`, `bg_5451` for `onrender` with a `find` preamble); their partial outputs added no
deployment hit — the only extra line was a mado-lane report quoting `x-gitbook-route-type: static`, and
`bg_5451`'s `find` half returned the single `./ds4cc-marketplace/render.yaml`. They are replaced by three
bounded sweeps that completed:

10. Deploy-config sweep, `find Projects -maxdepth 4 -type f \( -iname '*.yaml' -o -iname '*.yml' -o
    -iname '*.toml' -o -iname 'Dockerfile*' -o -iname '*.json' -o -iname 'CNAME' \) -not -path
    '*/node_modules/*' -not -path '*/.git/*' -not -path '*/.ufo/*'` piped to
    `xargs -0 grep -Il -i -E 'render\.com|onrender|render\.yaml'` → exactly one file,
    `./ds4cc-marketplace/render.yaml`, exit 0.
11. README sweep, `find Projects -maxdepth 3 -iname 'README*' … | xargs -0 grep -Il -i -E
    'render\.com|onrender|render\.yaml|render blueprint'` → two files, both `ds4cc-marketplace`
    (`README.md:233`, `apps-sdk/README.md:18`), exit 0. A first pass without the `render\.yaml` alternative
    returned none, exit 123 (xargs propagating grep's no-match status), which is the expected no-hit signal.
12. Script and doc sweep, `find Projects -maxdepth 5 -type f -size -2M \( -iname '*.sh' -o -iname '*.mjs' -o
    -iname '*.js' -o -iname '*.py' -o -iname '*.md' -o -iname '*.service' -o -iname 'Makefile' -o -iname
    '*.env*' \)` minus `node_modules`/`.git`/`.ufo`/`dist`, piped to `xargs -0 grep -Il -i -E
    'onrender\.com|render\.com|render\.yaml'` → eight files, exit 0: the lane's `publish-channels.md`,
    `render-static-sites.md`, `corpus/SOURCES.md`, `SKILL.md`, `lessons/round-1-aggregator-audit.md`, and
    the three `ds4cc-marketplace` docs above. No shell script, Makefile, service unit or deploy script
    anywhere names Render, so nothing local deploys it but the blueprint and the manual checklist.

## Confidence and remaining unknowns

- High: the single local Render blueprint, its service type/runtime, the `app.ds4cc.com` attachment, the
  Pages apex, the byte/blob datums, the S052 wording.
- High-to-medium: "no other operator property deploys on Render" now rests on an exhaustive file-based
  sweep of every `/home/vgpnk/Projects` root at depth ≤4 over yaml/yml/toml/Dockerfile/json/CNAME
  (excluding `node_modules`, `.git`, `.ufo`), which returns exactly one file — `ds4cc-marketplace/render.yaml`
  — plus the two READMEs that point at it. Residual, unchanged: a Render service configured only in the web
  dashboard, with no local file, would not be visible here.
- Unverified by design: whether `app.ds4cc.com` or `ds4cc-marketplace-app.onrender.com` is live now, and
  whether the committed blueprint is the dashboard's live state. Network was out of scope; the lane's
  closest evidence remains the round-23 [publish-channels:c6] HOLD observed 2026-10-21. That the
  onrender hostname is *served* is [INFERENCE] from `server.ts:15-20,142`; only the allowlist is observed.
