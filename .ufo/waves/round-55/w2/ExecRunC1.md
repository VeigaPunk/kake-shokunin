# ExecRunC1

ATTACKS: claim C1 measurement — `.ufo/waves/round-55/c55_readme_index.py` (v2) at build revision
`a7a548e102b71bd16b0a6ddafa469393a2c98b69` and at base `fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`,
plus an independent recount of the `unindexed` term from `corpus/README.md` §Coverage map against
`git ls-tree -r corpus/knowledge/` (no import of the counter).

## COMMANDS

All run with `cwd=/home/vgpnk/Projects/shokunin/kake-shokunin`; committed bytes only; no lane write
except this report (scratch scripts written under `/tmp`). Note the worktree HEAD had already moved to
`78963ae28e1c6a409a1a1322230c5671cd2efcbe` when I started (`git rev-parse HEAD`); every measurement
below names revision `a7a548e…` explicitly, so the moved worktree did not enter any count.

1. `python3 -B .ufo/waves/round-55/c55_readme_index.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision a7a548e102b71bd16b0a6ddafa469393a2c98b69` (run 1, stdout→`/tmp/c1_run1.txt`, stderr→`/tmp/c1_run1.err`)
   → `EXIT=0`; observed stdout:
   ```
   C1 readme-index index_mismatches=0 knowledge_files=49 met=True  (met: index_mismatches == 0 AND knowledge_files >= 46)
     unindexed=0 multi=0 thin=0 duplicate=0 head_changed=0 deleted=0 dangling=0 coverage_rows=51
     revision: a7a548e102b71bd16b0a6ddafa469393a2c98b69
   EXIT=0
   ```
   stderr byte count: `0 /tmp/c1_run1.err`.
2. Same command, run 2 (`/tmp/c1_run2.txt`) → `EXIT2=0`; `cmp /tmp/c1_run1.txt /tmp/c1_run2.txt` → no output (`BYTE_IDENTICAL`); `sha256sum` both:
   `bfa83484b88bfa606ef00a11b691b689aab99869cca5ca6fa099b63ce36cfe1f` for each; stderr 0 bytes.
3. Same command + `--json` (`/tmp/c1.json`) → `JSON_EXIT=0`. Parsed with `python3` `json.load`:
   `schema=kake-r55-c1-readme-index-v2`, `revision=a7a548e…`, `predicate=met: index_mismatches == 0 AND knowledge_files >= 46`,
   `met=True`, `exit=0`, `index_mismatches=0`, `knowledge_files=49`, `coverage_rows=51`,
   and each term list empty: `unindexed=0 multi=0 thin=0 duplicate=0 head_changed=0 deleted=0 dangling=0`.
   Key set observed: `coverage_rows dangling deleted duplicate exit head_changed index_mismatches
   knowledge_files met multi predicate revision schema thin unindexed`.
4. `python3 -B .ufo/waves/round-55/c55_readme_index.py --selftest` → stdout `c55 readme-index selftest: 35/35`, `SELFTEST_EXIT=0`.
5. Base control: same counter with `--revision fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d` → `BASE_EXIT=1`;
   stdout `index_mismatches=21 knowledge_files=46 met=False`, `unindexed=21 multi=0 thin=0 duplicate=0
   head_changed=0 deleted=0 dangling=0 coverage_rows=27`, then 21 `unindexed:` lines, `revision: fcaf4b85…`, `EXIT=1`.
   `diff /tmp/c1_base.txt .ufo/waves/round-55/controls/base-c1-readme-index-v2.txt` → no output
   (`BASE_IDENTICAL_TO_CONTROL`, exit 0).
6. Write-side check on the counter (`grep -n "open(\|write(\|makedirs\|shutil\|remove\|unlink\|subprocess.run"`):
   all write/`subprocess` sites are at lines 232–253 and 346, i.e. inside `_fixture()`/`selftest()`
   tempdir code; the `measure()` path (lines 128–225) only calls `git ls-tree`/`git show` reads
   (line 75 `subprocess.run(["git", "-C", root, *args], stdout=PIPE, stderr=PIPE)`). No write in the
   measurement path, so the counter cannot mutate the lane; my runs left `/tmp` scratch only.

## DETERMINISM

- Two consecutive runs at `a7a548e…` produced byte-identical stdout (`cmp` silent, identical sha256
  `bfa83484…cfe1f`), both `EXIT=0`, both stderr empty. Determinism observed, not inferred.
- Determinism mechanism checked in code: `measure()` reads only `git ls-tree -r --name-only` and
  `git show <rev>:<path>` (committed bytes); no worktree read, no network, no clock/random input,
  ordering fixed by `sorted()` on `know`/`base_know` and on the term lists printed. JSON mode emits the
  same `facts` dict with `indent=1`, so its determinism follows from the same inputs (json mode run
  once, not twice — the *text* mode pair is the byte-identity evidence required).
- `--json` and text mode agree on every shared field: `exit=0`/`EXIT=0`, `met=True`/`met=True`,
  `index_mismatches=0`, `knowledge_files=49`, `coverage_rows=51`.
- Base replay is byte-identical to the committed v2 base control (step 5), so the control receipt was
  produced by this same counter code on this base revision: `index_mismatches=21 knowledge_files=46 met=False exit 1`.
