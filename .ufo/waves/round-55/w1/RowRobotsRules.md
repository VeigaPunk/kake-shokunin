# RowRobotsRules

Claim C1 (coverage-map calibration). Drafted one coverage-map row for
`corpus/knowledge/robots-txt-rules.md`. The knowledge file and README were read only; no file was
edited, no git/jj state touched, no tool installed (none needed).

## ROW:

```markdown
| Offline robots.txt expectation rules | `knowledge/robots-txt-rules.md` (S011, S095, S096, S034, S098, S099, S100) | RFC 9309 robots.txt rules and this lane's offline expectation readings: access-result status handling, line and group parsing, rule matching with URL normalization, plus round-38 amendments (h) JSON numbers, (i) URL characters, (k) implicit /robots.txt allow. |
```

## EVIDENCE:

All line numbers are `corpus/knowledge/robots-txt-rules.md`. Every passage below was checked as a
whitespace-token unit count <= 25 and a raw substring (python `in`, both whole-body and the named
line); all passages are ASCII.

- `:5` — H1, the Area's source: "Offline robots.txt rules" (3 units). The front matter `:1` names
  the first source as S011 RFC 9309, which is what the Coverage cell's opening clause rests on.
- `:19` — status handling: "When the robots file is successfully retrieved, a crawler MUST follow
  its parseable rules" (14 units). The same line continues to the 4xx-allow and
  unreachable-disallow cases, which is the "access-result status handling" clause.
- `:33` — line and group parsing: "`user-agent`, `allow` and `disallow` are the records used here"
  (9 units). Section `## Read lines and groups` (`:27`) is the clause's source; `:29` gives the
  UTF-8 / 500 KiB parsing statements.
- `:55` and `:59` — matching and normalization: "choose the longest matching normalized rule value
  measured in octets" (10 units) and "construct the comparison target from the URL path" (8 units).
- `:87` — round-38 amendments: "Lane readings of the offline audit, added in round 38" (10 units);
  `:88` names the three rules as (h), (i), (k); their headings are `:91` "(h) JSON numbers, lane
  reading.", `:102` "(i) URL characters, lane reading." and `:113` "(k) Implicit `/robots.txt` allow
  on the normalized path, lane reading."

## RISKS:

- **No round tag in the file's own header.** The front matter (`:1`–`:3`) and the H1 (`:5`) carry no
  round tag; the only round label is the section heading `:85`, "## Round 38 amendments — lane
  readings (appended)", which governs the appended tail only. The Area therefore omits a round tag
  rather than attributing r38 to the whole file (the r37 core is the C1 contract readings).
- **Front-matter provenance is narrower than the source list.** `verified-at: 2026-10-23` names only
  "S011, S095 and S096 retained round-37 retrievals; `.ufo/waves/round-37/sources/receipts.json`"
  (that receipts file holds keys S011, S095, S096, S097). S034 and S098–S100 are dated 2026-10-23
  only inside `:87`–`:89`. No retained body for S098/S099/S100 exists under `.ufo` (a `find .ufo`
  for `S098*`, `S099*`, `S100*` returned nothing); S034's retained text is the round-26 copy at
  `.ufo/waves/round-26/fetched/text/S034-1.txt`. The row states nothing about retained-body
  verification of those four.
- **Duplicate document across two source ids.** `corpus/SOURCES.md` rows S011 and S099 are the same
  RFC 9309 URL (`https://www.rfc-editor.org/rfc/rfc9309.html`). The Entry cell copies the id list
  verbatim from `:1`, so it necessarily contains that duplicate document. The same RFC is cited as
  S011 at `:57` and as S099 at `:114`.
- **Version mismatch, not a contradiction.** `corpus/SOURCES.md` S100 is "Python 3.15.1
  documentation: json", while rule (h) records a measurement "on Python 3.14.8" (`:100`). The row
  says nothing about versions or measurements.
- **What the row cannot say.** It cannot claim C1/C2 admission (the file's own Evidence boundary at
  `:83` says the C1 rules are a public lane contract, "not evidence that an implementation passed
  any check"); cannot claim crawler behavior (`:77`–`:81` infer none for a particular crawler);
  cannot claim live fetch, redirect or caching (`:77`); cannot claim sitemap handling; and it omits
  the Google-difference paragraphs (`:25` says those details "are not substituted for the lane
  reading"; `:118`–`:121` on the implicit allow). It also does not itemize the individual line,
  group or percent-encoding rules.
- **Staleness.** `recheck: 90d` from `verified-at: 2026-10-23` falls due 2027-01-21, so not due at
  the round date 2026-10-25. Source anchors were not re-opened by this seat; no claim of anchor
  freshness is made.
- **Placement.** The `## Coverage map` table (`corpus/README.md:15`) runs to `:45`
  (`| Field performance (r28) | ...`), with `## Known gaps` at `:47`; the row appends after `:45`.
  No table row for this knowledge file existed — `:370`–`:371` are `scripts/robots_audit.py` rows and
  `:375` names the knowledge file only in prose.
- **Format checks run (this seat).** Coverage = 35 units (10–45 required); contains no `|`; does not
  start with `TBD`; shares "offline", "expectation", "robots.txt" and "rules" with the H1 plus first
  1500 characters; contains none of `all`/`every`/`complete` as a word; the 3-cell form
  `| Area | Entry | Coverage |` and the backticked `knowledge/<file>` Entry form match the map's
  existing rows.

VERDICT: One coverage-map row drafted for `knowledge/robots-txt-rules.md` (35-unit Coverage, all quoted passages verified as <=25-unit raw substrings); file left unedited; provenance gaps in the file's own front matter recorded as risks.
