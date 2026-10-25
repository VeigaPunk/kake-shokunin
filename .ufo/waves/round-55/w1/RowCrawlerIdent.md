# RowCrawlerIdent

Claim C1 (coverage-map calibration). Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`, round 55,
read at HEAD `143e592938967ac6a1eb7d9e6f7055bde5b59ed4` (base `fcaf4b85…` is an ancestor; two wave
commits on top). Sources read: `corpus/knowledge/crawler-identity.md` (whole file, 73 lines /
4 315 chars) and `corpus/README.md:1-83` (header + `## Coverage map` header and 3 of its existing
rows for the 3-cell format). Nothing edited outside this report.

ROW:

```markdown
| Crawler identity (Googlebot subtypes) | `knowledge/crawler-identity.md` (S263) | Googlebot names two crawlers, Smartphone and Desktop; the HTTP user-agent header identifies the subtype, and both types obey the same robots.txt product token; it also lists what the entry does not establish. |
```

Constraint check (run, output observed): Coverage = 32 words (limit 10–45); contains no `|`;
does not start with `TBD`; shares 5+-letter words `crawlers`, `googlebot`, `smartphone`, `desktop`,
`header`, `subtype`, `product`, `token` with the file's H1 + first 1 500 chars; row has exactly
4 `|` characters, i.e. 3 cells; Area = 4 words (limit 8); Entry = backticked
`knowledge/crawler-identity.md` followed by `(S263)`, the id copied from the file's `source:` line.
No `all`/`every`/`complete` claim and no count appears in the Coverage cell (the file's only counts,
15/3/2/10/7 quotations, are deliberately not carried over). A `grep` of `corpus/README.md` for
`crawler-identity`, `S263`, `Googlebot` and `crawler ident` returned no match, so the row is new
(exit 1, no output).

EVIDENCE:

- `corpus/knowledge/crawler-identity.md:10,16,18` — the naming claim rests on
  `"Googlebot is the generic name for two types of"`, plus
  `"Googlebot Smartphone : a mobile crawler that simulates a user on a mobile device"` and
  `"Googlebot Desktop : a desktop crawler that simulates a user on desktop"` (each ≤ 25 words).
- `corpus/knowledge/crawler-identity.md:22-23` — the header claim rests on
  `"You can identify the subtype of Googlebot by looking at the HTTP user-agent request header in the request"` (18 words).
- `corpus/knowledge/crawler-identity.md:27` — the shared-token claim rests on
  `"both crawler types obey the same product token (user agent token) in robots.txt"` (13 words).
- `corpus/knowledge/crawler-identity.md:46` — the "does not establish" clause rests on the section
  heading `## What this entry does not establish`, whose four bullets scope out crawl rate,
  scheduling, URL treatment, non-Google bots and per-property identity (`:48-55`).

RISKS:

- **Quotation class.** The row's wording is prose, but any downstream use of the three quoted
  passages above must not be read as page bytes: `:59-62` states only the first quotation is an
  exact raw substring of the retained body, and `:70-72` measures 3 raw / 2 collapse-only / 10
  markup-removal out of 15. The subtype lines and the robots-token line are renderings, so the row
  cannot be cited as proof that those exact strings occur in S263.html.
- **Not an observation.** `:52-55` says no operator-owned property was fetched and the entry is a
  documentation reading; the row therefore does not say anything about how a crawler identifies
  itself on any lane property, and I did not add such a claim.
- **Staleness / no re-fetch this round.** `verified-at: 2026-10-24`, `recheck: 180d`, page doc rev
  "Last updated 2026-02-03 UTC". S263 is not among this round's retained bodies
  (`sources/` holds only S372, S373, S418), so the file was not re-verified here and the row
  inherits the file's own 2026-10-24 date, not the round date.
- **Round tag omitted on purpose.** The file's header block (`:1-4`: source, verified-at, recheck,
  ground) carries no round tag; `(round-51 correction)` appears only in a section heading (`:57`).
  I did not invent an `(r51)` tag for the Area cell; if the map's convention wants one, the only
  defensible form is `(round-51 correction)` sourced from `:57`.
- **Scope the row cannot carry.** `:39-44` cites S011, S095 and S096 (robots reading, robots
  interpretation, `robotstxt` matcher) as neighbours; enumerating them would overstate a one-file
  row, so the Entry cell carries only S263.
- **Truncated digest.** `:61-62` gives the retained-body digest as `6afbdc82…`; the row asserts no
  digest, since the full value is not in the file.
- **Format note, not a defect.** Existing README rows are grouped by theme rather than
  alphabetised, and several carry prose caveats inside the Coverage cell; the new row is a plain
  one-liner and its placement in the map is the planner's call, not mine.
- Checks I did not run: no lint, build or freshness sweep; no comparison of the file against the
  live developers.google.com page (out of scope, and it would need a fetch this round does not
  retain). No tool was installed or upgraded.

VERDICT: One new, format-conformant coverage-map row for `knowledge/crawler-identity.md` drafted and constraint-checked; no file edited.
