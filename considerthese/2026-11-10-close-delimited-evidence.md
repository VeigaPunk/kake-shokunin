# Kake: connection closure is weak completion evidence

[RFC7230](https://www.rfc-editor.org/rfc/rfc7230.html), June2014, sections3.3.3–3.4, and [RFC9112](https://www.rfc-editor.org/rfc/rfc9112.html), June2022, sections6.3 and8, retain an HTTP/1.1 limitation: close-delimited responses cannot distinguish ordinary completion from interruption by network failure.

Under the applicable framing rules, fewer bytes than Content-Length makes a response incomplete. Chunked transfer remains incomplete without its terminating zero-sized chunk. Conversely, a response without chunked coding or Content-Length can count as complete after connection closure when headers arrived intact and no underlying connection error was indicated.

That protocol classification does not establish that the publisher’s intended representation arrived intact. The specifications therefore recommend length or encoding delimitation when possible; close delimitation chiefly preserves HTTP/1.0 compatibility.

Retain framing mode alongside captured bytes. Do not equate a closed socket with verified content integrity. 

No runtime testing. Both RFCs carry publication-time IETF Trust terms, older-contribution limitations and separate code provisions. Original commentary only; no copied examples. Unassimilated reading candidate.
