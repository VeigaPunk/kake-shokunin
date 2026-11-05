source: S471 S472 S473 S474 S475 S476 — RFC 9110 HTTP Semantics, §13.2.2 Precedence of Preconditions (plain-text line 6222), §13.1.1 If-Match (5785), §13.1.2 If-None-Match (5872), §13.1.3 If-Modified-Since (5942), §13.1.4 If-Unmodified-Since (6023), §8.8.3.2 Comparison incl. Table 3 (3643, 3658-3670); and RFC 9111 HTTP Caching, §4.3.2 Handling a Received Validation Request (plain-text line 866) — https://www.rfc-editor.org/rfc/rfc9110.txt (502941 B, sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a) and https://www.rfc-editor.org/rfc/rfc9111.txt (84477 B, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e); both opened by this seat with a live GET on 2026-11-05T01:27:45Z, HTTP 200, and byte-identical (`cmp` exit 0) to the lane's retained copies at `.ufo/waves/round-93/L1/src/`, so every line number below is the line number in the fetched body. Registry rows S471-S476 are this round's rows for those six anchors; the L1 appends them to `corpus/SOURCES.md`.
verified-at: 2026-11-04 — this seat opened both RFC texts itself (live GET, HTTP 200, byte counts and digests as recorded on the `source:` line; receipt in `.ufo/waves/round-93/w1/ScribeEntry/receipts.txt`), located each cited section by plain-text line number, and filed 14 located quotes, each verified mechanically to be a raw substring of the fetched body, confined to its stated line span and 3-25 words (`.ufo/waves/round-93/w1/ScribeEntry/quotes.txt`; re-run: `violations=0 checks=20`). It then derived 13 decision examples and 6 refusal examples from the contract's clauses by hand and ran them against both the delivered candidate `scripts/conditional_eval.py` and the frozen independent positive control `.ufo/waves/round-93/frozen/pos-good.py`: 13/13 decisions agree and 6/6 refusals are refused by both (`.ufo/waves/round-93/w1/ScribeEntry/tool-probe.txt`; `mismatches=0 decisions=13 refusals=6`). The candidate's `--selftest` printed a `selftest <n>/<n>` line and exited 0 at the moment of that measurement; the count is a property of the candidate, not of this entry, so re-run it rather than trusting the number quoted in an earlier draft.
recheck: 180d, or sooner after a source or contract change. Re-fetch https://www.rfc-editor.org/rfc/rfc9110.txt and https://www.rfc-editor.org/rfc/rfc9111.txt into a scratch directory of your own, compare sha256 21c1cdce…7232a and aeb52adb…5302cf3e, and re-locate §13.2.2 (plain-text line 6222), §13.1.1 (5785), §13.1.2 (5872), §13.1.3 (5942), §13.1.4 (6023), §8.8.3.2 with Table 3 (3643, 3658-3670) and RFC 9111 §4.3.2 (866) before reusing the conclusions. No ephemeral path is recorded in this line.
ground: freshness — round-93 C2, a bounded capability: deciding which status a recipient would answer a conditional request with, over supplied values.
scope: one decision per conditional request under contract v1 of this lane. Not a clock, an HTTP-date parser, a network client, a cache store, a validator generator, a storage or freshness decision, a serving or forwarding decision, or any claim about any live CDN, Pages front or Render service.

# Conditional request evaluation: which status a recipient would answer with

A **conditional request** is a request that carries a precondition: a claim
about the state of the target resource, supplied by the client, that the
recipient must evaluate before performing the method. The publisher-side point
of a conditional request is a promise about *when the answer changes*: a client
that already holds a representation sends back the validator it holds
(`If-None-Match`, `If-Modified-Since`) and asks "has this changed since?", and
a client about to write sends back the validator it read (`If-Match`,
`If-Unmodified-Since`) and asks "has this changed since I read it?". A `200`
means "your precondition held, carry on"; a `304` means "your stored
representation is still current"; a `412` means "your precondition failed, do
not perform the method".

Two properties make this harder than it looks, and both are why the lane
built an instrument for it.

