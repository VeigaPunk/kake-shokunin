VERDICT: C2 contract v1 is faithful to RFC 9110 §13.1.1–§13.1.4 and §13.2.2 on comparison and precedence for the origin role, but not self-describing against the RFC it cites: 18 ambiguities (9 material, 7 minor or disclosure, 2 informational) found by reading the contract against the retained RFC text; 2 material refusal divergences from normative RFC text (RFC 9110 §5.6.1.2 requires recipients to accept empty list elements, which clause 4 refuses; RFC 9110 §8.8.3 etagc admits obs-text, which clause 3 refuses); and the RFC 9110 §13.2 CONNECT/OPTIONS/TRACE method filter is absent from the contract entirely.

# Round 93 — ScoutContract: per-surface reconnaissance of the frozen C2 contract

Seat `ScoutContract` (scout, report-only). Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`
("LANE"). Freeze `bb8012fee38c0e497cdaf36337072737bca0b3cd`; base
`10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5`. Date 2026-11-04.

**Scope of this seat.** Reconnaissance of `.ufo/waves/round-93/c2-contract.md` (v1, frozen)
against the retained RFC text, per the round's item: (1) quote the RFC sentences the
contract's clauses 7–12 rest on and judge each clause's fidelity; (2) name every
underspecification as a concrete input object on which two reasonable readings decide
differently; (3) check refusal clauses 1–4 for a reading that would refuse a legal RFC
field value. **I edited nothing.** No frozen instrument, case, predicate, label or target
was touched. Machine-readable companion: `ambiguities.json` beside this file.

## What I read, and how

Read in the order the round prescribes: `round-93/freeze.md`, `round-93/c1-predicate.md`,
`round-93/c2-contract.md`, `corpus/lessons/round-92.md`,
`corpus/lessons/round-92-verifier-spotcheck.md`, `SCORECARD.md` §"Planned — after round 92",
`corpus/QUALITY.md`, `PROVINCE.md` tail. Then the two RFC bodies the round retained.

Sources verified by digest (receipt `receipts/src-digests.txt`):

```
$ sha256sum .ufo/waves/round-93/L1/src/rfc9110.txt .ufo/waves/round-93/L1/src/rfc9111.txt
21c1cdce6ab0e5509b04d84a28000836c7a087cf786efe6f04877ebfff47232a  rfc9110.txt   (502941 B)
aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e  rfc9111.txt   ( 84477 B)
```

Both match the digests `freeze.md` §Sources declares (`21c1cdce…`, `aeb52adb…`), so every
line number below is a line number in the bytes the round froze. No network fetch was made;
the retained copies are byte-identical to what the freeze records.

To pin behaviour I imported the frozen counter **read-only** and called its `reference()`
function directly (no subject was scored, no LANE file was written by it). Scripts and full
outputs are in `receipts/probe{,2,3,4,5}.{py,out}`; all five exited 0. Scratch root
`/fast/scratch/hyaku/kake-r93/ScoutContract/` was removed after the receipts were copied in.

---

## Part 1 — clause-by-clause fidelity, clauses 7–12

### Clause 7 — cache role

**RFC text relied on.** RFC 9111 §4.3.2 (`rfc9111.txt:887-892`):

> "In summary, the If-Match and If-Unmodified-Since conditional header fields are not
> applicable to a cache, and If-None-Match takes precedence over If-Modified-Since."

The contract's Grounding paragraph (contract lines 19–20) quotes exactly this. The contract
also relies on `rfc9111.txt:881-885`:

> "A cache MUST NOT evaluate conditional header fields that only apply to an origin server,
> occur in a request with semantics that cannot be satisfied with a cached response, or occur
> in a request with a target resource for which it has no stored responses; such preconditions
> are likely intended for some other (inbound) server."

and on `rfc9111.txt:875-879`:

> "If a cache receives a request that can be satisfied by reusing a stored 200 (OK) or 206
> (Partial Content) response, as per Section 4, the cache SHOULD evaluate any applicable
> conditional header field preconditions received in that request with respect to the
> corresponding validators contained within the stored response."

**Verdict: more narrowly than the text, and the narrowness is undisclosed.** The summary
sentence the contract quotes is faithfully reproduced, but it is a *summary*, and the three
normative conditions in the same section are what actually govern a cache. The contract's
clause 7 states only "if_match and if_unmodified_since are not evaluated (skipped);
evaluation starts at step 10" — it encodes the summary, and silently drops:

- the *semantics-that-a-cache-cannot-satisfy* condition (`rfc9111.txt:882-883`). A cache that
  cannot serve a POST from a stored response MUST NOT evaluate that request's preconditions at
  all; the contract evaluates them. Probe `A1`: `{"method":"POST","role":"cache",
  "if_none_match":"\"1\""}` → the contract/reference answers **412**, where the RFC text says
  the cache must not evaluate and therefore cannot produce that 412.
- the *no-stored-responses* condition (`rfc9111.txt:883-884`). The contract's `current.exists`
  is not tied to "the cache holds a stored response", so a cache-role request with
  `exists:false` still runs clauses 10–11.
- the *evaluate-against-the-stored-response* qualifier (`rfc9111.txt:877-879`). The contract
  compares against a single `current` object with no statement of which store it denotes for
  `role:"cache"` — the origin's current representation or the cache's stored response. Probe
  `A3` shows this changes the answer: for `{"role":"cache","if_none_match":"*",
  "current":{"exists":true,...}}` the contract returns 304, but under the stored-response
  reading `exists` means "the cache holds a stored response", a different predicate that can
  be true while the origin has none.

The RFC also allows a cache to *keep* evaluating If-Match: RFC 9110 §13.1.1
(`rfc9110.txt:5864-5865`) — "A cache or intermediary MAY ignore If-Match because its
interoperability features are only necessary for an origin server" — a MAY, not a MUST, and
not the same as "not applicable to a cache". The contract's skip is therefore a legitimate
reading of the summary it cites, but a reader cannot tell that the RFC's normative text is
narrower and more conditional.

### Clause 8 — If-Match

**RFC text relied on.** `rfc9110.txt:6236-6243` (§13.2.2 step 1):

> "When recipient is the origin server and If-Match is present, evaluate the If-Match
> precondition: * if true, continue to step 3 * if false, respond 412 (Precondition Failed)
> unless it can be determined that the state-changing request has already succeeded (see
> Section 13.1.1)"

and `rfc9110.txt:5794-5797` (§13.1.1):

> "An origin server MUST use the strong comparison function when comparing entity tags for
> If-Match (Section 8.8.3.2), since the client intends this precondition to prevent the
> method from being applied if there have been any changes to the representation data."

**Verdict: faithful on comparison and on the true/false test; narrower than the text on the
consequence, and the narrowing is undisclosed.** Clause 8 implements "true when `*` and
`exists`, or when any listed tag strong-matches `current.etag`" and strong comparison via
clause 5, which matches §13.1.1's evaluation list (`rfc9110.txt:5820-5829`) and §8.8.3.2's
definition (`rfc9110.txt:3648-3649`: "two entity tags are equivalent if both are not weak and
their opaque-tags match character-by-character"). Two narrowings:

1. The RFC's step 1 ends "**unless it can be determined that the state-changing request has
   already succeeded**", and §13.1.1 (`rfc9110.txt:5831-5841`) and §13.1.4
   (`rfc9110.txt:6077-6087`) permit a 2xx instead of 412 in that case. The contract's clause 8
   returns 412 unconditionally and the contract's input model has no "already succeeded"
   signal, so the RFC's alternative outcome is unreachable. The contract's Scope section says
   it decides "which status a recipient would answer" — but it never discloses that a status
   the RFC permits here is not representable. (`A5`)
2. The RFC's step-1 scope is "When recipient is the origin server". The contract reproduces
   this as "(origin role, present)". That is faithful.

Clause 8 also inherits two of the refusal-clause findings below: a malformed `if_match` is a
refusal rather than an evaluation, and the RFC 9110 §13.1.1 note (`rfc9110.txt:5867-5870`)
that a list value mixing `*` with other values "is syntactically invalid (therefore not
allowed to be generated)" is treated by the contract as a hard refusal.

### Clause 9 — If-Unmodified-Since

**RFC text relied on.** `rfc9110.txt:6245-6253` (§13.2.2 step 2):

> "When recipient is the origin server, If-Match is not present, and If-Unmodified-Since is
> present, evaluate the If-Unmodified-Since precondition: * if true, continue to step 3 * if
> false, respond 412 (Precondition Failed) unless it can be determined that the state-changing
> request has already succeeded (see Section 13.1.4)"

plus §13.1.4 (`rfc9110.txt:6037-6041`, `6043-6045`, `6047-6048`, `6069-6075`):

> "A recipient MUST ignore If-Unmodified-Since if the request contains an If-Match header
> field …" / "… if the received field value is not a valid HTTP-date (including when the field
> value appears to be a list of dates)." / "… if the resource does not have a modification
> date available." / "1. If the selected representation's last modification date is earlier
> than or equal to the date provided in the field value, the condition is true. 2. Otherwise,
> the condition is false."

**Verdict: faithful, with the same undisclosed consequence-narrowing as clause 8, plus one
role gap.** Clause 9's "ignored when `current.last_modified` is `null`" matches
`rfc9110.txt:6047-6048`; its "`current.last_modified <= value`" matches
`rfc9110.txt:6071-6073`; its "(origin role, `if_match` absent, present)" gate matches both
§13.2.2 step 2 and §13.1.4's first MUST-ignore. But:

- the RFC's `MUST ignore … if the received field value is not a valid HTTP-date (including when
  the field value appears to be a list of dates)` (`rfc9110.txt:6043-6045`) is not modelled: the
  contract's clause 1 refuses a non-integer date instead of ignoring the field. This is a real
  behavioural difference for a legal-but-unusual input — a *list* of dates in
  If-Unmodified-Since is exactly what §13.1.4 names — though the contract's epoch-integer
  adapter makes it a type error rather than a parse.
- the same 412-vs-2xx narrowing as clause 8 applies (`rfc9110.txt:6251-6253`).
- the role gap: the contract's clause 11 (not 9) is the one that ignores IMS in cache role,
  and RFC 9111 §4.3.2's Date fallback (`rfc9111.txt:904-907`) has no representation (`A2`).

### Clause 10 — If-None-Match

**RFC text relied on.** `rfc9110.txt:6255-6262` (§13.2.2 step 3):

> "When If-None-Match is present, evaluate the If-None-Match precondition: * if true, continue
> to step 5 * if false for GET/HEAD, respond 304 (Not Modified) * if false for other methods,
> respond 412 (Precondition Failed)"

and §13.1.2 (`rfc9110.txt:5880-5883`, `5917-5926`, `5928-5932`):

> "A recipient MUST use the weak comparison function when comparing entity tags for
> If-None-Match (Section 8.8.3.2) …" / "1. If the field value is '*', the condition is false if
> the origin server has a current representation for the target resource. 2. If the field value
> is a list of entity tags, the condition is false if one of the listed tags matches the entity
> tag of the selected representation. 3. Otherwise, the condition is true." / "An origin server
> that evaluates an If-None-Match condition MUST NOT perform the requested method if the
> condition evaluates to false; instead, the origin server MUST respond with either a) the 304
> (Not Modified) status code if the request method is GET or HEAD or b) the 412 (Precondition
> Failed) status code for all other request methods."

**Verdict: faithful for the origin role; the cache role is where it goes wrong.** Clause 10's
"false when the value is `*` and `exists`, or when any listed tag weak-matches
`current.etag`" matches §13.1.2's three-case list, and its "304 when the method is GET or
HEAD, else 412" matches §13.2.2 step 3 and §13.1.2's MUST exactly. Two defects:

- **The `*` case is stated origin-relative but applied cache-relative.** §13.1.2 line 5919-5920
  says "*" is false "if **the origin server** has a current representation for the target
  resource". The contract's clause 10 says "false when the value is `*` and `exists`", with
  `exists` unqualified by role. Under RFC 9111 §4.3.2 (`rfc9111.txt:894-897`) an If-None-Match
  in a cache "indicates that the client wants to validate one or more of its own stored
  responses in comparison to the stored response chosen by the cache", so `exists` should mean
  "the cache holds a stored response" — a different predicate. Probe `A3` shows the two
  readings answer differently for the same input.
- **Clause 10 runs for `role:"cache"` on methods a cache cannot serve.** See clause 7 /
  `A1`: RFC 9111 §4.3.2 line 881-885 makes that a MUST NOT.

### Clause 11 — If-Modified-Since

**RFC text relied on.** `rfc9110.txt:6264-6270` (§13.2.2 step 4):

> "When the method is GET or HEAD, If-None-Match is not present, and If-Modified-Since is
> present, evaluate the If-Modified-Since precondition: * if true, continue to step 5 * if
> false, respond 304 (Not Modified)"

and §13.1.3 (`rfc9110.txt:5956-5961`, `5963-5966`, `5968-5969`, `6006-6010`):

> "A recipient MUST ignore If-Modified-Since if the request contains an If-None-Match header
> field …" / "… if the received field value is not a valid HTTP-date, the field value has more
> than one member, or if the request method is neither GET nor HEAD." / "… if the resource does
> not have a modification date available." / "1. If the selected representation's last
> modification date is earlier or equal to the date provided in the field value, the condition
> is false. 2. Otherwise, the condition is true."

**Verdict: faithful, and this is the contract's strongest clause.** Every element of clause 11
maps onto cited text: the GET/HEAD gate (`rfc9110.txt:5965-5966`), the If-None-Match-absent
gate (`rfc9110.txt:5956-5957` and `rfc9110.txt:6264`), the null-last-modified ignore
(`rfc9110.txt:5968-5969`), and the `last_modified <= value` test (`rfc9110.txt:6008-6010`).
Probe `A18` confirms the non-GET/HEAD case matches the RFC's own "ignore" language. The only
gap is the cache-role Date fallback (`A2`, RFC 9111 `rfc9111.txt:904-907`), which the
contract's input model cannot express.

### Clause 12 — otherwise

**RFC text relied on.** `rfc9110.txt:6280-6283` (§13.2.2 step 6):

> "Otherwise, * perform the requested method and respond according to its success or failure."

**Verdict: more broadly than the text.** The contract's clause 12 returns
`{"decision": "200", "precondition": null}` unconditionally. The RFC's step 6 lets the
method's own outcome decide, and the RFC's step 5 (If-Range → 206, `rfc9110.txt:6272-6278`) is
not modelled at all. So the contract's "200" means "no precondition blocked", not "the
response was 200" — a reading a consumer of the instrument can easily get wrong, and the
contract's Scope section does not say so. This is defect **D5**.

### Summary table

| Clause | RFC ground | Verdict | Headline issue |
|---|---|---|---|
| 7 cache role | 9111 §4.3.2 `:887-892` (quoted), `:881-885`, `:875-879` | **more narrowly than the text**, undisclosed | RFC 9111's three normative cache conditions are dropped; `current` is not tied to a store (`A1`, `A3`) |
| 8 If-Match | 9110 §13.2.2 `:6236-6243`, §13.1.1 `:5794-5797` | faithful on comparison; **narrower** on consequence | RFC's "unless already succeeded" 2xx is unreachable, undisclosed (`A5`) |
| 9 If-Unmodified-Since | 9110 §13.2.2 `:6245-6253`, §13.1.4 `:6037-6075` | faithful; **narrower** on consequence | same 2xx gap; RFC's "MUST ignore invalid/list date" not modelled |
| 10 If-None-Match | 9110 §13.2.2 `:6255-6262`, §13.1.2 `:5880-5932` | faithful for origin role; **cache role diverges** | `*` is origin-relative in the RFC, unqualified in the contract (`A3`); cache evaluates unservable methods (`A1`) |
| 11 If-Modified-Since | 9110 §13.2.2 `:6264-6270`, §13.1.3 `:5956-6010` | **faithful** | only the RFC 9111 Date fallback is unrepresentable (`A2`) |
| 12 otherwise | 9110 §13.2.2 `:6280-6283` | **more broadly than the text** | RFC lets the method's outcome decide; contract fixes 200, and omits step 5's If-Range/206 (D5) |

### The gap the whole contract shares: RFC 9110 §13.2's method filter

`rfc9110.txt:6198-6207`:

> "A server that is not the origin server for the target resource and cannot act as a cache
> for requests on the target resource MUST NOT evaluate the conditional request header fields
> defined by this specification, and it MUST forward them if the request is forwarded … Likewise,
> a server MUST ignore the conditional request header fields defined by this specification when
> received with a request method that does not involve the selection or modification of a
> selected representation, such as CONNECT, OPTIONS, or TRACE."

The contract's Grounding paragraph cites §13.2.2 but never §13.2, and no clause encodes a
method filter. Probe `A6`: `{"method":"OPTIONS","if_none_match":"\"1\""}` → contract/reference
answer **412**, while RFC 9110 §13.2 says the fields MUST be ignored. This is inside the
scored population: **22 of the counter's 120 generated inputs use OPTIONS, and 13 of those
land on a 412** (receipt `receipts/probe2.out`, `receipts/probe4.out`), so a candidate
implementing the RFC's filter would disagree with the reference on 13 scored cases. No hand
case covers CONNECT, OPTIONS or TRACE at all.

Related, and also unmodelled: RFC 9110 §13.2.1 `rfc9110.txt:6190-6193` — "A server MUST ignore
all received preconditions if its response to the same request without those conditions,
prior to processing the request content, would have been a status code other than a 2xx
(Successful) or 412 (Precondition Failed)." The contract's `current.exists` is the nearest
proxy but is not that rule.

---

## Part 2 — underspecifications

Full machine-readable list: `ambiguities.json` (18 entries, with the concrete input object,
both readings, the silent clause, the reference's decision, and the RFC anchors). Summary:

**Material (9).** `A1` cache role + POST: MUST NOT evaluate vs. evaluate → 412 vs. no 412.
`A2` cache role + IMS with no Last-Modified: RFC 9111 Date fallback vs. ignore → the RFC's
fallback has no representation. `A3` cache role + If-None-Match `*`: `exists` = stored
response vs. origin's current representation → 304 vs. something else. `A6` the absent
CONNECT/OPTIONS/TRACE method filter → 412 vs. ignore. `A7` empty list member: RFC 9110
§5.6.1.2 "a recipient MUST accept" vs. clause 4's refusal. `A8` trailing comma: same, RFC
example "foo ,bar," at `rfc9110.txt:1718`. `A9` whitespace-only value: RFC 9110 §5.5's
mandatory whitespace exclusion then empty list vs. clause 4's refusal. `A11` obs-text in an
entity-tag: RFC 9110 §8.8.3 `etagc = %x21 / %x23-7E / obs-text` vs. clause 3's ASCII-only set.
`A14` whether clause 3's "a malformed entity-tag is a refusal" reaches `current.etag` or only
the request's precondition values.

**Minor or disclosure (7).** `A4` If-Match skip in cache role (RFC 9110's MAY vs. the contract's MUST-like
skip). `A5` (disclosure) the undisclosed 2xx narrowing. `A10` OWS around the whole field value. `A12` the
`>= 0` epoch bound excluding pre-1970 legal dates (RFC 9110 §5.6.7 `rfc9110.txt:1844`,
`:1873-1880`). `A13` case-sensitivity of the GET/HEAD test (the *tchar set itself* in clause 1
matches RFC 9110 §5.6.2 `:1735-1737` exactly — I checked — but the consequence for clauses
10–11 is not stated). `A15` the `precondition` label when a precondition was evaluated but did
not decide the outcome. `A16` `role: null` refused vs. defaulted.

**Informational (2).** `A17` the If-None-Match `*` case — the two readings *agree* on that
input; retained only because `A3`'s variant does not. `A18` IMS for a non-GET/HEAD method —
the RFC's own term is "ignore" and the contract matches; recorded so it is not re-derived.

### Population coverage of these classes

The counter's own population cannot discriminate most of these readings. Measured
(`receipts/probe2.out`): of the 120 generated inputs, **0** use an empty list member, **0** a
whitespace-only or empty value, **0** a whitespace-padded `*`, **0** a non-ASCII tag, **0** a
negative date, **0** a `role: null`; **13** use OPTIONS and none use CONNECT or TRACE; **40**
carry an explicit role. The 44 hand cases cover none of these classes except by refusing them
(`refuse/empty-member`, `refuse/empty-value`, `refuse/negative-date`, `refuse/role-unknown`).
The population gaps are enumerated in `ambiguities.json` →
`population_coverage_gaps_observed`.

---

## Part 3 — do refusal clauses 1–4 refuse a legal RFC field value?

Three findings, all in clause 3/4, all confirmed against the frozen reference (probes `A7`,
`A8`, `A9`, `A11`).

**(a) An entity-tag list with an empty member — legal, refused.** RFC 9110 §5.6.1.2
`rfc9110.txt:1693-1702`:

> "Empty elements do not contribute to the count of elements present. A recipient MUST parse
> and ignore a reasonable number of empty list elements: enough to handle common mistakes by
> senders that merge values, but not so much that they could be used as a denial-of-service
> mechanism. In other words, a recipient MUST accept lists that satisfy the following syntax:
> `#element => [ element ] *( OWS \",\" OWS [ element ] )`"

