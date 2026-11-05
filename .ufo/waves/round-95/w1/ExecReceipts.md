# ExecReceipts — round-95 receipt debt (R94-8 erratum + landed-tip receipt plan)

Seat: ExecReceipts (kake round 95, hyaku run 15, attempt 1, wave w1). Date:
2026-11-05. Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE). Lane
HEAD at report time: `d9be693fdb61dd080ae8cf6c007871d3a118c1d2` (amendment A
pre-scoring; the round freeze `8f638b591e739e1863f5fa22334d5e15178189ed` is its
ancestor — `git merge-base --is-ancestor` rc 0). Round base
`fdd5fdbeb8a2ba6c18f0f23135d1bee98068dca3`; instruments commit
`43cdd9fc899a2613d8ba7b55edf820825e57b4d1`. A copy of this report sits at
`.ufo/waves/round-95/w1/ExecReceipts/ExecReceipts.md`; receipts live flat in
that directory.

Axes (godspeed): (a) evidentiary precision — every claim in the erratum carries
the command and observed rc that measured it; (b) instrument fidelity — the
script reproduces the frozen counting commands byte-for-byte and
digest-self-identifies its receipts; (c) bounds compliance — writes confined to
`.ufo/waves/round-95/w1/ExecReceipts{,.md}` plus scratch, which is removed
before yield.

## Deliverable 1 — erratum-r94-8.md (ready)

Full text: `.ufo/waves/round-95/w1/ExecReceipts/erratum-r94-8.md`. Measured
core, each with its command and rc:

| Claim | Command | Observed |
|---|---|---|
| `191dd0ed…` absent from lane | `git cat-file -t 191dd0ed0cf594a29668f5862f536a925998cadd` | `fatal: git cat-file: could not get object info`, rc 128 |
| `base_rev` line location | read of committed bytes | `.ufo/waves/round-93/w1/recovered-partial/MutConditional/posgood-out/mutants.json:7` = `"base_rev": "191dd0ed0cf594a29668f5862f536a925998cadd",` |
| `mutants-posgood.json` has no `base_rev` | read of committed blob `f15c99f42ef250baaa21f2e3114b3b634de2734e` at `fdd5fdbe` | it pins base by content: `base.source = .ufo/waves/round-93/frozen/pos-good.py`, `base.sha256 = 0fe018a8e33ca82928a876f2b0d2e5b3f33befa00260f2fdf995418822a868e4` |
| pos-good bytes verified | `git show fdd5fdbe:.ufo/waves/round-93/frozen/pos-good.py \| sha256sum` | `0fe018a8e33ca82928a876f2b0d2e5b3f33befa00260f2fdf995418822a868e4` (blob `e78f28457fb6209bcdbac99aed0bfa56a289a4e4`, mode 100755) — exact match to the population's pin |
| other citers | `git grep -n 191dd0ed fdd5fdbe` and `… 8f638b59` (rc 0) | round-93: only the pointer file itself; round-94: `w1-results.json:52`, `w1/CriticClaims.md:39,83,168,174,187,208`, `w1/CriticClaims/git-and-digests.out:3-4`, plus `SCORECARD.md:5722` and `corpus/lessons/round-94.md:94`; at HEAD also `round-95/freeze.md:110` and `round-95/c95_conditional.py:37` (by-design disclosures) |

Digest correction to the seat brief's guess: `f15c99f4…` is the git blob of
`mutants-posgood.json` itself, not of `pos-good.py`; the erratum records the
full digests of both. The two-sentence correction text the round lesson will
carry is in the erratum; it marks `191dd0ed` **unrecoverable-from-this-lane**
and grounds the round-93 readings in the committed patch list plus the
content-pinned pos-good bytes. No lane file was modified.

## Deliverable 2 — run-final-receipts.sh + dry-run receipts

Script: `.ufo/waves/round-95/w1/ExecReceipts/run-final-receipts.sh`
(`bash -n` clean; exercised end-to-end).

- Usage: `run-final-receipts.sh <REVISION> [LANE_ROOT]`; `set -euo pipefail`.
- Resolves `$1` via `git rev-parse --verify "$REVISION^{commit}"` and echoes
  the full sha as line 1 (`revision <full-sha>`) of both receipts.
- Runs the frozen counting commands verbatim (cwd=LANE, `--root .`, `-B`,
  `--revision <full-sha>`, `--work` under
  `/fast/scratch/hyaku/kake-r95/ExecReceipts/final-<sha12>-$$`), C1 then C2.
- Writes `<LANE>/.ufo/waves/round-95/controls/after-c1-final.txt` and
  `after-c2-final.txt`: revision line, then the counter's stdout.
  `RECEIPTS_OUT_DIR` overrides the output dir so a dry run can target scratch.
