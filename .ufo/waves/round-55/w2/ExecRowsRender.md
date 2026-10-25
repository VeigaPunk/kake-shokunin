# ExecRowsRender
ATTACKS: `corpus/README.md` §Coverage map rows added at `a7a548e102b71bd16b0a6ddafa469393a2c98b69` — line 61 `knowledge/render-web-services.md`, line 62 `knowledge/render-static-sites.md`, line 63 `knowledge/robots-txt-rules.md` (claim C1). All bytes read with `git show <rev>:<path>`; no worktree read, no mutation.

## PER-ROW:

Commands are tagged `[C#]` and listed under COUNTS RE-DERIVED. Quoted spans are exact committed text, ≤25 units.

### Row 61 — `knowledge/render-web-services.md` (README:61)
| # | statement | class | evidence (file line, quote) | command output |
|---|---|---|---|---|
| 1 | "Render's documentation for web services" | SUPPORTED | L4 "Render platform documentation for web services, Docker-based services, health checks and the Blueprint file (render.yaml)" | `[C2]` |
| 2 | "the required 0.0.0.0 port bind" | SUPPORTED | L21 "Your web service must bind to a port on host 0.0.0.0 to receive HTTP requests from the public internet." (S058) | `[C3]` 0.0.0.0 hits=1 |
| 3 | "a Docker build context filtered by .dockerignore" | SUPPORTED | L30 "Render omits files and directories from your build context based on your .dockerignore file." (S059) | `[C3]` .dockerignore hits=1 |
| 4 | "health-check success at 2xx or 3xx within five seconds" | SUPPORTED | L36 "Render considers a check successful if the instance responds with a 2xx or 3xx status code within five seconds." (S060) | `[C3]` "within five seconds" hits=1 |
| 5 | "an offline key-by-key check of the lane's own render.yaml at ds4cc-marketplace commit 1fbdb8ed" | SUPPORTED | L50 "## The lane's render.yaml at ds4cc-marketplace 1fbdb8ed"; L52 "Read offline with `git -C ~/Projects/ds4cc-marketplace show 1fbdb8ed:render.yaml`"; one bullet per key L58–L67 | `[C3]` 1fbdb8ed hits=11, blob d17ab7e5 hits=2 |

Note (not a row defect): "the lane's own" is the entry's own phrase (L4); the file it names is in `ds4cc-marketplace`, which the row also names, so no location claim is overstated.

### Row 62 — `knowledge/render-static-sites.md` (README:62)
| # | statement | class | evidence (file line, quote) | command output |
|---|---|---|---|---|
| 1 | "Render Docs reading of a static site" | SUPPORTED | L4 "Render platform documentation for static sites only." | `[C2]` |
| 2 | "build details and dependency install" | SUPPORTED | L24 "specify your build details (including which Git branch to deploy)" (S049); L27 "By default, Render automatically attempts to detect and install your static site's dependencies." (S049) | `[C2]` |
| 3 | "redirect/rewrite rule matching order" | SUPPORTED | L40 "Apply the first matching rule (starting from the top of the list)" (S050); L38–L39 resource check, L40 "Return 404 Not Found" | `[C2]` |
| 4 | "dashboard response headers" | SUPPORTED | L49 "you can define response headers for your static sites in the Render Dashboard" (S051) | `[C2]` |
| 5 | "custom domains and TLS" | SUPPORTED | L60 "Render automatically creates and renews TLS certificates for all custom domains, including wildcard domains" (S052); L55–L66 | `[C2]` |
| 6 | "contrasts with the GitHub Pages entries already held" | SUPPORTED | L70–L71 "The GitHub Pages side of each contrast is cited to the lane entry that holds it"; L68 heading | `[C2]` |
| 7 | "four retained pages" | SUPPORTED | L2 "all four opened this round with one public GET each"; `.ufo/waves/round-30/sources/receipts.json` has exactly keys S049–S052 | `[C4]` 4 keys, 8/8 sha256 match |
| 8 | "no owned property measured" | SUPPORTED | L126–L127 "No live Render site was fetched, and no operator-owned property was contacted" | `[C2]` |

