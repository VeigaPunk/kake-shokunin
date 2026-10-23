# ScoutRobotsRefetch — freshness of the round-37 live robots set

Tip 79d3c780; written 2026-10-23T03:48Z. Sandbox-only; no installs; no owned-host request.

## Attacked

1. `corpus/lessons/round-37.md:104-105`: "the served `/robots.txt` of 12 hosts at
   03:23:15Z–03:23:31Z (all HTTP 200; receipts `realrun/robots/receipts.json`)".
2. Provenance strength: does any committed validator bind the bodies to the receipt hashes?

## Re-fetch — 10 non-owned hosts, one GET each, 1 s apart

```
export TMPDIR=/fast/scratch/hyaku/kake-r37w2/ScoutRobotsRefetch/tmp
for u in <10 urls>; do curl -sS --max-time 45 -A 'kake-shokunin-round37/1.0 (...)' \
  -o refetch/<host>.txt -w '%{http_code} %{size_download}' "$u"; sleep 1; done   # exit 0
```
Window 03:44:59Z–03:45:11Z (22 min after capture). Second pass `-A 'Googlebot'` (the
manifest's check UA), 03:46:15Z–03:46:27Z, exit 0.

| host | vs receipt | status/bytes/redir | sha256 |
|---|---|---|---|
| www.rfc-editor.org | same | 200/135/0 | df052cf3…3827 |
| developers.google.com | same | 200/93/0 | 2d1ba192…cdba |
| github.com | same | 200/14540/0 | b622e2dd…9956 |
| docs.github.com | same | 200/13/0 | d9066d29…56bb |
| www.sitemaps.org | same | 200/45/0 | 19edcf7d…dd2d |
| developer.mozilla.org | same | 200/119/0 | 8f2712e1…273a |
| en.wikipedia.org | same | 200/28275/0 | 48b98d80…678f |
| www.robotstxt.org | same | 200/24/0 | e5c4b844…553f |
| html.spec.whatwg.org | same | 200/69/0 | 6d81a8c0…9b72 |
| pages.github.com | same | 200/46/0 | e87ca891…4ac5 |

`cmp -s refetch/f.txt realrun/robots/f.txt` → IDENTICAL 10/10; `sha256sum` = `receipts.json`
10/10; Googlebot-UA pass identical too (no UA cloaking; the Googlebot-based checks rest on
these same bytes). **No change ⇒ no manifest check's answer changes.**

## Live bytes through the lane's own tools

Sandbox manifest = committed `manifest.json` with those ten bodies swapped for the fresh
fetches (two owned bodies copied from the repo, not fetched):

- `validate_manifest.py manifest.json --evidence` → rc=0, `faults: []`,
  `{checks:55, allow:38, disallow:17, quotes:71}` — every quote still present at its line.
- `scripts/robots_audit.py --manifest manifest.json` → rc=0,
  `{"verdict":"clean","checksEvaluated":55,"findings":[]}` = committed `audit.json`.

## Freshness is unenforced at the evidence chain (found, not claimed)

`build_manifest.py:335` copies `rec["sha256"]` into `evidence.bodySha256`, never hashing a
body; `validate_manifest.py` (163 lines, read in full) never reads `receipts.json`, never
hashes, never fetches. Mutations on the sitemaps body, sandbox:
- rule-neutral append (`Sitemap:` line; sha e8680008… ≠ receipt 19edcf7d…): validator rc=0
  no faults / 71 quotes; audit rc=0 clean 55 → drift undetected by both.
- decisive append (`User-agent: *` + `Disallow: /protocol.html`; sha 57af006a…): validator
  rc=0 still; audit rc=1 `failed-policy`, `sitemaps-protocol: blocked`,
  `sitemaps-protocol-fragment: blocked`.
So the audit catches answer flips, the validator catches neither hashes nor flips, and no
TTL/staleness gate exists (`scripts/*.py`: only `source_snapshot.py` stamps `fetchedUtc`).
A re-fetch is the only freshness test; this seat ran it. Coverage note: the 45-byte
`www.sitemaps.org/robots.txt` is one `Sitemap:` line with no rules, so its 4 checks are
empty-file `allow` and cannot show rule-level drift until that host publishes rules.

## Verdicts

| statement | verdict |
|---|---|
| 12 hosts recorded 03:23:15Z–03:23:31Z, all HTTP 200 (10 non-owned) | **holds** — 200, byte-identical 22 min later, also under Googlebot UA |
| 55 checks, each quoting its justifying robots line | **holds** on live bytes — 71/71 quotes at the stated lines |
| realrun shows the tool runs on real files (`clean`, 55) | **holds** — reproduced on the fresh bodies, rc=0 |
| receipts as a durable freshness guarantee | **overstated if read that way** — nothing binds body↔hash; no claim says otherwise, so a bounded weakness, not a falsified sentence |

## Unresolved

- Owned `ds4cc.com` / `veigapunk.github.io` not re-fetched (bounds); bodies copied only.
- Point-in-time: says nothing about bytes served after 03:46:27Z; no scheduled check exists.
- `fetch_robots.py` is tracked at 79d3c780, so the capture is re-runnable, but it writes
  into `realrun/` — outside this seat's write bounds, so it was not re-run.
