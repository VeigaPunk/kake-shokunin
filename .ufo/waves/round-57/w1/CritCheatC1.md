# CritCheatC1

Seat: CritCheatC1 — attack C1 by experiment. Clone `git clone --no-checkout` of the lane at
`b9a5d012f7fd7190bf4d4c6e4d79e9462a6471af` into `/tmp/c1crit-ecxadkug` (its own toplevel, verified; the tip hashes
below are live there, branches `exp1`…`expG`), all edits inside it,
every commit with `-c user.name=selftest -c user.email=selftest@local -c commit.gpgsign=false`. Each run is
`python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root <clone> --revision <tip>` from inside the clone.
Lane repo untouched (read-only `show`/`log` only).

Population at the contract commit is **50** files; the committed base control prints 45 because it was taken at
`28fa0b2` (before the five round-57 `controls/` files existed). Base run in my clone reproduces the control:
`undisclosed_relabels=6 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0
scorecard_pin=0 met=False`, exit 1.

The six real tuples (from `measure()` at base, full hashes): r52 `c1-ledger-real.txt` / `c2-quote-real.txt`
`3a50ae43…`→`1ae8de5d…` at `a4a890cf…`; r55 `after-c1-readme-index.txt` / `after-c2-quote-truth.txt`
`faf9abe8…`→`64c0ce12…` at `955e3d7b…`; r56 `after-c1-selftally.txt` / `after-c2-quote-truth.txt`
`f8438a28…`→`4cb225fb…` at `ad06cb8a…`.

## EXPERIMENTS:

Metric legend (order of the counter's own line): u=undisclosed_relabels p=phantom_errata d=deleted_receipts
nr=new_relabelled nu=new_unpinned nre=new_receipts sp=scorecard_pin. The predicate text is identical in every run.

| # | exact edit in the clone | u | p | d | nr | nu | nre | sp | exit | met | tip |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | honest: `receipt-errata.json` with the six tuples, `measured.json={revision:b9a5d012…}`, `SCORECARD.md` + `## Round 57 — calibration (C1)` naming `b9a5d012f7fd`, one commit; then three `controls/after-c{1,2,3}-receipt-pins.txt` each with the one `revision:` line, second commit | 0 | 0 | 0 | 0 | 0 | 3 | 1 | **0** | **True** | b8e8650e |
| 2 | cheapest dishonest: same errata; `measured.json` = `28fa0b2…` (a fabricated ancestor — the round-57 counter does not exist at that revision: `git cat-file -e` = 1); receipts `C1 met=True` with no run at all | 0 | 0 | 0 | 0 | 0 | 3 | 1 | **0** | **True** | ff7f779e |
| 2b | as 2, but receipt bodies label-swapped (`after-c1` says `C3 met=True`, `after-c2` says `C1`, `after-c3` says `C2`) | 0 | 0 | 0 | 0 | 0 | 3 | 1 | **0** | **True** | 0e2c14bf |
| 3 | `git mv` all six historical receipts to `round-5X/control-notes/` (outside `POP_RE`), commit; then pins + receipts, **no errata** | 6 | 0 | 6 | 0 | 0 | 3 | 1 | 1 | False | abdfb1da |
| 3b | same move, **with** the honest errata | 0 | 0 | 6 | 0 | 0 | 3 | 1 | 1 | False | 2bce3ba9 |
| 4 | pins committed (`measured=b9a5d012`), receipts committed with `revision: ffff…`, then a second commit rewrites the line to `b9a5d012` (no re-run) | 0 | 0 | 0 | 3 | 0 | 3 | 1 | 1 | False | aa3882d0 |
| 5 | honest errata (six tuples) + receipts pinned correctly, then a commit relabels **new** receipt `after-c3` `b9a5d012…`→`28fa0b2…`, then errata gains that entry with its true fields (`commit` = the relabel commit) | 0 | 1 | 0 | 1 | 1 | 2 | 1 | 1 | False | 850566d4 |

Verbatim decisive lines (all exit 0, met=True):
`EXP1  C1 receipt-pins undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=3 scorecard_pin=1 met=True`
`EXP2  C1 receipt-pins undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=3 scorecard_pin=1 met=True`
`EXP3  … undisclosed_relabels=6 … deleted_receipts=6 … met=False` / `EXP4 … new_relabelled=3 … met=False`
`EXP5  … phantom_errata=1 … new_relabelled=1 new_unpinned=1 new_receipts=2 … PHANTOM .ufo/waves/round-57/controls/after-c3-receipt-pins.txt b9a5d012f7fd -> 28fa0b23e699 at d71ab14fca8d`

Notes on the five: (3) the move hides nothing — the relabel stays in history (`u=6`) *and* the delete of a path that
once carried a `revision:` line is counted (`d=6`); the move only shrinks the population 50→47, which is not checked.
(4) caught. (5) caught twice over — but the errata entry is **true** (`git` agrees the relabel happened at the named
commit) and the counter prints it as `PHANTOM`: the errata channel cannot express a round-57 relabel, so a truthful
disclosure is scored as a lie.

## CHEATS THAT PASSED:

All exit 0, `met=True`, with the same seven metrics as the honest run.

| # | edit | evidence |
|---|---|---|
| A | history erasure: `git checkout --orphan`, `git add -A`, one root commit of the whole tree, then pins + receipts (no errata needed) | `relabels_in_history=0`; base `b9a5d012` **not** reachable from the tip (`merge-base --is-ancestor` = 1); 3 commits total. The counter has no `BASE_REV` anchor, so it certifies a history that never contained the defect |
| B | **relabel of the new receipts on a merged side branch** (no history rewrite, ordinary `git merge --no-ff`): pins on main; branch `sideB` commits the three receipts with `revision: aaaa…` (`94168aa`) then rewrites them to `b9a5d012…` (`6dc3e83`); merge into main | `new_relabelled=0`. `git log --first-parent --name-status` shows only `A  …/after-c1-receipt-pins.txt` at the merge; the pre-merge blob is never compared. This *is* the round-56 defect (`corpus/lessons/round-56-verifier-spotcheck.md` §6) and the counter calls it met |
| C | same as B with `git merge --squash` + one commit (GitHub-style) | identical result, `met=True` (`f05d4e55`) |
| E | `SCORECARD` section names the pin while denying the run: `## Round 57 — calibration (C1)` / "No C1 measurement was run this round. The base revision was b9a5d012f7fd…" | `scorecard_pin=1` — the check is `measured_rev[:12] in section`, not an assertion of measurement |
| F | three pinned receipts plus a fourth, contradictory `after-c3-receipt-pins-FAILED.txt` (`undisclosed_relabels=6 … met=False`, `EXIT=1`), all pinned to the measured rev | `new_nums` is a **set** of claim numbers, so `len==3` still holds; `new_receipts=3`, `met=True` |
| G | receipts whose bodies are the **truthful** output of a run at the pinned revision (`undisclosed_relabels=6 … new_receipts=0 scorecard_pin=0 met=False`), pinned to `b9a5d012` | `met=True`, exit 0. The three receipts certify that the claim was **not** met at the revision they pin, and the counter reports the claim met |

Strongest counterexample: **B** (plausible workflow, no history rewrite) and **G** (honest, self-refuting receipts).
**A** is the deepest structural one (no base anchor) but is visible to any reviewer who checks `BASE_REV`.

Root cause shared by 2/2b/E/G: the counter reads only `revision:` lines and file paths. It never parses a receipt
body, so "a run happened at X" and "a string that looks like a pin" are indistinguishable; and the pin rule
(`measured_rev` a *strict ancestor* of the receipt's own intro commit) guarantees that no run at the pinned
revision could ever have seen the receipt — a run at `measured_rev` necessarily prints `new_receipts=0 met=False`
(demonstrated: base run). The predicate therefore cannot be satisfied by a run that produced the receipts; it can
only be satisfied by a consistent claim.

## HONEST FIX RESULT:

Experiment 1 — six real errata tuples, `measured.json`, three pinned receipts, a `## Round 57` section naming the
pin — gives `undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0
new_receipts=3 scorecard_pin=1 met=True`, **exit 0**. The repair is reachable and cheap (3 commits, 6 errata
entries). It is also byte-indistinguishable from the dishonest version 2 except for one 40-hex string and the
wording of three bodies, and version G shows the same shape passing with bodies that record failure.

## WHAT THE COUNTER CANNOT SEE:

1. That anything ran. No receipt body is read; `met=True` and the truthful `met=False` both pass (G, F).
2. Which claim a receipt belongs to (2b) — only the digits in the filename, and duplicates are collapsed by a set (F).
3. Pre-merge history of a path introduced by a merge or a squash (B, C): `--first-parent` makes the path born at
   the merge, so every rewrite before the merge is invisible. Historical receipts are protected (extra D: a
   7th relabel of `round-56/after-c1-selftally.txt` on a side branch is caught at the merge, `u=1`, exit 1) only
   because the path already exists on the first-parent chain.
4. The base: no `BASE_REV` reachability check and no population baseline, so an orphan/grafted history (A) or a
   population shrink 50→47 (3b) is not flagged; only a delete of a path that once had a `revision:` line is.
5. Prose: `scorecard_pin` is a substring test over the `## Round 57` section (E), and relabels in report prose are
   out of scope by contract.
6. Any truth of an errata entry beyond git's view of the population: a true round-57 entry is labelled `PHANTOM` (5).

Impacted axis: **C1 calibration only** (C2/C3 counters untouched; no sibling-lane or fleet path was written).
Smallest safe corrections, in order of cost: (a) require `measured_rev` to equal the tip/intro commit that holds the
receipts, so a run over that tree is possible at all; (b) parse the receipt body's metric line and require it to
equal a recomputation at the pinned revision (kills 2/2b/E/G/F); (c) require `BASE_REV` to be an ancestor of
`--revision` and `population >= ` the base control's count (kills A and silent removal); (d) walk the new receipts
with `git log --all` (not `--first-parent`) and reject a path whose earlier blob carried a different pin (kills B/C);
(e) require one file per claim number, not a set (F); (f) reword `PHANTOM` for round-57 paths as out-of-scope (5).

VERDICT: C1's predicate is met by a fabricated pin with no run (exp 2/2b), by a merge-shaped relabel of the new receipts (B/C), by a SCORECARD that denies the run (E), by a contradictory duplicate receipt (F) and by receipts that truthfully record met=False at the pinned revision (G); the honest repair passes (exp 1, exit 0), but only because the counter cannot distinguish a run from a claim — refuse `met` until the receipt body is recomputed and the base is anchored.