Caveat on #7 (understatement, not overreach): the entry now also quotes S061 at L158–L160, and S061's retained text exists (`.ufo/waves/round-31/sources/S061.txt`; `[C4]` round-31 receipts = 5 keys S057–S061). Four is a true count of the round-30 pages; the entry's quoted page set is five. The row's id cell mirrors the file's `source:` header, which omits S061 — see ADJACENT below.

### Row 63 — `knowledge/robots-txt-rules.md` (README:63)
| # | statement | class | evidence (file line, quote) | command output |
|---|---|---|---|---|
| 1 | "RFC 9309 robots.txt rules" | SUPPORTED | L9 "The Robots Exclusion Protocol is a crawler-access convention, not authorization"; S011 and S099 are both RFC 9309 rows | `[C5]` |
| 2 | "this lane's offline expectation readings" | SUPPORTED | L11 "This entry describes the lane's offline expectation check" | `[C2]` |
| 3 | "access-result status handling" | SUPPORTED | L19 "an HTTP 4xx “unavailable” response means crawlers MAY access server resources"; L23–L25 lane mapping | `[C2]` |
| 4 | "line and group parsing" | SUPPORTED | L27 heading "## Read lines and groups"; L29 "RFC 9309 requires UTF-8 plain text and says parsers MUST try each line and use parseable rules"; L31–L45 | `[C2]` |
| 5 | "rule matching with URL normalization" | SUPPORTED | L47 heading "## Match rules to a URL"; L61 "octets outside ASCII and those "in the reserved range" MUST be percent-encoded before comparison"; L49–L63 | `[C2]` |
| 6 | "round-38 amendments (h) JSON numbers, (i) URL characters, (k) implicit /robots.txt allow" | SUPPORTED | L91 "**(h) JSON numbers, lane reading.**"; L102 "**(i) URL characters, lane reading.**"; L113 "**(k) Implicit `/robots.txt` allow on the normalized path, lane reading.**" | `[C6]` 3 amendment headings, exactly (h)(i)(k) |

### ID check (all three rows)
| file | row ids (range expanded) | file `source:` header ids | equal | each id a SOURCES.md row |
|---|---|---|---|---|
| render-web-services.md | S057 S058 S059 S060 | S057 S058 S059 S060 | yes | yes, 4/4 rows=1 |
| render-static-sites.md | S049 S050 S051 S052 | S049 S050 S051 S052 | yes | yes, 4/4 rows=1 |
| robots-txt-rules.md | S011 S095 S096 S034 S098 S099 S100 | same 7 (trailing prose repeats S034 S098 S100) | yes (set) | yes, 7/7 rows=1 |

`[C7]` observed: `render-web-services.md | row: ['S057','S058','S059','S060'] | hdr: [...] | set_equal: True | dup_hdr: False`; `render-static-sites.md | set_equal: True`; `robots-txt-rules.md | set_equal: True | dup_hdr: True`. `[C8]` per-id SOURCES check: `S049 rows=1 … S100 rows=1` (15 ids, every value 1).

### ADJACENT — same README addition, outside the three Coverage cells (reported, not judged as row defects)
- F1 `[C9]`: `render-static-sites.md` body cites S061 (L158, L159, L160) but its `source:` header (L1) lists only S049–S052; `corpus/SOURCES.md` S061 `used-by` = `corpus/knowledge/render-static-sites.md`. Frontier-map row README:97 names S061; Coverage row README:62 cannot, because it mirrors the header.
- F2 `[C9]`: `render-web-services.md` body cites S062 (L82, L88, L97, L107) but its header lists only S057–S060; SOURCES S062 `used-by` = `corpus/knowledge/render-web-services.md`; Frontier-map row README:98 names S062.
- F3 `[C9]`: `robots-txt-rules.md` mentions S101 once (L110) as rejected ("WHATWG registry row S101 rejected as this contract's source"); SOURCES S101 row status cell is `rejected` yet its `used-by` names this file, and Frontier-map row README:82 lists `S098–S101`. The frontier row mirrors the registry, so the anomaly is the registry `used-by` of a rejected row.
- F4: rows 61/62 titles carry "(r31)"/"(r30)" while both entries hold later appended corrections (round-31 at L141–L162; round-32 at L79–L109). Titles label the round of entry, not a claim of finality; no statement in either Coverage cell is falsified by the corrections (`[C10]` base→rev diff empty, so no statement is STALE by edit).

