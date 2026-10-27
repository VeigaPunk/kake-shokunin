# ExecResolverRealLane

Seat: no-harm baseline for Claim C2 (`scripts/id_resolver.py` closes K8–K14). Read-only measurement of the CURRENT tool on the
last 10 first-parent revisions of `master` in the lane `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Lane untouched: no git/jj mutation, no file written outside this report, this seat's `.files/`, and the seat scratch
(`/fast/scratch/hyaku/kake-r59/ExecResolverRealLane`, deleted on finish). Tooling: no install/upgrade was needed or made
(all checks are stock `python3 -B` 3.14.8 + `git`); pacman never invoked.

## RUNS:

Command form (per revision, two fleet roots):

    python3 -B <lane>/scripts/id_resolver.py --root <lane> --revision <rev> --fleet <fleet-root>

Fleet roots: real `/home/vgpnk/Projects/shokunin`; empty `/fast/scratch/hyaku/kake-r59/ExecResolverRealLane/empty-fleet`
(exists, `os.listdir` empty at run time). Revisions = `git -C <lane> rev-list --first-parent -10 master`, in order:

| # | revision | subject | real fleet | empty fleet |
|---|---|---|---|---|
| 1 | cb685273cc9e331b51f45485793d5d1c91184b3a | round-59: w1 spec and validated dispatch (66-seat v2 wave) | exit 0 | exit 0 |
| 2 | 45a92b64ac8a0f82dba369100e30682f14de81fb | round-59: frozen contract v1, counters, base controls, retained sources, mirror | exit 0 | exit 0 |
| 3 | fd6303ce5c14b3f892dec586297a942ab6e4193b | round-58 verifier spot-check (integrator, hyaku) — BASE_REV | exit 0 | exit 0 |
| 4 | 9892ea4ab42d305adb408905a3f19f7b7109f095 | round-58: hand-check quarantine slice and record frozen-claim conflict | exit 0 | exit 0 |
| 5 | f72c2854806ea7265c140f6136cd5c1ee8c99311 | round-58: record pending outside discernment check | exit 0 | exit 0 |
| 6 | 1b009b74c1effd8d811c9eaaecbadeb992c87c71 | round-58: T1 C1 receipt, measured claims, scorecard and log, residual reviews | exit 0 | exit 0 |
| 7 | de7d96e720522ea15fba3fd9ee3ce58c42596031 | round-58: T0 measurements and C2/C3 receipts | exit 0 | exit 0 |
| 8 | 8d340c15200959190ba3e894399cdc931976331f | round-58: fidelity corrections, historical receipt-pin gate note, lesson erratum | exit 0 | exit 0 |
| 9 | 0ffbabff7b3a6dfa600482cb841dc164d41ea91d | round-58: r1 residual attack dispatch, eight reviewers/critics | exit 0 | exit 0 |
| 10 | c1e39ef3567542b2dc602cc235ed717d6dfbd915 | round-58: build — resolver fence/NUL fix, receipt ledger (19 events), … | exit 0 | exit 0 |

Every one of the 20 runs printed exactly one line, byte-identical, and nothing on stderr:

    ids_cited=108 ids_resolved=108 dangling=0 owned_elsewhere=0 unowned=0

Zero `DANGLING` lines in all 20 runs. The summary line is identical across the ten revisions (checked by collapsing the 20
runs to a set: one distinct line) and identical between the real-fleet and empty-fleet runs.

Worktree mode (no `--revision`, same tool) for reference: exit 0, same line, real fleet and empty fleet byte-identical.

Raw receipts: `.ufo/waves/round-59/w1/ExecResolverRealLane.files/runs.txt` (all 20 runs + the symlink and non-UTF-8 counts),
plus the driver scripts `run_baseline.py`, `lane_facts.py`, `parse_inventory.py` and the two worktree outputs
`wt_real.txt` / `wt_empty.txt` in the same `.files/` directory.

Tool identity: `scripts/id_resolver.py` is the SAME blob `c1c47a41573a271e9dd9fbafbc28a482d4979e4a` at all ten revisions
(also equal to the base revision's blob) — the tool has not changed anywhere in the measured window; the C2 fix will be the
first change to this blob in it.

Counter cross-check (not part of my measurement, but run for orientation): `python3 -B .ufo/waves/round-59/c59_resolver_cases.py
--root <lane> --revision fd6303ce… --work <scratch> --seed 59` reproduces the committed control
`.ufo/waves/round-59/controls/base-c2-resolver-cases.txt` byte-for-byte in its case verdicts: 13/21, `met=False`, exit 1,
K8–K14 FAIL, P6 FAIL, P7 PASS (`ids_cited=108 ids_resolved=108 dangling=0`).

## LANE FACTS:

Counts as specified (same values at all ten revisions — every revision has the same `corpus/SOURCES.md` blob size and the
same tree shape; only file counts grow slightly across the window):

- Symlinks in the lane tree: `git -C <lane> ls-tree -r master | grep -c '^120000'` → **0**. Whole-tree mode census at master:
  17871 entries = 16733 × `100644` + 1138 × `100755`; **no `120000`, no `160000`, no `040000` blob-type entry**. Per revision
  (base → master): 17824 → 17871 entries, symlinks 0 at every one.
- `corpus/SOURCES.md` and `corpus/knowledge/**` are regular files/dirs at every one of the ten revisions: `git ls-tree -r <rev>
  -- corpus/SOURCES.md corpus/knowledge` shows only `100644`/`100755` modes (mode check per revision: "none" non-regular).
- Worktree symlinks under the lane (excluding `.git`): **0** (`find . -type l`).
- Non-UTF-8 names: **0** in the lane tree at every revision (`git -c core.quotePath=false ls-tree -r --name-only <rev>`, decoded
  strictly; no `core.quotePath` escaping either) and **0** in the worktree (`find . -print0` strict decode).
- `## Registry` section of `corpus/SOURCES.md`: heading at line 5, next `## ` heading at line 172 (`## Paths`); section body
  lines 6–171 = **166 lines**. Registry rows: **162** rows matching `^\| S[0-9]{3,} `, first id row line 9 (`S001`), last id row
  line 170 (`S424`), table separator row line 8 (`|---|…`), no duplicate ids, no rows with 1–3 leading spaces, and no `| S…`
  row outside the section (lines ≥172 contain none).
- HTML comments inside `## Registry`: **0** lines containing `<!--` or `-->` (whole file: 0 as well).
- Setext underlines inside `## Registry`: **0** lines consisting only of `-`/`=` runs (whole file: 0). The table separator at
  line 8 starts with `|`, so it is not a setext underline candidate.
- Registry parse by the CURRENT tool: **162** ids parsed from `## Registry` at every revision; `parse_registry` output identical
  across all ten revisions and identical to the worktree file. Cited set: **108** ids (min `S001`, max `S424`) over **53**
  `corpus/knowledge/**/*.md` files (53 `.md` + 3 `.json` sidecars = 56 files, no subdirectories) at every revision; dangling
  **0**; 54 registry ids are never cited.
- `corpus/SOURCES.md` blob size is 150968 bytes at all ten revisions (matches the committed mirror pin
  `.ufo/waves/round-59/assimilation/mirror-pin.json`: 150968 bytes, 162 rows, base `fd6303ce…`).
- Fleet root `/home/vgpnk/Projects/shokunin` holds 21 `*-shokunin` directories; the tool's `sibling_dirs` sees **20** siblings
  (the lane excluded by realpath). Every sibling is its own git repo. All 20 siblings own ids the lane also cites (overlap 14–108
  ids each) — so if any lane id ever became dangling, `owned_elsewhere` would become non-zero on the real-fleet run and stay 0 on
  the empty-fleet run. On this lane nothing dangles, so the fleet argument is inert (the tool only reads sibling registries when
  `dangling_ids` is non-empty) — hence the real/empty fleet outputs are identical. [INFERENCE, from reading `evaluate()` in the
  current tool: the fleet root is consulted only inside `if dangling_ids:`.]
- Lane root is a repository toplevel: `git -C <lane> rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/kake-shokunin`,
  equal to its realpath. (The fleet root is itself a separate git repo; the lane has its own `.git` directory.)
- The tool's built-in `--selftest` currently reports `selftest: 59/59` (exit 0) — 59 cases, all passing. The counter's P6 floor is
  `P6_FLOOR = 66`, which is why base P6 fails with `('59','59')`.

## EXPECTATION FOR THE FIX:

A correct C2 fix (closing K8–K14) must leave every number above unchanged on this lane. Concretely, for each of the ten
revisions and for both fleet roots, the fixed tool must still print exactly

    ids_cited=108 ids_resolved=108 dangling=0 owned_elsewhere=0 unowned=0

with exit 0, zero `DANGLING` lines, and the same summary format (`^ids_cited=(\d+) ids_resolved=(\d+) dangling=(\d+) `,
`^DANGLING <id> cited-by=… owners=… url-match=…`) — the counter's P7 (`ids_cited >= 106`, `dangling == 0`) and the K-case regexes
depend on that format. Because the real lane has 0 dangling ids, the fleet argument cannot discriminate sibling behaviour here;
the counter's P4 case is what covers that, so a "green on the lane" result alone does not prove sibling ownership survived.

Route-by-route, why each fix is a no-op on this lane (and therefore where a fix could silently regress the lane):

- K8 (HTML-comment registry row must not register): the lane's `## Registry` has 0 comment lines, so comment-aware parsing must
  still yield **162** registry ids and 0 dangling. Regression signal: registry ids ≠ 162 or any id newly dangling.