- Counter exit codes go to stderr (`c1_rc=`, `c2_rc=`); `met=false` exits 1 by
  design and is a receipt, not a script failure. The script exits 0 iff both
  receipt files exist and are non-empty.
- Digest check against `controls/instrument-sha256.txt` runs before counting
  and reports on stderr; a mismatch is reported, never repaired.
- Scratch-clean: one `trap rm -rf` removes the work dirs on exit (verified —
  only the dry-run outputs remained after the run).

Dry-run against the freeze commit `8f638b591e739e1863f5fa22334d5e15178189ed`
(outputs to scratch; 87.55 s wall):

- Script rc: **0**. Counter rcs: `c1_rc=1`, `c2_rc=1` (both `met=false` by
  design at a no-repair revision — receipts, not failures).
- `dryrun-c1.txt` line 2: `C1v95 revision=8f638b59… counter=04be4a7d… lessons=89
  entries=82 rows=255 criteria=39 mismatches=18 E1=0 E2=0 E3=3 E4=0 E5=15
  pins=ok battery=20/20 admit=5/5 shadow=absent predecessor_admits=10/19
  floor=4 self_pin=ok met=false` — the same counts as the committed base
  control (`controls/base-c1.txt` at `fdd5fdbe`), confirming the by-design red
  persists at the freeze tip where SKILL.md is byte-identical.
- `dryrun-c2.txt` line 2: `C2v95 revision=8f638b59… candidate=present
  hand=57/66 generated=79/120 forgeries_refused=7/7 positive=admitted
  mutants=40/40 survivors=none anti_table=ok population=ok seed=95 met=false` —
  identical to `controls/base-c2.txt` (which measured `43cdd9fc`), and
  `population=ok` over the freeze tree: the digest pins (population, mutants,
  receipts) resolve at the freeze commit.
- Both receipts committed to the seat dir as `dryrun-c1.txt` / `dryrun-c2.txt`.

At the round's landed tip the L1 runs:
`bash .ufo/waves/round-95/w1/ExecReceipts/run-final-receipts.sh <landed-tip-sha>`
(no `RECEIPTS_OUT_DIR` — receipts land in `controls/`), then integrates the two
files.

## Finding — instrument lineage across freeze → amendment A (L1-owned, not repaired)

The seat brief quoted the pin `c95_selfassess.py sha256 8fd27d62…`; measurement
shows that digest belongs to the **freeze commit** `8f638b59` (verified:
`git show 8f638b59:.ufo/waves/round-95/c95_selfassess.py | sha256sum` →
`8fd27d62…`; identical at instruments commit `43cdd9fc`). HEAD `d9be693f`
("round-95: amendment A pre-scoring — entry identity pins to presence,
regenerated C1 receipts", 2026-11-05T13:36:06-03:00) carries amended counter
bytes `04be4a7dc32adee08e386936e2af8257a191421bd2005c97b40af49933a24a32`
(diff vs freeze: 1 file, +6/−12) and the pin file was regenerated with it
(`c95_selfassess.py` → `04be4a7d…`, `frozen/c1-surfaces.json`
`00a04c9a…` → `9eff04c5…`); `c95_conditional.py` is unchanged (`f09f8409…`,
pin-exact). Working tree is clean against HEAD for all four live files
(`git status --porcelain` empty). The dry-run receipts self-identify via
`counter=04be4a7d…`, and the script's stderr digest check reads `ok` against
the current pin file. Recorded so the L1 can confirm amendment A is the
intended pre-scoring state; nothing was patched, and a receipt consumer can
always see which bytes counted.

## Bounds, tools, hygiene

- Writes: `.ufo/waves/round-95/w1/ExecReceipts/` (5 flat files:
  `erratum-r94-8.md`, `run-final-receipts.sh`, `dryrun-c1.txt`,
  `dryrun-c2.txt`, this report's copy) and the report file
  `.ufo/waves/round-95/w1/ExecReceipts.md` (the Report trailer path, LANE-
  relative). Nothing else in the lane; no `.ufo/state`; no MANIFEST; no git/jj
  mutations (read-only git only); fixtures none; no credentials touched.
- Scratch: `/fast/scratch/hyaku/kake-r95/ExecReceipts/` — **removed before
  yield** (verified absent); receipts copied out first.
- Tools installed: none. Sysctls: none touched, none needed.
- No subagent dispatched.

## Verdict

`RECEIPTS erratum=ready script-dryrun=rc=0`

Checks the L1 should run after integration: (1) re-run the script at the landed
tip with no `RECEIPTS_OUT_DIR` and confirm both `controls/after-*-final.txt`
files land with the tip sha on line 1; (2) `bash -n` the script; (3) confirm
the erratum's two-sentence correction text lands in
`corpus/lessons/round-95.md`; (4) confirm the amendment-A pin lineage above is
the intended pre-scoring state.
