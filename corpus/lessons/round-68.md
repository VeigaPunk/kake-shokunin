# Round 68 — lessons (kake)

Round opened 2026-11-01 on the Windows host at base
`396128196ffb1c3184a6dc4491da1e5612a3b425` (round-67 verifier spot-check tip,
pushed). Frozen contract: `.ufo/waves/round-68/contract.md` (predicates frozen
before any after-state). Python 3.13.15 (`python`; bare `python3` =
WindowsApps Store stub), node 24, git 2.55; no L2 dispatch surface (r65 L0
question stands, routed around). Carry-in: the r67 non-author spot-check §6
routed D-1 (report-header hash drift), D-2 (the ledger-wording count
re-measures 5 → 2 while every r67 record says 5 → 1; the described c56-row
rewording never landed) and D-3 (quote word-count label drifts) to this round.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| landing / number-drift (D1-class repeat, inherited from r67 and now closed) | the r67 after receipt `.ufo/waves/round-67/controls/greps-after-r67.txt` line "1 (after rewording the round's own c56 row …)" described a working-tree state that was never committed: at every r67 revision from `099923320` to the spot-check tip `3961281` the count re-measures 2 (`controls/greps-before-r68.txt` — the second match is the round's own REFUTED sentence, which contains the literal pattern phrase), while LOG/SCORECARD/lesson all said 1 | none at the r67 landing — the receipt was captured from the worktree after the ledger row was edited but before/without committing that edit; no "recorded count re-derives at a committed revision" check existed | the rewording LANDED this round as the spot-check's option 1 (the row's closing sentence now reads "The r65/r66 PYTHONUTF8 attribution is REFUTED by this differential."), with the dated `verified-at:` note; count re-measures 1 at the r68 tip (`controls/greps-after-r68.txt`, which SUPERSEDES the r67 line — the r67 receipt bytes are untouched); rule adopted: a count receipt must be captured at a committed revision (`git rev-parse` printed into the receipt), never from uncommitted worktree state |
| scope (repeat of the r67 S434 class, caught pre-commit this time) | the first S435 insert repeated the r67 mistake in a new guise: the BRE escape `\|` written literally inside a registry cell made the row 14 fields (census E01 class; awk NF!=13 found it at SOURCES.md line 289 before any commit) | the census malformed-row check (`awk -F'|' … NF!=13`), run immediately after the insert per the r67 lesson's own fix | the cell was reworded to name the operator in words ("the BRE escaped-alternation operator backslash-pipe") and the teaches cell likewise; malformed count 0 re-checked before any commit |

## Gate

Candidates: (a) land the spot-check-sanctioned c56 ledger rewording and make
the recorded ledger-wording count re-derive (C1, calibration — lowest owned
non-retired axis, 2); (b) re-verify on THIS host the three standing
property-map surfaces last dated 2026-10-21 (C2, freshness); (c) re-open S133
live again this round; (d) relabel any ledger row without a this-host pin run;
(e) rewrite the r67 receipt file or any other committed receipt; (f) adopt a
new considerthese proposal; (g) L2 wave.

- **Admit (a) as C1 — calibration 2→2 HOLD (measured, no score credit
  claimed).** Before: `grep -c "not adjudicated here\|candidate mechanism"
  corpus/knowledge/gate-status-ledger.md` = 2 at base `3961281…` and at
  `099923320…` (`controls/greps-before-r68.txt`) — the recorded 5 → 1 did not
  re-derive. After: the c56 row's closing sentence reworded
  (wording-only diff, exactly two lines changed with the dated `verified-at:`
  note — `controls/diff-ledger-r68.txt`), the same grep prints **1** at the
  r68 tip and the one remaining match is the out-of-scope historical
  c55_quote_truth row (`controls/greps-after-r68.txt`, which supersedes the
  r67 receipt's line; K5 held — no committed receipt bytes modified). Zero
  relabels; no row's class/disposition changed; the c66 counter reproduces
  `structural=0` at base and tip (`controls/c66-base-r68.txt`,
  `c66-tip-r68.txt`). Disclosure: `scripts/append_guard.py` base→tip receipt
  committed with the two sanctioned in-place lines disclosed
  (`controls/append-guard-r68.txt`).
- **Admit (b) as C2 — freshness 10→10 HOLD.** Three standing records last
  verified 2026-10-21 on the old host, probed GET-only once each on THIS host
  2026-11-01T09:58Z (`probes/receipt.json` + committed bodies): burnerchrome
  .kimi.page 200 / 11,975 B (property-map:c9/:c11 re-derive); lucario GHP
  200 / 3,435 B (:c33 re-derives); charter GHP front 200 / 53,660 B,
  sha256 `7c243a1d…7aba` EQUAL to `pins/charterGhpLiveSha` — the r18 pin
  re-derives byte-for-byte through 2026-11-01, and :c13/:c15 re-derive (one
  head canonical equal to the page URL). Dated corrections appended to
  `corpus/knowledge/publish-queue.md`. Counting command:
  `grep -c "r68 dated" corpus/knowledge/publish-queue.md` 0 → 1.
- **Reject (c):** S133 was re-derived against its RETAINED r67 body for the
  D-3 correction (presence + class, below); a fourth consecutive-round live
  re-open adds no new decision ground and the cadence sweep measured 0 rows
  due (`controls/cadence-sweep-r68.txt`) — no freshness claim rests on it.
- **Reject (d):** relabel without pin run — frozen rule K1 (r67) stands; zero
  relabels this round.
- **Reject (e):** rewriting committed receipts — K5; the supersession
  mechanism (a new receipt naming the old line) was used instead.
- **Reject (f):** `considerthese/` is unchanged since 2026-10-26 (newest file
  already evaluated: proposals 1–4 in r67, 5 adopted r66); shokuknow
  unreachable from this host. Assimilation: none.
- **Reject (g):** L2 wave — no dispatch surface on this host; the r65 L0
  question stands, routed around, never treated as answered.

### Fresh-start duty (§7), with the staleness noted

§7 of the rendered prompt declares a fresh-start round off the r62/r63/r64
rejections; r65, r66 and r67 were since admitted by non-author spot-checks
(commits `6a2ecb1`, `6ff73ed`, `3961281` — all verified ancestors of master
this round). The duty was honored anyway. Spot-checks: the r62 falsified
counter evidence exists and stands (`.ufo/waves/round-62/controls/
counter-false-green-l1.txt` + fixture), the r63/r64 kill-rule receipts exist
(`.ufo/waves/round-63/controls/`, `.ufo/waves/round-64/controls/after-final.txt`).
Ruled out and why: (1) any calibration claim whose green survives
marker-prose or a hidden criterion (the r62 falsified counter; the r63/r64
kill rules) — C1 promises no score credit and no agreement number; its delta
is a landing defect repair measured by a counting command anyone can re-run;
(2) counters without committed differential fixtures (r62 class) — no new
counter is claimed this round; the only instrument runs are the lane's
existing, receipted ones; (3) re-adjudication by relabel without this-host
pin runs (the r64 causation class) — frozen as K1, zero relabels; (4)
freshness via SOURCES recheck cadences — 0 rows due measured, so the
standing-record probe class was chosen instead; (5) claims a do-nothing
control can reach (§9) — both declared moves are defect-directed or
digest-bound (contract §Do-nothing controls).

### Sourced rows (opened this round)

- **S435 (new row this round)** — GNU Grep manual,
  https://www.gnu.org/software/grep/manual/grep.html — opened 2026-11-01,
  one GET (`curl -sS`), HTTP 200, 248,692 bytes, sha256
  `517177d0…675f37`, retained at `.ufo/waves/round-68/sources/S435-grep-manual.html`
  (receipt `.ufo/waves/round-68/sources/receipt.json`). Located quote
  (§2.1 Command-line Options, the `-c`/`--count` entry), **14 words — count
  derived by command (`wc -w`) BEFORE the label was written**:
  "Suppress normal output; instead print a count of matching lines for each
  input file." Class derived, not asserted: `collapsed-only`
  (`scripts/quote_class.py` over the retained raw body and the
  `extract_text.py` flat rendering; `controls/S435-quote-verify-r68.txt`).
  §3.6 Basic vs Extended Regular Expressions in the same body grounds the BRE
  escaped-alternation reading of the ledger-wording pattern. C1 rests on this
  row: the D-2 self-match mechanism IS the documented semantics (a count of
  matching LINES under a BRE alternation).
- S133/S434 were not re-opened live this round; their r67 retained bodies
  were re-derived for the D-3 correction: S434's Gate quote is a raw
  substring of the retained body; S133's derives **collapsed-only** (no raw
  claim was ever recorded for it — the class is now on record).

### Corrections (carry-in, recorded here; the r67 records are history and are not rewritten)

- **D-3 (quote labels).** Verified by command
  (`controls/wordcounts-d3-r68.txt`): the S133 Gate quote "an exit status of 0
  indicates that it ran successfully" is **10** words (the r67 label said 11);
  the S434 Gate quote "Use any character in the current code page for a name,
  including Unicode characters and characters in the extended character set
  (128–255), except for the following:" is **26** words by strict whitespace
  count (the r67 label said 16) — the r67 record therefore marginally exceeds
  the contract's ≤25-word cap. The corrected citation form going forward is
  the 22-word sub-quote ending at "(128–255)". Sites named: the r67 lesson's
  Sourced-claims bullet and the r67 report's Sources & frontier section (the
  same labels).
- **D-1 (hash citation).** The r67 report header names commit `b569bb638`,
  which is not an object name — one-char drift for the settlement commit
  `b569bb63a8bc2819553f08b4ce73eda12dc4d376` (correctly cited as `b569bb63`
  elsewhere in the same report). No rewrite of the filed report; the erratum
  is recorded here and in the r68 report. Discipline adopted: every revision
  name written into a receipt or report is re-derived with `git rev-parse`
  before it is written.
- **D-2** is C1 above (the substantive carry-in).
