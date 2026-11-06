# ReviewFresh — C2 contract review against RFC 9111 §3.1 / §3.2 / §4.3.4

Scope: `fresh304-contract.md` (contract v1, LC1–LC6), the 50 HAND expectations in `c99_fresh304.py`, and
erratum EID 9185. Read-only. Nothing in the lane was edited. Per-case verdicts: `hand-review.tsv`.
Command receipts (digest check, counter run, sha256 of fetched RFC 9110): `receipts.txt`.

Sources. RFC 9111 is the lane's retained copy (`sources/rfc9111.txt`; digest rc=0 in receipts.txt).
RFC 9110 is NOT retained in the lane. I fetched it from rfc-editor.org into scratch (sha256
21c1cdce…, in receipts.txt) and cite it as "RFC 9110". It should be retained before a closure cites it.

Headline: hand 48/50 agree; 2 disagree (both on one output-value rule, F2). Contract findings: 12.
RFC contradictions (direct): 3 (F1, F2, F10).

## Retained or fetched text relied on

- §3.1 (retained): exceptions to "MUST include all received header fields": Connection and listed fields
  ("MAY be implemented by doing so before storage"); hop-by-hop fields (see 7.6.1); no-cache / private
  qualified arguments ("can have arguments that prevent storage of header fields by all caches / shared
  caches"); proxy-specific fields ("MUST NOT be stored").
- §3.2 (retained): MUST add each header field, replacing present values, except §3.1 exceptions, fields the
  stored response depends upon (MAY, see LC5), auto-processed fields (MAY), and Content-Length.
- §4.3.4 (retained): bullet 1, strong (MUST NOT update if no initial-set response shares a strong validator);
  bullet 2, weak ("the most recent of those matching"); bullet 3, no validator (single response, no validator
  on either side). Update per §3.2.
- §5.2 (retained, lines 1098–1106): directive names case-insensitive; argument token OR quoted-string;
  "recipients ought to accept both forms". §5.2.2.4 and §5.2.2.7 define the qualified forms with
  quoted-string argument syntax; a sender SHOULD NOT generate the token form.
- §5.2.3 (retained): "A cache MUST ignore unrecognized cache directives."
- RFC 9110 5.5: a field value does not include leading or trailing whitespace; a field parsing implementation
  MUST exclude such whitespace prior to evaluating the field value; obs-text = %x80-FF (octets).
- RFC 9110 7.6.1: enumerated examples Proxy-Connection, Keep-Alive, TE, Transfer-Encoding, Upgrade
  ("includes but is not limited to"). These are exactly LC4's five names.
- RFC 9110 8.8.2.2: Last-Modified is implicitly weak unless strength is deducible.
- RFC 9110 8.8.3 / 8.8.3.2: entity-tag = [weak] opaque-tag; weak = %s"W/" (case-sensitive); etagc =
  %x21 / %x23-7E / obs-text; strong comparison needs both tags not weak; weak comparison ignores W/.
- RFC 9110 8.8.2 (fetched line 3487): Last-Modified = HTTP-date.

## Lane conventions: verdicts

- **LC1 (Last-Modified always weak): agree.** RFC 9110 8.8.2.2 makes LM weak unless strength can be deduced.
  The contract's input has no Date, so it cannot deduce. Side effect: LM-only 304s take rule 2 (one most-recent
  response), not rule 1 (all matches). Permitted.
- **LC2 (every validator the 304 carries must correspond): agree, but load-bearing (F7).** RFC 9111 4.3.4
  bullet 2 leaves "correspond" undefined for several validators.
- **LC3 (tie at the largest received -> refuse): agree.** RFC names a single "most recent" and gives no tie rule.
- **LC4 (fixed five-name hop list): agree.** Equal to the RFC 9110 7.6.1 enumerated examples. RFC says
  "not limited to", so fixing the list is a choice, which the LC marks.
- **LC5 (depends-upon and auto-processed exceptions not modelled): agree.** Both are MAY in §3.2 and §3.1 bullet 2.
- **LC6 (refuse a 304 with qualified no-cache / private): partly disagree as written (F1, F10).** Correct for the
  quoted form. The token form (`no-cache=Set-Cookie`) is the same qualified directive under §5.2 grammar, and
  LC6 misses it (F1). The literal substring also refuses unrecognized extension directives such as
  `x-no-cache="…"`, which §5.2.3 says MUST be ignored (F10).

## Findings

Severity H / M / L. RC = counted as an RFC contradiction: contract behaviour on RFC-valid input contradicts a
MUST, MUST NOT, or normative exception in the retained or fetched text.

