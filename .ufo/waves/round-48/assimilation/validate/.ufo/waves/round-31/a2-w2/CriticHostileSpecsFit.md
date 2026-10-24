# CriticHostileSpecsFit — do the five hostile specs match the five routed gaps? (round 31, attempt 2, wave 2)

Seat: KakeR31a2.CriticHostileSpecsFit (critic, leaf). Axis judged: operability.
Reviewed at fde133ab48086bb9a06911b4ab045e2ad9086347 in my sandbox clone. `git diff --stat fde133a 92235a0 -- scripts` is empty, so the verdict also holds at 92235a0.
Runner `scripts/citing_set_selftest.py` sha256 5371530d93ecb218b4607fb37de810fe7b7b2db869c65c8b65988b2f04c0ce6c.
Routed text: `corpus/lessons/round-30-verifier-spotcheck.md:151-162` (findings N1-N6) and `:250-261` (routed fixes).

## Verdict

All five specs exercise the routed shape as worded, and each fails against the base runner. Before the fix, P1's canary was written, the P2 and P3 victim repositories gained commits, P4 timed out and P5's case vanished. The repaired runner refuses all five.

The specs only prove that at least one guard refuses each shape. Mutation shows that four of the routed or claimed guards can be deleted while the hostile selftest still exits 0:
- the N3 pins (`--git-dir`/`--work-tree` and `GIT_CEILING_DIRECTORIES` on setup Git commands);
- the N2/N3 "git_init before git_commit" ordering check;
- the N5 regular-file check;
- the gate-side `GIT_CEILING_DIRECTORIES`.

Two narrower weakenings also pass: dropping the N1 allowlist breadth, and dropping the N2 "at any depth" walk.

The statement "each refusal has a committed hostile spec" (`corpus/lessons/round-31.md:10-13`) is therefore overstated for these guards. This is advisory: no harm is realised today, because each untested guard sits behind another one that is tested.

## Table

