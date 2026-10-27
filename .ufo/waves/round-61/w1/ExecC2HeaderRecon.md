# ExecC2HeaderRecon

Seat: leaf executor, claim C2 recon (header census). Lane `kake-shokunin`, round 61, wave w1,
access date 2026-10-27 (UTC), lane master at round open `9f07731a873585e655a6518233ea39f5d9fb8204`.
Inputs read (read-only, committed/worktree bytes of the lane): `.ufo/waves/round-61/contract.md`,
`contract.json`, `w1-spec.json`, `.ufo/waves/round-23/c2-population.json`, the 12 receipts under
`.ufo/waves/round-61/capture/<id>/response.json` (+ `body.bin`), `capture/manifest.json`,
`scripts/header_audit.py` (as landed by ExecC2Audit), `sources/{S430,S431,S432,S433}.html`.
No network fetch was issued by this seat: every datum below comes from the capture receipts.
Census method is archived and re-runnable: `.files/census.py`, `.files/predict.py`,
`.files/census.json`, `.files/predict.txt`, `.files/audit.txt`, `.files/audit.json`,
`.files/toolrev.txt`.

Population = the 12 round-23 live surface ids. Receipt integrity re-verified offline for 12/12:
sha256 equals the sha256 of the retained `body.bin`, `bytes` equals the file length, `fetchedAt`
is 2026-10-27T09:15:53Z..09:16:03Z, `userAgent` = `round61`, `finalUrl` == `url`, `redirects` = [],
`error` = null, `truncated` = false, no `Set-Cookie` on any surface.

## CENSUS:

Named singletons = the three declared in the manifest (`content-type`, `content-security-policy`,
`strict-transport-security`); `x-content-type-options` is also counted and shown because the
manifest declares an expectation on it.

| surface | status | #hdr | content-type | strict-transport-security | x-content-type-options | content-security-policy | dup(singletons) | field-name faults |
|---|---|---|---|---|---|---|---|---|
| `ds4cc-primary` | 200 | 22 | present | **MISSING** | absent | **MISSING** | none | none |
| `plazir15-ghp` | 200 | 23 | present | present (`max-age=31556952`) | absent | **MISSING** | none | none |
| `charter-ghp` | 200 | 23 | present | present (`max-age=31556952`) | absent | **MISSING** | none | none |
| `ds4cc-kimi` | 200 | 16 | present | present (`max-age=31536000; includeSubDomains`) | `nosniff` | **MISSING** | none | none |
| `burnerchrome-kimi` | 200 | 16 | present | present (`max-age=31536000; includeSubDomains`) | `nosniff` | **MISSING** | none | none |
| `vault-index-kimi` | 200 | 16 | present | present (`max-age=31536000; includeSubDomains`) | `nosniff` | **MISSING** | none | none |
| `plazir27-kimi` | 404 | 14 | present | present (`max-age=31536000; includeSubDomains`) | absent | **MISSING** | none | none |
| `ufo-fsd-kimi-pro` | 200 | 12 | present | present (`max-age=31536000; includeSubDomains`) | absent | **MISSING** | none | none |
| `lucario-ghp` | 200 | 23 | present | present (`max-age=31556952`) | absent | **MISSING** | none | none |
| `lucario-kimi` | 404 | 14 | present | present (`max-age=31536000; includeSubDomains`) | absent | **MISSING** | none | none |
| `plazir15-kimi` | 404 | 14 | present | present (`max-age=31536000; includeSubDomains`) | absent | **MISSING** | none | none |
| `charter-kimi` | 404 | 14 | present | present (`max-age=31536000; includeSubDomains`) | absent | **MISSING** | none | none |

Column totals: content-type 12/12 present; strict-transport-security 11/12 present;
x-content-type-options 3/12 present (3 × exactly `nosniff`, 0 non-`nosniff` values);
content-security-policy 0/12 present; singleton duplicates 0/12; field-name syntax faults 0/12
(all 207 recorded field lines / 12 surfaces carry RFC 9110 token names — no space, no non-ASCII,
no leading OWS).

