DISCLOSED MISTAKE (first line, per binding): I ran `ls /fast/scratch/hyaku/kake-r38ctl` once (child names only: CriticPredicate, CtlBaseWrapper, CtlLabelShortcut, CtlStdlibV2, CtlTrivial, MutCounterV2, MutRefPass); nothing inside any child was listed, stat'ed, read or searched, and nothing under /fast/scratch/hyaku/kake-r38/ was touched except committed receipt strings naming it. Counters not run; no key seen.

# CriticControlReceipts — round 38 wave 1: control receipts and the C1 withdrawal

Full report. Checked: 12 v2 control receipts, 69 v3 receipts, 42 `mutref` receipts (each with `.exit`); `toolSha256` vs retained bytes and vs each seat's `ctl/*.md`; `counterSha256`; predicate strings; claim fields; met/exit consistency; dispatch order.

## Per-receipt check (v2 = `sealed_count.py`, v3 = `sealed_count_v3.py`)
| tool (seat) | v2 | v3 | tool sha = receipt | report sha = receipt |
|---|---|---|---|---|
| base `af43a50f` | 8 | 8 | `944d2f51…` yes | yes |
| constant clean / junk / all-false / no-reader (`CtlTrivial`) | 0/0/0/1 | 0/0/0/1 | yes ×4 | yes ×4 |
| label / delegate ceiling (`CtlLabelShortcut`) | 16/20 | 16/20 | `69affa2d…`/`5c80fb01…` yes | yes |
| wrapper min / care (`CtlBaseWrapper`) | 18/20 | 14/20 | `a5a5fc0b…`/`3215ae1a…` yes | yes |
| stdlib patched (`CtlStdlibV2`) | 13 | 13 | `15b3f643…` yes | yes (harness `dd690f54…` receiptless, stated unscored) |
| rulepatch / rulepatch_pct (`CriticPredicate`) | 20/20 | 20/20 | `8a5712b4…`/`b2c86c8c…` yes | yes |
| 42 mutants (`MutRefPass`) | 16–20, **29 met**, 13 at 20 | 16–19, 0 met | 42/42 | 42/42 |
| 8 ablations / 6 r37 controls / reference | — | 16–18 / 0,0,1,1,5,7 / 20 | v3 receipts | n/a |

v2 counter `52daff55…6e7b` and v3 `28b120a5…` match every receipt of their set (`sha256sum` exit 0). All 140 receipts: exit 0 iff `met`, 0 mismatches; `toolPresent` true. Order: controls dispatched `04:15:37Z`, committed `04:28:54Z`, wave 1 dispatched `04:29:52Z` — receipts predate any build seat, as declared. The v3 counter does carry the three reported repairs: unknown ids no longer alias (`sealed_count_v3.py:114`), a missing `--tool-file` yields a JSON receipt (:15), `checksEvaluated` is compared when the case states it (:178).

## Findings

1. **Count drift.** SCORECARD:2194 and :2199 say "28 of 42 mutants … 13 pass all 20". Receipts: **29** met (`passed >= 19`), 13 at 20 (`python3` over `verification/mutref/*.json`, exit 0). Non-material (29 > 28 still withdraws) but wrong twice in the paragraph that justifies the withdrawal.

2. **Withdrawal: required by the text, mis-stated in the reason.** C1's declaration (:2167-2170) listed "a cheapest-wrapper shortcut around the base tool" as a control and said "no reclassification of the control is an option". That control met the predicate: care scores 20, and the seat itself wrote "B is the 'cheapest wrapper around the base tool' arm, and it meets by construction: base + the three amendments ≡ the reference" (`ctl/CtlLabelShortcut.md`). So withdrawal was the declared consequence. But SCORECARD:2196-2200 concludes it from "the wrapper arms do the claimed work" — i.e. the declared control was never a shortcut. The substantive cause is a mis-specified control class, not a counter defect; the mutants independently justify withdrawal (13 of 42 score 20 under a predicate meant to catch one broken sentence).

