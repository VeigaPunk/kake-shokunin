# Case21 — matrix case `data_url`

Scout, read-only. Base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Anchors: `.ufo/waves/round-22/contract.json:4` (interface/policy/findingIds/
exitMap) and `:5` (`matrixCases`; `data_url` is the 21st name, 1-based).
No validator, fixture set or `measure.py` exists at this base — the only
files under `scripts/` are `corpus-contract.mjs`, `freshness-sweep.mjs`,
`probe-delta.mjs`. Everything below is a case specification for L1, not a
test result.

## 1. Concrete fixture (byte-pinned)

Case dir contents (paths relative to the case dir; `measure.py` may inline
these bytes, but the sha256 must match so selftest and matrix cannot drift):

`data_url.html` — 182 bytes, sha256 `743065f2d9f6ac9c869ec4eaeb57f751370b336c595559e27562b0cea9684cfe`

```html
<!doctype html>
<html><head><meta charset="utf-8"><link rel="canonical" href="data:text/plain,https://example.test/project/a.html"></head><body><p>data_url fixture</p></body></html>
```

(trailing newline after the second line.)

`manifest.json` — 197 bytes, sha256 `10f85290fe86641b00a52b6223ad07a0f66c4a406ab84a62fe7390b0f919c950`

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "data_url.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

Materialisation consistent with sibling cases (`Case02.md:27`,
`Case16.md:31`): place the pair at `fixtures/data_url/manifest.json` +
`fixtures/data_url/data_url.html`; the manifest `file` stays the
manifest-relative `data_url.html`, so resolution is unchanged.

Invocation under test:
`python3 scripts/canonical_audit.py --manifest <case>/manifest.json --json`

## 2. Expected classification

| field | value |
|---|---|
| exit | `1` (failed policy) |
| findings | exactly one: `{"id": "canonical_url_invalid", "page": "https://example.test/project/a.html"}` |
| pagesChecked | `1` |
| clean? | no |

Illustrative stdout (key literals other than the finding id are not pinned by
the contract; see §8):

```json
{"verdict":"failed","pagesChecked":1,"findings":[{"id":"canonical_url_invalid","page":"https://example.test/project/a.html"}]}
```

`page` is the manifest `url`, not the file name (`page` must be identical for
this case and `absolute_match`; only the href differs). Sibling case reports
use the same field value (`Case08.md:111`, `Case16.md:71`).

## 3. Why this is the answer

1. **Structural checks all pass.** One `<link>` element, inside the explicit
   `<head>`, `rel` token list = `[canonical]`, `href` attribute present and
   non-empty. So none of `canonical_missing`, `canonical_multiple`,
   `canonical_outside_head`, `canonical_href_missing` applies.
2. **Resolution succeeds as identity.** The href is already an absolute URL
   with a scheme, so `urljoin(document, href)` returns the href unchanged
   (observed, §7). A `data:` URL has no relative forms — RFC 2397 §2: "The
   'data' URL scheme has no relative URL forms." It is a well-formed data URL
   (`dataurl := "data:" [ mediatype ] [ ";base64" ] "," data`, RFC 2397 §3;
   omitted mediatype defaults to `text/plain;charset=US-ASCII`). So this is
   **not** `invalid_url` (parser failure) and **not** `html_unsupported`: the
   document parses and the URL parses.
