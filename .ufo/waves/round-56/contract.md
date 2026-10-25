# Kake round 56 — frozen contract (predicates declared before any data)

Lane: kake-shokunin. Base revision (lane master tip at round open, = `BASE_REV` in both counters):
`e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`. This file, `contract.json`, both counters, their base-control receipts, the
retained source bodies with receipts and the pre-append registry mirror are committed together before any build edit and
before any seat scores. The predicate sentence below is the same sentence here, in each counter's code and in every receipt
label. Round date 2026-10-25. Round shape: two v1 waves (W1 build + pre-data attacks, W2 falsify), 64–100 seats in total;
the L1 holds the canonical planner seat (the validator rejects `planner`); seats are read-only except their own report
file (and a `<Seat>.files/` directory beside it for candidate code).

## Axis declaration (repeats the round-55 note for the operator)

The prompt-declared lane axes are operability + freshness. C1 is declared on **calibration**, the bounded sub-axis added in
round 54 (score 1, the lowest-scoring non-retired axis, so the lowest-axis obligation lands there); it is outside the
prompt's axis list and the operator may rule on that ownership. C2 is freshness. No exploratory claim.

## Claim C1 — calibration: SKILL.md registry self-test tallies against the observed tallies

Surface: the `SKILL.md` gate registry, whose rows state how many fixtures each gate's selftest holds — a self-assessment of
the lane's own tools. The observed state is what the same documented command prints in a clean clone of the revision.
- Population (enumerated, ten registry rows, first cell = name): base-path-audit, source-recheck-audit,
  robots-expectation-audit, sitemap-file-audit, redirect-expectation-audit, commit-citation-lint, wave-evidence-ledger,
  quote-truth-counter, readme-index-counter, yahoo-robots-quote-truth-counter. link-preview-audit is excluded: its row
  counts fixture *directories* (45) while its selftest prints a case total (46), so the two numbers answer different
  questions and a comparison would be a false positive. Rows whose self-test cell carries no tally claim are out of scope.
- Before (base): 7 of the 10 rows disagree with what their selftest prints (tallies claimed 101/137/150/8/18/35/47 against
  observed 106/204/235/9/18-fails-unpinned/44/54).
- After: every one of the ten rows states the tally its documented selftest command prints, the command runs as documented
  (including any `VAR=value` pin the row names), and exits 0 with A == B.
- Counter: `python3 -B .ufo/waves/round-56/c56_selftally.py --root <lane> --revision <rev>`
- Predicate (frozen): **met: tally_mismatches == 0 AND rows_checked == 10**
- Kill rule: exit 0 iff met; 1 not met; 2 evidence unevaluable (revision unresolved, tally unparsable, timeout); 64 usage.
- Do-nothing control: at base the counter prints `tally_mismatches=7 rows_checked=10 met=False`, exit 1
  (`controls/base-c1-selftally.txt`).
- Junk controls (selftest, 20 checks): stale count; count off by one; claim deleted; env pin removed; row deleted; command
  swapped to another script; selftest script replaced by a print; `2/3 passed`; claim placed in another cell; two claims
  summing wrong; population one short; unparsable tally.
