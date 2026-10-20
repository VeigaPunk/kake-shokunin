# Case10 — `attr_uppercase`

Seat: `KakeR22.Case10`, read-only scout. Lane `kake-shokunin` at base `7c61c8cc791bde36dd5e3688bdfea2678d90146c`. Contract read from `.ufo/waves/round-22/contract.json` (round 22, C1, matrix case 10 of 32). No tests run, no lane mutations; this report is the only lane file written. No tools installed or updated. Scratch fetches live at `/tmp/kake-r22-Case10/` (public docs only, no host services).

## Result

| Field | Value |
|---|---|
| Manifest `url` | `https://example.test/project/a.html` |
| `expectedCanonical` | `https://example.test/project/a.html` |
| Expected exit | **0** |
| Expected verdict | `clean` |
| Expected finding id | none emitted (`findings: []`); the matrix's positive sentinel should be `clean`, not a finding id |
| `pagesChecked` | 1 |

No `[INFERENCE]` is load-bearing for this expected value: it follows from the platform rules below plus the frozen contract policy. The concrete fixture bytes are a recommendation (Matrix owns the final fixture), not a required literal.

## Concrete fixture

Manifest entry (path relative to the manifest directory, per contract):

```json
{"version": 1, "pages": [
  {"url": "https://example.test/project/a.html",
   "file": "fixtures/attr_uppercase.html",
   "expectedCanonical": "https://example.test/project/a.html"}
]}
```

`fixtures/attr_uppercase.html`:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link REL="canonical" HREF="https://example.test/project/a.html">
</head>
<body><p>attr_uppercase positive control</p></body>
</html>
```

Design constraints for this case, so it stays single-axis:

- The `link` **element name is lowercase**; only the **attribute names** are uppercase (`REL`, `HREF`). Tag-name case is a separate parser property and must not be folded in.
- The `rel` **value** is lowercase `canonical` (value case is `rel_uppercase`). The `href` **value** is already the normalized target string, so no relative resolution, `base` precedence, percent-encoding, or host/scheme case normalization is exercised.
- Exactly one explicit `<head>`, one `link`, no `<base>`, no body `link`, no comment/script/template decoy. All other matrix cases keep their own axes.

## Why exit 0 / clean

1. **Attribute names are ASCII case-insensitive in HTML, and the tokenizer lowercases them.** The attribute-name state maps every ASCII upper alpha to its lowercase form before the attribute is stored (§13.2.5.33): "Append the lowercase version of the current input character (add 0x0020 to the character's code point) to the current attribute's name." So `REL`/`HREF` are the same attributes as `rel`/`href`.
2. **`rel` gives link types as a space-separated token list, matched ASCII case-insensitively.** §4.6.8 requires the element's `rel` to be split on ASCII whitespace and states "Keywords are always ASCII case-insensitive, and must be compared as such." The single token here is exactly `canonical`, which §4.6.8.4 defines as the preferred URL for the current document.
3. **One canonical signal in the explicit head.** The element is inside the explicit `<head>`, and no second canonical link exists in head or body; the policy's "exactly one canonical link in explicit head" holds.
4. **The URL matches.** `href` is an absolute `https://example.test/project/a.html`, identical to `expectedCanonical`. Since scheme and host are already lowercase and the path has no dot-segment, encoding, or default-port variation, any normalization the validator applies that is identity on this string yields equality. No fragment and no credentials are present.
5. **Stdlib behavior corroborates parsing, not policy.** Python docs: for `handle_starttag`, "The name will be translated to lower case" (attribute names; §Examples repeats "Attribute names are converted to lowercase"). Local probe on Python 3.14.8 confirmed: feeding `<LINK ReL="canonical" HREF="…">` yields `('link', [('rel', 'canonical'), ('href', '…')])` — tag and attribute names lowercased, values preserved byte-for-byte.

What this case therefore catches is a **false red**: an implementation that scrapes raw source for literal `rel="canonical"` / `href=` or otherwise compares attribute names case-sensitively would miss this valid link and emit `canonical_missing` (exit 1) or `canonical_href_missing`. The frozen expectation must remain exit 0; encoding `canonical_missing` here would bless the bug.

## Adjacent false-green attack (distinct from this case)

**Name:** uppercase-attribute canonical shadow (`attr_case_shadow`).

**HTML** (same manifest `url` and `expectedCanonical` as above):

```html
<!DOCTYPE html>
<html><head>
<link rel="canonical" href="https://example.test/project/a.html">
<link REL="canonical" HREF="https://example.test/project/b.html">
</head><body></body></html>
```

**Real platform behavior:** the second element's attribute names lowercase to the same `rel`/`href`, so it is a second `link` whose `rel` token list contains `canonical`. The page has two canonical links → expected `canonical_multiple`, exit **1**.

**False-green mechanism:** a validator that extracts canonical links by scanning the raw text for lowercase attribute names finds only the first element, concludes "exactly one canonical in head", and returns exit 0 with `findings: []`. A browser/HTML-parser consumer sees two canonical links pointing at different URLs; the page is not clean.

**Why it is distinct:**

- From `attr_uppercase`: that case is one well-formed link with uppercase attribute names and expects exit 0; this attack is two links and expects exit 1. A validator can pass `attr_uppercase` (because `HTMLParser` lowers names) and still fail this attack if any secondary path (e.g. a raw-text pre-scan for duplicates, a hand-rolled tokenizer, or a case-sensitive regex used to locate `<link>` boundaries) bypasses the parsed attribute stream.
- From `duplicate_different`: that matrix case uses uniformly lowercase markup, so the duplicate is visible to any extractor. Here the second canonical is hidden only from case-sensitive extraction, which is the exact weakness `attr_uppercase` nominally probes — making this the attack that converts the case's false-red risk into a false-green consequence.

