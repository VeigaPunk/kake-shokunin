source: S480 <https://www.rfc-editor.org/rfc/rfc9111.txt> §4.3, lines 812-949 (retained sha256 aeb52adb…)
verified-at: 2026-11-05
recheck: 180d
ground: freshness — round-96 C2, a bounded capability: the two stages of a cache's validation exchange, decided over supplied values.
scope: one decision per validation exchange under contract v1 of this lane; not a cache store, a cache-key computation, a freshness-lifetime decision, a serving decision, an HTTP-date parser, a network client, or any claim about a live cache.

# Revalidation exchange: which validators a cache sends, and what it does with the reply

A cache that cannot serve a stored response may ask the server whether that copy is
still current, and update or replace it from the answer. RFC 9111 §4.3 names the
process (lines 809-810):

> This process is known as "validating" or "revalidating" the stored response.

The trigger is narrow. A cache reaches this only when it holds a stored response it
cannot serve (lines 803-804):

> When a cache has one or more stored responses for a requested URI, but cannot serve any of them

**Two stages, in this order.** The first is *construction*: the cache decides which
precondition header fields to put in the request it forwards. The second is
*handling*: the cache decides what the status code it receives back means for the
stored response. The stages are separate because the second has no meaning without
the first — a status code is only a validation answer to a request that carried a
validator.

## What the contract decides

`scripts/reval_exchange.py` — the path contract v1 (`.ufo/waves/round-96/reval-contract-v1.md`)
names for the instrument — decides **one** thing over values the caller supplies: for
one validation exchange, which validators the cache constructs, or what the received
status means for the stored response.

- **Input**: one JSON object on stdin, exactly the keys `stored` and
  `received_status`. `stored` carries `exists` (bool), `etag` (string or null) and
  `last_modified` (non-negative integer or null). `received_status` is the status code
  the cache received in answer to its conditional request, or `null` while the
  exchange is still at the construction stage. `last_modified` is a supplied integer,
  the lane's convention, not a parsed HTTP-date.
- **Output**: `{"decision": ..., "if_none_match": string|null,
  "if_modified_since": int|null}` on stdout, exit 0. The two header fields are
  non-null only on the construction decision; every handling decision reports both as
  null.
- **Decisions**: `cannot-revalidate` (nothing to validate with), `construct` (the
  validators to send), `update-stored` (a 304), `replace-stored` (a full response),
  `may-reuse-stored` (a 5xx).
- **Refusal**: `invalid_input: <reason>` on stderr, nothing on stdout, exit 1. The
  contract fixes the exit code and requires a diagnostic; the `invalid_input:` prefix
  is the lane's, shared with `scripts/conditional_eval.py` and with the frozen
  positive control `.ufo/waves/round-96/frozen/pos-good-reval.py`.

Conformance to that contract is measured by the round's frozen counter
`.ufo/waves/round-96/c96_reval.py`; nothing in this entry reports a score.

## The clause table

Each clause is labeled with what the RFC fixes and what the lane chose. "RFC-exact"
means the RFC states the rule the instrument applies; "lane convention" means the RFC
grounds the topic but the instrument's reading is the lane's, and the reading is
visible rather than silent.

| Clause | What it decides | RFC-exact ground | Lane convention |
|---|---|---|---|
| **C1** validator selection | With no received status: no validator stored → `cannot-revalidate`, both fields null; a validator stored → `construct`, with `if_none_match` = the stored etag verbatim (weakness marker included) when an etag is stored and null otherwise, and `if_modified_since` = the stored `last_modified` when stored and null otherwise | The stored entity tags MUST be sent (lines 848-850); a cache's own revalidation uses If-None-Match, which takes precedence over If-Modified-Since, so If-Match and If-Range are never constructed (lines 889-891) | The decision names, and "no validator stored" being a refusal rather than an empty conditional request |
| **C2** both validators together | When both validators are stored, both header fields are reported | The Last-Modified SHOULD (lines 852-854) and the statement that both validators are generated in most cases (lines 861-862) | Treating the SHOULD as sent: the RFC makes it conditional, the contract decides the condition away |
| **C3** a 304 | `received_status` 304 → `update-stored` | The stored response can be updated and reused (lines 935-936) | The decision name, and which stored responses update and with which fields (§4.3.4) left out |
| **C4** a 5xx | `received_status` 500-599 → `may-reuse-stored` | A 5xx leaves the cache free to forward it, or to send a previously stored response, or to retry (lines 944-949) | Reporting the permission rather than choosing a branch; the lane does not decide which branch a real cache takes |
| **C5** any other 200-499 | `received_status` 200-499 → `replace-stored` | The cache MUST use the full response to satisfy the request (lines 940-941) | Deciding the class from the status code alone: whether a response carries content is invisible to supplied values, and is a named exclusion |
| **C6** refusals | Invalid input → `invalid_input:` on stderr, exit 1 | Nothing in §4.3 fixes an input grammar | The whole refusal set — unknown keys, missing keys, wrong types, a 1xx status, a status without a stored validator, a validator without a stored representation, and raw duplicate object keys (the S034 convention) |

