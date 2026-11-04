# ExecC2Receipts — C2 instrument receipts and controls (round 75, w1)

Scope: contract §C2 as amended by `amendment-1.md` (A1/A2, frozen population is a floor) and
`amendment-3.md` (A6 committed-receipt read, A7 declared-revision validation). Measured revision
`c9c5e484c533aa65f4374b841a3edcf572ed19a9`; every fixture run used a `git clone --shared` under
`/fast/scratch/hyaku/kake-r75/ExecC2Receipts/` with `TMPDIR`/`HOME` inside that scratch root. The
lane checkout was only ever read (`git show`/`cat-file`), including the landed-state check below.

Deliverables (all under `.ufo/waves/round-75/w1/ExecC2Receipts/`):

| File | What it is |
|---|---|
| `instrument-receipts.json` | the receipt, `instrument-receipts/v1`, 16 entries |
| `instrument_receipts.py` | the canonical ExecC2Tool writer (sha256 `162dd685…`), candidate for `scripts/instrument_receipts.py` |
| `fallback/instrument_receipts.py` | this seat's own writer (sha256 `48965bbb…`), audit trail only |
| `controls/after-c2-receipts.txt` | the admission receipt (committed carry commit, `bound=16 mismatches=0 met=true`, exit 0) |
| `controls/ctl-*.{json,txt}` | each control's receipt bytes and the check that consumed it |
| `worktree-uncommitted-edit.txt`, `committed-edit.txt` | the worktree-vs-commit pair |
| `receipt.sha256.txt` | two writes, `cmp`, receipt sha256/bytes, carrier commit |
| `population.txt`, `interop-tools.txt`, `selftest.txt`, `sim-tip-18.{txt,receipt.json}` | derivation, tool interop, self-test, 18-file landing simulation |
| `landed-tip-check.txt` | read-only check of the L1 landed receipt at HEAD `4e3fc159` (`bound=18 mismatches=0 met=true`) |

## Receipt

`instrument-receipts.json`: `{schema: instrument-receipts/v1, revision:
c9c5e484c533aa65f4374b841a3edcf572ed19a9, date: 2026-11-03, host: linux-x86_64, files: [16]}`,
each entry `{path, sha256, bytes, selftest_mode}` of the committed blob at the named revision.

- sha256 `b37d1b09415e2e63816c701324cf53d86b5e8dcc150130609583dcc836d81a69`, 3 397 bytes.
- `selftest_mode` true for 14 files; false for exactly `.ufo/waves/round-57/c57_idresolver_gate.py`
  (gate with no self-test of its own, differential substitute in its Kind cell) and
  `.ufo/waves/round-69/c69_tmp_honour.py` (no `--selftest` mode) — the same two files C1's E1
  reports at base.
- Second `--write` with identical arguments produced byte-identical output (`cmp`, same sha256) —
  `receipt.sha256.txt`.
- The canonical writer's `--write` line at base:
  `wrote corpus/knowledge/instrument-receipts.json revision=c9c5e484… population=16
  missing_frozen=0 sha256=b37d1b09… bytes=3397`, exit 0.

### Admission check (amendment 3 A6)

The receipt was written at base, committed as the only file of carry commit
`f51d9ce418b911281b81809d2a06cc81096039ff` (parent = base), and checked *from committed bytes* at
that commit (`controls/after-c2-receipts.txt`):

```
C2v1 revision=f51d9ce418b911281b81809d2a06cc81096039ff population=16 bound=16 mismatches=0 met=true
  population: derived=16 frozen=16 missing_frozen=0 beyond_frozen=0
  receipt: source=committed worktree=identical declared=c9c5e484c533 declared_match=false declared_valid=true
exit=0
receipt_path=corpus/knowledge/instrument-receipts.json
receipt_sha256=b37d1b09415e2e63816c701324cf53d86b5e8dcc150130609583dcc836d81a69
receipt_bytes=3397
```

At the bare base revision (no committed receipt) the same command is `population=16 bound=0
mismatches=16 met=false`, exit 1 — the seat's step (2) "green at base" is not reachable under A6 and
is superseded by the carrier-commit form above.

## Landed state (measured at HEAD `4e3fc159`, read-only)

The L1 landed `scripts/instrument_receipts.py` (blob `596e374f…`, sha256 `162dd685…` — byte-identical
to the canonical writer delivered here) and a receipt at the landed instrument revision
`f1fc5d0aba0aef588d943d423fc8767a784607a5` (18 files, sha256
`f3128628d928ae1977b79e9a1005d74a6e4cf97d8730399e4c3aa44a9b8ecc9b`, 3 793 B). Running the *landed*
tool against the lane at HEAD, read-only (`landed-tip-check.txt`):