- K9 (setext H2 ends the `## Registry` section): 0 setext underline lines in the section, so the section must still end at
  `## Paths` (line 172) and still register **162** ids. A setext detector that fires on the line-8 table separator (`|---|…`)
  would truncate the section and produce ~1 id and 108 dangling ids — that is the concrete regression to watch.
- K10 (in-lane symlinked knowledge directory must be read): the lane has **0** symlinks and no subdirectory under
  `corpus/knowledge`, so following in-lane symlinks (with the outside-the-lane guard retained) must still read **53** `.md`
  files and cite **108** ids. Regression signal: `ids_cited` drops below 108 or below the counter's floor 106.
- K11 (at a revision, a committed symlink resolves in-tree, never read as its target string): 0 symlinks in any of the ten
  revisions, so `--revision` must still read 53 blobs and cite 108 ids. The fix must read the raw path bytes (not a
  `str.replace`-mangled path) so the non-UTF-8 case stays readable — unexercised here.
- K12 (registry symlinked out of the lane → exit 2, unevaluable): `corpus/SOURCES.md` is a regular file at every revision, so the
  lane must stay evaluable (exit 0 with the summary line), not exit 2.
- K13 (non-UTF-8 knowledge file name at a revision is read, not fatal): 0 non-UTF-8 names, so the lane must stay exit 0; the
  current fatal (`cannot read corpus/knowledge/bad<?>.md`) must be gone without changing the lane's counts.
