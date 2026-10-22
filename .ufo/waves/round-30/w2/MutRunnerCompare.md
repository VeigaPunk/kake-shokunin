# Wave 2 — MutRunnerCompare: mutant ledger for scripts/citing_set_selftest.py

Seat KakeR30.MutRunnerCompare (leaf mutation tester), milestone r30-falsify, axis operability: the
fixture runner as an oracle. Target 71c6bfabd7aa957d15732d9224888bb32849238a.

## Attack points (pristine runner sha256 0fc87d5b8134c841b02d0db33d8a3262fb774d0c8aacaefc6b6811f190b6530a,
gate sha256 dbfade45e59351fb5edc010dfc45a4e15e1213fdb6fad9ec1668ffd3b77b7f02)

* m1 ids only for object entries — :269 returns "ids" instead of "pairs".
* m2 missing reason is a wildcard — new `pairs_match` helper, relaxed check at :479.
* m3 skip case.json setup — :368 `if setup:` becomes `if False and setup:`.
* m4 ignore the exit code for object cases — :476 guarded by `mode == "ids"`.
* m5 accept mixed string/object oracles — :265 mixed-oracle ValueError replaced by a pairs conversion.

The runner bytes are identical at 451e98fc8415edf10f41b2aad656318e7edc84ca, so mutant commits were branched from 451e98f in my sandbox clone to let the C2 counter run on them too.

## Instruments (pristine, mutated, restored)

* B: the runner over the 41 committed fixtures: `python3 -B scripts/citing_set_selftest.py --root <tree> --tmpdir <scratch>`.
* C1: `.ufo/waves/round-30/c1_reason_count.py --root <tree> --revision <commit> --scratch <dir>`; S1:
  `.ufo/waves/round-30/c1_strict_checks.py --root <tree> --revision <commit> --scratch <dir>`.
* C2: `.ufo/waves/round-30/c2_quote_truth.py --root <tree> --revision <commit>` (corpus quotes only; it
  cannot observe the runner, reported for completeness).
* Pristine baseline (71c6bfa and 451e98f): B exit 0, 41 cases, 0 failed; C1 exit 0, 14/14, runner baseline
  exit 0; S1 exit 0, 6/6; C2 exit 0, 4/4.

## Mutant ledger (every row observed)

| mutant | commit | runner sha256 | B runner | C1 | S1 | C2 | verdict |
|---|---|---|---|---|---|---|---|
| m1 | 7a4ed844 | 9002ddd5 | exit 0 (41/41) | exit 1, 4/14 | exit 1, 5/6 | 4/4 | KILLED by C1 + S1 |
| m2 | 4675b032 | a6f12f04 | exit 0 (41/41) | exit 0, 14/14 | exit 0, 6/6 | 4/4 | SURVIVED |
| m3 | cfcc7816 | 410b7877 | exit 1, 3 failing cases | exit 1, 4/14 | exit 0, 6/6 | 4/4 | KILLED by B + C1 |
| m4 | ed5770a6 | 06e18c95 | exit 0 (41/41) | exit 0, 14/14 | exit 0, 6/6 | 4/4 | SURVIVED |
| m5 | ebec6953 | 0e374b51 | exit 0 (41/41) | exit 0, 14/14 | exit 0, 6/6 | 4/4 | SURVIVED |

Killing detail:
* m1: C1 checks R01-R08, F01, F02 all fail on the part "compared" (the renamed-gate experiment no longer
  makes the runner fail, because ids match while the reason differs). S1 S2 fails for all ten codes with
  "runner exit 0 on the renamed gate, want 1 (case mismatch)".
* m3: the runner itself fails 30-document-not-regular-file ("exit mismatch: expected 2, observed 0"),
  33-corpus-empty (observed corpus_directory_missing) and 37-root-not-repository-top-level (observed
  revision_not_found); C1 then fails every coded check because its runner baseline exit is 1, not 0.
  S1 does not notice: S2 only asks that the runner fails on a renamed gate, which m3 already does.

## Survivors: demonstrated false passes (coverage findings; contract left unchanged)

