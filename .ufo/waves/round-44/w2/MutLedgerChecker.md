# MutLedgerChecker — mutation probe of `scripts/ledger_latest_check.py` (round 44, wave 2)

Seat: `MutLedgerChecker` (mutation-tester, lane `kake-shokunin`, axes: operability, freshness).
Scratch: `/fast/scratch/hyaku/kake-r44/MutLedgerChecker/`.
Target: `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/ledger_latest_check.py` — **read only; never edited.**
Lane file sha256 before **and** after the whole probe: `50384505b981352b691f24fbdd66c521c18b80408aeed4bbb54c70f8903f63dd` (unchanged).

## Axes named

1. **operability** — does the checker's own detector actually *fail* when the checker is wrong, i.e. is
   `--selftest` an able-to-fail gate for the C2 freshness claim?
2. **freshness** — does the checker detect a stale ledger figure (the round-43 `T5 1.13–1.18` value)
   when that stale statement is the *last* one in the file?

## What I did

Copied the checker into scratch (never the lane file), built five self-contained git fixture trees
(each carries the round-43 receipts on `master`), and applied four mutants at the smallest
behaviour-bearing point. Every mutant was run against **the same** bounded detector, on pristine,
mutated and restored bytes.

### Detector design (the load-bearing part)

The shipped `--selftest` is thin: it exercises only `latest_match()` + `evaluate()` on a single
integer figure (`rescore-tally`, quoted `14` vs derived `14`). It therefore cannot reach the
contract shape, the rounding decision, or the end-to-end `run_check()` path. I built **two** detector
flavours and report both:

* **shipped** — the lane's own `--selftest`, byte-for-byte unmodified. Applied to the mutation alone
  on pristine lane bytes (`m*/shipped/`).
* **ext** — a scratch copy whose `--selftest` keeps both shipped fixtures **verbatim** and adds seven
  behaviour checks (containment, rounding, contract shape, and three end-to-end fixture-tree
  verdicts). The extension block is **byte-identical** in the pristine extended copy and in every
  mutant (`detector_block_identical_in_all_mutants: true` in `verification.json`), so the detector
  is fixed across the entire run. No lane file was touched; `ext/` exists only in scratch.

## (a) Original `--selftest` exits 0 — **PASS**

```
$ python3 /fast/scratch/hyaku/kake-r44/MutLedgerChecker/orig/ledger_latest_check.py --selftest
ledger_latest_check --selftest
  PASS matching fixture MATCH quoted=14 derived=14
  RED MISMATCH mismatching fixture quoted=18 derived=14
selftest: 2/2 passed
exit=0
```

The lane file is byte-identical to `orig/` (same sha256), so this is the shipped checker's own result.

## (b) Four mutants — every one killed — **PASS**

Baseline first: the pristine **extended** copy passes its own detector (`selftest: 9/9 passed`, exit 0),
so a mutant failure is a real kill and not a broken baseline.

| mutant | mutation (one point) | ext `--selftest` | shipped `--selftest` | verdict |
|---|---|---|---|---|
| **m1** | `evaluate()`: `quoted == derived` → containment (`all(d in q for d, q in zip(derived, quoted))`) | **exit 1** (7/9) | exit 0 (2/2) | **KILLED** by ext; survives the shipped selftest |
| **m2** | `latest_match()`: `matches[-1]` → `matches[0]` (first match, not last) | **exit 1** (6/9) | **exit 1** (0/2) | **KILLED** by both |
| **m3** | `contract_spec()`: drop the `build-ratio-range` figure | **exit 1** (4/9) | exit 0 (2/2) | **KILLED** by ext; survives the shipped selftest |
| **m4** | `evaluate()`: accept a quote equal to the receipt value **truncated** (`ROUND_DOWN`) as well as `ROUND_HALF_UP` | **exit 1** (7/9) | exit 0 (2/2) | **KILLED** by ext; survives the shipped selftest |

Decisive output, m1 (extended detector; the two failing checks are the containment check and the
end-to-end superstring tree):

