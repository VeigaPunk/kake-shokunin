# CriticClaimSeparation — round-47 w1

Seat: `CriticClaimSeparation` (critic). Axes: operability (C1), freshness (C2).
Target: falsify causal separation — can C1 pass with zero C2 fixes; can C2 pass
with zero C1 registry rows/receipts. Verdict: **separation VERIFIED** on the
counters' actual inputs, via a 2×2 that includes two synthetic cells; two
collateral defects found (stale receipt provenance, predicate-text drift).

## 1. Counter inputs (the real surfaces)

C1 — `.ufo/waves/round-47/c47_registry_count.py`:
- `SKILL.md` only, `|` lines containing `scripts/redirect_audit.py` /
  `scripts/citation_lint.py` (lines 99, 112–116, TOOLS 38–41).
- every committed file under `.ufo/waves/round-47/verification/`: needs needle +
  `selftest: 23/23 passed` (redirect) / `selftest: 8/8 passed` (citation) +
  `exit=0` + a 64-hex sha (lines 118–126). Never reads LOG.md or the ledger.

C2 — `.ufo/waves/round-47/c47_routed_count.py`:
- `LOG.md` (R3 "R3"+"20 data rows" one line; R5 both full hashes one line;
  R6 `[r47-correction R6 withdrawal]`+"round-46"+"withdrawn", lines 133–140).
- `corpus/quality/citation-adjudications.md` (`## Round-47 corrections` block,
  five tokens × `Corrected reason:` phrases, lines 40–46, 100–112).
- `.ufo/waves/round-47/verification/` — **only** files named exactly
  `offline-sweep-r47-rerun.txt` (line 143), needing the "R47 rerun only…"
  label, `--offline`, and `exit=0` OR `OFFLINE_EXIT=0` (lines 145–149).
  Never reads SKILL.md and ignores C1's selftest receipts.

Shared surface: the receipt **directory** only — and C2 filters it by exact
filename while C1 filters by tool needle + tally. Current overlap: none —
`grep -rl 'scripts/redirect_audit.py\|scripts/citation_lint.py' verification/`
returns only the two `selftest-*.txt`, and `offline-sweep-r47-rerun.txt`
contains no C1 needle or `selftest:` string (grep exit 1).

## 2. Full 2×2 — commands and observed outputs

All runs: `python3 -B .ufo/waves/round-47/c47_{registry,routed}_count.py
--root . --revision <rev> --json -` (read-only `git show`/`ls-tree`).

| state | revision | C1 | C2 |
|---|---|---|---|
| real base | `cd42e3c310ba…` | NOT_MET 0/2,0/2 | NOT_MET 4/4 outstanding |
| real tip | `766f4610b64f…` (also `714e707`, `7855262`, `59146c9`, `846138c` under the tip counter) | MET 2/2,2/2 | MET 0/4 |
| sandbox `mutA` (`47fba85a69a04c…`) | tip + `LOG.md` and `corpus/quality/citation-adjudications.md` restored to base bytes | **MET** rows 2/2, receipts 2/2 | **NOT_MET** R3–R6 all false |
| sandbox `mutB` (`c525bb00be0b54…`) | tip + `SKILL.md` restored to base bytes + `selftest-redirect-audit.txt`/`selftest-citation-lint.txt` `git rm`'d | **NOT_MET** 0/2,0/2 | **MET** 0/4 outstanding |

Sandbox: read-only `git clone` of the lane to
`/fast/scratch/hyaku/kake-r47/CriticClaimSeparation/lane` (local, unpushed;
lane checkout untouched). `mutA`/`mutB` commit on top of tip `766f461`.

- **Direction 1 (C1 w/o C2): PROVEN.** mutA reverts every file C2 reads to
  base; C1 still exits 0 because its inputs (SKILL.md rows, two selftest
  receipts) are disjoint from all C2 fix inputs. Reverting LOG.md also removed
  C1's prose narration — the counter did not notice (it never reads LOG.md).
