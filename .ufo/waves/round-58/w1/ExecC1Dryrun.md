# ExecC1Dryrun

Claim C1 landing dry run (the round-57 D1 failure mode): simulate the T0/T1 landing — ledger + `after-c2-*/after-c3-*`
receipts at T0, run the C1 counter there, commit its output as `controls/after-c1-receipt-rewrites.txt` (T1), rerun —
then the two post-landing rewrite hazards (this round's C1 receipt, `census-before.txt`) and the SCORECARD/LOG/report
commits after T1. Everything ran in one throwaway shared clone; all receipts are copied beside this report in
`ExecC1Dryrun.files/` (each file is that step's verbatim `--list` stdout).

**Not run, declared:** the C2 and C3 counters were not executed (not this seat's scope). The two after-receipts in the
dry run carry synthetic content (`C2 ... cases_passed=12 of 12 met=True`, `C3 ... conditions_passed=8 of 8 met=True`);
the C1 counter reads them only as tip tree entries, never their bytes. No tool was installed (git/python3 present).

## SEQUENCE:

Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/kake-shokunin /fast/scratch/hyaku/kake-r58/ExecC1Dryrun/clone`,
`git -C clone rev-parse --show-toplevel` = the clone; started branch `dry` at lane tip `cc8da16` (base `0440485` + contract
`fff3eea` + spec `cc8da16` — the tree a landing begins from; nothing in w1 is committed, so this equals "base + round-58
freeze"). All commits below use `-c user.name=selftest -c user.email=selftest@local`.

| # | commit | command | result |
|---|---|---|---|
| S0 | `0440485` | `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root <clone> --revision 0440485 --list` | `events=19 undisclosed=19 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=0 met=False`, EXIT=1; its header + 19 `UNDISCLOSED` lines diff **identical** to the committed `controls/base-c1-receipt-rewrites.txt` (clone fidelity: BASE-REPRODUCED-IDENTICAL) |
| S0b | — | `... --selftest` | 18/18 PASS, exit 0 (`step0-base` companion in .files) |
| S1 | — | `python3 -B .ufo/waves/round-58/w1/ExecLedgerBuild.files/build_ledger.py --root <clone> --revision cc8da16 --note 'see {path}' --out <clone>/.ufo/waves/round-58/receipt-rewrites.json` | `wrote ...: 19 events`; kinds `relabel=12 rerun=6 fill=1`; note sample `see .ufo/waves/round-52/control/c1-mutation-ladder.json` |
| S2 | T0 `7336f7c` | commit ledger + `after-c2-resolver-cases.txt` + `after-c3-quote-truth.txt`; counter at T0 | `events=19 undisclosed=0 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=2 met=True`, EXIT=0 |
| S3 | T1 `26b1d2c` | counter at T0 `--list` → `controls/after-c1-receipt-rewrites.txt`, append `EXIT=0`, commit that one path; rerun at T1 | `events=19 undisclosed=0 … new_rewritten=0 new_receipts=2 met=True`, EXIT=0 (the receipt's first addition is not an event) |
| S4 | T1b `0a7d7a8` | append a line to `SCORECARD.md` and `LOG.md`, add `.ufo/waves/round-58/w1/ExecC1Dryrun.md`, commit | `events=19 undisclosed=0 … met=True`, EXIT=0 — **unchanged** (no receipt path touched) |
| S5 | T2 `b06e874` | append one line to `controls/after-c1-receipt-rewrites.txt`, commit | `events=20 undisclosed=1 … new_rewritten=1 met=False`, EXIT=1; names `M .ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt c09ced5cff89 -> 11cfb1f27ab2` |
| S6 | T3 `474af1b` | append one line to `controls/census-before.txt`, commit | `events=21 undisclosed=2 … new_rewritten=2 met=False`, EXIT=1 |
| S7 | T4 `0222160` | rebuild the ledger at T3 (21 entries) and commit — the round-58 rewrites are now *disclosed* | `undisclosed=0 … new_rewritten=2 met=False`, EXIT=1 (disclosure does not rescue a round-58 rewrite) |
| S8 | `411db8d`→`209f243` | branch from T1: append to round-57 `controls/after-c1-receipt-pins.txt`, commit; then ledger reissued | stale ledger: `events=20 undisclosed=1 met=False` EXIT=1; reissued: `events=20 undisclosed=0 met=True` EXIT=0 |
| det | — | two consecutive `--revision 7336f7c --list` runs | byte-identical (`cmp` silent) |

Extra probes (all in .files):

| # | setup | result |
|---|---|---|
| P2 | incremental landing: ledger only / +C2 receipt / +C3 receipt | `new_receipts=0 met=False` / `=1 met=False` / `=2 met=True` (exit 1,1,0) |
| P3 | single commit: ledger + C2 + C3 receipts (met), then C1 receipt `commit --amend`ed into that same commit | `met=True`, EXIT=0 both before and after the amend |
| P4 | a second file `controls/after-c2-resolver-cases-rerun.txt` | `new_receipts=3 met=False`, EXIT=1 |
| P5 | `git mv` of the C1 receipt after T1 (rename = delete+add) | `events=20 undisclosed=1 new_rewritten=1 met=False`, EXIT=1 |
| P6 | ledger copied verbatim from the sibling's `ExecLedgerBuild.files/receipt-rewrites.json` (builder default `--note TODO`) | `unpointed=19 met=False`, EXIT=1 |
| P7 | ledger built at the pre-T0 tip while the same commit also appended to round-56 `c2-selftest.txt` | `events=20 undisclosed=1 met=False`; rebuilt at the final tip → `undisclosed=0 met=True` |
| P8 | C1 re-run receipt under a new name `after-c1-receipt-rewrites-rerun.txt`; then edit it | `met=True` EXIT=0; after the edit `new_rewritten=1 met=False` EXIT=1 |

## BREAKS:

No deviation from `contract.md`/`PREDICATE` was observed: every counter run (23 measured runs kept in .files, plus one
discarded probe run) gave the exit code and the exact counters the contract predicts for its state. What the sequence *does* establish as landing constraints (counter working as
written, not defects):

1. **The ledger must be built at the final T0 tip, with a note template.** The sibling candidate as produced
   (`--note TODO`) fails `unpointed=19` (P6); `--note 'see {path}'` passes (`pointed()` accepts any repo-relative path
   present at the tip, or a resolvable 7–40 hex id). A build commit that itself touches an old receipt after the ledger
   was generated makes that event `undisclosed` (P7). The `see <path>` note is the minimum the counter accepts; whether
   the prose is *true* is reviewer-checked, so the final notes should be real disclosure sentences (C1's stated limit).
2. **`new_receipts` is exactly 2 and file-name driven.** A third `after-c2-*`/`after-c3-*` file (e.g. a re-run kept
   beside the first) yields 3 → `met=False` (P4). `after-c1-*` files are exempt, so C1 re-runs must use a new name (P8a)
   and then must not be edited (P8b).
3. **Ledger `kind` must be the counter's classification, not the contract prose.** `classify()` labels 12 of the 19
   historical events `relabel` (every changed line carries a 40-hex id or a `revision` key); the contract prose names 6
   disclosed revision relabels. `[INFERENCE]` the 6 are a subset of the 12 — a hand-typed ledger that takes kind from the
   prose would produce `wrong_kind`. Using the builder (which imports the counter) removes this class entirely.
4. **Only `.ufo/waves/round-<N>/control(s)/<file>` is a receipt.** SCORECARD.md, LOG.md and `w1/<Seat>.md` commits after
   T1 move nothing (S4); non-receipt `.ufo/waves/.../w1/` files are invisible to `events()`.
5. **Disclosure never launders a round-58 rewrite** (T4: `undisclosed=0 new_rewritten=2`, exit 1) and **rename == loss**
   (P5). Conversely a *historical* rewrite that is disclosed and has its ledger reissued still meets (S8), and
   squashing everything into one commit before the measurement is safe (P3).
6. Own-harness note, disclosed for honesty: my first stale-ledger probe used `git revert` of the disclosure commit; the
   revert did not apply and the fallback made a noop commit, which left the 20-entry ledger in place and therefore still
   met. The stale-ledger expectation was then verified at `411db8d` (19-entry ledger, `undisclosed=1`).

## RECOMMENDED LANDING ORDER:

1. Land the build content first (id_resolver fix, counters, entries, SOURCES/registry rows, lesson): none of those paths
   is a receipt, so none is a C1 event. Any pre-measurement squash is safe (P3).
2. Run the C2 counter → `controls/after-c2-resolver-cases.txt`, the C3 counter → `controls/after-c3-quote-truth.txt`.
   Exactly those names, exactly one file each (`new_receipts == 2`); intermediate tips may fail on `new_receipts` alone
   (P2) — only the measured tip must hold both.
3. With every other T0 file already in place, build the ledger from the **final** tip:
   `python3 -B .ufo/waves/round-58/w1/ExecLedgerBuild.files/build_ledger.py --root . --revision HEAD --note 'see {path}' --out .ufo/waves/round-58/receipt-rewrites.json`
   (or the same with real disclosure prose in `--note`). Never keep the default `TODO` notes.
4. Measure: `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision HEAD --list` → require `met=True`
   / exit 0. If it is not 0, commit no C1 receipt at all; fix and rebuild the ledger, then measure again.
5. Write the receipt from that run and commit it once:
   `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision HEAD --list > .ufo/waves/round-58/controls/after-c1-receipt-rewrites.txt` plus `EXIT=$?`; `git add` that single path; commit.
6. Re-measure at the new tip (expect `events` unchanged, `new_rewritten=0`, `met=True`). Any later C1 re-run goes to a
   **new** file name (`after-c1-receipt-rewrites-rerun.txt` passes, P8a) and is then itself never edited.
7. After T1, commit only non-receipt paths (SCORECARD, LOG, `w1/*.md`, `w1/<Seat>.files/`). Never modify, rename or
   delete anything under any `.ufo/waves/round-*/control(s)/` — that includes `census-before.txt` and the base receipts.

VERDICT: the landed T0/T1 sequence measures met at T0 and again at T1, this round's C1 receipt rewrite fails with new_rewritten=1, a census-before.txt rewrite fails, SCORECARD/LOG/report commits after T1 change nothing, and the three hazards a hand-built landing can still trip (TODO notes, a third after-c2/c3 file, a ledger built before the build commit) are each measured.
