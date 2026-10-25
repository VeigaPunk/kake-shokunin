# CriticC1CorrectionBinding — r54 C1 correction-binding attack

Seat: `L1Kake54.CriticC1CorrectionBinding` (critic, leaf, read-only).
Scope: attack the C1 "superseded by an r54 correction block" binding —
can an *unrelated* r54 marker plus text near it suppress the mismatch
without correcting the S374 gloss? Answer: **yes — concrete, demonstrated.**

## Verdict

C1.3 as implemented in `.ufo/waves/round-54/c54_s374_calib.py` (`8e408e0`
worktree + commit) binds a correction block by **position and token
co-presence, not by content**:

```python
for match in re.finditer(re.escape(CORRECTION_MARK), entry):
    window = entry[match.start():match.start() + 1200]
    if QUOTE in window and NEGATIVE_CRAWL_RE.search(window):
        correction_at = match.start(); break
mismatch = sum(1 for pos in suspects if corr_at == -1 or corr_at < pos)
```

A block qualifies iff (a) the literal marker `[r54-correction 2026-10-25]`
occurs anywhere (not required to start a line, contrary to the docstring's
"an entry line starting with"), (b) the exact source quote occurs within
1200 bytes after it, (c) `not recommend (the) crawl|crawling` occurs in
that same window. Nothing requires the block to mention, target, or
supersede the suspect rendered cell. "Supersession" is reduced to file
order: every suspect cell *before* a qualifying marker counts as corrected.

## Counterexample A — self-disclaiming block passes (demonstrated)

Append to the base entry (`68228b2d` bytes, one suspect cell intact):

```
## Round-54 housekeeping notes (2026-10-25)

**[r54-correction 2026-10-25]** Cataloguing note for the w2 gate audit: the
retained body line 「このリンク先のウェブページの巡回を推奨していない」
translates to "the owner does not recommend the crawl of the link target's
page". This note inventories phrasing for the registry; it does not supersede
or correct any rendered cell above.
```

The block **explicitly states it does not supersede or correct any rendered
cell**, yet the counter passes it:

```
PASS C1.3_correction: {'block_offset': 2861}
PASS C1.4_mismatch: {'mismatches': 0}
mismatches=0 met=True   EXIT=0
```

Receipt: scratch repo `/tmp/c1cex` rev `dcd26ce0222cc7a139b73da716708059ff87a91b`,
counter invoked exactly per contract (`--root <lane> --revision <rev>`,
production `run_checks` path, committed bytes via `git show`).

## Counterexample B — unrelated mid-prose marker + nearby text (demonstrated)

Marker used as a *ticket tag inside prose* (not a block opener, not a
correction), quote + phrase appearing in adjacent cataloguing text:

```
The w2 gate row audit is filed under ticket `[r54-correction 2026-10-25]` for
cross-reference. Unrelated scratch for the S374 entry: the catalogue indexes
the sentence 「このリンク先のウェブページの巡回を推奨していない」 as "owner
does not recommend the crawl of the target page". No rendered cell above is
changed or superseded by this note.
```

```
PASS C1.3_correction: {'block_offset': 2905}
PASS C1.4_mismatch: {'mismatches': 0}
mismatches=0 met=True   EXIT=0
```

Receipt: `/tmp/c1cex` rev `201051163f10c9b19f2ea309dd4f746f54a0d000`.
This is the literal hypothesized shape: an unrelated r54 marker, unrelated
text near it, zero correction of the S374 gloss — and `met=True`.

## Negative control (demonstrated)

Same entry, marker replaced by `[r55-audit]` (quote + phrase retained,
unchanged): `mismatches=1 met=False EXIT=1`. The marker is the suppressor;
the surrounding text alone does not pass.

## Impact on the landed claim

The genuine landed block at `8e408e0` ("this correction supersedes its
gloss") passes — but the counter cannot distinguish it from a block that
disclaims supersession, because **the supersession claim is never read**.
The frozen predicate's "not superseded by an r54 correction block" is
underspecified by the instrument: any downstream marker + quote +
correct-polarity gloss silences every upstream suspect.

Residual guards that *do* work: marker-before-suspect is rejected
(`correction_before_render` selftest), wrong polarity rejected
(`correction_wrong_polarity` selftest), missing quote/crawl rejected;
new stale cells appended after a correction still count. Selftest 7/7 ok.

## Drift observed during this review

Counter was edited mid-wave: first read (`#475A`) had `CRAWL_RE =
crawl|巡回` + inverted ordering (`pos < corr_at` ⇒ correction had to
*precede* the suspect, making the real appended correction a mismatch and
suppression trivial by a marker at file top); a later write introduced
`NEGATIVE_CRAWL_RE` + `qualifier_findings` + corrected ordering
(`corr_at < pos`). Both versions were run: current code at `acae1dc`
(freeze) → `met=False` (correction not yet committed — expected), at
`8e408e0` (repair) → `met=True`. Frozen-contract bytes cite counter path,
not a pin; the mid-wave redefinition itself is a provenance note the
closure should record (freeze commit `acae1dc` predates counter repair).

## Smallest safe correction

Tighten C1.3 to bind the block to the suspect it supersedes — pick any
combination the judge prefers, in increasing strength:

1. **Line-anchor + line-scope** (matches the docstring's own contract):
   `re.finditer(r"^[ \t>*-]*\[r54-correction 2026-10-25\]", entry, re.M)`
   and evaluate quote + phrase **within that same line/logical block**,
   not a 1200-byte window that can borrow tokens from unrelated text.
2. **Supersession vocabulary**: require the block to contain a
   supersede/correction token (`supersed|corrects?|replaces|the (?:earlier|
   above|old) (?:rendering|gloss)`), so a self-disclaiming note fails.
3. **Exclusion**: reject blocks containing an explicit non-supersession
   disclaimer (`does not (supersede|correct|change)` within the block).

Fixable defect — the counter stays one regex tighter; no new instrument
family, no contract rewrite. If the lane keeps token-co-presence only,
the canonical judge should treat "superseded" as positional sugar, not
binding: the counter then admits content that the contract sentence
("supersedes it", appended correction) does not.

## Axes impacted

- **Calibration (C1)**: claim-evaluating counter admits a non-correcting
  block → unearned `met=True` reachable; defect, not tradeoff.
- **Operability**: counter itself runs clean (selftest 7/7, exit contract
  honored, do-nothing control red as specified).
- **Integrity/provenance**: docstring ("entry line starting with …") vs
  code (any-offset match, 1200-byte window) disagree; mid-wave counter
  edit after freeze commit is a disclosure item for the closure.

No installs performed (pacman paused host-wide; none needed). Lane tree
untouched; all receipts from a `/tmp` scratch repo exercising the
committed counter code path.
