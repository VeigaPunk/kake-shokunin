# SentinelCounters

Integrity/security review of the three round-59 counters at the frozen contract commit
`45a92b64` (lane HEAD `cb68527`). Reviewed: the **contract-pinned version 1** of
`c59_axis_evidence.py` (`95d23511`), `c59_resolver_cases.py` (`ca2e85c6`), `c59_quote_truth.py`
(`b3aef90c`), extracted from git into scratch; plus the uncommitted wave-1 rewrite now on disk
for C1 (`1d04f19d`) and C3 (`f059b69e`), where the same defects reproduce.
All probes ran in fixture repos under `/fast/scratch/hyaku/kake-r59/SentinelCounters`
(git 2.56.0, Python 3.14.8). Nothing ran against the lane, a sibling lane, jj state or the lane
index; lane reads were `ls-tree`/`rev-parse`/`show` only. Scratch deleted after receipts were
copied to `SentinelCounters.files/` (lab*.log). No tool installs were needed.

## FINDINGS:

### F1 HIGH — C1 accepts a **symlink's target string** as a committed receipt: `met=True` with no receipt document in the tree
`c59_axis_evidence.py:74` (`git()`), `:78-92` (`show()`/`obj_type()`), `:131-166` (`resolve()`).
`resolve()` decides "committed bytes" with `git cat-file -t`, which answers **`blob` for mode
`120000`**; `show()` then uses `git show <rev>:<path>`, which for a symlink returns the **link
target string**, not a document. So a cited receipt may be a symlink whose *target text* holds the
tally, and the counter counts that as "the tally occurs in a resolved blob".

Reproduction (`lab19.log`; SCORECARD.md an ordinary committed file):
```
.ufo/waves/round-59/{operability,freshness,calibration}.md -> symlinks, targets
                                           "receipts/16/16", "receipts/20/20", "receipts/1/1"
git show <rev>:.ufo/waves/round-59/operability.md   =>  'receipts/16/16'
$ python3 -B c59_axis_evidence.py --root fx --revision <rev> --base <base>
C1 axis-evidence mismatches=0 unresolved=0 rows_no_receipt=0 receipts_off_axis=0
tallies_unfound=0 rows_no_tally=0 rows=3 scores_held=2 superseded_kept=3 met=True   -> EXIT=0
cat <checkout>/.ufo/waves/round-59/operability.md   =>  rc=1 (broken link; no receipt exists)
```
The measured revision holds **zero receipt documents**, yet the claim is reported met.
Fix: read the entry mode (`git ls-tree -z <rev> -- <path>`) and treat `120000` as **not committed
bytes** (or resolve the target in-tree and re-check); `cat-file -t == blob` must not stand in for
"regular file".

### F2 HIGH — C1 accepts a **symlinked SCORECARD.md**: the axis table itself can be a link target
`c59_axis_evidence.py:78-86` + `:160` (`measure()` calls `show(root, rev, SCORECARD)`).
`git show` on a `120000` entry returns the target string, so when that string parses as markdown
the counter measures a document that exists nowhere; a multi-line target (legal on Linux) carries
the whole table. Fixtures with a *broken* symlink fail closed (EXIT=1) — the hole is specifically
"target text that parses", which the committer chooses.
```
120000 blob ... SCORECARD.md  (target = the entire fake scorecard, 505 bytes)
120000 blob ... receipts x3
v1: EXIT=0    v2 (working tree): EXIT=0    cat <checkout>/SCORECARD.md => rc=1
```
Fix: same mode check as F1, in one `symlink_safe_show()` helper used by all three counters.

### F3 MEDIUM — C3 parses a symlinked registry / lesson / entry from its target string
`c59_quote_truth.py:125-141` (`show()`/`show_bytes()`), consumed by `parse_registry()` (`:176-189`),
the C2 header check and the C9 append-only diff:
```
ls-tree: 120000 blob ... corpus/SOURCES.md
show() => ['# Sources', '']       parse_registry(show(...)) => ['S425']
```
A symlinked knowledge entry likewise returns its target string as the entry body, so the `source:`/
`verified-at:`/`recheck:` header, the C5 spans and the C9 correction can come from link targets.
The two retained bodies are safe (pinned by `BODY_SHA256`) — digest pinning is the pattern the
other paths lack. Fix: apply F1's mode check in `show_bytes()`/`show()`.

