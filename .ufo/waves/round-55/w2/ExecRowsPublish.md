# ExecRowsPublish

ATTACKS: the three rows added to `corpus/README.md` §Coverage map at `a7a548e102b71bd16b0a6ddafa469393a2c98b69` — README line 57 (`knowledge/link-preview-metadata.md`), line 58 (`knowledge/pages-base-path.md`), line 64 (`knowledge/security-txt-publishing.md`) — i.e. claim C1's "coverage cell is descriptive" term, read semantically rather than mechanically.

Basis: every byte below is read with `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show a7a548e102b71bd16b0a6ddafa469393a2c98b69:<path>`; no worktree read of the lane, no lane mutation. Axis sentence repeated per contract: C1 is declared on **calibration**, the bounded sub-axis `SCORECARD.md` added in round 54 (score 1, lowest non-retired axis); that sub-axis is not in the prompt's axis list.

Setup evidence (run): `git diff -U0 fcaf4b85 a7a548e1 -- corpus/README.md` → one hunk `@@ -45,0 +46,84 @@`, 84 insertions, containing all three rows as `+` lines. `git show a7a548e1:corpus/README.md | grep -n '^#'` → `## Coverage map` at line 15, `### Frontier ground map (round 55)` at 71, `## Known gaps` at 131; the first contiguous table of the section is lines 17–69, so lines 57/58/64 are index rows. Counter at the revision (script extracted from the revision, run read-only): `python3 -B /tmp/c55run/c55_readme_index.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision a7a548e102b71bd16b0a6ddafa469393a2c98b69` → `index_mismatches=0 knowledge_files=49 met=True ... unindexed=0 multi=0 thin=0 duplicate=0 head_changed=0 deleted=0 dangling=0 coverage_rows=51`, `EXIT=0`. So the mechanical terms pass; what follows tests the cells' content.

## PER-ROW

### Row 57 — `knowledge/link-preview-metadata.md` (S067–S070)

