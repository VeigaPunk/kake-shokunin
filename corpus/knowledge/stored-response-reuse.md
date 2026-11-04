source: S469 — RFC 9111 HTTP Caching, §5.2.1 Request Directives, §4.2.1 Calculating Freshness Lifetime and §4.2.4 Serving Stale Responses (with §1.2.2 Delta Seconds for the argument form) — https://www.rfc-editor.org/rfc/rfc9111.txt; opened 2026-11-04; retained body `.ufo/waves/round-91/L1/src/rfc9111.txt` (84477 bytes, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e). S461 (duplicate/lifetime reading), S462 (§4.2.3 age arithmetic), S463 (§4.1 match profile) and S467 (§2/§4.1 construction) keep their own scopes; this row adds the request-directive, lifetime-order and stale-serving reading only.
verified-at: 2026-11-04 — this seat re-opened the retained body at that digest and located every quote below by plain-text line number (each a raw substring, ≤25 words). The decision table was read against `.ufo/waves/round-91/c2-contract.md` (sha256 faa91e096f4f9ae062d14402bbad5615c9ace8cfb2e820c519cb5cd01d768fe4). The candidate `scripts/stored_reuse.py` (sha256 5004657dbf2ae43399631f79e5d5955a8aa698b53f6127e22e2cc654ba9ad299) was run for the checklist examples below and its `--selftest` printed `selftest 45/45`; the frozen counter at lane HEAD f4fff130 read `candidate=absent … met=false` because the tool was not yet a LANE commit when this entry was written. This seat did not score C2, close a claim or commit anything.
recheck: 180d, or sooner after a source or contract change. Re-fetch https://www.rfc-editor.org/rfc/rfc9111.txt into a scratch directory of your own, compare sha256 aeb52adb…5302cf3e, and re-locate §5.2.1 (plain-text line 1111), §4.2.1 (line 652) and §4.2.4 (line 784) before reusing the conclusions. No ephemeral path is recorded in this line.
ground: operability — round-91 C2, a stored-response reuse decision over supplied integer seconds.
scope: one decision per stored response under contract v1 of this lane; not a Date parser, clock, network client, revalidation exchange, cache store, heuristic freshness, storage-key identity, Vary matching, or any claim about a live property.

# Stored-response reuse: what one stored response may be used for

A publisher engineer asks this question about a response a cache already holds:
*may I hand this stored copy to the request in front of me, or must I go back to
the origin?* RFC 9111 answers it in pieces — §5.2.1 says what the client's request
directives ask for, §4.2.1 says how long the response is fresh, §4.2.4 says when a
stale copy may still be served. `scripts/stored_reuse.py` joins those pieces into
one decision over values the caller supplies: a stored status and header map, a
request method and header map, an integer `now`, and a shared-cache flag.

Everything here is arithmetic on integers. The tool never reads a clock, opens a
socket, stores anything, or observes a live property. `Date` and `Expires` are
epoch seconds, not HTTP-dates — the same adapter convention
`scripts/cache_current_age.py` uses — and `now` is the caller's integer, so two
callers with different clocks get different, equally correct answers.

## What the instrument decides

One of seven outcomes, with the lifetime and age it computed:

`reuse`, `revalidate`, `serve-stale`, `must-revalidate-fail`, `not-storable`,
`heuristic-undecided`, `only-if-cached-miss`.

It reports the two numbers behind the decision — `freshness_lifetime` and
`current_age` — from two rules of the contract, both traceable to the source:

- **Current age** (contract clause 8, on S462's equation set):
  `current_age = max(0, Age) + max(0, now − Date)`. `Age` defaults to `0`.
- **Freshness lifetime** (contract clause 9, the order §4.2.1 fixes): `s-maxage`
  when the cache is shared and the directive is present, else `max-age`, else
  `Expires − Date`, else `null`. The order is first-match, as the source says
  (line 656 below), and `Expires` may precede `Date`, which yields a negative
  lifetime rather than an error.

A `null` lifetime is not a failure: it means the response carries no explicit
expiration, and this contract refuses to guess one.

## What it refuses to decide

Stated as a boundary, so no reader mistakes a decision for a permission:

- **No storage-key identity and no Vary field matching.** Whether *this* stored
  response is the one the presented request maps to is `scripts/cache_key.py`
  (r89) and `scripts/vary_match.py` (r88), not this tool. `Vary` enters here only
  as the `*` storability test.
- **No revalidation exchange.** §4.3 (conditional requests, 304 handling,
  updating stored metadata) is outside the contract entirely; `revalidate` means
  "do not reuse as-is", not "here is the request to send".
- **No heuristic freshness.** §4.2.2 lets a cache assign a heuristic expiration;
  this contract answers `heuristic-undecided` instead and never invents a number.
  That is a chosen narrower profile, not a reading that heuristics are wrong.
- **No stale-serving permission on its own.** §4.2.4 permits a stale response
  when a client or origin directive allows it; this tool answers `serve-stale`
  only when the *request* carries `max-stale`. A cache configured out of band to
  serve stale, or one that is disconnected, is outside the decision.
- **No live property claim.** A `reuse` verdict says nothing about what any real
  cache, CDN or browser does with the same response, and nothing about whether a
  publisher's site is served from cache.
- **No Date parsing, no clock, no network, no store.** Values in, one JSON object
  out.

## Decision table (contract clauses 10–21, first match wins)

Clauses 1–9 run first: every input is validated and the lifetime and age are
derived *before* any decision, so a malformed or missing `Date` is a refusal even
when the response would turn out to be `not-storable`.

| Clause | Condition (first match wins) | Decision | lifetime / age |
|---|---|---|---|
| 10 | request method not `GET`/`HEAD`; status outside `200 203 204 206 300 301 308 404 405 410 414 501`; `no-store` on the stored or the request side; `private` on a shared cache; a `Vary` member `*` | `not-storable` | `null` / `null` |
| 11 | no explicit lifetime (no shared `s-maxage`, no `max-age`, no `Expires`) | `heuristic-undecided` | `null` / age |
| 12 | request carries `no-cache` | `revalidate` | lifetime / age |
| 13 | stored response carries `no-cache` | `revalidate` | lifetime / age |
| 14 | request carries `max-age=N` and `current_age > N` | `revalidate` | lifetime / age |
| 15 | request carries `min-fresh=N` and `lifetime − current_age < N` | `revalidate` | lifetime / age |
| 16 | `current_age < lifetime` (the response is fresh) | `reuse` | lifetime / age |
| 17 | stale, and the stored response carries `must-revalidate`, or `proxy-revalidate` while shared | `must-revalidate-fail` | lifetime / age |
| 18 | stale, request carries `max-stale` and either it has no argument or `current_age − lifetime ≤ N` | `serve-stale` | lifetime / age |
| 19 | stale, and the client did not accept that staleness | `revalidate` | lifetime / age |
| 20 | request carries `only-if-cached` and the clause 10–19 answer is neither `reuse` nor `not-storable` | `only-if-cached-miss` | lifetime / age |
| 21 | reporting rule | — | lifetime is `null` only when clause 9 gave `null`, or on `not-storable` |

Two readings a publisher engineer will trip over, both deliberate:

- **`max-age` on the request is not `max-age` on the response.** The request
  directive is a *constraint the client states* (clause 14); the response
  directive is the *lifetime the origin granted* (clause 9). `max-age=10` in the
  request against a `max-age=60` response gives `revalidate` once the age passes
  10, and `reuse` while it does not (worked cases 16 and 17).
- **`must-revalidate` only bites when stale.** A fresh response carrying
  `must-revalidate` is still `reuse` (worked case 34); the directive forbids
  serving it *stale*, not using it while fresh.

## Error patterns

Every refusal is `invalid_input: <reason>` on stderr, nothing on stdout, exit 1.
These are the five shapes a publisher will actually hit, with the exact messages
the candidate emits (each run recorded in this seat's wave directory):

| Input | stderr | exit |
|---|---|---|
| `Cache-Control: max-age="60"` | `invalid_input: quoted delta-seconds argument: max-age` | 1 |
| `Cache-Control: max-age=60, max-age=30` | `invalid_input: duplicate Cache-Control directive: max-age` | 1 |
| `Cache-Control` and `CACHE-CONTROL` in one header map | `invalid_input: duplicate header name: CACHE-CONTROL` | 1 |
| no `Date` header at all | `invalid_input: stored response has no Date header` | 1 |
| a value containing CR, LF or NUL (here NUL in `X-N`) | `invalid_input: control character in header value: X-N` | 1 |
| `Age: -1` | `invalid_input: age must be nonnegative` | 1 |
| unknown top-level key / `stored.status` as a string / `now: -5` | `invalid_input: unknown top-level input key` / `stored status must be an integer 100..599` / `now must be a nonnegative integer` | 1 |

Why these are refusals and not silent repairs: a quoted delta-seconds value is a
sender error the source forbids (line 1128 below), so reading it as a number would
accept a message the origin should not have sent; a case-variant duplicate name is
an ambiguous header map, and this adapter declines to guess which line the caller
meant; two `max-age` directives with different arguments are a conflict the source
resolves two ways (line 679), so refusing keeps the tool out of that choice.

## Runnable checklist

Run from the lane root. Nothing is written; the tool reads stdin and writes
stdout.

1. **One example, reuse.** Input (one line):

   ```
   {"stored":{"status":200,"headers":{"Cache-Control":"max-age=60","Date":"1000000"}},"request":{"method":"GET"},"now":1000030}
   ```

   ```
   $ printf '%s' '<that object>' | python3 -B scripts/stored_reuse.py
   {"decision": "reuse", "freshness_lifetime": 60, "current_age": 30}
   ```

   exit 0. Expected exactly that line: three keys, `60` lifetime, `30` age.

2. **One example, serve-stale.** Same stored response, `now` 1000065, request
   `{"method":"GET","headers":{"Cache-Control":"max-stale=10"}}` →
   `{"decision": "serve-stale", "freshness_lifetime": 60, "current_age": 65}`,
   exit 0. Age 65 is 5 past the 60-second lifetime, inside the 10 seconds the
   client accepts.

3. **One example, refusal.** Add `"Age":"-1"` to the stored headers →
   `invalid_input: age must be nonnegative` on stderr, empty stdout, exit 1.

4. **The tool's own fixture check.**

   ```
   $ TMPDIR=$(mktemp -d) python3 -B scripts/stored_reuse.py --selftest
   selftest 45/45
   ```

   exit 0. The 45 fixtures are the contract's worked cases, in table order.

5. **The counter that scores it** (frozen; do not edit). `--work` must be an
   explicit scratch directory of your own; `--revision` must name a commit that
   contains the candidate:

   ```
   $ python3 -B .ufo/waves/round-91/c91_reuse.py --root . --revision <REV> \
       --work <explicit-scratch> --seed 91091
   ```

   Expected first line at a carrier that contains the tool:

   ```
   C2v91 revision=<sha> candidate=present hand=45/45 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok seed=91091 met=true
   ```

   exit 0; line 2 is a JSON detail object. Before the tool is committed the same
   command reads `candidate=absent hand=0/45 generated=0/120 forgeries_refused=0/5
   anti_table=n/a population=n/a … met=false`, exit 1 — measured at lane HEAD
   f4fff130 while this entry was written. The counter's own self-check is
   `python3 -B .ufo/waves/round-91/c91_reuse.py --selftest` →
   `selftest 45/45 hand cases, 120 generated, 7 decisions`, exit 0.

6. **Read the boundary before quoting a verdict.** `reuse` is a reuse decision
   over the supplied integers. It is not a cache-key match, not a revalidation
   plan, not heuristic freshness, and not evidence about any deployed cache.

## Located quotes

Retained body: `.ufo/waves/round-91/L1/src/rfc9111.txt`, 84477 bytes, sha256
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`. Each line
below is a plain-text line number in that body; each quote is a raw substring of
that line and at most 25 words (word counts in the last column).

§5.2.1 Request Directives (heading at line 1111):

| Line | Quote | Words |
|---|---|---|
| 1113 | This section defines cache request directives.  They are advisory; | 9 |
| 1128 | 'max-age=5' not 'max-age="5"'.  A sender MUST NOT generate the | 9 |
| 1137 | The max-stale request directive indicates that the client will accept | 10 |
| 1142 | will accept a stale response of any age. | 8 |
| 1145 | 'max-stale=10' not 'max-stale="10"'.  A sender MUST NOT generate the | 9 |
| 1166 | The no-cache request directive indicates that the client prefers a | 10 |
| 1197 | The only-if-cached request directive indicates that the client only | 9 |

The 1113 line is the one that keeps this tool honest about its own authority: the
request directives are *advisory*, so the contract's `revalidate` on a client
`no-cache` is this lane's conservative reading of a preference, not an RFC MUST.
Lines 1128 and 1145 are why a quoted delta-seconds argument is refused rather than
parsed; line 1142 is why a bare `max-stale` accepts a stale response of any age
(worked case 5). Line 1197 introduces `only-if-cached`; the directive's own answer
in the source is a stored response or a 504 — line 1201 reads `504 (Gateway Timeout) status code.` — and the contract's `only-if-cached-miss` is that miss
named as a decision rather than as a status the tool does not emit.

§1.2.2 Delta Seconds (heading at line 212):

```
214: The delta-seconds rule specifies a non-negative integer, representing
217: delta-seconds  = 1*DIGIT
```

Nine words and a three-word ABNF production: the argument is a bare non-negative
integer, which is why `max-age="60"` (quoted), `max-age=+60` (signed) and
`max-age=` (empty) are refusals in clause 4.

§4.2.1 Calculating Freshness Lifetime (heading at line 652):

| Line | Quote | Words |
|---|---|---|
| 656 | and using the first match: | 5 |
| 658 | If the cache is shared and the s-maxage response directive | 10 |
| 661 | If the max-age response directive (Section 5.2.2.1) is present, | 9 |
| 664 | If the Expires response header field (Section 5.3) is present, use | 11 |
| 669 | Otherwise, no explicit expiration time is present in the response. | 10 |
| 679 | age directives), either the first occurrence should be used or the | 11 |

Lines 656–669 are the lifetime order clause 9 implements, including the `null`
case at 669 that clause 11 turns into `heuristic-undecided`. Line 679 is the
duplicate-value rule: the source offers *first occurrence* **or** *treat as
stale*, and this contract takes neither — it refuses a duplicate directive with a
different argument, which is stricter than both readings and is an adapter
convention, not spec text.

§4.2.4 Serving Stale Responses (heading at line 784):

| Line | Quote | Words |
|---|---|---|
| 786 | A "stale" response is one that either has explicit expiry information | 11 |
| 790 | A cache MUST NOT generate a stale response if it is prohibited by an | 14 |
| 795 | A cache MUST NOT generate a stale response unless it is disconnected | 12 |
| 796 | or doing so is explicitly permitted by the client or origin server | 12 |

Line 786 defines stale as *not fresh under §4.2* — the same test clause 16
inverts. Lines 790–793 are the prohibition clause 17 implements: `no-cache`,
`must-revalidate`, or an applicable `s-maxage`/`proxy-revalidate` response
directive forbids a stale response outright. Lines 795–799 are the permission
clause 18 uses narrowly: this tool serves stale only when the *request* says
`max-stale`, so the disconnected-cache and out-of-band-configuration halves of
that sentence stay outside the decision.

## Adapter conventions the source does not require

Named so a later reader cannot mistake them for spec text:

- **`Date` and `Expires` are integer epoch seconds, and `Date` is required.**
  RFC 9111 §4.2.1 line 664–667 falls back to the time the message was received
  when `Date` is absent; this tool has no receipt time and refuses instead.
- **The storable-status list (clause 10) is a lane list.** The source's storage
  rules live in §3 and §15.1's heuristically-cacheable set; the twelve codes here
  are the contract's chosen list, and a status outside it is `not-storable`
  rather than "probably fine".
- **Duplicate directives and case-variant duplicate names are refused**, where
  the source either takes the first occurrence or treats the response as stale
  (line 679) and RFC 9110 §5.1/§5.2 would combine the lines in order.
- **`only-if-cached` is reported as a decision, never as a 504 status.** The tool
  emits a decision vocabulary only; emitting a status code would be an HTTP
  client, which this is not.
- **A negative `Expires − Date` lifetime is reported as-is** (worked case 12:
  `-100`), not clamped to zero; clamping belongs to age arithmetic (§4.2.3,
  S462), not to the lifetime.

## Limits

The 45 hand cases and the 120 seeded generated cases are contract conformance
evidence, not RFC conformance: they were written by the same round that wrote the
contract, and the generated population is scored against the counter's own
reference implementation of that contract. A passing candidate can still be wrong
about any RFC behaviour the contract does not encode — heuristic freshness,
revalidation, storage keys, field-specific matching. Nothing here is a statement
about a deployed cache, and no publish, deploy or account state follows from any
verdict.
