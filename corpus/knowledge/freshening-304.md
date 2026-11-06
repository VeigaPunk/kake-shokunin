source: S484, S485, S486, S487 — RFC 9111 (June 2022) §4.3.4 "Freshening Stored Responses upon Validation", §3.2 "Updating Stored Header Fields", the §3.1 "Storing Header and Trailer Fields" exceptions §3.2 points at, and §5.2 "Cache-Control" with §5.2.2.4 "no-cache", §5.2.2.7 "private" and §5.2.3 "Extension Directives", retained at `.ufo/waves/round-99/sources/rfc9111.txt` (sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e, 84 477 bytes, 1 956 lines); RFC 9110 (June 2022) §5.5 "Field Values", §5.6.1.2 "Recipient Requirements", §5.6.2 "Tokens" and §5.6.4 "Quoted Strings", retained at `.ufo/waves/round-100/sources/rfc9110.txt` (sha256 21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a, 502 941 bytes, 10 785 lines); RFC Editor erratum EID 9185 (Reported, Technical, on the §4.3.4 initial-set paragraph), retained at `.ufo/waves/round-99/sources/eid9185.html` (sha256 83c3b795290e09842d1af973f73b52c98fd661bf77cafc17658eb5ac4df63dd3)
verified-at: 2026-11-06
recheck: 180d (due 2027-05-05), or sooner after a change to the retained RFC bodies or to contract v2 of this lane
ground: freshness — the 304 freshening capability of this lane: which stored responses a 304 (Not Modified) freshens, and which of their header fields the 304 changes, decided over supplied values.
scope: one decision per 304 response over an initial set of stored responses the caller supplies, under contract v2 of this lane, which supersedes contract v1 for this decision; not the initial-set computation itself (§4 reuse conditions, cache keys or Vary), not HEAD freshening (§4.3.5), not invalidation (§4.4), not §3.4 partial-content combination, not §4.1 selecting-header re-association, not trailer fields, not storing the 304 itself, not Age or Date recalculation, not any clock, network or live cache.

# Freshening stored responses upon a 304: which responses are updated, and which header fields change

RFC 9111 §4.3.4 is the rule that decides which stored responses a cache may
update when it receives a 304 (Not Modified), and §3.2 is the rule that decides
what the updated response's header fields look like afterwards. The two are
separate steps: §4.3.4 selects, §3.2 updates.

This entry records what the two sections say, marks which clause of the decision
is fixed by the RFC and which is a convention this lane chose, names the
contract that fixes those conventions, and states plainly what it does not
decide. Every quotation below is a whitespace-collapsed substring of the body
named for it: the RFC 9111 and RFC 9110 quotations are located by plain-text
line number in the retained RFC bodies, and the erratum quotations are checked
against the retained errata page.

The governing contract is version 2 of this lane's 304-freshening contract,
which supersedes version 1. Everything version 1 fixed still holds unless the
version 2 clauses say otherwise; the changes are the Cache-Control test, the
trimming of output values, and the treatment of proxy-specific fields. The
section "Contract v2" below states each change and what it rests on.

## What RFC 9111 §4.3.4 says about the initial set

§4.3.3 puts the 304 in the validation flow (line 935):

> A 304 (Not Modified) response status code indicates that the stored response can be updated and reused

and §4.3.4 opens by naming the work that follows (line 953):

> When a cache receives a 304 (Not Modified) response, it needs to identify stored responses that are suitable for updating

The first thing the section fixes is *which* stored responses are even
candidates. The initial set is defined by exclusion from §4's reuse conditions
(line 957):

> The initial set of stored responses to update are those that could have been chosen for that request

and §4.3.4 then narrows that set further by a first-match filter (line 962):

> Then, that initial set of stored responses is further filtered by the first match of:

The initial set is thus a property of the request and of the stored responses,
not something the 304 alone determines. This entry does not compute it: the
contract takes the initial set as supplied by the caller, and contract v2 keeps
that.

## The three first-match rules

The first match of three rules applies, in the order the section lists them.

**Rule 1 — strong validators.** When the new response carries a strong
validator (line 965):

> If the new response contains one or more "strong validators" (see Section 8.8.1 of [HTTP])

