# ExecC1Rows — round 74 w1 counter evidence

Measured committed revision: `ced2878a1e77f57afb4ee3baebf1021e5130399b`. All executions ran in the shared scratch clone; no production edits. Axes: calibration, reproducibility, scratch operability. No installs.

## Summary

| Counter | Selftest / usage | Round-74 base | Kind |
|---|---|---|---|
| c69_recorded_counts.py | selftest 6/6; exit 0 | 0 | one-off instrument |
| c69_tmp_honour.py | no selftest mode; exit 2 | 0 | revision instrument |
| c70_pointer_audit.py | selftest 4/8; exit 1 | 1 | one-off instrument |
| c71_calibration.py | no selftest mode; exit 64 | 2 | one-off instrument |
| c71_tmp.py | no selftest mode; exit 64 | 1 | one-off instrument |
| c72_tmp_v2.py | C2v2 selftest 11/11; exit 0 | 0 | bounded gate v2 |
| c73_wave_pointers.py | selftest 6/6; exit 0 | 0 | one-off instrument |

Important: c69 TMP also has **no selftest mode** (usage exit 2). Its normal run executes the nested sweep selftest: `selftest: 36/36 passed`, exit 0. c70 selftest fails 4 cases under required `/fast` TMPDIR: minted tokens use TMPDIR, but the counter tmp-token regex only recognizes `/tmp/`. No fallback to forbidden system scratch was attempted. c70 with the original frozen `--base` fails append-only; a run omitting that flag would not establish the amended predicate. c71 calibration cannot evaluate the later revision because its exactly-one attack-share population has become two. c71 TMP has zero unannotated tokens but a failing historical replacement guard.

## Per-counter rows

### c69_recorded_counts.py

- Path: `.ufo/waves/round-69/c69_recorded_counts.py`
- Contract: `.ufo/waves/round-69/contract.md §C1 + Amendment 1`
- Frozen predicate (original sentence; whitespace joined): C1 is met iff `python3 -B .ufo/waves/round-69/c69_recorded_counts.py --root <lane> --revision <rev> --pairs .ufo/waves/round-69/c1/pairs.json` prints `unrelabelled=0` and exits 0.
- Frozen amendments / terms: Amendment 1 pins 20 pairs unchanged in id, rev, path, command and recorded_value; correction clears only an exact first-cell id and observed integer in the correction locus.
- Kind: One-off historical recorded-count correction instrument over the frozen 20-pair set; not a general count-correctness gate.
- Verdict map: 0 met; 1 not met; 2 usage/IO/instrument fault
- Pinned inputs: .ufo/waves/round-69/c1/pairs.json (20 pairs; sha256 4e787bcb7b588416dbe4db5d76a2e263cf147c26f3faeecdf826f4c198a9e9be); Each pair command and its historical revision; correction_locus corpus/lessons/round-69.md at measured revision; exact correction_id and observed integer
- Withdrawal / re-pin: Withdraw green if pairs bytes, named historical revisions or correction rule change/unavailable; re-pin only through an explicitly new population/contract. Original round-69 base must stay red.

Entry / measured base command (cwd `/fast/scratch/hyaku/kake-r74/ExecC1Rows/lane`):

```sh
python3 -B .ufo/waves/round-69/c69_recorded_counts.py --root /fast/scratch/hyaku/kake-r74/ExecC1Rows/lane --revision ced2878a1e77f57afb4ee3baebf1021e5130399b --pairs .ufo/waves/round-69/c1/pairs.json
```

Base summary (exit 0):

```text
pairs=20 mismatches=1 relabelled=1 unrelabelled=0 met=true
```

Selftest command:

```sh
python3 -B .ufo/waves/round-69/c69_recorded_counts.py --selftest --work /fast/scratch/hyaku/kake-r74/ExecC1Rows/work-0
```

Tally: `selftest 6/6`; exit 0.

Exact environment, full stdout/stderr, argv and exit: `ExecC1Rows/c69_recorded_counts-base.json` and `ExecC1Rows/c69_recorded_counts-selftest.json`.

