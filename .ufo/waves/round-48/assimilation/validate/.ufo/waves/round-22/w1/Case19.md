# Case19 — `invalid_url`: exact fixture, expected classification, and one adjacent false-green

Seat: `KakeR22.Case19` (scout, leaf). Read-only apart from this report: no lane tests, no scripts run, no
registry/lesson/verifier edits, no commits, no installs. Lane base observed in the live lane:
`7c61c8cc791bde36dd5e3688bdfea2678d90146c` (matches contract). Target pages were treated as data only.

## Scoped answer (one line)

A canonical `href` that fails WHATWG URL parsing (special scheme with no host) is a **policy** failure:
**exit 1**, finding **`canonical_url_invalid`**, one page checked, one finding. The sharpest fixture is
`href="https://"` because Python's `urljoin` silently resolves it to the document URL; a resolve-first
validator therefore returns *clean 0* — a false green this case exists to kill.

## Frozen fixture (recommended)

Manifest (path/layout as Matrix chooses; `file` is relative to the manifest directory):

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "invalid_url.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

HTML file (regular file, UTF-8, explicit `<head>`, exactly one canonical link, no `<base>`, no decoys):

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>invalid URL</title>
<link rel="canonical" href="https://">
</head>
<body><p>invalid_url</p></body>
</html>
```

| Field | Value |
|---|---|
| page `url` | `https://example.test/project/a.html` |
| `expectedCanonical` | `https://example.test/project/a.html` |
| canonical `href` | `https://` (empty authority; special scheme, no host) |
| expected exit | **1** (failed policy) |
| expected finding id | **`canonical_url_invalid`** |
| `pagesChecked` | `1` |
| findings | exactly one: `{"id": "canonical_url_invalid", "page": "https://example.test/project/a.html"}` |
| stdout shape | `{"verdict": "...", "pagesChecked": 1, "findings": [...]}`; the literal `verdict` string is not frozen by the contract — see Inference |

**Why `expectedCanonical` is the page's own URL.** It is already a normalized HTTP(S) absolute URL, so the
manifest is a clean positive control for every other field. It is also the most adversarial choice: a
validator that resolves first (`urljoin(document_url, "https://")`) gets the document URL back and then
compares equal, yielding the worst outcome (exit 0 clean) rather than merely the wrong finding id.

## Why the classification is exit 1 / `canonical_url_invalid`

1. **The href is not a URL at all under the frozen policy's model.** The contract requires resolving the
   href and comparing a "WHATWG-like HTTP(S) normalized absolute URL". WHATWG URL parsing fails for
   `https://`: for a special scheme, an empty host is `host-missing` and the parser returns failure.
   - WHATWG URL Standard §1.1, error table row `host-missing` (anchor `#host-missing`):
     > "The input has a special scheme, but does not contain a host."
   - WHATWG URL Standard §4.4, host state (anchor `#host-state`):
     > "If url is special and buffer is the empty string, host-missing validation error, return failure."
   - Corroborated by a compliant implementation: Node `v24.21.0` `new URL("https://")` throws
     `ERR_INVALID_URL` (observed; see table below).
2. **HTML also marks the attribute non-conforming.** WHATWG HTML §4.2.4 "The link element"
   (`#the-link-element`) says:
   > "If the href attribute is present, then its value must be a valid non-empty URL potentially surrounded by spaces."
   `https://` is present but not a valid URL. §4.6.8.4 (`#link-type-canonical`) says the keyword identifies
   "the preferred URL for the current document"; with no parseable URL there is no canonical target.
3. **Exit 1, not 2.** The page is readable, the manifest is schema-valid, and the document has an explicit
   head with exactly one canonical link. Every condition needed to *evaluate* the page holds; the defect is
   inside the evaluated markup. The contract reserves exit 2 for "could-not-evaluate input/unsupported
   shape", served by the separate ids `input_invalid` (manifest/file/traversal/symlink problems) and
   `html_unsupported` (document shape the static parser refuses). `canonical_url_invalid` is one of the
   policy finding ids, alongside `canonical_mismatch`/`canonical_fragment`, which are exit-1 class.
4. **Why not `canonical_mismatch`.** There is no valid resolved absolute URL to compare. A mismatch finding
   asserts two comparable URLs differ; here the declaration itself is unusable. The contract provides a
   dedicated id for this state, so emit `canonical_url_invalid` and do not degrade it to a comparison.
