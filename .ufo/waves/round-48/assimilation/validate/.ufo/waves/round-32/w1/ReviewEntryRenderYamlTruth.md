# ReviewEntryRenderYamlTruth — C2 truth sampling (routed item 4)

Seat: KakeR32.ReviewEntryRenderYamlTruth (reviewer, leaf). Judged axis: freshness.
Scope: every sentence in `corpus/knowledge/render-web-services.md` section
"The lane's render.yaml at ds4cc-marketplace 1fbdb8ed" (file lines 50–67) that
states a fact about render.yaml, checked against the retained copy
`.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/render.yaml`. Side checks on other
files used only the read-only clone `~/Projects/ds4cc-marketplace` via
`git show`/`git rev-parse`/`git ls-tree`. No network, no owned-property request.

## Commands and exits

- `cat -n .ufo/waves/round-32/sources/ds4cc-1fbdb8ed/render.yaml` → exit 0; 20 numbered lines captured.
- `git hash-object` on retained render.yaml → `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252`; `wc -l` → 20; last byte 0x0a.
- `git -C ~/Projects/ds4cc-marketplace rev-parse 1fbdb8ed:render.yaml 1fbdb8ed:apps-sdk/Dockerfile 1fbdb8ed:apps-sdk/src/server.ts` → exit 0; `d17ab7e5…`, `ee0b6381…`, `649726dfcd4bead92195992ed23e03dacd2d23ba`.
- `git show 1fbdb8ed:render.yaml | diff - <retained>` → exit 0, IDENTICAL (byte-identical confirmed).
- `grep -in 'port' render.yaml` → exit 1 (no match). `grep -nE '(domains|plan|region|autoDeployTrigger|renderSubdomainPolicy)'` → exit 1 (no match).
- `git ls-tree --name-only 1fbdb8ed` → only `.dockerignore` matches docker* (no root Dockerfile).
- `git show 1fbdb8ed:.dockerignore` → exit 0; `git show 1fbdb8ed:apps-sdk/Dockerfile | grep -nE 'EXPOSE|ARG'` → `15:EXPOSE 3000`, no ARG.
- `git show 1fbdb8ed:apps-sdk/src/server.ts | grep -nE …` → hits at 14, 19, 142, 193, 272 (see below).
- `git hash-object` on retained Dockerfile/server.ts/.dockerignore → `ee0b6381…`, `649726df…`, `d650445a…` (all match pinned blob ids).
- `find .ufo/waves/round-32/sources/ds4cc-1fbdb8ed -type f` → four files.

## Counts

Sentences stating render.yaml facts: **supported 12, wrong 0, not checkable 3**.
Collateral sentences resting on other named files: supported 7, wrong 0
(verified via clone/retained copies; listed for completeness since the entry
itself flags they need more than the render.yaml copy).

### Supported by retained render.yaml (sentence → resting line)

1. L52 "render.yaml … blob d17ab7e5…, 20 lines" → hash-object + `wc -l` on retained file.
2. L58 "`type: web` (line 2)" → render.yaml:2.
3. L59 "`runtime: docker` (line 4)" → render.yaml:4.
4. L60 "`dockerfilePath: ./apps-sdk/Dockerfile` (line 5)" → render.yaml:5.
5. L61 "`dockerContext: .` (line 6)" → render.yaml:6.
6. L62 "`healthCheckPath: /health` (line 7)" → render.yaml:7.
7. L63 "envVars (lines 8-20); file sets values for APP_ORIGIN, ALLOWED_HOSTS, ALLOWED_ORIGINS, MAX_UNAUTHENTICATED_SESSIONS, MCP_SESSION_IDLE_TIMEOUT_MS" → render.yaml:8-20; all five carry `value:`; `OPENAI_APPS_CHALLENGE` correctly excluded (has `sync:` only).
8. L64 "`sync: false` on OPENAI_APPS_CHALLENGE (lines 15-16)" → render.yaml:15-16.
9. L65 "The file sets no port" → `grep -in port` no match anywhere (no key, no PORT envVar).
10. L66 "ALLOWED_HOSTS names only ds4cc-marketplace-app.onrender.com (line 12)" → render.yaml:11-12; it is the sole value (line 12), correctly cited by the value line rather than the `key:` line.
11. L67 "Not in the file: domains, plan, region, autoDeployTrigger, renderSubdomainPolicy" → grep no match.
12. L53 "the Dockerfile is blob ee0b6381…" — retained Dockerfile hash matches; render.yaml:5 points at that same path, consistent.

### Supported via collateral files (clone `git show`, read-only)

- L52-53 server.ts blob `649726df…` → rev-parse prints `649726dfcd4bead92195992ed23e03dacd2d23ba`; retained copy matches.
- L60 "default would be the root Dockerfile, which this repository does not use" → `git ls-tree` shows no root Dockerfile.
- L61 ".dockerignore starts with `*`, re-admits only apps-sdk/ sources and marketplace/" → lines 1-9 match; lines 10-11 are `marketplace/**/target/` exclusions, still inside `marketplace/` — claim accurate.
- L62 "server answers GET /health with HTTP 200 (server.ts:193)" → `app.get("/health", … res.json(…))` (res.json defaults 200).
- L65 "EXPOSE 3000"; "server reads PORT with fallback 3000 (server.ts:14), listens on 0.0.0.0 (server.ts:272)" → `EXPOSE 3000` at Dockerfile:15 (retained copy identical); `process.env.PORT ?? "3000"` at :14; `.listen(PORT, "0.0.0.0")` at :272 (also `host: "0.0.0.0"` at :142).
- L66 "server's allow list also has app.ds4cc.com" → `allowedHosts` set includes `new URL(APP_ORIGIN).hostname` (server.ts:16) with `APP_ORIGIN ?? "https://app.ds4cc.com"` (:13).

### Not checkable from retained bytes (process/provenance or live-service claims)

- L54 "(wave-1 seat ScoutDs4ccRenderSurface)" — provenance tag, not a byte fact.
- L55 "Nothing was fetched from the service." — process claim; consistent with bounds, unverifiable from bytes.
- L52 "Read offline with `git -C ~/Projects/ds4cc-marketplace show 1fbdb8ed:render.yaml`" — provenance claim; I reproduced the read and the content matches, but the historical act itself is not checkable.

## Residual risk / notes

- All line-number citations in the section use physical file lines and all are
  correct. No wrong claim found in scope.
- Minor omission (not an error): the file's `name: ds4cc-marketplace-app`
  (render.yaml:3) and `services:` (line 1) are never discussed; the entry's
  singular "the service" phrasing is consistent with the single service listed.
- The `Retained copies` section's last sentence ("server.ts … is not retained")
  is superseded by the appended "Round-32 wave-1 correction" (lines 92-104);
  all four files are retained and hash to the pinned blobs — consistent.
- Doc-derived reasoning (S057–S060 quotes, dashboard behavior) was not
  re-sourced; those clauses are quote facts, not render.yaml facts.
- sandbox: /fast/scratch/hyaku/kake-r32/w1/ReviewEntryRenderYamlTruth/ (scratch only; report is the sole lane write).
- No tools installed; pacman untouched per pause.