**F1 (M, RC). Token-form qualified no-cache / private is not treated as qualified.**
- RFC: §5.2 grammar, cache-directive = token [ "=" ( token / quoted-string ) ], "recipients ought to accept
  both forms"; §5.2.2.4 and §5.2.2.7 define the qualified forms; §3.1 bullet 3: the argument "can have
  arguments that prevent storage of header fields by all caches / shared caches".
- Contract: LC6 matches `no-cache="` and `private="` only. A 304 with `Cache-Control: no-cache=Set-Cookie` (or
  `private=Set-Cookie`) passes, and the update copies Set-Cookie into the stored response. §3.1 bullet 3 says
  it must not be stored.
- The reference (`c99_fresh304.py`, lines 115–117) has the same gap. No HAND or generated case covers the token
  form, so a candidate can pass the counter while contradicting §3.1. Hand cases ref-qualified-nocache and
  ref-qualified-private test the quoted form only.
- Routed: LC6 should recognise both token and quoted argument forms (refuse, or exclude the named fields). Add
  a hand case for the token form at the next freeze.

**F2 (M, RC). Byte-for-byte copy of values with leading or trailing whitespace.**
- RFC 9110 5.5: a field value does not include leading or trailing whitespace; a field parsing implementation
  MUST exclude it before evaluating the field value.
- Contract, Output: "values are copied byte-for-byte (no trimming)" (not LC-marked). The contract trims before
  comparing ETag and LM, so it accepts OWS-bearing input, then stores untrimmed values in the updated response.
- Hand expectations that encode the violation: `strong-trim` (copies a trailing HTAB; decision agrees) and
  `upd-value-bytes-kept` (copies leading and trailing spaces and an inner HTAB). Both are marked disagree.
- Routed: trim values on input and say so in Output, or refuse OWS-bearing values. Either change flips those two
  hand expectations. Not repaired (frozen).

**F3 (M, propagation, not counted as RC). Stored proxy-specific and hop-by-hop fields pass through the update.**
- RFC 9111 3.1 bullet 4: Proxy-Authenticate, Proxy-Authentication-Info and Proxy-Authorization MUST NOT be stored.
- Contract: the updated map starts from the caller's stored headers (`dict(n[2])`) and filters only the 304's
  fields. A stored response that already holds Proxy-Authorization (RFC-conformant storage never does) comes back
  with it in `updated`. Nothing filters or refuses it, and no hand case covers it.
- Not counted as an RFC contradiction, because the input is not RFC-valid storage. Counted as a contract finding
  because the output is the new stored response.

**F4 (M). Erratum EID 9185: the contract names no initial-set definition.**
- EID 9185: Status Reported (not Verified); Type Technical; reported by Daniel Fox Franke, 2026-09-24.
  It replaces the §4.3.4 initial-set paragraph: a stored response qualifies if it matches the request (target,
  method, selecting headers) OR its ETag strong-matches the 304. The appended text says a strong-ETag
  identification despite a selecting-header mismatch MUST re-associate the updated response with the 304's
  request header fields (MUST, for the purposes of §4.1).
- Does it change any HAND expectation? **No.** Every HAND case supplies the stored list directly. The erratum
  changes which responses the caller places in `stored` (Vary-mismatched strong matches), not the decision or
  the update for a given list. Rule 1 already identifies by strong ETag. Rules 2 and 3 are unchanged. The
  contract's statement that the erratum "does not change it" is correct for what the contract computes.
- What is missing: the Input section says `stored` is the initial set "as the caller computed it" and does not
  name the definition. Under the erratum, a Vary-mismatched strong match enters rule 1 and a Vary-mismatched weak
  match is excluded from rule 2. Under the original text neither is in the set. The same wire exchange can give
  different results depending on the caller's definition. Name the definition (the erratum is not normative).
- The erratum's re-association MUST has no representation in the output (F12).

**F5 (L-M). "Most recent" is defined as receipt order with no LC marker.**
- RFC 9111 4.3.4 bullet 2 says "the most recent of those matching stored responses" and does not define it.
- Contract Input: `received` is an integer, "receipt order; larger = more recent". A reasonable cache reading
  (most recently stored). Not LC-marked, yet it decides four hand cases: weak-etag-most-recent,
  weak-tie-refused, weak-tie-below-top-ok, weak-negative-received.
- Routed: mark it as LC7.

**F6 (L). obs-text is defined as code points U+0080–U+00FF, not octets.**
- RFC 9110 5.5 and 8.8.3: obs-text = %x80-FF is an octet range. A UTF-8 ETag such as `"€"` (octets E2 82 AC, all
  obs-text) is RFC-valid, and the contract refuses it as malformed. `"é"` passes only because U+00E9 is in range.
