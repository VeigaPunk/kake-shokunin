# ConnMistakeClasses

Cross-round mistake mining over rounds 50–57: every `## Mistakes` section in
`corpus/lessons/round-5[0-7].md` (incl. round-51's two Mistakes sections) and every routed-defect
section in `round-5[0-7]-verifier-spotcheck.md`.

## CLUSTERS

Six recurring classes (counts = distinct rows/defects I counted across the 8 lesson files + 8
spot-checks; a class is counted once per round per source):

1. **landing (settlement / receipt provenance / committed-vs-claimed)** — 13 instances, all 8
   rounds (50–57). Sub-clusters:
   - (a) seat/settlement accounting stated in prose, not re-derivable: r50 spotcheck D1 (report
     said 26 reports, tree holds 25); r51 mistake (seat-report count prose-only); r52 mistake 1
     (dispatch "never ran", 0 seats); r52 spotcheck D1 (report claimed pushed, commits not on
     remote); r53 mistake row 2 + spotcheck D1/D2 (40 spawned, 0 committed reports, evidence
     pointers unresolved); r54 mistake row 2 + spotcheck D1/D4 (silent single wave; settlement
     precedent); r55 mistake `landing` (r54 shape) + spotcheck D3 (dead seats returned other
     lanes' output).
   - (b) receipt revision provenance: r51-attempt2 mistake (frozen artifact scored by a
     later-amended instrument); r56 spotcheck D1 (after-receipts committed at one revision,
     revision line edited at another); r57 mistake `landing` (six receipt revision pins rewritten
     across rounds 52–56, no disclosure) + r57 spotcheck D1 (r57 after-c1 receipt committed as
     `pending`, filled in later, while report said no receipt was rewritten).
2. **number-drift** (stated counts disagree with documented commands) — 4 instances, rounds
   55, 56, 57: r55 mistake row + r55 spotcheck D1 (SKILL registry selftest tallies 35→44,
   47→51); r56 mistake row (7/10 gate-registry rows disagree with what their command prints; the
   lesson itself notes the class "recurred inside round 55's own report"); r57 mistake row
   (lesson draft counts wrong).
3. **vacuous / false-green counters** (a counter meets its frozen predicate under junk or
   do-nothing input) — 4 instances: r51-attempt2 mistake (C1 scored 3/3 on empty wave/phantom
   seat/500-ok receipt); r55 mistake row (v1 counters met under junk; v2 attacked); r56 mistake
   row (v1 passes under fake command/dup row/host pin; 6/16 mutants survive); r57 mistake row
   (all three v1 counters met by do-nothing; C3 by junk files/sidebar markup, v2 by judge-import
   shim).
4. **reference-drift / attribution / dangling id citations** — 7 instances, rounds 52, 53, 55,
   56, 57: r52 spotcheck D4 (entries cite S367/S372/S373/S390/S409 that resolve only in
   kotodama; kake resolves 0); r53 mistake row 1 (staged, unadmitted source ids presented as
   lane-held ground; census exit 0 does not inspect prose ids); r53 spotcheck D2 (w1/ evidence
   pointers do not resolve); r55 mistake `attribution` (ScribeQuality drafted another lane's
   round); r56 mistake `attribution` (misroot sweep); r57 mistake `attribution` (S388 reject
   reason deleted a sentence that is on the page) + `reference-drift` (S422 entry cited staging
   id S408 — not a lane id; resolver caught it at build).
5. **quote/scope/locator fidelity** — 8 instances, rounds 50, 51, 53, 54, 55, 57: r50 mistake
   (quote class blurred: collapsed-only vs raw substring); r51 mistake + attempt-2 correction
   (staged quote mis-transcribed; real class = quote-class mislabelling, 10/13 labels wrong);
   r53 mistake row 2 + spotcheck D5 (locators copied from package description; S329/S312 section
   cells wrong); r54 mistake rows 1 and 3 (material crawl qualifier dropped in translation; CJK
   "word" counts conflated with unit counts); r55 mistake `scope` (every staged quote over the
   25-unit ceiling); r57 mistake `scope` (search-log note broke the append-only mirror).
6. **stale-premise** (a frozen premise contradicts evidence) — 2 instances, rounds 56, 57: r56
   mistake row (r52 quote-truth selftest rebuilds from `HEAD`, passes only under a pin the
   registry row never named); r57 mistake row (frozen C1 pin rule demanded the measured revision
   be a strict ancestor of the receipt commit, so an honest C1 receipt could only print
   `met=False`).

Other one-off classes (not clustered): r50 D2/D3 (route-failure detail and overrun figure
prose-only), r52 mistakes 2–5 (counter self-defense: dropped guard, weak mutation ladder, mirror
base snapshot, coverage floor), r53 mistake row 4 (r52 work omitted from LOG), r54 mistake rows
4–5 (unbound correction marker; settlement counter conflated status with loss).

## FIXED THIS ROUND

- **Cluster 1(b) — receipt provenance → C1** (`c58_receipt_rewrites.py`). The r57
  `landing`/D1 recurrence (placeholder receipt filled in after its run; revision relabels) is the
  exact "mined mistake" the contract names; `c57_receipt_pins.py` did not catch it (revision
  lines only). C1 watches every receipt ever committed under `control(s)/` in the tip's ancestry
  and requires the ledger `.ufo/waves/round-58/receipt-rewrites.json` to disclose each event with
  path/commit/kind/to-from blob ids/pointer-bearing note, and `new_rewritten == 0` +
  `new_receipts == 2` for this round. **Shown able to fail: I ran it at base
  `044048597d62f3199494b63b36e90dd57825e350` in a shared scratch clone — `events=19
  undisclosed=19`, EXIT=1, byte-identical to the committed base receipt; the 19 include the 13
  never-disclosed events (r52×6, r54×4, r55×3, r56×3, r57×1) the class left behind.**
- **Cluster 4 — dangling id citations → C2** (`scripts/id_resolver.py` + `c58_resolver_cases.py`).
  This is the r52 spotcheck D4 / r53 mistake-1 recurrence (five ids dangled at r52 until the r53
  verifier found them; r57's resolver caught S408 at build). C2 hardens the resolver against its
  two disclosed false-green defects (fence-blind registry D1; git-quoted knowledge paths dropped
  with `--revision` F1). **Shown able to fail: base run `7/12 met=False`, EXIT=1, byte-identical
  to the committed base receipt — K1–K5 each fail as false-greens (exit 0, `dangling=0` where an
  id is dangling), P1–P7 pass.** The fix makes dangles fail loudly (exit 1) instead of reporting
  clean.
- **Cluster 5 — quote truth → C3** (`c58_quote_truth.py`) on the two new Baidu rows S423/S424:
  raw substring of one text node of the retained body's article block, ≤25 units and ≤40 chars,
  ASCII double quotes, frozen body sha256, used-by, mirror. This is the counter-side successor of
  the r50 quote-class, r51 transcription, r53 locator, r55 scope-ceiling and r57 junk-quote
  recurrence. **Shown able to fail: base run `0/8 met=False`, EXIT=1, byte-identical to the
  committed base receipt (entries, rows, bodies, receipts, mirror all absent at base).**
- **Cluster 6 — stale-premise (C1 pin self-contradiction) → receipt rule.** Contract lines 11–13
  replace the self-defeating pin rule: a receipt is committed once after the run it records and
  never rewritten; no placeholder is committed. This dissolves the r57 stale-premise row's
  contradiction directly.
- **Cluster 1(a) — wave shape (operational, not counter-backed).** Round 58 runs the declared
  shape — one v2 wave w1 with build + attack items together, ≥25% attack roles — answering the
  r54 spotcheck D1 / r55 `landing` shape-conformance recurrence. Settlement per seat is still a
  process obligation, not a counter.

## STILL OPEN

- **number-drift** — no round-58 counter measures documented-command tallies (C1/C2/C3 are
  receipt/resolver/quote counters). The r55/r56/r57 recurrence is untouched.
- **vacuous / false-green** — no counter proves its own non-vacuity; defense is attack seats
  (this round's v2 wave includes ≥25% attack roles) and selftests. C3's selftest is a version-1
  stub, ported during wave 1 (contract line 72), so C3's vacuity floor is not yet evidenced at
  the freeze.
- **CJK unit-vs-word semantics** — C3 enforces the unit rule on the two new rows, but the
  semantic "word"-segmentation verdict for the existing S367/S372/S373 gate quotes (31/27/27
  units, carried open since the r53/r54/r55 spot-checks) is unresolved.
- **attribution** (seats producing other lanes' output) — settlement checks catch it after the
  fact; no counter prevents it (recurred r55, r56, r57).
- **Prose-only evidence** (r50 D2 route-failure HTTP codes; r50 D3 overrun figure) — the classes
  are not in any round-58 counter surface.
- **Refusal-reason fidelity** (r56 spotcheck D2, r57 attribution) — QUALITY criterion only, not
  counter-enforced.

Evidence note: all counter runs above were executed read-only (git show / rev-parse) against a
`--shared` clone of the lane in my scratch; no tools installed (system python3; no new tool
needed — nothing to record under the tooling rule). No mutation of the lane, its jj state, or
its index.

VERDICT: Six clusters mined across rounds 50–57; round 58 fixes the receipt-provenance (C1),
dangling-id (C2) and quote-truth (C3) recurrences with counters shown red at base, plus the wave
shape and C1 pin-rule process items; number-drift, vacuity floor (C3 selftest pending), CJK
word-semantics, attribution and prose-only-evidence stay open.
