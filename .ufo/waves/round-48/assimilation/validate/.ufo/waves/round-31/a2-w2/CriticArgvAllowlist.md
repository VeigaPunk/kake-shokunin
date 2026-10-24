# CriticArgvAllowlist — C1 N1 argv allowlist edge cases (kake r31 a2 w2, falsify)

Axis: operability. Target: `argv_refusal` in `scripts/citing_set_selftest.py:356-372` at fde133a, compared with the
gate parser `scripts/citing_set.py:785-831`: `GateParser.error` exits 64; `StoreOnce` is at 800-816 and
`build_parser` at 819-831; `parse_args` is called at 882. Between fde133a and the tip 92235a0, nothing under `scripts/` changed.

Verdict: N1 holds. I found no token that the allowlist admits and that argparse then routes to `--selftest`, `--json`
or `--help`. One real defect is still open: ReviewHostileContract F1, where `--r` is admitted but argparse rejects it
as ambiguous. It is low severity and harms no axis today. I also found two smaller issues, described below.

## Method (sandbox /fast/scratch/hyaku/kake-r31/a2-w2/CriticArgvAllowlist/, TMPDIR=<sandbox>/tmp)
- `git clone -q <lane> <sb>/clone && git -C <sb>/clone checkout -q fde133ab48086bb9a06911b4ab045e2ad9086347`, then
  `git diff --stat fde133a 92235a0 -- scripts` (empty output). Exit 0.
- `python3 -B argv_probe.py <sb>/clone`, exit 0 (Python 3.14.8). The probe imports both modules. It calls
  `argv_refusal(case)` and then `gate.build_parser().parse_args(PREFIX + case)`, where PREFIX is the runner's real
  prefix (`--root X --population population.json --ledger ledger.json --json`, runner.py:556-569). It only parses
  and never calls gate `main`, so delegation never runs. It also sweeps every `--` + s for len(s) ≤ 4 over the option
  letters plus `=` and `x`.
  Script sha256 444c0e7b…8198b; output `<sb>/argv_probe.out.json` sha256 93621f03…147af.
- `python3 -B mutant_probe.py <sb>/clone`, exit 0. Output: `<sb>/mutant_probe.out.json`.

## Table (gate behaviour = argparse with the token after the runner prefix)
| token(s) | allowlist | gate behaviour | verdict |
|---|---|---|---|
| `--` | refused | exit 64: unrecognized arguments | right (`--` would make everything after it positional) |
| `-` | refused | exit 64: unrecognized | right |
| `--=x` | refused (empty name) | exit 64: ambiguous, could match all 7 options | right |
| `--SELFTEST` | refused | exit 64: unrecognized (match is case-sensitive) | right |
| `--selftest=1` | refused | exit 64: ignored explicit argument '1' | right |
| `--selftest` | refused | parsed, selftest=True, so delegation would run | right (this is the N1 vector) |
| `--s` | refused | parsed, selftest=True | right (abbreviation vector) |
| `--j` | refused | parsed as --json (a harmless repeat) | over-strict but harmless, as the docstring documents |
| `--h`, `-h`, `--help` | refused | exit 0 with usage text and no JSON | right (it would give a false exit 0) |
| `-s` | refused | exit 64: unrecognized | right |
| `--r`, `--r HEAD`, `--r=HEAD` | ADMITTED | exit 64: ambiguous (--root, --revision) | WRONG versus the contract (F1 confirmed). No containment hole |
| `--re HEAD` | admitted | revision='HEAD' | right |
| `--ro .`, `--root=.`, `--l x`, `--p x`, `--ledger x` | admitted | exit 64: given more than once (StoreOnce) | right |
| `--ledger` (alone) | admitted | exit 64: expected one argument | right |
| `--rev=--selftest`, `--revision=--selftest` | admitted | revision='--selftest', selftest=False | right (the value never becomes an option) |
| `--revision --selftest` | refused at `--selftest` | exit 64: expected one argument | right |
| `--revision HEAD --selftest` | refused | selftest=True | right (P1 h1c) |
| `--self test` (two tokens) | refused at `--self` | exit 64: unrecognized `test` | right (P1 h1b) |
| `-- --selftest`, `--revision HEAD -- --selftest` | refused at `--` | exit 64: unrecognized | right |
| `@args.txt`, `@--selftest` | admitted (treated as a value) | exit 64: unrecognized. No fromfile_prefix_chars anywhere in scripts/ | right |
| `--revision @HEAD`, `--revision=@x` | admitted | revision taken literally | right |
| em dash, en dash, minus sign, fullwidth or U+2010 hyphen + `selftest`/`revision` | admitted (treated as a value) | exit 64: unrecognized (argparse prefix_chars is ASCII `-`) | right |
| `--ſelftest` (long s), `--revіsion` (Cyrillic i) | refused | exit 64: unrecognized (no case folding or normalisation) | right |
| `''` (empty string) | admitted (treated as a value) | exit 64: unrecognized | right |
| `--revision ''`, `--rev=` | admitted | revision='' | right (the gate then handles it) |
| `-1` | refused | exit 64: unrecognized | right |
| `--revision -1` | refused at `-1` | revision='-1' (argparse accepts negative-number values) | over-strict; harmless (Git refuses `-` revisions anyway) |
| `--revision=-1` | admitted | revision='-1' | right; it is inconsistent with the space form, but harmless |
| `--revision HEAD` (one token with a space), `--selftest x` | refused | exit 64: unrecognized (argparse treats it as positional) | right |

