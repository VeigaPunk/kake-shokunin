# SimplifierCounters — YAGNI review of round-37 counters and spec tooling

Axes: operability (the only lane axis this item touches). Frontier walked: static dead-code scan,
line-by-line classification, base reproduction, one inert-deletion falsification run. I never
touched /fast/scratch/hyaku/kake-r37/ and never ran the C1 counter (bound).

## Result: zero deletions proposed. Both counters are deletion-frozen by their own output design.

The counters print their own sha256 into every output (`counterSha256`, c2_mutkill.py:220,
sealed_count.py:182). Any byte deleted from a counter changes that field, so a literally
byte-identical output after ANY counter deletion is impossible — the tasking's own evidence
standard cannot be met for these two files, and 50 recorded receipts pin the exact current bytes:

- sealed_count.py 2ebb39b585e2a35f16ff71397f2fb22477a7a3c0e95da4415a26b0430b0cf0e3 — pinned in 41
  receipts (c1-at-621fb528.json, reference.json, 34 ablation JSONs, 5 control JSONs, all at
  .ufo/waves/round-37/verification/).
- c2_mutkill.py d72e232e4d4f120b6b45139958c40e9364d44d3d902207c0705ac97c1b6d5cb6 — pinned in 9
  round-37 files (verification/c2-at-621fb528.json, 7 retained/controls/c2/*.json, quoted in
  ctl/CtlC2FixtureSets.md).

Deleting anything would break all of these cross-checks at once, for zero dead weight gained:
pyflakes 4.0.3 reports no unused imports or variables in any of the three files (exit 0).

## Evidence

Sandbox: /fast/scratch/hyaku/kake-r37w1/SimplifierCounters/clone at 4b089da (the three files do
not exist at base 621fb528 — they first appear at 202d625; measured revision for C2 is 621fb528).

1. Baseline reproduction (exit 1, correct: base is not met):
   `timeout 900 python3 -B clone/.ufo/waves/round-37/c2_mutkill.py --root clone --revision 621fb528 --jobs 8 > base.json` → exit 1;
   fixtures 101, validFixtures 101, mutants 32, killed 27, met false, survivors M07 M08 M09 M11
   M24, counterSha256 d72e232e… — every value and the exit code match the recorded receipt
   .ufo/waves/round-37/verification/c2-at-621fb528.json and its .exit (1). Byte-identical
   instrument, so before/after runs below are grounded.

2. Inert-deletion falsification (proves the self-hash mechanism): deleted the one line that is
   provably dead on this interpreter (`from __future__ import annotations`, inert on python
   3.14.8) from a sandbox copy c2_nofut.py, re-ran the same command → exit 1; `diff base.json
   nofut.json` shows exactly one differing line of 365: counterSha256 d72e232e… → 5b59067c… .
   All measured values byte-identical; the self-hash is the only observable. Conclusion: no
   deletion inside either counter can ever satisfy byte-identical output, and the measured
   values are otherwise stable.

3. Line-by-line: every line of both counters is exactly one of — output field consumed by
   receipts or sibling seats (failedOnE1/failedOnE2 are named in the ExecC2Fixtures dispatch;
   killers[:8]/perMutant feed MutSelftestTolerance and RevengerSurvivors), a guard that changes
   behavior on some input (mutant-count check, bwrap/python3 presence, max(1, jobs) at
   c2_mutkill.py:278, RecursionError catches), a pin (KEY_SHA256 :49, PREDICATE :51/:53,
   MANIFEST_SHA256 :56, E1/E2 :57-59), the frozen judge copy (run_fixture :145 + snapshot :141 =
   round-36 run_case at 1a16b8e3, incl. the no-write clause), or anti-recognition freshness
   (uuid-named files/dirs; sealed_count materialize/judge fresh-id mapping). Nothing is dead.

4. sealed_count.py is a clean adaptation: diff against round-36's counter shows the version-history
   prose was already dropped and no vestigial round-36 branch (e.g. the (check, reason, target)
   projection) was carried over. Not run — bound forbids it; classification above is from reading
   plus pyflakes, and its 41 receipts demonstrate the fields are consumed.

5. make_w1_spec.py (197 lines): single-use generator, no dead lines, and it is load-bearing
   provenance — w1-spec.json is NOT committed at 4b089da (git ls-tree shows make_w1_spec.py but
   no w1-spec.json; the file exists only untracked in the lane working tree), so the committed
   generator is the lane's only record of the wave-1 spec text. Round-35/36 precedent committed
   both generator and spec. Deleting it would change no measured value but destroy spec
   provenance — rejected.

## Frozen parts (out of scope, listed per tasking)

- Frozen predicates: "passed >= 25 of 28 sealed cases" (sealed_count.py:53) and "killed >= 32 of
  32 round-36 tool mutants" (c2_mutkill.py:51), with their operands CASES/TARGET/MUTANTS.
- Pins: KEY_PATH/KEY_SHA256/TOOL (sealed_count.py:48-50), MANIFEST_SHA256/E1/E2 (c2_mutkill.py:56-59).
- Frozen judges: c2_mutkill.py run_fixture (:145) and snapshot (:141) as the copy of round-36
  run_case at 1a16b8e3, incl. DUMPER; sealed_count.py judge (:141) + materialize/project
  anti-recognition mapping.
- Receipt-pinned counter bytes (the 50 files above) — frozen in effect post-declaration.
- E2-validity rule (c2_mutkill.py:281) — the declaration's own sentence for the non-claim counter.

## Considered and rejected (no identical-output deletion exists)

- Output fields (failedOnE1/E2, killers cap, perMutant metadata): consumed downstream — deletion
  changes output bytes. `max(1, args.jobs)`, count/bwrap/RecursionError guards: behavior changes
  on some input. `--key-file` (sealed_count.py:180): documented CLI half used for scoring tools
  against keys outside git and by reviewer seats' dummy keys. Shared jail/git/show helpers across
  the two counters: dedup is a refactor, not a deletion, and would break both self-hash pins while
  coupling the sealed instrument to the public one. The next deletion that would harm an axis is
  any single receipt-pinned byte (operability: verifiability) — the stop condition is here.

## Tooling record

uvx pyflakes 4.0.3 (ephemeral `uv tool run`, channel uv/PyPI, reason: static unused-code scan; no
host tool installed or changed). pacman untouched per host-wide pause.

## Not verified

sealed_count.py was not executed (no key; run-evidence restricted to the C2 counter). My no-dead-code
verdict for it rests on pyflakes, the full read, and the r36→r37 diff. The working-tree
w1-spec.json was not compared against a fresh generator run (would write into the lane tree).

Report: .ufo/waves/round-37/w1/SimplifierCounters.md
