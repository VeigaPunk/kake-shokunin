source: S470 — RFC 9111 HTTP Caching, §4.2.2 Calculating Heuristic Freshness — https://www.rfc-editor.org/rfc/rfc9111.txt; opened 2026-11-04 (live GET 2026-11-05T00:30:25Z, HTTP 200, 84477 bytes, sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e); the lane's retained copy `.ufo/waves/round-92/L1/src/rfc9111.txt` has the same 84477 bytes and the same digest, so every line number below is the same line number in the fetched body. The section heading is at plain-text line 686; the four rule bodies are at lines 688-693 (permission), 695-696 (prohibition), 697-701 (cacheability restriction) and 706-709 (fraction and the 10% figure). S469 (§5.2.1 request directives, §4.2.1 lifetime order, §4.2.4 serving stale) and S462 (§4.2.3 age arithmetic) keep their own scopes; this row adds the heuristic-freshness reading only, and S028's "§4.2.2" is RFC 9110's URI-scheme section, a different document.
verified-at: 2026-11-04 — this seat opened the source itself (live GET, receipt in `.ufo/waves/round-92/w1/ScribeEntry/receipt.txt`), located §4.2.2 by plain-text line number and filed 32 located quotes (29 from RFC 9111, 3 from RFC 9110 §15.1), each verified mechanically to be a raw substring of the fetched body, of its stated line, and of this entry, every one 3-25 words (`w1/ScribeEntry/quotes.txt`; re-run: `violations=0`). The decision table below is a restatement of `.ufo/waves/round-92/c2-contract.md` v1 (sha256 5fc49c7af47ce4331563bf991e4199817eef8748621b02e05682a4f01f14c944), clauses 9-13, checked against the frozen counter's own reference implementation, which decides all 28 of its hand cases as the counter declares (`w1/ScribeEntry/refprobe.txt`); the 120 seeded generated cases are the reference's own outputs, so they are not independent evidence of anything. The instrument landed in the working tree during this seat's run and was then run against every worked example in the checklist below — all seven reproduce the described output and exit status, and `--selftest` prints `selftest 54/54` (`w1/ScribeEntry/instrument-probes.txt`); the tool was in no LANE commit at that moment. This seat did not score C2, did not write the instrument, did not commit anything, and asserts no `met`.
recheck: 180d, or sooner after a source or contract change. Re-fetch https://www.rfc-editor.org/rfc/rfc9111.txt into a scratch directory of your own, compare sha256 aeb52adb…5302cf3e, and re-locate §4.2.2 (plain-text line 686) and its four rule bodies (lines 688-693, 695-696, 697-701, 706-709) before reusing the conclusions. No ephemeral path is recorded in this line.
ground: freshness — round-92 C2, a bounded capability: assigning a heuristic expiration time to a stored response over supplied integer seconds.
scope: one decision per stored response under contract v1 of this lane. Not a clock, an HTTP-date parser, a network client, a cache store, a revalidation exchange, a reuse decision, a storage-key identity, a Vary match, or any claim about a live property.

# Heuristic freshness: when a cache may invent an expiration time

A stored response with no explicit expiration is a special case. RFC 9111 §4.2.2
gives a cache permission to invent one, a prohibition against inventing one when
the origin already said when, a gate on *which* responses may get one, and an
encouragement about *how long* the invented value should be.
`scripts/heuristic_freshness.py` — the path contract v1 names for the
instrument — turns those four rules into one decision over values the caller
supplies: a stored status and header map, an integer `now`, and a shared-cache
flag.

