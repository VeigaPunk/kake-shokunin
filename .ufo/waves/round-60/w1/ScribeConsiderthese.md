# ScribeConsiderthese

Base revision `97cdc122379711c2b02a8970752c8782da3ac81d` (lane master at round open); access date 2026-10-27.
Everything below is read from committed blobs at that revision (`git show`/`git ls-tree`/`git merge-base`) or from
committed reports; nothing in the lane, no counter and no git/jj state was touched. `EHG` =
`.ufo/waves/round-58/w1/ExecHistoricalGates.md`.

## PROPOSAL 5 GROUNDING:

The proposal to ground, verbatim (`considerthese/2026-10-26.md:33`): "**Historical-gate list.** Keep a list of gates that
go red by design on later trees (currently `c56_quote_truth.py` at 6/8), so the daily report doesn't mistake a pinned
historical gate for a regression, and can flag when one *should* have been re-pinned."

1. What the lane has today — a list that is derivable but never assembled. The labels live only inside `Kind` cells of
   the gate registry: 21 tables whose header is `| Name | Kind | Entry command | … |` (base `SKILL.md:210, 386, 410, 481,
   536, 554, 567, 586, 615, 724, 1044, 1065, 1091, 1126, 1196, 1213, 1231, 1251, 1271, 1291, 1305`), 37 data rows.
   Two prose sentences mention the class (`SKILL.md:1288` "Four earlier quote-truth counters are marked `historical`
   above"; `SKILL.md:1301-1302` the round-59 addition). No aggregate exists: `git show 97cdc12:README.md | grep -n
   historical` → 0 hits; `SKILL.md` has no section that assembles the historical set; the word "list" appears nowhere as a
   list. Nothing recomputes a label, so a row can stay `historical` long after it went green (proposal 5's second half).
2. Static ledger at base (derived by me with the contract's population regex over `git ls-tree -r`, rows joined by path in
   the `Entry command` cell; no counter executed): **28 members — 9 `live`, 7 `historical`, 0 `never-met`, 12
   `unregistered`, 0 duplicate rows**. The twelve unregistered are exactly the contract §C1 before-probe list
   (`c48 ×2, c49 ×2, c50 ×2, c51 ×2, c52_gate_registry, c52_mutation_ladder, c54 ×2`), so C1's structural before-state is
   reproducible without running anything. Every one of the seven historical rows has 8 non-empty cells and a first 40-hex
   pin in the `Kind` cell; the five distinct pins resolve as commits and each is an ancestor of base
   (`git merge-base --is-ancestor … 97cdc12` → exit 0 for `1ae8de5d`, `64c0ce12`, `4cb225fb`, `32754df`, `8d340c15`).
3. The instance the proposal names. `SKILL.md:1254` (`yahoo-crawl-handling-quote-truth-counter`) is `historical`, pin
   `4cb225fb…`, "mirror pins 158 rows". Measured record: exit 0, 8/8 at the pin; exit 1, 6/8 (C7, C8) at `cc8da16`
   (`EHG:37`, message `EHG:50` `registry rows 160 != mirror rows 156 + 2`); earlier at `20217f2` and `0440485`
   (`corpus/lessons/round-58.md:90`), and read the same way by the round-58 registry seat
   (`.ufo/waves/round-58/w1/ScribeSkillRows.md:80`). At base the red is arithmetic, not timing: `corpus/SOURCES.md` holds
   164 rows, the mirror pin's 158 + 2 accepted = 160, and `c56_quote_truth.py:534` fails whenever the counts differ. The
   exact 6/8 split at base is **[INFERENCE]** — I did not run the counter (no seat scores an after-state this wave).
4. One label the committed record contradicts — the strongest single grounding for the claim. `SKILL.md:1273`
   (`receipt-pin-counter`, `c57_receipt_pins.py`, pin `32754df…`) reads "historical from round 58: green at its round-57
   measured revision …; red on later trees by design", but `EHG:38` measured **exit 1 at `32754df`**
   (`new_receipts=0`, `scorecard_pin=0`) and met=True at `31b61a4`'s successors / `0440485` / `cc8da16` (`EHG:38, 58-63`),
   and `EHG:97-103` files it under DEFECTS ("red at the revision its round recorded as measured"; the after-receipt is not
   reproducible from committed bytes). `.ufo/waves/round-57/measured.json` names `32754df`. So 1 of 7 historical labels is
   inverted against its pin, not merely unpinned: C1 names it `historical_not_green_at_pin` (and, if the base exit is 0,
   `historical_but_green` as well — **[INFERENCE]**, unrun).
5. Adjacent conflict, reported not resolved. The live row `id-resolver-gate` (`SKILL.md:1274`) carries
   `[--fleet <fleet root>]`; `EHG:39` ran it **with** `--fleet /home/vgpnk/Projects/shokunin` → exit 0, 5/5. Contract §C1
   keeps a `[...]` segment whose `<…>` are placeholder words, so C1's command includes the fleet root and the member is
   green; the contract's before-probe line "`c57_idresolver_gate.py` labelled live, exit 2 without `--fleet`" describes a
   run with the segment dropped. The two cannot both hold; the judge rules.

## HISTORICAL ROWS AT BASE:

Seven rows, in file order. "At pin" is a committed measurement; "at base" is the state C1 will observe — marked
**[INFERENCE]** where no committed receipt measures base.

| `SKILL.md` | row `Name` | counter | pin (first 40-hex of `Kind`) | at pin (committed) | at base |
|---|---|---|---|---|---|
| 1216 | quote-truth-counter | `.ufo/waves/round-52/c52_quote_truth.py` | `1ae8de5d4dee8300624b0db2a94497ff905942c5` | exit 0, 8/8 (`EHG:32`) | red — 6/8 at `cc8da16` (`EHG:32`); C8 mirror pins 148 rows, base registry 164 (`SKILL.md:1216`) **[INFERENCE]** |
| 1233 | readme-index-counter | `.ufo/waves/round-55/c55_readme_index.py` | `64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` | exit 0, 0 mismatches / 49 files (`EHG:35`) | red from round 59 by its own row text (`head_changed` on the `[r59-correction]` insert in `crawler-identity.md`); green at `cc8da16` (`EHG:35`) **[INFERENCE]** |
| 1234 | yahoo-robots-quote-truth-counter | `.ufo/waves/round-55/c55_quote_truth.py` | `64c0ce12ffe3ca4d6d1891a3e3e33933a95380f6` | exit 0, 8/8 (`EHG:36`) | red — 6/8 at `cc8da16`, C7+C8 (`EHG:36`) **[INFERENCE]** |
| 1254 | yahoo-crawl-handling-quote-truth-counter | `.ufo/waves/round-56/c56_quote_truth.py` | `4cb225fb032b04166fb0232bc98a7bcce72675ec` | exit 0, 8/8 (`EHG:37`) | red — 6/8 at `cc8da16`; at base C8 arithmetic 164 ≠ 158+2 (`c56_quote_truth.py:534`) **[INFERENCE]** |
| 1273 | receipt-pin-counter | `.ufo/waves/round-57/c57_receipt_pins.py` | `32754df75774dd38e8a96fcda375fc93adf97f1e` | **exit 1** (`EHG:38`; `EHG:97-103` DEFECTS) — contradicts the row text | met=True at `0440485`/`cc8da16` (`EHG:38`); base exit unmeasured — if 0, the label is inverted |
| 1275 | baidu-dead-link-quote-truth-counter | `.ufo/waves/round-57/c57_quote_truth.py` | `32754df75774dd38e8a96fcda375fc93adf97f1e` | exit 0, 8/8 (`EHG:40`) | red — 158 + 2 pinned rows vs 164 (`SKILL.md:1275` "red once a later round appends a registry row") **[INFERENCE]** |
| 1295 | baidu-crawler-identification-quote-truth-counter | `.ufo/waves/round-58/c58_quote_truth.py` | `8d340c15200959190ba3e894399cdc931976331f` | exit 0, 8/8 (`.ufo/waves/round-58/measured.json` C3) | red — C7 pins the round-58 validate scratch, C8 the 160-row mirror; base registry 164 (`SKILL.md:1295`) **[INFERENCE]** |

No row in the population is labelled `never-met` at base, so C1's `never_met_but_green` class has no member this round;
the calibration content sits entirely in the seven pins above. Six of the seven are consistent with their pinned
measurement; `1273` is not.

## LESSON TEXT:

Draft for `corpus/lessons/round-60.md` `## Considerthese` (prose only; the table belongs to the claim, not the lesson):

`considerthese/2026-10-26.md` (2026-10-26) proposal 5 (historical-gate list) is implemented here as claim C1, grounded by
`w1/ScribeConsiderthese.md`. The list proposal 5 asks for stops being hand-kept and becomes derived: C1 reads the 21
`Name | Kind | Entry command` tables of `SKILL.md`, takes each row's label out of its `Kind` cell (`historical` /
`never-met` / `live`) with its 40-hex pin, and runs every one of the 28 round-48–59 counters at the measured revision
(`e_T`) and, for a labelled row, at its pin (`e_P`) — so the list cannot drift from the rows that carry it, and the two
warnings proposal 5 wanted become computed classes: `historical_but_green` (a gate that went green and should have been
re-pinned) and `historical_not_green_at_pin` (a pin that does not hold). At base `97cdc12` the ledger reads 9 live, 7
historical, 0 never-met, 12 unregistered; `c56_quote_truth.py` — the instance the proposal names at 6/8 — is its worked
example: green 8/8 at its pin `4cb225fb`, red 6/8 (C7, C8) at `cc8da16` (`ExecHistoricalGates.md:37`), red at base by
arithmetic because its mirror pins 158 rows while `corpus/SOURCES.md` holds 164 (`c56_quote_truth.py:534`), and the row
passes only while both halves hold. What stays open: whether a pin is the round's own measured revision is
reviewer-checked, not machine-checked (C1 accepts any ancestor pin); rounds 40–47 stay outside the population; the
verdict-map text is read only for `0=`/`1=`; the label remains prose in a `Kind` cell, so between measured rounds a row
can still go stale silently. One of the seven labels is already contradicted by a committed measurement —
`receipt-pin-counter` (`SKILL.md:1273`) advertises "green at its round-57 measured revision `32754df`" while
`ExecHistoricalGates.md:38` measured exit 1 there (`new_receipts=0`, `scorecard_pin=0`) and `:97-103` files it as a defect;
C1 counts that as a mismatch, the re-pin or re-management decision stays with the lane.

