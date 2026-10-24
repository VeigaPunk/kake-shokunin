# ReviewWave1Plan — padding, duplication and claim sizing of the round-45 wave-1 plan

Seat: `kake-r45.ReviewWave1Plan` (reviewer). Axes: operability + freshness (plan-level
instrument audit). Read-only on the lane; no lane bytes edited.

## Verdict

**Named attack: PASS — all three requested outputs are named.** Substantial overlaps:
01/04/12/21 (same split evidence) and 17/19 (same Gate rows). Items producing no C1/C2 or
frontier evidence: 03, 15, 17/18/19, 28, 32 (with reasons below; 16 is the record assembly,
not evidence). Claim-sizing violations: eleven listed in the table, the load-bearing ones
being C2(a)'s false 4/4, C2(c)'s misattributed 22/1/4, the unowned C2 command, and C1's
unanchored honest/not-met/mtime clauses.

**Wave unsound as declared.** The 32 items are mostly load-bearing (no pure-padding seat),
but the frozen C1/C2 after-states are not reachable as written:

1. **C2's frozen counting command has no owner and does not exist** — no item mentions
   `c45_freshness.py`; the three legs are planned as raw material (one landed, two blocked)
   and nothing composes them.
2. **C2(a) after = 4/4 is false on the shipped v2 selftest**: the m4 error-witness mutant
   survives (`SELFTEST PASS`, exit 0), so the instrument measures 3/4.
3. **C2(c) 22/1/4 belongs to the superseded pre-final receipt** (witnessed 23, ok=false),
   not the "27 witnessed" receipt the wave names; the named final receipt re-derives
   26/1/0. No single committed receipt yields both "27 witnessed" and "22/1/4".
4. **C1's frozen after receipt cannot carry `honest_witnessed=27`/`honest_build_met=3`**:
   `c45_matrix.py --stage after` (the frozen command, `SCORECARD.md:3654`) leaves
   `--with-honest` off, so it prints and records zeros; `passed` does not check the
   honest numbers even when the flag is on.
5. C1's not-met clause and the mtime half of clause (iii) have no after-state fixture in
   the frozen matrix.

Specific unsound items: **13** (honest-flag contract and after-stage stale fixture),
**11** (declared after leg unreachable), **12** (its expected 22/1/4 is wrong on its own
named path — its measured 26/1/0 is the correct evidence), and the **missing owner** of
`c45_freshness.py` (no item; L1-only fix).

Bytes audited (sha256 at 2026-10-24T03:23Z; seats were still writing, so reproduce against
these hashes): `c45_audit.py 5a342e29…c7051`, `c45_matrix.py cdddee5a…94cd`,
`c45_count.py ce8bf235…22556`.

## Method and decisive evidence

Read `SCORECARD.md:3628-3709` (frozen round-45 declaration), the 32 item prompts in
`.ufo/waves/round-45/w1-spec.json`, the round-44 receipts and wave-2 reports, and each
artifact that had landed at inspection. No LSP device was exposed in this seat's tool
inventory, so caller/definition checks were done by reading source; that is recorded as a
tooling limitation, not as semantic proof.

### F1 HIGH — the frozen C2 counting command is unowned and absent

```text
$ python3 -B -c "import json; d=json.load(open('.ufo/waves/round-45/w1-spec.json')); print('items mentioning c45_freshness:', [it['name'] for it in d['items'] if 'c45_freshness' in it['prompt']])"
items mentioning c45_freshness: []
$ ls .ufo/waves/round-45/c45_freshness.py
ls: cannot access '.ufo/waves/round-45/c45_freshness.py': No such file or directory
```

`SCORECARD.md:3698` defines C2's entire MET through
`python3 -B .ufo/waves/round-45/c45_freshness.py`; `SCORECARD.md:3701` makes the triple
conjunctive (`after=(4/4, false, 22/1/4)`). Items 10/11/12 produce the three legs; no item
composes them. This is the one frozen command the wave-1 build plan forgot to staff, while
`c45_audit.py` (item 8), `c45_count.py` (item 9) and `c45_matrix.py` (item 13) all have
owners. `CriticC2Scope` independently hit the absence (`python3: can't open file …`).

### F2 HIGH — C2(a) after 4/4 is false: m4 survives the shipped v2 selftest

