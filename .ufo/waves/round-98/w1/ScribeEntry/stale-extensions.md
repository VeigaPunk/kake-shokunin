source: S482, S483, S480, S478 — RFC 5861 (opened this round, retained sha256 1193f1c8…) and its errata record, RFC 9111 (retained sha256 aeb52adb…) and RFC 9110 §5.6 (retained sha256 21c1cdce6ab0…)
verified-at: 2026-11-05
recheck: 180d
ground: freshness — round-98 C2, a bounded capability: whether a stored response that is stale may be served, on a request or on an error, and up to how long, under the RFC 9111 §4.2.4 prohibitions.
scope: one decision per request or error over values the caller supplies, under contract v1 of this lane; not a cache store, a cache-key computation, a freshness-lifetime computation, a current-age computation, a storage decision, a revalidation scheduler, a Warning/Age emitter, or any claim about a live cache, CDN or proxy.

# Stale-serving extensions: stale-while-revalidate and stale-if-error under the RFC 9111 §4.2.4 prohibitions

RFC 5861 defines two Cache-Control extensions that let a cache serve a response
it already knows is stale: `stale-while-revalidate`, which lets it serve the
response stale for a bounded window while it revalidates in the background, and
`stale-if-error`, which lets it serve the response stale when the origin fails.
Both are permissions, not obligations, and RFC 9111 §4.2.4 sets the limits under
which either permission can be used at all.

This entry records what the two RFCs say, marks which clause of the decision is
fixed by an RFC and which is a convention this lane chose, names the instrument
that applies them, and states plainly what it does not decide.

## What RFC 5861 §3 says (stale-while-revalidate)

RFC 5861 §3 is the permission itself (lines 106-109):

> indicates that caches MAY serve the response in which it appears after it becomes stale, up to the indicated number of seconds

The extension has a token form (line 119):

> stale-while-revalidate = "stale-while-revalidate" "=" delta-seconds

When the response is served stale under that permission, RFC 5861 §3 asks for
asynchronous revalidation (lines 121-123):

> the cache SHOULD attempt to revalidate it while still serving stale responses (i.e., without blocking)

The permission has a lifetime: once the window has passed without the entity
being revalidated, the extension stops applying (lines 128-129):

> If delta-seconds passes without the cached entity being revalidated, it SHOULD NOT continue to be served stale, absent other information.

The worked example of §3.1 pairs the extension with `max-age` (line 135):

> Cache-Control: max-age=600, stale-while-revalidate=30

and reads it as fresh time plus a stale window (lines 137-138):

> it is fresh for 600 seconds, and it may continue to be served stale for up to an additional 30 seconds

## What RFC 5861 §4 says (stale-if-error)

RFC 5861 §4 is the second permission (lines 161-163):

> when an error is encountered, a cached stale response MAY be used to satisfy the request, regardless of other freshness information

with its own token form (line 165):

> stale-if-error = "stale-if-error" "=" delta-seconds

§4 also fixes the two scopes the directive can appear in (lines 175-176):

> When used as a request Cache-Control extension, its scope of application is the request it appears in

and the value is an upper limit on staleness (lines 180-182):

> when the cached response is more stale than the indicated amount, the cached response SHOULD NOT be used to satisfy the request, absent other information

§4 defines what counts as an error (lines 184-185):

> In this context, an error is any situation that would result in a 500, 502, 503, or 504 HTTP response status code being returned.

The §4.1 example pairs it with `max-age` (line 197):

> Cache-Control: max-age=600, stale-if-error=1200

and ends with the write-through rule (lines 231-232):

> After the age is greater than 1800 seconds (i.e., it has been stale for 1200 seconds), the cache must write the error message through.

## What RFC 9111 says about serving stale at all

RFC 9111 §4.2.4 is the constraint the two permissions sit inside. A stale
response must not be generated when an in-protocol directive prohibits it
(lines 790-791):

> A cache MUST NOT generate a stale response if it is prohibited by an explicit in-protocol directive

and the prohibited directives are named (lines 791-793):

> by a no-cache response directive, a must-revalidate response directive, or an applicable s-maxage or proxy-revalidate response directive

