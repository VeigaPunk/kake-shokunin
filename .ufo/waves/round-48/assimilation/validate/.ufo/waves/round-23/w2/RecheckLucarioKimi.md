# W2 falsify — C2 surface `lucario-kimi` (RecheckLucarioKimi)

Scope: one surface, frozen revision `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`.
Scratch: `/tmp/kake-r23w2-LucarioKimi-k6Rv` (fresh GET body + headers only).

## Verdict

**No counterexample found.** The committed not-served receipt reproduces exactly: fresh
GET is byte-identical to the committed snapshot, the counter accepts the surface
(`pass: true, verdict: "not-served"`; 12/12 overall), and the served/not-served
classification is forced by the frozen policy, not a judgment call. Attacks on the
`expectedCanonical` choice and on the classification produce only P3 documentation and
verification-strength findings; none can flip any pass/fail.

## Findings

### P3-1 — `expectedCanonical` premise ("mirror declares its primary") is evidenced by nothing, and is never exercised

- Population entry (at revision): `id=lucario-kimi`, `url=https://lucario.kimi.page/`,
  `expectedCanonical=https://veigapunk.github.io/lucario/`,
  `policyBasis="mirror declares its primary (map: never published, expected not served)"`.
- No artifact shows the mirror declaring any canonical: the slot 404s, and the 404 body
  contains no `<link rel="canonical">`, no `og:url`, no refresh, and no occurrence of
  `lucario`/`veigapunk` at all (grep over the fresh body: 0 matches). The primary's own
  audit contradicts the premise: `live/lucario-ghp/audit.json` finding is
  `canonical_missing` — the primary declares no canonical either.
- Impact: zero on the count. `measure_c2.py` runs the validator only on the `served`
  branch; for a not-served surface `expectedCanonical` is dead data. The choice is
  counterfactual decoration.
- Smallest fix: reword `policyBasis` to state the choice is unexercised while the slot is
  unserved (e.g. "expected canonical if ever published; unexercised while not served"), or
  cite the GHP row's `property map: lucario GHP is canonical` as the sole basis.

### P3-2 — `policyBasis` cites "never published", wording the lane's own receipts mark UNVERIFIABLE

- `receipts/property-map.json` c35: anchor `…404, **never published**`, claim "The
  historical assertion that this slot was never published is not established by a single
  current 404", verdict `UNVERIFIABLE`. The verifiable half of the basis (expected not
  served → 404 today) is c34, verdict `HOLD`.
- Impact: none on measurement (the counter never parses `policyBasis`), but the population
  row leans on a historical claim the same wave classifies as unverifiable.
- Smallest fix: anchor the row's basis to c34 (current 404, HOLD) and drop or qualify the
  "never published" history.

### P3-3 — not-served branch of `measure_c2.py` leaves `fetch.sha256` and receipt extras unchecked

- Docstring requires fetch.json to carry "a sha256 of the stored body", but for a
  not-served surface no body is stored and `check()` verifies `fetch["sha256"]` against
  nothing; likewise receipt keys beyond `verdict`/`status` are unconstrained (this
  receipt's `error: null, exit: null` pass unexamined; arbitrary junk extras would too).
- Impact: none here — I corroborated the digest externally (fresh GET sha256 equals
  `93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966`), and the extras are
  benign. This is verification-strength, not a defect in this receipt.
- Smallest fix: document `sha256` as informational for not-served surfaces, and either pin
  the allowed receipt key set or ignore extras explicitly.

## Checked and held

1. **Fresh GET vs committed fetch.json — all four axes identical, zero drift.**
   Command: `curl -sS -L --max-time 60 -o /tmp/kake-r23w2-LucarioKimi-k6Rv/body.html -D
   /tmp/kake-r23w2-LucarioKimi-k6Rv/headers.txt -w
   'status=%{http_code}\nfinalUrl=%{url_effective}\ncontentType=%{content_type}\nsize=%{size_download}\nnumRedirects=%{num_redirects}\n'
   https://lucario.kimi.page/ && sha256sum /tmp/kake-r23w2-LucarioKimi-k6Rv/body.html`
   Output: `status=404`, `finalUrl=https://lucario.kimi.page/`,
   `contentType=text/html; charset=utf-8`, `size=13409`, `numRedirects=0`,
   `93ddca9a021664d562e698eb99d52b84d696f81485847dcfeaf6f4a5c8fca966`. Committed fetch.json
   matches on every field (`bytes: 13409`, same sha256, same finalUrl, `redirects: []`,
   `fetchedAt: 2026-10-21T06:33:17Z`, `truncated: false`, `error: null`). Raw status line
   `HTTP/2 404`, `server: cloudflare`, `cf-cache-status: DYNAMIC`.
2. **By-eye derivation (assignment's page.html-head step does not apply here).** There is
   no committed `page.html` — `git -C <lane> show
   5e5afb9e…:.ufo/waves/round-23/live/lucario-kimi/page.html` →
   `fatal: path … does not exist in '5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd'`, and the
   working-tree directory holds only `audit.json` + `fetch.json`. Deriving from the
   committed fetch head instead: status 404 fails the policy's `served()` (requires 2xx),
   so the policy implies **not-served**; the absence of `page.html` is that verdict's
   required consequence, and it holds.
3. **Receipt classification attack — fails.** `{"error": null, "exit": null, "status":
   404, "verdict": "not-served"}`: the receipt's status equals fetch.status (404); verdict
   matches the not-2xx branch. `text/html` content type does not make it "served" — the
   frozen policy requires 2xx AND text/html. The served classification was considered and
   rejected upstream: `w1/SurfaceLucarioKimi.md` records an out-of-band validator run on
   the same 404 body yielding `failed-policy`/`canonical_missing`, exit 1 — correctly not
   committed as the receipt. A current fresh 404 (cloudflare, no redirect) confirms the
   receipt is not a transient blip.
4. **Counter reproduction.** `python3 …/.ufo/waves/round-23/measure_c2.py --root
   /home/vgpnk/Projects/shokunin/kake-shokunin --revision
   5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd` → `"accepted": 12, "total": 12`; the
   `lucario-kimi` row: `{"id": "lucario-kimi", "pass": true, "problems": [], "verdict":
   "not-served"}`; `validatorSha256 062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387`.
   The frozen population digest self-check passed (a mismatch would exit 2 before any row).

## Limits

- One GET, 2026-10-21T07:36:23Z UTC; the endpoint can drift after it. Today it had not.
- The historical "never published" claim stays unverifiable (no Kimi publication-history
  source; local `~/Projects/lucario` absent per wave-1) — out of my scope; only the
  current-state half is testable and it holds.
- Read-only lane: I wrote only this report; the GET was the single network call
  (read-only, no redirects followed — `numRedirects=0`).
- No tools installed or upgraded (none needed).
