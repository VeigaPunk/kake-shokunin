# AttackV6Diff — C2 kill rule 1

Axes: **freshness** (judged); operability (regression constraint).

## Named attack: PASS — landed v6 minimality survives

Independent, read-only review of every hunk in `.ufo/waves/round-45/v6diff/v5-v6.diff`, checked against both complete source files. This is a scoped attack result, not a canonical admission or a verdict on C2 as a whole.

| Hunk | Exact range | Reclassification | Result |
|---|---|---|---|
| 1, diff line 3 | `@@ -1,14 +1,12 @@` | **docstring-header**: only the opening version/provenance description changes (old source 2–11, new source 2–9). The inherited Round-42 description is context, not an edit. | PASS |
| 2, diff line 26 | `@@ -79,9 +77,11 @@` | **predicate-text + the permitted one-line module-level PREDICATE alias**: preserve the v5 string under `PREDICATE_V5`, introduce `PREDICATE_V4`, retain `PREDICATE = PREDICATE_V5`. | PASS |
| 3, diff line 41 | `@@ -993,7 +993,7 @@` | **predicate-text**: only the receipt's `predicate` value changes to the exact v5/v4 conditional. The rest of this shared construction line is unchanged. | PASS |

**OTHER hunks: zero.** The stored diff's entire hunk body exactly equals a freshly computed unified diff of the live frozen-v5 and landed-v6 bytes; it is not an incomplete or stale representation of those files.

## Counterexamples sought / smuggle-vector results

- **Ratio/reps smuggled on the changed receipt-construction line:** not present. `ratioLimit` still references `RATIO_LIMIT`, `reps` still references `REPS`, `met` remains `False`, and every other receipt field is AST-identical. This checks tokens, not merely the line's hunk label.
- **RATIO_LIMIT or REPS changed in predicate-hunk context or elsewhere:** not present. Declarations remain byte-identical at `2.0` and `5`; neither declaration is an added/removed line. All code outside the explicitly permitted spans is also byte-identical, covering their other uses and scoring logic.
- **Run-list/count/order smuggle:** not present. All three `runs` construction statements and `CLASS_MODULES` are byte-identical. The v4 list remains A–F plus T1–T5; class-list extension and class loading are unchanged.
- **PREDICATE_V5 differs from frozen PREDICATE:** not present. Python AST literal extraction and UTF-8 byte comparison agree: both are 229 bytes, SHA-256 `27ff711eebcec0b9ca60be84a8f5f08f79b981194760f1960fe1feffcae8c38e`.
- **The alias-deletion regression reported in `w1/ReviewKillRules.md` persists:** not present in the measured bytes. The one-line alias now exists. The historical report describes an earlier state and is not evidence that this current source lacks the alias.
- **Unconditional v4 text silently used in v5 mode:** not present. The receipt expression is exactly `PREDICATE_V5 if a.classes == "v5" else PREDICATE_V4`; isolated evaluation of that AST expression selects the frozen predicate in v5 mode and the v4 predicate in v4 mode. The v4 string removes only ` and the ten class runs` from the frozen text.

**Impacted axes:** no landed minimality regression found on freshness, and the specific missing-alias operability counterexample is repaired at source level. A generic hunk-label-only audit remains too weak to exclude adjacent-token smuggling, but that potential weakness is not an observed smuggle in this diff.

**Smallest safe correction:** none to the landed counter for this named attack. For this review, requiring unchanged non-predicate receipt fields and byte equality outside the permitted spans closes the hunk-label ambiguity without broadening the allowed source change. No source, rule, route, or receipt was edited.

## Exact commands and decisive output

Working directory: `/home/vgpnk/Projects/shokunin/kake-shokunin`.

```sh
mkdir -p /fast/scratch/hyaku/kake-r45/AttackV6Diff
python3 -B /fast/scratch/hyaku/kake-r45/AttackV6Diff/audit_v6_diff.py
```

The first command produced no output. The audit script was created with the file-write tool, remains in the named scratch directory, and performs AST/source-byte comparisons without importing either counter. Verbatim audit command output:

```text
Axes: freshness (judged), operability (regression constraint)
sha256 .ufo/waves/round-44/c44_count_v5.py 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
sha256 .ufo/waves/round-45/c45_count.py e17b5dc8a6bd710cd5b4c27569c0972730cf0048d8db4842e115945982cf403b
sha256 .ufo/waves/round-45/v6diff/v5-v6.diff c69a30ffb56b5e68a13279a87f1c8d2cfbe335894ea70bc08bd9a3b984b2c92f
Saved diff exactly covers live v5/v6 changes: PASS
Receipt keys unchanged: PASS
Every non-predicate receipt field unchanged: PASS
Receipt met: PASS | 'False' -> 'False'
Receipt ratioLimit: PASS | 'RATIO_LIMIT' -> 'RATIO_LIMIT'
Receipt reps: PASS | 'REPS' -> 'REPS'
Hunk count: PASS | 3
Hunk 1 at diff:3 @@ -1,14 +1,12 @@: PASS | class=docstring-header; removed=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]; added=[2, 3, 4, 5, 6, 7, 8, 9]
Hunk 2 at diff:26 @@ -79,9 +77,11 @@: PASS | class=PREDICATE alias+predicate-text; removed=[82, 83, 84]; added=[80, 81, 82, 83, 84]
Hunk 3 at diff:41 @@ -993,7 +993,7 @@: PASS | class=predicate-text; removed=[996]; added=[996]
RATIO_LIMIT declaration byte-identical: PASS | 2.0
RATIO_LIMIT declaration untouched by diff: PASS
REPS declaration byte-identical: PASS | 5
REPS declaration untouched by diff: PASS
CLASS_MODULES declaration byte-identical: PASS | (('G1', 'g1_longport_grammar.py'), ('G2', 'g2_default_port.py'), ('G3', 'g3_empty_path.py'), ('G4', 'g4_port_scope.py'), ('G5', 'g5_prefix_cut_45plus.py'), ('G6', 'g6_fold_pairs.py'), ('G7', 'g7_band_memos.py'), ('G8', 'g8_host_tables.py'), ('G9', 'g9_port_digits.py'), ('G10', 'g10_headtail_windows.py'))
CLASS_MODULES declaration untouched by diff: PASS
Every run-list construction byte-identical: PASS | 3 old / 3 new statements
run-list v6:1047-1048: 'runs = [("A", cases_a), ("B", cases_b), ("C", cases_c), ("D", cases_d), ("E", cases_e),\n                    ("F", None)]'
run-list v6:1049-1049: 'runs += [(key, None) for key, _ in CLASS_MODULES if key in classes]'
run-list v6:1050-1050: 'runs += [("T1", shape_t1), ("T2", shape_t2), ("T3", shape_t3), ("T4", None), ("T5", shape_t5)]'
PREDICATE_V5 UTF-8 byte-identical to frozen PREDICATE: PASS | old=229 bytes new=229 bytes sha256=27ff711eebcec0b9ca60be84a8f5f08f79b981194760f1960fe1feffcae8c38e
One-line module PREDICATE alias preserved: PASS | PREDICATE = PREDICATE_V5
Receipt predicate exact v5/v4 conditional: PASS
PREDICATE_V4 removes only ten-class phrase: PASS
Isolated receipt predicate selection classes=v5: PASS
Isolated receipt predicate selection classes=v4: PASS
All code outside permitted spans byte-identical: PASS | old=45965 bytes new=45965 bytes sha256=ea3ebc368641c97510db408f51b099a5736915573ad2b3a892e94c04dfd79b31
Named attack: PASS (landed v6 minimality survives; no smuggle found)
Counter/module execution: UNRUN; only AST parsing, byte comparison, and isolated predicate-expression evaluation performed
```

Audit command exit status: **0**.

## Scope and writes

Read for context: `AGENTS.md`, `w1/ReviewKillRules.md`, `w1/ExecCounterV6.md`, the two counters' header/receipt/run-list sections, the full stored diff, and a targeted search of `c45_freshness.py`. Artifact reports were treated as evidence only, not as contract changes.

Files written (complete list):

1. `.ufo/waves/round-45/w2/AttackV6Diff.md` — this report, the only lane write.
2. `/fast/scratch/hyaku/kake-r45/AttackV6Diff/audit_v6_diff.py` — read-only analysis script.

Created scratch directory: `/fast/scratch/hyaku/kake-r45/AttackV6Diff/`.

**Unrun:** full v4/v5 counter executions, audit-driver integration, timing/build/cohort runs, and mutation runs. No runtime receipt-equivalence claim is made. No tool installs, git/jj operations, subagent dispatch, frozen-file writes, or canonical-runtime invocation.
