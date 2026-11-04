# SOURCES row candidate — S464 (NOT recommended for integration; see ScribeEntry.md §3)

Spec-shaped, 11 cells, for the RFC 9111 plain-text §4.1 URL. The §4.1 ground is
already held by S463 at the httpwg URL, so the recommended integration is to
cite S463 and add no row. This file exists so the duplicate can be tested
against the census rather than argued.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S464 | RFC 9111 — HTTP Caching, §4.1 Calculating Cache Keys with the Vary Header Field — https://www.rfc-editor.org/rfc/rfc9111.txt | spec | A | The stored-response key a presented request maps to under a Vary value, read from the plain-text rendering of §4.1; not storability, freshness, revalidation, reuse or serving | §4.1 title line 526; reuse-condition sentence lines 530–532; wildcard sentence lines 556–557; plain-text body sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e, 84477 bytes, fetched 2026-11-04T21:14:38Z HTTP 200 | Section 4.1 is titled as cache-key calculation and conditions reuse on every presented request field nominated by Vary matching the original request; a wildcard member always fails to match | mined | 2026-11-04 | 180d | corpus/knowledge/cache-key-construction.md |
