# ExecTallyRobots

Claim C1 (calibration), seat ExecTallyRobots. Row: `SKILL.md` gate registry line 1093 at base
`e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`, name `robots-expectation-audit`. All runs are in
scratch clones under `/tmp`; the lane was read-only for this seat (no lane writes, no git/jj
mutation). No tool installs were needed.

## RUNS:

- Clone A: `D=$(mktemp -d)` → `/tmp/tmp.RQWY5PHRVT`;
  `git clone -q --no-checkout /home/vgpnk/Projects/shokunin/kake-shokunin "$D"`,
  `git -C "$D" checkout -q e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`.
  `git -C "$D" rev-parse --show-toplevel` = `/tmp/tmp.RQWY5PHRVT`; `rev-parse HEAD` =
  `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`.
- Command (exactly as documented; no env pin is documented by the script, and none was added):
  `cd $D && python3 -B scripts/robots_audit_selftest.py`. Run four times.
- Exit code: `0` on all four runs. stderr: 0 bytes on all four runs. stdout: exactly **one** line
  (the JSON summary), so "last 3 lines" = that single line, identical on every run:

```
{"cases": 204, "failed": 0, "failures": [], "passed": 204, "passedOverTotal": "204/204", "perContract": {"a": 13, "b": 19, "c": 15, "c-exact": 6, "d": 17, "d-match": 6, "e": 16, "f": 27, "g": 15, "h": 12, "h-bound": 1, "i": 28, "i-clar": 1, "k": 11, "k-clar": 2, "usage": 7, "verdict": 8}, "selftest": "kake-r38-robots-audit-selftest", "tool": "/tmp/tmp.RQWY5PHRVT/scripts/robots_audit.py", "verdict": "clean"}
```

- Wall time: run 1 and run 2 were not timed individually (`bc` absent on the host); the pair took
  54.1 s wall for two runs (≈27 s each). Timed runs: run 3 = **22.674 s**, run 4 = **14.675 s**.
  The variance is host load, not the script (same work, same output).
- `python3 -B scripts/robots_audit_selftest.py --list | wc -l` = **204** (corroborates `cases`).
- Post-run `git -C "$D" status --porcelain` was empty: the selftest writes nothing into the clone
  (`-B` suppresses bytecode; all fixture material is under `tempfile.mkdtemp`, removed in `finally`).

## WHAT N COUNTS:

- The printed N is `cases` = `len(FIXTURES)` = the number of **black-box fixture cases**, and
  `passedOverTotal` is `passed/cases` = `204/204`. Each fixture is one subprocess invocation of
  `python3 -B <tool> --manifest <case manifest>` (or the fixture's own argv), judged on exit code,
  report `version`, verdict, the multiset of findings projected on `(check, reason)`, plus
  `checksEvaluated` where the fixture states it. So N counts **fixtures/cases, not mutants, not unit
  checks, not coverage bullets** (the per-contract coverage counts are separate: `perContract`).
- `perContract` sums to 204: 13+19+15+6+17+6+16+27+15+12+1+28+1+11+2+7+8 = 204.
- The row's Self-test cell (line 1093) states **137 fixtures**:
  `` `python3 -B scripts/robots_audit_selftest.py [--tool PATH]` (137 fixtures) ``.
  137 ≠ 204, so the claim is off by **+67** and the counter's `claim_ne_observed` fires for this row.
  The 137 is the round-37 count; the script docstring records 137 (round 37) + 57 (round 38) = 194,
  then + 10 (round 39) = 204, and `SKILL.md`'s own prose agrees: line 1113 "194 fixtures" (round-38
  amendment) and line 1117 "The robots selftest now has 204 fixtures (round 39, routed defect 3)".

## HEAD DEPENDENCE:

- Static reads of `scripts/robots_audit_selftest.py` (1376 lines): no `git`, no `rev-parse`, no
  `git show`, no `HEAD`, no `open(` of any repository file. The only repository paths it names are
  `HERE = Path(__file__).resolve().parent`, `DEFAULT_TOOL = HERE / "robots_audit.py"` (overridable by
  `--tool`), and `Path(args.tool).resolve()`. `os.environ` appears only in `tool_environment()`
  (line 1123): it copies the ambient environment, `setdefault("LC_ALL", "C.UTF-8")`, and pops
  `PYTHONPATH`. Static fixtures are Python literals in the script itself (`FIXTURES`, `add(...)`).
- Syscall evidence (one traced run): `strace -f -qq -e trace=openat,open,stat,newfstatat,access`
  over a full run (exit 0, 204/204, 22.7 s). The only clone paths opened/stat'ed were
  `/tmp/tmp.RQWY5PHRVT`, `.../scripts`, `.../scripts/robots_audit_selftest.py` and
  `.../scripts/robots_audit.py`. No `corpus/`, no `SKILL.md`, no `.ufo/` path was touched.
