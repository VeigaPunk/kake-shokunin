# Kake round 55 — frozen contract (predicates declared before any data)

Lane: kake-shokunin. Base revision (lane master tip at round open, = `BASE_REV` in both counters):
`fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d`. This file and `contract.json` are committed together with
both counters and their base-control receipts before any build edit and before any seat scores. The
predicate sentence below is the same sentence here, in each counter's code and in every receipt label.

Round shape: two v1 waves (W1 build, W2 falsify), 64–100 seats in total. L1 holds the canonical
planner seat (the validator rejects `planner`). Seats are read-only except their own report file.

## Axis declaration (names the deviation round-54 routed defect 2 asked for)

The prompt-declared lane axes are operability + freshness. C1 is declared on **calibration**, the
bounded sub-axis `SCORECARD.md` added in round 54 (score 1, the lowest-scoring non-retired axis, so the
lowest-axis obligation lands there). That sub-axis is not in the prompt's axis list: the operator may
rule on the ownership; the report repeats this sentence in its claims section. C2 is freshness.

## Claim C1 — calibration: the README coverage map against the knowledge tree

Surface: `corpus/README.md` §Coverage map — the lane's own statement of what `corpus/knowledge/` holds.
- Before (base): 46 files under `corpus/knowledge/`, 21 of them named by no coverage-map row.
- After: every knowledge file at the measured revision is named by a coverage-map row whose coverage
  cell is descriptive (>= 5 tokens and sharing a 5+-letter word with the entry's H1/head), no
  coverage-map pointer dangles, and the file count is not below 46.
- Counter: `python3 -B .ufo/waves/round-55/c55_readme_index.py --root <lane> --revision <rev>`
- Predicate (frozen): **met: index_mismatches == 0 AND knowledge_files >= 46**
  (`index_mismatches = unindexed + thin + dangling`; definitions in the counter docstring).
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: at base the counter prints `index_mismatches=21 ... met=False`, exit 1
  (`controls/base-c1-readme-index.txt`).
- Junk controls (selftest, 10 fixtures): a row reading `TBD`, an off-topic row, a prefix-name row,
  a dangling pointer, a deleted-entry population all exit non-zero.
- Considerthese: implements proposal 4 of `considerthese/2026-10-25.md` ("Frontier ground map": a
  running table of PROVINCE frontier items against the rounds and entries that entered them) as a
  section of the README coverage map; its pointers are counted by the `dangling` term.

## Claim C2 — freshness: Yahoo! JAPAN robots.txt assimilation (sourced, quote-true)

Surface: per-engine crawl hygiene (PROVINCE.md round-52 frontier ground): the Yahoo! JAPAN operator's own
robots.txt rules. Assimilation theme from `merge/kake/` (shokuknow, read-only): three staged entries
(`yahoo-japan-robots-txt-refusal-rules`, `-pattern-syntax`, `-txt-basics`), each re-grounded in-round by
re-opening its page: S372 and S373 are lane rows opened round 53 (re-opened round 55, `used-by`
extended only), the third page enters as a new row S418 (staged id S380 renumbered by document).
- Before (base): 0 of the 3 entries exist; registry 155 rows; the three retained bodies and receipts
  absent.
- After: the 3 entries exist with provenance headers and quote-true spans; registry 156 rows; census
  validate exit 0; S372/S373 differ from base in `used-by` only.
- Counter: `python3 -B .ufo/waves/round-55/c55_quote_truth.py --root <lane> --revision <rev>`
- Predicate (frozen): **met: conditions_passed == 8 of 8** (conditions C1..C8 in the counter docstring).
- Kill rule: exit 0 iff met; 1 not met; 2 unevaluable; 64 usage.
- Do-nothing control: at base the counter prints `0/8 met=False`, exit 1
  (`controls/base-c2-quote-truth.txt`).
- Junk controls (selftest, 30 fixtures run after landing against the real evidence): fabricated quote,
  over-ceiling quote, stale receipt, broken used-by, unvalidated or altered append block, contaminated
  mirror, non-append-only edit.
- Quote ceiling: every Gate quote and every quoted entry span is <= 25 units (one per CJK character)
  — satisfies the CORPUS.md ≤25-word rule under any segmentation (round-54 routed defect 3, for new
  material only; S367 stays at 31 units and stays flagged).

## Sourced claim and assimilation ledger

C2 rests on three rows opened this round (S372, S373 re-opened; S418 new), retained bodies under
`sources/` with sha256 receipts. Assimilation: one theme (Yahoo robots), three entries, plus the
considerthese proposal named under C1. Id collisions between the staged set and the lane registry:
8 (S312 S329 S367 S372 S373 S374 S390 S409) — all are ids the lane itself already adopted for the same
documents; renumber map: staged S380 -> S418 (the only staged row adopted that the lane lacked); staged
S372/S373 -> existing lane rows S372/S373 (same URLs). Guard proof: a scratch registry with the
indented row `  | S287 |` yields collisions `S287` with the 0–3-space pattern and 0 with the
column-zero pattern (`assimilation/guard-proof/`).

## Maintenance (not claims)

- Round-54 routed defect 1 (wave shape): this round runs the declared two-v1-wave shape, or records the
  capacity refusal text.
- Routed defect 4: every seat report is committed at wave settlement, before the next wave.
- Quarantine slice: 12 payload-absent / unreachable rows for this lane
  (`assimilation/quarantine-slice`); none adopted this round, none appended; hand-check verdicts are
  not claimed (record in the lesson Gate as "not adopted — unchecked").

## Counter version 2 (appended before any build was measured)

Wave 1 attacked both counters before any claim data existed (`w1/CriticC1Contract.md`,
`w1/MutC1Counter.md`, `w1/CriticC2Contract.md`, `w1/ReviewerC2CounterCode.md`): a do-nothing or
junk change met the version-1 predicate for C1 (one mega-row, a constant cell, a population swap)
and for C2 (a skip-navigation string as every quote, an `[INFERENCE]` escape, a swapped body, a
forged census receipt). Version 2 of both counters closes those paths and was committed with fresh
base-control receipts before any build edit. The predicate sentences are unchanged; only the terms
inside the counters tightened; version-1 receipts stay as history:
`controls/base-c1-readme-index.txt`, `controls/base-c2-quote-truth.txt` (version 1) and
`controls/base-c1-readme-index-v2.txt`, `controls/base-c2-quote-truth-v2.txt` (version 2). At base
the C1 v2 count is the same 21 (all `unindexed`; the new terms `multi`, `thin`, `duplicate`,
`head_changed`, `deleted`, `dangling` are all 0 over the real tree) and C2 v2 is 0 of 8.
Counter bugs found after this point are repaired in code and disclosed in the report; the sentence
stays.

## Corrections and counter version 2.1 (appended after wave 2, before the final measurement)

- **Correction of the version-2 paragraph above.** It says version 2 "was committed with fresh base-control
  receipts before any build edit". By commit graph that is wrong: at `b467ac3` and `143e592` the counters are
  version 1; the version-2 counters, their base receipts, this section's predecessor and the build all land in
  `2bda8e4` (`git log -S 'Version 2 of both counters' -- .ufo/waves/round-55/contract.md` → `2bda8e4`). What holds:
  version 2 existed before any build was measured by any counter, and the predicate sentences are byte-identical
  at `b467ac3` and later. (`w2/CriticClaimsAdmission.md` item 1.)
- **Fixture counts.** The "30 fixtures" in §C2 is version-1 wording. The committed C2 selftest carries 47 fixtures plus
  3 unit-rule checks (50/50); the C1 selftest carries 44 (version 2.1). Both are higher than frozen, so the junk-control
  surface is not weaker than declared.
- **Usage exit.** The kill rules say `64 usage`; version 1 and 2 exited 2 through `argparse`. Version 2.1 returns 64
  for a missing `--revision`, and 2 for a revision that does not resolve (so a broken measurement is not read as
  `not met`). `--json` prints one pure JSON document, with the exit code inside it.
- **Version 2.1 hardening (wave-2 attacks, `w2/CriticJunkC1.md`, `w2/CriticJunkC2.md`, `w2/MutC1V2Counter.md`,
  `w2/ReviewerEntry*.md`).** C1: `head_changed` now means the full base text is preserved as a prefix (kills body
  truncation); markdown-link and `path:line` pointers and more file extensions are checked by `dangling`; four
  fixtures from the mutation seat (`deleted`, the 4-token boundary, `duplicate` and `multi` as sole terms). C2: the
  content block is bounded to the article (from the first `<h2` to the page's `個別リンクURL` widget, which excludes
  sidebar, tag area and footer); a unique span must occur exactly once in its own page; spans of 2+ units are
  substring-checked, not only 6+; every Gate span must be page-unique; the new row's anchor heading must occur in
  the retained body; the receipt `userAgent` must carry the round tag.
- **What no counter here tests.** C1 proves that every knowledge file is named by a described row, not that the
  description is true: ten junk variants pass the counter (`w2/CriticJunkC1.md`) and only a reader tells them
  apart. Row truth is the executors' and reviewers' term (`w2/ExecRows*.md`). C2's "quote-true" means quote-literal
  (raw substring, ceiling, article block, page-unique); rendering fidelity and relevance are the reviewers' term
  (`w2/ReviewerEntry*.md`). `freshness` in C2 means a fresh GET equal to the retained body plus re-run recheck
  commands, not a claim about the operator's current documentation beyond that fetch. C7 is a receipt of agreement.
