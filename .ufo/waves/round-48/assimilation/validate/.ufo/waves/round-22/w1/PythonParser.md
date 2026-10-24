# PythonParser — html.parser source scoping (C1 operability)

Seat: KakeR22.PythonParser (read-only scout). No registry/corpus edits. No installs performed.

## Source record

- URL: https://docs.python.org/3/library/html.parser.html
- Accessed: 2026-10-20 (UTC date of this session; page footer states "Last updated on Oct 20, 2026 (20:57 UTC)").
- Page identity: "html.parser — Simple HTML and XHTML parser — Python 3.15.0 documentation"; canonical URL above; PSF License v2.
- Consulted sections (anchors on that page):
  - `#module-html.parser` — module intro and `HTMLParser` constructor.
  - `#htmlparser-methods` — `feed()`, `close()`, `handle_starttag()`, `handle_endtag()`, `handle_startendtag()`, `handle_entityref()`, `handle_charref()`.
  - `#html.parser.HTMLParser.handle_starttag` — attribute contract.
  - `#examples` — lowercase attrs, invalid-markup, charref, raw-text examples.
- Primary quote (11 words, exact page text, emphasis markup omitted; section `#module-html.parser`, paragraph 4):
  > This parser does not check that end tags match start tags
  > — https://docs.python.org/3/library/html.parser.html#module-html.parser (accessed 2026-10-20)

### Supporting exact quotes (each <=25 words, located)

| Locator | Quote (exact text; emphasis markup omitted) | Words |
|---|---|---|
| `#html.parser.HTMLParser.handle_starttag`, sentence 3 | "The name will be translated to lower case, and quotes in the value have been removed" | 16 |
| `#html.parser.HTMLParser.handle_starttag`, final sentence | "All entity references from html.entities are replaced in the attribute values." | 11 |
| `#html.parser.HTMLParser.handle_starttag`, sentence 4 | "For empty attributes, value is None." | 6 |
| `#html.parser.HTMLParser` constructor, `convert_charrefs` paragraph | "all character references (except the ones in elements like script and style) are automatically converted to the corresponding Unicode characters" | 20 |
| `#html.parser.HTMLParser.handle_entityref` / `handle_charref` | "This method is only called if convert_charrefs is false." | 9 |
| `#html.parser.HTMLParser` constructor, opening sentence | "Create a parser instance able to parse invalid markup." | 9 |
| `#html.parser.HTMLParser.feed` | "incomplete data is buffered until more data is fed or close() is called" | 13 |
| `#examples`, raw-text paragraph | "The content of elements like script and style is returned as is, without further parsing" | 16 |

## Scoped teaches (what this source establishes for canonical_audit.py)

1. Tokenizer only, never a tree. The documented callback set (`handle_starttag`, `handle_endtag`, `handle_data`, `handle_comment`, `handle_decl`, `handle_pi`, `unknown_decl`) is a flat event stream; the source explicitly disclaims end/start matching and implicit end-tag dispatch. Therefore "explicit head" and head-bounded scanning MUST be implemented by the audit's own depth/state tracking; the parser will not report an implicit `</head>` or an implied `<head>`.
2. Attribute names are already ASCII-lowercased. `rel`/`href` name matching needs no extra name normalization. Attribute *values* are not lowercased, so `rel="Canonical"` arrives as `Canonical`; the audit must apply its own ASCII case-insensitive rel-token comparison.
3. Character references are decoded inside attribute values regardless of `convert_charrefs`. The `handle_starttag` contract states entity refs are replaced in values, and the `convert_charrefs` switch only governs `handle_data` versus `handle_entityref`/`handle_charref` dispatch in data. Consequence for the `entity_href` case: compare the already-decoded `href`; do not decode twice (`&amp;amp;` must stay `&amp;` after one decode).
4. Absent vs empty `href` are distinguishable. `href` with no value yields `None`; `href=""` yields `''` (confirmed by the docs example `<input TYPE='checkbox' checked required='' disabled=disabled>` producing `('checked', None)` and `('required', '')`). The audit can separate `canonical_href_missing` from `canonical_url_invalid`/empty-string handling on this basis.
5. `script`/`style` content is opaque raw text delivered to `handle_data`, so canonical-link lookalikes inside them cannot produce start tags. This makes `script_decoy` structurally safe without extra filtering.
6. Comments are delivered to `handle_comment`, never as tags, so `comment_decoy` is structurally safe.
7. `handle_startendtag()` defaults to calling `handle_starttag()` then `handle_endtag()`. An audit that overrides both and counts links must not double-count XHTML-style `<link ... />`; overriding `handle_starttag` only still observes exactly one link element.
8. Whole-document feed should end with `close()`; `feed()` buffers incomplete elements. Offline reads can feed the full bytes then close, but see limitation 4 below: `close()` does not guarantee an event for a truncated trailing tag.
9. Successful parsing is not validation. The constructor is documented to "parse invalid markup," and the examples show mismatched nesting and unquoted attributes accepted. The audit must not equate "no exception" with well-formed/HTML5-conformant input; unsupported-shape detection is the audit's responsibility.

