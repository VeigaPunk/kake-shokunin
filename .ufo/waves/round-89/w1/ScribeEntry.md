# ScribeEntry — round 89 C2 knowledge entry and registry row (lane-internal)

Seat: ScribeEntry (leaf scribe, no subagents). Writes: `.ufo/waves/round-89/w1/ScribeEntry/` and this file only. No `corpus/`, `scripts/`, `PROVINCE.md`, `SOURCES.md` or git mutation. No commit, push or fleet-repo write.

Candidates: `w1/ScribeEntry/cache-key-construction.candidate.md` (entry) and `w1/ScribeEntry/sources-row.candidate.md` (row). Receipts: `w1/ScribeEntry/receipts/`.

## 0. The state the seat found

The entry and rows this seat was asked to draft had already landed at HEAD `acc69ba5` before this seat's draft: `corpus/knowledge/cache-key-construction.md` (commits `08ce630d`, `acc69ba5`), rows S464 and S465 in `corpus/SOURCES.md`, `scripts/cache_key.py` (sha256 `3a658326…`), and a PROVINCE section at `PROVINCE.md:703`. The seat therefore audited the landed version and drafted corrections. It did not draft a parallel copy.

## 1. Findings, by severity

### F1 — High: S464 duplicates S463 on the same section 4.1

S463 (already in the registry, `corpus/SOURCES.md:210`) is the §4.1 row at `https://httpwg.org/specs/rfc9111.html#caching.negotiated.responses`. Its `teaches` cell covers the reuse sentence, the three transformations, the absence sentence and the wildcard sentence. S464 (landed) cites the same section, with the same three sentences, from `https://www.rfc-editor.org/rfc/rfc9111.txt`. The two URLs differ, so the census does not reject the duplicate; it reports W04 (`S463` and `S464` both listed as "duplicate url … across scopes").

Recommendation: remove S464 and cite S463 from the entry. Keep S465, which covers RFC 9110 §5.6.2 and §5.6.1.2 that no existing row cites in a matching scope.

### F2 — Registry URL status (the spec asked for this check)

- `https://httpwg.org/specs/rfc9111.html` (§4.1 anchor): already held as **S463**. Superseding form: cite S463.
- `https://www.rfc-editor.org/rfc/rfc9111.txt`: already held as **S456** (scope: §3, §4, §4.2, §4.3). Different scope from §4.1, so no E04. The candidate S464 row only adds a W04.
- `https://www.rfc-editor.org/rfc/rfc9110.txt`: already held as S033 (media-type scope), S028 (URI scope) and S453 (§5.6.7 scope). S465 is a fourth scope, distinct from each.
- Highest id at base `76225160`: **S463**. Next free: **S464**. At HEAD: S463, S464 and S465 present.

### F3 — Medium: landed entry does not carry the required `## Limits` heading

The landed section is `## What this entry does not establish` (HEAD line 165). The candidate renames it to `## Limits` and opens it with the key-construction-only sentence the spec requires. The content otherwise carries over, plus a new bullet on the counter gaps in F6.

### F4 — Medium: landed entry's quote line ranges are wrong or loose

Checked with `scripts/quote_class.py` against the committed `L1/src` bodies (`receipts/quote-classes-candidate.txt`):

| Quote | Landed says | Actual | Class |
|---|---|---|---|
| reuse sentence | lines 530–535 | 530–532 (line 535 is blank) | collapsed-only |
| wildcard | paraphrase in backticks, lines 555–557 | not blockquoted; sentence is 556–557 | (not a quote) |
| tokens | lines 1730–1738 | 1730–1731 (production at 1733) | collapsed-only |
| empty elements | lines 1695–1699 | 1696–1697 | collapsed-only |

The candidate blockquotes all four with exact lines, ≤25 words each (9, 24, 17, 12, 13 words), and states the class of each span (raw or collapsed-only). The title span is a raw substring at line 526; note that the same title text also occurs at line 82 in the table of contents, so it is not page-unique.

### F5 — Medium: the fourth separator is named nowhere in the landed entry

The landed entry says ESC escapes "the four separators with `%1C`, `%1D`, `%1E` and `%1F`" (HEAD line 87), but its layout names only U+001F, U+001E and U+001C. U+001D is escaped by `scripts/cache_key.py` and by the counter's reference, but no document names it. The contract (`c2-contract.md`) has the same gap, and `ReviewCounterC2` finding 6 routed it. The candidate names U+001D by code point and says it has no structural role. The contract's own name "GS" for U+001C is also not ASCII (ASCII GS is U+001D); the candidate keeps the contract's name and gives the code point beside it. **Decision for L1:** whether U+001D stays in the escape alphabet should be decided in the contract, not here.

