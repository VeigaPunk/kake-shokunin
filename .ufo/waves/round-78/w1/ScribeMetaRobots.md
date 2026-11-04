PASS — C3 knowledge and three mined registry rows completed against amendments 1–4; final census exits 0.

## Behavior, axes and scope

Axes: calibration, freshness, operability. This seat advances sourced operability documentation only; it makes no C1/C2 verdict or score claim. Touched surfaces: `corpus/knowledge/meta-robots-directives.md`, new `corpus/SOURCES.md` rows S449–S451, this report and its census receipt. Existing S032 was temporarily extended then restored; temporary registry prose and a provisional rejected S451 row were removed. Final S451 is RFC 3339 as the scout proposed. No product code, README, PROVINCE, commits, network fetches or tool installations.

The scout report was absent on first read; retained files were already present. It was subsequently re-opened in full along with all four amendments. Final entry replaces the obsolete initial-contract interpretation: body tags contribute, historical tokens are ignored with a finding, date-only and bounded RFC822 forms are accepted, RFC850 is unsupported, no expectations reach the tool, output is declared-after-collapse, 36 cases, finding exits are 1.

## Rows added

| id | URL | Why |
|---|---|---|
| S449 | https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag | Google's vocabulary, conflict sentence, body handling and date forms; not arbitrary unknown-content handling or observed crawler behaviour |
| S450 | https://html.spec.whatwg.org/multipage/semantics.html | Head/meta semantics and ASCII metadata-name comparison; not the robots name or directive syntax |
| S451 | https://www.rfc-editor.org/rfc/rfc3339.txt | Date-time grammar used by the selected date profile; not a source binding unavailable_after to RFC3339; distinct application from S032 |

All three are mined, opened 2026-11-03, 11 columns, used-by `corpus/knowledge/meta-robots-directives.md`. S450 and S451 reuse documents across distinct scopes and therefore add W04 warnings.

## Gates and exact outcomes

