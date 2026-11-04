[r80-correction 2026-11-04] The `X-Robots-Tag` paragraph above is historical for its date. Round 80 widens
that channel's instrument: `scripts/x_robots_tag_audit.py` now reads the `unavailable_after` date value
under the three RFC 9110 `HTTP-date` formats (IMF-fixdate, the obsolete RFC 850 shape and asctime) as well
as ISO 8601, and a comma that follows the leading weekday token of such a value no longer terminates the
directive segment — the round-79 grammar split every field value on commas first, which made S452's own
example undecidable. Terms: `.ufo/waves/round-80/amendments/amendment-1.md`; ground:
`corpus/knowledge/http-date-grammar.md` (S453, S452); case set `.ufo/waves/round-80/cases` with the
frozen round-79 matrix unchanged. Calendar validity, the RFC 850 50-year window, per-bot effective
resolution and header inheritance across redirect hops remain out of scope, and no crawler behaviour or
live property state is claimed.
