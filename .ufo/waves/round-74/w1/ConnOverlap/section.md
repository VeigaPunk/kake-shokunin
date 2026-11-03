### Round 74 gate registry additions

Round 74 registers the eight counters named by the frozen contracts of rounds 69-73 plus `c74_registry_gap.py`; the predicate is frozen in `.ufo/waves/round-74/contract.md` section C1 before any data is scored.
The section is appended at EOF — line 1404 at base — beyond line 935, the largest `.line` pinned for `SKILL.md` in `corpus/knowledge/freshness-sidecar.json`, so no pinned line moves.
Withdrawal rule: a row goes when its counter is superseded for its class and the successor row names the predecessor; a future row keeps this append-at-EOF discipline or re-pins the sidecar in the same commit.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values / frozen proof | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| c69_recorded_counts.py | gate (live; calibration: recorded counts of the round-69 receipt family) | `python3 -B .ufo/waves/round-69/c69_recorded_counts.py --root . --revision <rev>` | `0=met`; `1=not met`; `2=unevaluable`; `64=usage` | none (one-off round counter; predicate frozen in `.ufo/waves/round-69/contract.md` section C1) | predicate frozen before any data; base receipt `.ufo/waves/round-69/controls/c1-base.txt` | report only | L1 |
| c69_tmp_honour.py | gate (live; operability: honour of the scratch-root annotation rule in round-69 prose) | `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --root . --revision <rev>` | `0=met`; `1=not met`; `2=unevaluable`; `64=usage` | none (one-off round counter; predicate frozen in `.ufo/waves/round-69/contract.md` section C2) | predicate frozen before any data; base receipt `.ufo/waves/round-69/controls/c2-base.txt` | report only | L1 |
| c70_pointer_audit.py | gate (live; calibration: SCORECARD evidence pointers and the append-only conjunct) | `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --root . --revision <rev> --base <base>` | `0=met` (`unannotated=0 append_only=true`); `1=not met`; `2=unevaluable`; `64=usage` | `python3 -B .ufo/waves/round-70/c70_pointer_audit.py --selftest --work <scratch>` | predicate frozen in `.ufo/waves/round-70/contract.md` section C1, Amendment 1 | report only | L1 |
| c71_calibration.py | gate (live; calibration: the round-71 calibration count) | `python3 -B .ufo/waves/round-71/c71_calibration.py --root . --revision <rev>` | `0=met`; `1=not met`; `2=unevaluable`; `64=usage` | none (one-off round counter; predicate frozen in `.ufo/waves/round-71/contract.md` section C1) | predicate frozen before any data | report only | L1 |
| c71_tmp.py | gate (live; operability: the round-71 scratch-root scan) | `python3 -B .ufo/waves/round-71/c71_tmp.py --root . --revision <rev>` | `0=met`; `1=not met`; `2=unevaluable`; `64=usage` | none (one-off round counter; predicate frozen in `.ufo/waves/round-71/contract.md` section C2) | predicate frozen before any data | report only | L1 |
| c72_tmp_v2.py | gate (live; operability: v2 of the scratch-root citation counter) | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --root . --revision <rev>` | `0=met` (`findings=[]`); `1=not met`; `2=unevaluable`; `64=usage` | `python3 -B .ufo/waves/round-72/c72_tmp_v2.py --selftest --work <scratch>` | predicate frozen in `.ufo/waves/round-72/contract.md` section C2; the v3 successor is `c73_tmp_v3.py` | report only | L1 |
| c73_wave_pointers.py | gate (live; calibration: wave-relative receipt pointers for round 72) | `python3 -B .ufo/waves/round-73/c73_wave_pointers.py --root . --revision <rev>` | `0=met` (`unannotated=0`); `1=not met`; `2=unevaluable`; `64=usage` | `python3 -B .ufo/waves/round-73/c73_wave_pointers.py --selftest --work <scratch>` | predicate frozen in `.ufo/waves/round-73/contract.md` section C1 | report only | L1 |
| c74_registry_gap.py | gate (live; calibration: registration of the eight population counters in this table) | `python3 -B .ufo/waves/round-74/c74_registry_gap.py --root . --revision <rev>` | `0=met` (`unregistered=0 own_row=true`); `1=not met`; `2=unevaluable`; `64=usage` | `python3 -B .ufo/waves/round-74/c74_registry_gap.py --selftest --work <scratch>` | predicate frozen in `.ufo/waves/round-74/contract.md` section C1; base receipt `.ufo/waves/round-74/controls/base-c1-registry.txt` | report only | L1 |

Each row is offline and reads committed bytes; `--revision` names the measured commit and `--root` the lane directory when the counter takes one.
A row whose Entry-command path does not resolve at the measured revision fails registration conjunct 2 of section C1; a prose mention outside a table row is not a registration.

#### Evidence at base

| Counter | Registered at base | Row added by round 74 | Evidence |
|---|---|---|---|
| c69_recorded_counts.py | no | yes | absent from every rendered table row at base |
| c69_tmp_honour.py | no | yes | absent from every rendered table row at base |
| c70_pointer_audit.py | no | yes | absent from every rendered table row at base |
| c71_calibration.py | no | yes | absent from every rendered table row at base |
| c71_tmp.py | no | yes | absent from every rendered table row at base |
| c72_tmp_v2.py | no | yes | absent from every rendered table row at base |
| c73_wave_pointers.py | no | yes | absent from every rendered table row at base |
| c74_registry_gap.py | no | yes | the own row; base receipt `unregistered=7`, `met=false` |

Base receipt: `.ufo/waves/round-74/controls/base-c1-registry.txt` — `unregistered=7`, `met=false`, exit 1, reproduced by the round-74 counter at base.
After target: `unregistered=0`, `own_row=true`, every row path resolves at the measured revision, counter exit 0.

Every cell above is a single-line value with no literal pipe character; commands use `python3 -B` so no bytecode file is written into the lane.

Verification order: run the Self-test first, then the Entry command at the measured revision; a selftest that does not kill its fixtures blocks the row.
This section is the round-74 registry addition and supersedes no earlier row; `c73_tmp_v3.py` stays registered by its round-73 row above.
