# ReviewerContract

Whole-contract review, run LAST after all other w1 reports (41/41 peer reports on disk at write time).
Contract read at HEAD `142dda5` (post-Amendment-A1; base frozen text at `eaa9177`, base `9f07731a`).
My own measurements: population-144 == the loose path-rule enumeration at base exactly (diff 0,
`.files/`); 95 of 144 first committed versions carry the receipt grammar; SHONEN.md identical
base↔HEAD; registry 167 rows / census-before 15 W04 + `exit=0`; 16 non-rejected rows opened
2026-10-19 → due set S001–S010 verified; `c58_receipt_rewrites.py` + `receipt-rewrites.json` exist
at base. Sibling findings cited by seat; my findings independently derived where marked.

## FINDINGS:

### HIGH — blockers/major before the counter freeze

- **F1 (HIGH) — C2 case population (20) contradicts the frozen predicate (18).** Table: H1–H18 + R3
  + R4 = 20 rows under "18 fixture cases"; predicate `met: cases_passed == 18 of 18`; R4 expects
  `0/18`; the parenthetical "H-fixtures plus R3's run-recorded shape check" only reconciles with 16
  H-fixtures. C1 (16+2=18) is consistent; C2 is the outlier. Corroborates w1/ReviewerC2Contract F1,
  ExecC2Counter ambiguity 1 (its counter scores H1–H18=18 with R3/R4 as gate controls — one
  defensible reading). *Fix:* pre-freeze amendment pinning the denominator: either `20 of 20`, or
  explicitly "18 of 18 = H1–H18 scored; R3 shape-gates exit, R4 is the do-nothing control" (the
  landed counter's reading).
- **F2 (HIGH) — `extra_member` self-collision makes R2 unreachable on the honest build.** The receipt
  rule commits this round's receipts under `.ufo/waves/round-61/controls/`; the C1 path rule then
  flags them `extra_member` (outside the frozen 144). Already true at `eaa9177`: census-before.txt +
  population-144.txt match (146 vs 144 measured; w1/ReviewerC1Contract, CriticC1Semantics FR1,
  SentinelC1Bounds S4, ExecC1Counter, ConnCrossClaim Amendment A — independently reproduced in my
  `.files/`). The landed tool live-scans the population (sees 146), while the contract's member check
  is frozen-list (144) — the split is nowhere named. *Fix:* scope member/extra_member to population
  rounds N < measurement round, or exempt the declaring round's `controls/` prefix; state which
  population source the tool uses.
- **F3 (HIGH) — C3 condition C6 literally fails every conforming run.** "rows not in the due set are
  byte-identical to base" — the contract's own C2 appends S430–S433 (absent at base ⇒ not
  byte-identical). Corroborates w1/ReviewerC3Contract major + ConnCrossClaim Amendment B. *Fix:*
  rephrase: rows present at base outside the due set byte-identical; rows absent at base are strictly
  appended with next-unused ids; and pin S433's W04 as census-emitted, never an S088 row edit.
- **F4 (HIGH) — C1's motivation sentence is factually false at base.** "the lane owns no committed
  check for the class" — `.ufo/waves/round-58/c58_receipt_rewrites.py` and `receipt-rewrites.json`
  are committed at base (verified: `git cat-file -e`), SCORECARD cites its after receipt
  (events=19 undisclosed=0). Two ledgers now exist with divergent entry schema (c58: kind +
  from/to blobs + status; v1: path+commit only). SentinelC1Bounds S8. *Fix:* correct the sentence;
  name the c58↔c61 relationship (supersede with migration, or scope c61 to the gaps c58 misses).
- **F5 (HIGH) — The frozen span under-covers the claim title.** "undisclosed receipt rewrites become
  detectable": the 10-key span regex covers ~24% of receipt lines (575 of 2411, w1/ReviewerC1Contract
  measured). Verified by me via commit `a4a890cf`: r52 `c2-quote-real.txt`'s relabel
  `(fixture revision 3a50ae43…→1ae8de5d…)` is space-separated, escaping `revision\s*[:=]` — it and
  `a0a4fd48`'s two content rewrites are ledger events invisible to the frozen span (3 of 15). Also:
  colon-form JSON result fields (`"met": true`→false) invisible (CriticC1Semantics FG2); receipt
  deletion unmodelled — "a different blob" never matches an absent path, and the tool/counter split
  for `member_missing` is undefined (FG4, ReviewerC1Contract LOW). *Fix:* widen the span, add
  `revision\s+\S`, model deletions (absent path = event with empty span or member_missing), or name
  the residual classes under "What the counter does not test" and narrow the claim title.

