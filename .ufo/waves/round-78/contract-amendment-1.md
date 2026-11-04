# kake round 78 — contract amendment 1 (terms only, before any after-state)

Recorded 2026-11-03 after the L1 opened the C3 source itself and found that the frozen
contract's grammar contradicts it on five points. No after-state had been measured when this
amendment was written: `scripts/meta_robots_audit.py` does not exist at the base or in the
working tree, so no case had been decided. The C3 predicate is unchanged
(`met <=> cases == decided and correct == cases and constants_failed == 4`); only the
grammar the cases must encode is corrected, and every correction cites the opened source.

Source opened by the L1 (receipt `w1/L1Sources/`, 2026-11-03):
`https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag`
HTTP 200, 208,191 B, sha256 `bf8adcc7cdf686bd7c85c007…`, stripped to
`w1/L1Sources/robots-meta-tag.txt`. The URL the wave spec handed `ScoutSources`
(`/crawling/docs/specs/robots-meta-tag`) answers **404** (47,506 B) — that path is dead and is
recorded as a round mistake.

## A1 — head placement: body tags are respected

Frozen text: "A matching element outside `<head>` is reported as
`meta_robots_tag_outside_head` and does **not** join the effective set."

Source (`robots-meta-tag.txt:239-241`): "Google Search doesn't enforce placement of meta robots
in the HTML head and will respect robots meta tags in the body section of an HTML document as
well."

**Corrected:** a matching element outside `<head>` **joins** the effective set exactly like a
head element, and is additionally reported as `meta_robots_tag_outside_head` — a lane-policy
hygiene finding (publisher convention: the tag belongs in the head, per the same page's
"Place the robots meta tag in the `<head>` section of a given page", `:208-209`), not a
correction of Google's behaviour.

## A2 — `unavailable_after` date forms

Frozen text: "must parse as RFC 3339 date-time (`YYYY-MM-DDTHH:MM:SS(Z|±HH:MM)`); invalid →
`meta_robots_invalid_value`", with a date-only value invalid.

Source (`:399-402`): "The date/time must be specified in a widely adopted format including, but
not limited to RFC 822, RFC 850, and ISO 8601." The page's own example (`:410`) is the
**date-only** value `2020-09-21`.

**Corrected:** the accepted grammar is the union of
(i) RFC 3339 `full-date` (`YYYY-MM-DD`) and `date-time` (`YYYY-MM-DDThh:mm:ss[.frac](Z|±hh:mm)`),
and (ii) an RFC 822-style `DD Mon YYYY HH:MM:SS ZONE` (the form the same page uses at `:265`).
A value parsing under neither is `meta_robots_invalid_value` and is ignored (lane policy, see
A4). RFC 850 is declared **not implemented** (limit, not a claim): a case that pins it would
flip the limit.

## A3 — `noarchive` / `nocache` / `nositelinkssearchbox` are ignored rules

Frozen text listed `noarchive` in the effective vocabulary.

Source (`:424-441`, "Reference of historical and other unused rules"): "The following rules
aren't used by Google Search and are ignored." — `noarchive`, `nocache`,
`nositelinkssearchbox`.

**Corrected:** these three tokens are **ignored**: they never enter the effective set and are
reported as `meta_robots_ignored_rule` (lane policy: a publisher should not rely on them).
`indexifembedded` (`:318-327`) is a valid, effective rule and is added to the vocabulary; it
has an effect only with `noindex`, which the tool records as the declared rule set (no
independent merge rule is claimed).

## A4 — ignored-on-invalid, not "invalid as effective"

Frozen text: an invalid value "never enters the effective set" (consistent) and is a finding
(kept).

Source for numerics (`:337-340`, `:371-373`): "This rule is ignored if no parseable [number] is
specified." and for dates (`:399-403`): "The rule is ignored if no valid date/time is
specified."

**Corrected (wording only):** the invalid value is *ignored for effect* (unchanged) and the
`meta_robots_invalid_value` finding is explicitly labelled the lane's reporting policy, never
a sourced consequence. Unknown content tokens are likewise ignored for effect and reported as
`meta_robots_unknown_directive` (lane policy); the source's "other values are ignored"
sentence (`:229-231`) is about the *name* attribute's user-agent tokens, not content tokens,
and must not be cited for this rule.

## A5 — `nosnippet` dominates numeric snippet limits

Frozen text defined the numeric merge only as a minimum.

Source (`:292-296`): "Conflicting robots rules: In the case of conflicting robots rules, the
more restrictive rule applies. For example, if a page has both `max-snippet:50` and `nosnippet`
rules, the `nosnippet` rule will apply."

**Corrected:** the effective set renders `nosnippet` and drops any numeric `max-snippet` /
`max-video-preview` value from the rendering; `max-snippet:0` is the source's stated equivalent
of `nosnippet` (`:347-349`) and renders as `nosnippet`; `-1` is the source's "no limit"
(`:351-354`) and loses to any non-negative value, entering the effective set only when no
non-negative value is declared. `max-image-preview` keeps the `none < standard < large` order.

## Case-family deltas (frozen families otherwise unchanged)

- g12 — a valid `unavailable_after`, now split: g12a RFC 3339 date-time, g12b RFC 3339
  date-only (`2020-09-21`), g12c RFC 822-style.
- g13 — an invalid date (e.g. `2020-13-40`) stays `invalid_value` and leaves the effective set.
- g19 — a matching meta **in the body**: the effective set now includes it, and the finding
  `meta_robots_tag_outside_head` is reported.
- g23 — `noarchive` + `nosnippet`: `noarchive` is ignored (`meta_robots_ignored_rule`),
  `nosnippet` is effective.
- g25 (new) — `nosnippet` + `max-snippet:50`: `nosnippet` wins; no numeric rendered.
- g26 (new) — `max-snippet:0` renders as `nosnippet`; `max-video-preview:-1` alone is
  `max-video-preview:-1` (no limit).
- g27 (new) — `indexifembedded` + `noindex`: both effective.

The matrix must therefore decide the amended families; the four constants are unchanged and
must still each fail at least one case.

## What this amendment does not change

The C3 predicate, the counter CLI, the exit alphabet (0/1/2/64), the finding-id closed list
plus the three new ids (`meta_robots_ignored_rule`, and A1's `meta_robots_tag_outside_head`
stays), the ≥20-case floor, the four constants, and the "no fetch, no browser, no write"
bounds. C1 and C2 are untouched.