The same section makes the permission conditional (lines 795-797):

> A cache MUST NOT generate a stale response unless it is disconnected or doing so is explicitly permitted by the client or origin server

and it names RFC 5861 as one such permission (lines 797-798):

> extension directives such as those defined in [RFC5861]

So RFC 9111 §4.2.4 is the outer rule and RFC 5861 §3/§4 are the inner
permissions: a cache may serve a stale response only because an extension
directive such as RFC 5861 permits it, and never when a prohibition directive
applies.

The three prohibition directives have their own semantics. `must-revalidate`
(lines 1224-1225):

> The must-revalidate response directive indicates that once the response has become stale, a cache MUST NOT reuse that response to

and, when the cache is disconnected (lines 1232-1233):

> if a cache is disconnected, the cache MUST generate an error response rather than reuse the stale response

`proxy-revalidate` (lines 1357-1359):

> The proxy-revalidate response directive indicates that once the response has become stale, a shared cache MUST NOT reuse that response

`s-maxage` (lines 1395-1397):

> The s-maxage directive incorporates the semantics of the proxy-revalidate response directive (Section 5.2.2.8) for a shared cache

and (lines 1397-1399):

> A shared cache MUST NOT reuse a stale response with s-maxage to satisfy another request until it has been successfully validated

Two `no-cache` forms matter here. The response directive has an unqualified and
a qualified form; the qualified form (lines 1273-1274):

> The qualified form of the no-cache response directive, with an argument that lists one or more field names

and the request directive (lines 1166-1167):

> The no-cache request directive indicates that the client prefers a stored response not be used to satisfy the request

Two more rules the decision rests on: `delta-seconds` is a non-negative integer
(lines 214-215):

> The delta-seconds rule specifies a non-negative integer, representing time in seconds.

with its production (line 217):

> delta-seconds = 1*DIGIT

and, when a directive appears more than once, RFC 9111 §4.2.1 (lines 679-680):

> either the first occurrence should be used or the response should be considered stale

The grammar of the two Cache-Control fields comes from RFC 9110 §5.6. A token
is a short textual identifier (lines 1730-1731):

> Tokens are short textual identifiers that do not include whitespace or delimiters.

with its production (line 1733):

> token = 1*tchar

and a quoted string (lines 1786-1787):

> quoted-string = DQUOTE *( qdtext / quoted-pair ) DQUOTE qdtext = HTAB / SP / %x21 / %x23-5B / %x5D-7E / obs-text

whose quoted-pair form is (line 1794):

> quoted-pair = "\" ( HTAB / SP / VCHAR / obs-text )

## The clause table

"RFC-exact" means an RFC states the rule the instrument applies; "lane
convention" means the RFC grounds the topic but the reading is this lane's, and
the reading is visible rather than silent.

