# ScribeLessonMistakes

Round-57 W1 · lane `kake-shokunin` · base `28fa0b23e699303725aba2727094531f5e44494d` · drafted against lane HEAD `f7c98ff269286723077848f3caf1422c4004f46d` (read-only; no lane file touched but this report).
Read: `corpus/lessons/round-56-verifier-spotcheck.md` §4/§6, `corpus/lessons/round-56.md` §Gate/§Mistakes, `corpus/QUALITY.md` (head, L1146–1217), `/home/vgpnk/Projects/shokunin/CORPUS.md` §Rules added from the kaika campaign, `.ufo/waves/round-57/contract.md`, `controls/base-c1-receipt-pins.txt`, `c57_receipt_pins.py`, `w1/ScoutRejectCanonical.md`, `.ufo/waves/round-56/sources/S388.html`.

MISTAKES TABLE:

Rows in the `round-56.md` §Mistakes shape (`| Class | Evidence | Captured-by | Fix |`), for `corpus/lessons/round-57.md`.

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| landing | Six measurement receipts in rounds 52–56 carry a revision pin rewritten to a revision no run backs, with no receipt-level disclosure: r52 `control/c1-ledger-real.txt`, `control/c2-quote-real.txt` `3a50ae43…`→`1ae8de5d…` at `a4a890cf` (paths under `.ufo/waves/round-52/`; the r55 and r56 pairs under `.ufo/waves/round-5{5,6}/controls/`); r55 `controls/after-c1-readme-index.txt`, `controls/after-c2-quote-truth.txt` `faf9abe8…`→`64c0ce12…` at `955e3d7b`; r56 `controls/after-c1-selftally.txt`, `controls/after-c2-quote-truth.txt` `f8438a28…`→`4cb225fb…` at `ad06cb8a` — the r56 pair is the receipt the round-56 report's "After (`4cb225fb`)" column cites. Hand-checked: each diff is exactly the one `revision:` line (`git show ad06cb8a17bd -- .ufo/waves/round-56/controls/after-c1-selftally.txt`, same for `after-c2-quote-truth.txt`; `git show a4a890cf1381 -- .ufo/waves/round-52/control/c1-ledger-real.txt`; `git show 955e3d7bd6d1 -- .ufo/waves/round-55/controls/after-c1-readme-index.txt`); `c2-selftest.txt` also moved `67/67`→`86/86` at `ad06cb8a` with its fixture pin unchanged. Only r52's commit message claims a re-run ("C1/C2 receipts re-run at 1ae8de5"); r55's and r56's messages name no re-run. Measured 2026-10-25: `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root . --revision 28fa0b23…` → `undisclosed_relabels=6 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0 met=False`, exit 1. Routed by `corpus/lessons/round-56-verifier-spotcheck.md` §6.1 | none (round 53 kept the practice in prose — `final-verify.txt` "not relabelled as verified" — but no QUALITY criterion or protocol rule forbade rewriting a receipt, and none required a relabel to be disclosed; the r56 spot-check routed it after the fact) | C1 counter + QUALITY round-57 criterion 1. Red-before: `.ufo/waves/round-57/controls/base-c1-receipt-pins.txt`, exit 1, 6 undisclosed (re-run 2026-10-25, byte-equal to the committed control). After: `receipt-errata.json` discloses every historical relabel with the four true fields and git agrees (no phantom entry), the three `controls/after-c{1,2,3}-*.txt` each carry the one revision in `measured.json` and are never rewritten, and the SCORECARD names that revision — predicate `met=True` |
| attribution | The round-56 S388 reject reason treats the Google/Bing clause as wholly unsupported. The reason as logged reads: and "writing it once covers Google and Bing too" is an unsupported inference. Flip: a lane row for the page, the real h3 as locator, three page-unique spans of at most 25 units, the Google/Bing clause deleted or tagged (`corpus/lessons/round-56.md` §Gate). The retained page prints `この記述は、Yahoo!検索だけでなくGoogle、Bingの検索エンジンにも共通の規格です。` (`.ufo/waves/round-56/sources/S388.html`, offset 4378, raw line 133, count 1; sha256 `115b4353…`, 9681 bytes), so the shared specification is on the page and only "covers" is the extension; the scout doc itself split the claim (`w1/ScoutRejectCanonical.md` L18-19: first half SUPPORTED, "so writing it once covers…" INFERENCE) and the durable reason and its flip dropped the split and would delete the supported half. Measured: `grep -c '共通の規格' corpus/lessons/round-56.md` → 0 against `grep -c '共通の規格' .ufo/waves/round-56/sources/S388.html` → 1. Routed by `corpus/lessons/round-56-verifier-spotcheck.md` §4 (S388 row) and §6.2 | none | QUALITY round-57 criterion 2 ("a rejection reason is re-read against the page before it is logged"), applied to this round's rejects. Fixed form: the reason names the page's own sentence and its locator (h3 `<link rel="canonical" href="">の記述方法と機能`) and keeps the shared-specification half, rejecting only "covers"; falsifier is the grep pair above (0 vs 1), which the fixed reason turns into 1 vs 1 |

