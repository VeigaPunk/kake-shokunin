# MutPriorMutantsStillKilled — round 32, wave 1 (falsifier)

Seat: KakeR32.MutPriorMutantsStillKilled (mutation tester, leaf). Axis judged: operability. Milestone r32-build.
Target: C1 no-harm — the round-31 single-guard mutants m1, m2, m4, m5 stay killed at the lane tip
`285abcad632e3c1c57bb402232e7d218054db383`.

## Verdict

**PASS. All four mutants are still killed by the committed hostile selftest at the lane tip.**
Hostile selftest exits 1 for each of m1, m2, m4, m5, and each mutant is caught by exactly its own
hostile spec. The 45 benign fixtures stay clean (45 cases, `failed: 0`) under every mutant, and the
pristine baseline is green. No harm found; C1 is not weakened by the round-32 repair.

## Sandbox

`/fast/scratch/hyaku/kake-r32/w1/MutPriorMutantsStillKilled/`
- `clone/` — `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone` then `checkout -q 285abcad632e3c1c57bb402232e7d218054db383` (HEAD `285abca`).
- `mutate.py` — the harness (applies each mutant to a **copy** of the runner, runs the hostile selftest and the benign suite, records JSON).
- `mutation-results.json`, `h-<m>.json`, `b-<m>.json`, `h-base.json`, `benign-cases.json`, `literal-commands.json` — evidence.
- TMPDIR `/fast/scratch/hyaku/kake-r32/w1/MutPriorMutantsStillKilled/tmp`. Nothing under `/tmp` or `/dev/shm`.
- Python 3.14.8, git 2.56.0. No installs, no network, no owned web property contacted.

## Baseline (pristine, must be green before a mutant counts)

- `python3 -B scripts/citing_set_hostile_selftest.py --root <clone> --tmpdir <sandbox>/h-base --runner <clone>/scripts/citing_set_selftest.py` → exit **0**, `passed: true`, 6/6 specs (P1…P6).
- `python3 -B scripts/citing_set_selftest.py --root <clone> --tmpdir <sandbox>/b-base` → exit **0**, `cases: 45`, `failed: 0`, `verdict: clean`.
- Runner sha256 `7c95a18e4621ca6c4f0085eb9d208a0f1e6a1211989e51dd0c733ee1488b8969` (identical to the round-31 tip runner; the round-32 change added the P6 **spec**, not runner bytes).

## Mutant table (definitions taken verbatim from `.ufo/waves/round-31/a2-w2/MutRunnerGuards.md`)

| mutant | edit to `scripts/citing_set_selftest.py` | hostile exit | failing spec(s) | benign 45 | verdict |
|---|---|---|---|---|---|
| m1 | `argv_refusal` body → `return None` (allowlist accepts every token) | **1** | `P1-selftest-argv` | exit 0, 45/45 | **KILLED** |
| m2 | `dot_git = dot_git_entry(case_dir)` + the `.git` refusal block deleted from `run_case` | **1** | `P2-fixture-dot-git` | exit 0, 45/45 | **KILLED** |
| m4 | `read_expected` body → plain `open(path, "r", encoding="utf-8")` | **1** | `P4-expected-json-guard` | exit 0, 45/45 | **KILLED** |
| m5 | discovery filter `path.is_symlink() or (path.is_dir() and …)` → `path.is_dir() and not path.is_symlink() and …` | **1** | `P5-symlinked-case` | exit 0, 45/45 | **KILLED** |

The acceptance command form was also run literally for each mutant
(`python3 -B scripts/citing_set_hostile_selftest.py --root <clone> --tmpdir <sandbox>/h --runner <mutant>`);
exit codes 1/1/1/1 with the same failing specs (`literal-commands.json`).

## Observed detail per mutant

- **m1** — P1 fails with runner exit 1 and **`canary: true`** (the planted script ran): h1a/h1b/h1c report
  `gate report carries no 'findings' array` instead of the argv refusal
  (`case.json argv refused: --selftest` / `--self`). The other five specs pass; victim repository unchanged.
- **m2** — P2 fails: the `.git` refusal is gone, so h2a now fails for the unrelated reason
  `case.json setup op 'git_commit' needs an earlier 'git_init'` and h2b is no longer refused at all
  (only h2a appears in the failure list, so the spec's "every hostile case must fail" clause fires).
  Victim repository unchanged — the kill is a leak-detection kill, not a harm kill.
- **m4** — P4 fails with `exit: null` and **`timedOut: true`**: the plain `open()` blocks on the FIFO
  `expected.json` until the 90 s spec timeout. The kill is a hang, not a wrong answer.
- **m5** — P5 fails with runner **exit 0** and an empty failure list: the symlinked cases `h5` / `.h5b`
  are skipped by discovery, so the runner never sees them and reports clean. The spec demands the symlink
  case be *refused*, not *skipped*.

## Commands and exit codes

- `git clone -q … clone` → 0; `git -C clone checkout -q 285abcad…` → 0.
- `python3 -B mutate.py` (all four mutants + baseline, hostile + benign) → 0;
  `baseline hostile exit=0 passed=True benign exit=0 failed=0`;
  `m1 hostile exit=1 failed_specs=['P1-selftest-argv']`, `m2 … ['P2-fixture-dot-git']`,
  `m4 … ['P4-expected-json-guard']`, `m5 … ['P5-symlinked-case']`; benign exit 0 / failed 0 for all four.
- Literal acceptance command rerun per mutant → exit 1 for each, same failing specs.
- Benign case-count probe → pristine and all four mutants: `cases: 45`, `failed: 0`, `verdict: clean`.

## Restoration evidence

- Mutants were written as **separate copies** under `<sandbox>/mutants/`; the clone's runner was never edited.
  `sha256sum clone/scripts/citing_set_selftest.py` after all runs = `7c95a18e…b8969`, equal to the pristine hash.
- `restored_ok: true` for m1, m2, m4, m5 in `mutation-results.json`; each mutant copy was deleted after its run.
- `git -C clone status --porcelain` → empty (only the lane repo shows unrelated sibling files, none of them mine).

## What I did not verify

- I did not re-derive the L1's C1 receipts or the declared counter `.ufo/waves/round-32/c1_m3_probe.py`
  output; that counter exercises m3, not m1/m2/m4/m5, and m3 is another seat's line (KakeR32.MutM3Variants).
- I mutated the runner only; I did not mutate `scripts/citing_set.py` (the gate), the hostile selftest, or the
  hostile specs themselves.
- Verdict is at the tip `285abcad` only; not re-run at the base `a0b0dff`. No network, no owned web property, no package installed.
