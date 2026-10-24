# ReviewRunnerDiff — C1 runner line review (falsify)

Scope: `git diff f1ffb81..c88b97e -- scripts/citing_set_selftest.py`, reviewed at fde133a
(diff c88b97e..fde133a for that file is empty, verified). Clone:
`/fast/scratch/hyaku/kake-r31/a2-w2/ReviewRunnerDiff/clone`; fixtures/repros under
`/fast/scratch/hyaku/kake-r31/a2-w2/ReviewRunnerDiff/fx/`; transcripts in `.../tmp/`.

## Verdict on the diff: no correctness defect found in what it changes

Every named review point held under reading plus live exercise:

- `argv_refusal` (lines 356-368): correct and airtight *for the gate's real parser*.
  I enumerated every prefix and `=`-form of all seven gate options and replayed them
  through `citing_set.py:build_parser()`: no runner-allowed token sets `--selftest`
  (`[]` result). `--s`, `--j`, `--h`, `-x`, `-`, `--`, `--=x`, `-r` all refused.
  Allowed abbreviations can only bind value options, and since the runner already
  supplies all four, `StoreOnce` turns any fixture repeat into a usage error (exit 64),
  never an override — fixture argv cannot redirect the gate root.
- `dot_git_entry` (371-377): `os.walk(followlinks=False)` on the pre-copy case dir;
  `.git` as file, dir, or symlink all refused ("fixture carries a .git entry",
  FX run: `G1 reason fixture carries a .git entry, refused: .git`, exit 1).
- `read_expected` (384-407): O_NOFOLLOW+O_NONBLOCK+O_NOCTTY open; fstat ISREG and
  size cap; post-read length recheck kills fstat-size TOCTOU; single close path, no
  double-close (`fdopen(closefd=False)` + `os.close` in `finally`). O_NONBLOCK on a
  regular file is a no-op on POSIX — harmless. FIFO refused cleanly, symlink refused
  via ELOOP (hostile selftest h4a/h4c both pass).
- `git_env`/`git_command` (426-438): all `GIT_*` dropped for setup; ceiling is
  `dirname(realpath(work_dir))` = cases_root; every command pins `--git-dir`,
  `--work-tree` and `core.hooksPath=/dev/null`. `git init` accepts `--work-tree` —
  the clean 45/45 run includes 3 git_init + 3 git_commit cases, so it works.
- Setup validation order (326-352): argv refused before copy; `git_commit` before
  `git_init` refused at load AND re-checked at apply (476-477); `mkdir`/`fifo` cannot
  create a `.git` path (347-348); `inside()` realpath check refuses escapes.
- Symlinked case path (679-683 enumeration admits symlinks; 521-523 `run_case`
  refuses before walk/copy): live run — `link reason symlinked case directory
  refused`, sibling real case still evaluated, exit 1.
- Gate env (693-694): ceiling `cases_root` verified empirically —
  `GIT_CEILING_DIRECTORIES=T; git -C T/sub rev-parse` → `fatal: not a git repository`
  (git stops *below* a ceiling entry), so an enclosing repo (the lane checkout the
  runner runs inside!) is unreachable. N3 additionally double-covered.
- Docstring vs code: all five Containment bullets match; git_commit/--git-dir/
  ceiling descriptions accurate.

## Findings

1. LOW — `read_expected` wraps only the `os.open` OSError; an OSError from
   `os.fstat` (line 393) or `handle.read` (399) propagates past `run_case`'s
   `except ValueError` and crashes the whole runner mid-loop without a JSON
   summary or a clean exit code. fs-race/special-fs territory; also cosmetic:
   open-failure message always says "(symlinks are refused)" even for ENOENT.
2. LOW — enumeration predicate `path.is_symlink() or path.is_dir()` (line 681)
   still silently skips fixture-root entries that are regular files, FIFOs or
   sockets (N6 fixed only symlinks). Repro `fx/strays` (OK1 + strayfile +
   strayfifo): cases=1, strays absent from caseNames — the same "vanish from the
   count" shape one level up, unblocked.
3. INFO (maintenance hazard) — `GATE_VALUE_OPTIONS`/`GATE_OTHER_OPTIONS`
   (132-133) hand-duplicate the gate parser's option table. Correct today, but a
   future gate flag that is a prefix of a value option (e.g. `--rev` vs
   `--revision`) is reachable via exact/abbreviated spelling and `argv_refusal`
   accepts it. A comment near the gate parser would keep the tables honest.
4. INFO — `copytree(symlinks=True)` preserves inner-case symlinks and
   `dot_git_entry` does not descend into them; containment holds anyway: gate
   root escapes are refused by `inside()` ("setup path escapes the case copy",
   repro `fx/innerlink` exit 1), gate corpus/document code raises
   `symlink_rejected` (`citing_set.py` ~line 344), and ceiling+`GIT_LOCAL_ENV`
   stripping block repo discovery. Docstring's "a symlink in the fixture
   directory" should not be misread as covering symlinks *inside* a case.

## Commands run (all in sandbox, TMPDIR=sandbox/tmp)

- `git diff f1ffb81 c88b97e6 -- scripts/citing_set_selftest.py`; `git diff
  c88b97e fde133a -- <file>` → empty.
- `python3 -B scripts/citing_set_selftest.py --root . --tmpdir tmp/rt` → exit 0,
  `clean 45 0 True` (45/45; covers git_init/git_commit/fifo/mkdir/argv cases).
- `python3 -B scripts/citing_set_hostile_selftest.py --root . --tmpdir
  tmp/hostile` → exit 0, passed True, P1-P5 all pass, no canary, victims
  unchanged.
- Parser simulation: all option prefixes through `build_parser()` → zero
  selftest-reaching runner-allowed tokens.
- Fixture repros fifo-in-case / strays / symlinkcase / dotgitfile / innerlink /
  innerlink2 → exit 1 each, reasons quoted above (Python 3.14 copytree refuses
  FIFOs as "is a named pipe", so no copy-hang on this interpreter).
- git ceiling empirical test as quoted.

Not verified: exotic filesystems (the OSError path of finding 1 is speculative),
non-Linux portability (O_NOFOLLOW absent → `getattr` fallback makes symlinks
unrefused on systems lacking it — irrelevant to this lane's host).

Tool installs: none.
Report: .ufo/waves/round-31/a2-w2/ReviewRunnerDiff.md
