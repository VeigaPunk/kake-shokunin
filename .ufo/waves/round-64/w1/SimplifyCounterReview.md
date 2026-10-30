# SimplifyCounterReview — simplification review of the round-64 counters and fixture builder

Seat: SimplifyCounterReview (leaf; no subagents). Item: can
`c64_calibration.py` (449 lines), `c64_quote_tool.py` (~370), or
`fixtures/build_fixtures.py` (149) be materially smaller without losing any
frozen semantics? Concrete deletions with exact behavior preserved, or a
minimum certificate. No files edited; lane repo only read via
`git -C show/rev-parse/status`.

## Verdict

No material reduction is available. The three files are at their honest
minimum for semantics; the only provable simplifications are dead constants,
one dead output channel, one mechanical temp-file dance, and one factored
literal — together **−34 lines (−3.5 %)** across 972 lines. All were built as
prototypes under `/fast/scratch/hyaku/kake-r64/SimplifyCounterReview/` and
verified byte-identical against the committed originals on every reachable
input (see Evidence). Because any byte change alters the frozen instrument
shas in `contract.md`, none can land without a new freeze; they are evidence
that what remains is live code, not proof that it should ship unmodified.

Frozen-sha check (reproduced, `sha256sum` on the committed files):
`c64_calibration.py` = `5489eb2f…`, `c64_quote_tool.py` = `96fd64e9…`,
`build_fixtures.py` = `7fbd8cbc…`, `stub_tool.py` = `7c78a05d…` — all match
`contract.md`.

## Proven deletions (each verified, none applied)

### `c64_calibration.py` → 440 lines (−9)

1. **`MARKER_SPOT` (was lines 313–317)** — dead constant. An AST scan plus
   `grep` show zero references; it is the only module-level assigned-but-
   unread name in the file. Delete.
2. **`load_recipe` temp-file round-trip → in-memory exec** — the recipe is a
   pure-stdlib blob (`extract_text.py` has no `__file__` or sibling-import
   use; verified by `git show 1a481315:…/extract_text.py | grep import`).
   Replacing `spec_from_file_location` on a temp file with
   `exec(compile(blob, "extract_text.py", "exec"), types.ModuleType(…).__dict__)`
   is equivalent, and it also removes a real leak: the old code did
   `tempfile.mkdtemp("c64-t7-")` in the T7 selftest with no cleanup.
   Deletes the `work=` parameter, the `mkdtemp`/`shutil.rmtree` block in
   `evaluate`, and the `importlib.util` import (−9 lines net in that region).
   `met` output identical on all 7 inputs; selftest still 26/26 byte-identical.
3. **`text_at()` helper** — the `(git_show(...) or b"").decode("utf-8",
   errors="replace")` idiom appears 4× consecutively for KNOWLEDGE/QUALITY/
   LESSON/SOURCES. One one-line helper removes the quadruplication.
4. **Double-fetch of the spot blob in `run_selftest` (was lines 334–337)** —
   `git_show(root, BASE, SPOT_REL)` was called twice (once in the `any()`
   guard, once for `real_spot`). Hoist the fetch above the guard.

### `c64_quote_tool.py` → 361 lines (−13)

5. **`GARBAGE_TOOL` (was line 248)** — dead constant, zero references. Delete.
6. **`FIXTURE_RELS` literal → derived set** — the 6-path list duplicates the
   `raw`/`text` values already inside `FROZEN_CASES`. Replacing it with
   `sorted({p for c in FROZEN_CASES.values() for p in (c["raw"], c["text"])})`
   yields the identical set (verified by printing `m.FIXTURE_RELS` on the
   prototype — exact same 6 paths), removing a second authority that could
   drift. −7 lines net.
7. **`evaluate`'s `out` return channel is dead** — every one of its 9 return
   sites returned `…, ""`; `main` then did `if out: print(out)` on a string
   that was always empty. Changed signature `tuple[int, str] → int`, deleted
   `code, out = …; if out: print(out); return code` → `return evaluate(…)`.
   −3 lines net. (Contrast: `c64_calibration.evaluate` *does* use its `out`
   channel — keep.)