```
$ python3 .../m1/ext/ledger_latest_check.py --selftest
ledger_latest_check --selftest
  PASS matching fixture MATCH quoted=14 derived=14
  RED MISMATCH mismatching fixture quoted=18 derived=14
  FAIL containment-not-equal fixture - quoted 114 must not be accepted as the receipt-derived 14
  PASS rounded-differently fixture - quoted 7.04 must not be accepted for the receipt value 7.047
  PASS three-figure-contract fixture - the fixed contract must carry all three figures
  PASS good-tree-clean fixture - the good fixture tree must check clean
  FAIL superstring-tree-rejected fixture - the superstring fixture tree must be rejected
  PASS rounded-tree-rejected fixture - the rounded fixture tree must be rejected
  PASS rounded2-tree-rejected fixture - the rounded2 fixture tree must be rejected
selftest: 7/9 passed
exit=1
```

m2 — the two shipped fixtures already flip (it now takes the *first* statement, so `18` is read where
`14` is correct, and vice versa):

```
$ python3 .../m2/ext/ledger_latest_check.py --selftest
ledger_latest_check --selftest
  FAIL matching fixture MISMATCH quoted=18 derived=14
  FAIL mismatching fixture MATCH quoted=14 derived=14
  ...
  FAIL good-tree-clean fixture - the good fixture tree must check clean
selftest: 6/9 passed
exit=1
```

m3 — the contract no longer carries three figures, and the checker refuses to run against the
committed three-figure spec:

```
$ python3 .../m3/ext/ledger_latest_check.py --selftest
ledger_latest_check --selftest
  PASS matching fixture MATCH quoted=14 derived=14
  RED MISMATCH mismatching fixture quoted=18 derived=14
  PASS containment-not-equal fixture - quoted 114 must not be accepted as the receipt-derived 14
  PASS rounded-differently fixture - quoted 7.04 must not be accepted for the receipt value 7.047
  FAIL three-figure-contract fixture - the fixed contract must carry all three figures
  FAIL good-tree-clean fixture - the good fixture tree must check clean (raised InputError: ledger quote spec differs from the fixed three-figure contract)
  FAIL superstring-tree-rejected fixture - ... (raised InputError: ledger quote spec differs from the fixed three-figure contract)
  FAIL rounded-tree-rejected fixture - ... (raised InputError: ledger quote spec differs from the fixed three-figure contract)
  FAIL rounded2-tree-rejected fixture - ... (raised InputError: ledger quote spec differs from the fixed three-figure contract)
selftest: 4/9 passed
exit=1
```

m4 — a quote rounded *differently* from the receipt is accepted:

```
$ python3 .../m4/ext/ledger_latest_check.py --selftest
ledger_latest_check --selftest
  PASS matching fixture MATCH quoted=14 derived=14
  RED MISMATCH mismatching fixture quoted=18 derived=14
  PASS containment-not-equal fixture - quoted 114 must not be accepted as the receipt-derived 14
  FAIL rounded-differently fixture - quoted 7.04 must not be accepted for the receipt value 7.047
  PASS three-figure-contract fixture - the fixed contract must carry all three figures
  PASS good-tree-clean fixture - the good fixture tree must check clean
  PASS superstring-tree-rejected fixture - the superstring fixture tree must be rejected
  PASS rounded-tree-rejected fixture - the rounded fixture tree must be rejected
  FAIL rounded2-tree-rejected fixture - the rounded2 fixture tree must be rejected
selftest: 7/9 passed
exit=1
```

### The mutants really do weaken the verdict end-to-end (not just the unit check)

m1 accepts a *containment* of the receipt value — the ledger says `re-scored 114 of the 27`, the
receipt says `14`:

```
$ python3 .../m1/ext/ledger_latest_check.py --root .../trees/superstring
rescore-tally MATCH quoted=114 derived=14 SCORECARD.md:6
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:7
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:5
ledger-quotes: 3 figures, 0 mismatches
exit=0        <-- WRONG: the stale 114 passes

$ python3 .../orig/ledger_latest_check.py --root .../trees/superstring
rescore-tally MISMATCH quoted=114 derived=14 SCORECARD.md:6
...
ledger-quotes: 3 figures, 1 mismatches
exit=1        <-- correct
```

m4 accepts a value rounded the other way — the ledger says `T1 4.20, T5 7.04`, the receipt says
`4.207` / `7.047`:

```
$ python3 .../m4/ext/ledger_latest_check.py --root .../trees/rounded2
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:6
donothing-ratios MATCH quoted=T1 4.20, T5 7.04 derived=T1 4.21, T5 7.05 LOG.md:7
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:5
ledger-quotes: 3 figures, 0 mismatches
exit=0        <-- WRONG: the mis-rounded quote passes

$ python3 .../orig/ledger_latest_check.py --root .../trees/rounded2
donothing-ratios MISMATCH quoted=T1 4.20, T5 7.04 derived=T1 4.21, T5 7.05 LOG.md:7
...
ledger-quotes: 3 figures, 1 mismatches
exit=1        <-- correct
```

m2 on the *good* tree reports the earlier (superseded) statements as the latest ones:

```
$ python3 .../m2/ext/ledger_latest_check.py --root .../trees/good
rescore-tally MISMATCH quoted=18 derived=14 SCORECARD.md:3
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:7
build-ratio-range MISMATCH quoted=T1 1.00–1.01, T5 1.13–1.18 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:3
ledger-quotes: 3 figures, 2 mismatches
exit=1
```

m3 against the committed three-figure spec refuses to run (exit 2) — the spec-equality guard is real:

```
$ python3 .../m3/ext/ledger_latest_check.py --root .../trees/good
ledger_latest_check: unreadable input: ledger quote spec differs from the fixed three-figure contract
exit=2
```

### Coverage finding on m3 (mutation, not a defect)

`m3` as specified (drop a figure from `contract_spec()` only) is caught by the checker's own
`load_spec()` guard, so it can never run. The genuinely dangerous variant drops the figure from
**both** `contract_spec()` and the on-disk `ledger-quotes.json`; then the checker happily verifies a
two-figure contract and silently stops checking the third figure:

```
$ python3 .../m3b/ledger_latest_check.py --root .../m3b/tree     # two-figure spec on disk
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:6
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:7
ledger-quotes: 2 figures, 0 mismatches
exit=0        <-- the build-ratio-range figure is no longer checked at all

$ python3 .../orig/ledger_latest_check.py --root .../m3b/tree     # same tree, pristine checker
ledger_latest_check: unreadable input: ledger quote spec differs from the fixed three-figure contract
exit=2        <-- correct: the two-figure spec is refused
```

This is a property of the *spec file*, not of the checker bytes: `load_spec()` compares the on-disk
JSON with the fixed contract, so the third figure can only be dropped by editing the committed
`ledger-quotes.json` as well. Recorded as a coverage observation, not a request to change the
contract.

## (c) Crafted stale LOG.md — original checker exits nonzero — **PASS**

Root handling, read from the source before probing: `--root` is resolved with `Path(...).resolve()`;
`SPEC_PATH` is read from **disk** at `<root>/.ufo/waves/round-44/ledger-quotes.json`; the ledgers are
read from **disk** at `<root>/LOG.md` / `<root>/SCORECARD.md` if present, otherwise from
`git show master:<path>`; the **receipts always come from `git show master:<path>`** inside
`<root>`. So a usable `--root` is a git repo whose `master` carries the round-43 receipts, with the
spec JSON and the ledgers on disk.

The crafted `trees/stale/LOG.md` ends with the stale build-range statement, **EN-DASH U+2013**
(verified: 4 × U+2013 in the file; `cat -A` shows `M-bM-^@M-^S`):

```
Latest build statement (stale, as written at round 43): build `020bc457` met x3 (T1 1.00–1.02, T5 1.13–1.18).
```

```
$ python3 /fast/scratch/hyaku/kake-r44/MutLedgerChecker/orig/ledger_latest_check.py \
      --root /fast/scratch/hyaku/kake-r44/MutLedgerChecker/trees/stale
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:6
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:7
build-ratio-range MISMATCH quoted=T1 1.00–1.02, T5 1.13–1.18 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:5
ledger-quotes: 3 figures, 1 mismatches
exit=1
```

