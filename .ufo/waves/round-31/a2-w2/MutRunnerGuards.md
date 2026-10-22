# MutRunnerGuards — round 31 attempt 2, wave 2 (falsify), C1 guard-mutation coverage

Seat: KakeR31a2.MutRunnerGuards (mutation tester, leaf). Axis judged: operability. Milestone r31-falsify.
Target: does the hostile selftest kill a mutant of each of the five runner guards in `scripts/citing_set_selftest.py`?

Sandbox `/fast/scratch/hyaku/kake-r31/a2-w2/MutRunnerGuards/`, TMPDIR `<sandbox>/tmp`, Python 3.14.8, git 2.56.0.
No installs, no network, no lane writes other than this report.

## Result

Four of the five assigned guards are killed by the committed hostile selftest and by the declared C1 counter
(m1, m2, m4, m5). **One survives: m3 (git_commit no longer requires an earlier git_init).** The runner still
refuses the shape at a second layer, so the spec cannot see the removal of the first. Removing that second
layer too (m3b) still survives, because the `--git-dir`/`--work-tree` pin makes the failing `git` command
refuse the enclosing repository anyway. Only removing the git_init requirement *and* the Git pins together
(m3c) produces the harm the spec looks for (victim repository changed) and is killed. The P3 spec therefore
constrains one specific combination, not each guard. The same verdicts hold at the lane tip `9a7f5be`, whose
runner changed after `fde133a`, so this is not an artifact of the older commit.

Ran at two commits: base `fde133ab48086bb9a06911b4ab045e2ad9086347` (runner sha256
`5371530d93ecb218b4607fb37de810fe7b7b2db869c65c8b65988b2f04c0ce6c`) and lane tip
`9a7f5be2b2091fc9b76adc803b8b442d5c292d08` (runner sha256
`7c95a18e4621ca6c4f0085eb9d208a0f1e6a1211989e51dd0c733ee1488b8969`); verdicts identical. Clones
`<sandbox>/clone` (fde133a) and `<sandbox>/clone-tip` (9a7f5be). The lane checkout was never written; both
clones' runner files hash to the pristine values after every mutant (`restoreOk: true` in every record).

## Detector baseline (pristine, must be green before any mutant counts)

`python3 -B scripts/citing_set_hostile_selftest.py --root <clone> --tmpdir <sandbox>/h-base` -> exit 0, 5/5
specs passed. `python3 -B scripts/citing_set_selftest.py --root <clone> --tmpdir <sandbox>/b-base` -> exit 0,
45 cases, `failed: 0`. Evidence `<sandbox>/h-base.json`, `<sandbox>/b-base.json`.

## Mutant table (at the tip `9a7f5be`; identical at `fde133a`)

| mutant | diff (3 lines max) | hostile selftest | benign 45 | verdict |
|---|---|---|---|---|
| m1 argv allowlist accepts every token | `argv_refusal` body -> `return None` | exit **1**, P1-selftest-argv fails, **canary written** | exit 0, 45/45 | **KILLED** |
| m2 fixture `.git` refusal removed | `dot_git = dot_git_entry(case_dir)` + `if dot_git is not None: ... return row` deleted from `run_case` | exit **1**, P2-fixture-dot-git fails; h2b no longer refused (only h2a is) | exit 0, 45/45 | **KILLED** |
| m3 git_commit no longer requires an earlier git_init | `if step["op"] == "git_commit" and not initialized: raise ValueError(...)` deleted from `load_case_setup` | exit **0**, 5/5 pass; P3 still refuses h3 at `apply_setup` ("case setup failed: git_commit needs the repository created by git_init") | exit 0, 45/45 | **SURVIVED** |
| m4 expected.json read with plain open() | `read_expected` body -> `with open(path, "r", encoding="utf-8") as handle: return handle.read()` | exit **1**, P4-expected-json-guard fails, **`timedOut: true`** (hangs on the FIFO) | exit 0, 45/45 | **KILLED** |
| m5 symlinked case skipped instead of failed | discovery `path.is_symlink() or (path.is_dir() and ...)` -> `path.is_dir() and not path.is_symlink() and ...` | exit **1**, P5-symlinked-case fails; runner exits **0**, symlinked case vanishes | exit 0, 45/45 | **KILLED** |

Per-mutant evidence (mutant sha256, restored sha256, per-spec detail): `<sandbox>/tip-mutation-results.json`,
`<sandbox>/tip-h-<m>.json`, `<sandbox>/tip-b-<m>.json`; at fde133a `<sandbox>/mutation-results.json`,
`<sandbox>/h-<m>.json`, `<sandbox>/b-<m>.json`.

## The declared counter agrees

`.ufo/waves/round-31/c1_sandbox_probes.py --root <clone> --revision <mutant commit> --scratch <dir>`. The
counter exports `scripts/` with `git archive`, so each mutant was committed **inside the sandbox clone only**;
the lane was never committed to. Per mutant: m1 4/5 (P1 fails), m2 4/5 (P2 fails), m3 **5/5**, m4 4/5 (P4
fails), m5 4/5 (P5 fails); control K1 held (45 cases) in every run. At fde133a `<sandbox>/counter-results.json`;
at the tip `<sandbox>/tip-mutation-results.json` (`counter` field). The counter's P3 probe fails only for m3c,
exactly like the hostile spec.

## Attribution of the m3 survivor