| statement | class | evidence line (knowledge file) | command output |
|---|---|---|---|
| "Four required Open Graph properties" | SUPPORTED | L20–22 "The protocol names four required properties, not a recommended set: “The four required properties for every page are:” (S067), namely `og:title`, `og:type`, `og:image` and `og:url`" | `git show …:S067.txt \| grep -c 'four required properties'` = 1; `for p in og:title og:type og:image og:url; do … grep -c $p` = 1 1 1 1 |
| "what each preview field means" | SUPPORTED | L23–31 per-property definitions, e.g. L23–24 "The title of your object as it should appear within the graph" (S067) | 4 definition bullets counted at L23–31 |
| "Facebook's undecorated canonical og:url" | SUPPORTED | L56–57 "This should be the undecorated URL, without session variables, user identifying parameters, or counters." (S068) | `grep -ci undecorated` on S068.txt = 1 |
| "one og:type per URL" | SUPPORTED | L59–60 "Each URL should be a single object, so multiple og:type values are not possible." (S068) | quote is verbatim in entry; S068 retained text carries it (entry cites it as a curly-quoted span) |
| "URL-keyed image caching" | SUPPORTED (paraphrase) | L62–63 "Images are cached based on the URL and won’t be updated unless the URL changes." (S068) | literal token `URL-keyed` absent from file (word-diff below); the file's phrasing is "cached based on the URL" |
| "Sharing Debugger re-scrape" | SUPPORTED (file's own term) | L71–73 "The debugger also triggers a scrape of your page" (S068); L158–159 names it "the Sharing Debugger re-scrape (S068)" | `grep -ci 'sharing debugger'` on S068.txt = 1 |
| "Slack's range-limited fetch" | SUPPORTED | L82–84 "It fetches as little of the page as it can (using HTTP Range headers)" (S069) | `grep -c 'HTTP Range'` on S069.txt = 1 |
| "30-minute global cache" | SUPPORTED, hedge dropped (see nit N1) | L90–91 "Responses to these requests are cached globally across the service for around 30 minutes." (S069) | `grep -o 'around 30 minutes'` on S069.txt = `around 30 minutes` |
| "Mastodon's PreviewCard entity" | SUPPORTED | L101–102 "Represents a rich preview card that is generated using OpenGraph tags from a URL." (S070) | quote verbatim at L101–102 |
| "a source-byte census of 102 ds4cc pages" | SUPPORTED | L120–126 "Population: the 102 `.html` paths of the retained `git archive` … The count is over source bytes"; census line L128 `pages=102` | three independent recounts below |

### Row 58 — `knowledge/pages-base-path.md` (S040–S043)

| statement | class | evidence line | command output |
|---|---|---|---|
| "Publisher-side ground" | SUPPORTED | L7–9 "owns publisher-side knowledge of the base path; it owns no live property measurement and claims nothing about any owned site" | — |
| "a project site is published under a base path" | SUPPORTED | L11–13 "A GitHub Pages *project* site is published under a base path, so a reference written for the origin root does not stay inside the site" | — |
| "two site kinds (S040)" | SUPPORTED | L19 "There are two types of GitHub Pages sites. Sites associated with a user or organization account, and sites for a specific project." (S040) | `grep -c 'There are two types of GitHub Pages sites'` on S040.txt = 1 |
| "Liquid `relative_url`/`absolute_url` filters (S042)" | SUPPORTED | L33 relative_url definition + L34 absolute_url definition (both S042); L32 records that S041 shows relative_url only | `grep -c relative_url` S042.txt = 1; `grep -c absolute_url` S042.txt = 1; `grep -c absolute_url` S041.txt = 0 (matches L32) |
| "Vite's `base` option (S043)" | SUPPORTED | L39–41 "Set the correct base in vite.config.js ." and the `/<REPO>/` rule (S043) | `grep -c base` S043.txt = 1 |
| "an offline audit over a frozen 30-case matrix" | SUPPORTED | L54 "the frozen 30-case matrix is `.ufo/waves/round-29/c2-matrix.json`"; L55 "Cannot: the audit reads local files only" | `json.load` over the matrix at the revision → `cases 30 unique 30`, `Counter({'D': 14, 'I': 8, 'K': 7, 'U': 1})` |
| "root-relative breakage is inference" | SUPPORTED | L25 "[INFERENCE] under ordinary URL resolution `/style.css` resolves against the origin, not the base path … none of S040–S043 states this" | — |
| "no property measured" | SUPPORTED | L8–9 (above) + L56 "Not established here: the base path, domain or build mode of any owned property" | — |

### Row 64 — `knowledge/security-txt-publishing.md` (S078–S080, S082–S086, S001–S002, S006)

| statement | class | evidence line | command output |
|---|---|---|---|
| "Where `/.well-known/security.txt` lives" | SUPPORTED | L20–22 "A website's file belongs under `/.well-known/` (S078). The prefix is reserved only at the top of the path" | — |
| "the duplicate rule" | SUPPORTED | L26–29 "With both present, the well-known copy must be used (S078)"; the wave-2 correction L147–150 keeps only the MUST-use half, which the row does not exceed | — |
| "HTTPS and `text/plain` serving" | SUPPORTED | L35–36 "HTTPS only, HTTP/1.0 or later, `Content-Type: text/plain` with default charset `utf-8` (S078)" | — |
| "the registered fields with cardinality" | SUPPORTED (mirrors the file's own header L6 "every registered field with cardinality"; body gives the list + cardinality, and calls only *new* fields IANA-registered at L62) | L44 "`Contact` is mandatory", L48 "`Expires` is mandatory, exactly once", L51 "`Preferred-Languages` is optional, at most once", L53–54 "optional, repeatable" | 8 field names present: `grep -c '\`Contact\`'`=5, `Expires`=4, `Preferred-Languages`=3, `Canonical`=5, `Encryption`=4, `Policy`=4, `Hiring`=3, `Acknowledgments`=3 |
| "the `Expires` horizon" | SUPPORTED | L48–50 "a horizon shorter than a year is recommended (S078)" | — |
| "contact order" | SUPPORTED | L47 "Several `Contact` lines are ordered by preference, first line preferred (S078)"; correction L148–150 limits it to order among Contact lines, which is all the row says | — |
| "encryption and signing" | SUPPORTED | L57 "`Encryption` is a URI to a key, never the key itself (S078)"; L59–61 "An OpenPGP cleartext signature is recommended, with Canonical alongside" | — |
| "host scope" | SUPPORTED | L67–68 "It applies to the host actually used to fetch it, not its parents or subdomains" | — |
| "two live files" | SUPPORTED | L97 heading "## The two live files"; L99–102 (S084, GitHub) and L103–105 (S085, Google) | retained bodies exist at the revision: S084.txt and S085.txt each 1 line, first field `Contact:`; S084 `Contact:` lines=1, S085 `Contact:` lines=1 |
| "dot-directory handling for a Jekyll branch build versus an Actions artifact build" | SUPPORTED | L77–78 branch skip of `_`/`.`/`#` + `include` (S006, S080); L86–88 v4.0.0 drops hidden paths, v5.0.0 adds `include-hidden-files` (S002); L89–90 `.git`/`.github` unconditional (S001) | — |

Nits (no class failure):
- N1 (row 57): "30-minute global cache" compresses the file's "around 30 minutes" (L90). Hedge lost, substance unchanged.
- N2 (row 58): the entry's own index-row convention elsewhere carries a round tag (`(r34)`, `(r35)`); row 58 omits `(r29)` although L341 and the frontier-ground row (README L96) tag the same file r29. Label omission only; no statement is false.
- N3 (row 64): cell ends without a terminal period (rows 57/58 have one). Cosmetic; the row still parses as 3 columns (`grep -o '|' | wc -l` = 4 pipes on all three rows).
- N4 (row 64): the row's id list is a proper subset of the file's `source:` header ids — see id check below. The two omitted ids are declared rejected by the header sentence itself.

Id check (run): script comparing the row's parenthetical (ranges expanded) against `S\d{3}` tokens on the file's `source:` line, both read from the revision:
- `link-preview-metadata`: row_ids `['S067','S068','S069','S070']` = header_ids, `equal=True`, `only_row=[]`, `only_header=[]`.
- `pages-base-path`: row_ids `['S040','S041','S042','S043']` = header_ids, `equal=True`.
- `security-txt-publishing`: row_ids 11 = `['S001','S002','S006','S078','S079','S080','S082','S083','S084','S085','S086']`; header_ids 13 adds `['S081','S087']`; `equal=False`, `only_row=[]`, `only_header=['S081','S087']`. Header L1 says "S081 (Wikipedia) and S087 (404) were opened this round and rejected", so the subset is deliberate and the row is not wrong; adding them would be worse.
- Every id in all three rows exists as a registry row at the revision: `git show …:corpus/SOURCES.md | grep -c '^| *S0xx *|'` = 1 for each of S067 S068 S069 S070 S040 S041 S042 S043 S078 S079 S080 S082 S083 S084 S085 S086 S001 S002 S006 (19/19 = 1). Spot-printed rows confirm table shape (`| S067 | The Open Graph protocol — https://ogp.me/ | spec | A | …`).

Word-level check (run): every 5+ character word in each cell searched case-insensitively in the file's own bytes. Absent tokens: row 57 `['URL-keyed']`; row 58 `["Vite's", 'kinds', 'measured']` (the bare words `Vite`, `two types`, `measurement` are present — possessive/paraphrase forms only); row 64 `[]`. No cell word denotes a fact the file lacks.

Cell shape (run): tokens per Coverage cell = 43 / 39 / 42 (all ≥ 5); pipes per row = 4 / 4 / 4.

## COUNTS RE-DERIVED

| row | number in cell | command | observed |
|---|---|---|---|
| 57 | "Four required … properties" = 4 | `grep -c 'four required properties'` on retained S067.txt | 1 occurrence; 4 property names each present once |
| 57 | "102 ds4cc pages" | `git show …:…/ds4cc-7fc6aa2f/tree.txt \| grep -c '\.html$'`; `git show …:…/html.tar.xz \| tar -tJf - \| grep -c '\.html$'`; python walk of the extracted archive | 102; 102; `html files: 102` |
| 57 | census cross-check (og counts) | python re-count over the extracted archive (`<meta property=… content=…>`, non-empty after strip) | `og:title 87 og:type 87 og:url 87 og:image 1` — equals the file's L128 census line `pages=102 og:title=87 og:type=87 og:image=1 og:url=87` |
| 57 | "30-minute" | `grep -o 'around 30 minutes'` on S069.txt | `around 30 minutes` |
| 58 | "two site kinds" = 2 | `grep -c 'There are two types of GitHub Pages sites'` on S040.txt | 1 |
| 58 | "30-case matrix" = 30 | `python3 -c` over `.ufo/waves/round-29/c2-matrix.json` at the revision | `cases 30 unique 30` (D14 I8 K7 U1) |
| 58 | ids "(S040–S043)" = 4 | id-expansion script | 4 ids, equal to header |
| 64 | "two live files" = 2 | retained bodies S084.txt, S085.txt at the revision | both exist, 1 line each, first field `Contact:` |
| 64 | ids "S078–S080, S082–S086, S001–S002, S006" = 11 | id-expansion script | 3+5+2+1 = 11, all with a SOURCES.md row |
| 64 | "registered fields with cardinality" = 8 fields | `grep -c` per field name on the entry | Contact 5, Expires 4, Preferred-Languages 3, Canonical 5, Encryption 4, Policy 4, Hiring 3, Acknowledgments 3; cardinality sentences at L44/48/51/54 |

Counter corroboration (run): `c55_readme_index.py` at the revision → `thin=0 duplicate=0 dangling=0`, so none of the three cells is thin, none repeats another cell's normalized text, and no backticked pointer in the section dangles.

## PROPOSED REPLACEMENTS

none needed — no statement in any of the three cells is OVERREACH, UNSUPPORTED or STALE.

Optional micro-edit (not required by any failing class; N1 only): in row 57 replace `and 30-minute global cache` with `and an around-30-minute global cache`. Cell would then read: "Four required Open Graph properties and what each preview field means; Facebook's undecorated canonical og:url, one og:type per URL, URL-keyed image caching and Sharing Debugger re-scrape; Slack's range-limited fetch and an around-30-minute global cache; Mastodon's PreviewCard entity; a source-byte census of 102 ds4cc pages." — 44 tokens, no `|`, shares "preview"/"metadata"-family words with the H1 "# Link-preview metadata (Open Graph)", and is true against L90.

## UNRUN

- No live fetch of any cited page or of `/.well-known/security.txt` (S084/S085 "live" is read as the file's fetch-time property at its `verified-at: 2026-10-22`, not re-checked today). Class "live" therefore rests on the retained bodies, not on a 2026-10-25 request.
- Did not run the round-34/round-29/round-35 entry counters (`c2_source_census.py`, `c2_matrix_count.py`, `sealed_count.py`); only the C1 counter was run, and only for corroboration of the thin/duplicate/dangling terms.
- Did not diff the three cells against the older per-round rows (README L341/L405/L421) beyond reading them: no contradiction found by reading, but no mechanical equality check was run.
- No labrat probe was needed; no subagent was dispatched.

VERDICT: All three Coverage cells are SUPPORTED statement-by-statement against the committed entries, every count re-derives to the row's value (4 required properties, 102 pages / 87-87-87-1 census, 2 site kinds, 30 matrix cases, 2 live files, 11 ids), ids match each `source:` header except row 64's deliberate omission of the header's two rejected ids (S081, S087); no OVERREACH, UNSUPPORTED or STALE statement, no replacement required — only one optional hedge restoration (row 57 "around 30 minutes").
