### Round 60 gate-status ledger

The registry above says what each frozen counter measures; it does not say, in one readable place,
which rows may be red on today's tree and which red is a defect. This ledger is that place
(`considerthese/2026-10-26.md:33`, proposal 5: "Keep a list of gates that go red by design on later
trees … so the daily report doesn't mistake a pinned historical gate for a regression, and can flag
when one *should* have been re-pinned"). It is a view over the registry rows, not a second registry:
the label a counter reads lives in the row's `Kind` cell, so a ledger row that disagrees with its
`Kind` cell is a finding for the round — the ledger never becomes the authority. Both are derived
from observed exits by `python3 -B .ufo/waves/round-60/c60_gate_status.py --root . --revision <rev>
[--json]`; its `--json` report is the ledger's receipt and is committed once, after the run, under
`.ufo/waves/round-60/controls/` under a name that carries the measured revision. No placeholder is
committed, and a re-run lands under a new name.

**The three labels.** Each is read from the `Kind` cell of a registry row, never from this table,
and each is a statement about *when the row may be red*:

- **`live`** — the `Kind` cell carries neither marker below. The gate must exit 0 at the measured
  revision; any other exit is a counted mismatch (`live_not_green`), not a preference.
- **`historical`** — the `Kind` cell contains the word `historical`. The gate is green at its pin and
  red on later trees **by design**, because its predicate is pinned to a frozen input: a registry row
  count in a mirror (`c52_quote_truth.py` 148 rows, `c55_quote_truth.py` 156, `c56_quote_truth.py`
  158, `c57_quote_truth.py` 158 + 2 adopted, `c58_quote_truth.py` 160), a byte-prefix survival rule
  over every round-55-base knowledge file (`c55_readme_index.py`), or a frozen file set with
  `new_receipts == 3` (`c57_receipt_pins.py`). The row states what fails later, so a reader can tell
  a pinned gate from a regression.
- **`never met`** — the `Kind` cell contains the words `never met`, written with a space: the parse is
  a substring of the cell, so `never-met` is read as `live`. It marks a registered command that has
  never been observed to exit 0 at its pin or at the measured revision — the class the registry had no
  word for, and the one the round-60 base shows twice (`c53_gate_truth.py` labelled `live`, exit 1;
  `c57_idresolver_gate.py` labelled `live`, exit 2 without `--fleet`; `.ufo/waves/round-60/contract.md:78-81`).
  Whether either row is labelled is decided from the measured run, not from this prose: the label needs
  a pin at a revision where the command was red, and the run is what supplies it.

**The pin rule.** A non-`live` row carries the pin as the first 40-hex revision in its `Kind` cell;
the rest of the cell may explain the design and names nothing else in 40-hex. The pin is the last
revision at which the gate's command was observed to exit 0 — for a gate the current round's own
change reddened, the last revision *before* that change — and it must be an ancestor of the measured
revision: a pin that is a later commit, an uncommitted draft or a sibling branch's commit fails
`pin_not_ancestor`, and a non-`live` row without one fails `unpinned`. A `never met` pin is the
revision the red was measured at. The pin says *when*; the `Pinned values / frozen proof` cell still
says *what* is frozen, and neither cell substitutes for the other. A pin is not evidence that the
command is green there until it has been run at it.

**Relabel duty (routed defect R59-D1).** A live gate that a round's own change turns red is
relabelled with its pin **before** the counter scores the after-state, or the round says in its
contract why the gate stays live. The practice: before the contract freezes, every non-`historical`
row is run on a scratch draft of the after-state (a mock commit in a scratch clone); a gate the claim
must redden is named in the contract with its disposition — marked `historical` with its pin, or the
claim reshaped so it does not redden the gate — and if neither holds, the contract states why and the
round carries the red as a counted mismatch. Round 59 is the counterexample this duty exists for: its
C9 insertion inside `corpus/knowledge/crawler-identity.md` reddened the round-55 `readme-index-counter`
(`index_mismatches=1 … head_changed=1: crawler-identity.md`, exit 1), wave 1 had predicted it
(`.ufo/waves/round-59/w1/ExecHistoricalGates.md` H1), nothing recorded the trade until the no-harm
reviewer ran it (`.ufo/waves/round-59/a2r1/ReviewerNoHarm.md`), and the row was marked `historical`
afterwards (`SKILL.md`, `readme-index-counter`). A relabel that lands after the counter has scored is
a second defect, not a repair: the counted mismatch is exactly what the label was meant to prevent,
and a relabel used to launder a red is the same defect with a worse record. Round 60's own case is
its C3 registry growth: rows S427–S429 make the registry 167 rows where the live round-59
`crawler-identity-quote-truth-counter` requires `registry rows == mirror rows + 2` (162 + 2 = 164),
so that row is relabelled `historical` at its measured revision before the after-state is measured,
or the contract names why not (`contract.md` § Axis declaration, "C3's appended rows may turn a
population counter red; C1 then requires that counter's honest relabel"; `c59_quote_truth.py:93`
`NEW_ROWS = ("S425", "S426")`, mirror pin `rows: 162`).

**What the labels do not claim.** A label says when a gate may be red; it never says the gate's
verdict was true. The round-60 counter does not test whether a row's verdict-map prose is true beyond
`0=` and `1=`, nor whether a pin is the round's own measured revision (`contract.md:84-85`); those
stay reviewer checks. `unrun` is a state, not a cell to fill from memory: a gate whose command was not
run is written `unrun`, and an unrun gate is neither `live`-green nor `historical`.

| Gate (registry row name) | Label | Pin — first 40-hex in the `Kind` cell | Exit at pin | Exit at the measured tree | Why red by design (or why live) | Re-labelled |
|---|---|---|---|---|---|---|

The table lands header-only; the L1 adds one row per member of the round 48–59 population (28 at the
round-60 base) and one per non-population registry gate that can go red on tree growth, from the
counter's report and the round sections of `SCORECARD.md`, never from this prose. `Label`, `Pin` and
`Exit at pin` are written for the two non-live labels; `Exit at the measured tree` for every row.
The first three header cells are deliberately **not** `Name`, `Kind`, `Entry command`: the counter's
row rule keys on those three cells, so no ledger row can be misread as a registry row (and a second
row naming the same counter path would read `duplicate_row`). Withdrawal rule: a ledger row goes when
its registry row or its counter leaves the tree. When a gate *should* have been re-pinned — a
historical row whose frozen input no longer matches the round that owns it, or a live row that has
been red for two measured trees — the ledger says so in the last cell with the round number, which is
proposal 5's second half.
