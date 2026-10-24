# R35 W1 — ReviewSelftestContractChange: harm check for C1 contract (c)

Scope: find every lane text and check at `318561ef` that relies on the round-34
behaviour "any input fault suppresses all policy findings" (early return with
input findings only), say whether contract (c) makes it false, and check the
round-34 matrix input-fault cases keep their expected outputs. Contract (c)
source: `SCORECARD.md:1385-1392` at `318561ef` ("a page that cannot be read …
no longer stops the other pages. The readable pages are audited, and their
policy findings are reported beside the input findings. The verdict stays
`could-not-evaluate` (exit 2), and `pagesChecked` counts the readable pages.
Manifest-level faults are unchanged"). Old behaviour in the landed tool:
`scripts/link_preview_audit.py:215-217` at `318561ef` — `if input_findings:
return result("could-not-evaluate", 0, input_findings), EXIT_INPUT` before any
policy pass.

## Method

- Read-only `git grep -n -e policy_suppressed -e could-not-evaluate -e
  page_unreadable -e link_preview 318561efa67206699fdaf259ffb86e39f2d916a8 --
  SKILL.md corpus scripts .ufo/waves/round-34` in the lane → 268 hits, triaged
  below (exit 0). Most `could-not-evaluate` hits are other gates
  (freshness-sweep, corpus-contract, canonical-audit, base-path, citing-set,
  accessibility packet, receipt-replay) whose exit-2 semantics contract (c)
  does not touch; `corpus/QUALITY.md:197` is the round-25 packet profile.
- Sandbox clone `/fast/scratch/hyaku/kake-r35/w1/ReviewSelftestContractChange/clone`
  at `318561ef`; minimal probe patch implementing (c) (seed findings with
  input findings, audit readable pages, exit 2 with mixed findings when any
  input finding exists), sandbox-only commit `f252a4f12cc0f1233dc9d42d1fb8c135ee590993`.
- Ran the round-34 frozen counter and the committed selftest against the probe.

## Matrix check result (kept)

`python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision f252a4f1…`
→ exit 0, `passed: 28/28`, `byKind input 7/7`, `constantGatesAllRejected: true`,
tool sha256 `13406cbf…8c07`, matrix sha256 `246a6a3b…14f7` (pinned, unchanged).
Every round-34 matrix case with an input fault keeps its expected output under
(c): I1–I3, I5–I7 are manifest-level faults (unchanged by (c)); I4
(`page-file-missing`) keeps `exit 2 / could-not-evaluate / [page_unreadable]`
because its readable page `index.html` is policy-clean; its `pagesChecked`
would move 0→1, and the matrix compares only exit, verdict and projected
findings (`c1-matrix.json` "comparison"). So the r34 matrix does not pin the
old suppression anywhere: no matrix case pairs an unreadable page with a
policy-defective readable page.

## Selftest check result (one fixture flips)

`python3 -B scripts/link_preview_selftest.py` on the probe → exit 1,
`34/35 passed`, exactly one failure:
`input_policy_suppressed_on_input: expected [('page_unreadable',)], observed
[('og_required_missing','og:image'), ('og_required_missing','og:type'),
('og_required_missing','og:url'), ('page_unreadable',)]`.
Its `partial.html` has only `og:title`, so under (c) the three missing-property
findings join the `page_unreadable` finding (exit and verdict unchanged).
The other seven input fixtures keep their expectations:
`input_missing_page` and `input_page_not_utf8` list a single unreadable page
(nothing readable to audit), the rest are manifest-level.

## Dependent texts and needed appends (all at `318561ef`)

1. `SKILL.md:1010` — live recipe row: "Exit 2, `could-not-evaluate` | Fix the
   input, never the page … Exit 2 reports input findings only". FALSE under
   (c) for `page_unreadable`: exit 2 now carries readable pages' policy
   findings beside input findings. Append: "Round 35 (c): an unreadable page
   gives `page_unreadable` and no longer stops the other pages; the readable
   pages are audited and their policy findings are reported beside the input
   findings; verdict stays `could-not-evaluate` (exit 2) and `pagesChecked`
   counts the readable pages; manifest-level `input_invalid` is unchanged
   (nothing audited)."
2. `SKILL.md:1024` — "run the selftest" instruction. Becomes inconsistent the
   moment the (c) repair lands: the committed selftest then fails 1/35 against
   a contract-conforming tool until item 3 is applied. Append: "the round-35
   repair changes the `input_policy_suppressed_on_input` fixture expectation."
3. `scripts/fixtures/link-preview/input_policy_suppressed_on_input/expected.json:1`
   — pins `{"exit":2,"verdict":"could-not-evaluate","findings":
   [{"reason":"page_unreadable"}]}`. FALSE under (c); must become findings
   `og_required_missing`×(og:image, og:type, og:url) + `page_unreadable`
   (exit 2, verdict unchanged — verified observed set above). The directory
   name is also a misnomer after (c) (policy is no longer suppressed); rename
   it (e.g. `input_policy_beside_unreadable`) with the expected.json update.
4. `corpus/README.md:318` — audit gloss "clean exits 0, policy findings 1,
   input findings 2, usage 64". Incomplete under (c). Append: exit 2 can
   carry readable pages' policy findings beside input findings when a page is
   unreadable; the 28-case matrix and both r34 counters stay valid (verified
   against the probe).
5. `.ufo/waves/round-34/c1-matrix.json:8` (frozen interface) — "exit 2 … only
   input findings are reported" and the I4 note at `:425` "input findings
   only; policy findings are not reported with them". Do NOT edit (frozen r34
   artifact); (c) supersedes them for the repaired tool per the SCORECARD
   "Every other round-34 rule … unchanged" line holds because no case pairs
   the two fault kinds. Needed append goes in the round-35 lesson/report: a
   supersession note naming `c1-matrix.json:8` and the I4 note, stating the
   note is true only because I4's readable page is clean.

