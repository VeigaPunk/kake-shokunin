# Kake round 59 — frozen contract (predicates declared before any data)

Lane: kake-shokunin. Base revision (lane master tip at round open, = `BASE_REV`/`BASE` in the counters):
`fd6303ce5c14b3f892dec586297a942ab6e4193b` (the round-58 non-author spot-check). This file, `contract.json`, the three counters
(version 1), the derive scripts, their base-control receipts, the two retained source bodies with receipts and the pre-append
registry mirror are committed together before any build edit and before any seat scores. The predicate sentence of each claim is
the same sentence here, in the counter's code (`PREDICATE`) and in every receipt label. Round opened 2026-10-26 (-03:00); the two
source fetches ran 2026-10-27T01:21:22Z, so the **access date** of every row, Gate line, `verified-at:` and correction tag is
`2026-10-27` (UTC). Round shape: ONE v2 wave (`w1`, build + attack items together, >= 25 % attack roles, 64–128 seats) plus at most
one residual handoff of <= 8 reviewer/critic seats; round total <= 128. The L1 (KakeR59) holds the canonical planner seat (the
validator rejects `planner`). Seats are read-only except their own report file and a `<Seat>.files/` directory beside it.

Receipt rule (round 58, kept): a receipt under `.ufo/waves/round-59/controls/` is committed once, after the run it records, and never
rewritten; a re-run lands under a new file name. No placeholder receipt is committed.

Routed defects of the round-58 spot-check (`corpus/lessons/round-58-verifier-spotcheck.md` §6): D1 → claim C3 condition C9; D2 →
fixed forward in all three round-59 counters (inherited `GIT_*` scrubbed, `--base`/`--revision` resolved once to commit ids, `--root`
must be a repository toplevel) and, for the tool, claim C2 cases K11/K12/K14; D3 (present quarantine rows) → still held: the L0
question of round 58 has no answer, so nothing from the quarantine slice is appended (routed around, not treated as answered).

## Axis declaration

