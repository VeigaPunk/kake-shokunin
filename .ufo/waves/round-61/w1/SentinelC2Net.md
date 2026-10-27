# SentinelC2Net

Scope: the network surface of `scripts/response_snapshot.py` (claim C2 capture input) and the integrity of the 12
round-61 capture receipts under `.ufo/waves/round-61/capture/`. Access date 2026-10-27 (UTC). Method: source read +
AST/text audit, loopback-fixture dynamic probes, syscall trace (`strace -f -e openat,connect,socket,mkdir,unlink`),
and receipt re-verification. No lane mutation; scratch `/fast/scratch/hyaku/kake-r61/SentinelC2Net` deleted after
copying evidence. Tooling: no installs needed (`strace`, `python3.14` present).

Two tool versions exist. The 12 receipts (`response.json` mtimes 06:15:55–06:16:03 -0300 = 09:15:55–09:16:03Z) were
written by bytes sha256 `eac57099a6e097a28638bc2b7e29ddd3dfd301b34c0caa255d8d708bcb039643`; the committed file is
`ba107024c770db194f0b07c806641f1674e109134f62c0eac671e5b06bde1bb7` (mtime 06:17:14; the 06:15:45 file is the
`manifest.json` another seat added). I audited both: the AST delta is one added argparse flag (`--overwrite`) plus
docstring/usage text, and the security-critical region (`Redirects`, `utc_now`, `fetch` through the body cap,
`write_file`, `write_json`, `load_population`) occurs **verbatim** in the committed file — proved by string equality
against the pre-edit text I captured, not by eye. Dynamic probes produce identical results on both versions.

Capture line (for the C2 receipt rule, L1 ruling d): capture-time tool sha256
`eac57099a6e097a28638bc2b7e29ddd3dfd301b34c0caa255d8d708bcb039643`; committed tool sha256
`ba107024c770db194f0b07c806641f1674e109134f62c0eac671e5b06bde1bb7`; the receipts themselves are pinned by the 12
`sha256` fields re-verified below. No git blob is citable for the capture-time bytes (ruling d, corrected: the tool is
worktree-only).

## FINDINGS:

| # | severity | issue | fix |
|---|---|---|---|
| F1 | MEDIUM | Receipt-producing tool bytes are not retained (provenance gap) | copy the run-time tool into `w1/<Seat>.files/` and hash it there |
| F2 | MEDIUM | Redirects follow to any http(s) host incl. loopback/private; internal body+header get committed | pin the hop host to the initial host, or reject non-global destination IPs |
| F3 | LOW | No network off-switch: every invocation fetches | add `--reaudit`/`--offline` that re-verifies receipts without a socket |
| F4 | LOW | Ambient proxy env honoured (`build_opener` keeps default `ProxyHandler`) | `build_opener(urllib.request.ProxyHandler({}), redirects)` |
| F5 | LOW | `fetchedAt` is stamped before the request, not on completion | stamp after the response, or record both |
| F6 | LOW | A body-read failure keeps `status: 200` with no completeness flag | set `status: null` on a failed read, or add `"complete": false` |
| F7 | LOW | Bare `User-Agent: round61`; sibling report's "UA only" overstates the wire | UA with product/version/contact; accept `Accept-Encoding: identity`, `Host`, `Connection: close` |
| F8 | INFO | `--out` unconfined; `--overwrite` rewrites receipts in place; no fsync/O_EXCL | treat `capture/` as commit-once; record the 12 receipt digests before any re-run |

**F1 — provenance.** The report discloses the post-run edit but only in prose: the bytes that wrote the receipts
(`eac57099…`) survive nowhere — not in git (the tool is only in the worktree), not in `.files/`. Exploit path: rewrite
`fetch`/digest logic after a run and assert "only the guard changed"; the receipts' digests still check out because
they are self-consistent. Impact: the C1 class (undisclosed post-hoc receipt rewrite) recurs at the tool level, and w2
cannot re-derive the claim. In this instance the residual risk is contained — I proved the delta is confined to the
`--overwrite` pre-flight and docstring/usage, and both versions behave identically — but the mechanism is unenforced.
No git blob can be cited for the capture-time tool: it is worktree-only — `git ls-tree HEAD scripts/` has no
`response_snapshot.py` and `git log -- scripts/response_snapshot.py` is empty (checked 2026-10-27 at
`eaa9177e2965a50fa038d57254934a53909052b6`). The only surviving identifier of the producing bytes is the sha256
`eac57099…039643` quoted in `ExecC2Capture.files/run.txt`, and the only surviving proof of the delta is my
containment check above. Smallest fix: `sha256sum` + a byte copy of the tool written to `ExecC2Capture.files/`
immediately before the run; a committed blob would then be citable in later rounds.

