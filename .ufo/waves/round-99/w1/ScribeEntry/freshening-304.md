source: S484, S485 — RFC 9111 (June 2022) §4.3.4 "Freshening Stored Responses upon Validation", §3.2 "Updating Stored Header Fields" and the §3.1 "Storing Header and Trailer Fields" exceptions §3.2 points at, retained at `.ufo/waves/round-99/sources/rfc9111.txt` (sha256 aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e, 84 477 bytes, 1 956 lines); RFC Editor erratum EID 9185 (Reported, Technical, on the §4.3.4 initial-set paragraph), retained at `.ufo/waves/round-99/sources/eid9185.html` (sha256 83c3b795290e09842d1af973f73b52c98fd661bf77cafc17658eb5ac4df63dd3)
verified-at: 2026-11-05
recheck: 180d (due 2027-05-04), or sooner after a change to the retained RFC body or to contract v1 of this lane
ground: freshness — round-99 C2, a bounded capability: which stored responses a 304 (Not Modified) freshens, and which of their header fields the 304 changes, decided over supplied values.
scope: one decision per 304 response over an initial set of stored responses the caller supplies, under contract v1 of this lane; not the initial-set computation itself (§4 reuse conditions, cache keys or Vary), not HEAD freshening (§4.3.5), not invalidation (§4.4), not trailer fields, not storing the 304 itself, not Age or Date recalculation, not any clock, network or live cache.

# Freshening stored responses upon a 304: which responses are updated, and which header fields change

RFC 9111 §4.3.4 is the rule that decides which stored responses a cache may
update when it receives a 304 (Not Modified), and §3.2 is the rule that decides
what the updated response's header fields look like afterwards. The two are
separate steps: §4.3.4 selects, §3.2 updates.

This entry records what the two sections say, marks which clause of the decision
is fixed by the RFC and which is a convention this lane chose, names the
contract that fixes those conventions, and states plainly what it does not
decide. Every quotation below is a whitespace-collapsed substring of the body
named for it: the RFC 9111 quotations are located by plain-text line number in
the retained RFC body, and the erratum quotations are checked against the
retained errata page.

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
contract for round 99 takes the initial set as supplied by the caller.

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

The contract that governs this round's instrument is
`.ufo/waves/round-99/fresh304-contract.md` (sha256
2be46b4d8dcc57539b0a45e2e3b7b57e76cb1c4e570891e8cdea88c5ebbba2a6). Six of its
choices are **lane conventions**: they are this lane's reading, not a
requirement of RFC 9111, and each is marked in the contract with an LC tag.

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
  convention: a 304 whose Cache-Control carries a qualified `no-cache="` or
  `private="` form is refused as outside the contract, rather than handled by
  dropping the named fields.

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
(§3.1 exception 4). Field names in the output are lowercased; values are
copied byte for byte.

## The contract and the counter

The contract names one candidate path, `scripts/freshen_304.py`, and fixes its
interface: it reads one JSON object on stdin, writes one JSON object on
stdout, exits 0, and refuses on stderr with `invalid_input: <reason>` and exit
1 without writing to stdout. The counter that scores a candidate against the
contract is `.ufo/waves/round-99/c99_fresh304.py` (sha256
d13bba5d6b663b171ab57d42b5ec054b5f73d8deb8f9fd64f14adad455b6bc4b), which
prints one line:

    candidate=<absent|present> sha256=<hex> hand=a/b generated=c/d refusals=e/f seed=S met=<bool>

This entry describes the decision the contract defines. It reports no
measurement of any candidate and makes no claim that a candidate conforms to
the contract.

## The quotes, with their locations

Every quote below is a whitespace-collapsed substring of the retained RFC body,
taken from the stated plain-text line, and at most 25 whitespace-separated
words. `quotes-check.txt` records the substring check for each of them, with
the body, the id, the line, the word count and the found/not-found result.
The quotations in the erratum section come from the retained errata page
instead, and their check is `erratum-wording-check.txt`.