every stored response in the initial set carrying the same strong validator is
identified for update (line 967):

> All the stored responses in the initial set with one of those same strong validators are identified for update.

and when none of the initial set carries one of them, the new response must not
be used to update anything (line 970):

> then the cache MUST NOT use the new response to update any stored responses

**Rule 2 — weak validators.** When the new response carries no strong validator
but does carry one or more weak ones (line 974):

> If the new response contains no strong validators but does contain one or more "weak validators"

the most recent of the matching stored responses is the one identified (line 976):

> then the most recent of those matching stored responses is identified for update.

**Rule 3 — no validator.** When the new response carries no validator at all
(line 979):

> If the new response does not include any form of validator

the single stored response is identified only when it is the only one and it
too lacks a validator (line 982):

> there is only one stored response in the initial set, and that stored response also lacks a validator

Each rule identifies at most what it names; §4.3.4 does not say what to do
when a rule identifies nothing beyond the strong rule's explicit prohibition.

## What RFC 9111 §3.2 says about updating stored header fields

Once a stored response is identified, §4.3.4 hands the update to §3.2 (line 986):

> the cache MUST update its header fields with the header fields provided in the 304 (Not Modified) response

§3.2 states the update as a replacement of present values (line 375):

> the cache MUST add each header field in the provided response to the stored response, replacing field values that are already present

and then names four exceptions (line 377):

> with the following exceptions:

The four exceptions are, in the order the section lists them: fields excepted
from storage in §3.1 (line 379):

> Header fields excepted from storage in Section 3.1,

fields the stored response depends upon (line 381):

> Header fields that the cache's stored response depends upon

fields the recipient processes and removes automatically (line 384):

> Header fields that are automatically processed and removed by the recipient

and the Content-Length field itself (line 387):

> The Content-Length header field.

§3.2 also records a MAY for caches that store the *result* of processing rather
than the response (line 393):

> MAY omit these header fields from updating stored responses on an exceptional basis

and it forecloses reading the Content-* prefix as an omission rule (line 412):

> the Content-* prefix is not a signal that a header field is omitted from update

## The §3.1 exceptions §3.2 points at

§3.2's first exception points back at §3.1, which requires every received
header field to be stored, unrecognized ones included (line 340):

> Caches MUST include all received response header fields -- including unrecognized ones -- when storing a response

§3.1 then lists four exceptions to that requirement.

**§3.1 exception 1 — the Connection field and the fields it names** (line 345):

> fields whose names are listed in it are required by Section 7.6.1 of [HTTP] to be removed before forwarding the message

**§3.1 exception 2 — fields whose semantics require removal before
forwarding** (line 350):

> some fields' semantics require them to be removed before forwarding the message

**§3.1 exception 3 — qualified no-cache and private directives** (line 354):

> The no-cache (Section 5.2.2.4) and private (Section 5.2.2.7) cache directives can have arguments that prevent storage of header fields

**§3.1 exception 4 — proxy-specific fields** (line 358):

> Header fields that are specific to the proxy that a cache uses when forwarding a request MUST NOT be stored

which the section bounds to three fields (line 361):

> Effectively, this is limited to Proxy-Authenticate (Section 11.7.1 of [HTTP]), Proxy-Authentication-Info (Section 11.7.3 of [HTTP]), and Proxy-Authorization (Section 11.7.2 of [HTTP]).

## The lane conventions

The contract that governs this decision is
`.ufo/waves/round-100/fresh304-contract-v2.md` (sha256
343b3a558c5d2fb3059f9f9e1de2d26d0c9d7ff9fb977035f905b0729d09a092), which
supersedes `.ufo/waves/round-99/fresh304-contract.md` (sha256
2be46b4d8dcc57539b0a45e2e3b7b57e76cb1c4e570891e8cdea88c5ebbba2a6). Six of
the earlier contract's choices are **lane conventions**: they are this lane's
reading, not a requirement of RFC 9111, and each was marked in the contract
with an LC tag.

- **LC1 — Last-Modified is always a weak validator.** A lane convention: RFC
  9110 §8.8.2.2 makes a Last-Modified value implicitly weak unless strength
  can be deduced, and this lane never deduces it, so a stored response is never
  selected by the strong rule on a Last-Modified value. That RFC 9110 sentence
  is at plain-text lines 3530-3531 of the retained body
  `corpus/lessons/round-81-gate/rfc9110.txt`; it is stated here as the
  contract's ground, not quoted from the RFC 9111 body this entry quotes from.