Class decision (M1), stated once here so the row is not read as a coin-flip: **`landing`**, not `number-drift`. Precedent: round-26's `landing` row is "no committed code produced `manifest-retry.json`" — evidence at its canonical path that the run it names did not produce; `number-drift` (round-56's row) is a stated count that disagrees with what the documented command prints at the named revision. The six relabels are not values drifting from their measurement — the bodies are one-line edits of the provenance line, so the artifact claims a revision it was not run over. The r56 pair's `67/67`→`86/86` correction inside the same commit is the `number-drift` shape; it is carried in M1's evidence, not as a third row, because one defect is one row.

QUALITY CRITERIA:

Append target: `corpus/QUALITY.md`, after the last bullet at line 1217 (end of `## Round-56 criteria`): one blank line, then the heading at the same level (`##`), then the bullets in the file's `- **Title.**` body + `Grounding:` + `Falsifier:` style and ~140-column wrap of the round-56 section. Exact text:

```markdown
## Round-57 criteria

- **A receipt's revision pin is the revision its run covered, and a receipt is never rewritten.** A measurement receipt under
  `.ufo/waves/round-5[2-7]/{control,controls}/` names the revision the counter was run over; a later commit that edits that line, or a
  report column headed "after (`<rev>`)" for a receipt produced at another revision, is a relabel. A pin that no run backs is a defect even
  when the receipt's numbers are still true at the old revision. History is not rewritten: a historical relabel is closed by
  `receipt-errata.json` naming path, from, to and commit with git agreeing (no phantom entry), and a relabel of a receipt this round
  introduces is never disclosable — the counter is re-run at the named revision and the unedited output lands under a new file name. Six
  relabels across rounds 52–56 were undisclosed at the round-57 base. Grounding: `corpus/lessons/round-57.md` §Mistakes (landing);
  `corpus/lessons/round-56-verifier-spotcheck.md` §6.1; `.ufo/waves/round-57/controls/base-c1-receipt-pins.txt` (exit 1,
  `undisclosed_relabels=6`). Falsifier: `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root . --revision <tip>` must print
  `met=True` (exit 0); at the base it prints `undisclosed_relabels=6 … met=False`, exit 1, and its `--selftest` (19/19) carries the cases
  a pin-blind reading would accept (errata naming nothing git shows, a wrong `to`, a wrong commit, a deleted receipt, a relabelled new
  receipt, a non-ancestor measured revision, a stripped pin line, a round outside 52–57).
- **A rejection reason is re-read against the page before it is logged.** A reason that treats a clause as unsupported, or a page as
  silent, names the page's own sentence at the quoted locator and states what the page does say; only the extension beyond that sentence
  is rejected. Round-56's S388 reason called the Google/Bing clause an unsupported inference and its flip deleted the clause, while the
  retained page prints `この記述は、Yahoo!検索だけでなくGoogle、Bingの検索エンジンにも共通の規格です。` (offset 4378, once; 28 units, 47
  characters, quoted as the page's sentence, not as a Gate quote — the ceiling-compliant sub-span `Google、Bingの検索エンジンにも共通の規格です。` is 16 units, 28 characters): the shared specification is on the page and only "covers" is the extension, so the flip keeps
  the shared-specification half and rejects the extension. Grounding: `corpus/lessons/round-57.md` §Mistakes (attribution);
  `corpus/lessons/round-56-verifier-spotcheck.md` §4 (S388 row) and §6.2. Falsifier: `grep -c '共通の規格' corpus/lessons/round-56.md`
  prints 0 while `grep -c '共通の規格' .ufo/waves/round-56/sources/S388.html` prints 1 — the logged reason never states the sentence the
  page prints; a reason that re-read the page prints the sentence and its locator.
```

RED-BEFORE EVIDENCE:

M1, observed 2026-10-25 in this seat (not quoted from a committed receipt):

