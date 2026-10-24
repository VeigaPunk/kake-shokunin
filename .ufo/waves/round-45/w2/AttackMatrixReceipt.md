# AttackMatrixReceipt — matrix printed line vs JSON receipt, and the C1 arithmetic correction

Seat `kake-r45.AttackMatrixReceipt` (leaf, no subagent dispatch). Lane `kake-shokunin`,
round-45 wave 2, axis **operability** (receipt↔claim fidelity of the C1 counting
command). Scratch: `/fast/scratch/hyaku/kake-r45/AttackMatrixReceipt/`. No lane file
was edited; no commit, no push; every run outside the lane ran on scratch copies.

Targets:
- `.ufo/waves/round-45/verification/matrix/before.json`, `after.json`, `run-log.txt`
- `.ufo/waves/round-45/c45_matrix.py` (counting command), `.ufo/waves/round-45/c45_audit.py` (driver v2)
- `SCORECARD.md:3712-3745` (the round-45 measured append) against those receipts
- the frozen "9 rejected rows" arithmetic (correction must be recorded, not silently fixed)

## Verdicts against the named attacks

| # | Named attack | Verdict | Decisive point |
|---|---|---|---|
| 1 | Receipt carries every field the append cites, with the cited values | **PASS** | Both JSONs recompute from their cited cohort files; printed line equals the JSON |
| 2 | Per-fixture cohort paths exist and resolve to the cited summaries | **PASS** | All 8 paths exist; no cited file is newer than the receipt that cites it |
| 3 | `driver_sha256` matches the committed driver bytes | **PASS at HEAD / FAIL against the live tree** | `after.json` pins `f3c3171b…` = `HEAD:c45_audit.py`; the worktree driver is now `64bc3324…` (uncommitted, twice rewritten mid-wave) — F1 |
| 4 | `named_classes` is 3 distinct classes for after and empty for before | **PASS** | `["counter_error","stale_receipt","tool_absent"]`; before `[]` |
| 5 | The after gate certifies "each rejection named with its defect class" | **FAIL (gate weaker than the claim)** | The gate is a union over legs: a class *permutation* across legs still prints `MATRIX_AFTER_PASS` — F2 |
| 6 | The before PASS line protects the cited non-degeneracy evidence | **FAIL (gate blind to the honest leg)** | `MATRIX_BEFORE_PASS`, exit 0 with `honest_witnessed=0 honest_build_met=0` — F3 |
| 7 | The "9 rejected rows" arithmetic was corrected, not silently fixed | **PASS with a NOTE** | Frozen text still says 9 (unedited); correction recorded in three wave-1 reports + the landing draft; the append quotes no row count and the draft's mandated measured count is absent — F4 |
| 8 | The frozen counting command re-derives both receipts from committed bytes | **PASS** | Scratch copy with pinned driver bytes + `.git`: both stages reproduce every cited figure (below, 543 s) |

## Evidence

### 1. Receipt fields recompute from the cited cohorts (PASS)

```
$ python3 - <<'EOF'   # regex = c45_matrix.py:42; recompute from the receipt's own cohort files
... recompute invalid_accepted / rejections_named / honest_* from summary.json files ...
EOF
before recomputed invalid_accepted= 3 rejections_named= 0 honest_witnessed= 27 honest_build_met= 3
  legs: [('counter-error','counter-error',True,[],1), ('tool-absent','tool-absent',True,[],1), ('stale-planted','stale-planted',True,[],1)]
  receipt: 3 0 27 3
  cited files newer than receipt: []
after recomputed invalid_accepted= 0 rejections_named= 3 honest_witnessed= 27 honest_build_met= 3
  legs: [('counter-error','counter-error',False,['counter_error'],1), ('tool-absent','tool-absent',False,['tool_absent'],1), ('stale-planted','stale-backdate',False,['stale_receipt'],1)]
  receipt: 0 3 27 3
  cited files newer than receipt: []
```

Printed line vs JSON (committed `run-log.txt` vs the receipts):

```
$ cat .ufo/waves/round-45/verification/matrix/run-log.txt
stage=before invalid_accepted=3 rejections_named=0 honest_witnessed=27 honest_build_met=3
MATRIX_BEFORE_PASS
BEFORE_EXIT=0
stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3
MATRIX_AFTER_PASS
AFTER_EXIT=0
```

