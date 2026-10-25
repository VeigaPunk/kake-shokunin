
source: S303 — https://developer.chrome.com/docs/crux/vis — § "Access CrUX Vis" and "Does it work for all websites?" (doc rev. Last updated 2025-05-06 UTC) — fetched 2026-10-23
source: S304 — https://chromeuxreport.googleapis.com/v1/records:queryRecord — POST response body, `error.status` = PERMISSION_DENIED (own observation, 2026-10-23) — fetched 2026-10-23
verified-at: 2026-10-23
recheck: 180d — `curl -fsSL 'https://developer.chrome.com/docs/crux/vis' | grep -c 'may not have sufficient data to be included'` -> 1; `curl -sS -X POST -H 'Content-Type: application/json' --data '{"origin":"https://example.com"}' 'https://chromeuxreport.googleapis.com/v1/records:queryRecord' | grep -c 'PERMISSION_DENIED'` -> 1
ground: field performance — the CrUX eligibility question, answered to the edge of what a keyless reader can settle

# Checking CrUX coverage without an API key

Round 1 closed the *surfaces* of field performance and left the eligibility question open. The
API route to an answer is blocked by a key requirement, and the probe records it [S304]:
the CrUX API answers an unregistered caller with HTTP 403 and

> "Method doesn't allow unregistered callers (callers without established identity)." (S304)

with `error.status` = `PERMISSION_DENIED` and the message asking for an API key or another
form of API consumer identity. So the named source in round 1's ledger cannot be called at all
until a Cloud API key exists — which belongs to the secrets lane, not to this one.

There is, however, a key-free route to the same question [S303]. CrUX Vis is a dashboard over
the History API's weekly history, reached at `cruxvis.withgoogle.com` by entering an origin or
URL. The same page answers the failure case directly:

> "If your origin is not included in the CrUX dataset, there will be no data to display." (S303)

and names the false-negative causes — the wrong protocol (`http://` where `https://` was meant),
an omitted subdomain, and a redirect to a different host, in which case the canonical version
is the one to query.

The publisher-side rule: **"no CrUX data" has three distinguishable causes** — the origin is
not in the dataset, it is in the dataset under a different origin string, or the query used the
wrong protocol/host form. A keyless check answers which one applies; the API with a key then
answers the metric values.

## What this entry does not establish

- It does not establish the eligibility **outcome for any lane property** — no lane origin was
  queried through CrUX Vis or the API, because that is a measurement of an operator-owned
  property and the API path is key-blocked in any case. The check remains a named operator step.
- It does not establish the metric values for any origin.
- It does not change the held eligibility methodology row (S038); it supplies the operator-facing
  route to it.

---
