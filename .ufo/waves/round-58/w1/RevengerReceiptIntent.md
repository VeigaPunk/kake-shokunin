# RevengerReceiptIntent

Seat scope (leaf, revenger): reconstruction only. Claim **C1** — the 19 post-commit receipt events in
`.ufo/waves/round-58/controls/base-c1-receipt-rewrites.txt` at base `0440485`: what each rewrite *was*, and
whether the counter's `classify()` names that intent. Intent key: **(a)** re-run whose new output replaced the
old; **(b)** revision relabel with no run; **(c)** placeholder filled after the run; **(d)** cosmetic/format;
**(e)** append-only ladder.

Method: (1) read each rewriting commit's message and the 52/54/55/56/57 contract/settlement text; (2) cloned the
lane `--shared` into `/fast/scratch/hyaku/kake-r58/RevengerReceiptIntent/clone`, checked out each rewriting commit,
re-ran the receipt's own documented command there with the recorded `--revision` / `KAKE_R*_SELFTEST_REV` pin, and
compared stdout to the committed blob; (3) resolved every hash printed inside a receipt (lane commit, fixture commit,
or nothing). Lane tree, jj state, index and sibling lanes read-only; writes went to my scratch dir (deleted), this
report and `RevengerReceiptIntent.files/`.

## EVENTS:

`tag`: **R** new blob equals the documented command's stdout at the recorded pin, up to the receipt's `EXIT=0`
trailer (reproduced in the clone); **R\***
same data transcribed into the receipt's older human format; **H** hash-only turnover of *fixture* HEADs,
reproduced by a fresh run as a shape (values are run-unique); **X** no run attributable; **F** only the fill
commit reproduces the fill's numbers.

```
 # path (under .ufo/waves/)                          commit    intent counter kind agree tag
 1 round-52/control/c1-mutation-ladder.json          1ae8de5d  (a)    relabel      NO    H
 2 round-52/control/c1-ledger-real.txt               a4a890cf  (a)    relabel      NO    R
 3 round-52/control/c1-mutation-ladder.json          a4a890cf  (a)    relabel      NO    H
 4 round-52/control/c2-quote-real.txt                a4a890cf  (a)    relabel      NO    R
 5 round-52/control/c2-quote-selftest.txt            a4a890cf  (a)    relabel      NO    R
 6 round-52/control/c1-mutation-ladder.json          fd91527a  (a)    relabel      NO    H
 7 round-54/controls/c1-selftest.txt                 8e408e00  (a)    rerun        yes   R*
 8 round-54/controls/base-c1-s374.txt                a0a4fd48  (a)    rerun        yes   R*
 9 round-54/controls/base-c2-ops-debt.txt            a0a4fd48  (a)    rerun        yes   R
10 round-54/controls/c1-selftest.txt                 a631cc02  (a)    rerun        yes   R*
11 round-54/controls/sources-census.txt              5826682b  (b)    rerun        NO    X
12 round-55/controls/c1-selftest-v2.txt              64c0ce12  (a)    rerun        yes   R
13 round-55/controls/after-c1-readme-index.txt       955e3d7b  (a)    relabel      NO    R
14 round-55/controls/after-c2-quote-truth.txt        955e3d7b  (a)    relabel      NO    R
15 round-55/controls/c2-selftest.txt                 955e3d7b  (a)    relabel      NO    R
16 round-56/controls/after-c1-selftally.txt          ad06cb8a  (a)    relabel      NO    R
17 round-56/controls/after-c2-quote-truth.txt         ad06cb8a  (a)    relabel      NO    R
18 round-56/controls/c2-selftest.txt                 ad06cb8a  (a)    relabel      NO    R
19 round-57/controls/after-c1-receipt-pins.txt       20217f23  (c)    fill         yes   F
```

Totals: (a) 17, (b) 1, (c) 1, (d) 0, (e) 0. Agree 6, disagree 13.

Why the 12 `relabel` events are (a), not (b): every one pins a revision that is the rewriting commit's **first
parent** (HEAD at run time) or the documented selftest pin, and the new blob is what the command prints there —
reproduced in the clone: byte-identical for 13, 14, 15, 16, 17, 18; stdout plus one appended `EXIT=0` (the stdout
already ends with one) for 2 and 4, stdout plus `EXIT=0` for 5; equal-shape for 1, 3, 6 — the only non-run delta in
the whole set is that duplicated trailer, a cosmetic (d) on top of a run, not an event of its own. A
label-only edit would leave the bytes as reproducible only by construction; events 2/4 additionally carry the
commit body "C1/C2 receipts re-run at 1ae8de5". For 13/14/16/17 the preceding commit (64c0ce12 / 4cb225f) is the
content revision those counters measure, so a re-measurement is the only way the pin could move.
[INFERENCE] "a run happened" is not directly observable for 13/14/16/17; what is observed is that the receipt is
true at the revision it names and byte-identical to a fresh run there.
Event 18 is the sharp one: its **count changes** (67/67 -> 86/86) under an unchanged pin, and both sides are
genuine runs of the two counter versions at that pin (round-56 settlement:23).
Event 11 is the one true label-only edit: the measured rows "rows: 155; warnings: 14 W04 …" are byte-identical to
the previous blob; the only delta is the inserted "measured against lane tip a631cc02…" (68 bytes), no counter
involved. Event 19 is the round-57 D1 class (`pending` -> result line): (c), but a hybrid — see D6.