```
C2v1 revision=4e3fc159919f1af8db139f0931ac096512747895 population=18 bound=18 mismatches=0 met=true
  population: derived=18 frozen=16 missing_frozen=0 beyond_frozen=2
  receipt: source=committed worktree=identical declared=f1fc5d0aba0aef588d943d423fc8767a784607a5 declared_valid=true
exit=0
```

The landed receipt matches this seat's 18-file simulation (`sim-tip-18.receipt.json`) entry for entry
except the `revision` field and the `.ufo/waves/round-75/c75_row_truth.py` digest (the C1 seat rewrote
that counter after the freeze: 45 406 B / `0699a672…` landed vs 10 405 B / `43538343…` simulated).
The other 17 entries are byte-identical, so the simulation's landing sequence was exact.

## Population

Derived twice, independently: the seat's writer (`fallback/`) and the landed canonical writer both
derive the frozen 16 paths at base from `SKILL.md` (live rows of `### Round <N> gate registry
additions`; Name cell if a `.py`/`.mjs` path, else the first such token of Entry command, else
Self-test, else any cell; last row wins). A third derivation using the C1 counter's own
`parse_rows`/`effective` (`c75_row_truth.py` at `88f2e05f`) agrees: `c1_counter=16 equal=true`
(printed as `crosscheck:` on every run of the fallback tool; `population.txt` records the list).
`missing_frozen=0` at base; the Appendix A2 growth case is exercised in `sim-tip-18.txt`.

## Controls (all receipts committed at the measured commit except the worktree case)

| Control | Receipt | Observed line | Exit | File |
|---|---|---|---|---|
| base, no receipt | absent | `population=16 bound=0 mismatches=16 met=false` | 1 | `controls/ctl-absent.txt` |
| worktree-only receipt (A6) | `instrument-receipts.json` (same bytes) | `population=16 bound=0 mismatches=16 met=false`, `source=uncommitted` | 1 | `controls/ctl-worktree-only.txt` |
| fabricated digests | all 16 `sha256` replaced by 64 zeros | `bound=0 mismatches=16 met=false` | 1 | `controls/ctl-fabricated.{json,txt}` |
| dropped path | entry `scripts/redirect_audit.py` removed | `bound=15 mismatches=1 met=false` | 1 | `controls/ctl-dropped.*` |
| flipped `selftest_mode` | `scripts/citation_lint.py` true→false | `bound=15 mismatches=1 met=false` | 1 | `controls/ctl-flipped-mode.*` |
| entry outside population | extra `scripts/outside-the-population.py` | `bound=16 mismatches=0 met=true`; extra reported separately, not counted | 0 | `controls/ctl-extra.*` |
| declared revision missing (A7) | `revision = 000…0` (40 hex, unresolved) | `bound=0 mismatches=16 met=false`, `receipt_revision_invalid` | 1 | `controls/ctl-revision-missing.*` |
| declared revision not an ancestor (A7) | `revision = 88f2e05f…` (descendant of base) | `bound=0 mismatches=16 met=false`, `receipt_revision_invalid` | 1 | `controls/ctl-revision-not-ancestor.*` |
| declared ancestor with a stale blob | `revision = A`, digest the blob had at A; measured commit reverted the edit | `bound=15 mismatches=1 met=false`, `declared_valid=true` | 1 | `controls/ctl-revision-stale-blob.*` |
| frozen floor (A1/A2) | live row for `scripts/redirect_audit.py` removed from `SKILL.md` | `population=15 bound=15 mismatches=0 met=false`, `missing_frozen=1` | 1 | `controls/ctl-frozen-floor.txt` |

E1/E2/E3-style checks are C1's; the receipt controls exercise only §C2's binding terms.

## Worktree edit vs committed edit (seat item 4)

- Worktree edit, same commit: append a comment to `scripts/redirect_audit.py` in a clone checked out
  at the carry commit, do not commit — `HEAD` before/after identical, `git status` shows
  ` M scripts/redirect_audit.py`; check stays `bound=16 mismatches=0 met=true`, exit 0
  (`worktree-uncommitted-edit.txt`). The check reads committed bytes, so an uncommitted edit cannot
  move it.