| Clause | What it decides | RFC-exact ground | Lane convention |
|---|---|---|---|
| **C1** stale-while-revalidate permission | A stale response may be served up to the indicated number of seconds | RFC 5861 §3 (Q1, Q4) | The decision names, and the staleness arithmetic `staleness = max(0, A − L)` over the supplied lifetime and age |
| **C2** revalidation while serving stale | Serving stale and revalidating are not exclusive | RFC 5861 §3 (Q2) | The tool decides the serve-or-revalidate branch only; it schedules no revalidation |
| **C3** the window ends | The permission lapses once the window passes unrevalidated | RFC 5861 §3 (Q3) | The boundary is inclusive: staleness equal to the limit still serves |
| **C4** the worked window | `max-age=600, stale-while-revalidate=30` is fresh 600 s plus a stale 30 s | RFC 5861 §3.1 (Q5, Q6) | Which supplied lifetime and age stand for `max-age=600` and the current age |
| **C5** stale-if-error permission | A stale response may satisfy a request when an error occurs | RFC 5861 §4 (Q7, Q8) | The decision names, and `"network"` as an error token, which the RFC does not name |
| **C6** directive scope | A request directive applies to that request; a response directive applies to requests it may serve | RFC 5861 §4 (Q9) | When both a request and a response value are valid, the request value wins |
| **C7** the staleness bound | A response more stale than the limit should not be used | RFC 5861 §4 (Q10) | The boundary is inclusive, and the limit is compared against computed staleness |
| **C8** what an error is | An error is a situation yielding 500, 502, 503 or 504 | RFC 5861 §4 (Q11) | The decision name `not-an-error` for a status outside that set, and the refusal of anything else |
| **C9** the worked error window | `max-age=600, stale-if-error=1200` is usable until age 1800, then written through | RFC 5861 §4.1 (Q13, Q12) | Which error status is written through: the tool decides `error-through`, not a status code |
| **C10** prohibitions | `no-cache`, `must-revalidate`, and — for a shared cache — `s-maxage` and `proxy-revalidate` block serving stale | RFC 9111 §4.2.4, §5.2.2.2, §5.2.2.8, §5.2.2.10 (Q14, Q15, Q18, Q20, Q21, Q22) | A qualified `no-cache` counts as a prohibition too, and the prohibition reaches the response field only as far as the contract says |
| **C11** the outer permission | Stale may be served only when disconnected or explicitly permitted, including by RFC 5861 extensions | RFC 9111 §4.2.4 (Q16, Q17) | That the two RFC 5861 extensions are such permissions, and the decision names that carry them |
| **C12** the two `no-cache` forms | The response directive is unqualified or qualified; the request directive is a client preference | RFC 9111 §5.2.2.4, §5.2.1.4 (Q23, Q24) | Treating the qualified form conservatively, and refusing the request form as a prohibition |
| **C13** delta-seconds | A delta-seconds value is a non-negative integer of digits | RFC 9111 §1.2.2 (Q25, Q26) | The clamp at 2147483648, and a quoted or non-digit value making the directive absent rather than a refusal |
| **C14** repeated directives | A repeated directive may be read from its first occurrence, or the response treated as stale | RFC 9111 §4.2.1 (Q27) | The lane reads the first occurrence and does not treat the response as stale |
| **C15** field grammar | A Cache-Control element is a token, optionally `=` a token or a quoted string | RFC 9110 §5.6.2, §5.6.4 (Q28, Q29, Q30, Q31) | Which characters are refused, and that the quoted or non-digit delta-seconds value yields an absent directive |

## The instrument and its counter

The instrument named by contract v1 is `scripts/stale_extensions.py`. It reads
one JSON object on stdin and answers one question: given a stored response's
`Cache-Control` field, the request's `Cache-Control` field, a freshness
lifetime, a current age, an event (`request` or `error`) and, for an error
event, an error, may the stored response be served stale, and how stale is it.

A decided case exits 0 and writes one JSON object with exactly the keys
`decision` and `staleness`; a refused case exits 1, writes nothing to stdout and
writes a diagnostic beginning `invalid_input:` to stderr. The decision names
are `not-an-error`, `fresh`, `serve-stale-revalidate`, `revalidate`,
`serve-stale-error` and `error-through`; `staleness` is always reported,
whether the answer is to serve stale or not.

The contract the instrument implements is `.ufo/waves/round-98/stale-contract.md`
(sha256 ec077b4f30ad786316df86e784290267b12df1cb11519623d9519b88fd971075).
The counter that measures the instrument against it is
`.ufo/waves/round-98/c98_stale.py` (sha256
e0331e56378fb5acabe4447a37590cbf3273537aabd8c8d88f842e0a434a9f3f), which
scores the candidate from committed bytes and prints one line:

    candidate=present sha256=… hand=60/60 generated=240/240 refusals=…/… seed=… met=true|false

The round's frozen predicate for this claim is that the counter prints
`candidate=present`, `hand=60/60`, `generated=240/240` and `met=true` with
exit 0 at the landed content revision, that the scored sha256 equals the
landed `scripts/stale_extensions.py`, and that the SCORECARD capabilities table
gains the row in the same round. Two limits were declared before the data: the
generated population alone does not separate the exclusive-boundary and the
request-`stale-if-error` forgeries — the hand cases do — and the candidate is
not sandboxed beyond `-I` and a scratch working directory.

