# ExecC2Manifest

Claim C2 manifest seat (wave w1, build). Deliverable: the version-1 expectation manifest the
offline `scripts/header_audit.py` reads, bound to the 12 round-61 capture receipts. Expectations
declared from POLICY over frozen round-23 surface metadata — never from an observed header value.

## MANIFEST

Path: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/capture/manifest.json`
(bytes 5125, sha256 `c89707ab61587f06dbe7029d1d71bc5589d3502efb1d142e31621307110b64b6`)
Shape: `{"version": 1, "checks": [...]}` — **12 checks**, ids = the 12 round-23 surface ids,
one per surface, sorted by id. Each check: `id`, `source` (lane-root-relative
`.ufo/waves/round-61/capture/<id>/response.json`), `url` (requested URL, copied verbatim from
`.ufo/waves/round-23/live/<id>/fetch.json`), `https` (bool, derived from the URL scheme), `expect`.

`S` below = `["content-type","content-security-policy","strict-transport-security"]` (identical in
all 12 checks, in that order):

| id | https | content_type_present | hsts_present | xcto_nosniff_value | csp_present | singleton_fields |
|---|---|---|---|---|---|---|
| burnerchrome-kimi | true | true | true | true | true | S |
| charter-ghp | true | true | true | true | true | S |
| charter-kimi | true | true | true | true | true | S |
| ds4cc-kimi | true | true | true | true | true | S |
| ds4cc-primary | true | true | true | true | true | S |
| lucario-ghp | true | true | true | true | true | S |
| lucario-kimi | true | true | true | true | true | S |
| plazir15-ghp | true | true | true | true | true | S |
| plazir15-kimi | true | true | true | true | true | S |
| plazir27-kimi | true | true | true | true | true | S |
| ufo-fsd-kimi-pro | true | true | true | true | true | S |
| vault-index-kimi | true | true | true | true | true | S |

Schema self-check (run, exit 0): `version == 1`; 12 checks; 12 unique ids; every check has exactly
the keys `id,source,url,https,expect`; every `expect` has exactly
`content_type_present,hsts_present,xcto_nosniff_value,csp_present,singleton_fields`; the
`singleton_fields` list is byte-equal to the frozen order above in all 12.

## POLICY NOTE

Uniform rules, one per expectation class; the only permitted per-check variation is `hsts_present`,
and it is a function of the URL scheme alone (all 12 surfaces are `https://` → true ×12). No check
was tuned to the header it landed on.

- `content_type_present=true` (all): every one of the 12 checks is a page fetch expected to return a
  representation, so a 2xx answer without a media type is a policy finding. Applies to 2xx only —
  the four surfaces that answered 404 are outside this class by the frozen semantics, not by tuning.
- `hsts_present = (url scheme == https)` (all → true): the 12 URLs are https by the round-23
  population; a browser is expected to be told the TLS-only policy in `Strict-Transport-Security`
  (S430, RFC 6797).