```
$ cd /home/vgpnk/Projects/shokunin/kake-shokunin
$ python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root . --revision 28fa0b23e699303725aba2727094531f5e44494d
C1 receipt-pins undisclosed_relabels=6 phantom_errata=0 deleted_receipts=0 new_relabelled=0 new_unpinned=0 new_receipts=0 scorecard_pin=0 met=False  (met: undisclosed_relabels == 0 AND phantom_errata == 0 AND deleted_receipts == 0 AND new_relabelled == 0 AND new_unpinned == 0 AND new_receipts == 3 AND scorecard_pin == 1)
  population=45 relabels_in_history=6
  UNDISCLOSED .ufo/waves/round-52/control/c1-ledger-real.txt 3a50ae4321e6 -> 1ae8de5d4dee at a4a890cf1381
  UNDISCLOSED .ufo/waves/round-52/control/c2-quote-real.txt 3a50ae4321e6 -> 1ae8de5d4dee at a4a890cf1381
  UNDISCLOSED .ufo/waves/round-55/controls/after-c1-readme-index.txt faf9abe81d1e -> 64c0ce12ffe3 at 955e3d7bd6d1
  UNDISCLOSED .ufo/waves/round-55/controls/after-c2-quote-truth.txt faf9abe81d1e -> 64c0ce12ffe3 at 955e3d7bd6d1
  UNDISCLOSED .ufo/waves/round-56/controls/after-c1-selftally.txt f8438a282d59 -> 4cb225fb032b at ad06cb8a17bd
  UNDISCLOSED .ufo/waves/round-56/controls/after-c2-quote-truth.txt f8438a282d59 -> 4cb225fb032b at ad06cb8a17bd
  revision: 28fa0b23e699303725aba2727094531f5e44494d
EXIT=1
```

- Same command redirected and compared: `diff <(grep -v '^EXIT' controls/base-c1-receipt-pins.txt) <(… > out)` → empty, `BYTE-EQUAL-TO-CONTROL` (the committed control is reproducible today). The redirect target was `/tmp/c57pins.out`, outside the lane; no lane path was written.
- `python3 -B .ufo/waves/round-57/c57_receipt_pins.py --selftest` → `c57 receipt-pins selftest: 19/19`, exit 0.
- The counter reads only git history at `--revision` and uses `tempfile` sandboxes for its selftest; no repo path is written. The green state of the fix (`met=True`) is UNRUN: at HEAD `f7c98ff` there is no `.ufo/waves/round-57/receipt-errata.json`, no `measured.json` and no `controls/after-c*` receipt, so the predicate cannot yet be met.
- M2's red-before is the grep pair above: `grep -c '共通の規格' corpus/lessons/round-56.md` → `0`; `grep -c '共通の規格' .ufo/waves/round-56/sources/S388.html` → `1`. Both run today (exit 1 and exit 0 respectively — `grep -c` exits 1 on zero matches).

OPEN:

1. **Green half of M1 unrun.** No `receipt-errata.json`, `measured.json` or round-57 `after-c*` receipt exists at HEAD, so `met=True` is not observed; only the red-before is. The criterion's Falsifier line therefore states the expected green output, not a measured one.
2. **No round-57 reject exists yet to apply criterion 2 to.** `corpus/lessons/round-57.md` does not exist at HEAD; the C3 claim admits both entries and the quarantine-slice verdicts are not reject reasons. Criterion 2's only instance today is the r56 one, which is what its failing example uses. If the round-57 lesson logs a reject, that reason should be the applied case.
3. **Locator base differs from the spot-check's.** `round-56-verifier-spotcheck.md` §4 cites the S388 sentence at "line 23"; in the raw retained body it is line 133, offset 4378 (count 1, sha256 `115b4353…`, 9681 bytes). Both are the same sentence; I report the raw-body coordinates because the retained body is the artifact a re-read opens.
4. **M1 class is a decision, not a measurement.** `landing` is argued from the round-26 precedent and the one-line diffs; `number-drift` stays defensible for the r56 pair's `67/67`→`86/86` tally correction. If the canonical judge prefers one class per shape, splitting the tally correction out of M1 is the alternative.
5. **The r56 `67/67` reading is cited, not re-measured.** I did not run `c56_quote_truth.py --selftest` at `4cb225fb`; the `67/67` and `86/86` values are the committed `controls/c2-selftest.txt` versions (`git show ad06cb8a17bd -- …/c2-selftest.txt`), and "not a run over `4cb225fb`" is the r56 spot-check's finding, reproduced only in the sense that the diff is one line.
6. **r52's re-run claim is prose only.** Its commit message says "C1/C2 receipts re-run at 1ae8de5", which the counter still counts as undisclosed (no errata entry); I did not verify whether a run happened, and the criterion treats the missing four-field disclosure as the defect, not the missing run.
7. **Tooling:** nothing installed or upgraded this seat; no pacman transaction.

VERDICT: M1 drafted as `landing` (six receipt relabels, red-before reproduced at base: exit 1, 6 undisclosed, byte-equal to the committed control; selftest 19/19) and M2 as `attribution` (r56 S388 reason and flip, page sentence at offset 4378 count 1), with two `## Round-57 criteria` rows appended after line 1217; the C1 green state and any round-57 reject instance are unrun.