I applied item 11's m4 body (`if row.get("error"): return True` at the head of
`semantic_witness`) to a scratch copy of the shipped v2 driver and ran its selftest:

```text
$ python3 -B /fast/scratch/hyaku/kake-r45/ReviewWave1Plan/m4_v2.py --selftest
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
M4_V2_EXIT=0
$ python3 -B .ufo/waves/round-45/c45_audit.py --selftest
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, and build-count gates
UNMUTATED_V2_SELFTEST_EXIT=0
$ python3 -B /fast/scratch/hyaku/kake-r45/ReviewWave1Plan/m2_v2.py --selftest >/dev/null 2>&1; echo "M2_V2_EXIT=$?"
M2_V2_EXIT=1
```

Cause: the v2 selftest's `error_row` is passed only to `not_met_rows` and
`expectation_ok("not-met", …)` (`c45_audit.py:167-169`), never to `semantic_witness`.
m4's mutation is therefore unexercised, and the selftest reports PASS. C2(a)'s declared
after-state is 3/4, not 4/4. (m2 is killed, so the harness itself is fine; m1/m3 kills are
[INFERENCE] from the selftest assertions at `c45_audit.py:140-146`, which directly bite
those mutations.) This is the same "v2 selftest vs m4" suspicion `ScoutDoNothingControls`
recorded; the execution above makes it decisive for the current bytes.

### F3 HIGH — C2(c)'s 22/1/4 is the pre-final receipt; the named final receipt is 26/1/0

```text
$ for f in .ufo/waves/round-44/verification/claim/after-v5.json .ufo/waves/round-44/verification/claim/after-final/after-v5.json; do echo "== $f"; jq -r '.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length, mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length, met: map(select(.met==true))|length, other: map(select(.met==false and (.classCaught|length)==0))|length}' "$f"; jq -r '"controls=\(.controls) witnessed=\(.witnessed) ok=\(.ok)"' "$f"; done
== .ufo/waves/round-44/verification/claim/after-v5.json
{
  "class_only": 22,
  "mixed": 1,
  "met": 4,
  "other": 0
}
controls=27 witnessed=23 ok=false
== .ufo/waves/round-44/verification/claim/after-final/after-v5.json
{
  "class_only": 26,
  "mixed": 1,
  "met": 0,
  "other": 0
}
controls=27 witnessed=27 ok=true
```

