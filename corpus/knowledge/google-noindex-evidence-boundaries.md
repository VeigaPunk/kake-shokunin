source: S436 https://developers.google.com/search/docs/crawling-indexing/block-indexing (Important; Implementing; Debugging); S437 https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag (Using the robots meta tag; Using the X-Robots-Tag HTTP header; Valid indexing and serving rules)
verified-at: 2026-11-02, public documentation bodies retained in .ufo/waves/round-69/sources/receipts.json
recheck: 90d; reopen the two official documents and compare the named sections

# Google noindex: declaration is not an observed indexing outcome

S436 says crawler access is necessary to discover a noindex instruction; a
robots.txt block can prevent discovery without removing an indexed URL.
Its Important notice, retained HTML line 3888, states:

> the page can still appear in search results

Its implementation section supports meta or response-header delivery, not
noindex in robots.txt. Its Debugging section, retained HTML line3971, adds:

> it may take months for Googlebot to revisit a page.

[INFERENCE] A publisher's saved declaration therefore does not establish that
Google has already seen it or removed the URL.

S437 separates crawler applicability from placement. Generic robots and
Googlebot rules can apply to text results; Googlebot-News is scoped to news.
The Using robots meta note, retained HTML line 3963, states:

> will respect robots meta tags in the body section of an HTML document as well.

Head placement is recommended, but body placement alone is not evidence that
Google ignores the rule. The conflicting-rules paragraph under Using the X-Robots-Tag HTTP header favors restrictive rules;
none includes noindex, while nofollow addresses outgoing links. Headers serve
non-HTML resources. The indexifembedded section permits an embedded-content
exception when paired with noindex.

## Publisher review decisions (not a live test)

| Evidence | Bounded decision |
|---|---|
| noindex plus crawl block | Do not promise removal from this declaration. |
| HTML body meta noindex | Do not reject solely for body placement. |
| generic negative plus Googlebot positive | Do not let the positive cancel the negative. |
| non-HTML resource | Inspect response-header evidence, not HTML meta markup. |
| embedding or unfamiliar directives | Escalate interpretation; no blanket noindex conclusion. |

Extraction, crawler identity, delivery variation and actual index state remain
separate observations. No property, browser, account or publishing action was
performed. The proposed round69 automated evaluator was NOT built or admitted;
its finite counter has prebuild conformance defects. This document is retained
source learning, not proof of a new automated capability or round admission.