**The order of evaluation is normative.** When more than one conditional
header field is present, RFC 9110 §13.2.2 fixes the order in which a
recipient evaluates them, and the order is not the order the fields appear in.
The RFC gives the reason (lines 6227-6230):

> "lost update" preconditions have more strict requirements than cache
> validation, a validated cache is more efficient than a partial
> response

The order itself is a MUST (lines 6233-6234):

> A recipient cache or origin server MUST evaluate the request
> preconditions defined by this specification in the following order

The order the RFC then lists is: **If-Match** (origin server only) → **If-Unmodified-Since**
(origin server only, and only when If-Match is absent) → **If-None-Match** →
**If-Modified-Since** (GET/HEAD only, and only when If-None-Match is absent) →
If-Range/Range → otherwise perform the method. The first applicable step
wins; a false precondition stops the evaluation there.

**The two comparison functions are different, and which one applies depends on
the field.** RFC 9110 §8.8.3.2 (lines 3648-3653):

> "Strong comparison":  two entity tags are equivalent if both are not
> weak and their opaque-tags match character-by-character.

> "Weak comparison":  two entity tags are equivalent if their opaque-
> tags match character-by-character, regardless of either or both
> being tagged as "weak".

The RFC's Table 3 (lines 3658-3670) is the whole comparison surface:

| ETag 1 | ETag 2 | Strong Comparison | Weak Comparison |
|---|---|---|---|
| `W/"1"` | `W/"1"` | no match | match |
| `W/"1"` | `W/"2"` | no match | no match |
| `W/"1"` | `"1"` | no match | match |
| `"1"` | `"1"` | match | match |

Each field names its function. For If-Match (lines 5794-5797):

> An origin server MUST use the strong comparison function when
> comparing entity tags for If-Match

For If-None-Match (lines 5880-5881):

> A recipient MUST use the weak comparison function when comparing
> entity tags for If-None-Match

So `W/"1"` **matches** `"1"` under If-None-Match and **does not match** it
under If-Match. The third row of Table 3 is the case that decides a request:
a weak tag that a client sent, compared against a strong current tag, means
"the client already has this, send me 304" under If-None-Match, and "this is
not the representation I read, refuse" under If-Match.

## The origin-vs-cache difference

The first two steps of the order apply only to an **origin server**. A cache
is not an origin server, and RFC 9111 §4.3.2 says so in one line (lines
889-892):

> the If-Match and If-Unmodified-Since conditional header
> fields are not applicable to a cache, and If-None-Match takes
> precedence over If-Modified-Since.

The reason is given just above (lines 881-885):

> A cache MUST NOT evaluate conditional header fields that only apply
> to an origin server

A cache's job is to answer from what it already holds; If-Match and
If-Unmodified-Since are write-protection preconditions aimed at whoever
performs the method, and a cache that merely revalidates has no method to
protect. What a cache *does* evaluate is the validation pair: If-None-Match
and If-Modified-Since.

## What the tool decides

`scripts/conditional_eval.py` — the path contract v1 names for the
instrument — decides **one** thing over values the caller supplies: which
status a recipient would answer a conditional request with, and which
precondition decided it.

- **Input**: one JSON object on stdin, exactly the keys `method`, `current`,
  `request` and optionally `role`. `current` carries `exists`, `etag` and
  `last_modified`; `request` carries `if_match`, `if_none_match`,
  `if_modified_since` and `if_unmodified_since`. Header values are supplied
  as the **raw field value** (the string after the colon), so the entity-tag
  and list syntax is part of the problem rather than something the tool
  hides. `role` is `"origin"` (the default) or `"cache"`.
- **Output**: `{"decision": "200"|"304"|"412", "precondition": <name>|null}`
  on stdout, exit 0. `precondition` names the field that decided the outcome
  (`if_match`, `if_unmodified_since`, `if_none_match`, `if_modified_since`) or
  is `null` when no precondition was evaluated.
- **Refusal**: `invalid_input: <reason>` on stderr, nothing on stdout,
  exit 1.

