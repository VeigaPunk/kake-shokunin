# Case17 — `href_absent`

Seat `KakeR22.Case17`, read-only scout. Lane `kake-shokunin`, base
`7c61c8cc791bde36dd5e3688bdfea2678d90146c` (observed `git rev-parse HEAD`, matches contract).
Contract read from `.ufo/waves/round-22/contract.json` (round 22, C1, matrix case 17 of 32; finding-id
list and exit map at `interface`). No validator, fixture set, `matrix.py`, or `measure.py` exists at this
base (`scripts/` contains only `corpus-contract.mjs`, `freshness-sweep.mjs`, `probe-delta.mjs`). No tests
run against an implementation; this is a case specification for L1. Only this report was written; no
tools installed, no lane/registry/jj mutation, no live properties touched. Scratch fetches are under
`/tmp` (public official docs only).

## Frozen expectation

| field | value |
|---|---|
| manifest `url` | `https://example.test/project/a.html` |
| manifest `file` | `href_absent.html` (relative to the manifest directory; regular file) |
| `expectedCanonical` | `https://example.test/project/a.html` |
| expected exit | **1** (failed policy) |
| expected finding id | **`canonical_href_missing`** |
| finding `page` | `https://example.test/project/a.html` (the manifest URL, not the file path) |
| `pagesChecked` | `1` |
| verdict | not clean; literal `"failed"` is `[INFERENCE]` from the contract's exit-map wording |

Minimum stdout payload for assertion:

```json
{"verdict":"failed","pagesChecked":1,
 "findings":[{"id":"canonical_href_missing","page":"https://example.test/project/a.html"}]}
```

## Concrete fixture

`manifest.json`:

```json
{
  "version": 1,
  "pages": [
    {
      "url": "https://example.test/project/a.html",
      "file": "href_absent.html",
      "expectedCanonical": "https://example.test/project/a.html"
    }
  ]
}
```