### F4 MEDIUM — C2 runs arbitrary code from the operator's **global git config** inside its own fixtures, and the hook flips a failing case to PASS
`c59_resolver_cases.py:54-58` (`env()` strips only `GIT_*`, keeps `HOME`/`XDG_CONFIG_HOME`),
`:83-90` (`commit_all()` — `git init`/`add`/`commit` per fixture). The D2 scrub stops at the `GIT_`
prefix, so global config still applies: `core.hooksPath` and `init.templateDir` execute inside the
fixture the case asserts on, and can restage a rewrite before the measured tool reads the revision.
```
init.templateDir alone: 18 pre-commit firings in .../fleet/kake-shokunin (lab16.log)
core.hooksPath alone  : pre-commit 18, prepare-commit-msg 18, post-commit 18
K13_non_utf8_path_at_revision  FAIL (exit=2 cannot read corpus/knowledge/bad\xff.md)
  -> hook renames it to ASCII + `git add -A`:  PASS (exit=1, DANGLING ... renamed.md)
passes 13 -> 14                            (lab14.log; base tool unchanged)
```
The route the case exists to exercise is never exercised, and the hook is arbitrary shell.
Fix: point `HOME`, `XDG_CONFIG_HOME`, `GIT_CONFIG_GLOBAL`/`_SYSTEM` at scratch and set
`GIT_CONFIG_NOSYSTEM=1` in `env()`; pass `-c core.hooksPath=` and `-c init.templateDir=` on the
fixture `init`/`commit` calls (`--hooks-path` alone does not stop `init.templateDir`).

### F5 MEDIUM — PYTHONPATH reaches the **child interpreter that runs the measured tool**
`c59_resolver_cases.py:54-58`, `:146` (`py = [sys.executable, "-B", tool]`). `env()` keeps
`PYTHONPATH`, so a `sitecustomize.py` runs inside the measured child, reads the fixture and prints
exactly the lines a case asserts on: K13 FAIL → PASS (13/21 → 14/21, `lab18.log`; 7 forged child
invocations). Twice-demonstrated false green in C2, independent of the tool. Fix: drop
`PYTHONPATH`/`PYTHONHOME`/`PYTHONSTARTUP` in `env()` (or launch with `-I`/`-E`).

### F6 LOW — `--work` inside the measured repo plants an empty directory; C3 has a dead import
`c59_resolver_cases.py:332-338`: the `mkdtemp` child is removed in `finally`, but the **parent** is
created with `os.makedirs(parent, exist_ok=True)` and never removed — `--work <lane>/x` leaves
`x/` inside the repo (`lab11.log`: `dir_exists_after=True contents=[]`). Normal runs are clean
(no `/tmp` residue with `TMPDIR` unset or set; C1/C3 write nothing). C3 imports `tempfile` (`:60`)
and never uses it. Fix: refuse `--work` inside `--root`; drop the dead import.

### F7 LOW — contract-pin drift: two of the three counters on disk are not the pinned version
`contract.json` pins C1 `95d23511…`, C3 `b3aef90c…`; the tree holds `1d04f19d…`, `f059b69e…`
(wave-1 build in flight, not a counter defect). C1/C3 receipts must name the **digest actually
executed**. Every finding above was reproduced on both versions where the code is shared.

### F8 LOW — the `--root` toplevel guard compares `realpath`, so a symlinked root is accepted
`C1:282-285`, `C3:701-705`, `C2:323-326`. A symlink to the true toplevel passes (`lab11.log`:
C1 EXIT=0 on link and real path) — intended (same repo), recorded so F7/D2 is not over-read.
Subdirectory, `.git` dir and missing path are all correctly refused (`EXIT=2`, all three).

## NON-ISSUES (measured)

1. **Argument injection `--revision`/`--base`** (`--output=…`, `--upload-pack=…`, `--exec=…`,
   `--sq-quote`, `--all`, `--`, `-q`, `--help`, `--parseopt`, `--git-dir=/tmp`, `-c`): closed in
   all three, both argv forms. A separate leading-dash token is refused by argparse (`rc=64`); the
   `--opt=value` form reaches git but each counter appends `^{commit}` (`C1:286-287`, `C2:327`,
   `C3:706-707`) so `rev-parse --verify` fails → `EXIT=2`. No `PWN` file created; no `shell=True`.