The decision order the tool implements is the RFC's order, with the cache
role entered at the top:

| Step | Applies when | Precondition true | Precondition false |
|---|---|---|---|
| If-Match | `role=origin`, `if_match` present | continue | `412` (`if_match`) |
| If-Unmodified-Since | `role=origin`, `if_match` absent, `if_unmodified_since` present, `current.last_modified` present | continue | `412` (`if_unmodified_since`) |
| If-None-Match | `if_none_match` present | continue | `304` for GET/HEAD, else `412` (`if_none_match`) |
| If-Modified-Since | method is GET or HEAD, `if_none_match` absent, `if_modified_since` present, `current.last_modified` present | continue | `304` (`if_modified_since`) |
| otherwise | | | `200` (`null`) |

Two rules sit above the table and hold for **every** input, so a malformed
field is refused even when the field would never have been evaluated:
"no evaluation before validation" (the field syntax is checked first), and
the two ignore rules the RFC states as MUSTs. For If-Modified-Since (lines
5956-5957):

> A recipient MUST ignore If-Modified-Since if the request contains an
> If-None-Match header field

For If-Unmodified-Since (lines 6037-6038):

> A recipient MUST ignore If-Unmodified-Since if the request contains
> an If-Match header field

## The lane's adapter convention: dates are integers

`current.last_modified`, `if_modified_since` and `if_unmodified_since` are
**integer epoch seconds**, not HTTP-dates. There is no HTTP-date parsing
anywhere in the tool, and a string date is a refusal, not a parse attempt.

This is the lane's convention, not the RFC's. RFC 9110 §13.1.3 and §13.1.4
both define the field as `HTTP-date`; the lane's other readers
(`scripts/stored_reuse.py`, `scripts/heuristic_freshness.py`,
`scripts/cache_current_age.py`) already work in supplied integer seconds,
and one convention across the corpus is worth more than RFC-shaped dates
here. The consequence is stated plainly: the tool cannot be handed a real
`If-Modified-Since: Sat, 29 Oct 1994 19:43:31 GMT` and will refuse it.

The same convention carries one RFC rule the contract keeps only in the
RFC's own terms. RFC 9110 §13.1.3 (lines 5963-5966) also says a recipient
MUST ignore If-Modified-Since if the field value "has more than one member,
or if the request method is neither GET nor HEAD", and §13.1.4 says the same
of an invalid or list-valued If-Unmodified-Since. In the lane's integer
encoding there is no such thing as an invalid HTTP-date and no list-valued
date field: a non-integer or negative value is a **refusal** at clause 1
rather than an ignored precondition. That is a narrowing the lane's
convention forces, and it is visible rather than silent.

## Worked examples

Thirteen decisions and six refusals, derived from the contract's clauses.
Each expected value below was written by hand from the contract's decision
order and then confirmed against **both** the delivered candidate and the
frozen independent positive control
(`.ufo/waves/round-93/frozen/pos-good.py`): 13/13 decisions agree, 6/6
refusals are refused by both. Receipt:
`.ufo/waves/round-93/w1/ScribeEntry/tool-probe.txt`.

| # | Clause | Input (abridged) | Decision |
|---|---|---|---|
| W1 | 8 | `PUT`, current `"abc"` mtime 500, `if_match: "\"abc\""` | `200`, precondition `null` |
| W2 | 8 | `PUT`, current `"abc"`, `if_match: "W/\"abc\""` | `412`, precondition `if_match` |
| W3 | 8 | `PUT`, no representation, `if_match: "*"` | `412`, precondition `if_match` |
| W4 | 9 | `PUT`, mtime 600, `if_unmodified_since: 600` | `200`, precondition `null` |
| W5 | 9 | `PUT`, mtime 700, `if_unmodified_since: 600` | `412`, precondition `if_unmodified_since` |
| W6 | 10 | `GET`, current `"abc"`, `if_none_match: "W/\"abc\""` | `304`, precondition `if_none_match` |
| W7 | 10 | `POST`, current `"abc"`, `if_none_match: "\"abc\""` | `412`, precondition `if_none_match` |
| W8 | 10 | `GET`, no representation, `if_none_match: "*"` | `200`, precondition `null` |
| W9 | 11 | `GET`, mtime 500, `if_modified_since: 500` | `304`, precondition `if_modified_since` |
| W10 | 11 | `POST`, mtime 500, `if_modified_since: 900` | `200`, precondition `null` |
| W11 | 7 | `PUT`, `role: "cache"`, `if_match: "\"zzz\""`, `if_unmodified_since: 600` | `200`, precondition `null` |
| W12 | 10 | `GET`, `if_none_match: "\"zzz\""` and `if_modified_since: 900` | `200`, precondition `null` |
| W13 | 12 | `GET`, no precondition at all | `200`, precondition `null` |

