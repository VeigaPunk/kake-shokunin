# CriticC1FalsePositive — C1 suspect classification audit

Seat: L1Kake54.CriticC1FalsePositive — read-only review of `.ufo/waves/round-54/c54_s374_calib.py`
against the frozen predicate in `.ufo/waves/round-54/contract.md`.
Lane state reviewed: HEAD `8e408e00fbe1c5908df62ba79e78c944bda479e2` ("round-54: repair S374
calibration and settle r53 ops debt"); do-nothing base `68228b2d74e7930ae4f07e90e382a0d03ab80c7b`.
All numbers below are from the named read-only counter and direct `git show` byte inspection —
no lane index or shared-checkout writes were made (sole write: this report).

## Observed landscape at HEAD `8e408e0`

`corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` contains exactly:

- **2 rendered cells** (`(rendered: ` marker count = 2):
  - off 520 — endorsement gloss of `このリンク先のウェブページの巡回を推奨していない`:
    "…one it does not recommend, or a link it cannot vouch for".
    `SEMANTIC_RE` hits, `CRAWL_RE` misses → **suspect=True**.
  - off 759 — ranking gloss of `検索結果の表示順序を決める要素としては考慮されません`:
    "the attribute is not weighed when the result order is decided".
    `SEMANTIC_RE` misses (no recommend|vouch|endorse|refusal|refuse) → **suspect=False**.
- **1 correction mark** `[r54-correction 2026-10-25]` at off 2876; its 1200-byte window
  contains the exact QUOTE and matches `NEGATIVE_CRAWL_RE` → valid, `corr_at=2876`.
- QUOTE occurs twice in the entry (quoted block + correction block) and exactly once in the
  retained body `.ufo/waves/round-52/sources/S374.html` (sha256
  `3ad358bd…aecb`, verified — matches contract).

Counter receipts (landed tool, this session):
- `--revision 8e408e0`: `C1.2 suspect_cells=1`, `C1.3 block_offset=2876`,
  `C1.4 mismatches=0` → `met=True EXIT=0`.
- `--revision 68228b2d`: `suspect_cells=1`, no correction, `mismatches=1` → `met=False
  EXIT=1`. Identical to committed receipt `controls/base-c1-s374.txt` (byte-for-byte content).
- `--selftest`: 7/7 fixtures ok, including `correction_wrong_polarity` and
  `correction_before_render` → `EXIT=0`.

## Verdict on the suspect classification at the claimed state

**False positives on non-suspect rendered cells: none.**
The ranking-only cell (off 759) is correctly not counted: it lacks endorsement/refusal
vocabulary, and its source sentence is genuinely ranking-only — the retained body reads
"…新しいウェブページを見つけるために利用されますが、検索結果の表示順序を決める要素としては考慮されません",
so nothing about that gloss demands a crawl qualifier. Two non-defects noted but verified not
charged: (a) the counter's *literal* predicate wording "rendered cells missing the crawl
qualifier" is broad enough to cover cell 2, but the contract's "Before" clause binds the
mismatch to cells that "describe the S374 phrase with endorsement/refusal vocabulary", and the
implemented `SEMANTIC_RE` gate matches that binding — consistent, not a false negative; (b) the
ranking gloss is loose ("the attribute" for "the URL with the attribute") and drops the
used-to-find-pages half, but those inaccuracies are outside this predicate's scope and are
separately covered by the entry's own "URL is still used to find new pages" prose and the
correction block.

**False negatives: none at the observed states.**
The only cells that exist are enumerated above; cell 1 is flagged at base and at HEAD.
The correction block itself is not `(rendered: …)`-wrapped, so it cannot self-flag even though
it contains "recommend" — and its "not recommend the crawling" phrasing is precisely what makes
it a *positive* correction, so treating it as a non-cell is the right asymmetry.

**"Exactly one mismatch" confirmed end-to-end.**
Pre-repair: the sole bad gloss is cell 1 (endorsement-only, drops 巡回); `mismatches=1` at base.
Post-repair: the same cell is superseded by the appended valid correction; `mismatches=0` at
HEAD. The actual source-to-gloss correction was exactly one cell, both in bytes and in counter
accounting.

## Residual attack surface (latent, not triggered)

Tested the strongest counterexamples available against the committed bytes; these are fixable
defects in classification breadth, none firing at HEAD:

1. **Correction validation is too narrow (`NEGATIVE_CRAWL_RE`).** The contract only requires
   "states the crawl qualifier with English crawl vocabulary". A semantically valid correction
   phrased "discourages the crawl", "crawl is not endorsed", or "recommends against crawling"
   fails the `\bnot\s+recommend…` shape → false unevaluation (exit 1 despite a real repair).
   Asymmetric: suspect cells accept bare `crawl|巡回`, corrections accept only one phrasing.
2. **`CRAWL_RE` substring suppression → latent false negative.** A suspect cell that *quotes*
   the Japanese source (`巡回` inside the gloss) while rendering endorsement-only English would
   not be flagged; likewise "crawlspace"/"pub-crawl" or a gloss glossing another page's crawl
   sentence in the same cell. Only dormant because cell 1 quotes no Japanese.
3. **Positional supersession is undiscriminating.** `corr_at < pos` means a single correction
   forgives *all* earlier suspects, not just the one it quotes. A second stale gloss inserted
   before the correction would be silently superseded → false negative on multi-defect states.
   Current file has exactly one suspect, so not triggered; selftest fixture
   `correction_before_render` covers only the post-correction side.
4. **Cell extraction `[^)]+` truncates at the first literal `)`.** A gloss containing "(i.e.
   not recommended)" or any `)` inside the render cell shortens the examined text; a truncated
   prefix that loses the last "recommend"/"vouch" token would escape the suspect flag →
   false-negative path on gloss punctuation style alone.
