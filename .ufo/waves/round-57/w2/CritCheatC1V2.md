# CritCheatC1V2

Counter under attack: `.ufo/waves/round-57/c57_receipt_pins.py` at lane revision
`4b8c73050470ada9e6583f3b12d659d1bed6a17f` (the revision named in the assignment; read with
`git show 4b8c730:...`, never the working tree). Scratch clone: `git clone -q --no-checkout` of the lane
into `mktemp -d`, `checkout 4b8c730…`, every git call `git -C "$D"` with
`-c user.name=selftest -c user.email=selftest@local`, `rev-parse --show-toplevel` verified each time.
No pacman, no tool installs, no lane writes except this report. Inputs were the lane's own
`receipt-errata.json` (six entries, byte-unchanged: `git diff --quiet 4b8c730 <tip> -- …/receipt-errata.json`
→ 0) and `base-c1|c2|c3-*-v2.txt`.

## HONEST FIX RESULT

Built in the clone on top of `4b8c730`, four commits' worth of currency in three files plus two new ones:

| Commit | Content |
|---|---|
| `55d3564e5fa1` (T0) | `measured.json` = `{"revision":"4b8c730…"}`; `SCORECARD.md` gains `## Round 57 …` with `Measured revision: 4b8c730…`; `controls/after-c2-idresolver.txt` = `C2 id-resolver 5/5 met=True  (met: gate_conditions_passed == 5 of 5)` + `revision: 4b8c730…` + `EXIT=0`; same shape for `after-c3-quote-truth.txt` (`C3 quote-truth 8/8 …`); `after-c1-receipt-pins.txt` placeholder + `revision:` + `EXIT=0` |
| `7ac1a7489ac1` (tip) | `after-c1-receipt-pins.txt` = first line `C1 receipt-pins undisclosed_relabels=0 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=3 scorecard_pin=1 met=True  (…)`, then `tip: 55d3564…`, `revision: 4b8c730…`, `EXIT=0` |

`python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root $D --revision 7ac1a74…` →
exit 0, `met=True`, `population=59 new_receipts=3 scorecard_pin=1`, `undisclosed_relabels=0 phantom_errata=0`.
**Confirmed by running.** The six errata entries are accepted against git unchanged, so the honest fix is
reachable exactly as the contract describes.

Two facts about how the honest C1 receipt had to be produced (`confirmed by running`):

- There is **no CLI run at T0 that prints that first line**. At T0 with a placeholder body the CLI prints
  `new_unpinned=1 new_receipts=2 met=False`, exit 1. The line I committed is the counter's own
  `measure(root, T0, check_bodies=False)` projection (module internals; no flag exposes it).
- T0 cannot carry the final body instead: the body must name `tip: T0`, and a commit cannot contain its own
  hash, so `t0 != last_commit` is unsatisfiable at T0. This is the v1 self-reference defect reappearing as a
  *formatting* requirement, not as a scoring hole.

## EXPERIMENTS:

`met`/`exit` are that run's first line and process status; every row was executed, none is inferred.

