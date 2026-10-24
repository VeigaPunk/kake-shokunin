# ReviewQualityCriteria — round 47, w1

**Target:** `corpus/QUALITY.md:1072` ("Citation reason fidelity") and `corpus/QUALITY.md:1073`
("Verdicts carry committed receipts") — groundedness in round-47 mistakes and resolution of
their evidence pointers.

**Method:** read-only. No language server answers Markdown evidence artifacts in this lane, so
`lsp references`/`definition`/`diagnostics` were not applicable and no semantic-LSP result is
claimed; callers were checked by `git show`/`git diff` against the frozen base
`cd42e3c310ba442e89dde638ba6401adaefaf3e8` and by file-level reads. Every sha256 below was
recomputed locally. Nothing in the lane was mutated; the two predicate probes ran on
module-in-memory copies (scratch: `/fast/scratch/hyaku/kake-r47/ReviewQualityCriteria/`).

## Verdicts

| Criterion | Grounded in a real r47/r46 defect | Evidence pointers resolve | Falsifier exists |
|---|---|---|---|
| Citation reason fidelity | yes | yes (spotcheck file + §Round-47 corrections both exist) | partial — phrase drift only |
| Verdicts carry committed receipts | yes | **no for the inline pointer**; yes for the adjacent correction block | no standing control |

Both criteria are genuinely motivated; neither ground is fabricated. The defects below are
pointer and enforcement defects, not invented grounding.

## Findings

### F1 — Medium (freshness): criterion B's inline pointer names a file that never existed

`corpus/QUALITY.md:1073` grounds the criterion on
`.ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt`.

```
$ ls .ufo/waves/round-47/verification/offline-sweep-r46-verdict-time.txt
ls: cannot access ...: No such file or directory
```

