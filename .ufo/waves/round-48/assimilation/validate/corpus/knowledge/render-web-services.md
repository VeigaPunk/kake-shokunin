source: S057, S058, S059, S060 (corpus/SOURCES.md) — https://render.com/docs/blueprint-spec; https://render.com/docs/web-services; https://render.com/docs/docker; https://render.com/docs/health-checks
verified-at: 2026-10-22 (all four opened this round with one public GET each at 2026-10-22T15:41:23Z–15:41:28Z, HTTP 200; retained visible text and receipts under .ufo/waves/round-31/sources/, text sha256 S057 ca8179f2…, S058 983a792d…, S059 f8e60da0…, S060 1f934877…)
recheck: 90d, or on a Render Docs change — re-open each page once (`.ufo/waves/round-31/fetch_sources.py` logic, in a sandbox) and compare the visible-text sha256 with `.ufo/waves/round-31/sources/receipts.json`; the counter `python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision <commit>` replays the retained text only and cannot see a page change
scope: Render platform documentation for web services, Docker-based services, health checks and the Blueprint file (render.yaml), plus an offline key-by-key check of the lane's own render.yaml at ds4cc-marketplace commit 1fbdb8ed. No live request to any operator-owned property; nothing about the live service is asserted.
ground: the four retained Render Docs pages named above and `git show 1fbdb8ed:<path>` reads of ~/Projects/ds4cc-marketplace; every factual sentence about Render carries a curly-quoted span that is an exact substring of one retained text, with the source id in parentheses.
coverage: web-service port binding, deploy on push, Docker build and start, build arguments and secrets, health-check success, failure and deploy rules, Blueprint file location and the keys the lane's file uses, and what the file leaves to Render's defaults.
falsifier: an operator-authorized read of the app.ds4cc.com service settings, or a fresh fetch of the four Render Docs pages, that contradicts any quoted sentence below.
counter: python3 -B .ufo/waves/round-31/c2_quote_truth.py --root . --revision <commit> — 4/4 declared ids expected at the landed commit; strict supplement .ufo/waves/round-31/c2_strict_checks.py 5/5.

# Render web services and the Blueprint file

Coverage-map ground: publishing-platform semantics for the lane's one Render
property, the `app.ds4cc.com` Docker web service recorded in
`publish-channels.md` ("Render — app.ds4cc.com" and its round-30 recheck).
`render-static-sites.md` covers Render static sites, custom domains and TLS;
this entry does not repeat those and cites them where they meet.

## Web services: port, host and deploys

- A web service is rebuilt and redeployed from Git on each push: “Render builds and deploys your code with every push to your linked Git branch.” (S058).
- To receive public traffic it must listen on all interfaces: “Your web service must bind to a port on host 0.0.0.0 to receive HTTP requests from the public internet.” (S058).
- The port Render expects has a default that can be changed: “The default expected port is 10000 (you can configure this ).” (S058). [INFERENCE] The page says the port can be configured but this entry did not retain the page that says how, so the mechanism (the PORT environment variable) is not stated from a source here.
- Every web service keeps a Render host name beside any custom domain: “Every Render web service gets a unique onrender.com subdomain, and you can add your own custom domains .” (S058). Custom-domain and certificate behaviour is in `render-static-sites.md` (S052, S061).

## Docker-based services

- Render can build the image itself from the repository: “Build their own image at deploy time based on the Dockerfile in your project repo.” (S059).
- The container starts with the Dockerfile's own command unless a Docker Command is set: “If Render should run a custom command to start your service instead of using the CMD instruction in your Dockerfile (this is uncommon), specify it in the Docker Command field under Advanced” (S059).
- Service environment variables reach the build: “Render automatically translates those values to Docker build arguments that are available during your image's build process.” (S059), so secrets must not be read as build arguments: “In your Dockerfile, do not reference any build arguments that contain sensitive values (such as passwords or API keys).” (S059).
- The build context is filtered by `.dockerignore`, and secret files are placed in it: “Render omits files and directories from your build context based on your .dockerignore file.” (S059) and “Render copies your service's secret files into the root of your build context.” (S059).
- Docker services deploy without downtime like native ones: “Your Docker-based services support zero-downtime deploys , just like services that use a native language runtime.” (S059).

## Health checks

- A web service can name an HTTP path for checks: “Web services can receive health checks as HTTP GET requests to a path you specify:” (S060).
- Success has a status and a time limit: “For HTTP checks , Render considers a check successful if the instance responds with a 2xx or 3xx status code within five seconds.” (S060).
- A new deploy goes live only when its instances pass together: “Whenever all of the new instances are passing their health checks at the same time , Render considers the deploy successful and starts routing traffic to the new instances.” (S060), and otherwise is cancelled: “If this condition is not met within 15 minutes, Render cancels the deploy and continues routing traffic to your service's existing instances.” (S060).
- A running instance that fails is first taken out of routing and then restarted: “If a running service instance fails consecutive health checks for 15 seconds, Render temporarily stops routing traffic to it to give it an opportunity to recover.” (S060) and “If an instance fails consecutive health checks for 60 seconds, Render automatically restarts the instance .” (S060).
- The checks carry a Host header the app must accept: “If your service has any verified custom domains , Render sets one of those domains as the value of the Host header for all HTTP health checks.” (S060), and “Otherwise, Render uses the service's onrender.com subdomain.” (S060).

