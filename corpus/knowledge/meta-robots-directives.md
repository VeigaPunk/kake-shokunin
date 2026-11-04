scope: offline declarations in local HTML meta elements; not crawler behaviour or any live property's state

# Page-level robots directives

This entry supports round-78 C3 as corrected by `contract-amendment-1.md` through
`contract-amendment-4.md`. These terms supersede the original contract's head exclusion,
RFC-3339-date-time-only rule, historical vocabulary and tool-side expectations. The amended matrix
has 36 cases; no matrix result is claimed here.

## Sourced rules

Quotes below are exact substrings after whitespace collapse of retained text under
`.ufo/waves/round-78/w1/ScoutSources/`. Each table row names its source, file, located line range
and whitespace-delimited word count. Markup/ABNF code spans are literal quoted source text.

### The metadata channel

| Rule | Source / retained file:line | Exact quote | Words |
|---|---|---|---|
| A head holds document metadata | S450 `whatwg-semantics.txt:93-94` | The head element represents a collection of metadata for the Document. | 11 |
| Named meta belongs where metadata is expected | S450 `whatwg-semantics.txt:1117` | If the name attribute is present: where metadata content is expected. | 11 |
| Metadata names use ASCII case comparison | S450 `whatwg-semantics.txt:1185-1186` | Names are case-insensitive, and must be compared in an ASCII case-insensitive manner. | 12 |
| Missing content has empty value | S450 `whatwg-semantics.txt:1171-1172` | If a meta element has no content attribute, then the value part of the metadata name-value pair is the empty string. | 21 |
| Robots key identifies the declared audience | S449 `google-robots-meta.txt:941-942` | The value of the name attribute (robots) specifies that the rule applies to all crawlers. | 15 |
| Key and rules are case-insensitive | S449 `google-robots-meta.txt:942-943` | Both the name and the content attributes are case-insensitive. | 9 |
| Head placement is recommended | S449 `google-robots-meta.txt:921-922` | Place the robots meta tag in the <head> section of a given page, like this: | 15 |
| Body tags are nevertheless respected by Google | S449 `google-robots-meta.txt:969` | will respect robots meta tags in the body section of an HTML document as well. | 15 |
| Rules combine across content lists and elements | S449 `google-robots-meta.txt:1026-1027` | Multiple rules may be combined in a comma-separated list or in separate meta tags. | 14 |

WHATWG supplies metadata semantics, **not** the `robots` name or its directive vocabulary. Google's
statements about its interpretation are documentation, not observations of a crawler run.

### Vocabulary and conflicts

| Rule | Source / retained file:line | Exact quote | Words |
|---|---|---|---|
| `all` is the unrestricted default | S449 `google-robots-meta.txt:1035` | There are no restrictions for indexing or serving. This rule is the default value | 14 |
| `none` expands to the negative pair | S449 `google-robots-meta.txt:1054` | Equivalent to noindex, nofollow. | 4 |
| `noindex` | S449 `google-robots-meta.txt:1040` | Do not show this page, media, or resource in search results. | 11 |
| `nofollow` | S449 `google-robots-meta.txt:1048` | Do not follow the links on this page. | 8 |
| `nosnippet` | S449 `google-robots-meta.txt:1058` | Do not show a text snippet or video preview in the search results for this page. | 16 |
| `noimageindex` | S449 `google-robots-meta.txt:1195` | Do not index images on this page. | 7 |
| `notranslate` | S449 `google-robots-meta.txt:1185` | Don't offer translation of this page in search results. | 9 |
| Restrictive rule wins | S449 `google-robots-meta.txt:1015-1016` | In the case of conflicting robots rules, the more restrictive rule applies. | 12 |
| `nosnippet` beats a numeric snippet limit | S449 `google-robots-meta.txt:1016-1018` | For example, if a page has both max-snippet:50 and nosnippet rules, the nosnippet rule will apply. | 16 |
| Zero snippet bound means `nosnippet` | S449 `google-robots-meta.txt:1100-1101` | 0: No snippet is to be shown. Equivalent to nosnippet. | 10 |
| Snippet minus one delegates length | S449 `google-robots-meta.txt:1104-1105` | -1: Google will choose the snippet length that it believes is most effective | 13 |
| Video minus one is unlimited | S449 `google-robots-meta.txt:1173` | -1: There is no limit. | 5 |
| Image preview `none` | S449 `google-robots-meta.txt:1133` | none: No image preview is to be shown. | 8 |
| Image preview `standard` | S449 `google-robots-meta.txt:1136` | standard: A default image preview may be shown. | 8 |
| Image preview `large` | S449 `google-robots-meta.txt:1139-1140` | large: A larger image preview, up to the width of the viewport, may be shown. | 15 |
| Malformed numeric values are ignored | S449 `google-robots-meta.txt:1092-1093` | This rule is ignored if no parseable [number] is specified. | 10 |
| Historical rules are ignored | S449 `google-robots-meta.txt:1217` | The following rules aren't used by Google Search and are ignored. | 11 |
| `indexifembedded` has conditional consumer effect | S449 `google-robots-meta.txt:1078-1079` | indexifembedded only has an effect if it's accompanied by noindex. | 10 |

