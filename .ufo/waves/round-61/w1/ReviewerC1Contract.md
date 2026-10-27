# ReviewerC1Contract

Scope: contract.md + contract.json (at `142dda5`, post-Amendment-A1) § Claim C1 line-by-line vs corpus/QUALITY.md
bar and the CORPUS.md ruleset it cites; receipt-grammar fidelity checked against the actual r52/r55/r56/r57 defect
receipts via lane git history. Evidence scripts + outputs: `ReviewerC1Contract.files/`.

FINDINGS:

- HIGH — `extra_member` rule vs R2 real-lane expectation conflict. Surface prose: "every receipt file … under
  `.ufo/waves/round-<N>/control/` or `.ufo/waves/round-<N>/controls/` (either spelling; files only in those
  directories, any depth of round number, `.txt` or `.json` extension)"; population rule: "a new file matching the
  path rule outside the frozen list → `extra_member`". Read literally, the contract-mandated round-61 files
  `.ufo/waves/round-61/controls/{population-144.txt,census-before.txt}` — and every round-61 receipt the frozen
  receipt rule commits under `round-61/controls/` — match the path rule and are not in the frozen list, so the
  counter must flag them `extra_member` and R2 ("met") can never pass on the honest build. Verified at `142dda5`:
  `git ls-tree -r` shows exactly 2 extra matches under both the direct-child prose reading (129 matches) and the
  loose any-depth reading implied by the population (146 matches); both extras are round-61 controls files
  (`scope-out.txt`). The population itself already contradicts "files only in those directories" — 18 entries sit
  under `retained/controls/` or `assimilation/validate/.ufo/waves/…` mirror paths, so the operative rule must be a
  components-match, which widens the hazard. Fix (pre-freeze amendment): bound the member-check to the population
  rounds (N ≤ 60) or name the exclusion of the measurement round's own controls dir.
- HIGH — Result-span rewrite detection is blind to ~76% of receipt lines, and the claim overstates coverage.
  Span = lines matching a 10-key regex; measured over the 95 grammar-detected receipts: 575 span lines vs 1836
  non-span lines (`span-coverage-out.txt`), with 20 receipts having ≤2 span lines (census/selftest/sweep receipts
  whose whole result table is invisible). Three real receipt-rewrite events in the lane's own r58 ledger
  (`.ufo/waves/round-58/receipt-rewrites.json`, 18 events over population files) are undetectable under the frozen
  rules: `a0a4fd48` on `round-54/controls/base-c1-s374.txt` and `base-c2-ops-debt.txt` (content rewrites incl.
  `uncovered=4→7`, `cited=`/`uncovered_names=` lists, and a verdict-sentence edit) and `a4a890cf` on
  `round-52/control/c2-quote-selftest.txt` (a relabel of `(fixture revision 3a50ae43…→1ae8de5d…)` — a
  space-separated "revision" that escapes `revision\s*[:=]`). A1 says events=12, matching my independent census,
  but the claim title says "undisclosed receipt rewrites become detectable" — 3 of 15 receipt rewrites in the
  ledger remain undetectable. Fix: widen the span (all lines minus a noise list), add an unanchored
  `revision\s+\S` form, or name these residual classes under "What the counter does not test" and scope the claim.
- MEDIUM — `scores_held == 3` term: no case exercises it, and its read scope is unspecified. The contract says the
  term is "shown able to fail by a score-only mutant, per R59-D2", but none of the 18 cases is a score-mutant, and
  none of the named selftest controls is one either — "shown able to fail" has no named failing witness. The term
  parses SCORECARD.md but the contract never says which cells: a whole-file or row-count reading breaks under C2's
  legitimate capability-row append this round (contract C2: "Capability row enters SCORECARD.md"), and a
  wrong-cell read (e.g. the round-table `| freshness |` rows at 89–94) breaks on any honest edit. Fix: name a
  score-mutant control case and pin the parsed cells (axis-table operability=10, freshness=10, calibration=2).
- MEDIUM — Do-nothing-control reachability partially meets the bar; pre-build receipts not mandated. Base → 0/18
  and the four named selftest controls cannot reach 18 under the frozen expectations, so the bare do-nothing is
  out of reach (round-35 criterion satisfied at the surface). But QUALITY.md r35 requires the controls "scored
  with the frozen counter and committed before the build" with receipts; the contract only names them "(before
  data)" with no committed-receipt requirement, no counter-sha256 naming, and no retained prior-round hollow
  control. Residual (recorded limit, per r34/r35): the expected-value column is published, so a tool that
  classifies fixture histories (rather than implementing lineage) can replay the published table; seeded ids stop
  id-keying, not semantics-keying — named control is a fixture-sniffer, not a contract-table replayer. Fix: require
  committed control receipts at freeze and add a semantics-keyed lookup control to the selftest list.