Sweep: 1242 admitted tokens produced 0 violations (none set selftest, json, or exit 0). There were 382 ambiguous
results, and every one is `--r` or `--r=…`.

## Findings
- LOW — F1 confirmed. The docstring requires `name` to be a "prefix of root, revision, population or ledger and
  of no other gate option" (runner.py:67-70, 360-362). `--r` satisfies that wording, so the code matches the docs,
  but argparse rejects it as ambiguous. If a future case used it, it would show up as an ordinary gate exit-64
  outcome, and the expectation would record exit 64 instead of the argv refusal. Smallest safe correction, at
  runner.py:369: replace `not any(option.startswith(name) for option in GATE_VALUE_OPTIONS)` with
  `sum(option.startswith(name) for option in GATE_VALUE_OPTIONS) != 1`, and add "and of exactly one of them" to the
  docstrings. Mutant M2 tests exactly this. Over 505,263 tokens (leads `--`, `-` and none, with bodies up to 4
  characters), it differs from the shipped code on 446 tokens, and every one is the `r` family. None of the 8
  committed case.json argvs uses `--r` (36: `--revision`; 37: `--revision`; 42: `--population`; 43: `--ledger=`;
  44: `--roo`; 45: `--revision`/`--rev`), so all 45 cases stay admissible.
- INFO — dead clause today. Mutant M1 drops the `GATE_OTHER_OPTIONS` test (runner.py:370) and differs on 0 of
  505,263 tokens, because no valued option shares a first letter with json, selftest or help. The clause only
  matters if the gate later gains a flag whose exact name is a prefix of a valued option (for example `--rev`), and
  only if someone adds that flag to the hard-coded tuple. Nothing ties `GATE_VALUE_OPTIONS`/`GATE_OTHER_OPTIONS`
  (runner.py:131-132) to `gate.build_parser()`. Even so, an admitted name is always a prefix of some valued option,
  so a new gate option can only cause an ambiguity exit 64, never a silent route. Keeping the clause is a design
  choice, not a defect.
- INFO — this counters part of ReviewHostileContract F2. The claim that "argparse last-wins lets case argv override
  the runner's own values" is false at fde133a. The runner always passes `--root`, `--population` and `--ledger`
  first, so any case spelling of those (`--root=/`, `--ro .`, `--l x`, `--p x`) hits StoreOnce and exits 64. Only
  `--revision` (with any of its unique abbreviations, once) can actually be set from case argv. Values stay free-form
  but cannot become options.
- INFO — coverage. The hostile P1 spec (`scripts/fixtures/citing-set-hostile/P1-selftest-argv/hostile.json`) tests
  `--selftest`, `--self` and a trailing `--selftest`. No hostile spec tests `--s`, `--h`/`-h` (which would give exit 0
  with no JSON), `--`, or `--r`. The table above shows the code refuses all of these today, but no committed probe
  pins that behaviour.

## Not verified
- I did not run the runner or hostile selftest end to end on these tokens; I only made in-process
  `argv_refusal` + `parse_args` calls. I did not run gate `main` or the delegation path.
- I checked only Python 3.14.8 argparse. Abbreviation and `=` handling has changed across 3.x versions.
- I did not run the C1 counter (`c1_sandbox_probes.py`); that belongs to KakeR31a2.RerunC1Counter.
- Installs: none. Lane writes: this report only.

Report: .ufo/waves/round-31/a2-w2/CriticArgvAllowlist.md
