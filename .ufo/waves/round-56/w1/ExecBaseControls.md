# ExecBaseControls

Replication of the frozen round-56 base controls for C1 (`c56_selftally.py`) and C2 (`c56_quote_truth.py`) in a
throwaway clone of the lane checked out at contract commit `2d308e808bfd`, measuring base revision
`e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`. Every command below was run; none is unrun.

Lane bounds: the only file written in the lane is this report. No lane entry, registry, README, jj state or git index
touched; no `git add/commit/stash/checkout/reset/pull/push` in the lane; no subagent dispatched; no campaign tool run in
shokuknow; no tool installed or upgraded (none needed). All scratch is outside the lane.

## SETUP (read-only clone, not a counter run)

`D=$(mktemp -d /tmp/execbase.XXXXXX)` → `/tmp/execbase.89G9EN`; `git clone -q --no-checkout <lane> "$D"`;
`git -C "$D" checkout -q 2d308e808bfd`; `rev-parse HEAD` → `2d308e808bfdabced268294ff823fb6acce9e02e`;
`rev-parse --show-toplevel` → `/tmp/execbase.89G9EN` (equals `$D`); `status --porcelain | wc -l` → 0.

Measured blobs at `2d308e8` (`git ls-tree`): `c56_selftally.py` `12514d96…b241434`, `c56_quote_truth.py`
`f65ed0f2…b4056faf`, `base-c1-selftally.txt` `68feb110…ea8e2a0c`, `base-c2-quote-truth.txt` `997bdd71…db1001c6`.
The clone's tree comes from the commit, so the lane worktree's in-flight `M c56_quote_truth.py` (a sibling's edit, not
mine) cannot leak into these runs. Lane tip at run time `6b3df99d…1e9be75`; clone left at `2d308e8`. Scratch output
dir `/tmp/execbaseout.9qrCEy`.

## COMMANDS:

**1. C1 base run** (cwd `/tmp/execbase.89G9EN`, wall 94.89 s, 600 s budget) — exit **1**, 13 stdout lines, stderr empty
```
python3 -B .ufo/waves/round-56/c56_selftally.py --root /tmp/execbase.89G9EN \
  --revision e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6      # -> c1-base.out
```
first 3:
```
C1 selftest-tally tally_mismatches=7 rows_checked=10 met=False  (met: tally_mismatches == 0 AND rows_checked == 10)
  base-path-audit: claim=45 observed=45/45 OK
  source-recheck-audit: claim=101 observed=106/106 MISMATCH claim_ne_observed
```
last 3:
```
  yahoo-robots-quote-truth-counter: claim=47 observed=54/54 MISMATCH claim_ne_observed
  revision: e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6
EXIT=1
```

**2. C2 base run** (cwd `/tmp/execbase.89G9EN`) — exit **1**, 31 stdout lines, stderr empty
```
python3 -B .ufo/waves/round-56/c56_quote_truth.py --root /tmp/execbase.89G9EN \
  --revision e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6      # -> c2-base.out
```
first 3:
```
C2 quote-truth 0/8 met=False  (met: conditions_passed == 8 of 8)
  C1_entries_exist FAIL
    - S367: knowledge entry corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md absent at the measured revision
```
last 3:
```
    - mirror .ufo/waves/round-56/assimilation/pre-append/corpus/SOURCES.md absent at the measured revision
  revision: e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6
EXIT=1
```

**3/4. Selftests** (cwd `/tmp/execbase.89G9EN`, stderr empty both)
```
python3 -B .ufo/waves/round-56/c56_selftally.py --selftest     -> exit 0, 1 line
c56 selftally selftest: 20/20
python3 -B .ufo/waves/round-56/c56_quote_truth.py --selftest   -> exit 2, 1 line
c56 quote-truth selftest: not yet supplied (version 1 ships without fixtures; wave 1 adds them)
```
C1's `20/20` matches the contract's "Junk controls (selftest, 20 checks)". C2's stub exit 2 matches the contract's
"version 1 ships a stub (`--selftest` exits 2)": the round-56 C2 junk-control surface is absent at base **by design**,
not a replication failure. For both, first 3 == last 3 == the single printed line.

