source: S430, S431, S432, S433 — RFC 6797 HTTP Strict Transport Security, W3C Content Security Policy Level 3, WHATWG Fetch (`X-Content-Type-Options`), RFC 9110 HTTP Semantics; rows in `corpus/SOURCES.md`, retained bodies at `.ufo/waves/round-61/sources/S430.html`…`S433.html`
verified-at: 2026-10-27
recheck: 180d
fetches: four public GETs, 2026-10-27T09:14:55Z, HTTP 200 each, userAgent `round61`, receipts `.ufo/waves/round-61/sources/receipts.json` (sha256 S430 f086bfac…c72c0a, S431 be8f2468…e3144e, S432 63b0a018…bad911b, S433 d4317606…368fe1e5)
ground: publisher-side operability — what a recorded response header list can be checked against offline, without a browser and without a fetch at audit time
scope: the six expectation classes the round-61 audit declares (content_type_present, hsts_present, xcto_nosniff_value, csp_present, singleton_fields, field_name_syntax), each read off its specification; nothing here says any particular site serves or should serve a given field
coverage: the response field each class reads, the specification sentence that grounds it, the audit rule the class encodes, and the limits of reading a recorded header list
falsifier: a fresh fetch of a cited page whose retained body no longer contains a quoted span, or a specification revision that changes what the field conveys; the quotes below are checked against the sha256-pinned bodies, so a drifted body is detectable without judgement

# Response headers an offline audit can check, and what each check is worth

The six classes below are the expectations the round-61 audit declares. Each
class names the field it reads, quotes the specification text that gives the
field its job, states the audit rule in plain words, and then says what the
rule cannot conclude. Two conventions hold throughout: field names are matched
case-insensitively [S433 §5.1], and a value is compared after its leading and
trailing optional whitespace is trimmed [S433 §5.5]:

> "A field value does not include leading or trailing whitespace."

## content_type_present — a 2xx answer should name its media type

RFC 9110 §8.3 carries the sender-side rule in one sentence whose subject and
modal sit in their own markup nodes and whose continuation is quoted here
[S433 §8.3]:

> "generate a Content-Type header field in that message unless the intended media type of the enclosed representation is unknown to the sender"

The same sentence's opening clause describes the sender as one that generates a
message containing content [S433 §8.3; the clause is a separate node, so it is
paraphrased rather than quoted], and the sentence's modal is the RFC's SHOULD
keyword, itself a separate node. [INFERENCE] Two consequences follow for a
publisher: content that is served is content whose media type the sender is
expected to declare, and the declared exception is the sender's own ignorance
of that media type, not convenience. Because the source's modal is SHOULD, the
audit's rule is the lane's declared policy, stricter than the sentence quoted
here.

**Audit semantics.** The audit reads a recorded response whose status is 2xx
and reports `content_type_present` when the recorded header list carries no
`Content-Type` field. Non-2xx recorded responses are outside the class, and a
2xx with the field is clean whatever the field's value. [INFERENCE] A response
with no `Content-Type` is a finding under the declared policy, not a proof that
a client will guess the type wrongly: the class records absence, nothing more.

## hsts_present — an https answer should carry the HSTS policy field

RFC 6797 §7.1 gives the server-side rule, and §6.1 gives the field its meaning
[S430 §7.1, §6.1]:

> "an HSTS Host SHOULD include in its response message an STS header field"

> "indicates to a UA that it MUST enforce the HSTS Policy in regards to the host emitting the response message containing this header field"

The condition of the first sentence, stated earlier in the same §7.1 node and
in its heading, is that the request arrived over a secure transport; the second
sentence is why the field matters at all, and it is the user agent, not the
server, that must then enforce the policy. [INFERENCE] For a publisher this
reads as: an https surface that never sets the field leaves a browser free to
reach it over plain http on a later navigation, which is the downgrade the
policy exists to prevent.

**Audit semantics.** For a check declaring `https: true` and
`hsts_present: true`, the audit reports `hsts_present` when the recorded header
list carries no `Strict-Transport-Security` field. A field present with
directives is clean for this class: the audit records presence, and it does not
parse `max-age` or the subdomain directive.

## xcto_nosniff_value — where the field appears, its value is the one literal

WHATWG Fetch §3.6 gives the field its purpose in the response-processing steps;
the sentence is fragmented by inline markup — the field's name sits in the
section heading and in a code element immediately before the first span — so
the quotable pieces are short and the normative value grammar is cited by
location [S432 §3.6]:

> "can be used to require checking of a"

> "Web developers and conformance checkers must use the following"