**F2 — redirect confinement (proven).** `safe_url` blocks `file:`/userinfo but not private address space, and a hop
may change host. Fixture: a surface at `127.0.0.1:40655` answered `302 → http://localhost:33013/secret`; the tool
followed it and recorded the internal service's body (`INTERNAL-ADMIN-PANEL`) and header
(`X-Internal-Token: shh-abc`) into `response.json`/`body.bin`. Impact: a compromised or mis-pointed owned surface can
make the lane commit internal plaintext; bodies are untrusted content committed verbatim (bounded by 2 MiB and a
`SAFE_ID` directory). No credentials are sent, so this is ingress-only. Fix: require hop host == initial host (or a
declared allowlist), and/or resolve each hop and refuse `ipaddress.ip_address(…).is_global == False`.
**Disposition (L1 decision): carried as a stated limit, not fixed pre-freeze** — the real capture recorded
`redirects=[]` on 12/12, so no receipt is affected, and an edit now would re-open F1.

**No receipt needs purging.** The `X-Internal-Token` sample exists only in my fixture run (`dyn-probe2-ssrf-timeout.json`,
emitted by a loopback server I started on 127.0.0.1:33013); it was written under my scratch `dyn2/outA/ssrf/` — never
under `capture/` — and the scratch was deleted. Across all 12 real receipts: no `X-Internal-Token`, no
token/auth/cookie header, no loopback body. One *published page's own prose* contains the literal `127.0.0.1:9222`
(`burnerchrome-kimi/body.bin`: "Shared transport: Chrome 149+ on 127.0.0.1:9222 via musketeer-chrome…") — that is the
surface owner's own public copy, not captured internal service data. The only internal-looking headers are
publisher-sent infrastructure markers with no credential content: `x-internal-adhoc-canary: 586427312` (7 receipts),
`x-proxy-by: appproxy` (1), `x-proxy-cache: MISS` (3).

**L1 rulings (2026-10-27).** (a) the `127.0.0.1:9222` string is the page's own published prose — keep, cite as-is;
(b) `x-internal-adhoc-canary` / `x-proxy-*` are publisher infrastructure markers, numeric and non-credential — keep
(they feed the singleton/field-name cases); (c) F2 goes to w2 as a stated limit, no pre-freeze edit; (d) the
capture-time tool sha256 is recorded above and the `sha256sum` + byte-copy discipline is routed to the round-61
lesson's `## Mistakes` as a new row (`process/tool-bytes-not-retained`, captured-by `none` + manual sentinel) — the
paste-ready row is `SentinelC2Net.files/lesson-mistake-row4.md`; the lesson file itself is the scribe's and I did not
touch it.

**F3–F8.** No off-switch: `env_reads` is empty and argparse offers only `--population/--out/--overwrite`, so the tool
can never be re-verified — or run at all — without egress; the reference `scripts/live_snapshot.py` has `--reaudit`
(no network) and this tool does not. Proxy: `build_opener(redirects)` keeps urllib's default `ProxyHandler`, so
`http_proxy`/`https_proxy` silently redirect egress while receipts record only the target URL; not triggered here
(no proxy in env). `fetchedAt` (line 90, pre-request) lagged completion by 20.1 s in the stall fixture. In that same
fixture the receipt kept `status: 200`, `bytes: 0`, `truncated: false`, `error: "TimeoutError: timed out"` — the
audit's `content_type_present`/`hsts_present` classes are 2xx-gated, so a transport failure can be scored as a served
page. Wire request (measured): `Accept-Encoding: identity`, `Host`, `User-Agent: round61`, `Connection: close` — so
"request headers: User-Agent only" in `ExecC2Capture.md` is inaccurate (no `Accept`, but Accept-Encoding is sent).
`--out` is caller-controlled with no lane-confinement assertion; default is confined.

**Attested clean (no finding).** GET-only: one `Request(method="GET")`, no `data=`, redirect re-issue refused unless
GET; fixtures saw only GET (a reachable `do_POST` was never hit), 0 request-body bytes, one socket per hop. No
cookies: no `http.cookiejar`, no `Cookie` header emitted, no cookie/auth field recorded. Caps: 5 hops followed then
`302` + `error: "blocked redirect"` (6th refused); `file:` and userinfo destinations blocked (exit 2 for input);
2 MiB cap → `bytes=2097152`, `truncated=true`, digest over the capped prefix; 20 s timeout measured at 20.1 s.
Confinement: strace of a full run shows exactly two write-mode opens — `response.json` and `body.bin`, both
`O_NOFOLLOW`, mode 0600, relative to one opened surface-dir fd — plus `mkdir` only for `--out` and the surface dir;
no temp file, no `/tmp` write, no `rename`. Capture tree: 0 symlinks, 0 non-regular files, all leaves regular
single-link 0600. Integrity: 12/12 `sha256(body.bin)==sha256` and `len(body.bin)==bytes`; `headerCount==len(headers)`
on 12/12; `url` equals the round-23 population url on 12/12; `finalUrl` consistent with the (empty) redirect chains;
duplicates preserved on live data (`vary` ×2 on the seven `kimi.page` receipts) and in wire order (fixture:
Content-Type, Content-Type, Set-Cookie, Set-Cookie, X-Content-Type-Options); no cookie/secret/userinfo/local-path
material in any receipt; no high-entropy credential values (the three 40-char values are Fastly request IDs).
Tree bytes reconcile with `ExecC2Capture.md`: 19 056 (12 `response.json`) + 325 253 (12 `body.bin`) = 344 309,
plus the 5 125-byte `manifest.json` added later = 349 434.

