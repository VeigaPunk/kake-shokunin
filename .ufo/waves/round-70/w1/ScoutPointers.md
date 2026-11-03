# ScoutPointers — C1 pointer population, SCORECARD @ e5f6fd9e

Lane `/home/vgpnk/Projects/shokunin/kake-shokunin`; base `e5f6fd9e4c243d092160bc74e8bea24256087173`. Leaf scout, no subagents, no installs, no tracked file touched.

## Base bytes
- `git show e5f6fd9e:SCORECARD.md`: 4727 lines, sha256 `e11f211840de2ea483e82179a194454c2b2a1a1eda92313dbd0695794330b902`, blob `1ac34091f170d50849c52911aac21996378d2853`.
- `grep -c 'Pointer calibration'` → `0`, exit 1: no annotation section at base, so U0 = every dangling token.

## Method
C1's three regexes applied line-by-line to the committed bytes; dedupe `(class, token)` keeping first line. Repo status = `git cat-file -e e5f6fd9e:<path>` (exit 0 resolves). Home/tmp = `test -e` after `~`→`/home/vgpnk`; spellings exact, `~/projects` and `~/Projects` are distinct tokens, both checked.

## Totals — `python3 -B final_enum.py` → `unique: 348 per-class: {'repo': 333, 'home': 6, 'tmp': 9}`; `dangling: 19`
- repo 333: resolves 325, dangling 8. home 6: exists 3, missing 3. tmp 9: exists 1, missing 8.
- **Expected base unannotated U0 = 19** (8 repo + 3 home + 8 tmp); per unique token, no cross-class collisions.

## Dangling repo (8)
- L89 `.ufo/charter-scribe/ledger.jsonl` — absent from base tree and full history (`ls-tree -r | grep -i ledger.jsonl` → none).
- L1583 `scripts/sources-census.sh` — absent in lane; exists at fleet root (35466 B, mode 755).
- L2357 `.ufo/waves/round-39/r38w2-evidence.SHA256S` — regex truncation; real `.SHA256SUMS` resolves.
- L3451 `.ufo/waves/round-44/verification/before-v4.json` — command `--out` target, never committed (tree-wide grep → none).
- L3456 `.ufo/waves/round-44/verification/after-v5.json` — same; near file `verification/claim/after-v5.json` exists.
- L3750 `.ufo/l0-questions.md` — absent in lane; exists at fleet root (167849 B).
- L4184 `scripts/hyaku/ufo-wave-policy.json` — absent in lane; exists at fleet root (12499 B).
- L4214 `scripts/../.ufo/waves/round-51/c51_wave_ledger.py` — cat-file exit 128; normalized path resolves.

## Dangling home (3) / tmp (8)
- `~/Projects/plazir-15-site` L62, `~/DIRMAP.md` L76, `~/projects` L77 (lowercase, distinct from `~/Projects` L66 which exists) — all missing.
- `/tmp/kake-r10..r15`, `r17`, `r18` missing (L101,100,99,94,93,92,90,89); `/tmp/kake-r16` L91 exists (76K dir).

## Predicate-boundary findings
1. **Extension cap `{1,7}`:** L2357 source text is `.ufo/waves/round-39/r38w2-evidence.SHA256SUMS`; the regex yields `…SHA256S`; cat-file on the real name exits 0 while the truncated token dangles. The counter must annotate the literal truncated token to reach `unannotated=0`.
2. **`..` segment:** cat-file on `scripts/../.ufo/waves/round-51/c51_wave_ledger.py` exits 128 ("path exists on disk, but not in e5f6fd9e"); normalized `.ufo/waves/round-51/c51_wave_ledger.py` exits 0. Literal predicate → dangling.
3. **Round-44 pair** are `--out` paths in a counting command, not committed evidence; `before-v4.json` matches nothing tree-wide.
4. **Fleet-root-only lane pointers:** `sources-census.sh`, `hyaku/ufo-wave-policy.json`, `.ufo/l0-questions.md` exist under `/home/vgpnk/Projects/shokunin`, not in the lane base tree; note the contract's own census command names `scripts/sources-census.sh`.

## Excluded (reasons)
- **URLs:** 9 unique (`grep -oE 'https?://[^ )>"]+' | sort -u | wc -l` → 9), e.g. `https://[not-ipv6]/p`, `http://localhost/%zz`; URL, not a filesystem pointer, and no class-prefixed token arises.
- **Bare filenames:** 204 unique (`LOG.md`, `QUALITY.md`, `SKILL.md`, …); no path separator — class needs `.ufo|corpus|scripts|handoffs|considerthese/`, `~/` or `/tmp/`.
- **Inline git/grep command strings:** 5 tokens occur only there — `.ufo/waves/round-31/sources/S057.txt`…`S061.txt` (L904); all resolve. Broader command reading (git/grep/curl/python3/node/bash/awk/sed/find/ls/cat/test/jj) covers 63 tokens (`excluded-command-strings.json`), all resolving, so U0 is identical under either population (348 vs 285).
- **Other prefixes** (`tmp/…`, `docs/…`, `src/…`): 0 class-matching tokens; `tmp/` fragments carry no extension.

## Contract discrepancy (unknown)
The contract says 12 `/tmp/kake-rNN` tokens across move-log rows 10–18; base bytes hold 9 unique (`/tmp/kake-r10`…`r18`) in 11 occurrences (rows 89–101 one each, plus L4461 and L4478 for r17). Not reproducible; U0 unaffected. Unknown: which extra tokens the author counted.

## Artifacts
- `.ufo/waves/round-70/w1/ScoutPointers/pointers-inventory.json` — 348 rows, keys exactly `{token,class,line,status}`, sorted by first line (17…4713); plus `excluded-command-strings.json` (63), `excluded-git-grep-strings.json` (5), `excluded-urls.json` (9), `run-receipt.txt`.

## Verification exercised
- `show | sha256sum` → `e11f211840de2ea483e82179a194454c2b2a1a1eda92313dbd0695794330b902`; `| wc -l` → 4727; `rev-parse` → `1ac34091f170d50849c52911aac21996378d2853`.
- `grep -c 'Pointer calibration'` → 0, exit 1.
- `final_enum.py` → unique 348, per-class `{'repo':333,'home':6,'tmp':9}`, dangling 19; JSON check: 348 entries, key shape `{('class','line','status','token')}`, sorted-by-line true, unique `(class,token)` 348.
- `git cat-file -e` exits: `.SHA256SUMS` 0; `scripts/../…py` 128; normalized `.py` 0.
- `test -e`: ds4cc-marketplace exists; plazir-15-site missing; `~/Projects` exists; ufo-fsd-alpha exists; `~/DIRMAP.md` missing; `~/projects` missing; `/tmp/kake-r16` exists (76K dir); r10–r15,r17,r18 missing.

## Unknowns
- Counter dedupe by token vs `(class, token)`: no collision, 348 either way.
- Command-prose exclusion applied (285) or regex-only (348): dangling and U0 are 19 either way.
- Whether the annotation section keys the truncated `.SHA256S` and the `..` token verbatim; frozen text gives no normalization.
- Annotation content duty (dated absence class) is review-checked, not assessed here.

Scratch `/fast/scratch/hyaku/kake-r70/ScoutPointers` removed after artifact copy.
