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


### Round-23 falsifier clarifications

S030 caveat: a separate trailing solidus has no effect on a void-element start tag; a slash immediately following an unquoted attribute is part of the value (`href=/x/>` means `/x/`). This is not an XML-style self-closing element (w2/ReopenS030).

A clean canonical receipt does not check HTML meta refresh, HTTP redirects, navigation/readiness or rendering. Meta refresh does not alter the declared canonical href/base, so a refresh page can match the local canonical policy while remaining unfit to publish; never treat that result as publication approval (w2/CritRelaxationProbe disagreement).

The snapshot producer now opens output leaves no-follow relative to an opened directory, rejects non-regular or multiply linked leaves, and verifies stored body length/digest before re-audit. Missing or altered capture data is input error, not not-served. The counter reproduces captures, not the network event: GET provenance is in the producer invocation and independent seat observations.

## Receipt replay hardening — round 24 (2026-10-21)

Sources: S032 (RFC3339 §5.6–5.7), S033 (RFC9110 §8.3.1 and §5.6.6), S034 (RFC8259 §3/4/6/9), all opened this round. The former lexical timestamp prefix comparison accepted malformed and future strings; an untyped Content-Type could crash the historical counter. The round-23 producer fix did not fix that separate reader.

Run the maintained reader from the lane root:

```sh
python3 -B scripts/receipt_replay.py c1 --root . --revision <commit> --json
python3 -B scripts/receipt_replay.py c2 --root . --revision <commit> --json
python3 -B scripts/receipt_replay.py --selftest
```

Both modes retain round23's digest-pinned populations, baseline anchors, heading and canonical replay. Exit0 means all named receipts pass, exit1 means at least one named rejection, exit2 unreadable inputs/usage or a caught internal error (one-line stderr, never a Python traceback). They read Git blobs and create only isolated temporary validator inputs; they do not GET, publish, edit source trees, or renew observation times. Raw revision options are resolved once to a commit object before blob reads.

The field-specific local policy is explicit:

- c1 observedAt permits RFC3339's full-date production as well as date-time, preserving historical date-only observations. c2 fetchedAt requires date-time with offset. Values are parsed, not prefix-compared: real calendar/clock fields, ASCII digits, UTC lower bound 2026-10-21 and no later than the revision's committer instant (UTC date for date-only observations). Date-only support and the bounds are lane policy, not an assertion that RFC3339 date-time is date-only. Runtime-supported calendar/seconds are the local profile; leap-second spellings are not evaluated as valid instants.
- contentType permits null for an omitted header (not-served) or an HTTP media-type string. Type/subtype comparison is case-insensitive; semicolon parameters may be empty under RFC9110; field OWS is trimmed. Other JSON types and malformed media-type strings reject cleanly. Status/byte counts exclude booleans and audit comparison is recursively type-strict, so false cannot impersonate exit0 or true a count1.
- JSON duplicate names are rejected as local integrity policy (RFC8259 says SHOULD-unique, not MUST). Non-standard NaN/Infinity, invalid encodings and runtime number/depth overflows reject without traceback. Unknown metadata members remain allowed; valid controls are not rejected merely for extra fields.
- Redirect endpoints must be safe absolute HTTP URLs without controls or userinfo. A body stored for a response that cannot carry content (204/205) is rejected; canonical replay still distinguishes reproducibility from clean policy.

Round24's malformed-case counter is `python3 -B .ufo/waves/round-24/measure_c2.py --root . --revision <commit> --json` (selftest: same script with `--selftest`). It grades 130 frozen single-file mutations/controls in a clone reset to the round23 fixture base. New runner bytes come from the measured revision; if absent there, the historical round23 runner supplies the actual before instrument. Population digest and the selection register are committed.

Historical round23 commands and their evidence remain valid at their named revisions; the current maintained entry point above supersedes them for new structural replay. Acceptance authenticates neither the GET event nor a claim's truth; producer observations and non-author review still carry that authority. A failed-policy canonical result is not receipt incompleteness, and receipt completeness is not publication readiness.

## Round-26 source recheck

