# S457 re-open receipt draft — ScoutCache, kake round 86 w1

Draft only. This seat writes nothing in production; `corpus/SOURCES.md` and the
round lesson are owned by L1's integration after WAVE-DONE. Paths below are
relative to the lane root `/home/vgpnk/Projects/shokunin/kake-shokunin`.

## Re-open GET receipts (2026-11-04)

| Field | S457 (primary, re-opened) | S456 (support) |
|---|---|---|
| URL | https://httpwg.org/specs/rfc9111.html | https://www.rfc-editor.org/rfc/rfc9111.txt |
| Final URL | https://httpwg.org/specs/rfc9111.html (no redirect) | https://www.rfc-editor.org/rfc/rfc9111.txt (no redirect) |
| Status | 200 | 200 |
| Bytes | 178,573 | 84,477 |
| sha256 | `999f401328ed8991d172aeb1cd4ab048630928437af2401d3e39552c4a073f64` | `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e` |
| Fetched (UTC) | 2026-11-04T15:37:19Z | 2026-11-04T15:37:20Z |
| Server hints | last-modified Mon, 19 Oct 2026 01:13:54 GMT; etag "6ad56ed2-2b98d"; date Wed, 04 Nov 2026 15:37:19 GMT | etag W/"f8907618635703edd228aee4aa834eee"; date Wed, 04 Nov 2026 15:37:20 GMT |
| Retained body | `.ufo/waves/round-86/w1/ScoutCache/s457.body.html` | `.ufo/waves/round-86/w1/ScoutCache/s456.body.txt` |
| Retained headers/meta | `s457.headers`, `s457.fetch.meta` | `s456.headers`, `s456.fetch.meta` |

Both sha256 values match the abbreviated expectations displayed in
`corpus/knowledge/policy-value-classes.md` (`recheck:` line: S457 expect
`999f4013…`, S456 expect `aeb52adb…`); no full historical-body comparison
was run. S457 HTML contains the operative text
(`first match` ×2, `overrides the maximum age` ×1) and all cited anchors
(`rfc.section.1.2.2`, `rfc.section.4.2.1`, `rfc.section.5.2`,
`rfc.section.5.2.2.1`, `rfc.section.5.2.2.5`, `rfc.section.5.2.2.10`) exactly
once each. Method: GET-only public fetches (curl, exit 0), no POST probe (none
authorized for this seat).

## Proposed used-by old→new (S457, `corpus/SOURCES.md` row S457, used-by cell)

- old: `corpus/knowledge/policy-value-classes.md`
- new: `corpus/knowledge/policy-value-classes.md; corpus/knowledge/cache-control-effective.md`

Ground: round-86 C2 introduces the bounded value-level Cache-Control reader
`scripts/cache_control_effective.py`, grounded in S457 per the frozen contract
(`.ufo/waves/round-86/contract.md` §C2). The new knowledge entry
`corpus/knowledge/cache-control-effective.md` does not exist at base
(`test -e` → absent) and is to be created during integration; it consumes S457
alongside, not instead of, the r84 entry. The r84 entry stays listed; this is an
addition to the used-by set, not a migration.

## Quoted spans re-grounded (all verified as dehyphenated substrings of the retained `s456.body.txt`; word counts within the ≤25 limit)

| Section (S457 anchor) | rfc9111.txt lines | Quote (≤25 words) | Verify |
|---|---|---|---|
| §4.2.1 `rfc.section.4.2.1` first-match | 654–656 | "evaluating the following rules and using the first match" | PASS, 9 w |
| §4.2.1 duplicate first-occurrence-or-stale | 677–681 | "either the first occurrence should be used or the response should be considered stale" | PASS, 14 w |
| §5.2 `rfc.section.5.2` case-insensitive + quoted acceptance | 1099–1104 | "identified by a token, to be compared case-insensitively, and have an optional argument that can use both token and quoted-string syntax" | PASS, 21 w |
| §5.2.2.1 `rfc.section.5.2.2.1` token-form generation | 1218–1220 | "This directive uses the token form of the argument syntax: e.g., 'max-age=5' not 'max-age=\"5\"'.  A sender MUST NOT generate the quoted-string form." | PASS, 22 w |
| §5.2.2.5 `rfc.section.5.2.2.5` no-store | 1297–1299 | "MUST NOT store any part of either the immediate request or the response and MUST NOT use the response to satisfy any other request" | PASS, 24 w |
| §5.2.2.10 `rfc.section.5.2.2.10` s-maxage override | 1390–1393 | "the maximum age specified by this directive overrides the maximum age specified by either the max-age directive or the Expires header field" | PASS, 22 w |
| §1.2.2 `rfc.section.1.2.2` delta-seconds cap | 222–225 | "the cache MUST consider the value to be 2147483648 (2^31) or the greatest positive integer it can conveniently represent" | PASS, 19 w |

Verification transcript: `.ufo/waves/round-86/w1/ScoutCache/verify-quotes.txt`
(7/7 substring PASS, 7/7 within word limit).

## Limits

- Quotes are normalized-whitespace substrings of the retained `.txt` body; the
  `.html` body carries markup inside sentences, so `.txt` line numbers are the
  raw-span reference and `.html` ids are the anchors, matching the lane's r84
  convention in `corpus/knowledge/policy-value-classes.md`.

Modal qualification: §5.2 also says “recipients ought to accept both forms,
even if a specific form is required for generation” (lines 1101–1102,
same section anchor). §1.2.2's overflow treatment applies to overflow or an
unrepresentable value, not every representable number over 2147483648;
the contract selects a fixed bounded cap. First-occurrence is one allowed
duplicate disposition; stale is the alternative. No global cache model
or arbitrary-header equivalence follows from these spans.
- Proposal only: no SOURCES.md row, lesson, or knowledge file was written by
  this seat; `cache-control-effective.md` content is L1's to author.
