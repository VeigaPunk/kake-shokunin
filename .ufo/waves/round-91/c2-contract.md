# Round 91 C2 contract — stored-response reuse decision (v1)

Frozen before data, together with `.ufo/waves/round-91/c91_reuse.py`. This file is the
declared form a candidate must implement. The counter's own reference implementation is
checked against every worked hand case below before any candidate is scored, so an
oracle/contract drift exits 2 rather than passing silently.

Scope, stated up front: this is a **reuse decision over supplied values only**. It is not
a Date parser, a clock, a network client, a revalidation exchange, a cache store, or a
statement about any live property. Freshness is computed from integer seconds the caller
supplies; no heuristic freshness is computed (RFC 9111 §4.2.2 permits heuristics, this
contract does not).

## Input

One JSON object on stdin, exactly these keys:

```
{"stored":  {"status": <int 100..599>, "headers": {<name>: <value>, ...}},
 "request": {"method": <string>, "headers": {<name>: <value>, ...}},
 "now": <int, epoch seconds, >= 0>,
 "shared": <bool, optional, default false>}
```

`request.headers` may be absent (treated as `{}`). `shared` absent is `false`.
Any other top-level key is refused. `stored` and `request` must be objects.

## Output

Success: one JSON object on stdout with exactly three keys, exit 0:

```
{"decision": "<vocabulary member>", "freshness_lifetime": <int|null>, "current_age": <int|null>}
```

Refusal: `invalid_input: <reason>` on stderr, exit 1, nothing on stdout.

Vocabulary: `reuse`, `revalidate`, `serve-stale`, `must-revalidate-fail`, `not-storable`,
`heuristic-undecided`, `only-if-cached-miss`.

## Field reading (clauses)

1. **Names.** Header names are matched case-insensitively (ASCII `A`–`Z` only). Two names
   that differ only in case are a refusal (`duplicate header name`).
2. **Values.** A value is trimmed of leading and trailing SP and HTAB and is otherwise
   byte-exact. A value containing CR, LF or NUL is a refusal.
3. **Header map type.** Every name is a string, every value is a string; anything else is
   a refusal.
4. **Cache-Control.** Split on `,`; each directive is trimmed of SP and HTAB; its name is
   lowercased (ASCII); an optional `=` introduces a token or quoted-string argument.
   An empty directive is a refusal. The same directive name twice with different
   arguments is a refusal. Unknown directive names are ignored. A delta-seconds argument
   (`max-age`, `s-maxage`, `min-fresh`, and a `max-stale` value) must be a bare
   non-negative decimal integer: a quoted or signed form is a refusal.
5. **Date.** The `Date` header is required and is a decimal integer in epoch seconds
   (this is the lane's adapter convention, the same one `scripts/cache_current_age.py`
   uses; no HTTP-date parsing). Absent or non-integer is a refusal.
6. **Age.** The `Age` header is optional, default `0`, and must be a non-negative decimal
   integer.
7. **Expires.** Optional; when present it is a decimal integer in epoch seconds, and may
   precede `Date`.
