# CriticC3QuoteTruth

## Axes

C3 freshness (recheck quote truth and pin evidence); the review also checks the Gate's source-boundary/provenance claims. No C1/C2 surface was examined.

## Independent re-open and quote checks

I reopened all ten `.ufo/waves/round-61/recheck/S00N.html` bodies and `receipts.json`. Independently recomputed SHA-256 and byte counts matched the receipt for all ten; all receipts say HTTP 200, fetched 2026-10-27, userAgent `round61`. I checked the Gate lines in `corpus/lessons/round-61.md` (S001–S010, lines 47–56) against the retained bytes. For S002–S010, the listed span is in exactly one collapsed text node and occurs once on the retained page. Unit counts below were independently recounted (all spans are ASCII, so each whitespace token contributes one); every quote is 6–25 units and <=160 characters. S006 required preserving the literal served entity `&#x27;` while parsing text nodes; with that form retained it occurs once in one node.

| Row | Gate quote / observed state | Units (Gate) | Page occurrences; node-bounded | Quote/provenance finding |
|---|---|---:|---|---|
| S001 | No quote; unpinned note records `anchor_moved`, HTTP 200, and keeps `on-release` | — | Candidate quote in ExecC3Quote report: 1; one raw line | Honest carry. Fresh body is the first URL's v4.0.0 `action.yml` (85 lines); `include-hidden-files` is absent, lines 17–20 are outputs, and the referenced Archive step lines 37–39 do not match the cited anchor. Archive steps instead start at 24, 42, 60. Exclusion material remains present, so `anchor_moved`, not `page_changed`, is the defensible distinction. The main-branch second URL was not fetched. |
| S002 | “Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact” | 14 | 1; yes | Valid quote in the v4.0.0 “What's Changed” section. Gate explicitly says the row's v5.0.0 second URL was not fetched; its claim is therefore limited to the fetched primary URL, not a verification of both URLs. |
| S003 | “file in your repository file does not automatically add or remove a custom domain. Instead, you must configure the custom domain” | 21 | 1; yes | Valid, unique span; Gate identifies the publishing-sources/custom-workflow-note scope. |
| S004 | “file must be under 10GB in size and should not contain any symbolic or hard links. For more information, see the” | 21 | 1; yes | Valid, unique span; Gate identifies the upload-artifact section. |
| S005 | “, you must configure a custom domain in your repository settings and at least one” | 15 | 1; yes | Valid, unique span in the apex-domain paragraph; the longer repeated step-4 instruction is not the Gate quote. |
| S006 | “By default, Jekyll doesn&#x27;t build files or folders that:” | 9 | 1; yes | Valid in the retained served-HTML spelling (entity preserved); Gate names the Jekyll section. |
| S007 | “The process by which the GitHub Pages site will be built.” | 11 | 1; yes | Valid, unique span; Gate scopes it to the Get/Update site material. |
| S008 | “For the purposes of this section, we call @dfn{exclusion members} all” | 11 | 1; yes (one raw line) | Valid, unique span. `@node controlling pattern-matching` begins at line 8480 and the next node is 8621, consistent with the named section. |
| S009 | “etag->value.data = ngx_pnalloc(r->pool, NGX_OFF_T_LEN + NGX_TIME_T_LEN + 3);” | 8 | 1; yes (one raw line) | Valid, unique span at line 1682 under `ngx_http_set_etag`; the cited formatter appears at line 1708. |
| S010 | “An entity tag consists of an opaque quoted string, possibly prefixed by a weakness indicator.” | 15 | 1; yes | Valid, unique span; Gate's §8.8.1/§8.8.3 scope and fragment-not-sent note are consistent with the receipt URL/effective URL. |

S001's candidate span is the quote reported by the quote-location seat, not a Gate quote: the Gate correctly uses the unpinned-note form because the row anchor moved. The S001 note's `anchor_moved` wording is supported by the body/line check and it does not turn the present invariant-exclusion material into a page-change claim. S002's multiple-URL ambiguity is also disclosed on its Gate line; only the v4.0.0 URL has a retained body and receipt, while the second v5.0.0 URL remains unverified. Thus neither row falsely represents the unrequested/unfetched URL as checked.

## Counterexample, impact, correction

Strongest counterexample tested: a quote can be page-unique but be made to appear missing by decoding/dropping HTML character references. That initially affected my independent parser for S006; checking the literal retained text-node form `&#x27;` resolved it, and the quoted bytes are present once. It is not a lane defect. No quote-unit, uniqueness, node-boundary, hash/byte, or unpinned-note defect found. Impacted axis: C3 freshness; no adverse counterexample to its Gate quote evidence found. Smallest correction: none indicated by this review. This is a bounded quote/provenance review, not a run of the frozen C3 counter or a claim that the source pages are semantically unchanged beyond the quoted spans.

VERDICT: All ten retained rows independently checked; S002–S010 Gate quotes are unique, node-bounded and within the unit limit, S001 is honestly unpinned as anchor_moved, and S002 discloses its unfetched second URL.