8. **`rederive_ok` clause 2 (was lines 219–220)** — `by_id.get(cid,
   {}).get("derived") not in (None, mine) → rederive_ok = False` cannot
   change `met`: `frozen_ok` already requires the tool's `derived ==
   spec["expected"]` and clause 1 requires `mine == spec["expected"]`, so
   clause 2 can only flip when `met` is already false on another term. Proved
   exhaustively: 18/18 per-case combinations enumerated
   (`passed ∈ {T,F,missing} × tool-derived ∈ {None,E,other} × mine ∈
   {E,other}`), zero counterexamples to `(frozen ∧ clause1) ⇒ clause2`.
   Removing it only narrows a diagnostic token in an already-false run; all
   committed receipts are identical.

### `fixtures/build_fixtures.py` → 137 lines (−12)

9. **`MARKER_SPOT` (was lines 45–50)** — dead constant, zero references.
   Delete.
10. **Planted-file dict → single `planted` literal** — the four-file
    knowledge/QUALITY/lesson/SOURCES dict was written out 3× identically
    (marker, fabrication, junk) plus once amended (fabrication's knowledge
    override). Factored to one `planted` dict; fabrication overrides the one
    key. All 4 output `HEAD^{tree}` hashes identical to the committed
    fixtures (see Evidence).

## What must NOT be deleted (examined, justified, kept)

- **Duplicated helpers across the two counters** (`sha256`, `git_show`,
  `classify`, `_fixture`, `_head`, `materialize`-ish): look like the obvious
  dedup win but the contract's §Separability requires each claim
  re-derivable alone — "C1 verifies on a tree where the tool or its counter
  never landed; C2's counter only reads the tool…". A shared module would be
  a third frozen file (more weight, not less) and would couple the claims.
  The duplication is intentional.
- **`ledger_row.get("locatedRawLines") != located` in c64 `evaluate`**: in
  reachable states this is redundant (the clause runs only when `pins=1`,
  which already forces the ledger blob to its pinned bytes, so the value is
  `"6150-6154"` by construction). However the contract's C1 wording
  *specifies* "equal the ledger's locatedRawLines and the pinned constant" —
  the ledger comparison is a stated semantic, not dead weight. Keep.
- **`LYING_TOOL`/`CRASH_TOOL` selftest branches (T3/T5)**: they exercise the
  same sha-mismatch branch as T2, but each is a distinct semantic witness
  that a hostile tool is never executed (the pin fires pre-exec). Shrinking
  the selftest 11→9 would also diverge from the committed `selftest-c2.txt`
  receipt. Keep.
- **`parse_ledger(blobs["ledger"] if pins else None)` gating** — looks
  odd (why parse the ledger only when pins pass?) but produces the
  observable `ledger_state=ledger_absent` token in the junk/ledger-mut
  receipts. Removing the guard changes committed output. Keep.
- **`section()` vs `correction_block()`** — distinct heading grammars
  (`## X` vs `[rN-correction`), both needed.
- **Docstrings (~45 lines each)** — contain the frozen predicate sentence
  that must be identical across contract/docstring/receipts; the remaining
  bulleted repair rationale is the counter's contract-facing provenance.
  Runtime-safe to trim, but it is load-bearing documentation; do not delete.
- **`disagreements`/`unresolved` masking, `max(…,0)`** — the unmasked
  `unresolved == 0` gate is the claim's own anti-masking mechanism.
- **`RUN_TIMEOUT`, `safe_json`, `materialize`, `env` isolation** — all reach
  live code paths.
- **`assert toplevel` in fixture/selftest repo builders** — required by the
  seat bounds themselves.

## Tradeoffs / observations

