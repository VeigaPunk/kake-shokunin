# Round 39 — sitemap file audit (C1 capability move)

author: kake L1, round 39 attempt 2 (KakeR39A2)

Claim and frozen rule: `SCORECARD.md` "Round 39 — C1 declared". Contract:
`.ufo/waves/round-39/c1-contract.md`. Attempt 1 landed nothing; its leftovers were moved out of the
lane unread (`/fast/scratch/hyaku/kake-r39a2/attempt1-leftovers/`).

## Gate

Sources opened this round by the L1 (retained under `.ufo/waves/round-39/sources/`, sums in
`SHA256SUMS` there).

| Row | URL | Accessed | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S102 | https://www.sitemaps.org/protocol.html | 2026-10-23T05:28:42Z, HTTP 200 | "each Sitemap file that you provide must have no more than 50,000 URLs and must be no larger than 50MB (52,428,800 bytes)" (`sitemaps-protocol.txt:176-177`) | admit, A, spec, mined; supersedes S012 (wider scope) |
| S103 | https://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd; …/siteindex.xsd | 2026-10-23T05:29:28Z, HTTP 200 | "The value for this element is a number between 0.0 and 1.0 where 0.0 identifies the lowest priority page(s)." (`sitemap.xsd`, tPriority documentation) | admit, A, spec, mined |
| S104 | https://www.w3.org/TR/NOTE-datetime | 2026-10-23T05:29:28Z, HTTP 200 | "YYYY-MM-DDThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00)" (`w3c-datetime.txt`, Formats) | admit, A, spec, mined |

Readings where the sources disagree (contract "lane reading" sentences): `loc` length — S102
"This value must be less than 2,048 characters" versus S103 `<xsd:maxLength value="2048"/>`; the
contract follows S102. `lastmod` — S102 and S103's documentation name the W3C Datetime format,
S103's type is `xsd:date` ∪ `xsd:dateTime`, which allows no time zone; the contract requires a
complete date and a TZD with any time (S104 levels 3–6).

Row changes: S012 `status` mined → mined (unchanged; S102 supersedes its scope, recorded in S102's
`teaches`). No other row touched.
