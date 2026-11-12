# Kake: stored fragments are not a complete response

[RFC9111](https://www.rfc-editor.org/rfc/rfc9111.html), June 2022, replaces [RFC7234](https://www.rfc-editor.org/rfc/rfc7234.html), June 2014. The older specification already separated incomplete storage from partial assembly; this is continuity, not invention.

Sections 3.3–3.4 permit retaining an interrupted GET 200 after its complete headers arrive, marked incomplete. A cache lacking range support or understanding of the range unit cannot store incomplete or partial responses.

Retention does not authorize ordinary reuse: an incomplete response can answer only after completion, or for a partial request wholly covered by its stored range. Partial delivery must use 206.

Combining fragments requires the same strong validator and compliance with the referenced client requirements. Matching URLs or contiguous offsets alone do not meet that condition. General cache reuse rules still apply.

For publisher diagnostics, distinguish stored coverage, representation identity and permission to serve. Unlike HEAD freshening, this concerns body assembly. No CDN behavior or implementation was tested.

Publication-time IETF Trust terms apply, including older-contribution restrictions and separate code provisions. Original commentary only.

Reviewed 2026-11-10. Space hold; unassimilated.