### c69_tmp_honour.py

- Path: `.ufo/waves/round-69/c69_tmp_honour.py`
- Contract: `.ufo/waves/round-69/contract.md §C2 + Amendment 1`
- Frozen predicate (original sentence; whitespace joined): C2 is met iff `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root <lane> --revision <rev> --work <scratch dir>` prints `tmp_literals=0 selftest_under_tmpdir=true offline_exit=0` and exits 0.
- Frozen amendments / terms: Amendment 1 explicitly replaces offline_exit=0 with offline_unchanged=true: offline exit and VERDICT must equal frozen round-69 baseline on this host. TMPDIR and HOME are distinct; fixture must appear only under TMPDIR and must not be a symlink. The original sentence above is preserved rather than silently rewritten.
- Kind: Reusable revision instrument for the sweep TMPDIR/no-literal/no-offline-regression conjunction, pinned to the round-69 baseline; no standalone counter selftest mode.
- Verdict map: 0 met; 1 not met; argparse usage 2; runtime failures are not a uniform unevaluable map (SystemExit errors may be 1; uncaught exceptions may be 1)
- Pinned inputs: scripts/freshness-sweep.mjs and full git archive at measured revision; Frozen baseline 4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4 (not overridden); Node runtime, host state, ambient HOME for offline comparison; fresh distinct HOME/TMPDIR for nested selftest
- Withdrawal / re-pin: Withdraw if literals return, placement fails or offline result differs from frozen same-host baseline; host/runtime/baseline changes require fresh side-by-side receipts. Counter-level selftest cannot be claimed.

Entry / measured base command (cwd `/fast/scratch/hyaku/kake-r74/ExecC1Rows/lane`):

```sh
python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root /fast/scratch/hyaku/kake-r74/ExecC1Rows/lane --revision ced2878a1e77f57afb4ee3baebf1021e5130399b --work /fast/scratch/hyaku/kake-r74/ExecC1Rows/work-1
```

Base summary (exit 0):

```text
tmp_literals=0 selftest_under_tmpdir=true offline_unchanged=true
```

Selftest command:

```sh
python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root /fast/scratch/hyaku/kake-r74/ExecC1Rows/lane --revision ced2878a1e77f57afb4ee3baebf1021e5130399b --work /fast/scratch/hyaku/kake-r74/ExecC1Rows/work-1 --selftest
```

Tally: `no selftest mode`; exit 2.

Help command: `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --help`; exit 0. Argparse prints supported flags without --selftest.

Exact environment, full stdout/stderr, argv and exit: `ExecC1Rows/c69_tmp_honour-base.json` and `ExecC1Rows/c69_tmp_honour-selftest.json`.

### c70_pointer_audit.py

- Path: `.ufo/waves/round-70/c70_pointer_audit.py`
- Contract: `.ufo/waves/round-70/contract.md §C1 + amendment-1-note.md §C1`
- Frozen predicate (original sentence; whitespace joined): C1 is met iff `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root <lane> --revision <rev>` prints `unannotated=0` and exits 0.
- Frozen amendments / terms: Amendment 1 adds --base and append_only=true (SCORECARD base is an unchanged line-prefix), 8 selftest cases, revised extraction and annotation rules. Both the original sentence and amendment are retained.
- Kind: One-off historical SCORECARD pointer-calibration instrument when run with the original append-only baseline; not an unrestricted continuing gate.
- Verdict map: 0 met; 1 not met; 2 usage/IO fault
- Pinned inputs: SCORECARD.md at measured revision; Pointer calibration (round 70) exact-token table rows; Append-only --base e5f6fd9e4c243d092160bc74e8bea24256087173; Host HOME and tmp existence; regex population from Amendment 1
- Withdrawal / re-pin: Current guarded measurement is red; do not label it live/green. Withdraw full-selftest claim (4/8 at mandated scratch TMPDIR). Re-pin only under a new explicit baseline/contract if later SCORECARD edits are intended; retain old red and TMPDIR portability defect.