2. **D2 `GIT_*` scrub** — fixed and verified: `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE`,
   `GIT_CONFIG_COUNT/KEY_0/VALUE_0` exported give **byte-identical** output in all three
   (`lab3/lab6/lab10.log`). F4 is the non-`GIT_` residual of the same class, not a regression.
3. **D2 base/revision pinned once** — fixed: C1 resolves both (`:286-291`, empty `--base` → 64),
   C3 resolves both (`:706-713`, empty `--base` → 2), C2 resolves the revision (`:327`). Round-58
   F3 (index read via `":path"`) and F4 (symbolic-ref drift) are gone.
4. **D2 toplevel root** — fixed in all three (`C1:282`, `C2:323`, `C3:701`); acceptance rule in F8.
5. **Hostile `.git/config` in the *measured* repo** — `core.fsmonitor`, `core.hooksPath`,
   `core.pager`, `diff.external`, `diff.<d>.textconv`, `alias.*`, `filter.*.smudge` fired **0**
   markers for C1/C3 and for C2's tool read (`lab3.log`). Contrast F4: only read-only commands run
   in the measured repo; commits happen in the fixture repos.
6. **Symlinked tool at the revision (C2)** — fail-closed: the copy is the target string, not valid
   Python, 21/21 `SyntaxError`, `0/21 EXIT=1` (`lab7.log`).
7. **Hardcoded `/tmp`** — none. C1 has no scratch; C2 honours `--work`→`$TMPDIR`→`gettempdir()`;
   C3's unused import. C1's `BARE` regex *detects* `/tmp`/`~`/`/home` pointers to reject them.
8. **Leftover scratch** — none in normal runs (`/tmp` delta `[]`, explicit `--work` delta `[]`);
   only F6(a) remains.
9. **Untrusted record content in argv** — pointers are filtered by `PATHISH`/`LINEONLY`, then
   `normpath` + `..` rejection before `cat-file`/`show`; C2 uses constant pathspecs; no
   `:(magic)`/`--` confusion reachable.
10. **`--seed`** — drawn once and printed, so a run is replayable and no fixed id is keyable.

## D2 STATUS:

| Round-58 D2 item | C1 | C2 | C3 |
|---|---|---|---|
| inherited `GIT_*` scrubbed | fixed (`:67-71`) | fixed (`:54-58`) | fixed (`:113-117`) |
| `--base`/`--revision` resolved once to commit ids | fixed (`:286-291`) | fixed for `--revision` (`:327`) | fixed for both (`:706-713`) |
| `--root` must be a repository toplevel | fixed (`:282-285`) | fixed (`:323-326`) | fixed (`:701-705`) |
| symlink escape at `--revision` (tool side) | n/a | cases K11/K12/K14 present | n/a |

All four verified forward: `GIT_*` injection byte-identical; non-toplevel roots `EXIT=2` in all
three; empty `--base` rejected. **But D2 is not closed as a class**: the "symlink read as its
target string" defect D2 routed to the *tool* (K11) is still present **in the counters themselves**
(F1/F2 in C1, F3 in C3), and the env scrub stops at the `GIT_` prefix, leaving global git config
executable inside C2's fixtures (F4) and PYTHONPATH executable in the measured child (F5).
Round 60 successors: "regular-file check on every blob a counter reads" and "scrub
`HOME`/`XDG_CONFIG_HOME`/`PYTHONPATH` on fixture-commit and child-spawn paths" — each a
one-helper fix.

VERDICT: Argument injection, non-toplevel roots, `GIT_*` scrubbing and base/revision pinning are fixed forward and verified, but the round-58 D2 symlink defect survives inside the counters themselves — C1 reports `met=True` (exit 0) on a revision whose cited receipts are symlinks carrying the tally as their target text (F1/F2) and C3 parses a symlinked registry/entry from its target string (F3) — plus C2 executes ambient global git-config hooks and inherits PYTHONPATH inside its own fixture repos and measured child, either of which flips a failing route case to PASS (F4 13/21→14/21, F5 13/21→14/21); no code-execution path exists through the measured repo's config or the three CLIs' arguments.