`before.json` = `{invalid_accepted:3, rejections_named:0, named_classes:[], honest_witnessed:27,
honest_build_met:3}`; `after.json` = `{invalid_accepted:0, rejections_named:3,
named_classes:["counter_error","stale_receipt","tool_absent"], honest_witnessed:27,
honest_build_met:3}` — identical to the printed line. All eight per-fixture/honest cohort
paths and summary paths resolve; every cohort mtime precedes its receipt
(`before.json` 2026-10-24T00:46:21.776, `after.json` 00:49:56.057; fixture cohorts
00:42:59 and 00:46:21–00:46:22; honest cohorts 00:46:21.763 / 00:49:56.047).
`honest.summary` of after is byte-identical to `verification/honest-regression/after-v5-v2.json`
(`cmp` → IDENTICAL), and that summary carries `ok=True, witnessed=27, controls=27,
counterSha256=5cedaa3b…(= sha256 of frozen c44_count_v5.py), errors=[], build met 3/3` —
the append's "identity validation" sentence is backed.

The stale leg's class is genuinely the mtime branch, not an exit or sha artefact:
`tools/ctl1.json` carries `counterSha256` equal to `sha256(fixtures/stale-backdate/fake_counter.py)`,
`note=None`, `seed=424242`, counter exit 0, and its mtime is 4.985 s **before** the cohort
manifest's `started_ns` (`window would accept: False`). The append's "valid exit 0 via the
committed fixtures/stale-backdate fake" is accurate.

Driver pins: `sha256sum .ufo/waves/round-44/c44_audit.py` =
`8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75` = `before.json.driver_sha256`;
`git show HEAD:.ufo/waves/round-45/c45_audit.py | sha256sum` =
`f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076` = `after.json.driver_sha256`.

### F1 (HIGH, operability) — the measured driver is being mutated in the worktree mid-wave

At review time, while `after.json` still pins `f3c3171b…`:

```
$ sha256sum .ufo/waves/round-45/c45_audit.py
64bc33248c9ba2088f5447d7c3064cb2aea3f2dce9e2ba4ec4dd514a6a07841e  .ufo/waves/round-45/c45_audit.py
$ git show HEAD:.ufo/waves/round-45/c45_audit.py | sha256sum
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  -
$ stat -c '%y %s' .ufo/waves/round-45/c45_audit.py
2026-10-24 01:02:22.147170508 -0300 22854
$ git diff --stat -- .ufo/waves/round-45/c45_audit.py
 .ufo/waves/round-45/c45_audit.py | 53 ++++++++++++++++++++++++++++++++++++----
 1 file changed, 48 insertions(+), 5 deletions(-)
```

Two uncommitted rewrites were observed inside this seat's window: `b61447e6…` (21904 B,
mtime 00:59:29 — `AttackKnowledgeEntry.md:11-13` independently records the same drift) and
then `64bc3324…` (22854 B, mtime 01:02:22). The second is not test-only: it changes
`receipt_validity()`'s signature and semantics (adds a `toolSha256` binding that can return
`stale_receipt` for a substituted control receipt) plus selftest fixtures. Snapshot kept at
`/fast/scratch/hyaku/kake-r45/AttackMatrixReceipt/driver-drift-64bc3324.py`.

Consequences:
- The literal attack "`driver_sha256` matches the committed driver bytes" passes at `HEAD`
  (`e545525`), because `after.json` was written at 00:49:56 from those bytes.
- It fails against the live lane: the shipped instrument no longer hashes to the value the
  append publishes, and the change alters gate behaviour after measurement. Re-running the
  frozen command `python3 -B .ufo/waves/round-45/c45_matrix.py --stage after` today writes
  `driver_sha256=64bc3324…` (the field is a pure function of the file, `c45_matrix.py:163`)
  and exercises a different gate, so the published receipt can no longer be re-derived in
  place.
- Wave-2 bounds: every seat is read-only over the lane except its report; no w2 write grant
  names `c45_audit.py` (`grep -n c45_audit .ufo/waves/round-45/make_w2_spec.py` → none; the
  registry carries no write paths). Author unattributed; the diff matches the m10 build-gate
  kill-test in `w2/MutV2GateFinal.md` and the tool-sha binding is a substitution fix, i.e.
  sibling-authored repairs landing in the tree, not in scratch.

If the L1 commits this drift, `SCORECARD.md:3713-3714` ("driver v2 sha256 `f3c3171b…`") and
`after.json.driver_sha256` become stale in one commit, with no new receipt to supersede them.
Either revert the worktree file or land it with a fresh `--stage after` receipt and an append
line naming both the old and new hash.

