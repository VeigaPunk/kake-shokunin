---
source: S478 (RFC 9110 §5.6.1.2, §5.6.3 — https://www.rfc-editor.org/rfc/rfc9110.txt), S455 (RFC 9110 §8.8.3 — https://www.rfc-editor.org/rfc/rfc9110.txt), S034 (RFC 8259 §4 — https://www.rfc-editor.org/rfc/rfc8259.txt), S479 (RFC Editor errata for RFC 9110 — https://www.rfc-editor.org/errata_search.php?rfc=9110)
verified-at: 2026-11-05
recheck: 180d
ground: freshness -- conditional-request evaluation semantics under contract v2: list membership, entity-tag characters, and the GET/HEAD method filter.
scope: what the RFCs decide for the conditional-request evaluator (empty list elements, obs-text in an opaque-tag, duplicate JSON member names, the 304/412 method split) and which of contract v2's clauses are lane conventions rather than RFC requirements; not entity-tag comparison functions, not cache handling, and not the round's own candidate implementation.
---

# Conditional-request evaluation: list membership, entity-tag characters, and method filters

**List membership (contract v2 clause C1; RFC 9110 §5.6.1.2).** A recipient must
accept lists that carry empty elements:

>    Empty elements do not contribute to the count of elements present.  A
>    recipient MUST parse and ignore a reasonable number of empty list
>    elements: enough to handle common mistakes by senders that merge
>    values, but not so much that they could be used as a denial-of-
>    service mechanism.  In other words, a recipient MUST accept lists
>    that satisfy the following syntax:

```
    #element => [ element ] *( OWS "," OWS [ element ] )
```

Empty members therefore contribute no members, and the lane accepts and
ignores them: a list of only empty members decides as the empty list and
matches nothing. A whitespace-only field value is not a list and stays
refused, and `*` mixed with tags stays refused. The whitespace around a
member is OWS:

```
    OWS            = *( SP / HTAB )
```

**Entity-tag characters (clause C2; RFC 9110 §8.8.3, re-read this round).** An
opaque-tag may carry obs-text:

```
     etagc      = %x21 / %x23-7E / obs-text
                ; VCHAR except double quotes, plus obs-text
```

with obs-text defined in §5.5 as

```
     obs-text       = %x80-FF
```

so obs-text (0x80-0xFF) is accepted inside an opaque-tag, while other control
characters stay refused.

**Method filters (clause C5; RFC 9110 §13.1.2 and §13.1.3).** A matching
If-None-Match answers 304 or 412 by method:

>    An origin server that evaluates an If-None-Match condition MUST NOT
>    perform the requested method if the condition evaluates to false;
>    instead, the origin server MUST respond with either a) the 304 (Not
>    Modified) status code if the request method is GET or HEAD or b) the
>    412 (Precondition Failed) status code for all other request methods.

and If-Modified-Since is ignored when the method is neither GET nor HEAD:

>    A recipient MUST ignore the If-Modified-Since header field if the
>    received field value is not a valid HTTP-date, the field value has
>    more than one member, or if the request method is neither GET nor
>    HEAD.

so If-None-Match under OPTIONS yields 412 on a match, and If-Modified-Since
under OPTIONS is ignored.

**Lane conventions (clauses C3 and C4; not RFC requirements).** `"role": null`
is accepted and means the same as omitting the key (origin); the key remains
optional. An input whose raw bytes contain duplicate object keys is refused
before any decision, because RFC 8259 §4 says only that

>    name.  The names within an object SHOULD be unique.

an advisory the RFC does not turn into a duplicate-member rule: refusing the
document is local receipt-integrity policy, not an RFC requirement. The
round-95 re-read of S455 against the retained body is recorded in
`corpus/lessons/round-95.md`; the RFC Editor errata page for RFC 9110
(S479, pending admission) was opened once this round by the round's scout.
