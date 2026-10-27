# SentinelC2Capture

Seat: sentinel, round-61 wave 2 (falsify). Target: `scripts/response_snapshot.py` **after** the w1 F2 fix,
as committed at the measured revision.

- Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`, HEAD `f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f`.
- Attacked blob: `scripts/response_snapshot.py` = `e1f9b0ea039cea99351498062ddda894f4071fff` (233 lines);
  worktree file hash-object equals the committed blob, so the attacked bytes are the lane's current tool.
- No lane file, index, jj or git state was touched. Read-only `git cat-file` / `git ls-files` only. Scratch was
  `/fast/scratch/hyaku/kake-r61/SentinelC2Capture/` (deleted on exit; every number below is a recorded run output).
- No tool installed, nothing upgraded (pacman paused host-wide and unused).

Axes: (1) network boundary — which hosts the tool will contact; (2) artifact truth — what the receipt attests and
whether it can be forged or made to carry foreign secrets; (3) cap honesty — the docstring's 20 s / 2 MiB / 5
redirect / one-GET / exit-set claims versus observed behavior; (4) containment — where bytes land and whether a
committed receipt can be rewritten. Moves kept: those with scratch-only reproduction and no lane mutation.

Method: copy the committed blob to scratch as `rs.py`, import it, and drive both the module functions and the CLI
against loopback fixture servers (`ThreadingHTTPServer`, ephemeral ports). Nothing was directed at a third party.

## F1 — MUST-FIX (critical): no network-class restriction; loopback / link-local / private / reserved hosts and
## names are fetched, and every redirect hop is a fresh SSRF decision

`safe_url()` (lines 52-55) checks only scheme ∈ {http, https}, non-empty hostname, and no userinfo. It never
resolves the name and never inspects the peer address. `Redirects.redirect_request` (line 72) applies the same
predicate to each hop, so a publisher that 302s anywhere wins.

Evidence (scratch):

```
p1_safe_url   -> true for http://127.0.0.1/  http://localhost/  http://[::1]/  http://0.0.0.0/
                 http://169.254.169.254/latest/meta-data/  http://10.0.0.5/  http://192.168.1.1/
                 http://172.16.0.1/  http://2130706433/  http://0x7f.1/  http://[::ffff:127.0.0.1]/
                 http://metadata.google.internal/  http://internal.corp.local/   (false only for userinfo)
p3_redirect_acceptance -> "http://169.254.169.254/latest/meta-data/": ACCEPTED
                          "http://127.0.0.1:9/x": ACCEPTED   "http://[::1]:9/x": ACCEPTED
                          "http://10.0.0.5/x": ACCEPTED      "file:///etc/passwd": refused
p2_loopback_redirect   -> CLI rc 0; publisher 302 -> http://127.0.0.1:<internal>/internal?access_token=TOKEN-IN-URL
                          internal_hits 1, path "/internal?access_token=TOKEN-IN-URL"
                          status 200, body == internal secret page (byte-identical), 7 recorded headers
```

Exploit path (unprivileged third party → lane history): one of the 12 round-23 surfaces is compromised, hijacked,
or simply returns `302 Location: http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>` (or
`http://127.0.0.1:<admin-port>/`). The capture run performs the GET, records status, every header and the first
2 MiB of the body, and commits them under `.ufo/waves/round-61/capture/<id>/`. That is a durable SSRF plus
exfiltration channel: cloud metadata credentials, an internal admin page, or a router/CI port scan result become a
committed blob, and the receipt asserts `url` beside `finalUrl` as if the named public surface answered. A single
mis-served `Location` converts the "offline capture of 12 public surfaces" into an internal-network reader.

DNS rebinding needs no separate exploit: there is no resolution-time or connect-time verification at all, so a
name that resolves (or rebinds) to a private address is followed on the first connection.

```
p4b_rebind_name_followed -> fetch("http://rebind.test:<port>/rebound") via a scratch resolver mapping
                            rebind.test -> 127.0.0.1: rc 0, status 200, body == internal secret page
p4c_ip_literal_forms     -> "2130706433", "0x7f.1", "0.0.0.0": rc 0, status 200, body == internal secret page
p1_resolver              -> getaddrinfo("2130706433") = 127.0.0.1 ; getaddrinfo("0x7f.1") = 127.0.0.1
```

The literal-form results matter for the fix: glibc resolves decimal and hex-encoded IPv4 to loopback, so a
hostname-string blocklist cannot work. Minimal remediation: before connecting, resolve and require every
`getaddrinfo` result to satisfy `ipaddress.ip_address(a).is_global`; after the connection is up, re-verify
`response.fp.raw._sock.getpeername()` (pin the peer, which also closes rebinding); and on redirect require the new
hop's host to be the recorded host (or same registrable domain) in addition to the address check. Reject, do not
merely record, and keep the blocker independent of `--population`.

## F2 — MUST-FIX (high): the documented 20 s cap is per socket operation, so wall time per surface is unbounded

