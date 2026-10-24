# QualityCriteriaCheck — round 29, wave 2 (falsify)

Seat `KakeR29.QualityCriteriaCheck`. Item attacked: the appended `corpus/QUALITY.md` section "Fixtures, reason codes and quote truth — round 29" (lines 334-394) at lane commit 7697990cbca20291f3b0367b8ff4220e93b38b03. Work ran in a sandbox clone at `/fast/scratch/hyaku/kake-r29/w2/QualityCriteriaCheck/clone`, with TMPDIR inside the sandbox. Mutant commits exist only in that clone. Nothing in the lane was written except this file; lane HEAD is still 7697990. No tools were installed and no network was used.

## Prefix check (append-only, round-20 ruling): holds
- `git show fe1805cf:corpus/QUALITY.md` is 26089 bytes / 332 lines; at 7697990 the file is 30246 bytes / 394 lines. `cmp -n 26089 base new` exits 0.
- The sha256 of the base and of the first 26089 bytes of the new file are both 27fbe16f…aeef0f. Only 7697990 touches the file in fe1805cf..7697990.

## Grounding citations
- `corpus/lessons/round-28-verifier-spotcheck.md:208-230`: holds, with slightly loose bounds. Routed defects 1 to 3 are at lines 208-227; lines 228-230 belong to defect 4.
- `corpus/lessons/round-28-verifier-spotcheck.md:70-74` (the eight reason codes): holds. All eight are on lines 70-74.
- `corpus/QUALITY.md:298` (round-28 heading) and `:317` ("Conformance exceptions stay named"): both hold.
- `.ufo/waves/round-28/c1_interface_count.py:141` (match on the id only) and `:150-151` (`findingReasons` is a display field only): both hold. The file is unchanged between fe1805cf and 7697990.
- `.ufo/waves/round-28/c2_source_count.py:126-131` (quote shape only, no source read): holds.
- **`PROTOCOL.md:398-402` (§Gate standard, Self-test): broken.** The lane tree has no `PROTOCOL.md` (`git ls-tree -r 7697990` lists none). In the fleet `PROTOCOL.md` (HEAD 7c5b34f, working tree identical), lines 398-402 are the **Registry** clause. The Self-test clause is at lines **385-389**. The wave-1 draft carried the same wrong range (`.ufo/waves/round-29/w1/DraftQualityCriteria.md:46`).
- **"Round 28 observed `grep -rl reason scripts/fixtures/citing-set` → 0 files" (QUALITY.md:357-358): false provenance.** `git grep 'grep -rl reason' fe1805cf` finds nothing. The command first appears in round-29 wave-1 (`DraftQualityCriteria.md:10`). The finding itself is true: I re-observed 0 files at both fe1805cf and 7697990, and the 29 fixtures have only the keys `exit` and `findings`. What round 28 actually recorded is the related `git grep` statement at spot-check line 212-213.
- **"(see the round-29 note below)" (QUALITY.md:373-374): dangling pointer.** No note follows in QUALITY.md; lines 375-394 hold two more bullets. The note landed at `corpus/lessons/round-29.md:88` ("Not repaired this round").

## Per-criterion verdicts

1. **A committed fixture asserts the reason code (lines 348-363): limit to state.** The rule is grounded in spot-check lines 210-215 and 223-227, and it narrows line 317 without contradicting it. The Fails-if line can fail. In fact it **fails today on the lane's own tip**, because unlike criterion 2 this criterion has no deferral clause:
   - `python3 -B scripts/citing_set_selftest.py` at 7697990 exits 0 (29 cases, 0 failed), and 0 fixtures name a reason code.
   - At sandbox mutant dcc5ebf, all eight reason codes are renamed `zz_*` in `scripts/citing_set.py`. The same self-test still exits 0 with 29 cases and 0 failed.
   - The Fails-if line is also weaker than the rule it guards. A single fixture naming a single reason would clear it, while seven of the eight codes stayed uncovered.
