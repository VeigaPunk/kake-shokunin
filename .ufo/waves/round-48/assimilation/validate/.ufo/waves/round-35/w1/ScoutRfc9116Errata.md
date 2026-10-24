# ScoutRfc9116Errata — errata and status of RFC 9116 (freshness of retained row S078)

Sealed keys untouched: nothing under `/fast/scratch/hyaku/kake-r35/sealed/` was read, listed, stat'ed or grepped.

## Question attacked
S078 (RFC 9116, the security.txt format) is the backbone of the pending C2 entry. If the canonical
text had erratum-level changes, an update or an obsoletion since capture, a publisher rule stated
from it (field names, `Expires`, `/.well-known/` location, `text/plain` media type) could be stale.

## Commands run (all GET, no browser, no auth, no challenge solving)
1. `curl -sS -L --max-time 60 -o errata-rfc9116.html https://www.rfc-editor.org/errata/rfc9116` — exit 0
2. `curl -sS -L --max-time 60 -o datatracker-rfc9116.html https://datatracker.ietf.org/doc/rfc9116/` — exit 0
3. Repeat GET of both with `-o /dev/null -w '%{http_code} %{size_download}'` — exit 0,
   `200 25394` and `200 80220` (bodies byte-identical to the first fetch, so the pages are stable)
4. HTML→text extraction of both bodies (`python3`, strip script/style/tags, unescape) — exit 0
5. `grep -c` for `Updated by|Obsoleted by|Updates:|Obsoletes:` on the datatracker body — exit 1, count 0
6. Grounding reads of `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-35/sources/S078.txt`

Fetched at 2026-10-22T22:26:03Z. Bodies and derived text stay in the sandbox:
`/fast/scratch/hyaku/kake-r35/w1/ScoutRfc9116Errata/` (`errata-rfc9116.html` sha256
`76591a42ee973f4143bf86042d9f30edb6c0905ef0c2f5344bee4f73ccae01bf`; `datatracker-rfc9116.html`
sha256 `edd0871b5f242d799a2be176c1c721a03f4560e4cb577e5469871bcdce98686c`;
receipt `receipt-rfc9116-errata.json`).

## Errata on RFC 9116 — 3 total (1 Verified, 2 Reported, 0 Held for Document Update, 0 Rejected)
Page headings literally `Verified (1)` and `Reported (2)` (errata-rfc9116.txt:45, :86).
All three carry `Source of RFC: IETF - NON WORKING GROUP`.

| id | section | type | status | reported | one-line summary |
|---|---|---|---|---|---|
| 6946 | 4 (ABNF comment) | Editorial | **Verified** (verified 2022-04-28) | 2022-04-28 | Comment cross-reference `Section 3.5.3` → `Section 2.5.3`, the section that actually defines Contact priority ordering |
| 7264 | 2.5.5 | Technical | **Reported** | 2022-12-10 | Example `Expires: 2021-12-31T18:37:07z` uses lowercase `z`; ISO 8601 zulu indicator must be uppercase `Z` |
| 7743 | 4 vs 2.2 | Technical | **Reported** | 2023-12-30 | ABNF `CRLF = CR LF` contradicts Section 2.2, which allows CRLF **or** LF; proposes `CRLF = [CR] LF` |

Located quote, errata page (errata-rfc9116.txt:85): "Reference to Section 2.5.3 (describing ordering
semantics of the Contact field) mistakenly given in ABNF comments as 'Section 3.5.3'". Erratum 6946's
basis is real and reproducible in the retained source: S078's ABNF carries `; priority (see Section
3.5.3)` while no Section 3.5.3 exists (the string `3.5.3` occurs exactly once in S078), and the
ordering rule lives in `2.5.3. Contact`. Erratum 7264's basis is likewise real: S078 Section 2.5.5's
example ends `Expires: 2021-12-31T18:37:07z`. Each Reported erratum in one sentence: 7264 = example
casing of the `Expires` value; 7743 = ABNF line separator not matching the normative Section 2.2 LF
allowance.

## Is RFC 9116 updated or obsoleted? No.
Datatracker metadata block, `datatracker-rfc9116.txt:94-99` — `RFC` / `- Informational` /
`(April 2022)` / `Errata` / `Was` / `draft-foudil-securitytxt`. No `Updates`, `Updated by`,
`Obsoletes` or `Obsoleted by` row exists on the page (`grep -c` = 0 for all four labels; the only
`related` hits are in the RFC body text). Status-of-memo quote, `datatracker-rfc9116.txt:145`:
"This document is not an Internet Standards Track specification; it is published for informational
purposes." `Last updated 2026-05-20` (`:105-106`) is page bookkeeping, not a document revision. So the
canonical text has been frozen since April 2022 apart from one editorial verified erratum, newest
erratum activity Dec 2023. [INFERENCE] Absence of update/obsolete rows on the
datatracker document page is a reliable negative for RFC-level relations, though it does not by itself
prove no revision draft exists elsewhere; nothing I was allowed to open suggests one.

## Publisher-facing change? **No.**
Rules a publisher follows, quoted from S078, and errata coverage:
- Location — Section 3: "For web-based services, organizations MUST place the \"security.txt\" file
  under the \"/.well-known/\" path ... The file MUST be accessed via HTTP 1.0 or a higher version, and
  the file access MUST use the \"https\" scheme." No erratum touches this.
- Media type — Section 3: "It MUST have a Content-Type of \"text/plain\" with the default charset
  parameter set to \"utf-8\"." No erratum touches this.
- Field names — Section 2.5 defines Acknowledgments, Canonical, Contact, Encryption, Expires, Hiring,
  Policy, Preferred-Languages. No erratum renames or adds a field.
- Expires — Section 2.5.5: value is RFC 3339 / ISO 8601, "RECOMMENDED that the value of this field be
  less than a year into the future", "MUST always be present and MUST NOT appear more than once".
  7264 corrects only the *example* casing, not this normative sentence; 2.2 already makes CRLF-or-LF
  normative, so 7743 changes no publisher obligation either.
- 6946 is a comment-only cross-reference fix in the ABNF block.

Practical guidance for C2: quote the normative sentences, not the Section 2.5.5 example verbatim; if
the example must be quoted, use uppercase `Z` and do not cite 7264 or 7743 as authoritative — both are
status Reported, not Verified. RFC 9116 itself is safe to cite as current.

## Not verified / remaining unknowns
- Did not open the RFC-Editor `inline-errata` annotated copy, `errata_search.php?rfc=9116`, RFC 9116's
  txt/pdf/xml formats, or any draft that might revise it — out of the two named URLs for this seat.
  The errata page and datatracker page were treated as authoritative for counts and relations. No file
  was written outside this report in the lane; no tool was installed or updated (none needed).
