source: S459 — https://developer.chrome.com/docs/crux/vis — “Access CrUX Vis” and “Does it work for all websites?”; reopened GET-only 2026-11-04, HTTP 200; retained `.ufo/waves/round-86/w1/ScribeAssim/docs.html` lines 2918–2936 (page last updated 2025-05-06 UTC).
source: S460 — https://chromeuxreport.googleapis.com/v1/records:queryRecord — lane own-work observation re-run 2026-11-04: one keyless POST with `{"origin":"https://example.com"}`, HTTP 403, `error.status=PERMISSION_DENIED`; complete response `.ufo/waves/round-86/w1/ScribeAssim/probe.json`, headers `probe.headers` in the same directory.
verified-at: 2026-11-04
recheck: Reopen the documentation when its no-data or canonical-origin guidance changes, and before relying on it after 180 days. Re-verify the refusal observation only with authorization for the exact keyless probe; compare HTTP status, error status, and caller-identity message. Source changes or a successful anonymous response require revising this entry; never infer eligibility from a caller-identity failure.
ground: field performance — CrUX coverage guidance and the observed boundary of an unauthenticated API request.

# Checking CrUX coverage without an API key

The CrUX API refused this lane’s unauthenticated request for `https://example.com` on 2026-11-04 [S460]: HTTP 403, `error.status` equal to `PERMISSION_DENIED`, and a message requiring an API key or another form of API consumer identity. This is evidence about the caller’s access, not evidence that the requested origin lacks CrUX data. Credentials and consumer-identity setup remain outside this entry.

The current documentation describes a dashboard route [S459]: CrUX Vis visualizes weekly historical data from the CrUX History API; users visit `cruxvis.withgoogle.com` and enter an origin or URL. This route is documented here, not exercised in this observation.

The no-data condition is explicit (20 words, S459, retained HTML line 2932):

> If your origin is not included in the CrUX dataset, there will be no data to display.

The documentation also notes insufficient data, wrong protocol, omitted subdomains, and redirects. Its guidance is to use the canonical origin after a redirect; if a protocol is omitted, HTTPS is assumed. URL-level data may be unavailable even when origin-level data is available [S459].

An operator investigating “no data” should therefore distinguish a missing dataset entry from querying the wrong origin form, and distinguish origin-level coverage from URL-level coverage. These checks guide investigation; they do not guarantee that a keyless check uniquely determines why data is absent. The API refusal must not be substituted for such an investigation.

## What this entry does not establish

- No lane property’s eligibility outcome was measured. The only API payload used `https://example.com`; the response was an access refusal, not a coverage result.
- No metric values or origin/URL coverage verdict were returned or established.
- CrUX Vis was not opened, rendered, or queried. The documented dashboard route is not a successful keyless retrieval receipt.
- The observation does not establish that all keyless routes fail, or that this API refusal persists at another time or for another caller identity.
- It does not establish eligibility criteria, revise the held methodology, authorize credentials, or authorize measurement of operator-owned properties.
- Adoption is a lane-local draft until integration; the source-id collision proof and scratch-mirror census gate must pass before any registry append.
