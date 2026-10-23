# w2 seat report — RevengerLineage

Axes: operability, freshness. Item: reverse-engineer the freeze lineage — run
`build_v5.py --check`, independently verify what it compares, diff the ten
class modules against `classes-placebo/`, confirm placebo sha256.

## Verdict

**PASS.** No undeclared capability found. Three findings, none of which is a
smuggled capability; one is named for L1 adjudication because the item's
literal wording ("ONLY differences inside cases()") is stricter than observed:

1. **[NAMED, INERT] Class-vs-placebo diffs are not literally confined to
   `cases()`.** Each pair differs in three places: (a) the module docstring,
   (b) private `_`-prefixed helper functions / uppercase constants used only by
   `cases()`, (c) the `cases()` body itself. The placebo `cases()` is
   `return h.cases_f(rng)`. The docstring is a string literal and the helpers
   are dead code unless `cases()` calls them, so there is no executable
   capability outside the `cases()` call chain — but a literal reading of the
   item is violated by (a) and (b).
2. **[INERT] `classes/__pycache__/` holds 9 fresh `cpython-314` pycs** (g3's is
   stale-but-ignored; g9 has none). All validating caches are byte-identical to
   a fresh compile of the current source, so even `-B` runs (which skip writing
   but not reading caches) execute source-equivalent code.
3. `--check` is purely textual on `c44_count_v5.py`; it does not cover
   `classes/` or the placebo. That is a scope note, not a failure.

## What --check compares (read from build_v5.py, lines 140–149)

`SRC = .ufo/waves/round-43/c43_count_v4.py`, `OUT = c44_count_v5.py`. `build()`
applies 8 anchored (OLD→NEW) replacements — each guarded by
`text.count(old) != 1 → sys.exit("anchor not unique …")` — plus a final
`replace('"""Round-43 C1 counter', '"""Round-44 C1 counter', 1)`. `--check`
prints `sha256(cur)` and `sha256(built)` and exits 0 iff `cur == text` byte
equality. It never writes.

### Command

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 -B .ufo/waves/round-44/build_v5.py --check; echo "EXIT=$?"
```

### Verbatim output

```
current sha256: 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
built   sha256: 5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc
EXIT=0
```

### Independent verification

```
$ sha256sum .ufo/waves/round-44/c44_count_v5.py .ufo/waves/round-43/c43_count_v4.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
1c3b96610873301b1ea17d123677dd76a86f77edf26020c1ff5ef38221fe8eab  .ufo/waves/round-43/c43_count_v4.py
```

- OUT hash equals both printed lines (tool output corroborated outside the tool).
- SRC hash `1c3b9661…` matches the provenance stated in NEW_HEAD
  ("built from the round-43 counter v4, sha256 1c3b9661…").
- v4→v5 delta is exactly the 8 declared replacements — one hunk each:

```
$ diff -u .ufo/waves/round-43/c43_count_v4.py .ufo/waves/round-44/c44_count_v5.py | grep -n '^@@'
3:@@ -1,10 +1,14 @@        # OLD_HEAD -> NEW_HEAD
24:@@ -75,9 +79,9 @@       # OLD_PRED -> NEW_PRED
37:@@ -91,6 +95,20 @@      # CONST_ANCHOR -> CONST_ADD (CLASS_DIR/CLASS_MODULES)
58:@@ -115,6 +133,27 @@    # LOADER before git()
86:@@ -947,6 +986,9 @@     # MAIN_OLD -> MAIN_NEW (runs list)
96:@@ -954,7 +996,10 @@    # BRANCH_OLD -> BRANCH_NEW (class-run branch)
108:@@ -998,9 +1043,11 @@  # ARGS_OLD -> ARGS_NEW (--classes)
122:@@ -1013,6 +1060,9 @@  # REC_OLD -> REC_NEW (record fields)
```

Nothing else differs between v4 and v5: the builder cannot have smuggled an
undeclared edit into the frozen counter.

## Class-vs-placebo diffs (the named attack: undeclared capability in the freeze)

Method: `diff -u` per pair (all ten: `diffexit=1`, exactly ONE hunk, each
starting at `@@ -1,` → identical tails), then an AST audit
(`audit_classes.py`, scratch) asserting per module:

- placebo = docstring + a single `cases(rng, h)` whose body is
  `return h.cases_f(rng)` — held for all ten;
- real module top level = only docstring, `Assign` to plain `Name`s, `def`;
- zero `Import`/`ImportFrom` anywhere;
- helpers all `_`-private, exactly one `cases`, signature `(rng, h)`;
- no calls to `setattr/delattr/exec/eval/compile/open/__import__/globals/
  locals/vars/breakpoint`; no writes to `h.*`; no dunder access on `h`
  (`h` is the counter module itself, passed as `sys.modules[__name__]`, so
  `h`-mutation was the live smuggling vector — none found).

### Verbatim output

```
VERDICT: CLEAN — no capability outside cases()+its private helpers
AUDIT_EXIT=0
```

Per-file diff shape (all ten identical pattern, g1→g10): placebo 5-line
docstring + 2-line delegating `cases()` replaced by real docstring + private
helpers/constants + real `cases()`. Both dirs contain exactly the ten `gN_*.py`
files (`classes/` additionally has `__pycache__/`).

## Placebo sha256

```
$ sha256sum .ufo/waves/round-44/c44_placebo.py
9ce3acd4c4c72de0b3c26a31bd1101307b71b2174100eb260b8b04fa5fc77a27  .ufo/waves/round-44/c44_placebo.py
```

Matches the required value exactly.

## Bonus falsification: pyc cache poison check

`-B` sets `sys.dont_write_bytecode` (writing off, reading still on), so a forged pyc with a matching source
mtime/size header would execute instead of the source even under `-B`. Checked all ten:

```
g10: header_validates=True structural_diffs=none -> WOULD LOAD CACHED; bytecode==
g1:  header_validates=True structural_diffs=none -> WOULD LOAD CACHED; bytecode==
g2:  header_validates=True structural_diffs=none -> WOULD LOAD CACHED; bytecode==
g3:  header_validates=False structural_diffs=[...] -> header mismatch -> recompiles from source; cached ignored
g4:  header_validates=True structural_diffs=none -> WOULD LOAD CACHED; bytecode==
g5:  header_validates=True structural_diffs=none -> WOULD LOAD CACHED; bytecode==
g6:  header_validates=True structural_diffs=none -> WOULD LOAD CACHED; bytecode==
g7:  header_validates=True structural_diffs=none -> WOULD LOAD CACHED; bytecode==
g8:  header_validates=True structural_diffs=none -> WOULD LOAD CACHED; bytecode==
g9:  no cached pyc -> always compiled from source. SAFE
FINAL: CLEAN — no pyc forgery
```

g3's cache is stale (source edited 20:11:11.856, cache written 20:11:11.608);
its header fails validation, so CPython recompiles from source — benign. An
earlier raw `marshal.dumps` comparison flagged g1; recursive field-by-field
code comparison shows all validating caches are semantically identical to their
sources (the g1 flag was a marshal interning artifact).

## Files written

- `/fast/scratch/hyaku/kake-r44/RevengerLineage/class-diffs.txt` (674 lines, ten unified diffs)
- `/fast/scratch/hyaku/kake-r44/RevengerLineage/audit_classes.py` (AST audit)
- this report.

## Blockers / unrun checks

None. All checks run. Tool installs: none needed.