## FINDINGS:

What the audit flags on this manifest (12 checks, policy declared uniformly: all four booleans
true, singletons `[content-type, content-security-policy, strict-transport-security]`):

1. **`csp_present` × 12 — every surface.** No surface returns a `Content-Security-Policy` field.
   This is 12 of the 13 findings. Includes the four 404 error pages (see 7): the frozen class is
   status-blind, unlike `content_type_present` which is 2xx-gated.
2. **`hsts_present` × 1 — `ds4cc-primary` only.** `https://ds4cc.com/` serves GitHub Pages
   (`Server: GitHub.com`, `Via: 1.1 varnish`) with no `Strict-Transport-Security`, while the three
   `*.github.io` surfaces on the same platform do send `max-age=31556952`. Grounded by S430 §7.2:
   "If an STS header field is included, the HSTS Host MUST include only one such header field."
   A response with none is the finding here because the check declares `https: true` +
   `hsts_present: true`.
3. **`xcto_nosniff_value` × 0, and that is a declaration gap, not cleanliness.** The frozen class
   fires only on a *recorded* field with a value other than `nosniff`; 9 of 12 surfaces send no
   `X-Content-Type-Options` at all and are therefore silent. The manifest's
   `"xcto_nosniff_value": true` reads as an expectation of the header's presence but asserts
   nothing about absence. Nothing at the live surfaces is mis-valued: the three present values are
   exactly `nosniff` (lowercase as served). Naming this is the recon duty; the class is frozen by
   the contract and is not changed here.
4. **`singleton_fields` × 0, correctly.** No surface duplicates `content-type`,
   `strict-transport-security` or `content-security-policy` (each occurs at most once, under
   mixed casing). `vary` is recorded twice (`Accept-Encoding`, `Origin`) on the 7 kimi.page
   surfaces; that is legal — RFC 9110 §5.3: "a sender MUST NOT generate multiple field lines with
   the same name" applies only "unless that field's definition allows multiple field line values
   to be recombined as a comma-separated list", and `Vary` is `#( *field-name )`. It is not in the
   singleton list, so the duplicate is not a finding — a live positive control that duplicate
   detection does not over-fire on the one duplicated name the census contains.
5. **Manifest declares `content-security-policy` a singleton — latent false-positive class.**
   CSP3 §8.1 shows two `Content-Security-Policy` field lines in one response as legitimate and
   states: "when multiple policies are present, each must be enforced or reported, according to
   its type". A compliant multi-policy publisher would therefore be reported under
   `singleton_fields` by this manifest. Zero live impact this round (no surface sends CSP at
   all), so R3's verdict is unaffected; the risk is in wave-2 reproduction and in any future
   re-use of this manifest shape. `content-type` and `strict-transport-security` are genuine
   singletons (RFC 9110 §8.3 field definition; RFC 6797 §7.2 quoted above).
6. **`field_name_syntax` × 0 — fixture-only class this round.** No recorded name fails the token
   test, so the H12 path is exercised only by the counter's fixtures, not by live data.
7. **Status shape: 4 of 12 surfaces answer 404** (`charter-kimi`, `lucario-kimi`,
   `plazir15-kimi`, `plazir27-kimi`), all four with the identical 13409-byte cloudflare body
   (sha256 `93ddca9a0216…`) and with `Content-Type: text/html; charset=utf-8` and HSTS present.
   `content_type_present` is 2xx-gated, so those four produce no content-type finding; their
   `csp_present` findings (4 of the 13) come from the error template, not from a served page.
8. **Case folding is exercised on live data, not just fixtures.** The kimi.page surfaces serve
   lowercase field names (`content-type`, `strict-transport-security`,
   `x-content-type-options`, `vary`) while GitHub/Fastly serves Title-Case. The audit located
   both correctly, so the case-insensitive path behind `hsts_present` / `content_type_present` is
   evidenced live.