3. **The target is inadmissible for the declared policy.** Contract policy
   requires "WHATWG-like HTTP(S) normalized absolute URL". `data` is not a
   special scheme — WHATWG URL Standard: special schemes are `ftp`, `file`,
   `http`, `https`, `ws`, `wss`; "A URL is special if its scheme is a special
   scheme. A URL is not special if its scheme is not a special scheme." A
   `data:` URL also carries an opaque path ("A URL has an opaque path if its
   path is a URL path segment"; "A URL path that is a URL path segment is
   opaque and can contain U+002F (/)") and therefore cannot serve as a base
   URL ("...the base URL cannot be used as a base URL because it has an
   opaque path", missing-scheme-non-relative-URL row). It cannot name a
   published, consolidatable resource at all. Only `canonical_url_invalid`
   fits, and the contract has no scheme-specific finding id.
4. **Exit 1, not 2.** The page was fully evaluated: link counted, rel
   matched, href resolved, target classified. Exit 2 is contracted as
   "could-not-evaluate input/unsupported shape" and is the bucket for
   `input_invalid`/`html_unsupported` (missing/unreadable file, malformed
   manifest, non-HTML document). A declared signal that violates policy is
   exit 1. The same logic fixes `javascript_url` at exit 1. `base_invalid` is
   not assigned an exit by the contract; peer review puts it at exit 2 only
   when the invalid base makes resolution impossible (`StdoutExit.md`), so
   this seat does not claim it.
5. **Honesty about the authority.** RFC 6596 §3 permits a target with
   "different scheme names, such as \"http\" to \"https\" or \"gopher\" to
   \"ftp\"", so the HTTP(S)-only restriction is a **stricter local policy**
   (contract policy line; `corpus/QUALITY.md` "Source recommendations are
   distinguished from stricter local policy"), not an RFC requirement and
   not a Google requirement. RFC 6596 §3 does require the target to "identify
   content that is either duplicative or a superset of the content at the
   context (referring) IRI", which a self-contained payload URL cannot
   establish offline.

## 4. What the fixture is deliberately shaped to catch

The document URL and `expectedCanonical` are **equal**, and the data payload
literally contains that expected URL. `data_url` is therefore the negative
twin of `absolute_match`: any implementation that passes one and fails the
other must be keying on the href, and several plausible shortcut shapes go
green here:

| implementation shortcut | observed/derived outcome | why it is wrong |
|---|---|---|
| filter links by `scheme in {http,https}` while collecting, emit no finding for skipped links | one link collected, 0 findings → **exit 0** | silent skip turns a policy violation into a clean page; the page has a declared canonical |
| `if expectedCanonical in href:` substring test | `True` (payload contains it) → **exit 0** | substring is not URL identity |
| on unusable canonical, fall back to document URL ("self") | resolved = document URL = expected → **exit 0** | the declared signal is unusable; a fallback invents a signal |
| percent-decode the href, then compare components | payload variant can reconstruct the expected URL → **exit 0** | the payload is opaque data, not a reference |
| `urljoin` + full-string compare, or `(scheme, hostname, port, path, query)` compare | exit 1 with `canonical_mismatch` | red, but wrong id — measure.py's id assertion must fail it |
| treat non-HTTP(S) as "unsupported shape" | exit 2 with `canonical_url_invalid` | right id, wrong exit |
| classify the link as absent when its scheme is unsupported | `canonical_href_missing` or `canonical_missing` | attribute is present and non-empty |

Observed checks behind the first two rows: `urljoin` returns the data URL
unchanged; `expectedCanonical in href` is `True`; component compare is
`False` (hostname is `None`).

## 5. Adjacent false-green attack (distinct from this case): credentials

**Proposed extra case `credentials_url` (not in the frozen 32; no matrix
name implies userinfo — `wrong_host`/`wrong_path`/`wrong_query` are component
mismatches).** Same document URL and `expectedCanonical` as above, href:

```html
<link rel="canonical" href="https://user:secret@example.test/project/a.html">
```

Expected: **exit 1, `canonical_url_invalid`** — the contract says "reject
fragments and credentials", and there is no dedicated credential id.

**Attack mechanics.** The natural fix for `data_url` is exactly the code
shape that fails here: parse with `urlsplit`, then compare identity as
`(scheme, hostname, port, path, query)`. `hostname` strips userinfo, so the
credentialed URL compares **equal** to the expected canonical — observed
`True` in §7 — and the validator emits zero findings, exit 0. `data:` is
caught (hostname `None`) while credentials sail through: the same
normalization is right for one case and wrong for the other.

**Spec grounding.** WHATWG URL Standard lists a validation error
`invalid-credentials` — "The input includes credentials." — with the example
input `https://user@example.org`; the defining predicate is "A URL includes
credentials if its username or password is not the empty string." RFC 3986
§3.2.1: "Use of the format \"user:password\" in the userinfo field is
deprecated" and "Applications may choose to ignore or reject such data when
it is received as part of a reference." Rejecting credentials is thus
spec-sanctioned, and the contract makes it local policy.

Peer convergence (author-side, not authority): `URLNormalization.md:17`
independently pins both `data:`/`javascript:` → `canonical_url_invalid` and
credentialed `https://user@example.test/...` → exit 1 `canonical_url_invalid`;
`Case18.md:77` puts "non-HTTP(S) scheme (`javascript:`, `data:`)" in that same
id/exit row; `NoWrites.md:49` states `javascript_url`/`data_url` must yield
`canonical_url_invalid`; `StdoutExit.md` maps every policy id in this family
to exit 1.

**Precision caveat (avoid a false red while fixing the false green).** Test
non-empty username/password, not the presence of `@` and not
`netloc != hostname`: `https://@example.test/project/a.html` parses with
`netloc='@example.test'`, `hostname='example.test'`, `username=''`,
`password=None` (observed). Per the spec predicate it does **not** include
credentials and serializes away the empty userinfo, so a `netloc`-differs
check would reject a URL that should pass; use `username or password`.

**Also considered, rejected as the primary.**
- Empty fragment `href="https://example.test/project/a.html#"`: real
  false-green risk (`urlsplit(...).fragment` is `''`, so an `if fragment:`
  check misses it), but that is matrix case `fragment_url` (Case22) and
  `URLNormalization.md:17` already pins it as exit 1 `canonical_fragment` —
  covered elsewhere, so not this seat's claim.
- One valid canonical plus one `data:` canonical in the same head
  (count-before-validity ordering): strong, but it is a `data_url` ×
  `duplicate_different` hybrid; recorded here as a second candidate if L1
  wants a second extra case. It asserts that the exactly-one count is
  computed over link elements before URL validity is considered.

## 6. Sources

No spec copy is vendored in the lane: the lane root, `plans/`, `corpus/`
and `SKILL.md` were searched for `6596`, `WHATWG`, `rfc` and `data:` and
return only the lesson/QUALITY mentions of RFC 6596 and canonical policy —
no RFC, HTML or URL-spec text. The following were fetched from their official
publishers on 2026-10-20 under the contract's allowance for public official
documentation — no live property, service or credential was touched, and the
copies live only in `/tmp` scratch, not in lane bytes.

| source | location | quoted evidence used |
|---|---|---|
| RFC 6596, The Canonical Link Relation | `https://www.rfc-editor.org/rfc/rfc6596.txt` | §3 "The target (canonical) IRI MUST identify content that is either duplicative or a superset..."; target MAY "Have different scheme names"; "Specify only one canonical link relation for a resource"; improper designations may be ignored by applications |
| RFC 2397, The "data" URL scheme | `https://www.rfc-editor.org/rfc/rfc2397.txt` | "The 'data' URL scheme has no relative URL forms."; `dataurl := "data:" [ mediatype ] [ ";base64" ] "," data`; default `text/plain;charset=US-ASCII`; "only useful for short values" |
| RFC 3986, URI Generic Syntax | `https://www.rfc-editor.org/rfc/rfc3986.txt` | §3.2.1 userinfo grammar; user:password deprecated; applications may reject such data |
| WHATWG URL Standard | `https://url.spec.whatwg.org/` | special-scheme table and "A URL is special if..."; "A URL has an opaque path..."; "base URL cannot be used as a base URL because it has an opaque path"; `invalid-credentials` row with `https://user@example.org`; "A URL includes credentials if its username or password is not the empty string." |
| Google Search Central, consolidate duplicate URLs | `https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls` | "Use absolute paths rather than relative paths... Even though relative paths are supported by Google, they can cause problems..." — supports treating resolved relatives as valid positive controls, absolute as preferred |

Source-vs-policy split, stated so it is not misattributed:
- RFC 6596 does **not** forbid non-HTTP(S) canonical targets; it allows
  mixed schemes. HTTP(S)-only is local policy.
- None of the fetched sources says a `data:` canonical is invalid; the
  rejection comes from the contract's "compare ... HTTP(S) normalized
  absolute URL" clause plus the RFC 2397/URL-spec structure of `data:`.

## 7. Observed, inferred, unresolved

Observed (stdlib probes on the exact fixture bytes, `/tmp` only; no lane
bytes read-modified, no validator and no test suite run):
- `html.parser.HTMLParser(convert_charrefs=True)` emits exactly one link
  inside head: `{'rel': 'canonical', 'href': 'data:text/plain,https://example.test/project/a.html'}`.
- `urljoin("https://example.test/project/a.html", <href>)` returns the data
  URL unchanged; `urlsplit` gives `scheme='data'`, `netloc=''`,
  `path='text/plain,https://example.test/project/a.html'`, no query, no
  fragment; `expected in href` is `True`; component compare is `False`.
- `urlsplit("https://user:secret@example.test/project/a.html")` → username
  `'user'`, password `'secret'`, hostname `'example.test'`; component compare
  equals the expected canonical (`True`).
- `urlsplit("https://@example.test/project/a.html")` → netloc
  `'@example.test'`, hostname `'example.test'`, username `''`, password
  `None`.

Inferred (marked as such, not observed):
- The frozen expectation for `data_url` is exit 1 / `canonical_url_invalid`.
  The contract pins the policy wording, `findingIds` and `exitMap`, but does
  not ship per-case expectations; `measure.py` must materialize this one and
  L1 must adopt it before the count claim is meaningful.
- Python's `urlsplit` is not the WHATWG parser; for this href both agree
  (non-special scheme, no leading `//` after `data:`, so opaque path), but
  the validator must not treat `urlsplit` as the normative parser.

Unresolved:
- Exact `verdict` literal and whether default (non-`--json`) stdout is the
  contracted JSON object; contract names `--json` and describes `stdout` as
  the JSON object, which can be read either way. A peer reading
  (`StdoutExit.md`) resolves it as: every evaluated invocation emits exactly
  one parseable JSON object on stdout and `--json` is optional; `measure.py`
  should still pass `--json` and assert exit + ids only.
- `page` field source is not stated; manifest `url` is the only stable
  identifier and is recommended for both this case and `absolute_match`.
- Finding precedence when one page has two defects is unspecified. This case
  needs validity-before-comparison; the credentials proposal and the
  duplicate hybrid need count-before-validity.

## 8. Implementation requirements this case imposes

Deterministic order per page, because the id is asserted:
count canonical link elements in the explicit head → check `rel` token
(ASCII case-insensitive) → check `href` present and non-empty → resolve
against first head `<base>` or document URL → require absolute HTTP(S),
reject credentials → reject fragment → normalize and compare query-preserving
to `expectedCanonical`. `data_url` fails at the HTTP(S) requirement with
`canonical_url_invalid`; it must never reach comparison, and it must not be
dropped at collection.

Also: `--selftest` must use the same 182-byte fixture (hash above), otherwise
the selftest can be green while the matrix case is red or vice versa.

## 9. Checks for L1 (not run by this seat)

1. Confirm `measure.py` asserts, for `data_url`: exit `1`, findings exactly
   `[canonical_url_invalid]`, `page` = `https://example.test/project/a.html`,
   `pagesChecked` = 1.
2. Confirm the fixture hashes match §1 and that `absolute_match` uses the
   same document URL/expectedCanonical with an `https:` href, proving the
   pair is href-isolated.
3. Confirm the validator does not treat `--json`-less stdout differently for
   this case beyond the finding id (do not over-pin `verdict`).
4. If the credentials case is adopted, pin its id as `canonical_url_invalid`
   and include the `https://@example.test/...` acceptance control so the fix
   does not create a false red.
5. Re-read contract `matrixCases` after `measure.py` lands; the frozen list
   must stay 32 names and `data_url` must not be renamed.

Report: `.ufo/waves/round-22/w1/Case21.md`

Constraints honoured: read-only lane seat — no lane file edited, no git/jj
write, no build/test/lint/formatter run, no package transaction, no service,
no credentials. Scratch only under `/tmp/kake-r22-Case21` and `/tmp` spec
copies. Tool installs/updates: none.