**5. C1 base run with `--json`** (wall 62.53 s) — exit **1**, 135 stdout lines, stderr empty
```
python3 -B .ufo/waves/round-56/c56_selftally.py --root /tmp/execbase.89G9EN \
  --revision e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6 --json   # -> c1-json.out
```
first 3:
```
{
 "schema": "kake-r56-c1-selftally-v1",
 "predicate": "met: tally_mismatches == 0 AND rows_checked == 10",
```
last 3:
```
 "exit": 1,
 "met": false
}
```

**6. C2 base run with `--json`** — exit **1**, 100 stdout lines, stderr empty
```
python3 -B .ufo/waves/round-56/c56_quote_truth.py --root /tmp/execbase.89G9EN \
  --revision e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6 --json   # -> c2-json.out
```
first 3:
```
{
 "schema": "kake-r56-c2-quote-truth-v1",
 "predicate": "met: conditions_passed == 8 of 8",
```
last 3:
```
 "exit": 1,
 "met": false
}
```

## DIFFS:

Both base runs reproduce the frozen control receipts **byte for byte** (`diff -u` empty, sha256 equal):

| observed | control | sha256 | size |
|---|---|---|---|
| `c1-base.out` | `controls/base-c1-selftally.txt` | `155ab35c7c5808c0100b7fad121d22a39f6fb3cdcab7346a5385d45972b7bfb6` | 872 B |
| `c2-base.out` | `controls/base-c2-quote-truth.txt` | `3724b54573f1cebdd118179493f34bd8ccd82509bd77bb71c59e09e4de99d725` | 1649 B |

The trailing `EXIT=<code>` line is emitted by each counter's own render path, so it is inside the compared bytes, not a
harness artefact. C1 reproduces `tally_mismatches=7 rows_checked=10 met=False` with the same seven mismatching rows
(`source-recheck-audit`, `robots-expectation-audit`, `sitemap-file-audit`, `commit-citation-lint`,
`quote-truth-counter` [selftest_failed], `readme-index-counter`, `yahoo-robots-quote-truth-counter`) and the same three
OK rows (`base-path-audit`, `redirect-expectation-audit`, `wave-evidence-ledger`). C2 reproduces `0/8 met=False` with all
eight conditions FAIL and identical notes: S367 held row present but `used-by` one entry short; S419/S420 rows and all
three entries, retained bodies, receipts, the C7 validation receipt and the C8 mirror absent.

## JSON CHECK:

- C1 `--json` **parses** (`json.load`, 135 lines): `schema=kake-r56-c1-selftally-v1`,
  `predicate='met: tally_mismatches == 0 AND rows_checked == 10'` — the frozen string, identical to `contract.json`
  `claims.C1.predicate` and to the module constant at `c56_selftally.py:45`. Fields `tally_mismatches=7`,
  `rows_checked=10`, `met=false`, `exit=1`, 10 `rows` in registry order, 7 with non-empty `problems`.
- C2 `--json` **parses** (100 lines): `schema=kake-r56-c2-quote-truth-v1`,
  `predicate='met: conditions_passed == 8 of 8'` — frozen string, identical to `contract.json` `claims.C2.predicate` and
  to `c56_quote_truth.py:55`. Fields `conditions_passed=0`, `met=false`, `exit=1`.
- Both: JSON `exit` equals the process exit status (1) and `met=false` agrees with the human render, so machine and
  human surfaces of the base control agree.

## EXIT CODES:

| probe | argv after `--root /tmp/execbase.89G9EN` | exit | expected |
|---|---|---|---|
| C1 no revision | `c56_selftally.py` | **64** | 64 |
| C2 no revision | `c56_quote_truth.py` | **64** | 64 |
| C1 bad revision | `c56_selftally.py --revision deadbeef` | **2** | 2 |
| C2 bad revision | `c56_quote_truth.py --revision deadbeef` | **2** | 2 |

- no-revision: stdout empty; stderr `usage: --revision is required unless --selftest is used` (both counters).
- `deadbeef`: stdout `unevaluable: revision 'deadbeef' does not resolve in '/tmp/execbase.89G9EN'` + `EXIT=2`; stderr
  empty (both counters). The declared kill rule `0 met / 1 not met / 2 unevaluable / 64 usage` therefore holds on the
  non-measurement branches as well as on the measured one.

VERDICT: Base controls replicated exactly — both counters byte-identical to their control receipts (exit 1 each), C1 selftest 20/20 exit 0, C2 selftest stub exit 2 as contracted, both `--json` payloads parse and carry the frozen predicate strings, usage/unresolvable-revision probes exit 64/2 as declared.
