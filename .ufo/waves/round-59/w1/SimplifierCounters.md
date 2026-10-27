# SimplifierCounters

Scope: three counters + two derive scripts. Anchors are the frozen HEAD blobs at
`cb685273cc9e331b51f45485793d5d1c91184b3a` (`c59_axis_evidence.py` 317, `c59_resolver_cases.py` 350,
`c59_quote_truth.py` 735, `derive_c59_resolver_cases.py` 194, `derive_c59_quote_truth.py` 301 lines). The worktree is
live (`c59_axis_evidence.py` +88/−28, `c59_quote_truth.py` +9/−7 by other seats), so worktree lines shift by +1/+2;
no hunk below overlaps an in-flight version-2 hunk (checked against `git diff` at read time).

Method. No `lsp`/language-server device answers in this session (unavailable — recorded); semantic callers were
proven by (a) repo-wide importer search, (b) module-load analysis (`span_tools.py` loads `c59_quote_truth.py` and
touches only `NEW_ROWS`, `units`, `in_content`, `text_segments`, `UNIT_CEILING`, `CHAR_CEILING`, `re`), (c) the
constancy of the value gating a branch, and (d) pre/post differentials. Tool: `vulture 2.16` (`uv tool`, already
installed; channel `uv tool`, reason: independent dead-code scan).

Evidence (scratch `/fast/scratch/hyaku/kake-r59/SimplifierCounters`, deleted at exit):
- vulture, five HEAD blobs: `c59_quote_truth.py:57 shutil`, `:60 tempfile`, `:61 timezone` (unused imports, 90%),
  `c59_resolver_cases.py:295 BASE_REV` (60%); nothing else but the argparse `error` override and two unpack fields.
- quote_truth P1–P5 patch: `--json` byte-identical to the original at `fd6303ce` (exit 1) and `cb685271` (exit 2),
  all nine checks and every note equal.
- quote_truth C8, two throwaway repos (commits `-c user.name=selftest`): mirror/append pair with (a) an untouched
  pre-existing used-by cell → C8 pass, notes `[]`; (b) an edited used-by cell → C8 fail with exactly
  `append-only: measured registry minus new rows, used-by restored, != mirror bytes`. Original and patched agree
  in both — the deleted "restore" path never rescued anything and never will.
- resolver P8–P9 patch: 21 cases against `fd6303ce`, seed 42, original vs patched, frozen `gate` fixture identity
  replaced by `selftest` in *both* harnesses → `13/21`, `EXIT=1` both; only diff lines are random fixture commit
  ids (K13) and the scratch path in P5's note. Byte-identical fixture trees for `lane()` (K1 shape) and for
  `write()` vs `put()` on `a"b.md`, `line\nbreak.md`, `中文.md`; `fixture_ids(20)` equal at `SEED=42`.
- Not run: the 21 cases under the frozen `gate` identity (my seat bounds commit only as `selftest`), and no
  after-state scoring anywhere — these are proposals, not a measured version 2.

## PROPOSALS:

**P1 `c59_quote_truth.py:57,60,61` — three imports nothing reads** (round-58 residue: `shutil`/`tempfile` came
with `--work` handling, `timezone` with the pre-ISO parse; each name occurs once, the import itself).
`import shutil` and `import tempfile` go; `from datetime import datetime, timezone` becomes `... datetime`.
Preserved: no other reference to the three names; `datetime` stays.

**P2 `c59_quote_truth.py:83` + `:583-595` — `PRIOR_USED_BY` is `{}` at freeze and nothing rebinds it**, so the
`restored` "used-by restore" branch is unreachable and `mlines` exists only to feed it. Round-58's live reader was
C4 (`want = PRIOR_USED_BY.get(sid, []) + [path]`), which the derivation replaced with `USED_BY[sid]`; the C8 branch
was already dead in round 58 (`c58_quote_truth.py:81` is also `{}`).
```diff
@@ -81,5 +79,4 @@
 NEW_ROWS = ("S425", "S426")
-PRIOR_USED_BY: dict = {}
 USED_BY = {
@@ -581,15 +570,6 @@
-            restored = []
-            mlines = row_lines(mirror_text)
-            for line in (registry_text or "").split("\n"):
-                m = re.match(ROW_RE % r"S[0-9]{3,}", line)
-                sid = m.group(1) if m else None
-                if sid in NEW_ROWS:
-                    continue
-                if sid in PRIOR_USED_BY and sid in mlines:
-                    mrow = [c.strip() for c in mlines[sid].strip().strip("|").split("|")]
-                    line = set_used_by(line, mrow[10])
-                restored.append(line)
+            restored = [ln for ln in (registry_text or "").split("\n")
+                        if not (m := re.match(ROW_RE % r"S[0-9]{3,}", ln)) or m.group(1) not in NEW_ROWS]
```
Preserved: with the map empty the guard is always false, so `restored` was always "every line whose id is not a new
row"; the comprehension keeps those lines, in order, including the trailing empty string, so the byte comparison
`"\n".join(restored).rstrip("\n") != mirror_text.rstrip("\n")` and the newline-suffix test are untouched — proven
by the two-repo differential (pass passes, edited fails with the same note). No check is lost: an append that edits
a pre-existing row still fails C8. `row_lines()` (`:159-172`) dies with it **if** P6 stays empty.