Proposals 1 (read the lane's own receipts), 2 (receipt-rewrite watch) and 4 (gate-agreement ledger) are not taken this
round. Proposal 2 duplicates a gate the lane already runs — the round-58 `receipt-rewrite-counter`
(`c58_receipt_rewrites.py`, `SKILL.md:1293`), whose first-parent-walk limit is already recorded as carried. Proposal 4
needs a non-author verifier per round, and round 60's declared shape is two v1 waves (w1 build, w2 falsify) plus at most
one residual call of ≤8 reviewer/critic seats — there is no second column to fill, and the round-59 verifier's
agree/disagree counts survive only as spot-check prose, not as a machine-readable file. Proposal 1 is a reporting habit
with no committed artefact; the one part of it that has a surface — the gate registry — is what C1 mechanises.

## NOT TAKEN:

| Proposal (`considerthese/2026-10-26.md:29-33`) | Taken? | Why |
|---|---|---|
| 1 read the lane's own tool receipts instead of re-deriving | no | No committed artefact to judge; the only part with a machine-readable surface (gate rows/receipts) is what C1 measures. One proposal per round (round-59 §Considerthese precedent). |
| 2 receipt-rewrite watch (`git log --follow` over `controls/`) | no | Already shipped as a gate: `receipt-rewrite-counter` / `.ufo/waves/round-58/c58_receipt_rewrites.py` (`SKILL.md:1293`, live at base), first-parent limit carried in round-59 §Routed defects D2. Re-proposing it would duplicate a live counter. |
| 4 gate-agreement ledger | no | Requires a non-author verifier each round; round 60's shape (`contract.md` §Round shape) has none — w1 build, w2 falsify, one residual ≤8 reviewer/critic call. Round-59's agree/disagree counts (r56 6/6, r57 7/7) exist only as prose. |
| 5 historical-gate list | **yes** — carried by C1 | Grounded above: derivable today, assembled nowhere; one of seven labels already contradicted by a committed measurement. |

## NOTES (behavior, gates, touched surfaces, out of scope)

- Behavior: read-only. Commands run: `git show`, `git ls-tree -r`, `git merge-base --is-ancestor`, `git cat-file -e`,
  `grep`/`sed`/`awk` over the base blobs and committed reports, and a local Python 3 parse of the 21 registry tables in a
  scratch copy (`/fast/scratch/hyaku/kake-r60/ScribeConsiderthese`, deleted). No counter, selftest or tool of the lane was
  executed; no `--root`/clone was built; no network.
- Gates: none scored or claimed. The static ledger is a derivation from committed bytes, not a C1 run; C1's own
  before-state is the L1's probe, and this report only confirms its structural half (12 unregistered, 9 live, 7
  historical, 0 never-met of 28).
- Touched surfaces: this report only. No lane file, no `.files/` directory, no index/jj state, no fleet-root file, no
  commit/push. No tool installed or upgraded.
- Out of scope: writing C1's code, any after-state measurement, the direction of the `receipt-pin-counter` defect
  (relabel vs re-pin) — the lane's decision, not a scribe's.
- Provenance: base `97cdc12`, `SKILL.md` and `README.md` blobs at base, `EHG` (round-58 seat report), `measured.json`
  (rounds 57/58), `c56_quote_truth.py` at base, `considerthese/2026-10-26.md`, `corpus/lessons/round-58.md`,
  `corpus/lessons/round-59.md`, `.ufo/waves/round-60/contract.md`.

VERDICT: Proposal 5 grounds on committed bytes and is carried by C1 — the historical set is derivable (9 live / 7 historical / 0 never-met / 12 unregistered of 28) but assembled nowhere, its named example `c56_quote_truth.py` is green 8/8 at pin `4cb225fb` and red 6/8 later, and 1 of 7 labels (`receipt-pin-counter`, `SKILL.md:1273`) is contradicted by a committed measurement at its own pin.
