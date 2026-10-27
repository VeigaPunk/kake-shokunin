# ScribeConsiderthese

Read-only seat. Every fact below comes from lane base `0440485` (contract commit `fff3eea`) via read-only git and one read-only
import of the C1 counter's own `events()`/`classify()` in scratch; no lane file, index, jj state or counter was written or rerun
as a gate. Where a sibling seat's result would be needed I say "dispatched", not "landed".

GROUNDING:
- The pointer opens. `git -C <lane> log --follow --format='%h %ad %s' -- .ufo/waves/round-56/controls/after-c1-selftally.txt`
  prints two commits: `4cb225f` (add, revision `f8438a2…`) and `ad06cb8` (relabel to `4cb225f`). The same command on
  `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` prints `31b61a4` (body = the single line `pending`) and `20217f2`
  (body = the full `C1 receipt-pins … met=True` line plus `  tip: 31b61a4…`). Both are events in the C1 base set, so the two
  examples the proposal names are real.
- Base receipt `.ufo/waves/round-58/controls/base-c1-receipt-rewrites.txt` reads `events=19 undisclosed=19 phantom=0 malformed=0
  wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=0 met=False`, `EXIT=1`. I re-derived the event set with the counter's own
  walk at base (`c58_receipt_rewrites.events`): 19 events on 16 distinct paths — same count, so the receipt's population reproduces.
- Event mix by the counter's `classify()`: 12 `relabel`, 6 `rerun`, 1 `fill`. A (path, commit) join against
  `.ufo/waves/round-57/receipt-errata.json` matches 6 of the 19 (r52 `c1-ledger-real.txt`, `c2-quote-real.txt`; r55
  `after-c1-readme-index.txt`, `after-c2-quote-truth.txt`; r56 `after-c1-selftally.txt`, `after-c2-quote-truth.txt`) and leaves 13
  in no errata — the contract's "6 disclosed / 13 never" holds.
- Population: 70 receipts directly under `.ufo/waves/round-*/{control,controls}/` at base (r46 1, r51 4, r52 19, r54 6, r55 11,
  r56 9, r57 20). 16 of the 70 carry events; the heaviest are `.ufo/waves/round-56/controls/after-c2-quote-truth.txt` (6 commits,
  5 events), `round-55/controls/after-c2-quote-truth.txt` (4 commits, 3 events), `round-52/control/c1-mutation-ladder.json`
  (4 commits, 3 events).
- Counter event definition (code, not prose): `git log --reverse --no-renames --full-history -m --first-parent --name-status` over
  `.ufo/waves`; each path's first `A` is the baseline and is skipped; every later `M`/`D`/`A` is one event keyed on
  `(path, commit, status, fromBlob, toBlob)`. Because of `--no-renames`, a rename is a `D` at the old path and the new path's `A`
  is skipped unless that path was seen before (that skip is the "re-add" gate). Consequence worth stating: a rename that also
  edits content yields exactly one `delete` event and the new path's content is never compared.
- The history shape where the two methods can diverge is unexercised at base: `git log --diff-filter=R -M -- .ufo` prints nothing
  (no rename), `git log --diff-filter=D -- .ufo/waves` prints nothing (no receipt deleted), `git log --merges -- .ufo/waves` prints
  nothing (no merge joins the receipt set).

Where proposal 2 is right:
- It names the same class as routed defect D1 (a post-commit receipt edit presented as unedited) and both of the round-57 examples.
- The read is cheap and read-only: no lane mutation, exactly C1's surface.
- Its line test would have caught 15 of the 19 base events (a `revision`-bearing line, or a line carrying `met=`/`EXIT=`), i.e.
  every relabel and the fill.
- Its `--follow` is a fair choice for a renamed file; the counter deliberately folds a rename into one `delete` instead.

DIFFERENCES (proposal method vs counter event definition):
1. Selector. The proposal lists `round-*/controls/`; round 52 uses `control/` singular. That directory holds 19 receipts holding
   6 of the 19 events (4 of the 16 event paths). A `controls`-only listing never sees them.
2. Granularity. "more than one commit touching them" is a file flag, not an event: at base it selects all 16 event paths but
   reports 19 post-commit changes as 16, hiding the 5-event, 3-event and 3-event files (a path with 6 commits holds 5 events).
   And because `--follow` counts the initial add, ">1 commit" is an off-by-one proxy for ">=1 event", with no status, no blob ids
   and no kind.
3. Line test vs content classification. The counter classifies each event by diffing `fromBlob`/`toBlob`
   (append/format/relabel/fill/rerun/delete/readd). The proposal's two named line kinds cover relabel and fill; 4 events on 4
   paths change neither: `round-54/controls/base-c1-s374.txt` (PASS/FAIL detail lines plus a trailing qualifier; the `argv=` line
   keeps `--revision 68228b2…` unchanged), `round-54/controls/base-c2-ops-debt.txt`, `round-54/controls/sources-census.txt`,
   `round-55/controls/c1-selftest-v2.txt`. Under a stricter reading of "result line" (the top summary line only) the test drops to
   14/19.
