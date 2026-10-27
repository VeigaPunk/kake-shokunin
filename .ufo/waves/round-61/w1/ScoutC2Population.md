# ScoutC2Population

Recon of the round-23 capture population for the C2 round-61 capture run. Sources read: every `fetch.json` and `manifest.json` under `.ufo/waves/round-23/live/<id>/` (4 ids have no `manifest.json`). Live probe: one GET per url on 2026-10-27 (probe started ~09:15 UTC), status + finalUrl + content-type only, body discarded, UA `round61-scout-recon`. Raw probe output: `ScoutC2Population.files/probe-results.tsv`.

## POPULATION:

| id | url | expectedCanonical (manifest) | r23 status / finalUrl | today status / finalUrl |
|---|---|---|---|---|
| burnerchrome-kimi | https://burnerchrome.kimi.page/ | https://burnerchrome.kimi.page/ | 200 / same | 200 / same |
| charter-ghp | https://veigapunk.github.io/charter-ufo-fsd/ | https://veigapunk.github.io/charter-ufo-fsd/ | 200 / same | 200 / same |
| charter-kimi | https://charter-ufo-fsd.kimi.page/ | (no manifest.json) | 404 / same | 404 / same |
| ds4cc-kimi | https://ds4cc.kimi.page/ | https://ds4cc.com/ | 200 / https://ds4cc.kimi.page/ | 200 / same |
| ds4cc-primary | https://ds4cc.com/ | https://ds4cc.com/ | 200 / same | 200 / same |
| lucario-ghp | https://veigapunk.github.io/lucario/ | https://veigapunk.github.io/lucario/ | 200 / same | 200 / same |
| lucario-kimi | https://lucario.kimi.page/ | (no manifest.json) | 404 / same | 404 / same |
| plazir15-ghp | https://veigapunk.github.io/plazir-15-site/ | https://veigapunk.github.io/plazir-15-site/ | 200 / same | 200 / same |
| plazir15-kimi | https://plazir15.kimi.page/ | (no manifest.json) | 404 / same | 404 / same |
| plazir27-kimi | https://plazir27.kimi.page/ | (no manifest.json) | 404 / same | 404 / same |
| ufo-fsd-kimi-pro | https://ufo-fsd.kimi.pro/ | https://ufo-fsd.kimi.pro/ | 200 / same | 200 / same |
| vault-index-kimi | https://veigapunk.kimi.page/ | https://veigapunk.kimi.page/ | 200 / same | 200 / same |

## CHANGES:

- Reachability: all 12 hosts answer on the recorded https scheme today; no dead, moved, or redirect-changed surfaces. `curl_rc=0` for every probe; `num_redirects=0` and finalUrl == url for all 12.
- Status deltas vs round-23 record: none. The 8 manifest-bearing surfaces still return 200 at their recorded finalUrls; the 4 manifest-less surfaces (charter-kimi, lucario-kimi, plazir15-kimi, plazir27-kimi) still return 404 — the same state as the round-23 fetch (kimi.page 404 page, r23 sha256 93ddca9a… on all four).
- canonical note (pre-existing, unchanged): ds4cc-kimi serves 200 at https://ds4cc.kimi.page/ while its manifest's expectedCanonical is https://ds4cc.com/; the round-23 fetch recorded the same 200-with-no-redirect shape. Capture/audit should treat url and expectedCanonical as distinct fields.
- Content-types seen today: `text/html; charset=utf-8` on charter-ghp, ds4cc-primary, lucario-ghp, plazir15-ghp, ufo-fsd-kimi-pro, and the four 404s; bare `text/html` on burnerchrome-kimi, ds4cc-kimi, vault-index-kimi.
- Implication for the C2 capture: all 12 ids are capturable today; the 4 standing 404s will record non-2xx statuses, which the audit's expectation classes already accommodate (content_type_present is 2xx-scoped per case H11; hsts/csp presence checks must not fire on 404 records unless declared).

VERDICT: Population stable — 12/12 surfaces reachable, statuses and finalUrls unchanged vs the round-23 record; no dead or moved urls; capture can proceed on all ids.
