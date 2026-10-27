# ReviewerC1Counter

## R2

At the w2 tip `f5a9b8a`, `python3 -B scripts/receipt_lineage.py --root . --revision HEAD` reports `receipts=95 events=12 undisclosed=0 met=True`, exit 0. An independent first-parent/tree/blob walk reproduced 95 first-version grammar matches and the same 12 event commits/kinds. The committed disclosure registry has 12 entries; all 12 `(path, commit, kind)` tuples match exactly, with no unmatched event or entry. Frozen `population-144.txt` independently equals the 144 path-rule matches at base. Tool JSON at HEAD reports `population=146`: the two additional paths are `round-61/controls/census-before.txt` and `population-144.txt`.

At base revision, a clean scratch checkout with the HEAD tool copied in and no worktree disclosures reports `receipts=95 events=12 undisclosed=12 met=False`, exit 1. In the ordinary HEAD checkout, running that same tool against base instead reports `undisclosed=0 met=True`, exit 0: the worktree disclosure file is being applied retroactively.

Tool `--selftest` passes 68 checks. This is not the specified C1 counter/predicate run.

## CASES

- Counter absence: `git ls-tree`, `git grep`, and `git log --all` find no `c61_lineage_cases.py` at any path/commit; `w1/ExecC1Counter.files/` is empty. Its own report says the counter was incomplete, L1–L16 unimplemented, selftest not run, and no cases run (`w1/ExecC1Counter.md:8-15`). Thus no instrument evaluates the frozen `cases_passed == 18 of 18 AND scores_held == 3` predicate (`contract.md:274-275`).
- Deletion false-green: scratch fixture creates a valid receipt then deletes it. Tool reports `receipts=0 events=0 undisclosed=0 met=True`, exit 0. Delete-and-readd with unchanged content also exits 0. This contradicts A3's frozen-population/deletion-event rule (`contract.md:278`); `population()` only selects paths present at the measured tree (`scripts/receipt_lineage.py:130-146`), while `segments_of()` discards the delete operation (`:313-332`).
- JSON result-span false-green: scratch fixture changes `{"met": false}` to `{"met": true}` in a receipt. Tool reports zero events and exit 0. A3 requires JSON `:` separators (`contract.md:278`); `RESULT_SPAN_RE` only recognizes `met\s*=` / `findings\s*=` / `members\s*=` (`scripts/receipt_lineage.py:104-107`).
- Worktree-disclosure false-green: `load_disclosures()` falls back to opening `<root>/.ufo/receipt-disclosures.json` when the measured revision has no committed blob (`scripts/receipt_lineage.py:378-400`). This violates committed-bytes-only/missing-means-zero in A3 (`contract.md:278`) and is demonstrated by the differing base results above.
- Population mismatch: at measured HEAD the tool scans 146 paths, not the frozen 144; A2 limits new-member accounting to rounds `<61` and excludes round-61 apparatus (`contract.md:277`). No counter exists to apply frozen membership or the missing/changed/extra-member checks.
- C1 distinctness from c58 is not demonstrated: all 12 C1 event `(path, commit)` pairs overlap the 19 events in `.ufo/waves/round-58/receipt-rewrites.json`. A2 expressly says C1 earns no calibration credit unless w2 demonstrates a distinct class c58 misses (`contract.md:282`).
- Score mutant: `git diff 9f07731a..HEAD -- SCORECARD.md` is empty (10/10/2 held). However, no round-61 executable reads/enforces those cells; `scores_held == 3` is only in the frozen predicate, and the missing counter cannot demonstrate the required score-only mutant failure.

## FINDINGS

1. **High — C1 predicate unmeasured.** The required counter is absent, and its own w1 report says it was incomplete with no cases run (`w1/ExecC1Counter.md:8-15`). Tool selftest success and matching R2 summary do not establish 18/18 or `scores_held == 3`.
2. **High — false-green on receipt deletion.** Scratch deletion fixture is clean/zero-event although A3 requires a deletion event; deleted frozen paths are not enumerated from the measured tree (`scripts/receipt_lineage.py:130-146,313-332`; `contract.md:278`).
3. **High — false-green on JSON result changes.** A `met` JSON value mutation passes clean despite A3's required colon recognition (`scripts/receipt_lineage.py:104-107`; `contract.md:278`).
4. **High — worktree state changes committed-revision verdict.** Base measurement returns green with the HEAD worktree's disclosures but red in a clean base checkout (`scripts/receipt_lineage.py:378-400`; `contract.md:278`).
5. **High — no distinct-vs-c58 evidence.** All 12 observed events overlap c58's 19; A2 bars calibration credit without a missed class demonstration (`contract.md:282`).
6. **Medium — population is live-scanned, not frozen.** Tool reports 146 at HEAD against 144 frozen; the round-61 extras are the census and frozen-list files. A2 excludes round-61 apparatus from extra-member accounting (`contract.md:277`).

Verification gaps: no C1 counter, so the frozen fixture suite, counter-level R1/R2 and score-only mutant could not be executed. No LSP device is mounted in this session; source checks used committed text and isolated scratch fixtures. No tool was installed or updated.

VERDICT: C1 predicate is not demonstrated; multiple A3 false-green cases and the missing distinct-vs-c58 demonstration block acceptance.