3. **The C2 class list reclassifies after the scores, in time and identity.** The same four files are controls under claim C1 and builds under claim C2, by identical sha256 (`3215ae1a…` care, `5c80fb01…` delegate, `8a5712b4…`, `b2c86c8c…`): `verification/control-*.json` carry `"claim":"C1"`, `verification/v3/*.json` the same hashes with `"claim":"C2"`. mtimes (stat exit 0): all `ctl/*.md` 01:20:17–01:27:23; `sealed_count_v3.py` 01:27:00; first v3 receipt 01:28:03; `SCORECARD.md` 01:28:53. The class list (:2243) was written with the four 20s already on disk. "Named before any v3 control score is read as a control" is unfalsifiable: the scores predate the naming, and the naming decides what counts as a "control score". This is the round-37 defect in a form that does not save C1 (C1 was withdrawn), but it does carry C2. Other side: the criterion "implements all three rules" is semantic and score-independent, and no admitted claim survives the relabel; if each of the four tools is ablated rule by rule and each falls below 20, the relabel is defensible and C2 stands. What is missing today is that measurement (finding 5), not the intent.

4. **Class (6) gap: partial rules.** "(6) a tool that implements at most two of (h), (i), (k)" (:2245) excludes a tool with code for all three that implements one only for the shapes the declaration names (:2160). If such a tool scores 20, no declared class withdraws C2, and C2's "gains rule (k)" is admitted on example-bound evidence.

5. **The "all three rules" discharge is prose.** No receipt ablates any of the four 20/20 tools; the only ablations (`v3/A1–A8`) are of the private reference. The score-independent test the class criterion needs (delete rule X, score falls below 20) is absent.

6. **v2 predicate string.** :2104 declares the receipts hold "met: passed >= 19 of 20 sealed cases"; all 28 v2-counter receipts hold it without `met: ` (28 counted; the 29th pre/v3-string receipt is `c2-at-af43a50f`). C1 withdrawn, so no live effect; v3 receipts carry the declared string verbatim.

7. **Reproducibility.** Only `retained/controls/` (12 tools) is in the lane; the 42 mutants and 8 ablations live outside it, so their receipts are re-checkable by hash only.

8. **"Every tool a seat named was scored" (:2178) is false for `MutCounterV2`**: 8 fixture tools and 10 counter mutants (23 hashes) have no receipt, by design (dummy key). True for every robots-audit tool named.

## Missed control (built; needs the L1's key to score)
`CtlExampleK` = base bytes + full (h) + full (i) + (k) only for the escape shapes the C2 text names; every other unreserved escape falls to the rules.
- `/fast/scratch/hyaku/kake-r38w1/CriticControlReceipts/CtlExampleK.py`, sha256 `e29d92ebb2c03bf55b4a483272207acdda330db28334d66129a2b6f6fbb1d4be` (`py_compile` exit 0).
- Probe (own manifest, sha256 `c311f380…6e47`; commands `timeout 20 python3 -B <tool> --manifest probe/manifest.json`): care `clean` exit 0; CtlExampleK `failed-policy` exit 1, blocking only `/robots.tx%74` and `/r%6Fbots.txt`; base blocks 5 of 10. It differs from the 20/20 care arm on nothing else.
- Interpretation: **20/20** ⇒ the key tests (k) only through the declaration's own examples; C2's "gains rule (k)" is overstated and finding 4 is live; smallest correction is one sealed (k) check whose implicit-allow path uses an unreserved escape other than `%2E`/`%72`. **≤19** ⇒ the key generalises and finding 3 is bookkeeping. My expectation: 20 (the v3 added-check list names no further `/robots.txt` escape).

Not verified: I could not score `CtlExampleK` (no key), did not run the selftest against it, and re-scored no receipt. All claims above come from committed bytes, mtimes and seat reports.
