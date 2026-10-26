# ScoutIdSyntax

Scope: /home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/ — 49 `.md` + 3 `.json` (52 files). `git diff 28fa0b23… -- corpus/knowledge` is empty and `git log -1 -- corpus/knowledge` is the base commit, so this directory is byte-identical to the base (lane HEAD is f7c98ff2…, not the base; irrelevant here). All checks read-only (scan scripts in /tmp).

## COMMANDS:
- `grep -ohE 'S[0-9]{3,}' *.md | sort -u | wc -l` → **105** (loose; 1126 total occurrences).
- `grep -ohE '\bS[0-9]{3,}\b' *.md | sort -u | wc -l` → **104** (word-bounded; 1094 total occurrences; ids S001..S420).
- Difference = exactly one distinct token: **S404**, only occurrence `S404_SHA256` (free-read-verbs.md:195, "409-byte Kimi 404 sentinel"). `_` is `\w`, so `\b` rejects it. S404 has no row in corpus/SOURCES.md — not a source id. The other 32 loose-only occurrences (1126−1094) are glued filename fragments of already-cited ids (below).
- Also run: dash/slash/`and` spellings (`grep -noE 'S[0-9]{3}(–|-|—|\.\.|/| to )…'`), lowercase `s###` (0), `S`+2 digits (0), `S`+4+ digits (0), `S 262`/`S-262` (0), ids in fenced lines (0), in `https?://` URLs (0), in hex hashes (0), in `.json` (0).
- Cross-check vs corpus/SOURCES.md (158 `^| S### |` rows): all 104 cited ids have a row (0 dangling); 54 rows are never cited in knowledge/*.md.

## FORMS TABLE:
| Form | Real example (file:line) | Count / finding |
|---|---|---|
| Bare, space-delimited | `source: S011, S095` | 321 SP…SP; 116 SP…`,`; 47 SP…`)` |
| Parenthesised | `(S262)` | 297 `(…)`; 59 `(…,`; 37 `(…SP`; few `(…:` `(…;` `(…'` |
| Bracketed | `[S367]` | 86, always exactly `[Sn]`; multi-id brackets 0 |
| Trailing `,` `.` `;` `:` `'` `’` `"` | `S049–S052;` | all delimit fine under `\b` |
| Curly possessive | `S041’s`, `S043’s` (pages-base-path.md:48) | `\b` OK; read UTF-8 |
| En-dash range `S040–S043` (U+2013) | pages-base-path.md:25,27,48 | 14 occurrences |
| ASCII-hyphen range `S001-S007` | publish-channels.md:2; sitemap-orphan-audit.md:2,153; static-canonical-preflight.md:2 (×2) | 5 occurrences |
| Slash pair | `S273/S274` yahoo-japan-deleted-url-recrawl.md:8; `S003/S004` ghp-served-set.md:105 | two literals, NOT a range |
| Hyphen glued to word | `S003-containing` sitemap-orphan-audit.md:159 | NOT a range |
| `Sxxx and Syyy` | `S009 and S010` | 10 occurrences, plain literals |
| Em-dash, `..`, ` to `, `through` ranges | none | 0 |
| Range end without `S` (`S036–039`) | none | 0 |
| Letters before: `PairS010GhpEtag…`, `ScoutReopenS096`, `ReviewS066RowTruth`, `ReopenS030` | ghp-etag-anatomy.md:62,64; ghp-served-set.md:85,87,89; robots-txt-rules.md:63,81; sitemap-orphan-audit.md:274; static-canonical-preflight.md:151,186-194 | report basenames, not citations; `\b` rejects |
| Digit before: `Correction3S010.md`, `Correction4S010`, `Rejection13S009`, `Rejection02S001`, `Rejection07S013`, `Correction6S026`, `Correction7S030`, `Correction8S030`, `Rejection10S021` | ghp-etag-anatomy.md:68-70; ghp-served-set.md:93,95; static-canonical-preflight.md:201-203 | `\b` rejects (digit is `\w`) |
| Glued to following letters/`_`/another `S` | `S010Ghp…`, `S404_SHA256`, `UncoveredS024S025.md` (static-canonical-preflight.md:198,199) | `\b` rejects |
| `S`+2 digits | none | 0 |
| Placeholder `S0NN` | claim-count-derivation.md:33; `rechecks/S0NN.json` in 9 files | letters, inert vs `S[0-9]{3,}` |
| Lowercase `s262` | none | 0 |
| Backticked `` `S262` `` | none | 0 (backticked paths contain the glued forms above) |
| Fenced code / URL / hash | none | 0 ids |
| `.json` knowledge files | accessibility-review-cards.json (55 WCAG cards, ids like "1.1.1"), freshness-pins.json, freshness-sidecar.json | 0 S-ids |
| Header lines | line 1 `source: …`, line 2 `verified-at: …` | 63 header lines (`source|verified-at|sources|cite`) carry ids; densest cite sites |

Note: the assignment's example ranges `S011–S013` and `S036–S039` do NOT exist at the base as ranges; crawl-scope-per-host.md:1 writes `S011, S012, S013` and field-performance-cwv.md:1 writes `S036, S037, S038, S039` as literal lists.

## RANGE IMPLIED IDS:
19 range occurrences (14 en-dash, 5 ASCII hyphen) over 9 distinct ranges:
| Range | Where | Size | Implied ids never cited literally |
|---|---|---|---|
| S001-S007 | publish-channels.md:2 | 7 | none |
| S001-S006 / S001–S006 | sitemap-orphan-audit.md:2,153; static-canonical-preflight.md:54,214 | 6 | none |
| S020-S027 / S020–S027 | static-canonical-preflight.md:2,241 | 8 | none |
| S028-S029 | static-canonical-preflight.md:2 | 2 | none |
| S040–S043 | pages-base-path.md:25,27,48 | 4 | none |
| S049–S052 | render-static-sites.md:19,36,71,85,130 | 4 | none |
| S098–S100 | robots-txt-rules.md:1 (`source:` header) | 3 | none |
| S078–S099 | security-txt-publishing.md:8 ("≥ 3 good cites of S078–S099", a requirement band) | 22 | **S088 S089 S090 S091 S092 S093 S094 S097** (8) |
| S120–S128 | claim-count-derivation.md:14 ("S120–S128 added") | 9 | **S121 S122 S123 S124 S125 S126 S127** (7) |

IDS ONLY IN A RANGE (not literal word-bounded anywhere): **15** — S088, S089, S090, S091, S092, S093, S094, S097, S121, S122, S123, S124, S125, S126, S127. All 15 have SOURCES.md rows. 62 of the 104 literal ids sit in no range. Range-expanding the corpus would give 104 + 15 = 119 distinct ids, but both bands are semantically loose (requirement band / "rows added"), so expansion would assert citations the entries do not make.

## HAZARDS FOR THE RESOLVER:
1. Use `\bS[0-9]{3,}\b`, not `S[0-9]{3,}`: the loose form over-counts by 1 distinct id (S404) and 32 occurrences, all inside filenames/identifiers.
2. Do NOT substitute `(?<![A-Za-z])S[0-9]{3,}`: it would accept `Correction3S010`, `Rejection13S009` (digit before) and `S404_SHA256` (no lookahead). `\b` rejects all.
3. `ids_cited` must not expand ranges. Selftest should include en-dash U+2013 and ASCII `-` range spellings, the slash pairs (not ranges), `S003-containing` (not a range), and the 15 range-only ids as "not literally cited".
4. Selftest negatives: `S404_SHA256`, `PairS010Ghp…`, `Correction3S010.md`, `UncoveredS024S025.md`, `S0NN`. Positives: `(S262)`, `[S367]`, `S367,`, `S041’s`, `S273/S274` (two ids).
5. No stripping step is needed at the base (no ids in fences, URLs, hashes, JSON); any defensive stripping must not change the 104.
6. No lowercase, `S`+2-digit or `S`+4-digit forms exist, so `{3,}` is unambiguous at the base.
7. Every cited id has a SOURCES.md row (0 dangling); 54 SOURCES rows are uncited (the 15 range-only ids are among them).
8. Heavy-tailed counts (S001 47, S011 40, S078 40, S419 31, S372 29, S052 28); newest S416 1, S417 1, S418 17, S419 31, S420 24.

## EXPECTED CITED-ID COUNT:
At base 28fa0b23e699 (corpus/knowledge unchanged since): **`ids_cited` = 104** distinct literal word-bounded ids (`\bS[0-9]{3,}\b` over `corpus/knowledge/*.md`, 1094 occurrences). Loose grep prints 105 (adds S404). Range-expanded would be 119 (not recommended). `.json` adds 0.

VERDICT: 104 literal word-bounded S-ids (loose grep 105 = +S404_SHA256); 9 distinct ranges / 19 occurrences leave 15 ids range-only; no S-ids in json/fences/URLs; glued filename hazards documented.
