# SimplifierBuild
ATTACKS: surplus added by round 55 at `a7a548e` — `assimilation/validate/` (153 files, 2,589,070 B), the 51 README coverage-map rows and the 21-row Frontier ground map, prose inside the three new Yahoo entries, and wave-1 scaffolding (`make_spec_w1.py` outputs, `w1.ready*`, `w1-validator.err`, `__pycache__`).

Method: committed bytes only (`git show`/`ls-tree` at `a7a548e`); every mutation was applied in a throwaway clone (`git clone -q --no-hardlinks` → `/tmp/simp55-axsnd0ae`; `git -C /tmp/simp55-axsnd0ae rev-parse --show-toplevel` = `/tmp/simp55-axsnd0ae`). The lane was not edited; this file is my only write. No tools installed. No `lsp` device is mounted in this session (`read xd://lsp` → `No such tool: xd://lsp`), so caller evidence below is literal reading of both counters and of `scripts/sources-census.sh`, not semantic reference resolution; it is not presented as semantic proof.

## CANDIDATES:

### C-1 `assimilation/validate/` — delete 90 of 153 files, 1,330,915 B (51.4% of the mirror)
- Size: mirror 153 files / 2,589,070 B = 77.9% of the round's 223 files / 3,323,461 B (`git ls-tree -r -l a7a548e .ufo/waves/round-55` → `files=223 bytes=3323461`).
- Consumers, measured, not assumed: `c55_quote_truth.py` C7 reads **5** paths — `validate/corpus/SOURCES.md`, `census-argv.txt`, `census-stdout.txt`, `census-exit.txt`, plus the 3 scratch entries (`grep -n 'VALIDATE'` → `VALIDATE_REG` used only at lines 436/460/465/584/586). Nothing enumerates the tree. A census re-run needs existence of the **58** distinct `used-by` paths of the 126 `mined` rows, because `usedby_findings()` tests `[ ! -e "$dir/$path" ]` with `dir = realpath(dirname(file)/..)` (`scripts/sources-census.sh:501,567`).
- Minimum that keeps both green: 63 files / 1,258,155 B = 58 used-by copies (1,111,367 B) + registry 145,418 B + 4 census receipts 1,370 B.
- Deletion shape: 70 `corpus/lessons/` 813,679 B; 15 `corpus/knowledge/` 357,836 B (largest `accessibility-review-cards.json` 163,613 B — no row names it as `used-by`); `corpus/QUALITY.md` 98,742 + `corpus/README.md` 46,134; 2 handoffs 8,444; `corpus/quality/citation-adjudications.md` 6,080.
- Verification stays green (run in the clone): after deleting the 90 files and committing `c7fc2d3`,
  `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root /tmp/simp55-axsnd0ae --revision c7fc2d3` → `C2 quote-truth 8/8 met=True … EXIT=0`;
  `… c55_readme_index.py …` → `index_mismatches=0 knowledge_files=49 met=True`;
  `scripts/sources-census.sh validate --file <clone>/…/validate/corpus/SOURCES.md` → exit 0, 15 stdout lines identical to the committed receipt modulo the path (`file<TAB>ok<TAB><path>`, same 14 `W04`).

### C-2 counter-only floor — 8 files / 169,181 B — REJECTED
Deleting down to what C7 literally reads keeps `C2 8/8 met=True`, but the census re-run then returns exit 1 with **203** `E11 missing used-by` findings (`S001 missing used-by corpus/knowledge/ghp-served-set.md`, …). That breaks C7's stated re-run discipline, so 63 files is the floor, not 8.

### C-3 README coverage cells — 4 trims, 128 B net, all green
Rows whose Coverage cell echoes the entry's H1 (measured: content-word overlap of the cell with H1+1500-char head, `words()` as the counter defines it):

| row | cell tokens | shared H1 words | proposal | net |
|---|---|---|---|---|
| `baidu-friendly-crawl-guidance.md` (S329) | 31 | 7/15 = 0.47 — highest in the map | delete the opening `Baiduspider robots scope: a block on that agent binds the desktop and mobile crawlers; ` — the H1 is `A Baiduspider robots block binds the desktop and mobile crawlers at once` | −87 B |
| `yahoo-japan-robots-txt-refusal-rules.md` | 10 | 3/9 = 0.33 | `root placement, directory scope,` is the H1 verbatim (`…: root placement, directory scope, case`); drop both phrases and keep one head word (`directory scope` moved to the end) | −16 B |
| `yahoo-japan-robots-pattern-syntax.md` | 13 | 2/7 = 0.29 | `prefix versus end marker,` restates the H1 (`The end marker is what stops a path rule from matching as a prefix`) | −6 B |
| `yahoo-japan-robots-txt-basics.md` | 22 | 2/14 = 0.14 | `request channel` restates the H1 (`robots.txt is a request channel …`) | −19 B |

