# ExecResolverHistoryRuns

Scope: run the shipped C2 tool `scripts/id_resolver.py` over the C2 history window and compare
`ids_cited`, `dangling` and the dangling id sets against a re-derivation of the w1 ground truth.
Tool revision read / executed: `4b8c73050470ada9e6583f3b12d659d1bed6a17f` (`git rev-parse
4b8c730:scripts/id_resolver.py` = `2937c653b82985b8cc7d92c323603b00dd3e73d6`); the working tree blob
hashes to the same value (`git hash-object scripts/id_resolver.py`), and `git diff --stat 4b8c730 HEAD
-- scripts/id_resolver.py` is empty, so every run below is the named build. Lane HEAD during the work:
`51921b9`; no tracked file under `corpus/` or `scripts/` is modified (`git status --porcelain -- corpus scripts` empty).

## COMMANDS:

All runs, one shell line each (lane cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`):

```
python3 -B scripts/id_resolver.py --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision <rev> --fleet /home/vgpnk/Projects/shokunin
```

- The three named runs are the same line with `--revision 28fa0b23e699303725aba2727094531f5e44494d`,
  `--revision 4b8c73050470ada9e6583f3b12d659d1bed6a17f`, and with **no** `--revision` (working tree).
- History sweep (62 revisions): a stdin driver (`python3 -B -`, no file written) imports
  `.ufo/waves/round-57/w1/ExecResolverGroundTruth.files/truth.py` via `importlib`, calls
  `truth.revision_list(62)` then `truth.snapshot(rev)` per revision, and shells the command above,
  capturing stdout, exit code and `time.monotonic()` wall. The 62 = the 60 rows of the w1 TABLE
  (`f8438a2`…`f8675e5`) plus `4b8c730` and `cddef5b`, which landed after the w1 report and pushed the
  live 60-revision path window forward (current window `4b8c730`…`d8cd2e4`).
- Set-equality check over the same 62: `id_resolver.parse_cited(id_resolver.knowledge_bodies(root, rev))`
  vs `truth.snapshot(rev)["cited_ids"]` → **no mismatch**; `id_resolver.parse_registry(git show
  rev:corpus/SOURCES.md)` id set vs `truth.registry_rows(rev)` → **empty symmetric difference** (the
  tool's `## Registry`-only, first-cell-exact parser and truth's whole-file `^ {0,3}\|\s*S\d{3,} ` scan
  coincide in this window). `git ls-tree -r --name-only <rev>` shows no nested `.md` under
  `corpus/knowledge/` at any of the 62, so the tool's recursive `**/*.md` and truth's
  `corpus/knowledge/*.md` pathspec cover the same files.
- Extra red-state run: `--revision 3994101dba28896830604fd0b08c7f00faca8ed6` (contract §C2 G4), same form.

## TABLE:

`tool` = `ids_cited`/`dangling` from the tool's summary line; `truth` = distinct cited ids / dangling
id count re-derived with `truth.py`; `agree` additionally requires the DANGLING id lists to be equal
and the exit code to be 0 iff truth's dangling set is empty (it always was).