Docstring: "at most 5 redirects, 20 s and 2 MiB per surface". `TIMEOUT = 20` is passed to `opener.open(timeout=)`,
which sets the socket timeout for each `send`/`recv`; `response.read(MAX_BODY + 1)` then reads under that same
per-operation timeout, and each redirect hop restarts the clock with a fresh 20 s.

```
p10_drip          -> server sends Content-Length: 26 then one byte every 1.2 s:
                     elapsed 30.01 s (TIMEOUT 20), status 200, bytes 26, error null  (cap exceeded, run succeeded)
p11_hop_deadline  -> 4 hops, each 12 s before responding: elapsed 48.01 s (TIMEOUT 20), hops 4
```

A surface trickling 2 MiB at one byte per 19 s holds the seat for ~470 days; a hostile publisher gets free
occupancy of the capture run and the operator sees a process that never prints a summary. Impact is availability of
the round-61 capture plus a false receipt: when such a run is finally killed, any surfaces already written carry
`fetchedAt` on the access date and look like a complete capture.

Minimal remediation: one `deadline = time.monotonic() + TIMEOUT` per surface, `min(remaining, TIMEOUT)` passed as
the socket timeout at every hop and re-checked around the read loop; on expiry record `error: "deadline"` with the
bytes received. (A total deadline also fixes the 5-hop × 20 s = 100 s worst case.)

## F3 — MUST-FIX (high): an over-100-header or over-64 KiB-header response aborts the entire run with a traceback
## and an exit code outside the documented set