- What the counter does not test: that a gate's selftest is *good* (a passing selftest says nothing about mutants), nor the
  other ~20 fixture-count mentions in SKILL.md prose outside the ten rows; nor helper files a selftest imports (only the
  named script's blob is pinned to its base blob).

## Claim C2 — freshness (sourced): three Yahoo! JAPAN crawl-handling entries, quote-true

Surface: per-engine crawl hygiene (PROVINCE.md round-52 frontier ground) — what the operator's own pages say a server's
answer does to the crawl. Assimilation theme from `merge/kake/` (shokuknow, read-only), three staged entries re-grounded
in-round: `yahoo-japan-link-target-crawl-restriction` (row S367, a held row re-opened; `used-by` extended only),
`yahoo-japan-deleted-url-recrawl` (page 002856, staged S375 -> new row S419) and `yahoo-japan-soft-404-recrawl` landing as
`yahoo-japan-nonexistent-url-recrawl` (page 002857, staged S376 -> new row S420).
- Before (base): 0 of the 3 entries exist; registry 156 rows; retained bodies and receipts absent from the lane's round-56
  evidence.
- After: the 3 entries exist with provenance headers and quote-true spans; registry 158 rows; S367 differs from its base row
  in `used-by` only; `sources-census.sh validate --root ... kake` exits 0.
- Counter: `python3 -B .ufo/waves/round-56/c56_quote_truth.py --root <lane> --revision <rev>` (conditions C1..C8 are the
  round-55 version-2.1 conditions unchanged; generated from it by `derive_c56_quote_truth.py`).
- Predicate (frozen): **met: conditions_passed == 8 of 8**
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: at base the counter prints `0/8 met=False`, exit 1 (`controls/base-c2-quote-truth.txt`).
- Quote ceiling: every Gate quote and every quoted entry span is <= 25 units (one per CJK character).
- Selftest: version 1 ships a stub (`--selftest` exits 2). The round-55 fixtures name round-55 rows; wave 1 supplies the
  round-56 fixtures and the L1 integrates them before measurement. Until then the junk-control surface of C2 is the
  round-55 selftest of the same conditions (54/54 at `e48354b7c26b`), not a round-56 one.
- Sourced claim: C2 rests on three rows opened or re-opened this round (S367 re-opened; S419 and S420 new), retained bodies
  under `sources/` with sha256 receipts (`sources/receipts.json`; S367 body equals the round-53 body, sha256 0188de9d…).

## Assimilation and considerthese ledger

- Theme: Yahoo! JAPAN crawl handling (deleted URL, non-existent URL, link-target restriction) from `merge/kake/`. Id lists
  `assimilation/reg-ids` (156), `assimilation/staged-ids` (129), `assimilation/collisions` (8: S312 S329 S367 S372 S373 S374
  S390 S409 — the same documents already held; only S367 is adopted here). Renumber map by document: staged S375 -> S419,
  staged S376 -> S420, staged S367 -> lane S367. Guard proof: `assimilation/guard-proof/` carried from round 55 (the guard
  is unchanged; wave 1 re-proves it).
- Quarantine slice (12 rows, `assimilation/quarantine-slice`): not adopted, not hand-checked this round.
- Considerthese: one proposal of `considerthese/2026-10-25.md` — proposal 1, the landed-vs-claimed check (a report's cited
  hashes against branch ancestry) — lands as `scripts/landed_check.py` with a selftest and is run on the round-55 report and
  on this round's report. Not a claim; proposals 2 and 3 are not taken (at most one per round).

## Maintenance (not claims)

- Round-55 routed defect 1 (stale SKILL.md registry tallies) is the substance of C1; defect 3 (dead scribe seats) is handled
  by seat settlement before each wave hand-off; defect 4 (S367 31 units) is addressed by re-cutting S367's quotes to <= 25 units
  in the new entry (the row's own cells are unchanged).
- Frontier step: census before/after, one mined mistake, sourced claim — in `corpus/lessons/round-56.md`.

## Counter versions (appended after wave 1, before the final measurement)

The contract commit `2d308e808bfd` froze both counters at version 1 and the predicate sentences, which are byte-identical in
`contract.md`, `contract.json` and both counters since. Wave 1 attacked both counters before any claim was measured
(`w1/CriticC1Contract.md`, `w1/MutC1Counter.md`, `w1/ReviewerSelftallyCode.md`, `w1/CriticC2Contract.md`, `w1/CriticControls.md`,
`w1/CritCheatC1.md`, `w1/CritCheatC2.md`). What changed, with the evidence:

- **C1 counter version 2** (`c56_selftally.py`): the documented command must be exactly `[KAKE_R5N_SELFTEST_REV=<hex>] python3 -B
  <script> <pinned args>` and sit in the row's `Self-test` column (a fake `python3 -c`, extra arguments, a command in another column are
  `command_invalid`/`command_missing`); the environment is fixed instead of inherited (a host-exported pin cannot rescue a row);
  duplicate row names are mismatches; every `*.py` beside the pinned script at the base revision must be byte-identical; exactly one
  claim per cell (two for the one declared sum row); the tally line is anchored; `rows_checked` counts rows whose command was found and
  valid (v1 counted rows looked up). Selftest 20 -> 47 checks (generated sandbox repos; includes the six mutants that survived v1). Base
  control re-run under version 2: `tally_mismatches=7 rows_checked=10`, exit 1 (`controls/base-c1-selftally-v2.txt`). Version-1 junk that
  met the frozen predicate (`w1/CritCheatC1.md` experiments 5-8, `w1/CriticC1Contract.md` A1-A9) is closed by version 2, except one
  disclosed limit: a helper outside the pinned script's directory is not pinned.
- **C2 counter version 2** (`c56_quote_truth.py`; version 1.1 had added the ported selftest): the held row S367's retained body is pinned by
  its sha256 instead of a title substring (v1 rejected a truthful build at 7 of 8: the held row's title uses fullwidth punctuation the page
  does not print; `w1/CriticC2Contract.md` WR-1, `w1/CritCheatC2.md`); Gate quotes must occur once in their own body; a 40-character
  ceiling beside the 25-unit ceiling (punctuation and markup entities cost 0 or 1 unit); one-token quoted spans of 12+ characters are
  substring-checked; `verified-at` must carry the round date; `recheck` must open with NNd, an ISO date or on-release; kind, tier, scope and
  teaches cells are checked; the staged candidate name must be absent; page-uniqueness is judged against every retained body. Selftest 54
  (round 55) -> 67 checks (64 fixtures + 3 unit checks), run with `KAKE_R56_SELFTEST_REV=<measured content revision>`.
- A first C2 measurement was taken at `d5afc48acd72` (8/8) before the Gate-uniqueness change and the C1 version-2 column rule; it is
  recorded here, not cited as the final measurement. The final measurements are at the revision named in the report.
- **After-state correction.** The C2 after-state's clause "`sources-census.sh validate --root ... kake` exits 0" is satisfied at base
  (`controls/census-before.txt`), so a do-nothing control meets it: it is a no-harm check, not part of the predicate. C2's predicate
  measures three facts: the 3 entries (C1-C6), 158 registry rows with S367 changed in `used-by` only (C3/C8), and the validated append
  (C7).
- **What the C2 counter does not test.** Quote truth is substring truth, not support: three arbitrary page-unique spans satisfy C5
  (`w1/CritCheatC2.md` builds a one-commit junk tree that reaches 8 of 8 under version 1; rendering fidelity, relevance and whether the
  entry says anything are reviewers' terms); C6 is receipt-shaped, not a fetch proof; C7 is a receipt of agreement, not proof the census
  ran (re-run by wave-2 executors); a quote that contains a raw `"` (the S367 meta-tag examples) is split by the quote regex and cannot
  be verified whole, so the entries do not quote those lines.
- **Axis note.** `w1/CriticAxisClaim.md` argues C1 is operability (the surface is the gate registry's runnable-command claims) and C2 is
  coverage/expansion (the counter has no drift condition). The frozen declarations stand; the report states both views and the
  lowest-axis obligation is reported as open pending the operator's ownership ruling. SCORECARD calibration stays at 1.