W2 and W6 are the Table 3 pair: the *same* pair of tags (`"abc"` against
`W/"abc"`) decides differently under the two comparison functions, which is
why the function is a per-field rule and not a global one. W11 shows the
cache role: a non-matching `if_match` that would be a `412` at the origin is
simply not evaluated at a cache, and the request proceeds to `200`. W12 shows
the precedence: If-None-Match is present and does not match, so the
precondition is *true* and evaluation continues — If-Modified-Since is never
reached, and the answer is `200`, not the `304` that If-Modified-Since alone
would have produced.

The six refusals: a malformed entity-tag in `current.etag` (clause 3);
`if_none_match: "*, \"1\""`, a `*` mixed with other members (clause 4);
`if_modified_since: "400"`, a string where an integer is required (clause 1);
`if_unmodified_since: false`, a bool where an integer is required (clause 1);
`current.exists` false with a non-null `etag` (clause 2); and an unexpected
top-level key (clause 1). Every one prints `invalid_input: <reason>` on
stderr, nothing on stdout, and exits 1.

## What this does not claim

- **No live CDN, Pages front or Render service was observed.** Nothing here is
  evidence about what any deployed host, CDN, reverse proxy or browser does
  with a conditional request. A `304` is a decision over the values the caller
  supplied.
- **No storage and no freshness.** The tool stores nothing, indexes nothing,
  evicts nothing, and never decides whether a stored response is fresh or may
  be reused. `scripts/stored_reuse.py` (r91) and
  `scripts/heuristic_freshness.py` (r92) hold that ground; this entry does
  not touch it, and no lifetime, age or storable verdict appears in its
  output.
- **No revalidation exchange and no forwarding.** The tool does not send a
  request, does not receive a `304`, does not update stored metadata, and
  does not decide whether a cache forwards, revalidates or combines
  If-None-Match lists with its own stored set. RFC 9111 §4.3.2 is cited here
  only for the applicability rule that shapes the decision order.
- **No serving decision.** `304` and `412` are statuses a recipient *would*
  answer with; the tool does not produce a response, choose a body, or decide
  what metadata accompanies the status.
- **No HTTP-date parsing and no clock.** See the adapter convention above.
  The tool reads no clock and no network.
- **No validator generation.** The tool never produces an entity-tag, never
  computes a `Last-Modified`, and never says what a representation's
  validator should be.
- **The 304 body content is not decided here.** RFC 9110 §15.4.5 (lines
  7477-7478) says a 304 response "is terminated by the end of the header
  section; it cannot contain content or trailers", and names the header
  fields a server generating a 304 MUST reproduce. The tool decides the
  status only; the header set is out of its scope.

Two narrower limits worth carrying. The contract's `304` is the status a
recipient answers a conditional GET or HEAD with; the RFC also describes
what a 304 response *contains*, and that is not this tool's output. And the
frozen counter scores the **contract**, not the RFC: its hand cases and its
seeded generated population were written by the same round as the contract,
so a passing candidate is conformance to contract v1 and never evidence about
a deployed server's behaviour. The instrument's own conformance is measured
by `.ufo/waves/round-93/c93_conditional.py`; the L1's re-run at the landing
revision is what counts.