and its own worked examples at `rfc9110.txt:1717-1719`:

> "foo ,bar," / "foo , ,bar,charlie"

are valid *recipient-side* values. `If-None-Match: "a",, "b"` is exactly the "senders that
merge values" case §5.6.1.2 names. Contract clause 4 refuses it ("An empty member is a
refusal"); the reference refuses it (`REFUSED: empty list member`). **A recipient that
refuses it violates a MUST.** Note the contract's rule tracks §5.6.1.1's *sender* rule
(`rfc9110.txt:1676-1677`: "a sender MUST NOT generate empty list elements") while the
contract models a *recipient*. The trailing-comma form `"a",` is the same defect (`A8`).

**(b) A whitespace-only field value — legal after §5.5's mandatory exclusion, refused.**
RFC 9110 §5.5 `rfc9110.txt:1591-1594`:

> "A field value does not include leading or trailing whitespace. When a specific version of
> HTTP allows such whitespace to appear in a message, a field parsing implementation MUST
> exclude such whitespace prior to evaluating the field value."

After that exclusion the value is empty, which under §5.6.1.2 is a zero-member list, and
under §13.1.2 line 5926 ("Otherwise, the condition is true") an If-None-Match with an empty
list evaluates **true** → 200 / `precondition: null`. The contract refuses it (clause 4: "A
value that is the empty string or only whitespace is a refusal"; reference:
`REFUSED: empty precondition field value`).