2. **A counter compares the reason code (lines 364-374): holds, apart from the dangling pointer.** The Fails-if line is live. `python3 -B .ufo/waves/round-28/c1_interface_count.py --root . --revision dcc5ebf…` exits **0 with 15/15**, and its output shows all eight renamed `zz_*` reasons in `findingReasons`. The control run at 7697990 also exits 0 with 15/15. So the old counter meets the stated failure condition, which shows the condition can fail. The deferral to the next round that works this surface is consistent with `corpus/lessons/round-29.md:88-100`.
3. **A Gate quote is found in retained source text (lines 375-388): holds.** The Fails-if line is live:
   - At 7697990, `c1_quote_truth.py --revision 7697990` exits 0 (4/4, `controlBroken` false).
   - Mutant d4d66e6 flips one letter in the S040 Gate quote in `corpus/lessons/round-29.md:36`: exit **1**, 3/4.
   - Mutant 6f4f0e4 appends one byte to `.ufo/waves/round-29/sources/S040.txt`, so its digest no longer matches: exit **1**, 3/4.
   - No contradiction with the earlier quote rules (QUALITY.md:170-173 for round 25, 212-216 for round 26). One wording limit: the bar says "exact substring", but the cited counter collapses whitespace on both sides before comparing (`c1_quote_truth.py:51-52`, `:108`, `:111`).
4. **A new gate ships its fixtures in the same round (lines 389-394): holds, with one overstatement.** I reproduced the stub numbers:
   - `python3 -B scripts/base_path_selftest.py` exits 0 with 30/30.
   - With `--tool` set to a constant-clean stub: exit 1, 7/30.
   - With a refuse-everything stub: exit 1, 7/30.
   - With a copy of `base_path_audit.py` whose `input_invalid` reason is renamed: exit 1, 23/30. So the runner really does compare reason codes.
   - The overstatement: "each `expected.json` naming exit, verdict and reason codes" is true for 22 of 30. The 7 control cases and the 1 usage case pin an empty findings list.
   - The Fails-if line covers stub discrimination only, not reason comparison. The renamed-reason run above is the stronger evidence, but the section does not cite it.

## Contradiction check against earlier criteria
- I found no contradiction with lines 1-332. Criterion 4 is consistent with the round-28 "A counter must be able to reject a constant" bullet (lines 307-316), and criterion 1 keeps line 317 as history, as the section says.
- The internal inconsistency is within the section itself: criterion 2 is deferred to the next round, but criterion 1 is not, and the tip fails criterion 1.

## Smallest safe corrections (append-only; QUALITY.md lines are frozen, so these go in a later appended erratum)
- Cite the Self-test clause as `PROTOCOL.md:385-389` (fleet root), not `398-402`.
- Attribute the `grep -rl reason` observation to round 29 (`.ufo/waves/round-29/w1/DraftQualityCriteria.md:10`), or cite round 28's `git grep` statement at spot-check lines 212-213.
- Point "the round-29 note below" at `corpus/lessons/round-29.md:88`.
- Give criterion 1 the same deferral as criterion 2, or record that the citing-set gate fails criterion 1 at 7697990. Tighten its Fails-if to: "some reason code the gate can emit is named by no committed fixture expectation."
- Either say "exact after whitespace collapse" in criterion 3, or make the counter compare exact bytes.
- In criterion 4, say "22 of 30 name reason codes; 8 pin an empty findings list".

## Impacted axes
- Operability: the criterion 1 bar fails on the citing-set gate as committed.
- Freshness and provenance: the wrong PROTOCOL line range, the round-28 attribution of a round-29 command, and the dangling pointer.

## Not verified
- I did not run `c2_matrix_count.py`, `base_path_audit.py` on real inputs, or the round-28 C2 counter against a quote mutant.
- I did not re-open any web source.
- I did not check other files in commit 7697990 beyond what is cited above.

Sandbox outputs are in `/fast/scratch/hyaku/kake-r29/w2/QualityCriteriaCheck/*.out`.