**Secondary hazard, not counted as the named attack:** duplicate attributes on one tag are first-wins per spec — §13.2.5.33 states that when leaving the attribute-name state "if there is already an attribute on the token with the exact same name, then this is a duplicate-attribute parse error and the new attribute must be removed from the token." Python `HTMLParser` does **not** drop duplicates (local probe: `[('rel','canonical'), ('rel','other'), ('href','a')]`), so `dict(attrs)`/last-wins can false-green a page such as `<link rel="canonical" href="https://example.test/project/other.html" HREF="https://example.test/project/a.html">` (real href = `other.html` → `canonical_mismatch`, exit 1; last-wins sees `a.html` → exit 0). The audit must implement first-wins itself.

## Sources (official, fetched 2026-10-20 UTC)

| ID | Source and locator | Exact text used | Use |
|---|---|---|---|
| S1 | WHATWG HTML Standard, §13.2.5.33 Attribute name state, https://html.spec.whatwg.org/multipage/parsing.html#attribute-name-state (multipage, fetched bytes line 2213) | "Append the lowercase version of the current input character (add 0x0020 to the character's code point) to the current attribute's name." | Tokenizer lowercases attribute names |
| S2 | Same, lines 2219-2223 | "…if there is already an attribute on the token with the exact same name, then this is a duplicate-attribute parse error and the new attribute must be removed from the token." | First-wins duplicate rule (secondary hazard) |
| S3 | WHATWG HTML Standard, §13.1 Writing HTML documents, https://html.spec.whatwg.org/multipage/syntax.html#writing (lines 85-88) | "Many strings in the HTML syntax (e.g. the names of elements and their attributes) are case-insensitive, but only for ASCII upper alphas and ASCII lower alphas." | Normative case-insensitivity framing |
| S4 | Same, §13.1.2.3 Attributes, https://html.spec.whatwg.org/multipage/syntax.html#attributes-2 (lines 256-258) | "In the HTML syntax, attribute names, even those for foreign elements, may be written with any mix of ASCII lower and ASCII upper alphas." | Conforming uppercase names |
| S5 | Same, lines 346-347 | "There must never be two or more attributes on the same start tag whose names are an ASCII case-insensitive match for each other." | Duplicate-name constraint |
| S6 | WHATWG HTML Standard, §4.6.8 Link types, https://html.spec.whatwg.org/multipage/links.html#linkTypes (lines 891-906) | "Keywords are always ASCII case-insensitive, and must be compared as such." | `rel` token match rule |
| S7 | WHATWG HTML Standard, §4.6.8.4 Link type "canonical", https://html.spec.whatwg.org/multipage/links.html#link-type-canonical (lines 1095-1102) | "The canonical keyword indicates that URL given by the href attribute is the preferred URL for the current document." | Meaning of the canonical token |
| S8 | WHATWG HTML Standard, §4.6 link element, https://html.spec.whatwg.org/multipage/semantics.html#the-link-element (lines 406-413) | "If the href attribute is present, then its value must be a valid non-empty URL potentially surrounded by spaces." / "The types of link indicated (the relationships) are given by the value of the rel attribute…" | `link` attribute semantics |
| S9 | Python Software Foundation, "html.parser", https://docs.python.org/3/library/html.parser.html#html.parser.HTMLParser.handle_starttag (accessed 2026-10-20) | "The name will be translated to lower case, and quotes in the value have been removed" | Stdlib lowercases attribute names |
| S10 | Google Search Central, "How to specify a canonical URL with rel=canonical and other methods", https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls (keyword `rel="canonical" link` section; document `rel="canonical"` example) | "A `rel="canonical"` `link` element … is an element used in the `head` section of HTML to indicate that another page is representative of the content on the page." | Publishing-side corroboration of head placement and self-reference; not a parsing rule |

Sibling platform reports in this wave (`HTMLLink.md`, `PythonParser.md`) independently reach the same rel-token and parser-lowercasing conclusions; this report's expectations do not depend on their bytes.

## Remaining unknowns / explicit inferences

- **Verdict string:** the contract only maps exit 0 to "clean" in `exitMap`; the literal JSON `verdict` value `"clean"` is `[INFERENCE]` from that wording. The exit code, `pagesChecked: 1`, and empty `findings` are contract-derived.
- **Fixture literal:** the HTML above is `[INFERENCE]`/recommended. Matrix may place it at any manifest-relative path and may use `<LINK>` or mixed case in the tag name, provided the attribute-name case is the only perturbed axis; expected outcome must stay exit 0 / clean.
- **URL normalization depth:** not exercised by this case. Since the `href` is already the exact expected absolute string, clean holds whether the validator compares raw absolute URLs or WHATWG-normalized ones. No WHATWG URL Standard page was fetched for this seat.
- **Not verified:** the not-yet-existing `scripts/canonical_audit.py`, `matrix.py`, `cases.json`, and `measure.py` at this base (they were absent from the lane and from all tracked files). This report specifies expectations only.

## Checks for L1 (not run by me)

- When Integrate lands `scripts/canonical_audit.py` and `.ufo/waves/round-22/cases.json`, confirm `attr_uppercase` is encoded as exit 0 with no finding id (or the matrix's `clean` sentinel) and uses an uppercase-attribute positive fixture.
- Reject any matrix expectation that maps `attr_uppercase` to `canonical_missing`/exit 1 — that would encode case-sensitive attribute lookup.
- Confirm the duplicate-attribute expectation (if a case is added) is first-wins, and that `duplicate_*` columns use parsed elements rather than raw-text scans; consider the `attr_case_shadow` attack above as an extra acceptance probe.
- Confirm no lane edits beyond this report were made by this seat.
