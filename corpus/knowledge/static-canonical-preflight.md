source: S020 RFC 6596 section 3 https://www.rfc-editor.org/rfc/rfc6596.html; S021 Google canonical guidance https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls; S026 Python HTMLParser https://docs.python.org/3/library/html.parser.html; S027 Python URL parsing https://docs.python.org/3/library/urllib.parse.html
verified-at: 2026-10-20, documentation opened this round; local behavior has separate committed round22 receipts, not live website verification
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
and nonregular inputs are rejected, not fetched or executed. Prepare the
manifest over actual built/deployable HTML when that artifact exists, not over
an assumed checkout served set (S001–S006, `ghp-served-set.md`). No production
artifact was available or claimed as tested in round22; its fixtures are local,
authorized publisher examples.

| Observation | Meaning | Publisher action |
|---|---|---|
| Exit 0, no findings | Named static pages match declared canonical policy | Retain the JSON receipt with artifact revision; perform remaining operator-owned readiness checks |
| Exit 1, canonical_missing/multiple/mismatch or other policy finding | A supported input violates local policy | Correct the source signal or explicitly justify and change publisher policy; rebuild and recheck |
| Exit 2, input_invalid/html_unsupported | The tool could not evaluate that input safely/within its parser boundary | Repair input or use a proper HTML5/browser audit; never round up to clean |
| Exit 64 | Usage could not be evaluated | Correct arguments; no publishing verdict was made |

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

Normal invocation is read-only and network-free. Selftests and the matrix use
isolated local fixtures. A frozen failure case plus a clean positive control
show the checker can reject the named mistake; neither replaces testing a real
publisher's artifact. No credential, browser, live property or publishing
operation is needed or authorized by this runbook.
