# RederiveMutantsV2 — C2(a) after-state attack (kake round 45, wave 2)

Seat: `kake-r45.RederiveMutantsV2`. Lane repo: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Scratch: `/fast/scratch/hyaku/kake-r45/RederiveMutantsV2/`. No tree writes outside this report;
the official counter was re-run against a *copy* of the wave tree in scratch (§3), never in place.

## 0. Named attack and verdict

| # | Named attack | Verdict |
|---|---|---|
| 1 | `python3 -B .ufo/waves/round-45/mutants/mN_v2.py --selftest` for N=1..4 exits 1, 4/4 | **PASS (measured 4/4)** — and baseline canonical driver exits 0 |
| 2 | Each `mN_v2.py` equals committed `c45_audit.py` except the one documented mutation line | **PASS on content** (1 removed / 1 added / 1 hunk each; worktree sha == HEAD blob sha); documented-expression provenance has two caveats, F4 |
| 3 | Same figure re-derivable through the *official* counting path (`c45_freshness.py`) | **PASS** — reproduced `before=2/4 after=4/4` in a scratch mirror, exit 0 |
| 4 | The 4/4 is backed by the after receipts the scorecard cites | **FAIL — evidence citation dangling, F1** |

## 1. Attack 1+2 — mutant selftests and one-line diff (decisive output)

Command:

```
cd /home/vgpnk/Projects/shokunin/kake-shokunin
for n in 1 2 3 4; do python3 -B .ufo/waves/round-45/mutants/m${n}_v2.py --selftest; echo "EXIT=$?"; done
```

Verbatim (tail of each, `EXIT` from `PIPESTATUS[0]`):

```
########## m1_v2 --selftest ##########
  File ".../mutants/m1_v2.py", line 181, in selftest
    assert semantic_witness(mixed_divergence, keys)
AssertionError
EXIT=1
########## m2_v2 --selftest ##########
  File ".../mutants/m2_v2.py", line 184, in selftest
    assert not semantic_witness(timing_only, keys)
AssertionError
EXIT=1
########## m3_v2 --selftest ##########
  File ".../mutants/m3_v2.py", line 182, in selftest
    assert not semantic_witness(v4_divergence, keys)
AssertionError
EXIT=1
########## m4_v2 --selftest ##########
  File ".../mutants/m4_v2.py", line 212, in selftest
    assert not semantic_witness(errored_class_witness, keys)
AssertionError
EXIT=1
########## canonical c45_audit.py --selftest (baseline) ##########
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
EXIT=0
```

Each failure is on the assertion that names the mutated semantics — not an import/syntax/
wiring accident:

| mutant | mutated line (`mutants/mN_v2.py`) | killed at | fixture that fires |
|---|---|---|---|
| m1 | `any(... key in class_keys ...)` → `all(...)` | `:181` | `mixed_divergence` caughtBy `["D","G3"]`, keys `{G1,G2,G3}` → `all` = False |
| m2 | `key in class_keys` → `key in class_keys or key in ("T1".."T5")` | `:184` | `timing_only` caughtBy `["T1"]` → True |
| m3 | `key in class_keys` → `key in class_keys or key in ("A".."F")` | `:182` | `v4_divergence` caughtBy `["D"]` → True |
| m4 | `if row.get("error"): return False` → `return True` | `:212` | `errored_class_witness` = class witness + `error` → True |

Diff against the committed driver (exactly one hunk, one removed / one added line each):

```
$ sha256sum .ufo/waves/round-45/c45_audit.py .ufo/waves/round-45/mutants/m*_v2.py
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  .ufo/waves/round-45/c45_audit.py
8901a8ed952fa7fe055e35061d93960c746254228626593ec7f74eabb74d640e  .ufo/waves/round-45/mutants/m1_v2.py
ea5fd6250369a9c8d5ae07fdfff0ba1aec0d70450a6a9ffc9cc12c75e6f720d6  .ufo/waves/round-45/mutants/m2_v2.py
5eb13bcf83387838c8d0e4fbf829128646fc6151de36325ff4f48dd05b821cba  .ufo/waves/round-45/mutants/m3_v2.py
9c717c1374ab71ee19bd687de00727ecf2f819cd392564ec811d7e3b087f0527  .ufo/waves/round-45/mutants/m4_v2.py

$ for n in 1 2 3 4; do ... diff c45_audit.py m${n}_v2.py ... ; done
m1_v2 removed=1 added=1 hunks=1
m2_v2 removed=1 added=1 hunks=1
m3_v2 removed=1 added=1 hunks=1
m4_v2 removed=1 added=1 hunks=1
```

Driver sha `f3c3171b…` matches the round-state declaration. Provenance — worktree bytes equal the
HEAD blobs, so nothing was edited after commit:

```
$ git cat-file -p HEAD:.ufo/waves/round-45/c45_audit.py | sha256sum
f3c3171b658abccd05bcbf35059243b607ff9979cb88055eed6920f7f4e0a076  -
$ git cat-file -p HEAD:.ufo/waves/round-45/mutants/m1_v2.py | sha256sum
8901a8ed952fa7fe055e35061d93960c746254228626593ec7f74eabb74d640e  -   (m2..m4 likewise equal)
$ git ls-files .ufo/waves/round-45/mutants/      # all 8 witness mutants + 11 v2/m* tracked
```

