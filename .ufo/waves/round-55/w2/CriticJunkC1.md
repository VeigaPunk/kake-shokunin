# CriticJunkC1
ATTACKS: C1 predicate `met: index_mismatches == 0 AND knowledge_files >= 46` at a7a548e102b71bd16b0a6ddafa469393a2c98b69 —
`.ufo/waves/round-55/c55_readme_index.py` (v2) and the C1 wording in `.ufo/waves/round-55/contract.md`;
axis declaration `calibration` in `contract.md` vs `SCORECARD.md`; harm of `corpus/README.md` fcaf4b85→a7a548e.

Scratch method: `D=$(mktemp -d) && git clone -q --no-hardlinks <lane> "$D"`, `git -C "$D" checkout -q --detach <rev>`,
verified `git -C "$D" rev-parse --show-toplevel` = `/tmp/tmp.YCkFXt3YjP`; every later git call names `-C "$D"`;
commits use `-c user.name=criticjunk -c user.email=criticjunk@local` inside `$D` only. Counter bytes copied from the
revision: `git -C "$D" show a7a548e:.ufo/waves/round-55/c55_readme_index.py > /tmp/cjc1_counter.py`, sha256
`0ffb8d31cfe5e1483a19a7913321ff6ee0af8ee12280d529d4b6e10d4ace5091` (identical to the committed blob's sha). Lane worktree
untouched; only this report written. No tools installed (nothing needed; pacman not run).

Controls I ran:
- `python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision a7a548e…` → `index_mismatches=0 knowledge_files=49 met=True`, `coverage_rows=51`, `EXIT=0`.
- same counter `--revision fcaf4b85…` → `index_mismatches=21 knowledge_files=46 met=False`, `coverage_rows=27`, `EXIT=1` (matches `controls/base-c1-readme-index-v2.txt`).

## JUNK VARIANTS:

Every row below is a real commit in `$D` and a real counter run `python3 -B /tmp/cjc1_counter.py --root "$D" --revision <rev>`.
"Human passes?" = would a reviewer accept the row set as a real description of `corpus/knowledge/`.

PASSES (counter exit 0, `index_mismatches=0`):

| id | edit | rev | counter output | human passes? |
|---|---|---|---|---|
| V10_base_junk_rows | from **base** fcaf4b85 only: append 21 rows, one per unindexed file, cell = one rare head word + `purple bananas orbit sideways <slug>` | 88fa6c3 | `index_mismatches=0 knowledge_files=46 coverage_rows=48 EXIT=0`; `git diff --stat` = `1 file changed, 21 insertions(+)` | **NO** — adds no description at all; the same 21→0 the build claims |
| V4b_five_token_rare_unique | every row's cell = 1 rare head word + fixed 4-token junk + slug (6 tokens) | cf8261f | `0 / 49 / EXIT=0` | **NO** — e.g. `absent purple bananas orbit sideways fleet-registry` |
| V1c_head_copy_clean | every cell = first 8 tokens of the file's own head (the `source:` line for 48 of 49 files), backticks stripped | 47f520e | `0 / 49 / EXIT=0` | **NO** — restates provenance, never what the entry covers |
| V2b_wrong_file_unique | every cell = **another** file's coverage paragraph, donor chosen only to share one rare word with the named file's head | 9cdcd18 | `0 / 49 / EXIT=0` | **NO** — each row describes a different entry (row for `field-performance-cwv.md` carries the Baidu paragraph) |
| V5c_junk_first_real_second | first table = V4b junk; the real 51 rows moved to `### The real map` | 710ed51 | `0 / 49 / coverage_rows=51 / EXIT=0` | **NO** — the table the counter reads is junk; two contradictory maps in one section |
| V6b_header_shift_headcopy | header renamed `| Area | Index | Notes |` (no `Entry`/`Coverage`), cells = V1c head copies | 1b8be4e | `0 / 49 / coverage_rows=52 / EXIT=0` | **NO** — fallback roles land on `Index`/`Notes`; cells are head copies |
| V7_truncate_bodies | truncate **all** knowledge bodies to their first 1500 chars; index untouched | 9e84cd5 | `0 / 49 / head_changed=0 / EXIT=0`; `git diff --stat a7a548e` = `47 files changed, 46 insertions(+), 5894 deletions(-)` | **NO** — 5 894 lines of entry content deleted; cells now describe text that no longer exists |
| V8_markdown_link_dangling | add `[old map](knowledge/ghost-index.md)` in the section | d382841 | `0 / 49 / dangling=0 / EXIT=0` | **NO** — a pointer that resolves nowhere |
| V9_second_row_per_file | keep every real row, append a second junk row per file (98 rows) | df46d8d | `0 / 49 / coverage_rows=98 / EXIT=0` | **NO** — two claims per file, the second false |
| V11_unchecked_pointers | add `` `knowledge/robots-txt-rules.md:9999-10000` ``, `` `knowledge/ghost.png` ``, `` `/corpus/knowledge/ghost.md` ``, a markdown link | 5a0f651 | `0 / 49 / dangling=0 / EXIT=0` (entry has 123 lines, `git show …| wc -l`) | **NO** — four dangling pointers, none enumerated |
| V5_second_table | all 51 rows moved verbatim into a second table; no first table | e0b0d7a | `0 / 49 / coverage_rows=51 / EXIT=0` | **YES** — benign: the rows are unchanged and the counter follows the only table |

FAILS (counter exit 1 — the v2 terms that do bite):

| id | edit | rev | counter output |
|---|---|---|---|
| V1_h1_copy | cells = first 8 head tokens **with backticks** | 8fbe734 | `dangling=1` (`corpus/knowledge/self-assessment-at-writing.md`); `thin=0` — every junk cell passed the descriptive test |
| V1b_h1_line_only | cells = literal H1 line (48 of 49 files have no `# ` line) | 4d3db38 | `thin=12 duplicate=1` |
| V2_other_file_paragraph | donor rotated without uniqueness control | 961345d | `duplicate=36` |
| V3_universal_cell | constant cell "source-backed entry with dated evidence and registry identifiers" | b61f0c6 | `thin=29 duplicate=46` |
| V3b_universal_cell_varied | same cell + `noteN` suffix (unique) | 3d63e3b | `thin=29` |
| V4_five_token_rare | rare word + junk, no uniqueness control | 01e5f2c | `duplicate=21` |
| V5b_second_table_keeps_one_row | one non-knowledge row left in table 1, 49 index rows moved to table 2 | cdfd151 | `unindexed=49 coverage_rows=1` |
| V6_header_shift | `| Area | Index | Notes |` fallback + identical cells | ced6bb7 | `duplicate=21` |

Reading of the table: the only real defences are `duplicate` (identical cells) and the incidental `dangling` hit from a
copied backtick. Once cells are made unique (V4b, V9, V2b, V10) and backticks are dropped (V1c), nothing in v2 separates
junk from description. **A change that improves nothing meets the predicate** — V10 does it in 21 lines from base with the
same 21→0 movement the build reports.

The build itself is not junk on the evidence I could check: at a7a548e the first table has 51 rows naming 49 knowledge
files, **each exactly once** (script over the first contiguous table: `rows: 51 files named: 49 twice+: {} unnamed: []`),
and spot checks match the entries — `freshness-sidecar.json` `entries: 30` (row says 30), `accessibility-review-cards.json`
list of 55 cards, `canonical-selection.md` lists exactly four variant classes (row says four), `PROVINCE.md` §Frontier
bullets do occupy lines 22–30 as the new prose says. But the build's weakest cell is `speedrun-pipeline.md` at
**5 tokens / 1 shared rare word** — the identical form as V4b's junk (measured over all 49 cells: min tokens 5, min shared 1).

## WORDING:

1. **The After clause defines "descriptive" as the proxy, and the proxy admits junk.** `contract.md` says "descriptive
   (>= 5 tokens and sharing a 5+-letter word with the entry's H1/head)". V4b and V10 satisfy that definition literally
   while describing nothing. The counter is faithful to the sentence; the sentence is not an honest-index claim. This is
   the defect, not a counter bug — and it is the same proxy the round-54 calibration score already rests on.
2. **Universal clause not enumerated: "every knowledge file is named by a coverage-map row whose coverage cell is
   descriptive".** The counter resolves a file to the *first* row that names it (`named_rows.setdefault`); later rows naming
   the same file are never thin-tested. V9 (98 rows, second row junk per file) passes. The docstring's v2 changelog claims
   "one authority per surface" was folded in from W1; no code path implements a per-file row count.
3. **Negative clause not enumerated: "no coverage-map pointer dangles".** `dangling` inspects only backticked tokens whose
   basename ends in one of 12 extensions, skips tokens with `<`/`>`/`*`, `http(s)://`, `/`-rooted, and exempts 6 protocol
   names. Not checked at all: markdown links, line anchors (`path.md:9999-10000` — the lane's most common pointer form),
   `.png/.js/.css/.pdf/...`, root-relative paths, prose paths. V8 and V11 both pass.
4. **"the file count is not below 46" cannot bite.** With base 46, `met` already requires `deleted == 0`, so
   `knowledge_files >= 46` is logically implied by the other conjunct. The shrinkage guard advertised in the sentence is
   dead weight; the real shrinkage exposure is V7 (content deleted below the 1500-char `head_changed` window).
5. **Terms in `index_mismatches` are not in the sentence.** `duplicate` and `head_changed` are counted but appear in no
   clause of the After sentence; conversely the sentence's "no pointer dangles" is only partly implemented. One printed
   integer cannot tell a reader which clause was actually enforced, and the receipt prints only that integer.
6. `MAX_FILES_PER_ROW = 2` lets one coverage cell stand for two files (selftest `pass_two_files_one_row`) — one description
   for two claims, not forbidden by the sentence.

## AXIS/HARM:

- **Is `calibration` honestly the lowest non-retired axis?** Yes, per `SCORECARD.md` at a7a548e: axis table lines 17–19 read
  `operability | 10`, `freshness | 10`, `calibration | 1`; line 5–6 puts depth/coverage/adjacency "outside this lane's
  scored ownership"; line 114 states "The two owned axes themselves are NOT retired". So 1 is the lowest scored, non-retired
  axis, and the contract's disclosure (sub-axis added in round 54, not in the prompt's axis list, ownership left to the
  operator) is accurate. Caveat that follows from the above: the C1 movement this round is on a lane-authored sub-axis and
  does not improve either prompt axis, and the number it moves (21→0) is reproducible by V10 junk — so `21→0` is
  necessary-only evidence and must not be cited as a calibration improvement on its own.
- **No pre-existing row changed.** `git diff --numstat fcaf4b85 a7a548e -- corpus/README.md` → `84	0`; the only `-` line in
  `git diff … | grep -c '^-'` is 1 (the diff header). Additive only: no existing coverage row was rewritten.
- **Operability harm: none observed.** No script reads `corpus/README.md` (`grep -rn "corpus/README\|README.md" scripts/*.mjs
  scripts/*.py` → one comment hit, `scripts/probe-delta.mjs:5`); `scripts/corpus-contract.mjs` mentions neither README nor
  coverage. The added second table does not disturb the counter (it is explicitly outside the index and its backticked
  pointers are still checked).
- **Freshness exposure the edit creates:** the new "Frontier ground map" rows are prose row-sets (`S011–S013`, `used-by`
  claims) that this counter cannot see at all, and the section's line-anchored pointers are unchecked (WORDING 3). Those
  are C2/reviewer surfaces, not C1 surfaces — a green C1 must not be read as freshness evidence for them.
- No credential material, session tokens or private URLs were used or written.

**Smallest safe correction (my recommendation, not an edit):** do not treat `index_mismatches == 0` as an honest-index
proof this round; the receipt label and the report should call it a structural necessary condition. Cheapest term additions
for round 56, each with no false positive on the real build: count rows naming a file more than once; check markdown-link
and `path:line` anchors; hash the whole entry body instead of 1500 chars. The semantic clause cannot be repaired by a
one-word proxy — it needs a reviewer gate over the added rows (21 this round), which is what actually distinguishes the
build from V10.

VERDICT: C1 is met at a7a548e and the build's own rows are real descriptions, but the frozen predicate is satisfied by
changes that improve nothing — 10 junk variants pass, including a 21-line junk addition from base scoring the same 21→0 —
so the predicate proves structure, not an honest index.