## COUNTS RE-DERIVED:
- `[C1]` `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision a7a548e…` → `index_mismatches=0 knowledge_files=49 met=True`, `unindexed=0 multi=0 thin=0 duplicate=0 head_changed=0 deleted=0 dangling=0 coverage_rows=51`, `EXIT=0`. The three rows are in the first contiguous table: `[C11]` blank line at README:70, `### Frontier ground map` at 71, so the index table spans 19–69 and rows 61–63 sit inside it; each of the three files is named exactly once in 19–69 (`render-static-sites: 1`, `render-web-services: 1`, `robots-txt-rules: 1`).
- `[C4]` "four retained pages": round-30 `receipts.json` keys = `['S049','S050','S051','S052']` (4); sha256 of committed `S049.txt`…`S052.txt` equals each receipt `textSha256` → 4/4 `match=True`. Round-31 receipts = 5 keys `['S057','S058','S059','S060','S061']`; `S057`–`S060` texts 4/4 `match=True` (S061 also retained, unused by row 61).
- `[C12]` `.ufo/waves/round-30/sources/` holds 7 `*.txt`: the four page texts plus `screened/C1.txt C2.txt C3.txt` (screened receipts = 3, ids `C1 C2 C3`). "Four retained pages" counts the entry's cited pages, not every text in the directory.
- `[C3]` literal numbers in row 61: `0.0.0.0` 1 hit in S058.txt; `.dockerignore` 1 hit in S059.txt; `within five seconds` 1 hit in S060.txt; `2xx or 3xx` 1 hit in S060.txt; `1fbdb8ed` 11 hits in the entry; blob `d17ab7e5` 2 hits.
- `[C6]` row 63 amendment count: `grep -nE '^\*\*\([a-z]\)'` → exactly 3 lines (91, 102, 113), ids (h), (i), (k).
- `[C13]` knowledge tree at the revision: `git ls-tree -r --name-only <rev> corpus/knowledge/ | wc -l` → 49 (matches counter `knowledge_files=49`).
- `[C14]` quote fidelity: 9/9 entry quotes re-checked as exact substrings of the retained texts — S058 0.0.0.0 sentence FOUND; S059 .dockerignore sentence FOUND; S060 2xx/3xx sentence FOUND; S049 atomic-build and dependency-install sentences FOUND; S050 first-match and 404 FOUND; S051 header-path sentence FOUND; S052 HTTP→HTTPS sentence FOUND.

## PROPOSED REPLACEMENTS:
none needed — no OVERREACH, UNSUPPORTED or STALE statement found in rows 61–63; each row's id cell equals its file's `source:` header and every id is a registry row.

Advisory (do not apply to the row alone; fix the file header first, else the id rule breaks): if the lane wants the rows to state the entries' full quoted page set, the minimal cell edit is row 62 `four retained pages` → `five retained pages (S049–S052, S061)` and row 61 id cell `(S057, S058, S059, S060)` → `(S057–S060, S062)`; both require adding S061/S062 to the respective `source:` headers. This is a provenance-completeness fix, not a truth fix.

## UNRUN:
- Fresh network re-fetch of the Render Docs, RFC 9309/8259/3986, Google and Python pages (page freshness is C2's surface, not a coverage-row audit) — unrun.
- `python3 -B .ufo/waves/round-30/c2_quote_truth.py` and `.ufo/waves/round-31/c2_quote_truth.py` — unrun (row claims do not depend on those counters; quote fidelity was checked directly, `[C14]`).
- No labrat probe used; no external evidence was needed.
- No files other than this report were written; no git add/commit/stash/checkout/reset, no jj call.

VERDICT: All three rows' coverage cells are fully supported (19/19 atomic statements SUPPORTED), ids match headers and registry; only adjacent provenance gaps found — S061/S062 body-cited but absent from two headers, S101 rejected yet listed in the frontier row via its registry `used-by`.
