# ExecSnapshotFetcher — round-36 wave-1 report

## What I built
`/fast/scratch/hyaku/kake-r36w1/ExecSnapshotFetcher/source_snapshot.py` (sha256 `8530a8c5…130`, 291 lines)
— a recorder that turns a JSON list of `{id, url, quote}` into a C1 version-1 manifest from live
GET fetches. Behavior per spec:
- GET only via `urllib` with a `NoRedirect` handler (`redirect_request -> None`, so urllib raises
  `HTTPError` on every 3xx, which is recorded as a hop with its raw `Location` header).
- At most 8 redirect hops followed; each `Location` is resolved against the hop URL with
  `urllib.parse.urljoin` (RFC 3986 §5.2 resolution) to decide where to fetch next. The manifest
  records the raw `location` value; the contract resolves it itself.
- Stops at the first non-redirect status; that response is the final hop (`"location": ""`, since
  a non-redirect hop carries no Location).
- Final body capped at 8 MiB (`read(MAX_BODY + 1)`); on 200 the check gets `contentType` from the
  final response headers and `body` = a relative file inside the manifest's directory.
- One `User-Agent` naming kake-shokunin round 36 (`kake-shokunin-round-36-source-snapshot (one GET
  per source)`), ≥1 s between requests (global `_LAST_REQUEST`), 30 s timeouts.
- Unrecordable items are skipped from the manifest but kept in a sidecar `receipts.json` (reasons:
  `invalid_id|invalid_url|invalid_quote|redirect_without_location|too_many_redirects|body_too_large|
  fetch_error: ...`). URL must be absolute http(s) with a host and no userinfo.

Support files (same dir): `test_server.py` (local fixture server, 127.0.0.1 only — 301, 302 chain,
301→302→302 chain, relative Location, 303/307/308, 8-hop chain, >8-hop chain, redirect loop,
redirect without Location, 404, 200 html + text/plain), `check_manifest.py` (independent
contract-shape checker), `input*.json` fixtures, `manifest.compact.txt`.

## Commands run and results
- `python3 -B test_server.py 8734` (fixture server, async job; killed afterwards)
- `python3 -B source_snapshot.py --input input.local.json --out-dir out-final` → exit 0,
  `manifest out-final/manifest.json checks 7 of 7`
- `python3 -B check_manifest.py out-final/manifest.json` → `0 problem(s)`, exit 0
- `python3 -B source_snapshot.py --input input.edge.json --out-dir out-edge` → exit 0,
  0 of 5 recorded: `ELOOP too_many_redirects`, `ENOLOC redirect_without_location`,
  `EBADURL/EEMPTY invalid_url`, `EQUOTE invalid_quote`
- `python3 -B source_snapshot.py --input input.chain.json --out-dir out-chain` → exit 0, 4 of 5:
  `C303 [303,200]`, `C307 [307,200]`, `C308 [308,200]`, `CDEEP8 [302×8,200]`,
  `CLONG (13 hops) too_many_redirects`
- Cross-check vs the sibling tool (`ExecToolBuild`'s `source_recheck.py`, still in-flight in its
  clone): `python3 -B .../source_recheck.py --manifest out-final/manifest.json` → exit 1,
  `{"verdict":"failed-policy","checksEvaluated":7,"findings":[moved→/ok (T301), moved→/ok
  (T301REL — relative "ok" resolved against the hop URL), moved→/chain2b (T301CHAIN leading
  permanent hop), gone (T404)]}` — the manifest parses cleanly and resolution/moved logic agrees
  with the contract (301 chain gets `moved` at the leading permanent run's last hop; 302-first
  chain gets none; `quote_missing` on none since quotes matched).

## Manifest it writes (pasted, hop objects compacted)
```json
{
 "version": 1,
 "checks": [
  {"id": "T200", "url": "http://127.0.0.1:8734/ok", "quote": "The registry row quotes this sentence about re-checking sources", "hops": [{"status":200,"location":""}], "contentType": "text/html; charset=utf-8", "body": "T200.body"},
  {"id": "T301", "url": "http://127.0.0.1:8734/moved", "quote": "...", "hops": [{"status":301,"location":"/ok"}, {"status":200,"location":""}], "contentType": "text/html; charset=utf-8", "body": "T301.body"},
  {"id": "T301REL", "url": "http://127.0.0.1:8734/moved-rel", "quote": "...", "hops": [{"status":301,"location":"ok"}, {"status":200,"location":""}], "contentType": "text/html; charset=utf-8", "body": "T301REL.body"},
  {"id": "T302CHAIN", "url": "http://127.0.0.1:8734/chain", "quote": "...", "hops": [{"status":302,"location":"/chain2"}, {"status":302,"location":"/chain3"}, {"status":302,"location":"/ok"}, {"status":200,"location":""}], "contentType": "text/html; charset=utf-8", "body": "T302CHAIN.body"},
  {"id": "T301CHAIN", "url": "http://127.0.0.1:8734/chain-perm", "quote": "...", "hops": [{"status":301,"location":"/chain2b"}, {"status":302,"location":"/chain3b"}, {"status":302,"location":"/ok"}, {"status":200,"location":""}], "contentType": "text/html; charset=utf-8", "body": "T301CHAIN.body"},
  {"id": "T404", "url": "http://127.0.0.1:8734/missing", "quote": "gone", "hops": [{"status":404,"location":""}]},
  {"id": "TPLAIN", "url": "http://127.0.0.1:8734/plain", "quote": "...", "contentType": "text/plain; charset=utf-8", "hops": [{"status":200,"location":""}], "body": "TPLAIN.body"}
 ]
}
```
Full files: `out-final/manifest.json` (sha256 `ea7e7f4a…`), `out-final/receipts.json` (per-id
fetchedUtc, finalUrl, hops, resolvedLocations, bodySha256), `manifest.compact.txt`.

## Design notes / risks
- `body` path is a bare filename (`<safe-id>.body`) inside the manifest's directory — satisfies
  "relative path to a regular file inside the manifest's directory" and survives id sanitization
  (`safe_name`, collision-safe via sha256 suffix when cleaned).
- Checks whose chain can't honestly end non-redirect (redirect w/o Location, >8 hops, fetch error,
  body >8 MiB) are NOT emitted, because a manifest rule would then break (`check_invalid`, which
  poisons the verdict to could-not-evaluate). They stay visible in `receipts.json`. If the L1
  prefers them emitted anyway (deliberate `check_invalid`), it's a one-line change.
- `"location": ""` on the final hop: contract says a redirect hop needs `location`; a non-redirect
  hop doesn't have one, so empty string. The tool read it fine.
- Not verified: `checksEvaluated`/findings projection under the sealed counter (no key — sealed
  tree untouched); real-world hosts (never fetched — 127.0.0.1 only); interplay with the landed
  tool beyond the cross-check above.
- Tooling: none installed (stdlib only; Python 3.14.8). pacman untouched.
- No mutation of the lane repo or sibling lanes; git used read-only.