Entry / measured base command (cwd `/fast/scratch/hyaku/kake-r74/ExecC1Rows/lane`):

```sh
python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root /fast/scratch/hyaku/kake-r74/ExecC1Rows/lane --revision ced2878a1e77f57afb4ee3baebf1021e5130399b --base e5f6fd9e4c243d092160bc74e8bea24256087173
```

Base summary (exit 1):

```text
pointers=362 dangling=17 annotated=17 unannotated=0 append_only=false met=false
```

Selftest command:

```sh
python3 -B .ufo/waves/round-70/c70_pointer_audit.py --selftest --work /fast/scratch/hyaku/kake-r74/ExecC1Rows/work-2
```

Tally: `selftest 4/8`; exit 1.

Exact environment, full stdout/stderr, argv and exit: `ExecC1Rows/c70_pointer_audit-base.json` and `ExecC1Rows/c70_pointer_audit-selftest.json`.

### c71_calibration.py

- Path: `.ufo/waves/round-71/c71_calibration.py`
- Contract: `.ufo/waves/round-71/contract.md §C1`
- Frozen predicate (original sentence; whitespace joined): C1 met iff mismatches == 0 and the append-only guard holds, where mismatches = stale_planned + attack_share_mismatch.
- Frozen amendments / terms: Guard permits only Planned-to-Superseded heading replacements; all other base lines survive. Exactly one uncorrected attack-share statement is required by code.
- Kind: One-off round-71 self-assessment instrument with a frozen population and heading-replacement guard; not a continuing calibration gate.
- Verdict map: 0 met; 1 not met; 2 unevaluable; 64 usage
- Pinned inputs: Frozen baseline cc6b4e0b8c35e72dfb02c6184b847f68c1262153 SCORECARD.md; Measured SCORECARD.md and .ufo/waves/round-70/w1-results.json; Strict roles reviewer, critic, mutation-tester, labrat; Correction (round 71) recomputed share
- Withdrawal / re-pin: Unevaluable at round-74 base: two stated attack-share lines violate exactly-one population. Do not claim green; any broader population requires a new contract/counter, not a silent re-pin.

Entry / measured base command (cwd `/fast/scratch/hyaku/kake-r74/ExecC1Rows/lane`):

```sh
python3 -B .ufo/waves/round-71/c71_calibration.py --lane /fast/scratch/hyaku/kake-r74/ExecC1Rows/lane --revision ced2878a1e77f57afb4ee3baebf1021e5130399b
```

Base summary (exit 2):

```text
C1 unevaluable: stated attack-share population is 2, frozen population is 1
```

Selftest command:

```sh
python3 -B .ufo/waves/round-71/c71_calibration.py --selftest
```

Tally: `no selftest mode`; exit 64.

Help command: `python3 -B .ufo/waves/round-71/c71_calibration.py --help`; exit 64. Both --help and --selftest print the module usage/docstring on stderr and exit 64; no selftest mode.

Exact environment, full stdout/stderr, argv and exit: `ExecC1Rows/c71_calibration-base.json` and `ExecC1Rows/c71_calibration-selftest.json`.

### c71_tmp.py

- Path: `.ufo/waves/round-71/c71_tmp.py`
- Contract: `.ufo/waves/round-71/contract.md §C2`
- Frozen predicate (original sentence; whitespace joined): C2 met iff unannotated_tokens == 0 and the replacement guard holds.
- Frozen amendments / terms: Annotated means the exact phrase not an executable instruction; repointed recipe has mktemp and no token. Guard requires equal removed/added counts, removed lines with tokens and added lines with annotation or mktemp.
- Kind: One-off round-71 seven-token repair instrument with an equal-count replacement guard; not a continuing SKILL.md gate.
- Verdict map: 0 met; 1 not met; 2 unevaluable; 64 usage
- Pinned inputs: Frozen baseline cc6b4e0b8c35e72dfb02c6184b847f68c1262153 SKILL.md; Measured SKILL.md; exact annotation phrase and replacement guard
- Withdrawal / re-pin: Red at round-74 base: replacement guard fails despite zero unannotated tokens. Preserve as historical round-71 repair instrument; a continuing gate needs an explicitly new contract/counter (v2 exists).