**State of the instrument when this entry was written (2026-11-04):** the path
`scripts/heuristic_freshness.py` did **not yet exist in the lane** when this
seat began — the executor seat that owns it was still running, and no LANE
commit contained it. Everything below about the instrument's behaviour was
therefore read from contract v1 and from the frozen counter's own reference
implementation, both of which this seat read and ran. The instrument landed in
the working tree at 21:40 local, after those readings were made; this seat then
ran it against the worked examples below and they reproduce the described
behaviour exactly (sha256
`7bfe82da8e1a1d541930ef1b4ee64cfe9b3fa5b8169680795bcc8626d2f37f5c` at that
moment, `--selftest 54/54`, exit 0 — receipts in
`.ufo/waves/round-92/w1/ScribeEntry/instrument-probes.txt`). That is a working-
tree observation, not a commit: no LANE commit contained the instrument when
this seat measured it, so the L1's landing run of the frozen counter
`.ufo/waves/round-92/c92_heuristic.py` is what decides whether the delivered
instrument matches this description.

Everything here is arithmetic on integers. The tool never reads a clock, opens a
socket, stores anything, or observes a live property. `Date`, `Expires` and
`Last-Modified` are epoch seconds, not HTTP-dates — the same adapter convention
`scripts/cache_current_age.py` and `scripts/stored_reuse.py` use.

## What the instrument decides

One of five outcomes, with the lifetime it computed and whether that lifetime is
a heuristic one:

`explicit`, `heuristic`, `not-heuristically-cacheable`, `heuristic-undecided`,
`not-storable`.

The `heuristic` flag is the point of the tool: it is `true` **only** for the
case where the cache had no explicit expiration and invented one. Every other
outcome reports `heuristic: false`.

## Decision table (contract clauses 9-13, first match wins)

Contract clauses 1-8 run first and for every input (clause 8 is the rule
"no arithmetic before validation"): a malformed field is a refusal even when the
response turns out not to be storable. The decision order below is the
contract's clauses 9-13, first match wins.

| Clause | Condition (first match wins) | Decision | `lifetime` | `heuristic` |
|---|---|---|---|---|
| 9 | the stored Cache-Control carries `no-store`; or it carries `private` and the cache is shared; or `Vary` is present with a member `*` | `not-storable` | `null` | `false` |
| 10 | an explicit expiration is present: `s-maxage` (only when the cache is shared), else `max-age`, else `Expires` (`Expires − Date`, which may be negative) | `explicit` | that value | `false` |
| 11 | no explicit expiration, the status is **not** in the heuristically-cacheable set `{200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501}`, **and** the stored Cache-Control carries no `public` directive | `not-heuristically-cacheable` | `null` | `false` |
| 12 | `Last-Modified` is present and `Last-Modified ≤ Date` | `heuristic` | `min((Date − Last-Modified) // 10, 86400)` | `true` |
| 13 | `Last-Modified` is absent, or `Last-Modified > Date` (a negative interval supports no plausible estimate) | `heuristic-undecided` | `null` | `false` |

Three readings worth naming, because each is easy to get backwards:

- **Clause 10 outranks everything.** A response with `max-age=600` *and* a
  `Last-Modified` is `explicit` with lifetime 600, never `heuristic`. This is
  the source's prohibition, not a lane preference: heuristics must not be used
  to determine freshness when an explicit expiration time is present (line 695).
