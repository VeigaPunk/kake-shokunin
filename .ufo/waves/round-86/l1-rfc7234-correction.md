# Round 86 — historical attribution correction

L1 opened https://www.rfc-editor.org/rfc/rfc7234.txt on 2026-11-04, after freezing. RFC 7234 §4.2.1 (page 13) says: “the directive's value is considered invalid.” Located context: more than one value for a given directive (multiple Cache-Control max-age values); caches encouraged to consider invalid freshness information stale.

This supersedes the frozen contract/L1 receipt sentence attributing a most-restrictive duplicate rule to RFC 7234. That attribution was false. RFC 9111 §4.2.1 does say first occurrence or stale; choosing first occurrence remains the frozen local calculator convention. Case 15 discriminates first from minimum, not RFC9111 from a supposed RFC7234 minimum algorithm. No frozen counter, target or expected output is changed. Production teaching must not repeat the false historical comparison. Captured-by: L1 direct primary-source re-open; source-grounding/located-quote rule.
