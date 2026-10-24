# Round 22 · w1 · PythonURL — urllib.parse: `urljoin` safety warning and `urlsplit` non-validation

Seat: KakeR22.PythonURL (scout, leaf). Read-only apart from this file. No registry edits, no lane scripts run, no tests, no commits, no installs. Target content was treated as data only.

## Source and access

| Field | Value |
|---|---|
| URL (stable alias) | `https://docs.python.org/3/library/urllib.parse.html` |
| URL (versioned, fetched and verified) | `https://docs.python.org/3.15/library/urllib.parse.html`; `https://docs.python.org/3.14/library/urllib.parse.html` |
| Access date | 2026-10-20 |
| Page-declared version | 3.15 page title: `Python 3.15.0 documentation`; 3.14 page title: `Python 3.14.8 documentation`; both HTTP 200 |
| `/3/` alias behavior | Serves the 3.15 page today (effective URL stays `/3/library/urllib.parse.html`, title 3.15.0) — a moving pointer, not a pinned version |
| Sections read | `#urllib.parse.urlsplit` (Warning), `#urllib.parse.urljoin` (Note and Warning), `#url-parsing-security` |
| Host interpreter observed | `python3 --version` → `Python 3.14.8` (matches the 3.14 docs page) |

## Exact quotes (≤25 words each, located)

| # | Location | Exact quote | Words |
|---|---|---|---|
| Q1 | `#urllib.parse.urlsplit`, Warning admonition | "urlsplit() does not perform validation. See URL parsing security for details." | 11 |
| Q2 | `#urllib.parse.urljoin`, Warning admonition | "Because an absolute URL may be passed as the url parameter, it is generally not secure to use urljoin with an attacker-controlled url." | 23 |
| Q3 | `#url-parsing-security`, first paragraph | "The urlsplit() and urlparse() APIs do not perform validation of inputs. They may not raise errors on inputs that other applications consider invalid." | 23 |
| Q4 | `#urllib.parse.urljoin`, Note | "If url is an absolute URL (that is, it starts with // or scheme://), the url’s hostname and/or scheme will be present in the result." | 25 |
| Q5 | `#url-parsing-security`, third paragraph | "These functions incorporate some aspects of both, but cannot be claimed compliant with either." | 14 |
| Q6 | `#url-parsing-security`, second paragraph | "We recommend that users of these APIs where the values may be used anywhere with security implications code defensively." | 19 |

Quote verification: each string was extracted from the rendered HTML of both the 3.14.8 and 3.15 pages; all six are byte-identical across the two versions. The only divergence in the surrounding text is that 3.15 inserts "(depending on the value of the *missing_as_none* argument)" after "empty strings", tied to the 3.15-only `missing_as_none` parameter. Neither warning text depends on that parameter.

## Scoped teaches (observed on the page)

1. **`urlsplit()`/`urlparse()` are parsers, not validators.** The page says so twice, once as a per-function Warning (Q1) and once as the opening of the dedicated security section (Q3). It adds that they "may also succeed on some inputs that might not be considered URLs elsewhere", that they "may instead return some component parts as empty strings or None", and that "components may contain more than perhaps they should".
2. **Defensive verification is explicitly the caller's job** (Q6): check that the returned `scheme`, `hostname` and `path` make sense before trusting them.
3. **`urljoin` is unsafe with attacker-controlled input** (Q2), because an absolute or scheme-relative `url` keeps its own host/scheme (Q4). `urljoin(base, "//host/x")` therefore escapes the base host; `urljoin("https://website.com/users/", username)` may return the attacker's absolute URL.
4. **No standards-compliance claim**: the functions mix WHATWG and RFC 3986 behavior and "cannot be claimed compliant with either" (Q5); "What constitutes a URL is not universally well defined."
5. **Documented `ValueError` triggers in `urlsplit`** (not a rejection mechanism for arbitrary invalid input): reading `.port` when the port is invalid; out-of-range ports raise since 3.6; unmatched square brackets in `netloc`; and characters in `netloc` that decompose under NFKC normalization into `/`, `?`, `#`, `@`, or `:` (since 3.8).
6. **Documented silent normalizations that change the string**: leading C0 control and space characters are stripped (3.12+); `\n`, `\r` and tab are removed at any position (3.10+); percent-encoded sequences are **not** decoded; `geturl()` may lowercase the scheme and drop empty components, so a rebuild "may result in a slightly different, but equivalent URL" (also stated for `urlunsplit`/`urlunparse`).
7. **`urlsplit()` should generally be used instead of `urlparse()`**; `urlparse` splits `params` per obsoleted RFC 1738/1808.
8. **`urljoin` semantics follow RFC 3986 since 3.5**, but the docs do not enumerate edge-case behaviors.

## What this supports for claim C1, and what it does not