C1 is the only clause whose construction half rests on two sections: §4.3.1 says what
a cache may send, and §4.3.2 says which of those fields a cache evaluates at all
(lines 888-891):

> In summary, the If-Match and If-Unmodified-Since conditional header fields are not applicable to a cache, and If-None-Match takes precedence over If-Modified-Since

That sentence is why the instrument reports an etag under `if_none_match` and never
under `if_match`: a cache's own revalidation is a response validation, not a
representation selection, and the two use different fields.

## The quotes, with their locations

Every quote below is a raw substring of the retained RFC 9111 body
(`.ufo/waves/round-93/L1/src/rfc9111.txt`, sha256 `aeb52adb…5302cf3e`, 84 477 bytes),
byte-identical to the body this round's scout fetched
(`.ufo/waves/round-96/w1/ScoutRFC/rfc9111.txt`, `cmp` exit 0). Line numbers are
plain-text line numbers in that body. Word counts are whitespace-separated tokens.

| # | Lines | Words | Quote |
|---|---|---|---|
| R1 | 803-804 | 19 | When a cache has one or more stored responses for a requested URI, but cannot serve any of them |
| R2 | 809-810 | 11 | This process is known as "validating" or "revalidating" the stored response. |
| R3 | 827-829 | 24 | The precondition header fields are then compared by recipients to determine whether any stored response is equivalent to a current representation of the resource. |
| R4 | 848-850 | 23 | MUST send the relevant entity tags (using If-Match, If-None-Match, or If-Range) if the entity tags were provided in the stored response(s) being validated. |
| R5 | 852-854 | 22 | SHOULD send the Last-Modified value (using If-Modified-Since) if the request is not for a subrange, a single stored response is being validated |
| R6 | 861-862 | 18 | In most cases, both validators are generated in cache validation requests, even when entity tags are clearly superior |
| R7 | 888-891 | 21 | In summary, the If-Match and If-Unmodified-Since conditional header fields are not applicable to a cache, and If-None-Match takes precedence over If-Modified-Since |
| R8 | 935-936 | 17 | A 304 (Not Modified) response status code indicates that the stored response can be updated and reused |
| R9 | 938-940 | 21 | A full response (i.e., one containing content) indicates that none of the stored responses nominated in the conditional request are suitable |
| R10 | 940-941 | 12 | Instead, the cache MUST use the full response to satisfy the request. |
| R11 | 944-946 | 22 | However, if a cache receives a 5xx (Server Error) response while attempting to validate a response, it can either forward this response |
| R12 | 947-949 | 23 | the cache can send a previously stored response, subject to its constraints on doing so (see Section 4.2.4), or retry the validation request |
| R13 | 986-988 | 22 | the cache MUST update its header fields with the header fields provided in the 304 (Not Modified) response, as per Section 3.2 |

R3, R7 and R13 are re-reads of ground this lane already holds; R3 and R13 are the
§4.3.1 and §4.3.4 spans S456 names, and R7 is the §4.3.2 span S476 names. R4, R5, R6,
R8, R9, R10, R11 and R12 are the §4.3.1 and §4.3.3 spans S480 opens.

## What this entry cites

- **S480** — RFC 9111 §4.3, lines 812-949: the validation exchange the instrument
  decides. Opened this round; the fetched body is byte-identical to the retained
  round-93 body at sha256 `aeb52adb…5302cf3e`.
- **S456** (re-read) — RFC 9111 §3.1, §3.2, §4 and §4.3.1/§4.3.4: the storage and
  freshening context around the exchange, and the R3 and R13 spans.
- **S476** (re-read) — RFC 9111 §4.3.2: the cache-side applicability and precedence
  rule, and the R7 span.

## What this entry does not claim

This entry decides a validation exchange over values the caller supplies. It claims
no storage behavior — nothing here stores, indexes, evicts or selects a stored
response; it computes no cache key and names no key identity; it does not update the
merged header field set of a 304, which RFC 9111 §4.3.4 specifies separately (lines
986-988) and which this contract leaves out; and it makes no claim about any live
cache, CDN, proxy or browser. `may-reuse-stored` reports a permission the RFC grants,
not an observation of what any deployed cache did, and `construct` reports the
validators a cache would send, not traffic on a wire.