### F2 (MEDIUM) — `MATRIX_AFTER_PASS` is permutation-blind

`c45_matrix.py:154-158` builds `named` as the **union** of per-leg class sets, and
`:174-179` gates on `len(named) == 3`. The per-leg expected mapping built by
`stage_fixtures()` (`counter-error→counter_error`, `tool-absent→tool_absent`,
`stale-*→stale_receipt`) is never used for gating. A driver that swaps two class labels
still passes. Demonstrated on a scratch copy (class strings swapped in `receipt_validity`
only; the exit gate now returns `tool_absent`, the note gate `counter_error`):

```
$ python3 - <<'EOF'    # imports the frozen c45_matrix, calls run_fixture_leg with the swapped driver
...
EOF
leg classes: {'counter-error': ['tool_absent'], 'tool-absent': ['counter_error'], 'stale-planted': ['stale_receipt']}
invalid_accepted=0 rejections_named=3 named_classes=['counter_error', 'stale_receipt', 'tool_absent']
GATE_PASS
```

The honest clause (`honest_witnessed==27 and honest_build_met==3`) was not re-run for the
swapped driver; the honest receipts are unaffected by the label swap (their rows have no
error), so on source the full gate would also pass — stated as source-derived, not observed.
Effect on the claim: the append's "each rejection named with its defect class" is true of the
recorded receipt (verified per leg above) but is **not** what the PASS line certifies. The
frozen counting command cannot distinguish correct naming from a permutation. No dishonesty
in the landed numbers; the gate is weaker than the prose it is cited to support.

### F3 (MEDIUM) — `MATRIX_BEFORE_PASS` is blind to the honest leg

`c45_matrix.py:174-175`: `passed = invalid_accepted == 3`. The before stage runs the honest
leg and records it, but the exit code ignores it. Observed in a scratch copy of the lane
(`/fast/scratch/hyaku/kake-r45/AttackMatrixReceipt/lane`, driver/counter bytes identical;
`.git` initially absent, which the frozen counter v5 needs — it resolves
`git -C <root> show 1ef7a0e9…:scripts/sitemap_audit.py`):

```
stage=before invalid_accepted=3 rejections_named=0 honest_witnessed=0 honest_build_met=0
MATRIX_BEFORE_PASS
BEFORE_RC=0
```
with `before.json.honest.problems = ["ok is not True","witnessed != 27","build not 3/3 met"]`
(terminal output captured before the later with-`.git` rerun overwrote that scratch
`before.json`; the quoted output is the verbatim run result, not a re-read of the overwritten file).

So a degenerate before receipt (`honest_witnessed=0`) still prints `MATRIX_BEFORE_PASS`, exit 0.
The append cites "honest 27/27 + build 3/3 also certified, proving the before receipts are not
degenerate" as evidence; that figure is real in the committed receipt but is not gate-enforced.
The after stage does enforce it (`:176-178`). The asymmetry means the frozen counting command,
run in an environment without `.git` (tarball/CI copy), reports the non-degeneracy evidence as
0/0 while still exiting 0. The frozen declaration's MET condition does not require the before
honest figure, so the claim as declared is unharmed; the evidence sentence is not protected.

### F4 (LOW/NOTE) — the 9-vs-12 correction is recorded, and the frozen text is intact

The frozen text still says 9, so nothing was silently rewritten:

```
$ grep -rn "9 rejected rows" --include=*.py --include=*.json --include=*.md .
./.ufo/waves/round-45/make_w1_spec.py:277: "error classes among the 9 rejected rows: 3 fixture classes x control+3 builds), then run the "
./.ufo/waves/round-45/w1-plan.json:432 (same text; committed at 7ed9378)
./.ufo/waves/round-45/w1-spec.json:116, .ufo/waves/round-45/w1-taskcall.json:427 (same text)
```

`git status --porcelain .ufo/waves/round-45/make_w1_spec.py .ufo/waves/round-45/w1-plan.json
SCORECARD.md` → clean; `git log -S '9 rejected' -- .ufo/waves/round-45/make_w1_spec.py`
returns only `7ed9378` (its introduction). The correction (3 × (control + 3 builds) = 12, and
the landed semantic is *distinct named classes*, not rows) is recorded in four wave-1
artifacts:

- `.ufo/waves/round-45/w1/ExecMatrixRunner.md:31` — "Contract arithmetic is inconsistent:
  '9 rejected rows' conflicts with '3 fixture classes × control + 3 builds' (12 rows)…"