- `xcto_nosniff_value=true` (all): the expectation is conditional by construction ("where the field
  occurs, its value is exactly `nosniff`"); asserting it for every check expresses the uniform policy
  that a surface which sets the field must set it correctly (S432, WHATWG Fetch / nosniff).
- `csp_present=true` (all): every surface under audit is a public HTML publisher and the declared
  policy is that each ships a Content-Security-Policy (S431, W3C CSP Level 3).
- `singleton_fields=[content-type, content-security-policy, strict-transport-security]` (all): the
  three declared names are single-occurrence field-lines (S433, RFC 9110 §5.3 / field-line
  semantics). `set-cookie` is deliberately absent — repeatable by contract (case H10), never a
  singleton; `vary` observed repeated on several surfaces is likewise not declared.

Declaration order (evidence the expectations are not outcome-derived): the manifest was written at
`2026-10-27 06:15:45.745 -03`; the capture receipts it binds did not exist yet — first receipt
mtime `06:15:55.458`, last `06:16:03.721`. Inputs were the frozen round-23 `fetch.json` records
(fetched 2026-10-21) and the policy rows above.

Disclosure of what the receipts show (census only — NOT an input to any declaration and NOT a
score; R3's verdict is recorded, not asserted):
- `Content-Security-Policy` (or any `*-security-policy` name): present 0/12.
- `Strict-Transport-Security`: present 11/12; absent on `ds4cc-primary` (200 over https).
- `X-Content-Type-Options: nosniff`: present 3/12 (`burnerchrome-kimi`, `ds4cc-kimi`,
  `vault-index-kimi`).
- Duplicate declared singleton fields: 0/12. Other repeated fields (`vary`) are outside the list.
- Field-name syntax faults (space/tab in name): 0/12.
- Lane audit (`python3 -B scripts/header_audit.py --manifest .ufo/waves/round-61/capture/manifest.json`,
  run after the tool landed at 06:16): `checks=12 findings=13`, exit **1** — 12 × `csp_present`
  (`missing=content-security-policy`) plus 1 × `hsts_present` on `ds4cc-primary`
  (`https=true missing=strict-transport-security`). Byte-identical output and same exit when the
  same absolute manifest was audited from a foreign cwd (scratch dir), so the manifest's
  lane-root-relative `source` resolves under both invocations. Output retained:
  `.files/audit.out`, `.files/audit2.out`. Per contract this non-clean live census is reported, not
  a failure of the claim.

## RECEIPTS

sha256 of each `response.json` (the `source` the manifest binds), read after the capture completed:

| id | bytes | sha256(response.json) |
|---|---|---|
| burnerchrome-kimi | 1492 | 3b2e6530699f82b04d5e44e77c8bb0749656ace45e9b0bd3c847dd185dbef81f |
| charter-ghp | 1982 | cf721dfd1a4ef1a2d141833dacf2ba922054682f8f55992d25094563622da08a |
| charter-kimi | 1400 | d9e10c72d222b75121eecdd7fe4d3a6af90376139d4f4dd8f5686ebfc4bd1809 |
| ds4cc-kimi | 1478 | 45d1f10f53ede3d2f59b25a5a623f0db927ae88f089bdfa58d56e6efeb170fde |
| ds4cc-primary | 1851 | 103e3013c3fdca20f0b3f374c3dc8c32430c4c23bbe02be4e56d009356661040 |
| lucario-ghp | 1963 | aad28be25c0518d6e049a4d9627686c6afd5b5f7a42548e8321d9eb883a041e6 |
| lucario-kimi | 1384 | a28350d59cbc37ac9583b1459de5c00b4e1af5d0210de03e68ecf3cd2f2df278 |
| plazir15-ghp | 1980 | 1603e62d0b5f73f7e4a389aad02722a4170eda37d6621940c7f190fb89e71e35 |
| plazir15-kimi | 1386 | 0390704f5a3a654789e88b1312daa2d4ca3b5b52f19ff12b03da27d010b2622e |
| plazir27-kimi | 1386 | 244c419e8a38a2820f3f8a765814a0e3d20fbcbf378c5b8cb38aab0fe273be10 |
| ufo-fsd-kimi-pro | 1268 | 1de9733b26fdc3424e6e4e968d54c2a807828adaa187b7bd2416417dec4821d7 |
| vault-index-kimi | 1486 | 6c3b5eac246303f25359bfcb1936be4ce0544db210f9510e4292be78bd44a99b |

Receipt lint (run, exit 0, output in `.files/lint.txt`; script `.files/lint_receipts.py`): all 12
parse as JSON; all 12 carry the capture tool's 15 keys (`url, finalUrl, method, status, headers,
headerCount, contentType, bytes, sha256, truncated, fetchedAt, userAgent, redirects, error,
bodyFile`); `headerCount == len(headers)` in all 12; every `bodyFile=body.bin` resolves next to the
receipt and its sha256 equals the receipt's recorded `sha256` (0 mismatches); `userAgent="round61"`
in all 12; `finalUrl == url` and 0 redirects in all 12; `fetchedAt` 2026-10-27T09:15:53Z..09:16:02Z
(access date). Statuses: 200 ×8, 404 ×4 (charter-kimi, lucario-kimi, plazir15-kimi, plazir27-kimi).
Every `source` in the manifest resolves to an existing receipt (12/12).

Discovery uniqueness for counter R3: `manifest.json` under `.ufo/waves/round-61/capture/` is the only
version-1 manifest with a `checks` array in this wave tree. A byte copy was briefly kept in
`.files/` as evidence and then removed for that reason; `.files/manifest.json` no longer exists, and
the canonical file's citation is the path + sha256 in `MANIFEST` above.

Independent confirmation from the audit seat (ExecC2Audit, its own run, recorded in its report as a
smoke run, not a verdict): exit 1, `checks=12 findings=13`, every source resolved, zero
`could_not_evaluate` — same as this seat's run.

## RISKS

- `source` is lane-root-relative. Observed: the current `scripts/header_audit.py` resolves it correctly
  from the lane root and from a foreign cwd (both runs identical, exit 1), so this is retired for the
  tool as it stands; a later rewrite or the counter's R3 harness could still resolve differently.
- `csp_present=true` on all 12 makes R3's live census non-clean by construction (0/12 ship CSP). That
  is the declared policy, not tuning; R3's verdict is recorded, not asserted, per contract.
- Receipt stability (confirmed by the capture seat): `response_snapshot.py` refuses to rewrite an
  existing receipt (a re-run exits 2 without `--overwrite`), so the 12 digests above are stable for
  the round; a deliberate `--overwrite` re-run would invalidate them and the manifest's `source`
  paths would then bind different blobs.
- Declaration timing is evidenced by mtimes in a live workspace, not by a commit: once the wave is
  committed, the manifest and the receipts land together and the ordering argument rests on this
  report plus the fact that every expected field was sourced from round-23 metadata and policy rows.
- The audit exit 1 is expected for this manifest under the frozen classes; a reader who equates exit 1
  with "manifest broken" would misread it (exit 1 = policy findings, exit 2 = manifest fault).

VERDICT: manifest v1 written at `.ufo/waves/round-61/capture/manifest.json` (12 checks, sha256 `c89707ab…64b6`), declared from policy before any capture landed, bound 12/12 to parsing, body-verified receipts, and read cleanly by the lane audit (`checks=12 findings=13`, exit 1 = recorded census).
