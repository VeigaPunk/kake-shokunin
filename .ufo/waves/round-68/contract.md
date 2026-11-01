# Round 68 contract — kake (frozen before any after-state measurement)

Base (round-67 verifier spot-check tip, pushed):
`396128196ffb1c3184a6dc4491da1e5612a3b425`. Host: Windows, python 3.13.15
(`python`; bare `python3` = Store stub), node 24, git 2.55. Frozen before any
claim's after-state exists. Receipts live under `.ufo/waves/round-68/controls/`
(claims/corrections), `.ufo/waves/round-68/probes/` (freshness probes) and
`.ufo/waves/round-68/sources/` (retained source bodies). Every count below
carries its counting command.

Carry-in (r67 non-author spot-check §6, all three addressed this round):
D-1 report-header hash citation (`b569bb638` is not an object name; the
settlement commit is `b569bb63a8bc2819553f08b4ce73eda12dc4d376`); D-2 the
ledger-wording count re-measures **5 → 2** at every revision since `099923320`
while LOG/SCORECARD/lesson and `controls/greps-after-r67.txt` say 5 → 1, the
described c56-row rewording never having landed; D-3 the r67 Gate quote-label
drifts (S133 claimed 11, S434 claimed 16).

## Claims

### C1 — calibration (lowest owned non-retired axis, score 2): the recorded ledger-wording count re-derives at the tip; the last r67 recorded-count drift is eliminated

Before-state (measured, receipt
`controls/greps-before-r68.txt`): at base `3961281` and at the r67 work
commit `099923320`,
`grep -c "not adjudicated here\|candidate mechanism" corpus/knowledge/gate-status-ledger.md`
prints **2** (the out-of-scope historical `c55_quote_truth` row AND the r67
`c56_selftally` row, whose REFUTED sentence self-matches), while the committed
r67 settlement records (LOG round-67 entry, SCORECARD C1 row, lesson round-67
Gate, `controls/greps-after-r67.txt`) all say **1** — the recorded count does
not re-derive at the revision it names (the r67 spot-check D-2).

Move (the spot-check's option 1, sanctioned): land the described c56-row
rewording — the row's final sentence becomes "The r65/r66 PYTHONUTF8
attribution is REFUTED by this differential." (verified-class, mechanism and
disposition untouched: `live | e_T=2 | live_not_green | PROVEN r67` all stay);
the `verified-at:` header line gains a dated r68 note naming the spot-check
defect so the change is not silent. After-state: the same grep prints **1** at
the r68 tip, and every committed r67 settlement record re-derives as written.

Frozen decision rules:

- Wording-only: `git diff base..tip -- corpus/knowledge/gate-status-ledger.md`
  may touch exactly two lines (the `c56_selftally` row and the `verified-at:`
  line); no row's Gate/Registry-label/Class/disposition cell changes; zero
  relabels (K1 of r67 stands — no pin run exits 0 on this host).
- The one remaining grep match at tip must be the out-of-scope historical
  `c55_quote_truth` row.
- Supersede, never edit: the r67 receipt line "1 (after rewording …)" is
  superseded by `controls/greps-after-r68.txt` (naming the r67 line and the
  state at its named revisions); `controls/greps-after-r67.txt` bytes are not
  modified (no receipt-rewrite event).
- Disclosure: `scripts/append_guard.py` is run base→tip over
  `corpus/knowledge/` and its receipt committed; the two sanctioned in-place
  lines are disclosed as guard findings with their sanction pointer (r67
  spot-check §6 D-2), not silently normalized.

Kill rules (any → C1 fails):

- K1: any ledger row relabelled without a this-host pin run exiting 0.
- K2: any count recorded anywhere this round without its counting command.
- K3: the c66 counter at the tip does not reproduce
  `members=28 evaluated=28 structural=0 agreement=18 scores_held=3/3 met=True`
  exit 0 (no structural harm from the edits).
- K4: the offline freshness sweep does not exit 0 at the tip.
- K5: any rewrite of a committed r67 receipt file.