### F6 — High: the C2 counter does not measure seven contract rules (counter defect, confirmed by probe)

`receipts/probe_counter_gaps.py` applies single-point mutants to the counter's own REFERENCE and scores each with `score_candidate` (seed 89089). Output: `receipts/counter-gap-probe.txt`, `summary: mutants=10 killed=3 survived_met_true=7`.

| Mutant (contract rule weakened) | Counter result |
|---|---|
| duplicate `Vary` member accepted | met=true |
| non-empty non-token `Vary` member accepted (`a b`) | met=true |
| empty header name accepted | met=true |
| CR alone in a value accepted | met=true |
| URI not percent-escaped | met=true |
| header name not escaped | met=true |
| U+001D not escaped | met=true |
| *killed:* value not escaped; absent equals empty; `vary` not a string | met=false |

The landed script refuses or escapes every one of the seven on the probed inputs (`receipts/landed-script-probes.txt`, `receipts/landed-script-name-and-cr-probes.txt`): duplicate `a,A` → `invalid_input: duplicate vary member`; `a b` → `vary member is not a token`; empty header name → `header name is not a token`; CR → `header value contains CR or LF`; `u`+`a%b` → `u\u001fa%25b\u001ex`; `x\u001dy` → `x%1Dy`. So the production script is right on these inputs and the counter cannot show it. The counter's own gate therefore overstates its coverage. It is not the production code that fails.

Two mutants in my first probe run had malformed anchors (duplicate-`Vary` and URI-escape). They were fixed and re-run; the table above is the corrected run. The first run's rows are not evidence.

The `ReviewCounterC2` finding 2 (guard defeated by string construction) and finding 3 (hybrid table) are not re-tested here.

### F7 — Medium: the counter's mutant-kill rate is a property of the population, not the contract

The seven survivors are all rules whose inputs the 200-pair population never generates (empty name, duplicate member, non-token non-empty member, URI with `%`, name with `%`). The frozen cases do not cover them either. Adding these as frozen refusals or adding a generator class is the repair; this seat does not write the counter.

## 2. Province scope check (PROVINCE.md)

The scope test is whether the ground is admitted. Quotes from `PROVINCE.md` at HEAD:

- Line 3, Domain: "**Domain:** web properties & publishing — scopes ds4cc.com, kimi.page/pro mirrors, Pages deploys"
- Line 5, Owns: "**Owns:** the domain knowledge, playbooks, error patterns, and checklists above."
- Lines 697–698 (Round 87): "missing-Date handling, cache storage/reuse permission, Vary/Pragma, browser/runtime behavior and publication remain outside this capability."
- Lines 705–708 (Round 89, the line that admits this ground): "`scripts/cache_key.py` and `corpus/knowledge/cache-key-construction.md` (S464, S465) add offline construction of the stored-response key a presented request maps to under a `Vary` field … This is the construction half of RFC 9111 §4.1 only."
- Lines 711–712: "The instrument does not yet establish conformance to the whole contract … so the ground is recorded as held-but-unadmitted."

Verdict: **conditional, not admitted.** The Domain line covers publisher-side web properties; a cache's key construction is cache-side behaviour, which the Round 87 sentence at 697 explicitly keeps out ("Vary/Pragma … remain outside"). The Round 89 section admits the ground only as held-but-unadmitted, which is consistent with the Frontier rule "ground moves to Core only with source-backed entries and a gate": the gate exists but does not establish the contract (F6). L1 should decide whether the round-89 section's wording is an admission or a hold before integrating. This seat recommends the hold wording stands and that no Core line is added.

## 3. The row: candidate, and why the spec-shaped row is not recommended

`sources-row.candidate.md` is the spec-shaped S464 row (11 cells, tier A, kind spec, status mined, used-by `corpus/knowledge/cache-key-construction.md`). Tested in a scratch copy of the base registry with the row inserted after S463: 13 fields per row; non-E11 E-lines 0; one W04 for S464 (duplicate URL across scopes). It is not recommended, because F1 shows the §4.1 ground is already a registry row. Recommended integration: no S464 row; the entry cites S463 for §4.1 and S465 for §5.6.

## 4. Candidate entry — what changed from the landed version

`cache-key-construction.candidate.md` keeps the landed structure and decision table and makes these changes: `## Limits` heading (F3); exact quote lines and classes (F4); U+001D named by code point (F5); the wildcard as a blockquote with its exact lines; the source trio cites S463 and S465, not S464; the verified-at line records this seat's re-fetch and `cmp` result; a Limits bullet stating the counter gaps (F6). Worked examples A, B and C name the separators by code point (U+001F, U+001E, U+001C) with their expected keys.