The frozen sentence ("the round-44 claim receipt's **27 witnessed controls** re-derive as
22 class-only + 1 mixed + **4 met**", `SCORECARD.md:3687-3689`) mixes two receipts: the
22/1/4 split comes from the pre-final 23-witness `ok=false` receipt, where the four
`met` rows are not witnesses at all; the 27-witness receipt is 26/1/0. Item 12 names
`after-final` and expects 22/1/4 — its own command cannot produce its expected value.
`ExecWitnessSplit` landed the measured 26/1/0 and correctly reported FAIL; `CriticC2Scope`,
`ScoutRoutedLedger` and `ScoutDoNothingControls` reached the same conclusion. The finding
is corroborated; the plan defect is that the declaration was frozen with an unreachable
third leg and that four seats were spent re-proving it.

### F4 HIGH — C1's honest-cohort leg is not enforced by the frozen command

```text
$ grep -n "with-honest\|if not requested\|passed = (\|honest_control_ok" .ufo/waves/round-45/c45_matrix.py
181:    if not requested:
205:    parser.add_argument("--with-honest", action="store_true",
272:    honest_control_ok = (isinstance((honest_run or {}).get("summary"), dict)
287:        passed = (complete_fixture_runs and all_fixture_runs_rejected and invalid_accepted == 0
288:                  and all_rejected and rejections_named == 3 and honest_control_ok)
```

With `--with-honest` absent, `honest_metrics` returns the zero sentinel (`:181`), so the
after receipt and the printed line carry `honest_witnessed=0 honest_build_met=0`. The frozen
invocation (`SCORECARD.md:3654`) has no flag, and the frozen C1 MET requires
`honest_witnessed=27`, `honest_build_met=3` (`SCORECARD.md:3657-3658`). Even with the flag,
`passed` (`:287-288`) checks only the one-control junk control, not the 27-control cohort or
the three builds: a v2 that loses one honest witness still writes `passed: true` and the
frozen command's exit code is green. The honest clause is therefore do-nothing-reachable at
the counting-command level. (The 27/27 comparison itself lives in item 14, which was
blocked because the receipt did not exist at its start.)

### F5 MED — the after matrix never exercises the mtime/window conjunct

```text
$ grep -n "plant_from = None\|args.stage == \"before\" and fixture_name" .ufo/waves/round-45/c45_matrix.py
234:            plant_from = None
235:            if args.stage == "before" and fixture_name == "stale-planted":
```

Planted receipts are copied only for `--stage before`. For `--stage after`, the
stale-planted run gets a fresh empty cohort; its fake counter writes nothing and
`os.kill(os.getpid(), signal.SIGKILL)`s (`fixtures/stale-planted/fake_counter.py`), so
`receipt_validity` returns at its first check — `exit_code not in (0, 1)` →
`counter_error` (`c45_audit.py:73`). The fixture named `stale-planted` therefore contributes
no `stale_receipt` row after the fix. The `stale_receipt` names that do appear in the after
stage come from the *build* rows of the other two classes: their copied `build-1.json`
carries the real v5 counter sha (`5cedaa3b…`), which mismatches the invoked fake counter, so
the sha-binding path is exercised — but every after-stage receipt is written *inside* the
run window, so a v2 with sha binding and no mtime check passes `invalid_accepted=0`,
`rejections_named=3`. The declared clause "was not written inside the driver's own run
window" is not measured after the repair.

The per-fixture naming also contradicts the declaration's "each rejection named with its
defect class" (`SCORECARD.md:3650`). With v2 as written (`error=validity_error`,
`c45_audit.py:256`): counter-error control → `counter_error`; counter-error builds →
`stale_receipt` (their copied real receipts carry a foreign `counterSha256`); tool-absent
control → `tool_absent`; tool-absent builds → `stale_receipt`; all four stale-planted rows →
`counter_error` (exit -9). `rejections_named=3` is therefore reached by the sha-mismatch
build rows, while the fixture class named `stale-planted` is never the source of a
`stale_receipt` name.

### F6 MED — item 13's rejected-row arithmetic was wrong in the plan (already fixed in bytes)

Item 13 says "distinct named error classes among the 9 rejected rows: 3 fixture classes x
control+3 builds". 3 × (1 + 3) = 12, and the fixtures carry `ctl1` + `build-1..3`
(`fixtures/*/controls.tsv`, `fixtures/stale-planted/{build-1,build-2,build-3}.json`). The
implementation corrected it to `expected_rows = 3 * 4` (`c45_matrix.py:282`) and
`ExecMatrixRunner` reported the same inconsistency. No action beyond noting that a literal
implementation would have hard-failed the after predicate.

### F7 MED — C1's not-met half has no after fixture

```text
$ grep -n '"witnessed", with_builds\|"not-met", with_builds' .ufo/waves/round-45/c45_matrix.py
247:                              controls, fake_counter, "witnessed", with_builds=True,
258:                                   honest_controls, counter, "not-met", with_builds=False))
```

All three invalid fixtures run under `--expect witnessed`; only the honest control runs
`--expect not-met`. Defect 2 (`--expect not-met` counts exit-2 cannot-evaluate receipts as
not-met, `ReviewCounterContract.md` MEDIUM) has no after-state measurement. A v2 with the
exit/note/sha/window gates but the old `not_met` counting still produces
`invalid_accepted=0`, `rejections_named=3`, `honest=27/3`. The v2 selftest asserts
not-met exclusion (`c45_audit.py:167-169`), but the frozen counting command never reads
that assertion. The same holds for the claim sentence's second half ("refuses to count as
not-met") — it is unmeasured by `c45_matrix.py`.

### F8 LOW — C2(b) after leg is a negative test

`SCORECARD.md:3701` only requires `v4_predicate_names_class_runs=false`. A predicate naming
zero runs satisfies it. Item 10's manual jq ("must name only the eleven v4 runs") is
stricter but is not the counting command. Current bytes are correct — `PREDICATE_V4` names
"the eleven v4 runs", and `PREDICATE_V5` is byte-identical to the frozen string:

```text
frozen PREDICATE len 229
v6 PREDICATE_V5 len 229
byte-identical: True
```

Recommend `c45_freshness.py` assert the eleven names are present and no `G` key, not just
absence of the phrase.

### F9 LOW — C2(a) mutant inputs are post-freeze reconstructions

Item 11 reconstructs m1–m4 from `MutClassGate.md`'s behavioral descriptions; kill rule 3
requires documentation, not byte identity. `before=2/4` is stable only if the reconstruction
matches; a weaker m2 or a different m4 is a different experiment. The receipt should pin
mutant sha256, and `c45_freshness.py` should hash-check them. `ExecMutantMatrix`'s before
table (2/4, m2/m4 surviving) matches, so today's reconstruction is faithful — this is an
input-pinning risk, not a defect.

### F10 LOW — the invalid fixtures are post-freeze, though the declaration calls them "committed"

```text
$ git ls-tree -r --name-only 3b4c430a -- .ufo/waves/round-45/
(no output)
$ git diff --stat 3b4c430a HEAD -- SCORECARD.md
(no output; declaration bytes unchanged)
```

No round-45 tree existed at the freeze commit, so "the three committed invalid fixture
classes" (C1 before/after) did not exist when the claim was frozen. The before=3/3 is a
measurement over fixtures authored in the same wave; kill rule 5 (non-strawman) is enforced
only post hoc (item 22). The fixture READMEs document byte-copy provenance from committed
receipts, which lowers the risk, but the "before" is not a re-derivation over pre-existing
bytes.

### F11 LOW — wording: "records a counter exit"

Real receipts have no exit field (`repeat-len-band.json` keys start
`predicate, met, ratioLimit, reps, revision, toolFile, label, seed, counterSha256, …` — no
`exit`). The driver records the observed subprocess returncode on its row, and v2 correctly
uses that argument (`c45_audit.py:68-73`), so the instrument matches the intent. The frozen
sentence says the *receipt* records the exit; a strict evaluator could call the fixture
non-conforming under that reading. Wording risk only.

## Duplication / overlap

| Pair(s) | Overlap | Call |
|---|---|---|
| **01 ScoutRoutedLedger, 04 ScoutDoNothingControls, 12 ExecWitnessSplit, 21 CriticC2Scope** | All four land the same evidence: the 22/1/4 split vs the final receipt's 26/1/0 (`ScoutRoutedLedger` MX-arith, `ScoutDoNothingControls` C2(c) row, `ExecWitnessSplit` split.txt, `CriticC2Scope` counterexample). Same receipt, same jq, same conclusion. | **Substantial overlap.** Independent confirmation has value, but four seats on one arithmetic defect is the wave's largest redundancy; 01 or 04 could have owned it and the others cited it. |
| **07 ExecInvalidFixtures, 13 ExecMatrixRunner** | Both run frozen v1 over the same three classes and count 3/3 acceptance; 07's per-class captures (`verification/hardening/before/`) duplicate 13's `--stage before` receipt. | Bounded: 07 constructs and proves the fixtures (unique), 13 is the frozen command. Keep 07 for provenance; its before summaries are redundant once 13 runs. |
| **17 ScribeSourcesGate, 19 ScribeLessonMistakes** | 17 drafts the S133 admission row plus one reject; 19's item (2) drafts a Gate table skeleton containing "S133 admit" and "the rejected non-primary source". Same Gate rows, two files. 18's entry also cites S133 and narrates the same three defects as 19's Mistakes row. | **Substantial overlap** on the Gate rows; 17 should own the decisions and 19 import them, or 19 should carry placeholders only. Three seats (17/18/19) for one source row + one entry + one lesson. |
| 11 ExecMutantMatrix, 29 MutDriverV2Spec | Both mutate the driver and run `--selftest`; paths differ (`mutants/m1-4.py` vs `mutants/v2/m1-11.py`), mutant semantics differ (witness-class vs gate-removal). | Minor: two independent "v2 selftest kills N" tables will need reconciling in one receipt; no file collision. |
| 12 ExecWitnessSplit, 16 ScribeDeclarations | 12 drafts the exact witness-split SCORECARD sentence; 16's C2 paragraph includes that same sentence. | Minor: 16 must consume `drafts/witness-split-sentence.md`, not re-draft it. |