**P3 `c59_quote_truth.py:336-346` — the C3 "not a new row" branch cannot run**: the loop is `for sid in ADOPTED`
and `ADOPTED`'s keys are exactly `NEW_ROWS`, so `sid in NEW_ROWS` is a tautology and the `else` (base-row diff) is
unreachable — the docstring already states both rows are new.
The ten lines `if sid in NEW_ROWS: (… in base_rows …) else: (base diff)` collapse to
`if sid in base_rows: c3.append(f"{sid}: already in the base registry; not a new row")`.
Preserved: for both adopted ids the removed `else` was dead, so the append list is identical. Tradeoff: a later
round adopting an existing row must re-add the five lines; C8's byte comparison already covers an edited row.

**P4 `c59_quote_truth.py:391` — tautological guard** in the same `for sid in ADOPTED` loop (C5):
`if sid in NEW_ROWS and row and len(row) > 5:` → `if row and len(row) > 5:`. Preserved: the removed conjunct is
true for every adopted id.

**P5 `c59_quote_truth.py:398,406` — a copy read once, re-solving the same comprehension C9 writes inline**
(`others = [... texts.items() ...]`): delete `all_texts = dict(texts)` and read `texts.items()` directly.
Preserved: `texts` is not mutated between copy and read; dict-copy iteration order equals the original's.

**P6 `c59_quote_truth.py:159-172` — `row_lines()`** reader evidence: only `:583/:587` (the branch P2 deletes) and
its `def`; round-58's selftest mutates `MIRROR` bytes directly (`c58:931`), no call. Delete unless the in-flight C3
selftest port registers a caller; vulture flags it unused once P2 lands.

**P7 `c59_quote_truth.py` (v2 text, optional, coordination-gated)** — the "what is a text node" pair (strip
style/script, then `>([^<>]+)(?=<)`) now exists twice: in `text_segments()` and inline in the C5 printed-revision
check added by the version-2 hardening. One helper, one authority:
`text_segments` keeps only `return text_nodes(text[win[0]:win[1]])`; new helper
`def text_nodes(text): return re.findall(r">([^<>]+)(?=<)", re.sub(r"(?is)<(style|script)\b.*?</\1>", "<>", text))`;
C5's inline pair becomes `text_nodes(texts[sid])`.
Preserved: same two regexes, same order on the same input; `text_segments` still slices the window first. Verified
byte-identical on the v2 snapshot (`sha256 7430841144fa12bc`) at `fd6303ce`. Tradeoff: +3 lines net; buys one
definition instead of two that drift. `article_headings` keeps its `(pre|code|script|style)` variant — different
strip set, do not merge.

**P8 `c59_resolver_cases.py:99-102` + 14 call sites — `lane()`'s `name` parameter is deleted on entry.**
```diff
-def lane(work: str, name: str, reg: str, knowledge: dict[str, str], siblings: dict[str, str | None] | None = None,
+def lane(work: str, reg: str, knowledge: dict[str, str], siblings: dict[str, str | None] | None = None,
          git_lane: bool = False) -> tuple[str, str, str | None]:
-    del name
```
Call sites `lane(work, "k1", ` … `lane(work, "p5", ` (K1–K9, P1–P5): drop the literal. Preserved: `del name`
proves no read after entry, every call is positional, no `name=` keyword exists (only the unrelated
`user.name=gate` string at `:89`); K1-shape fixture trees byte-identical. Coordination: `ExecC2GateSelftest`'s
`_fixture_lane` calls `repo()`, not `lane()` — apply to the ported file.

**P9 `c59_resolver_cases.py:69-75` — second file writer**: `write()` duplicates `put()` (`:130`) minus bytes
support; on POSIX `utf-8` text with `newline=""` writes `put`'s exact bytes.
`write`'s four-line body (join, `makedirs`, `open(..., "w", encoding="utf-8", newline="")`, write) becomes
`put(base, rel, text)`.
Preserved: `put` creates the same parents (`exist_ok=True`) and writes `text.encode("utf-8")`; checked byte- and
name-identical on a tree with `a"b.md`, `line\nbreak.md`, `中文.md`, nested empty file. Callers (`repo`, `lane`) pass
`dict[str, str]`.