Counting commands: the grep pair above (before at base/`099923320`, after at
tip); `git diff base..tip --numstat -- corpus/knowledge/gate-status-ledger.md`;
the c66 counter line; `ls .ufo/waves/round-68/controls/ | wc -l`.

Do-nothing control: a control reaches none of this — the rewording is
defect-directed (names the specific committed self-match), the superseding
receipt names the r67 line it replaces, and the guard disclosure requires the
diff this round actually makes.

Sourced-claim binding: this claim rests on **S435** (GNU grep manual, opened
this round): the counting command's documented semantics — `-c` counts
matching LINES per file, and the pattern is a BRE using the escaped alternation
`\|` — are also the mechanism of the D-2 self-match (a sentence containing the
phrase counts as a line). Gate record in `corpus/lessons/round-68.md`.

### C2 — freshness (10, HOLD): three standing property-map records last verified on the old host re-verified GET-only on THIS host with dated corrections

Before: the three surfaces below are dated only 2026-10-21 (old Linux host,
property-map receipts) and `grep -c "r68 dated" corpus/knowledge/publish-queue.md`
= 0:

- `https://burnerchrome.kimi.page/` — property-map:c9 (live surface) /
  c11 (Kimi-published), r23 2026-10-21.
- `https://veigapunk.github.io/lucario/` — property-map:c33 (live-200),
  r23 2026-10-21.
- `https://veigapunk.github.io/charter-ufo-fsd/` — property-map:c13 (live,
  final URL matches) / c15 (head canonical equals the GHP URL), r23 2026-10-21.

After: each probed GET-only on this host 2026-11-01, receipt
`probes/receipt.json` + committed bodies/headers, digests computed
mechanically from the committed bytes; each record's r68 observation appended
as a dated correction under `## r68 dated corrections` in
`corpus/knowledge/publish-queue.md`; `grep -c "r68 dated"
corpus/knowledge/publish-queue.md` ≥ 1 at the tip. Verdicts report what the
GET shows (status, bytes, digest, title/marker where applicable) and never
round up: half-states get named verdicts per the standing rule.

Kill rules: any non-GET action (publish/deploy/fire) — forbidden outright; any
SKILL.md property-table edit (sidecar-bound lines stay untouched; K4 guard);
any digest asserted without being computed from the committed body.

Do-nothing control: a control cannot produce this-host dated receipts whose
digests re-derive from committed bytes, nor the publish-queue section.

## Corrections (carry-in, protocol work — not claims)

- D-1: the r67 report's header commit name `b569bb638` is a one-char drift for
  `b569bb63a8bc2819553f08b4ce73eda12dc4d376`; per the spot-check, no rewrite
  of the filed report — the erratum is recorded in the round-68 report (and
  lesson), naming the superseded text. Cite-by-hash discipline: full shas or
  helper-printed prefixes only; a pasted name must be re-derived with
  `git rev-parse` before it is written.
- D-3: verified word counts recorded in `controls/wordcounts-d3-r68.txt`:
  S133 Gate quote = **10** words (label claimed 11), S434 Gate quote = **26**
  words by strict whitespace count (label claimed 16; the r67 record marginally
  exceeds the ≤25-word cap and stays as recorded history — the corrected
  citation form going forward is its 22-word sub-quote). Corrections land in
  the round-68 lesson + report naming the superseded labels; the r67 lesson's
  recorded lines are not rewritten. Quote presence/class re-derived with the
  lane's r50 machinery: S434 raw-substring of the retained body; S133
  collapsed-only.
- Fresh-start §7 duty (see the round report for the full ruled-out list), the
  cadence sweep (`controls/cadence-sweep-r68.txt`: 0 rows due), and the
  r65/r66/r67 non-author spot-check commits verified as ancestors of HEAD.

## SOURCES clause (carried from the r67 amendment 1, recorded pre-row)

Append-only; at most ONE new row this round (S435, GNU grep manual), written
only after the source is opened this round with a retained body, and a Gate
record carrying URL, access date, command, byte count, digest and a located
quote whose word count is VERIFIED BY COMMAND before the label is written.
`status`/`recheck`/`used-by` changes are logged old→new in the lesson.
