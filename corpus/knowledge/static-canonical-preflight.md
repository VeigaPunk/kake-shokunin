source: S020 RFC 6596 section 3 https://www.rfc-editor.org/rfc/rfc6596.html; S021 Google canonical guidance https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls; S026 Python HTMLParser https://docs.python.org/3/library/html.parser.html; S027 Python URL parsing https://docs.python.org/3/library/urllib.parse.html; S028 RFC 9110 sections 4.2.1-4.2.2 https://www.rfc-editor.org/rfc/rfc9110.txt; S029 RFC 3986 section 3 https://www.rfc-editor.org/rfc/rfc3986.txt
verified-at: 2026-10-20 (S020-S027) and 2026-10-21 (S028-S029), documentation opened this round; local behavior has separate committed round22 receipts, not live website verification
recheck: Reopen the cited sections; python3 scripts/canonical_audit.py --selftest; python3 .ufo/waves/round-22/matrix.py --root .

# Static canonical publishing preflight

Coverage-map ground: canonical signals (previously Frontier). This entry owns
publisher-side static-file validation, not browser crawling or search-engine
canonical selection. Original hosting/source-restoration debts are unchanged.

## Signal, recommendation, local policy

RFC 6596 section 3 defines a preferred IRI for duplicated or superset content.
A relative IRI, self-reference, or a different hostname may be valid. Its
single-canonical guidance is not proof that a target is reachable or duplicate.
The offline tool cannot establish either condition.

Google's “Use rel=canonical link annotations” requires the HTML declaration in
the head, recommends absolute URLs while supporting relatives, and ignores
canonical annotations carrying hreflang/lang/media/type. Its “Best practices”
rejects fragment canonicals and explains that JavaScript may affect the signal.
These are Google's documented processing rules, not guarantees that it chooses
the publisher's preference. Absence of a declaration is not inherently a site
error; it is a failure only when the explicit local publishing policy requires
one. Cross-domain canonical is likewise not intrinsically invalid.

The tool deliberately enforces a stricter local policy: one canonical signal,
no fragment or credential-bearing target, an HTTP(S) target and exact agreement
with the manifest's expectedCanonical after its documented URL normalization.
A mismatch is policy failure, not a claim that the URL violates RFC 6596.

## Input and handoff

Create a version-1 manifest beside regular HTML files, for example:

```json
{"version":1,"pages":[{"url":"https://example.test/project/a.html","file":"a.html","expectedCanonical":"https://example.test/project/a.html"}]}
```

Run from this lane:

```sh
python3 scripts/canonical_audit.py --manifest /absolute/path/to/manifest.json --json
```

The manifest names the entire measured population; an omitted page is outside
the result. Paths are relative to the manifest directory; traversal, symlinks
and nonregular inputs are rejected, not fetched or executed. The manifest file
itself must not be a symlink. The directory you name for it is your chosen
location: it is opened once, as given, and every page is resolved from that
same opened directory, so a symlink earlier in your own path is followed
while a symlink inside the manifest-relative page path is not. Prepare the
manifest over actual built/deployable HTML when that artifact exists, not over
an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production
artifact was available or claimed as tested in round22; its fixtures are local,
authorized publisher examples.

| Observation | Meaning | Publisher action |
|---|---|---|
| Exit 0, no findings | Named static pages match declared canonical policy | Retain the JSON receipt with artifact revision; perform remaining operator-owned readiness checks |
| Exit 1, canonical_missing/multiple/mismatch or other policy finding | A supported input violates local policy | Correct the source signal or explicitly justify and change publisher policy; rebuild and recheck |
| Exit 2, input_invalid/html_unsupported | The tool could not evaluate that input safely/within its parser boundary | Repair input or use a proper HTML5/browser audit; never round up to clean |
| Exit 64 | Usage could not be evaluated; stdout is `{"findings":[],"pagesChecked":0,"verdict":"could-not-evaluate"}` (a repeated `--manifest` is a usage error, never "last path wins") | Correct arguments; no publishing verdict was made |

## Parser and proof boundaries

Python HTMLParser lowercases tag/attribute names and decodes attribute entities;
it is not an HTML5 DOM/tree builder. Its docs explicitly say it does not check
matching start/end tags or report all implicit closures (S026). The gate's
explicit-head supported subset and unsupported-shape rejection are therefore
part of the interface, not HTML conformance certification. Comments, raw script
text and template descendants cannot supply a document-head canonical.

