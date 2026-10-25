# ReviewerC1Order — C1 correction-ordering attack

Seat: L1Kake54.ReviewerC1Order. Read-only review; no edits.
Target: `.ufo/waves/round-54/c54_s374_calib.py` as committed at `8e408e00fbe1c5908df62ba79e78c944bda479e2`
(`round-54: repair S374 calibration and settle r53 ops debt`, landed 10:44:56 -0300 while this
review ran; contract/controls frozen at `acae1dc`, base control rev `68228b2d`).

## Method

- Ran the read-only counter at HEAD (`8e408e0`): `mismatches=0 met=True`, `EXIT=0`
  (`C1.2 suspect_cells=1`, `C1.3 block_offset=2876`).
- Re-ran the do-nothing control at base `68228b2d`: `mismatches=1 met=False`, `EXIT=1` — matches
  `controls/base-c1-s374.txt`.
- `--selftest`: all 7 fixtures pass, incl. `correction_wrong_polarity` and
  `correction_before_render` rejected. `run_checks_fix` shares the production
  `qualifier_findings` parser (no divergent duplicate).
- Drove the committed `run_checks`/`qualifier_findings` code directly (import of
  `git show HEAD:` bytes, `show()` bound to in-memory fixtures) — 13 synthetic entries below.

## Answer to the assignment

**Q1 — correction appended after suspect render: does the predicate still pass incorrectly?**

Not for the ordering itself. The committed comparison is

    mismatch = sum(1 for pos in suspects if corr_at == -1 or corr_at < pos)

where `pos` is `match.start()` of the `(rendered: …)` cell and `corr_at` is the byte offset of the
first *valid* `[r54-correction 2026-10-25]` mark. A suspect cell is superseded iff a valid mark
exists at a *later* offset — exactly the contract's "appended, never rewritten" (correction_before
and suspect_after_correction fixtures both verified `exit=1`). But "after" is judged against the
suspect cell's *start*, not its end — see F1.

**Q2 — must the correction window carry the source quote and an English crawl token?**

Yes, but stricter than "any crawl token", and only in a forward window: a mark is valid iff the
1200 characters *after* it contain both the exact substring
`このリンク先のウェブページの巡回を推奨していない` and a match of
`NEGATIVE_CRAWL_RE = \bnot\s+recommend(?:\s+the)?\s+(?:crawl|crawling)\b` (case-insensitive).
Verified: mark with no tokens (`exit=1`), mark with tokens only *before* it (`exit=1`), tokens
>1200 chars after the mark (`exit=1`). Tokens are trivially parrotable — presence is positional
only (no binding to the specific cell being corrected).

## Findings

**F1 (HIGH) — "appended after" measured against the cell's start, not its end.** A mark placed
*inside* the suspect `(rendered: …)` cell (cell-start < corr_at < cell-end) is counted as
superseding it. Repro: `(rendered: the owner does not recommend or vouch for it [r54-correction
2026-10-25])` + later line carrying `QUOTE` + "not recommend the crawl" → `suspects=[4]`,
`corr_at=60`, `exit=0`. No separate correction block, no repair; the gloss still asserts
endorsement-only. The code must compare `corr_at` against `match.end()` (or require the mark to be
line-start-anchored, as the docstring already promises).

**F2 (MEDIUM) — lexical suspect test forgives negated crawl vocabulary.** A cell is non-suspect
iff `CRAWL_RE = crawl|巡回` appears *anywhere* in it, polarity unchecked:
`(rendered: the owner does not recommend and refuses the crawl of it)` → `suspects=[]`,
`exit=0` with any valid correction. A gloss that affirmatively asserts a crawl *refusal* — the
over-read the row exists to stop — is classified "has the crawl qualifier". Predicate met with a
materially false rendering still in force.

**F3 (MEDIUM) — `[^)]+` truncation hides endorsement vocabulary behind any `)`.**
`(rendered: (cf. S374) the owner does not recommend the target page)` → `suspects=[]`, `exit=0`.
Everything after the first literal `)` is invisible to `SEMANTIC_RE`, so an arbitrary amount of
un-repaired endorsement-only prose rides free.

**F4 (MEDIUM) — "preserved as historical text" is unenforced.** `met` requires only
`corr_at >= 0 and mismatch == 0`; zero suspect cells satisfies it. Deleting the suspect gloss
entirely (or writing a gloss with no endorsement vocabulary at all, e.g. "the owner dislikes the
page") plus a boilerplate correction → `exit=0` both cases. The contract's append-only property —
and `suspect_cells=1` at base — is not asserted as a precondition.

**F5 (LOW) — NEGATIVE_CRAWL_RE false-negatives honest repairs.** "does not vouch for the crawl",
"does not recommend a crawl" (article `a` breaks `(?:\s+the)?` since only `the` is allowed), or
any honest negative phrasing without `recommend` → `corr_at=-1`, `exit=1`, blocking a real fix.
Verified (`L_honest_phrase_variant`).

**F6 (LOW) — docstring drift.** C1.3/C1.4 still say the mark must *start a line* and needs "at
least one crawl token"; the code searches the mark anywhere and requires the negative phrase +
exact quote within a forward 1200-char window. The looser docstring is what enables F1 to surprise.

## Residual risk / gaps

- Exploits were exercised against the committed code via in-memory `run_checks`, not against a
  crafted commit (wave is read-only; no scratch commits permitted). All reported `exit` values are
  observed, not inferred.
- A mid-review HEAD advance (`acae1dc` → `8e408e0`) was observed; the earlier pre-`8e408e0`
  worktree code additionally required only `\bcrawl\b` and used an *inverted* order comparison
  (a correction *preceding* a suspect suppressed the mismatch); that flaw is dead code at HEAD but
  is worth noting if older receipts are ever re-scored.
- Not in scope: whether the correction's asserted semantics are true (no content binding), and the
  CJK quote-length maintenance item.
- No tool installs; pacman untouched.
