# ExecTallyLedger

Claim C1 (calibration), row `wave-evidence-ledger` (SKILL.md line 1215 at base `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`).
All runs in scratch clones under `/tmp` (`c1tally*`), never in the lane; no lane git/jj state touched. No tool installs.

## RUNS:

Scratch clone `D=/tmp/c1tally.SJKEIf` (`git clone --no-checkout` of the lane, `checkout -q e48354b7c26b…`;
`git -C $D rev-parse --show-toplevel` == `$D`, HEAD == base). Command, from `$D`:
`python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest`. No env pin is documented and none is needed
(the script contains no `os.environ`/`getenv` reference at all), so none was added.

| run | exit | wall | stdout line count | last 3 lines of stdout | sha256 of stdout |
|---|---|---|---|---|---|
| 1 | 0 | 2953 ms | 1 | `c52 ledger selftest: 19/19` | `f33b502c9f82b920ec47c5560d9810b0dd86cd10989a6d62857e5ea1200a6880` |
| 2 | 0 | 4134 ms | 1 | `c52 ledger selftest: 19/19` | `f33b502c9f82b920ec47c5560d9810b0dd86cd10989a6d62857e5ea1200a6880` |

Both runs: stderr empty, stdout is exactly one line (so "last 3 lines" is that one line), outputs byte-identical.
Wall time difference is host load, not output. The committed receipt `.ufo/waves/round-52/control/c1-ledger-selftest.txt`
is `c52 ledger selftest: 19/19` / `EXIT=0` — identical to both runs.

Counter cross-check (real `c56_selftally.py`, `POP` row `('.ufo/waves/round-52/c52_wave_ledger.py', r"\((\d+) fixtures")`,
`measure()` called with `pop=` this single row against the base clone):

```
exit: 0
{"row": "wave-evidence-ledger", "problems": [],
 "facts": {"claim": 19, "command": "python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest",
           "observed": "19/19", "exit": 0}}
```

So at base this row is already A == B (claim 19, observed total 19, exit 0, no `tool_changed`). It is therefore one of the
three C1 rows that already agree, not one of the seven mismatches the contract lists.

## WHAT N COUNTS:

N counts **fixtures** — sandbox git repositories, not checks, cases, mutants or unit assertions. `selftest()` does
`fixtures = _selftest_fixture_files(); total = len(fixtures)`, loops once per fixture, builds a throwaway repo per fixture
and prints `passed/total`. The 19 keys are `pass` plus 18 `fail_*` (static enumeration of `fixtures["…"] =` assignments):

`pass`, `fail_spawn0`, `fail_phantom`, `fail_zerobyte`, `fail_48of0`, `fail_multiset`, `fail_logtoken`,
`fail_timetautology`, `fail_seatsrename`, `fail_47of48`, `fail_grant`, `fail_namekey`, `fail_dupdigest`,
`fail_statusconflict`, `fail_statusok`, `fail_timingcarry`, `fail_roledrift`, `fail_deadreason`, `fail_acctroster`.

Per fixture it runs the three ledger checks (L1/L2/L3) and asserts the aggregate exit code: `pass` -> 0,
`fail_namekey` -> 2, every other `fail_*` -> 1. The numerator (19) is "fixtures that produced their expected exit code";
it is not a count of L1/L2/L3 evaluations (that would be 57).

Row's Self-test cell at base: `` `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest` (19 fixtures, sandbox repos;
receipt `.ufo/waves/round-52/control/c1-ledger-selftest.txt`) ``. The counter regex `\((\d+) fixtures` captures `19`, and
`parse_tally` reads the last `pass|selftest` line's `\b(\d+)/(\d+)\b` -> `(19, 19)`, compared as `claim != tally[1]`.
**19 == 19: the cell already equals the integer the command prints as its denominator.** No defect in this row's number.

## HEAD DEPENDENCE:

Reads, enumerated from the script (`root = os.getcwd()`; all reads via `git show`/`git ls-tree` against one **hardcoded,
immutable revision** `rev = "907790c78008819fc95c988431188f90b81f0d5f"` — round-51, an ancestor of base):

- `git show 907790c:<p>` for 7 fixed paths: `.ufo/waves/round-51/{settlement.json, w51-taskcall.json, route-map.json,
  wave-timing.json, round-time-accounting.json, wave-grant.txt}` and `LOG.md`.
- `git ls-tree -r --name-only 907790c -- .ufo/waves/round-51/w1` -> 48 `*.md` reports (harvested whole).
- `git ls-tree -r --name-only 907790c -- .ufo/waves/round-51/route-probes` -> 2 `*.json` probes.