**(c) An entity-tag containing obs-text — legal, refused.** RFC 9110 §8.8.3
`rfc9110.txt:3582-3588`:

> "entity-tag = [ weak ] opaque-tag / opaque-tag = DQUOTE *etagc DQUOTE /
> etagc = %x21 / %x23-7E / obs-text ; VCHAR except double quotes, plus obs-text"

(collected ABNF `rfc9110.txt:9873-9874` identical), with `obs-text = %x80-FF`
(`rfc9110.txt:1589`) and §5.5 `rfc9110.txt:1603-1604`: "A recipient SHOULD treat other
allowed octets in field content (i.e., obs-text) as opaque data." Contract clause 3 states
etagc as "any character in `!` or `#`–`~` (0x23–0x7E)" — no obs-text alternative — so
`"a\u0080b"` is refused as a malformed entity-tag (reference confirms). The contract also
says the opaque-tag is "the bytes between the quotes, compared byte-for-byte", which is a
byte-level comparison in a Unicode transport; that phrase is unreconciled with the §5.5
obs-text rule it omits.

**Checked and NOT defects** (stated so a later reviewer does not re-derive them):

- *A legal but unusual method token.* Clause 1's tchar set — `!` `#` `$` `%` `&` `'` `*` `+`
  `-` `.` `^` `_` `` ` `` `|` `~`, DIGIT, ALPHA — is **exactly** RFC 9110 §5.6.2
  `rfc9110.txt:1735-1737` (and the collected ABNF `:9960-9961`). No legal token is refused.
  What is unstated is the *consequence*: RFC 9110 §9.1 `:3748-3749` ("The method token is
  case-sensitive") means `get` is a different method, so a lowercase `get` with a matching
  If-None-Match yields 412, not 304. The contract's reference does that, but clause 1 says
  only that the *token* is "compared case-sensitively" (`A13`).
- *`*` mixed with other members.* RFC 9110 §13.1.1 note `rfc9110.txt:5867-5870` calls this
  "syntactically invalid (therefore not allowed to be generated)". The contract refuses it;
  refusing a value the RFC declares invalid is defensible, though the RFC frames the
  obligation on the sender, not the recipient.
- *`*` with OWS around it.* Probe `A10`: the reference strips SP/HTAB from the whole value
  before testing for `*`, matching RFC 9110 §5.5's exclusion rule. The contract's text does
  not say so, which is a documentation gap rather than a behaviour defect.
- *Pre-1970 dates.* `>= 0` excludes legal IMF-fixdate values (`A12`) — a narrowing the
  contract states but does not attribute to §5.6.7.

---

## Defects found in the round's own instruments

Reported as FINDINGS, not repaired (frozen instruments).

**D1 — `.ufo/waves/round-93/c93_conditional.py:6`.** The module docstring says "(30 hand
cases + a seeded generated population decided by this file's own reference …)". `hand_cases()`
returns **44** (measured, `receipts/probe2.out`: `hand_cases() length = 44`). The freeze and
`controls/base-c2.txt` both say 44 (`hand=0/44`), so the docstring is the sole outlier.

**D2 — same file, line 214.** `hand_cases()`'s own docstring repeats "30 worked cases" against
an actual 44.

**D3 — same file, `generate()`.** The seeded population's method set is
`GET/HEAD/PUT/POST/DELETE/PATCH/OPTIONS` — it includes OPTIONS but never CONNECT or TRACE —
and it never generates an empty list member, a whitespace-only or empty value, a
whitespace-padded `*`, a non-ASCII tag, a negative date, or `role:null` (all measured 0 in
`receipts/probe2.out`). The 120-case population therefore cannot discriminate the readings in
Part 2; only the 44 hand cases can, and they reach none of these classes except by refusing
them. This is the R92-4 lesson recurring in a new shape: round 92's C2 counter carried 28
hand cases over a 120-case seeded population (`.ufo/waves/round-92/freeze.md` line 45) and
round 93's carries 44 over 120 — the hand-case count grew, but the *classes* the generated
population can reach did not grow at all (the six classes listed above are all at 0 in both
rounds' generators for the same structural reason: the generator draws from a fixed set of
well-formed tags, `*` and comma-joined tag lists, and non-negative integers).

**D4 — `.ufo/waves/round-93/c2-contract.md`, Grounding paragraph (lines 15–20).** The
paragraph names RFC 9110 §13.2.2, §13.1.1–§13.1.4 and §8.8.3.2 plus RFC 9111 §4.3.2. The
contract's own decisions also depend on RFC 9110 §13.2 (`:6198-6207`, the CONNECT/OPTIONS/
TRACE MUST-ignore), §13.2.1 (`:6190-6193`), §5.5 (`:1591-1594`, whitespace exclusion),
§5.6.1.2 (`:1693-1702`, recipient MUST accept empty list elements), §8.8.3 (`:3587`, obs-text
etagc) and §5.6.7 (`:1844`, the date range) — none cited, none acknowledged as departures.
Because the freeze cannot be edited, a contract v2 must carry these as explicit, cited
narrowings so a reader can tell deliberate scope from oversight.