Verified on the candidate:
- trio present in the first 8 lines (`source:`, `verified-at:`, `recheck:` non-empty), plus `ground:` and `scope:`;
- `scripts/corpus-contract.mjs` in a scratch root holding only the candidate: no finding for `cache-key-construction`;
- all five blockquotes classified with the lane's tool (`receipts/quote-classes-candidate.txt`, all exit 0);
- checklist item 4: `python3 -B .ufo/waves/round-89/c89_key.py --selftest` prints `selftest: 43/43 passed`, exit 0 (`receipts/c89_key-selftest.txt`).

## 5. Census (lane root, HEAD)

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-11-04 --root /home/vgpnk/Projects/shokunin /home/vgpnk/Projects/shokunin/kake-shokunin` → exit 0, 0 E-lines, 27 W04-lines (base `76225160`: 25). The two new W04 lines are S464 and S465 (`receipts/census-validate-HEAD.txt`). Census counts at HEAD: rows 203, tier A 178, B 8, C 17; mined 173, queued 8, rejected 22 (`receipts/census-counts-HEAD.txt`).

Note on file-mode runs: `validate --file` resolves `used-by` against the parent of the file's `corpus/` directory; in scratch roots this reports 267 E11 lines from unrelated rows. I excluded E11 from those runs and report non-E11 codes only.

`corpus-contract.mjs --root` at HEAD reports three findings, all in `corpus/knowledge/meta-robots-directives.md` (missing `source:`, `verified-at:`, `recheck:`). That entry is not this seat's and is not touched.

## 6. Deviations from the seat spec (stated, not silent)

- The spec asked for one row. Landed has two (S464, S465). This seat keeps S465 and recommends dropping S464 (F1).
- The spec asked for the entry at `corpus/knowledge/cache-key-construction.md`. It exists at HEAD. This seat wrote a candidate in its wave directory and did not edit `corpus/`.
- The spec's `## Limits` heading was absent in the landed entry (F3).
- Own GET: the two rfc-editor URLs are named in the sibling ScoutRFC item, not in this seat's item. ScoutRFC had not published, so this seat fetched them once each (plain unauthenticated curl; status 200; 84477 and 502941 bytes; sha256 match the committed `L1/src` copies by `cmp`). Receipt: `receipts/rfc-get-receipt.txt`.
- Two small files were written to `/tmp` (`/tmp/o.txt`, `/tmp/e.txt`) during one landed-script probe and removed the same minute. The spec forbids writing a tree under `/tmp`; these were files, not a tree, and are disclosed.

## 7. Quotes used by the candidate (exact text, classes in receipts)

- §4.1 title, line 526 (raw substring; also line 82 in the TOC).
- §4.1 reuse sentence, lines 530–532 (collapsed-only): "the cache MUST NOT use that stored response without revalidation unless all the presented request header fields nominated by that Vary field value match"
- §4.1 wildcard, lines 556–557 (collapsed-only as one span; each physical line raw): "A stored response with a Vary header field value containing a member "*" always fails to match."
- §5.6.2 tokens, lines 1730–1731 (collapsed-only): "Tokens are short textual identifiers that do not include whitespace or delimiters."
- §5.6.1.2 empty elements, lines 1696–1697 (collapsed-only): "A recipient MUST parse and ignore a reasonable number of empty list elements"

## 8. Tools

No tool installed, upgraded or removed. Only `curl`, `git` (read-only), `python3` (stdlib), `node` and `bash` were used. Pacman was not touched.

## 9. Scratch

`/fast/scratch/hyaku/kake-r89/ScribeEntry/` held the two RFC bodies, flat renderings, the landed script copy, probe work directories and the scratch lane root. Every receipt was copied into `w1/ScribeEntry/receipts/` before the directory was deleted.

## 10. Hand-off for L1

Integrate: (a) cite S463 and S465 from the entry, remove S464; (b) replace the landed entry with `cache-key-construction.candidate.md` after L1 decides F5 (U+001D) and F6 (counter gaps); (c) decide the PROVINCE wording at F-section 2; (d) the counter repair (F6, F7) belongs to the counter seat, not here.

Checks L1 should run once after integration: `python3 -B scripts/sources-census.sh validate` at the lane root (expect 0 E, W04 back to 25 after S464 is removed); `node scripts/corpus-contract.mjs --root .` (expect only the meta-robots-directives findings); the counter selftest.