"git_init before git_commit" is enforced at three independent layers in the tip runner: L1 load-time
`load_case_setup` lines 362-363; L2 apply-time `apply_setup` lines 489-490; L3 Git binding `git_command`
lines 447-451 (`--git-dir`/`--work-tree` inside the copy) and `git_env` line 443 (`GIT_CEILING_DIRECTORIES`
= the copy's parent). Probes at the tip, each removing exactly one layer set:

| probe | removed | hostile | counter | victim repo |
|---|---|---|---|---|
| m3 | L1 only | exit 0, 5/5 | 5/5 | unchanged |
| m3b | L1 + L2 | exit 0, 5/5 (P3 refuses h3: "setup command failed (128): fatal: not a git repository: .../cases/h3/.git") | 5/5 | unchanged |
| m3c | L1 + L2 + L3 pins | exit **1**, P3 fails, **victimUnchanged: false** | 4/5 (P3 fails) | **changed** |
| m3d | L3 setup pins only | exit 0, 5/5 | 5/5 | unchanged |
| m3e | L1 + L2 only, pins kept | exit 0, 5/5 | 5/5 | unchanged |
| m3f | L3 setup pins + gate ceiling | exit 0, 5/5 | 5/5 | unchanged |
| m3g | gate ceiling only | exit 0, 5/5 | 5/5 | unchanged |

Evidence `<sandbox>/pins-mutation-results.json` (m3d, m3e), `<sandbox>/pins2-mutation-results.json` (m3f, m3g),
`<sandbox>/tip-mutation-results.json` (m3, m3b, m3c).

Reading: **P3 is a joint test of L1+L2+L3, not of any one of them.** The harm it looks for (victim HEAD/refs/
commit count changing) can only happen when all three are gone. A runner that lost L1 alone, or L1+L2, or L3
alone, still refuses the shape and still leaves the victim untouched, so no committed instrument distinguishes
it from the pristine runner. The contract is not broken; the coverage is incomplete. This also confirms the
tip docstring at `scripts/citing_set_selftest.py:83-85` ("The Git pins ... are not separately probed: a runner
without them still passes the hostile selftest and the round-31 C1 counter") — m3d and m3f show that sentence is
accurate as written; m3/m3b/m3e add that the *git_init requirement* is equally unprobed on its own.

## Findings (advisory; the contract is unchanged)

1. **m3 survives — the "git_init required" guard has no committed fixture of its own.** P3 is satisfied by L2
   or by L3 alone. A future edit dropping L1 and L2 together, leaving L3, is invisible to both instruments;
   only the three-layer removal is caught. A per-layer fixture (e.g. a case whose copy already holds a `.git`
   *directory*, so L3 cannot be the thing that refuses) would close this.
2. **m2 is killed for a partly incidental reason.** With the `.git` refusal removed, h2b (setup `mkdir`) is no
   longer refused; h2a still fails for the unrelated L1 reason. The spec requires *every* hostile case to be a
   failure, so one leaked case suffices. The victim repository was untouched, so the harm channel did not fire.
3. **m4's kill is a hang, not a wrong answer.** The mutant blocks on the FIFO until the 90 s limit
   (`timedOut: true`); the spec's timeout clause catches it. The benign suite stays green because no committed
   fixture uses a FIFO for `expected.json`.
4. **m5 has two independent tripwires** (discovery keeps symlinks; `run_case` refuses `case_dir.is_symlink()`),
   so either one alone keeps the case counted as a failure.

## Commands (exit codes)

- `git clone -q ... <sandbox>/clone` + `checkout -q fde133a...` -> 0; `clone-tip` at 9a7f5be -> 0.
- pristine hostile selftest -> 0; pristine 45 benign fixtures -> 0.
- `python3 -B mutate.py` (m1..m5 at fde133a) -> 0; `m1 hostile_exit=1 benign_exit=0 restored_ok=True` ...
  `m5 ... restored_ok=True`, `pristine_sha256 5371530d...ce6c`.
- `python3 -B mutate_m3.py` (m3b, m3c at fde133a) -> 0; `m3b hostile_exit=0`, `m3c hostile_exit=1`.
- `python3 -B mutate_counter.py` (declared counter per mutant commit at fde133a) -> 0; m1/m2/m4/m5 4/5,
  m3/m3b 5/5, m3c 4/5; `clone restored sha256 5371530d... match True`.
- `python3 -B mutate_tip.py` (m1..m5, m3b, m3c at 9a7f5be: hostile + benign + counter) -> 0; m1/m2/m4/m5/m3c
  4/5 with the matching probe failing, m3/m3b 5/5; all `restore=True`.
- `python3 -B mutate_pins.py` (m3d, m3e) -> 0; both hostile exit 0, counter 5/5.
- `python3 -B mutate_pins2.py` (m3f, m3g) -> 0; both hostile exit 0, counter 5/5.

## What I did not verify

- The mutants are single-point edits to the runner only. I did not mutate `scripts/citing_set.py` (the gate),
  `scripts/citing_set_hostile_selftest.py`, or the hostile specs themselves.
- I did not re-derive the lane's after-receipts; the L1's `c1-a2-at-9a7f5be.json` (5/5, K1 hold) is consistent
  with my pristine runs but is not my measurement.
- I did not search for benign fixtures distinguishing L1 from L2 (the finding is that none exists).
- Nothing was fetched from the network; no owned web property was contacted.