5. **Why not `canonical_href_missing`.** The attribute is present and non-empty as a string. (The empty
   string `href=""` is a different matrix case, `href_empty`, and under URL parsing it resolves to the
   document URL; do not merge the two cases.)
6. **Why not `canonical_fragment` / `base_url_invalid` / `canonical_multiple`.** No `#` component, no
   `<base>`, and exactly one canonical link element. One defect → one finding (recommended exactly one).
   The spec's own `host-missing` example `https://#fragment` is deliberately not used as this fixture: the
   `#` would add a second, competing policy dimension (`canonical_fragment`), making the expected id depend
   on a precedence rule the contract does not state. `https://` isolates the URL-validity defect.

## Implementation obligations this fixture tests (anti-false-green)

1. **Validate the raw href before resolving it, or validate the href's own authority.** Do not let
   resolution absorb an unparseable absolute reference. Observed on the host interpreter (Python 3.14.8):
   `urljoin("https://example.test/project/a.html", "https://")` returns
   `"https://example.test/project/a.html"` — exactly `expectedCanonical`. A resolve-then-compare validator
   returns clean 0. This is the primary cheat this fixture detects.
2. **Never rely on `urlsplit` raising.** `urlsplit("https://")` returns
   `SplitResult(scheme="https", netloc="", path="", query="", fragment="")` with `hostname is None`; it
   does not raise. The CPython documentation is explicit:
   - `#urllib.parse.urlsplit` Warning: "urlsplit() does not perform validation."
   - `#url-parsing-security`: "The urlsplit() and urlparse() APIs do not perform validation of inputs."
   The invalid verdict must come from explicit checks, not exception handling.
3. **Explicit validity predicate for this class:** scheme ASCII-case-insensitively `http` or `https`;
   non-empty host (reject `hostname is None` or `""`); optional port within 0–65535 (reject
   port-out-of-range / non-numeric); no credentials (non-empty username or password); no fragment; host
   free of forbidden host code points. Note that `urlsplit` defers port validation to the `.port`
   accessor: `urlsplit("https://example.test:99999/")` itself succeeds, and only reading `.port` raises;
   a predicate that never reads `.port` accepts the bad port. WHATWG URL §3.2
   (`#forbidden-host-code-point`) includes
   U+0020 SPACE, `#`, `/`, `:`, `<`, `>`, `?`, `@`, `[`, `\`, `]`, `^`, `|` and C0 controls; a space-bearing
   host such as `https://exa mple.test/a` is a parse failure (Node also rejects it), even though Python's
   `urlsplit` accepts it.
4. **Do not confuse this case with `https:///path`.** WHATWG parses `https:///path` against a base as host
   `path` (`https://path/`, observed Node v24.21.0), while Python's `urlsplit`/`urljoin` produce an empty
   authority and a base-relative path. `https:///path` is therefore a poor `invalid_url` fixture: the
   contract says "WHATWG-like", and a compliant parser does not call it invalid. Use `https://` or a
   forbidden-code-point/port form instead.
5. **Do not build `invalid_url` from a bare relative token such as `not a url`.** WHATWG resolves it to
   `https://example.test/project/not%20a%20url` (observed Node), a valid absolute URL; the correct finding
   would be `canonical_mismatch`, not `canonical_url_invalid`. This is the main fixture-construction trap
   for the Matrix seat.