Entry / measured base command (cwd `/fast/scratch/hyaku/kake-r74/ExecC1Rows/lane`):

```sh
python3 -B .ufo/waves/round-71/c71_tmp.py --lane /fast/scratch/hyaku/kake-r74/ExecC1Rows/lane --revision ced2878a1e77f57afb4ee3baebf1021e5130399b
```

Base summary (exit 1):

```text
C2 revision=ced2878a1e77f57afb4ee3baebf1021e5130399b tokens_total=8 unannotated_tokens=0 unannotated_lines=[] removed=8 added=16 guard=fail met=False
```

Selftest command:

```sh
python3 -B .ufo/waves/round-71/c71_tmp.py --selftest
```

Tally: `no selftest mode`; exit 64.

Help command: `python3 -B .ufo/waves/round-71/c71_tmp.py --help`; exit 64. Both --help and --selftest print the module usage/docstring on stderr and exit 64; no selftest mode.

Exact environment, full stdout/stderr, argv and exit: `ExecC1Rows/c71_tmp-base.json` and `ExecC1Rows/c71_tmp-selftest.json`.

### c72_tmp_v2.py

- Path: `.ufo/waves/round-72/c72_tmp_v2.py`
- Contract: `.ufo/waves/round-72/contract.md §C2`
- Frozen predicate (original sentence; whitespace joined): C2 is met iff `c72_tmp_v2.py --selftest` exits 0 with `11/11`, `c71_tmp.py` exits 0 and `c72_tmp_v2.py` exits 1 on the J3 control commit that `.ufo/waves/round-72/controls/j3-control.sh` builds (a scratch clone of base tip `3c68645a` with line 27 replaced by a command-form `cp` line carrying the phrase; the commit hash differs per run and is printed by the script; the script is the frozen artifact), the counter exits 1 at the round-71 base `cc6b4e0b8c35e72dfb02c6184b847f68c1262153` (red-before), and exits 0 at the measured tip.
- Frozen amendments / terms: The full frozen predicate has four legs. This assignment ran selftest and round-74 base only, not the J3 script or round-71 red-before leg; no full round-72 claim is asserted.
- Kind: Reusable but bounded SKILL.md annotation gate v2 with a frozen round-71 guard baseline; full round-72 acceptance also needs J3 and red-before controls. Does not cover c73 routed holes.
- Verdict map: 0 met; 1 not met; 2 unevaluable; 64 usage
- Pinned inputs: Frozen baseline cc6b4e0b8c35e72dfb02c6184b847f68c1262153 SKILL.md; Measured SKILL.md; Full contract also pins .ufo/waves/round-72/controls/j3-control.sh, round-72 base 3c68645af27706d1d09b8dc7e27b0b0a9ffef6f1, c71_tmp.py for J3 comparison and S439
- Withdrawal / re-pin: Withdraw if any finding, guard failure, non-full selftest or failure of J3/red-before legs; newer fallback/command/symlink/phrase classes require v3 rather than overstating v2.

Entry / measured base command (cwd `/fast/scratch/hyaku/kake-r74/ExecC1Rows/lane`):

```sh
python3 -B .ufo/waves/round-72/c72_tmp_v2.py --lane /fast/scratch/hyaku/kake-r74/ExecC1Rows/lane --revision ced2878a1e77f57afb4ee3baebf1021e5130399b
```

Base summary (exit 0):

```text
C2v2 revision=ced2878a1e77f57afb4ee3baebf1021e5130399b brace_findings=0 command_findings=0 prose_findings=0 findings=[] removed=8 added=16 guard=ok met=True
```

Selftest command:

```sh
python3 -B .ufo/waves/round-72/c72_tmp_v2.py --selftest
```

