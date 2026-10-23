# Round 40 — sitemap audit repairs (C1) and round-39 routed defects

author: kake L1, round 40 attempt 1 (KakeR40)

Claim and frozen rule: `SCORECARD.md` "Round 40 — C1 declared". Base `f171c58b`. Outside check of
round 39: `corpus/lessons/round-39-verifier-spotcheck.md` (not edited here).

## Gate

Sources opened this round by the L1 (retained under `.ufo/waves/round-40/sources/`, sums in
`SHA256SUMS` there; quotes found in the fetched HTML with markup stripped).

| Row | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S110 | https://www.w3.org/TR/xml/ | 2026-10-23T08:28:47Z, HTTP 200 | "When an XML 1.0 processor encounters a document that specifies a 1.x version number other than '1.0', it will process it as a 1.0 document." (§2.8, Note after [26]) | admit, A, spec, mined; also §2.2 "[2] Char ::= #x9 \| #xA \| #xD \| [#x20-#xD7FF] \| …" (no #x0) |
| S111 | https://docs.python.org/3/library/urllib.parse.html | 2026-10-23T08:28:47Z, HTTP 200 | "leading C0 control and space characters are stripped from the URL. \n, \r and tab \t characters are removed from the URL at any position." (`urlsplit`) | admit, A, docs, mined |
| S112 | https://www.w3.org/TR/xml-names/ | 2026-10-23T08:29:16Z, HTTP 200, sha256 = S106's | "The comparison is case-sensitive, and no %-escaping is done or undone." (§2.3); `ignor` occurs 0 times in the page (and 0 times in S102) | admit, supersedes S106 (routed defect 1) |
| S113 | https://www.w3.org/TR/xmlschema11-2/ | 2026-10-23T08:29:16Z, HTTP 200, sha256 = S107's | "dateTimeLexicalRep ::= yearFrag '-' monthFrag '-' dayFrag 'T' ((hourFrag ':' minuteFrag ':' secondFrag) \| endOfDayFrag) timezoneFrag?" (§3.3.7.2 [16]); [18] dateLexicalRep has no time part | admit, supersedes S107 (routed defect 1) |
| S114 | https://yandex.com/support/webmaster/en/controlling-robot/sitemap | 2026-10-23T08:29:16Z, HTTP 200, 223,735 bytes | "The total character limit is 2048. 1024 Characters are intended for the site’s domain name" (U+2019) | admit, supersedes S109 (routed defect 1) |

Row changes: S110–S114 added. No `status`, `recheck` or `used-by` change to an existing row
(S106, S107, S109 stay as written; the superseding rows carry the corrections, CORPUS.md §SOURCES
rule 2).

Rejects this round (recorded before data):
- **Rejected: routed defect 2's "fix D1" (XML 1.x accepted).** Reason: S110 §2.8 — an XML 1.0
  processor processes a `1.x` declaration as a 1.0 document, so `version="1.1"` with 1.0 content is
  well-formed XML 1.0 and sentence 8 holds; `version="2.0"` already gives `xml_malformed`
  (`.ufo/waves/round-40/l1-probe.py`). The tool is not changed for D1.
- **Not changed: D3** (`doctype_present` over a malformed remainder). Reason: sentence 9 is the lane's
  safety reading and the round-39 build declared this precedence; the contract does not order (b)'s two
  sentences, and changing it would be a contract change, not a repair.