## RECEIPTS:

12/12 parse as a JSON object and carry every contracted key (`url`, `finalUrl`, `method`, `status`, `headers`,
`headerCount`, `contentType`, `bytes`, `sha256`, `truncated`, `fetchedAt`, `userAgent`, `redirects`, `error`,
`bodyFile`); `body.bin` re-verified against `bytes`/`sha256`.

| id | parse | keys | hdr shape | status | hdrs | bytes | sha256(body.bin) | ua | fetchedAt |
|---|---|---|---|---|---|---|---|---|---|
| burnerchrome-kimi | ok | all 15 | {"name","value"} list | 200 | 16 | 11976 | 44dc3491fbc6cdc5 | round61 | 2026-10-27T09:15:53Z |
| charter-ghp | ok | all 15 | {"name","value"} list | 200 | 23 | 53660 | 7c243a1d81357cde | round61 | 2026-10-27T09:15:55Z |
| charter-kimi | ok | all 15 | {"name","value"} list | 404 | 14 | 13409 | 93ddca9a021664d5 | round61 | 2026-10-27T09:15:55Z |
| ds4cc-kimi | ok | all 15 | {"name","value"} list | 200 | 16 | 74641 | bc8bb28d7ef97b81 | round61 | 2026-10-27T09:15:57Z |
| ds4cc-primary | ok | all 15 | {"name","value"} list | 200 | 22 | 78897 | f2c5d2b3ab34e8e1 | round61 | 2026-10-27T09:15:57Z |
| lucario-ghp | ok | all 15 | {"name","value"} list | 200 | 23 | 3435 | bee2d9f5b5777768 | round61 | 2026-10-27T09:15:57Z |
| lucario-kimi | ok | all 15 | {"name","value"} list | 404 | 14 | 13409 | 93ddca9a021664d5 | round61 | 2026-10-27T09:15:58Z |
| plazir15-ghp | ok | all 15 | {"name","value"} list | 200 | 23 | 38337 | d82af77aee401d22 | round61 | 2026-10-27T09:15:58Z |
| plazir15-kimi | ok | all 15 | {"name","value"} list | 404 | 14 | 13409 | 93ddca9a021664d5 | round61 | 2026-10-27T09:15:58Z |
| plazir27-kimi | ok | all 15 | {"name","value"} list | 404 | 14 | 13409 | 93ddca9a021664d5 | round61 | 2026-10-27T09:16:00Z |
| ufo-fsd-kimi-pro | ok | all 15 | {"name","value"} list | 200 | 12 | 612 | 1df92e30ba5a76e6 | round61 | 2026-10-27T09:16:00Z |
| vault-index-kimi | ok | all 15 | {"name","value"} list | 200 | 16 | 10059 | a0a7f33aba443a85 | round61 | 2026-10-27T09:16:02Z |

All 12: `method=GET`, `error=null`, `truncated=false`, `redirects=[]`; ids exactly the 12 round-23 population ids,
no extras or gaps. The four 404 receipts share one body digest (the host error page) and still carry `content-type`.

## Evidence (in `SentinelC2Net.files/`)

`static-audit-pre-edit-eac57099.json`, `static-audit-current-ba10702.json` (AST/property diff: only `--overwrite`),
`pre_excerpt.txt` (the pre-edit region proved present verbatim in the committed tool), `dyn-probe.json` /
`dyn-probe-current.json` (identical results pre/post edit), `dyn-probe2-ssrf-timeout.json` (cross-host redirect,
input hardening, 20.1 s stall), `strace-current.txt` (write/connect/mkdir set), `audit_net.py`, `dyn_probe.py`,
`dyn_probe2.py`.

Unrun: no second independent fetcher cross-checked the 12 bodies (w2 reviewer/sentinel scope); live serving was not
sampled beyond the one capture. Tool version/hash recorded, no installs.

VERDICT: capture tool and all 12 receipts pass the substantive network checks (GET-only, no cookies/body, 5-hop cap, 2 MiB/20 s caps, capture-only writes, sha-verified receipts) — two MEDIUM gaps stand: the receipt-producing tool bytes are unretained (F1), and cross-host redirects reach loopback/private targets whose content is then committed (F2).