**D5 — same file, clause 12 (line 91).** `{"decision": "200", "precondition": null}` is
unconditional. RFC 9110 §13.2.2 step 6 (`:6280-6283`) lets the method's own success or
failure decide, and step 5 (`:6272-6278`, If-Range → 206) is not modelled. The contract's
"200" therefore means "no precondition blocked", which the contract never says.

**Minor / scope notes.** RFC 9110 §13.1.1 `:5867-5870` and §13.1.2 `:5937-5940` both note that
a list value mixing `*` with other values is "syntactically invalid" — the contract treats
that as a refusal, which is stricter than the cited text requires of a recipient. RFC 9110
§13.1.1 `:5831-5841` and §13.1.4 `:6077-6087` allow a 2xx instead of 412 when the
state-changing request appears already applied; the contract's fixed 412 forecloses a
permitted outcome without saying so (`A5`).

**Routed round-92 defects, status.** R92-4 (one case per clause and refusal class) and
R92-5 (the counter's reference checked against the contract by an independent reader before
the freeze) are the two this round's C2 instrument directly answers. On the evidence here:
the population grew but its *class reach* did not (D3), and the reference was checked against
the contract — but the reference and the contract agree with each other while both diverge
from RFC text the contract does not cite (D4), so the check confirmed internal consistency
rather than fidelity to the RFC. R92-4 is therefore **partially** answered: 44 cases over 12
clauses, but nine of the ambiguities above sit in classes the population never reaches.