- LOW — Uncased rule surface: `rename-ends-history` semantics, `member_missing` (only `member_changed`/`extra_member`
  are cased), counter exit-64, and L15's "not an ancestor tip"→exit-2 mapping (the tool spec's exit-2 names
  "revision unresolved", not "resolvable non-ancestor") are all specified-but-never-exercised; not named in
  "What the counter does not test". Fix: add cases or move them to the not-tested clause.
- LOW — Receipt deletion is unmodeled: an event candidate requires "a different blob"; a commit deleting the file
  has no blob at all (span-set empty vs parent — implementor's choice: skip, event, or crash). r58's event set had
  `status M/D/re-add`; r61's spec is silent on D. Fix: state the behavior.
- LOW — `--disclosures` default read is ambiguous: "committed bytes only" governs population files but the
  disclosures default path `.ufo/receipt-disclosures.json` could be worktree-read (uncommitted files currently
  pass) or committed-read (fixtures then can't supply it by --flag without committing). Fix: specify.
- LOW — Disclosure matching on (path,commit) only (A1, deliberate) relaxes r58's falsifier (kind, from/to blobs,
  resolved pointer must all match): a wrong-kind or wrong-value disclosure can now satisfy. Prose truthfulness is
  reviewer-checked per the not-tested clause, so this is a recorded relaxation; note it as such in the
  not-tested clause rather than only inside A1.
- LOW — Amendment-surface nits: contract.md line 15 names "§ Counter versions", a section that does not exist
  (the operative surface is § Amendments + contract.json `amendments[]`); the frozen R2 row still reads
  `receipts=144 events=<k>` while § Amendments reads `receipts=95 events=12` — superseding by convention works,
  but an inline `(amended by A1)` on the R2 row would have prevented a table-only implementor from hardcoding the
  stale expectation. Amendment mechanism itself was exercised and landed pre-freeze at `142dda5` — surface works.
- NIT — "FIRST committed version (base..revision first-parent history)" is imprecise for all 144 population files
  (every file predates base); empirically the intended semantics is first-ever committed version (all commits ≤
  measured revision, unbounded below — same range as the history walk). No case where the readings diverge exists
  today; inert but worth one disambiguating word.

CHECKS PASSED (no finding): predicate is a single sentence (`met: cases_passed == 18 of 18 AND scores_held == 3`);
kill rule covers exits 0/1/2/64 with unevaluable named; do-nothing base → 0/18 unreachable vs the frozen 18; the
three grammar forms catch every r52/r55/r56/r57 defect receipt's first version (`EXIT=` in all six; verified in
git history: r52 `c1-ledger-real.txt`/`c2-quote-real.txt` @`1ae8de5`, r55 pair @`64c0ce12`, r56 pair @`4cb225f`,
r57 `after-c1-receipt-pins.txt` @`31b61a4`); r56 relabels are span-diff `rewrite` events ✓; r57 pending fill is
`pending_filled` only under A1's whole-first-version fix (frozen md text, span-bounded, would misclassify it —
finding recorded in the historical note, resolved by amendment); my independent re-implementation of the frozen
rules reproduces A1's data claims exactly — 95 receipts, 12 events (`events-out.txt`); `.ufo/receipt-disclosures.json`
(untracked worktree, to be committed this wave) covers exactly those 12 (path,commit) pairs, schema keys uniform,
no phantom entries; population-144 equals the loose-rule enumeration at `9f07731a` exactly (144/144, `scope-out.txt`).

Residual risk: census numbers are from my own re-implementation of the contract rules, not from the tool — if the
landed `receipt_lineage.py` diverges (e.g. span-set vs diff semantics), A1's `events=12` could shift; wave-2 must
verify the tool's printed numbers match this census. The kind-blind disclosure match means wave-2 prose review is
the only guard on wrong-kind disclosures.

VERDICT: HOLD — C1's predicate/kill-rule skeleton is sound and A1 already repaired the biggest contradictions I
found independently (receipts=95, whole-version pending); but `extra_member` must be scoped off the measurement
round before freeze or R2 is unreachable on the honest build, and the span's 24% line coverage must be named or
widened or the claim title overstates what is detectable.
