# PlannerCalibrationWalk — S374 planning/data-walk (round 54)

Seat: `L1Kake54.PlannerCalibrationWalk` (leaf scout, read-only; sole write = this report)
Date: 2026-10-25
Scope: trace S374 from retained source phrase → old rendered gloss → correction →
counter predicate → base control → target commit; flag missing steps or mismatched
claim sentences. Findings only; no admission claimed.

## Traced chain — every station resolves

1. **Retained source phrase.** `.ufo/waves/round-52/sources/S374.html` line 104,
   once in the whole body: 「このリンク先のウェブページの巡回を推奨していない」.
   Page title: `リンク先のウェブページの巡回制限　― rel属性の利用`. Body sha256
   `3ad358bdbe7a74798df151c282e4b57af7475686dc405b3f8bad08f68881aecb` — identical
   at base `68228b2d` and target `8e408e0` (verified via `git show` + sha256sum,
   matches the digest pinned in the entry, contract, lesson and `source-reopen.txt`).

2. **Old rendered gloss (the harm).** `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`
   lines 13–14, unchanged since commit `5422ff3` (round 52):
   `(rendered: the site owner is taken to consider the link target's page one it does
   not recommend, or a link it cannot vouch for)` — endorsement vocabulary only; the
   source's crawl qualifier 巡回 is dropped. This is exactly the defect the round-53
   non-author spot-check (`corpus/lessons/round-53-verifier-spotcheck.md`, digest
   `68228b2d…` in MANIFEST rounds[]) ruled `quality=harmed`.

3. **Correction.** Same entry, appended `## Round-54 correction` block (lines 52–68)
   carrying mark `[r54-correction 2026-10-25]`, the exact source substring, and the
   crawl qualifier rendered "not recommend the crawling of the link target's web
   page". Append-only: the old prose is preserved as historical text per the
   contract's "the repair is appended, never rewritten".

4. **Counter predicate.** `.ufo/waves/round-54/contract.md` line 27 →
   `c54_s374_calib.py` line 40 `PREDICATE` → base/target receipts — one identical
   sentence everywhere: *"S374 qualifier: mismatches = rendered cells missing the
   crawl qualifier and not superseded by an r54 correction block; met when 0."*
   Counter: `python3 -B .ufo/waves/round-54/c54_s374_calib.py --root <lane>
   --revision <rev>`; reads committed blobs via `git show` only.

5. **Base control.** Committed receipt `.ufo/waves/round-54/controls/base-c1-s374.txt`
   and seat report `w1/ExecC1Base.md` at frozen base
   `68228b2d74e7930ae4f07e90e382a0d03ab80c7b`: `suspect_cells=1`, no correction
   block, `mismatches=1 met=False`, exit 1 — matches contract's do-nothing
   requirement exactly.

6. **Target commit.** `8e408e0` ("round-54: repair S374 calibration and settle r53
   ops debt", child of freeze commit `acae1dc`) appends the correction and lands the
   repaired counter. Executed by this seat: landed counter prints
   `mismatches=0 met=True` exit 0 at `HEAD` and `mismatches=1 met=False` exit 1 at
   `68228b2d` — byte-identical receipt line at base. Chain closed.

## Finding 1 (material): counter code changed after the freeze

The repair commit `8e408e0` rewrote `c54_s374_calib.py` (62-line diff vs frozen
`acae1dc`), and the rewrite was **needed, not cosmetic**:

- Frozen code had `mismatch = sum(1 for pos in suspects if corr_at == -1 or pos <
  corr_at)` — counting suspect cells that *precede* the correction. A superseded
  cell (the intended success shape, suspect before correction) therefore counted
  as a mismatch; the frozen implementation could **never** print mismatches=0.
  Landed code uses `corr_at < pos` — counting only cells *after* the correction,
  i.e. unsuperseded ones — which matches the frozen predicate's semantics.
- Frozen `EN_CRAWL_RE = r"\bcrawl\b"` could not match "crawling" in the landed
  correction text; landed `NEGATIVE_CRAWL_RE` requires the negative-polarity
  form `not recommend (the)? crawl|crawling` — stricter and passes.
- Selftest gained `correction_wrong_polarity` and `correction_before_render`
  cases; `controls/c1-selftest.txt` shows 7/7 ok.

The frozen predicate *sentence* is unchanged across plan/code/receipts (contract
rule satisfied at the sentence level), but the implementing *condition* moved
mid-round — the frozen counter as committed at `acae1dc` was unpassable, so C1
could only land by repairing the counter. The contract's "kill rule / code
changed after any seat has scored is not the claim's rule" precedent (cited in
fleet prompts, kumitate r42) makes this worth flagging to the closure.

## Finding 2 (minor): transient broken working-tree state observed

Mid-run the checkout briefly held a half-applied counter edit (`NEGATIVE_CRAWL_RE`
added but `CRAWL_RE` still referenced at line 89 → `NameError` on every run) and
a stale index state. Current HEAD `8e408e0` is consistent; residual working-tree
diffs (`c54_ops_debt.py`, `SKILL.md` c53_gate_truth.py row spelling) belong to C2/
sibling lanes, not S374. No S374 step is missing from committed bytes.

## Claim-sentence audit — no mismatch

- Contract "Before": 1 suspect cell, no correction, mismatch = 1 → observed at
  base: `suspect_cells=1`, `mismatches=1`. Exact.
- Contract "After": appended `[r54-correction 2026-10-25]` block with exact quote
  + crawl vocabulary, mismatch = 0 → observed at `8e408e0`: `block_offset=2876`,
  `mismatches=0`. Exact.
- Second `(rendered:)` cell ("not weighed when the result order is decided")
  carries no endorsement/refusal vocabulary, so it correctly never enters the
  suspect set — predicate wording consistent with behaviour.
- `corpus/lessons/round-54.md` Mistakes row and Gate section name the same
  phrase, body path, digest and append-only fix; `source-reopen.txt` corroborates
  quote occurrence = 1 and local (non-network) re-open.

## Remaining unknowns

- No `.ufo/reports/round-54/` report exists yet; the closure's claim verdict and
  whether it will treat the counter repair as a freeze violation are undecided.
- C2 residual working-tree edits in flight (sibling concern; tracked here only
  because they share the checkout).

No tool installs performed (python3, git pre-existing). Confidence: high — all
stations verified against committed bytes, counters executed by this seat.
