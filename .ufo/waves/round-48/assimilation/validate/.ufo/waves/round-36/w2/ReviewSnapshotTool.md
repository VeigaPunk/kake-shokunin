# ReviewSnapshotTool — falsify review of `scripts/source_snapshot.py` (r36 wave 2)

Axes (godspeed): recording fidelity, safe fetching, contract conformance. Attacked the landed
recorder at master `f3a38bf` (291 lines). `git show 4d5b3d55:scripts/source_snapshot.py` and
`git show f3a38bf:…` have identical sha256 `8530a8c5…130`, `git diff` empty — the "tool from
wave-1 ExecToolBuild, unedited" claim holds. Python 3.14.8. Note: the lane working tree
(25f8487) adds one `Accept-Language` header post-wave-2 (ReopenFlagS068); orthogonal to every
finding below, which reproduce against the f3a38bf bytes.

Method: full read; offline 127.0.0.1-only scenario server (`harness.py`: 21-item benign run,
5 single-item probes, 1 write-scope probe; 45 requests); round-trip of produced manifests
through the landed `scripts/source_recheck.py` (offline, reads only). No owned host contacted;
no tools installed. All runs under `/fast/scratch/hyaku/kake-r36w2/ReviewSnapshotTool/`.

## Verified clean (line cites = scripts/source_snapshot.py @ f3a38bf)
- No redirect following: `NoRedirect` :57-62 returns None; every 3xx surfaces as HTTPError and
  is recorded as a hop. Server log shows each hop as its own GET: hops `[{302,"/ok"},{200,""}]`;
  same for 303/307/308, absolute, and other-host (`http://localhost:8391/`) Locations.
- Raw Location recorded; `urljoin` :167,169 only picks the next URL; receipts carry
  `resolvedLocations` (the RFC 3986 resolution) for diagnosis.
- 8-hop cap exact: 8×302→200 recorded (8 hops + final); 9-chain → too_many_redirects, not
  emitted (:128 `range(max_hops + 1)`, :157).
- Pacing: 43 of 45 gaps ≥ 0.9 s; the only two sub-second gaps (0.051/0.049 s) are across
  process starts (`_LAST_REQUEST` is per-process, global across items inside a run, :105/:109/:129).
- Body cap: exactly 8 MiB+1 → truncated → body_too_large, not emitted (:104, :227-229).
- contentType recorded as `""` when the header is absent (contract wants a str; :236).
- Manifest shape: `{"version":1,"checks":[…]}`; final hop non-redirect with `location:""`
  matches the recheck validator (`source_recheck.py:436-469`); non-200 final carries no
  contentType/body; 200 always carries both (:231-236).
- `safe_name` neutralizes traversal id `"../evil"` → `evil-2d6afc71.body` (:68-75).
- Input faults skip with receipts: invalid_id / invalid_url (userinfo) / invalid_quote /
  invalid_item all observed.
