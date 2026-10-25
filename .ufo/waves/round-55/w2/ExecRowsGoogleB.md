# ExecRowsGoogleB

ATTACKS: `corpus/README.md` §Coverage map rows at revision `a7a548e102b71bd16b0a6ddafa469393a2c98b69` — line 52
(`knowledge/crawl-error-status-table.md`, S286), line 54 (`knowledge/dynamic-rendering-workaround-limits.md`, S249),
line 56 (`knowledge/js-rendering-queue.md`, S137–S139). Claim C1 (calibration).

Method: committed bytes only, `git show <rev>:<path>`; no worktree reads, no network, no writes outside this report.
Row extraction: `git show a7a548e…:corpus/README.md | sed -n '52p;54p;56p'` →
`| Error-status crawl layer | …` / `| Dynamic rendering workaround limits | …` / `| Render queue status-code contract | …`.
Each is in the first contiguous table of `## Coverage map`. The rows at 87/88/90 name the same three files in the
*later* frontier-ground-map table (Entries column, not Entry), so they are not index rows
(counter docstring: "later tables, e.g. the frontier ground map, never index a file").

Row identity: `git diff fcaf4b85… a7a548e… -- corpus/README.md` → `1 file changed, 84 insertions(+)`, 0 deletions;
all three rows appear as `+` lines, i.e. they were added at the measured revision.
No drift: `git diff fcaf4b85… a7a548e… -- corpus/knowledge/<each of the three>.md` → empty output for all three,
so each row describes exactly the bytes it is attached to.

## PER-ROW

Statements are the Coverage cell split at `;`/`:`/`,` into atomic factual claims. `L<n>` = line in the knowledge file
at the revision (`git show <rev>:corpus/knowledge/<file> | cat -n`). Quotes ≤ 25 words.

| file | statement | class | evidence (line + quote) | command output |
|---|---|---|---|---|
| crawl-error-status-table.md | one admitted Googlebot sentence | SUPPORTED | L8 "Only one sentence is admitted."; L10 is the single page-attributed sentence | `grep -c 'Only one sentence is admitted'` → 1; `grep -c 'crawl-errors page says'` → 1 |
| crawl-error-status-table.md | crawling scales back when server trouble is detected | SUPPORTED | L10 "Googlebot will scale back its crawling if it detects that your servers are having trouble" | same string in retained body `grep -F -c` → S286.raw.html 1, S286.txt 1 |
| crawl-error-status-table.md | the admitted quote is a raw substring of the retained page | SUPPORTED | L10 "That sentence is a raw substring of the retained HTML. It is not a collapsed-only quote." | raw grep → 1; whitespace-collapsed grep → 1 (present in raw bytes) |
| crawl-error-status-table.md | unlike S273's collapsed-only crawl-budget quote | SUPPORTED | L10 "S273's crawl-budget quote is collapsed-only."; also `corpus/QUALITY.md:1106` "(S273 collapsed-only, S274 a raw substring)" | S273.raw.html raw `grep -F -c` → **0**; after `tr '\n' ' ' \| tr -s ' '` → **1** |
| crawl-error-status-table.md | no soft-404 remedy claimed | SUPPORTED | L14 "A soft-404 remedy is not claimed from this sentence." | `grep -c 'soft-404 remedy is not claimed'` → 1 |
| dynamic-rendering-workaround-limits.md | one engine's own account | SUPPORTED | L46 "This entry holds one engine's own account of a technique"; L49-51 "A different engine's rule … is not implied" | distinct hosts in `source:` header (L1) → `developers.google.com` (1) |
| dynamic-rendering-workaround-limits.md | dynamic rendering as a workaround, not a recommended solution | SUPPORTED | L15-16 "Dynamic rendering is a workaround and not a recommended solution, because it creates additional complexities and resource requirements." | `grep -c 'workaround and not a recommended solution'` → 2 (L3 recheck string + L15 quote); S249.txt `grep -F -c` → 1 |
| dynamic-rendering-workaround-limits.md | the cloaking boundary is a content condition, not a technique | SUPPORTED | L27 "the cloaking boundary is a content condition, not a technique condition"; L30-31 "As long as your dynamic rendering produces similar content" | `grep -c 'content condition, not a technique condition'` → 1; S249.txt:219 carries the similar-content clause |
| dynamic-rendering-workaround-limits.md | error pages inherit the rendering-queue status-code rule | SUPPORTED (provenance note) | L38-42 "they inherit the status code rule of `corpus/knowledge/js-rendering-queue.md`, where a non-200 response may skip the rendering pass entirely" | joined-text `grep -c 'inherit the status code rule of'` → 1. NOTE: S249 body has `grep -c -i 'status code'` → **0**; S249.txt:220 only says "treats the error as any other error page" — the inheritance is the entry's cross-entry inference, which the row restates faithfully |
| dynamic-rendering-workaround-limits.md | nothing was observed on a live crawl | SUPPORTED | L47-49 "Nothing here was observed on a live crawl: no crawler was run, no owned property was fetched" | joined-text `grep -c 'Nothing here was observed on a live crawl'` → 1 |
| js-rendering-queue.md | 200 responses queue for rendering regardless of JavaScript | SUPPORTED | L13-14 "All pages with a 200 HTTP status code are sent to the rendering queue, no matter whether JavaScript is present on the page." | `grep -c 'sent to the rendering queue'` → 2 (L3 recheck string + L13); S137.txt `grep -F -c` → 1 |
| js-rendering-queue.md | non-200 may skip | SUPPORTED | L18-19 "If the HTTP status code is non- 200 (for example, on error pages with 404 status code), rendering might be skipped." | `grep -c 'rendering might be skipped'` → 1; S137.txt `grep -F -c 'If the HTTP status code is non- 200'` → 1 |
| js-rendering-queue.md | robots.txt check precedes the request | SUPPORTED | L31-33 "it first checks if you allow crawling. Googlebot reads the robots.txt file" | `grep -c 'it first checks if you allow crawling'` → 1; S137.txt same string → 1 |
| js-rendering-queue.md | four publisher rules | SUPPORTED | L39 "A publisher reading that order gets four rules:"; numbered items at L41, L44, L47, L50 | `grep -c 'gets four rules'` → 1; `grep -cE '^[0-9]\. \*\*'` → **4** |
| js-rendering-queue.md | zh-CN and ja locale restatements | SUPPORTED | L56-58 "The Simplified-Chinese edition states the same rule in that language, and the Japanese edition states it in Japanese"; quotes at L60-64 carry (S138)/(S139) | `grep -c 'Simplified-Chinese edition states the same rule'` → 1; `grep -c 'Japanese edition states it in Japanese'` → 1; S138.txt `grep -c '渲染队列'` → 2; S139.txt `grep -c 'レンダリング キュー'` → 1 |