5. **Cell syntax is marker-bound.** Only `(rendered: …)` counts. An unmarked gloss that
   misrenders the phrase (e.g., the free prose at entry line ~20) is invisible to the count.
   Today the only unmarked crawl-adjacent prose is accurate, so the binding is consistent —
   but the predicate silently delegates "rendered cell" to a syntax convention.

## Prior-version defect (fixed before final HEAD — documented for provenance)

At `acae1dc` (the commit live when this seat started), the counter had **inverted supersession
direction**: `mismatch = sum(1 for pos in suspects if corr_at == -1 or pos < corr_at)` counted
*superseded* cells, making `met=True` unreachable for any appended repair; `run_checks_fix`
also crashed (`NameError: EN_CRAWL_RE` — name existed only in `run_checks` scope) and used
per-line logic divergent from `run_checks`. Commit `8e408e0` replaced both paths with shared
`qualifier_findings()`, flipped to `corr_at < pos`, and added the two polarity/position
fixtures. Verified: the fix is real on the landed bytes (receipts above), not a shim.

## Impacted axes

- Calibration (C1): counter now sound at both endpoints; receipts match committed controls.
- Admissibility risk: residual items 1–5 are lanes for future mutation attacks; item 1 is the
  only one that can flip a *correct future repair* to exit 1 (fixable by widening the
  correction-side crawl vocabulary to match `CRAWL_RE` semantics or the contract wording).

## Smallest safe correction

None required for the current claim state — `mismatches=0` at `8e408e0` is a true reading, and
`mismatches=1` at base is a true reading. If hardening is wanted before reliance: align the
correction-side qualifier test with the contract's "English crawl vocabulary" wording
(`EN`-crawl token + the QUOTE, not the single `not recommend the crawl` phrase shape), and
count suspects relative to the correction's *quoted* cell rather than its byte position alone.

## Tool installs

None. pacman transactions paused host-wide per wave instructions; nothing required.

Report: .ufo/waves/round-54/w1/CriticC1FalsePositive.md