| revision | tool cited/dang | truth cited/dang | agree | exit | wall s |
|---|---|---|---|---|---|
| 4b8c730 | 106/0 | 106/0 | YES | 0 | 0.11 |
| cddef5b | 106/0 | 106/0 | YES | 0 | 0.12 |
| f8438a2 | 104/0 | 104/0 | YES | 0 | 0.11 |
| d5afc48 | 104/0 | 104/0 | YES | 0 | 0.12 |
| 64c0ce1 | 102/0 | 102/0 | YES | 0 | 0.12 |
| faf9abe | 102/0 | 102/0 | YES | 0 | 0.12 |
| 2bda8e4 | 102/0 | 102/0 | YES | 0 | 0.12 |
| 8e408e0 | 101/0 | 101/0 | YES | 0 | 0.12 |
| 7559149 | 101/0 | 101/0 | YES | 0 | 0.11 |
| fd91527 | 99/0 | 99/0 | YES | 0 | 0.11 |
| a4a890c | 99/5 | 99/5 | YES | 1 | 0.17 |
| 5422ff3 | 99/5 | 99/5 | YES | 1 | 0.18 |
| 907790c | 91/0 | 91/0 | YES | 0 | 0.12 |
| 5591557 | 91/0 | 91/0 | YES | 0 | 0.12 |
| ff3f6ec | 89/0 | 89/0 | YES | 0 | 0.11 |
| 1c846ed | 88/0 | 88/0 | YES | 0 | 0.11 |
| af7b217 | 86/0 | 86/0 | YES | 0 | 0.11 |
| 59146c9 | 82/0 | 82/0 | YES | 0 | 0.11 |
| 846138c | 82/0 | 82/0 | YES | 0 | 0.10 |
| ee43e66 | 81/0 | 81/0 | YES | 0 | 0.10 |
| dc7f03e | 80/0 | 80/0 | YES | 0 | 0.10 |
| 290b570 | 80/0 | 80/0 | YES | 0 | 0.10 |
| 297aa62 | 78/0 | 78/0 | YES | 0 | 0.10 |
| b49cba9 | 78/0 | 78/0 | YES | 0 | 0.10 |
| 6858665 | 75/0 | 75/0 | YES | 0 | 0.09 |
| b061585 | 75/0 | 75/0 | YES | 0 | 0.09 |
| 0c5ad2f | 75/0 | 75/0 | YES | 0 | 0.09 |
| 2653b62 | 75/0 | 75/0 | YES | 0 | 0.09 |
| 9e3c31d | 75/0 | 75/0 | YES | 0 | 0.09 |
| d8d5578 | 75/0 | 75/0 | YES | 0 | 0.09 |
| 6d5cd54 | 75/0 | 75/0 | YES | 0 | 0.09 |
| f043c72 | 75/0 | 75/0 | YES | 0 | 0.09 |
| 4c080d3 | 75/0 | 75/0 | YES | 0 | 0.10 |
| ceecb1b | 75/0 | 75/0 | YES | 0 | 0.09 |
| 729878e | 75/0 | 75/0 | YES | 0 | 0.09 |
| adab4c7 | 75/0 | 75/0 | YES | 0 | 0.10 |
| b99b667 | 72/1 | 72/1 | YES | 1 | 0.15 |
| 528a6d0 | 72/1 | 72/1 | YES | 1 | 0.15 |
| 25f8487 | 70/1 | 70/1 | YES | 1 | 0.15 |
| e5a293b | 70/1 | 70/1 | YES | 1 | 0.15 |
| 4d5b3d5 | 70/1 | 70/1 | YES | 1 | 0.16 |
| 662578e | 70/1 | 70/1 | YES | 1 | 0.16 |
| 95abec2 | 70/1 | 70/1 | YES | 1 | 0.16 |
| 2ac06c5 | 59/0 | 59/0 | YES | 0 | 0.09 |
| 76fac3b | 59/0 | 59/0 | YES | 0 | 0.09 |
| 24a1647 | 59/0 | 59/0 | YES | 0 | 0.09 |
| 9ef758c | 58/0 | 58/0 | YES | 0 | 0.10 |
| 3abfc44 | 52/0 | 52/0 | YES | 0 | 0.10 |
| e490381 | 52/0 | 52/0 | YES | 0 | 0.09 |
| b1752a2 | 51/0 | 51/0 | YES | 0 | 0.09 |
| 96d49d6 | 50/0 | 50/0 | YES | 0 | 0.09 |
| d061f38 | 50/0 | 50/0 | YES | 0 | 0.09 |
| 4d13e68 | 50/0 | 50/0 | YES | 0 | 0.09 |
| 285abca | 50/0 | 50/0 | YES | 0 | 0.09 |
| 2f2f12d | 50/0 | 50/0 | YES | 0 | 0.09 |
| 9a7f5be | 49/0 | 49/0 | YES | 0 | 0.09 |
| fde133a | 49/0 | 49/0 | YES | 0 | 0.09 |
| 1c7773e | 44/0 | 44/0 | YES | 0 | 0.09 |
| 451e98f | 44/0 | 44/0 | YES | 0 | 0.09 |
| d8cd2e4 | 40/0 | 40/0 | YES | 0 | 0.08 |
| 7697990 | 40/0 | 40/0 | YES | 0 | 0.08 |
| f8675e5 | 40/0 | 40/0 | YES | 0 | 0.08 |
| 28fa0b2 (named) | 104/0 | 104/0 | YES | 0 | 0.120 |
| 4b8c730 (named) | 106/0 | 106/0 | YES | 0 | 0.121 |
| working tree (named) | 106/0 | n/a (no worktree mode in truth.py) | see DISAGREEMENTS | 0 | 0.053 |
| 3994101 (extra, contract G4) | 99/5 | 99/5 | YES | 1 | 0.230 |

Dangling id lists, tool vs truth: `5422ff3` and `a4a890c` → both `S367,S372,S373,S390,S409`;
`b99b667`,`528a6d0`,`25f8487`,`e5a293b`,`4d5b3d5`,`662578e`,`95abec2` → both `S099`; every other
revision → both empty. Truth's own `history` output reproduces the w1 TABLE's `cited` and `dangling`
columns exactly for all 60 of its revisions; the only table deltas are the two revisions added above.