- The tool under test is likewise self-contained: `scripts/robots_audit.py` reads only the manifest
  and the robots files that manifest names, with `cwd` = the fixture case dir inside the temp tree;
  it contains no `os.environ` read (its docstring claims "no environment reads" and the grep agrees).
- Extra-commit rerun (proof, not inference): clone B `/tmp/tmp.YPJsnkksKb` at the same base, then one
  extra commit `ba08bc9` made with `git -C "$D2" -c user.name=selftest -c user.email=selftest@local
  commit`, touching exactly the paths named in the claim: appended text to `corpus/SOURCES.md` and
  `corpus/README.md`, added `corpus/knowledge/zz-head-dependence-probe.md`, appended an extra
  registry row to `SKILL.md`, and added `.ufo/waves/round-56/probe-note.md` +
  `.ufo/waves/round-56/sources/S999.html` (6 files, +12 lines).
  Rerun of the same command: **exit 0, 10.356 s, `cases` 204, `passed` 204, `failed` 0,
  `verdict` clean, `passedOverTotal` 204/204, `perContract` identical**; the JSON differs from the
  base run only in the `tool` path field. **The tally does not change and the selftest does not fail**
  when a later commit changes those paths.
- Consequently the row's only real dependencies are (i) its own script bytes and (ii) the tool bytes
  at `scripts/robots_audit.py`. The counter's separate `tool_changed` gate compares the pinned
  script's blob at `<rev>` with the blob at `BASE_REV`; at `e48354b7` they are equal (verified), so a
  cell-only fix keeps that gate clean.

## REPLACEMENT CELL:

Exact replacement for the Self-test cell of line 1093 (command unchanged and still first, same
`[--tool PATH]` bracket, only the integer changes):

```
`python3 -B scripts/robots_audit_selftest.py [--tool PATH]` (204 fixtures)
```

Checked against the counter (`POP` entry for this row, regex `\((\d+) fixtures\)` in
`.ufo/waves/round-56/c56_selftally.py`), using the counter's own `table_rows`,
`selftest_cell`, `documented_command`:

- `selftest_cell(...)` on the patched cell returns it verbatim; `re.findall(rx, cell)` = `['204']`,
  sum = **204**, equal to the observed tally B (`204/204`) → `claim_ne_observed` clears.
- `documented_command(...)` = `['python3', '-B', 'scripts/robots_audit_selftest.py']` (the counter
  strips the `[...]` group) → `command_missing` does not fire; `_is_selftest_span` sees the pinned
  script among the words.
- The cell's other digits (`3` in `python3`) are not matched by the claim regex, so nothing else is
  summed. The rest of the row (entry command, verdict map, pinned proof, write scope, owner) is
  untouched.

## RISKS:

- Fix the **cell**, never the script: trimming 67 fixtures out of the script would trip
  `tool_changed` (blob ≠ base blob) and would be a false green; the script's 204 is the intended
  count (docstring round-39 history, SKILL.md line 1117).
- The claim regex only sees the table row. SKILL.md line 1113 still says "194 fixtures" in the
  round-38 amendment prose; the counter ignores prose, but a later seat re-reading prose could
  re-derive 194. That prose is outside this cell's claim and was left alone.
- Load sensitivity: 204 subprocess runs take 10.4–22.7 s on this heavily loaded host against the
  counter's `TIMEOUT = 300` (~13× margin at the slowest observed). The most fragile single case is
  `h11` (64 MiB integer literal with its own 20 s subprocess timeout): a stall there yields
  `203/204`, which the counter reports as `selftest_failed`, not as a claim mismatch. Rerun on a
  quieter host if the counter ever shows that.
- `--tool PATH` sits inside brackets and is stripped by the counter, so the command it actually runs
  is `python3 -B scripts/robots_audit_selftest.py` — same 204 tally, no `--tool` dependency.
- No env pin is documented, and none is needed; ambient env is inherited wholesale (`LC_ALL`
  defaulted to `C.UTF-8`, `PYTHONPATH` dropped) and `TMPDIR` only picks where the fixture tree is
  built, so an unusable `TMPDIR` fails the run before any fixture.
- Scratch clones left in place for L1 re-verification: `/tmp/tmp.RQWY5PHRVT` (base) and
  `/tmp/tmp.YPJsnkksKb` (base + extra commit `ba08bc9`).

VERDICT: Row `robots-expectation-audit` observes 204/204 (exit 0, four runs, stable under a later commit touching corpus/SKILL.md/round-56) but claims 137 → `claim_ne_observed`; replace the cell's integer with `(204 fixtures)`.