`href_absent.html`:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>canonical href absent</title>
<link rel="canonical">
</head>
<body>
<p>href absent fixture</p>
</body>
</html>
```

Design constraints, so the case stays single-axis:

- The `link` element is lowercase and inside an **explicit** `<head>`/`</head>`; there is exactly one.
- `rel` value is the lowercase single token `canonical` (rel tokenization/casing has its own cases).
- The `href` **attribute name is entirely absent** — not empty, not valueless, not an entity, not a
  lookalike such as `data-href` (that is the adjacent attack below). The start tag has exactly one
  attribute.
- No `<base>`, no second canonical, no body link, no comment/script/template/noscript decoy. Those axes
  belong to `first_base`, `second_base_ignored`, `duplicate_*`, `body_link`, `comment_decoy`,
  `script_decoy`, `template_decoy`.

## Why exit 1 / `canonical_href_missing`

1. **The document shape is supported and explicitly evaluable.** Regular UTF-8 file, explicit head,
   serialized static HTML, one `link` element. Nothing here is `input_invalid` or `html_unsupported`
   (exit 2 is contracted as "could-not-evaluate input/unsupported shape").
2. **The element is a canonical declaration attempt.** The `link` is in the explicit head and its `rel`
   token list (split on ASCII whitespace, ASCII case-insensitive) is exactly `{canonical}`. The HTML
   Standard defines the keyword: "The canonical keyword indicates that URL given by the href attribute
   is the preferred URL for the current document." (§4.6.8.4). So the element asserts a canonical
   relationship; what it lacks is the target.
3. **The href attribute name is absent.** HTMLParser emits for this exact fixture:

   ```
   link [('rel', 'canonical')]
   ```

   There is no `href` key at all. (Local probe, Python 3.14.8, stdlib only.) The contract's policy
   requires the canonical URL to be resolved from an href; with no href there is nothing to resolve or
   compare. The dedicated id is `canonical_href_missing`, which the contract's finding-id set provides
   and Case13/URLNormalization independently assign to `href_absent`.
4. **Platform semantics, and the deliberate policy overlay.** WHATWG HTML §4.2.4 says: "The address of
   the link(s) is given by the href attribute." and "If both the href and imagesrcset attributes are
   absent, then the element does not define a link." Strictly, a browser-side consumer therefore sees
   no canonical hyperlink at all — which, read alone, would suggest `canonical_missing`. The frozen
   contract adds a distinct id for this shape, so the preflight treats a `link rel=canonical` element
   without an href as a **broken declaration attempt**, not as "no declaration". Rationale
   (`[INFERENCE]`, but strongly implied by the frozen id set and case names):
   - `missing_link` owns zero canonical-rel elements; `href_absent` owns one element with no URL.
   - Collapsing this page to `canonical_missing` hides the actionable defect (the author declared a
     canonical but omitted the attribute) and would leave `canonical_href_missing` with no matrix case.
   - The verdict consequence is the same exit (1), but the matrix asserts the id, so it must be the
     specific one.
   If L1 instead freezes strict platform semantics (`canonical_missing`), that contradicts Case13,
   URLNormalization, and the id's only plausible fixture; do not do it silently.
5. **Exit 1, not 2.** The page was fully evaluated: head found, link counted, rel matched, absence
   concluded. Exit 2 is for inability to evaluate (bad manifest, symlink/traversal, no explicit head,
   unsupported document), none of which applies. Exit 64 is CLI usage only.
6. **`expectedCanonical` is deliberately self-referential.** It is the URL the page *should* declare,
   and setting it equal to the page URL means a validator cannot launder the missing href into a clean
   self-match by defaulting to the document URL. The finding must be emitted **before** any URL
   resolution/comparison; with a different non-self `expectedCanonical` the result must stay the same
   id and exit (no `canonical_mismatch`).
7. **Other ids do not fit.** `canonical_url_invalid` needs an href value to parse; `canonical_mismatch`
   needs a resolved URL to compare; `canonical_outside_head` needs the link outside the explicit head;
   `canonical_multiple` needs more than one canonical declaration; `base_url_invalid` needs a base.
   None applies.

## Parser facts and implementation constraints

- **Explicit head is audit-side state.** `html.parser` is an event stream and does not build a tree or
  report implicit head boundaries (PythonParser report, this wave). Track `head_seen` / in-head depth
  yourself; an href-less `link` found outside the explicit head is `canonical_outside_head`, not this
  case.
- **Attribute-name presence, not value.** Detect absence with an exact-name scan over the `attrs` list:
  `any(name == 'href' for name, _ in attrs)`. Do **not** use `dict(attrs).get('href') is None` as the
  absence test: HTMLParser also yields `('href', None)` for the *present but valueless* attribute
  `<link rel="canonical" href>` (and `('href', '')` for `href=""`). The tokenizer shapes are distinct
  even if L1 decides some of them share a finding id.
- **Never resolve before the presence check.** In particular, do not run
  `urljoin(base_href_or_page_url, attrs.get('href') or '')`, and do not use the first head `<base href>`
  as a fallback for a missing href. `<base>` supplies the base URL for parsing a *present* URL
  reference; it is not an href. The same applies to the document URL.
- **rel tokenization** is a split on ASCII whitespace, unordered unique token set, ASCII case-insensitive
  comparison. The fixture's single lowercase `canonical` token exercises none of that machinery; do not
  add extra tokens here.
- **Finding payload** must carry the manifest `url` as `page`, and `pagesChecked` must be 1 for a
  one-page manifest. `findings: []` or exit 0 is the failure this case exists to catch.
- **Precedence recommendation (`[INFERENCE]`).** Count canonical-rel `link` elements in the explicit
  head including href-less declaration attempts, so a broken element cannot mask a duplicate
  (`canonical_multiple` before per-element href checks). The isolated fixture has exactly one, so this
  precedence is not exercised here; L1 should freeze it for the mixed shape.
- **No network, no writes, no JS.** Nothing in this fixture requires them.

## Adjacent false-green attack (distinct from this case)

**Name:** `lookalike_href_attribute`.

Same `url` and `expectedCanonical` as above; `file`: `lookalike_href_attribute.html`:

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>lookalike href fixture</title>
<link rel="canonical" data-href="https://example.test/project/a.html">
</head>
<body>
<p>lookalike href fixture</p>
</body>
</html>
```

(Replace the title text with anything; only the `link` line is load-bearing.)

| field | value |
|---|---|
| expected exit | **1** |
| expected finding id | **`canonical_href_missing`** |
| `page` | `https://example.test/project/a.html` |
| `pagesChecked` | `1` |

**Real platform behavior.** The link's `href` attribute is absent; `data-href` is a **custom data
attribute**, not the link address. WHATWG HTML §3.2.6.6: "A custom data attribute is an attribute in no
namespace whose name starts with the string `data-`, has at least one character after the hyphen, is a
valid attribute local name, and contains no ASCII upper alphas." Such attributes "are intended to store
custom data, state, annotations, and similar, private to the page or application". The HTML tokenizer
stores the literal name `data-href` (§13.2.5.33 appends characters to the current attribute's name;
ASCII uppercase is lowercased, nothing else is stripped), so it never becomes `href`. The element
therefore has no href and does not define a link (§4.2.4), and the correct preflight result is the same
as `href_absent`: `canonical_href_missing`, exit 1.

