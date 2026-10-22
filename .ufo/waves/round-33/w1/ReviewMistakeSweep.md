ReviewMistakeSweep — r33 w1: rounds 31–32 findings with no lesson ## Mistakes row

Seat: KakeR33.ReviewMistakeSweep (leaf). Axes: operability (lesson ledger vs wave reports)
and freshness (recheck/drift gaps). Read-only sweep; the only lane write is this file.
Comparison set: ## Mistakes rows in round-31.md (8) and round-32.md (1), plus
round-32.md "Carried open" and corpus/lessons/round-32-verifier-spotcheck.md "Routed
defects" 1–7, so items tracked elsewhere are not called unmined. Read: all 34 files in
.ufo/waves/round-32/w1/; predecessor .ufo/waves/round-32/w1/ReviewMistakeSweep.md
(U1–U7) re-checked for residual status. All checks on a sandbox clone at bc6c4a8
(/fast/scratch/hyaku/kake-r33/w1/ReviewMistakeSweep/clone, `git clone` + `checkout -q`,
exit 0); no counter or selftest executed — file/receipt reads only.

## Candidates ranked by clarity of captured-by gap (no Mistakes row, untracked)

1. **counter misattributes which condition failed** — w1/MutC2Conditions.md F1: mutant M2
   (S062 `opened` cell changed) drops met by 2 not 1; c3Cites is built only from rows that
   pass the opened-date filter (c2_retained_count.py:54-61). Captured-by: routed item 4 lists
   the counter's seven coverage holes (ReviewC2CounterCode F1–F7) but not this executed
   attribution defect — neither a row nor a routed line.
2. **receipts captured while the registry failed the census** — w1/ReviewCensusShape.md F2:
   after-receipts verification/c2-after-2f2f12d.json were taken at 2f2f12d where
   sources-census.sh validate exits 1 (E09, S062 free-text recheck); fixed at 285abca.
   Captured-by: none — nothing requires the tree to validate at the rev a receipt names.
3. **blank reason_contains accepted; one bad spec zeroes the suite** —
   w1/ExecReasonContainsNegatives.md F2/F1: `"reason_contains": "   "` passes load validation
   and fails as a spec (exit 1) instead of bad input (exit 2); one malformed spec makes the
   whole hostile suite exit 2 with `cases: []`. Live at tip
   (citing_set_hostile_selftest.py:142-144,243-253). F3 (exit 1 conflates spec-fail and
   crash) overlaps routed item 3.
4. **hostile selftest silently skips a symlinked spec dir** — discovery filter
   `citing_set_hostile_selftest.py:237` is `p.is_dir() and not p.is_symlink()`; a symlinked
   spec dir (or citing-set-hostile itself symlinked out of --root) is skipped silently — the
   shape the lane repaired in the runner and row 5 of round-31.md, never extended to the
   hostile harness. Evidence: a2-w2/ReviewHostileSelftestCode.md:33-40 (F3/F4 LOW); live at
   tip. Absent from carried open (which names only F2's NUL crash), routed defects and rows.
5. **"before measurement" not provable from history** — w1/ReviewDeclarationOrder.md note:
   the before receipts measure a0b0dff but first appear in the repair commit 2f2f12d with
   the build; the ordering claim rests on receipt content only. Captured-by: the new
   QUALITY criterion (QUALITY.md:549-554) covers the stated clock time, not commit layout.
6. **stale docstring/diagnostics at tip** — citing_set_hostile_selftest.py:2 still says
   "(round 31)"; the Output docstring (:62-64) omits `runner`/`error` keys main() emits
   (:235). w1/ReviewHostileSelftestDiff.md INFO items; live at tip. Captured-by: none;
   cosmetic, lowest rank.
7. **freshness header gaps for S062** — w1/CriticS062KindTier.md adjacent gaps:
   render-web-services.md:1 `source:` omits S062; the S062 drift check lives only in the
   appended section (:107-109), not the header `recheck:` line (:3 covers S057–S060 only);
   gate quote (round-32.md:31) spans render.yaml lines 2–7 while `teaches` cites lines
   15–16. Still true at tip. Captured-by: none (each soft — precedent is new entries).

## Round-31 carried items — residual check (carried by pointer in round-32.md, no row)

U1–U3, U5–U7 stand as carried. **U4 residual only**: census-mode receipts
(.ufo/waves/round-31/census-mode-{before-f1ffb81,after-a2}.txt) now exist — the "no
census-mode receipt" core is repaired; what remains is census-before.txt and
census-after.txt still byte-identical validate transcripts (sha256 6ba6b789…c186 each at
tip, verified) named for a 56→61 change they cannot witness.
One addendum to the predecessor's list: round-32 w1 itself produced findings absent from
every row and from that carried list — items 1–7 above.

## Tracked elsewhere — not gaps (verified live state, excluded)

Routed (round-32-verifier-spotcheck.md 1–7): m3d/m3f/m3g incl. the m3g under-count (1);
reason-text pinning (2); C1 probe killed/timeout holes (3); C2 counter coverage + hollow
commit (4); PROVINCE.md:122 "five hostile fixture shapes" — still live at tip, six specs
since P6 (5); shared-scratch collision (6); routed item 3 sub-items — still open at tip,
citing_set_selftest.py:403-417 (7). Patched elsewhere: SCORECARD.md:1060-1068 corrections
(behaviour-equivalent → refusal-equivalent; h0-control misattribution; P6-vs-P3
redundancy); QUALITY.md:562-567 discloses the declared-time check's narrowness.
Note for whoever owns c2_pin_count.py: it repairs the routed item-4 classes (exact `## `
heading equality at :73, unescaped-pipe split at :119, row pinned to S065 at :120,
path/mode/id-exact retention at :101-107); residual same-family risk (unverified):
section() still stops on a `## ` line inside a fence, and a failed `git archive` leaves
rev.tar absent → crash exit 1, not 2.

## Not verified

No counter, selftest or census run by this seat; tip-state claims rest on committed bytes
at bc6c4a8 and the committed reports. I did not re-read the 38 round-31 a2-w2 reports;
the predecessor's U1–U7 enumeration is trusted and only re-checked for residual status.
Tooling: none installed (pacman paused; none needed).
