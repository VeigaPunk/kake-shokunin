## Verdict

**Counterexample found to complete C1 freshness across the canonical surfaces; none against the assigned c4 correction sentence.** Receipt claim c4 is genuinely STALE as phrased: the current `plazir27.kimi.pro` GET redirects before the final preview-404 response, and neither hop showed `x-fc-request-id` or Function-Compute ingress evidence. The correction in `corpus/knowledge/drift-detection.md:104` is true, complete for this c4 observation, date/response-scoped, and not overclaiming. The 5,995-byte/title-404 body description itself still matches.

## Findings

### P2 — stale c4 Function-Compute assertion remains in `SKILL.md`

- **Evidence:** `SKILL.md:292` still states: `` `plazir27.kimi.pro` = Function-Compute ingress serving preview-404. `` The SKILL round-23 section found at line 418 is for `property map`; there is no drift-detection c4 correction in that file. In contrast, `corpus/knowledge/drift-detection.md:104` has the corrected c4 entry.
- **Impact:** C1 freshness across the canonical knowledge surfaces. The stale, unqualified SKILL statement contradicts the live response and leaves readers of that surface with the old ingress attribution.
- **Read-only live command and exact output (relevant headers):**
  ```text
  curl -sS -o /dev/null -D - https://plazir27.kimi.pro
  HTTP/2 302
  location: https://statics.kimi.ai/pages/preview-404-en.html
  server: cloudflare
  ```
  ```text
  curl -sS -o /dev/null -L -D - -w 'EFFECTIVE url=%{url_effective} code=%{http_code} size=%{size_download}\n' https://plazir27.kimi.pro
  HTTP/2 302
  location: https://statics.kimi.ai/pages/preview-404-en.html
  server: cloudflare
  HTTP/2 200
  server: Byte-nginx
  content-length: 5995
  x-request-id: f690590ad5a9f84eff53a9a1dd386598
  EFFECTIVE url=https://statics.kimi.ai/pages/preview-404-en.html code=200 size=5995
  ```
  Neither hop's returned headers contained an `fc-`/`function` marker. The final request ID is per-request and is evidence only for that response.
- **Smallest fix:** Update or remove `SKILL.md:292` and propagate the dated redirect/Byte-nginx correction there, or explicitly mark the old statement as historical rather than current.

## Checked and held

- **c4 verdict:** STALE is correct. The old ingress/header portion is not supported by the live response; the preview-404 page remains, but GET now gives 302 to `statics.kimi.ai/pages/preview-404-en.html`, followed by 200 from Byte-nginx.
- **Correction truth and completeness:** Its stated redirect destination, final status/server, 5,995-byte size, title, `x-request-id`, and “not observed x-fc-request-id” all matched the recheck. The correction does not claim the endpoint is permanently configured this way; “not supported by this response” is appropriately narrow.
- **Body probe:**
  ```text
  curl -sS -L -o /tmp/kake-r23w2-StaleDriftDetection-RYH7/body.html -w 'code=%{http_code} size=%{size_download}\n' https://plazir27.kimi.pro && grep -c -i "fc-" /tmp/kake-r23w2-StaleDriftDetection-RYH7/body.html; grep -o "<title>[^<]*</title>" /tmp/kake-r23w2-StaleDriftDetection-RYH7/body.html
  code=200 size=5995
  0
  <title>404</title>
  ```
- **Cache-miss check against the redirect destination:**
  ```text
  curl -sS -o /dev/null -D - -w 'code=%{http_code} size=%{size_download}\n' "https://statics.kimi.ai/pages/preview-404-en.html?cachebust=kaker23w2a7x"
  HTTP/2 200
  server: Byte-nginx
  content-length: 5995
  x-bdcdn-cache-status: TCP_MISS,TCP_MISS
  x-request-id: c05cf9d4069f4723938260536575d9e6
  x-tos-cs-type: CDN
  code=200 size=5995
  ```
- **Repeatability:** Three subsequent followed GETs each output `code=200 size=5995`, `url=https://statics.kimi.ai/pages/preview-404-en.html`, `hop_code=1`.
- **No P1 correction error found:** the assigned correction in `drift-detection.md` matches the live response and avoids a durable/future claim.

## Limits

Read-only probes were made on 2026-10-21. They establish the observed route and response for these requests, not future availability or all possible client/request variants. The cache-miss probe targeted the redirect destination with a unique query; it does not independently establish every possible origin configuration. No installs, builds, tests, or production edits were performed.
