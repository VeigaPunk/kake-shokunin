```json
{"id":"S020","verdict":"HOLD","fetchIndex":1,"quote":"The target (canonical) IRI MAY: o Specify a relative IRI (see [RFC3986], Section 4.2).","anchorObserved":"Section 3 'The Canonical Link Relation', page 2, bullet list 'The target (canonical) IRI MAY' (text view is one collapsed line)","reason":"Re-fetched rfc-editor HTML still renders RFC 6596 as Category: Informational, April 2012, with Section 3 intact: the target IRI MUST be duplicative or a superset of the context content, and MAY be relative, self-referential, on a different hostname/domain, on a different scheme, or a superset. The teaches' second clause remains a valid reading: Section 3 imposes a content condition and Section 5 only RECOMMENDS verifying duplication, so a static declaration audit cannot establish duplicate/superset content. Scope (preferred-relation semantics, not Standards-Track conformance) matches the RFC's own Informational status disclaimer.","correction":null}
```

Caveat:
- RFC 6596 is an immutable RFC; same number can never drift, so this recheck tests availability + anchor only, not content drift. Status 200, sha256 87a13951ce93195e9a52915e6d170eebd4c48260576b637407bb96ea8c47f5e4, fetched 2026-10-21T15:10:43Z, no retry entry.
- Required corroboration sentence (same Section 3 list): "o Exist on a different hostname or domain." (count 1); superset MUST sentence also present verbatim (count 1).
- Anchor holds literally: "Category: Informational" (1), "3. The Canonical Link Relation" (1), "April 2012" (8 page-runner repeats); row's opened 2026-10-20 is metadata, unchanged.
- Text view is a single collapsed line (11,883 chars from 18,428 HTML bytes), so line-number anchors are unavailable; section/page markers were used instead.
- Used-by consistency: corpus/knowledge/static-canonical-preflight.md:13-16 states duplicated/superset content, relative/self/different-hostname validity, and that guidance is not proof of reachability/duplication — all supported; corpus/lessons/round-22.md:43 quotes the same Section 3 relative-IRI sentence verbatim.
- No corpus or knowledge edits made; no tool installs needed.
