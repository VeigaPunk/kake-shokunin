# W1 frontier step (routed item 7) — screen one non-primary Render Docker / health-check page

Verdict: **REJECT** candidate S064. Nothing written to `corpus/SOURCES.md`; this file is the only lane write.

## Candidate and access record

- URL: https://osher.com.au/blog/how-to-host-n8n-on-render-com/
- Command: `curl -sS -L --max-time 45 -A 'Mozilla/5.0 (compatible; kake-scribe/1.0)' -o osher.html -w 'status=%{http_code} bytes=%{size_download} url=%{url_effective}' https://osher.com.au/blog/how-to-host-n8n-on-render-com/`
- Result: `status=200 bytes=91504 url=https://osher.com.au/blog/how-to-host-n8n-on-render-com/`; shell exit 0
- Access time UTC: 2026-10-22T19:00:21Z (GET issued) to 2026-10-22T19:00:22Z
- Saved copy: `/fast/scratch/hyaku/kake-r32/w1/ScribeScreenDockerCandidate/osher.html`, sha256 `b2894fcd1b6fdb7be97dc0ed9da8acbfa49eed084d27af96156db999aeb3e734`, 91504 bytes
- Plain GET only; no browser, no challenge or access control met, no owned property touched (osher.com.au is not in `corpus/knowledge/freshness-pins.json` and is not the operator's).

## Located quote (20 words)

> "Rewritten to reflect Render’s current pricing, the move to native Docker support, and the production patterns we run for clients."

Location: page body, the status paragraph immediately under the byline, directly after the visible line "Updated May 2026."; rendered text line 4 of the extraction (`osher.txt:4`), raw HTML in the inline `"body"` JSON at byte offset 9149 of `osher.html`.

## Drafted row (11 cells, S064) — for the L1, not applied

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S064 | Osher Digital: Hosting n8n on Render.com — Lessons from Production — https://osher.com.au/blog/how-to-host-n8n-on-render-com/ | community | C | A consultancy's n8n-on-Render case study: a prebuilt Docker image as a Render web service with a disk, and the render.yaml that declares it; not Render's documented Dockerfile build, not its health-check rules, and not a statement about the operator's own service | Status paragraph under the byline ("Updated May 2026. Rewritten to …") and the render.yaml block: `runtime: image`, `image.url: docker.io/n8nio/n8n:1.94.0`, `disk.mountPath: /home/node/.n8n`, `healthCheckPath: /healthz`; fetched 2026-10-22T19:00:21Z | REJECTED: the Docker service it configures is a prebuilt image (`runtime: image` + `image.url`), outside S059's Dockerfile-build scope, and the field itself belongs to S057's Blueprint-spec scope [INFERENCE: S057's body was not re-opened this seat, so I do not assert it names `runtime: image`]; its only health-check content is the bare `healthCheckPath: /healthz` line, which states nothing about success criteria, timing or Host that S060 does not already carry; the page also carries four disagreeing dates (visible byline "June 27, 2024"; JSON-LD datePublished 2024-06-28T00:00:00+10:00; visible "Updated May 2026"; footer "Last updated on July 1, 2026"; JSON-LD dateModified 2026-07-02T08:35:49+10:00), so a recheck interval cannot be anchored to the revision actually read. flip: the page states a Docker-service or health-check rule in a locatable sentence that S059 or S060 does not already carry, and its visible and structured dates agree on one revision date | rejected | 2026-10-22 | 90d | — |

## Why reject (evidence, against S059/S060)

1. Docker content is out of the row's primary scope. The Blueprint it teaches is `runtime: image` with `image.url: docker.io/n8nio/n8n:1.94.0` (render.yaml block, `osher.txt:35-37`). S059's own scope cell is "building from a repository Dockerfile, the start command, build arguments, .dockerignore and secret files" — a prebuilt image build is a different path. The page does mention the Dockerfile option but only to dismiss it: "We rarely need this for n8n." (`osher.txt:110`).
2. Health-check content is one key, no rule. The only health-check text is `healthCheckPath: /healthz` (`osher.txt:44`); grep over the 16587-byte extraction for `unhealthy|restart|probe|timeout|zero-downtime` returns one unrelated n8n disk sentence at `osher.txt:152`. S060 already carries success criteria (2xx/3xx, five seconds), the 15-minute cancel, the 15-second routing stop and 60-second restart, and the Host rule — none of which this page states.
3. Freshness: the page cannot be date-anchored. Five date signals, four distinct days: byline "June 27, 2024" (HTML offset 57517), JSON-LD `datePublished 2024-06-28`, visible "Updated May 2026.", footer "Last updated on July 1, 2026", JSON-LD `dateModified 2026-07-02`. The body says it was "Rewritten" (`osher.txt:4`), so the 2024 byline does not describe the bytes read, and no single date can carry a 90-day recheck.

## Secondary page opened the same session (not the screened candidate)

- https://mymcptools.com/blog/deploying-mcp-to-render — `status=200 bytes=77007`, sha256 `8cc3486ced29c4a1f799a35c814f4c3c8503d1075728ba272fc0db3e0d15dee0`, GET at 2026-10-22T18:59:25Z; dates agree (visible and JSON-LD both 2026-05-31).
- Rejected on scope when compared: it says "no Dockerfile required" (`mymcp.txt:2`) and its health-check sentence, "Render polls this endpoint and automatically restarts the service if it becomes unhealthy" (`mymcp.txt:100`), drops S060's 15-second routing stop, the 60-second restart threshold and the 2xx/3xx-within-five-seconds criterion. Not drafted as a row; kept only as a negative observation.

## Not verified / limits

- I did not read either page end to end; I read the byline and render.yaml regions of the Osher page and the health-check and opening regions of the MyMCPTools page.
- I did not re-open S057's body or S059/S060 bodies this seat; comparisons use the registry cells quoted above plus `corpus/knowledge/render-web-services.md:25-39` and `:58-62`.
- No live request to ds4cc.com, app.ds4cc.com, any operator onrender.com host, kimi.page, kimi.pro, veigapunk.github.io, or any host in `freshness-pins.json`.
- No tools installed or updated; no pacman run.
- Nothing written outside `/fast/scratch/hyaku/kake-r32/w1/ScribeScreenDockerCandidate/` and this report file.
