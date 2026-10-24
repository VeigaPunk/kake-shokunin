# ScoutDs4ccRenderSurface — C2 target surface: what ds4cc-marketplace's Render web service declares and serves

Scope: read-only, offline. Every fact below was read with
`git -C /home/vgpnk/Projects/ds4cc-marketplace show <blob-or-commit>:<path>`; no working-tree
read, no live request to ds4cc.com, app.ds4cc.com or any onrender host.
Commit: `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28` (2026-10-21 05:51:24 -0300).
Source texts S058/S060 are single-line dumps, so quotes are cited by character offset, not line.

## Files read and blob hashes (all mode 100644)

| path | blob | bytes |
|---|---|---|
| `render.yaml` | `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252` | 565 |
| `apps-sdk/Dockerfile` | `ee0b63819a9ce71e51469796541b9075e9676ae9` | 380 |
| `apps-sdk/src/server.ts` | `649726dfcd4bead92195992ed23e03dacd2d23ba` | 16164 |
| `apps-sdk/package.json` | `4ee3a416c99c76e595f1ceb555f0bda069132802` | 616 |
| `apps-sdk/package-lock.json` | `d3f97b345e10404df2c3942c5befd2f384b713e4` | — |
| `apps-sdk/src/server.test.ts` | `08b3e26c4925691af262f9e427e2d23faac80cd4` | 18357 |
| `apps-sdk/src/catalog.ts` | `1cf8db1595ae7a1f4ee74350cc4d776f7b83908a` | — |

## Observed — what the service declares

`render.yaml` (blob `d17ab7e5`): `type: web` (:2), `name: ds4cc-marketplace-app` (:3),
`runtime: docker` (:4), `dockerfilePath: ./apps-sdk/Dockerfile` (:5), `dockerContext: .` (:6),
`healthCheckPath: /health` (:7). Env vars :8-20: `APP_ORIGIN=https://app.ds4cc.com` (:9-10),
`ALLOWED_HOSTS=ds4cc-marketplace-app.onrender.com` (:11-12),
`ALLOWED_ORIGINS=https://chatgpt.com` (:13-14), `OPENAI_APPS_CHALLENGE` with `sync: false` (:15-16),
`MAX_UNAUTHENTICATED_SESSIONS=64` (:17-18), `MCP_SESSION_IDLE_TIMEOUT_MS=120000` (:19-20).
There is **no `PORT` env var** and **no `domains` key** (consistent with `corpus/knowledge/publish-channels.md:100-102`).

`apps-sdk/Dockerfile` (blob `ee0b6381`):
- :1 `FROM node:22-alpine AS build`; :3-6 `COPY apps-sdk/package*.json ./`, `npm ci`, `COPY apps-sdk/ ./`, `npm run build`.
- :8 final `FROM node:22-alpine`; :9 `ENV NODE_ENV=production`; :10 `WORKDIR /app/apps-sdk`.
- :12 `npm ci --omit=dev`; :13 `COPY --from=build /app/apps-sdk/dist ./dist`; :14 `COPY marketplace /app/marketplace`.
- :15 `EXPOSE 3000`; :16 `USER node`; :17 `CMD ["node", "dist/server.js"]`.
- No `ENTRYPOINT`, no `HEALTHCHECK`, no `ENV PORT`.

`apps-sdk/package.json` (blob `4ee3a416`): `"type": "module"` (:5), `build: tsc -p tsconfig.json` (:10),
`start: node dist/server.js` (:12). Deps include `express ^5.1.0` (:18), `@modelcontextprotocol/sdk ^1.17.5` (:17);
the lock resolves `@modelcontextprotocol/sdk` **1.29.0** (package-lock blob `d3f97b34`).

`apps-sdk/src/server.ts` (blob `649726df`): the Dockerfile `CMD` starts exactly this file compiled to `dist/server.js`.

## Observed — what it serves

- `PORT` read from env at `server.ts:14`: `Number.parseInt(process.env.PORT ?? "3000", 10)`.
- Host allowlist at `server.ts:15-20`: `APP_ORIGIN`'s hostname (`app.ds4cc.com` via :13), `localhost`,
  `127.0.0.1`, plus each `ALLOWED_HOSTS` entry.
- Express app created at `server.ts:142`: `createMcpExpressApp({ host: "0.0.0.0", allowedHosts: [...] })`.
- Only middleware registered before the routes sets three security headers (`server.ts:185-190`); no auth,
  no rate limit, no redirect on that path. `app.disable("x-powered-by")` at :184.
- **`/health` exists** at `server.ts:193`: `app.get("/health", (_req, res) => res.json({ status: "ok",
  service: "ds4cc-marketplace", version: "1.0.0" }))` → HTTP 200, `application/json`, body
  `{"status":"ok","service":"ds4cc-marketplace","version":"1.0.0"}`.
- Bind at `server.ts:272`: `createApp().listen(PORT, "0.0.0.0", () => console.log(...))`; host is the
  literal `0.0.0.0`, not localhost.
- `catalog.ts:40` derives the repo root as two levels up from the module (`dist/server.js` → `/app`), which
  matches `Dockerfile:14` copying `marketplace` to `/app/marketplace` — the Docker layout and the served
  catalog agree.
- `server.test.ts:71-79` asserts `/health` is 200 with exactly that JSON; the test server binds
  `127.0.0.1` on an ephemeral port (`server.test.ts:46`), so the tests never exercise a Render-style Host header.

## Conformance against S058 / S060 (quotes with offsets into the retained bodies)

- S058 @8801: "Every Render web service must bind to a port on host 0.0.0.0 to serve HTTP requests."
  → satisfied by `server.ts:272` (`listen(PORT, "0.0.0.0")`).
