# ExecHistoricalGates

Routed defect D3 / considerthese proposal 5 (historical-gate list). Every counter of
rounds 50-57 that appears as a gate-registry row in `SKILL.md` was run at the lane tip
and at the revision its round measured, in one shared clone under
`/fast/scratch/hyaku/kake-r58/ExecHistoricalGates` (read-only; clone deleted after the
receipts below were copied here).

## Method

- Lane tip `master` = `cc8da1674d6e590ae2d05e1f48944ac7939e9ecd`. Clone checked out at
  master; each counter is the master copy, invoked with `--root .` (c53 from the clone
  cwd), `python3 -B`, one run per cell, host Python 3.14.
- Measured revisions used (source):
  - r52 `1ae8de5d4dee8300624b0db2a94497ff905942c5` (SCORECARD "Measured revision").
  - r53 `3994101dba28896830604fd0b08c7f00faca8ed6` (its own pinned receipt
    `.ufo/waves/round-53/exec-quality-gate/real-round52-tip.{txt,json}`); the round-53
    land `fd91527` and `8e408e0` were also run.
  - r55 `64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6`, r56
    `4cb225fb032b04166fb0232bc98a7bcce72675ec` (SCORECARD).
  - r57 `32754df75774dd38e8a96fcda375fc93adf97f1e` (`.ufo/waves/round-57/measured.json`).
- Scope: rounds 50, 51 and 54 have no `.ufo/waves/round-5N/` gate-registry row in
  `SKILL.md` (grep), so their counters are not registry gates and were not run.
  `c56_selftally.py` excluded by the assignment. `c52_mutation_ladder.py` is a
  red-before helper, not a row. Every run below finished far under 60 s.

## RUNS

| Gate | Measured rev | Result there | Result at master | s (meas / tip) |
|---|---|---|---|---|
| `c52_wave_ledger.py` | `1ae8de5` | exit 0, 3/3 (`met=True`) | exit 0, 3/3 | 0.09 / 0.09 |
| `c52_quote_truth.py` | `1ae8de5` | exit 0, 8/8 | exit 1, 6/8 (`C5`, `C8`) | 0.06 / 0.06 |
| `c52_gate_registry.py` | `1ae8de5` | exit 0, 3/3 (`met=True`) | exit 1, 2/3 (`frozen_baselines`) | 0.06 / 0.05 |
| `c53_gate_truth.py` | `3994101` | exit 1, 2/7 | exit 1, 2/7 | 0.05 / 0.05 |
| `c55_readme_index.py` | `64c0ce12` | exit 0, 0 mismatches / 49 files | exit 0, 0 / 54 files | 0.22 / 0.24 |
| `c55_quote_truth.py` | `64c0ce12` | exit 0, 8/8 | exit 1, 6/8 (`C7`, `C8`) | 0.07 / 0.07 |
| `c56_quote_truth.py` | `4cb225fb` | exit 0, 8/8 | exit 1, 6/8 (`C7`, `C8`) | 0.08 / 0.08 |
| `c57_receipt_pins.py` | `32754df` | exit 1 (`new_receipts=0`, `scorecard_pin=0`) | exit 0, `met=True` | 0.31 / 0.69 |
| `c57_idresolver_gate.py` (`--fleet /home/vgpnk/Projects/shokunin`) | `32754df` | exit 0, 5/5 | exit 0, 5/5 | 1.38 / 1.40 |
| `c57_quote_truth.py` | `32754df` | exit 0, 8/8 | exit 0, 8/8 | 0.08 / 0.08 |

Exact failure lines at the tip:

- `c52_quote_truth` C5 `S374: entry line 72 quotes "the lane's robots-refusal ground (S372, "… which is not a raw substring of the retained body`;
  C8 `registry rows 160 != mirror rows 145 + 3`, `append-only: measured registry minus the adopted rows != mirror bytes`.
- `c52_gate_registry` `frozen_baselines: wave-evidence-ledger: pinned input LOG.md does not hash to its pin`
  (`baselines.json` pins `LOG.md` = `96a4e0f0…0370a2`).
- `c55_quote_truth` C7 `validated scratch registry is not byte-equal to the landed registry`;
  C8 `registry rows 160 != mirror rows 155 + 1`.
- `c56_quote_truth` C7 same message; C8 `registry rows 160 != mirror rows 156 + 2`.
- `c53_gate_truth` at `3994101`, `fd91527`, `8e408e0` and `cc8da16` (identical notes):
  `L1_gate_locator`, `L2_registry_anchor`, `L3_revision_notes` fail on S329/S312 locator
  leaves and revision notes; `R1_refusal_ids` fails (`jekyll-url-baseurl-options.md:
  refusal names staged ids ['S041','S042'], the staged entry's source ids are ['S296']`);
  `R2_held_ground` fails for `crux-keyless-check.md` and `jekyll-url-baseurl-options.md`;
  `R0_staged_snapshot` and `R3_true_ground` pass. Its `--selftest` is green (exit 0,
  including `round52_as_committed: exit 1 (expected 1)`).
- `c57_receipt_pins` at `32754df`:
  `C1 receipt-pins undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0 met=False`.
  At `31b61a4`: `new_unpinned=1 new_receipts=2 met=False`; at `20217f2`, `7ff6379`,
  `0440485`, `cc8da16`: `new_receipts=3 scorecard_pin=1 met=True`. Its committed receipt
  `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` states `met=True`,
  `tip: 31b61a4ddfcade92c108ff3786b8e9770bc8da31`.

