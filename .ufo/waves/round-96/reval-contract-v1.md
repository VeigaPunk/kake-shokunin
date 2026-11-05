# Revalidation exchange — contract v1 (kake, round 96)

Frozen before data (`.ufo/waves/round-96/freeze.md`). The instrument decides,
over supplied values only, the two stages of an HTTP-cache validation exchange
(RFC 9111 §4.3): which precondition header fields a cache constructs for a
stored response, and how a cache handles the response it receives to that
conditional request. It reads committed bytes at `--revision` for identity and
scores a subject program over stdin/stdout JSON. It decides nothing about
storage, cache keys, freshness lifetimes, serving, the merged header field set
of a 304 (§4.3.4), wire traffic, or any live cache.

Every subject is a Python program that reads one JSON document from stdin and
writes one JSON decision object to stdout (exit 0), or refuses the input with
a diagnostic and a nonzero exit.

## Input shape

```json
{"stored": {"exists": bool, "etag": string|null, "last_modified": int|null},
 "received_status": int|null}
```

`etag` is an entity-tag as RFC 9110 §8.8.3 defines it (`DQUOTE *etagc DQUOTE`,
optionally prefixed `W/`; etagc includes obs-text). `last_modified` is a
supplied non-negative integer standing for a timestamp value (the lane's
supplied-values convention; the instrument never parses HTTP dates).
`received_status` is the status code the cache received in response to the
conditional request, or null while the exchange is still at the construction
stage.

## Output shape

```json
{"decision": "...", "if_none_match": string|null, "if_modified_since": int|null}
```

`if_none_match`/`if_modified_since` are non-null only on the `construct`
decision; every handling decision reports both as null.

## Clauses

- **C1 — validator selection (construction).** With `received_status` null:
  both validators absent → `cannot-revalidate` with both fields null; any
  validator present → `construct`, `if_none_match` = the stored etag verbatim
  (weakness marker included) when an etag is stored, null otherwise, and
  `if_modified_since` = the stored `last_modified` value when stored, null
  otherwise. RFC grounding: §4.3.1 bullet 1 (plain-text line 848, retained
  body sha256 `aeb52adb…`): "MUST send the relevant entity tags … if the
  entity tags were provided in the stored response(s) being validated"; the
  bullet's If-Match/If-Range alternatives are representation-selection
  fields, and a cache's own revalidation uses If-None-Match (§4.3.2, line
  887-891: "If-None-Match takes precedence over If-Modified-Since" — the
  instrument never constructs If-Match or If-Range).
- **C2 — both validators are constructed together (lane convention, RFC
  grounded).** When both validators are stored, both header fields are
  reported. Grounding: §4.3.1 bullet 2 (line 852) makes If-Modified-Since a
  SHOULD whose condition ("a single stored response is being validated, and
  that response contains a Last-Modified value") does not exclude an etag,
  and line 861: "In most cases, both validators are generated in cache
  validation requests, even when entity tags are clearly superior". The
  MUST/SHOULD asymmetry is the RFC's; the instrument's decision treats the
  SHOULD as sent (a lane convention, labeled as such here).
- **C3 — a 304 updates the stored response.** `received_status` 304 →
  `update-stored`. Grounding: §4.3.3 bullet 1 (line 935): "A 304 (Not
  Modified) response status code indicates that the stored response can be
  updated and reused". Which stored responses update and with which merged
  fields is §4.3.4 — out of scope (named exclusion).
- **C4 — a 5xx permits reuse or forwarding.** `received_status` 500–599 →
  `may-reuse-stored`. Grounding: §4.3.3 bullet 3 (line 944): "if a cache
  receives a 5xx (Server Error) response while attempting to validate a
  response, it can either forward this response to the requesting client or
  act as if the server failed to respond. In the latter case, the cache can
  send a previously stored response, subject to its constraints on doing so
  (see Section 4.2.4), or retry the validation request." The instrument
  reports the permission, not which branch a real cache takes.
- **C5 — any other 200–499 status is the full-response class.**
  `received_status` 200–499 → `replace-stored`. Grounding: §4.3.3 bullet 2
  (line 938): "A full response (i.e., one containing content) indicates that
  none of the stored responses nominated in the conditional request are
  suitable. Instead, the cache MUST use the full response to satisfy the
  request." Lane convention (labeled): statuses 200–499 are decided as the
  full-response class from the status code alone; whether one carries content
  (a payload-less 204, for instance) is invisible to supplied values and is a
  named exclusion.
- **C6 — refusals (invalid input, exit 1 with a diagnostic).** Non-object
  input; unknown keys at either level; missing keys; `exists` not a bool; an
  etag that is neither null nor a well-formed entity-tag (RFC 9110 §8.8.3
  etagc grammar, obs-text included, per S455); `last_modified` neither null
  nor a non-negative integer; `received_status` neither null nor an integer
  in 100–599; a 1xx `received_status` (an interim response is never a
  validation response); `received_status` present while no validator is
  stored (an exchange presupposes a conditional request, which needs a
  validator); validators present while `exists` is false; and raw duplicate
  object keys in the input bytes (the S034 convention the conditional_eval
  line pins: refuse, never silently last-wins).

## met predicate (frozen)

`c96_reval.py` reports `met=true` iff, at the measured revision: the candidate
`scripts/reval_exchange.py` is present; the population pins file and every
pinned fixture digest match; the anti-table finds no hand-case input digest,
no generated-case input digest and no forgery stem in the candidate source
(R95-8: generated cases are digested too); every hand case is decided as
declared (or refused as declared); all 120 seeded generated cases match the
in-counter reference; every forgery subject is refused; the frozen positive
control is admitted; and every mutant of the frozen positive control is
killed (no survivors, no unreceipted drift).