- Committed edit: same edit committed as the next commit (receipt committed at that commit too) —
  `bound=15 mismatches=1 met=false`, exit 1; finding names `scripts/redirect_audit.py: sha256
  1e1dff18… != …` (`committed-edit.txt`).

The first run of the committed-edit control (fallback writer) and the final run (canonical) agree on
the bound/mismatch counts; the fixture commit ids are scratch-only and are not resolvable after this
seat exits — the receipt JSON bytes are the durable evidence.

## Tool provenance and interop

`w1/ExecC2Tool/instrument_receipts.py` did **not** exist when this seat started (verified by `ls`;
the directory was absent), so the seat rule "otherwise implement the writer from contract §C2 in your
own scratch copy" applied: `fallback/instrument_receipts.py` (sha256 `48965bbb…`, `--selftest`
28/28) implements A6/A7, the floor, `missing_frozen`, and a C1-counter cross-check. The canonical
writer landed mid-wave (final sha256 `162dd685…`, `--selftest` 17/17); every receipt in this report
was then regenerated with it, and it is the delivered `instrument_receipts.py`. Both writers derive
the same 16 paths and emit byte-identical receipt JSON (`interop-tools.txt`), and both are red
(`met=false`, exit 1) on the same A6/A7 probes.

## Landing sequence the L1 ran (verified here)

1. Land `scripts/instrument_receipts.py` (canonical bytes) and the round-75 `SKILL.md` section;
   commit. The derived population at that commit is 18 (16 frozen + `c75_row_truth.py` +
   `instrument_receipts.py`), `missing_frozen=0`.
2. `python3 -B scripts/instrument_receipts.py --root . --revision <landing commit> --write
   --date 2026-11-03` → `population=18 missing_frozen=0`; commit the receipt as a child commit `C`.
3. `python3 -B scripts/instrument_receipts.py --root . --revision C --check` → expect
   `population=18 bound=18 mismatches=0 met=true`, exit 0; record it with `receipt_path`,
   `receipt_sha256`, `receipt_bytes` in `controls/after-c2-receipts.txt`.
   This was simulated before the landing at `sim-tip-18.txt` (population 18, bound 18, `met=true`,
   `beyond_frozen=2`) and has now been performed by the L1 and re-measured at HEAD
   (`landed-tip-check.txt`, green above).

## Risks and limits

- **The base receipt cannot be the tip receipt.** At the tip the receipt written at base binds 16 of
  18 files → `bound=16 mismatches=2 met=false`. This is a landing-sequence requirement, not a
  receipt defect; the measurement above is deliberately at base (the seat's revision).
- **Seat step (2) vs amendment 3.** The seat asked for `--check` green at base; A6 makes that
  impossible without a committed receipt, and the amendment is later and binding. Both measurements
  are recorded (`controls/ctl-worktree-only.txt` red; `controls/after-c2-receipts.txt` green at the
  carry commit).
- `--write` self-checks its own output as a content check and prints `admission: false` until the
  receipt is committed; only the committed `--check` is admission evidence. That matches A6 and the
  canonical writer's behaviour.
- No pacman transaction ran; no tool was installed or upgraded (nothing was needed). This seat wrote
  only its own artifacts under `w1/ExecC2Receipts/` and its report. The L1 committed a mid-flight
  snapshot of that directory at `f1fc5d0a`, so `git status` now shows five modified receipts
  (`controls/ctl-{fabricated,dropped,flipped-mode,extra}.txt`, `worktree-uncommitted-edit.txt` —
  regenerated with the final canonical writer) and three deleted files
  (`controls/base-absent.txt`, `controls/ctl-other-revision.{json,txt}` — fallback/v0 duplicates
  superseded by `controls/ctl-absent.txt` and `controls/ctl-revision-not-ancestor.*`). The worktree
  state is the final evidence; the L1 may re-commit it. Other concurrent changes (`SKILL.md`,
  `LOG.md`, `SCORECARD.md`, `w1/ExecC1Counter`, `w1/ExecC2Tool`, other seats' `controls/` and
  `corpus/lessons/` files) belong to other seats and were not touched here.
- Scratch tree `/fast/scratch/hyaku/kake-r75/ExecC2Receipts/` was deleted before the seat yielded;
  fixture commit ids recorded in the receipts are therefore not resolvable afterwards.

Checks this seat did not run (main-agent/closure): the C1 counter at the after-state revision, the
tip's `--check` after the receipt is rewritten, and any lane-side commit. The C2 self-test
(`selftest.txt`) was run because the capability row names it as evidence.