## HISTORICAL

Green at the measured revision, red at the tip, each because of a documented pin:

- `c52_quote_truth` — two pins. C8: `.ufo/waves/round-52/assimilation/pre-append/corpus/SOURCES.md`
  + `mirror-pin.json` freeze the 145-row pre-append registry, and the condition
  `registry rows == mirror rows + 3` is only valid in the round-52 window (already red at
  the round-54 measured revision `a631cc0`, registry 155). C5: the round-55 append
  (`.ufo/waves/round-55`, measured `64c0ce12`) added the cross-reference paragraph at
  entry line 72, whose intra-document quotation `"the lane's robots-refusal ground
  (S372, S373)"` the r52 scanner reads as a source quote. First red: `a631cc0` (C8 only),
  `64c0ce12` (C5 + C8).
- `c52_gate_registry` — `baselines.json` pins the round-52 `LOG.md` blob digest; `LOG.md`
  is edited every round, so `frozen_baselines` fails at every revision after round 52
  (first red observed at `64c0ce12`).
- `c55_quote_truth` — C7 compares the round-55 committed validated scratch registry
  `.ufo/waves/round-55/assimilation/validate/corpus/SOURCES.md` with the landed registry
  as a whole, and C8 pins the 155-row round-55 mirror; any later append breaks both.
  Green at `64c0ce12`, red from `4cb225fb` (round 56) onward.
- `c56_quote_truth` — same C7 mechanism plus the 156-row mirror pin; this tip red is
  already disclosed in SCORECARD round 57 ("6/8 at the tip by design"). Green at
  `4cb225fb` only.

## DEFECTS

- `c53_gate_truth.py` — red at every revision present in the tree, not only at the tip:
  2/7 at its pinned receipt revision `3994101`, at the round-53 land `fd91527`, at
  `8e408e0`, and at `cc8da16`, with the same five findings (S329/S312 locator leaves and
  revision notes, the jekyll refusal naming S041/S042 for an S296 entry, and two held-ground
  citations). Its selftest passes, so the tool runs; the tree never satisfies it. The row
  is registered with `0=all 7 pass`, so its only admitted state is unreachable; the five
  findings it names are round-52 spot-check items that no later round repaired.
- `c57_receipt_pins.py` — red at the revision its round recorded as measured. `measured.json`
  names `32754df` (the build-X freeze commit), but the predicate requires
  `new_receipts == 3` and `scorecard_pin == 1`, which only exist from the T0 commit
  `20217f2`; at `32754df` the counter sees `new_receipts=0, scorecard_pin=0`. The round's
  own after-receipt names `tip: 31b61a4` with `met=True`, but re-running the landed counter
  at `31b61a4` gives `new_unpinned=1, new_receipts=2, met=False` — the receipt was produced
  on a pre-commit working tree, so it is not reproducible from committed bytes. (The gate is
  green from `20217f2` to the tip; the defect is the pin/receipt, not the predicate.)
- `c52_wave_ledger`, `c55_readme_index`, `c57_idresolver_gate`, `c57_quote_truth` are green
  at both points and show no defect.

## SKILL ROW TEXT

Proposed appended sentences (measurement date 2026-10-26, tip `cc8da16`):

- `wave-evidence-ledger` row: "Re-run: green at its measured revision and at the tip (3/3)."
- `quote-truth-counter` row: "Historical from round 54: green at `1ae8de5` only; tip 6/8 on
  frozen pins — C8's 145-row pre-append mirror and C5's quote scan, which flags the round-55
  cross-reference at entry line 72. Tip red is not a quote defect."
- `c52_gate_registry.py` completeness sentence: "Historical: its `baselines.json` `LOG.md`
  digest pin fails at every revision after round 52 (tip 2/3)."
- `c53_gate_truth.py` row: "Permanent red as registered: 2/7 at `3994101`, `fd91527`,
  `8e408e0` and the tip, with the same five findings (L1, L2, L3, R1, R2). The row certifies
  a defect; it cannot certify a clean tree."
- `readme-index-counter` row: "Green at `64c0ce12` and at the tip (54 knowledge files, 0
  mismatches)."
- `yahoo-robots-quote-truth-counter` row: "Historical from round 56: green at `64c0ce12`;
  tip 6/8 — C7's round-55 validated scratch registry and C8's 155-row mirror pin."
- `yahoo-crawl-handling-quote-truth-counter` row: "Historical at the tip by design (as
  SCORECARD round 57 states): green at `4cb225fb`; tip 6/8 on C7's round-56 scratch registry
  and the 156-row mirror pin."
- `receipt-pin-counter` row: "Green from `20217f2` to the tip; red at the `measured.json`
  revision `32754df`, which precedes the T0 receipts its predicate requires. The after-c1
  receipt's `tip: 31b61a4` is not reproducible from committed bytes (`new_unpinned=1,
  new_receipts=2` on re-run)."
- `id-resolver-gate` row: "Green at `32754df` and at the tip (5/5)."
- `baidu-dead-link-quote-truth-counter` row: "Green at `32754df` and at the tip (8/8)."
- `selftest-tally-counter` row: not measured here (excluded by the assignment as slow);
  keep it unmarked by this pass.

VERDICT: 4 of 10 registry counters are green at both points, 4 are historical-by-design reds at the tip (c52 quote/registry, c55 quote, c56 quote — named pins), 2 are defects (c53 never green; c57 receipt-pin measured revision and its after-receipt unreproducible).
