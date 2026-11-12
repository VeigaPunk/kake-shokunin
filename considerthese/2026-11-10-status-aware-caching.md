# Kake: status-aware caching needs a fallback

[RFC7234](https://www.rfc-editor.org/rfc/rfc7234.html), June2014, section5.2.3 explains extension compatibility: unfamiliar directives are ignored while established directives provide fallback behavior.

[RFC9111](https://www.rfc-editor.org/rfc/rfc9111.html), June2022, introduces must-understand. Section5.2.2.3 conditions caching on understanding and implementing the response status code’s caching requirements. It recommends pairing this directive with no-store. An implementing cache that also understands those status requirements should ignore the paired no-store.

This does not require understanding every response header. The older extension model remains useful: a cache unaware of must-understand still sees no-store. Omitting that fallback weakens the intended restriction for older implementations.

Record both directives and the cache’s documented capabilities. Do not treat the exception as general permission to ignore no-store, bypass other storage restrictions, or declare a CDN compliant. No cache tested or deployment changed.

AppendixB identifies the protocol transition; this is not a performance comparison. Both RFCs carry publication-time IETF Trust terms and code-component conditions. Original commentary only, no copied code or examples. Unassimilated reading candidate.
