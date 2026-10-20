# Round 22 · w1 · Case11 — `entity_href`

Seat: `Case11` (scout, leaf) · Lane: `kake-shokunin` · Baseline: `7c61c8cc791bde36dd5e3688bdfea2678d90146c`
Mode: read-only; this report is the only artifact written. No validator, matrix, selftest, or lane test was executed.
Stdlib probes only (Python 3.14.8 `HTMLParser` + `html.unescape` + `urllib.parse`), no files created.
Contract: `.ufo/waves/round-22/contract.json`; interface `scripts/canonical_audit.py`; policy "exactly one canonical
link in explicit head", "resolve href", "compare WHATWG-like HTTP(S) normalized absolute URL to expectedCanonical".

## Case specification (proposed frozen fixture)

Manifest record (the page's document URL equals the expected canonical; the only variable is the source encoding):

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html?tab=docs&mode=full","file":"entity_href.html","expectedCanonical":"https://example.test/project/a.html?tab=docs&mode=full"}]}
```

`entity_href.html` (regular file beside the manifest, UTF-8, LF endings):

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Entity-encoded canonical href</title>
<link rel="canonical" href="https://example.test/project/a.html?tab=docs&amp;mode=full">
</head>
<body>
<p>Canonical href uses a named character reference for the ampersand.</p>
</body>
</html>
```

Expected observation:

| Field | Value |
|---|---|
| exit | `0` (clean) |
| `pagesChecked` | `1` |
| `findings` | `[]` |
| finding id | none; matrix-level positive sentinel `clean` (the Matrix charter's "positive id clean"); `clean` is not one of the ten contract `findingIds` |
| `verdict` | clean class; exact string is **not frozen** by the contract (inference) |

Non-vacuity: the source attribute text is `...?tab=docs&amp;mode=full`, while `expectedCanonical` is
`...?tab=docs&mode=full`. A validator comparing raw bytes cannot pass this page; only decoding the character
reference produces the expected URL. A missing decode surfaces as `canonical_mismatch` with exit 1, which is the
case's intended failure diagnosis.

## Why (evidence chain)

1. **Observed — HTML tokenization decodes the attribute before any URL processing.**
   In the attribute-value (double-quoted) state, `U+0026 AMPERSAND` switches to the character reference state;
   `&amp;` is a named reference to `U+0026`. The token's attribute value is the decoded string.
   Sources: HTML Standard §13.2.5.36 ("Switch to the character reference state."), §13.2.5.77, §13.2.5.78.
2. **Observed — the declared stdlib parser supplies the decoded value.**
   Python 3.14.8 `/usr/lib/python3.14/html/parser.py` unescapes every non-empty quoted attribute value
   (`parse_starttag`, line 483 → `_unescape_attrvalue`, lines 28/93–106). A probe with this exact fixture returned
   `href = "https://example.test/project/a.html?tab=docs&mode=full"` both with `convert_charrefs=True` and
   `False`; attribute decoding is independent of that flag. The docs state: "All entity references from
   html.entities are replaced in the attribute values."
3. **Observed — the URL layer leaves the decoded ampersand alone.**
   The href is absolute, so resolution against the document URL is identity. The WHATWG query percent-encode set
   excludes `&`, and RFC 3986 §3.4 admits `sub-delims` (which includes `&`) in `query`; `urljoin`/`urlsplit`/
   `urlunsplit` round-tripped the URL byte-identically in the probe.
4. **Derived from contract policy — comparison succeeds.**
   Exactly one canonical `link` sits in the explicit head; `rel` is the ASCII-lowercase token `canonical`; the
   target is HTTP(S), fragment-free, credential-free, query preserved; it equals `expectedCanonical`. Therefore
   there is no finding and the exit class is 0. The page is a supported serialized-HTML shape, so exit 2 does not
   apply.
5. **Scope of the inference.** Steps 1–3 are observed from primary text/source. Step 4 assumes the implementation
   follows the frozen contract literally; the script is **absent at baseline** (`scripts/canonical_audit.py`
   does not exist), so no implementation behavior is claimed.

Guard against a weakened test: `expectedCanonical` must stay the decoded URL. Re-encoding it as
`...&amp;mode=full` would invert the case and let a decoderless validator pass, defeating the only property
this case measures.

Deliberate exclusions (so a failure has one cause): numeric references (`&#38;`), semicolon-less legacy forms
(`&amp`), and ambiguous ampersands (`&amp=` / `&copy=`) are **not** used here. The HTML Standard's
attribute-specific rule for semicolon-less named references (flush as literal when followed by `=` or an ASCII
alphanumeric) is a separate behavior; Python 3.14 implements it in `_replace_attr_charref`. This case uses the
unambiguous `&amp;` only.

What this case does **not** establish: a full HTML5 tree/encoding implementation, browser behavior, or any remote
property; the validator remains a documented-subset checker (contract limitation).

## Adjacent false-green attack (distinct from this case): double decoding

Name suggestion: `entity_double_decoded` — an over-decoding negative, not one of the frozen 32 matrix names.
Fixture `entity_double_encoded.html`, same manifest URL/expected canonical as above:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Double-encoded canonical href</title>
<link rel="canonical" href="https://example.test/project/a.html?tab=docs&amp;amp;mode=full">
</head>
<body>
<p>Query contains a literal ampersand encoded twice.</p>
</body>
</html>
```

- **True attribute value (observed):** `https://example.test/project/a.html?tab=docs&amp;mode=full`.
  The query data contains the literal characters `amp;mode=full`; it is a valid HTTP(S) URL.
- **Correct verdict:** `canonical_mismatch`, exit 1. The decoded URL does not equal
  `https://example.test/project/a.html?tab=docs&mode=full`; `&amp;` is query data, and the URL standard never
  decodes character references at the URL layer.
- **False green:** a validator that decodes attributes twice — e.g. receiving the already-decoded value from
  `handle_starttag` and then calling `html.unescape()` or `.replace("&amp;", "&")` on it — obtains
  `...?tab=docs&mode=full`, matches `expectedCanonical`, emits no finding, and exits 0 on a page whose canonical
  declaration points at a different query.
- **Why plausible:** the Python docs' attribute-unescaping sentence is easy to miss; an implementer who assumes
  the parser returns raw values (or who pre-unescapes raw source before/after parsing) introduces exactly one
  extra decode. The observed stdlib pipeline makes the extra pass a one-line mistake.
- **Pinning pair:** `entity_href` must be clean **and** `entity_double_decoded` must be `canonical_mismatch`.
  Together they pin exactly one decode pass; either alone does not.
- **Placement:** recommended as an `--selftest` negative control in `scripts/canonical_audit.py`. Adding it to
  the frozen 32-case matrix is an L1 decision: the matrix population is frozen, and the Measure gate counts that
  population.

Related edge (not selected as the attack): `&num;` decodes to `#`, so a fragment can be entity-encoded as
`...a.html&num;section` with no literal `#` in the source. That bypasses a raw-string fragment check, but to turn
it into a false green it needs a fragment-bearing `expectedCanonical`, which makes it a fragment-rejection test
rather than a pure entity-layer attack. Kept as a note for the fragment/critic seats, not claimed here.

## Boundaries and non-claims

- No network, browser, JS, HTTP header, redirect, credentials, or live property was consulted; all sources are
  public official documentation/specification text plus the local stdlib.
- The case is a publisher-side static-file policy control, not proof that any engine selects this canonical, and
  not a claim that the target URL is reachable or duplicate (contract limits).
- The fixture is an authorized publisher example; no production artifact was audited.
- Registry mapping (S020+, `corpus/SOURCES.md`) is owned elsewhere; this seat did not edit it.

## Sources (all opened 2026-10-20)

| Source | Section/anchor | Located quote or grammar | Class |
|---|---|---|---|
| HTML Standard | [§4.6.8.4 Link type "canonical"](https://html.spec.whatwg.org/multipage/links.html#link-type-canonical) | "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." | official spec |
| HTML Standard | [§13.2.5.36 Attribute value (double-quoted) state](https://html.spec.whatwg.org/multipage/parsing.html#attribute-value-(double-quoted)-state) | On ampersand: "Switch to the character reference state." | official spec |
| HTML Standard | [§13.2.5.77 Character reference state](https://html.spec.whatwg.org/multipage/parsing.html#character-reference-state) | Entry state appending `&` to the temporary buffer | official spec |
| HTML Standard | [§13.2.5.78 Named character reference state](https://html.spec.whatwg.org/multipage/parsing.html#named-character-reference-state) | "If the character reference was consumed as part of an attribute" … next char `=` or ASCII alphanumeric | official spec |
| WHATWG URL Standard | [query percent-encode set](https://url.spec.whatwg.org/#query-percent-encode-set) | Set is C0 controls plus SPACE, `"`, `#`, `<`, `>` — `&` absent | official spec |
| RFC 3986 | [§2.2](https://www.rfc-editor.org/rfc/rfc3986.html#section-2.2), [§3.4](https://www.rfc-editor.org/rfc/rfc3986.html#section-3.4) | `sub-delims = "!" / "$" / "&" / …`; `query = *( pchar / "/" / "?" )` | official spec |
| RFC 6596 | [§3](https://www.rfc-editor.org/rfc/rfc6596.html#section-3) | "Specify only one canonical link relation for a resource." | official spec |
| Python docs | [html.parser](https://docs.python.org/3/library/html.parser.html) | "All entity references from html.entities are replaced in the attribute values." | official docs |
| Local stdlib | `/usr/lib/python3.14/html/parser.py` lines 28, 93–106, 483 | `_unescape_attrvalue` applied in `parse_starttag` | observed implementation |

Probe evidence (stdlib only, no lane state): exact fixture attr →
`https://example.test/project/a.html?tab=docs&mode=full`; `html.unescape` of that decoded value →
`...&mode=full` (demonstrates the double-decode outcome); `urlsplit(...).query` → `tab=docs&mode=full`;
`urlunsplit` round-trip equal.

## Residual unknowns

1. The contract does not freeze the clean `verdict` string; only exit 0 and the empty findings list are decisive.
2. Python-version portability: 3.14.8 is observed here; the current 3.x docs state the same attribute
   replacement, but no other interpreter was probed (inference for those versions).
3. Fixture directory/file naming and matrix schema are owned by the Matrix seat; names above are proposals.
4. The implementation is absent at baseline; no claim is made that it currently behaves as this case requires.