- **Direction 2 (C2 w/o C1): PROVEN.** mutB leaves zero `|` rows naming the
  tools and zero needle-bearing receipts (verified: no remaining
  `verification/` file contains a tool needle); C2 still exits 0 because the
  counter has no code path that can consume SKILL.md or a `selftest-*.txt`.

Causal separation cannot be falsified: both directions hold. Neither counter
can observe the other claim's inputs.

## 3. Adversarial findings (impacted axes; smallest safe corrections)

### F1 — Evidence provenance defect, not disclosed at the artifact level
`verification/c2-after-846138c.json` records `outstanding=1, R6:false,
C2_NOT_MET`, but re-running the **current** counter at that revision returns
`C2_MET` (I reproduced both). Cause, verified by `git show 714e7074…`: commit
`846138c` had already landed **all** C2 fix inputs including
`offline-sweep-r47-rerun.txt` ending in `OFFLINE_EXIT=0`; `714e707` changed
only `c47_routed_count.py` (+2/−1) to accept that spelling. So the recorded
"after" pair measures a counter-code relaxation, not an artifact change, and
no real revision ever exhibited C1-fixed-without-C2. SCORECARD.md:3978
discloses the note, but the JSON artifact itself carries no counter-version
stamp and reads as a live verdict.
- Axes: freshness (provenance); operability unharmed.
- Smallest safe correction: regenerate `c2-after-846138c.json` with the tip
  counter (it will read C2_MET), or add a `counter_revision`/`superseded`
  field to the existing file — append-only, one receipt edit.

### F2 — Frozen predicate text diverges from enforced predicate
The frozen sentence in `SCORECARD.md:3957` and `c47_routed_count.py:21`
states the receipt records "`--offline` exit=0"; the actual receipt's exit
marker is `OFFLINE_EXIT=0` (line 87; the only lowercase `exit=0` in the file
is inside "VERDICT: OK (exit 0, partial: offline)" — which does satisfy the
literal `exit=0` substring! verified: `grep -n 'exit=0'` hits line 86 too).
So the predicate text is still technically true via the VERDICT line, but the
`714e707` code now *also* accepts a receipt with **no** literal `exit=0` —
the enforced predicate is strictly weaker than the frozen sentence.
- Axes: freshness (claim fidelity).
- Smallest safe correction: amend the one predicate sentence in
  SCORECARD.md + counter docstring to "…recording `--offline` and an
  explicit exit=0 marker" (single simultaneous touch, per the file's own
  frozen-sentence convention), or drop the `or "OFFLINE_EXIT=0"` disjunct
  since the VERDICT line already matches.

### F3 — Brittle (non-blocking): shared receipt dir
C1 scans *every* committed file in `verification/` for needle+tally+sha+exit.
Any future C2-support file there carrying `selftest: 23/23 passed`-style text
for a tool would silently satisfy a C1 receipt. Zero-cost hardening: restrict
C1 to `selftest-*.txt` filenames, mirroring C2's exact-name filter. Optional;
does not affect the current separation verdict.

## 4. Not run / caveats

- No selftest binaries were re-executed (`scripts/*_selftest.py --selftest`);
  receipts were trusted as committed bytes per the counters' own model.
- `c47_r4_mutation_check.py` was inspected, not re-run (mutation-tester's
  lane; its recorded run at `714e707` passed 5/5 mutants).
- Sandbox mutants are synthetic controls, not lane history: no real commit
  separates the claims — the repair commit `846138c` landed all inputs for
  both, and `714e707` changed only instrument code. Under each state's own
  contemporaneous counter, `846138c` was a true (C1=1, C2=0) cell; that cell
  evaporated retroactively when the counter relaxed (F1).

## Bottom line

Claim separation holds — C1's pass is causally independent of every C2 fix
input and C2's pass is causally independent of every C1 input; proven on
mutants since real history never split them. The historical record slightly
overstates how that separation was demonstrated (F1), and the C2 frozen
sentence no longer exactly describes what the counter accepts (F2).