## CLASSIFIER DEFECTS:

D1–D5 must be fixed **before** the ledger is written: the ledger's `kind` is the counter's classification
(contract.md:32), so a ledger written to *intent* scores `wrong_kind = 13` and cannot meet C1, while one written
to pass publishes 13 false `kind`s. That is the calibration defect this claim exists to catch.

**D1 — syntax mistaken for provenance (`all(REVLINE_RE …)`, c58:118,142).** Any changed line that merely
*contains* a 40-hex or the word "revision" makes the event `relabel`. A re-measured receipt whose only byte
delta is its own run stamp is therefore named a label edit: events **2,4,5,13,14,15,16,17** (8). Event **18** is
the same test failing one level up — its line changes 67/67 -> 86/86 *and* keeps a hex, so only a residue test
(not a "does the line contain a hex" test) separates it. Each new pin is
the first parent (or `KAKE_R52_SELFTEST_REV=1ae8de5d4dee`, `KAKE_R55_SELFTEST_REV=64c0ce12…` documented at
SKILL.md:1216,1234) and the blob reproduces. Rule: strip every `[0-9a-f]{40}` and the word `revision` from both
sides of each changed line; equal residue means "pin-only" and must be decided by D2, not by syntax.

**D2 — `classify(status, old, new)` has no commit context (c58:130).** A pin-only change is a re-run when the
new pin is the first parent or a documented run pin, and is a label edit when the pin could not be run output —
in particular a pin equal to the rewriting commit itself (a run cannot print the hash of the commit that will
contain its output). No such event exists at base; the class must be closed or the next one passes as honest.
Fix: pass the commit (or its parent and the documented pins) into `classify`.