Supported (source-grounded constraints on `scripts/canonical_audit.py`):

- **`invalid_url` must be rejected by explicit policy, not by trusting an exception.** `urlsplit` "does not perform validation" (Q1, Q3); a validator that only calls `urlsplit` and assumes a raise on bad input will false-green. Scheme allowlist (`http`/`https`), non-empty `hostname`, userinfo rejection, control-character rejection and port handling must be coded explicitly. [INFERENCE: mapping the page's warning to the contract's policy rules; the page itself prescribes no specific allowlist.]
- **`scheme_relative` / `wrong_host` share the escape mechanism** in Q4: a `//host/path` canonical href resolves with the base scheme but the *href's* host. A comparison that checks only path/query will accept a cross-origin canonical. Compare resolved `scheme` + `hostname` against the page URL from the manifest, then path/query. [INFERENCE: the page states the resolution behavior; the same-origin rule comes from the contract, not this source.]
- **Compare on components, not on `geturl()` text.** The page documents scheme lowercasing and empty-component dropping, so string equality of `geturl()` versus `expectedCanonical` can disagree for equivalent URLs. [INFERENCE: which normalization the validator should apply is a policy decision; the page only documents what the API does.]
- **Keep the raw href and parsed components distinct around percent-encoding**, since percent sequences are not decoded; whether `%2F` counts as `/` is a contract decision the API will not make.

Not supported by this source:

- It cannot establish what a canonical URL *is*, whether `rel=canonical` is head-only, or how search engines select canonicals. Those are HTML/RFC 6596/search documentation questions.
- It does not say which malformed inputs `urlsplit` accepts, beyond the examples above. Silence here is not evidence that an input is rejected.

## Limitations

- CPython **implementation documentation**, not a URL standard; it explicitly disclaims compliance with WHATWG and RFC 3986 (Q5). It can source "what the stdlib does and does not guarantee", not canonical-policy semantics.
- `/3/` is a moving alias; behavior text is stable across 3.14.8 and 3.15 for everything cited, but a future version can change it. The page lists changes in 3.2, 3.3, 3.5, 3.6, 3.8, 3.10, 3.12 and 3.15.
- No interpreter experiment was run (no probes of `urlsplit`/`urljoin` against the 32 fixtures). Whether a given fixture's href is accepted or raises is an observable for the Matrix/Measure runs, not a fact this report can claim.
- The docs give no exhaustive list of accepted-invalid inputs and no same-origin or canonicalization guarantee; the security section's advice is generic.
- Access was a single-day read of the rendered official pages; no mirror or cached copy was used.

## Source status recommendation (for L1; this seat edited nothing)

- **Register it**: official first-party documentation for the CPython API the validator will use.
- **kind**: `docs` (registry vocabulary: `code`, `docs`, `dataset`, `spec`, `own-work`, `community`). **tier**: `A`, scoped to "CPython `urllib.parse` parsing, resolution and its explicit non-validation/non-security warnings; **not** canonical URL semantics".
- **Suggested teaches line**: "`urlsplit`/`urlparse` do not validate, and `urljoin` is unsafe with attacker-controlled input because absolute or scheme-relative URLs keep their host."
- **status**: `mined` once a knowledge entry cites it (candidate consumer: `corpus/knowledge/static-canonical-preflight.md`); otherwise `queued`. `opened` 2026-10-20; `recheck` 365d (stdlib doc drift is release-paced).
- **id**: next free at registration (S019 is the current maximum at read time; S020 would be next).
- **Anchor**: cite the versioned page matching the measured interpreter (currently `https://docs.python.org/3.14/library/urllib.parse.html`) plus `#urllib.parse.urljoin`, `#urllib.parse.urlsplit`, `#url-parsing-security`; keep the `/3/` alias only as a convenience pointer.
- **Do not** let any C1 policy claim cite this row as authority for canonical semantics; it supports the *validation-gap* and *resolution-escape* premises only.

## Checks for the integrator (run once, after integration; not run here)

1. Record `python3 --version` in the measurement output and confirm the cited docs page matches it; 3.14 vs 3.15 differ only by `missing_as_none` in the quoted region, but future versions may differ more.
2. Confirm the policy implementation does not rely on `urlsplit` raising for `invalid_url`; the finding must come from explicit checks.
3. Confirm the `scheme_relative`/`wrong_host` comparison includes scheme and hostname, not just path.
4. Do not cite this report as evidence that any fixture passes; only the matrix run can show that.

## Changes and tooling

- Files changed: this report only, `.ufo/waves/round-22/w1/PythonURL.md`.
- Registry: no edit (`corpus/SOURCES.md` untouched); no lane scripts, lessons, knowledge entries or verifier/aggregator bytes touched.
- Tool installs or upgrades: none. Reads used the existing `read`/`curl`/`python3`; no package transactions, no services, no credentials.
