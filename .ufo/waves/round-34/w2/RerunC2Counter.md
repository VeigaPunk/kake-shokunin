# KakeR34 wave-2 — RerunC2Counter

Attacked: re-ran the C2 source-census counter in a sandbox clone at the four
declared revisions and diffed every JSON field against the L1's receipts.

## Setup (sandbox only; lane untouched)

- `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r34/w2/RerunC2Counter/clone`
- `git -C <clone> checkout -q 24a16474ee73e20453f3e1be9d2f33573c5196d9` → HEAD 24a16474
- `TMPDIR=/fast/scratch/hyaku/kake-r34/w2/RerunC2Counter/tmp`; `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE`
- Outputs: `/fast/scratch/hyaku/kake-r34/w2/RerunC2Counter/out/{1e54c895,d08d8de2,9ef758c9,24a16474}.json` (+`.err`, `24a16474-b.json`)
- Tools installed: none. System `python3`, `git`, `lzma` module only.

## Commands

For each `<rev>`:
`python3 -B <clone>/.ufo/waves/round-34/c2_source_census.py --root <clone> --revision <rev>`

Exit codes: 1e54c895→1, d08d8de→1, 9ef758c→0, 24a1647→0. stderr per run is the
one-line `C2 <met>/5 at <rev>` summary; stdout is the JSON report.

Field-by-field diff (recursive dict/list walk of stdout vs
`.ufo/waves/round-34/verification/c2-at-*.json`, compared after rewriting
`revision` to the full sha): **0 differences on all four revisions**, including
`counterSha256`, `controlBroken`, every `ids[].checks.*`, every `quote` string,
and the whole `census` block.

## Per-revision table

| rev | exit | met | controlBroken | S067..S070 checks a,b,c,d | census derived | census stated | equal to receipt |
|-----|------|-----|---------------|--------------------------|----------------|---------------|------------------|
| 1e54c895 | 1 | 0/5 | false | all 4 ids: a,b,c,d all false; quote null | derived=null, why="retained tree or archive missing" | statedLines=0, stated=null | YES (0 diffs) |
| d08d8de | 1 | 0/5 | false | all 4 ids: a,b,c,d all false; quote null | {102,87,87,1,87,1,87}, why="ok" | statedLines=0, stated=null | YES (0 diffs) |
| 9ef758c | 0 | 5/5 | false | all 4 ids: a,b,c,d all true; quotes match receipt text verbatim | {102,87,87,1,87,1,87}, why="ok" | statedLines=1, stated=derived | YES (0 diffs) |
| 24a1647 | 0 | 5/5 | false | all 4 ids: a,b,c,d all true; quotes match receipt text verbatim | {102,87,87,1,87,1,87}, why="ok" | statedLines=1, stated=derived | YES (0 diffs) |

Census key order: pages, og:title, og:type, og:image, og:url, all-four,
og-url-equals-canonical → 102, 87, 87, 1, 87, 1, 87 at every rev where the
retained archive exists (d08d8de onward).

## Counter byte identity

`git -C <clone> show <rev>:.ufo/waves/round-34/c2_source_census.py | sha256sum`

- 1e54c895: path absent in that commit (counter landed at d08d8de; the counter
  reads it from `__file__`, i.e. the working-tree copy — consistent with the
  receipt carrying `counterSha256` ee7461b9… even for the base rev).
- d08d8de, 9ef758c, 24a1647, and the checked-out working tree: all
  `ee7461b9e3a33949174591c527ccbf2854ca178c41638f71b5128cbd57e5f892` — byte-identical
  to d08d8de's version and equal to `counterSha256` in all four receipts.

## Determinism / extra probes

- Rerun at 24a1647: `cmp` identical to first run; exit 0.
- Critic-hollow rev 0cce15f is **not an object in the lane clone**
  (`git cat-file -t` → "Not a valid object name"); it lives only in the retained
  bundle, so `c2-at-critic-hollow-0cce15f.json` cannot be re-verified from this
  root. Not re-run (wave-1 already disclosed it as a transcription pass; the
  counter is declared necessary-not-sufficient).
- Counter reads committed bytes only via `git show` (lines 83-86, 194-245);
  no network, no working-tree reads besides `__file__` for its own sha.

## Findings

- **None adverse.** The counter is deterministic, byte-stable across
  d08d8de→24a1647, and all four receipts reproduce exactly — field by field,
  including quotes, check booleans, derived census numbers, exit codes, and the
  `C2 m/5` stderr line.
- Receipt `c2-at-1e54c895.json` reflects "tool from working tree, revision from
  --revision"; my run reproduces that framing exactly (same counterSha256
  recorded at a rev where the file did not yet exist). Consistent, not a defect.

## Not verified / residual risk

- Whether the census numbers are *correct for upstream ds4cc* (only that
  stated==counter-recount; the recount code was read, not independently
  re-derived — other seats cover the retained bundle vs upstream).
- The 0cce15f critic-hollow receipt (commit absent from clone, as designed).
- No tool installs; no pacman transaction attempted (host-wide pause).
