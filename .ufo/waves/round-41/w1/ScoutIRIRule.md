# ScoutIRIRule — non-ASCII vs S102 and RFC 3987

Axis: freshness. No tools installed. No counter run (this seat scored no tool).

Fetches (both GET, both exit 0, both Date: Fri, 23 Oct 2026 09:48:40 GMT):

- https://www.sitemaps.org/protocol.html — HTTP 200, 45292 bytes, sha256 5e7570590fcb92d473d7015c88940a830383b6a61bc6c16be4df51e97f471654. Equals the S102 retained hash (corpus/SOURCES.md:110). Last-Modified: Thu, 15 Dec 2022. Page text still "Last Updated: Monday, November 21, 2016" (protocol.html:1511).
- https://www.rfc-editor.org/rfc/rfc3987.txt — HTTP 200, text/plain, 111190 bytes, sha256 7cc9e3c4e61ea326130d29d959b723209fe3a6c75cdcfb5badbd315d96cd7878. No prior pin in SOURCES. Copies: /fast/scratch/hyaku/kake-r41w1/ScoutIRIRule/.

## Located quotes

S102 escaping section (protocol.html):

- :563-565 "all URLs (including the URL of your Sitemap) must be URL-escaped and encoded for readability by the web server".
- :569-575 "Please check to make sure that your URLs follow the RFC-3986 standard for URIs, the RFC-3987 standard for IRIs, and the XML standard." (anchors split the tokens; visible text matches SCORECARD.md:2684-2685).
- :579-581 "a URL that uses a non-ASCII character (ü)" plus "&". Rendered examples: :583 http://www.example.com/ümlat.php&q=name (source &uuml; / &amp;); :591 same URL ISO-8859-1 and URL-escaped …/%FCmlat.php&q=name; :599 UTF-8 …/%C3%BCmlat.php&q=name; :605 also entity-escaped …/%C3%BCmlat.php&amp;q=name.
- Second naming, text-file bullet :1021-1027, stops at "for IRIs" (no "XML standard").

RFC 3987 (rfc3987.txt):

- :324-327 unreserved "is extended by adding the characters of the UCS … beyond U+007F, subject to the limitations given in the syntax rules below and in section 6.1."
- :363-365 unreserved "expanded to include UCS characters, with the restriction that private UCS characters can occur only in query parts."
- iunreserved replaces unreserved in iuserinfo :403, ireg-name :406, isegment-nz-nc :422-423, ipchar :426-427 (so path segments, and via ipchar also iquery :429 and ifragment :431).
- :433 iunreserved = ALPHA / DIGIT / "-" / "." / "_" / "~" / ucschar.
- :435-440 ucschar = %xA0-D7FF / %xF900-FDCF / %xFDF0-FFEF / %x10000-1FFFD / … / %xD0000-DFFFD / %xE1000-EFFFD.
- :442 iprivate = %xE000-F8FF / %xF0000-FFFFD / %x100000-10FFFD — added only in iquery (:429), not in iunreserved.
- :455-463 rules "the same as" RFC 3986 include IPvFuture = "v" 1*HEXDIG "." 1*( unreserved / sub-delims / ":" ) with ASCII unreserved (:488).
- :577-578 map each ucschar or iprivate to UTF-8 %HH. :974-975 "IRIs MUST NOT contain bidirectional formatting characters (LRM, RLM, LRE, RLE, LRO, RLO, and PDF)." :1588-1591 scheme allows no character beyond US-ASCII. :1596-1602 look-alikes "should be avoided" (§6.1.b), not a grammar reject.

U+00FC (ü) is inside ucschar (%xA0-D7FF). U+0080 is not.

## Statements

- "S102 names RFC 3987" (SCORECARD.md:2684-2688) — holds. Same bytes as the 2026-10-23 pin; the sentence is still at protocol.html:569-575.
- "U+0080 and above stay accepted where RFC 3986 allows unreserved, as RFC 3987 IRI characters" (SCORECARD.md:2687-2688), and the build phrase "non-ASCII code points stay accepted where unreserved stands (RFC 3987 IRI characters)" — overstated.
- The narrower fact that an IRI keeps the RFC 3986 unreserved set and adds ucschar in the productions that switched to iunreserved — holds (rfc3987.txt:324-327, :403-433).

Why overstated, not merely a gloss: ucschar is not "U+0080 and above". It starts at U+00A0 (so U+0080–U+009F are out), skips surrogates U+D800–U+DFFF, skips U+FDD0–U+FDEF and U+FFF0–U+FFFF, skips the *FFFE/*FFFF code point of each other plane, and skips U+E0000–U+E0FFF (in neither ucschar nor iprivate). iprivate is an IRI character class but not where unreserved stands: legal in query only (:364-365, :429, :442). IPvFuture still cites ASCII unreserved (:463). LRM/RLM/LRE/RLE/LRO/RLO/PDF sit inside %xA0-D7FF and so match iunreserved, but section 4 forbids them (:974-975). S102 does not say to leave the raw character in the URL: it requires URL-escaping (:563-565) and shows ü as %FC (ISO-8859-1) and %C3%BC (UTF-8). Only the UTF-8 form is the RFC 3987 section 3.1 mapping (:577-580). Accepting every code point >= U+0080 in every unreserved position accepts values RFC 3987 rejects (U+0080 in a path; U+E000 in a path, userinfo, host, or fragment).

Not checked: "which is the round-40 behaviour" (SCORECARD.md:2688-2689). No tool was scored.

Confidence: high on the fetches, the hashes, and the productions. The judgment is a reading of those lines, not a counter receipt.