**D3 — any 40-hex is treated as a revision (c58:118), but the ladder's are fixture HEADs.** Events **1,3,6**
change 18 `old_tail` lines each, written by the harness itself (c52_mutation_ladder.py:92 reads the old
counter's last line; :117-118 writes the JSON). A fresh run at the same commit changes *all* 18 fixture hashes
and no verdict — observed, three times. Rule: hash-only turnover on ≥2 machine-written JSON row fields with
equal non-hash residue is `rerun`.

**D4 — the `all(...)` is symmetric, so a one-sided relabel is called `rerun`.** Event **11**: the added line
names `lane tip a631cc02…`, the removed line carries no hash, so the `all` fails and the event is `rerun` —
overstating a prose annotation as a measurement. Rule: a hash added to / removed from a line pair is `relabel`
(this rule must precede D1's residue test).

**D5 — `relabel` is overloaded between shape and intent.** The lane already uses the word for label-only edits
(receipt-errata.json:3: "Six historical relabels … the later label (`to`) written by the commit"), and the ledger
inherits the same field. The six `revision:`-line events the errata lists (E2,E4,E13,E14,E16,E17) are, on the
evidence above, re-runs whose only visible delta is the pin — the errata's wording understates them, and a ledger
copying it would too. Fix: one field whose value is the *intent*, gated by D1–D4, plus (recommended) a `shape`
field for the mechanical class; or keep one field and add "results re-derived at `<rev>`" to every `rerun` note.

**D6 — `fill` is right about the shape but blind to the fill's provenance.** Event **19**: the filled result line
is exactly what `c57_receipt_pins.py --revision 20217f2` prints (`new_receipts=3 … met=True`) — i.e. at a tip
that *contains the fill*. At the tip it asserts (`tip: 31b61a4…`) the same command prints
`new_unpinned=1 new_receipts=2 met=False`; the body also keeps the placeholder's stale `revision: 32754df7` and
drops the run's `population=` line. So a `fill` entry whose recorded `tip:` is not the tip that reproduces its
numbers should be `malformed` (new check), not merely annotated; otherwise the ledger discloses the right *kind*
for a receipt whose *values* are unattributable to the tip it names.

**D7 — watch, not a misname.** Events 7, 8, 10 are re-runs *transcribed*: the counter there prints
`ok  base_unrepaired: exit 1 (met=False) expected 1 (met=False)` / `PASS C1.2_cells: [] {'suspect_cells': 1, …}`,
the receipts carry the earlier human format plus author-added `argv=`/`revision=`/`EXIT=` lines. The data agrees
with the run, so `rerun` is correct, but `kind` alone cannot say the bytes were retyped; the note should.

## EVIDENCE:

- `.ufo/waves/round-58/controls/base-c1-receipt-rewrites.txt:1` — 19 events, `undisclosed=19`, exit 1; `:2-21`
  the event list reproduced here.
- `.ufo/waves/round-58/c58_receipt_rewrites.py:118` `REVLINE_RE`; `:130-146` `classify`; `:142` the
  `all(REVLINE_RE…)` test; `:144` fill; `:146` default `rerun`; `:25` the `wrong_kind` definition; `:37,54` the
  predicate.
- `.ufo/waves/round-58/contract.md:32` — the ledger carries "the counter-classified kind"; `:11-13` the receipt
  rule (committed once, re-run lands under a new name).
- `.ufo/waves/round-52/c52_mutation_ladder.py:92` (`old_tail` = old counter's last line), `:117-118` (receipt is
  machine-written), `:58` (fixture `rev-parse HEAD`) — the evidence for D3.
- `.ufo/waves/round-52/c52_quote_truth.py:466` (`rev` = `KAKE_R52_SELFTEST_REV` else HEAD), `:617` (printed
  label); `.ufo/waves/round-55/c55_quote_truth.py:597,852`; `.ufo/waves/round-56/c56_quote_truth.py:618,1002` —
  the stamp is a run *input*, so a parent-valued or pinned stamp is run-consistent, not a relabel by nature.
- `SKILL.md:1216,1234` — the documented pins (`KAKE_R52_SELFTEST_REV=1ae8de5d4dee`,
  `KAKE_R55_SELFTEST_REV=64c0ce12ffe3…`).
- commit `a4a890cf` body — "C1/C2 receipts re-run at 1ae8de5" (events 2,3,4,5); commit `1ae8de5d` body —
  "receipts record the real-data runs … the mutation ladder (13 of 18 families)" (event 1).
- `.ufo/waves/round-57/receipt-errata.json:3` — "Six historical relabels … the later label (`to`) written by the
  commit"; its 6 entries are E2,E4,E13,E14,E16,E17 — the ones the probes re-derive at the pinned revision, so
  D5's (b) reading does not survive.
- `.ufo/waves/round-56/settlement.md:23` — "C2 selftest 67 -> 86 (19 dual-edit fixtures)" (event 18's count
  change); `.ufo/waves/round-56/controls/c2-selftest.txt:1` the 86/86 line with the unchanged pin.
- `.ufo/waves/round-54/controls/sources-census.txt:4` — the added "measured against lane tip a631cc02…" line;
  the `rows: 155` / `warnings: 14 W04` lines are byte-identical to `a631cc02`'s blob (event 11).
- `.ufo/waves/round-55/controls/c1-selftest-v2.txt:1` — `44/44` at `64c0ce12`; the blob at `2bda8e4` says
  `32/32` while the counter at that commit prints `35/35` (the old receipt was already stale; the rewrite fixed
  it — event 12).
- `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt:1-3` — result line, `tip: 31b61a4…`,
  `revision: 32754df7…`; `git show 31b61a4:<same>` = `pending\n  revision: 32754df7…\nEXIT=0`;
  `.ufo/waves/round-57/c57_receipt_pins.py:40` (`new_receipts` counts *valid* new receipts, so `met` requires
  the fill to exist — the self-measurement behind D6).
- Probes (scratch clone, deleted; per-event command + result in `w1/RevengerReceiptIntent.files/repro.json`):
  E2/E4 reproduce at both pins; E5 `18/18 (1ae8de5d4dee)`; E13 `4/4`, E14 `11/11`, E15 `54/54 (64c0ce12ffe3)`;
  E16 `13/13`, E17 `11/11` at `--revision 4cb225fb`; E18 `86/86 (f8438a282d59)` pinned and `67/67` with the
  pre-86 counter at the same pin; E1/E3/E6 ladder re-runs exit 0 with all 18 fixture hashes new and every verdict
  identical; E19 as in D6.

VERDICT: 13 of 19 events are misnamed by `classify` (12 re-runs sold as `relabel`, 1 relabel sold as `rerun`); fix D1–D4 in `classify` (commit/pin context + residue test + one-sided rule + multi-row fixture test), and treat a `fill` whose `tip:` does not reproduce as malformed (D6), before any ledger is written.
