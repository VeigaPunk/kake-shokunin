# ReviewerPinsV2

Scope: code review of the version-2 C1 counter, read at lane revision `4b8c73050470ada9e6583f3b12d659d1bed6a17f`
(`.ufo/waves/round-57/c57_receipt_pins.py`, 668 lines; the working-tree copy is byte-identical — `diff` of `git show 4b8c730:…`
against the file is empty). Every finding below was reproduced in a scratch repo (`git init` under `mktemp -d`, `-c user.name=selftest`)
or against the lane read-only; "confirmed by running" means I ran that exact input. Nothing outside this report was written.

## FINDINGS:

**F1 — HIGH — line 119 (with `scan` 147-178): a relabel written inside a merge commit is invisible.**
Input (confirmed by running): receipt `.ufo/waves/round-56/controls/after-c1.txt` pinned `a…`; side branch with an unrelated file;
`git merge --no-ff --no-commit side`; rewrite the receipt to `b…`; `git commit -m "merge side"`. The counter prints
`undisclosed_relabels=0 … new_relabelled=0`, exit 1 for the unrelated missing claims, while `git show --first-parent --name-status <tip>`
reports `M .ufo/waves/round-56/controls/after-c1.txt` and `<tip>:<path>` holds `b…`. Same result when the merge is produced by
`git commit --amend` after a plain merge. Cause: `git log --name-status` emits no diff for merge commits, and `scan` never reads the
tip's pin values (only `ls-tree` names). This is the exact v1 escape the contract says version 2 closes ("a merge-shaped relabel"); it is
still open. Fix: `git log --diff-merges=first-parent --name-status -M` (confirmed by running: it emits `M …/after-c1.txt` for the merge,
and first-parent `A`/`D` records re-compare idempotently), and/or reconcile every present population path's tip pin set against the
walk's `last[path]` at the end of `scan` (I ran that reconciliation over the real lane at `4b8c730`: 56 present paths, 0 drift, so it
adds no false positives).

**F2 — HIGH — lines 147-178: the pin state is one global cell, so on a branched receipt the reported `from` is whichever parent was
walked last; a truthful errata becomes impossible.**
Input (confirmed by running): base pinned `a…`; side relabels to `b…`; main relabels to `c…`; merge resolved to `c…`; an unrelated later
commit. Output: `UNDISCLOSED <path> a… -> c… at <main>` and `UNDISCLOSED <path> c… -> b… at <side>`. The second tuple never happened at
that commit — the side commit's real predecessor is `a…` (line 175 compares against the global `last`, overwritten by main's commit).
An honest `receipt-errata.json` cannot name `(path, c…, b…, side)`, so disclosure is rejected as phantom while the truth is reported as
undisclosed. Fix: make the state per commit — read each parent's blob (`git cat-file`/`git show <parent>:<path>`) instead of carrying a
single `last` across the DAG.

**F3 — HIGH — lines 152-163 and 174-178: renaming a pinned receipt out of the population and back in hides a relabel and clears the
deletion latch.**
Input (confirmed by running): pin `a…`; `git mv` to `.ufo/waves/round-56/notes/advanced.txt` (R100); `git mv` back with the body rewritten
to pin `b…`. Output: `undisclosed_relabels=0 deleted_receipts=0`, while the tip blob holds `b…`. Line 152 `last.pop(old, set())` throws
the pin state away on the way out; the re-add arrives as `A` (content changed too much for `-M`), so line 175 compares against an empty
set, and line 178 `deleted.discard(path)` drops the latch set at line 155. Fix: keep the popped pin set (a `moved[old]`/`moved[new]`
map) and consult it for the first `A`/`M` after a rename-out; do not discard the latch when the path re-enters from a rename.

**F4 — MED-HIGH — lines 65-67: `KAKE_R57_PINS_TEST_BASE` relaxes a real run and is never echoed.**
Inputs (confirmed by running, three separate scratch repos): (a) `KAKE_R57_PINS_TEST_BASE=<tip>:0` on a repo whose history was replaced by
an orphan commit turns `new_unpinned=1` plus the note "base revision … is not an ancestor of the tip (history replaced)" into
`new_unpinned=0` and no note; (b) the same env on a tip that is short of the base population turns `deleted_receipts=1` into `0`;
(c) neither change touches the CLI arguments, and `report()` never prints `BASE_REV`/`BASE_POPULATION`, so the poisoned receipt is
indistinguishable from an honest one. The comment says "selftest only"; nothing enforces it. Fix: take the base/population through a
`--test-base` flag that is refused unless `--selftest` (the selftest already drives `globals()` in-process, so the env var can go), or
refuse the env var unless `os.path.realpath(root)` is under `tempfile.gettempdir()`; print the effective base and population in the
report header.

