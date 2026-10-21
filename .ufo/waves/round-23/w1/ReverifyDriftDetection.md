## Verdict

C1 `drift-detection`: 6 load-bearing claims checked against their live local/public surfaces on 2026-10-21; 5 HOLD and 1 STALE. No claim in this receipt is UNVERIFIABLE. This is a freshness receipt only, not an independent admission.

## Findings

### P2 — `plazir27.kimi.pro` no longer presents the cited Function-Compute response path

- Exact command: `curl --silent --show-error --location --max-time 30 --dump-header /tmp/kake-r23-ReverifyDriftDetection-Cwa2/plazir27-get.headers --output /tmp/kake-r23-ReverifyDriftDetection-Cwa2/plazir27-get.body --write-out 'http_code=%{http_code} url=%{url_effective} size_download=%{size_download} content_type=%{content_type}\n' https://plazir27.kimi.pro`
- Exact observed output: `http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html`. Captured response headers: `HTTP/2 302`, `location: https://statics.kimi.ai/pages/preview-404-en.html`, `server: cloudflare`; then `HTTP/2 200`, `server: Byte-nginx`, `content-length: 5995`, `x-request-id: d006fefde588a635fd54dbba470aa211`. The body contains `<title>404</title>` and `404 Page Not Found`; no `x-fc-request-id` was observed.
- Impacted claim/axis: C1 freshness, `drift-detection` line 28–30 anchor below.
- Smallest fix: replace the old ingress/header assertion with the dated 302-to-`statics.kimi.ai` then 200 `Byte-nginx` observation; retain the warning that HTTP 200 alone does not mean the page is live.

```json
{
  "unit": "drift-detection",
  "path": "corpus/knowledge/drift-detection.md",
  "observedAt": "2026-10-21",
  "claims": [
    {
      "id": "c1",
      "anchor": "the webzites and plazir source trees remain absent after the 2026-10-12 prune.",
      "claim": "The documented webzites and plazir-15-site source trees are absent locally.",
      "surface": "/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site",
      "method": "test -e",
      "observation": "absent /home/vgpnk/Projects/webzites\nabsent /home/vgpnk/Projects/plazir-15-site",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    },
    {
      "id": "c2",
      "anchor": "`ufo-fsd.kimi.pro` is a 612B React shell",
      "claim": "GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.",
      "surface": "GET https://ufo-fsd.kimi.pro",
      "method": "GET",
      "observation": "http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\"root\"></div>.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    },
    {
      "id": "c3",
      "anchor": "GET it, don't HEAD (HEAD→403).",
      "claim": "HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.",
      "surface": "HEAD https://ufo-fsd.kimi.pro",
      "method": "HEAD",
      "observation": "http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    },
    {
      "id": "c4",
      "anchor": "`plazir27.kimi.pro` returns 200 with a 5,995B preview-404 body (x-fc-request-id, Function-Compute ingress).",
      "claim": "The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.",
      "surface": "GET https://plazir27.kimi.pro",
      "method": "GET",
      "observation": "http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.",
      "verdict": "STALE",
      "correction": "As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.",
      "reason": ""
    },
    {
      "id": "c5",
      "anchor": "canonical = `veigapunk.github.io/lucario/` (live)",
      "claim": "The cited canonical GitHub Pages Lucario URL still serves the page.",
      "surface": "GET https://veigapunk.github.io/lucario/",
      "method": "GET",
      "observation": "http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario</h1>.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    },
    {
      "id": "c6",
      "anchor": "plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path",
      "claim": "Both explicitly named dead-slot Kimi pages still return HTTP 404.",
      "surface": "GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page",
      "method": "GET",
      "observation": "https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.",
      "verdict": "HOLD",
      "correction": "",
      "reason": ""
    }
  ]
}
```

## Checked and held

- Local source-tree claim: `test -e` checks returned exactly `absent /home/vgpnk/Projects/webzites` and `absent /home/vgpnk/Projects/plazir-15-site`.
- `ufo-fsd.kimi.pro`: GET returned `http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8`; body showed the cited DS4CC shell with an asset bundle and root div. HEAD returned `http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8`.
- Canonical Lucario URL: GET returned `http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8`; the observed body title and heading were both `lucario`.
- Dead-slot pages: GET `https://plazir15.kimi.page` returned `http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8`; GET `https://charter-ufo-fsd.kimi.page` returned `http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8`.

### Skipped claims and why

- The listed `webzites` command behavior (`probe`, `grokbot reconcile`, `sync-check`, `kimi-map`, `tick`; lines 14–18) was not run: its documented source tree is absent, so the historical command descriptions cannot be checked against the implementation or current configuration.
- The `in-sync*`/digest semantics, `reconcile` index-only coverage, probe blind spot, marker-vs-byte-twin behavior, and `vault PROPERTIES[]` findings (lines 23–37 and 48) were not re-derived. They require the missing scripts, source snapshots, or mutation fixtures; ordinary GET/HEAD observations cannot establish those tool behaviors.
- Dated row states and counts not represented by the explicit URLs tested above (the 2026-09-26 table and 2026-09-28 probe/sync-check totals and row aliases, lines 39–69) were not treated as current claims. The historical run/config/history files under the missing `webzites` tree are unavailable, and row aliases alone are not a safe substitute for the original URL/sourceDir map.
- The plazir15-ghp sitemap/source/origin comparison and its `origin/main..HEAD` count (lines 71–91) were not re-derived: `/home/vgpnk/Projects/plazir-15-site` is absent, and the unit does not give an exact current live URL for that GHP row. No current source or origin comparison was possible.
- The round-20 citation-local note (line 95) is an explicitly dated historical note, not a separately testable live behavior; the source-tree absence it records is covered by claim c1.

## Limits

Only read-only local existence checks and public HTTP GET/HEAD requests were used. No authentication, cookies, form submissions, publishing, deployment, or source-tree execution occurred. The absent repository prevents implementation-level validation of the historical CLI and its stored state. No tools were installed or updated.