The bodies this entry quotes are the retained RFC 5861 body
(`.ufo/waves/round-98/sources/rfc5861.txt`, sha256 1193f1c8…, 10 359 bytes,
339 lines), the retained RFC 9111 body
(`.ufo/waves/round-93/L1/src/rfc9111.txt`, sha256 aeb52adb…, 84 477 bytes,
1 956 lines — byte-identical to the body fetched this round, `cmp` exit 0) and
the retained RFC 9110 body (`corpus/lessons/round-81-gate/rfc9110.txt`,
sha256 21c1cdce6ab0…, 10 785 lines).

## The quotes, with their locations

Every quote below is a raw substring of the retained body named for it, taken
from the stated plain-text line span, and at most 25 whitespace-separated
words. `quote-check.txt` records the `grep -n` locator for each of them.

| # | Body | Lines | Words | Quote |
|---|---|---|---|---|
| Q1 | rfc5861.txt | 106-109 | 22 | indicates that caches MAY serve the response in which it appears after it becomes stale, up to the indicated number of seconds |
| Q2 | rfc5861.txt | 121-123 | 15 | the cache SHOULD attempt to revalidate it while still serving stale responses (i.e., without blocking) |
| Q3 | rfc5861.txt | 128-129 | 20 | If delta-seconds passes without the cached entity being revalidated, it SHOULD NOT continue to be served stale, absent other information. |
| Q4 | rfc5861.txt | 119-119 | 5 | stale-while-revalidate = "stale-while-revalidate" "=" delta-seconds |
| Q5 | rfc5861.txt | 135-135 | 3 | Cache-Control: max-age=600, stale-while-revalidate=30 |
| Q6 | rfc5861.txt | 137-138 | 21 | it is fresh for 600 seconds, and it may continue to be served stale for up to an additional 30 seconds |
| Q7 | rfc5861.txt | 161-163 | 21 | when an error is encountered, a cached stale response MAY be used to satisfy the request, regardless of other freshness information |
| Q8 | rfc5861.txt | 165-165 | 5 | stale-if-error = "stale-if-error" "=" delta-seconds |
| Q9 | rfc5861.txt | 175-176 | 17 | When used as a request Cache-Control extension, its scope of application is the request it appears in |
| Q10 | rfc5861.txt | 180-182 | 25 | when the cached response is more stale than the indicated amount, the cached response SHOULD NOT be used to satisfy the request, absent other information |
| Q11 | rfc5861.txt | 184-185 | 24 | In this context, an error is any situation that would result in a 500, 502, 503, or 504 HTTP response status code being returned. |
| Q12 | rfc5861.txt | 231-232 | 24 | After the age is greater than 1800 seconds (i.e., it has been stale for 1200 seconds), the cache must write the error message through. |
| Q13 | rfc5861.txt | 197-197 | 3 | Cache-Control: max-age=600, stale-if-error=1200 |
| Q14 | rfc9111.txt | 790-791 | 17 | A cache MUST NOT generate a stale response if it is prohibited by an explicit in-protocol directive |
| Q15 | rfc9111.txt | 791-793 | 17 | by a no-cache response directive, a must-revalidate response directive, or an applicable s-maxage or proxy-revalidate response directive |
| Q16 | rfc9111.txt | 795-797 | 24 | A cache MUST NOT generate a stale response unless it is disconnected or doing so is explicitly permitted by the client or origin server |
| Q17 | rfc9111.txt | 797-798 | 8 | extension directives such as those defined in [RFC5861] |
| Q18 | rfc9111.txt | 1224-1225 | 20 | The must-revalidate response directive indicates that once the response has become stale, a cache MUST NOT reuse that response to |
| Q19 | rfc9111.txt | 1232-1233 | 18 | if a cache is disconnected, the cache MUST generate an error response rather than reuse the stale response |
| Q20 | rfc9111.txt | 1357-1359 | 20 | The proxy-revalidate response directive indicates that once the response has become stale, a shared cache MUST NOT reuse that response |
| Q21 | rfc9111.txt | 1395-1397 | 17 | The s-maxage directive incorporates the semantics of the proxy-revalidate response directive (Section 5.2.2.8) for a shared cache |
| Q22 | rfc9111.txt | 1397-1399 | 21 | A shared cache MUST NOT reuse a stale response with s-maxage to satisfy another request until it has been successfully validated |
| Q23 | rfc9111.txt | 1273-1274 | 18 | The qualified form of the no-cache response directive, with an argument that lists one or more field names |
| Q24 | rfc9111.txt | 1166-1167 | 19 | The no-cache request directive indicates that the client prefers a stored response not be used to satisfy the request |
| Q25 | rfc9111.txt | 214-215 | 11 | The delta-seconds rule specifies a non-negative integer, representing time in seconds. |
| Q26 | rfc9111.txt | 217-217 | 3 | delta-seconds = 1*DIGIT |
| Q27 | rfc9111.txt | 679-680 | 14 | either the first occurrence should be used or the response should be considered stale |
| Q28 | rfc9110.txt | 1730-1731 | 12 | Tokens are short textual identifiers that do not include whitespace or delimiters. |
| Q29 | rfc9110.txt | 1733-1733 | 3 | token = 1*tchar |
| Q30 | rfc9110.txt | 1786-1787 | 22 | quoted-string = DQUOTE *( qdtext / quoted-pair ) DQUOTE qdtext = HTAB / SP / %x21 / %x23-5B / %x5D-7E / obs-text |
| Q31 | rfc9110.txt | 1794-1794 | 12 | quoted-pair = "\" ( HTAB / SP / VCHAR / obs-text ) |

