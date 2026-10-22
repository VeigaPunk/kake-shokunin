# KakeR32.CriticC1Wording — C1 declaration wording (round 32, wave 1)

Target: every sentence of C1 and its disclosed limits in `SCORECARD.md` "Round 32 — declared claims"
at 285abcad632e3c1c57bb402232e7d218054db383 (lines 1009-1038), checked against receipts and code.
Result: three overstated or misattributed sentences (one provenance, two low); the core C1 claim holds.

## Overstated sentences

1. **Provenance timestamp (MEDIUM, false provenance).** SCORECARD.md:1016-1017 "Declared at 18:58Z, before
   either counting command was run at any revision." Git metadata contradicts the clock time:
   - 5b32cc7 (declaration + both counters): author 2026-10-22T15:50:53-03:00 = 18:50:53Z, commit 18:54:19Z.
   - 2f2f12d (holds `c1-before-a0b0dff.json`): commit 15:55:33-03:00 = 18:55:33Z.
   - 285abca (holds `c1-after-2f2f12d.json`): commit 15:55:47-03:00 = 18:55:47Z.
   So 18:58Z falls after both C1 receipts were already committed; the stated time cannot be the declaration
   time. Commit order (counters committed before any receipt) is consistent with "before measurement",
   but whether a counter was run before 5b32cc7 was committed is not recoverable from Git (receipts carry no
   timestamp) — [INFERENCE] unverifiable either way. Smallest correction: replace "18:58Z" with the commit
   time (18:50Z authored / 18:54Z committed) or drop the clock time and cite commit order only.

2. **"m3 is otherwise behaviour-equivalent" (LOW, overstated universal).** SCORECARD.md:1034-1035. m3 is
   refusal-equivalent, not behaviour-equivalent: without the load-time guard the runner copies the case into
   scratch (`scripts/citing_set_selftest.py:510`) and executes every setup step before the `git_commit`
   (`:515`, `apply_setup` at `:473`) before the apply-time re-check refuses. Reproduced (sandbox, export of
   285abca, one case with setup `[mkdir made-before-refusal, git_commit, git_init]`):
   - pristine runner: exit 1, reason "case.json setup op 'git_commit' needs an earlier 'git_init'", no copy.
   - m3 runner: exit 1, reason "case setup failed: git_commit needs the repository created by git_init",
     and `eq/t-m3/citing-set-selftest/cases/c1/made-before-refusal` exists.
   Effects stay inside the scratch copy (`inside()` containment), so no harm channel; the parenthetical
   ("the apply-time re-check and the Git pins still refuse the shape") is accurate and matches round-31
   m3/m3b (`.ufo/waves/round-31/a2-w2/MutRunnerGuards.md:39,66`). Correction: "refusal-equivalent".

3. **"so the spec also keeps the `h0-control` benign control" (LOW, misattribution).** SCORECARD.md:1036-1037.
   The P6 spec (`scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json`) holds only case
   `h6`; `h0-control` is injected by the harness for every spec (`scripts/citing_set_hostile_selftest.py:187`,
   check `:220`) and a spec may not even name it (`:137`). The control is pre-existing round-31 wave-2
   harness behaviour, not something round 32 kept in the spec. Correction: "the harness still adds the
   `h0-control` benign control to every spec". (Whether that control offsets reason-text trust is the held
   line KakeR31.CriticC1Counter; I stopped there and did not assess it.)

## Sentences checked and accurate

- Base a0b0dff; C1 = round-31 routed item 2, mutant m3 (`corpus/lessons/round-31-verifier-spotcheck.md:168-169`).
- "stagnation nudge applies as in rounds 28 to 31": SCORECARD.md:580, 618, 679, 822.
- Before `killed` 0, "round-31 MutRunnerGuards saw exit 0": MutRunnerGuards.md:39 (m3 exit 0, 5/5, SURVIVED);
  receipt c1-before-a0b0dff.json `killed` 0, `guard_ok` true.
- Killed by the committed hostile selftest, unmutated runner passes, benign clean: c1-after-2f2f12d.json and my
  tip rerun agree (mutant exit 1, only P6 false; pristine exit 0, 6/6; benign exit 0, 45 cases, 0 failed;
  runner sha256 7c95a18e… unchanged since base). The benign run uses the pristine runner only
  (`c1_m3_probe.py:87`), which is what the sentence says. 45 = fixture dirs under `scripts/fixtures/citing-set/`.
- "for that one case": `reason_contains` appears in exactly one spec case (P6 `h6`, hostile.json:23).
- "m3d/m3f stay unprobed alone; not claimed": matches MutRunnerGuards.md:68,70 and runner docstring.
  Note routed item 2 named both "Git pins and mutant m3"; C1 repairs only the m3 half, disclosed here.
- "the same shape as routed item 1": not assessed — it is the reason-text-trust line under hold.

## Adjacent (not C1 wording, cleanup)

- `scripts/citing_set_selftest.py:83` (unchanged this round) still says "The hostile specs probe five routed
  shapes (N1, N2, N3, N5, N6)"; there are six specs at 285abca (P6, gap "m3"). Stale count.

## Commands (all exit 0)

- `git show 285abca:SCORECARD.md | sed -n '1009,1200p'`; `git log --format='%H %cI %aI %s' a0b0dff..285abca`;
  `git show --stat` of 5b32cc7, 2f2f12d, 285abca; `git diff a0b0dff 285abca -- scripts/citing_set_hostile_selftest.py`;
  `git grep -n reason_contains 285abca -- scripts/fixtures`.
- `TMPDIR=<sandbox>/tmp python3 -B .ufo/waves/round-32/c1_m3_probe.py --rev 285abca…` -> exit 0; killed 1,
  guard_ok true. Output: /fast/scratch/hyaku/kake-r32/w1/CriticC1Wording/c1-tip-285abca.json
- Equivalence probe (export via `git archive 285abca`, m3 by the probe's own regex): pristine and m3 runner
  `--fixtures eq/fx --timeout 20` -> both exit 1. Outputs: /fast/scratch/hyaku/kake-r32/w1/CriticC1Wording/eq/
  {pristine.json,m3.json,t-m3/}.

Not verified: actual run order of the counters relative to the declaration commit; m3b/m3e kill by P6.
No tools installed. No lane file written except this report.