- **Clause 11 is an `and` of two conditions, so `public` opens the gate on its
  own.** A `500` (not heuristically cacheable) with `Cache-Control: public` and a
  `Last-Modified` is `heuristic`, lifetime 1000 on the worked inputs. The
  disjunctive reading is grounded in §3's storage list, which names "a public
  response directive" and "a status code that is defined as heuristically
  cacheable" as two entries of one "at least one of the following" set (lines
  306-323) — the same structure RFC 9110 §15.1 uses ("unless otherwise
  indicated by the method definition or explicit cache controls").
- **Clause 13 is not a failure.** `heuristic-undecided` means the inputs do not
  support any estimate: no `Last-Modified`, or a `Last-Modified` later than
  `Date` (which would give a negative interval). The tool declines rather than
  guessing.

## The two lane conventions, and why they are not spec text

The source gives a permission, a prohibition, a gate, and an encouragement. It
gives **no algorithm and no numbers** — line 692 says "This specification does
not provide specific algorithms" and line 693 says it "does impose worst-case
constraints on their results". Two numbers in clause 12 are therefore the
lane's, and a reader must not cite them as the RFC's:

- **The 10 % fraction.** The source says caches "are encouraged to use a
  heuristic expiration value that is no more than some fraction of the interval
  since that time" (line 708) and calls 10 % a *typical setting* (line 709).
  "Encouraged" is not "required", and "typical" is not "the value". The
  contract's `// 10` is one choice among the ones the source leaves open; it
  happens to be the source's own illustrative number, and the floor division
  makes the result no more than 10 % of the interval.
- **The 86400-second cap.** The source names no cap and no interval. The
  contract caps the invented lifetime at one day, which is this lane's
  concrete way of honouring the "worst-case constraints" the source does impose
  in general terms. A different cache may cap differently, or not at all.

Everything else in clauses 9-13 is a direct reading of §4.2.2, with one
adapter convention the reader should know: **the interval is measured to
`Date`, not to `now`.** The source says "the interval since that time" without
naming an endpoint; the contract measures `Date − Last-Modified`, the age the
response had when it was produced. The consequence is that the tool's `now`
input is validated (clause 3) but **no clause of the decision uses it** — the
same response with the same headers yields the same decision and the same
lifetime at every `now`.

## How this composes with `scripts/stored_reuse.py`

The two instruments are separate tools over the same supplied integers, and
**neither calls the other**; the composition is a reader's, done by hand.

`scripts/stored_reuse.py` (round 91) decides what a cache may *do* with a
stored response — `reuse`, `revalidate`, `serve-stale`, `must-revalidate-fail`,
`not-storable`, `heuristic-undecided`, `only-if-cached-miss`. When the stored
response carries no explicit expiration, it reports `heuristic-undecided` and a
`null` `freshness_lifetime` — that tool deliberately guesses nothing. This
entry's instrument is the piece that was missing: it answers the question
`stored_reuse.py` declined to answer, and it answers it only about the
lifetime.

The relationship, precisely:

| | `scripts/stored_reuse.py` (r91) | `scripts/heuristic_freshness.py` (r92) |
|---|---|---|
| question | may this stored response be handed to the request in front of me? | may a heuristic expiration time be assigned to this stored response, and what is it? |
| when there is no explicit expiration | `heuristic-undecided`, lifetime `null` | `heuristic` with a lifetime, `not-heuristically-cacheable`, or `heuristic-undecided` |
| what it outputs | a decision plus `freshness_lifetime` and `current_age` | a decision plus `lifetime` and a `heuristic` flag |
| request side | reads the presented request's method and directives | **no request at all** — the input has `stored`, `now`, `shared` and nothing else |

So the pair composes as a two-step reading of the same stored response: run the
r92 instrument to obtain a heuristic lifetime, and read the r91 instrument's
`heuristic-undecided` as "no explicit lifetime was supplied", not as "no
lifetime is knowable". Two cautions a reader must carry:

- **The r91 `heuristic-undecided` is broader than the r92 `heuristic-undecided`.**
  The r91 verdict fires whenever no explicit lifetime exists, whether or not a
  `Last-Modified` is present. The r92 verdict subdivides that situation into
  `heuristic` (a `Last-Modified` supports an estimate), `not-heuristically-
  cacheable` (the status and the directives forbid the estimate) and
  `heuristic-undecided` (no `Last-Modified`, or one later than `Date`). The
  r92 vocabulary is the finer one; the r91 verdict is not a synonym for any
  single r92 verdict.
- **The two storability rules are not the same rule.** The r91 tool refuses a
  request that is not `GET`/`HEAD`, a status outside its own list, a
  request-side `no-store`, and it applies §3's conditions. The r92 clause 9
  names three conditions only (`no-store` in the *stored* Cache-Control,
  `private` while shared, `Vary: *`) because the r92 contract is scoped to the
  heuristic decision. A response the r91 tool calls `not-storable` may still
  receive a `heuristic` verdict from the r92 tool, and that is not a
  contradiction: the two are answering different questions over a deliberately
  narrow input.

Nothing in this entry licenses feeding the r92 lifetime into the r91 tool. No
such code path exists (`grep -rn "heuristic_freshness" scripts/` → no hits), and
the r91 contract was frozen before this round. The two measured side by side are
in `.ufo/waves/round-92/w1/ScribeEntry/composition.txt`.

## Runnable checklist

Run from the lane root. Nothing is written; the tool reads stdin and writes
stdout. The expected outputs below were read from contract v1, checked against
the frozen counter's own reference implementation, and then confirmed against
the landed instrument (`w1/ScribeEntry/instrument-probes.txt`).

1. **One example, a heuristic lifetime.** Input (one line):

   ```
   {"stored": {"status": 200, "headers": {"Date": "1000000", "Last-Modified": "990000"}}, "now": 1000000}
   ```

   ```
   $ printf '%s' '<that object>' | python3 -B scripts/heuristic_freshness.py
   {"decision": "heuristic", "heuristic": true, "lifetime": 1000}
   ```

   exit 0. Exactly three keys; `(1000000 − 990000) // 10 = 1000`, under the
   86400 cap; `heuristic` is `true` because no explicit expiration was present.
   (The tool emits the three keys in the order `decision`, `heuristic`,
   `lifetime`; the contract names them `decision`, `lifetime`, `heuristic`. The
   set is what the contract fixes, not the order.)

2. **One example, the cap.** `Last-Modified` `100000` (a 900 000-second
   interval) → `{"decision": "heuristic", "heuristic": true, "lifetime": 86400}`,
   exit 0 — 90 000 floored to the one-day cap.

3. **One example, the prohibition wins.** Add `"Cache-Control": "max-age=600"`
   to example 1's headers → `{"decision": "explicit", "heuristic": false,
   "lifetime": 600}`, exit 0. `heuristic` is `false` even though a
   `Last-Modified` is present: an explicit expiration time forbids the
   heuristic path (line 695).

4. **One example, the gate.** `"status": 500` with `Last-Modified` and no
   directives → `{"decision": "not-heuristically-cacheable", "heuristic": false,
   "lifetime": null}`, exit 0. Add `"Cache-Control": "public"` and the same
   input → `{"decision": "heuristic", "heuristic": true, "lifetime": 1000}`.

5. **One example, undecided.** `"Last-Modified": "1000001"` (later than
   `Date`) → `{"decision": "heuristic-undecided", "heuristic": false,
   "lifetime": null}`, exit 0.

6. **One example, a refusal.** Drop the `Date` header → `invalid_input: Date is
   absent` on stderr, empty stdout, exit 1.

7. **The tool's own fixture check.**

   ```
   $ TMPDIR=<scratch> python3 -B scripts/heuristic_freshness.py --selftest
   selftest 54/54
   ```

   exit 0. (The counter's own population is 28 hand cases; the tool's selftest
   is a larger fixture set of its own — 54 — and the two are different
   populations, so the two numbers are not comparable.)

8. **The counter that scores it** (frozen; do not edit). `--work` must be an
   explicit scratch directory of your own; `--revision` must name a commit that
   contains the candidate:

   ```
   $ python3 -B .ufo/waves/round-92/c92_heuristic.py --root . --revision <REV> \
       --work <explicit-scratch>
   ```

   Expected first line at a carrier that contains the tool:

   ```
   C2v92 revision=<sha> candidate=present hand=28/28 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok seed=92 met=true
   ```

   exit 0; line 2 is a JSON detail object. Before the tool is committed the same
   command reads `candidate=absent hand=0/28 generated=0/120
   forgeries_refused=0/5 anti_table=n/a population=n/a … met=false`, exit 1.
   The counter checks its own reference against all 28 hand cases before it
   scores any candidate, so a contract drift exits 2 with the drifting case
   named rather than passing silently.

9. **Read the boundary before quoting a verdict.** A `heuristic` verdict is a
   lifetime computed over the integers the caller supplied. It is not a reuse
   decision, not a storage, not a revalidation, and not evidence about any
   deployed cache.

## Error patterns

Every refusal is `invalid_input: <reason>` on stderr, nothing on stdout, exit 1.
The shape of the refusals follows contract clauses 1-7. The reason strings
below are the ones the landed instrument emits, measured
(`w1/ScribeEntry/instrument-probes.txt`):

| Input | stderr | exit | Clause |
|---|---|---|---|
| no `Date` header | `invalid_input: Date is absent` | 1 | 5 |
| `Date: 1e6` | `invalid_input: Date is not a decimal integer` | 1 | 5 |
| `Cache-Control` and `date` in one header map | `invalid_input: duplicate header name` | 1 | 1 |
| `Cache-Control: max-age=+5` | `invalid_input: max-age argument is not a bare non-negative decimal integer` | 1 | 4 |
| `Cache-Control: max-age=5, ` | `invalid_input: empty Cache-Control directive` | 1 | 4 |
| a value containing CR, LF or NUL | `invalid_input: header value contains CR, LF or NUL` | 1 | 2 |
| `now` absent or negative | `invalid_input: now is not a non-negative int` | 1 | 3 |
| an unknown top-level key | `invalid_input: unexpected top-level key extra` | 1 | input section |

Why these are refusals and not silent repairs: a case-variant duplicate name is
an ambiguous header map, and this adapter declines to guess which line the
caller meant; a signed delta-seconds value is a sender error the source forbids
(RFC 9111 §1.2.2 delta-seconds), so reading it as a number would accept a
message the origin should not have sent; a malformed field is refused even when
the response turns out not to be storable, because the tool does not decide
storability before it validates.

One consequence of the clause-3 rule is worth stating: `now` is a **required**
key even though no decision clause reads it. Omitting it is a refusal
(`invalid_input: now is not a non-negative int`), not a default. A caller that
has no notion of "now" still has to supply one.

## Located quotes

Body: https://www.rfc-editor.org/rfc/rfc9111.txt, 84477 bytes, sha256
`aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`, fetched
2026-11-05T00:30:25Z (HTTP 200). Each line below is a plain-text line number in
that body; each quote is a raw substring of that line and of the whole body, and
at most 25 words (word counts in the last column). The full filing and the
mechanical check are in `.ufo/waves/round-92/w1/ScribeEntry/quotes.txt`.

§4.2.2 heading, line 686:

| Line | Quote | Words |
|---|---|---|
| 686 | 4.2.2.  Calculating Heuristic Freshness | 4 |

The permission (lines 688-693):

| Line | Quote | Words |
|---|---|---|
| 688 | Since origin servers do not always provide explicit expiration times, | 10 |
| 689 | a cache MAY assign a heuristic expiration time when an explicit time | 12 |
| 690 | is not specified, employing algorithms that use other field values | 10 |
| 691 | (such as the Last-Modified time) to estimate a plausible expiration | 10 |
| 692 | time.  This specification does not provide specific algorithms, but | 9 |
| 693 | it does impose worst-case constraints on their results. | 8 |

Line 689 is the permission clause 10 protects ("Heuristics are never used when
an explicit expiration time is present"). Line 691 names `Last-Modified` as the
field the algorithm may use — the field clause 12 reads. Lines 692-693 are the
sentence that keeps the two lane conventions honest: the source supplies no
algorithm and no number, only a general worst-case constraint.

The prohibition (lines 695-696):

| Line | Quote | Words |
|---|---|---|
| 695 | A cache MUST NOT use heuristics to determine freshness when an | 11 |
| 696 | explicit expiration time is present in the stored response. | 9 |

This is the one MUST in the section. It is what makes clause 10 an ordering
rule rather than a preference, and what makes `heuristic: true` mean exactly
"no explicit expiration was present".

The cacheability restriction (lines 697-701):

| Line | Quote | Words |
|---|---|---|
| 697 | of the requirements in Section 3, heuristics can only be used on | 12 |
| 698 | responses without explicit freshness whose status codes are defined | 9 |
| 699 | as "heuristically cacheable" (e.g., see Section 15.1 of [HTTP]) and | 10 |
| 700 | on responses without explicit freshness that have been marked as | 10 |
| 701 | explicitly cacheable (e.g., with a public response directive). | 8 |

Line 697 points the rule at §3, and §3's storage list (line 306, "the response
contains at least one of the following", with line 323 naming "a status code
that is defined as heuristically cacheable") is what grounds the disjunctive
reading of clause 11. Line 699 points the status set at RFC 9110 §15.1, where
the codes are enumerated (see below). Line 701 names `public` as the
explicitly-cacheable marker clause 11 tests.

The fraction and the 10 % figure (lines 706-709):

| Line | Quote | Words |
|---|---|---|
| 706 | If the response has a Last-Modified header field (Section 8.8.2 of | 11 |
| 707 | [HTTP]), caches are encouraged to use a heuristic expiration value | 10 |
| 708 | that is no more than some fraction of the interval since that time. | 13 |
| 709 | A typical setting of this fraction might be 10%. | 9 |

Line 707's "encouraged" and line 709's "might be" are why the 10 % is recorded
above as a lane convention and not as spec text; line 708 is also why the
contract caps the value rather than computing an unbounded fraction.

The heuristically-cacheable status set, from RFC 9110 §15.1 — the section
RFC 9111 §4.2.2 line 699 points to. Read from the lane's retained body
`.ufo/waves/round-89/L1/src/rfc9110.txt` (502941 bytes, sha256
`21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a`), **not**
re-fetched by this seat:

| Line | Quote | Words |
|---|---|---|
| 6846 | Responses with status codes that are defined as heuristically | 9 |
| 6847 | cacheable (e.g., 200, 203, 204, 206, 300, 301, 308, 404, 405, 410, | 12 |
| 6848 | 414, and 501 in this specification) can be reused by a cache with | 13 |

That list is exactly the contract's twelve codes. The `e.g.` in RFC 9111 line 699
is why the contract's list is the RFC 9110 §15.1 list and not a re-invention.

The pointer back from §4.2.1, which is why this section sits where it does in
the source's own structure:

| Line | Quote | Words |
|---|---|---|
| 669 | Otherwise, no explicit expiration time is present in the response. | 10 |
| 670 | A heuristic freshness lifetime might be applicable; see | 8 |

These two lines (line 671 is the two-word cross-reference "Section 4.2.2.") are
the source's own statement of the gap this instrument fills: §4.2.1's lifetime
order ends with "no explicit expiration time is present", and points at §4.2.2
for what may happen then. The word is *might* — the source permits a heuristic
lifetime, it does not require one, which is exactly what the
`heuristic-undecided` outcome is for.

### Supporting anchors

The four rules above are the section's own text. These are the neighbouring
passages the lane's reading leans on, quoted so the reading can be checked
against the bytes rather than taken on trust.

§3's storage list, which grounds the disjunctive reading of clause 11:

| Line | Quote | Words |
|---|---|---|
| 306 | the response contains at least one of the following: | 9 |
| 323 | a status code that is defined as heuristically cacheable (see | 10 |

§4.1's wildcard rule, which the contract reads as a storability bar:

| Line | Quote | Words |
|---|---|---|
| 557 | "*" always fails to match. | 5 |

§5.2.2.7 `private`, unqualified against qualified:

| Line | Quote | Words |
|---|---|---|
| 1327 | The unqualified private response directive indicates that a shared | 9 |
| 1328 | cache MUST NOT store the response (i.e., the response is intended for | 12 |
| 1334 | If a qualified private response directive is present, with an | 10 |
| 1335 | argument that lists one or more field names, then only the listed | 12 |

§3's shared-cache `private` rule, which is what makes the contract's clause 9
stricter than the RFC:

| Line | Quote | Words |
|---|---|---|
| 297 | if the cache is shared: the private response directive is either | 11 |
| 298 | not present or allows a shared cache to store a modified response; | 10 |

## Adapter conventions the source does not require

Named so a later reader cannot mistake them for spec text:

- **`Date`, `Expires` and `Last-Modified` are integer epoch seconds, and `Date`
  is required.** RFC 9111 §4.2.1 falls back to the time the message was received
  when `Date` is absent; this adapter has no receipt time and refuses instead.
  It also parses no HTTP-date.
- **The twelve heuristically-cacheable codes are read from RFC 9110 §15.1**, as
  quoted above; the contract restates them as a literal set.
- **The interval is measured to `Date`**, not to `now`, and `now` is therefore
  validated but unused by clauses 9-13.
- **The `not-storable` gate is three conditions, not §3's full list.** RFC 9111
  §3 (lines 284-330) also conditions storage on the request method being
  understood, the status being final, the cache understanding a 206/304 or a
  `must-understand` response, and the `Authorization` field on a shared cache.
  The contract's clause 9 names only `no-store`, `private`-while-shared and
  `Vary: *` because the heuristic decision is scoped narrowly.
- **`Vary: *` is treated as not-storable.** The source says such a stored
  response "always fails to match" (line 557, §4.1) — a matching rule, not a
  storage rule; reading it as a storability bar is this lane's convention.
- **A qualified `private` is treated like an unqualified one.** RFC 9111
  §5.2.2.7 (lines 1327-1338) distinguishes them: the *unqualified* `private`
  means "a shared cache MUST NOT store the response", while a *qualified*
  `private="Set-Cookie"` limits only the listed fields to a single user and
  lets a shared cache store the remainder. The contract's clause 9 tests only
  for the presence of the directive name, so `private="Set-Cookie"` on a shared
  cache is `not-storable` here — stricter than §3's rule, which admits a
  private directive that "allows a shared cache to store a modified response"
  (lines 297-299). Stated so a reader does not take the refusal for a reading
  of the RFC.
- **The `heuristic` flag is reported, not inferred by the caller.** The tool
  says whether *this* lifetime was a heuristic one, so a consumer cannot
  mistake a heuristic value for an explicit one.

## What this does not claim

- **No live cache was observed.** Nothing here is evidence about what any
  deployed cache, CDN, reverse proxy or browser does with a response that
  carries no explicit expiration. A `heuristic` verdict is a decision over the
  integers the caller supplied.
- **No storage.** The tool does not store, index, evict or retain anything; it
  assigns a number to a response the caller already holds. Cache-key identity
  and `Vary` matching are `scripts/cache_key.py` (r89) and
  `scripts/vary_match.py` (r88), not this tool.
- **No revalidation.** RFC 9111 §4.3 — conditional requests, 304 handling,
  updating stored metadata — is outside the contract entirely. A `heuristic`
  lifetime does not authorise a conditional request, and it is not an answer
  about validators.
- **No browser behaviour.** Nothing here says what a user agent, a service
  worker, or a fetch implementation does with a response lacking an explicit
  expiration, and nothing here is a claim about any live property, published
  site, or deploy.

Two narrower limits. The RFC's own note (lines 711-717) records that RFC 2616
§13.9 used to prohibit heuristic freshness for URIs with query components; the
contract has no URI input at all, so that note is out of scope rather than
discharged. And the 28 hand cases and 120 seeded generated cases are **contract**
conformance evidence, written by the round that wrote the contract: a passing
candidate can still be wrong about any RFC behaviour the contract does not
encode, and about any heuristic algorithm the source deliberately leaves open.