The node after the second span introduces the ABNF value block for
`X-Content-Type-Options`; that block gives one production whose only permitted
value is the literal `nosniff`, with the comment `; case-insensitive` (S432
§3.6, retained body; the block is not quoted because it spans element
boundaries). The same section's algorithm reads the field values and compares
the first one to `nosniff` as an ASCII case-insensitive match (S432 §3.6,
paraphrased for the same reason).

**Audit semantics.** Where the recorded header list carries an
`X-Content-Type-Options` field, the audit reports `xcto_nosniff_value` when the
trimmed value is not `nosniff` under ASCII case folding. A check with no such
field is clean for this class, because the class reads a value and does not
require the field. [INFERENCE] The rule is therefore a quality rule on a
publisher's own choice, not a demand that every surface set the field.

## csp_present — the policy field a publisher declares

CSP Level 3 §3.1 names the delivery mechanism; the field name sits in the
nodes before the quoted span, and the quoted span begins after it [S431 §3.1]:

> "HTTP response header field is the preferred mechanism for delivering a policy from a server to a client"

The field is delivered in the response itself, which is what makes an offline
read of a recorded response meaningful at all [INFERENCE: the sources say only
that the header is the delivery mechanism; that a recorded response is the
right artifact to read is this lane's reading].

**Audit semantics.** For a check declaring `csp_present: true`, the audit
reports `csp_present` when the recorded header list carries no
`Content-Security-Policy` field. The audit does not parse the policy, does not
compare two policies, and does not read the report-only variant.

## singleton_fields — one field line per declared name

RFC 9110 §5.2 states the sender-side rule about repeated field lines; the
quoted span is its object clause [S433 §5.2]:

> "generate multiple field lines with the same name in a message"

§5.3's Set-Cookie note explains the one exception a publisher will meet in
practice, and the quoted clause is the reason it cannot be folded into the
general rule [S433 §5.3]:

> "Since it cannot be combined into a single field value"

RFC 6797 states the same cardinality for its own field in one sentence
[S430 §7.1]:

> "If an STS header field is included, the HSTS Host MUST include only one such header field"

**Audit semantics.** For each name listed in a check's `singleton_fields`, the
audit reports `singleton_fields` when the recorded header list carries that name
more than once (case-insensitively). One finding is emitted per offending name,
not per surplus occurrence. `Set-Cookie` can never be a singleton under this
rule, so listing it cannot produce a finding: §5.3 grounds the special case,
and treating the name as never single is the audit's declared rule.

## field_name_syntax — a field name is a token

RFC 9110 §5.6.2 defines the token, and §5.1 gives the field name its role
[S433 §5.6.2, §5.1]:

> "Tokens are short textual identifiers that do not include whitespace or delimiters."

> "A field name labels the corresponding field value as having the semantics defined by that name"

> "Field names are case-insensitive and ought to be registered within the"

That third span stops at the words it covers: the name of the field-name
registry follows it in the next node, so the span is not a whole sentence.

The §5.1 ABNF production is the shortest form of the same fact: the retained
body reads `field-name = token` (S433 §5.1, cited by location; three whitespace
units, so it is not quoted here). [INFERENCE] A recorded name carrying a space,
such as `X Bad Name`, is therefore not a field name at all: it is a fault in
whatever emitted the line, and no class above can be trusted to have read that
line as the publisher intended.

**Audit semantics.** The audit reports `field_name_syntax` for a recorded
header name that is not an RFC 9110 token, in every check, independent of the
check's declared expectations (the version-1 `expect` object carries no toggle
for this class). A finding here is about the record itself, not about a
declared policy.

## Lane use

The capture and the audit are two commands with one artifact between them.

1. `python3 -B scripts/response_snapshot.py` makes one GET per surface of the
   round-23 population and writes `.ufo/waves/round-61/capture/<id>/response.json`:
   final status, final URL, every header field-line in wire order as name/value
   pairs with duplicates preserved, the body's sha256 and byte count, the fetch
   time and the user agent tag `round61`. No cookies, credentials or request
   body; at most five redirects, 20 s and 2 MiB per surface; a committed
   capture is not overwritten in place.
2. `.ufo/waves/round-61/capture/manifest.json` (version 1) binds each check to
   one capture receipt: `id`, `source`, `url`, `https`, and the five declared
   expectations. The round-61 manifest carries one check per surface — 12,
   `jq '.checks|length' .ufo/waves/round-61/capture/manifest.json` → 12,
   2026-10-27 — and declares the singleton names `content-type`,
   `content-security-policy` and `strict-transport-security`.