- Exit-code contract observed on the three reachable paths: 0 (met, build), 1 (not met, base),
  0 (`--selftest`, 35/35). Exit 2 / 64 were not exercised by me (`unrun`) — the selftest does cover
  the unevaluable fixtures (`fail_two_sections`, `fail_no_section`, both expected 2).

## INDEPENDENT RECOUNT

Method (own code, `/tmp/c1_recount.py`, `/tmp/c1_recount2.py`; no import of `c55_readme_index`):
`git ls-tree -r --name-only <rev> -- corpus/knowledge/`; extract the section matching
`^## Coverage map` up to the next `^## `; keep the first contiguous run of `|`-lines; drop header +
separator; take the **second column literally** (`cells[1]`, not by header name); a file counts as
indexed iff some second-column cell contains `knowledge/<rel>` with a right boundary (next char not
`[A-Za-z0-9_-]`, and not `.`+alnum).

- Base `fcaf4b85…`: `header=['Area','Entry','Coverage'] table_rows=27 knowledge_files=46`,
  **`UNINDEXED_COUNT=21`** — the 21 names printed match, one for one, the counter's 21
  (`accessibility-review-cards.json`, `accessibility-review-packet.md`, `baidu-friendly-crawl-guidance.md`,
  `baidu-mobile-matching-error-causes.md`, `canonical-selection.md`, `crawl-budget-consequences.md`,
  `crawl-error-status-table.md`, `crawler-identity.md`, `dynamic-rendering-workaround-limits.md`,
  `freshness-sidecar.json`, `js-rendering-queue.md`, `link-preview-metadata.md`, `pages-base-path.md`,
  `receipt-integrity.md`, `redirect-rewrite-rules.md`, `render-static-sites.md`, `render-web-services.md`,
  `robots-txt-rules.md`, `security-txt-publishing.md`, `vault-properties.md`,
  `yahoo-japan-rel-nofollow-semantics.md`). Expected 21 → observed 21.
- Build `a7a548e…`: `header=['Area','Entry','Coverage'] table_rows=51 knowledge_files=49`,
  **`UNINDEXED_COUNT=0`**. Matches the counter's `unindexed=0 knowledge_files=49 coverage_rows=51`.
- Column-literal vs header-name: header names are `Area|Entry|Coverage`, so literal column 2 == the
  counter's header-derived `Entry` index (1) and literal last column == `Coverage` index (2). No
  divergence possible on this revision; `named_only_in_other_column=0` at both revisions confirms no
  file is indexed only from a non-Entry column that my literal rule would miss.
- Tree delta base→build (`LC_ALL=C` sorted `diff` of the two `ls-tree` listings): exactly three
  additions, `corpus/knowledge/yahoo-japan-robots-pattern-syntax.md`,
  `corpus/knowledge/yahoo-japan-robots-txt-basics.md`, `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md`;
  0 deletions → 46+3=49, above the 46 floor, so the `knowledge_files >= 46` guard is satisfied without
  any population swap.
- Transition check (`/tmp/c1_recount2.py`): all 21 base-unindexed files are named at build
  (`21 / 21` → `True`), and the build rows name **no path absent from the build tree**
  (`false index: []`), leave **no build file unnamed** (`[]`), and name **no deleted file** (`[]`).
- Secondary corroboration of the counter's non-`unindexed` terms at build, computed raw without the
  counter's stoplist/common-word heuristics: `rows=51 cells_under_5_tokens=0 duplicate_cells=0
  rows_over_2_files=0 max_files_per_row=2` — consistent with `thin=0 duplicate=0 multi=0`, and every
  row stays inside the counter's 2-file cap.

## DISAGREEMENTS

None. My independent count and the counter agree on all three measured quantities
(`unindexed` 21→0, `knowledge_files` 46→49, `coverage_rows` 27→51), and the base replay is
byte-identical to `controls/base-c1-readme-index-v2.txt`.

Attacks that failed (recorded so the wave does not re-run them): (a) worktree-drift attack — the
worktree HEAD had moved past the build revision before I started, yet the counter still measured
`a7a548e…` exactly, because it reads `git show`/`git ls-tree` at the named revision; (b) literal-column
vs header-column divergence — the header is `Area|Entry|Coverage`, so both readings coincide here;
(c) stoplist/`common`-word masking of `thin` — a raw `<5` whitespace-token scan over the 51 build
Coverage cells finds 0 short cells, so the heuristic's exemptions are not load-bearing on this tree;
(d) false index (a row naming a file that does not exist) — 0 such rows at build.

Residual limits, stated not hidden: I exercised only exit codes 0 and 1 plus the selftest
(exit 2/64 paths `unrun` by direct invocation; the selftest covers the exit-2 fixtures); I did not
re-derive the `dangling` term's resolver set independently (only the build-side fact `0 rows name a
nonexistent knowledge path`, and the counter's own `dangling=0`); the `head_changed`/`deleted`
terms I corroborated only through the `ls-tree` delta (0 deletions, and the counter's byte-prefix
comparison was not re-implemented) — `[INFERENCE]` that `head_changed=0` follows from no
`corpus/knowledge/` file being modified, which I did not diff byte-wise myself (`unrun`).

Tool installs/upgrades this wave: none (no pacman, no `uv tool`, no network); scratch files under
`/tmp` only. No credential material, tokens or private URLs are reproduced in this report.

VERDICT: C1's measurement is deterministic and independently reproduced — 21 unindexed at base, 0 at
build with 49 knowledge files and 51 coverage rows; no disagreement with the counter.
