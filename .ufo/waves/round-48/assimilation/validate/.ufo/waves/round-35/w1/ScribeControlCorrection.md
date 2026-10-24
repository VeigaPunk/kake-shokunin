# ScribeControlCorrection — round 35, wave 1

Behavior: drafted the append-only correction of how the round-34 lookup control `dcef39b5`
works, for the three misdescription sites named by round-34 routed defect 2
(`corpus/lessons/round-34-verifier-spotcheck.md:222-230`). Draft only; nothing was appended to
the lane, and no product code, counter, judge, ref or commit was touched. Sealed keys under
`/fast/scratch/hyaku/kake-r35/sealed/` were not read, listed, stat'd, copied or grepped. No tool
installs or updates. No blocker, so the L1 was not messaged.

## Built

- `/fast/scratch/hyaku/kake-r35/w1/ScribeControlCorrection/correction.md` — one paragraph per
  site (`corpus/lessons/round-34.md:68`, `.ufo/waves/round-34/criteria/lookup_control_check.py:4-7`,
  `SCORECARD.md:1254-1256`), each quoting the old text verbatim with append-only replacement
  wording, the control's own lines with line numbers, and what defeats it.
- `/fast/scratch/hyaku/kake-r35/w1/ScribeControlCorrection/probe/probe_variants.py` plus
  `probe/c1_matrix_count.py` (copy of the frozen round-34 counter, matrix digest unchanged) and
  `probe/{unchanged,renamed,commented}.{json,err}` — sandbox-only measurement.

## Commands and observed results

| # | command | exit | observed |
|---|---|---|---|
| 1 | `git -C clone fetch <r34-c1-lookup bundle> 'refs/heads/*:refs/heads/r34/*'` | 0 | `dcef39b5f4e8373970eb74858d2c6175524cdfd0`; `git show --stat` 18 insertions; parent `a2fe31b2d1d2b…`; blob `scripts/link_preview_audit.py` sha256 `a2e274c0ce9168bb10d7217a8c9a09c2516aea1c2c148dbf583306dcc56730ec` |
| 2 | `git show dcef39b5:scripts/link_preview_audit.py \| sed -n '3,13p'` (also `'9,15p'`, `'5,15p'`) | 0 | outputs pasted in `correction.md`; a re-diff of the three pasted blocks against the command output reports `match` for each (python one-liner, exit 0) |
| 3 | `TMPDIR=$PWD/tmp python3 -B probe/probe_variants.py unchanged "$PWD/clone" dcef39b5` | 0 | `C1 28/28`; byKind control 6/6, defect 13/13, input 7/7, usage 2/2 |
| 4 | same with `renamed` (case under `base / uuid4().hex`) | 0 | `C1 28/28`; same byKind |
| 5 | same with `commented` (`<!-- closure perturbation -->` appended to each `.html`) | 1 | `C1 7/28`; control 6/6, defect 0/13, input 1/7, usage 0/2 |

## Findings

- The control reads no directory name. Lines 5–8 of the blob walk the cwd and keep every relative
  path and file content; lines 9–13 sha256 `json.dumps(argv)` then each sorted relative path, a
  NUL, the content and a NUL; line 14 substitutes the literal `"default"` for argv on the
  counter's manifest invocation (`--manifest` plus an absolute `.../manifest.json`); line 15
  falls back to `key(argv)` and then to `[0, "clean", []]`.
- Renaming each case's parent directory is a no-op for the key and leaves 28/28 (measured above);
  a one-comment HTML change defeats it at 7/28, the seven survivors being clean cases the
  fallback satisfies without a table hit. This matches the round-34 closure's 7/28
  (`corpus/lessons/round-34-verifier-spotcheck.md:81-84`) and is consistent with the frozen
  round-35 counter's pre-scored 7 for this control.
- The lesson site needs the append to cover `:130-131` as well: "case identity leaks through the
  case directory name" repeats the same wrong mechanism; the correction paragraph says so.

## Not verified / out of scope

- The append itself was not applied (draft only; lane text untouched).
- No round-35 sealed counter run; no sealed key content was needed. Only the 28 frozen round-34
  cases were exercised; a single-file content change and non-manifest argv variants were not
  measured separately.
- The probe's `commented` mode perturbs every page, same as the closure; it does not establish
  which single file would suffice for every case.

## Artifact paths

- `/fast/scratch/hyaku/kake-r35/w1/ScribeControlCorrection/correction.md`
- `/fast/scratch/hyaku/kake-r35/w1/ScribeControlCorrection/probe/probe_variants.py`
- `/fast/scratch/hyaku/kake-r35/w1/ScribeControlCorrection/probe/{unchanged,renamed,commented}.json`
- `/fast/scratch/hyaku/kake-r35/w1/ScribeControlCorrection/clone` (sandbox clone, lane rev 318561e + r34 refs)