3. `python3 -B scripts/header_audit.py --manifest .ufo/waves/round-61/capture/manifest.json --root .`
   reads only those files, never the network, and prints one line
   `<check-id> <class> <detail>` per finding and one summary line
   `checks=<n> findings=<k>`; exit 0 clean, 1 findings (including a check that
   could not be evaluated), 2 manifest fault, 64 usage.

**What this flow does not claim.** The capture is input preparation: it is
reported as having run with its receipts, and no claim here depends on any
surface being up. Nothing in this entry endorses a policy as good, sufficient
or required by a browser; the classes are declared expectations, and a reading
of a recorded header list is not a reading of a rendered page. The audit passes
no judgement on MIME sniffing, on how a renderer would treat the body, or on
whether a serving stack would keep the same fields on the next request.

## Limits

- A recorded header list is one response to one request at one moment, sent to
  the capture's user agent; a CDN, a proxy or a different request path may
  answer differently [INFERENCE].
- Presence is not policy strength. The audit reads that
  `Strict-Transport-Security` occurs, not what `max-age` says, and it reads that
  a `Content-Security-Policy` field occurs, not what the policy allows
  [INFERENCE for the consequence: a present field can still be a weak or
  immediately expiring policy].
- The singleton class counts recorded field lines. A single field line may
  still carry a comma-separated list, which RFC 9110 permits where a field's
  definition allows it; the audit does not decide list semantics [S433 §5.2].
- Header-name matching is case-insensitive and values are OWS-trimmed; a
  duplicated name differing only in case is still one name to this audit.
- A check whose receipt is missing or unreadable, or whose recorded status is
  not parseable, is reported as not evaluable rather than clean [INFERENCE: the
  consequence is that a broken capture cannot turn into a passing audit line].
- The four sources are read at their 2026-10-27 bodies; a later revision of a
  specification may reword a quoted span. The `recheck: 180d` cadence is how
  the lane keeps that from going stale silently.

## Round-62 correction held — S432 quote remains unresolved

[r62-correction 2026-10-27] The round-61 non-author spot-check records that the admitted S432 span “Web developers and conformance checkers must use the following” is a generic lead-in, not evidence for a response-header expectation (`corpus/lessons/round-61-verifier-spotcheck.md:33`). The earlier fragment “can be used to require checking of a” ends before its object. The retained §3.6 sentence at `.ufo/waves/round-61/sources/S432.html:6150–6156` contains the field-purpose proposition across inline markup, but that rendered sentence is not a raw substring of the retained HTML. Existing `corpus/QUALITY.md` quote rules require raw-substring evidence. This round therefore does not substitute a normalized cross-markup quote or claim the knowledge citation is corrected; the S432 disagreement remains open. The row stays mined for the field's separately supported value rule; no registry cell changed.

## Round-63 correction — S432 field-purpose span admitted as collapsed-only

[r63-correction 2026-10-27] The round-62 held correction above resolves this
round. The field-purpose sentence of WHATWG Fetch §3.6 — retained body
`.ufo/waves/round-61/sources/S432.html` raw lines 6150–6154 — is quoted here in
its located rendering and classed by derivation from its two retained blobs,
under the round-50 quote-class rule (`corpus/QUALITY.md`):

> "The `X-Content-Type-Options` response header can be used to require checking of a response’s `Content-Type` header against the destination of a request."

The span is a substring of the committed flat-text rendering
`.ufo/waves/round-63/quote-class/S432.txt` (sha256
`8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69`) and not of
the retained HTML (sha256
`63b0a018753c330adf1e40417524eb70ea02d4d3e123bcb39b6770f23bad911b`), so its
derived class is `collapsed-only` — never described as a raw substring. The
class, both blob digests and the extraction recipe
(`.ufo/waves/round-63/quote-class/extract_text.py`, textContent semantics) are
recorded in `.ufo/waves/round-63/quote-class/quote-classes.json`; the class is
re-derived by the lane tool `scripts/quote_class.py` (selftest 4/4, real case
`s432_real`). This span substantively states the proposition the
`xcto_nosniff_value` section attributes to S432 (a field-purpose statement,
kept separate from the `nosniff`-only value rule per the round-62 criterion).
The two earlier spans quoted in that section — the fragment ending before its
object and the generic lead-in — remain historical text and ground nothing.
The source was re-opened live this round: one GET of
https://fetch.spec.whatwg.org/ on 2026-10-27 returned a body byte-identical
(sha256 `63b0a018…911b`) to the round-61 retained body. No registry cell
changed; the S432 row stays `mined` with its existing scope.