The lane itself records this at `corpus/lessons/round-47-verifier-spotcheck.md:41` ("never
committed — verified absent from tree") and repairs it only in the *next* block,
`corpus/QUALITY.md:1077`. Consequences: (a) the criterion body still directs a reader to a
nonexistent receipt; (b) the same dead path remains a live line in `LOG.md:1811`
(`receipt: ...offline-sweep-r46-verdict-time.txt`), superseded only in prose at `LOG.md:1815`;
(c) the citation carries no sha256, which the lane's own round-46 criterion "Receipt identity
for filed counts" (`corpus/QUALITY.md:1071`) makes a violation in its own right. The
append-only correction is legitimate practice, but the acceptance test ("their evidence
pointers resolve") fails on the criterion body as written, and any mechanical pointer check
over QUALITY will flag it.

### F2 — Medium (freshness): criterion B's inline example is a counter-example to its own clause

The criterion requires the output to be committed "at the round it is claimed". The only
receipt it names is the r47 rerun, whose first line states `R47 rerun only; not contemporaneous
r46 verdict-time evidence and not a retroactive receipt for it.` (verified in the committed
blob at `714e707`). Read literally against R6, the named example proves R6 *unfixed* under the
criterion's own wording; the qualifier that the r46 claim is *withdrawn* rather than receipted
appears only at `QUALITY.md:1077` and `LOG.md:1814`. The grounding would be honest if it named
the withdrawal as the R6 repair and the rerun as the positive example for a different claim.

### F3 — Low/Medium: the criterion's two normative clauses have no falsifier

The able-to-fail evidence (`c2-r4-mutation.txt`, mutation checker) exercises reason-phrase
drift only. Probes against the predicate that grounds the criterion
(`c47_routed_count.py:100 r4_reasons_fixed`, the same module the mutation receipt execs):

```
baseline, unmodified ledger                                       -> True
(a) old-line "reason says …" citation stripped from all 5 bullets -> True
(b) table row b74190e reason edited in place, block kept          -> True
```

So "citing the old line" and "never an in-place cell edit" are unenforced: an in-place cell
edit plus a surviving correction block passes. This round's compliance with the append-only half
is real but proven only by the commit diff (`git diff cd42e3c --
corpus/quality/citation-adjudications.md` → single hunk `@@ -27,3 +27,28 @@`, 25 insertions,
0 deletions), not by any gate the criterion cites. A criterion whose distinctive innovation
(append-only repair) has no negative control is weaker than its wording implies.

### F4 — Low: the lesson pointer overstates the R4 population (6 vs 5)

`corpus/lessons/round-47.md:17-23` says "five ledger reason cells named ds4cc-marketplace …
and `dc8e1adf` named `CriticC2Sufficiency`", i.e. 6 rows. The correction block
(`corpus/quality/citation-adjudications.md:31-53`) has exactly 5 bullets — 4 repo-drift
(`b74190e`, `d69dd22`, `0c767c2`, `b9db4b1`) + 1 wrong critic (`dc8e1adf`) — matching
`corpus/lessons/round-46-verifier-spotcheck.md:70` and the criterion's own "five rows … / the
wrong critic" phrasing at `QUALITY.md:1072`. `QUALITY.md:1081` points at the overstated lesson
item as the motivating pointer, so the criterion inherits an off-by-one it does not itself
commit. The source spotcheck line 55 is itself ambiguous ("5 rows' reason prose misattributes
the external repo" while listing 4 such tokens), which is likely where the drift entered.

### F5 — Low: "Mistake 2/3/4" anchors are positional, not textual

`QUALITY.md:1081` and `QUALITY.md:1085` cite "Mistake 2", "Mistake 3", "Mistake 4" in
`corpus/lessons/round-47.md`. No such literal token occurs there (`grep -c "Mistake 2\|Mistake
3\|Mistake 4"` → 0; the only "Mistake" string is the `## Mistakes` heading at line 3); the
items are ordinals in that list (lines 5, 17, 32, 46). Resolution works today and append-only
ordering keeps it stable, but the pointer is not greppable and breaks if the list is reordered
or an item is inserted.

### F6 — Low (residual risk): counter keyed last-wins makes a future honest correction red

`r4_reasons_fixed` builds `entries[token]` and keeps the last bullet per token. A later
append-only re-correction of the same row with different prose —
`- Row b74190e … corrected reason: charter repo commit in the 2026-09-28 HUMAN push series` —
evaluates to `False` even though the round-47 block is byte-intact. The r47 counter (and the
receipt that stands on it) therefore cannot be re-run green at a future tip where the criterion
it grounds was followed again. Not a defect in this round's claim; a defect in the artifact
filed as durable evidence for it.

### F7 — Low: repo-vs-surface spelling is unstated

The citing line names `charter-ghp` (`LOG.md:47`: "(4) charter-ghp … the HUMAN pushed 5
commits …"), while the corrected reason says "charter repo commit". The correction is
substantively right (charter-ghp is the charter repo's Pages surface; the ledger's `9c28d29`
row already spells `webzites/charter`), but the criterion's phrase "the same repository … its
citing line names" does not say whether a deployment surface counts as the repository. A future
adversarial seat can argue both ways on this exact row.

## Verified positive (grounds the verdicts above)

- Criterion A's correction accuracy sampled and confirmed:
  `LOG.md:47-50` is the round-13 entry's charter-ghp clause carrying
  `b74190e`/`d69dd22`/`0c767c2`/`b9db4b1` under a HUMAN push series — the correction's
  provenance is exact. `dc8e1adf`: `SCORECARD.md:1550-1551` names ``CriticProbeLeniency``,
  `dc8e1adf`, 12 of 12, and `0b7779dc` is the `CriticC2Sufficiency` 11-of-12 row
  (`corpus/lessons/round-35.md:154-156`) — the correction is exact, including the
  disambiguation from the neighbouring row.
- Ledger is genuinely append-only versus the frozen base: `git diff cd42e3c --
  corpus/quality/citation-adjudications.md` = `1 file changed, 25 insertions(+)`, single
  appended hunk; the 20 data rows are byte-identical.
- Mutation receipt reproduces independently:
  `python3 -B .ufo/waves/round-47/c47_r4_mutation_check.py --root . --revision 714e7074110469a9ed2a3594677197baa0890905`
  → `R4_REASON_FIDELITY base=pass mutants=5/5_rejected PASS`, exit 0.
- All cited sha256 pins recompute exactly, at `714e707` and at HEAD (no drift):
  `c2-r4-mutation.txt` `1e7636ec…507c3`; `offline-sweep-r47-rerun.txt` `b86bc459…2a717`;
  `c2-after-846138c.json` `af6fcdbf…1674`; `c2-after-714e707.json` `141ede64…1b5dba`.
  Receipt-internal pins also hold: counter `9be35ef2…359e`, ledger `e75bc3a7…669`, probe
  `0c8aa7a4…ada2` — identical at `714e707` and HEAD.
- Criterion B's positive case is a real committed receipt at the claiming round:
  `git ls-tree 714e707 .ufo/waves/round-47/verification/` lists
  `offline-sweep-r47-rerun.txt` (`blob d43c3215…`), its content read from that revision hashes
  to `b86bc459…2a717`, and it ends `VERDICT: OK (exit 0, partial: offline)` /
  `OFFLINE_EXIT=0` after opening with the non-retroactive label — i.e. the r47 rerun claim, and
  only that claim, is receipted.

## Verification gaps / not run

- No `Check:` line exists for either criterion (no "Check:" between `QUALITY.md:1070` and
  `1085`), so neither has a gate. Criterion B has no standing control at all; its only
  able-to-fail demonstration is the historical r46 defect.
- I did not re-run `node scripts/freshness-sweep.mjs --offline` (live-host action outside this
  seat's read-only remit); the receipt's contents are verified as bytes, not as a fresh
  execution.
- No tool was installed or updated for this review (`python3`, `git`, `grep` only).