- **LC2 — the meaning of "corresponds" in rule 2.** A lane convention: a
  stored response corresponds to the 304 when, for every validator the 304
  carries, the stored response carries the same field and it matches — ETag by
  weak comparison (opaque tags equal ignoring `W/`), Last-Modified by trimmed
  equality.
- **LC3 — a tie on the most recent response is a refusal.** A lane convention:
  when two or more corresponding stored responses share the largest `received`
  value, the case is refused rather than resolved by an arbitrary tie-break.
  RFC 9111 §4.3.4 says "the most recent" and does not say what to do when two
  are equally recent.
- **LC4 — the fixed list of fields never copied.** A lane convention: the
  contract's reading of §3.1 exception 2 is a fixed set —
  `keep-alive`, `proxy-connection`, `te`, `transfer-encoding`, `upgrade` — and
  no other field is dropped on that ground.
- **LC5 — §3.2's other exceptions are not modelled.** A lane convention: the
  "depends upon" exception, the "automatically processed and removed"
  exception and the MAY-omit allowance are not modelled, so no field is
  excluded beyond the ones named above. The RFC permits those exclusions; this
  lane does not exercise them.
- **LC6 — qualified no-cache and private are refused, not excluded.** A lane
  convention, and the one contract v2 replaces. Version 1 refused a 304 whose
  Cache-Control carried a qualified `no-cache="` or `private="` form as outside
  the contract, rather than handling it by dropping the named fields. Version 2
  keeps that outcome and widens the test: it recognises the qualified form in
  either argument syntax and in any case, it ignores unrecognised extension
  directives instead of refusing them, and it refuses an unparseable list.
  The widened form is stated in the "Contract v2" section below.

  Version 1's LC6 also left one reading difference open: it did not say
  whether `no-cache="` is matched case-sensitively, and the lane's reference
  and the tool built under it matched it case-insensitively (RFC 9111 §5.2
  compares directive names case-insensitively). Version 2 closes that
  difference by stating the comparison explicitly, so a reader who took
  version 1's sentence literally and one who took the implementation's
  behaviour no longer differ.

Contract v2 adds one further lane convention, **LC8** — refusing an
unparseable Cache-Control list — and states the seven escape classes as
binding hand cases. Both are in the "Contract v2" section below.

## The decision table

The first-match rule is decided by the 304 alone; the identified set is what
that rule names.

| Validators the 304 carries | Rule | Identified set | Decision |
|---|---|---|---|
| A strong ETag | `strong` | Every stored response in the initial set whose ETag is strong and equal to it, compared character for character; none so matched → nothing identified | `update` when the set is non-empty, otherwise `must-not-update` |
| No strong validator, but a weak ETag and/or Last-Modified | `weak` | The single corresponding stored response with the largest `received`; a tie on the largest `received` → refusal; no correspondence → nothing identified | `update` when the set is non-empty, otherwise `no-update` |
| Neither ETag nor Last-Modified | `no-validator` | The stored response, but only when the initial set holds exactly one element and it carries neither ETag nor Last-Modified; otherwise nothing identified | `update` when the set is non-empty, otherwise `no-update` |