- `.ufo/waves/round-45/w1/ScribeDeclarations.md:337` (item 8)
- `.ufo/waves/round-45/w1/ReviewWave1Plan.md:175` (item 13 flagged)
- `.ufo/waves/round-45/drafts/scorecard-measurement.md:267-271` (item 8, with the landing
  instruction to quote the measured `{{C1_REJECTED_ROW_COUNT}}` "rather than the frozen '9'")

The landed append neither repeats 9 nor publishes any row count: `grep -c
C1_REJECTED_ROW_COUNT SCORECARD.md` → `0`, and the C1 measured block (`SCORECARD.md:3718-3745`)
contains no rejected-row figure. So the falsity was never landed (nothing was silently fixed),
and the correction lives in committed wave-1 reports; but the landing checklist's mandated
measured row count is absent from the append. That is a bookkeeping gap in the append, not a
false statement. The append's own figure gate is clean:
`python3 -B scripts/ledger_latest_check.py --root .` → `ledger-quotes: 3 figures, 0 mismatches`,
exit 0.

## Re-derivation (rerun of the frozen counting command) — PASS

Scratch lane copy `/fast/scratch/hyaku/kake-r45/AttackMatrixReceipt/lane` carries the
receipt-pinned bytes (`c45_audit.py` = `f3c3171b…`, `c44_audit.py` = `8ee2c8bf…`, verified
after the copy; taken before the 00:59 worktree drift) and the lane's `.git` (so counter v5's
`git -C <root> show 1ef7a0e9…:scripts/sitemap_audit.py` base-revision lookup works). Ran both
stages of the frozen command in that copy (543 s wall):

```
$ cd /fast/scratch/hyaku/kake-r45/AttackMatrixReceipt/lane
$ python3 -B .ufo/waves/round-45/c45_matrix.py --stage after
stage=after invalid_accepted=0 rejections_named=3 honest_witnessed=27 honest_build_met=3
MATRIX_AFTER_PASS
AFTER_RC=0
$ python3 -B .ufo/waves/round-45/c45_matrix.py --stage before
stage=before invalid_accepted=3 rejections_named=0 honest_witnessed=27 honest_build_met=3
MATRIX_BEFORE_PASS
BEFORE_RC=0
$ # receipts written by this run:
before driver_sha 8ee2c8bf93332069 invalid 3 named 0 [] honest 27 3 valid True problems []
after  driver_sha f3c3171b658abccd invalid 0 named 3 ['counter_error','stale_receipt','tool_absent'] honest 27 3 valid True problems []
```

Both attested figures re-derive exactly from committed bytes at their recorded inputs
(cohorts differ only by fresh uuid/nonce/seed, as the runner documents). Stderr was empty on
both stages. This is the positive half of the attack: the receipts are reproducible in a copy
that has the committed bytes and `.git`. The contrast with F3's no-`.git` run is the point:
same command, same fixture bytes, honest leg silently 0/0 while `MATRIX_BEFORE_PASS` still
prints and exits 0.

## Residual risk

- F1 is the largest: the receipt is honest about the bytes it measured, but the instrument it
  names is drifting in the tree during the wave. Until the tree is reverted or re-measured, the
  published pin and the shipped driver disagree.
- F2/F3 do not falsify the landed numbers (both receipts' legs were verified individually);
  they falsify the *strength of the gate* the append leans on. Any future run of the frozen
  command inherits them.
- The counting command is not read-only: `--stage after` overwrites `matrix/after.json` and
  copies the fresh honest summary over the committed
  `verification/honest-regression/after-v5-v2.json` (`c45_matrix.py:138-140,169-170`). Re-running
  it to "re-derive" destroys the committed receipt it reproduces; there is no `--out`/dry-run
  path. A re-derivation should be done on a copy (as here), and the append's "rerun the counting
  command" instruction should say so.
- Unrun audits: I did not audit the v2 driver's own semantics beyond the receipt path, and did
  not verify the freshly drifted worktree driver's behaviour (out of scope; siblings hold that).

## Files written

- `.ufo/waves/round-45/w2/AttackMatrixReceipt.md` (this report)
- scratch only: `/fast/scratch/hyaku/kake-r45/AttackMatrixReceipt/{lane/,swap/swapped.py,driver-drift-64bc3324.py,before.stdout,before.stderr,after.stdout,after.stderr,before2.stdout,before2.stderr}`

Tool installs/updates: none.
