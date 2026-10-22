# CriticC1Wording — does C1 text claim more than the probes show? (round 31, attempt 2, wave 2)

Seat: KakeR31a2.CriticC1Wording (critic, leaf). Axis: operability. Reviewed at lane tip 92235a0 (C1 content same as c88b97e/fde133a).
Sandbox: /fast/scratch/hyaku/kake-r31/a2-w2/CriticC1Wording/ (clone, TMPDIR=./tmp). No installs. No network. Lane untouched except this report.

## Result
No sentence says the runner is safe in general. Eight sentences name a guard that no probe exercises, or claim more than the code does. Two of them are false on a reproducible counterexample (W1, W5 below). A sandbox mutant runner with six named guards removed still scores C1 5/5 with K1 holding, and the hostile selftest exits 0 against it.

## Commands (exit codes)
- `git clone -q <lane> clone && git -C clone checkout -q 92235a0` → 0
- `python3 -B wording_probes.py clone clone/scripts/citing_set_selftest.py w-real` → 0 (harness; per-probe runner exits below). Output: w-real.json
- Mutant commit 7dbaabff930c62aa69fae48e3426a01f54452044 on sandbox branch `critic-mutant`, runner sha256 f60b4da0…d31c; diff in mutant.diff (2+/12-). Removed: the setup `--git-dir`/`--work-tree` pinning, the setup `GIT_CEILING_DIRECTORIES`, the gate-environment `GIT_DIR`/`GIT_WORK_TREE` drop and its `GIT_CEILING_DIRECTORIES`, the mkdir/fifo `.git` path refusal, `O_NOCTTY`, and the `git_commit` check that `.git` is a directory.
  - `python3 -B clone/scripts/citing_set_hostile_selftest.py --root clone --tmpdir hs-mutant` → **0**, P1–P5 all passed (hs-mutant.json)
  - `python3 -B .ufo/waves/round-31/c1_sandbox_probes.py --root . --revision 7dbaabf… --scratch counter-mutant` → **0**, "C1 5/5 K1=hold", counterSha256 4707cebf…6d1a (c1-mutant.json)
  - `python3 -B wording_probes.py … w-mutant` → 0 (w-mutant.json)

Wording probes against the landed runner (runner sha256 5371530d…ce6c), then against the mutant:
| Probe | Landed runner | Mutant |
|---|---|---|
| W1 symlink `.h5` pointing at the benign case | **exit 0, case list ["00-benign"]: skipped silently** | same |
| W2/W3/W4 argv `--json` / `-h` / `--he` | exit 1, "argv refused" | same |
| W5 argv `--root=/elsewhere` | exit 1, gate **exit 64** (`StoreOnce` repeat refusal, scripts/citing_set.py:800-816; the runner already passes `--root` at citing_set_selftest.py:560) | same |
| W6 `sub/.git` file | refused, "sub/.git" | same |
| W7 setup mkdir `sub/.git` | refused | **not refused** (exit 0) |
| W8 expected.json is a directory | refused, "must be a regular file" | same |
| W9 symlink to a file | refused | same |
| W10 git_init and git_commit, tmpdir inside victim | passes, victim unchanged | passes, victim unchanged |
| W11 argv `--revision HEAD` with no git_init, tmpdir inside victim | gate exit 2, `revision_not_found` | gate exit 2, `root_not_repository_top_level` (the gate found the victim repository) |

W11 shows that the gate's ceiling does work, but exit-code matching cannot see the difference. W10 shows that once git_init is required first, pinning is defence in depth that no probe can observe.

