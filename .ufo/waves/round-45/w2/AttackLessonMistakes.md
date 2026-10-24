# AttackLessonMistakes — round-45 wave 2, lesson entries 14–15

Seat: `kake-r45.AttackLessonMistakes`. Lane axes: **operability** (does entry 14's
fix description match the landed driver bytes) and **freshness** (does entry 15's
receipt identity and red state re-derive from committed bytes). Read-only over the
lane except this file; every re-run used a copy/output path under
`/fast/scratch/hyaku/kake-r45/AttackLessonMistakes/`. No pacman/uv/npm installs.

## Named attack and verdict

**Attack:** entries 14–15 of `corpus/lessons/round-45.md` must each carry class,
evidence pointer, captured-by, fix, and an able-to-fail demonstration that now
exists; entry 14's fix must match the landed v2 bytes (function names binding, line
refs allowed to drift); entry 15's red state (the two receipts) must be real.

**Verdict: PASS on the core, one LOW calibration finding.**
- Entry 14 fix ↔ v2 bytes: **PASS**. All four named functions exist at exactly the
  cited lines; every behavior in the fix sentence is present in the bytes; the
  shipped `--selftest` passes.
- Entry 15 red state: **PASS**. Both receipts are committed and re-derive exactly as
  stated (sha256, witnessed count, `ok`, split); the frozen `22/1/4` tuple is red on
  the named receipt and green on the earlier one.
- Able-to-fail demonstrations: **PASS**. Matrix values re-derive; independently
  reproduced the 3/3-accepted → 0/3-accepted transition on scratch copies, with the
  stale class refused by the mtime branch at exit 0.
- Finding LOW-1: entry 14's *captured-by* fuses two distinct frozen texts into one
  quote attributed to round-44 kill rule (2); the quoted sentence is not that rule's
  text. The field still exists and the class analysis is verifiable from the correct
  sources, so this is calibration, not a claim-breaking defect.

## Entry 14 — fix description vs landed v2 bytes

Commands:

```
sha256sum .ufo/waves/round-45/c45_audit.py .ufo/waves/round-44/c44_audit.py
grep -n '^def ' .ufo/waves/round-45/c45_audit.py
sed -n '68,87p' .ufo/waves/round-45/c45_audit.py
sed -n '284,449p' .ufo/waves/round-45/c45_audit.py
python3 -B .ufo/waves/round-45/c45_audit.py --selftest
```

Decisive output:

```
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  .ufo/waves/round-45/c45_audit.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py

68:def receipt_validity(receipt, exit_code, mtime_bounds, counter_sha):
90:def semantic_witness(row, class_keys):
98:def build_control_row(base, tool_sha, code, rec, mtime_ns, started_ns, finish_ns,
122:def build_build_row(i, code, rec, mtime_ns, started_ns, finish_ns, counter_sha,
135:def row_valid(row):
147:def build_met(build, build_runs):
153:def expectation_ok(expect, results, build, expected_rows, class_keys, build_runs=0):
170:def selftest():
223:def _selftest_cohort():
308:def main():

SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
```

(`grep` also reports a literal `def main():` at line 244; an AST pass shows 17
top-level defs, **no duplicates** — line 244 is the embedded fake-counter source
inside the `_selftest_cohort` triple-quoted string. Not a defect.)

Each fix clause checked against bytes:
- `receipt_validity` at `:68-86` (last line `return True, None`); exit ∉ {0,1} →
  `counter_error`; `note == "tool absent"` → `tool_absent`; `counterSha256 !=
  sha256(invoked counter)` → `stale_receipt`; missing/None `seed` → `stale_receipt`;
  `st_mtime_ns` outside `[started_ns - 1 s, finish_ns + 1 s]` → `stale_receipt`.
- both row paths call the gate: `score()` → `build_control_row` (`:98`), `score_build`
  → `build_build_row` (`:122`); no launched counter bypasses it.
- invalid rows: `semantic_witness` returns False when `row["error"]` is set;
  `not_met_rows` filters `row_valid`; `expectation_ok` returns False if any row is
  invalid.
- build count pinned: `build_met(build, build_runs)` requires `len(build) ==
  build_runs`; `expectation_ok` re-checks.
