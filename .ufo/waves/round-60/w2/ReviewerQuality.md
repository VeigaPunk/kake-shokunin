# ReviewerQuality

ATTACKS: Round-60 QUALITY.md criteria at B1: run each named falsifier and its example where feasible.

CRITERIA:

| Criterion | Falsifier run | Example run |
|---|---|---|
| C1 gate status | `python3 -B .ufo/waves/round-60/c60_gate_status.py --root . --revision 8b33fd248d126b48d838af5c38bc175850f41a09` → `C1 gate-status members=28 mismatches=0 scores_held=3/3 met=True`; exit 0. | Contract control `controls/base-c1-gate-status.txt` proves baseline failed (14 mismatches); C1 calibration score mutant not executed by this seat. |
| C3 source scope | `python3 -B .ufo/waves/round-60/c60_quote_truth.py --root . --revision 8b33fd248d126b48d838af5c38bc175850f41a09` → `9/9 met=True`; C3_row_shape PASS; exit 0. | Example phrase not separately injected/run. |
| C2 append-only | `python3 -B scripts/append_guard.py --root . --base fd6303ce5c14b3f892dec586297a942ab6e4193b --revision 8b33fd248d126b48d838af5c38bc175850f41a09` → `files=53 findings=0`; exit 0. `python3 -B .ufo/waves/round-60/c60_guard_cases.py --root . --revision 8b33fd248d126b48d838af5c38bc175850f41a09` → `24/24 met=True`, exit 0 (K3/K8/K9/K10/K16 and others). | The exact `[r20-correction 2026-10-19: …]` example was not separately run. K9/K10 verify comment/code-span cases, not the legacy spelling. |

FINDINGS: none.

Residual risk: criterion example mutants were not each executed independently; C2 case suite covers general untagged insertion and tag visibility but not specifically the legacy spelling shown in QUALITY.md. This is a coverage gap, not demonstrated behavior defect. Initial symbolic ref `B1` attempt failed (`fatal: ambiguous argument 'B1'`); checks rerun at pinned B1 hash in isolated shared clone.

VERDICT: No actionable finding; three falsifiers pass at B1.