- No owned-host guard: confirmed — nothing in the tool consults freshness-pins.json;
  SKILL.md:1070-1071 puts that burden on the input list (matches the assignment's claim).

## Findings (advisory for the L1; severity = impact when a hostile/odd source is fetched)
F1 HIGH robustness — one malformed Location crashes the whole run and loses the manifest plus
ALL receipts (written only at :278-282, after the loop). Repros (each exit 1, traceback, no
manifest.json / receipts.json):
  - `Location: http://[` → `ValueError("Invalid IPv6 URL")` raised inside urllib's own
    `http_error_302` (it urlparses the raw Location before NoRedirect is consulted).
  - `Location: http://127.0.0.1:8391/<non-ascii>` → `UnicodeEncodeError` in http.client
    putrequest `_encode_request` (ascii).
  Neither is in the except tuple at :134 (URLError, HTTPException, OSError); both escape
  `record()` and kill `main()`. Mid-run, every earlier receipt dies with the crash.
  Fix: widen the caught set around the hop walk; write receipts incrementally.
F2 HIGH safe-fetch/contract — a redirect's Location is fetched under any scheme (:169 never
re-validates; `valid_url` :77 applies to the input item only):
  - 302 → `file:///etc/hostname`: urllib's FileHandler read the local file (receipt
    `finalUrl: "file:///etc/hostname"`); the response carries no HTTP status, so the emitted
    check hop is `{"status": null}` → landed recheck: `check_invalid`, verdict
    `could-not-evaluate`, exit 2. One remote header poisons the manifest verdict and performs a
    local read outside the contract's http(s) universe. (runs/nonhttp-file)
  - 302 → `data:text/plain,hi`: same status-null check emitted; recheck exit 2.
    (runs/nonhttp-data)
  - 302 → `ftp://127.0.0.1:2121/x`: an FTP fetch was attempted (receipt "ftp error:
    Connection refused") — FTPHandler is active; arbitrary scheme/host fetches are attempted.
    (runs/nonhttp-ftp)
  Fix: re-validate each resolved target (scheme http/https, host present) before fetching;
  skip with a receipt otherwise.
F3 MEDIUM — duplicate ids silently share one body file: two items with id `dup` → both
manifest checks name `dup.body`; the second write overwrites the first (:233-234). Round-trip:
the first check's quote (present in the body actually fetched for it) reports `quote_missing`
— the manifest no longer describes the first fetch, and recheck cannot tell the two findings
apart (both named "dup"). `safe_name`'s "no collisions" docstring (:69) holds only for
distinct ids. Fix: reject duplicate ids with a receipt.
F4 MEDIUM — writes follow the manifest path, not `--out-dir`: with `--out-dir X --manifest
Y/manifest.json`, X stays empty and manifest+receipts+bodies land in Y (observed; :234,
:279-282). SKILL.md's round-36 row "write scope: --out-dir only" holds only for the
documented invocation where `--manifest` is inside DIR.
F5 LOW — `redirect_without_location` fabricates `"location": ""` for a hop whose Location
header was absent (:152): absence and empty value are indistinguishable in the honesty record.
F6 LOW — `too_many_redirects` receipt drops the 9th hop (the response that tripped the cap;
:157-163 returns before appending); the trailing return after the :128 loop is unreachable.
F7 LOW — receipts can carry credentials: input userinfo is rejected (:77-90), but a 302 to
`http://u:p@…/…` records the userinfo URL in receipt `finalUrl`/`hops`; urllib then fails with
a DNS error (fails closed, but the secret is now in receipts.json).

## Observations (not defects)
- Redirect-hop bodies are read too (≤8 MiB each): a 9-request chain can pull ~72 MiB for one
  check; the cap is per response, not per check.
- 30 s timeout is wired (:52, :103) but not live-tested against a hanging server.
- Proxy env would be honored (default ProxyHandler); operator env had none; runs stripped it.

## Offline run (excerpts; full: runs/harness-output.txt)
- benign: `python3 -B scripts/source_snapshot.py --input runs/benign/input.json --out-dir
  runs/benign/out` → exit 0, "checks 13 of 21"; not recorded: noloc-302
  (redirect_without_location), big-body (body_too_large), nine-hops (too_many_redirects),
  user-302 (fetch_error: URLError: … Name or service not known), None (invalid_id), badurl
  (invalid_url), emptyquote (invalid_quote), None (invalid_item). Manifest: eight-hops with
  8×302 + 200; rel-302 hops `[{302,"/ok"},{200,""}]`; `../evil` → `evil-2d6afc71.body`.
- crash: single-item run with `Location: http://[` → exit 1, stderr
  `ValueError: Invalid IPv6 URL`, "manifest exists: False | receipts exists: False".
- round-trip: `python3 -B scripts/source_recheck.py --manifest
  runs/nonhttp-file/out/manifest.json` → exit 2 `{"verdict":"could-not-evaluate",
  "checksEvaluated":0,"findings":[{"check":"tofile","reason":"check_invalid","target":null}]}`;
  on runs/benign → exit 1 failed-policy: gone(final-404), moved(code-308→…/ok),
  quote_missing+unsupported_type(dup), unsupported_type(noctype-200) — the dup pair confirms F3.

Artifacts (sandbox): `/fast/scratch/hyaku/kake-r36w2/ReviewSnapshotTool/{harness.py,
runs/harness-output.txt, runs/benign, runs/crash-tobad, runs/crash-nonascii,
runs/nonhttp-file, runs/nonhttp-data, runs/nonhttp-ftp, runs/xman, runs/xdir}`; recorder under
review at `clone/scripts/source_snapshot.py` @ f3a38bf.
Not verified: live timeout behavior, proxy interception, real-world hosts (out of bounds),
sealed-counter interplay (another seat's item). No tools installed; pacman untouched.