8. **Current age** (adapter convention, from S462's equation set):
   `current_age = max(0, Age) + max(0, now - Date)`.
9. **Freshness lifetime**: `s-maxage` when `shared` is true and the directive is present;
   else `max-age` when present; else `Expires - Date` when `Expires` is present; else
   `null`.

## Decision order (first match wins)

Clauses 1–9 run first: every input is validated and the lifetime derived before any
decision is taken, so a missing or malformed `Date` is a refusal even when the response
turns out not to be storable. Clauses 10–21 then decide.

10. **not-storable** if any of: `request.method` is not `GET` or `HEAD`; `stored.status`
    is not one of `200 203 204 206 300 301 308 404 405 410 414 501`; `no-store` in the
    stored Cache-Control; `no-store` in the request Cache-Control; `private` in the
    stored Cache-Control while `shared`; `Vary` present and one of its members is `*`.
    On `not-storable`, `freshness_lifetime` and `current_age` are both `null` (no
    arithmetic is performed for a response that is not stored).
11. **heuristic-undecided** if the lifetime from clause 9 is `null`.
12. **revalidate** if the request Cache-Control carries `no-cache`.
13. **revalidate** if the stored Cache-Control carries `no-cache`.
14. **revalidate** if the request carries `max-age=N` and `current_age > N`.
15. **revalidate** if the request carries `min-fresh=N` and `lifetime - current_age < N`.
16. **reuse** if `current_age < lifetime` (the response is fresh).
17. **must-revalidate-fail** if the response is stale and the stored Cache-Control carries
    `must-revalidate`, or carries `proxy-revalidate` while `shared`.
18. **serve-stale** if the response is stale, the request carries `max-stale`, and either
    `max-stale` has no argument or `current_age - lifetime <= N`.
19. **revalidate** otherwise (stale, and the client did not accept the staleness).
20. **only-if-cached-miss**: if the request carries `only-if-cached` and the decision from
    clauses 10–19 is neither `reuse` nor `not-storable`, the decision is
    `only-if-cached-miss`.
21. `freshness_lifetime` and `current_age` are reported from clauses 8–9 for every
    decision other than `not-storable`; `freshness_lifetime` is `null` only when clause 9
    yields `null` (or the decision is `not-storable`).

## Worked cases

These are the counter's hand cases; each is checked against the reference implementation
before any candidate is scored. `Date = 1000000` unless stated.

| # | input | decision | lifetime | age |
|---|---|---|---|---|
| 1 | `max-age=60`, GET, now 1000030 | reuse | 60 | 30 |
| 2 | `max-age=60`, GET, now 1000060 | revalidate | 60 | 60 |
| 3 | `max-age=60`, GET, now 1000065, request `max-stale=10` | serve-stale | 60 | 65 |
| 4 | `max-age=60`, GET, now 1000071, request `max-stale=10` | revalidate | 60 | 71 |
| 5 | `max-age=60`, GET, now 1001000, request `max-stale` | serve-stale | 60 | 1000 |
| 6 | `max-age=60, must-revalidate`, GET, now 1000061, request `max-stale` | must-revalidate-fail | 60 | 61 |
| 7 | `max-age=60, proxy-revalidate`, shared, now 1000061, request `max-stale=100` | must-revalidate-fail | 60 | 61 |
| 8 | `max-age=60, proxy-revalidate`, not shared, now 1000061, request `max-stale=100` | serve-stale | 60 | 61 |
| 9 | `max-age=10, s-maxage=100`, shared, now 1000050 | reuse | 100 | 50 |
| 10 | `max-age=10, s-maxage=100`, not shared, now 1000050 | revalidate | 10 | 50 |
| 11 | `Expires: 1000120`, GET, now 1000100 | reuse | 120 | 100 |
| 12 | `Expires: 999900`, GET, now 1000000 | revalidate | -100 | 0 |
| 13 | no lifetime header, GET, now 1000010 | heuristic-undecided | null | 10 |
| 14 | `max-age=60`, GET, now 1000030, request `no-cache` | revalidate | 60 | 30 |
| 15 | `no-cache, max-age=60`, GET, now 1000030 | revalidate | 60 | 30 |
| 16 | `max-age=60`, GET, now 1000030, request `max-age=10` | revalidate | 60 | 30 |
| 17 | `max-age=60`, GET, now 1000030, request `max-age=30` | reuse | 60 | 30 |
| 18 | `max-age=60`, GET, now 1000030, request `min-fresh=40` | revalidate | 60 | 30 |
| 19 | `max-age=60`, GET, now 1000030, request `min-fresh=30` | reuse | 60 | 30 |
| 20 | `max-age=60`, GET, now 1000060, request `only-if-cached` | only-if-cached-miss | 60 | 60 |
| 21 | `max-age=60`, GET, now 1000030, request `only-if-cached` | reuse | 60 | 30 |
| 22 | `max-age=60`, POST, now 1000030 | not-storable | null | null |
| 23 | status 500, `max-age=60`, GET, now 1000030 | not-storable | null | null |
| 24 | `no-store, max-age=60`, GET, now 1000030 | not-storable | null | null |
| 25 | `max-age=60`, GET, now 1000030, request `no-store` | not-storable | null | null |
| 26 | `private, max-age=60`, shared, now 1000030 | not-storable | null | null |
| 27 | `private, max-age=60`, not shared, now 1000030 | reuse | 60 | 30 |
| 28 | `max-age=60`, `Vary: *`, GET, now 1000030 | not-storable | null | null |
| 29 | `max-age=60`, `Vary: Accept`, GET, now 1000030 | reuse | 60 | 30 |
| 30 | `Age: 40, max-age=60`, GET, now 1000010 | reuse | 60 | 50 |
| 31 | `Date: 1000100`, `Age: 5`, `max-age=60`, now 1000000 | reuse | 60 | 5 |
| 32 | `max-age=60`, HEAD, now 1000030 | reuse | 60 | 30 |
| 33 | `max-age=60, foo=bar`, GET, now 1000030 | reuse | 60 | 30 |
| 34 | `max-age=60`, GET, now 1000030, `must-revalidate` fresh | reuse | 60 | 30 |
| 35 | `max-age=60`, `Expires: 1000120`, GET, now 1000030 | reuse | 60 | 30 |
| 36 | `max-age="60"` | refusal | — | — |
| 37 | `max-age=60` and `cache-control: max-age=30` both present | refusal | — | — |
| 38 | a stored header value containing CR | refusal | — | — |
| 39 | `Date` absent | refusal | — | — |
| 40 | `now` negative | refusal | — | — |
| 41 | an unknown top-level input key | refusal | — | — |
| 42 | `stored.status` as a string | refusal | — | — |
| 43 | `max-age=60, max-age=30` | refusal | — | — |
| 44 | `Age: -1` | refusal | — | — |
| 45 | `max-age=60`, POST, now 1000030, request `only-if-cached` | not-storable | null | null |

## What this contract deliberately does not decide

Storage-key identity (`scripts/cache_key.py`, r89), Vary field matching
(`scripts/vary_match.py`, r88), the six-equation current-age arithmetic in isolation
(`scripts/cache_current_age.py`, r87), revalidation exchanges (§4.3), serving stale
without any client directive (§4.2.4's permission, not a client preference), heuristic
freshness (§4.2.2), and any live property's behaviour.