**P10 `c59_resolver_cases.py:262` — stale number**: comment says "floor 55" (round-58's constant) while
`P6_FLOOR = 66` (`:278`) and the docstring (`:19`) say 66. `floor 55` → `floor 66` in the comment. Doc-only.

**P11 `derive_c59_resolver_cases.py:6` — the derivation record is inconsistent with the source it reads**:
"P6 floor 59 -> 66 (one tool selftest case per new route)" while round-58's frozen constant is `55`
(`c58_resolver_cases.py:206`), i.e. 55+7 = 62. Three numbers (55, 59, 66) for one fact. The floor's *value* is
`CriticC2P6`'s remit, not mine: fix the record to whichever the L1 rules, then make P10 agree.

**P12 `derive_c59_quote_truth.py` CONSTS — generator twin of P2**: the recipe still emits
`PRIOR_USED_BY: dict = {{}}`, so a re-derivation reintroduces dead weight; delete that line (same argument as P2).

Micro (cosmetic, fold in with P8/P9 only): `c59_resolver_cases.py:140` `import random` inside `fixture_ids` and
`c59_quote_truth.py:627` `import difflib` inside C9 → stdlib blocks. No behaviour change (`fixture_ids(20)` verified
equal at a fixed seed).

## KEEP:

- **`set_used_by` (`c59_quote_truth.py:253-256`)** — unused in v1, but it is the fixture mutator of the round-58
  selftest (`c58:870,873,876,1143`, `dual(..., set_used_by(...))`), and `ExecC3SelftestPort` is porting exactly
  those C4 controls now. Deleting it would be re-added.
- **`BASE_REV` (`c59_resolver_cases.py:295`)** — dead in v1 (vulture 60%), but round-58's selftest read it in
  `_base_tool` (`c58:459-461,532` `git show {BASE_REV}:{TOOL}`) and the port is specified to bring `_base_tool` plus
  "the base tool at {BASE} = 13/21" (`make_spec_w1.py:158-159`). Live on landing; re-check after the port.
- **`NEW_ROWS`** (`span_tools.py:21` binds `IDS = qt.NEW_ROWS`) and **`pointers()`** (`make_spec_w1.py:418` invites
  a seat to import it) — published names, not redundant with `ADOPTED`.
- **`c59_axis_evidence.py` at HEAD: no deletion candidate survives the harm-none test.** vulture+read leave only
  `_P.error`, which argparse calls; `AXES/HELD/EXT/BARE/TALLY/LINEONLY` are all read, and the
  `outside = ... else text` fallback is reachable when the measured SCORECARD has no axis table.
- **Cross-file `clean_env`/`git`/`show` duplication** — consolidating adds a fourth file under the frozen wave dir
  and changes the contract's unit ("counter: `python3 -B <path>`"); costs more than the ~30 duplicated lines.
- **`ARTICLE_START`/`ARTICLE_END` per-row dicts** with equal values — frozen per-page container description;
  collapsing to scalars would encode "both pages share a container" as an assumption at three call sites.
- **`units()`/`CJK_RE`** — the CJK branch never fires on these two English bodies, but `units` is the contract's
  unit rule applied to registry cells, titles and anchors too; deleting the branch redefines the rule.
- **`env()` `PYTHONDONTWRITEBYTECODE` beside `-B`**, **unused unpack fields `rc` (`:597`) / `i2` (`:640`)**, and the
  **argparse `_P.error` override in all three counters** — deliberate or idiomatic; nothing to remove.
- **The derive scripts as artifacts** — one-shot generators, but they are this round's derivation provenance
  (`c59_*.py` docstrings cite them); P11/P12 correct their text, nothing is deleted.

## VERDICT:

12 proposals (P6 conditional on the C3 selftest port, P7 optional), 25 net deleted lines: `c59_quote_truth.py`
−20 (three dead imports, an unreachable C8 restore path and its helper, a tautological guard, a needless copy, an
unreachable C3 branch), `c59_resolver_cases.py` −4 (dead `lane` parameter, duplicated writer),
`derive_c59_quote_truth.py` −1 (generator twin); −22 if P7 lands. Each is proven inert by byte-identical output on
the real lane and on two-repo/two-harness fixtures; `set_used_by`, `BASE_REV`, `NEW_ROWS`, `pointers` stay because
wave-1 selftest ports are about to call them, and the axis counter has nothing worth deleting — no proposal harms
any axis.
VERDICT: propose 12 deletions/consolidations (25 net lines, differential-verified), keep 9 load-bearing or in-flight items.