| gap | spec | fit | missing variant |
|---|---|---|---|
| N1 argv reaches `--selftest` (`:151-155`; fix `:251-252` "refuse `--selftest`, and any argv outside an allowlist") | P1: h1a `--selftest`, h1b `--self`, h1c `--revision HEAD --selftest`; planted scripts with canary | Exercises the gap as worded. Removing `argv_refusal` (MA) is detected: the canary is written in all three cases. | The allowlist half of the fix is untested. Mutant MA2 refuses only tokens that are prefixes of `selftest` and still passes P1. Under MA2, `--json` reaches the gate and the case passes as clean, while `--help` and `-h` fail only by accident (the gate's stdout is not JSON). No case uses `--json`, `--help`, `-h` or `--selftest=x`. Harmless today: the gate has no other side-effecting option (`scripts/citing_set.py:821-830`). |
| N2 fixture `.git` accepted by setup ops other than git_init (`:156-157`; fix `:253-254`) | P2: top-level `.git` pointer file with h2a `[git_commit]` and h2b `[mkdir extra]` | Exercises the gap as worded for one `.git` shape. Removing `dot_git_entry` (MB) is detected, but only through h2b. h2a is triple-guarded: under MB it is still refused by the ordering check (`case.json setup op 'git_commit' needs an earlier 'git_init'`), so h2a never isolates N2. | Three variants are missing. **(a) Nested `.git`:** `sub/.git` is untested, although the runner docstring (`:72`) and SKILL.md (`:844`) both say "at any depth". Mutant MB2 checks only the top-level `.git` and still passes P2. Under MB2, the variant `v1-nested-dotgit` runs and passes as a normal case. **(b) `.git` as a directory or symlink, not a pointer file:** untested. The repaired runner refuses the directory form (`v2-dotgit-dir`); with MB it runs as a normal case. **(c) No `case.json`, a fifo-only setup, or an argv-only `--revision` with a `.git` present:** untested, but the `.git` guard runs before any setup is loaded (`run_case` `:524-527`), so this is structurally covered. |
| N3 git_commit without git_init discovers an enclosing repository (`:158-160`; fix `:255` "Pin `GIT_CEILING_DIRECTORIES` and `--git-dir`/`--work-tree`") | P3: h3 `[git_commit]` with no init, `--tmpdir` inside the victim repository | Exercises the gap's shape, but **not the routed fix**. h3 is refused at parse time by the ordering check (`:351-352`) before any Git command runs. Four mutants still pass P3: pins removed (MC); ordering check removed (MD), where the is-directory check `:476-477` refuses instead; ordering and is-directory checks removed (ME), where the pins make `git add` fail with 128; and the gate-side ceiling `:694` removed (MK). Only removing all three layers (MF) lets the victim gain a commit. | The pins are never isolated, and no fixture shape can isolate them while the earlier guards stand. Gate-side discovery is untested: argv `["--revision","HEAD"]`, no git_init, tmpdir inside the victim (variant `v3-revision-no-init`). With the ceiling, the gate reports `revision_not_found`. Without it (MK), the gate reaches the victim repository and reports `root_not_repository_top_level`. Both are read-only (victim HEAD and commit count unchanged) and both count as failed cases, so the hostile selftest's only check (refused or not, `citing_set_hostile_selftest.py:204-205`) cannot tell them apart. |
| N5 `expected.json` read with no symlink, file-type or size guard (`:161`; fix `:256-257` `O_NOFOLLOW`, regular-file check, size cap) | P4: h4a symlink to a matching file outside the case, h4b padded past 1 MiB, h4c FIFO | Exercises the symlink and size gaps as worded. Removing `O_NOFOLLOW` (MG) is caught by h4a. Removing both size checks (MI) is caught by h4b. The regular-file check is **not** isolated: with it removed (MH), h4c is still refused because the non-blocking FIFO read returns empty bytes, which fails as invalid JSON. | `expected.json` as a directory is the missing variant. Under MH it crashes the whole runner with `IsADirectoryError` (a traceback and no JSON summary, so every other case's result is lost). The repaired runner refuses it cleanly with "expected.json must be a regular file". Removing only one of the two size checks is redundant layering, not a gap. |
| N6 symlinked case skipped silently (`:162`; fix `:258` "count a symlinked case as a failure") | P5: h5 symlink to the benign case, default `--min-cases 0` | Exercises the gap as worded. Removing the `run_case` symlink refusal (MJ) is detected (exit 0, h5 not refused). A dangling symlink (`v7-dangling-symlink`) is also refused. | A dot-named symlinked case is untested and **still skipped silently by the repaired runner**. `fixtures/.v6-hidden-symlink -> 00-benign` is absent from both `caseNames` and failures because enumeration drops names starting with "." (`citing_set_selftest.py:679-683`). This contradicts SKILL.md `:851` and runner docstring `:77-78` ("a symlink in the fixture directory ... never a skip"). Low severity: dot-named directories are skipped by design too. |

## Smallest safe corrections (for the L1; none applied)

1. **N3:** add a direct check, either in `citing_set_hostile_selftest.py` or as a unit assertion that imports the runner, that `git_command(w)` names `--git-dir=<w>/.git` and `--work-tree=<w>` and that `git_env(w)` sets the ceiling. Add a P3b spec with argv `--revision HEAD` and tmpdir in the victim, and let specs assert the failure reason or finding (`revision_not_found`). Otherwise, reword `round-31.md:10-13` and SKILL `:845-848` to say the pins are defence in depth with no isolating spec.
2. **N2:** add a P2 case with `sub/.git` and one with `.git` as a directory, and drop h2a or label it as triple-guarded.
3. **N5:** add `"directory"` to `EXPECTED_SHAPES` (`citing_set_hostile_selftest.py:77`) as case h4d.
4. **N1:** add cases for `--json` and `-h`, or narrow the docs to "refuses `--selftest` prefixes".
5. **N6:** refuse dot-named symlinks in enumeration, or narrow SKILL `:851` and docstring `:77-78` to "non-dot entries".

## Commands run (sandbox /fast/scratch/hyaku/kake-r31/a2-w2/CriticHostileSpecsFit, TMPDIR inside it)

- `git clone -q <lane> clone && git -C clone checkout -q fde133a…` → exit 0.
- Mutants: copies of the repaired runner with one guard edited, in `mut/`. sha256 prefixes: MA c994f11f, MA2 7663941c, MB 8a5b4815, MB2 a9e2286e, MC 822d7b25, MD 29aa1a23, ME f62c207f, MF d7a99189, MG 9b2f6c72, MH b96df1ec, MI 89c3cabe, MJ 6208e5f1, MK e074761e. The base runner `git show f1ffb81:scripts/citing_set_selftest.py` is `mut/BASE.py`.
- `python3 -B clone/scripts/citing_set_hostile_selftest.py --root clone --tmpdir run/<M> --runner <runner>`, one run per runner, output in `out/<M>.json`. Exit is 0 exactly when `passed` is true.

| Runner | Result |
|---|---|
| repaired | passed, exit 0 (also recorded) |
| BASE | P1-P5 all fail |
| MA | P1 fails (canary written) |
| MB | P2 fails (h2b only) |
| MF | P3 fails (victim changed) |
| MG | P4 fails (h4a) |
| MI | P4 fails (h4b) |
| MJ | P5 fails |
| MC, MD, ME, MH, MK, MA2, MB2 | **passed (all five specs green)** |

The MA2 and MB2 exits (0) were recorded directly. The exit files for BASE, MA, MB, MF, MG, MI and MJ were lost when the batch was backgrounded; their exit 1 is inferred from `passed` false.
- Variant fixtures (`var/fixA`, `var/fixB`, `var/fixC`), run with `python3 -B <runner> --root clone --fixtures var/fix<X> --tmpdir … --timeout 20`, exit 1 each:

| Fixture | Runner | Result |
|---|---|---|
| fixA | repaired | v1, v2, v5, v7 refused; the hidden symlink is absent |
| fixA | MB | v1 and v2 pass as normal cases |
| fixA | MB2 | v1 passes as a normal case |
| fixA | MH | traceback `IsADirectoryError`, no JSON |
| fixB | repaired | `revision_not_found` |
| fixB | MK | `root_not_repository_top_level`; victim HEAD and count unchanged |
| fixC | repaired | `-h`, `--help`, `--json` refused |
| fixC | MA2 | `--json` case passes; `-h` and `--help` fail as non-JSON |

## Not verified

- I did not run `c1_sandbox_probes.py`; I read only its docstring, whose P1-P5 shapes match the specs.
- I did not attack containment beyond the five gaps, such as `--root=/elsewhere` (SKILL `:841-843`, not routed), the `root` key or the FIFO setup op.
- I did not check that each spec's failure reason is the intended one. The hostile selftest does not record intent.

No network, no installs, no lane mutation. The only lane write is this report.