### MEDIUM — defects a w2 falsifier can walk through

- **F6 — `scores_held == 3` has no failing witness.** No score-mutant case exists; the parsed cells
  are unnamed (whole-file/row-count reads break under C2's legitimate SCORECARD append).
  w1/ReviewerC1Contract. *Fix:* name a score-mutant selftest control + pin axis-table cells
  (operability=10, freshness=10, calibration=2).
- **F7 — C3 is vacuous without pins.** No C1–C6 condition requires ≥1 pinned row; a zero-fetch /
  ten-Gate-notes after-state passes 6/6 (w1/CriticC3Rule). *Fix:* require ≥1 pinned row, or require
  the ten named rows each pinned-or-noted.
- **F8 — Multi-URL due rows underspecified.** S001/S002 carry two URLs; "the row's URL"/"one fresh
  GET" forced the seats' first-URL choice: S001 anchor material lives in the unfetched URL → carried
  (ExecC3Fetch/Pins); S002 pinned with half its anchor unverified. C4's "receipt URL = row URL" is
  ambiguous for 2-URL rows (ScribeLessonMistakes). *Fix:* state first-URL-GET + a pin stands on the
  fetched URL only, with the Gate line naming unverified URLs (what the seats did) — or require all
  URLs.
- **F9 — `--disclosures` read scope unstated.** Committed `<rev>:<path>` vs worktree; the landed tool
  resolves committed-first then falls back to a filesystem read of an explicitly named path — a
  "committed bytes only" spec that permits worktree reads (SentinelC1Bounds S5; ReviewerC1Contract
  LOW). *Fix:* state committed-read as the default; absent-at-revision → zero entries.
- **F10 — `field_name_syntax` (H12) is a sixth class absent from the five-class enumeration**
  (ReviewerC2Contract F3; ExecC2Counter amb.2; both built tools implement it). *Fix:* name it in the
  class list.
- **F11 — `(base..revision first-parent history)` parenthetical is misleading.** All 144 files
  predate base; A1's `events=12` includes pre-base commits ⇒ operative semantics are unbounded-below
  first-parent history (SentinelC1Bounds S1, ReviewerC1Contract nit). *Fix:* strike the range phrase
  or write "unbounded-below".
- **F12 — `phantom_disclosure` punishes honest bookkeeping.** A disclosed cosmetic non-span edit →
  phantom finding (CriticC1Semantics FR3). A1's (path,commit)-only match also lets a wrong-kind or
  wrong-value entry cover an event — a deliberate relaxation of c58's falsifier, currently recorded
  only inside A1. *Fix:* scope phantom to population-receipt paths; name the kind-blind relaxation
  in "What the counter does not test".
- **F13 — `xcto_nosniff_value` fires only on present-but-wrong.** Missing XCTO is not flagged
  (w1/CriticC2Semantics, live-confirmed on real 200s); flag-gated vs literal reading deliberately
  undecided (ExecC2Counter amb.10). *Fix:* freeze the flag-gated reading; state "absent XCTO → no
  finding".
- **F14 — All-could_not_evaluate manifests fall in the exit-code gap.** per-check cne → exit 1 vs
  "exit 2 only when NO check is evaluable" collide for a valid manifest whose every check is cne
  (ExecC2Counter amb.7). *Fix:* pin exit 1-with-cne-findings.
- **F15 — Control receipts unmandated.** QUALITY r35 wants selftest controls "scored with the frozen
  counter and committed before the build"; the contract names them "(before data)" with no committed
  receipt or counter-sha256 (ReviewerC1Contract). *Fix:* require committed control receipts at freeze.

### LOW — errata and nits

- **F16** S430 line carries stray `rfc6790` URL token (ReviewerC2Contract F2; ScribeLessonMistakes);
  must not propagate into the row/Gate/entry.
- **F17** S431 blurb says "W3C CSP Level 3 REC"; the retained 2026-10-27 body is the Working Draft
  (ScribeC2Rows; ReviewerC2EntryQuotes). Fix the tier word.
- **F18** SHONEN section: "All four boxes stay `[~]` … with resolvable pointers" — committed
  SHONEN.md (byte-identical base↔HEAD, verified) has four `[ ]` boxes and no pointers; R60-D6 repeats
  the spot-check's `[~]` description. The contract misdescribes committed state (the report can still
  fill the section — see fillability). Fix: state `[ ]`-as-committed or fix the file.