Verified in the clone (`8ebe547`, `f4b56e9`, `541c667`, `0bddbc0`, final state `639fd78`): C1 `met=True`, `thin=0` after each step. The baidu clause goes as a **pure** deletion (`fc8ecda` keeps the original row minus exactly that clause → `thin=0`, `met=True`). **Pure** deletion is not available on the other three: deleting the refusal row's echo outright (`| absent-file negation, case-sensitive names, meta-tag fallback |`) gives `thin=1` and `met=False` (`074808b`), because the `thin` term needs ≥5 tokens *and* a 5+-letter word shared with the head. The H1 echo is the counter's price; the other three trims pay it with a different head word. Net saving is small (128 B) — this is a wording finding, not a size one.

### C-4 Duplicated sentences inside the three entries — 6 deletions, 664 B, C2 stays 8/8
Sentence pairs that say the same thing (all in prose, no quoted span touched, so C5 is untouched):

| id | file | pair |
|---|---|---|
| P1 | refusal-rules | "Nothing about any crawler's live behaviour: no robots.txt was served, no crawl was observed, and no directive was tested against a crawler." ↔ "Scope note: … No robots.txt was served, no crawl was observed, and no directive was tested against a crawler." |
| P2 | refusal-rules | "Every statement above is about what the page says." ↔ "Scope note: a claim about what the operator's documentation states." |
| P3 | pattern-syntax | "Nothing about whether any live crawler implements this syntax as written; no robots.txt was served and no crawl was observed." ↔ "Scope note: … no robots.txt was served and no crawl observed." |
| P4 | pattern-syntax | "Case." bullet: "S373's table states no case rule for either symbol, and the page carries no section on upper and lower case at all." ↔ "No case rule for `*` or `$`; the page is silent (see above)." |
| P5 | basics | "the page states no status code, no redirect, no fetch failure, no cached copy [S418]" ↔ "No HTTP-status, redirect or caching rule; …" |
| P6 | basics | "the lane's scope is the service (protocol, authority, port)" ↔ "[INFERENCE] Reading サイト as the RFC's service (scheme, host and port) is the lane's mapping…" |

Not duplicates, kept: the five "Contrast with the RFC side" paragraphs (same template, different content); `prefix` vs `containment` in pattern-syntax (the bullet does RFC-comparison work); the `ground:` header line (provenance). The three Scope-note trailers are near-identical to each other, but nothing in `SKILL.md` mandates them (`grep -i 'scope note'` → only a round-46 heading), so the cheap fix is dropping the in-body duplicates, not the trailers.
Verification: `d8839f0` → `C2 7/8 met=False` with `C7 FAIL — S372/S373/S418: validated scratch entry differs from the landed entry`; after copying the three edited entries into `validate/corpus/knowledge/` (what `validate_append.sh` does) `20c444d` → `C2 8/8 met=True`, C1 `met=True`.

### C-5 Ground map — table 2,374 B — no deletion proposed (contract), one wording fix
- Consumer: **no counter**. The section is 4,322 B; the table is 23 lines / 2,374 B. Removing the table alone (`80a7bf2`) leaves `index_mismatches=0 … dangling=0 met=True`, under the committed v2 counter *and* under the in-flight worktree edit. Of the 28 extension-bearing backtick tokens the table contributes, 5 appear nowhere else in the section (`PROVINCE.md`, `corpus/SOURCES.md`, `corpus/lessons/round-39.md`, `corpus/lessons/round-53.md`, `scripts/sitemap_audit.py`) and all 5 resolve, so `dangling` never depends on the table (observed `dangling=0` after removal).
- Why it stays: `contract.md` C1 names it as the implementation of considerthese proposal 4. Deleting it would remove a mandated artifact, not surplus.
- Real defect found instead: the intro says "One row per `PROVINCE.md` §Frontier ground … (`PROVINCE.md:22-30`)", but `PROVINCE.md:22-30` names **5** items while `grep -c '^## ' PROVINCE.md` = **21** headings, including `Round-34 link-preview frontier step` (:158) and `Round-35 security.txt publishing frontier step` (:202) — the only places rows 19 and 20 are declared "held Frontier ground". Five rows (r7 sitemap, r48 js-rendering, r48 dynamic-rendering, r50 crawl-error, r28 field performance) have no PROVINCE section of their own at all. Fix the citation to the sections the rows actually use; do not delete rows (rows 2, 12, 13 carry repair/supersession dating `r37; repaired r38` / `locators superseded r53` that the coverage map does not hold).

