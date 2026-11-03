# Round 71 w1 — ReviewContract (reviewer seat)

Attack of contract.md + amendment-1.md and counters c71_calibration.py / c71_tmp.py, all at freeze 04557e17, base cc6b4e0b.
All probes ran in scratch clone /fast/scratch/hyaku/kake-r71/ReviewContract/clone (tree deleted before yield; probe commits f03f1b97,
b0453671, 69836788, d6617ba6, 5b371a4c, ed954306, 70a64a7e, 13abed6f exist only there — outputs quoted verbatim below). Counters invoked as `python3 -B .ufo/waves/round-71/c71_*.py --lane <clone> --revision <rev>`. No tools installed; pacman untouched.

## Verdicts per assigned item
- (a) predicate sentences ↔ counter code: **holds** (C1/C2 met/mismatches/unannotated/guard implemented as written; caveats F7, F8).
- (b) population assumptions: **holds** — both committed base receipts reproduce byte-for-byte (exit 1 each); exactly 2 planned
  headings (line 21 bare, body `**Round 21**` @23 → r=21; line 3990 `— round 48`); exactly 1 stated `attack share 4/14`
  (line 4770; zero correction lines at base); w1-results.json n=14, strict k=3 (reviewer 1, critic 1, mutation-tester 1, labrat 0,
  revenger 1); SKILL.md exactly 7 `/tmp/` tokens, one per line 27,95,227,356,359,463,464; no bare-`/tmp` (slash-less) occurrences.
- (c) guards close deletion and rename gaming: **partly** — junk deletion, rename-wash and in-place rewrite are closed
  (probes below); repoint-to-bare-`/tmp` (F2) and round-70 data rewrite (F1) are open.
- (d) correction rule accepts only the recomputed value: **falsified** (F1 primary, F3 leniency).
- (e) amendment arithmetic: **holds** — 3+3+2+1+1+1+1+1 = 13 seats; attack 4 (reviewer 2, critic 1, mutation-tester 1);
  4/13 = 30.8 % ≥ 25 %; labrat-exclusion premise verified (skills/swarm SKILL.md:123-125 "Do not include frozen-topology seats
  (planner, distiller, labrat, Main) as swarm roles"); "no round-70 labrat" verified. Nit: F6.

## Findings by severity
- **F1 HIGH — C1 strict count is recomputed over TIP bytes of `.ufo/waves/round-70/w1-results.json`** (`show(lane, rev, RESULTS)`),
  and the guard covers SCORECARD.md lines only. A landed commit can rewrite round-70 history so the strict count equals the stated
  4/14 with NO correction line. Probe commit 69836788: C1 repair items 1,2,4 applied, item 3 omitted, one results row
  `"agent": "revenger" → "labrat"` (labrat ∈ STRICT_ROLES, n stays 14; flip verified in the commit tree). Output:
  `attack_stated=4/14 attack_strict=4/14 attack_mismatch=0 guard=ok mismatches=0 met=True`, exit 0 — the M1 defect passes uncorrected.
  Fix direction: read RESULTS at the frozen base rev (and/or guard the file against edits).
- **F2 MED — C2 accepts `${TMPDIR:-/tmp}` repoints**: token regex `/tmp/[A-Za-z0-9_.\-/]*` sees no `/tmp/` substring there, and an
  added line with any `mktemp` word passes the guard. Probe commit 70a64a7e: SKILL.md:27 →
  `` `${TMPDIR:-/tmp}/kake-r12/live/  # recreated via $(mktemp -d)` `` → `unannotated_tokens=0 guard=ok met=True`, exit 0, while the
  line still instructs a /tmp fallback. Latent only (zero bare-`/tmp` at base), but the guard does not close it.
- **F3 MED — C1 correction leniency vs kill rule**: `corrected = any(...)` accepts one correct-valued `Correction (round 71)` line
  even when another names a different number; the kill rule makes any differing-valued correction → unprovable. Probe commit
  b0453671: correct correction + `Correction (round 71): … attack share 9/99 …` → `met=True`, exit 0.
- **F4 MED — C2 repair rule is self-killing for lines 463/464**: they are imperative commands (`git -C … show b5d599e1…:SKILL.md >
  /tmp/kake-r23-…/SKILL-base.md`); the rule says "the other six lines are annotated", but corpus/QUALITY.md:14 ("Absence annotation
  content") fails "an annotation beside a still-imperative command", and the C2 kill rule turns that into C2 unprovable. Literal
  execution of the repair walks into its own kill; 463/464 must be repointed (mktemp) or rewritten non-imperative — rule says neither.
- **F5 LOW — C1 exit hygiene**: results JSON without `results` key → `KeyError: 'results'` traceback, exit 1, indistinguishable from
  red; should be exit 2. Also `if len(results) != N and N <= 0` is near-dead (`and` should be `or`): stated N ≠ len(results) never
  trips unevaluable. Probe P7 (`{"nope": []}`) → traceback, exit 1.
- **F6 LOW — bookkeeping**: frozen contract says "`w1`, 11 seats" and "4 of 11 (36.4 %)" but its own table has 12 rows; the amendment
  counts 13 (= 12 + ReviewRepair) and 4/13 = 30.8 % — internally right, yet the 11-vs-12 discrepancy is carried forward unnoted.
  No rule outcome flips (≥ 25 % holds at 36.4/33.3/30.8 %).
- **F7 LOW — C1 guard is non-positional**: "replaced by" means the superseded heading exists anywhere in tip; multiset diffing also
  permits moving section bodies anywhere (deleting them still fails). Fail-closed bonus: a `## Planned` heading with no parseable
  round counts stale — stricter than the contract's "naming a round < 72"; disclosed in the docstring; no base instance.
- **F8 LOW — counter identity not pinned at invocation**: the documented command runs working-tree counter bytes; currently identical
  to 04557e17 (`git diff 04557e17 -- <counters>` empty) and the kill rule covers later edits, but receipts should hash the counters.

## Guards exercised and holding
- Junk deletion: C2 delete the 7 token lines → `removed=7 added=0 guard=fail met=False` exit 1 (13abed6f). C1 relabel-wash of both
  planned headings to `## Planned — round 72` → `guard=fail met=False` exit 1 (d6617ba6).
- In-place rewrite of stated `4/14`→`3/14`, no correction → `guard=fail` exit 1 (5b371a4c): the append-only design holds.
- Honest repairs reach green exactly as contracted: C1 items 1–4 verbatim → `stale_planned=0 … mismatches=0 met=True` exit 0
  (f03f1b97); C2 line 95 → `$(mktemp -d)` + six annotated → `unannotated_tokens=0 guard=ok met=True` exit 0 (ed954306).
  `test -e` on all four cited /tmp targets exits 1 on this host (2026-11-03), so those absence annotations are truthful.

## Residual risk / verification gaps
- No LSP device is mounted for this seat (no server answers) — every check above is execution/text level; no semantic-index proof claimed. Kill-rule items (counter edit after first seat scored) are procedural, not machine-checkable here (F8 is that exposure); F1–F3 fix directions are recommendations — counters are frozen and were not modified (probes ran against unmodified 04557e17 bytes).
