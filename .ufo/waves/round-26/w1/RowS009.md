# RowS009 — round 26 freshness recheck

Seat: `KakeR25.RowS009-6`. Row: `corpus/SOURCES.md:17` (S009, tier A, kind code, cadence 365d). Source re-fetched this round: `#1 https://raw.githubusercontent.com/nginx/nginx/release-1.28.0/src/http/ngx_http_core_module.c` — HTTP 200, fetchedAt `2026-10-21T15:10:38Z`, body 147,410 B, sha256 `c58ebede93aa6c790858ce7e14e01f80f3480466ceb9f7d784c1051321cec3fe` (`fetched/S009-1.raw.gz`), text view `fetched/text/S009-1.txt` (113,589 B).

```json
{"id":"S009","verdict":"HOLD","fetchIndex":1,"quote":"etag->value.len = ngx_sprintf(etag->value.data, \"\\\"%xT-%xO\\\"\", r->headers_out.last_modified_time, r->headers_out.content_length_n) - etag->value.data;","anchorObserved":"src/http/ngx_http_core_module.c:1708-1710 inside ngx_http_set_etag (function definition at line 1682); line numbers derived from decompressed raw bytes because fetched/text/S009-1.txt is newline-flattened","reason":"The tag-pinned URL still resolves (200) and the re-fetched bytes place ngx_http_set_etag at 1682 and the ETag sprintf with last_modified_time and content_length_n at 1708-1710; the hex-time/hex-length format and the nginx-only scope still hold.","correction":null}
```

Caveats (≤10 lines):

1. Content is byte-stable at the tag: exactly one `%xT-%xO` in the file, and `ngx_http_set_etag(ngx_http_request_t *r)` sits at line 1682 with the sprintf at 1708-1710, matching the recorded anchor.
2. Immutable tag URL, so this recheck tests availability and anchor placement rather than living-document drift; no newer-edition question arises for a pinned `release-1.28.0` row.
3. The commit pin `481d28cb4e04c8096b9b6134856891dc52ecc68f` is not encoded in the fetched bytes; it is carried from `corpus/lessons/round-20.md:211` (L1 re-verified 2026-10-19). The tag content matches that anchor, but the tag→commit mapping was not re-queried this round to respect the one-GET-per-recorded-URL fetch plan.
4. Hex semantics of `%xT`/`%xO` are defined by nginx's format directives (`src/core/ngx_string.c`), not by this file; the call is consistent with the row's format claim and unchanged.
5. The text view is newline-flattened (sha256 `f81bf1500b4336a0532ad2a61c0ac6194a4753b29e2c6bfd202862b6c82407bf`); the quote is a contiguous substring present exactly once, word-bounded, and line anchors were checked on the raw bytes instead.
6. Scope unchanged: this file is nginx's own ETag implementation and makes no statement about the GitHub Pages backend.
7. Citing entry `corpus/knowledge/ghp-etag-anatomy.md:8-9,22-23` quotes the same format at the same lines; knowledge-entry judgement is a separate seat.
8. Row cells unchanged; HOLD needs no correction and no `[r26-recheck S009 STALE]` block.
9. No tools installed or updated; no builds/tests/linters run; only this report written.