The stale `T5 1.13–1.18` is rejected, the other two figures still match, and the exit code is
nonzero. The original checker against the **live lane** still exits 0 (claim C2 unaffected):

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin && python3 scripts/ledger_latest_check.py --root .
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3576
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1703
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1705
ledger-quotes: 3 figures, 0 mismatches
exit=0
```

### Root handling proven by a disk/master split

Two trees, identical receipts, differing only in which side carries the stale range:

* `trees/stale-disk` — `master` carries the **current** range, the **on-disk** LOG.md carries the
  stale one → checker reads the **disk** statement and exits 1 (`build-ratio-range MISMATCH
  quoted=T1 1.00–1.02, T5 1.13–1.18`).
* `trees/stale-master` — `master` carries the **stale** range, the **on-disk** LOG.md carries the
  current one → checker reads the **disk** statement and exits **0**.

So ledgers come from disk and only the receipts come from `master` — exactly as the source says, and
the stale-on-disk case is the one that must fail.

## Restoration evidence

* Lane file sha256 before = after = `50384505b981352b691f24fbdd66c521c18b80408aeed4bbb54c70f8903f63dd`
  (`lane_unchanged: true`). No lane file was written at any point.
* The pristine extended copy is a pure function of the lane bytes; regenerating it reproduces
  `b015c013c6b194904eb725aa4f2d2dca4c7c48ddb7f12ee8f2c1056e01e3022f` — identical to the copy used in
  the run (`ext_restored: true`).
* Every mutant file was regenerated from the pristine bytes and compared with the bytes actually
  exercised: `m1_shipped_identical`, `m2_shipped_identical`, `m3_shipped_identical`,
  `m4_shipped_identical` and the four `*_ext_identical` flags are all `true`
  (`verification.json`).
* The detector block is byte-identical in the pristine extended copy and all four mutants
  (`detector_block_identical_in_all_mutants: true`).

## Files written (all in scratch; nothing else in the lane)

Scratch dir `/fast/scratch/hyaku/kake-r44/MutLedgerChecker/`:

* scripts — `setup_trees.py` (fixture-tree builder), `make_mutants.py` (copy + mutant generator, also
  holds the extension text), `run_matrix.py` (matrix runner), `probe_m3b.py` (m3b probe),
  `probe_stale.py` (part-c probe + disk/master split), `verify.py` (restoration + matrix verifier).
* checker copies — `orig/ledger_latest_check.py` (byte-identical to the lane file),
  `ext/ledger_latest_check.py` (pristine extended),
  `m1/shipped/`, `m1/ext/`, `m2/shipped/`, `m2/ext/`, `m3/shipped/`, `m3/ext/`,
  `m4/shipped/`, `m4/ext/` (`ledger_latest_check.py` in each), plus `m3b/ledger_latest_check.py`.
* fixture trees — `trees/good`, `trees/stale`, `trees/superstring`, `trees/rounded`, `trees/rounded2`,
  `trees/stale-disk`, `trees/stale-master` (each a git repo with the round-43 receipts on `master`,
  plus the on-disk spec JSON and ledgers), and `m3b/tree/` (two-figure spec).
* results — `manifest.json`, `results.json`, `verification.json`, `m3b.json`, `stale_probe.json`,
  and 61 verbatim capture files under `out/`.

This report: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w2/MutLedgerChecker.md`.

## Blockers / dead ends

* None. No tool installs were needed (python 3.14.8 and git 2.56.0 were already present); no pacman
  transaction was attempted.
* The lane's `scripts/ledger_latest_check.py` is **untracked** in the lane repo (`git status` shows
  `?? scripts/ledger_latest_check.py`), so it has no committed history to diff against — the pristine
  baseline is the working-tree bytes, and that is what every copy was made from.
* The one thing the shipped `--selftest` cannot do is kill m1, m3 or m4; that is a property of the
  shipped detector's reach (one integer figure), and it is why this probe also ran the extended
  detector. The lane file itself was **not** modified.

## Verdict

* (a) original `--selftest` exits 0 — **PASS**.
* (b) all four mutants make the copy's `--selftest` exit nonzero — **PASS** (m1/m2/m3/m4 → 7/9, 6/9,
  4/9, 7/9 passed, exit 1 each; baseline 9/9, exit 0). m1, m3 and m4 additionally **survive the
  shipped `--selftest`** — recorded as a coverage finding.
* (c) the original checker exits nonzero against a crafted scratch tree whose last build-range
  statement is the stale `T5 1.13–1.18` (EN-DASH) — **PASS** (exit 1, `build-ratio-range MISMATCH`).
* Restoration — **PASS** (lane file byte-identical before/after; every copy regenerable and hash-equal).