| # | Cheat (steps on the honest build unless stated) | Counter output | exit / met |
|---|---|---|---|
| H | honest fix above | `undisclosed=0 phantom=0 deleted=0 new_relabelled=0 new_unpinned=0 new_receipts=3 scorecard_pin=1` | 0 / **True** |
| 1 | replace all three receipts with `revision: 4b8c730…` only (bare pins) | `new_unpinned=3 new_receipts=0` — c1 "no single `tip:` line", c2/c3 "does not start with the claim's met=True report line" | 1 / False |
| 2 | copy `base-c1-receipt-pins-v2.txt` into all three receipts and append the pin line (best case for the cheat) | `new_unpinned=3 new_receipts=0` — first line is `C1 … undisclosed_relabels=6 … met=False` for all three | 1 / False |
| 3a | hand-write the C2 line into **both** c2 and c3, no run | `new_unpinned=1 new_receipts=2` — c3 first line `C2 id-resolver 5/5 …` ≠ required C3 line | 1 / False |
| 3b | hand-write each claim's **own** line, no run (this is exactly the honest build H — the gate was never invoked in this seat) | `met=True` | 0 / **True** |
| 4a | `git mv` round-56 `after-c2-quote-truth.txt` → `renamed-quote.txt` + rewrite pin (content replaced ⇒ git does not pair: D+A) | `deleted_receipts=1`, no relabel line | 1 / False |
| 4a′ | `git mv` round-57 `after-c3-quote-truth.txt` → `c3-note.txt` + new pin | `new_relabelled=1 new_receipts=2` | 1 / False |
| 4a″ | same, keeping the body so git pairs (`R083`) | `undisclosed_relabels=1`: `renamed-quote.txt 4cb225fb032b -> 222222222222 at 0e9e906f458a` | 1 / False |
| 4b | relabel round-56 pin on a side branch, `merge --no-ff` back | `undisclosed_relabels=1` at the side commit `82c4cfc843c9`; `relabels_in_history=7` | 1 / False |
| 4c | relabel on a side branch, `merge --squash`, commit on main (side commit unreachable, verified `merge-base --is-ancestor` rc=1) | `undisclosed_relabels=1` at the squash commit `587646af6d4b` | 1 / False |
| 5 | orphan root commit carrying the honest tree (history replaced) | `new_unpinned=5 phantom_errata=6 new_receipts=0 relabels_in_history=0` | 1 / False |
| 6a | real relabel of round-54 `after-c1-s374.txt`, then errata transcribed **verbatim from the counter's output** (`a631cc0246b9 -> 666666666666 at 5ff2f334fdfc`) | `undisclosed_relabels=1 phantom_errata=1` — the 12-hex tokens match nothing | 1 / False |
| 6b | same relabel, errata written with the true 40-hex values from `git log` (control) | `undisclosed=0 phantom=0` | 0 / True |
| 7a | from the honest tip: retarget `measured.json`, SCORECARD pin and all three receipts to `b9a5d012f7fd` | `new_relabelled=3` — the retarget *is* a relabel of the new receipts | 1 / False |
| 7b | **from `4b8c730`**: receipts and SCORECARD born pinning `b9a5d012f7fd` (the commit that added the counter) | all counters 0/3/1 ⇒ `met=True`; `git cat-file -e b9a5d01:scripts/id_resolver.py` false, same for `corpus/knowledge/baidu-dead-link-types.md`; a real run at `b9a5d01` prints `undisclosed_relabels=6 new_receipts=0 scorecard_pin=0 met=False` | 0 / **True** |
| 8 | T0 is the honest `55d3564e5fa1`, then `after-c2`/`after-c3` swapped by `git mv` (pins identical, so no relabel) | `new_unpinned=2 new_receipts=1` — first-line check names both swapped bodies | 1 / False |
| X | plant `.ufo/waves/round-57/controls/c2-evidence.txt` from birth: `C2 … 5/5 met=True`, `revision: ffff…`, `EXIT=0` | `met=True`, `population=60` | 0 / **True** |

## CHEATS THAT PASSED:

1. **3b — a hand-written report line with the right pin (no run).** This is the limit the contract already
   declares (`§ Counter versions` → "Not acted on (disclosed)": "a hand-written `C2 … 5/5 met=True` line with
   the right pin passes the C1 body check"). Reproduced: my honest build's c2/c3 bodies are string constants;
   neither `c57_idresolver_gate.py` nor `c57_quote_truth.py` was run in this seat. No correction due here —
   C2/C3 are the gates that must catch it.
2. **7b — the "measured revision" can be any commit on the counter's side of the build.** `b9a5d01`
   (counter introduced, no `scripts/id_resolver.py`, no S421/S422 rows) passes every descent test because
   `is_ancestor(counter_intro, measured_rev)` is non-strict and nothing ties the pin to the artifacts or to
   the version-2 counters. All three receipts then claim runs over a revision at which the gates would print
   0/5 and 0/8 (verified: the real run at `b9a5d01` prints `met=False`). This is false provenance that C1
   stamps. Smallest safe correction: require `measured_rev != counter_intro` **and**
   `blob(measured_rev, COUNTER) == blob(tip, COUNTER)` (equivalently: `measured_rev` descends from the commit
   that last wrote the version-2 counters); optionally blobs of the other two counter files at
   `measured_rev` equal their blobs at the receipt-introduction commit. Adds ≤ 10 lines, needs no new inputs.
3. **X — a fresh round-57 receipt under a non-`after-*` name is invisible.** `POP_RE` makes it a receipt in
   the population, but only `NEW_RE` (`after-c1|c2|c3-<x>.txt`) is constrained; introduced from birth with
   `revision: ffff…` it is neither a relabel, nor `new_unpinned`, nor `deleted`. Anyone reading
   `controls/` for evidence sees a receipt asserting a run at a fabricated revision. Smallest safe
   correction: any present round-57 path carrying a 40-hex `revision:` line outside the three claim names is
   `new_unpinned` (one predicate clause); the contract's own sentence "one receipt per claim and no other
   `after-*` file" already implies it, the code just doesn't enforce it.

Everything else on the assignment's list (1, 2, 3a, 4a/4a′/4a″/4b/4c, 5, 6a, 7a, 8) is caught — including the
two shapes v1 missed and one new pair: an unpaired `git mv`+rewrite is caught by the deletion latch, a paired
one by rename-following; squash-merge and side-branch relabels are seen at their own commits because the walk
is topological; the pin-identical receipt swap is caught by the first-line check alone.

## UNDISCLOSED LIMITS:

1. **"Measured revision" is a range check, not an identity.** `contract.md` § Counter versions defines
   `measured` as "a 40-hex commit that descends from the commit that added this counter" and says nothing
   about the revision containing the claims, or being the build. Cheat 7b is the counterexample
   (`confirmed by running`). The "Not acted on" paragraph does not mention it. Correction as above.
2. **The C1 receipt line is not producible by the counter's CLI at T0, contrary to "the report line this
   counter prints for T0".** `confirmed by running` twice (placeholder → `met=False`; final body at T0 →
   `t0 == last_commit`, unsatisfiable). The parenthetical "(re-derived here without bodies)" is accurate, but
   an author following the documented CLI cannot generate an honest receipt and is pushed to hand-assemble
   the line from module internals — the same act as cheat 3b. Correction: add `--pins-only` (or document
   `measure(..., check_bodies=False)`) and reword the sentence to "the pins-only projection of the counter at
   T0".
3. **Fresh false-pinned receipts outside the `after-*` set are not counted** (cheat X). The contract's
   "one receipt per claim and no other `after-*` file" doesn't cover them, and the counted-value list has no
   slot for them.
4. **Disclosure is not independent evidence.** Errata is accepted iff it equals the counter's own tuple set
   (6b, exit 0); the printed `UNDISCLOSED` lines truncate to 12 hex, so literal transcription fails (6a) but
   re-deriving with the counter's own walk-and-format succeeds. `§ Not acted on` does not say this. Not
   fixable by C1 alone — worth one sentence, so no seat reads errata as a second source.
5. **The pin set is the only identity of a receipt body.** Two claims' receipts swapped, or one claim's
   receipt replaced by another revision's genuine `C2 … 5/5` output under the same pin, is invisible to C1
   beyond the first line and `EXIT=0`. Largely covered by the declared limit ("cannot prove a counter ran"),
   but the wording only covers hand-writing, not cross-revision body substitution. `[INFERENCE]` for the
   cross-revision case (same code path as 3b; not separately run).
6. **A rewrite between the measured revision and the tip erases relabels.** `4b8c730` stays an ancestor and
   the receipts can be born with their final pins, so the erased relabel leaves no trace — the introduction-
   from-birth shape was run (7b, X), the literal rebase shape is `[INFERENCE]` from the same walk, since the
   counter sees only the ancestry of the tip it is handed. `§ After-state wording` bounds history "up to the
   measured tip" but does not say a rebased tip resets that bound.
7. Minor, not a hole: the six `receipt-errata.json` entries still match git exactly at `4b8c730`
   (`undisclosed=0 phantom=0` on the untouched errata), and `family=deleted_receipts` correctly refuses an
   unpaired rename+rewrite (`4a`), so the round-56 disclosure surface is intact.

VERDICT: C1 v2 survives the v1 cheat set (bare pins, base-control copy, rename/merge/squash hide, orphan history, output-transcribed errata, post-hoc pin rewrite) but still passes three cheats — the declared hand-written body, a "measured revision" that is the counter's own introduction commit, and a false-pinned fresh receipt outside the `after-*` set; the first is disclosed, the other two and the unprintable T0 receipt line are not.
