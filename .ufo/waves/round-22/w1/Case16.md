# Case16 — `body_link`

Seat: KakeR22.Case16 (scout, read-only). Lane base observed: `7c61c8cc791bde36dd5e3688bdfea2678d90146c`.
Contract read: `.ufo/waves/round-22/contract.json`. Case name read from the frozen `matrixCases` array.
No tests, no commands against any implementation, no installs, no registry/corpus edits. At this base the
lane has no `scripts/canonical_audit.py`; this report is author-side design evidence only. The only file
written is this report.

## Frozen rule being tested

Contract policy, verbatim (contract line 4): "Exactly one canonical link in explicit head per page, rel
ASCII case-insensitive token list; resolve href with first head base href or document URL; compare
WHATWG-like HTTP(S) normalized absolute URL to expectedCanonical, preserve query, reject fragments and
credentials."

Frozen ids include `canonical_outside_head`; frozen exits are `0` clean, `1` failed policy, `2`
could-not-evaluate input/unsupported shape, `64` usage. The contract does not further define the
`body_link` fixture; the shape below is this seat's fixed proposal, chosen to make the case
single-cause.

## Concrete case

Manifest entry:

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/body-link.html",
      "file": "fixtures/body_link.html",
      "expectedCanonical": "https://example.test/project/body-link.html"
    }
  ]
}
```

`fixtures/body_link.html` (exact bytes; LF endings):

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>body link</title>
</head>
<body>
  <p>Only canonical declaration is below, outside the head.</p>
  <link rel="canonical" href="https://example.test/project/body-link.html">
</body>
</html>
```

| Field | Value |
|---|---|
| Manifest `url` (document URL / resolution base) | `https://example.test/project/body-link.html` |
| Manifest `expectedCanonical` | `https://example.test/project/body-link.html` |
| `href` in the fixture | `https://example.test/project/body-link.html` (byte-equal to `expectedCanonical`) |
| Canonical link elements in `<head>` | 0 |
| Canonical link elements in `<body>` | 1 |
| Expected exit | `1` (failed policy) |
| Expected finding id | `canonical_outside_head` |
| Expected `page` | `https://example.test/project/body-link.html` (manifest `url`, not the file path) |
| Expected `pagesChecked` | `1` |
| Expected findings count for this page | exactly 1 |

Expected stdout (minimal shape; `verdict` literal is **not** frozen by the contract — `"failed"` is a
proposal, exit and id are binding):

```json
{"verdict":"failed","pagesChecked":1,"findings":[{"id":"canonical_outside_head","page":"https://example.test/project/body-link.html"}]}
```

Invocation used by the Matrix seat: `python3 scripts/canonical_audit.py --manifest <abs>/manifest.json --json`.

## Why this is the correct observation

1. **Single-cause fixture.** The only defect is location. `href` is absolute, byte-equal to
   `expectedCanonical`, with no `<base>`, no query, no fragment, and no credentials. Resolution and
   normalization therefore cannot distinguish this fixture from the clean positive control; only the
   head-scope check can. If the implementation returns 0, it is a false green by construction. If it
   returns `canonical_mismatch`, normalization/comparison has been run before (or instead of) placement.
2. **Local policy maps body placement to the dedicated id.** The policy scopes the declaration to the
   "explicit head". The element is a parsed `link` start tag after `</head>` and `<body>`, so it is
   outside that scope. The frozen id set contains `canonical_outside_head` specifically for this shape;
   `canonical_missing` is reserved for the `missing_link` case and must not absorb it.
3. **Platform semantics agree that a body canonical is not a canonical declaration.** Google Search
   Central, "The `rel="canonical"` `link` element": "The rel="canonical" link element is only accepted if
   it appears in the `<head>` section of the HTML" (observed, accessed 2026-10-20). WHATWG HTML makes
   `link` metadata content and permits it where phrasing content is expected only when "allowed in the
   body", i.e. when its `rel` contains only body-ok keywords; the §4.6.8 summary table lists `canonical`
   with an empty body-ok cell, and the body-ok list is `dns-prefetch`, `modulepreload`, `pingback`,
   `preconnect`, `prefetch`, `preload`, `stylesheet`. `canonical` is absent, so a `canonical` link in body
   is non-conforming (observed, WHATWG HTML `links.html` §4.6.8 table + `semantics.html` §4.2.4).
