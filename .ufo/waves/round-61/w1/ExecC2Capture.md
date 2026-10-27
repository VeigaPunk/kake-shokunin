# ExecC2Capture

Claim C2 (operability) — capture input preparation only. Built `scripts/response_snapshot.py`, ran it once
against the 12 round-23 surfaces, kept the receipts. Nothing here asserts a census result, scores the claim, or
touches a counter/manifest/audit file (`.ufo/waves/round-61/capture/manifest.json` is ExecC2Manifest's).
Access date 2026-10-27 (UTC); fetchedAt span 09:15:53Z–09:16:02Z.

## TOOL:

`/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/response_snapshot.py` — stdlib-only Python 3, 233 lines,
sha256 `ba107024c770db194f0b07c806641f1674e109134f62c0eac671e5b06bde1bb7`.

- Population: one subdirectory per surface under `--population` (default `.ufo/waves/round-23/live`), each
  `fetch.json` naming `id` + `url`; id must match `[a-z0-9][a-z0-9-]{0,62}`, url must be http(s) with a host and
  no userinfo (else exit 2 before any GET). Duplicate ids rejected.
- One `GET` per surface, no retry loop. Request headers: `User-Agent: round61` only — no cookies (no cookie
  processor installed), no credentials, no request body, no `Accept`/content negotiation sent.
- Caps, same constants as `scripts/live_snapshot.py`: `MAX_REDIRECTS=5`, `TIMEOUT=20`, `MAX_BODY=2 MiB`.
  Redirect handler refuses a 6th hop, a non-http(s)/userinfo destination (so urllib cannot report an unfetched
  `file:` target as `finalUrl`) and any non-GET redirect re-issue.
- Per surface writes `--out/<id>/response.json` (default `.ufo/waves/round-61/capture`) with: `url`, `finalUrl`,
  `method:"GET"`, `status` (int, or null on transport failure), `headers` = ordered list of
  `{"name","value"}` objects in wire order with duplicates preserved and names as received (not lowercased),
  `headerCount`, `contentType` (last Content-Type field or null), `bytes`, `sha256` of the body, `truncated`
  (2 MiB cap hit), `fetchedAt` (`%Y-%m-%dT%H:%M:%SZ` UTC), `userAgent:"round61"`, `redirects`
  (`[{status,from,to}]`), `error` (null or `TypeName: message`), `bodyFile`.
- Body retention: the received body is written byte-identically to `<id>/body.bin` (`bodyFile:"body.bin"`, null
  when zero bytes), so the recorded `sha256`/`bytes` stay re-verifiable offline without a second fetch.
- Output discipline: one opened output dir, `O_NOFOLLOW` dir fds, each leaf written through a single no-follow
  fd and rejected unless regular/single-link; nothing is written outside `--out`; no temporary file is created,
  so `$TMPDIR` is not used and `/tmp` is never touched.
- Receipt immutability: a pre-flight refuses the run (exit 2, before any GET) if a target `response.json` exists,
  unless `--overwrite`; a re-run otherwise belongs under a fresh `--out`.
- Exits: 0 every attempt recorded (inspect per-surface `status`/`error`); 2 bad population, unsafe id/url,
  existing receipt without `--overwrite`, unwritable output; 64 usage. JSON summary on stdout.
- CLI: `python3 -B scripts/response_snapshot.py [--population DIR] [--out DIR] [--overwrite]`.
- Provenance: the 12 receipts were written by this tool at sha256 `eac57099…039643`; the only later change is
  the `--overwrite` pre-flight guard (report/usage text plus the `main()` pre-flight). Fetch, header, digest and
  write paths were not edited afterwards, so the receipts match the committed fetch logic.

## CAPTURE:

Run: exit 0, stderr empty, wall 10.1 s, 12/12 recorded, `error:null` and `redirects:[]` on all twelve.
Offline re-verification: for all 12 receipts `len(body.bin)==bytes` and `sha256(body.bin)==sha256` (12/12 true);
`method=GET`, `userAgent=round61`, `fetchedAt` on 2026-10-27Z on all twelve; `truncated=false` on all twelve.
Total capture tree: 344,309 bytes (12 `response.json` + 12 `body.bin`).

| id | status | finalUrl | hdrs | bytes | sha256 head |
|---|---|---|---|---|---|
| burnerchrome-kimi | 200 | https://burnerchrome.kimi.page/ | 16 | 11976 | 44dc3491fbc6cdc5 |
| charter-ghp | 200 | https://veigapunk.github.io/charter-ufo-fsd/ | 23 | 53660 | 7c243a1d81357cde |
| charter-kimi | 404 | https://charter-ufo-fsd.kimi.page/ | 14 | 13409 | 93ddca9a021664d5 |
| ds4cc-kimi | 200 | https://ds4cc.kimi.page/ | 16 | 74641 | bc8bb28d7ef97b81 |
| ds4cc-primary | 200 | https://ds4cc.com/ | 22 | 78897 | f2c5d2b3ab34e8e1 |
| lucario-ghp | 200 | https://veigapunk.github.io/lucario/ | 23 | 3435 | bee2d9f5b5777768 |
| lucario-kimi | 404 | https://lucario.kimi.page/ | 14 | 13409 | 93ddca9a021664d5 |
| plazir15-ghp | 200 | https://veigapunk.github.io/plazir-15-site/ | 23 | 38337 | d82af77aee401d22 |
| plazir15-kimi | 404 | https://plazir15.kimi.page/ | 14 | 13409 | 93ddca9a021664d5 |
| plazir27-kimi | 404 | https://plazir27.kimi.page/ | 14 | 13409 | 93ddca9a021664d5 |
| ufo-fsd-kimi-pro | 200 | https://ufo-fsd.kimi.pro/ | 12 | 612 | 1df92e30ba5a76e6 |
| vault-index-kimi | 200 | https://veigapunk.kimi.page/ | 16 | 10059 | a0a7f33aba443a85 |

Duplicate preservation is exercised by the live data, not a fixture: the seven `kimi.page` surfaces each return
two `vary` field-lines with different values (`Accept-Encoding`, `Origin`), and both are recorded as separate
entries in wire order — no merge, no comma-join. Every `finalUrl` equals its requested `url` (0 redirect hops
anywhere).

Observed while retaining receipts (not my census seat — ExecC2HeaderRecon owns the census): `content-type`
present on all 12; `strict-transport-security` on 11 (absent on ds4cc-primary); `x-content-type-options` on 3
(burnerchrome-kimi, ds4cc-kimi, vault-index-kimi); `content-security-policy` on none; no duplicated
content-type/csp/hsts field.

## FAILURES:

No surface was unreachable: 0 transport errors, 0 non-null `error`, 0 `truncated`, 0 blocked redirects. No retry
was attempted anywhere (one GET per surface by construction).

Four surfaces answered HTTP 404 and were recorded as they answered, not retried: `charter-kimi`,
`lucario-kimi`, `plazir15-kimi`, `plazir27-kimi` — each 13,409 bytes with the identical 404 body
(`93ddca9a021664d5…`), 14 header field-lines, still carrying `content-type` and `strict-transport-security`.
Those receipts hold the host's error page, not the intended page; the 2xx-only `content_type_present` class in
the contract is therefore not triggered by them.

## LIMITS:

- Single snapshot at 09:15–09:16Z: CDN/edge fields (`Date`, `Age`, `CF-RAY`, `X-Cache(-Hits)`, `x-fc-request-id`,
  `X-GitHub-Request-Id`) are per-request, so byte-identity across runs is not expected and a later run would
  produce different `sha256` values for dynamic pages.
- "One GET per surface" is a code property (a single `opener.open` per surface, no loop); it is not observable
  from the receipts themselves — a sentinel would have to watch egress.
- 2 MiB cap: `bytes`/`sha256` cover the received prefix and `truncated` marks the cap. No surface hit it here.
- Body bytes are what `http.client` hands back after chunked-transfer decoding: the eight kimi-family surfaces
  carry a `Transfer-Encoding` field while the four github.io/ds4cc.com pages send `Content-Length`; the receipts
  say nothing about the wire framing beyond those headers [INFERENCE: decoding, not verified against a raw
  capture].
- Header values are recorded verbatim with no redaction. This run contained no `Set-Cookie`, `Cookie`,
  `Authorization`, `Proxy-Authorization` or `WWW-Authenticate` field and no URL userinfo, so no session material
  was retained; a surface that did send such a field would be captured as-is.
- No browser semantics: no JS, no HTTP/2, no meta-refresh/HTML-level redirect following, no TLS-policy
  inspection beyond Python's default certificate verification.
- Nothing independently confirms that the servers meant what they sent, and no second fetcher cross-checks these
  receipts; that is w2's sentinel/reviewer job. I ran no build, lint, test suite or audit tool.

## Artifacts

- Tool: `kake-shokunin/scripts/response_snapshot.py`.
- Receipts: `kake-shokunin/.ufo/waves/round-61/capture/<id>/response.json` + `body.bin` (12 each).
- Evidence copied out of scratch: `w1/ExecC2Capture.files/capture-summary.json` (stdout of run 1),
  `w1/ExecC2Capture.files/evidence.txt` (per-id integrity + presence matrix), `w1/ExecC2Capture.files/run.txt`
  (commands, exit codes, provenance hashes, the no-rewrite check).
- Messaged peers with the receipt schema: ExecC2Manifest, ExecC2Audit, ExecC2HeaderRecon (+ addendum),
  ExecC2Counter.
- Cross-seat confirmation (peer runs, not mine): ExecC2Audit reports the audit parsing all 12 receipts and
  resolving all 12 checks with zero `could_not_evaluate` (checks=12 findings=13, exit 1); ExecC2HeaderRecon
  independently reproduced the five header aggregates and the 12/12 offline integrity result; ExecC2Manifest's
  v1 manifest binds all 12 `source` paths. The LIMITS statement above still holds: this seat ran no audit.
- Scratch `/fast/scratch/hyaku/kake-r61/ExecC2Capture` deleted after copying.
- No `git add/commit/stash/checkout/reset/pull/push`, no jj mutation; lane writes limited to the tool, the
  capture tree and this report/.files.

VERDICT: capture tool written and run once over all 12 surfaces — 12/12 receipts retained and offline-verified (status, ordered duplicate-preserving headers, sha256, bytes, fetchedAt, UA round61); no surface unreachable; 4 surfaces answered 404 and are recorded as such; receipts provably not rewritten by a second invocation.
