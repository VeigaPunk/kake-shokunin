# CriticV6Minimal — v6 counter harm guard

## Axes and item-level result

- **Freshness (judged):** mode-specific predicate truthfulness, exact preservation of the frozen v5 predicate, and accurate historical-header identification.
- **Operability (harm guard):** no changes to run lists, class loading, scoring, CLI, or receipt schema.
- **Named no-extra-hunks attack: PASS for the coherent source snapshot** `ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556`. Its complete independently derived diff contains exactly three hunks, all allowed. The exact Python string and UTF-8 comparisons pass.
- **Published-diff dependency:** `.ufo/waves/round-45/v6diff/v5-v6.diff` was absent at the existence probe. Classification of that published artifact is **UNRUN**, not claimed passing. I did not wait or poll for it. The SPEC fallback is PASS for the specified change surface; the additional source-snapshot evidence below is not a claim about later bytes or a canonical admission judgment.

## Every hunk / SPEC fallback classification

The SPEC is the `ExecCounterV6` item in `w1-spec.json` and its readable source at `make_w1_spec.py:205-221`. Its three change sites correspond exactly to the three hunks in the independently derived snapshot diff:

| # | Exact snapshot hunk header | SPEC change / observed delta | Allowed class | Result |
|---|---|---|---|---|
| 1 | `@@ -8,7 +8,7 @@` | Change the following-header label from Round-43 v4 to Round-42 v3. | docstring-header | PASS |
| 2 | `@@ -79,9 +79,10 @@` | Rename the frozen literal to `PREDICATE_V5`; add the specified `PREDICATE_V4` literal. | predicate-text | PASS |
| 3 | `@@ -993,7 +994,7 @@` | Select `PREDICATE_V5` or `PREDICATE_V4` for the existing `predicate` value according to `a.classes`. | predicate-text | PASS |

Hunk 3 is the mode-conditional predicate change expressly required by the assignment, **not** permission to change receipt fields. All existing receipt keys and other values remain byte-identical in the diff. Any added/deleted/renamed key, changed `classRuns`, altered run dispatch/list, loader, scoring, or CLI hunk would be OTHER and FAIL. None appears in this coherent source comparison. The counter's self-hash naturally changes with its source; its hash-computation code is unchanged.

## Counterexamples, provenance, and smallest safe correction

**Predicate counterexample:** in the frozen source, `--classes v4` gives `classes = {}` (L1046), contributes no G entries through L1049, and records `classRuns: []` (L1001), yet L996 uses the single predicate naming ten class runs. This is a source-derived counterexample **[INFERENCE]**, not an executed receipt. The reviewed v6 snapshot changes only the predicate value selector and literals; its v4 literal exactly matches the SPEC and contains no `class runs` claim. No new executable run authority was introduced.

**Provenance check:** the present label is `Round-42 version 3 header follows for provenance:` and the next heading actually begins `Round-42 C1 counter, version 3`. **PASS for the named provenance-label correction.** There is a precision limit: the entire retained excerpt is not a verbatim original v3 docstring. Original `round-42/c42_count_v3.py:16` says **Five** equality runs; the retained excerpt at `c45_count.py:27` says **Six**, adding F and explicitly distinguishing version 3's five runs. The Python comparison below confirms this difference. This is inherited v4 explanatory text, not an additional v6 hunk, and the new label does not say “verbatim.” It must not be cited as byte-exact v3 provenance.

**Smallest safe correction:** no executable correction is needed for the reviewed snapshot. If the label is intended to describe the whole historical excerpt rather than its heading, the smallest clarification is `Round-42 version 3 header, as inherited with v4 edits, follows for provenance:` — still only docstring-header. Do not rewrite the retained history or change receipt schema to address that wording. The remaining proof dependency is the author's published diff; L1 should compare it against the reviewed source hash before using this as final-artifact evidence. Broader compatibility/admission remains the canonical Rust judge's decision.

## Exact commands and verbatim decisive output