No item is pure padding. The opposite failure is more visible: the wave is over-manned on
the split arithmetic and the corpus prose, and unmanned on the C2 counting command.

## Items that cannot produce C1/C2 (or frontier) evidence

- **03 ConnectorSiblingOverlap** — cross-lane surface sweep; output is a coordination report,
  not evidence. Foldable into 28 (both are scope audits); keep only if cross-lane duplicate
  claims are a live risk.
- **15 ExecLedgerGate** — guards the round-43/44 ledger figures (`scripts/ledger_latest_check.py`
  contract: rescore tally in SCORECARD, do-nothing ratios in LOG), neither of which is in the
  round-45 claims or kill rules. Justified only as a standing-gate no-harm check because 16's
  append can shift those quoted figures; it produces no C1/C2 evidence.
- **17/18/19 corpus drafts** — no frozen command reads `corpus/` or the drafts. Round-45 has
  no quote-truth counter (unlike rounds 28–31), so the S133 row, the knowledge entry and the
  Gate rows are unmeasured prose this round. They serve a freshness corpus step, but cannot
  move either MET.
- **28 ReviewScopeBound** — bounds guard; necessary, no claim evidence (already landed).
- **32 SimplifierV2** — report-only YAGNI; cannot change the frozen sentence, and the
  implementation bytes now exist, so its deletion advice is post hoc. Lowest value in the wave.
- 16 ScribeDeclarations is documentation, not evidence, but it is the assembly step for the
  SCORECARD record and should stay after the receipts exist.

## Claim-sizing violations (declared claims)

| # | Violation | Evidence |
|---|---|---|
| 1 | C1 universal: "**any** control whose receipt …" while the counting command enumerates exactly three fixture classes plus the 27-control cohort. | `SCORECARD.md:3640-3645`; `c45_matrix.py` runs `FIXTURE_CLASSES` only. Item 20 owns the text attack; the gap is known. |
| 2 | C1 honest leg unmeasurable/do-nothing-reachable at the frozen command. | F4. |
| 3 | C1 not-met half unmeasured. | F7. |
| 4 | C1 mtime conjunct unmeasured after the fix. | F5. |
| 5 | C2(a) after-state false on current bytes (3/4, not 4/4). | F2. |
| 6 | C2(c) after-state unreachable / misattributed (22/1/4 vs 26/1/0). | F3. |
| 7 | C2(b) after leg is a negative test a vacuous predicate passes. | F8. |
| 8 | C2(a) mutant population not pinned at freeze (reconstructed inputs). | F9. |
| 9 | "Committed" fixtures did not exist at freeze; before-state is same-wave construction. | F10. |
| 10 | Item 13's 9-vs-12 rejected-row arithmetic (fixed in bytes, plan text still wrong). | F6. |
| 11 | "receipt records a counter exit" — no such receipt field. | F11. |

## Residual risk and verification gaps

- **Unrun by this seat:** `c45_matrix.py --stage before|after`, the full 27-control honest
  regression, the v6 v4 receipt, and `c45_freshness.py` (absent). My C1 after-stage analysis
  is static plus the m4/m2 selftest executions on scratch copies; the matrix writes under
  `verification/matrix/`, outside my write scope, so I did not run it.
- m1/m3 kills were not executed against v2 (only m2/m4); their kill is [INFERENCE] from the
  assertions at `c45_audit.py:140-146`.
- If `c45_freshness.py` lands after this report, F1 becomes a staffing omission rather than a
  missing artifact; F3's target (22/1/4 vs 26/1/0) and F2's 3/4 remain until the declaration
  or the selftest changes.
- The artifacts audited are moving (wave in flight); the hashes at the top let the L1 tell
  whether a finding still applies.

## Files written

- `.ufo/waves/round-45/w1/ReviewWave1Plan.md` (this report).
- `/fast/scratch/hyaku/kake-r45/ReviewWave1Plan/m4_v2.py` and `m2_v2.py` (scratch mutant
  copies used for the F2 execution; no lane file touched).

Tools installed/updated: none (python3, jq, git and coreutils already present; pacman paused).
Blockers: none to this audit. The C2 legs' own blockers (missing command/receipts) are
reported as findings F1/F3.
