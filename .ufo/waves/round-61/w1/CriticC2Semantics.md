# CriticC2Semantics

Attack on claim C2's expectation classes: source fidelity (retained bodies opened
under `.ufo/waves/round-61/sources/`), decidability from recorded headers, cheapest
false greens/reds. Evidence: `.files/audit_play.py` (read-only evaluator implementing the
class rules as the contract text states them — NOT the lane tool), `.files/manifest.json`,
`.files/cap.tar.gz` (hand-built receipts), `.files/audit_play.out`. Lane capture
inspected read-only: 12/12 receipts status∈{200,404}, headers as `{"name","value"}`
pairs, duplicates preserved (real `vary` x2 seen).

## CLASS CHECKS:

- `content_type_present` — source-faithful? Partially. S433 §8.3 located quote (verified
  page-unique, 17 tokens, 112 chars): "A sender that generates a message containing
  content SHOULD generate a Content-Type header field in that message". The class is a
  flat presence rule on 2xx; the source is a content-scoped SHOULD. Decidable? Yes —
  needs only the recorded status + header names. Issues: no status carve-out (see FR-1)
  and no empty-value arm (see FG-2).
- `hsts_present` — source-faithful? Yes for presence. S430 §6.1 located quote (20 tokens,
  107 chars): "indicates to a UA that it MUST enforce the HSTS Policy in regards to the
  host emitting the response message". Decidable? Yes (manifest `https` bool + recorded
  names). Issues: presence-only passes headers UAs MUST ignore (S430 rule 4 located quote,
  19 tokens: "UAs MUST ignore any STS header field containing directives, or other header
  field value data, that does not conform") — empty and garbage values included (FG-2/FG-3).
  Note `https` is a manifest assertion; receipts carry `finalUrl` so a wrong flag is
  detectable but not checked by the class. Fine as declared-expectation mechanism.
- `xcto_nosniff_value` — source-faithful? Partially. S432 located quote (16 tokens,
  90 chars): "If values is null, then return false. If values [0] is an ASCII
  case-insensitive match for" — Fetch checks only values[0], returns false on absent,
  ABNF `= "nosniff" ; case-insensitive`. Case-insensitive comparison is correct (H6) but
  the class text says "not exactly nosniff" — the case-insensitivity is forced by fixture
  H6, not stated in the text (wording gap). Decidable? Yes. Issues: no absent-arm (FG-1,
  the big one); multi-value divergence (FR-2).
- `csp_present` — source-faithful? Yes for presence. S431 located quote (20 tokens,
  131 chars): "The Content-Security-Policy HTTP response header field is the preferred
  mechanism for delivering a policy from a server to a client". CSP3 parses an empty
  serialized value to a policy with an empty directive set → syntactically present,
  operationally absent (FG-2). Decidable? Yes.
- `singleton_fields` — source-faithful? Yes. S433 §5.2 located quote (15 tokens,
  79 chars): "a sender MUST NOT generate multiple field lines with the same name in a
  message". Set-Cookie exemption grounded by S433 §5.2 note (17 tokens, 96 chars):
  "often appears in a response message across multiple field lines and does not use the
  list syntax". Decidable? Yes — capture preserves duplicates (real receipts already
  carry `vary` twice; the class is live). Issues: none beyond manifest-driven scope.
- `field_name_syntax` — source-faithful? Grammar exists in S433: `field-name = token`
  (§5.1), tchar §5.6.2; located quote candidate (11 tokens, 70 chars): "Field names are
  case-insensitive and ought to be registered within the". Decidable? Yes from recorded
  names. Issues: it is a sixth class that appears ONLY in fixture H12's expected column —
  it is not in the contract's five-class list, not in the manifest `expect` shape (evaluated
  unconditionally), and S433's row scope text names "Content-Type and field-line
  semantics scopes" without field-name grammar. Asymmetric and under-declared.

## FALSE GREENS:

- **FG-1 (cheapest): `xcto_nosniff_value` never fires on an absent header.** The class
  text quantifies over "a recorded X-Content-Type-Options field"; absence produces no
  finding even when the check declares `xcto_nosniff_value: true` — while Fetch's
  determine-nosniff returns false on null (no protection). Demonstrated in
  `.files/audit_play.out`: check `fg-xcto-absent` (all expectations true, XCTO omitted)
  → 0 findings. **Live-confirmed**: in the real capture, 5 of 8 recorded-200 surfaces
  (charter-ghp, ds4cc-primary, lucario-ghp, plazir15-ghp, ufo-fsd-kimi-pro) carry no
  XCTO while their manifest checks declare `xcto_nosniff_value: true` → the audit as
  specified reports clean for this class on every one. All three sibling presence
  classes fire on absence; this one alone doesn't. The expectation name promises a
  nosniff value that absence cannot supply.