### C-6 Wave-1 scaffolding — merge candidate, no counter reads it
`git ls-tree -r --name-only a7a548e | grep -iE '__pycache__|\.pyc$'` → **empty**: no compiled leftovers at the measured revision, nothing to delete there.
- `w1-dispatch.json` 76,784 B duplicates `w1-spec.json` 63,933 B: all 40 `taskCall.tasks[i].task` strings start with `items[i].prompt` (40/40) and differ only by one of **2** suffix shapes ("Lane bounds: … Report: write your scoped findings to <reportDir>/<Name>.md"), 5,342 B total. 58,257 B of spec prompt text reappears verbatim inside the 63,679 B of dispatch task text (similarity 0.957 on a sample). Neither counter reads either file (`grep -n 'w1\|spec.json\|dispatch'` in both counters → only docstring mentions).
- Proposal (merge, not delete): dispatch records name + report path + spec digest, or the spec keeps prompts and dispatch keeps names/agents/timestamp. Saves ~58 KB per wave. Tradeoff: the suffix template lives only in the fleet dispatcher, so the "what was sent" record would then depend on fleet tooling; `history://` transcripts are the independent witness.
- `w1-validator.err` is **0 B** with no reader: delete or keep at zero cost. `w1.ready` 156 B / `w1.ready.dispatched` 20 B: the timestamp `2026-10-25T17:45:02` is order evidence — keep.
- `make_spec_w1.py` 26,792 B: keep (only record of how the spec was built; reads an external read-only tree, so the spec is not byte-reproducible).

## KEEP:
| path | bytes | why |
|---|---|---|
| `assimilation/pre-append/corpus/SOURCES.md` + `mirror-pin.json` | 144,364 + 362 | C8 pins sha256/rows and requires the add-commit to be an ancestor |
| `assimilation/validate/corpus/SOURCES.md` | 145,418 | C7 requires byte-equality with the landed registry |
| `validate/corpus/knowledge/yahoo-japan-robots-*.md` | 9,630 + 7,471 + 5,292 | C7 requires byte-equality with the landed entries (observed to fail otherwise) |
| `validate/{SCORECARD.md,SKILL.md,scripts/source_recheck.py,.ufo/waves/round-41/*}` | 545,649 | the 5 non-corpus `used-by` targets — E11 existence only |
| `w1/*.md` reports | 39 files / 314,288 | seat evidence; C7's docstring relies on them for the wave-2 attacks |
| `sources/{S372,S373,S418}.html` + `receipts.json` | 27,129 + 926 | C5/C6 quote truth and receipt pins |
| `assimilation/{collisions,reg-ids,staged-ids,quarantine-slice,guard-proof/*}` | 1,966 | contract's id-collision guard proof; read by reviewers, not counters |
| `c55_readme_index.py` + `c55_quote_truth.py`; `contract.md` + `contract.json`; `controls/*` | 61,360; 7,952; 7,241 | frozen predicate and do-nothing controls |

## RISK:
1. **The mirror trim is undone by the next re-run.** `validate_append.sh:9-10` does `rm -rf "$V"; …; cp -r corpus "$V/corpus"`, so trimming the committed mirror without changing the script buys one commit only. Required pair: derive the copy set from the `mined` rows' `used-by` cells (plus the 3 entries and 4 receipts) instead of `cp -r corpus`. A missing `used-by` target then fails the copy step loudly instead of silently shrinking — equivalent or stronger than today's E11.
2. **The mirror is not a snapshot.** Of the 58 used-by copies, 57 are byte-identical to the landed files and `SKILL.md` differs (`mirror=136469 landed=139515`). E11 tests existence only, so stale bytes are harmless to C1/C2 — but any reader who treats `validate/` as a frozen copy of the revision is wrong.
3. **Symlink shortcut rejected.** Pointing `validate/corpus` at `../../../../corpus` would satisfy E11 and cut the floor to a handful of files, but it makes the scratch entries identical to the landed entries by construction, so "validated before the append" becomes unfalsifiable. Not proposed.
4. **C7 couples any entry edit to the mirror.** Any prose edit to the three entries fails C7 until the three scratch copies are re-synced (observed `7/8`), i.e. the dedup in C-4 must land before the final validate run or be followed by one.
5. **Counter edited after the measured revision.** The worktree carries an uncommitted `M .ufo/waves/round-55/c55_readme_index.py` (+34/−11: `head_changed` now compares the whole base text as a prefix, `EXTS` widened, `TOKEN_RE` also scans `](path)` links, `LINESUFFIX_RE` strips `:NNN`). My greens were re-tested under that file too (`c55_readme_index_wt.py` at `639fd78` and `80a7bf2` → `met=True`, `dangling=0`), but a counter changed mid-wave needs the contract's "repaired in code and disclosed" line to hold.
6. **Wording-level findings dominate.** Beyond the mirror, the round's surplus is 128 B of README cells + 664 B of entry prose + 58 KB of spec/dispatch duplication; the three entries (22,393 B) are dense, and the ground map is duplicated *data* but mandated. Anyone expecting a second large deletion will not find one.

VERDICT: one real deletion — 90 of the 153 mirror files (1,330,915 B, 51.4%) go with C2 still 8/8, C1 met and the census re-run byte-identical; 8 files is the counter-only floor but breaks the re-run (203 E11). Everything else this round adds is small-surplus: 128 B of H1-echoing cells (pure deletion fails `thin` on 3 of 4 rows), 664 B of duplicated entry sentences (green after the mandatory scratch re-sync), and a 58 KB spec/dispatch duplication that is a merge, not a delete.
