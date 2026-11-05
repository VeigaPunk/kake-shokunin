# Round 93 C2 contract — conditional request evaluation (v1)

Frozen before data, together with `.ufo/waves/round-93/c93_conditional.py`. This file is the
declared form a candidate must implement. The counter's own reference is checked against every
worked hand case below before any candidate is scored, so an oracle/contract drift exits 2 rather
than passing silently.

Scope, stated up front: this is a **decision over supplied values only**. It is not a clock, an
HTTP-date parser, a network client, a cache store, a validator generator, or a statement about any
live property. It decides *which status a recipient would answer a conditional request with*, given
a supplied current representation and supplied request precondition values. It does not store,
reuse, freshen, serve, forward or revalidate anything, and it does not claim that any live CDN,
Pages front or Render service evaluates preconditions this way.

Grounding (RFC 9110 §13.2.2, §13.1.1–§13.1.4, §8.8.3.2; RFC 9111 §4.3.2; all opened this round):
a recipient "MUST evaluate the request preconditions ... in the following order"; If-Match "MUST
use the strong comparison function"; If-None-Match "MUST use the weak comparison function"; a
recipient "MUST ignore If-Modified-Since if the request contains an If-None-Match header field" and
if the method "is neither GET nor HEAD"; and, for a cache, "the If-Match and If-Unmodified-Since
conditional header fields are not applicable to a cache".

## Input

One JSON object on stdin, exactly these keys:

```
{"method": <str>,
 "current": {"exists": <bool>, "etag": <str|null>, "last_modified": <int|null>},
 "request": {"if_match": <str|null>, "if_none_match": <str|null>,
             "if_modified_since": <int|null>, "if_unmodified_since": <int|null>},
 "role": <"origin"|"cache", optional, default "origin">}
```

Any other top-level key is refused. `current` and `request` must be objects with exactly the keys
shown. Header values are supplied as the **raw field value** (the string after the colon) so the
list and entity-tag syntax is part of the problem; dates are supplied as integer epoch seconds (the
lane's adapter convention, the same one `scripts/stored_reuse.py` and `scripts/heuristic_freshness.py`
use; no HTTP-date parsing).

## Output

Success: one JSON object on stdout with exactly two keys, exit 0:

```
{"decision": "200"|"304"|"412", "precondition": "<name>"|null}
```

`precondition` names the field that decided the outcome (`if_match`, `if_unmodified_since`,
`if_none_match`, `if_modified_since`), or `null` when no precondition was evaluated. Refusal:
`invalid_input: <reason>` on stderr, exit 1, nothing on stdout.

## Field reading (clauses)

1. **Types.** `method` is a string matching the token syntax of RFC 9110 §5.6.2 (`tchar` = `!` `#`
   `$` `%` `&` `'` `*` `+` `-` `.` `^` `_` `` ` `` `|` `~`, DIGIT, ALPHA), at least one character,
   compared case-sensitively. `exists` is a bool. `etag` is `null` or a string. `last_modified` is
   `null` or an int (not a bool) `>= 0`. `if_match` and `if_none_match` are `null` or the raw field
   value as a string. `if_modified_since` and `if_unmodified_since` are `null` or an int (not a
   bool) `>= 0`, read as epoch seconds. Anything else is a refusal.
2. **Absent representation.** When `exists` is false, `etag` and `last_modified` must both be
   `null`; otherwise a refusal.
3. **Entity-tag syntax.** An entity-tag is `"` *etagc `"` or `W/"` *etagc `"`, where *etagc is any
   character in `!` or `#`–`~` (0x23–0x7E), zero or more. The opaque-tag is the bytes between the
   quotes, compared byte-for-byte. A malformed entity-tag is a refusal.
4. **List syntax.** A precondition field value is `*` or a comma-separated list of entity-tags with
   optional SP/HTAB around each member. An empty member is a refusal. `*` mixed with any other
   member is a refusal. A value that is the empty string or only whitespace is a refusal.
5. **Comparison.** *Strong*: equivalent iff neither tag is weak and the opaque-tags are equal.
   *Weak*: equivalent iff the opaque-tags are equal, regardless of weakness. When `current.etag`
   is `null`, no supplied tag is equivalent to it.
6. **No evaluation before validation.** Clauses 1–4 run for every input, so a malformed field is a
   refusal even when the field would not be evaluated.

## Decision order (first applicable step wins)

7. **Cache role.** When `role` is `"cache"`, `if_match` and `if_unmodified_since` are not evaluated
   (skipped); evaluation starts at step 10.
8. **If-Match** (origin role, present): the precondition is true when the value is `*` and
   `exists`, or when any listed tag strong-matches `current.etag`. True → continue. False →
   `{"decision": "412", "precondition": "if_match"}`.
9. **If-Unmodified-Since** (origin role, `if_match` absent, present): ignored when
   `current.last_modified` is `null`. Otherwise true iff `current.last_modified <= value`. False →
   `{"decision": "412", "precondition": "if_unmodified_since"}`.
10. **If-None-Match** (present): the precondition is false when the value is `*` and `exists`, or
    when any listed tag weak-matches `current.etag`. True → continue. False → `304` when the method
    is `GET` or `HEAD`, else `412`; `precondition` is `if_none_match`.
11. **If-Modified-Since** (method `GET` or `HEAD`, `if_none_match` absent, present): ignored when
    `current.last_modified` is `null`. Otherwise the precondition is false iff
    `current.last_modified <= value` → `{"decision": "304", "precondition": "if_modified_since"}`.
    True → continue.
12. **Otherwise** `{"decision": "200", "precondition": null}`.
