# ScribeLessonMistakes

Scope: the frontier step only — draft `corpus/lessons/round-58.md` §Mistakes and the matching
`corpus/QUALITY.md` round-58 criteria. Leaf seat: I wrote this report and
`ScribeLessonMistakes.files/` only; no lane corpus file, SKILL.md, git or jj state was touched.
Sources read: `corpus/lessons/round-57-verifier-spotcheck.md` §5 (D1–D5), `corpus/lessons/round-57.md`
§Mistakes, `corpus/QUALITY.md` §Round-57 criteria, `CORPUS.md` (mistake-row vocabulary, "a fix counts
only once shown able to fail"), `.ufo/waves/round-58/contract.md`, `controls/base-c1-receipt-rewrites.txt`,
`c58_receipt_rewrites.py` (kinds: `delete|readd|append|format|relabel|fill|rerun`), `SKILL.md`
§Round 56/57 gate registry additions, `.ufo/waves/round-57/receipt-errata.json`. First-hand runs: C1
counter at the base revision, `c56_quote_truth.py` at three revisions, `git show`/`log`/`diff` over the
receipt blobs (read-only). Tools installed: none.

## MISTAKES:

Append to `corpus/lessons/round-58.md` as `## Mistakes` (columns per `CORPUS.md`: class · evidence pointer · captured-by · fix).

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| landing | `.ufo/waves/round-57/controls/after-c1-receipt-pins.txt` landed at `31b61a4` as three lines — `pending`, `  revision: 32754df75774dd38e8a96fcda375fc93adf97f1e`, `EXIT=0` — and was filled at `20217f2` (blob `417ca0c615ba -> b514c80d7f36` at `20217f23eca1`; `git log -- .ufo/waves/round-57/controls/after-c1-receipt-pins.txt` lists exactly those two commits), while the round-57 report said no receipt carrying a `revision:` line was rewritten. This is the shape C1 exists to forbid: a pre-written receipt with a pin and an exit code. The report half is quoted through `corpus/lessons/round-57-verifier-spotcheck.md` §5 D1 only — `.ufo/reports/round-57/kake.md` and its commit `bdfe1efd6ceecc8632508c47e8be2630e7289bd4` do not resolve in this repo (`git cat-file -t` → bad object; `git ls-tree -r 20217f23 -- .ufo/reports` → `round-20` alone). | `c57_receipt_pins.py` missed it by construction: it watched `revision:` lines, and the fill kept the same pin (`32754df7…` in both blobs), so no relabel was visible; QUALITY round-57 criterion 1 stated the rule but its counter could not see a fill. | C1 counter `.ufo/waves/round-58/c58_receipt_rewrites.py` — predicate carries `new_rewritten == 0`, the ledger vocabulary has a `fill` kind, and the contract's receipt rule forbids a placeholder (committed once after the run; a re-run lands under a new name). Shown able to fail: `controls/base-c1-receipt-rewrites.txt` prints `undisclosed=19 … met=False`, `EXIT=1`, and its last event is this file (`UNDISCLOSED M … after-c1-receipt-pins.txt at 20217f23eca1 417ca0c615ba -> b514c80d7f36`). |
| landing | Twelve post-commit edits to measurement receipts in rounds 52–56 disclosed nowhere: round-52 ×4 (`control/c1-mutation-ladder.json` three times, `old_tail` revision strings, at `1ae8de5d4dee`/`a4a890cf1381`/`fd91527a2860`; `control/c2-quote-selftest.txt` fixture revision `3a50ae4321e6` → `1ae8de5d4dee`), round-54 ×5 (`controls/c1-selftest.txt` +2 checks at `8e408e00fbe1` and again at `a631cc0246b9`; `controls/base-c1-s374.txt` PASS/FAIL lines at `a0a4fd482700`; `controls/base-c2-ops-debt.txt` `uncovered=4` → `uncovered=7` at `a0a4fd482700`; `controls/sources-census.txt` measured-tip note at `5826682b3781`), round-55 ×2 (`controls/c1-selftest-v2.txt` `32/32` → `44/44` at `64c0ce12ffe3`; `controls/c2-selftest.txt` fixture revision at `955e3d7bd6d1`), round-56 ×1 (`controls/c2-selftest.txt` `67/67` → `86/86` at `ad06cb8a17bd`). Counter kinds over the 13 undisclosed events: 6 `relabel`, 6 `rerun`, 1 `fill`. Derived from `controls/base-c1-receipt-rewrites.txt`: `events=19` − 6 disclosed by `receipt-errata.json` (all `relabel`) − 1 round-57 fill (row above) = 12 here. Harm: the two round-54 base controls had their *before* values rewritten, so no reader can tell what the round-54 counter measured. | none: the round-57 counter's population was revision lines only, and the round-57 landing table listed neither the `rerun` edits nor the rewritten base controls; the round-57 spot-check §2 C1 re-derived the 6 relabels only. | C1 ledger `.ufo/waves/round-58/receipt-rewrites.json`: one entry per event with path, commit, status, from/to blob ids, the counter's kind and a note whose pointer resolves at the tip. History is not rewritten — the receipts stay as committed, the disclosure is additive. Shown able to fail: base control prints the 19 events and `undisclosed=19` while the ledger is absent (`ledger: … absent (0 entries)`). |
| stale-premise | `c56_quote_truth.py` measured 2026-10-26: `8/8 met=True` exit 0 at its measured revision `4cb225fb032b04166fb0232bc98a7bcce72675ec`, and `6/8 met=False` exit 1 at the round-57 tip `20217f23eca1` and at the round-58 base `044048597d62f3199494b63b36e90dd57825e350` (`C8_mirror_bytes FAIL`, `registry rows 160 != mirror rows 156 + 2`). Its mirror is pinned to the 158-row registry, so the red is by design and the SKILL.md row `yahoo-crawl-handling-quote-truth-counter` (§Round 56 gate registry additions) advertises `0=met` for any `<commit>` that no later tree can reach; round-57 spot-check D3 carried the same item. | none: the round-56 criterion "a selftest that rebuilds from `HEAD` names its fixture revision in its row" covered selftests; nothing required a gate whose population moves to name its measured revision or leave the live set. | Register the row as historical, pinned: Name → `yahoo-crawl-handling-quote-truth-counter (historical, measured at 4cb225fb032b)`; Kind → `gate (historical — green only at its measured revision; a later tree fails C8 by design)`; Pinned values gains the pinned entry command `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision 4cb225fb032b04166fb0232bc98a7bcce72675ec` → `8/8` and the divergence `registry rows 160 != mirror rows 156 + 2`. No round-58 claim rests on it (C1/C2/C3 are the round-58 counters). Shown able to fail: the pinned form exits 0 while the same command at `cc8da16` exits 1 with `6/8`. |

## QUALITY:

Exact append text for `corpus/QUALITY.md`, after §Round-57 criteria:

```markdown
## Round-58 criteria

- **A receipt is written after the run it records; a placeholder is not a receipt.** A file
  committed under `.ufo/waves/round-5N/control(s)/` that carries a revision line and an exit code
  but whose body is `pending` records no run, and every counter that reads pins reads it as a
  receipt: `controls/after-c1-receipt-pins.txt` landed as `pending` at `31b61a4` and was filled at
  `20217f2` (`417ca0c615ba -> b514c80d7f36`) while the round-57 report said no receipt carrying a
  `revision:` line was rewritten. A re-run lands under a new name; a placeholder is never
  committed. Grounding: `corpus/lessons/round-58.md` §Mistakes (landing);
  `.ufo/waves/round-58/controls/base-c1-receipt-rewrites.txt` (exit 1, `undisclosed=19`, its last
  event is that fill); `corpus/lessons/round-57-verifier-spotcheck.md` §5 D1. Falsifier:
  `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision <tip>` must print
  `new_rewritten=0`, and the selftest case that rewrites a round-58 receipt — even disclosed —
  fails. Example that fails it: a receipt whose body is `pending` with `EXIT=0` and a true pin;
  its pin is honest, its run does not exist.
- **An edit to a committed measurement receipt is disclosed from git, with the values git shows,
  whatever kind it is.** 19 post-commit edits exist in the tip's ancestry (`events=19`), and the 6
  the round-57 errata disclosed are all revision-line relabels, so a disclosure population
  restricted to pins leaves 6 `rerun` edits and 1 `fill` unseen — including
  `round-54/controls/base-c2-ops-debt.txt`, whose before-state moved from `uncovered=4` to
  `uncovered=7` at `a0a4fd482700`. An entry names path, commit, status, from/to blob ids, the
  counter's kind, and a note whose pointer resolves at the tip; the note's prose is
  reviewer-checked, not counter-checked. Grounding: `corpus/lessons/round-58.md` §Mistakes
  (landing); `.ufo/waves/round-58/receipt-rewrites.json`; `controls/base-c1-receipt-rewrites.txt`.
  Falsifier: `python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision <tip>`
  must print `undisclosed=0 phantom=0 malformed=0 wrong_kind=0 unpointed=0`; its selftest carries
  a wrong blob, an invented commit, a duplicate entry, a false kind, a pointer-free note and a
  note naming an absent path. Example that fails it: a ledger note reading "re-pinned" with no
  path and no commit — the event exists, the disclosure does not (`unpointed`).
- **A gate that cannot be green on any later tree is registered as historical at its measured
  revision.** `c56_quote_truth.py` prints `8/8 met=True` exit 0 at `4cb225fb032b` and
  `6/8 met=False` exit 1 at `20217f23eca1` and at the round-58 base `0440485…`, with
  `C8_mirror_bytes FAIL: registry rows 160 != mirror rows 156 + 2`: its mirror is pinned to the
  158-row registry, so the divergence is by design and a live-gate row advertises a standing red.
  The row says `historical`, names the measured revision, and states what fails later.
  Grounding: `corpus/lessons/round-58.md` §Mistakes (stale-premise);
  `corpus/lessons/round-57-verifier-spotcheck.md` §5 D3; `SKILL.md`
  `yahoo-crawl-handling-quote-truth-counter`. Falsifier:
  `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision 4cb225fb032b04166fb0232bc98a7bcce72675ec`
  prints `8/8 met=True` exit 0 while the same command with `--revision cc8da16` prints
  `6/8 met=False` exit 1. Example that fails it: the row as it
  stands at the base, whose Verdict map promises `0=met` for any `<commit>` and whose cells name
  no revision; a reader takes the 6/8 as a current defect instead of a closed one.
```

## RED-BEFORE:

All outputs below were produced by me on 2026-10-26 from `/home/vgpnk/Projects/shokunin/kake-shokunin`;
copies in `ScribeLessonMistakes.files/`.

1. C1 counter at the base revision (do-nothing control) — exit 1, 19 undisclosed:

```
$ python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision 044048597d62f3199494b63b36e90dd57825e350
C1 receipt-rewrites events=19 undisclosed=19 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=0 met=False  (met: undisclosed == 0 AND phantom == 0 AND malformed == 0 AND wrong_kind == 0 AND unpointed == 0 AND new_rewritten == 0 AND new_receipts == 2)
  ledger: .ufo/waves/round-58/receipt-rewrites.json absent (0 entries)
  revision: 044048597d62f3199494b63b36e90dd57825e350
EXIT=1
exit=1;  19 `  UNDISCLOSED` lines
last event: UNDISCLOSED M .ufo/waves/round-57/controls/after-c1-receipt-pins.txt at 20217f23eca1 417ca0c615ba -> b514c80d7f36
```
   The committed twin `controls/base-c1-receipt-rewrites.txt` holds the same 19 events, `met=False`,
   `EXIT=1` (`exit=1`).

2. The placeholder that C1 must catch (M1) — three lines, pin and exit code with no run:

```
$ git show 31b61a4:.ufo/waves/round-57/controls/after-c1-receipt-pins.txt
pending
  revision: 32754df75774dd38e8a96fcda375fc93adf97f1e
EXIT=0
$ git log --format='%h %s' -- .ufo/waves/round-57/controls/after-c1-receipt-pins.txt
20217f2 round-57: C1 receipt written after its run at T0
31b61a4 round-57: T0 — … placeholder C1 receipt
```

3. One `rerun` example (M2) — a base control's numbers moved with no errata entry:

```
$ git diff 559bf9ba22ab 67a6902af5d6   # .ufo/waves/round-54/controls/base-c2-ops-debt.txt
-registry=absent manifest=absent uncovered=4
-cited=['CriticCrossLane.md', 'ReviewerProvenance.md', 'ScoutQuarantine.md', 'ScoutS329.md']
+registry=absent manifest=absent uncovered=7
```

4. The standing red gate (M3) — same script, three revisions:

```
$ python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision 4cb225fb032b04166fb0232bc98a7bcce72675ec
C2 quote-truth 8/8 met=True  (met: conditions_passed == 8 of 8)   → exit=0
$ python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision 20217f23eca1
C2 quote-truth 6/8 met=False (met: conditions_passed == 8 of 8)   → exit=1
$ python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision 044048597d62f3199494b63b36e90dd57825e350
C2 quote-truth 6/8 met=False …
  C8_mirror_bytes FAIL
    - registry rows 160 != mirror rows 156 + 2   → exit=1
```

## OPEN:

- **The round-57 report is not resolvable here.** `.ufo/reports/round-57/kake.md` is absent from the
  tip's ancestry (`git ls-tree -r 20217f23 -- .ufo/reports` → `round-20` only) and the commit the
  spot-check cites for it (`bdfe1efd…`) is a bad object, so M1's "the report said no receipt was
  rewritten" rests on the spot-check §5 D1 quotation, not on the report file. Not re-derived; the
  receipt history half of M1 is first-hand.
- **Brief arithmetic, reported not absorbed.** The assignment says "the 13 rewrites never disclosed
  in rounds 52–56"; the base receipt yields 12 in rounds 52–56 plus the round-57 fill (M1) = 13
  undisclosed in total (19 events − 6 errata-disclosed). The M2 row states 12 and the derivation.
- **What my red-before does not certify.** I measured the *base* states only. The after state
  (`receipt-rewrites.json` present, `met=True`), the C1 selftest, C2's 12/12 and C3's 8/8 were not
  run by me and are the C1/C2/C3 seats' and the L1's to measure; a fix counts only once the after
  run lands.
- **M3's fix is an integration edit, not a seat's.** I state the exact SKILL.md row text; I did not
  edit `SKILL.md`. `ScribeRegistryGate` confirms its seat covers only the two SOURCES rows (S423,
  S424) and the round-58 Gate block, so the §Round 56 gate row and the MISTAKES table are the L1's
  to place. The mirror repair (re-pinning C8 to
  the current registry) is not proposed: the assignment routes the gate to historical status, and
  a repair would change a closed round's receipt.
- **Classifier quirk worth knowing for the ledger.** `classify()` marks a changed line `relabel`
  when it contains `revision` or a 40-hex word, so
  `round-56/controls/c2-selftest.txt` (tally `67/67` → `86/86`, fixture revision unchanged) is
  typed `relabel` although the tally moved. The ledger notes should say what changed; the kind is
  the classifier's, not the truth of the edit.
- Not checked: round-57 spot-check D2 (untracked `w1/ExecPinsIndependent.files/relabels.json`) and
  D4/D5; no claim here depends on them.

VERDICT: Three mistake rows (2 landing, 1 stale-premise) and three round-58 QUALITY criteria drafted with failing examples; C1 base control and the c56 red re-measured first-hand (exit 1 / 6-8) while the after states and two routed limits (unresolvable round-57 report, 12-vs-13 arithmetic) stay open.