## Texts checked and NOT false (no append needed)

- `SKILL.md:1003-1004` (invocation / frozen-counter rows): no suppression
  claim; counter row re-verified true on the probe (28/28, receipt in this
  report).
- `scripts/link_preview_audit.py:42-43` docstring ("Input problems produce a
  could-not-evaluate result"): still true under (c); the build seat rewrites
  it anyway.
- `scripts/link_preview_selftest.py:16` `INPUT_REASONS` and its projection
  (input=(reason,), policy=(reason, property)): unchanged code path; it is
  the fixture data, not the runner, that flips.
- Historical receipts/lessons pinned to revisions: `corpus/lessons/round-34.md`
  (real-input exit 1, mistake row 4), `corpus/lessons/round-34-verifier-spotcheck.md`
  C1 ruling, `.ufo/waves/round-34/w2/SentinelToolInputs.md:19` (observed
  `pagesChecked:0` on exit 2 — exactly the failure mode (c) repairs),
  `verification/selftest-link-preview-at-76fac3b.txt`, `real_input_run.py`
  (all 102 pages readable). They describe r34 state at pinned shas; (c) makes
  none of their sentences false.
- `.ufo/waves/round-35/sealed_count.py`: c1 projection is (page, property,
  reason) with exit+verdict — mixed exit-2 cases are expressible; no
  counter-side reliance on suppression.
- Out of scope by term: `corpus/SOURCES.md` S074 (Telegram LinkPreviewOptions,
  unrelated), `link-preview-metadata.md:193` (property-only rule, unaffected),
  all non-link-preview `could-not-evaluate` rows/scripts listed above.

## Commands and exit codes

- `git grep … 318561ef -- SKILL.md corpus scripts .ufo/waves/round-34` → 0.
- `python3 -B scripts/link_preview_selftest.py` (probe, TMPDIR sandbox) → 1
  (34/35, one failure as quoted).
- `git -c user.name=… commit` in sandbox clone → commit `f252a4f1…` (0).
- `python3 -B .ufo/waves/round-34/c1_matrix_count.py --root . --revision
  f252a4f1…` → 0, 28/28, allRejected true.

## Not verified / residual

- The 24 sealed C1 cases were not run (sealed key; never touched
  `/fast/scratch/hyaku/kake-r35/sealed/`). Nothing here judges whether the
  round passes.
- The probe patch is a minimal (c) implementation for dependency testing, not
  the build: it does not add the (a)/(b) repairs, and its exit-2 mixed
  findings ordering/id fields were not asserted beyond the selftest's
  projection.
- No lane file other than this report was written; the probe lives only in
  the sandbox commit `f252a4f12cc0f1233dc9d42d1fb8c135ee590993`
  (`/fast/scratch/hyaku/kake-r35/w1/ReviewSelftestContractChange/clone`).
- No tools were installed or updated.
