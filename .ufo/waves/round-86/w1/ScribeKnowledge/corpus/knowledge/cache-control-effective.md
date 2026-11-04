source: S461 — proposed new lane row for RFC 9111 HTTP Caching (httpwg rendering) — https://httpwg.org/specs/rfc9111.html §4.2.1/§5.2/§5.2.2, also §1.2.2 and §5.3; pending L1's guarded append and mirror-census gate. S457 supports preexisting max-age/freshness semantics only; S456 supports the general caching background, not directive argument syntax. Neither old row is enlarged to cover ordering. Independently fetched GET-only by ScribeKnowledge; HTTP 200, 178573 bytes, sha256 999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64; retained at `.ufo/waves/round-86/w1/ScribeKnowledge/s457-rfc9111.html` with response headers alongside it.
verified-at: 2026-11-04 — own GET completed 15:36:38Z; lane re-open receipt `.ufo/waves/round-86/w1/ScoutCache/s457.fetch.meta` records GET 200 at 15:37:19Z with the same size and SHA-256. Own located quote: retained HTML line 270, §4.2.1 paragraph 4. This seat verified source text, not reader execution or C2 acceptance.
recheck: 180d, due 2027-05-03, or sooner after a source change. In authorized scratch, run `curl --fail --silent --show-error --output /fast/scratch/hyaku/kake-r86/ScribeKnowledge/rfc9111-recheck.html https://httpwg.org/specs/rfc9111.html && sha256sum /fast/scratch/hyaku/kake-r86/ScribeKnowledge/rfc9111-recheck.html`; create that scratch directory first and remove it afterward. Compare the fingerprint above and relocate §4.2.1/§5.2/§5.2.2 before reusing the conclusions.
ground: freshness — round-86 C2, bounded value-level Cache-Control reading.
scope: Already-isolated response field values, explicit freshness lifetime inputs and directive flags; not general HTTP cache conformance.

# Cache-Control effective freshness

## Effective-freshness decision order

RFC 9111 §4.2.1 evaluates these rules in order and uses the first match:

1. For a **shared** cache, use `s-maxage` when present.
2. Otherwise use `max-age` when present.
3. Otherwise use `Expires − Date` when `Expires` is present.
4. Otherwise there is no explicit freshness lifetime; heuristic freshness is a separate question.

The first three rules are at retained HTML line 270. §5.2.2.10 (line 282) expressly makes shared `s-maxage` override `max-age` or `Expires`; a private-cache reader must not apply that override. The RFC permits receipt time when Date is absent; this offline JSON adapter has no receipt-time input and must not invent a live clock observation. Nulls and negative-lifetime clamping are local output conventions, not quotations from the RFC.

Freshness lifetime is not remaining freshness: §4.2 (line 269) compares age with lifetime. This instrument does not calculate current age or decide whether a stored response can actually satisfy a request.

## Duplicates, conflict and invalid information

Own located quote (14 words), §4.2.1 paragraph 4, retained HTML line 270:

> either the first occurrence should be used or the response should be considered stale.

This is the source's lower-case “should,” not a MUST requiring every cache to implement one algorithm. The round-86 adapter deliberately selects the first-occurrence branch and records duplicate names. Thus ordered `max-age=200`, `max-age=100` yields lifetime 200, not the minimum 100. Reversing those duplicate values changes the selected lifetime. Frozen cases 5 and 15 distinguish first occurrence from a minimum-value shortcut; they are expectations, not executions by this seat.

Do not conflate duplicate values with conflicting directives. The following source sentence says conflicting directives (for example `max-age` and `no-cache`) should honor the most restrictive directive. Invalid freshness information, such as a noninteger max-age, is encouraged to be treated as stale. The local reader reports `invalid_directives` and `conflict`; those JSON fields are the contract's reporting convention. Its `max-age=100, no-cache` example retains the numeric lifetime while setting `no_cache=true` and `conflict=true`; the numeric lifetime alone does not authorize reuse without validation.

### RFC 7234 contrast — correcting the minimum-value folk rule

Independently fetched https://www.rfc-editor.org/rfc/rfc7234.txt GET-only at 2026-11-04T15:37:12Z: HTTP 200, 90647 bytes, sha256 1d084238ae6692d1e3322fa0850dbb9596812332d92b76d9a815c5ed9b600dea, retained at `.ufo/waves/round-86/w1/ScribeKnowledge/rfc7234-contrast.txt`.