`fetch()` guards only the body read with `except (http.client.HTTPException, OSError)` (line 98). The header
parse happens inside `opener.open(...)`, whose failure modes are covered by `urllib.error.HTTPError` and
`(urllib.error.URLError, OSError, ValueError)` — but `http.client.HTTPException` (raised for "got more than 100
headers" and for `LineTooLong`) is not an `OSError`, so it escapes `fetch()` and `main()`.

```
g1_many_headers_crash -> 101 response headers: rc 1, stdout "", stderr ends
                         http.client.HTTPException: got more than 100 headers
                         receipt dirs ["a-good", "b-many"]; response.json written for a-good only
                         c-long and d-good2 (the 3rd and 4th surfaces) were never fetched
g2_long_header_line   -> 70 000-byte header line: rc 1, http.client.LineTooLong, no receipt at all
```

Impact: any publisher (or any CDN that echoes many `Set-Cookie` fields) can abort the whole 12-surface capture at
will; the run leaves partial receipts and empty per-surface directories with no summary, no per-surface `error`
record, and rc 1 — which the tool's own contract does not define ("0 every attempt recorded; 2 bad population;
64 usage"). The claim "one GET per surface" is falsified for every surface after the aborting one.

Minimal remediation: wrap `opener.open()` and the `response.status`/`geturl()`/`headers.items()` access in
`except (http.client.HTTPException, OSError, ValueError)` → `error = f"{type(exc).__name__}: {exc}"`, `status=None`,
continue to the next surface. (Optionally raise `http.client._MAXHEADERS` deliberately and record
`headerCount` vs a declared cap rather than depending on the stdlib limit.)

## F4 — MUST-FIX (medium): `--overwrite` rewrites an already-committed capture receipt in place

`write_file` opens with `O_CREAT` (no `O_EXCL`) and `ftruncate`s (lines 141-149); `main` only refuses when a
target `response.json` exists *and* `--overwrite` was not passed, and the refusal check runs before the GETs.

```
f1_overwrite -> first run sha 2949e165b9bb; second run with --overwrite: rc 0, changed true, same inode true,
                sha f586c8dd5e5e, body.bin replaced with the new body
p9_write_file_no_excl -> write_file() over an existing file yields "NEW": creates_exclusively false
```

Contract A4 and the round receipt rule state the immutability rule covers `capture/` and that a re-run lands under
a new name. The tool ships a flag that does exactly the forbidden thing, with no warning and no record that the
prior bytes existed — the same "rewrite a committed receipt after the fact" class C1 exists to detect, handed to
the operator as a convenience. Minimal remediation: delete `--overwrite` (a fresh `--out` is the contract's re-run
path); if it must stay, refuse when the target path is tracked in git (`git ls-files --error-unmatch`) and add
`O_EXCL` to `write_file` so the guarantee is not a pre-check race spanning the whole fetch (`p9` shows the window
is open for the entire run).

## F5 — STATED LIMIT, tighten at the boundary (medium): secrets ride into the committed artifact

The receipt is contract-mandated to carry "ordered header name/value pairs (duplicates preserved)", `finalUrl`,
and `body.bin` byte-identically, so this is a declared design, not a coding error — but the evidence shows what it
means once a response is internal or session-bearing:

```
p2_loopback_redirect -> Set-Cookie values recorded verbatim:
                        "session=SEKRET-9f3a11; HttpOnly; Secure" and "tenant=SEKRET-tenant-2; Path=/"
                        X-Auth-Token: SECRET-TOKEN-abc recorded verbatim
                        finalUrl "http://.../internal?access_token=TOKEN-IN-URL"
                        redirects[0].to carries the same token; body.bin == the internal page, committed
```

Today's committed round-61 capture is clean of this class (checked read-only: 12 `response.json`, all
`redirects=0`, zero `set-cookie` headers), so the exposure is latent, not realized. Tightening that keeps every
frozen check: record `Set-Cookie` as name + `[redacted]` (H10 counts duplicates only), and mask query strings in
`url`/`finalUrl`/`redirects[].to` (the manifest's `url` is the declared one, so no check loses input). Combined
with F1 this is the difference between "a publisher's header set was recorded" and "a capability token is now in
lane history forever".

## F6 — MUST-FIX (medium): the capture trusts ambient proxy settings, so the receipt's provenance is forgeable

`urllib.request.build_opener(redirects)` installs the default `ProxyHandler`, which honours `http_proxy` /
`https_proxy` / `all_proxy`.

```
p8_proxy_provenance -> population url http://origin.invalid/orig (unresolvable name) with http_proxy=<scratch proxy>:
                       rc 0, status 200, body "PROXY-INJECTED-BODY", recorded url "http://origin.invalid/orig",
                       proxy saw GET http://origin.invalid/orig
```

The receipt asserts a 200 from `origin.invalid`, a host that does not resolve and was never contacted; the body
came from whatever the environment pointed at. Any operator shell, container image, or hostile `.env` therefore
decides what the audit sees, and nothing in `response.json` records that a proxy was used. Minimal remediation:
`build_opener(urllib.request.ProxyHandler({}), redirects)` and record `"proxy": null` in the receipt (or record
`proxy` as a field so a proxied capture is visibly not origin-attested).

## F7 — Verified-clean (no action; keeps the frontier honest)

- Userinfo in the recorded URL: refused before any GET — `p7_userinfo_initial` rc 2, publisher hits 0, message
  `s1: url must be http(s) with a host and no userinfo`.
- Userinfo in a redirect `Location`: refused, zero internal hits, `error: "blocked redirect"`, hops 0 —
  `p7_userinfo_redirect` status 302, internal_hits 0.
- Non-http(s) redirect (`file:///etc/passwd`): refused (`p3_redirect_acceptance`).
- Size cap exact: a 3 MiB response produced `bytes 2097152`, `truncated true`, `body.bin` 2 097 152 bytes, sha256
  of the retained 2 MiB (`p5_size_cap`).
- Redirect cap: a self-chaining 302 was followed exactly 5 hops, the 6th blocked, `error "blocked redirect"`,
  `status 302` (`p6_redirect_cap`).
- F2 fix holds: a blocked hop never appears as `finalUrl` — `out7b` finalUrl is the publisher URL, `out6`
  finalUrl is the URL that returned the 5th 302. The pre-F2 defect (urllib reporting the unfetched destination) is
  gone.
- Containment on the receipt leaf: a pre-planted `response.json` symlink was refused pre-GET with exit 2 and the
  victim file untouched, because `lexists` catches it before the fetch (`p9_symlink_receipt`: publisher hits 0,
  victim intact). `O_NOFOLLOW` + `st_nlink == 1` also hold for the leaf once open.

## F8 — Low (recorded, not blocking)

- `--out` is passed through `os.path.realpath`, so a symlinked `--out` writes into the link target and the tool
  reports nothing about the substitution (`f2_out_symlink`: `written_under_realpath true`, `is_link true`). Only
  reachable with an operator-supplied path.
- `load_population` follows a symlinked `<dir>/fetch.json` and takes the surface `id` from the file, not the
  directory name, so a population directory can aim output at any `SAFE_ID` inside `--out`
  (`f3_fetch_json_symlink`: dir `s1` holding a symlink to a file declaring `id: s9` produced `out/s9/`). Lane-owned
  input, low.
- Response headers have no declared cap of their own: `http.client` stops at 100 fields / 65 536 bytes per line
  (`p1_httpclient_caps`), and the failure mode is F3's crash, not a recorded `could_not_evaluate`. If the fix in
  F3 only catches the exception, a surface with 100 fields × 60 KiB would still write a ~6 MB `response.json`
  because the body cap is the only byte cap in the contract.

## Scope note

Attacked surface was `scripts/response_snapshot.py` only; `header_audit.py`, the manifest, the counters and the
C1/C3 surfaces were not examined. Nothing here changes a frozen predicate; F1–F4 are failures of the tool's own
stated constraints, F5 is a declared design with a tightening that preserves every check, F6 is an unstated trust
boundary, F7 records what already holds.

VERDICT: F1 critical must-fix (loopback/private/link-local and every redirect hop fetched, SSRF body+headers committed), F2 high must-fix (20 s is per socket op: 30.01 s and 48.01 s observed), F3 high must-fix (101 headers → uncaught http.client.HTTPException, rc 1, run aborted after partial receipts), F4 medium must-fix (--overwrite rewrites a committed receipt in place), F6 medium must-fix (ambient proxy forges origin provenance); F5 is a stated limit (verbatim Set-Cookie/query-token/body capture, latent only — today's 12 receipts carry 0 redirects and 0 Set-Cookie); userinfo, scheme, 2 MiB and 5-redirect caps and the F2 finalUrl fix all verified holding.