**False-green mechanism.** A second, non-exact extraction path sees the URL:

- A raw-text regex over the start tag finds it. Locally observed on Python 3.14.8:
  `re.search(r'\bhref\s*=', '<link rel="canonical" data-href="…">')` matches — `-` is a non-word
  character, so `\b` sits between it and `h`. `r'<link[^>]*href\s*='` also matches. Only an anchored
  exact-name pattern such as `r'(?:^|\s)href\s*='` avoids it.
- An attribute lookup that strips a namespace prefix, tests `name.endswith('href')`, tests
  `'href' in name`, or normalizes `data-href`/`xlink:href` to `href` also extracts the value.
- A "collect any URL-looking attribute on a canonical link" fallback can prefer `data-href` when `href`
  is missing, then `urljoin` yields the expected URL and the validator returns exit 0 with no findings.

The same class covers `xlink:href` (HTMLParser emits the literal `('xlink:href', '…')`; local probe) and
any other `*href` attribute. `hreflang` is not an address and must not be used either.

**Why it is distinct.**

- From `href_absent`: that fixture has no href-like attribute at all, so its presence check is
  trivially exact. This attack carries the expected URL in a lookalike attribute; a validator can pass
  `href_absent` and still fail here if any secondary path extracts attributes leniently. It pins
  **exact attribute-name equality**, not merely "no href key".
- From Case10's named attack (`attr_uppercase` shadow): that attack is a second *element* whose real
  `HREF` is hidden from a case-sensitive extractor and expects `canonical_multiple`. Case10's secondary
  hazard is duplicate attributes on one tag (first-wins). Neither is a differently named, non-href
  attribute.
- From `entity_href` / `attr_uppercase`: those exercise value decoding and ASCII case folding of the
  real attribute; `data-href` is a different attribute name and the correct result is href-missing, not
  a resolved match.
- From `body_link` / `duplicate_*`: the element count, head placement, and rel token are all correct
  here; only URL acquisition is spoofed.

**Guard.** Extract the address only from an attribute whose name is exactly `href` (the parser already
lowercases names; no further normalization). Never treat `data-href`, `xlink:href`, `hreffoo`, or a
suffix match as the link address, and never parse the lookalike's value as a URL. This applies to every
path that can produce a canonical URL, including any raw-text duplicate scan or diagnostics side channel.

## Cross-seat status and remaining unknowns

- **`href_empty` is contested and is not my case.** `URLNormalization.md` P2 says `href=""` resolves to
  the base and must be clean-if-equal or `canonical_mismatch`, explicitly not
  `canonical_href_missing`; `Case02.md` §7.1 says empty belongs to the same failure family as absent and
  must never resolve to the document URL; `Case18` initially proposed mapping `href=""`/valueless/
  whitespace to `canonical_href_missing`. The frozen contract names both `href_absent` and `href_empty`
  as separate cases but does not fix the empty mapping. This does not change `href_absent`
  (`canonical_href_missing` in every reading). L1 must decide `href_empty` separately; do not let the
  `href_absent` fixture quietly settle it.
- **Verdict literal** `"failed"` is `[INFERENCE]`; the contract only fixes exit 1 and the finding.
- **Fixture literals** (file name, exact title, whitespace) are recommendations; `measure.py`/Matrix may
  place them anywhere manifest-relative as long as the perturbed axis is only the href attribute's
  absence and the expectation stays exit 1 / `canonical_href_missing`.
- **Precedence for mixed shapes** (an href-less canonical plus another canonical, or a lookalike plus a
  real href) is not exercised by this case and is a policy decision; the recommendation above is
  inference.
- No implementation exists at this base, so no code behavior is asserted. `scripts/canonical_audit.py`,
  `measure.py`, `matrix.py`, and `cases.json` were confirmed absent.

## Sources

Official pages fetched 2026-10-20 UTC from `/tmp` scratch; sibling source reports already in this wave
are cited instead of re-fetching where noted. No source text was treated as an instruction.