All three pass every instrument yet accept a wrong outcome; scratch fixtures in
/fast/scratch/hyaku/kake-r30/w2/MutRunnerCompare/demo/ :

* m2 (null reason wildcard): expectation `{"exit":2,"findings":[{"id":"input_invalid"}]}`; pristine exits 1
  with "finding mismatch: expected [["input_invalid", null]], observed [["input_invalid","corpus_empty"]]";
  m2 exits 0 (clean). No committed fixture carries a reason-less expectation, so no instrument sees it.
* m4 (exit code ignored for object cases): stub gate prints the expected finding but exits 0 where the
  expectation says 2; pristine exits 1 with "exit mismatch: expected 2, observed 0"; m4 exits 0 (clean).
  The declared contract says the exit code is compared exactly in both forms; no fixture separates them.
* m5 (mixed oracles accepted): expectation `{"exit":1,"findings":["alpha",{"id":"beta","reason":"r"}]}`;
  pristine exits 1 with `expected.json "findings" must be all strings or all objects, not mixed`; m5 exits 0.
  The malformed-oracle rejection has no fixture and no counter probe.
* m1 (killed) also passes the committed fixtures untouched (41/41); only the rename experiment in C1/S1
  detects it, so that probe is the only guard on reason-code comparison.

## Commands run (exit codes)

* `git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin clone && git checkout -q 71c6bfa` — 0.
* `python3 -B scripts/citing_set_selftest.py --root . --tmpdir .../tmp/base` — 0 (41 cases, 0 failed).
* `python3 -B mutants/<m>/citing_set_selftest.py --root clone --tmpdir .../tmp/<m>` — m1 0, m2 0, m3 1, m4 0, m5 0.
* `c1_reason_count.py --root clone --revision <rev> --scratch .../scratch/c1-<tag>` — base 0 (14/14),
  base71 0 (14/14), m1 1, m2 0, m3 1, m4 0, m5 0. `c1_strict_checks.py --root clone --revision <rev>
  --scratch .../scratch/strict-<tag>` — base 0 (6/6), base71 0 (6/6), m1 1 (5/6), m2 0, m3 0, m4 0, m5 0.
* `c2_quote_truth.py --root clone --revision <rev>` — base 0 (4/4), m1..m5 0 (4/4 each).
* Demo pairs (pristine vs mutant) on demo/fixtures-noreason, demo/fixtures-wrongreason,
  demo/fixtures-exit, demo/fixtures-mixed — pristine 1, mutant 0 in every pair.

## Evidence pointers

* Sandbox /fast/scratch/hyaku/kake-r30/w2/MutRunnerCompare/ (clone, mutants/, demo/, logs/, diffs-m*.patch);
  counter outputs .../logs/{c1,strict,c2}-<tag>.json; patches .../diffs-m{1..5}.patch (only
  scripts/citing_set_selftest.py changed in each mutant commit, 1-22 added lines).
* Pristine sites: scripts/citing_set_selftest.py:265, :269, :368, :476, :479.

## Restoration and lane safety

* Nothing in the lane repo was modified by this seat except this report; `git status --porcelain -- scripts/`
  is empty and the lane runner still hashes 0fc87d5b... The lane working tree already showed changes to
  PROVINCE.md, SKILL.md, corpus/README.md, corpus/knowledge/publish-channels.md and untracked .ufo files
  when I looked; those are not mine and I did not touch them.
* All mutation happened in the sandbox clone (branches mutant/m1..mutant/m5 over 451e98f); the clone is
  now checked back out at 451e98f with a clean tree and the pristine runner hash. No git write command and
  no jj command ran in the lane repo. The counters read only from git revisions (git archive, git show),
  so the lane working tree never influenced a measurement.

## Not verified

* I did not read the lane receipt files (.ufo/waves/round-30/verification/c1-after-71c6bfa.json etc.) and
  did not test mutants against the round-27 contract JSON or a pre-round-28 fixture set; I reproduced the
  claimed 14/14, 6/6 and 4/4 from the counters themselves.
* I did not exercise --min-cases, --timeout, unknown arguments or the could-not-evaluate paths under
  mutation, and no tool was installed or upgraded (python 3.14.8 and git 2.56.0 were already present).