The historical section names `noarchive`, `nocache`, `nositelinkssearchbox` (lines 1223-1236).
Amendment 1 removes them from effective output and adds `meta_robots_ignored_rule` reporting.
`indexifembedded` is recognized and retained as a declaration, including when consumer effect is
conditional; the audit does not simulate that effect. Standalone positive `index`/`follow` tokens
are lane vocabulary: the opened Google rule list names `all`, not that positive token pair.

### Dates

| Rule | Source / retained file:line | Exact quote | Words |
|---|---|---|---|
| Google's accepted date families are broad | S449 `google-robots-meta.txt:1200-1204` | The date/time must be specified in a widely adopted format including, but not limited to RFC 822, RFC 850, and ISO 8601. | 22 |
| Invalid dates are ignored | S449 `google-robots-meta.txt:1205` | The rule is ignored if no valid date/time is specified. | 10 |
| Google's example is date-only | S449 `google-robots-meta.txt:1213` | `<meta name="robots" content="unavailable_after: 2020-09-21">` | 4 |
| RFC 3339 date-time production | S451 `rfc3339.txt:345` | `date-time = full-date "T" full-time` | 5 |
| Full time carries an offset | S451 `rfc3339.txt:343` | `full-time = partial-time time-offset` | 4 |
| Offset grammar | S451 `rfc3339.txt:338` | `time-offset = "Z" / time-numoffset` | 5 |
| Lowercase delimiters are permitted | S451 `rfc3339.txt:347-348` | `the "T" and "Z" characters in this syntax may alternatively be lower case "t" or "z" respectively.` | 17 |

Amendments 1–2 accept RFC 3339 **full-date or date-time**, plus the bounded RFC-822-style form
`[EEE,] D Mon YYYY HH:MM:SS ZONE`. Named zones are `GMT`, `UT`, `UTC`, `EST`, `EDT`, `CST`, `CDT`,
`MST`, `MDT`, `PST`, `PDT`; numeric zones are signed four-digit offsets. Thus Google's date-only
example is accepted, not an invalid value. This selected union is lane policy rather than a
complete implementation of Google's open-ended date sentence.

## Lane policy

- **Head-only scope is rejected.** A matching body tag contributes its rules (amendment 1 A1).
  `meta_robots_tag_outside_head` remains a placement-hygiene finding, not exclusion or a claim that
  Google ignores the declaration. Flip: revise the amended contract, not the source's body sentence.
- **Reporting is policy.** Unknown content tokens are ignored for effect and reported as
  `meta_robots_unknown_directive`; malformed recognized values produce `meta_robots_invalid_value`;
  historical tokens produce `meta_robots_ignored_rule`. The source's other-values-ignored sentence
  concerns user-agent **names**, not arbitrary content tokens. A source explicitly addressing unknown
  content would flip this grounding gap; it would not itself define the audit's finding ids.
- **Parsing and selection are policy.** `agents` defaults to `["robots"]`. Matching names and content
  use ASCII folding; WHATWG directly grounds ASCII comparison for names, but Google's content sentence
  says case-insensitive without specifying ASCII. Split content on commas, trim tokens, ignore empty
  pieces, and report all-empty or missing content as `meta_robots_empty_content`. `http-equiv` without
  a matching `name` is not selected. No opened source defines these empty-token mechanics.
