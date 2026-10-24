# CriticHarmGuard — v4-mode harm-guard attack

## Axes and result

- **Operability:** counter behavior, CLI compatibility, and truthful receipt semantics.
- **Freshness:** accuracy of the compatibility/provenance statement against the compared bytes; C2 ledger behavior was not assessed.
- **Named harm guard: FAIL. Attack succeeded.** The diff has **8 hunks**, not solely class-run dispatch. In particular, the shared `PREDICATE` and receipt construction change on the explicit v4 path. This is an item-level falsification, not a round-admission judgment.

## Counterexample and smallest safe correction

**Decisive counterexample:** select `--classes v4`. The source sets `classes = {}` (line 1046), inserts no G runs (1049), and records `classRuns: []` (1001), but `rec["predicate"]` unconditionally uses the new `PREDICATE` (996), which says the generated runs include **“the eleven v4 runs and the ten class runs”** (82–84). Thus a v4 receipt describes ten class runs that its mode does not execute. This is a source-derived counterexample, **[INFERENCE]**, not a fabricated runtime receipt.

The original receipt also had neither `classesMode` nor `classRuns`; both now appear in v4 mode. These additive fields are an interface change, not evidence of an observed downstream parser failure. The new CLI option/default likewise changes the shared interface: legacy invocations omitting it now select v5, though an explicit v4 invocation retains the old run sequence.

**Important limit:** the diff shows no changed bodies in `cases_f`, `layout_f`, the A–E generators/layout helpers, T1–T5 generators, sandbox/runner, timing repetitions, ratio computation, or final `met` computation. With explicit v4 mode, the refactored run list remains A, B, C, D, E, F, T1, T2, T3, T4, T5; the class loader is not called and the class branch is unreachable. Therefore this review finds a shared-path/receipt defect, **not** an observed change to v4 generated cases or computed acceptance. No runtime equivalence test was run.

**Smallest safe correction:** leave the frozen counter untouched in this seat. L1 should record the non-dispatch deltas and the false v4 receipt predicate rather than certify that every hunk is class dispatch. Repairing the predicate in an explicitly authorized future counter requires selecting the original predicate for v4 mode; strict v4 receipt compatibility additionally requires retaining its original receipt schema. Correct the header's provenance label as well: it says “Round-43 version 4 header follows” but immediately shows the Round-42 v3 header. Additive receipt fields and a changed default are compatibility tradeoffs, not a zero-harm equivalence proof; their disposition belongs to the canonical Rust judge, not this critic. No correction was applied.

## Every diff hunk

Old coordinates refer to `master:.ufo/waves/round-43/c43_count_v4.py`; new coordinates refer to `.ufo/waves/round-44/c44_count_v5.py`.

| # | Exact hunk header | Changed authority/path | Classification against the named attack |
|---|---|---|---|
| 1 | `@@ -1,10 +1,14 @@` | Module docstring/version/provenance | Not dispatch. No executable v4 case change. The claimed following v4 header is actually the retained v3 header. |
| 2 | `@@ -75,9 +79,9 @@` | Shared `PREDICATE` | **Harm under the item's rule.** Executed/read by v4 receipt construction; incorrectly names ten class runs in v4 mode. |
| 3 | `@@ -91,6 +95,20 @@` | `CLASS_DIR`, ordered G1–G10 module registry | Class-run wiring only; no edits to existing generator bodies. The declarations exist in both modes, without consuming the RNG. |
| 4 | `@@ -115,6 +133,27 @@` | New `load_classes(root)` | Class loader only; called only when `a.classes == "v5"`. No v4 body change. |
| 5 | `@@ -947,6 +986,9 @@` | Shared argument parser; new `--classes`, default `v5` | **Shared v4-entry/CLI change, not solely dispatch.** Explicit v4 is available, but omitted-option legacy invocations now select the new mode. |
| 6 | `@@ -954,7 +996,10 @@` | Shared receipt dictionary | **Harm under the item's rule.** v4 receipts gain `classesMode: "v4"` and `classRuns: []`; the unconditional predicate is still the v5 wording. |
| 7 | `@@ -998,9 +1043,11 @@` | Shared run-list construction around A–F and T1–T5 | **Touches the legacy run-list code.** Adds conditional loading and G insertion between F and T1; under explicit v4 the resulting eleven-run order is unchanged. This is dispatch-related, but the literal “nothing in runs A–F/T1–T5” condition is false. |
| 8 | `@@ -1013,6 +1060,9 @@` | Shared dispatcher between F and T4 | Class-run dispatch only: adds `elif key in classes` and reuses `layout_f`. In v4 the test is false; existing F/T4 bodies and `layout_f` itself are unchanged. |