- `fixtures/build_fixtures.py` does **not** build `ledger-mut-repo`; the
  contract lists it under "Fixture revisions (built by
  `build_fixtures.py`…)" and `controls/fixture-builds.txt` prints only 4
  JSON lines, while `controls/control-ledger-mut.txt` describes it as
  `<marker-repo + ledger locatedRawLines mutated>`. I verified
  `ledger-mut-repo` exists at `5b981bd0` under `l1/fixtures/` and differs
  from marker-repo only in `quote-classes.json` — but in *three* ways, not
  one: `locatedRawLines` 6150-6154→6150-6156, the curly quote
  `’` re-escaped to `\u2019`, and the trailing newline dropped (it was
  re-serialized through JSON, not edited in place). The C1 ledger sha pin
  catches it anyway (`pin_drift=drift:ledger`), but the fixture is not
  reproducible from the committed builder and its description under-states
  the diff. Worth a follow-up (add a `ledger-mut-repo` arm or fix the
  contract wording), not a simplification.
- c64 selftest `MARKER_*` constants and builder `MARKER_*` constants
  deliberately differ in wording (the selftest's knowledge block lacks
  "without the frozen quote"); both produce `quote_correction=0` correctly.
  Not mergeable across files — same separability reason as above.

## Evidence

All runs under `/fast/scratch/hyaku/kake-r64/SimplifyCounterReview/`
(scratch, `TMPDIR=$PWD/tmp`), lane repo `/home/vgpnk/Projects/shokunin/
kake-shokunin` read-only, l1 fixtures at `/fast/scratch/hyaku/kake-r64/l1/
fixtures/` read-only.

- **Originals reproduce receipts** — `orig/c64_calibration.py` on T0
  `4c8295fa` prints `… met=true exit=0`; on `1a481315`, marker `4c666e76`,
  fabrication `f924538e`, junk `82dcba0d`, ledger-mut `5b981bd0` prints
  `met=false exit=1` (field-for-field identical to `controls/*.txt`,
  including `pin_drift=drift:ledger` and `ledger_state=ledger_absent` on the
  two ledger fixtures). `orig/c64_quote_tool.py` on T0 → `met=true exit=0`;
  on stub `14fe2eab` → `tool_sha=mismatch met=false exit=1`.
- **Prototype = original on every input** — `diffrun` compared stdout+exit
  for all 7 C1 inputs and 3 C2 inputs, all `SAME`; `python3 -B
  proto/c64_calibration.py --selftest` prints `selftest 26/26`, proto C2
  `selftest 11/11`, and `diff` of the full 26-line/11-line check listings
  vs the originals' is byte-identical.
- **`rederive` clause-2 redundancy** — exhaustive 18-combination truth
  table: `(frozen_ok_case ∧ clause1) ⇒ clause2` in every case (0
  counterexamples); clause 2 only differs on 6 combos where `met` is already
  false.
- **Builder equivalence** — `proto/build_fixtures.py` output `HEAD^{tree}`
  for stub-repo `f8271b11…`, marker-repo `8cab4d28…`, fabrication-repo
  `c8dc2d14…`, junk-repo `fe8c1cfa…` — all MATCHES vs the committed
  `l1/fixtures/` trees (commit ids differ only by timestamp).
- **Lint** — `pyflakes` (4.0.3, pre-installed at `~/.local/bin/pyflakes`,
  no install performed) clean on all three prototypes; an AST
  assigned-but-never-loaded scan found exactly the three dead constants
  reported above and nothing else.
- **Lane untouched** — `git status --porcelain` shows only the pre-existing
  `??` entries (`w1*`, `w1/`, `sources/S432.live.html`) before and after;
  no mutating git/jj command was run on the lane, nothing written except
  this report.

Tooling: no installs. Used pre-existing `pyflakes` 4.0.3
(`~/.local/bin/pyflakes`, Python 3.14.8) for the unused-name scan; channel:
already-installed binary; reason: dead-code detection.
