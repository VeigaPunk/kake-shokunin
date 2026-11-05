# MutC1 — mutation probe of the strict C1 counter (`c94_selfassess.py`, frozen digest 58028584…)

VERDICT: 12/12 killed; surviving: none (under the seat's rule). Caveat: E4-deletion-pin is killed only at the mismatch-count level (E4 1→0); the verdict `met` does not change, because the identity pin still refuses. Two kills are over-flags on clean fixtures, not missed defects (E2-criteri-test, E5-absence-span-ignored). Counter's own battery (supplemental, not the seat rule) kills only 4 of 12.

## Method (what was run)

- Scratch copy: `/fast/scratch/hyaku/kake-r94/MutC1/copy/` = `c94_selfassess.py` + `frozen/`. `sha256(copy) == sha256(LANE counter)` = `58028584f1aab19a294d24147854f56a703b2442f5af2d32fed69a5a87a8306a` (checked, True).
- Each mutant: one `str.replace` of a find string asserted to occur exactly once; the unified diff shows exactly one changed line (receipts `receipts/<id>.diff`). Each mutant lives in its own dir with its own `frozen/` copy.
- Per mutant: `python3 -B <mut> --selftest` (exit code); `python3 -B <mut> --root LANE --revision 0f7d9bbc… --skip-battery` (base); and each designated fixture with `--skip-battery --base-pins-json <SYNTH_PINS> --surfaces-file <synthetic surfaces>`.
- Reference (unmutated) runs: real LANE counter on base: `rc=1`, `lessons=88 entries=81 rows=255 criteria=39 mismatches=15 E1=0 E2=0 E3=0 E4=0 E5=15 pins=ok battery=0/8 predecessor_admits=0/0 floor=2 self_pin=ok met=false` (receipt `receipts/ref-base.txt`). Unmutated selftest: `rc=0`, `selftest 9/9 …` (`receipts/ref-selftest.txt`).
- Verdict compared = line 1 from `lessons=` through `met=`; rev and counter sha excluded (they differ by file).
- Fixtures: git fixtures in scratch (`git init` in `$S/fx/<id>`, toplevel asserted equal to the fixture dir before the first commit; identity `mutc1-fixture@example.invalid`). Each fixture = the counter's own `CLEAN` synthetic lane (clean commit) plus one defect commit. Fixture revs are in `mutants.json` (`fixture_revs`). Nothing was written to LANE; the counter ran read-only against LANE (`git show`, `cat-file`, `ls-tree`, `rev-parse`).
- Supplemental: full battery (`--work` in scratch) for the reference and every mutant on base, using a deep scratch layout so the counter's predecessor lookup (`here/../../../.ufo/waves/round-93/`) finds a copy of the frozen round-93 counter. Receipts `receipts/<id>-fullbattery.txt`.

Kill rule (seat): killed iff selftest rc ≠ 0 OR base verdict ≠ reference OR a designated fixture verdict ≠ reference fixture verdict.

## Per-mutant results

| id | class | selftest rc | base line 1 (mut) | designated fixture(s), mut vs ref (met) | killed (seat rule) | met flips? | full battery (supplemental) |
|---|---|---|---|---|---|---|---|
| E1-gate-heading | E1 | 0 | mismatches=15, E1=0 (same) | E1-gate: mut 0 met=true; ref 1 met=false | yes (fixture) | yes | 8/8 same |
| E1-vacuity-threshold | E1 | 0 | same | E1-vac: mut 0 met=true; ref 1 met=false | yes (fixture) | yes | 8/8 same |
| E2-criteri-test | E2 | 0 | mismatches=18 E2=3 criteria=48 (count only, met=false both) | E2-criteri-A: same (not discriminating); E2-criteri-B: mut 1 met=false; ref 0 met=true (over-flag) | yes (over-flag only) | yes (over-flag) | 8/8 same |
| E2-blob-nonempty | E2 | 0 | same | E2-blob: mut 0 met=true; ref 1 met=false | yes (fixture) | yes | 8/8 same |
| E3-rowid-vs-prose | E3 | 0 | same | E3-rowid: mut 0 met=true; ref 1 met=false | yes (fixture) | yes | **7/8** (killed by battery F5) |
| E3-locator | E3 | 1 | same | E3-loc: mut 0 met=true; ref 1 met=false | yes | yes | 8/8 same |
| E4-deletion-pin | E4 | 0 | same | E4-del: mut 0 `pins=identity` met=false; ref 1 `pins=identity` met=false | yes, count-level only | **no** | 8/8 same |
| E4-blankline-first-section | E4 | 0 | same | E4-first: mut 0 met=true; ref 1 met=false | yes (fixture) | yes | 8/8 same |
| E5-tree-check | E5 | 1 | mismatches=0 met=true (ref 15 met=false) | E5-tree: mut 0 met=true; ref 1 met=false | yes | yes | **7/8** (killed by battery F6) |
| E5-empty-blob-check | E5 | 1 | same | E5-empty: mut 0 met=true; ref 1 met=false | yes | yes | **7/8** (battery F6b) |
| E5-absence-span-ignored | E5 | 1 | same (count 15, no change) | E5-abs: mut 0 met=true; ref 1 met=false. E5-abs-B: mut 1 met=false; ref 0 met=true (over-flag) | yes | yes | 8/8 same |
| identity-pins-removed | pins | 1 | same | PIN-ident: mut 0 `pins=ok` met=true; ref 0 `pins=identity` met=false | yes | yes | **7/8** (battery F3) |

Notes per row:
- Selftest (seat column) killed 5/12: E3-locator, E5-tree, E5-empty-blob-check, E5-absence-span-ignored, identity-pins-removed. It did not kill E1-gate-heading, E1-vacuity-threshold, E2-criteri-test, E2-blob-nonempty, E3-rowid-vs-prose, E4-deletion-pin, E4-blankline-first-section.
- Base (real lane, skip-battery) killed 2/12 by verdict change: E5-tree-check (mismatches 15→0; met true) and E2-criteri-test (mismatches 15→18, E2=3). The other 10 are base-invariant (base has E1–E4 = 0, and E5 absence spans are absent at base, see below).
- E2-criteri-test and E5-absence-span-ignored are killed only by false positives on clean fixtures (the reference counter reads met=true there). This is a valid "different verdict" kill under the seat rule, but it does not show that the mutant misses a defect. The other 10 kills show a missed defect (reference met=false, mutant met=true or count changed).
- E4-deletion-pin is the only mutant whose `met` does not change. It is caught on the E4-del fixture by the E4 count (1→0), while the identity pin (`mistakes_section:`) still refuses the fixture. Deleting a `## Mistakes` section is therefore caught by the identity pin regardless of the E4 check, so the E4 deletion check is redundant for the verdict.

## Surviving mutants

None under the seat rule (0 survivors). Under a strict met-only comparison (predicate `met`, not count), one mutant survives: E4-deletion-pin (see above).

## Counter defects and gaps found (lane-internal findings, not repaired: counter is frozen)

1. Selftest coverage is thin. The 9 planted defects do not discriminate: the selftest's vacuous Gate has zero non-empty body lines, so threshold `<2` vs `<1` is not separated (E1-vacuity-threshold survives selftest); no planted missing `## Gate` heading (E1-gate-heading survives selftest); no planted non-criteria Round section and no planted empty cited lesson (E2-criteri-test, E2-blob-nonempty survive selftest); no planted prose-token id other than battery route F5 (E3-rowid-vs-prose survives selftest); no planted deleted-Mistakes-only case distinct from the identity pin (E4-deletion-pin survives selftest); no planted second `## Mistakes` section with a blank gap (E4-blankline-first-section survives selftest).
2. Battery route closure is narrower than the docstring suggests. Full battery (supplemental) kills 4/12: E3-rowid (F5), E5-tree (F6), E5-empty (F6b), identity (F3). It does not close E1-gate-heading, E1-vacuity (Fv uses a zero-line body, same weakness as selftest), E2-criteri-test, E2-blob-nonempty, E3-locator, E4-blankline-first-section, or E5-absence-span-ignored: no battery route targets these classes.
3. E4 deletion is closed by the identity pin, not by the E4 check (see E4-deletion-pin). Redundant, not a hole, but it means E4-deletion's `mismatches` count is not an independent signal.
4. The counter's predecessor lookup is relative to the counter file (`here/../../../.ufo/waves/round-93/...`). A copy outside the lane tree scores `predecessor_admits=0/0`, so `met` cannot be true under the full battery. Observed: the copy-located reference runs used `--skip-battery`; the full battery was run only in the deep layout (`receipts/REF-fullbattery.txt`: `battery=8/8 predecessor_admits=7/7 met=false`, false only because mismatches=15). [INFERENCE] for the plain copy without the deep layout: from code reading, not run.
5. Base contains no `[rNN-absence …]` span: E5-absence-span-ignored leaves the base verdict unchanged (E5 still 15), so the absence route is not exercised on the real lane. Only the synthetic selftest exercises it.
6. E2 criteri scope is load-bearing at base: dropping the `criteri` test adds 9 Round sections to scope (criteria 39→48) and 3 findings (E2=3). The current base has three non-criteria Round sections that name no lesson; the criteri test is what keeps them out. Not a defect; a documented scope decision that the counter should name in its docstring.

## Limits

- Mutants were chosen by me from the seat's list; the textual form of each is in `mutants.json` (`find`, `replace`). Equivalence to the original was not proven; the fixtures are the only evidence of non-equivalence.
- Fixtures are synthetic (the counter's own CLEAN lane, SYNTH_PINS, synthetic surfaces), not the frozen population: they test sensitivity of the predicate, not calibration of the real lane.
- Full-battery supplement used deep scratch layout; the seat rule did not use the battery.
- Single host run; no repeats; no timing data.
- Not run: `c94_conditional.py` (C2) and the round-93 counter beyond the battery's use of it.

## Receipts and cleanup

- `.ufo/waves/round-94/w1/MutC1/mutants.json`: per-mutant record (id, class, find, replace, selftest rc, base line 1, fixture line 1, met flips, full-battery tail, killed, fixture revs, summary).
- `.ufo/waves/round-94/w1/MutC1/receipts/`: `<id>.diff`, `<id>-selftest.txt`, `<id>-base.txt`, `<id>-fullbattery.txt`, `REF-fullbattery.txt`, `ref-base.txt`, `ref-selftest.txt`.
- Scratch `/fast/scratch/hyaku/kake-r94/MutC1/` removed after receipts were copied. Nothing under LANE edited; no git mutating commands run in LANE; no tools installed; no network access.
