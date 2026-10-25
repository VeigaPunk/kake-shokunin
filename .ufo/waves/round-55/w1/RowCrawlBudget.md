# RowCrawlBudget

Seat: RowCrawlBudget — C1 coverage-map calibration, one draft row for
`corpus/knowledge/crawl-budget-consequences.md`. Lane `kake-shokunin`, base
`fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`, round 2026-10-25. Read-only seat: no file
outside this report was written; `corpus/README.md` and the knowledge file are untouched.

## ROW:

```markdown
| Per-host crawl hygiene | `knowledge/crawl-budget-consequences.md` (S273, S274) | Two admitted Google sentences: a robots block does not make Google shift the spared crawl budget to other pages unless the capacity limit is already hit (S273); emergency backoff reduces crawl rate across the whole hostname (S274); status codes unadmitted; no lane property measured. |
```

Row shape checked against `## Coverage map` (`corpus/README.md:15-22`): 3 cells, header
`| Area | Entry | Coverage |`, Entry names the file in backticks as `knowledge/<file>` and
then copies the ids from the file's own `source:` lines (`:1` S273, `:2` S274). Area = 3
words. Coverage = 44 whitespace tokens, no `|`, does not start with `TBD`.

Mechanical constraints, run in Python against the file's own bytes (`corpus/knowledge/crawl-budget-consequences.md`):
`len(cov.split()) == 44`; shared 5+-letter words with H1 + first 1500 chars include
`across, admitted, already, backoff, block, budget, capacity, crawl, emergency, hostname,
limit, measured, other, pages, property, reduces, sentences, shift, spared, unless, whole`;
`'|' in cov == False`; `cov.startswith('TBD') == False`; cell split on `|` yields exactly 3
cells. These mirror the `thin`/`dangling` predicates of
`.ufo/waves/round-55/c55_readme_index.py`, but that counter was not run: it reads committed
bytes at a revision and this row exists only in this report.

## EVIDENCE:

1. `corpus/knowledge/crawl-budget-consequences.md:5` — the Area phrase is the file's own
   ground line: `ground: per-host crawl hygiene — budget consequence of robots and status codes` (12 units).
2. `:11` — the S273 claim the Coverage repeats:
   `Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit (S273)` (22 units).
   The same sentence's lead-in, `a block does not hand the spared fetches to other pages`
   (11 units), is where the word "spared" comes from; it is the file's paraphrase, not a
   verbatim source string (see the cross-check below).
3. `:13` — the S274 claim and the admission boundary behind "status codes unadmitted":
   `the backoff reduces your site's crawl rate across the whole hostname (S274)` (12 units);
   `The checked S274 quote does not itself name the status codes that trigger that backoff.` (15 units).
4. `:17` — the negative claim "no lane property measured":
   `No lane property was fetched or measured.` (7 units).

All four passages verified as raw substrings of the knowledge file with Python `in` (exact
match, ASCII text as written). No passage exceeds 25 whitespace-token units. Nothing inside
backticks was paraphrased; the Coverage cell paraphrases outside them, inside the admitted
scope.

Source-body cross-check, run (read-only) against the round-49 retained bodies
`.ufo/waves/round-49/sources/S273.txt` and `S274.txt`, all verified as raw substrings:

- `S273.txt`: `Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit` (21 units) — verbatim;
  the same page's rule line `Don't use robots.txt to temporarily reallocate crawl budget for other pages` (11 units) is what the file's "spared fetches" lead-in restates.
- `S274.txt`: `It reduces your site's crawl rate across the whole hostname` (10 units) — verbatim;
  `return a 500, 503, or 429 HTTP response status code instead of 200` (13 units) sits in the
  same list block, so the file's "same retained paragraph" statement holds.

Other read-only checks, run: `git show <base>:corpus/knowledge/crawl-budget-consequences.md | diff -`
against the worktree file → no output (committed bytes equal the file read here);
`git show <base>:corpus/README.md | grep -n crawl-budget` → rc=1 (the map at base has no row
for this file); `git ls-tree <base> corpus/knowledge/ | grep -c crawl-budget` → 1. The absence
matches `corpus/lessons/round-49-verifier-spotcheck.md:73` ("Coverage map `corpus/README.md`
has no `crawl-budget-consequences` row").

## RISKS:

- **No round tag is available from the file.** The header (`:1-5`) is
  `source:`/`source:`/`verified-at: 2026-10-24`/`recheck: 180d`/`ground:` — no round token —
  so the Area cell omits one. The r49 provenance is recorded outside the file
  (`corpus/lessons/round-49.md:12`, `round-49-verifier-spotcheck.md:68`); the row does not
  import that external fact.
- **"spared" is paraphrase, not source text.** The retained S273 body says "this newly
  available crawl budget"; "spared" comes from the file's own lead-in. The row keeps the
  file's word because the seat is calibrated to the file, and the difference is disclosed
  here rather than hidden.
- **The row cannot name the status codes.** `:13` says the checked S274 quote does not name
  them and those words "are not the admitted quote"; the retained body does carry 500/503/429
  in that block, but admitting them would exceed the entry, so the row says only "status codes
  unadmitted".
- **"backoff" is reported speech.** `:13` writes "the backoff reduces …"; the source verbatim
  is "It reduces …". The row mirrors the file and does not present the S274 sentence as a
  quoted string.
- **Scope limits are the file's own.** `:17` disclaims Search Console crawl stats
  (operator-gated), publishing (operator-owned) and Bing/Baidu budget models; the row claims
  none of them. The `:11` "unless … capacity limit" is a condition, not a general rule about
  blocking cost.
- **Undated "this round".** `:9` says "Two Google documents opened this round" with no round
  number; only `verified-at: 2026-10-24` dates the entry, so the row makes no recency claim.
- **Retained bodies live outside the file.** `:13` refers to "the same retained paragraph",
  but the body is in `.ufo/waves/round-49/sources/`, not in the knowledge file; the row does
  not pretend the paragraph is quoted inside it.
- **Freshness.** `recheck: 180d` from 2026-10-24 puts a recheck due around 2027-04-22. No
  recheck was performed in this seat; the file shows no later verification.
- **Unrun gates.** `c55_readme_index.py` was not executed (row is not in committed bytes); no
  README edit, no index write, no git or jj mutation, no subagent. No tool was installed or
  upgraded in this seat (no `pacman`, no `uv tool`, no binary download).
- No inaccuracy was found in the file's own statements; the items above are row-scope and
  format limits plus one disclosed paraphrase, not defects of the entry.

VERDICT: one 44-token, pipe-free coverage-map row drafted for `knowledge/crawl-budget-consequences.md`, every clause grounded in four ≤25-unit raw file passages (lines 5, 11, 13, 17) and cross-checked against the retained S273/S274 bodies; no file edited and no counter run.