## The Blueprint file

- A Blueprint is one file at the repository root by default: “By default, this file has the name render.yaml and resides in your Git repository's root directory” (S057).
- A Blueprint can take over a service that already exists: “If you add the name of an existing service to your Blueprint file, Render attempts to apply the Blueprint's configuration to that existing service.” (S057).
- For many omitted fields the file does not reset an existing service: “Render retains the current value for an existing service.” (S057). [INFERENCE] So the plan, region and deploy trigger of a running service cannot be read from a Blueprint that omits them.
- Environment variables not named in the file are kept: “Render preserves existing environment variables, even if you omit them from the Blueprint file.” (S057).
- Secrets are declared without values: “Do not hardcode these values in your Blueprint file! Instead, you can define these environment variables with sync: false” (S057), and Render asks for them once: “Render prompts you for these values only during the initial Blueprint creation .” (S057). “When you update an existing Blueprint, Render ignores any environment variables with sync: false .” (S057).
- The onrender.com host can be switched off by a field the lane's file does not set: “disabled : The service is not reachable at its onrender.com subdomain.” (S057). The `domains` field text says “Internet-accessible services are always reachable at their onrender.com subdomain.” (S057); [INFERENCE] read together, "always" holds unless `renderSubdomainPolicy` is `disabled`.

## The lane's render.yaml at ds4cc-marketplace 1fbdb8ed

Read offline with `git -C ~/Projects/ds4cc-marketplace show 1fbdb8ed:render.yaml`
(blob `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252`, 20 lines); the Dockerfile is
blob `ee0b63819a9ce71e51469796541b9075e9676ae9` and the server entry
`apps-sdk/src/server.ts` blob `649726df…` (wave-1 seat `ScoutDs4ccRenderSurface`).
Nothing was fetched from the service.

- `type: web` (line 2). The field takes “Required. The type of service. One of the following: web for a web service or static site” (S057); with `runtime: docker` it is a web service, not a static site, so `render-static-sites.md` does not apply.
- `runtime: docker` (line 4). Supported values include “docker for services that build an image from a Dockerfile” (S057).
- `dockerfilePath: ./apps-sdk/Dockerfile` (line 5). The field is “The path to the service's Dockerfile , relative to the repo root.” (S057); the default would be the root Dockerfile, which this repository does not use.
- `dockerContext: .` (line 6). The field is “The path to the service's Docker build context, relative to the repo root.” (S057), and “If omitted, Render uses the repo root.” (S057), so `.` restates the default. The repository's `.dockerignore` starts with `*` and re-admits only `apps-sdk/` sources and `marketplace/`, which by “Render omits files and directories from your build context based on your .dockerignore file.” (S059) keeps the rest of the repository out of the build [INFERENCE: the secret-file copy into the context root is not filtered by this rule, and the Dockerfile copies only `apps-sdk/` and `marketplace` paths].
- `healthCheckPath: /health` (line 7). The field is “The path of the service's health check endpoint . This value always starts with a / character.” (S057). The server answers `GET /health` with HTTP 200 (`server.ts:193`, scout report), which meets “responds with a 2xx or 3xx status code within five seconds.” (S060) [INFERENCE: response time not measured].
- `envVars` (lines 8-20). The file sets values for `APP_ORIGIN`, `ALLOWED_HOSTS`, `ALLOWED_ORIGINS`, `MAX_UNAUTHENTICATED_SESSIONS` and `MCP_SESSION_IDLE_TIMEOUT_MS`; other variables set in the dashboard survive, since “Render preserves existing environment variables, even if you omit them from the Blueprint file.” (S057).
- `sync: false` on `OPENAI_APPS_CHALLENGE` (lines 15-16). Its value lives only in Render; “When you update an existing Blueprint, Render ignores any environment variables with sync: false .” (S057), so changing or adding this secret later is a dashboard step, not a Blueprint edit.
- Port. The file sets no port. The image says `EXPOSE 3000`, and the server reads `PORT` with fallback 3000 and listens on host `0.0.0.0` (`server.ts:14`, `server.ts:272`, scout report). That meets “Your web service must bind to a port on host 0.0.0.0 to receive HTTP requests from the public internet.” (S058). [INFERENCE] Whether Render's expected port is 10000 or 3000 for this service is a dashboard setting not visible here; the app follows `PORT` when Render sets it.
- Host header. `ALLOWED_HOSTS` names only `ds4cc-marketplace-app.onrender.com` (line 12), and the server's allow list also has `app.ds4cc.com`. Because “Render sets one of those domains as the value of the Host header for all HTTP health checks.” (S060) when a custom domain is verified, a health check would carry `app.ds4cc.com` or the onrender host; [INFERENCE] both are in the server's list, so the check is not refused for its Host, but a new custom domain would need to be added to that list first.
- Not in the file: `domains`, `plan`, `region`, `autoDeployTrigger`, `renderSubdomainPolicy`. For an existing service these keep their current values (S057, quoted above), so this file cannot show where or how the live service runs.