- **F19** Dangling references: "contract rule 2" (C3 pin rule) and "§ Counter versions" (cosmetic —
  the operative surface is § Amendments + `amendments[]`).
- **F20** Frozen R2 row still reads `receipts=144 events=<k>`; A1 supersedes it with
  `receipts=95 events=12 undisclosed=0` — add an inline "(amended by A1)" on the row so a table-only
  implementor cannot hardcode the stale number (ReviewerC1Contract).
- **F21** Receipt rule scope: literal text covers `controls/` only; capture/, sources/, recheck/
  receipts fall outside the never-rewrite discipline (ReviewerC2Contract F6). One-sentence extension.
- **F22** Grammar `(?im)` scope: A1 pins `EXIT=` unanchored but not the `i` scope (95 case-insensitive
  vs 84 case-sensitive, ScoutC1Shapes). Fold "case-insensitive" into the A1 erratum wording.
- **F23** Finding-line schema `<kind> <path> <commit>` under-specifies member_changed/member_missing/
  extra_member/phantom_disclosure lines (extras/missings have no commit). Name the format.

## Checks the seat item names, stated plainly:

- **Predicates:** all three are one sentence each and identical between contract.md, contract.json,
  and the counter tasks (C3's task quotes it verbatim; C1/C2 tasks bind via "PREDICATE constant" +
  contract reference; ExecC2Counter prints `PREDICATE = "met: cases_passed == 18 of 18"` matching
  contract.json byte-for-byte). The only predicate-level defect is the number inside C2's (F1), not
  singleness.
- **Frozen tables:** C1 L1–L16+R1/R2 = 18 consistent with its predicate (with F2/F5 caveats on R2);
  C3 C1–C6 = 6 consistent; C2 table-vs-predicate inconsistent (F1). Pin dates verified:
  2026-10-19+90d = 2027-01-17, +365d = 2027-10-19; due set S001–S010 re-derived (16 non-rejected
  10-19 rows, lowest 10).
- **Amendment surface:** named and exercised — § Amendments section + contract.json `amendments[]`;
  A1 landed pre-freeze at `142dda5`, `predicate_unchanged: true`, resolving the `receipts=`/`EXIT=`/
  pending/span-set/dedup divergences I independently confirmed (95/144 receipts at base).
- **Report sections fillable:** claims — counter reports + selftest receipts exist for C2/C3;
  measurements — census-before exit 0 / 167 rows / 15 W04 verified, ExecC2Manifest findings=13
  recorded (not asserted), ExecC3Pins 9 pins + S001 carry, ExecC1History 12 events, ExecC1Disclose
  registry 12/12 exact (ExecC1DiscloseCheck); sources — S430–S433 bodies + receipts on disk, entry
  and rows drafted; trends — fillable from w1 evidence; SHONEN — fillable (F18).

## Residual risks / verification gaps:

- `c61_lineage_cases.py` is ABSENT: ExecC1Counter declared its own file incomplete (no fixtures,
  no population list, selftest not exercising the named controls). It must land and selftest before
  the L1 freeze or C1 has no counter.
- Disclosures registry, SOURCES.md appends + recheck-cell pins, the lesson, and the C2 entry are
  drafted but uncommitted — pending L1 integration; until they land, the after-state cannot evaluate.
- `receipts=`/`events=` at the final measured revision depend on whether round-61 control receipts
  enter the walked population (F2's population-source split) — must be pinned at freeze.
- w2 attack surface recorded but open: span coverage (F5), kind-blind disclosures (F12), C3 vacuity
  (F7), worktree-read disclosures (F9), scores_held mutants (F6).

VERDICT: Contract is consistent in predicates and C1/C3 table structure and the amendment surface works in-band (A1 landed pre-freeze), but three HIGH defects must be amended before the counters freeze — C2's 18-vs-20 denominator (F1), extra_member self-collision making R2 unreachable (F2), and C6 literal-fail on C2's appends (F3) — plus the false C1 motivation sentence (F4) and the overstated span coverage (F5) need correcting or explicit scoping; none of my checks found the contract unfillable once those lands.
