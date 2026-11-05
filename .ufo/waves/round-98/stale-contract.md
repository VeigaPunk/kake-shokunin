# Stale-serving extensions decision — contract v1 (kake round 98, C2)

Frozen by the L1 (KakeR98) before any seat runs. Candidate path:
`scripts/stale_extensions.py` (standard library only, Python 3).

Ground: RFC 5861 §3 (stale-while-revalidate), §3.1, §4 (stale-if-error),
§4.1 (opened this round, row S482); RFC 9111 §4.2.4 (serving stale
responses), §5.2.2.2 must-revalidate, §5.2.2.8 proxy-revalidate,
§5.2.2.10 s-maxage, §5.2.2.4 / §5.2.1.4 no-cache, §1.2.2 delta-seconds
(S480); RFC 9110 §5.6.2 token / tchar, §5.6.4 quoted-string (S478).

## Interface

`python3 scripts/stale_extensions.py` reads ONE JSON object on stdin.

- Decided: exit 0, stdout exactly one JSON object with exactly the keys
  `decision` (string) and `staleness` (integer), then a newline.
- Refused: exit 1, stdout empty, stderr begins `invalid_input:`.
- `--selftest` may exist; it is not scored.

## Input object (unknown keys → refuse)

| key | type | required |
|---|---|---|
| `response_cc` | string: the stored response's Cache-Control field value | yes |
| `request_cc` | string: the request's Cache-Control field value | no (default `""`) |
| `freshness_lifetime` | integer ≥ 0 (JSON booleans and floats refused) | yes |
| `current_age` | integer ≥ 0 (same) | yes |
| `event` | `"request"` or `"error"` | yes |
| `error` | integer 100–599 or the string `"network"`; required when `event` is `"error"`, absent or `null` when it is `"request"` | conditional |
| `shared` | boolean (default `false`) | no |

## Cache-Control parsing (both fields)

1. Split on commas outside quoted-strings. Strip SP/HTAB around each element;
   empty elements are skipped.
2. An element is `name` or `name=value`: `name` is 1*tchar; `value` is
   1*tchar or a quoted-string (DQUOTE *(qdtext / quoted-pair) DQUOTE; qdtext
   HTAB / SP / %x21 / %x23-5B / %x5D-7E / %x80-FF; quoted-pair `\` followed by
   HTAB / SP / VCHAR / obs-text). No whitespace around `=`. Anything else (an
   empty value after `=`, an unterminated quote, text after a closing quote, a
   character above U+00FF or a control character) → refuse.
3. Names compare case-insensitively. The FIRST occurrence of a name is used
   (RFC 9111 §4.2.1 allows "the first occurrence").
4. `stale-while-revalidate` and `stale-if-error` values are delta-seconds:
   valid only as an unquoted token of 1*DIGIT; values above 2147483648 are
   clamped to 2147483648 (RFC 9111 §1.2.2). A quoted or non-digit value makes
   that directive **absent** (lane convention).
5. Request directives `max-age`, `max-stale`, `min-fresh`, `only-if-cached`
   are outside this contract → refuse. `stale-while-revalidate` in a request
   is ignored (RFC 5861 defines it for responses only). Storage directives
   (`no-store`, `private`, `public`) and unknown extensions are ignored: this
   tool takes the response as already stored and decides nothing about storage.

## Decision (first rule that applies)

Let `L` = freshness_lifetime, `A` = current_age, `staleness` = max(0, A − L).
`prohibited` holds when the response carries `no-cache` (qualified or not —
conservative lane convention) or `must-revalidate`, or `shared` is true and
the response carries `proxy-revalidate` or `s-maxage`, or the request
carries `no-cache`.

1. `event` is `"error"` and `error` is not 500, 502, 503, 504 or
   `"network"` → `not-an-error` (RFC 5861 §4: an error is a situation that
   would yield 500, 502, 503 or 504).
2. `A < L` and neither field carries `no-cache` → `fresh`.
3. `event` is `"request"`: not `prohibited` and a valid response
   `stale-while-revalidate` value `W` with `staleness ≤ W` →
   `serve-stale-revalidate`; otherwise `revalidate`.
4. `event` is `"error"`: the limit is the request's valid `stale-if-error`
   value when present, else the response's valid value (lane convention: the
   request directive's scope is the request it appears in). Not `prohibited`
   and a limit `E` with `staleness ≤ E` → `serve-stale-error`; otherwise
   `error-through`.

Boundaries are inclusive (RFC 5861 §4: "more stale than the indicated
amount" SHOULD NOT be used; §4.1: usable until the age is greater than 1800
at max-age 600 + 1200). `staleness` is always reported.

Out of scope: computing `L` or `A` (see `scripts/cache_current_age.py`,
`scripts/heuristic_freshness.py`), Warning/Age emission, background
revalidation scheduling, storage, and any live cache behaviour.