Id binding (all three rows): `git show <rev>:corpus/SOURCES.md | grep -nE '^\| S(137|138|139|249|286) '` →
5 rows at lines 145 (S137), 146 (S138), 147 (S139), 148 (S249), 151 (S286); count → **5**.
`awk -F'|'` on those rows, `used-by` cell → S137/S138/S139 `corpus/knowledge/js-rendering-queue.md`,
S249 `corpus/knowledge/dynamic-rendering-workaround-limits.md`, S286 `corpus/knowledge/crawl-error-status-table.md`.
Row id cells vs file `source:` headers: line 56 `(S137–S139)` expands to S137 S138 S139 =
`sed -n '1p' | grep -oE 'S1[0-9]{2}' | sort -u` → `S137 S138 S139`; line 54 `(S249)` = header S249;
line 52 `(S286)` = header S286. **Equal in all three cases; no extra or missing id.**

## COUNTS RE-DERIVED

| count in a row | how re-derived | observed |
|---|---|---|
| "One admitted Googlebot sentence" (row 52) | `grep -c 'Only one sentence is admitted'` + `grep -c 'crawl-errors page says'` on the file | 1 and 1 |
| raw-substring class (row 52) | `grep -F -c` of the sentence in `S286.raw.html` / `S286.txt` | 1 / 1 |
| S273 collapsed-only class (row 52) | `S273.raw.html`: raw `grep -F -c` = 0; whitespace-collapsed = 1 | 0 raw, 1 collapsed |
| "One engine" (row 54) | distinct hosts in the `source:` header URL | 1 (`developers.google.com`) |
| "four publisher rules" (row 56) | `grep -cE '^[0-9]\. \*\*'` | 4 |
| "zh-CN and ja" (row 56) | distinct locale ids in header (`S138`, `S139`) beyond English `S137` | 2 |
| row ids exist in SOURCES.md | `grep -cE '^\| S(137|138|139|249|286) '` | 5 of 5 |
| Coverage-cell tokens / shared-word term | independent recompute over committed bytes (5+-letter words minus the 40 %-of-heads stoplist) | 32 / 38 / 26 tokens; shared_minus_common non-empty for each (`thin=False` ×3) |
| no `\|` inside any cell | `awk -F'\|' '{print NF}'` on lines 52/54/56 | `fields=5` ×3 (3 cells) |
| C1 counter at the revision | `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision a7a548e…` | `index_mismatches=0 knowledge_files=49 met=True`; `unindexed=0 multi=0 thin=0 duplicate=0 head_changed=0 deleted=0 dangling=0 coverage_rows=51`; EXIT=0 |

## PROPOSED REPLACEMENTS

none needed — 15 of 15 statements classified SUPPORTED; 0 OVERREACH, 0 UNSUPPORTED, 0 STALE.

Optional, *not required by any classification* (only if L1 wants row 54 to carry the provenance the entry carries):
`One engine's own account of dynamic rendering as a workaround, not a recommended solution: the cloaking boundary is a
content condition, not a technique; error pages are treated as any other error page, so the rendering-queue non-200 skip
rule applies; nothing was observed on a live crawl.` — 40 whitespace tokens, no `|`, shares `rendering`/`cloaking`/
`workaround` with the H1, and is true of the file at the revision (S249.txt:220 + js-rendering-queue.md L18-19).

## UNRUN

- No live re-fetch of S137/S138/S139/S249/S286: row truth is checked against the committed retained bodies
  (`.ufo/waves/round-48/sources/S137.txt`, `S138.txt`, `S139.txt`, `S249.txt`; `.ufo/waves/round-50/sources/S286.raw.html`,
  `S286.txt`) and the committed knowledge files, not the network. Source-level freshness of those pages is C2's surface, not mine.
- Labrat probe: not run — no dispatch tool is mounted in this seat's tool inventory; all checks were direct commands.
- Tooling: no installs or upgrades were needed or performed.

VERDICT: The three C1 coverage-map rows are faithful — 15/15 statements SUPPORTED with committed-byte evidence, ids and counts re-derived (1, 1, 1, 0-vs-1, 1, 4, 2, 5/5), counter green at the revision; one provenance risk recorded in row 54's error-page clause (inherited from the entry, not the row), no replacement required.