There are no hunks between the new loader and `main()`: all existing generation, layout, timing-shape, and sandbox implementations in that interval remain unchanged in this comparison. There are also no hunks in the subsequent comparison/timing/final-decision code.

## Exact commands and decisive output

All shell commands ran with cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`.

```sh
mkdir -p /fast/scratch/hyaku/kake-r44/CriticHarmGuard
```

Exit 0; no output.

```sh
git show master:.ufo/waves/round-43/c43_count_v4.py | tee /fast/scratch/hyaku/kake-r44/CriticHarmGuard/master-c43_count_v4.py
```

Exit 0. The complete extracted source was printed and saved in the named scratch file. Its fingerprint is included below.

```sh
diff -u /fast/scratch/hyaku/kake-r44/CriticHarmGuard/master-c43_count_v4.py .ufo/waves/round-44/c44_count_v5.py
```

Exit **1** (differences found, not a command failure). The following is the complete verbatim raw diff, recovered from the tool's raw-output artifact rather than its abbreviated display:

```diff
--- /fast/scratch/hyaku/kake-r44/CriticHarmGuard/master-c43_count_v4.py	2026-10-23 23:00:51.642295636 -0300
+++ .ufo/waves/round-44/c44_count_v5.py	2026-10-23 19:34:56.712660369 -0300
@@ -1,10 +1,14 @@
 #!/usr/bin/env python3
-"""Round-43 C1 counter, version 4 (frozen before any seat scores; built from the round-42
-counter version 3, sha256 ce2d5a0c..., by .ufo/waves/round-43/build_v4.py). Adds run F and the
-timing-shape repetition classes of the round-42 lesson Mistake-5 fix criteria: 6+-digit ports
-and repetition classes (case-fold pairs, shared-prefix pairs, repeated hosts, common-host
-tables). The predicate sentence, ratio limit, reps, sandbox and scoring protocol are unchanged
-from version 3. Round-42 version 3 header follows for provenance:
+"""Round-44 C1 counter, version 5 (frozen before any control is scored; built from the round-43
+counter v4, sha256 1c3b9661..., by .ufo/waves/round-44/build_v5.py). Version 5 keeps the v4
+predicate, ratio limit, reps, sandbox, runner and scoring protocol, and appends ten class runs
+G1-G10 generated by the class modules under .ufo/waves/round-44/classes/ (each exposes
+`cases(rng, h)` in the run-F unit vocabulary). The class runs close the round-43 routed generator
+blind spots: 6+-digit ports paired with grammar defects, explicit default ports, empty paths,
+port-dropped scope comparison, shared-prefix cuts of 45/48/64 code points, non-degenerate and
+non-ASCII case-fold pairs, the three repetition guard bands, host tables outside the v4 host
+population, port-digit caches, and head/tail windows over long ports.
+Round-43 version 4 header follows for provenance:
 
 Round-42 C1 counter, version 3 (pre-freeze redesign of version 2, sha256 01d3fb8d...: adds run E, every
 ASCII character, percent form and boundary code point inserted in each of eleven URL slots, after wave-1
@@ -75,9 +79,9 @@
 import sys
 import tempfile
 
-PREDICATE = ("met: the tool's exit code and output equal the round-41 tool's on every generated run, "
-             "and its median CPU time on each of the five timing shapes is at most 2.0 times the "
-             "round-40 tool's")
+PREDICATE = ("met: the tool's exit code and output equal the round-41 tool's on every generated "
+             "run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the "
+             "five timing shapes is at most 2.0 times the round-40 tool's")
 RATIO_LIMIT = 2.0
 REPS = 5
 TOOL_PATH = "scripts/sitemap_audit.py"
@@ -91,6 +95,20 @@
 OUT_CAP = 256 * 1024 * 1024
 AS_CAP = 4 * 1024 * 1024 * 1024
 
+CLASS_DIR = ".ufo/waves/round-44/classes"
+CLASS_MODULES = (
+    ("G1", "g1_longport_grammar.py"),
+    ("G2", "g2_default_port.py"),
+    ("G3", "g3_empty_path.py"),
+    ("G4", "g4_port_scope.py"),
+    ("G5", "g5_prefix_cut_45plus.py"),
+    ("G6", "g6_fold_pairs.py"),
+    ("G7", "g7_band_memos.py"),
+    ("G8", "g8_host_tables.py"),
+    ("G9", "g9_port_digits.py"),
+    ("G10", "g10_headtail_windows.py"),
+)
+
 COMPONENTS = ("userinfo", "host", "port", "path", "query", "fragment")
 LOC_UNITS = [chr(9), chr(10), chr(13)] + [chr(c) for c in range(0x20, 0x80)]
 URL_UNITS = [chr(c) for c in range(0x00, 0x80)]
@@ -115,6 +133,27 @@
     pass
 
 
+def load_classes(root):
+    """Load the ten class modules; every one is required in v5 mode."""
+    import importlib.util
+    here = sys.modules[__name__]
+    base = os.path.join(root, CLASS_DIR)
+    out = {}
+    for key, fname in CLASS_MODULES:
+        path = os.path.join(base, fname)
+        if not os.path.isfile(path):
+            raise CannotEvaluate("class module missing: %s" % fname)
+        spec = importlib.util.spec_from_file_location("kake44_%s" % key.lower(), path)
+        mod = importlib.util.module_from_spec(spec)
+        spec.loader.exec_module(mod)
+        if not hasattr(mod, "cases"):
+            raise CannotEvaluate("class module has no cases(): %s" % fname)
+        out[key] = mod
+    return out
+
+
+
+
 def git(root, *args):
     return subprocess.run(["git", "-C", root, *args], check=True, capture_output=True,
                           stdin=subprocess.DEVNULL).stdout
@@ -947,6 +986,9 @@
     src.add_argument("--tool-file")
     ap.add_argument("--label", default="")
     ap.add_argument("--seed", type=int)
+    ap.add_argument("--classes", choices=("v5", "v4"), default="v5",
+                    help="v5 = the eleven v4 runs plus the ten class runs; v4 = the v4 corpus only "
+                         "(the round-44 skip-work control)")
     ap.add_argument("--out")
     a = ap.parse_args()
     root = os.path.abspath(a.root)
@@ -954,7 +996,10 @@
     rec = {"predicate": PREDICATE, "met": False, "ratioLimit": RATIO_LIMIT, "reps": REPS,
            "revision": None, "toolFile": a.tool_file, "label": a.label, "seed": seed,
            "counterSha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
-           "ref41Sha256": REF41_SHA, "base40Sha256": BASE40_SHA, "toolSha256": None,
+           "ref41Sha256": REF41_SHA, "base40Sha256": BASE40_SHA,
+           "classesMode": a.classes,
+           "classRuns": [key for key, _ in CLASS_MODULES] if a.classes == "v5" else [],
+           "toolSha256": None,
            "equalRuns": None, "equalValues": None, "runs": {}, "ratios": {}, "ratiosExact": {}, "note": None}
 
     def finish(code):
@@ -998,9 +1043,11 @@
                 with open(paths[key], "wb") as fh:
                     fh.write(data)
             box = Sandbox(rng, td)
+            classes = load_classes(root) if a.classes == "v5" else {}
             runs = [("A", cases_a), ("B", cases_b), ("C", cases_c), ("D", cases_d), ("E", cases_e),
-                    ("F", None),
-                    ("T1", shape_t1), ("T2", shape_t2), ("T3", shape_t3), ("T4", None), ("T5", shape_t5)]
+                    ("F", None)]
+            runs += [(key, None) for key, _ in CLASS_MODULES if key in classes]
+            runs += [("T1", shape_t1), ("T2", shape_t2), ("T3", shape_t3), ("T4", None), ("T5", shape_t5)]
             equal = 0
             values = 0
             for key, gen in runs:
@@ -1013,6 +1060,9 @@
                 elif key == "F":
                     units, n = cases_f(rng)
                     mname = layout_f(rng, units, cd)
+                elif key in classes:
+                    units, n = classes[key].cases(rng, sys.modules[__name__])
+                    mname = layout_f(rng, units, cd)
                 elif key == "T4":
                     mname = shape_t4(root, cd, rng)
                     n = None
```

```sh
sha256sum /fast/scratch/hyaku/kake-r44/CriticHarmGuard/master-c43_count_v4.py .ufo/waves/round-44/c44_count_v5.py
```

Exit 0; verbatim output:

```text
1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab  /fast/scratch/hyaku/kake-r44/CriticHarmGuard/master-c43_count_v4.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
```

Additional evidence was read with the `read` tool: `.ufo/waves/round-44/c44_count_v5.py:1-160` and `:981-1140`; the complete raw diff was read from `artifact://1291:raw:1-240`. Required godspeed/shokunin skill and linked protocol material were read; their artifact content did not alter this seat's assignment or write bounds.

## Files written, unrun checks, blockers

Files written (complete list):

1. `/fast/scratch/hyaku/kake-r44/CriticHarmGuard/master-c43_count_v4.py` — exact `git show master:...` extraction.
2. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w2/CriticHarmGuard.md` — this report, including the complete decisive diff.

Created directory: `/fast/scratch/hyaku/kake-r44/CriticHarmGuard/`.

No lane source, class module, frozen counter, receipt, ledger, or history was edited. No commits/pushes, tool installs/updates, or alternate runtime invocations were performed. No build/test/lint/formatter, counter execution, C1 audit, canary run, or C2 ledger check was run by this seat; all are **unrun**, not claimed passing. No blockers.