- Round-26 source recheck (2026-10-21, append-only; original lines unchanged). Rows S020, S021, S026, S027, S028, S029, S030, S031, S032, S033 and S034 were re-fetched by one public GET each (`.ufo/waves/round-26/fetched/manifest.json`, S008 via `manifest-retry.json`) and judged HOLD at their anchors against the retained bytes; receipts `.ufo/waves/round-26/rechecks/S0NN.json`, statement-level reviews `.ufo/waves/round-26/w1/Pair*.md`. Older verified-at/reopened dates in this entry remain the historical record of the earlier reading; they are not rewritten. Pointers labelled `at base cb807bc` stay base-scoped (QUALITY.md round-21 coordinate rule), so current-tree line movement is not a stale claim. Counting command: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`.

- [r26-recheck S021 STALE] Line 25's “Cross-domain canonical is likewise not intrinsically invalid” is not stated by S021: the 2026-10-21 re-fetch has no cross-domain canonical statement and defers annotation semantics to RFC 6596. Read it as an S020 claim (RFC 6596 §3: the target IRI MAY “Exist on a different hostname or domain.”). The fragment wording at line 21 remains governed by the existing [r23-correction] at lines 140-142. Evidence: w1/PairS021StaticCanonicalPrefl.md.

- [r26-recheck S026 STALE] Line 69's “or report all implicit closures (S026)” overstates S026: the 2026-10-21 page limits its sentence to elements “closed implicitly by closing an outer element”. The page now labels itself Python 3.15.1 documentation (S026 and S027 alike); the 3.15 family and the relied-on sentences are unchanged. Evidence: w1/PairS026StaticCanonicalPrefl.md, w1/PairS027StaticCanonicalPrefl.md.

- [r26-recheck S030 STALE] Line 110's “Self-closed HTML void elements” misuses S030's term: §13.1.2.1 says that on void elements the trailing solidus “does not mark the start tag as self-closing”; it marks self-closing only on foreign elements. Read: void-element start tags with a trailing solidus (the 13 names in §13.1.2) are evaluated after the closed head. Evidence: w1/PairS030StaticCanonicalPrefl.md (C-1).

- [r26-recheck S030 STALE] Line 111's “A self-closed non-void element (`<div/>`) stays unsupported” keeps the right outcome with the wrong label: a trailing solidus is permitted only on void or foreign elements, so `<div/>` is outside the S030 start-tag grammar and stays unsupported. `scripts/canonical_audit.py:108` uses the same informal label; behaviour is unchanged. Evidence: w1/PairS030StaticCanonicalPrefl.md (C-2).

- Version note (not STALE): the RFC Editor info page reports RFC 3339 (S032) as updated by RFC 9557, which revises the unknown-local-offset convention of §4.3 and keeps the §5.6 grammar this entry relies on (w1/PairS032StaticCanonicalPrefl.md). A new source row is needed before any claim depends on RFC 9557.

### Round-26 falsify-wave adjudication (2026-10-21, append-only)

- [r26-recheck S024 STALE] Line 101's “S024 (the first base in tree order wins)” drops S024's attribute scope. The 2026-10-21 bytes read “If there are multiple base elements with href attributes, all but the first are ignored” and “A base element that is the first base element with an href content attribute in a document tree has a frozen base URL”. A `base` with only `target` does not set the document base URL. Evidence: w2/UncoveredS024S025.md.
- [r26-recheck S024 STALE] Lines 115-117 justify rejecting any `<base>` after the head because “a body base is still the document's first base in tree order (S024)”. Under S024 a later `base[href]` is ignored when a head `base[href]` exists, and a `base` tag inside SVG/MathML content is a foreign element, not S024's HTML `base`. The blanket `html_unsupported` outcome is this tool's conservative local policy (also consistent with “There must be no more than one base element per document”); it is not S024's tree-order rule. Tool behaviour is unchanged. Evidence: w2/UncoveredS024S025.md.
- S025 HOLD: the [r23-correction] at lines 143-146 matches the 2026-10-21 bytes (“The template contents of a template element are not children of the element itself”). S024 and S025 were re-fetched this round (receipts HOLD) but were missing from the recheck paragraph's row list above.
- Reclassified as a precision note (not STALE): the S026 block. Line 69's “does not … report all implicit closures” is weaker than, and consistent with, S026's sentence that the parser does not “call the end-tag handler for elements which are closed implicitly by closing an outer element”. Ledger: `reclassified: 1` (w2/Correction6S026.md).
- Reclassified as precision notes (not STALE): both S030 blocks. “Self-closed” is the WHATWG parsing section's vocabulary (S031: a trailing solidus sets the tag token's “self-closing flag”; an unacknowledged flag on a non-void element is the parse error `non-void-html-element-start-tag-with-trailing-solidus`). Lines 110-111 cite S030 only for the 13 void names. The S030 syntax wording (“does not mark the start tag as self-closing”) remains the precise reading, and line 151 already gives it. Ledger: `reclassified: 2` (w2/Correction7S030.md, w2/Correction8S030.md).
- S021 note: the line-21 fragment wording was STALE at base and is already corrected by the [r23-correction] at lines 140-142; the ledger records it as `staleAlreadyCorrected: 1`, not as a rejected finding (w2/Rejection10S021.md).

## Round-27 grouped-citation adjudication (2026-10-21)

The recommendation at lines52–54 is **local publisher policy / synthesis**:
when an actual built/deployable artifact exists, derive the manifest from its
HTML rather than assuming a checkout listing is the deployed set. It does
not assert that every build differs from its checkout, or that any one
source prescribes a canonical manifest. No production artifact or website
is evaluated by this documentary recheck.

All six members of the original S001–S006 range were opened and individually
judged this round; the omitted range is not reduced to its endpoints.
Observed received-body digests/access times and separately retained public
representations: `.ufo/waves/round-27/fetched/manifest.json`. HTML is retained
only as visible text: original attributes/received bytes are not retained,
not reconstructable, and not claimed byte-identical. Plain action source
may retain received bytes verbatim as the manifest explicitly distinguishes.
Located source-specific judgments: `.ufo/waves/round-27/pairs.json` and its
named A/B reports. This repairs new round27 evidence, not round26 admission:
the earlier41-pair/313-unit ledger remains unchanged and its omission remains
part of that rejected round's record.

| Row | Contribution to the original recommendation | Located support (≤25 words) |
|---|---|---|
| S001 | HOLD, limited premise: the action archives a configured directory and excludes paths; checkout membership is not sufficient. | v4.0.0 action.yml, `inputs.path`: `description: "Path of the directory containing the static assets." required: true default: "_site/"`; archive exclusions are at lines29–36. |
| S002 | HOLD, limited premise: artifact membership depends on version and hidden-file settings. | v4.0.0 release, What's Changed: “Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact”. |
| S003 | HOLD, limited premise: branch/source-folder selection and optionally built uploaded static files define publishing inputs. | Creating a custom GitHub Actions workflow, flow steps3–4: “If required by your site, build any static site files. Use the actions/upload-pages-artifact action to upload the static files as an artifact.” |
| S004 | HOLD, limited premise: the deployment artifact is a packaged unit; this alone does not prove checkout divergence. | Configuring the upload-pages-artifact action: “The GitHub Pages artifact should be a compressed gzip archive containing a single tar file.” |
| S005 | Rejected as support for this HTML-membership sentence; the source's own domain-configuration teaching still holds. | Configuring an apex domain, step4: “If you are publishing from a custom GitHub Actions workflow, no CNAME file is created”. |
| S006 | HOLD, limited premise: Jekyll branch builds have default exclusions, modifiable by include/exclude settings; not every workflow uses Jekyll. | Configuring Jekyll: “By default, Jekyll doesn't build files or folders that: Are located in a folder called /node_modules or /vendor”. |

- [r27-recheck S005 STALE] The source range at line54 over-includes S005.
  It describes custom-domain/CNAME configuration, not which built HTML files
  populate a manifest. A proposed extra host-component leg is not in the
  original sentence and is not invented to save the attribution. Read the
  recommendation as local synthesis supported by the scoped premises from
  S001, S002, S003, S004 and S006 above; no CNAME servedness conclusion follows.
- The line2 S020–S027 metadata band records historical opening dates, including
  S022 and S023, not fresh round27 observations or individual support for
  every body claim. Their registry/round22 records support the dates.
  The line184 S008 retry aside is historical artifact provenance only, not
  GNU-tar support for this entry. All three pairs are explicitly adjudicated.
- Prior UNVERIFIABLE statement units remain disclosed; the new pair-completeness
  count does not promote them to HOLD or establish perpetual source freshness.