- S058 @9008: "We recommend binding your HTTP server to the port defined by the PORT environment variable."
  and @9167: "The default value of PORT is 10000 for all Render web services."
  → satisfied: `server.ts:14` reads `PORT`; with no `PORT` in `render.yaml:8-20`, Render will supply `PORT=10000`
  and the app listens on 10000.
- S060 @3630: "Web services can receive health checks as HTTP GET requests to a path you specify"; @4674:
  "Specify a path starting with a / character"; @4983: success requires "a 2xx or 3xx status code within five
  seconds".
  → satisfied: `healthCheckPath: /health` (`render.yaml:7`) begins with `/`; `server.ts:193` is a GET route returning
  200 with no work that could exceed five seconds (static JSON literal, no I/O).
- S060 @4057: "Render sets one of those domains as the value of the Host header for all HTTP health checks"
  (a verified custom domain, else the onrender subdomain) — see risk R2.

Nothing in the served path binds localhost or pins a port other than `PORT`.

## Risks and mismatches (freshness-relevant, not rule violations observed at runtime)

- **R1 — stale `EXPOSE 3000`.** `Dockerfile:15` advertises 3000 while the container will serve on Render's
  `PORT` (default 10000, S058 @9167). Declarative metadata only; S058 @9338 says Render "is usually able to
  detect and use" a bound port, and here the app binds `PORT` anyway, so this cannot fail a deploy. It misstates
  the served port to any reader of the image and to a local `docker run` that trusts it.
- **R2 — health-check reachability is coupled to a host string that `render.yaml` hardcodes.** The Host header of
  Render health checks is a verified custom domain or the onrender subdomain (S060 @4057). `/health` sits behind
  the app-wide allowlist (`server.ts:15-20`), so the Open Blueprint values `APP_ORIGIN=app.ds4cc.com`
  (`render.yaml:9-10`) and `ALLOWED_HOSTS=ds4cc-marketplace-app.onrender.com` (`render.yaml:11-12`) are load-bearing:
  renaming the service, or attaching a custom domain that is neither `app.ds4cc.com` nor in `ALLOWED_HOSTS`, would
  fail the check, and per S060 @5934 an instance failing checks for 15 s loses traffic and for 60 s is restarted.
  [INFERENCE: that the 1.29.0 helper rejects a non-allowlisted Host before route handlers — see gap G2.]
- **R3 — version literal duplicated.** `/health` returns a hardcoded `"version": "1.0.0"` (`server.ts:193`) that also
  appears in `package.json:3` and in the test assertion (`server.test.ts:75`); nothing derives one from the other, so a
  release bump can leave the surfaced version stale in three places.
- **R4 — PORT is parsed, not validated.** A non-numeric `PORT` yields `NaN` and `listen` throws at boot
  (`server.ts:14`, :272). Render supplies a numeric `PORT`, so this is latent. [INFERENCE on the throw path.]

## Gaps / not verified

- G1. No live request was made (lane bounds). Whether the service is currently deployed, which custom domains are
  verified, and what Host header its checks actually carry are **unobserved**. `render.yaml` has no `domains` key, so
  `app.ds4cc.com` is not attached by this Blueprint (matches `publish-channels.md:100-102`).
- G2. The host-validation semantics of `createMcpExpressApp({host, allowedHosts})` in `@modelcontextprotocol/sdk` 1.29.0
  could not be read offline: the repo vendors no `node_modules`, and fetching the npm tarball is outside the network
  grant. Both `host: "0.0.0.0"` and `allowedHosts` are passed at `server.ts:142`; whether `host` also narrows or widens
  Host acceptance is unverified. Binding is not in doubt — it is the explicit `listen` at `server.ts:272`.
- G3. `corpus/knowledge/render-web-services.md` (C2's stated artifact) **does not exist** at this revision:
  `corpus/knowledge/` lists `render-static-sites.md` and `publish-channels.md` but no `render-web-services.md`, and
  `find . -name render-web-services.md` inside the lane returns nothing. The Render web-service section currently lives
  in `corpus/knowledge/publish-channels.md:88-110`, which records the Blueprint keys but states no port-binding or
  health-check rule from S058/S060.

## Commands run (exit codes)

1. `git show 1fbdb8ed:render.yaml` → 0 (20 lines, blob `d17ab7e5`).
2. `git ls-tree -r --long 1fbdb8ed` (grep for render/Dockerfile/health/server/package.json) → 0.
3. `git show 1fbdb8ed:apps-sdk/Dockerfile`; `git show 1fbdb8ed:apps-sdk/package.json` → 0 (both dumped, 17 and 27 lines).
4. `git show 1fbdb8ed:apps-sdk/src/server.ts > server.ts.snapshot` then `grep -n` → 0 (273 lines; 0.0.0.0 at :142/:272).
5. `git show 1fbdb8ed:apps-sdk/src/catalog.ts | head -40` → 0 (`repositoryRoot` at :40).
6. `git show 1fbdb8ed:apps-sdk/src/server.test.ts` → 0; `sed -n` slices → 0 (`/health` assertions at :71-79, `listen(0,"127.0.0.1")` at :46).
7. `git show 1fbdb8ed:apps-sdk/package-lock.json | grep -A3 ...sdk` → 0 (sdk 1.29.0).
8. `git show -s --format='%H%n%ci%n%s' 1fbdb8ed` → 0.
9. Python offset extraction over `.ufo/waves/round-31/sources/S058.txt`, `S060.txt` → 0 (quotes and offsets above;
   receipts confirm both fetched 2026-10-22T15:41:26Z / 15:41:28Z with status 200).
10. `cat -n` of `render.yaml` for line citations → 0.
11. `find . -name 'render-web-services.md'` in the lane → 0, no matches (G3).

No installs or upgrades were made. No file was written in the lane except this report.
