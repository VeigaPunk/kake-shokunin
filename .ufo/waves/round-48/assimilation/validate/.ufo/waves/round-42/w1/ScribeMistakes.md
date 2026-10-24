# ScribeMistakes — round 42

Axis: operability. This is a report-only draft for `corpus/lessons/round-42.md`; that target was absent when read, so it was not edited.

## Draft `## Mistakes` entries

1. **Class: C03 — scope overreach (the harm rule treated guards as changes).** Evidence: `corpus/lessons/round-41-verifier-spotcheck.md:64-72` records 13 of 42 new fixtures green on base while the frozen rule required every new fixture red; `:159-161` routes a split between change fixtures and parity/regression guards and an explicit cost. Captured-by: **none** in round 41; the non-author spot-check surfaced the rule's construction problem. Fix: a pre-data QUALITY criterion classifies fixtures as changes (red on base) or guards (green on base), checks guards against the build, and includes a numeric runtime bound; round 42's corrected H1/H3 is at `SCORECARD.md:2976-2987`. Shown able to fail: the class-aware guard condition has a real red-before witness: six IP-literal TAB/LF/CR guards failed on first build `0b485431…` and passed after repair (`corpus/lessons/round-41-verifier-spotcheck.md:122-126`).

2. **Class: C04 — vacuous or inert verification (draft-1 timing measured the wrong work and weakened the adversarial shape).** Evidence: `SCORECARD.md:2955-2958`; draft code reads `RUSAGE_CHILDREN` around bwrap at `.ufo/waves/round-42/draft1/c42_count_draft1.py:420-435`, while the do-nothing receipt is `met: true`, equal 8/8, with 1–2 ms samples and ratios 0.82–1.33 (`.ufo/waves/round-42/draft1/donothing-tip-42001-draft1.json:3,10-15,48-60,152-157`). Captured-by: the L1's pre-data do-nothing probe caught it; this is not independent-seat evidence for draft 1. QUALITY (o) is the formal pre-freeze control requirement, not an observed non-author run of this draft. Fix: charge sandbox descendants with the child-subreaper runner and use slash-free late-defect T1/T5 values (`.ufo/waves/round-42/c42_count.py:249-272,362-384,412-425`). Shown able to fail: with the corrected counter, the unchanged round-41 tool is not met despite equal 8/8; T1/T2/T5 ratios are 5.367/2.811/8.87 (`.ufo/waves/round-42/verification/pre/donothing-tip-42001.json:3,10-14,157-163`).

3. **Class: C08 — correction error (S117–S119 were edited in place).** Evidence: `corpus/lessons/round-41-verifier-spotcheck.md:131-133` names commits `9e3c31d2`, `2653b629`, `0c5ad2f6` and the forbidden `anchor`/`teaches` edits; the governing rule is `/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`. Captured-by: CORPUS SOURCES rule 2 existed but was not gated; the verifier spot-check reported the violation. Fix: restore the committed row text and put corrections in new superseding rows (`teaches` begins `supersedes S0NN —`), logging permitted in-place changes old→new. Shown able to fail: the recorded red-before is the historical pair of diffs with prohibited fields changed. No dedicated append-only check or exit status is evidenced here; require such a check to fail on those deltas and pass after the superseding-row repair before calling the fix proved.

## Gates, surfaces, limits

- Evidence reviewed: source text and retained receipts cited above. No counter, build, test, or shell command was run by this seat; no execution result is claimed.
- Touched surface: this report only. No product or judge files changed; no tool installed.
- Out of scope: inserting the entries into the absent round-42 lesson; implementing criteria/checkers or repairing SOURCES rows.
- Artifact: `.ufo/waves/round-42/w1/ScribeMistakes.md`.
