# W2 mutation report — C1 citing-set gate repairs (71c6bfa)

Seat: `KakeR30.MutGateRepeatsWalkTty` (mutation tester, wave 2, falsify).
Target: the four repairs landed in `scripts/citing_set.py` at
`71c6bfabd7aa957d15732d9224888bb32849238a` — store-once options, abbreviation
handling, iterative corpus walk, `O_NOCTTY`.
Sandbox: `/fast/scratch/hyaku/kake-r30/w2/MutGateRepeatsWalkTty/`.
The lane repository was read only; its `scripts/citing_set.py` and
`scripts/citing_set_selftest.py` are byte-identical before and after
(sha256 `dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02`).

## Commands run (exit codes)

    python3 -B .ufo/waves/round-30/c1_reason_count.py --root . --revision 71c6bfab... --scratch <sandbox>/scratch/counter   # exit 0
      -> "C1 14/14 at 71c6bfabd7aa957d15732d9224888bb32849238a (controls True, constant gates rejected True)"
    python3 -B .ufo/waves/round-30/c1_strict_checks.py --root . --revision 71c6bfab... --scratch <sandbox>/scratch/strict    # exit 0
      -> "C1 strict 6/6 ... {'S1': True, 'S2': True, 'S3': True, 'S4': True, 'S5': True, 'S6': True}"
    python3 -B probe.py                                                                                                  # exit 0

`probe.py` (sandbox) exports `scripts/` at 71c6bfa, builds one mutated tree per
mutant, and for every tree (pristine + 4) runs the committed runner, the
declared counter's own case builders (`behaviour_cases`, `family_cases`,
`controls`) and the strict supplement's `S1/S3/S4/S5/S6`.

## Mutant ledger

| id | mutation | gate sha256 (16) | committed runner | declared counter | strict supplement | verdict |
|----|----------|------------------|------------------|------------------|-------------------|---------|
| — | pristine 71c6bfa | dbfade45e59351fb | exit 0, 41 cases, 0 failed | 14/14 | 6/6 | baseline |
| M1 | store-once on one option only (`--ledger` loses `StoreOnce`) | 5cc6781e0e5c183 | exit 0, 41/41 pass | 13/14, F04 fails (`exit 0, want 64`) | 5/6, S3 fails on `--ledger twice`, `--ledger=value twice`, `--ledger mixed`, `--ledger abbreviated` (all exit 0) | killed by both counters; **survives the committed runner** |
| M2 | abbreviations allowed again (`StoreOnce` dropped, repetition detected by exact option name, argparse default `allow_abbrev`) | f4689203952283d | exit 0, 41/41 pass | **14/14, survives** | 5/6, S3 fails on all four `… abbreviated` variants (exit 0, no usage object) | **survives the declared counter**; killed only by the strict supplement |
| M3 | corpus walk made recursive again (`_walk`) | 802760f39b163560 | exit 0, 41/41 pass | 13/14, F05 fails (`stdout is not one JSON object`, `traceback on stderr`) | 5/6, S4 fails (no finding, exit 1) | killed by both counters; **survives the committed runner** |
| M4 | `O_NOCTTY` dropped from the document open | 758c4129f43feaa | exit 0, 41/41 pass | 13/14, F06 fails (`tty_nr 34817 after the run, want 0`) | 5/6, S5 fails (`device opened without O_NOCTTY: [['/dev/pts/1', 526336]]`, `tty_nr 34817`) | killed by both counters; **survives the committed runner** |

Direct observations (same tree, three spellings of the same repeated option):

    --revision HEAD --rev HEAD   pristine exit 64 (usage JSON)   M2 exit 0, verdict clean
    --rev HEAD --revision HEAD   pristine exit 64 (usage JSON)   M2 exit 0, verdict clean
    --ledger missing --ledger ledger.json   pristine exit 64   M1 exit 0, verdict clean (last value kept)
    1000-deep corpus             pristine exit 1 + JSON report  M3 exit 1, stdout empty, RecursionError traceback

## Fixture coverage gap list

Committed fixtures: 41 cases; expected exits are only 0 (5), 1 (22), 2 (14) —
**no fixture carries exit 64**. Only fixtures 36 and 37 use `case.json`
`argv`, and neither repeats an option.

1. Repeated valued option → exit 64: **no committed fixture**. Guarded only by
   the round counters (declared F04, strict S3). The runner can express it
   today with `case.json` `argv` (no new setup op needed) — this gap is free to
   close.
2. Abbreviation spelling of the repeat rule (`--rev x --revision HEAD`, named in
   the gate docstring and in the declared interface): **no committed fixture and
   no case in the declared counter** (F04 uses exact option names only). It is
   guarded only by the strict supplement's S3, which is not the counter named in
   C1's claim. Measured gap: the declared counter scores **14/14 on a gate that
   silently accepts the forbidden spelling** (exit 0, verdict clean).
3. Iterative corpus walk (1000 levels deep): **no committed fixture**. Guarded
   only by declared F05 and strict S4; the runner can only reach it by
   committing a 1000-level fixture tree.
4. `O_NOCTTY` on the document open: **no committed fixture**. Guarded only by
   declared F06 and strict S5; the runner's setup vocabulary
   (`mkdir`, `fifo`, `git_init`, `git_commit`) has no pty op, so the committed
   runner cannot express it without extending the runner.

**Answer to the asked question:** all four repairs — repeated-option refusal,
the abbreviation spelling of it, the iterative walk and `O_NOCTTY` — have **no
committed fixture**; every one of them is guarded only by the round counters,
and the abbreviation spelling is guarded only by the strict supplement, not by
the declared counter.

## Evidence pointers

- driver: `/fast/scratch/hyaku/kake-r30/w2/MutGateRepeatsWalkTty/probe.py`
- full results: `…/probe-results.json`; summary `…/probe-summary.json`
- pristine counter run: `…/counter-pristine.json` (exit 0); strict: `…/strict-pristine.json` (exit 0)
- mutant gates: `…/work/tree-M{1,2,3,4}/scripts/citing_set.py` (sha256 in the ledger)
- counter sources used read-only from the lane: `.ufo/waves/round-30/c1_reason_count.py`,
  `.ufo/waves/round-30/c1_strict_checks.py`

Not verified: I did not run the lane's other suites, did not exercise the mutants
outside the counters' cases, and did not change the gate, the fixtures or the
contract. A surviving mutant is a coverage finding only — I make no claim about
the intended contract. No tool was installed or upgraded in this seat.
