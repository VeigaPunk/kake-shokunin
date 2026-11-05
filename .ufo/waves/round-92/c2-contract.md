# Round 92 C2 contract — heuristic freshness decision (v1)

Frozen before data, together with `.ufo/waves/round-92/c92_heuristic.py`. This file is the
declared form a candidate must implement. The counter's own reference is checked against every
worked hand case below before any candidate is scored, so an oracle/contract drift exits 2
rather than passing silently.

Scope, stated up front: this is a **decision over supplied integer seconds only**. It is not a
clock, an HTTP-date parser, a network client, a cache store, a revalidation exchange, or a
statement about any live property. It decides *whether a heuristic freshness lifetime may be
assigned to a stored response and what that lifetime is*; it does not store, reuse, serve or
revalidate anything. It deliberately does not re-decide what `scripts/stored_reuse.py` (round 91)
already decides beyond the freshness lifetime: it reports the lifetime and the heuristic flag, not
a reuse decision.

Grounding (RFC 9111 §4.2.2, opened this round): a cache "MAY assign a heuristic expiration time
when an explicit time is not specified"; it "MUST NOT use heuristics to determine freshness when an
explicit expiration time is present"; heuristics "can only be used on responses without explicit
freshness whose status codes are defined as 'heuristically cacheable' ... and on responses without
explicit freshness that have been marked as explicitly cacheable (e.g., with a public response
directive)"; and "caches are encouraged to use a heuristic expiration value that is no more than
some fraction of the interval since that time. A typical setting of this fraction might be 10%."

Two conventions below are the lane's, not the RFC's, and are marked so: the 10 % fraction (the RFC
gives it only as a "typical setting") and the 86400-second cap (the RFC states a worst-case
constraint but names no value). Everything else is a direct reading of the section.

## Input

One JSON object on stdin, exactly these keys:

```
{"stored": {"status": <int 100..599>, "headers": {<name>: <value>, ...}},
 "now": <int, epoch seconds, >= 0>,
 "shared": <bool, optional, default false>}
```

Any other top-level key is refused. `stored` must be an object. `shared` absent is `false`.

## Output

Success: one JSON object on stdout with exactly three keys, exit 0:

```
{"decision": "<vocabulary member>", "lifetime": <int|null>, "heuristic": <bool>}
```

Refusal: `invalid_input: <reason>` on stderr, exit 1, nothing on stdout.

Vocabulary: `explicit`, `heuristic`, `not-heuristically-cacheable`, `heuristic-undecided`,
`not-storable`.

## Field reading (clauses)

1. **Names.** Header names are matched case-insensitively (ASCII `A`–`Z` only). Two names that
   differ only in case are a refusal (`duplicate header name`).
2. **Values.** A value is trimmed of leading and trailing SP and HTAB and is otherwise byte-exact.
   A value containing CR, LF or NUL is a refusal.
3. **Types.** Every header name is a string, every value is a string; anything else is a refusal.
   `status` must be an int (not a bool) in 100..599, `now` an int (not a bool) >= 0, `shared` a
   bool.
4. **Cache-Control.** Split on `,`; each directive is trimmed of SP and HTAB; its name is
   lowercased (ASCII); an optional `=` introduces a token or a quoted-string argument. An empty
   directive is a refusal. The same directive name twice with different arguments is a refusal.
   Unknown directive names are ignored. A delta-seconds argument (`max-age`, `s-maxage`) must be a
   bare non-negative decimal integer: a quoted or signed form is a refusal.
5. **Date.** Required; a decimal integer in epoch seconds (the lane's adapter convention, the same
   one `scripts/cache_current_age.py` and `scripts/stored_reuse.py` use; no HTTP-date parsing).
   Absent or non-integer is a refusal.
6. **Expires.** Optional; when present a decimal integer in epoch seconds, and may precede `Date`.
7. **Last-Modified.** Optional; when present a decimal integer in epoch seconds.
8. **No arithmetic before validation.** Clauses 1–7 run for every input, so a malformed field is a
   refusal even when the response turns out not to be storable.

## Decision order (first match wins)

9. **not-storable** if any of: `no-store` in the stored Cache-Control; `private` in the stored
   Cache-Control while `shared`; `Vary` present and one of its members is `*`. `lifetime` and
   `heuristic` are `null` and `false`.
10. **explicit** if an explicit expiration is present: `s-maxage` (only when `shared`), else
    `max-age`, else `Expires`. `lifetime` is that value (`s-maxage`/`max-age` as given,
    `Expires - Date` for `Expires`); it may be negative. `heuristic` is `false`. Heuristics are
    never used when an explicit expiration is present.
11. **not-heuristically-cacheable** if no explicit expiration is present and the status is not in
    the heuristically-cacheable set `{200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501}`
    and the stored Cache-Control carries no `public` directive. `lifetime` `null`, `heuristic`
    `false`.
12. **heuristic** if `Last-Modified` is present and `Last-Modified <= Date`:
    `lifetime = min((Date - Last-Modified) // 10, 86400)`, `heuristic` `true`.
    *Lane conventions:* the 10 % fraction and the 86400-second cap. The RFC encourages "no more
    than some fraction of the interval" and calls 10 % a typical setting; it names no cap.
13. **heuristic-undecided** if `Last-Modified` is absent, or `Last-Modified > Date` (a negative
    interval supports no plausible estimate). `lifetime` `null`, `heuristic` `false`.
