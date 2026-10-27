# ScribeLedgerR52

Seat: C1 ledger notes for the six round-52 receipt events. Lane `kake-shokunin`, base `044048597d62f3199494b63b36e90dd57825e350`, contract commit `fff3eea6aa349c8635fd84a791cc32de350ee1c2`. Read-only git only; no lane mutation, no tool installs.

## Run

Counter, run once from `/fast/scratch/hyaku/kake-r58/ScribeLedgerR52`:

```
python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/c58_receipt_rewrites.py \
  --root /home/vgpnk/Projects/shokunin/kake-shokunin \
  --revision 044048597d62f3199494b63b36e90dd57825e350
```

Observed: `C1 receipt-rewrites events=19 undisclosed=19 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=0 met=False`, exit 1; `ledger: .ufo/waves/round-58/receipt-rewrites.json absent (0 entries)`.

My six events are 4 paths across 3 commits (`1ae8de5d`, `a4a890cf`, `fd91527a`) out of those 19. Kind values below are `classify("M", oldBlob, newBlob)` executed against the counter module (not reasoned).

## EVENTS:

| path | commit | kind (counter) | what happened | disclosed at the time |
|---|---|---|---|---|
| `.ufo/waves/round-52/control/c1-mutation-ladder.json` | `1ae8de5d4dee8300624b0db2a94497ff905942c5` (2026-10-25 07:26:42, "round 52: frozen baselines and the seven measurement receipts") | relabel | **Re-run of `c52_mutation_ladder.py`**, not a text edit: blob `69a045918a98` → `9a95330d6e14`, 19 rows, `old_tail` changed in 18 of them, every other field and the whole header identical (families 18, families_caught 13, pass_fixture_agrees true, met true). `old_tail` is the *last line of the old counter's live output* (`c52_mutation_ladder.py:92`), and each fixture is a freshly built sandbox repo (`c52_wave_ledger.py:411 _selftest_repo`, no fixed author/committer date) that is `shutil.rmtree`'d on exit — so every run mints new HEAD shas. The one unchanged row is `fail_namekey`, whose tail is `KeyError: 'name'`, not a revision line. Spot-checked tails (`05643750f12344…`, `6b8627beb136a…`, `d0102c9a4ff412…`) do not resolve in the lane. No result line changed. | not disclosed as a rewrite. The freeze commit message says only that the receipts "record the real-data runs … both selftests (19/19, 18/18) and the mutation ladder (13 of 18 families)"; `corpus/lessons/round-52.md:80-84` discusses the earlier family-set change (7/18 → 13/18), not the file committed 69 seconds earlier in `73c22a3`. |
| `.ufo/waves/round-52/control/c1-ledger-real.txt` | `a4a890cf1381a194891689dcbba0bf524350926b` (07:30:04, "round 52: measured receipts, drift reconciliation, scorecard and province") | relabel | **Re-run at the newer tip**: `bd1024254674` → `ce0e0394aef9`; L1/L2/L3 still PASS, `met=True`, two `EXIT=0` lines unchanged; only the printed `revision:` line moved `3a50ae43…` → `1ae8de5d…` (the printed value is verbatim `args.revision`, so a run at `1ae8de5d` reproduces these bytes). | disclosed, generically: same commit message line 6, "C1/C2 receipts re-run at 1ae8de5". |
| `.ufo/waves/round-52/control/c1-mutation-ladder.json` | `a4a890cf1381a194891689dcbba0bf524350926b` | relabel | **Second ladder re-run** in the same commit: `9a95330d6e14` → `23252321f30d`, again 18/19 `old_tail` shas churned, zero other changes, tally still 13/18. | disclosed only by the generic "C1/C2 receipts re-run at 1ae8de5" line; the ladder file is not named, and its revision-string churn is described nowhere in round 52. |
| `.ufo/waves/round-52/control/c2-quote-real.txt` | `a4a890cf1381a194891689dcbba0bf524350926b` | relabel | **Re-run at the newer tip**: `a7b5d69484be` → `aee2e7d949ce`; C1..C8 all PASS before and after, `8/8 met=True`, both `EXIT=0`; only the `revision:` line moved `3a50ae43…` → `1ae8de5d…`. | disclosed: same "C1/C2 receipts re-run at 1ae8de5" line. |
| `.ufo/waves/round-52/control/c2-quote-selftest.txt` | `a4a890cf1381a194891689dcbba0bf524350926b` | relabel | **Selftest re-run with a new evidence revision**: `ad318495b0b7` → `907047dd6ed2`, `18/18` both sides; text moved from `(fixture revision 3a50ae4321e6)` to `(fixture revision 1ae8de5d4dee)`. `c52_quote_truth.py:466-471` takes the revision from `KAKE_R52_SELFTEST_REV` if set, else from `git rev-parse HEAD` of the run cwd, and prints `rev[:12]` (line 617); no pin existed in round 52, so the printed value is the run's HEAD — and `LOG.md` (round 56) records the pin `KAKE_R52_SELFTEST_REV=1ae8de5d4dee` being added to the round-52 row only later. | disclosed: same "C1/C2 receipts re-run at 1ae8de5" line (the selftest receipt is one of the C2 receipts). Provenance caveat: the value is env-overridable, so this file alone cannot prove a re-run. |
| `.ufo/waves/round-52/control/c1-mutation-ladder.json` | `fd91527a286086c1f4e6d4f44f715a907f041b5d` (07:45:37, "round-53: re-ground crawl source citations", empty message body) | relabel | **Third ladder re-run, committed as a pre-existing dirty working file**: `23252321f30d` → `d13c73526262`, 18/19 shas churned, 13/18 unchanged. The commit's own diffstat touches only this ladder json among round-52 files, and the lane's own round-53 lesson calls it "the inherited mutation-ladder receipt … committed as it stood; its throwaway revision strings are nondeterministic" and "this only resolves the uncommitted-file state; it does not repair the nondeterminism". | not disclosed at `fd91527a`. Disclosed ~1.5 h later in `ceb5c7b2ffa6461691eec56e56e43f37d17455b2` (09:16:32, "round-53: record routed defect dispositions"), `corpus/lessons/round-53.md` items 8 and 11. |