## What this entry cites

- **S482** — RFC 5861, opened this round; the retained body
  `.ufo/waves/round-98/sources/rfc5861.txt` (sha256 1193f1c8…, 10 359 bytes,
  339 lines) is the text Q1-Q13 are quoted from.
- **S483** — the RFC Editor errata record for RFC 5861, opened this round
  alongside S482.
- **S480** — RFC 9111 §4.3.1/§4.3.3, the lane's existing validation-exchange
  ground. The RFC 9111 quotes above (Q14-Q27) come from the same retained
  RFC 9111 body, `.ufo/waves/round-93/L1/src/rfc9111.txt` (sha256
  aeb52adb…, 84 477 bytes, 1 956 lines), which is byte-identical to the body
  the S480 row was drawn from and to the body fetched this round.
- **S478** — RFC 9110 §5.6, the lane's existing RFC 9110 list-grammar ground.
  The RFC 9110 quotes above (Q28-Q31) come from the retained body
  `corpus/lessons/round-81-gate/rfc9110.txt` (sha256 21c1cdce6ab0…, 10 785
  lines), the body the S478 row names.

## Errata on RFC 5861

The RFC 5861 errata record (S483) carries two errata, both Verified and both
Editorial: EID 2255 on §3 and EID 2256 on §4. Both propose the same rewording
of the note that follows the stale-if-error paragraph — "Age header" to "Age
header field" and "warning header" to "Warning header field" — for consistent
standard terminology and header-field-name capitalization. Neither erratum
touches the §3 serving window, the §4 staleness bound, the §4 error
definition or the §4 scope sentence, so no clause above is affected by them.

## What this entry does not decide

- It does not compute a freshness lifetime or a current age. Both are supplied
  by the caller; the lifetime and age arithmetic live in
  `scripts/cache_current_age.py` and `scripts/heuristic_freshness.py`.
- It does not decide storage: `no-store`, `private` and `public` are ignored,
  and the tool takes the response as already stored.
- It does not decide the request directives `max-age`, `max-stale`,
  `min-fresh` and `only-if-cached`. A request field carrying one of them is
  refused rather than decided.
- It does not emit `Warning` or `Age` headers, and it does not schedule or
  perform background revalidation. RFC 5861 §3 asks for revalidation while
  stale is served; the tool records the branch, not the revalidation.
- It does not decide which error status a cache writes through when the
  permission has lapsed: `error-through` names the branch, not a status code.
- It does not parse HTTP dates, compute cache keys, match `Vary`, or select a
  stored response. It decides one serving question over supplied values.
- It claims no behaviour of any live cache, CDN, proxy or browser. `fresh`,
  `serve-stale-revalidate`, `revalidate`, `serve-stale-error` and
  `error-through` are the answers a reading of the two RFCs gives for the
  supplied values, not observations of what a deployed cache did.