- K14 (`--root` below a repository toplevel → exit 2): the lane root IS a toplevel (realpath equals `rev-parse --show-toplevel`),
  so the new toplevel guard must accept it and keep exit 0.
- P6: the fixed tool's `--selftest` must print a tally of the form `selftest: N/N` with **N ≥ 66** (floor) and every case
  passing; today it prints `59/59`, which is why base P6 fails. The 7 new routes need their own in-tool cases, not just the
  counter's fixtures.

Caveat for the integrator: C3 (same wave) appends rows `S425`/`S426` to the registry and two new knowledge files plus a
`[r59-correction 2026-10-27]` tail citing `S425`. If C3 lands before the C2 measurement, the expected lane numbers move from
162 registry ids / 108 cited / 0 dangling to 164 registry ids and ~110 cited / 0 dangling — the invariants that must not move are
`dangling == 0`, `ids_resolved == ids_cited`, exit 0, `ids_cited >= 106`, and "every id in the registry's `## Registry` section
parses to a registered id". [INFERENCE: the 164/110 figures are derived from the contract's row counts and the two new
knowledge entries, not measured — this lane has no C3 rows yet.]

Also worth pinning for the fix author: the summary line is produced from `ids_cited`/`ids_resolved`/`dangling`/`owned_elsewhere`/
`unowned` derived from `parse_registry` + `parse_cited`; any fix that changes the *counting* of cited ids (e.g. reading
non-`.md` sidecars, or de-duplicating differently) would move `ids_cited` and trip the P7 floor.

VERDICT: Baseline measured and reproducible — the CURRENT tool is green (exit 0, `ids_cited=108 ids_resolved=108 dangling=0
owned_elsewhere=0 unowned=0`) at all ten first-parent revisions of master under both the real and an empty fleet root; the lane
carries 0 symlinks, 0 non-UTF-8 names, 0 HTML-comment lines and 0 setext underlines inside `## Registry` (162 registry rows,
166 section lines, 53 knowledge `.md` files), so every K8–K14 fix must be a no-op on these numbers and the in-tool selftest must
grow from 59/59 to at least 66/66.