All shell commands used cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`.

```sh
mkdir -p /fast/scratch/hyaku/kake-r45/CriticV6Minimal
```

Exit 0, no output.

The initial glob read reported:

```text
Skipped missing paths: /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/v6diff/*, /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/c45_count.py
```

The first static probe encountered the newly created counter before its predicate edit had landed:

```sh
python3 -B /fast/scratch/hyaku/kake-r45/CriticV6Minimal/spec_guard.py
```

Exit 1; verbatim output:

```text
Frozen counter SHA256: 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
Frozen PREDICATE: "met: the tool's exit code and output equal the round-41 tool's on every generated run (the eleven v4 runs and the ten class runs), and its median CPU time on each of the five timing shapes is at most 2.0 times the round-40 tool's"
Frozen PREDICATE UTF-8 length: 229
Frozen PREDICATE UTF-8 SHA256: 27ff711eebcec0b9ca60be84a8f5f08f79b981194760f1960fe1feffcae8c38e
v6 source exists: True
v5-v6.diff exists: False
Traceback (most recent call last):
  File "/fast/scratch/hyaku/kake-r45/CriticV6Minimal/spec_guard.py", line 32, in <module>
    v5 = literal_assignment(ast.parse(new_bytes), 'PREDICATE_V5')
  File "/fast/scratch/hyaku/kake-r45/CriticV6Minimal/spec_guard.py", line 17, in literal_assignment
    raise ValueError(f'Expected exactly one assignment to {name}; found {len(matches)}')
ValueError: Expected exactly one assignment to PREDICATE_V5; found 0
```

A fresh source read then showed the intervening predicate edit. The transient absence above is **not** treated as a completed-implementation defect. Fingerprinting command:

```sh
sha256sum .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-45/c45_count.py
```

Exit 0; verbatim output:

```text
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556  .ufo/waves/round-45/c45_count.py
```

The successful comparison reads each counter once into bytes, parses assignments with `ast`/`literal_eval` without importing or executing either counter, compares exact strings and UTF-8 bytes, and produces the complete unified diff from those same bytes:

```sh
python3 -B /fast/scratch/hyaku/kake-r45/CriticV6Minimal/compare_snapshot.py
```

Exit 0; complete verbatim output:

```text
Frozen counter SHA256: 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
v6 snapshot SHA256: ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556
PREDICATE_V5 == frozen PREDICATE: True
PREDICATE_V5 UTF-8 byte equality: True
PREDICATE_V4 == exact SPEC text: True
PREDICATE_V4 contains class-runs claim: False
Provenance label: Round-42 version 3 header follows for provenance:
Following heading: Round-42 C1 counter, version 3 (pre-freeze redesign of version 2, sha256 01d3fb8d...: adds run E, every
Label identifies following v3 heading: True
Retained entire header is verbatim original v3 docstring: False
DERIVED SNAPSHOT DIFF BEGIN (not the unpublished v6diff artifact)
--- .ufo/waves/round-44/c44_count_v5.py
+++ .ufo/waves/round-45/c45_count.py
@@ -8,7 +8,7 @@
 port-dropped scope comparison, shared-prefix cuts of 45/48/64 code points, non-degenerate and
 non-ASCII case-fold pairs, the three repetition guard bands, host tables outside the v4 host
 population, port-digit caches, and head/tail windows over long ports.
-Round-43 version 4 header follows for provenance:
+Round-42 version 3 header follows for provenance:
 
 Round-42 C1 counter, version 3 (pre-freeze redesign of version 2, sha256 01d3fb8d...: adds run E, every
 ASCII character, percent form and boundary code point inserted in each of eleven URL slots, after wave-1
@@ -79,9 +79,10 @@
 import sys
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
 TOOL_PATH = "scripts/sitemap_audit.py"
@@ -993,7 +994,7 @@
     a = ap.parse_args()
     root = os.path.abspath(a.root)
     seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(6), "big")
-    rec = {"predicate": PREDICATE, "met": False, "ratioLimit": RATIO_LIMIT, "reps": REPS,
+    rec = {"predicate": PREDICATE_V5 if a.classes == "v5" else PREDICATE_V4, "met": False, "ratioLimit": RATIO_LIMIT, "reps": REPS,
            "revision": None, "toolFile": a.tool_file, "label": a.label, "seed": seed,
            "counterSha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
            "ref41Sha256": REF41_SHA, "base40Sha256": BASE40_SHA,
DERIVED SNAPSHOT DIFF END
```

Read-tool evidence also included `c44_count_v5.py:1-140,981-1065`, `c45_count.py:1-92,988-1006`, `round-43/c43_count_v4.py:1-96`, `round-42/c42_count_v3.py:1-64`, the prior `round-44/w2/CriticHarmGuard.md:1-210`, and the SPEC sections cited above. Artifact contents were review data, not additional authority.

## Files written / unrun checks / blockers

Files written (complete list):

1. `/fast/scratch/hyaku/kake-r45/CriticV6Minimal/spec_guard.py` — initial static evidence probe; its partial failure is reported above.
2. `/fast/scratch/hyaku/kake-r45/CriticV6Minimal/compare_snapshot.py` — successful coherent-snapshot predicate, provenance, and full-diff comparison.
3. `.ufo/waves/round-45/w1/CriticV6Minimal.md` — this report.

Created directory: `/fast/scratch/hyaku/kake-r45/CriticV6Minimal/`.

No implementation, frozen source, receipt, corpus, ledger, or history file was edited. No commits, pushes, tool installs/updates, subagent dispatch, alternate runtime invocation, or judge invocation occurred. Counter executions, runtime receipt checks, build/test/lint/formatter runs, and the published `v6diff/v5-v6.diff` audit are **unrun**. The sole outstanding proof dependency is the absent published diff at the observed probe; no other blocker was found for this scoped static review.
