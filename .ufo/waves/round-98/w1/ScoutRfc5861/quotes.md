# Located quotes for C2 sourcing — ScoutRfc5861 (round 98 w1, 2026-11-05)

Line numbers are body line numbers of the retained files:
- RFC 5861: .ufo/waves/round-98/sources/rfc5861.txt
  sha256 1193f1c8710af162e1b9fb4250d79bc6dd26497df4caeeaaa8bcb2fefdd2529e;
  the live fetch of 2026-11-05T22:01:17Z is byte-identical (fetch.txt).
- RFC 9111: .ufo/waves/round-96/w1/ScoutRFC/rfc9111.txt
  sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e.

All five quotes are verbatim substrings with line breaks joined to single spaces. None crosses a
hyphenated line wrap (the nearest wrap, "Cache-" / "Control" at lines 105-106, sits before quote 1
begins).

1. RFC 5861 §3 serving window — sentence at lines 105-108, target phrase at lines 107-108;
   section heading "3.  The stale-while-revalidate Cache-Control Extension" at line 104.
   "caches MAY serve the response in which it appears after it becomes stale, up to the
   indicated number of seconds" (20 words)

2. RFC 5861 §4 staleness bound — sentence at lines 180-182, target phrase at line 181.
   "when the cached response is more stale than the indicated amount, the cached response
   SHOULD NOT be used to satisfy the request" (22 words)

3. RFC 5861 §4 error definition — sentence at lines 184-185.
   "an error is any situation that would result in a 500, 502, 503, or 504 HTTP response
   status code being returned" (21 words)

4. RFC 5861 §4 request-directive scope — sentence at lines 175-178, request clause quoted.
   "When used as a request Cache-Control extension, its scope of application is the request
   it appears in" (17 words)
   Paired response clause (lines 176-178), for completeness: "when used as a response
   Cache-Control extension, its scope is any request applicable to the cached response in
   which it occurs" (20 words).

5. RFC 9111 §4.2.4 stale-serving prohibition — sentence at lines 790-793 (continues to line 793).
   "MUST NOT generate a stale response if it is prohibited by an explicit in-protocol
   directive" (15 words)

Tally: 5/5 located.