| ID | Source and locator | Exact text used | Use |
|---|---|---|---|
| S1 | WHATWG HTML Standard §4.2.4 "The `link` element", https://html.spec.whatwg.org/multipage/semantics.html#the-link-element (fetched bytes lines 406–411) | "The address of the link(s) is given by the href attribute." / "If the href attribute is present, then its value must be a valid non-empty URL potentially surrounded by spaces." / "If both the href and imagesrcset attributes are absent, then the element does not define a link." | href is the only address; absent href means no link |
| S2 | WHATWG HTML Standard §4.6.8.4 "Link type canonical", https://html.spec.whatwg.org/multipage/links.html#link-type-canonical | "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." | canonical target is the href value |
| S3 | WHATWG HTML Standard §13.2.5.33 "Attribute name state", https://html.spec.whatwg.org/multipage/parsing.html#attribute-name-state (fetched bytes lines 2219–2223) | "the complete attribute's name must be compared to the other attributes on the same token; if there is already an attribute on the token with the exact same name, then this is a duplicate-attribute parse error and the new attribute must be removed from the token." | names are stored/compared as names; `data-href` is not `href` |
| S4 | WHATWG HTML Standard §3.2.6.6 "Embedding custom non-visible data with the data-* attributes", https://html.spec.whatwg.org/multipage/dom.html#embedding-custom-non-visible-data-with-the-data-*-attributes | "A custom data attribute is an attribute in no namespace whose name starts with the string "data-", has at least one character after the hyphen, is a valid attribute local name, and contains no ASCII upper alphas." / "Custom data attributes are intended to store custom data, state, annotations, and similar, private to the page or application" | `data-href` is a custom data attribute, not a link href |
| S5 | WHATWG HTML Standard §4.2.3 "The base element", https://html.spec.whatwg.org/multipage/semantics.html#the-base-element | "The base element allows authors to specify the document base URL for the purposes of parsing URLs" / "If there are multiple base elements with href attributes, all but the first are ignored." | base is a resolution base, not a default href |
| S6 | Python Software Foundation, "html.parser", https://docs.python.org/3/library/html.parser.html#html.parser.HTMLParser.handle_starttag (as recorded in this wave's `PythonParser.md`, accessed 2026-10-20) | "For empty attributes, value is None." / "The name will be translated to lower case" | parser shape for absent/valueless href and literal names |
| S7 | Local stdlib probe, Python 3.14.8, `/tmp` only | `<link rel="canonical">` → `[('rel','canonical')]`; `href` (valueless) → `('href', None)`; `data-href` → `('data-href','…')`; `xlink:href` → `('xlink:href','…')`; `\bhref=` matches `data-href=` | observed parser/extractor behavior (corroboration, not a validator test) |
| S8 | Google Search Central, "How to specify a canonical URL with rel="canonical" and other methods", https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls (as recorded in this wave's `GoogleCanonical.md`, accessed 2026-10-20; page last updated 2026-07-10) | "The rel="canonical" link element is only accepted if it appears in the <head> section of the HTML" / "Use absolute paths rather than relative paths" | head-only acceptance and absolute-URL recommendation; the page does **not** address a missing href, so it is not load-bearing for this case |
| S9 | RFC 6596 §3 (as recorded in this wave's `RFC6596.md`, accessed 2026-10-20) | "Specify a relative IRI (see [RFC3986], Section 4.2)." / self-referential target permitted | canonical relation permits relative and self targets; not a resolution or HTML rule |

Source-vs-policy split: WHATWG grounds the parser and element semantics; the mapping of an href-less
canonical element to the dedicated `canonical_href_missing` id (rather than `canonical_missing`) is the
frozen local policy implied by the contract's finding-id set. No source says Google will reject the
page or select any canonical; this is a policy preflight only.

## Checks for L1 (not run by me)

- Encode `href_absent` as exit **1**, finding id **`canonical_href_missing`**, `page` =
  `https://example.test/project/a.html`, `pagesChecked` 1, non-clean verdict; fixture has explicit head,
  one `link`, `rel="canonical"`, and no `href` attribute.
- Reject any clean/exit-0 result or any fallback that resolves the missing href to the document URL,
  the first `<base href>`, or the manifest file path.
- If the matrix also adds `lookalike_href_attribute` (`data-href` / `xlink:href`), expect exit 1 /
  `canonical_href_missing`, not clean and not `canonical_url_invalid`; assert that the extractor compares
  attribute names exactly.
- Keep `href_empty` and valueless `<link rel=canonical href>` out of this row until L1 freezes their
  mapping; they are tokenizer-distinct from this case and currently contested across reports.
- Confirm no lane edits beyond this report were made by this seat.

## Touched surfaces

`.ufo/waves/round-22/w1/Case17.md` only. No scripts, corpus, registry, verifier, or lane state edited;
no installs; no tests, builds, or formatters run.