---

## Limits of this report

- I judged the contract against the RFC text only. I did not evaluate whether the RFC text
  is the right ground for the lane's purpose, nor whether `conditional_eval.py` (the
  candidate) exists at the base — that is the counter's job, not this seat's.
- The "reference decides" column throughout is `c93_conditional.py::reference()` called
  read-only. I did not score any subject, did not run the counter's `--selftest`, and did not
  reproduce `controls/base-c2.txt`; the base reading is the freeze's, quoted here.
- My probes import the frozen counter from its committed path. That is a read of frozen
  bytes, not an edit; `git status` on the lane shows no change from this seat. The RFC line
  numbers are line numbers in the round's retained copies (digests verified above), not in a
  fresh fetch — a fresh fetch was not authorised for this seat.
- Where I wrote "the RFC permits X but the contract does not", I mean the *normative* text.
  Several of these (§13.2's method filter, §5.6.1.2's recipient acceptance) are obligations
  on a recipient in a deployed server. This instrument decides a precondition question over
  supplied values and is explicitly not a server, so a divergence from a recipient's
  obligation is not automatically a defect in the instrument — it is an undisclosed narrowing
  in the contract, which is what I have reported it as. A contract v2 should say which
  divergences are deliberate scope and which are corrections.
- **No tool was installed or upgraded** for this seat, so there is nothing to record under the
  tooling authorisation. Everything used was already present: `python3` (stdlib only), `sha256sum`,
  `wc`, `grep`, `awk`.

## Files written by this seat

All under `LANE/.ufo/waves/round-93/w1/ScoutContract/` (my own directory; nothing else in
LANE, nothing in the fleet root, no sibling lane, no git or jj command anywhere):

- `ScoutContract.md` — this report.
- `ambiguities.json` — machine-readable: 18 ambiguities with input objects, both readings,
  the silent clause, the reference's decision and RFC anchors; 9 population coverage gaps;
  5 instrument/contract defects; source digests and reading notes.
- `receipts/probe{,2,3,4,5}.{py,out}` — the read-only probes and their full outputs
  (exit 0 each).
- `receipts/src-digests.txt` — the sha256/wc receipt for both RFC bodies.

Scratch `/fast/scratch/hyaku/kake-r93/ScoutContract/` was deleted after the receipts were
copied in, per the round's scratch rule.

**Report path:** `.ufo/waves/round-93/w1/ScoutContract.md`
