# RowRedirectRules

Seat: C1 coverage-map calibration, one drafted row for
`corpus/knowledge/redirect-rewrite-rules.md` (56 lines, unmodified vs HEAD,
last touched by `ee43e66` "round-46: C1 redirect/rewrite audit + C2
citation-hygiene gate …"). No file was edited; the only write is this report.

ROW:

```
| Redirect/rewrite rule semantics (r46) | `knowledge/redirect-rewrite-rules.md` (S050, S135) | Render and Cloudflare Pages redirect/rewrite rule semantics: resource precedence, first-match order, dashboard versus `_redirects` placement, Cloudflare's status codes 301, 302, 303, 307, 308 with 302 default, splat and placeholder expansion; manifest fields declaring which precedence an offline audit applies. No live serving claim. |
```

Insertion point: immediately after the last existing row of `## Coverage map`
(`| Field performance (r28) | …`, `corpus/README.md:45`), before the blank line
that precedes `## Known gaps` (`corpus/README.md:47`). No existing row names
this file (`grep -c redirect-rewrite-rules corpus/README.md` → 0), so the new
row is the first naming row and the counter's `unindexed` term clears.

Row-shape facts measured on the drafted line itself (no repo write): 3 cells;
coverage cell 43 whitespace tokens, no `|`, does not start with `TBD`; the
backticked entry path is the only extension-bearing backticked token in the
line; shared 5+-letter words with the H1/first-1500-chars set are
`audit, cloudflare, offline, pages, redirect, redirects, render, resource,
rewrite, semantics`.

EVIDENCE:

- `corpus/knowledge/redirect-rewrite-rules.md:15` — "Rules are dashboard-defined per site." (5 words; grounds the cell's dashboard-vs-`_redirects` placement clause).
- `corpus/knowledge/redirect-rewrite-rules.md:18-22` — "If a resource exists at the path, serve it — no rule is applied" (14) and "Apply the first matching rule (starting from the top of the list)" (12); grounds the cell's resource-precedence and first-match clauses.
- `corpus/knowledge/redirect-rewrite-rules.md:35,40-42` — "Rules live in a plain-text `_redirects` file in the static asset directory." (12) and "Redirects are always followed, regardless of whether or not an asset" (11) plus "an existing asset does NOT shadow a Cloudflare redirect rule." (10); grounds the Cloudflare half and its inverse precedence.
- `corpus/knowledge/redirect-rewrite-rules.md:43-45,49-51` — "Status codes 301, 302, 303, 307, 308 are supported; 302 is the default when" (14), "Splats (`/blog/*` → `https://blog.my.domain/:splat`)" (4), "An offline expectation audit must declare which precedence semantics it" (10), "the manifest field `resourcePrecedence` (true = Render, false =" (9); grounds the status set, splat/placeholder clause and the manifest-fields clause.
- Round tag and no-live-claim: `:10` "(`scripts/redirect_audit.py`, round 46)" is the only round marker in the file; `:53-54` carry the disclaimer across a line wrap — "Nothing here is a live" then "serving claim: the audit reads a local manifest of rules, resources and" — so the cell restates it as unquoted prose (its final sentence, No live serving claim.) instead of quoting a string that no single line contains.

All quoted passages above were verified as single-occurrence raw substrings of
the file body (python `str.count` → 1 each) and are ≤ 14 units (whitespace
tokens; no CJK present, so one unit per token).

RISKS:

- **Round tag provenance is the weak point.** The frontmatter block (`:3-7`)
  carries `source:`, `verified-at:`, `recheck:` and no round field; `(r46)` is
  derived from the body sentence at `:10` and from commit `ee43e66`. If the
  index owner requires the tag to come from the header block, the Area cell
  should drop to `Redirect/rewrite rule semantics` with no tag.
- **Overlap with an existing row.** `corpus/README.md:281` (`| Render static
  sites (r30) | knowledge/render-static-sites.md (S049–S052) | …`) already
  states Render's "redirect and rewrite rules apply only where no resource
  exists at the path, first matching rule wins, otherwise 404". The new row
  restates that Render half; its non-duplicated content is Cloudflare's inverse
  precedence and the manifest declaration fields. Two rows now describe
  overlapping Render behavior and can drift independently.
- **What the row must not say.** The file states no counts and no live
  measurement, and for Render only "the doc's table names a 301 Moved
  Permanently response" (`:25-26`); the five-code status set is Cloudflare's
  alone (`:43`). The cell therefore attributes the status list to Cloudflare
  and does not generalize it to Render, and makes no "all"/"every" claim.
- **Staleness inside the file.** `:5` reads "verified-at: 2026-10-24 (S135
  fresh GET this round; S050 retained text re-read)" — "this round" is
  round-46 relative and reads stale at round 55, and the S050 half rests on a
  retained round-30 text (`.ufo/waves/round-30/sources/S050.txt` per
  `corpus/lessons/round-46.md:52-54`), not a round-55 GET. Recheck is due
  2027-01-22 (90d, `:7`). None of this is in the row, by design.
- **Unrun check (reported as unrun).** The frozen C1 counter
  (`python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision
  <rev>`) was **not** run against a README containing this row — no seat may
  edit `corpus/README.md`, so no revision exists with the row appended. What
  was run instead, read-only: importing the counter module and applying its own
  `words()` and `strip('|').split('|')` cell logic plus its
  `knowledge/<basename>(?![A-Za-z0-9_.-])` pattern to the drafted line. No
  `unindexed`/`thin`/`dangling` totals were measured.
- **Repo state observed (read-only).** HEAD is
  `143e592938967ac6a1eb7d9e6f7055bde5b59ed4` ("round-55: W1 spec and dispatch,
  pre-append registry mirror pin"), two commits ahead of the contract base
  `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`, which is an ancestor; worktree
  diff for the knowledge file vs HEAD is empty. `scripts/redirect_audit.py`
  cited by the file exists and is tracked (25 452 bytes), so a future row
  citing it would not dangle; this row does not cite it.

VERDICT: One row drafted for `knowledge/redirect-rewrite-rules.md` — 43-token coverage cell, 3 cells, no pipe/TBD, 10 shared 5+-letter words, all six substantive clauses traceable to cited single-line passages; counter itself left unrun (README unedited by seat).