No cheat path: `_selftest_cohort` binds `me = os.path.abspath(__file__)` (`c45_audit.py:229`) and
spawns `[sys.executable, "-B", me, ...]`, i.e. each mutant drives *itself* end-to-end; it never
re-reads the canonical file. The unit assertions fire before that subprocess, so the kill is
unit-level and correctly targeted (the mutation is in the unit predicate).
`-B` left no `__pycache__`/`.pyc` under `mutants/` (checked with `find`); tree unpolluted.

Before-leg cross-check (frozen v1 mutants, same four expressions):

```
m1.py(v1) EXIT=1     m2.py(v1) EXIT=0     m3.py(v1) EXIT=1     m4.py(v1) EXIT=0   → 2/4
```
matches `verification/selftest-coverage/before/m{1..4}.txt` last lines
`SELFTEST_EXIT=1 / 0 / 1 / 0`.

## 2. Attack 3 — re-derive the *official* counting path without touching the tree

`c45_freshness.py` writes `verification/freshness/freshness.json` inside the lane, so it cannot be
run in place under this wave's read-only bound. I mirrored the exact inputs into scratch
(`mirror/.ufo/waves/round-45/{c45_freshness.py,mutants/m1..4.py,m1..4_v2.py,verification/v6v4/counter-v4.json}`
plus `mirror/.ufo/waves/round-44/verification/claim/{v4-final/v4.json,after-final/after-v5.json}`)
and ran it there (`LANE = Path(__file__).resolve().parents[3]` resolves to the mirror):

```
$ cd /fast/scratch/hyaku/kake-r45/RederiveMutantsV2/mirror && python3 -B .ufo/waves/round-45/c45_freshness.py
selftest_kills before=2/4 after=4/4
v4_predicate_names_class_runs before=true after=false
witness_split class_only=26 mixed=1 met=0
FRESHNESS_RAN_OK
FRESHNESS_EXIT=0
```

Byte-for-byte the same triple as the committed `verification/freshness/freshness.json`
(`after: 4`, `split 26/1/0`). Environment fact: `which jq` → `jaq 3.1.1` on this host; the split
leg still re-derived correctly, so the jq dependency is satisfied by a jq-compatible binary here.

## 3. Findings

### F1 — HIGH (operability / reproducibility): the scorecard's C2(a) after-evidence path is empty

`drafts/scorecard-measurement.md:131-133` cites
`.ufo/waves/round-45/verification/selftest-coverage/after/m{1..4}.txt` and states the after stdout
is `SELFTEST PASS: ... invalid receipt, error-row, and build-count gates`, exit 0. That directory
holds **zero files**, and git tracks **zero** entries there:

```
$ ls -la .ufo/waves/round-45/verification/selftest-coverage/after/
total 0
drwxr-xr-x 1 vgpnk vgpnk  0 Oct 24 00:14 .
drwxr-xr-x 1 vgpnk vgpnk 22 Oct 24 00:14 ..
$ git ls-files .ufo/waves/round-45/verification/selftest-coverage/ | wc -l
4                      # only before/m1..m4.txt
```

(An empty directory cannot be committed, so the cited `after/` receipts do not exist in any commit;
the `{{C2_SELFTEST_AFTER_TABLE}}` placeholder at `scorecard-measurement.md:132` is still unrendered
for the same reason.) The *number* is true — I re-derived 4/4 three ways (§1, §2) — but an auditor
following the scorecard's own evidence path finds nothing, and the before-leg receipts (`00:14`) are
9× older than the only committed after-evidence (`freshness.json`, `00:56`). Remedy is documentary:
either commit `after/m{1..4}.txt` (each `SELFTEST_EXIT=1`, with the canonical baseline's
`SELFTEST_EXIT=0`) or strike the citation and point at `freshness.json` + `c45_freshness.py`.

### F2 — MEDIUM (operability): `--selftest` is a false green under `-O` / `PYTHONOPTIMIZE`

The entire gate is bare `assert`. Optimized mode strips it, and the driver still prints PASS:

```
$ for n in 1 2 3 4; do python3 -O -B .ufo/waves/round-45/mutants/m${n}_v2.py --selftest; echo "EXIT=$?"; done
SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, build-count gates, and the end-to-end fixture cohort
EXIT=0      (identical for m2_v2, m3_v2, m4_v2)
$ python3 -O -B .ufo/waves/round-45/c45_audit.py --selftest
SELFTEST PASS: ... EXIT=0
```

Bounded, not unbounded: `run_selftest` in `c45_freshness.py:35-38` passes only `-B`, and
`PYTHONOPTIMIZE` inherited by those children would push `after_kills` to 0/4 — a loud contradiction
of the claim rather than a silent pass — so the *counting* command degrades safely. The exposed
surface is the `--selftest` interface itself: a caller (or a wrapper that adds `-O`, or an
environment with `PYTHONOPTIMIZE=1`) gets `SELFTEST PASS` + exit 0 from a known-defective driver.
Cheap hardening: assert an explicit `if not __debug__: sys.exit(2)` at the top of `selftest()`, or
raise `RuntimeError` instead of `assert`.