- **FG-2: empty value satisfies all three presence classes.** `Strict-Transport-Security:` /
  `Content-Security-Policy:` / `Content-Type:` with empty value "carry" the field per the
  class text → 0 findings, but convey nothing (6797 ABNF allows zero directives; CSP3
  yields an empty directive set; RFC 9110 media-type grammar requires type/subtype).
  Demonstrated: `fg-hsts-empty`, `fg-csp-empty`, `fg-ct-empty` all clean. This is the
  "syntactically present but empty" hole the seat brief predicted — the class rule does
  not catch empty values, and it should: for these policy fields an empty value is
  operationally equivalent to absent.
- **FG-3 (deeper): `hsts_present` passes garbage the UA MUST ignore.** Demonstrated:
  `fg-hsts-garbage` (`Strict-Transport-Security: this is not valid at all,,,,`) → 0
  findings while S430 §6.1 rule 4 has UAs ignore it (no policy established). Presence
  cannot see `max-age=0` (immediate expiry) either. A stricter rule (require a parseable
  `max-age` directive) is decidable from recorded headers; costs a policy tightening.

## FALSE REDS:

- **FR-1 (cheapest): `content_type_present` flags a compliant 204.** Demonstrated:
  `fr-ct-204` (recorded 204, no headers) → `content_type_present` finding. S433
  §15.3.5 located quote (18 tokens, 100 chars): "A 204 response is terminated by the
  end of the header section; it cannot contain content or trailers" — the §8.3 SHOULD
  is scoped to "a message containing content", so a 204 legitimately omits Content-Type
  and the finding contradicts the cited source. 304 (§15.4.5, same "cannot contain
  content" sentence) is 3xx and outside the 2xx gate anyway; 205 (§15.3.6) is the other
  2xx contentless status.
- **FR-2: `xcto_nosniff_value` diverges from Fetch on multi-value.** Demonstrated:
  `fr-xcto-first-nosniff` (recorded `X-Content-Type-Options: nosniff` then `sniff`) →
  `xcto_nosniff_value` finding, but Fetch's algorithm tests values[0] only — the UA is
  protected. (The reversed order `sniff, nosniff` flags too, which matches spec's
  unprotected result, so only first-value orderings diverge.) The class has no stated
  multi-value rule at all — a manifest ambiguity, not just a divergence.
- Minor: `hsts_present`/`csp_present` fire on non-2xx recorded statuses too (real
  capture has four https:true 404 checks). That is consistent with the declared-
  expectation model (R3 is recorded, not asserted clean), noted as intentional.

## TIGHTENINGS:

1. `xcto_nosniff_value`: add an absence arm — "or carries no `X-Content-Type-Options`
   field when the expectation is declared true → finding". Counter side: one new
   fixture case (expectation true, header absent → 1 finding). Cheapest fix of the
   audit's only asymmetric class; grounded by S432's null→false step.
2. Presence classes (CT/HSTS/CSP): redefine "carry no F" as "carry no F with a
   non-empty value after OWS trim". One clause; three empty-value greens closed.
3. `content_type_present`: scope to statuses that can carry content — exclude 204
   and 205 (or phrase "2xx responses other than 204/205"). Cited-source-consistent;
   one fixture suffices (204, declared expectation, no CT → 0).
4. `xcto_nosniff_value` wording: replace "not exactly nosniff" with "not an ASCII
   case-insensitive match for `nosniff` after OWS trim" — matches Fetch §3.6 and the
   already-frozen H6/H17 fixtures; closes the text-vs-fixture gap.
5. `xcto_nosniff_value` multi-value: pin the rule. Recommended: flag if ANY recorded
   value is not the case-insensitive nosniff match (current behavior, stricter than
   Fetch's values[0] — say so in the class text), or adopt values[0] for spec parity.
   Either kills the ambiguity; no frozen fixture changes needed.
6. `field_name_syntax`: add it to the contract's class list as the sixth,
   unconditional class with pinned grammar `field-name = token` (RFC 9110 §5.1,
   tchar §5.6.2) and extend the S433 row scope to name §5.1. Currently it exists only
   in H12's expected column.
7. (Optional, deeper) `hsts_present`: consider requiring a parseable `max-age`
   directive — decidable from recorded values; rejects `max-age=0`-expired and
   UA-ignored garbage. Bigger policy tightening than 1–6; name it, don't bake it in.

All candidate located quotes above were verified in the retained bodies: exact
substring of the whitespace-collapsed text, page-unique, 6..25 tokens, ≤160 chars,
ASCII. Unverified claim (H12's `X Bad Name` can't arrive via a conformant client):
[INFERENCE] response_snapshot records whatever its HTTP parser accepts; the syntax
class is exercised by hand-built manifests only.

VERDICT: 4 of 6 classes are decidable-but-loose: cheapest false green is xcto_nosniff_value firing only on present-but-wrong values (live-confirmed on 5/8 real 200s), empty-value variants fool all three presence classes; cheapest false red is content_type_present flagging compliant 204s; six one-line tightenings + one optional deepen listed.
