# ScoutCounterV4Map — v4 run list, receipt predicate, provenance label

Axes: **freshness** (receipt predicate names only runs the selected mode executes) and **operability** (run list, loader, scoring, and receipt schema other than `predicate` stay put). This seat is judged on freshness. No tool was installed.

Frozen map target: `.ufo/waves/round-44/c44_count_v5.py`, sha256 `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc`. Line numbers below are that file unless marked v6. The file was not edited.

## Named attack

C2(b) / CriticHarmGuard counterexample: `--classes v4` still writes a `predicate` that names ten class runs the mode does not execute.

**Frozen counter: FAIL** (defect present). **Landed `.ufo/waves/round-45/c45_count.py` source: PASS** on the predicate-text contract (strings and the one receipt selector). This seat did not run the counter, so there is no runtime v6 receipt from this seat.

## v4 execution path (observed)

`--classes` is parsed at 989–991 (`choices=("v5", "v4")`, default `"v5"`). Help text: v5 = eleven v4 runs plus ten class runs; v4 = v4 corpus only.

Under `a.classes == "v4"`:

| Step | Lines | What happens |
|---|---|---|
| Class table | 1046 | `classes = {}`. `load_classes` (136–152) is not called. |
| Base list | 1047–1048 | `("A", cases_a), ("B", cases_b), ("C", cases_c), ("D", cases_d), ("E", cases_e), ("F", None)` |
| Class insert | 1049 | `[(key, None) for key, _ in CLASS_MODULES if key in classes]` — empty, because `classes` is `{}`. |
| Timing | 1050 | `("T1", shape_t1), ("T2", shape_t2), ("T3", shape_t3), ("T4", None), ("T5", shape_t5)` always appended. |

Resulting list, in this order, eleven keys: **A, B, C, D, E, F, T1, T2, T3, T4, T5**. G1–G10 are not inserted. Definition order of the generators is not this order (`cases_d` is at 685, after `cases_e` at 414 and `cases_f` at 497).

Dispatch (1053–1071), v4 branch taken:

- A–E (`key in ("A","B","C","D","E")`, 1056–1059): `gen(rng)` then `layout_cases` (725). Defs: `cases_a` 281, `cases_b` 304, `cases_c` 708, `cases_d` 685, `cases_e` 414.
- F (1060–1062): `cases_f` (497) then `layout_f` (546). F is one of the eleven v4 runs, not a class module.
- `elif key in classes` (1063–1065): unreachable when `classes` is `{}`.
- T4 (1066–1068): `shape_t4` (865). T1/T2/T3/T5 fall through to `gen(rng, cd)` (1069–1071). Defs: `shape_t1` 795, `shape_t2` 642, `shape_t3` 813, `shape_t5` 843.

`met` (1109–1113) uses `len(runs)` and the five ratios. It does not read the predicate sentence. v4 therefore scores 11 runs. The ten class runs are `CLASS_MODULES` G1–G10 at 99–110.

## Receipt fields

Built once, before the loop, at 996–1003. Written by `finish` (1005–1012) on every exit.

- `predicate` (996): unconditional `PREDICATE`. Same sentence in v4 and v5.
- `classesMode` (1000): `a.classes` (`"v4"` in this mode).
- `classRuns` (1001): `[key for key, _ in CLASS_MODULES] if a.classes == "v5" else []`. v4 writes `[]`.

`PREDICATE` the name occurs only at the assignment (82) and this receipt read (996). No other read.

## PREDICATE string (frozen)

Lines 82–84, value length 229, concatenated (the indent outside the quotes is not part of the value):

```
met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's
```

That parenthetical is what a v4 receipt falsely claims. It is not the round-43 predicate. The round-43 value (`c43_count_v4.py` 78–80) is the shorter sentence with no parenthetical: `... on every generated run, and its median CPU time ...` (no `(the eleven v4 runs)`). Round 45 does **not** restore that sentence.

## Shipped v4 receipt (same counter bytes)

`.ufo/waves/round-44/verification/claim/v4-final/tools/hosttable-A.json`: `counterSha256` `5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc` (matches the frozen file), `classesMode` `"v4"`, `classRuns` `[]`, `equalRuns` `"11/11"`, `runs` keys exactly `A B C D E F T1 T2 T3 T4 T5`, and `predicate` still contains `and the ten class runs`. The paired v5 receipt `after-final/tools/hosttable-A.json` has keys `A B C D E F G1 G2 G3 G4 G5 G6 G7 G8 G9 G10 T1 T2 T3 T4 T5`, `classesMode` `v5`, `classRuns` the ten G keys.

## Docstring provenance nit

Line 11 says `Round-43 version 4 header follows for provenance:`.

What follows, lines 13–70 (5047 bytes including the trailing newline), is byte-identical to `c43_count_v4.py` lines 9–66. That span opens `Round-42 C1 counter, version 3 (pre-freeze redesign of version 2, ...` and runs through the v3 usage, equality (A–F), timing (T1–T5), and sandbox paragraphs, closing the docstring at line 70. `c43_count_v4.py` line 7 already labels that same span `Round-42 version 3 header follows for provenance:`.

The actual Round-43 version 4 preamble is `c43_count_v4.py` lines 2–7 (also `build_v5.py` `OLD_HEAD`, lines 19–25). `build_v5.py` `NEW_HEAD` (27–37) replaced that preamble and then mislabeled the retained v3 text as a version 4 header. So the accurate one-line description of what follows line 11 is:

```
Round-42 version 3 header follows for provenance:
```

## Minimal v6 change (specified; already present on disk)

