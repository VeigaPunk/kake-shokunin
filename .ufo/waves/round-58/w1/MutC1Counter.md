# MutC1Counter

Mutation test of `kake-shokunin/.ufo/waves/round-58/c58_receipt_rewrites.py` (round-58 C1 counter) against its own selftest. Leaf seat: no subagent dispatch; no tool installs (RULES.md read; nothing installed). Lane/fleet read-only — all work in `/fast/scratch/hyaku/kake-r58/MutC1Counter/`.

Method: baseline copy (`c58_receipt_rewrites.py`, sha256 `dace35ce…`); 21 single-point mutants each written as a scratch copy; each run `TMPDIR=/fast/scratch/hyaku/kake-r58/MutC1Counter python3 -B <mutant> --selftest`. Killed = exit != 0 (selftest reports failures/crash); survived = exit 0. Baseline: 18/18 PASS, rc=0.

## MUTANTS

| id | change (single point) | killed? | evidence |
|-----|-----------------------|---------|----------|
| M01 | git log: drop `--no-renames` (rename becomes M, not D+A) | killed | FAIL rename is a deletion event; delete and readd disclosed meets |
| M02 | `status == "A" and path not in seen` → `status == "A"` (re-add never an event) | killed | FAIL re-add after delete is an event; delete and readd disclosed meets |
| M03 | drop `seen.add(path)` on event paths (line 108) | survived | rc=0, 18/18 |
| M04 | match key drops fromBlob/toBlob (path/commit/status only) | killed | FAIL wrong blob is phantom |
| M05 | `used` set removed (duplicate entries both match) | killed | crashes: `NameError: name 'used' is not defined` (measure line 194) |
| M06 | classify: format checked before append | survived | rc=0, 18/18 |
| M07 | `pointed()` always returns True | killed | FAIL pointer-free note counted; note naming an absent path counted |
| M08 | `NEW_RE` round 58 → 57 (this-round rewrites invisible) | killed | FAIL true disclosure meets; note naming a resolvable commit meets |
| M09 | predicate `new_receipts == 2` → `>= 1` | killed | FAIL missing C3 receipt not met; non-receipt ignored |
| M10 | `wrong_kind` term dropped from `met` | killed | FAIL false kind (rerun for a pending fill) counted |
| M11 | `HEX40` loosened `{40}` → `{4,40}` | survived | rc=0, 18/18 |
| M12 | malformed check on empty note removed | killed | FAIL empty note malformed |
| M13 | `POP_RE` widened to any path under `round-N/` | killed | FAIL wrong blob is phantom; note naming a resolvable commit meets; round-58 rewrite fails even disclosed; missing C3 receipt not met |
| M14 | selftest exit code inverted (0↔1) | killed | PASS-lines intact, rc=1 (exit swap detectable) |
| M16 | git log: drop `-m` (merge diffs) | survived | rc=0, 18/18 |
| M17 | `NEW_RECEIPT_RE` only `after-c2-*` | killed | FAIL true disclosure meets; note naming a resolvable commit meets; delete and readd disclosed meets |
| M18 | drop commit-hash pointer lookup in `pointed()` | killed | FAIL note naming a resolvable commit meets |
| M19 | git log: drop `--reverse` (events newest-first) | killed | FAIL undisclosed fill counted; true disclosure meets; wrong blob is phantom; note naming a resolvable commit meets; round-58 rewrite fails even disclosed; rename is a deletion event; delete and readd disclosed meets |
| M20 | `fromBlob` unguarded (always `blob_id(parent)`) | survived | rc=0, 18/18 |
| M26 | git log: drop `--first-parent` | survived | rc=0, 18/18 |
| M27 | `POP_RE` filter inverted (matching paths skipped) | killed | 13 FAIL checks (all events vanish) |

Mutant hashes (first 12 hex): M01 6707612c, M02 c2f32758, M03 138dbd59, M04 bbc3200a, M05 69c94b8e, M06 fcef79c0, M07 bc927812, M08 590cd0f4, M09 f3b9ec35, M10 a3048135, M11 28045576, M12 552d9659, M13 58ded7b4, M14 363e6237, M16 f6a0e680, M17 8108b36d, M18 781c2371, M19 8a6fc2bf, M20 db0df504, M26 b206bc36, M27 2d768e99.

## SURVIVORS

1. **M03** — `seen.add(path)` on event paths is redundant: any path's first sighting reaches line 106's add; every later `A`/`M`/`D` event is on an already-seen path, so removing line 108 changes nothing observable.
2. **M06** — format-before-append only differs when `new.startswith(old)` AND whitespace-equal, i.e. a change that only adds whitespace to an extending edit; 18/18 pass, no such fixture existed.
3. **M11** — `{4,40}` hex still accepts every id used in fixtures (all real 40-hex); no short/non-hex id exercised.
4. **M16** — drop `-m`: with `--first-parent`, git emits first-parent diffs for merges regardless, so `-m` is redundant in this walk (validated: P3 below passes untouched, 22/22).
5. **M20** — `has_parent` guard: root commits can only contribute status `A` (skipped), so every observable event has a resolvable parent; the branch is dead logic.
6. **M26** — drop `--first-parent`: no fixture contains a merge/side-branch receipt event; the walk's ancestry restriction is untested.

## PROPOSED FIXTURES

(one per survivor; appended to `selftest()` as check tuples before the `finally:` block; full extended suite validated: 22/22 at base, rc=0)

- **P1 (kills M06)**: `checks.append(("blank-line append is append not format", classify("M", "a\n", "a\n\n") == "append"))` — old `a\n` → new `a\n\n` is an extending edit; swapped order returns `"format"`. Validated: base passes; M06 FAILs P1 only.
- **P2 (kills M11)**: fixture repo with R filled (M event), N2/N3 receipts, ledger entry `_entry(d, R, c, "M", commit="a" * 8)` (8-hex commit): expect `v["malformed"] == 1 and not v["met"]`. Validated: base passes; M11 FAILs P2 only.
- **P3 (kills M26)**: side-branch receipt rewrite merged `--no-ff`: R v1 on main → topic branch rewrites R → checkout main, add N2/N3, `git merge --no-ff topic`; expect `v["events"] == 1` (the merge surfaces the rewrite; the topic commit is outside the first-parent walk). Validated: base passes 22/22; M26 FAILs P3 only (`events` becomes 2: topic commit + merge).
- **M03 / M16 / M20**: no behavioral fixture can kill these — each is state-equivalent to the base code on all histories (redundant `seen.add`; `-m` superseded by `--first-parent`; `has_parent` unreachable for events). Recommended instead: delete the dead branch/flag (`M16` `-m`, `M20` guard, `M03` line 108) or add an internal invariant assertion; not new black-box checks.

Restoration: lane source untouched; all mutants live only in scratch. Scratch receipts: baseline + 21 mutant copies + extend.py + extended runs; scratch dir removed after this report (this report is the receipt).

VERDICT: 15/21 mutants killed; 6 survived — 3 killable by proposed fixtures (P1→M06, P2→M11, P3→M26) and 3 semantically neutral dead-code findings (M03, M16, M20); selftest coverage gaps documented, no contract changes made.
