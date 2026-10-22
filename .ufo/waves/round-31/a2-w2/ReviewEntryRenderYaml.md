# ReviewEntryRenderYaml — C2 entry "The lane's render.yaml at ds4cc-marketplace 1fbdb8ed" vs real files

Axes: freshness (pointer truth), operability (reproducible evidence). Verdict: **no wrong pointer, key, value, blob hash or server.ts reference found**; every checkable claim in the section verified against `git show`/`rev-parse` at `1fbdb8ed` (= `1fbdb8ed2dfe29cbb79eea6f644302f4d0fa5e28`, 2026-10-21 05:51:24 -0300). Two minor nits, no defects.

## Checks run (all exit 0 unless noted)

`git -C /home/vgpnk/Projects/ds4cc-marketplace rev-parse 1fbdb8ed:<path>` for the four paths; `git show 1fbdb8ed:<path> | cat -n`; `git ls-tree --name-only 1fbdb8ed`; `wc -l`; `od -c` tail; `grep -nE` for absent keys (exit 1 = no match, expected). `rev-parse` is read-only; the assignment's Change line names it. No live request to any ds4cc/onrender host; no sandbox clone needed (all work read-only).

## Verified claims — section header

| Claim | Observed | Result |
|---|---|---|
| render.yaml blob `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252` | identical | OK |
| 20 lines | `wc -l` = 20, file ends `"120000"\n` | OK |
| Dockerfile blob `ee0b63819a9ce71e51469796541b9075e9676ae9` | identical | OK |
| server entry `apps-sdk/src/server.ts` blob `649726df…` | `649726dfcd4bead92195992ed23e03dacd2d23ba` (prefix OK); it is the entry: `CMD ["node","dist/server.js"]` (Dockerfile:17), `start: node dist/server.js` (package.json:12) | OK |
| wave-1 seat `ScoutDs4ccRenderSurface` | `.ufo/waves/round-31/w1/ScoutDs4ccRenderSurface.md` exists; cites identical blobs and lines :14/:142/:193/:272 | OK |
| "Nothing was fetched" | consistent; scout report states offline-only reads | OK |

## Verified claims — bullets

| Claim | Observed | Result |
|---|---|---|
| `type: web` (line 2) | line 2 `  - type: web` | OK |
| `runtime: docker` (line 4); implies web service not static | line 4 `runtime: docker`; S057 text: `static for static sites` is a separate runtime value | OK |
| `dockerfilePath: ./apps-sdk/Dockerfile` (line 5); default is root Dockerfile, repo has none | line 5 exact; S057: `If omitted, Render uses ./Dockerfile .`; `git ls-tree` root shows no `Dockerfile` | OK |
| `dockerContext: .` (line 6) restates default | line 6 exact; S057: `If omitted, Render uses the repo root.` | OK |
| `.dockerignore` starts `*`, re-admits only `apps-sdk/` sources + `marketplace/` | lines 1-9 exactly as described; lines 10-11 additionally re-exclude `marketplace/**/target/` (see nit 2) | OK |
| Dockerfile copies only `apps-sdk/` + `marketplace` paths | `COPY` lines 3,5,11,13 (`apps-sdk/…`), 14 (`marketplace`); no other `COPY` | OK |
| `healthCheckPath: /health` (line 7); `GET /health` → 200 (`server.ts:193`) | line 7 exact; `server.ts:193` `app.get("/health", … res.json({status:"ok"…}))` → HTTP 200 | OK |
| `envVars` lines 8-20; values for APP_ORIGIN, ALLOWED_HOSTS, ALLOWED_ORIGINS, MAX_UNAUTHENTICATED_SESSIONS, MCP_SESSION_IDLE_TIMEOUT_MS | lines 8-20 exact: values `https://app.ds4cc.com` (:10), `ds4cc-marketplace-app.onrender.com` (:12), `https://chatgpt.com` (:14), `"64"` (:18), `"120000"` (:20) | OK |
| `sync: false` on OPENAI_APPS_CHALLENGE (lines 15-16) | lines 15-16 exact | OK |
| No port set; `EXPOSE 3000`; `PORT` fallback 3000 (`server.ts:14`); listens `0.0.0.0` (`server.ts:272`) | no port key in render.yaml; Dockerfile:15 `EXPOSE 3000`; :14 `Number.parseInt(process.env.PORT ?? "3000", 10)`; :272 `createApp().listen(PORT, "0.0.0.0", …)` | OK |
| `ALLOWED_HOSTS` names only `ds4cc-marketplace-app.onrender.com` (line 12); server list also has `app.ds4cc.com` | line 12 is the single value; server list `server.ts:15-20` = `APP_ORIGIN` hostname (`app.ds4cc.com`, default :13) + localhost + 127.0.0.1 + env; enforced via `createMcpExpressApp({host:"0.0.0.0", allowedHosts:[…]})` at :142 | OK |
| Absent: `domains`, `plan`, `region`, `autoDeployTrigger`, `renderSubdomainPolicy` | grep over full blob: zero matches (exit 1) | OK |

## Nits (not defects)

1. **Unmarked unquoted claim.** The `dockerfilePath` bullet asserts "the default would be the root Dockerfile" with no quoted span and no `[INFERENCE]` marker, unlike sibling bullets. Substance is true — S057 retains `If omitted, Render uses ./Dockerfile .` — but it breaks the entry's own quote-discipline stated in its `ground:` header.
2. **`.dockerignore` bullet omits the carve-back.** Lines 10-11 (`marketplace/**/target/`, `marketplace/**/target/**`) re-exclude Rust build output after `!marketplace/**`; the claim "re-admits only `apps-sdk/` sources and `marketplace/`" stays accurate but a reader could infer all of `marketplace/` enters the context. Also `apps-sdk/Dockerfile` itself is excluded from the context — harmless, and the Dockerfile is consumed outside context semantics.

## Residual risk / not verified

- Did not re-run `c2_quote_truth.py` / `c2_strict_checks.py` (L1's counters; outside this seat's target).
- Did not check `createMcpExpressApp` host-rejection semantics (SDK not vendored; scout gap G2 stands — entry's Host claim is correctly hedged `[INFERENCE]`).
- Header `verified-at` range 15:41:23Z–15:41:28Z matches receipts S057–S060 (23/26/26/28Z); S061 at 15:41:29Z is outside the entry's stated window but is a round-30 id, not C2.

## Installs

None. Commands ran against existing git/python3.

Report: .ufo/waves/round-31/a2-w2/ReviewEntryRenderYaml.md