The updated header map of an identified response starts from the stored headers
and adds every header field of the 304, replacing a present field of the same
case-insensitive name, except for the fields never copied: `content-length`
(§3.2's fourth exception), `connection` and every field name listed in the
304's `Connection` value (§3.1 exception 1), the LC4 list (§3.1 exception 2),
and `proxy-authenticate`, `proxy-authentication-info`, `proxy-authorization`
(§3.1 exception 4). Field names in the output are lowercased. On values,
contract v1 copied them byte for byte; contract v2 trims the leading and
trailing whitespace of every output value and keeps the inner whitespace byte
for byte, as stated below.

## Contract v2 (round 100)

Contract v2 changes three things and binds seven hand cases. Each change is
stated here with the RFC text it rests on; the parts of contract v1 that v2
does not touch are unchanged and are described above. The RFC 9111 text below
is S486 and the RFC 9110 text is S487.

### The Cache-Control of the 304 (the replacement for LC6)

Only the 304's own Cache-Control is examined; a stored response's
Cache-Control value is copied as data and never tested.

The 304's Cache-Control field name is compared case-insensitively, and its
value is parsed as an RFC 9111 §5.2 list (S486). RFC 9111 §5.2 identifies a
cache directive by a token (line 1098):

> Cache directives are identified by a token

and gives the directive an optional argument that may use either syntax
(line 1099):

> and have an optional argument that can use both token and quoted-string syntax

The RFC asks recipients to take both argument forms (line 1101):

> recipients ought to accept both forms, even if a specific form is required for generation.

and gives the grammar (line 1106):

> cache-directive = token [ "=" ( token / quoted-string ) ]

The list around the directives is the RFC 9110 §5.6.1.2 list syntax, in which
a recipient must accept empty list elements (line 1695):

> A recipient MUST parse and ignore a reasonable number of empty list elements

and which is written (line 1702):

> #element => [ element ] *( OWS "," OWS [ element ] )

The argument of a directive is a token (RFC 9110 §5.6.2, line 1730):

> Tokens are short textual identifiers that do not include whitespace or delimiters.

written (line 1733):

> token = 1*tchar

or a quoted string, which RFC 9110 §5.6.4 describes as a single value (line
1783):

> A string of text is parsed as a single value if it is quoted using double-quote marks.

and writes (line 1786):

> quoted-string = DQUOTE *( qdtext / quoted-pair ) DQUOTE

whose quoted-pair element is (line 1794):

> quoted-pair = "\" ( HTAB / SP / VCHAR / obs-text )

The qualified forms are the ones RFC 9111 defines with an argument. For
`no-cache` (line 1273):

> The qualified form of the no-cache response directive, with an argument that lists one or more field names

and for `private` (line 1334):

> If a qualified private response directive is present, with an argument that lists one or more field names

Both sections state the syntax of that argument — §5.2.2.4 at line 1286 and
§5.2.2.7 at line 1344:

> This directive uses the quoted-string form of the argument syntax.

The qualified form's meaning is what §3.1 exception 3 records: a qualified
`no-cache` or `private` "can have arguments that prevent storage of header
fields" (line 354). A directive the recipient does not recognise is a
different case; RFC 9111 §5.2.3 says (line 1411):

> A cache MUST ignore unrecognized cache directives.

The decision contract v2 fixes is therefore:

| The 304's Cache-Control | Decision |
|---|---|
| `no-cache` or `private` **with an argument**, in token form or quoted-string form (the empty quoted string `""` counts), the directive name matched ignoring ASCII case | refused: `invalid_input: qualified cache-control outside contract` |
| `no-cache` or `private` **without** an argument (unqualified) | ignored for this test; the 304 is processed as usual |
| any other directive, including an unrecognised extension whose name merely contains or ends in `no-cache` or `private` (`x-no-cache="a"`, `no-cachex=1`) | ignored, as RFC 9111 §5.2.3 requires |
| a value that does not parse as an RFC 9111 §5.2 list | refused: `invalid_input: malformed cache-control` |
| the stored response's own Cache-Control | copied as data; never tested |

The last row of that table is **LC8**, a lane convention: refusing an
unparseable list is this lane's choice, not an RFC requirement. The lane
refuses because a list it cannot parse cannot be checked for the qualified
forms, so failing closed is the safe reading; RFC 9111 does not require the
refusal.

### Output values are field values without surrounding whitespace

Every header value in the output — whether it came from the stored response or
from the 304 — has its leading and trailing spaces and tabs removed, and its
inner whitespace is kept byte for byte. RFC 9110 §5.5 (S487) states
(line 1591):

> A field value does not include leading or trailing whitespace.

and requires the exclusion (line 1593):

> a field parsing implementation MUST exclude such whitespace prior to evaluating the field value.

Contract v1 copied values byte for byte instead, which is what this clause
replaces. The ETag and Last-Modified comparisons are unchanged: values are
trimmed before they are compared.

### No proxy-specific field in an updated response

`proxy-authenticate`, `proxy-authentication-info` and `proxy-authorization`
never appear in an updated response. Version 1 already withheld them from the
304's copy; version 2 also drops them when the *stored* response carries
them, because the updated header map is the new stored response and RFC 9111
§3.1 exception 4 (S486) says (line 358):

> Header fields that are specific to the proxy that a cache uses when forwarding a request MUST NOT be stored

No other stored field is dropped: a stored `connection`, a stored hop-by-hop
field (the LC4 names), a stored `content-length` and every other stored field
stay (escape class e1 below).

### The seven escape classes

Contract v2 states seven hand cases that bind the earlier contract's looser
wording. Each row is a decision, not a description of a tool.

| Class | The decision it binds |
|---|---|
| e1 | The update starts from **all** stored fields, except the three proxy-specific names that clause V2-3 drops. |
| e2 | A malformed ETag in **any** stored response is refused, whether or not the selection reads it. |
| e3 | The Last-Modified comparison trims spaces **and** tabs at both ends. |
| e4 | On refusal stdout is empty (zero bytes). On a decision stdout is one JSON object with no leading whitespace, optionally followed by exactly one newline, nothing else. |
| e5 | Stdin that is not valid JSON, or not UTF-8, is refused with `invalid_input:` on stderr and exit 1, never a traceback. |
| e6 | `age`, and every other 304 field not excluded by version 1 or by clause V2-3, is copied (LC5 unchanged). |
| e7 | The LC3 tie at the largest `received` is refused, whatever validators the 304 carries. |

### What contract v2 closes, and what stays open

Contract v2 closes four numbered findings that the review of the earlier
contract raised against it, and leaves seven open. The numbering is the one
contract v2 uses.

Closed by version 2:

- **F1 — the token form of a qualified directive.** Version 1's LC6 matched
  only the quoted form, so `no-cache=Set-Cookie` was processed as an ordinary
  304 although it is the same qualified directive under the RFC 9111 §5.2
  grammar. Version 2 treats a qualified `no-cache` or `private` in either
  argument form and in any case as outside the contract.
- **F2 — output values copied byte for byte.** Version 1 copied leading and
  trailing spaces and tabs into the updated response although RFC 9110 §5.5
  says a field value does not include them. Version 2 trims them.
- **F3 — proxy-specific fields carried over from the stored response.** A
  stored response that already holds `proxy-authorization` came back with it
  in the updated map. Version 2 drops the three proxy-specific names from the
  stored side too.
- **F10 — the substring test on the Cache-Control value.** Version 1's test
  refused an unrecognised extension directive such as `x-no-cache="a"` that
  merely ended in the name of a known directive, although RFC 9111 §5.2.3 says
  a cache MUST ignore unrecognised cache directives. Version 2 matches the
  whole directive name and ignores the extension.

Still open, and therefore not decided by this entry:

- **F4 — the initial set has no named definition.** The contract takes the
  initial set as supplied by the caller and never computes it; the erratum on
  the §4.3.4 initial-set paragraph is Reported, not Verified, and is not
  normative.
- **F5 — "most recent" is receipt order, and is not marked.** The contract
  reads "the most recent" as the largest `received` integer, receipt order.
  The review asked for that reading to be marked as a lane convention; it is
  not marked in contract v2, whose new convention is numbered LC8.
- **F6 — obs-text is mapped to code points, not octets.** RFC 9110 §5.5
  defines obs-text as the octet range %x80-FF; the contract maps it to the
  code points U+0080-U+00FF, so a UTF-8 entity-tag whose octets are all
  obs-text is refused as malformed.
- **F7 — the quantifier in "correspond".** §4.3.4 says the most recent of
  "those validators [that] correspond to one of the initial set's stored
  responses" without defining the quantifier; LC2 is this lane's reading and
  it decides cases.
- **F8 — a §3.1 MAY is presented as a requirement.** §3.1's Connection and
  hop-by-hop exceptions are MAYs; the contract excludes those fields from the
  update as if they were required.
- **F9 — Last-Modified accepts any string.** The contract compares
  Last-Modified values as trimmed octet strings and never parses an HTTP-date.
- **F11 — the stored-side refusal is broader than the RFC requires.** A
  malformed ETag on a stored response that the selection never reads refuses
  the whole call, which no RFC text requires.

Contract v2 also moved the three items of a further finding into its
not-covered list: the erratum's re-association rule, §3.4 partial-content
combination, and §4.1 selecting-header matching. Contract v1 and its frozen
counter are unchanged.

## The contract and the counter

The contract names one candidate path, `scripts/freshen_304.py`, and fixes its
interface: it reads one JSON object on stdin, writes one JSON object on
stdout, exits 0, and refuses on stderr with `invalid_input: <reason>` and exit
1 without writing to stdout. The counter that scores a candidate against the
contract is `.ufo/waves/round-100/c100_fresh304.py` (sha256
e7dff63b93d33254ea278bf34d18ae98fc1462616aedad46e6ff416c6d3f3fed), which
prints one line:

    candidate=<absent|present> sha256=<hex> hand=a/b generated=c/d refusals=e/f seed=S met=<bool>

It runs each candidate inside a sandbox with new user, PID, network, IPC and
UTS namespaces, a read-only `/usr`, a private `/tmp` and its own `/proc`, an
empty environment apart from `PATH`, `LANG` and `HOME`, only the candidate file
bound in, and `/tmp` as the working directory. If the sandbox cannot start,
the counter exits 2 (could-not-evaluate) and scores nothing. The earlier counter
`.ufo/waves/round-99/c99_fresh304.py` (sha256
d13bba5d6b663b171ab57d42b5ec054b5f73d8deb8f9fd64f14adad455b6bc4b`) scores the
earlier contract, so it is expected to disagree with a candidate built to
contract v2 on the qualified-form and trimming clauses; it does not score this
decision.

This entry describes the decision the contract defines. It reports no
measurement of any candidate and makes no claim that a candidate conforms to
the contract.

## The quotes, with their locations

Every quote below is a whitespace-collapsed substring of the retained body,
taken from the stated plain-text line, and at most 25 whitespace-separated
words. `quotes-check.txt` records the substring check for each of them, with
the body, the id, the line, the word count and the found/not-found result.
The quotations in the erratum section come from the retained errata page
instead, and their check is `erratum-wording-check.txt`.

| # | Body | Row | Line | Words | Quote |
|---|---|---|---|---|---|
| Q1 | rfc9111.txt | S484 | 957 | 18 | The initial set of stored responses to update are those that could have been chosen for that request |
| Q2 | rfc9111.txt | S484 | 962 | 15 | Then, that initial set of stored responses is further filtered by the first match of: |
| Q3 | rfc9111.txt | S484 | 965 | 15 | If the new response contains one or more "strong validators" (see Section 8.8.1 of [HTTP]) |
| Q4 | rfc9111.txt | S484 | 967 | 19 | All the stored responses in the initial set with one of those same strong validators are identified for update. |
| Q5 | rfc9111.txt | S484 | 970 | 14 | then the cache MUST NOT use the new response to update any stored responses |
| Q6 | rfc9111.txt | S484 | 974 | 16 | If the new response contains no strong validators but does contain one or more "weak validators" |
| Q7 | rfc9111.txt | S484 | 976 | 13 | then the most recent of those matching stored responses is identified for update. |
| Q8 | rfc9111.txt | S484 | 979 | 11 | If the new response does not include any form of validator |
| Q9 | rfc9111.txt | S484 | 982 | 18 | there is only one stored response in the initial set, and that stored response also lacks a validator |
| Q10 | rfc9111.txt | S484 | 986 | 18 | the cache MUST update its header fields with the header fields provided in the 304 (Not Modified) response |
| Q11 | rfc9111.txt | S484 | 375 | 22 | the cache MUST add each header field in the provided response to the stored response, replacing field values that are already present |
| Q12 | rfc9111.txt | S484 | 377 | 4 | with the following exceptions: |
| Q13 | rfc9111.txt | S484 | 379 | 8 | Header fields excepted from storage in Section 3.1, |
| Q14 | rfc9111.txt | S484 | 381 | 9 | Header fields that the cache's stored response depends upon |
| Q15 | rfc9111.txt | S484 | 384 | 11 | Header fields that are automatically processed and removed by the recipient |
| Q16 | rfc9111.txt | S484 | 387 | 4 | The Content-Length header field. |
| Q17 | rfc9111.txt | S484 | 393 | 13 | MAY omit these header fields from updating stored responses on an exceptional basis |
| Q18 | rfc9111.txt | S484 | 412 | 15 | the Content-* prefix is not a signal that a header field is omitted from update |
| Q19 | rfc9111.txt | S484 | 340 | 17 | Caches MUST include all received response header fields -- including unrecognized ones -- when storing a response |
| Q20 | rfc9111.txt | S484 | 345 | 21 | fields whose names are listed in it are required by Section 7.6.1 of [HTTP] to be removed before forwarding the message |
| Q21 | rfc9111.txt | S484 | 350 | 12 | some fields' semantics require them to be removed before forwarding the message |
| Q22 | rfc9111.txt | S484 | 354 | 19 | The no-cache (Section 5.2.2.4) and private (Section 5.2.2.7) cache directives can have arguments that prevent storage of header fields |
| Q23 | rfc9111.txt | S484, S486 | 358 | 20 | Header fields that are specific to the proxy that a cache uses when forwarding a request MUST NOT be stored |
| Q24 | rfc9111.txt | S484 | 361 | 21 | Effectively, this is limited to Proxy-Authenticate (Section 11.7.1 of [HTTP]), Proxy-Authentication-Info (Section 11.7.3 of [HTTP]), and Proxy-Authorization (Section 11.7.2 of [HTTP]). |
| Q25 | rfc9111.txt | S484 | 935 | 17 | A 304 (Not Modified) response status code indicates that the stored response can be updated and reused |
| Q26 | rfc9111.txt | S484 | 953 | 20 | When a cache receives a 304 (Not Modified) response, it needs to identify stored responses that are suitable for updating |
| Q27 | rfc9111.txt | S486 | 1098 | 7 | Cache directives are identified by a token |
| Q28 | rfc9111.txt | S486 | 1099 | 13 | and have an optional argument that can use both token and quoted-string syntax |
| Q29 | rfc9111.txt | S486 | 1101 | 15 | recipients ought to accept both forms, even if a specific form is required for generation. |
| Q30 | rfc9111.txt | S486 | 1106 | 11 | cache-directive = token [ "=" ( token / quoted-string ) ] |
| Q31 | rfc9111.txt | S486 | 1273 | 18 | The qualified form of the no-cache response directive, with an argument that lists one or more field names |
| Q32 | rfc9111.txt | S486 | 1286 | 10 | This directive uses the quoted-string form of the argument syntax. |
| Q33 | rfc9111.txt | S486 | 1334 | 18 | If a qualified private response directive is present, with an argument that lists one or more field names |
| Q34 | rfc9111.txt | S486 | 1344 | 10 | This directive uses the quoted-string form of the argument syntax. |
| Q35 | rfc9111.txt | S486 | 1411 | 7 | A cache MUST ignore unrecognized cache directives. |
| Q36 | rfc9110.txt | S487 | 1591 | 10 | A field value does not include leading or trailing whitespace. |
| Q37 | rfc9110.txt | S487 | 1593 | 14 | a field parsing implementation MUST exclude such whitespace prior to evaluating the field value. |
| Q38 | rfc9110.txt | S487 | 1695 | 13 | A recipient MUST parse and ignore a reasonable number of empty list elements |
| Q39 | rfc9110.txt | S487 | 1702 | 13 | #element => [ element ] *( OWS "," OWS [ element ] ) |
| Q40 | rfc9110.txt | S487 | 1730 | 12 | Tokens are short textual identifiers that do not include whitespace or delimiters. |
| Q41 | rfc9110.txt | S487 | 1733 | 3 | token = 1*tchar |
| Q42 | rfc9110.txt | S487 | 1783 | 17 | A string of text is parsed as a single value if it is quoted using double-quote marks. |
| Q43 | rfc9110.txt | S487 | 1786 | 9 | quoted-string = DQUOTE *( qdtext / quoted-pair ) DQUOTE |
| Q44 | rfc9110.txt | S487 | 1794 | 12 | quoted-pair = "\" ( HTAB / SP / VCHAR / obs-text ) |

## What this entry cites

- **S484** — RFC 9111 §3.1, §3.2 and §4.3.4; the retained body
  `.ufo/waves/round-99/sources/rfc9111.txt` (sha256 aeb52adb…, 84 477 bytes,
  1 956 lines) is the text Q1-Q26 are quoted from, located by plain-text line
  number.
- **S485** — the RFC Editor errata record for RFC 9111; the retained body
  `.ufo/waves/round-99/sources/eid9185.html` (sha256 83c3b795…) carries EID
  9185.
- **S486** — RFC 9111 §5.2 with §5.2.2.4, §5.2.2.7 and §5.2.3, and the
  §3.1 proxy-specific-fields sentence (lines 358-360); the same retained body,
  Q27-Q35 and, with S484, Q23, located by plain-text line number.
- **S487** — RFC 9110 §5.5, §5.6.1.2, §5.6.2 and §5.6.4; the retained body
  `.ufo/waves/round-100/sources/rfc9110.txt` (sha256 21c1cdce…, 502 941 bytes,
  10 785 lines), Q36-Q44, located by plain-text line number.

## Erratum EID 9185 on the §4.3.4 initial-set paragraph

The errata record for RFC 9111 carries EID 9185, status **Reported** (not
Verified), type Technical, raised on 2026-09-24 against the §4.3.4
initial-set paragraph. Its status is Reported: the working group has not
accepted it, so the published RFC text stands as written.

What the erratum proposes: it would replace the initial-set paragraph — the
one this entry quotes as Q1 — with a list of explicit conditions. The record's
own proposed text opens:

> The initial set consists of stored responses that satisfy all of the following conditions

and, on what the change is for, the reporter's Notes say:

> The key technical change is to allow the initial set to include stored responses whose requests have nonmatching selecting request header fields

The proposed conditions are a matching target URI, a method that permits the
stored response's use, and either a match of the selecting request header
fields under §4.1 or a strong-ETag match between the stored response and the
304. The erratum would also append a paragraph requiring that, when a response
is identified for update through a strong entity-tag match despite a
selecting-header mismatch, the cache associate the updated response with the
header fields of the request that elicited the 304:

> the cache MUST, for the purposes of Section 4.1, associate the updated response with the header fields of the request that elicited the 304 response

The record states that recasting the affected paragraph is editorial (the
Notes section of the record):

> The choice to recast the affected paragraph as a list of criteria rather than a list of exceptions to the Section 4 requirements is editorial

The technical change is the one quoted above. These quotations come from the
retained errata page, not from the RFC body, and their substring check is
recorded in `erratum-wording-check.txt` beside `quotes-check.txt`.

Why the contract does not depend on it: the contract takes the initial set as
**supplied by the caller** and never computes it. It does not evaluate §4
reuse conditions, cache keys or Vary, so the width of the initial set is
outside the contract entirely, and neither the proposed conditions nor the
proposed association rule changes the three first-match rules, the §3.2
update rule, or any of the four exceptions. An erratum that changed one of
those would matter to this decision; this one does not. If the erratum is ever
Verified, the clause it touches is one this contract does not implement.

## What this entry does not decide

- It does not compute the initial set. The contract supplies it; §4 reuse
  conditions, cache keys, `Vary` matching and the §4.1 selection profile are
  outside this decision.
- It does not decide the strong-comparison and weak-comparison functions
  themselves, or parse HTTP dates. The contract fixes which comparison each
  rule uses and that Last-Modified is compared after trimming.
- It does not model §3.2's "fields the stored response depends upon"
  exception, its "automatically processed and removed" exception, or the
  MAY-omit allowance; LC5 records that.
- It does not handle HEAD freshening (§4.3.5), invalidation (§4.4), §3.4
  partial-content combination, trailer fields, storing the 304 itself, or
  recalculating `Age` or `Date`.
- It does not decide the qualified `no-cache` and `private` cases themselves:
  contract v2 refuses them as outside the contract, in either argument form
  and in any case, and that refusal is the decision it states above.
- It does not decide the seven findings listed as still open above, and it
  names no measurement of any candidate.
- It claims no behaviour of any live cache, CDN, proxy or browser. The
  decisions `update`, `must-not-update` and `no-update` are what a reading of
  RFC 9111 §4.3.4 and §3.2 gives for the supplied values, not observations of
  what a deployed cache did.