- Not counted as an RFC contradiction: JSON input has no octet semantics and the mapping is stated. It is still
  an unmarked convention that refuses RFC-valid input. Routed: mark the mapping as an LC.

**F7 (L-M). LC2's "all validators must correspond" decides a hand case and rests on open RFC text.**
- RFC 9111 4.3.4 bullet 2: "those validators correspond to one of the initial set's stored responses". The
  quantifier is undefined.
- Under "any validator corresponds", hand `weak-both-need-both` flips: stored a (received 3, ETag only) would be
  identified and win. LC2 is marked, so this is a stated choice. Record it as a known interpretation.

**F8 (L). A §3.1 MAY is presented as a requirement.**
- §3.1 bullet 1: Connection and listed fields "MAY be implemented by doing so before storage". Bullet 2 is also MAY.
  §3.2 counts "excepted from storage in Section 3.1" as an exception to the update MUST, so excluding them from the
  update is permitted.
- Contract cites "(§3.1 bullet 1)" for "never copied" as if mandatory. Hand case `upd-connection-listed` depends
  on the permitted choice. Not a contradiction. Relabel as a choice.

**F9 (L). Last-Modified accepts any string.**
- RFC 9110 8.8.2 (fetched line 3487): Last-Modified = HTTP-date. LC1 (marked) says "any string value", and the
  Refusals list has no malformed-LM case. Recipients are not required to refuse, so this is a noted choice.
  Exact-octet comparison of arbitrary strings means two spellings of one instant do not match.

**F10 (M, RC). LC6 literal check refuses a 304 whose unrecognised directive merely ends in `no-cache` or `private`.**
- RFC 9111 5.2.3 (retained): "A cache MUST ignore unrecognized cache directives." `Cache-Control: x-no-cache="y"`
  is an unknown extension, yet LC6's text ("contains `no-cache="`") and the reference's substring check
  (`c99_fresh304.py` line 116: `'no-cache="' in cc.lower()`, and the same for private) refuse it.
- No HAND or generated case covers it.
- Routed: match the whole directive name at a token boundary before applying the argument check. The reference
  defect is an instrument-level observation for the instrument owner; not repaired here.

**F11 (L). Stored-side refusal is broader than the RFC requires.**
- Contract Refusals: "malformed ETag in the 304 or in any stored response" refuses the whole call. RFC 9111 says
  nothing about refusing. A malformed ETag on a stored response that is not identified cannot change the result,
  yet the whole call is refused. Unmarked. Routed: refuse on identified responses only, or mark the choice.

**F12 (L-M). The Not-covered list omits three things the RFC or erratum needs.**
- The erratum's Vary re-association (F4). §3.4 (combining partial content), which §3.2 cites as a case where updates
  are required. It is a 206 path, out of scope for this 304 contract, but the list should say so. §4.1 selecting-
  header matching, which determines the initial set the caller must compute.
- Add these to Not covered.

## Instrument notes (not counted in contract_findings)

- I1: the reference LC6 substring check (`c99_fresh304.py` lines 115–117) is the instrument root of F10.
- I2: no HAND or generated case exercises the token form (F1) or extension directives containing `no-cache=` /
  `private=` (F10). A candidate can pass the counter while violating §3.1 bullet 3 or §5.2.3.
- I3: the counter reference agrees with all 50 HAND expectations (receipts.txt: counter exit 1 with
  `candidate=absent`, no drift exit 2). The reference therefore carries F1/F10 forward but not any HAND drift.

## Counts

- Hand expectations: agree 48/50. Disagree 2 (`strong-trim`, `upd-value-bytes-kept`; F2).
- Hand expectations grounded only in unmarked Input/Refusal sentences (interface, not RFC, not LC): 10 cases
  marked IFACE in hand-review.tsv (ref-status-bool, ref-extra-key, ref-dup-id, ref-empty-id, ref-received-bool,
  ref-received-float, ref-case-dup, ref-nonstring, ref-stored-not-list, ref-not-object). Counted as agree (they are
  interface checks), but not RFC-grounded. ref-status-200 rests on §4.3.4 scope.
- contract_findings = 12 (F1–F12).
- rfc_contradictions = 3 (F1: §3.1 bullet 3 with §5.2 token form; F2: RFC 9110 5.5; F10: RFC 9111 5.2.3).

## Verdict line

`REVIEWFRESH hand=48/50 contract_findings=12 rfc_contradictions=3`
