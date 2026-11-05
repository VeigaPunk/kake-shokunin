# RFC 5861 errata inventory — ScoutRfc5861 (round 98 w1, 2026-11-05)

Evidence: one GET of https://www.rfc-editor.org/errata_search.php?rfc=5861 answered HTTP/2 302 to
https://errata.rfc-editor.org/search/?rfc_number=5861 then HTTP/2 200, 17788 bytes, sha256
9603a690cfa9b5b1c7c0f9d2a52c2b5b98f38a90e7c14e76e5dd90e0f3ab8ce9 (full receipt: fetch.txt).
Body retained here as errata-5861.html. All line numbers below are body line numbers of that
retained file (1-based, as printed by grep -n / ranged reads).

## Result: 2 errata, both inside the single status card "Verified (2)" (line 108)

| EID | status | type | section | evidence lines in errata-5861.html |
|---|---|---|---|---|
| 2255 | Verified | Editorial | 3 (pg.3) | record header line 129; status badge line 135; Type field line 138, Editorial badge line 141; "Section 3, pg.3 says:" line 174; notes pre ending line 198 |
| 2256 | Verified | Editorial | 4 (pg.4) | record header line 205; status badge line 211; Type field line 214, Editorial badge line 217; "Section 4, pg.4 says:" line 250; cf. EID=2255 note line 274 |

Card census: the page carries exactly one status-category card, "Verified (2)" at line 108; there
is no Reported, "Held for Document Update" or Rejected card. A grep of every card-header in the
body returns only lines 107, 116, 128 and 204 — the category card, the RFC header card, and the
two erratum record cards. Total inventory: 2 errata. No erratum targets §3.1, §4.1, §5 or §6.

## What the errata change — nothing C2's decision text relies on

Both records propose the same editorial rewording of the sentence after the stale-if-error note
("...visibly stale when sent (i.e., have a non-zero Age header and a warning header...)"):

- change: "Age header" → "Age header field" and "warning header" → "Warning header field"
  (standard-terminology consistency and header-name capitalization only);
- EID 2255 notes (pre ending line 198): "(These issues recur in the last paragraph of Section 4.)";
- EID 2256 notes (line 274): "(Similar issues as for section 3 -- cf. EID=2255.)".

Neither erratum touches: the §3 serving window ("up to the indicated number of seconds",
sources/rfc5861.txt lines 105-108), the §4 staleness bound ("more stale than the indicated
amount", lines 180-182), the §4 error definition (500, 502, 503, 504; lines 184-185), or the §4
request/response scope sentence (lines 175-178). Located quotes with line numbers: quotes.md.
Both types are Editorial; there is no Technical, and no Verified/Reported erratum needs holding
against the stale-serving contract's reading of RFC 5861 as of this fetch.