RFC 7234 §4.2.1, retained lines 691–695, considered a duplicate directive's value **invalid**, encouraging stale treatment. It did not prescribe taking the minimum duplicate value. Calling minimum selection “RFC 7234's most-restrictive rule” is therefore a false attribution. RFC 9111 Appendix B (retained HTML line 304) says duplicate/conflicting directive handling was clarified. Its first-occurrence-or-stale rule and its separate most-restrictive **conflict** advice must not be collapsed into a minimum-value algorithm.

## Storage, names, arguments and bounds

- **no-store:** §5.2.2.5 (line 282) prohibits storage and reuse for another request, in both shared and private caches. The adapter reports `storable=false`, `basis="no-store"`, and no numeric lifetime. Absence of no-store does not prove general cacheability; `storable` is a bounded local output, not every §3 storage condition. `must-understand` store-permission is excluded.
- **Case:** §5.2 (line 279) compares directive-name tokens case-insensitively. Thus `MAX-AGE=90` is recognized. This is not permission to lowercase arbitrary argument values or other header fields.
- **Quoted arguments:** the same §5.2 paragraph says recipients ought to accept token and quoted-string argument forms even when generation requires a particular form. A recipient can therefore accept quoted numeric arguments; quoted field-name lists such as `no-cache="Set-Cookie"` must not be split as ordinary comma-separated directives. Qualified no-cache is distinct from unqualified no-cache; reporting a field-name list is not a full qualified-no-cache implementation.
- **Delta-seconds:** §1.2.2 (line 267) defines a nonnegative decimal integer and guards binary overflow with 2147483648 (2^31) **or** the greatest conveniently representable positive integer. The adapter's unconditional 2147483648 cap is a deterministic local profile, not a universal RFC ceiling. The huge-integer frozen case expects that profile.
- **Flags:** `must_revalidate` and `must_understand` report recognized directives; they do not implement validation, status-code storage permissions, or network behavior.

## Contrast with Referrer-Policy: field-specific semantics

The round-85 S458 entry `referrer-policy-effective.md` documents the last recognized nonempty Referrer-Policy token winning in ordered input. Reordering `no-referrer, strict-origin` changes its result.

For Cache-Control's distinct `no-store` and `max-age` directives, their positions do not change the bounded no-store result: `max-age=60, no-store` and `no-store, max-age=60` both forbid storage. This is the frozen order-witness pair, not arbitrary-header equivalence. Duplicate max-age values are the important exception: first-occurrence selection is order-sensitive. Neither “all Cache-Control order is irrelevant” nor a blanket reordered-header equivalence follows. The r84 general classifier remains experimental and is not rewritten by this separate reader.

## Planned offline interface — not exercised by this seat

After L1 integrates the candidate, the planned command is:

```sh
printf '%s\n' '{"cache_control":["max-age=200","max-age=100"],"expires":null,"date":null,"shared":false}' | python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/cache_control_effective.py
```

Contract-derived expected output, JSON whitespace immaterial:

```json
{"storable":true,"freshness_lifetime_seconds":200,"basis":"max-age","no_cache":false,"no_cache_qualified":[],"must_revalidate":false,"must_understand":false,"duplicate_directives":["max-age"],"conflict":false,"invalid_directives":[]}
```

Input is a JSON object with ordered Cache-Control field-value strings, nullable Expires/Date HTTP-dates, and a shared-cache boolean. Output has the ten fields shown above. The contract specifies exit 0 for decoded input, 1 for invalid data, 64 for usage, plus a TMPDIR-honoring `--selftest`. The frozen counter has fifteen cases; L1 owns measurement and integration. No result here upgrades those expectations into `15/15`, offline proof, or independent closure evidence.

## What this entry does not establish

No browser cache model; no Vary, Age calculation, Pragma, heuristic freshness, raw HTTP extraction, request/response cache interaction, or must-understand store-permission implementation. No arbitrary-header equivalence, full RFC conformance, or upgrade of the r84 classifier. No live property was measured; the public specification GETs are source acquisition only. No publishing authorization, deployment approval, or evidence of a server's actual cache behavior follows. D84-2 and D84-3 remain retained-open; no full D84-queue closure is claimed.