9. **Observation, no fault:** `x-internal-adhoc-canary: 586427312` is recorded on all 7 kimi.page
   surfaces and on none of the `*.github.io`, `ds4cc.com` or `ufo-fsd.kimi.pro` surfaces; the value
   is constant across the 7. The name is a valid token and violates no expectation class. What the
   field means is [INFERENCE] and is not claimed.
10. **Context, not a claim:** versus the round-23 bodies, 10 of 12 are byte-identical; two changed —
    `ds4cc-primary` (76159 → 78897 bytes) and `ds4cc-kimi` (same 74641 bytes, different sha256).
    The census is of the 2026-10-27 receipts regardless.

## CROSS-CHECK:

Audit tool present at `.ufo/waves/round-61`-time: `scripts/header_audit.py` and
`scripts/response_snapshot.py` (landed by ExecC2Audit / ExecC2Capture). Manifest
`.ufo/waves/round-61/capture/manifest.json` is version 1 with 12 checks whose ids equal the 12
population ids and whose `source` paths all resolve from the lane root to the matching
`response.json`.

Run (from the lane root, read-only, network-free):

    python3 -B scripts/header_audit.py --manifest .ufo/waves/round-61/capture/manifest.json

Output: 13 finding lines, one per (check, class) pair — the 12 `csp_present` lines
(`missing=content-security-policy`) plus `ds4cc-primary hsts_present
https=true missing=strict-transport-security` — then `checks=12 findings=13`, **exit 1**.

`--json`: `version 1`, `verdict "failed-policy"`, `checksCount 12`, `findingsCount 13`,
`policyFindings 13`, `unevaluableChecks []`, `problem null`; the 12 per-check items are all
`failed-policy` (11 with 1 finding, `ds4cc-primary` with 2).

Revision pin: the audit seat was still landing while this was measured — 40210 bytes at 06:16 and
41608 bytes / sha256 `282d5b04676f2de1ee80fb360629c81dfbd15e0790b2033f53e1f85d741569b2` at
06:18:07. Both revisions were run on this manifest and produced the identical 13-line output,
`checks=12 findings=13`, exit 1 (captures in `.files/audit.txt`, `.files/audit.json`,
`.files/toolrev.txt`). The L1 should re-run this one command after wave-1 integration; the
expected output is the 13 lines above.

Differential: `.files/predict.py` is this seat's independent implementation of the five frozen
classes over the same receipts under the same declared policy. Its finding set is exactly the
tool's: 13 findings, `{(check, class)}` identical, empty difference in both directions
(`.files/predict.txt` vs `.files/audit.json`). `header_audit.py --selftest` was NOT run by this
seat (audit seat's scope) — UNRUN here.

Second independent witness: the capture seat (ExecC2Capture-2) reported its own presence tallies
after landing the receipts — content-type 12/12, STS 11/12 (absent on `ds4cc-primary`), XCTO 3/12
(`burnerchrome-kimi`, `ds4cc-kimi`, `vault-index-kimi`), CSP 0/12, two `vary` lines on the seven
kimi.page surfaces, four 404s on one 13,409-byte body. This census derives the same five aggregates
from the receipts directly and agrees on every one; the two computations share only the receipts.

VERDICT: census of all 12 receipts is complete and internally consistent — 13 predicted findings (12 × `csp_present`, 1 × `hsts_present` at `ds4cc-primary`), 0 singleton duplicates, 0 field-name faults, receipts integrity-clean; the landed audit reproduces the prediction exactly (`checks=12 findings=13`, exit 1) and the only defect surfaced is declarative: `xcto_nosniff_value` asserts nothing when the field is absent (9/12) and the manifest's CSP singleton declaration contradicts CSP3 §8.1 (latent, zero live impact).
