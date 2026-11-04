# Round-80 amendment 1 — `unavailable_after` date shapes and comma segmentation

Terms only. Written 2026-11-04 before any round-80 case was scored and before
`scripts/x_robots_tag_audit.py` was touched. It changes no round-79 case, oracle byte, receipt or
predicate; it extends the grammar of the same tool under this round's own case set.

Grounding. S452 (MDN, *X-Robots-Tag header*, tier B, retained at
`.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.raw`) states the `unavailable_after` value as a
date and shows, in its own example, an RFC 822 shaped value with a comma:
`unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT`. S453 (RFC 9110 §5.6.7, tier A, opened this
round) defines the HTTP-date as three shapes: IMF-fixdate, the obsolete RFC 850 shape, and asctime.
The round-79 grammar accepts the three shapes but splits the field value on ASCII comma before any
directive is parsed, so every comma-bearing shape is unreachable.

## A1 — the comma inside a date belongs to the date

A comma that immediately follows the leading weekday token of an `unavailable_after` value belongs
to that value and does not terminate the directive segment. Scope: only `unavailable_after` values
whose first token is a weekday name; every other comma keeps the round-79 rule (it terminates the
segment, and an empty segment is `xrt_empty_rule`).

Shape of the weekday tokens: `Mon` `Tue` `Wed` `Thu` `Fri` `Sat` `Sun` for IMF-fixdate, and
`Monday` … `Sunday` for the RFC 850 shape.

## A2 — asctime joins the accepted shapes

`unavailable_after` accepts a value matching, in addition to the three shapes already in the tool:

    (Mon|Tue|Wed|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)
    {1,2}[0-9]{1,2} hh:mm:ss YYYY

i.e. the RFC 9110 §5.6.7 asctime form, with the day-of-month field space-padded to width two (a
single space is also accepted). The accepted IMF-fixdate and RFC 850 shapes, and the ISO 8601 date
and date-time shapes already in the tool, are unchanged.

## A3 — no new finding id, no new exit code

The seven-id finding vocabulary and the 0/1/2/64 exit alphabet are unchanged. A value that matches
no accepted shape is `xrt_invalid_value` and is dropped, exactly as in round 79; a comma-bearing
value that fails its shape therefore yields `xrt_invalid_value` **only**, never
`xrt_unknown_directive`.

## A4 — no regression on the frozen round-79 set

The frozen round-79 matrix must keep printing `cases=31 correct=31 wrong=0 constants_failed=4/4
selftest_ok=true met=true` over the repaired tool. That run is a conjunct of this round's predicate,
not a separate claim.

## A5 — the tool's own selftest grows with the amendment

The tool's `--selftest` gains cases for the three accepted comma-bearing shapes, the asctime shape,
and the segment boundary after a comma-bearing value; the count is whatever the tool prints, and the
round's receipt is that printed line at the carried revision, re-derived by the C1 counter.
