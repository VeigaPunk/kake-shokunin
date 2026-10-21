## Verdict

Counterexample found: none. The STALE verdicts for fleet-registry c5, c6, and c7 are supported by my read-only live checks, and each correction in the round-23 knowledge section is true, complete for the scoped claim, and not overclaiming.

## Findings

None (no P0–P3 finding; no fix required).

## Checked and held

- **c5 — confirmed STALE; correction held.** Receipt: `.ufo/waves/round-23/receipts/fleet-registry.json:48-56`; baseline row: `corpus/knowledge/fleet-registry.md:55`; correction: `corpus/knowledge/fleet-registry.md:95`. Exact live-check command:
  ```sh
  curl -sS --max-time 30 -L -o /tmp/kake-r23w2-StaleFleetRegistry-kL9Blz/plazir27.html -w 'plazir27 http=%{http_code} final=%{url_effective} bytes=%{size_download} redirects=%{num_redirects}\n' https://plazir27.kimi.page/
  ```
  Exact output: `plazir27 http=404 final=https://plazir27.kimi.page/ bytes=13409 redirects=0`. The fetched body contains `<title>404</title>` and `404 Page Not Found`. This contradicts the row's present-tense “live (canonical kimi charter)” claim. The correction accurately limits itself to the URL's 2026-10-21 response and does not infer that the charter is absent elsewhere or that the URL was never published.

- **c6 — confirmed STALE; correction held.** Receipt: `.ufo/waves/round-23/receipts/fleet-registry.json:59-67`; baseline row: `corpus/knowledge/fleet-registry.md:53`; correction: `corpus/knowledge/fleet-registry.md:96`. Exact live-check command:
  ```sh
  curl -sS --max-time 30 -L -o /tmp/kake-r23w2-StaleFleetRegistry-kL9Blz/plazir27runson.html -w 'plazir27runson http=%{http_code} final=%{url_effective} bytes=%{size_download} redirects=%{num_redirects}\n' https://plazir27runson.kimi.page/
  ```
  Exact output: `plazir27runson http=404 final=https://plazir27runson.kimi.page/ bytes=13409 redirects=0`. The fetched body contains `<title>404</title>` and `404 Page Not Found`. This contradicts the row's present-tense “live (Night Trilogy)” status at this URL. The correction is URL- and date-bounded; it does not claim that the Night Trilogy content is unavailable at every location.

- **c7 — confirmed STALE; correction held.** Receipt: `.ufo/waves/round-23/receipts/fleet-registry.json:70-78`; baseline row: `corpus/knowledge/fleet-registry.md:63`; correction: `corpus/knowledge/fleet-registry.md:97`. Exact live-check command:
  ```sh
  curl -sS --max-time 30 -L -o /tmp/kake-r23w2-StaleFleetRegistry-kL9Blz/xsnapshot.html -w 'xsnapshot http=%{http_code} final=%{url_effective} bytes=%{size_download} redirects=%{num_redirects}\n' https://xsnapshot.app/ && getent ahosts xsnapshot.app
  ```
  Exact curl output: `xsnapshot http=200 final=https://xsnapshot.app/ bytes=1985 redirects=0`. `getent ahosts` returned IPv4 addresses `172.67.202.253`, `104.21.22.61` and IPv6 addresses `2606:4700:3032::ac43:cafd`, `2606:4700:3030::6815:163d`. The response body contains `<title>xsnapshot — your X profile, persistent and crawlable</title>` and `domain live · build in progress`. This verifies resolution, HTTP 200, and the quoted page tag. The correction appropriately says only that NXDOMAIN is no longer a valid basis for the row; it does not say the build is finished or that the `queued` label itself must be removed. The knowledge file defines `queued` as “awaiting operator action” (`corpus/knowledge/fleet-registry.md:39-41`), which is consistent with the live page's “build in progress” tag.

Body-marker checks used the saved GET responses: regex `<title>404</title>|404 Page Not Found` matched both Kimi bodies, and regex `<title>|domain live|build in progress` matched the xsnapshot title and tag. All requests were public GETs; no authentication, cookies, or writes were used. No tools were installed.

## Limits

These are point-in-time checks on the listed root URLs only. They do not establish later availability, historical publication state, alternate paths, or whether the queued xsnapshot work has completed. The corrections make no such claims.