- **Most-restrictive numeric merge is composition [INFERENCE].** Take the smallest non-negative
  snippet/video bound; `-1` is the no-limit sentinel and loses to a concrete bound. The video sentence
  states no limit explicitly, while the snippet sentence delegates choice. Order image previews
  `none`, `standard`, `large`; choose the earliest valid expiration. The source gives the general
  restrictive principle and value descriptions, not this full algorithm. A primary enumeration of
  these precedence rules would flip the composition-only classification.
- **Declared-after-collapse output is policy (amendment 3 C2).** Expand `none` to `noindex,nofollow`,
  and `all` to the lane's `index,follow` tokens. Collapse only declared binary families; do not inject
  a positive counterpart beside `noindex` or `nofollow`. Retain declared non-collapsing tokens.
  Explicit `nosnippet` suppresses numeric snippet/video output; `max-snippet:0` renders as `nosnippet`.
  Amendment 3's frozen g26 nevertheless retains `max-video-preview:-1` beside synthesized `nosnippet`;
  this explicit case distinguishes zero conversion from the general dominance prose. It is a contract
  edge, not a sourced precedence claim. If nothing valid survives (including only ignored or invalid
  tokens), emit `["follow","index"]`. Default output can coexist with findings.
- **No expectation reaches the tool (amendment 2 B1).** Input checks contain id, local path and URL,
  not `expect`. The matrix compares exit, effective output and findings with separate `expect.json`.
  `meta_robots_expected_mismatch` is retired as a tool finding. Sorted output and de-duplicated finding
  ids are serialization policy.
- **Exit alphabet is policy (amendment 4).** Exit 0 means no findings, 1 means any finding, 2 means
  `missing_file`, `duplicate_check_id` or `bad_manifest`, and 64 means usage. Sources define none of
  these process statuses. A clean declared `noindex` exits 0; a correctly read body tag still exits 1
  for its placement finding. The matrix's 36-case predicate also requires selftest success (at least
  40 tests) and all four constants to fail at least one case. No execution result is asserted here.

## Limits

- **No fetch:** read the named local HTML, never request its URL. No live property's declarations were
  inspected by this seat.
- **No `X-Robots-Tag` response headers:** the source document covers that separate channel, but this
  audit does not. Header instruments own it.
- **No rendering or JavaScript:** inspect static markup, not script-created DOM or a separately fetched
  iframe document. No browser-equivalent HTML tree-construction claim.
- **No crawler behaviour:** declared directives and hygiene findings establish no indexing, crawling,
  serving or ranking outcome and no consumer support guarantee.
- **RFC 850 is explicitly unsupported:** it yields `meta_robots_invalid_value`, although Google names
  it. Flip: a contract change and cases that pin RFC 850 acceptance. RFC 822 support is the bounded
  subset above, not its complete grammar; the union does not cover all widely adopted formats.
- **Source volatility:** quotes bind to the scout's retained bytes, not a fresh network response. The
  obsolete `/crawling/docs/specs/robots-meta-tag` URL returned 404 and is a rejected lead; flip: it serves
  the specification again. The admitted Google source is the working Search Central URL below.

source: S449 — https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag — raw sha256 d9fdfe42019fc49ca9f21c2ae1580b8dabf7356b24f6a19043b7021067296b5e; text sha256 b6728f0c73460c78bb2fdc240b14e4538f59f36ab62ba0c230a360bf3fdb1df8; S450 — https://html.spec.whatwg.org/multipage/semantics.html — raw sha256 08058785b3b995ff5c0cefa6edf2e58eb24b2833bba2928f8ee4c378fc7abb02; text sha256 31cfec326e4220d206af8cbe8dcd9cd4313cf9b724e96e1a3d20dcbf9f0f344e; S451 — https://www.rfc-editor.org/rfc/rfc3339.txt — raw sha256 9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a; text sha256 1d35e5292cadacc72542e2161f11458d413108ef111bdfc3a0ee026fec8eb620. All retained at .ufo/waves/round-78/w1/ScoutSources/ with the filenames in the tables.
verified-at: 2026-11-03 — this seat re-opened retained files, not the network
recheck: 90d for S449/S450; 365d for S451; re-locate quotes and hashes when sources change

[r79-correction 2026-11-04] The §Limits line "No `X-Robots-Tag` response headers" (line 123) is superseded for channel ownership only: round 79 lands `scripts/x_robots_tag_audit.py` and `corpus/knowledge/x-robots-tag-header.md` (S452, with S449's header sections), which audit recorded response header fields offline. This entry and the round-78 instrument still do not read that channel.
