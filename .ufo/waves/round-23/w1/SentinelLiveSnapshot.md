## Verdict

**HOLD on output confinement.** At candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`, the fetch path used GET, bounded reads to 2 MiB, timed out at 20 seconds, required `text/html`, and surfaced TLS verification failures. However, an input surface ID can write snapshot files outside `--out`. A second conditional issue is that URL userinfo is retained verbatim in snapshot metadata, even when the request fails before connecting. No production files were changed.

## Findings

### P2 — Surface IDs escape `--out`

**Exact command:**

```text
/usr/bin/python -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py --population /tmp/kake-r23-SentinelLiveSnapshot-RZd3/unsafe-pop.json --out /tmp/kake-r23-SentinelLiveSnapshot-RZd3/unsafe-out
```

The local population used IDs `../escaped-relative` and `/tmp/kake-r23-SentinelLiveSnapshot-RZd3/escaped-absolute`; both URLs returned local 404s. **Exact observed output:**

```text
UNSAFE_EXIT 0
OUTSIDE_OUTPUT_EXISTS /tmp/kake-r23-SentinelLiveSnapshot-RZd3/escaped-relative True ['audit.json', 'fetch.json']
OUTSIDE_OUTPUT_EXISTS /tmp/kake-r23-SentinelLiveSnapshot-RZd3/escaped-absolute True ['audit.json', 'fetch.json']
OUT_DIR_CHILDREN []
```

`main()` joins the unchecked ID directly to `args.out` at line 113, then creates and writes in that directory (lines 114–125). `os.path.join` permits both `..` traversal and an absolute second component, so this contradicts the script's “writes only under DIR” claim and the operability/output-confinement requirement. A crafted population can create or overwrite the snapshot-named files in another writable directory.

**Smallest fix:** reject IDs unless they are a safe single path component (including rejecting absolute paths, separators, `.` and `..`), and check the resolved destination remains inside the resolved `--out` before creating or opening anything; this also closes pre-existing symlink escapes.

### P2 — URL userinfo is persisted verbatim

**Exact command:**

```text
/usr/bin/python -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py --population /tmp/kake-r23-SentinelLiveSnapshot-RZd3/probe-pop.json --out /tmp/kake-r23-SentinelLiveSnapshot-RZd3/probe-out
```

One local test URL contained only dummy credentials: `http://probe-user:probe-pass@127.0.0.1:36761/cgi-bin/redirect.py?code=401`. The request failed before reaching the local server, but the snapshot retained the credentials. **Exact observed output:**

```text
FAKE_USERINFO_IN_SNAPSHOT True None URLError: <urlopen error [Errno -2] Name or service not known>
```

The resulting `fetch.json` contained both:

```json
"finalUrl": "http://probe-user:probe-pass@127.0.0.1:36761/cgi-bin/redirect.py?code=401"
"url": "http://probe-user:probe-pass@127.0.0.1:36761/cgi-bin/redirect.py?code=401"
```

`fetch()` stores the original and final URLs in metadata (lines 72–75), which `main()` writes to `fetch.json` (lines 115–117). This test did **not** send credentials: the resolver error occurred before a request reached the server. Nevertheless, if an input URL contains real userinfo, the output artifact discloses it to anyone with access to the snapshot.

**Smallest fix:** reject URL userinfo before opening the URL and do not serialize unredacted userinfo in `url`, `finalUrl`, or error fields.

## Checked and held

- **GET and redirect method logic:** `Request(..., method="GET", headers={"User-Agent": USER_AGENT, "Accept": "text/html"})` is the only constructed request. A direct local call through `Redirects.redirect_request` gave the exact output `REDIRECT_RESULTS 301:GET 302:GET 303:GET 307:GET 308:GET`; original and redirected headers were both only `[["User-agent", "kake-shokunin-readonly-preflight/1 (+GET only)"], ["Accept", "text/html"]]`. Thus 307/308 preserve GET in the runtime's urllib handler. The opener had `COOKIE_PROCESSOR False`; ordinary local CGI observations were `{"method": "GET", "cookie": "", "auth": false}`. No request body is supplied.
- **Body cap:** a local `big.html` of 2,097,153 bytes produced `{"bytes": 2097152, "contentType": "text/html", "truncated": true, "status": 200}`; no `page.html` was written. The read is `MAX_BODY + 1`, then sliced to `MAX_BODY`.
- **Timeout:** a local CGI endpoint delayed its response. The command exited `0` after `20.06` seconds; metadata was `{"bytes": 0, "contentType": null, "error": "TimeoutError: timed out", "method": "GET", "status": null, "truncated": false}`. This exercises `TIMEOUT = 20` and the error path.
- **Content type:** local CGI returned `TEXT/HTML; charset=utf-8`; metadata recorded that value and the page was audited (`verdict: "clean"`). Static `text.txt` returned `contentType: "text/plain"` and was not saved as a page. The check is case-insensitive, strips parameters, and accepts only `text/html` for page storage.
- **TLS failure:** a local Python HTTPS server used a generated self-signed certificate. The snapshot exited `0` with `status: null`, `bytes: 0`, and `error: "URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self-signed certificate (_ssl.c:1082)>"`; no page was written. TLS validation was not disabled or suppressed.
- **Cleanup:** both local HTTP server processes were terminated and reaped (`LOCAL_SERVERS_CLEANED True`). All probe files and the test certificate remained under `/tmp/kake-r23-SentinelLiveSnapshot-RZd3`.

## Limits

All network requests were to `127.0.0.1`; the only credentials used were the dummy strings `probe-user:probe-pass`. The stock `python -m http.server --cgi` endpoint forced CGI responses to HTTP 200, so it could not provide a genuine wire-level redirect response; the 301/302/303/307/308 check therefore exercised the candidate's redirect handler directly rather than a live redirect chain. No public URL, publishing action, build, lint, formatter, or test suite was run.