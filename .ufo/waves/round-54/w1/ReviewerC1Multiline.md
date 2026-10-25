# ReviewerC1Multiline — C1 counter on multiline `(rendered: …)` cells

Seat: `L1Kake54.ReviewerC1Multiline` (leaf; no subagents, no installs, no writes beyond
this report). Counter under review: `.ufo/waves/round-54/c54_s374_calib.py`.

## Evidence timeline (matters: the counter was not frozen)

The counter changed under review. Distinct states observed on 2026-10-25:

| State | Where | Semantics |
|---|---|---|
| **Frozen v1** | committed `acae1dc` ("round-54: freeze claims and calibration controls") | `EN_CRAWL_RE` gate; mismatch = `pos < corr_at`; selftest twin `run_checks_fix` scanned **per line** and required mark+quote+`\bcrawl\b` on one line |
| **v2** | worktree ~10:36, committed as `8e408e0` | shared `qualifier_findings`; `NEGATIVE_CRAWL_RE`; mismatch = `corr_at < pos` |
| **v3/v4** | worktree ~10:50–10:53 | added `CORRECTION_MARK_RE` (anchored bold), `BOUND_CORRECTION_RE`, `BASE_RENDER`; transient `SyntaxError`/`IndentationError`/`ValueError` mid-edit; selftest `corrected` FAILed |
| **v5 (current worktree)** | 10:54:50, uncommitted on top of `8e408e0` | v4 semantics + fixed fixtures; all checks green |

This means the "frozen" predicate in `contract.md` was declared before data, but the
**counter implementation was repaired after freeze and after control receipts were
taken**. Receipts in `controls/` are keyed by argv, not by script hash, so
`base-c1-s374.txt` and `c1-selftest.txt` silently describe different code than
what produced `ExecC1Selftest.md`'s recorded 5-fixture output.

## Q1 — does it observe the original multi-line gloss?

**Production path: yes, in every version observed.** `RENDER_RE = \(rendered: ([^)]+)\)`
— `[^)]+` crosses newlines (the `re.S` flag is dead code; `[^)]` needs no DOTALL).
Verified live: the real gloss at entry bytes 520–647 —

```
(rendered: the site owner is taken to consider the link target's page one it does not recommend,
or a link it cannot vouch for).
```

— is captured as one cell spanning the wrap, classified suspect
(`recommend|vouch` present, `crawl|巡回` absent). Canonical run at base `68228b2d`:
`C1.2_cells suspect_cells=1` (reproduced under v5; matches `base-c1-s374.txt`).

**Selftest (frozen v1): no.** Frozen `run_checks_fix` ran `RENDER_RE.finditer` **per
line**, so the multiline fixture cell never matched — `suspects` was always `[]`.
`ExecC1Selftest.md` §39 documented the per-line invisibility but missed the
verdict consequence below.

## Q2 — did a selftest cover the production parser?

**Frozen v1: no, and it masked a fatal defect.** `run_checks_fix` was a hand-written
approximation differing in three ways: per-line cell scan, correction required on a
single line, line-index vs char-offset positions. Concrete divergent verdict
(reconstructed frozen logic, in-memory):

- frozen selftest twin on its own `corrected` fixture → exit **0**
- frozen production `run_checks` on the same bytes → exit **1** (suspect at 42 < corr 209)

**Frozen v1 was unfixable-by-construction for the contract's prescribed repair.**
`mismatch = suspects where pos < corr_at` counts exactly the cells an *appended*
correction is meant to supersede; the contract requires append-only repair
("the old prose above is preserved as historical text"). Result: any entry
containing the original gloss + any valid appended correction can never print
`met=True`. Demonstrated in-memory on the real repaired entry:
suspects `[520]`, corr_at `2876`, mismatch `1` → exit 1. The vacuous selftest is
what let this ship — had `corrected` exercised the real parser it would have
exited 1.

**Current (v2+/v5): substantially yes.** `run_checks_fix` and `run_checks` share
`qualifier_findings` — the same `RENDER_RE`, `CORRECTION_MARK_RE`,
`NEGATIVE_CRAWL_RE`, `BOUND_CORRECTION_RE`, `BASE_RENDER` run on fixtures. The
multiline fixture gloss is `BASE_RENDER` verbatim, and `correction_before_render`
makes the verdict depend on seeing the suspect cell. Verified live under v5:
selftest 9/9 `ok` (rc 0); canonical satisfied run at `8e408e0` →
`mismatches=0 met=True EXIT=0`; base `68228b2d` → `mismatches=1 met=False EXIT=1`.

**Residual selftest gaps (v5):**
- `run_checks_fix` still duplicates `run_checks`'s final boolean
  (`corr_at >= 0 and mismatch == 0`); a regression in `run_checks`'s `met` line
  is invisible to the selftest. It never calls `run_checks`.
- The selftest cannot run the committed-byte path at all; `git show` plumbing and
  per-check `add()` wiring are unexercised.

## Residual falsifications on the settled (v5) counter — all demonstrated in-memory

1. **Positional supersession, not referential.** Any suspect cell *ending before*
   the first valid correction is cleared. An extra unqualified gloss
   `(rendered: the owner does not recommend or vouch for the link at all)` inserted
   between the original gloss and the correction → still `met=True`. The correction
   need not identify which cell it supersedes.
2. **Exact-format cell grammar.** `\(rendered: ` requires the literal colon+space:
   `(rendered:` followed by newline (or no space) evades detection entirely →
   `met=True` with the bad gloss present.
3. **Inner-paren truncation.** `[^)]+` stops at the first `)`. A cell
   `(rendered: marks link (as noted) owner does not recommend or vouch)` drops the
   endorsement tail → cell invisible → `met=True`.
4. **`crawl|巡回` substring discharge.** A bad gloss carrying bare 「巡回」
   (e.g. `…does not recommend the link — 巡回制限の話`) clears suspect-hood without
   asserting any crawl qualifier → `met=True`.
5. **Overfit correction acceptance** (over-strict; false-rejection, not false-pass):
   `NEGATIVE_CRAWL_RE` requires literally `not recommend (the)? (crawl|crawling)` —
   "does not recommend that crawling be restricted" or "should not be crawled" fail;
   `BOUND_CORRECTION_RE` requires the token sequence
   `earlier rendering … endorsement … supersedes … gloss` in order. Both are
   wording-locked to the landed repair.

## Scope notes / honest claims

- The counter reads committed bytes only (`git show <rev>:<path>`); all runs
  performed were read-only (`-B`); `run_checks` performs zero mutation. Same
  committed bytes → same verdict (verified at `68228b2d` and `8e408e0`).
- `met=True` is now reachable and demonstrated on the canonical command at
  `8e408e0` under the **v5 worktree script** (uncommitted). The committed
  `8e408e0` script is v2 semantics (window-based, no anchored/bound/BASE_RENDER);
  the worktree drift is uncommitted review-surface delta.
- `ExecC1Selftest.md`'s retained output is stale w.r.t. every version after v1;
  `controls/c1-selftest.txt` agrees with current code, not with the frozen one.
- Frozen-state reconstruction (`acae1dc` logic) ran in-memory only; no checkout or
  index was touched.

## Verdict

Findings only. The original multiline gloss is observed by production `run_checks`
(all versions). The **frozen** selftest was a divergent approximation that could
not see multiline cells and thereby concealed that the frozen counter could never
report `met=True` on the contract's append-only repair — the headline defect this
review was assigned to test. Post-repair code shares one parser between selftest
and production, but supersession remains positional and the cell grammar remains
exact-format brittle (items 1–5).