Tally: `C2v2 selftest 11/11`; exit 0.

Exact environment, full stdout/stderr, argv and exit: `ExecC1Rows/c72_tmp_v2-base.json` and `ExecC1Rows/c72_tmp_v2-selftest.json`.

### c73_wave_pointers.py

- Path: `.ufo/waves/round-73/c73_wave_pointers.py`
- Contract: `.ufo/waves/round-73/contract.md §C1`
- Frozen predicate (original sentence; whitespace joined): C1 met iff `unannotated == 0` and `dead ≥ 2` (both dead tokens still named, annotated by a resolving correction) and the append-only conjunct holds (every base line of LOG.md and SCORECARD.md survives as a prefix line), at the measured tip.
- Frozen amendments / terms: Frozen round-73 baseline is mandatory, no CLI override; population is only round-72 wave-relative pointers in the specified LOG section and SCORECARD first-cell 72 rows.
- Kind: One-off round-72 wave-pointer correction instrument with frozen round-73 prefix baseline; not a general receipt-pointer gate.
- Verdict map: 0 met; 1 not met; 2 unevaluable; 64 usage
- Pinned inputs: Frozen baseline c1f3d8d4ed9470ecbaaf3353952a374b079e68cc LOG.md and SCORECARD.md; Measured LOG.md Round 72 section and SCORECARD first-cell 72 rows; Receipt tokens under .ufo/waves/round-72/; corrections in appended tails with resolving corrected paths
- Withdrawal / re-pin: Withdraw if any dead pointer unannotated, dead below 2 or either prefix guard fails; a different round/pointer population requires a new explicit contract.

Entry / measured base command (cwd `/fast/scratch/hyaku/kake-r74/ExecC1Rows/lane`):

```sh
python3 -B .ufo/waves/round-73/c73_wave_pointers.py --root /fast/scratch/hyaku/kake-r74/ExecC1Rows/lane --revision ced2878a1e77f57afb4ee3baebf1021e5130399b
```

Base summary (exit 0):

```text
C1v1 revision=ced2878a1e77f57afb4ee3baebf1021e5130399b pointers=9 dead=2 annotated=2 unannotated=0 append_only=true met=true
```

Selftest command:

```sh
python3 -B .ufo/waves/round-73/c73_wave_pointers.py --selftest --work /fast/scratch/hyaku/kake-r74/ExecC1Rows/work-6
```

Tally: `selftest 6/6`; exit 0.

Exact environment, full stdout/stderr, argv and exit: `ExecC1Rows/c73_wave_pointers-base.json` and `ExecC1Rows/c73_wave_pointers-selftest.json`.

## Retained evidence and limits

`ExecC1Rows/rows-evidence.json` embeds all seven rows, exact per-run environment/argv/stdout/stderr/exits, source hashes, full committed contracts and their git-show commands/exits, and frozen pairs bytes. Separate per-run JSON receipts and committed contract copies sit alongside it. Setup clone/check-out command exited 0. All retained contract extraction commands exited 0. No counter source was modified.

Only assigned invocations were run; the c72 J3/red-before legs and general harm battery were not run and are not claimed passed. Source reads used the detached base clone and git-show of named revisions; no LSP refactor was needed (read-only evidence task).

Self-evaluation: accuracy 4 (host-relative results remain host-bound); completeness 4 (full c72 acceptance beyond assignment unrun and explicitly named); clarity 4 (long predicates retained verbatim for fidelity); actionability 4 (registration must keep the historical/unevaluable distinctions); conciseness 4 (JSON intentionally duplicates receipts). Overall 4.0. Improvements: preserve these distinctions in any table integration; do not convert a nested sweep tally into a counter selftest claim. Self-check: evidence supports bounded findings, not full gate acceptance.

Cleanup: pending scratch removal; final status is recorded below and in rows-evidence.json.

Scratch cleanup completed with `shutil.rmtree(S)`; the assigned tree no longer exists. No cleanup defect.