- cohort dir self-created and refused non-empty (`main`: `makedirs` + `listdir`);
  `run-manifest.json` written with mode `"x"` before any `run_counter` spawn.

## Entry 15 — red state of the two receipts

Commands (the lesson's jq filter, and a strict tuple predicate):

```
sha256sum .ufo/waves/round-44/verification/claim/after-final/after-v5.json \
          .ufo/waves/round-44/verification/claim/after-v5.json
jq -r '{ok, witnessed, rows:(.rows|length)}' <receipt>
jq -r '.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length, mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length, met: map(select(.met==true))|length}' <receipt>
jq -e '.rows | (…class_only==22) and (…mixed==1) and (…met==4)' <receipt>
```

Decisive output:

```
9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1  …/claim/after-final/after-v5.json
{"ok": true, "witnessed": 27, "rows": 27}
{"class_only": 26, "mixed": 1, "met": 0}

2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902  …/claim/after-v5.json
{"ok": false, "witnessed": 23, "rows": 27}
{"class_only": 22, "mixed": 1, "met": 4}

frozen 22/1/4 on named   → jq -e exit 1   (red)
frozen 22/1/4 on earlier → jq -e exit 0   (green)
measured 26/1/0 on named → jq -e exit 0   (green)
```

"Only from the earlier 23-witness receipt": across all 17 row-bearing receipts under
`.ufo/waves/round-44/verification/claim/` (recursive), `after-v5.json` is the only
one giving 22/1/4; the wave-2 baselines give 21/2/4 and 23/0/4. The four `met` rows
in the earlier receipt are exactly `casememo-v3/v4/v7/v8`; in the named receipt the
same four are `met=false`, `classCaught=["G6"]`, `legacyCaught=[]` — the
"pre-G6-fix casememo rows" parenthetical is accurate.

Frozen leg and disposition: `SCORECARD.md:3681-3701` states the quoted sentence and
`Claim MET iff after=(4/4, false, 22/1/4)`; `SCORECARD.md:3759-3765` records leg (c)
**FALSIFIED as declared** with the full sha256 of the named receipt, and the appendix
header (`:3716`) says "the declarations above are not edited". Entry 15's
"reported falsified-as-declared in SCORECARD.md, not amended" is real.

Fix re-derivation (committed `c45_freshness.py`, output redirected to scratch):

```
selftest_kills before=2/4 after=4/4
v4_predicate_names_class_runs before=true after=false
witness_split class_only=26 mixed=1 met=0
FRESHNESS_RAN_OK
freshness main() rc = 0
```

## Able-to-fail demonstration (entry 14)

Committed matrix receipts were read and the fixture legs re-run independently on
scratch copies (same argv as `c45_matrix.py`, `--root`/`--controls`/`--counter`
pointed at the committed fixtures, `--build-rev 020bc457 --build-runs 3 --workers 1`;
stale-planted leg pre-planted `tools/` and `build-{1,2,3}.json` exactly as the
runner does):

```
before counter-error driver_exit 0 ok True  errors []
   rows: [('ctl1', 2, None, ['G5','G7'])]
before tool-absent  driver_exit 0 ok True  errors []
   rows: [('ctl1', 1, None, ['A',…,'T5'])]
before stale-planted driver_exit 0 ok True errors []
   rows: [('ctl1', -9, None, ['G2','G4','G9'])]
after  counter-error driver_exit 1 ok False errors ['build#1:stale_receipt',…,'ctl1:counter_error']
   rows: [('ctl1', 2, 'counter_error', ['G5','G7'])]
after  tool-absent  driver_exit 1 ok False errors ['…','ctl1:tool_absent']
   rows: [('ctl1', 1, 'tool_absent', ['A',…,'T5'])]
after  stale-backdate driver_exit 1 ok False errors ['…','ctl1:stale_receipt']
   rows: [('ctl1', 0, 'stale_receipt', ['G2'])]
```

The stale class is refused at exit 0, i.e. by the mtime branch. Isolated on the same
receipt dict (same sha/seed/note/exit, only mtime differs):

```
in-window mtime (start+1s): (True, None)
fixture backdate (start-5s) : (False, 'stale_receipt')
```

Committed receipts agree: `verification/matrix/before.json` → `invalid_accepted=3`,
`rejections_named=0`; `verification/matrix/after.json` → `invalid_accepted=0`,
`rejections_named=3`, `named_classes=[counter_error, stale_receipt, tool_absent]`,
`honest_witnessed=27`, `honest_build_met=3`, unhyphenated values matching the
lesson. The honest after summary (`verification/honest-regression/after-v5-v2.json`
and its cohort twin) shows `ok=true, controls=27, witnessed=27, notMet=27, errors=[]`,
build 3/3 `met=true`, 0 rows with `error`.

## Findings

**LOW-1 — entry 14 `captured-by` misattributes a quote to round-44 kill rule (2).**
The entry says: *"Captured-by: kill rule (2) as frozen for round 44 ('receipts
re-derive at recorded seeds') certified seed-binding …"*. The frozen round-44 C1
kill rules (`SCORECARD.md:3459-3462`) say: *"(2) Any witness that is a timing-only
failure, a v4-corpus divergence, or a counter error → not a witness; if it was the
only one, C1 NOT MET."* — no seed/re-derivation clause. The quoted phrase is the
capability row (`SCORECARD.md:218`: "per-row receipts re-derive at their recorded
seeds") and the C1 claim text (`SCORECARD.md:3617`: "reproduced at their recorded
seeds"). The round-45 draft distinguished the two sources
(`drafts/mistakes.md:52-58`); the landed sentence fused them. Evidence that this is
a real misattribution: `round-44/w2/ReviewCounterContract.md:13` cites round-44
kill rule (2) as the rule that "says [a counter error] is not a witness", matching
the SCORECARD text, not the seed phrase.
Fix: split the sentence — kill rule (2) constrains witness admissibility; the
capability row/claim sentence is what certified seed-binding. No numeric claim or
fix behavior changes.

**NIT-1 — entry 14 v1 evidence range.** `expectation_ok` is cited as `:69-83`; the
frozen function spans `69-81` (`sed -n '69,84p' c44_audit.py` — lines 82-83 are
blank). Line refs are allowed to drift, but this is frozen bytes with no drift.

**NIT-2 — entry 15 fix says the SCORECARD correction "names both receipts with
sha256s".** The named receipt gets a full digest; the earlier one is abbreviated
(`2383efae…ce0902`, `SCORECARD.md:3764`). Full digest verified on disk:
`2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902`. Acceptable as
an identifier; not the full digest the fix's own "cite path + digest" standard asks
for.

## Residual risk / verification gaps

- **Not re-run by me:** the honest 27-control + 3-build leg under driver v2. I
  verified the committed cohort summary and the matrix receipt's identity block
  (27 controls, 27 witnessed, build 3/3, zero errors). The fixture legs, v2
  `--selftest`, and the freshness runner were re-run.
- **Freshness runner exit status is not a gate.** `c45_freshness.py` returned rc 0
  while printing the falsified `26/1/0` (`ok` only checks that every leg ran, as its
  docstring states). Entry 15's "able to fail" is the manual `jq -e` green/red pair
  (reproduced above), not a failing committed command.
- **The v2 gate binds a window, not authorship.** A receipt with the invoked
  counter's sha, a seed, `note != "tool absent"`, exit ∈ {0,1}, and an mtime inside
  `[started_ns - 1 s, finish_ns + 1 s]` is accepted. Measured: pre-planted 0.5 s
  before `started_ns` → `(True, None)`; 1.5 s before → `stale_receipt`. This is the
  same residual the SCORECARD C1 verdict records ("NOT MET as declared", causal
  clause unfalsifiable, routed to the operator); entry 14 does not overclaim it, but
  its fix should not be read as closing that clause.
- **Working-tree drift observed, not mine:** `git status --porcelain` shows
  `M .ufo/waves/round-45/verification/freshness/freshness.json` (a concurrent seat's
  re-run; values match the claim). Matrix receipts, `split.json`, both claim
  receipts, `SCORECARD.md`, and `corpus/lessons/round-45.md` are tracked.

## Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2/AttackLessonMistakes.md` (this report)
- `/fast/scratch/hyaku/kake-r45/AttackLessonMistakes/fixtures/{before,after}/*/summary.json` and their cohort `tools/`, `build-*.json`
- `/fast/scratch/hyaku/kake-r45/AttackLessonMistakes/freshness/freshness.json`

No lane file other than this report was written; no tool installs.