| # | Body | Line | Words | Quote |
|---|---|---|---|---|
| Q1 | rfc9111.txt | 957 | 18 | The initial set of stored responses to update are those that could have been chosen for that request |
| Q2 | rfc9111.txt | 962 | 15 | Then, that initial set of stored responses is further filtered by the first match of: |
| Q3 | rfc9111.txt | 965 | 15 | If the new response contains one or more "strong validators" (see Section 8.8.1 of [HTTP]) |
| Q4 | rfc9111.txt | 967 | 19 | All the stored responses in the initial set with one of those same strong validators are identified for update. |
| Q5 | rfc9111.txt | 970 | 14 | then the cache MUST NOT use the new response to update any stored responses |
| Q6 | rfc9111.txt | 974 | 16 | If the new response contains no strong validators but does contain one or more "weak validators" |
| Q7 | rfc9111.txt | 976 | 13 | then the most recent of those matching stored responses is identified for update. |
| Q8 | rfc9111.txt | 979 | 11 | If the new response does not include any form of validator |
| Q9 | rfc9111.txt | 982 | 18 | there is only one stored response in the initial set, and that stored response also lacks a validator |
| Q10 | rfc9111.txt | 986 | 18 | the cache MUST update its header fields with the header fields provided in the 304 (Not Modified) response |
| Q11 | rfc9111.txt | 375 | 22 | the cache MUST add each header field in the provided response to the stored response, replacing field values that are already present |
| Q12 | rfc9111.txt | 377 | 4 | with the following exceptions: |
| Q13 | rfc9111.txt | 379 | 8 | Header fields excepted from storage in Section 3.1, |
| Q14 | rfc9111.txt | 381 | 9 | Header fields that the cache's stored response depends upon |
| Q15 | rfc9111.txt | 384 | 11 | Header fields that are automatically processed and removed by the recipient |
| Q16 | rfc9111.txt | 387 | 4 | The Content-Length header field. |
| Q17 | rfc9111.txt | 393 | 13 | MAY omit these header fields from updating stored responses on an exceptional basis |
| Q18 | rfc9111.txt | 412 | 15 | the Content-* prefix is not a signal that a header field is omitted from update |
| Q19 | rfc9111.txt | 340 | 17 | Caches MUST include all received response header fields -- including unrecognized ones -- when storing a response |
| Q20 | rfc9111.txt | 345 | 21 | fields whose names are listed in it are required by Section 7.6.1 of [HTTP] to be removed before forwarding the message |
| Q21 | rfc9111.txt | 350 | 12 | some fields' semantics require them to be removed before forwarding the message |
| Q22 | rfc9111.txt | 354 | 19 | The no-cache (Section 5.2.2.4) and private (Section 5.2.2.7) cache directives can have arguments that prevent storage of header fields |
| Q23 | rfc9111.txt | 358 | 20 | Header fields that are specific to the proxy that a cache uses when forwarding a request MUST NOT be stored |
| Q24 | rfc9111.txt | 361 | 21 | Effectively, this is limited to Proxy-Authenticate (Section 11.7.1 of [HTTP]), Proxy-Authentication-Info (Section 11.7.3 of [HTTP]), and Proxy-Authorization (Section 11.7.2 of [HTTP]). |
| Q25 | rfc9111.txt | 935 | 17 | A 304 (Not Modified) response status code indicates that the stored response can be updated and reused |
| Q26 | rfc9111.txt | 953 | 20 | When a cache receives a 304 (Not Modified) response, it needs to identify stored responses that are suitable for updating |

## What this entry cites

- **S484** — RFC 9111 §3.1, §3.2 and §4.3.4, opened this round; the retained
  body `.ufo/waves/round-99/sources/rfc9111.txt` (sha256 aeb52adb…, 84 477
  bytes, 1 956 lines) is the text Q1-Q26 are quoted from, located by plain-text
  line number.
- **S485** — the RFC Editor errata record for RFC 9111, opened this round; the
  retained body `.ufo/waves/round-99/sources/eid9185.html` (sha256 83c3b795…)
  carries EID 9185.

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

Why the contract does not depend on it: the round-99 contract takes the
initial set as **supplied by the caller** and never computes it. It does not
evaluate §4 reuse conditions, cache keys or Vary, so the width of the initial
set is outside the contract entirely, and neither the proposed conditions nor
the proposed association rule changes the three first-match rules, the §3.2
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
- It does not handle HEAD freshening (§4.3.5), invalidation (§4.4), trailer
  fields, storing the 304 itself, or recalculating `Age` or `Date`.
- It does not decide the qualified `no-cache="` and `private="` cases; LC6
  records that they are refused as outside the contract.
- It claims no behaviour of any live cache, CDN, proxy or browser. The
  decisions `update`, `must-not-update` and `no-update` are what a reading of
  RFC 9111 §4.3.4 and §3.2 gives for the supplied values, not observations of
  what a deployed cache did.
