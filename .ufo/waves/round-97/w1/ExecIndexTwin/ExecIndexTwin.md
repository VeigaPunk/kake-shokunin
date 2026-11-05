# ExecIndexTwin — round 97 C1 twin check

Seat: ExecIndexTwin (executor, leaf). Target: independent second implementation of the C1 predicate from the docstring, plus per-entry agreement with the frozen counter at the round base and the C1 repair.

## Result

EXEC-TWIN agree_base=84/84 agree_repair=84/84

- Base `36d148f5c60100021304903c30e5663207c72f4f`: twin and counter both `entries=84 indexed=46 unindexed=38 dangling=0 mismatches=38 met=false`. Per entry, the twin's 38 false set equals the counter's 38-entry `unindexed` JSON. Disagreements: 0.
- Repair `9e27ce0b2a8d168e032ab79ea11471b36eaceedf`: twin and counter both `entries=84 indexed=84 unindexed=0 dangling=0 mismatches=0 met=true`. Disagreements: 0.

## Commands and observed rc

- Digest check (before attacking): `sha256sum` on `c97_index.py`, `c97_reval.py`, `frozen/neg-lookup-table.py` → 8535150e…, f3895a32…, 898df9a2…; all match the frozen digests. rc=0.
- Lane tip: `git -C LANE rev-parse master` → `9e27ce0b2a8d168e032ab79ea11471b36eaceedf`.
- Twin, base: `python3 twin_index.py --root LANE --revision 36d148f5… --work SCRATCH` → rc=1 (expected: met=false). Output `twin-base.txt`.
- Twin, repair: same with `9e27ce0b…` → rc=0. Output `twin-repair.txt`.
- Frozen counter, base: `python3 -B c97_index.py --root LANE --revision 36d148f5… --work SCRATCH` → rc=1. Output `counter-base.txt`. Matches the committed `controls/base-c1.txt` summary line.
- Frozen counter, repair: same with `9e27ce0b…` → rc=0. Output `counter-repair.txt`.
- Reading boundary: I read only `c97_index.py` lines 1-45 (the docstring). I did not open its code.

## Twin construction and its own defects (disclosed)

Readings the twin chose where the docstring allowed more than one are listed in `agreement.md` (R1–R7). Two defects were in my first twin draft and were corrected before the reported runs:
1. Population listing: I parsed `git ls-tree` output as four fields and kept full paths, so the population came out empty (`entries=0`). Fixed: three-field parse, basename keys.
2. Dangling tokens: my first ENTRY_RE accepted `knowledge/*` tokens of any suffix, so `.json` tokens (4 per revision, e.g. `knowledge/accessibility-review-cards.json`, referenced in README lines 48, 291) counted as dangling. The docstring's dangling rule names `knowledge/X.md` tokens only. Restricted to `.md`; the counter's dangling=0 is then matched.

Both corrections changed the twin, not the counter. No counter disagreement was produced by either.

## Findings

- F1 (counter/docstring, none disagreed): The 84-entry population, 46/38 split at base and 84/0 at repair, is reproduced by the independent reading. The twin used the same semantic choices the docstring states (fence, header, source, word-count rules). No per-entry divergence arose, so the docstring's ambiguous points did not change any verdict on this population. This is a measured result, not a proof that the readings are unique: R5 (letter count), R2 (delimiter test) and R6 (comment handling) were not stress-tested beyond this population.
- F2 (route, L1): Seat spec names the report path `.ufo/waves/round-97/w1/ExecIndexTwin.md`; the hard bounds limit writes to `.../w1/ExecIndexTwin/`. I followed the hard bounds and placed this report at `.../w1/ExecIndexTwin/ExecIndexTwin.md`. The L1 should reconcile the path.
- F3 (peer incident, observed): ConnectorScope-23 reports an `rm -rf` of the round parent scratch dir at ~18:14Z. My scratch dir was re-created by me (`mkdir -p`) at 18:13 and held no receipts, since the counter and twin read only git objects. All deliverables are in the w1 seat directory and were present after the notice (`ls` at 18:14). Nothing frozen, in the lane tree, or in MANIFEST was touched by this seat.

## Tools

None installed or upgraded. Stdlib python3 and `/usr/bin/git` only.

## Scratch

Scratch root `/fast/scratch/hyaku/kake-r97/ExecIndexTwin/` removed before yield. No fixture repos or clones were created; all git access was read-only (`git show`, `git ls-tree`).

## Files (w1/ExecIndexTwin/)

- `twin_index.py` — independent checker (stdlib, reads committed bytes via `git show`/`ls-tree`, GIT_NO_REPLACE_OBJECTS=1)
- `twin-base.txt`, `twin-repair.txt` — twin output per entry, summary, JSON, exit
- `counter-base.txt`, `counter-repair.txt` — frozen counter output
- `agreement.md` — readings R1–R7, per-entry table (84 rows), verdict line
- `ExecIndexTwin.md` — this report
