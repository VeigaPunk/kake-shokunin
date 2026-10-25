# ExecRowsGoogleA

ATTACK: the three coverage-map rows added at revision `a7a548e102b71bd16b0a6ddafa469393a2c98b69` in
`corpus/README.md` §Coverage map — line 50 (`knowledge/canonical-selection.md`, S262), line 51
(`knowledge/crawl-budget-consequences.md`, S273 S274), line 53 (`knowledge/crawler-identity.md`, S263) — claim C1.
All bytes read via `git -C …/kake-shokunin show a7a548e…:<path>`; nothing written except this report.

## Method (commands run)

- Row extraction: `python3 - <<PY` over `git show a7a548e…:corpus/README.md`, filtering lines that start
  `|`, contain `` `knowledge/<file>` ``, and have exactly 4 pipes (coverage-map table shape).
  Observed: canonical-selection → `[50]`, crawler-identity → `[53]`, crawl-budget-consequences → `[51]`;
  no second 4-pipe row for any of the three files. (The same files also appear once each in the
  *Frontier ground map* sub-table, 5-pipe rows 85/86/89, which carry no coverage cell — different section,
  not a duplicate coverage row.)
- `git diff fcaf4b85… a7a548e… -- corpus/README.md | grep -E '^[+-]\|'` → all three rows appear as `+` lines,
  so each is genuinely added in this commit (README diff: 84 insertions, 0 deletions).
- Entry-file stability: `git diff --quiet fcaf4b85… a7a548e… -- corpus/knowledge/{canonical-selection,crawler-identity,crawl-budget-consequences}.md`
  → exit 0, printed `UNCHANGED base..rev`. No STALE window can exist: the prose the rows describe did not move.
- Registry: `git show a7a548e…:corpus/SOURCES.md | grep -nE '^\| S(262|263|273|274) '` → 4 hits at lines
  149 (S273), 150 (S274), 152 (S262), 153 (S263); each row's final (`used-by`) cell names the matching
  knowledge file (`…/crawl-budget-consequences.md` ×2, `…/canonical-selection.md`, `…/crawler-identity.md`).

## PER-ROW:

| file | statement (atomic) | class | evidence line (quoted ≤25 words) | command output |
|---|---|---|---|---|
| canonical-selection.md | "Google's selection mechanism" | SUPPORTED | :12 "Google's own statement of the selection mechanism [S262]" | row 50 extracted; file line 12 printed |
| canonical-selection.md | "a declared canonical is a hint" | SUPPORTED | :15 "indicating a canonical preference is a hint, not a rule." | raw-substring quote, same words |
| canonical-selection.md | "weighed against HTTPS, redirects and sitemap inclusion" | SUPPORTED | :20-22 "whether the page is served over HTTP or HTTPS, redirects, presence of the URL in a sitemap" | file line 20-22 printed; factor list also names `rel="canonical"`, which the row omits without saying "only" → subset, not overreach |
| canonical-selection.md | "four recognised variant classes" | SUPPORTED | :37 "The page lists the variant classes it recognises" + bullets :41,42,43,45 | count derived: `canonical-selection bullet-quotes: 4 [41, 42, 43, 45]` |
| canonical-selection.md | "quotation rendering classes and the round-51 correction" | SUPPORTED | :81 "## Quote classes (round-51 correction)"; :83-86 "Every quotation in this entry is a rendering of the page, not a byte slice" | headings printed: `(81, '## Quote classes (round-51 correction)')` |
| canonical-selection.md | id set `(S262)` = header ids | SUPPORTED | :1 "source: S262 — https://developers.google.com/search/docs/crawling-indexing/canonicalization" | `source-header-lines: 1`; id histogram `S262 ×9, S021 ×1, S022 ×1` — body-only mentions of S021/S022 are not `source:` headers, so no mismatch under the stated rule |
| crawl-budget-consequences.md | "Two admitted Google sentences" | SUPPORTED | :9 "Two Google documents opened this round, and only these two sentences are admitted." | count derived: `(S273)` ×1 at line 11, `(S274)` ×1 at line 13 → 2 admitted sentences; `source: headers: [(1,S273),(2,S274)]` |
| crawl-budget-consequences.md | S273: "a robots block does not make Google shift the spared crawl budget to other pages unless the capacity limit is already hit" | SUPPORTED | :11 "Google won't shift this newly available crawl budget to other pages unless Google is already hitting your site's crawl capacity limit" | file line 11 printed; conditional preserved verbatim in sense |
| crawl-budget-consequences.md | S274: "emergency backoff reduces crawl rate across the whole hostname" | SUPPORTED | :13 "the backoff reduces your site's crawl rate across the whole hostname (S274)" | file line 13 printed; "emergency" sourced from :13 "Google's emergency crawl-rate page" |
| crawl-budget-consequences.md | "status codes unadmitted" | SUPPORTED | :13 "The checked S274 quote does not itself name the status codes that trigger that backoff." | file line 13 printed |
| crawl-budget-consequences.md | "no lane property measured" | SUPPORTED | :17 "No lane property was fetched or measured." | file line 17 printed |
| crawl-budget-consequences.md | id set `(S273, S274)` = header ids | SUPPORTED | :1 "source: S273 — …/crawl-budget"; :2 "source: S274 — …/reduce-crawl-rate" | `source-header-lines: 2`; histogram `S273 ×2, S274 ×3`; both ids are SOURCES.md rows 149/150 |
| crawler-identity.md | "Googlebot names two crawlers, Smartphone and Desktop" | SUPPORTED | :10 "Googlebot is the generic name for two types of"; :16/:18 name "Googlebot Smartphone"/"Googlebot Desktop" | `crawler-identity subtype quotes: 2 [16, 18]` |
| crawler-identity.md | "the HTTP user-agent header identifies the subtype" | SUPPORTED | :22-23 "You can identify the subtype of Googlebot by looking at the HTTP user-agent request header in the request" | file lines 22-23 printed |
| crawler-identity.md | "both types obey the same robots.txt product token" | SUPPORTED | :27 "both crawler types obey the same product token (user agent token) in robots.txt" | file line 27 printed |
| crawler-identity.md | "it also lists what the entry does not establish" | SUPPORTED | :46 "## What this entry does not establish" (4 bullets :48-55) | headings printed incl. `(46, '## What this entry does not establish')` |
| crawler-identity.md | id set `(S263)` = header ids | SUPPORTED | :1 "source: S263 — https://developers.google.com/search/docs/crawling-indexing/googlebot" | `source-header-lines: 1`; histogram `S263 ×6, S011 ×1, S095 ×1, S096 ×1` (body-only) |