The URL module's splitting/joining functions do not perform validation and
cannot be claimed as an exact WHATWG URL implementation (S027). The validator
adds its own stated constraints; successful normalization does not prove URL
identity on a remote server. Query differences remain meaningful local policy
changes; fragments are rejected rather than silently stripped.

A reference that starts with `//` but has an empty authority (`///project/a.html`,
also as a base href) is rejected as `canonical_url_invalid` / `base_url_invalid`.
RFC 3986 section 3 says a path without an authority cannot begin with `//` (S029),
so the reference carries an empty authority, and RFC 9110 sections 4.2.1-4.2.2
require a recipient to reject an http(s) URI with an empty host as invalid
(S028). Python's `urljoin` instead silently inherits the base host, which made
the round-22 build-wave candidate report a false clean (w2/Attack05). Browsers'
WHATWG slash-skipping would read the first path segment as the host; neither
reading equals the document host, so rejection is the conservative policy.

Normal invocation is read-only and network-free. Selftests and the matrix use
isolated local fixtures. A frozen failure case plus a clean positive control
show the checker can reject the named mistake; neither replaces testing a real
publisher's artifact. No credential, browser, live property or publishing
operation is needed or authorized by this runbook.

## Round 23: body markup, live snapshots, corrections (2026-10-21)

Sources: S030 (WHATWG syntax: a slash is allowed only on void or foreign
elements and has no effect on void elements), S031 (WHATWG parsing: in-body
`<svg>`/`<math>` insert foreign elements; breakout tags and integration points
return to HTML rules), S024 (the first base in tree order wins), S026.

The tool is still not an HTML5 tree builder. After an explicitly closed head it
now evaluates, instead of rejecting the whole page:

- SVG/MathML subtrees whose tokens contain no `base`, `head` or canonical-looking
  `link`, and whose end tags match a modelled element stack exactly. SVG/MathML
  `title`/`style`/`script` are tokenized, not treated as HTML raw text, so markup
  hidden there stays visible (SVG `title` is an HTML integration point).
- Self-closed HTML void elements (`<input />`, `<img />`, `<br/>`, …, the 13 names
  in S030). A self-closed non-void element (`<div/>`) stays unsupported.

Still `html_unsupported`: SVG/MathML before the head closes; any `base`, `head`
or canonical-looking `link` token inside SVG/MathML; mismatched or unclosed
foreign end tags; and **any `<base>` after the head**, in or out of foreign
content, because a body base is still the document's first base in tree order
(S024) and would change a relative canonical. Before this fix the round-23
candidate reported six such pages clean (w1/FalsifyForeignContent); a base after
the head was also silently accepted by the round-22 validator.

Also tightened: raw C1 control characters (U+0080–U+009F) in a URL are rejected,
not percent-escaped (w1/BoundaryURLAuthority); a manifest that repeats a page URL
or file is `input_invalid` instead of being counted twice (w1/BoundaryManifestKeys).

### Live snapshot handoff

`python3 scripts/live_snapshot.py --population <pop.json> --out <dir>` issues one
GET per surface (no credentials, cookies or body; ≤5 redirects, each http(s)
without userinfo; 2 MiB; 20 s), stores `fetch.json`, `page.html` for a 2xx
`text/html` response, and an `audit.json` from `canonical_audit.py`. Surface ids
must be one safe path component. `--reaudit` re-runs only the audit over stored
bytes (no network), which is how a validator change is applied without
refetching. A receipt proves the policy result of the bytes served at
`fetchedAt`, not current delivery, rendered DOM (tabi's ground) or search-engine
selection. Round 23's 12 owned surfaces are in
`.ufo/waves/round-23/live/`; `measure_c2.py` reproduces each receipt.

### Corrections to earlier text in this entry

- [r23-correction] "rejects fragment canonicals" overstates S021: Google says it
  generally does not support fragment canonicals; rejecting them is this tool's
  stricter local policy (w1/ReopenGoogleCanonical).
- [r23-correction] "template descendants cannot supply a document-head
  canonical" rests on S025 (template contents are not children of the template),
  which the round-22 text did not cite; it holds for the static input bytes
  only, not for script-cloned template content (w1/ReopenHTMLTemplate).
