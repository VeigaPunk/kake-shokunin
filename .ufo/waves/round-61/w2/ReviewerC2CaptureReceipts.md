# ReviewerC2CaptureReceipts

Scope: Round-61 C2 capture receipts and their committed provenance. Read the round-61 contract and tooling rules first. No lane files were changed except this report; verification read the lane at `HEAD=f5a9b8acc8e4d0995e8ba849c4a9d56ba1ab0a8f`.

## Findings

- **Receipt integrity: 12/12 pass.** Re-read each `response.json` and corresponding `body.bin` from committed `HEAD` bytes using `git cat-file`. All JSON parsed. For every surface, `sha256(body.bin) == response.json.sha256`, `len(body.bin) == response.json.bytes`, and `headerCount == len(headers)`. The per-receipt run summary (`w1/ExecC2Capture.files/capture-summary.json`) agrees with each committed receipt on body digest, bytes, header count, status, final URL, and error (12/12; zero mismatches).
- **Capture fields: 12/12 pass.** Every method is `GET`; `userAgent` is `round61`; `fetchedAt` falls on 2026-10-27 UTC; `error` is null; `truncated` is false; and each body is below the 2 MiB cap. All 12 requested URLs match the round-23 population and each `finalUrl` matches its requested URL. Redirect count is zero for all 12 (zero total; limit is five). Statuses are 200 ×8 and 404 ×4 (`charter-kimi`, `lucario-kimi`, `plazir15-kimi`, `plazir27-kimi`); the 404s are recorded responses, not integrity failures.
- **Headers/credentials: no credential-like response header found.** The 12 responses contain 33 distinct case-insensitive header names (207 field-lines total); no `Cookie`, `Set-Cookie`, `Authorization`, `Proxy-Authorization`, `Proxy-Authenticate`, `WWW-Authenticate`, API-key, token, or auth-named field. The tool's request construction at `scripts/response_snapshot.py:86-90` creates one GET with only `User-Agent: round61`; there is no request body or cookie/credential header construction. The tool serializes response field-lines in order without collapsing duplicates (`:121-135`). Observed duplicate `vary` fields are retained.
- **Manifest and immutability: pass.** Manifest v1 has 12 checks; IDs equal the 12 population IDs, all 12 sources resolve to committed receipts, and each manifest URL matches the source receipt URL. Git history shows the capture tree (manifest, response JSONs, body files) was introduced in `f512eee`; each inspected response and body has one add commit and one history commit, with no later rewrite through HEAD.
- **Response JSON digests (computed over committed bytes):**

| Surface | response.json SHA-256 |
|---|---|
| burnerchrome-kimi | `3b2e6530699f82b04d5e44e77c8bb0749656ace45e9b0bd3c847dd185dbef81f` |
| charter-ghp | `cf721dfd1a4ef1a2d141833dacf2ba922054682f8f55992d25094563622da08a` |
| charter-kimi | `d9e10c72d222b75121eecdd7fe4d3a6af90376139d4f4dd8f5686ebfc4bd1809` |
| ds4cc-kimi | `45d1f10f53ede3d2f59b25a5a623f0db927ae88f089bdfa58d56e6efeb170fde` |
| ds4cc-primary | `103e3013c3fdca20f0b3f374c3dc8c32430c4c23bbe02be4e56d009356661040` |
| lucario-ghp | `aad28be25c0518d6e049a4d9627686c6afd5b5f7a42548e8321d9eb883a041e6` |
| lucario-kimi | `a28350d59cbc37ac9583b1459de5c00b4e1af5d0210de03e68ecf3cd2f2df278` |
| plazir15-ghp | `1603e62d0b5f73f7e4a389aad02722a4170eda37d6621940c7f190fb89e71e35` |
| plazir15-kimi | `0390704f5a3a654789e88b1312daa2d4ca3b5b52f19ff12b03da27d010b2622e` |
| plazir27-kimi | `244c419e8a38a2820f3f8a765814a0e3d20fbcbf378c5b8cb38aab0fe273be10` |
| ufo-fsd-kimi-pro | `1de9733b26fdc3424e6e4e968d54c2a807828adaa187b7bd2416417dec4821d7` |
| vault-index-kimi | `6c3b5eac246303f25359bfcb1936be4ce0544db210f9510e4292be78bd44a99b` |

## Provenance caveat

The committed `scripts/response_snapshot.py` SHA-256 is `ba107024c770db194f0b07c806641f1674e109134f62c0eac671e5b06bde1bb7`, matching the capture report. The run report says the receipts were produced by earlier tool bytes with SHA-256 `eac57099a6e097a28638bc2b7e29ddd3dfd301b34c0caa255d8d708bcb039643`; thus they were **not produced by the exact committed file digest**. This difference is disclosed in `w1/ExecC2Capture.md` lines 37-39. Its stated boundary is substantiated by the committed sentinel evidence: `pre_excerpt.txt` is still a substring of the committed tool, and the recorded pre/current static-audit JSONs differ in the `--overwrite` pre-flight/usage addition and corresponding line-count/tool-SHA metadata; fetch, header, digest, and write paths are reported unchanged. The run summary's body digests and all receipt bytes were independently rechecked above. The historical producing executable itself is not present as a committed blob in the capture tree, so its exact run cannot be reproduced from this lane evidence.

## Verification gaps / residual risk

- No LSP device/server was available in this seat's tool inventory; no references/definition/diagnostics requests could be made. These findings concern fixed committed artifacts and were checked by committed-byte reads and the capture tool's implementation, not by semantic caller analysis.
- Request credentials are established from tool source (request construction sends only the user-agent) rather than observed from a network trace. Response-header scan found no credential-bearing fields. The tool intentionally records response headers without redaction; this run retained no credential header.
- The capture run was performed by the earlier `eac57099…` tool version, not the exact final committed digest. The documented source delta and independent receipt integrity checks bound this provenance discrepancy but do not make the historical executable available for replay.

VERDICT: 12/12 committed capture receipts are parseable, body-digest/byte/header-count consistent, manifest-bound, GET-tagged, round61-tagged, redirect-free, and free of credential-like response headers; the reported pre-run to committed tool digest change is limited by the recorded evidence to the later --overwrite guard, with the exact historical executable unavailable for replay.