Totals: 17 atomic statements, 17 SUPPORTED, 0 OVERREACH, 0 UNSUPPORTED, 0 STALE.

## COUNTS RE-DERIVED:

| number in row | where | re-derivation command | observed |
|---|---|---|---|
| four variant classes | row 50 | `python3` count of lines matching `^- "` in `canonical-selection.md` | 4 (lines 41, 42, 43, 45; bullets 3–4 wrap onto 44/46) |
| two crawlers / two subtypes | row 53 | `python3` count of lines starting `> "Googlebot Smartphone`/`> "Googlebot Desktop` | 2 (lines 16, 18) |
| two admitted sentences | row 51 | `python3` per-line count of `(S273)`/`(S274)` markers + `source:` header count | 2 (line 11 S273, line 13 S274); headers = 2 |
| ids in row 50 / 51 / 53 | rows 50,51,53 | `git show …:corpus/SOURCES.md \| grep -nE '^\| S(262\|263\|273\|274) '` | 4 registry rows: 149 S273, 150 S274, 152 S262, 153 S263 — all present, all `used-by` the matching entry |
| coverage-cell token counts (>=5 rule) | rows 50/51/53 | `python3` `len(cell.split())` | 27 / 44 / 32 tokens; no `\|` inside any cell |

## PROPOSED REPLACEMENTS:

none needed — every statement in all three cells is supported by the named file at the measured revision,
every number re-derives to the observed value, and every `(S###)` id matches the file's own `source:` header
and exists as a registry row.

## UNRUN:

- Live re-fetch of `developers.google.com` for S262/S263/S273/S274 — `unrun`; this attack is row-vs-file, not
  file-vs-vendor, so vendor-side drift is out of scope (the entries were unchanged base..rev, so no in-lane drift).
- `python3 -B .ufo/waves/round-55/c55_readme_index.py …` — `unrun` (counter execution is the parent's gate, not this seat's).
- No labrat probe dispatched: no subagent tool is exposed to this seat and the attack needed none.

VERDICT: all three C1 rows (README lines 50, 51, 53) are fully SUPPORTED at a7a548e — 17/17 atomic statements, all counts and ids re-derived and matching; no replacement coverage cell required.