## Sentences, with narrower wording
1. Commit c88b97e subject: "git_init before git_commit with pinned git dir and ceiling … symlinked case fails". The pinning and both ceilings are unexercised (the mutant scores 5/5), and W1 is a counterexample to "symlinked case fails". Narrower: "git_init before git_commit (git-dir pinning and ceilings added, not probed) … a symlinked case not named with a leading dot fails". History stays; record the correction in the SCORECARD scope list. This sentence also breaches the new QUALITY rule at corpus/QUALITY.md:493-499 (each claimed refusal has a spec).
2. scripts/citing_set_selftest.py:58-62 (git_commit: `GIT_CEILING_DIRECTORIES` and `--git-dir`/`--work-tree`). The text describes the code correctly, but no probe reaches it. Narrower: append "(defence in depth; no hostile spec exercises it)".
3. scripts/citing_set_selftest.py:75-76: "so a FIFO cannot block the run". This is too broad: SKILL.md:869-871 itself records that a setup fifo on `.gitattributes` blocks `git add`. Narrower: "so a FIFO at expected.json cannot block that read". `O_NOCTTY` is unprobed (the mutant drops it and survives).
4. scripts/citing_set_selftest.py:77-78: "a symlink in the fixture directory (a symlinked case is a failed case, never a silent skip)". False for dot-named entries (W1; the cause is the `not path.name.startswith(".")` filter at :681). Narrower: "a symlink in the fixture directory whose name does not start with '.' …; dot-named entries are still skipped".
5. SKILL.md:851: "a symlink in the fixture directory (a failed case, never a skip)". Same counterexample and same narrower wording as item 4. SCORECARD.md:939-943 says the dot-named skip is "named in SKILL.md 'Citing-set runner containment — round 31'"; it is not: the section's open list (SKILL.md:863-871) never mentions it, and :851 says the opposite. Add it to the open list.
6. SKILL.md:841-843: "a case could still pass `--root=/elsewhere`; that path is read only". False (W5): a second `--root`, `--population` or `--ledger` is a gate usage error, exit 64. Only `--revision` takes a free value. Narrower: "Option values are not restricted: a case may pass any `--revision` value; a second `--root`, `--population` or `--ledger` is a gate usage error (exit 64)". SCORECARD.md:941 ("option values in `argv` are not restricted") should be narrowed the same way. This error understates the guard rather than overstating it.
7. SKILL.md:840-841: "`--selftest`, `--self`, `--json`, `-h` are refused". The committed specs (P1 hostile.json) carry only `--selftest` and `--self`. W2 and W3 hold in the critic sandbox. Narrower: "`--selftest` and `--self` are refused (P1); `--json` and `-h` are refused by the same rule but have no spec".
8. SKILL.md:844-848 (".git at any depth"; setup Git commands pinned; ceilings for setup and gate). Every P2 spec puts `.git` only at the case root (citing_set_hostile_selftest.py build_case: `target / ".git"`), and P3 is refused while loading, before any Git command runs. Narrower: "a case directory holding an entry named .git (probed at the case root; deeper entries and setup paths naming .git are refused but have no spec); setup Git pinning and both ceilings are defence in depth with no probe". W6 holds; W7 is refused only by a guard that the mutant removed without detection.
9. Minor. corpus/lessons/round-31.md:68 (Fix column): "Each refusal now has a hostile spec". The runner now has refusals with no spec (setup `.git` paths, non-FIFO non-regular files, `git_commit` without `.git`). Narrower: "Each of the five routed shapes now has a hostile spec". The same applies to the "each refusal" phrase at SCORECARD.md:833.
10. Minor. scripts/citing_set_hostile_selftest.py:4-7: "must refuse fixture shapes that would run foreign code, touch a Git repository outside the case copy, hang, or vanish from the count". This reads as coverage of whole classes, but W1 vanishes and the SKILL.md:869 fifo hangs. Narrower: "checks that the runner refuses the hostile shapes in the committed specs (the five routed by round 30)".

These hold as written: PROVINCE.md:121-123 ("containment for five hostile fixture shapes"); SCORECARD.md:833, 836-857, 928 and 939 ("C1 covers the five routed shapes … nothing more"); lesson :10-15; LOG.md:1300-1305.

## Smallest safe correction
Wording only: apply items 3-8 to the runner docstring and the SKILL section, add the dot-named skip and "pinning and ceilings unprobed" to the SKILL open list, and fix the SCORECARD.md:939-943 cross-reference and :941. The C1 5/5 measurement stands; the mutant result shows its scope, not a defect in it. Optional, not claimed this round: specs for a dot-named symlinked case, `sub/.git`, a setup mkdir of `.git`, and a gate `--revision` run with the tmpdir inside a victim that checks the gate's finding id rather than only its exit code.

## Not verified
- I did not mutate the argv allowlist or the depth walk one guard at a time. That `--json`/`-h` and depth are unprobed follows from the spec contents, not from a surviving mutant.
- I did not re-run C2 or K1 separately; K1 held inside the mutant counter run.
- The wave-1 bare-repository route (SCORECARD.md:947-950) is a held item, and I did not touch it.

Evidence (sandbox, sha256): wording_probes.py 6bd29380…0a29; mutant.diff a6148bc4…ea43; w-real.json 1bd5bea0…076df; w-mutant.json f84c8300…73df; hs-mutant.json b96b5509…05c1; c1-mutant.json d30692fa…cc05. All are under /fast/scratch/hyaku/kake-r31/a2-w2/CriticC1Wording/.