Final command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` — exit **0**, W04 **19** (baseline 17; final +2), no errors. Full stdout/stderr: `ScribeMetaRobots/census.txt` (also reproduced below).

Quote check run in Python Eval: split each sourced table row into cells; reopen its retained file; collapse whitespace; require the quote inside the stated line range, actual word count equal to its recorded count, and count ≤25. Exit equivalent: all assertions succeeded; 34 quotes located. This is this seat's direct retained-byte check, not a matrix or canonical quote-truth-counter result. Earlier draft-only checks found 48 candidate quotes and later 53 prose spans; those draft counts are not the final count. One draft checker piped into head raised BrokenPipeError; no source-truth failure was suppressed. A composite shell ending with a no-match grep exited 1 despite its enclosed census returning 0; final standalone receipt removes that ambiguity.

No C3 audit/matrix/selftest was run by this seat. L1 retains integration verification.

## Every admitted quote

Locations below are relative to `.ufo/waves/round-78/w1/ScoutSources/`. Code delimiters are presentation only; quotes are exact after whitespace collapse.

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
| Google's accepted date families are broad | S449 `google-robots-meta.txt:1200-1204` | The date/time must be specified in a widely adopted format including, but not limited to RFC 822, RFC 850, and ISO 8601. | 22 |
| Invalid dates are ignored | S449 `google-robots-meta.txt:1205` | The rule is ignored if no valid date/time is specified. | 10 |
| Google's example is date-only | S449 `google-robots-meta.txt:1213` | `<meta name="robots" content="unavailable_after: 2020-09-21">` | 4 |
| RFC 3339 date-time production | S451 `rfc3339.txt:345` | `date-time = full-date "T" full-time` | 5 |
| Full time carries an offset | S451 `rfc3339.txt:343` | `full-time = partial-time time-offset` | 4 |
| Offset grammar | S451 `rfc3339.txt:338` | `time-offset = "Z" / time-numoffset` | 5 |
| Lowercase delimiters are permitted | S451 `rfc3339.txt:347-348` | `the "T" and "Z" characters in this syntax may alternatively be lower case "t" or "z" respectively.` | 17 |

## Rejects, limits and flip conditions

- Former Google `/crawling/docs/specs/robots-meta-tag` URL: retained HTTP404 error body, not source evidence. Flip: it serves the specification again. No network retry by this seat.
- Head-only exclusion: contradicted by Google's body sentence; amendment1 respects body rules and keeps a lane hygiene finding. Flip: amended contract changes, not a reinterpretation of the source.
- Exclusive RFC3339 date-time acceptance: rejected by the broad source sentence and its date-only example. Final policy accepts full-date/date-time and bounded RFC822; RFC850 remains explicitly unsupported. Flip: new contract/cases implementing that grammar.
- Arbitrary unknown-content values ignored as a sourced fact: refused; the nearest other-values sentence concerns names. Flip: primary text explicitly describes unknown content. Reporting ids remain lane policy.
- WHATWG defines robots: refused; opened document gives metadata mechanics, not that name. Flip: a retained WHATWG paragraph defines robots.
- Standalone positive index/follow as Google rule names: not established by the opened rule list. Flip: primary rule-list evidence names them. They remain lane vocabulary.
- Per-family numeric order, earliest-date selection, ASCII content folding, empty-token mechanics and exits: lane policy/composition, not verbatim sourced algorithms. Flip: corresponding primary algorithm text; process exits remain tool policy.
- Historical noarchive as current Google effect: rejected; final entry follows amendment1 ignored_rule treatment. indexifembedded is now recognized.
- Contract edge retained verbatim in meaning: amendment3 C2 says synthesized nosnippet participates in dominance, but its frozen g26 retains max-video-preview:-1 beside synthesized nosnippet. The entry records that explicit case/prose edge without claiming a sourced ordering or silently choosing a different case expectation.

No fetch, headers, rendering, crawler simulation or live-property claim. Scratch probes did not create a fixture repo. Scratch cleanup is performed before yield; retained census is copied first.

## Provenance hashes

| retained file | bytes | sha256 |
|---|---|---|
| `google-robots-meta.raw` | 208195 | `d9fdfe42019fc49ca9f21c2ae1580b8dabf7356b24f6a19043b7021067296b5e` |
| `google-robots-meta.txt` | 27619 | `b6728f0c73460c78bb2fdc240b14e4538f59f36ab62ba0c230a360bf3fdb1df8` |
| `whatwg-semantics.raw` | 333092 | `08058785b3b995ff5c0cefa6edf2e58eb24b2833bba2928f8ee4c378fc7abb02` |
| `whatwg-semantics.txt` | 97899 | `31cfec326e4220d206af8cbe8dcd9cd4313cf9b724e96e1a3d20dcbf9f0f344e` |
| `rfc3339.raw` | 35064 | `9ab2b8864a85dca73a88f49b0927bc7bc85f596926e4fd1890905777924e700a` |
| `rfc3339.txt` | 28229 | `1d35e5292cadacc72542e2161f11458d413108ef111bdfc3a0ee026fec8eb620` |
| `google-robots-meta-contract-url-404.raw` | 47502 | `c08c232f5f3d4b01608d863bbd727d05d787b3c2d162de6ccab81f739a4b1e23` |

## Census output (final)

```text
COMMAND: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake
EXIT: 0
W04_COUNT: 19
STDOUT:
kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes
kake	W04	S088 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S092 duplicate url html.spec.whatwg.org/multipage/syntax.html across scopes
kake	W04	S098 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S099 duplicate url www.rfc-editor.org/rfc/rfc9309.html across scopes
kake	W04	S102 duplicate url www.sitemaps.org/protocol.html across scopes
kake	W04	S110 duplicate url www.w3.org/TR/xml across scopes
kake	W04	S111 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S115 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S116 duplicate url docs.python.org/3/library/urllib.parse.html across scopes
kake	W04	S117 duplicate url www.rfc-editor.org/rfc/rfc3986.txt across scopes
kake	W04	S127 duplicate url www.rfc-editor.org/rfc/rfc9844.txt across scopes
kake	W04	S416 duplicate url ziyuan.baidu.com/college/courseinfo?id=1399 across scopes
kake	W04	S417 duplicate url ziyuan.baidu.com/college/courseinfo?id=267&page=15 across scopes
kake	W04	S427 duplicate url developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers across scopes
kake	W04	S433 duplicate url www.rfc-editor.org/rfc/rfc9110.html across scopes
kake	W04	S445 duplicate url html.spec.whatwg.org/multipage/links.html across scopes
kake	W04	S450 duplicate url html.spec.whatwg.org/multipage/semantics.html across scopes
kake	W04	S451 duplicate url www.rfc-editor.org/rfc/rfc3339.txt across scopes
kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md
STDERR:
```

## Self-evaluation

Accuracy 4 — every final quote checked at its stated retained line; canonical matrix not run here. Completeness 4 — documentation and required census complete; C3 execution belongs to L1. Clarity 4 — policies separated from source tables; amendment3 g26 edge needs care. Actionability 4 — exact registry ids, quotes and census receipt retained. Conciseness 3 — full quote inventory is necessarily longer than the short verdict. Overall 3.8; prioritize the amended g26 interpretation in integration review, avoid conflating process gates with source truth, keep this exhaustive inventory in the report. User agreement is expected only for this scoped documentation result, not overall round admission.