4. **Not another id.**
   - `canonical_multiple` is wrong: exactly one canonical `link` element exists.
   - `canonical_missing` is wrong: a canonical declaration was present and observed, merely misplaced.
   - `canonical_href_missing` / `canonical_url_invalid` / `canonical_fragment` / `canonical_mismatch` are
     wrong: `href` is present, absolute, valid, fragment-free, and equal to `expectedCanonical`.
   - `base_url_invalid` is wrong: there is no `<base>`.
   - `input_invalid` / `html_unsupported` are wrong: regular file, explicit head, serialized static HTML,
     one plain absolute HTTP(S) URL. The page is fully evaluable, so exit `2` is a false "could not
     evaluate".
   - Exit `64` is wrong: the manifest and CLI invocation are valid.
5. **Precedence rule required for a stable id.** If zero canonical links exist in the explicit head and
   one or more canonical links exist outside it, emit only `canonical_outside_head` (exit 1). Do not also
   emit `canonical_missing`. This is the only reading compatible with the Matrix seat's "stable
   finding-id per case" requirement and with `missing_link` retaining its own id. The contract does not
   spell out finding precedence, so L1 should freeze this sentence for Implement and Matrix before
   measurement.

## Head-scope implementation note (operability)

`html.parser.HTMLParser` is a tokenizer, not a tree builder: "This parser does not check that end tags
match start tags or call the end-tag handler for elements which are closed implicitly by closing an outer
element" (Python 3.15 docs, `#module-html.parser`; local interpreter is 3.14.8). The audit must therefore
own the head state machine:

- Head scope opens at `handle_starttag('head')`. The page must have an explicit head start tag; if the
  contract's `missing_head` case is classified `canonical_missing`, that is the same explicit-head model
  applied here.