Three named runs: **base `28fa0b2` and the build `4b8c730` do not agree on `ids_cited` (104 vs 106)**;
`4b8c730` and the working tree agree exactly (106/106, `dangling=0`, exit 0, byte-identical summary
line). The 104→106 step is corpus growth, not a tool difference: truth independently gives 158 rows /
104 cited (1094 occurrences) at `28fa0b2` and 160 rows / 106 cited (1132 occurrences) at `4b8c730`
(`cddef5b` "two Baidu dead-link entries, S421/S422 rows"). Also note `scripts/id_resolver.py` does not
exist at `28fa0b2` (`git ls-tree -r --name-only 28fa0b2 -- scripts/id_resolver.py` empty; first
appearance `cddef5b`, `git log --diff-filter=A -- scripts/id_resolver.py`), so "the tool at base" can
only mean this build pointed at base blobs.

## DISAGREEMENTS:

1. **None between tool and re-derived truth** in the 62-revision sweep: `ids_cited`, dangling counts,
   dangling id sets, full cited id sets, and exit-code polarity (0 clean / 1 dangling) all match. This
   is confirmed by running the commands above.
2. **w1 TABLE is stale by two revisions** — `.ufo/waves/round-57/w1/ExecResolverGroundTruth.md` TABLE
   starts at `f8438a2` (158/104) and ends at `f8675e5`; the live window now starts at `4b8c730`
   (160/106) and ends at `d8cd2e4`, having gained `cddef5b`/`4b8c730` and dropped `7697990`/`f8675e5`.
   Cause: the report was written at HEAD `f7c98ff`; two later commits (`cddef5b` build, `4b8c730`
   repairs) touched the registry and knowledge tree (`git diff --stat 28fa0b2 4b8c730 -- corpus` =
   6 files, +322/−6; `git diff --stat 4b8c730 HEAD -- corpus` empty). All 60 of its rows still
   reproduce exactly; no row is wrong.
3. **`owned_elsewhere` means id-string collision, not document identity** (semantic caveat matching the
   w1 NOTES and contract §C2 "what the counter does not test"). At `b99b667` the tool prints
   `DANGLING S099 ... owners=chousa-,kaidoku-,kama-,kotoba-,kotodama-,kumitate-,mado-,mori-,souji-,tabi-,tameshi-,tsukuroi-shokunin
   url-match=-` (12 lanes) for what truth shows is the range endpoint `S078–S099` in
   `corpus/knowledge/security-txt-publishing.md`; at `3994101`/`5422ff3` all five ids report
   `owners=kotodama-shokunin url-match=-`, exactly the w1 owner table. `url-match=-` everywhere is the
   tool correctly reporting that no sibling row URL is quoted in the citing file — consistent with the
   w1 finding that kotodama's five rows are unrelated documents. Not a defect, but
   `owned_elsewhere=1`/`5` must not be read as "citation resolved".
4. **Working-tree row has no truth counter-value** by construction: `truth.py` reads only git
   revisions; it is compared instead against HEAD `51921b9` (clean `corpus/`), where the tool's
   `--revision 4b8c730` and no-`--revision` summaries are identical.

## TIMING:

62 history runs + 3 named runs + 1 extra, all `python3 -B`, warm page cache, loaded host.
- Per-run wall: 0.08 s (oldest, `d8cd2e4`/`7697990`/`f8675e5`) to 0.18 s (`5422ff3`); 53 clean runs
  0.08–0.12 s, 9 dangling runs 0.15–0.18 s (they trigger the sibling registry scan: `sibling_dirs`
  plus one `git show HEAD:corpus/SOURCES.md` per sibling lane). Sum of the 62 walls = 6.68 s; driver
  total 7.18 s.
- Named runs (bash `time`, real): base `28fa0b2` 0.120 s; build `4b8c730` 0.121 s; working tree
  0.053 s (no per-file `git show`, it reads the tree); extra `3994101` red run 0.230 s;
  six consecutive `4b8c730` repeats 0.139–0.150 s, exit 0 each.
- Exit codes: 53×0 and 9×1 over the sweep, 0 for all three named runs, 1 for `3994101`; no exit 2
  (every revision had a readable `corpus/SOURCES.md` and knowledge corpus, so no unevaluable state).

Unrun: the counter `c57_idresolver_gate.py`, `id_resolver.py --selftest`, builds, lints, tests
(editing wave in flight; the assignment is the history comparison only). Tool installs: none (no
package manager touched; `/usr/bin/time` is absent, bash `time` used instead).

VERDICT: the shipped resolver (`2937c653`, build `4b8c730`) agrees with an independently re-derived
truth on `ids_cited`, dangling counts and dangling ids at all 62 revisions (9 red / 53 green, exit
1/0 matching), 0.08–0.18 s per run; base vs build differ only by corpus growth (104 vs 106 cited),
build and working tree agree exactly; the only real divergence is the w1 TABLE's two-revision window
staleness, not a tool defect.
