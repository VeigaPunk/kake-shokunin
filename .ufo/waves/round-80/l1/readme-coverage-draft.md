## Coverage — round 80 (2026-11-04)

| Area | Entry | Coverage |
|---|---|---|
| HTTP-date grammar for `unavailable_after` (r80) | `knowledge/http-date-grammar.md` + `scripts/x_robots_tag_audit.py` + `.ufo/waves/round-80/cases` (S453; S452 re-opened; S433's field-line ground) | The three RFC 9110 `HTTP-date` formats with their ABNF, which of them carry a comma and where, the §5.5 sentence on a comma that is data inside a member, and the lane's resulting segmentation rule; the tool now decides IMF-fixdate, RFC 850 and asctime values that a comma-first splitter destroyed, with the frozen 31-case round-79 set unchanged. Not covered: calendar validity, the RFC 850 50-year window, per-bot effective resolution, or any crawler outcome. |

Sources opened this round: S453 (RFC 9110 §5.6.7, tier A, new row) and S452 (MDN X-Robots-Tag,
re-opened; raw bytes identical to round 79). Registry 190 → 191 rows; census exit 0 with 19 → 20
`W04` lines (the S453 row is a second scope on RFC 9110's URL, the same pattern as S010/S028/S033/
S088/S433).

Frontier line to append to §Frontier: the HTTP-date grammar moves from frontier to core for the
`X-Robots-Tag` carrier; per-bot effective resolution, meta+header conflicts and header inheritance
across redirect hops stay frontier.