## Round-31 wave-2 corrections (appended; supersede the lines named)

- Supersedes the `[INFERENCE]` at line 22 (found by wave-2 seat `CriticLearningClaimAfter`). The retained S058 text does name the mechanism: “The default value of PORT is 10000 for all Render web services.” (S058), “You can override this value by setting the environment variable for your service in the Render Dashboard” (S058), and “If you bind your HTTP server to a different port, Render is usually able to detect and use it.” (S058).
- Supersedes the `[INFERENCE]` at line 65. Render sets `PORT` (default 10000, per the quotes above) and the server reads `PORT` before its 3000 fallback (`server.ts:14`), so with no Dashboard override the server binds 10000, the expected port; `EXPOSE 3000` in the image does not change that [INFERENCE: whether the live service has a Dashboard override is not visible here].
- Build arguments: `apps-sdk/Dockerfile` at `1fbdb8ed` has no `ARG` instruction (`git -C /home/vgpnk/Projects/ds4cc-marketplace show 1fbdb8ed:apps-sdk/Dockerfile | grep -c ARG` prints 0), so although “Render automatically translates those values to Docker build arguments that are available during your image's build process.” (S059), the build never reads `OPENAI_APPS_CHALLENGE` [INFERENCE: build arguments that no `ARG` declares are not used by the build].
- Supersedes the bracketed `[INFERENCE]` at the end of line 61 (found by wave-2 seat `CriticEntryInferences`). S059 says secret files are subject to `.dockerignore`: “To keep them out of your image, add them to .dockerignore” (S059). The lane's `.dockerignore` starts with `*`, so a secret file at the context root is excluded unless a later `!` pattern re-admits its name [INFERENCE: re-include patterns not checked against a Docker source].
- Narrows line 67. S057 states a retain rule field by field, not for every omitted field: “Render retains the current IP ranges for an existing service.” (S057) is one such field text, while for `region` it gives only a new-service default: “If omitted for other service types, the default value is oregon” (S057). This entry did not check a retain rule for `domains` or `renderSubdomainPolicy`, so line 67's “keep their current values” is an [INFERENCE] for those fields, and it assumes the live service is managed by this Blueprint, which was not observed.
- Narrows line 23: the onrender.com host is kept only while `renderSubdomainPolicy` allows it (line 48 of this entry); the live value of that field is not known from the file.
- Marks line 39 (wave-2 seats `ReviewEntryHealthBlueprint`, `CriticQualityCriteria`): "the app must accept" that Host header is an [INFERENCE]; S060 states only which Host value Render sends, not an obligation on the app. Line 48's reading also omits that disabling the onrender.com subdomain applies to a service with a custom domain, per S057's `renderSubdomainPolicy` text.

## Retained copies (round 32, append-only)

The two ds4cc-marketplace files read offline above are now retained in this
lane byte-identical to the external blobs (S062):
`.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/render.yaml` (`git hash-object`
prints `d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252`) and
`.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/apps-sdk/Dockerfile`
(`ee0b63819a9ce71e51469796541b9075e9676ae9`). A fresh session re-checks the
render.yaml and Dockerfile sentences in the section above against those
copies (S062) without the external clone; `apps-sdk/src/server.ts` (blob
`649726df…`) is not retained, so the sentence about the server's allow list
still needs the external repository.

## Round-32 wave-1 correction (appended; supersedes the last sentence of the section above)

Wave-1 seat `CriticC2Scope` found that more sentences than "the server's allow
list" rested on unretained files: `apps-sdk/src/server.ts` supports the Port,
Host-header and listen-host sentences, and `.dockerignore` supports the secret
file sentences. Both are now retained byte-identical as well (S062):
`.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/apps-sdk/src/server.ts`
(`649726dfcd4bead92195992ed23e03dacd2d23ba`) and
`.ufo/waves/round-32/sources/ds4cc-1fbdb8ed/.dockerignore`
(`d650445a62b723cb8331eb0159756d3cbfacc502`), so every ds4cc-marketplace
fact in this entry can be re-checked from lane bytes. Drift check
2026-10-22T19:00Z (read-only): the local clone's HEAD is `1fbdb8ed` and its
tree holds the same four blob ids; the remote `main` is `7fc6aa2`, one commit
ahead, which wave-1 seat `ScoutGithubPin` reports touches only `magga/**` and
`sitemap.xml` (not re-checked by the L1).
Re-check step for S062 (no network needed beyond a fetch the operator
allows): `git -C ~/Projects/ds4cc-marketplace diff --stat 1fbdb8ed <new HEAD> -- render.yaml apps-sdk/Dockerfile apps-sdk/src/server.ts .dockerignore`;
an empty result means the retained copies still match the repository.