### F3 — MEDIUM (claim boundary): 3 of the 4 kills are fixture-only; only m1 is visible on real data

I re-evaluated the canonical and all four mutant predicates over the 27 real rows of the honest
after-cohort receipt (`verification/matrix/runs/after/honest-8e7184ba711d/after-v5-v2.json`,
`classKeys G1..G10`, script `/fast/scratch/hyaku/kake-r45/RederiveMutantsV2/diff_witness.py`):

```
classKeys: G1,...,G10 | rows: 27 | canonical witnessed: 27 notMet: 27 errors: []
repeat-len-band  False  C,G7   base=True m1=False  <== MUTATION VISIBLE
TOTALS {'base': 27, 'm1': 26, 'm2': 27, 'm3': 27, 'm4': 27}
error rows: []
```

So on the cohort the lane actually certifies, m1 flips exactly one row (`repeat-len-band`, the one
mixed `C,G7` witness that supplies leg (c)'s `mixed=1`), while m2/m3/m4 are semantically inert
(m4 is inert because the honest cohort has **no** error rows). The 4/4 is honest as a
*synthetic-fixture* coverage number — each mutant dies on a distinct asserted invariant — but it
must not be read as "the real cohort would notice 4/4 of these mutations". Any downstream sentence
that attributes the 4/4 to the 27-control evidence would be an overclaim.

### F4 — LOW (documentation): "m1–m4" names two different mutant sets, and the mutation *expression* form differs from its documentation

- `w1/MutDriverV2Spec.md:39-73` documents m1–m4 as **`receipt_validity`** mutations with its own
  `m1..m4 selftest_exit=1` table; the C2(a) mutants here are the **witness-class** mutations of
  `round-44/w2/MutClassGate.md` §"The four mutants". The scorecard names the correct source, and
  `w1/ReviewKillRules.md:196` already flagged the collision, so the ambiguity is disclosed but
  unresolved; a reader who greps "m1_v2" lands on the wrong table first.
- Content provenance for the mutated line: m1/m4 are byte-identical to the round-44 documented
  expressions; m2_v2/m3_v2 use the inlined literals `("T1","T2","T3","T4","T5")` /
  `("A","B","C","D","E","F")` that the *delivered* v1 mutants also use, whereas `MutClassGate.md:74,79`
  names them `TIMING_KEYS` / `V4_RUN_KEYS`. `m2_v2` vs `m2.py` differs only by tuple spacing. So
  "one documented mutation line" is true semantically; the doc's prose form is not literally the
  committed form (pre-existing, round-44-frozen — report only, do not edit).
- Mode is the one non-content variance: canonical `755`, `m*_v2.py` `644` (v1 mutants are `755`).
  Irrelevant to `python3 -B <path>` invocations; would matter only to a `./mN_v2.py` call.

## 4. Positive verifications recorded

- 4/4 after-kills real, each on its exact semantics; canonical baseline green (exit 0).
- One-hunk content equality with the committed driver; worktree == HEAD for driver and all four mutants.
- Official counting script reproduces `before=2/4 after=4/4`, `v4 true→false`, `split 26/1/0`, exit 0, from a scratch mirror.
- Before-leg receipts match a fresh run (`1/0/1/0`).
- No self-reference cheat (`me = __file__`), no bytecode/permission pollution of the tree.

## 5. Residual risk / verification gaps

- **Unrun:** the `--selftest` kills were not re-run against the counter-side (`mutants/v2/m1..m11.py`) —
  out of this seat's target. The `w1/MutDriverV2Spec.md` survival claims for the wiring mutants
  (m8–m11) and its `detect.py`/`pristine_v2.py` tables were not re-executed.
- **Unrun:** the real 27-control + build 3/3 audit was not re-executed end-to-end (needs the live
  counter over 27 repos, ~minutes-per-row class runs); F3's differential uses the *committed*
  after-cohort rows, which is a lower bound on real-data visibility, not a substitute.
- **Dependency recorded, not blocking:** F1's remedy lives in `drafts/` evidence, owned by the
  L1/scribe seats; this seat is read-only over the lane.
- Kill-coverage style: mutants are mutated drivers carrying the *fixed* test, so the measurement is
  test-suite strength (correct for leg (a)); it does not prove the shipped matrix would refuse a
  mutated driver whose selftest was removed.

## 6. Files written

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-45/w2/RederiveMutantsV2.md` (this report)
- `/fast/scratch/hyaku/kake-r45/RederiveMutantsV2/diff_witness.py` (scratch differential, §F3)
- `/fast/scratch/hyaku/kake-r45/RederiveMutantsV2/mirror/**` (scratch mirror for §2 only)

No tool installs or updates were performed. No committed file, frozen artifact, or lane receipt was
modified; no git/jj mutation commands were run (only `git ls-files` / `git cat-file` reads).
