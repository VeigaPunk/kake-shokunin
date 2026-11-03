# Consider these: links outside their original response

**Status: unassimilated reading after hyaku.** Primary source checked 2026-11-03 UTC. This is a candidate for later review, not a deployment or publishing change.

## RFC 9264: standalone links need explicit context

**Original summary.** Linkset represents links in standalone documents, including a JSON format, when embedding them or supplying a large HTTP Link field is impractical. Explicit anchors and non-relative context and target references help preserve meaning outside the original response. Moving a document can otherwise change link interpretation. Third-party link assertions also need an explicit trust decision.

**Exact source.** [RFC 9264](https://www.rfc-editor.org/rfc/rfc9264.html), **July 2022**, Standards Track, DOI 10.17487/RFC9264. The numbered RFC is the fixed publication pin rather than a rolling draft.

**Reading path.** Start with §§3.2–3.3, then §4's self-contained-link recommendations. Read §§4.2.2–4.2.3 for context and target objects, §6 for discovery, and §9 for context loss and third-party assertions.

**Future question.** After hyaku, consider a paper-only comparison for one already authorized publishing surface: a link embedded in a page, conveyed in a response header, or described in a separate document. If that description were saved or moved, could a reader still identify exactly which resource the link describes? Record the anchor, target, publisher and unresolved trust assumption. Do not infer that a relation supplied by another publisher is endorsed by the resource owner.

**Limits and rights.** This proposal establishes neither host support nor search-engine consumption. It is not a replacement sitemap or a reason to alter production headers. The RFC copyright notice applies BCP 78 and IETF Trust Legal Provisions; extracted code components have Revised BSD requirements. Keep later reuse within those terms.

**Novelty.** Existing base-path, crawler and retirement work concerns related publishing questions. The added gap is preserving link context in a separate representation. No RFC 9264/linkset alias appeared in the reviewed inventories or earlier notes.