Byte-copy `c44_count_v5.py` to `.ufo/waves/round-45/c45_count.py`, then only:

1. Replace the `PREDICATE` assignment with two constants. `PREDICATE_V5` must concatenate to the 229-byte frozen value above (keep the same three literals; a longer name may reindent the continuation lines — indent outside the quotes does not change the value). `PREDICATE_V4` value, length 206, is that string with the parenthetical reduced and nothing else changed:

```
met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's
```

2. Receipt line: `"predicate": PREDICATE_V5 if a.classes == "v5" else PREDICATE_V4`. Do not touch `classesMode`, `classRuns`, the run list, `load_classes`, or scoring.

3. Docstring line 11 becomes the Round-42 version 3 label above. Do not rewrite the retained v3 header.

`c45_count.py` (sha256 `ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556`) already matches. This seat did not write it. `diff` against the frozen file is exactly three hunks: docstring label (v6 line 11), the two predicate constants (v6 lines 82–85; `PREDICATE_V4` is one single-quoted literal whose value equals the 206-byte sentence), and the receipt selector (v6 line 997). No run-list, loader, CLI, `classesMode`, `classRuns`, or scoring hunk. v6 run-list lines are the frozen lines plus one because the predicate block grew by one line. `.ufo/waves/round-45/v6diff/` contained no file at read time.

## Commands and verbatim output

In-process (`ast` + `difflib`), not a counter run. First extraction:

```text
sha256 c44 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
sha256 c43 1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab
v3-header byte-identical True len 5047
c44 L11: 'Round-43 version 4 header follows for provenance:'
c43 L7: 'from version 3. Round-42 version 3 header follows for provenance:'
first following line c44 L13: 'Round-42 C1 counter, version 3 (pre-freeze redesign of version 2, sha256 01d3fb8'
first following line c43 L9: 'Round-42 C1 counter, version 3 (pre-freeze redesign of version 2, sha256 01d3fb8'
PREDICATE repr: "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's"
PREDICATE len 229
specified PREDICATE_V4: "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's"
V4 is V5 with parenthetical swap only True
ORIGINAL v4 PREDICATE: "met: the tool's exit code and output equal the round-41 tool's on every generated run, and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's"
specified V4 == original v4 predicate? False
PREDICATE name lines [82, 996]
--- classes == comparisons ---
1001 a.classes == "v5"
1046 a.classes == "v5"
1049 key in classes
1063 key in classes
```

Shipped receipts:

```text
runs keys ['A', 'B', 'C', 'D', 'E', 'F', 'T1', 'T2', 'T3', 'T4', 'T5']
n 11
G keys []
classesMode v4
classRuns []
equalRuns 11/11
predicate names class runs True
predicate met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's
v5-mode runs keys ['A', 'B', 'C', 'D', 'E', 'F', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'T1', 'T2', 'T3', 'T4', 'T5']
v5 classesMode v5 classRuns ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10'] equalRuns 20/21
```

Landed v6 versus frozen v5:

```text
sha256 v5 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
sha256 v6 ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556
PREDICATE_V5 byte-identical to frozen PREDICATE: True
lens 229 229 206
PREDICATE_V4: met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's
names class runs in V4: False
names eleven v4 runs in V4: True
DIFF_LINES 28
--- c44_count_v5.py
+++ c45_count.py
@@ -9,5 +9,5 @@
 non-ASCII case-fold pairs, the three repetition guard bands, host tables outside the v4 host
 population, port-digit caches, and head/tail windows over long ports.
-Round-43 version 4 header follows for provenance:
+Round-42 version 3 header follows for provenance:

 Round-42 C1 counter, version 3 (pre-freeze redesign of version 2, sha256 01d3fb8d...: adds run E, every
@@ -80,7 +80,8 @@
 import tempfile

-PREDICATE = ("met: the tool's exit code and output equal the round-41 tool's on every generated "
-             "run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the "
-             "five timing shapes is at most 2.0 times the round-40 tool's")
+PREDICATE_V5 = ("met: the tool's exit code and output equal the round-41 tool's on every generated "
+                "run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the "
+                "five timing shapes is at most 2.0 times the round-40 tool's")
+PREDICATE_V4 = 'met: the tool\'s exit code and output equal the round-41 tool\'s on every generated run (the eleven v4 runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool\'s'
 RATIO_LIMIT = 2.0
 REPS = 5
@@ -994,5 +995,5 @@
     root = os.path.abspath(a.root)
     seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(6), "big")
-    rec = {"predicate": PREDICATE, "met": False, "ratioLimit": RATIO_LIMIT, "reps": REPS,
+    rec = {"predicate": PREDICATE_V5 if a.classes == "v5" else PREDICATE_V4, "met": False, "ratioLimit": RATIO_LIMIT, "reps": REPS,
            "revision": None, "toolFile": a.tool_file, "label": a.label, "seed": seed,
            "counterSha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
```

## Files written

- `.ufo/waves/round-45/w1/ScoutCounterV4Map.md` (this report).

No scratch files. No counter, audit, build, or formatter was run.

## Unrun / not owned

- No v6 `--classes v4` receipt. `ExecV4ReceiptV6` owns that. `c45_count.py` was already present, so the dependency is not absent.
- `.ufo/waves/round-45/v6diff/v5-v6.diff` was absent. The in-process diff above is this seat's classification, not that artifact.
- Confidence: high on the line map, the 229/206 predicate bytes, the v3-header identity, and the shipped v4 receipt. The v6 source match is a read of the file as it stood during this seat, not a claim that a later edit cannot drift.