Cross-event finding: none of the six changes a result line (PASS/FAIL tally, verdict, exit). Every rewrite is either the receipt's own `revision:` line (3 files) or the ladder's 18 throwaway fixture revisions. That is materially different from the round-57 precedent the counter was built for (`controls/after-c1-receipt-pins.txt` committed `pending`, filled later) — but the receipts still moved after being committed, and only 4 of 6 had a contemporaneous statement (all four in the `a4a890cf` message, one of them naming no path); the `1ae8de5d` ladder rewrite is disclosed nowhere at the time and the `fd91527a` one only at `ceb5c7b2`.

## NOTES JSON:

```json
[
 {"path": ".ufo/waves/round-52/control/c1-mutation-ladder.json", "commit": "1ae8de5d4dee8300624b0db2a94497ff905942c5", "note": "Re-run of .ufo/waves/round-52/c52_mutation_ladder.py at the freeze commit rebuilt all 18 sandbox fixtures, so 18 of 19 old_tail fixture revisions moved while families_caught stayed 13 and pass_fixture_agrees stayed true (receipt .ufo/waves/round-52/control/c1-mutation-ladder.txt)."},
 {"path": ".ufo/waves/round-52/control/c1-ledger-real.txt", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "note": "C1 ledger re-run at 1ae8de5d after the freeze commit: L1-L3 still PASS and only the printed revision line moved 3a50ae43 to 1ae8de5d, as the message of a4a890cf1381a194891689dcbba0bf524350926b states ('C1/C2 receipts re-run at 1ae8de5'); receipt kept at .ufo/waves/round-52/control/c1-ledger-real.txt."},
 {"path": ".ufo/waves/round-52/control/c1-mutation-ladder.json", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "note": "Second ladder re-run recorded by a4a890cf1381a194891689dcbba0bf524350926b: the 18 throwaway fixture revisions churned again with the tally fixed at 13 of 18 in .ufo/waves/round-52/control/c1-mutation-ladder.json and .ufo/waves/round-52/c52_mutation_ladder.py unchanged."},
 {"path": ".ufo/waves/round-52/control/c2-quote-real.txt", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "note": "Quote-truth re-run at 1ae8de5d: all eight conditions PASS before and after and only the revision line changed, per the message of a4a890cf1381a194891689dcbba0bf524350926b and the receipt .ufo/waves/round-52/control/c2-quote-real.txt."},
 {"path": ".ufo/waves/round-52/control/c2-quote-selftest.txt", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "note": "Quote-truth selftest re-ran with its evidence revision taken from HEAD (no KAKE_R52_SELFTEST_REV pin existed then, as LOG.md records the pin being added at round 56), printing 18 of 18 against 1ae8de5d in .ufo/waves/round-52/control/c2-quote-selftest.txt."},
 {"path": ".ufo/waves/round-52/control/c1-mutation-ladder.json", "commit": "fd91527a286086c1f4e6d4f44f715a907f041b5d", "note": "A dirty post-re-run ladder receipt was committed with the round-53 evidence set at fd91527a286086c1f4e6d4f44f715a907f041b5d and the lane later names its throwaway revision strings nondeterministic in corpus/lessons/round-53.md item 8."}
]
```

Full ledger entries (`receipt-rewrites.json` schema) for the same six, status `M` throughout; `kind` here is the counter's, see the disagreement section:

```json
[
 {"path": ".ufo/waves/round-52/control/c1-mutation-ladder.json", "commit": "1ae8de5d4dee8300624b0db2a94497ff905942c5", "status": "M", "fromBlob": "69a045918a98b0a19abcc068eda6063083976afa", "toBlob": "9a95330d6e14f1db5daa7d03102fd626c92f3cc2", "kind": "relabel"},
 {"path": ".ufo/waves/round-52/control/c1-ledger-real.txt", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "status": "M", "fromBlob": "bd10242546748d4b53c1e0320ae9224fab726c95", "toBlob": "ce0e0394aef9e93454373799d4c36cf05b5208f3", "kind": "relabel"},
 {"path": ".ufo/waves/round-52/control/c1-mutation-ladder.json", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "status": "M", "fromBlob": "9a95330d6e14f1db5daa7d03102fd626c92f3cc2", "toBlob": "23252321f30d92a90dd85351e2057833e6388350", "kind": "relabel"},
 {"path": ".ufo/waves/round-52/control/c2-quote-real.txt", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "status": "M", "fromBlob": "a7b5d69484beceed9cecf2cb19a38e4fd65a6f53", "toBlob": "aee2e7d949ce6074f6da105dfc25aa0ac248cf50", "kind": "relabel"},
 {"path": ".ufo/waves/round-52/control/c2-quote-selftest.txt", "commit": "a4a890cf1381a194891689dcbba0bf524350926b", "status": "M", "fromBlob": "ad318495b0b7ca4ef3ee62789d09189b0d79402b", "toBlob": "907047dd6ed29914b2d84c8ca2c6fac1db1cab8d", "kind": "relabel"},
 {"path": ".ufo/waves/round-52/control/c1-mutation-ladder.json", "commit": "fd91527a286086c1f4e6d4f44f715a907f041b5d", "status": "M", "fromBlob": "23252321f30d92a90dd85351e2057833e6388350", "toBlob": "d13c735262629ce56ceb89c247c6567f0dc786bc", "kind": "relabel"}
]
```

Full ids read from `git ls-tree <commit>` and `<commit>^` for each path (not prefixes). An entry matches an event only when path, commit, status and both blob ids match git exactly, so paste these verbatim.

Checked against the counter's own matchers at the base revision (read-only import, no lane write): all six notes return `pointed() == True`, and all six entries match `events()` keys exactly, so these six alone raise no `phantom`, `unpointed`, `malformed` or `wrong_kind` if entered with `kind: "relabel"` — the disagreement in the next section is about truth, not about passing.

## KIND DISAGREEMENTS:

All six. The counter's `classify` returns `relabel` for every one of them; on the evidence above the event every time was a **re-run**, not a relabel of a label without re-execution:

1. **The three ladder events (`1ae8de5d`, `a4a890cf`, `fd91527a`) are misdescribed by `relabel`.** `classify` fires `relabel` because "every changed line carries a 40-hex revision"; but the changed tokens are the *old counter's recorded output* of throwaway sandbox HEADs, regenerated per run, and the lane itself calls them "throwaway revision strings … nondeterministic" (`corpus/lessons/round-53.md` item 8). Corroboration that this is execution, not editing: 18 of 19 tails change and the 19th is the row whose tail is an exception string; the fixture builder stamps the current time into every fixture commit; the recorded shas resolve nowhere in the lane. Accurate kind: `rerun`.
2. **`c1-ledger-real.txt` and `c2-quote-real.txt` at `a4a890cf` are `rerun`**, stated in the commit's own message ("C1/C2 receipts re-run at 1ae8de5"). `relabel` describes the byte shape, not the event.
3. **`c2-quote-selftest.txt` at `a4a890cf` is `rerun`** on the same message, with a caveat I will not bury: the printed revision is env-overridable (`KAKE_R52_SELFTEST_REV`), so this one file cannot by itself prove a re-run. `[INFERENCE]` for this event alone; the other five are established.

Consequence the integrator must decide, stated plainly: `classify` cannot separate "re-executed at a new revision, verdict unchanged" from "label hand-edited", so a truthful `rerun` entry would be counted in `wrong_kind` and would block `met`. Recording `relabel` passes the counter but misdescribes 6 of 19 events. I did not edit the counter (out of seat scope) and do not recommend editing the frozen claim.

Mitigating fact, verified: no result line was rewritten in any of the six — only revision labels and throwaway fixture ids moved. The round-57 failure mode the counter exists for (a `pending` placeholder filled in later) does not occur here.

Unrun / out of scope: the counter's `--selftest` was not run (not my assignment); the other 13 undisclosed events (rounds 54, 55, 56, 57 paths) belong to sibling seats; the frozen `receipt-rewrites.json` ledger is the L1's to write; no lane, fleet, jj or index mutation was performed.

VERDICT: All six round-52 events are re-runs (18/18 fixture-id churn on the ladder, revision-line-only churn on the other three; no result line touched); the counter calls all six `relabel`, which is right about the bytes and wrong about the event, and 4 of 6 had a contemporaneous statement (the `a4a890cf` "C1/C2 receipts re-run at 1ae8de5" line), with the `1ae8de5d` ladder rewrite disclosed nowhere at the time and the `fd91527a` one only later at `ceb5c7b2`.