## Limitations the source does not remove (must stay explicit in C1)

1. No HTML5 tree construction or conformance claim appears anywhere on this page: no implied `html`/`head`/`body`, no foster parenting, no template-contents semantics, no spec charref error handling. `[INFERENCE]` from the handler-only model plus the explicit non-checking statement.
2. No template inertness. `<template>` gets no special treatment on this page; `[INFERENCE]` it is tokenized like any other element, so `template_decoy` MUST be suppressed by audit-side template-depth tracking, not by the parser.
3. No attribute de-duplication is documented. `[INFERENCE]` duplicate `href`/`rel` pairs survive as separate list entries, so duplicate detection must be audit-side.
4. Truncated trailing markup may be silently dropped even after `close()`; the docs promise buffered-processing semantics, not an error event. The audit cannot rely on the parser to surface `html_unsupported` for truncated input.
5. Nothing here defines canonical policy: no rel="canonical" syntax, base-URL precedence, relative resolution, WHATWG URL normalization, query preservation, credentials/fragment rejection, or Google selection. Those require RFC 6596 / WHATWG URL / Google documentation; this page only bounds parser behavior.
6. Version scope: page is Python 3.15.0 docs; `convert_charrefs` default changed to `True` in 3.5 and `scripting` was added in 3.14.1. Pin interpreter version in evidence; the behaviors cited above are stable for 3.5+ as documented.

## Local behavior corroboration (not a doc claim)

Environment: local `python3` 3.14.8, stdlib only, no writes/network. Observed, to make limitations 2–4 concrete:

```
start link [('rel', 'Canonical'), ('href', '/a?x=1&y=2&z=3'), ('href', '/dup')]
start template []
start link [('rel', 'canonical'), ('href', '/t')]
start script []
data "document.write('<link rel=canonical href=/s>')"
before close: done
after close                      # trailing '<div' produced no event
start a [('href', '/x?a=1&b=2')]
data 't'; ent amp; data 't'      # convert_charrefs=False
```

Confirms: value case preserved; named+numeric refs decoded in attributes; duplicate attrs preserved; template content tokenized normally; script content inert; incomplete trailing tag vanishes. This corroborates, but does not replace, the doc citations above.

## Source status recommendation

- ACCEPT as a primary official source for `html.parser` API semantics (attribute lowercasing/decoding, callback dispatch, non-validating tokenizer behavior).
- Use it to satisfy C1's "HTMLParser stdlib limitations must be explicit" clause and to justify an audit-side head/template/duplicate/truncation state machine; do not cite it for canonical policy, URL normalization, or search-engine selection.
- Cite as: Python Software Foundation, "html.parser — Simple HTML and XHTML parser," Python 3.15.0 documentation, https://docs.python.org/3/library/html.parser.html, accessed 2026-10-20, sections `#module-html.parser`, `#html.parser.HTMLParser.handle_starttag`, `#html.parser.HTMLParser.feed`, `#examples`.
- No registry edits and no corpus changes made by this seat.

## Remaining unknowns

- Exact CPython behavior for pathological inputs (NUL bytes, very long unclosed tags, surrogate handling) is not covered by this page and was not probed; treat as out of scope unless the contract's `html_unsupported` path needs a bounded input policy.
- Whether the project should pin 3.14 versus 3.15 docs is an L1/planner decision; cited behavior is unchanged across those versions per the page's change log.