57 blobs total, all at the pinned rev. Grep evidence: no `rev-parse HEAD` outside the sandboxes (the only
`rev-parse HEAD` is line 669, `git -C <fixture_work_dir>`, i.e. each throwaway fixture's own HEAD); no `os.environ`/`getenv`;
the only `open(..., "w")` is line 418 writing fixture files. **The clone's HEAD and working tree are never read.**
Writes: sandbox repos under `.ufo/waves/round-52/selftest/ledger/work/<fixture>` (path is `.gitignore:4`
`.ufo/waves/round-52/selftest/`), `rmtree`d at the end; only the empty `selftest/ledger` dir survives. `git status --porcelain`
in the clone after both runs was empty, and `--ignored` listed nothing.

Proof by extra commit (second scratch clone `D2=/tmp/c1tally2.BYtD4Z` at base, then one commit
`1ae85f5dda275691ea03f8feabb52e9a096d1d19` made with `-c user.name=selftest -c user.email=selftest@local`, touching exactly the
named paths: appended a probe row to `corpus/SOURCES.md`, a line to `corpus/README.md`, added
`corpus/knowledge/probe-extra-knowledge.md`, inserted an **extra registry row** (`probe-extra-row`, itself carrying
`(19 fixtures)`) into the round-52 SKILL.md table, and added `.ufo/waves/round-56/probe/{extra.json,note.md}`):

- rerun at HEAD = `1ae85f5`: `c52 ledger selftest: 19/19`, exit 0, 2448 ms, stdout sha256
  `f33b502c9f82b920ec47c5560d9810b0dd86cd10989a6d62857e5ea1200a6880` — **byte-identical to the base runs**.

Stronger control (same `D2`, second commit `4a5f66e`): `git rm -r .ufo/waves/round-51` so HEAD *and* the working tree no
longer contain the round-51 evidence (`ls-tree HEAD -- .ufo/waves/round-51` = 0 files). Rerun: `c52 ledger selftest: 19/19`,
exit 0. The tally is a function of object `907790c` only.

Failure mode of that pin (clone `D4`, real shallow clone `--depth 1 file://…`, r51 object absent — `git cat-file -e 907790c`
fails): `selftest: missing r51 evidence .ufo/waves/round-51/settlement.json`, exit 1.

Answer: changing `corpus/SOURCES.md`, `corpus/README.md`, `corpus/knowledge/`, `SKILL.md` or adding files under
`.ufo/waves/round-56/` **cannot change the tally and cannot fail the selftest** (proved). The only ways the selftest fails are
(a) the script's own edits, (b) absence of the r51 objects at `907790c` (shallow/filtered clone), (c) running from a
subdirectory (below).

## REPLACEMENT CELL:

Because the base cell's integer already matches, this is a clarification that keeps the compared integer at 19 and adds the
printed form, the semantics of the number, and the cwd requirement. Exact cell text (5th cell of the row):

`` `python3 -B .ufo/waves/round-52/c52_wave_ledger.py --selftest` (19 fixtures, sandbox repos; prints `c52 ledger selftest: 19/19` and exits 0; the tally is the fixture count (`total` in `_selftest_fixture_files()`), not a check count; run from the repo root; receipt `.ufo/waves/round-52/control/c1-ledger-selftest.txt`) ``

Checked against the counter, not just by eye: clone `D5=/tmp/c1tally5.DH8x5F` at base with only that cell replaced,
commit `6aacfab40e37f1af611187981de39aae2e191aef`; `measure(pop=[ledger row], rev=6aacfab)` prints
`claim: 19`, `documented command: ['python3','-B','.ufo/waves/round-52/c52_wave_ledger.py','--selftest']`,
`observed: 19/19`, `exit: 0`, `problems: []`, aggregate exit 0; `re.findall(r"\((\d+) fixtures", cell) == ['19']`
(exactly one match, so the sum stays 19). The extra backticked span `c52 ledger selftest: 19/19` is not picked up by
`documented_command`/`_is_selftest_span` (the script path is not one of its words), verified by the printed command list.

## RISKS:

- **cwd must be the repo root, and this is undocumented and unguarded.** From `$D/.ufo/waves` the same command dies with
  `StopIteration` at `probe_json` (traceback, exit 1, 65 ms): `show()` uses cwd-independent `rev:path`, but `list_paths()`
  passes a *pathspec* (`git ls-tree -r --name-only <rev> -- <prefix>`), which git resolves relative to the cwd, so the
  route-probe list comes back empty and the `fail_statusconflict` fixture cannot be built. The documented command carries no
  `--root`/cwd guard; the counter is safe only because it runs with `cwd=clone`. Hence the "run from the repo root" clause in
  the replacement cell. Not a defect of the tally, but a real trap for anyone copying the command.
- **The row's "19" says nothing about gate quality.** It counts fixtures that produce their expected exit code; a mutant can
  still survive. Mutant coverage lives in the separate Pinned-values cell (`c52_mutation_ladder.py`, 13 of 18 families), and
  the counter does not test it.
- **The selftest is pinned to a historical object, not to HEAD.** A shallow or partial clone (`--filter=blob:none`, CI
  `--depth 1`) fails with `selftest: missing r51 evidence …`, exit 1, and the counter's `parse_tally` would then find no
  tally and return exit 2 `tally_unparsable` — an unevaluable, not a red, result. `c56_selftally.py:clone_at` does a full
  clone, so the round-56 measurement is safe; a future CI harness must not shallow-clone.
- **`tool_changed` guard.** The counter also requires `blob(rev, script) == blob(base, script)`; the script must not be edited
  while this row is being recalibrated — my replacement is SKILL.md-only, so that guard stays green.
- Selftest writes into the measured tree (`.ufo/waves/round-52/selftest/`, gitignored). Harmless in a clone, but it means the
  selftest is not strictly read-only; a lane run leaves an empty ignored `selftest/ledger` directory behind.
- Not tested (out of scope, named for honesty): whether the 19 fixtures still detect anything after a future edit of the
  round-52 ledger logic (mutant surface), and the other two already-agreeing rows.

VERDICT: Row `wave-evidence-ledger` is already calibrated — documented selftest prints `19/19`, exit 0, twice byte-identical (2953/4134 ms), N = 19 sandbox-repo fixtures, counter agrees (claim 19 == observed 19, problems []); the tally is HEAD-independent (identical output after an extra commit touching corpus/, SKILL.md, .ufo/waves/round-56/, and after deleting round-51 evidence at HEAD) and reads only rev `907790c`; replacement cell supplied and verified at claim 19 / observed 19/19 / exit 0; residual risk is the undocumented run-from-root requirement (subdir run crashes) and shallow-clone fragility.