The prompt-declared lane axes are operability + freshness; the scorecard also carries the round-54 bounded sub-axis **calibration**
(score 2, the lowest-scoring non-retired axis), so the lowest-axis obligation lands on C1. The ownership question stays open for the
operator, as in rounds 55–58. Three claims on three distinct axes: C1 calibration, C2 operability, C3 freshness (sourced). No
exploratory claim. Causal separability: C1 reads only `SCORECARD.md` (axis table, round sections) and the blobs its cells cite; C2
reads only `scripts/id_resolver.py` and gate-built fixtures (P7 reads the lane's registry/knowledge, floor `ids_cited >= 106`, which
holds with or without C3's rows); C3 reads only its two entries, `crawler-identity.md`, their rows, the lesson Gate and the round-59
evidence files. C1's after-cells may cite C2/C3 receipts only if those land first; the C1 counter does not require it.

## Claim C1 — calibration: the SCORECARD axis table's evidence cells match committed state

Surface: `SCORECARD.md` axis table (`| Axis | Score | Evidence pointer | Last change |`; rows operability 10, freshness 10,
calibration 2) — the lane's self-assessment of its owned axes. Observed state: the committed tree at the measured revision.
- Before (base): `mismatches=16 unresolved=11 rows_no_receipt=3 receipts_off_axis=0 tallies_unfound=0 rows_no_tally=2 rows=3
  scores_held=2 superseded_kept=0 met=False`, exit 1 (`controls/base-c1-axis-evidence.txt`). The operability row points at
  `cli.mjs:935` and three line continuations in a source tree the lane no longer holds; the freshness row at six `/tmp/kake-r17/…`
  files (deleted; `/tmp` is never citable, prompt §7.5) and the vanished `corpus/claims`; no row cites a committed receipt.
- After: every axis cell names only committed paths, cites at least one on-axis receipt and states at least one tally found in a
  cited blob; operability/freshness scores unchanged; the three base cells kept verbatim outside the table.
- Counter: `python3 -B .ufo/waves/round-59/c59_axis_evidence.py --root <lane> --revision <rev>`.
- Predicate (frozen): **met: mismatches == 0 AND rows == 3 AND scores_held == 2 AND superseded_kept == 3**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: base, exit 1, 16 mismatches. Emptied cells fail (`rows_no_receipt`, `rows_no_tally`, `superseded_kept`); a
  receipt of a round with no claim on the axis fails (`receipts_off_axis`); a tally absent from every cited blob fails.
- What the counter does not test: whether a cited receipt supports the score (reviewer-checked); evidence outside the table.

## Claim C2 — operability: `scripts/id_resolver.py` closes seven disclosed false-green / robustness routes

Surface: the lane tool `scripts/id_resolver.py` (round-57 capability, round-58 fence fix). Routes disclosed after the round-58
freeze: HTML-comment registry row (w1/ReviewerResolverOther c01), setext section end (c06), in-lane symlinked knowledge dir (c07a),
revision-mode committed symlink read as its target string (w1/SentinelCounters F2), registry symlinked out of the lane (F5),
non-UTF-8 file name fatal at `--revision` (r1/ReviewerResolverDiff F1), non-toplevel `--root` measuring an ancestor (F6).
- Before (base): `13/21 met=False`, exit 1 (`controls/base-c2-resolver-cases.txt`, seed 59): K8–K14 fail, P6 fails (59 < 66).
- After: 21/21.
- Counter: `python3 -B .ufo/waves/round-59/c59_resolver_cases.py --root <lane> --revision <rev> [--work <scratch>] [--seed N]`.
- Predicate (frozen): **met: cases_passed == 21 of 21**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: base 13/21, exit 1. The round-58 cheat classes (constant green, always-exit-1, id masks, canned output) are
  ported into the gate selftest by wave 1 before data.
- What the counter does not test: P6 reads a printed tally (disclosed since round 58); `.markdown`, zero-width-split ids,
  markdown outside `corpus/knowledge` (contract-ambiguous).

## Claim C3 — freshness (sourced): the stale crawler-identity claim corrected on rows opened this round

Surface: `corpus/knowledge/crawler-identity.md` line 31 states "A user-agent string is the only thing a server log records about the
crawler" (routed since round 51; round-58 spot-check D1). Google's crawler overview (re-opened 2026-10-27) says its crawlers identify
themselves by user-agent, source IP address and reverse DNS hostname, and that "your logs may show visits from several IP addresses".
- Rows: S425 = staged S398, renumbered by document (`https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers`,
  retained `sources/S425.html`); S426 lane-found, linked from S425's "Learn how to use these details to verify" sentence
  (`…/verify-google-requests`, retained `sources/S426.html`). Both opened 2026-10-27.
- Entries: `corpus/knowledge/crawler-identity-signals.md` (S425; staged `crawler-identity-three-signals.md` re-grounded, staged name not
  carried), `corpus/knowledge/googlebot-verification.md` (S426); an append-only `[r59-correction 2026-10-27]` tail in
  `crawler-identity.md` citing S425.
- Before (base): `0/9 met=False`, exit 1 (`controls/base-c3-quote-truth.txt`); registry 162 rows.
- After: 9/9; registry 164 rows.
- Counter: `python3 -B .ufo/waves/round-59/c59_quote_truth.py --root <lane> --revision <rev>` (generated by
  `derive_c59_quote_truth.py` from the round-58 counter version 2; conditions C1..C9 in its docstring).
- Predicate (frozen): **met: conditions_passed == 9 of 9**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: base 0/9, exit 1. C9 fails on a correction that rewrites or deletes the stale line, sits away from it, or
  quotes a span the page does not hold.
- What the counter does not test: whether the English entries are faithful (reviewer/critic-checked); quote truth, not support.

## Frontier step and assimilation (inside the claim cap)

SOURCES census at round start: exit 0, 162 rows, 14 W04 (`controls/census-before.txt`). Collision check (0–3-space pattern):
reg 162, staged 129, collisions 8 (S312 S329 S367 S372 S373 S374 S390 S409, the round-57/58 set) — S398 does not collide; renumber
map S398 → S425 by document. Quarantine slice: 12 rows (`assimilation/quarantine-slice`), unchanged; nothing appended (L0 open).
Assimilation theme: `crawler identity verification signals` from `merge/kake/`. Reject candidates screened in wave 1: the staged
`amendments/corpus/knowledge/crawler-identity.md` (round2) and `yahoo-crawler-ua-carrier-survey.md`.
Mined mistakes (to be shown able to fail): routed defect D1 carried seven rounds unrepaired (C3 C9, base 0/9); axis evidence pointing
at `/tmp` and a removed tree while scores stayed 10 (C1, base 16 mismatches).

## Counter versions — version 2 (after wave 1, before any claim was measured)

Wave 1 (66 seats, `w1/`) attacked every version-1 counter before data. Version 1 stays committed at `45a92b64` as history; version 2 is
what the claims are judged on. Base controls were re-run under version 2 under new file names (`controls/base-c{1,2,3}-*-v2.txt`); the
version-1 receipts are never rewritten. Disclosure: during integration the L1 ran the drafted C1 cells through the C1 working copy in
a scratch clone (and wave-1 scribes trial-scored their single rows under version 1, as assigned); the C1 changes made after the first
L1 trial (receipt directory rule, passing-receipt rule, symlink rule, superseded-heading rule) all tighten. The one loosening in version
2 is C3's row-title floor (6 -> 3 units), made because a faithful English title could not pass; no C3 after-state had been scored.

- **C1** (`c59_axis_evidence.py` v2). Predicate (frozen, version 2): **met: mismatches == 0 AND tables == 1 AND rows == 3 AND axes_ordered == 1 AND scores_held == 2 AND superseded_kept == 3**.
  Changes (each tightens): exactly one rendered axis table — HTML comments, fenced code and indented code do not count
  (w1/CriticC1Parse, w1/CriticC1Cheat shadow table); unescaped-pipe cell split (w1/CriticC1Parse false red); path mentions outside code
  spans, `<code>` spans and Unicode slash lookalikes are pointers (w1/CriticC1Cheat); a committed symlink never resolves
  (w1/SentinelCounters F1/F2); a receipt lives under `round-N/control(s)/` (w1/LabratC1Controls) of a round before 59 whose
  base-revision section is kept verbatim and holds a table row whose `axis` column begins with the axis name (w1/CriticC1Cheat); a
  tally must occur in a cited on-axis receipt (w1/CriticC1Cheat); each row cites at least one receipt of a met / exit-0 run
  (`rows_no_passing_receipt`, w1/ReviewerC1Contract); replaced cells are kept under a `## ` heading naming them superseded, outside
  comments (w1/ReviewerC1Contract, w1/CriticC1Cheat); the row-order rule is in the predicate (w1/ScribeC2SkillRows finding 1).
  Selftest: L1-written 24-case matrix (`controls/c1-selftest-v2.txt`); w1/ExecC1Selftest's version-1 matrix stays as wave evidence.
  Base under v2: `mismatches=24` (11 unresolved, 3 rows without a receipt, 3 without a passing receipt, 4 tallies unfound, 3 rows
  without a found tally), exit 1. Stated limits: whether a cited receipt supports the score (reviewer-checked); a tally can occur in
  a receipt without being its own result (w1/CriticC1Cheat coincidental tally).
- **C2** (`c59_resolver_cases.py` v2). Predicate unchanged: **met: cases_passed == 21 of 21**. Gate selftest = the 13-control port of
  w1/ExecC2GateSelftest (base 13/21, cheats 1–15/21, full_fix 21/21; `controls/c2-selftest-v2.txt`); a hanging tool run fails its case
  (exit 124) instead of crashing the gate (w1/SentinelResolver FIFO); fixture URL hosts are drawn from the seed instead of the constant
  `example.invalid` (w1/ReviewerC2Counter H1: a fixture-keyed tool could tell fixtures from the real lane). Stated limits demonstrated by that port and w1/MutC2Gate: P6
  trusts a printed tally (a real defect plus `selftest: 66/66` scores 21/21); K12/K14 are reason-blind; K9 alone is passed by an exact
  `---` dropper. w1/MutC2Gate's eight proposed cases Q1–Q8 (validated 29/29 on a green tool) are carried to a later round, not
  added here. Tool-side hardening beyond the 21 cases (FIFO skip, dangling-link skip, descriptor-level containment, thematic break)
  is verified by the tool's own selftest and the residual reviewers, not by this counter.
- **C3** (`c59_quote_truth.py` v2). Predicate unchanged: **met: conditions_passed == 9 of 9**. Changes: `Last updated` read only
  outside <script>/<style>; anchor headings exclude <pre>/<code>; page chrome (<aside>, <nav>, feedback/rating widgets) is not article
  text (w1/ExecC3BaseControls H2); C9 attaches the correction exactly where the stale bullet ends and reads tag, citation and span as
  rendered prose (comments, code spans and tag attributes removed; w1/CriticC3Cheat, w1/ExecC3SelftestPort); row-title floor 3 units
  (loosened, above). Selftest: w1/ExecC3SelftestPort's matrix plus one chrome-span case, 121/121 (`controls/c3-selftest-v2.txt`).
  Base under v2: 0/9, exit 1. Stated limits: a tagged correction that restates the stale claim, and prose that contradicts true quotes,
  still meet (quote truth, not support; w1/ExecC3BaseControls H4, (b)).