4. Disclosure vs occurrence. The proposal has no disclosure concept, so on its own it cannot fail a disclosure predicate. C1 is
   falsifiable only because the ledger must match git on `(path, commit, status, fromBlob, toBlob)`, carry the counter's kind, a
   note pointing at resolvable evidence, and `new_rewritten == 0`. The proposal is a watch (early warning); the claim needs the
   event set.
5. One provenance claim is wrong. "r56 and r57 both did this and only the verifier caught it" holds for r57 (the `pending` fill,
   verifier D1) but not for r56: the two r56 relabels are in the lane's own round-57 errata, recorded by `c57_receipt_pins.py`
   (`considerthese/2026-10-26.md` Part 1 item 2: "6 undisclosed receipt relabels … → 0"). The class recurred; the lane's own
   counter, not only the verifier, caught the r56 pair.
6. "A cheap read I can do from GitHub" is per-path history: GitHub lists only paths present at the tip and follows renames, so it
   reproduces the proposal's granularity and both blind spots (round-52 `control/`, deleted paths) rather than the event set.
   [INFERENCE] from the method's shape; not exercised here.

DRAFT TEXT — for `corpus/QUALITY.md`, appended as a new section (append-only; no earlier line touched):

```markdown
## Round-58 criteria

- **A receipt's history is an event list, not a file list.** A rewrite is one `(path, commit, status, fromBlob, toBlob)` history
  entry after the path's first add, over every file directly under `.ufo/waves/round-<N>/{control,controls}/` (both spellings;
  round 52 uses `control/`) in the tip's first-parent ancestry, with rename detection off so a rename reads as a `delete` of the
  old path. A watch that lists files with more than one commit, or reads only `revision:`/result lines, is an early warning and
  cannot carry the claim: at base the 70 receipts hold 19 events over 16 paths (12 relabel, 6 rerun, 1 fill), a file flag names
  the 16 paths but not the events (one path carries 5), and its line test keeps 15 of the 19 events, losing the four
  round-54/55 reruns that change only detail lines. Disclosure is the predicate, not the occurrence: each event is listed with
  the git blobs, the counter's kind and a note pointing at resolvable evidence, and a receipt this round introduces is never
  edited. Grounding: `considerthese/2026-10-26.md` (2026-10-26) proposal 2, adopted as round-58 C1;
  `corpus/lessons/round-57-verifier-spotcheck.md` D1; `.ufo/waves/round-58/controls/base-c1-receipt-rewrites.txt` (exit 1,
  `undisclosed=19`; 6 of the 19 are the relabels `receipt-errata.json` already records). Falsifier:
  `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision <tip>` must print `met=True`; at base it exits 1
  with `undisclosed=19`, and the selftest's rename, deletion and re-add cases fail a file-and-line reading.
```

OTHER PROPOSALS:
1. **Read the lane's own tools instead of duplicating them — tool half already landed, daily-read half not a lane artifact.**
   `scripts/id_resolver.py` (r57, selftest 49/49), `landed_check` (r56) and the README frontier ground map (r55) exist and are
   cited in `corpus/QUALITY.md` (round-57 row). Round 58 keeps them exercised: seat `ExecLandedCheck` runs `landed_check.py` on
   the round-57 report and seat `ScribeSkillRows` writes the r58 counter rows plus the `historical` mark for `c56_quote_truth.py`.
   The proposal's "report only a change or a red, weekly spot-check" is a reflector practice with no lane deliverable, so no seat
   implements it.
2. **Receipt-rewrite watch — this round, as C1.** Implementation is the event-set ledger, not the file watch (DIFFERENCES 1–4).
3. **Operator-decision queue — not taken this round.** No seat records the four routed items (calibration vs operability
   ownership, CJK <=25-unit quote rule, SHONEN promotion, `wip/operator-save-20261023` / draft PR #1). They appear only as
   context in other seats: `CriticAxisClaims` asks whether C1 is really calibration, and `CriticC3Cheat` exercises the CJK
   25-unit vs 40-character rule. Round-58 files carry no queue artifact. [INFERENCE] that the queue is still owed, from those
   absences; not a claim about the operator's inbox.
4. **Gate-agreement ledger — not built this round.** The lane has per-round verifier spot-check lessons with agree/disagree prose
   (round-20 … round-57) but no cross-round ledger; `ConnCrossClaim` reads proposals 2/4/5 for one shared field set for a later
   round, which is representation work, not a per-round agreement count. No `*agreement*` artifact exists under `corpus/`.
5. **Historical-gate list — taken this round as routed defect D3, as the assignment says.** Seat `ExecHistoricalGates` is
   dispatched to run the rounds 50–57 counters that finish in ~60 s and record green-at-revision vs result-at-tip; seat
   `ScribeSkillRows` marks `c56_quote_truth.py` `historical` with its pinned revision (round-57 spot-check D3). Dispatched, not
   observed landed by this seat.

VERDICT: Proposal 2's pointer is real (both examples are C1 base events) but its file-level `--follow` watch is not the C1
predicate — it misses round 52's `control/` (6 of 19 events) and the four detail-line-only reruns — so C1 correctly keeps the
git-keyed event set with disclosure as the claim; proposals 1 and 5 are carried this round, 3 and 4 are not.
