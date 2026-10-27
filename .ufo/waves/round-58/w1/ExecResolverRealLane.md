# ExecResolverRealLane

C2 no-harm baseline: the CURRENT, unfixed `scripts/id_resolver.py` run with `--revision <rev>` over the last 10
first-parent revisions of `master` in the lane `/home/vgpnk/Projects/shokunin/kake-shokunin`. Every command below was
read-only (`rev-list`, `show`, `ls-tree`, `diff`, plus the tool itself with `--revision`/`--selftest`). No lane
mutation, no jj, no index touch, no pacman, no installs, no subagents.

## RUNS:

Revision list (`git rev-list --first-parent -10 master`), each run as
`python3 -B <lane>/scripts/id_resolver.py --root <lane> --revision <rev>`:

| # | rev | exit | tail line |
| --- | --- | --- | --- |
| 1 | cc8da1674d6e590ae2d05e1f48944ac7939e9ecd | 0 | `ids_cited=106 ids_resolved=106 dangling=0 owned_elsewhere=0 unowned=0` |
| 2 | fff3eea6aa349c8635fd84a791cc32de350ee1c2 | 0 | same |
| 3 | 044048597d62f3199494b63b36e90dd57825e350 (base) | 0 | same |
| 4 | fdae359f91be47ecb755360bd1822873a72bd9e2 | 0 | same |
| 5 | 7ff637929c938f56c625e01d54b6156843c9d469 | 0 | same |
| 6 | 20217f23eca15862febe14545523832e21584106 | 0 | same |
| 7 | 31b61a4ddfcade92c108ff3786b8e9770bc8da31 | 0 | same |
| 8 | 32754df75774dd38e8a96fcda375fc93adf97f1e | 0 | same |
| 9 | 51921b97124616d8526160231aec5c5708c74f3d | 0 | same |
| 10 | 4b8c73050470ada9e6583f3b12d659d1bed6a17f | 0 | same |

Zero `DANGLING` lines in all 10 runs; all-summaries identical, so the 10-run matrix is
`106/106/0/0/0` with exit 0, ten times.

The `--revision` flag is genuinely honored, not silently falling back to the working tree: extending the same probe to
`git rev-list --first-parent -40 master` (read-only) moves the counts with the corpus —
`106` for the 11 newest, `104` for the next 10, `102` for the next 10, `101` for the oldest 9 in that window
(rev `cddef5b4fd…` is the last 106; `f7c98ff269…` is the first 104). Cited ids therefore do move with `--revision`.

Current tool selftest (`--selftest`, `TMPDIR` pinned to seat scratch): `selftest: 49/49`, exit 0.

## LANE FACTS:

- `git ls-tree -r --name-only master corpus/knowledge | grep -c '^"'` → **0**. Git quotes a path by wrapping the whole
  name in ASCII double quotes, so a leading `"` is an exact test; no knowledge path at `master` is git-quoted.
  Per-revision over the same 10 revs: `quotednames=0` at every one.
- Fence count in `corpus/SOURCES.md`: `grep -c '^```'` → **0**; widening to `grep -cE '^\s*(```|~~~)'` → **0**; the
  `~~~`-only count is **0** too. Per-revision over the same 10 revs: `fences=0` at every one. `## Registry` sits at
  line 5, the file is 275 lines, 162 lines begin with `|`.
- `corpus/knowledge` holds 54 tracked files at `master`.
- `git diff --stat 044048597d62f3199494b63b36e90dd57825e350 master` touches **no** `corpus/` path (`git diff --stat
  <base> master -- corpus/` prints nothing); the whole base→master delta is `.ufo/waves/round-58/` machinery. This is
  why the summary is constant across the ten revisions.
- `git diff <base> master -- scripts/id_resolver.py` is empty (0 lines): the working-tree tool **is** the base tool, so
  "current tool" and "tool at the base revision" are the same bytes and the defects below are live here, not fixed.
- The two disclosed defects are present in this source, by direct reading:
  - **F1 (quoted paths, false green).** `knowledge_bodies()` line 144 runs `_git(root, "ls-tree", "-r", "--name-only",
    revision)` with no `-z` and no `-c core.quotePath=false`, then keeps entries with `rel.endswith(".md")`. A quoted
    name arrives as `"corpus/knowledge/…"` and ends in `"`, so it is dropped and its citations are never read.
  - **D1 (fence-blind registry, false green).** `parse_registry()` has no fence state at all: ``` / ~~~ lines match
    neither `REGISTRY_HEADING_RE`, `SECTION_END_RE` nor `ROW_RE`, so a fenced `## Registry` opens the section and a
    fenced `| S### |` row counts as a live row.
- Because the real lane has **0** fences and **0** quoted knowledge names, neither defect has any trigger on this lane:
  the tool's output here is blind to both, before and after a correct fix. The 106/106/0 result is a *no-harm
  constraint*, not evidence that either defect is closed. [INFERENCE] confirming closure needs the gate's own
  fixture lanes (counter cases K1–K5), which are outside this seat.

## EXPECTATION FOR THE FIX:

1. **Exact no-harm target on this lane.** A fixed tool must reproduce, at all ten revisions above, byte-identical
   summary `ids_cited=106 ids_resolved=106 dangling=0 owned_elsewhere=0 unowned=0`, no `DANGLING` lines, exit 0.
   Ordering, id set and counts must not drift.
2. **F1 fix site** — line 144. Correct form is either `ls-tree -r -z --name-only` split on `\0` (quoted paths are
   never emitted with `-z`) or `-c core.quotePath=false`; either way the `.md` filter must then run on the real name.
   On this lane the fix is a provable no-op: no quoted names exist, so the kept set is the same 54 files and the count
   stays 106. A fix that changes the count here (e.g. dropping or duplicating the `corpus/knowledge/` prefix test, or
   splitting `-z` output with `splitlines()`) is a regression.
3. **D1 fix site** — `parse_registry()`. Add fence tracking that keeps the parser's rule set unchanged for unfenced
   text: fence opens on ``` or ~~~ (CommonMark: closing fence is the same character, length >= opening, trailing blanks
   only), lines inside a fence are inert for the heading, the section end and the row regex, and a fence cannot leak
   the `inside` flag across a heading. Requirement: the 162 `|` lines of the live registry must still resolve the same
   id→url map. Since the real file contains zero fence lines, a correct fence-aware parser is a **no-op on this
   lane**; the no-harm matrix above is the mechanical test of that.
4. **Selftest floor.** The current selftest prints `selftest: 49/49`, exit 0. Case P6 of the C2 counter demands
   `N >= 49` with exit 0 after the fix, so the fix must not delete or rename existing cases to make the count; new
   cases for K1/K2/K3/K5 are additive.
5. **Out of scope, do not touch.** The census is explicitly *not* made fence-aware (the counter's stated choice: the
   census keeps counting a fenced row, the tool does not). Changing `corpus/` or the census parser is a scope break.
6. **Residual risk to state at integration.** Lane-history no-harm is necessary but weak: it cannot distinguish the
   fixed tool from the unfixed one, because the lane exercises neither defect. Green on the ten-rev matrix plus
   `49/49` must be reported as *no-harm only*; the closure claim rests on the counter's fixture cases (base 7/12 →
   target 12/12), which this seat did not run.

VERDICT: Current unfixed tool reproduces 106/106/0/0/0 exit 0 on all 10 first-parent revs; lane has 0 quoted knowledge names and 0 fences in corpus/SOURCES.md, so a correct F1+D1 fix must be a byte-level no-op here — no-harm confirmed as a constraint, closure unverified from this seat.