6. **Keep expected-URL validation separate.** If `expectedCanonical` itself is not a valid HTTP(S) URL,
   that is manifest input error (`input_invalid`, exit 2), not `canonical_url_invalid` (which describes the
   page's declaration). This fixture's `expectedCanonical` is valid by construction.
7. **No HTMLParser edge applies here.** No comments, raw-text (`script`/`style`), template descendants,
   entities, attribute casing, or `<base>` are involved; the link is a plain start tag in the explicit head.
   The failure is entirely in URL validity.

## Adjacent false-green attack (distinct from `invalid_url`)

**Name:** `userinfo_credentials_match`.

```html
<!doctype html>
<html><head>
<link rel="canonical" href="https://user:pass@example.test/project/a.html">
</head><body><p>credentials attack</p></body></html>
```

| Field | Value |
|---|---|
| page `url` | `https://example.test/project/a.html` |
| `expectedCanonical` | `https://example.test/project/a.html` |
| canonical `href` | `https://user:pass@example.test/project/a.html` |
| expected exit / id | **1 / `canonical_url_invalid`** (id choice [INFERENCE]: no dedicated credentials id exists) |
| expected finding page | `https://example.test/project/a.html` |

**Why it should fail.** The contract's policy sentence explicitly says "reject fragments and credentials".
WHATWG URL §4.2 (`#include-credentials`) defines the predicate:

> "A URL includes credentials if its username or password is not the empty string."

The error table (§1.1, `#invalid-credentials`) lists "The input includes credentials" as a validation error,
but — unlike `host-missing`, `port-out-of-range`, `port-invalid` — it is **not** a parser failure: the URL
still parses. There is no dedicated credentials finding id in the frozen contract, so credentials fold into
`canonical_url_invalid`.

**False-green mechanism.** `urlsplit` exposes `hostname="example.test"`, `path="/project/a.html"`,
`query=""`, and `username="user"`, `password="pass"`. A validator that compares
`(scheme, hostname.lower(), port, path, query)` — or that serializes `scheme://host/path?query` — silently
drops userinfo and finds exact equality → exit 0 clean. WHATWG's own origin also strips userinfo: Node
`new URL("https://user:pass@example.test/project/a.html").origin` is `https://example.test` (observed), so
an origin-based comparison greens it too. This attack specifically punishes passing `invalid_url` by a
"did the parser throw?" shortcut plus a hostname-based comparator.

**Why it is distinct from `invalid_url`.** The URL parses successfully; scheme, host, port, path and query
all match `expectedCanonical`; there is no fragment, no wrong host/path/query, and no non-HTTP scheme. Only
the forbidden userinfo component differs. It is not covered by any of the 32 case names, so it is a genuine
adjacent attack rather than a duplicate of `wrong_host`, `fragment_url`, `javascript_url` or `data_url`.

**Boundary that must not over-reject.** WHATWG treats empty userinfo as *no* credentials: both
`https://@example.test/project/a.html` and `https://:@example.test/project/a.html` serialize to
`https://example.test/project/a.html` with `username=""` (observed Node), and §4.2 requires the username or
password to be non-empty. A validator that rejects any `@` in the netloc would false-red those forms. The
predicate must be "non-empty parsed username or password", not "`'@' in netloc`".

## Sources (official, fetched 2026-10-20 UTC)

| # | URL | Section / anchor | Exact located quote |
|---|---|---|---|
| S1 | https://url.spec.whatwg.org/ | §1.1 Writing, `#host-missing` | "The input has a special scheme, but does not contain a host." |
| S2 | https://url.spec.whatwg.org/ | §4.4 URL parsing, host state, `#host-state` | "If url is special and buffer is the empty string, host-missing validation error, return failure." |
| S3 | https://url.spec.whatwg.org/ | §1.1 Writing, `#invalid-credentials` | "The input includes credentials." |
| S4 | https://url.spec.whatwg.org/ | §4.2 URL miscellaneous, `#include-credentials` | "A URL includes credentials if its username or password is not the empty string." |
| S5 | https://url.spec.whatwg.org/ | §3.2 Host miscellaneous, `#forbidden-host-code-point` | excerpt: "A forbidden host code point is U+0000 NULL, … U+0020 SPACE, U+0023 (#), U+002F (/), U+003A (:), … U+007C (\|)." |
| S6 | https://url.spec.whatwg.org/ | §1.1 Writing, `#port-out-of-range` | "The input's port is too big." (row marked as parser failure) |
| S7 | https://html.spec.whatwg.org/multipage/semantics.html | §4.2.4 The link element, `#the-link-element` | "If the href attribute is present, then its value must be a valid non-empty URL potentially surrounded by spaces." |
| S8 | https://html.spec.whatwg.org/multipage/links.html | §4.6.8.4 Link type "canonical", `#link-type-canonical` | "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." |
| S9 | https://docs.python.org/3.14/library/urllib.parse.html | `#urllib.parse.urlsplit` Warning | "urlsplit() does not perform validation." |
| S10 | https://docs.python.org/3.14/library/urllib.parse.html | `#url-parsing-security` | "The urlsplit() and urlparse() APIs do not perform validation of inputs." |

Scratch copies used for extraction: `/tmp/urlspec.html`, `/tmp/semantics.html`, `/tmp/links.html`,
`/tmp/pyurl.html`. Quotes S1–S8 are normative spec text; S9–S10 are CPython implementation documentation,
not URL-standard authority.

## Observed local parser behavior (evidence, not spec)

Host: Python `3.14.8`, Node `v24.21.0`. Base for all relative probes:
`https://example.test/project/a.html`.

| Input | Python `urlsplit` | Python `urljoin(base, input)` | Node `new URL(input, base)` |
|---|---|---|---|
| `https://` | OK, `scheme=https`, `netloc=""`, `hostname=None` | **base URL** (false-green vector) | throws `ERR_INVALID_URL` |
| `https://:443` | OK, `netloc=":443"`, `hostname=None` | unchanged | throws `ERR_INVALID_URL` |
| `https://example.test:70000/` | OK at split; `.port` raises `ValueError: Port out of range 0-65535` | unchanged | throws `ERR_INVALID_URL` |
| `https://example.test:abc/` | OK at split; `.port` raises `ValueError: Port could not be cast to integer value as 'abc'` | unchanged | throws `ERR_INVALID_URL` |
| `https://exa mple.test/a` | OK, hostname `exa mple.test` | unchanged | throws `ERR_INVALID_URL` |
| `https:///path` | OK, `netloc=""`, path `/path` | `https://example.test/path` | **OK, `https://path/`** (host `path`) |
| `https://user:pass@example.test/project/a.html` | OK, `username="user"`, `password="pass"`, `hostname="example.test"` | unchanged | OK; `origin=https://example.test` |
| `https://@example.test/project/a.html` | OK, `username=""`, netloc `@example.test` | unchanged | OK, serializes `https://example.test/project/a.html` |
| `not a url` | OK, relative | `https://example.test/project/not a url` | `https://example.test/project/not%20a%20url` |

Consequences: (a) `https://` is the strongest `invalid_url` fixture because the stdlib resolution path
yields the expected URL; (b) `https:///path` and `not a url` are unsuitable fixtures for this case;
(c) credentials are invisible to host/origin comparisons; (d) `urlsplit` accepts space-bearing hosts that
WHATWG rejects.

## Inference and limits (explicit)

- **[INFERENCE]** The contract does not freeze the literal `verdict` string (`"failed"` is only the natural
  spelling). The Matrix seat should assert exit code, `pagesChecked`, and the finding `id`/`page` first; a
  literal verdict assertion should be added only after the implementation freezes its spelling.
- **[INFERENCE]** Mapping credentials to `canonical_url_invalid` follows from the absence of any other
  credential id in `findingIds`; it is the only policy id that can carry a URL-validity rejection.
- **[INFERENCE]** Exit-2 boundaries (`input_invalid`, `html_unsupported`) are read from the contract's
  `exitMap` wording; this case is on the evaluable/policy side.
- **"WHATWG-like" grants latitude** on normalization details (default-port elision, trailing-dot hosts,
  percent-encoding, IDNA). This case deliberately avoids that latitude: empty-host parse failure is explicit
  in WHATWG §4.4 (`host-missing`, return failure). RFC 3986's generic grammar alone is more permissive about
  an empty `reg-name`, so do not use RFC 3986 as an alternate oracle for this fixture. Do not widen the
  fixture into normalization-equivalence questions here.
- The Matrix seat's own `invalid_url` fixture may differ in bytes. The rule that must converge:
  **href present + non-empty + cannot yield a valid absolute HTTP(S) URL → exit 1 / `canonical_url_invalid`**.
  Preferred bytes are `https://`; avoid `not a url` (valid relative reference) and `https:///path`
  (WHATWG parses host `path`).
- No tests or matrix runs were performed by this seat; the only executions were read-only probes of
  Python/Node URL APIs and documentation fetches.

## Checks for L1 (run once, after integration; not run here)

1. Confirm `.ufo/waves/round-22/cases.json` gives `invalid_url` expected exit **1** and finding
   **`canonical_url_invalid`**, and that its fixture href is a WHATWG parse-failure form (ideally `https://`).
2. Confirm `scripts/canonical_audit.py` does not resolve before validating: run the `invalid_url` manifest
   and verify it is not clean. If it returns 0, the `urljoin` absorption described above is present.
3. Confirm credentials are rejected only when parsed username/password is non-empty (test both
   `https://user@…` and the empty-userinfo `https://@…` boundary).
4. Confirm normal mode performs no network access and no writes, and that a bad `expectedCanonical`
   yields exit 2 / `input_invalid` rather than `canonical_url_invalid`.
5. Re-run `measure.py` against the integrated revision; this report supplies no measurement.

## Tooling / changes

- Files changed: this report only (`.ufo/waves/round-22/w1/Case19.md`).
- Installs/upgrades: none (no package transactions; no services; no credentials).
- Registry/lesson/knowledge/verifier bytes: untouched.
