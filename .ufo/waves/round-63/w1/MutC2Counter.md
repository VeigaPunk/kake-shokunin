# W1 seat report — MutC2Counter (mutation test of `c63_quote_tool.py`)

Date: 2026-10-27. Round-63 wave-1, leaf seat (no subagents, no commits/push, no
git/jj mutation outside the sanctioned scratch fixture). Item: mutation-test
`c63_quote_tool.py` with ≥6 assigned mutants, each run against a stub tool and
the real tree; report the kill matrix.

## Target and provenance

- Counter under mutation (frozen, never modified by this seat):
  `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/c63_quote_tool.py`
  sha256 before `9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e`
  = sha256 after (matches the contract's frozen C2 counter sha).
- Tool blob at measured revision, read-only:
  `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 05b0d7f4b4a23513390f7b92547e2b0f1fccb06f:scripts/quote_class.py | sha256sum`
  → `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14` (matches
  the contract's frozen tool sha; the worktree copy hashes identically).
- Fleet repo HEAD during the probe: `15eb965c1d0f23ce2a522c651e9306a0952da7d3`
  (unchanged before/after; only read-only `rev-parse`/`show` were run).
- Pristine working copy: `/fast/scratch/hyaku/kake-r63/MutC2Counter/pristine/c63_quote_tool.py`
  sha256 `9fcbfad0…` (byte-identical to the fleet counter). All six mutants are
  scratch copies of these pristine bytes; the fleet file was never opened for
  writing.

## Method — bounded behavioral detector

Driver: `/fast/scratch/hyaku/kake-r63/MutC2Counter/run_detector.sh`; raw output:
`/fast/scratch/hyaku/kake-r63/MutC2Counter/results.tsv` (49 lines).

Each run is the contract's counting command shape against a counter variant:

```
python3 -B <counter> --root <repo> --revision <rev>    # one stdout line + exit code
```

Environments (7 per counter variant):

- `real` — fleet repo at measured rev `05b0d7f4b4a23513390f7b92547e2b0f1fccb06f`.
- `stubA…stubF` — scratch fixture repo `/fast/scratch/hyaku/kake-r63/MutC2Counter/stubrepo`
  (built by `build_fixture.sh`: `git init -q`, `git rev-parse --show-toplevel`
  asserted equal to the fixture dir before the first commit, throwaway inline
  identity `MutC2Counter scratch <mutc2counter@scratch.invalid>`, one commit per
  stub; deleted after the runs). Each stub seeds exactly one tool defect and is
  otherwise fully conforming (ok=true, all cases pass, JSON on stdout, exit 0):
  - stubA `7d2ec9cbb1901ad759db5a061be78b6ef3582837` — case set misses every frozen id (`case_1..4`)
  - stubB `15f640e3796c525fa0602e9cad00a3ba2694808f` — `markup_collapsed_only` has `derived != expected`
  - stubC `cecf3349e86a7f0e2a0fb7556de5737cae5ea7da` — summary undercounts `passed=3` of `total=4`
  - stubD `5306d25b0bca49cb3e839087733e3f63fa792e56` — `total=3` off the frozen count of 4
  - stubE `627bca42675175abc60031a7ce2152739e54e856` — valid passing JSON but exits 3
  - stubF `2016363c8c76b169670fec1926810cb5eb5e6584` — JSON on stderr, stdout empty

Baseline gate: the mutant phase aborts (verdicts `inconclusive`) unless the
pristine counter prints `met=true` (exit 0) on the real tree. Baseline held:

| env | pristine output (tail) | exit |
|---|---|---|
| real | `present=1 selftest=4/4 frozen_cases=ok met=true` | 0 |
| stubA | `selftest=4/4 frozen_cases=missing met=false` | 1 |
| stubB | `selftest=4/4 frozen_cases=missing met=false` | 1 |
| stubC | `selftest=3/4 frozen_cases=ok met=false` | 1 |
| stubD | `selftest=3/3 frozen_cases=ok met=false` | 1 |
| stubE | `selftest=failed met=false` | 1 |
| stubF | `selftest=unparseable met=false` | 1 |

Kill criterion: a mutant is **killed** if any run's (stdout line, exit code)
differs from pristine's on the same environment; otherwise it **survives**
(a coverage finding against the detector, not a contract change).

## Mutants — one behavior-bearing point each

`diff -u pristine/c63_quote_tool.py mutants/mX.py` (paths under
`/fast/scratch/hyaku/kake-r63/MutC2Counter/`); sha256 of each mutant in
parentheses:

- **m1 frozen-case check removed** (`a5c16b5b07793b8724d7f0a4b2a9bc40f6bd1cf10aba7fb7c2bf354614e93821`):
  `met = bool(result.get("ok") and frozen_ok and total == passed …)` → `frozen_ok` dropped from `met`.
- **m2 derived==expected dropped** (`d9f87b228f8d24ea9c77ae5bf6a3d76e0448b623658909aa8fcae4196967c4c0`):
  the `and cases.get(cid, {}).get("derived") == cases.get(cid, {}).get("expected")` clause deleted from `frozen_ok`.
- **m3 ok/total not compared** (`dd6759b776465b0159ac1402e532bd78d987009a3a2de366cf3fa1b98ebbdd6a`):
  `total == passed` dropped from `met`.
- **m4 total not compared to frozen count** (`37079a4d7ea84e50c1cc840fa8c2e80853e59f31887617ba2e30d4aeaee0d9bc`):
  `and total == len(FROZEN_CASE_IDS)` dropped from `met`.
- **m5 returncode ignored** (`527591d082ef5031ed5f71da76fc10326b21e079aff436834a9740eedbc798c6`):
  the `if proc.returncode != 0: … return 1` gate deleted.
- **m6 JSON parsed from stderr** (`28949dca85eefbf264d9ae7f498b0160501ed184043a82e4df171ef6ba98d3ea`):
  `json.loads(proc.stdout.decode("utf-8"))` → `json.loads(proc.stderr.decode("utf-8"))`.

No other line of any mutant differs from pristine (diffs above are complete).

## Kill matrix (met flag / exit per environment)

| mutant | real | stubA | stubB | stubC | stubD | stubE | stubF | verdict |
|---|---|---|---|---|---|---|---|---|
| pristine | true/0 | false/1 | false/1 | false/1 | false/1 | false/1 | false/1 | baseline |
| m1 | true/0 | **true/0** | **true/0** | false/1 | false/1 | false/1 | false/1 | **KILLED** (stubA, stubB) |
| m2 | true/0 | false/1 | **true/0** | false/1 | false/1 | false/1 | false/1 | **KILLED** (stubB) |
| m3 | true/0 | false/1 | false/1 | **true/0** | false/1 | false/1 | false/1 | **KILLED** (stubC) |
| m4 | true/0 | false/1 | false/1 | false/1 | **true/0** | false/1 | false/1 | **KILLED** (stubD) |
| m5 | true/0 | false/1 | false/1 | false/1 | false/1 | **true/0** | false/1 | **KILLED** (stubE) |
| m6 | **false/1** | false/1* | false/1* | false/1* | false/1* | false/1 | **true/0** | **KILLED** (real tree + stubF) |

Bold = differs from pristine. \* m6's stubA–D lines also differ textually from
pristine (`selftest=unparseable met=false` instead of the per-defect
annotation); the decisive flips are the real-tree false alarm and the stubF
miss. Exact lines for every cell are in
`/fast/scratch/hyaku/kake-r63/MutC2Counter/results.tsv`; example killers:

```
m1 stubA exit=0 … selftest=4/4 frozen_cases=missing met=true      (pristine: exit=1 met=false)
m2 stubB exit=0 … selftest=4/4 frozen_cases=ok met=true           (pristine: exit=1 frozen_cases=missing met=false)
m3 stubC exit=0 … selftest=3/4 frozen_cases=ok met=true           (pristine: exit=1 met=false)
m4 stubD exit=0 … selftest=3/3 frozen_cases=ok met=true           (pristine: exit=1 met=false)
m5 stubE exit=0 … selftest=4/4 frozen_cases=ok met=true           (pristine: exit=1 selftest=failed met=false)
m6 real exit=1 … selftest=unparseable met=false                   (pristine: exit=0 selftest=4/4 frozen_cases=ok met=true)
m6 stubF exit=0 … selftest=4/4 frozen_cases=ok met=true           (pristine: exit=1 selftest=unparseable met=false)
```

## Verdict and coverage notes

6/6 mutants killed; no survivor; no inconclusive verdict (baseline held). Every
check in the counter's `met` conjunction is load-bearing:

- The frozen-case-set check (m1) and the `derived == expected` clause (m2) are
  independently exposed — dropping either turns a defective tool's green
  (`stubA`/`stubB`) into `met=true` exit 0, i.e. the C2 kill rule's "a stub
  tool passes" scenario.
- `total == passed` (m3) and `total == len(FROZEN_CASE_IDS)` (m4) each catch a
  distinct summary lie (3/4 and 3/3-with-total≠4).
- The returncode gate (m5) is invisible on a healthy tree (the real tool exits
  0, so m5's real-tree output is byte-identical to pristine) — it is only
  observable against a seeded nonzero-exit tool. Detectors that only ever run
  the counter on healthy trees cannot distinguish m5; the stub run is what
  kills it.
- m6 (stderr parse) is killed twice over: it false-alarms on the healthy tree
  (`met=false` where the frozen predicate demands `met=true`) and waves through
  the JSON-on-stderr tool.

All runs executed with Python 3.14.8; invocation mirrors the contract counting
command (`python3 -B … --root … --revision …`).

## Restoration and cleanup evidence

- Fleet counter sha256 after = `9fcbfad06fe6abed2b23556894879491204a1ef4d2b9f3cf194a9a3aeaa7f01e` (before = same; never modified).
- Fleet worktree tool sha256 after = `431e75e8fee2c913c6fa74aebbf7cb2e678f139a1a37b3d38994d1bb22841f14` (before = same).
- Pristine scratch copy sha256 after = `9fcbfad0…` (before = same; mutants live only in `mutants/m1..m6.py`).
- Fleet HEAD after = `15eb965c1d0f23ce2a522c651e9306a0952da7d3` (before = same); no git/jj mutation anywhere in the fleet repo.
- Fixture repo `/fast/scratch/hyaku/kake-r63/MutC2Counter/stubrepo` deleted and confirmed absent after the runs (stub revs recorded above in case of audit).
- Tooling installs: none. pacman: none. Files written outside scratch: only this report.

Report: .ufo/waves/round-63/w1/MutC2Counter.md