- Head scope closes at `handle_endtag('head')`, or at the first start tag that is not permitted inside
  head. The in-head start-tag set is `base`, `basefont`, `bgsound`, `link`, `meta`, `noframes`,
  `noscript`, `script`, `style`, `template`, `title` (plus `html`, which merges and does not close head);
  every other start tag and any non-whitespace character data closes it (WHATWG HTML §13.2.6.4.4,
  "Anything else": "Pop the current node (which will be the `head` element) off the stack of open
  elements." / "Switch the insertion mode to `after head`.").
- A `link` start tag whose `rel` token set contains `canonical` is a canonical declaration wherever it
  appears. Location decides the finding; URL normalization must not decide whether the element counts.
- Attribute names arrive lowercased and attribute values are character-reference-decoded (docs
  `#html.parser.HTMLParser.handle_starttag`), so `rel`/`href` need no name normalization and no second
  entity decode. `rel` token comparison is audit-side ASCII case-insensitive.
- Do not double count `<link ... />`: `handle_startendtag` defaults to calling `handle_starttag` and then
  `handle_endtag`. Counting only in `handle_starttag` observes one element; overriding both without a
  guard observes two.
- `script`/`style` content is raw text (`handle_data`), so `script_decoy` is structurally inert; comments
  arrive in `handle_comment`. `template` content is tokenized normally and needs separate suppression —
  neither fact changes this case.

## Adjacent false-green attack (distinct from this case)

**Name:** `head_implicit_close_body_canonical` (omitted `</head>`).

Same manifest `url` and `expectedCanonical` as above; fixture:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>implicit head close</title>
  <div>
    <link rel="canonical" href="https://example.test/project/body-link.html">
  </div>
```

**Correct result:** exit `1`, `canonical_outside_head`. WHATWG HTML in-head "Anything else" pops the
head at `<div>`, switches to "after head", implies `<body>`, and reprocesses the `<div>`, so the `link`
is a body descendant (observed, §13.2.6.4.4). The head start tag is explicit, so this is not
`missing_head`.

**False green:** a validator that sets `in_head = True` at `<head>` and clears it only on
`handle_endtag('head')` receives no end event for the omitted `</head>` — HTMLParser does not synthesize
implicit end tags — so the link is counted as a head canonical. Its `href` equals `expectedCanonical`, the
comparison passes, and the tool returns exit `0` clean. Using `<div>` instead of `<body>` also defeats the
narrow fix that resets head on the `<body>` start tag, so this attack is strictly stronger than an
explicit-`<body>` variant of the same page.

**Why it is distinct from `body_link`:** `body_link` contains explicit `</head>` and `<body>`; both of the
obvious resets (end tag, body start tag) classify it correctly. The attack has no `</head>` and no body
tag, so it isolates the implicit-close rule. It is also distinct from `missing_head` (explicit head start
tag present) and from the decoy cases (no comment/script/template).

**Placement:** the 32-case matrix is frozen; do not add a 33rd case. Put this fixture in
`canonical_audit.py --selftest` (assert exit 1 + `canonical_outside_head`) or propose it as an r23 matrix
case. The expected id/exit are already frozen-compatible.

## Sources and status

| Source | Locator | Supports | Status |
|---|---|---|---|
| Frozen contract | `.ufo/waves/round-22/contract.json`, line 4 interface/policy/findingIds/exitMap | Policy cardinality, ids, exits, explicit head | Observed (local authority) |
| Google Search Central, consolidate duplicate URLs | https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls, accessed 2026-10-20, "The `rel="canonical"` `link` element" | Head-only acceptance: "The rel="canonical" link element is only accepted if it appears in the `<head>` section of the HTML" | Observed (fetched by this seat) |
| WHATWG HTML `link` element | https://html.spec.whatwg.org/multipage/semantics.html, §4.2.4, accessed 2026-10-20 | `link` contexts; body-ok rule: allowed in body only if `rel` contains only body-ok keywords | Observed (fetched by this seat) |
| WHATWG HTML link types | https://html.spec.whatwg.org/multipage/links.html, §4.6.8 table and §4.6.8.4, accessed 2026-10-20 | `canonical` affects `link`, not body-ok; "preferred URL for the current document" | Observed (fetched by this seat) |
| WHATWG HTML parsing | https://html.spec.whatwg.org/multipage/parsing.html, §13.2.6.4.4 "in head", §13.2.6.4.6 "after head", accessed 2026-10-20 | In-head "Anything else" closes head and implies body; after-head `link` is pushed back into head (policy boundary below) | Observed (fetched by this seat) |
| RFC 6596 §3 | https://www.rfc-editor.org/rfc/rfc6596, accessed 2026-10-20 | Canonical relation designates the preferred IRI; relative IRIs allowed | Observed (fetched by this seat) |
| Python `html.parser` docs | https://docs.python.org/3/library/html.parser.html, accessed 2026-10-20, `#module-html.parser`, `#html.parser.HTMLParser.handle_starttag` | No implicit end-tag callbacks; attr lowercasing/decoding; script/style raw text; `scripting` flag (3.14.1+) | Observed (fetched by this seat) |

## Confidence and remaining unknowns

- Exit `1` / `canonical_outside_head`: **HIGH** (contract policy + dedicated id + head-only platform
  semantics).
- Exactly one finding for the page, and outside-head suppressing `canonical_missing`: **MEDIUM-HIGH**.
  The contract fixes the id set but not precedence; L1 should freeze the sentence above.
- `page` value = manifest `url` and `pagesChecked = 1`: **MEDIUM-HIGH** (contract names the fields but
  not the value source; the manifest `url` is the only stable page identity).
- `verdict` literal: **UNKNOWN / non-binding**. The contract does not freeze a string; `"failed"` is a
  proposal. Matrix should compare exit and id, not the literal.
- Boundary not exercised by the matrix: a `link rel=canonical` between `</head>` and `<body>`. HTML5
  after-head rules push the head element back on the stack and insert such a link inside the head
  (§13.2.6.4.6), but the contract's "explicit head" wording is best served by treating source position
  outside `<head>...</head>` as `canonical_outside_head`. L1 should record that strict-source-scope
  choice explicitly; it is a local policy divergence from tree-construction, not a platform claim.
- Not exercised: a head canonical plus a body canonical on the same page. The matrix has no such case;
  this report does not invent an expectation for it. For a single body-only canonical the classification
  above is unambiguous.
- No implementation exists at the observed base, so no behavior was measured or asserted; the adjacent
  attack is a falsification recipe, not an observed defect.