**F5 — MED — lines 135 and 219: the lost-population guard is a count, not a set, so any added file masks a lost base receipt.**
Input (confirmed by running): base holds `after-c1.txt` and `after-c2.txt` (population 2); a merge commit deletes `after-c2.txt`; a normal
commit adds `after-c9-extra.txt`. `9703ad6:…/after-c2.txt` exists and the tip lacks it, yet `deleted_receipts=0`
(`max(0, 2-2-0)=0`). Combined with F1 this makes a whole receipt disappear silently. Fix: keep the base set —
`base_present = {p for p in ls-tree BASE_REV if in_pop(p)}` — and count `len(base_present - present)`, asserting
`len(base_present) == BASE_POPULATION` instead of trusting the literal 44.

**F6 — MED — line 287: the `## Round 57` section match is truncated by a `## Round <other>` line inside a fenced block, and pins inside
fences are counted.**
Inputs (confirmed by running): (a) `## Round 57 — measured` / `Measured revision: <M>` / a ```` ```text ```` fence containing
`## Round 56 — quoted in a fence` / `Measured revision: 9999…` → `scorecard_pin=1` (the contradicting labelled line is dropped);
(b) a fence containing `Measured revision: 9999…` → `scorecard_pin=0` (false fail on a quoted example). The real SCORECARD has one
fenced block today (lines 145-154), so the defect is latent, and round sections do embed fences. Fix: strip fenced regions first
(toggle on `^```` lines), then split on `^## ` headings, before extracting pins.

**F7 — MED — lines 270-280 with `report_first_line` (306-307): the first line the body rule demands cannot be printed by the documented
counting command at T0.**
Input (confirmed by running on a lane clone at `4b8c730`, receipts introduced at C' and after-c1's final body committed at T0): the CLI at
T0 prints `… new_receipts=2 … met=False` — at T0 after-c1 can never already carry its final body, because `fine` requires `t0 != lc` and
`lc` is the commit that writes that body — while the re-derivation at line 277-280 (`measure(..., check_bodies=False)`) yields
`… new_receipts=3 scorecard_pin=1 met=True`, and the check demands exactly that. So the receipt line is only obtainable by calling the
module's `measure(..., check_bodies=False)`; a seat that follows the contract's command and pastes the CLI line is rejected with
`body line … != re-derived` (this is what my fixture produced). Fix: derive T0 with bodies enabled and require the CLI line, or drop
`new_receipts` from the compared prefix and state in the docstring and the contract that the receipt line is a derivation, not a run.
Related: the alternative (amending after-c1 to carry the final body at T0) rewrites a committed file carrying a `revision:` line, which
the round's receipt discipline forbids, and `compare` cannot see it because only pin sets are diffed.

**F8 — MED — lines 644-664: an unexpected exception exits 1 ("not met"), not 2 ("unevaluable").**
Input (confirmed by running): `KAKE_R57_PINS_TEST_BASE=not-a-rev` → Python traceback, empty stdout, exit 1 — a crashed run is
indistinguishable from a measured unmet run in a receipt. Same for a missing `git` binary or any `OSError` in `Sandbox`/`measure`.
`main` catches only `Unevaluable`. Fix: wrap the `main` body in `except Exception` → print `C1 receipt-pins unevaluable: …` and return 2;
validate the override shape (`^[0-9a-f]{40}:[0-9]+$`) at parse time and return 64 on mismatch.

**F9 — LOW — line 288: labelled pin lines in other forms are ignored.**
Inputs (confirmed by running): `- **Measured revision:** 9999…` and `Measured revision: 9999999` (abbreviated) both leave
`scorecard_pin=1` although the Round 57 section states a different revision. The docstring says every `Measured revision:` line must name
the measured revision. Fix: allow an optional `**`/backtick around the label and fail when a `Measured revision` label in-section carries
anything but the measured 40-hex value.

**F10 — LOW — lines 119 and 135: git's C-quoting hides non-ASCII paths.**
Input (confirmed by running): an extra receipt `.ufo/waves/round-57/controls/after-c2-测试.txt` is invisible — `ls-tree` returns
`".ufo/waves/round-57/controls/after-c2-\346\265\213\350\257\225.txt"`, so it is neither counted as a second receipt for claim 2 nor
flagged malformed (`new_unpinned=0`, `population` unchanged). Fix: `-c core.quotePath=false` and `-z` with `-z`-aware parsing, or
`rev-parse`-normalise both sides.

Notes, not counted above: `[INFERENCE]` `-M` degrades to `A`+`D` past `diff.renameLimit` (default 1000) in one commit, which turns one
relabel into a false `deleted_receipts` plus a fresh, never-compared path; the v2 text does not bound commit size. The `C` branch in
`scan` (150-163) is unreachable with `--name-status -M` (measured: with `diff.renames=copies` the copy is still reported as `A`), and if
`-C` were ever added it would take `rec[1]` (the old path) and ignore the new one.

## TIMING:

- Counter at the base, `--revision 28fa0b23e699303725aba2727094531f5e44494d` (counter copy read from `4b8c730`; the file does not exist at
  28fa — `git show 28fa…:.ufo/waves/round-57/c57_receipt_pins.py` fails): **0.14 s wall**, exit 1. Output reproduces the committed control
  `controls/base-c1-receipt-pins-v2.txt` exactly (same first line, same six `UNDISCLOSED` lines, same `tip:`).
- Counter at the tip, `--revision 4b8c73050470ada9e6583f3b12d659d1bed6a17f`: **0.14 s wall**, exit 1, `population=56 relabels_in_history=6`,
  `new_receipts=0 scorecard_pin=0` — correct for a pre-measurement tip (`measured.json`, `after-c*` and any `## Round 57` section are
  absent at `4b8c730`), so nothing to flag there.
- Recursive path (`after-c1` with a `tip:` line, lane clone of 335 commits, measured revision `4b8c730`): **0.29 s wall** vs 0.15 s
  without recursion — one extra full `scan` plus its blobs, i.e. ~2×, not exponential. Recursion depth is 1: the nested call is
  `measure(root, t0, check_bodies=False)` and the whole body block (the only recursion site) is guarded by `if ok and check_bodies`
  (line 259), so **no infinite-recursion risk**; `t0` is a strict ancestor of `lc` (line 272), which is an ancestor of the tip, so `t0`
  can never equal the tip.
- Cost shape: one `git show` per changed population path per commit, plus `rev-parse`, `ls-tree`, one `first_add` per receipt/counter and
  one `last_commit`; linear in commits × population churn (~0.4 ms/commit at 56 population paths), so ~1 s at 2 000 commits — acceptable.
- `--selftest` at `4b8c730`: **7.25 s wall, 48/48 PASS, exit 0** (the committed receipt `controls/c1-selftest-v2.txt` says the same).

## NO-DEFECT CHECKS:

- **`@@` parsing (117-130)**: `--format=@@%H` prints only the hash line; commit subjects/bodies are not printed, so the only tab-bearing
  lines are name-status records. An `R067` record with two paths is handled (confirmed: internal-population rename + relabel in one commit
  → `undisclosed_relabels=1 deleted_receipts=0`).
- **Copy records**: `--name-status -M` emits no `C` (confirmed with `diff.renames=copies`: a byte-identical copy is reported as `A`), so the
  two-path non-R branch is unreachable today and the copy-then-relabel evasion does not exist; the relabel of the copy is caught
  (`undisclosed_relabels=1`). Latent risk recorded above.
- **`first_add` newest add (188-189)**: delete + re-add returns the re-add commit, not the original add (confirmed, two-commit fixture).
- **`last_commit` (183-184)**: `git log -1 --format=%H tip -- path` returns the commit that last wrote after-c1 (confirmed indirectly but
  decisively on the lane clone: the C1 body rule reached the re-derivation at line 277, which requires `lc` to be the body-writing commit
  and `is_ancestor(t0, lc)` to hold; if `lc` were wrong, `fine` would fail before the recursion).
- **`deleted` vs `present` (167-179)**: a pin stripped and left stripped yields one relabel with an empty `to` (confirmed:
  `… a… -> at …`); an unpinned receipt renamed out is not latched by line 168 but is caught by the population count (confirmed:
  `deleted_receipts=1` at population 2, `0` at population 1 — i.e. the count is the only guard, see F5).
- **scorecard sections joined (287)**: two `## Round 57` sections are both checked and a contradiction in either gives
  `scorecard_pin=0` (confirmed); a `Measured revision:` in a following `## Round 58` section is excluded (confirmed, `scorecard_pin=1`).
- **exit codes**: nonexistent `--revision` → exit 2 with a one-line `C1 receipt-pins unevaluable: git rev-parse --verify …` (confirmed);
  missing `--revision` → 64 and malformed errata/`measured.json` → 2 (both confirmed by the 48/48 selftest run, which exercises the CLI
  child in four cases). Only the uncaught-exception conflation in F8 is a defect here.
- **errata/measured validation (192-232)**: non-object/non-list errata, non-string fields, duplicates and a non-string or non-40-hex
  `revision` all raise `Unevaluable` → exit 2, never a pass; errata matching is exact on all four fields, so a disclosure with a wrong `to`
  or `commit` yields `undisclosed=1 phantom=1` (confirmed by the selftest scenarios and by the base run's six real relabels matching
  `receipt-errata.json` exactly: `undisclosed_relabels=0` at `4b8c730`).
- **`new_paths`/`NEW_RE` (238-251)**: a malformed `after-c4-*` name and a second receipt for one claim both count as `new_unpinned`
  (selftest) — except when the path is C-quoted (F10).

VERDICT: reproducible and cheap (0.14 s; 0.29 s with the C1 re-derivation) and its base control matches the committed receipt, but the frozen predicate is still satisfiable by a merge-shaped relabel (F1), by a rename out of the population and back (F3) and by the undocumented env override (F4), while a branched receipt makes honest disclosure impossible (F2) and the C1 receipt line cannot come from the documented command (F7) — not fit to certify C1 until F1-F5 and F7 are fixed.
