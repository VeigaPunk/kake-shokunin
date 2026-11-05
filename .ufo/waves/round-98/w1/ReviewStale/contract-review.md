# Contract review — stale-contract.md vs RFC 5861 / RFC 9111 (seat ReviewStale, round 98)

Reviewed: `.ufo/waves/round-98/stale-contract.md` (sha256 `ec077b4f…71075`, frozen digest
reproduced) against `sources/rfc5861.txt` (sha256 `1193f1c8…2529e`, matches the freeze) and
`round-96/w1/ScoutRFC/rfc9111.txt`. Companion verdicts: `hand-verdicts.tsv` (60/60 judged).

## A. Contract sentences that state a convention as if it were an RFC requirement (unmarked)

**F1 — the SWR/SIE event split (medium).** The Decision section routes every `error` event to
stale-if-error only; `stale-while-revalidate` never covers an error (hand case H16 asserts this
as "5861§3"). RFC 5861 §3 states the permission circumstance-free: "caches MAY serve the
response in which it appears after it becomes stale, up to the indicated number of seconds." A
literal reading licenses stale serving inside the window even when the revalidation errors; the
error-through expectation rests on the synthesis "§3 governs revalidation serving, §4 governs
error serving" (supported by §1 "two independent" extensions and RFC 9111 §4.2.4's
generate-stale-unless-permitted frame), but the contract never marks this reading as an
interpretive choice — unlike its three explicitly marked lane conventions. The decision is
defensible and mainstream; it should carry a convention mark or a citation, because the counter
and the pos-oracle bake it in as if quoted from the RFC.

**F2 — request `no-cache` as a hard prohibition (minor).** The `prohibited` definition includes
"the request carries `no-cache`" with no convention mark. RFC 9111 §5.2.1 intro: request
directives "are advisory; caches MAY implement them, but are not required to"; §5.2.1.4 states a
client *preference*, and §4's reuse-conditions list (lines 469-484 of the retained body) does not
include request no-cache among the MUST-level blocks. Implementing the preference as a
prohibition is a permitted choice, but the contract states it flat alongside the genuinely
unconditional §5.2.2 response-directive MUSTs — an asymmetry with its own marked
qualified-`no-cache` convention three words earlier.

**F4 — delta-seconds clamp (cosmetic).** Parsing rule 4: "values above 2147483648 are clamped to
2147483648 (RFC 9111 §1.2.2)". §1.2.2's MUST is conditioned on the value exceeding "the greatest
integer it can represent"; an unbounded-arithmetic recipient reads the rule differently. The
clamp is the conventional strict reading (the §1.2.2 note frames 2147483648 as infinity), and no
hand case distinguishes the readings (H35: 1e9 < both candidate limits), but as written the
contract presents the conventional reading as the quoted MUST.

## B. RFC 5861/9111 rules in scope that the contract omits

**F3 — the s-maxage freshness coupling (medium-minor).** The contract makes `s-maxage` a shared-
cache prohibition on *presence* and simultaneously takes `freshness_lifetime` as an opaque input
("Out of scope: computing L"). RFC 9111 couples them: §4.2.1 computes freshness_lifetime with
s-maxage as the first match for a shared cache, and §5.2.2.10's prohibition scopes to "a **stale**
response with s-maxage" — stale per the s-maxage-overridden lifetime. The contract nowhere
states the assumption that the caller computes L per §4.2.1 (s-maxage first when shared). Where
`shared=true` and L < current_age < s-maxage-value, a §4.2.1-faithful shared cache holds a
*fresh* response while the contract's model blocks it via `prohibited`. No hand case hits the
gap (H28/H29 use s-maxage=600=L), but the 240-case generator draws `s-maxage=` independently of
L with `shared` coin-flipped, so the oracle itself will encode the over-blocking answer on
generated cases. One sentence ("freshness_lifetime is assumed to already reflect s-maxage for a
shared cache, per §4.2.1") would close it.

## C. Checks that produced no finding

- Parsing rule 3 (first occurrence) — accurately cited: §4.2.1 does *allow* first occurrence
  ("either the first occurrence should be used or the response should be considered stale").
- Inclusive boundaries — properly derived from §4 ("more stale than the indicated amount") and
  §4.1 ("after the age is greater than 1800"); verified against both quotes.
- Marked rule 4 ("quoted or non-digit value → absent") is unnecessarily modest: it follows from
  RFC 5861 §3/§4 ABNF (delta-seconds = 1*DIGIT via §1.2.2) plus §5.2.3 ("MUST ignore
  unrecognized"). Marked-conservative, not wrong.
- RFC 9111 §5.2 intro "recipients ought to accept both forms" (token/quoted-string) applies only
  to directives defined in 9111; for in-scope 5861 extensions the absent-directive reading
  stands. No observable effect in scope (the tool consumes neither max-age's nor s-maxage's
  value), so no finding.
- RFC 5861 §3 SHOULD-revalidate-while-serving and the §3/§4 visible-staleness requirements
  (non-zero Age, Warning) are explicitly declared out of scope in the contract, not omitted.
- must-revalidate's disconnected case (§5.2.2.2: MUST generate an error even when disconnected)
  is covered by `error-through` at decision level.

## Sourcing note

RFC 9110 §5.6.2/§5.6.4 (token/quoted-string; row S478) is cited by the contract but no RFC 9110
body is retained in-lane (`sources/` holds only rfc5861.*; ScoutRFC holds rfc9111.txt). The
grammar-dependent verdicts (H44, H46, H52, H54, H57, H60) are judged against the contract's
stated grammar, which mirrors the 9110 ABNF; they could not be checked against a retained 9110
body. Flagged for the L1's source ledger, not a contract defect.
