# LabratK12Contract

Seat: LabratK12Contract (read-only labrat probe of C2 route K12).
Scope: does the CURRENT `scripts/id_resolver.py` already exit 2 when `corpus/SOURCES.md` is missing or unreadable,
so that K12's "out-of-lane registry -> exit 2" is consistent with the tool's existing contract?
Method: the lane tool was copied out read-only into scratch (no lane mutation, no lane git/jj operation) and run
against purpose-built fixtures. Base revision of the tool is unchanged at HEAD: `git ls-tree fd6303ce… scripts/id_resolver.py`
= blob `c1c47a41573a271e9dd9fbafbc28a482d4979e4a` = `git rev-parse HEAD:scripts/id_resolver.py` = the same blob, and the
worktree file hashes to `2c1b4970a652023a883a414620c07cf393f7c4b28b87053564a45302428e663a` = the copied tool
(`git diff --stat fd6303ce… HEAD -- scripts/id_resolver.py` and `git diff --stat HEAD -- scripts/id_resolver.py` both empty).
The tool snapshot used is therefore identical to the base-revision tool the counter measures.

Scratch (deleted before this report was written; receipts copied into `.ufo/waves/round-59/w1/LabratK12Contract.files/`):
`/fast/scratch/hyaku/kake-r59/LabratK12Contract/`. Fixtures were plain directories under scratch (no git repo, so the
"assert toplevel before first commit" rule did not apply to them); the revision-mode probe used a fixture repo created with
`git init -q`, whose `git rev-parse --show-toplevel` was asserted to equal the fixture dir before its single commit, committed
with `-c user.name=selftest -c user.email=selftest@local -c commit.gpgsign=false`. No pacman, no `uv tool install`, no PATH
change, no host service touched — no tool was installed or upgraded by this seat.

## RUNS:

Fixture shape for every row: fleet root `…/fleet`, lane `…/fleet/kake-shokunin`, `corpus/knowledge/ok.md` = `Cites S900 and S901.`,
registry content `## Registry` + header + rows for `S900` and `S901`. Invocation:
`python3 -B tool_current.py --root <lane> --fleet <fleet>` (worktree mode), plus a separate `--revision <head>` probe.
Tool's own built-in selftest on the same snapshot: `selftest: 59/59`, exit 0.

| # | Fixture | `corpus/SOURCES.md` state | exit | stdout/stderr |
| --- | --- | --- | --- | --- |
| R1 | registry missing | absent | **2** | `id_resolver: unevaluable: registry absent: corpus/SOURCES.md` |
| R2 | registry is a directory | dir `corpus/SOURCES.md/` (with a subdir) | **2** | `id_resolver: unevaluable: registry absent: corpus/SOURCES.md` |
| R3 | registry is a broken symlink | symlink -> `<lane>/corpus/nope.md` (target absent) | **2** | `id_resolver: unevaluable: registry absent: corpus/SOURCES.md` |
| R4 | registry symlinked to an in-lane file | symlink -> `./SOURCES-real.md` (inside the lane) | **0** | `ids_cited=2 ids_resolved=2 dangling=0 owned_elsewhere=0 unowned=0` |
| R5 | registry symlinked out of the lane | symlink -> `<scratch>/outside/SOURCES.md` (outside lane and outside fleet) | **0** | `ids_cited=2 ids_resolved=2 dangling=0 owned_elsewhere=0 unowned=0` |
| R6 | registry present but unreadable (extra) | regular file, mode `000` | **2** | `id_resolver: unevaluable: registry unreadable: [Errno 13] Permission denied: '…/corpus/SOURCES.md'` |

R5 is the K12 shape. The counter's own K12 fixture puts the outside registry at `<scratch>/outside/SOURCES.md` and the lane
registry symlinked to it; R5 reproduces that geometry, and the base control receipt for C2 records the same outcome from the
gate's own run: `K12_registry_outside_lane_is_unevaluable FAIL  exit=0 ids_cited=2 ids_resolved=2 dangling=0`.
R5's `ids_cited=2 ids_resolved=2` is reproduced because the outside registry holds both `S900` and `S901`, which the entry cites.

Revision-mode probe (`--revision <head>`, fixture repo committed; same three registry shapes committed):

| # | Fixture at the revision | exit | stdout |
| --- | --- | --- | --- |
| R7 | committed symlink -> outside-the-lane `SOURCES.md` | **1** | `DANGLING S900 cited-by=corpus/knowledge/ok.md owners=- url-match=-` / `DANGLING S901 …` / `ids_cited=2 ids_resolved=0 dangling=2 owned_elsewhere=0 unowned=2` |
| R8 | committed symlink -> in-lane `SOURCES-real.md` | **1** | same two DANGLING lines, `ids_cited=2 ids_resolved=0 dangling=2` |
| R9 | committed regular registry (control) | **1** | `DANGLING S901 …` / `ids_cited=2 ids_resolved=1 dangling=1` |

R8 is the important negative: at a revision, an in-lane symlinked registry is read as its **target string**, so the registry
parses as empty and *every* citation dangles (2 cited, 0 resolved) — the same class as route K11 for knowledge symlinks,
which the counter already covers for `corpus/knowledge`. The registry analogue is not in the counter's case list.

Fixture driver and raw JSON receipts: `.ufo/waves/round-59/w1/LabratK12Contract.files/run_fixtures.py`,
`run_revision_probe.py`, `results.json`, `results_revision.json`, `tool_current.py` (the exact tool snapshot run).

## READING:

The hypothesis is **half true, and the false half is the operative one**.

1. "The current tool already exits 2 when `corpus/SOURCES.md` is missing or unreadable" — **confirmed** (R1, R2, R3, R6 all exit 2).
   The mechanism is `lane_registry()` in `scripts/id_resolver.py`: `os.path.isfile(path)` is False for an absent path, a
   directory, and a dangling symlink, so all three return `(None, "registry absent: corpus/SOURCES.md")` and `evaluate()`
   maps that to `_err(...)` -> status 2; a present-but-unreadable file raises `OSError` -> `"registry unreadable: …"` -> status 2.
   The tool's own docstring (lines 25–26) already lists "registry absent" among the exit-2 causes, and the built-in selftest
   case `case_missing_registry` asserts exactly `status == 2 and "registry" in error` (selftest passes 59/59 on this snapshot).
   So the *exit code and the "registry" error family* for a registry the tool cannot use as a file are already contractual.

2. "therefore K12's 'out-of-lane registry -> exit 2' is consistent with its existing contract" — **not established by that
   precedent, and false for the tool as it stands**. R5 shows the current tool exits **0 with a green summary**
   (`ids_cited=2 ids_resolved=2 dangling=0`) when `corpus/SOURCES.md` is a symlink to a file outside the lane: the outside
   registry is read and its ids are trusted as resolved. The counter's base receipt confirms the same (`K12 FAIL exit=0 … dangling=0`).
   The reason is structural: the `inside()` guard at `scripts/id_resolver.py:196–198` (realpath containment, added for
   knowledge symlinks) is applied only inside `knowledge_bodies()`; `lane_registry()` at lines 166–171 has **no** containment
   check, so `os.path.isfile()` follows the symlink and the outside file is opened.
   Consequently the exit-2 precedent is *adjacent* but not the same route: an out-of-lane symlink is not "absent" and not
   "unreadable" — it is **present and readable but untrustworthy**. The tool must therefore refuse it explicitly, and it
   must refuse it with status 2 (unevaluable), which is the only status that matches the counter's K12 expectation
   (`check("K12_registry_outside_lane_is_unevaluable", …, 2, [], [r"^ids_cited=\d+ ids_resolved=\d+ dangling=0\b"])`).
   Exit 2 is the right choice under the existing contract because the tool's contract reserves exit 2 for "the evidence
   needed to evaluate was not obtained" (revision unresolved, fleet root absent, registry absent, no knowledge file) — a
   registry the lane does not own belongs to that family, and exit 0/1 would mean the lane evaluated citations against
   evidence it does not hold.

3. The contrast that fixes the intended boundary: R4 (symlink to an **in-lane** file) currently exits 0 and resolves both ids.
   That is the shape route K10 already protects in the other direction ("a citation reachable only through an in-lane
   symlinked knowledge directory is read"), and the counter's K12 fixture is silent about the in-lane registry symlink. A fix
   that refuses *all* symlinked registries would therefore risk over-reach; the rule that matches both the counter and the
   tool's existing containment semantics is: **the registry must resolve inside the lane** (realpath containment), so an
   in-lane symlink is read and an out-of-lane symlink is exit 2. [INFERENCE: the counter does not pin the in-lane registry
   symlink case, so this boundary is my reading of the contract text ("a registry symlinked to a file outside the lane"),
   not a tested requirement.]

4. R7/R8 add a second, untested route of the same family: at `--revision`, a **committed** symlinked registry is read as its
   target *string* by `git show <rev>:corpus/SOURCES.md`, so the parsed registry is empty and every citation dangles
   (2 cited, 0 resolved, exit 1) — an in-lane symlink (R8) is broken just as badly as an out-of-lane one (R7). The counter's
   case list has no revision-mode registry-symlink case (K11 covers committed symlinks under `corpus/knowledge` only), so
   this route is currently unmeasured. It is not a false green — it fails loudly — but it is a false-red source: the same
   defect K11 discloses for knowledge symlinks, applied to the registry, and the wave-1 build should consider whether K12's
   fix is expected to cover it.

5. Note on measurement hygiene: no after-state is scored here. All rows are the current/base tool's behaviour on fixtures
   I built; the counter itself was not run by this seat (the base control receipt `controls/base-c2-resolver-cases.txt`,
   seed 59, `13/21 met=False`, exit 1, is the gate's own record and is quoted, not re-measured). The tool's built-in selftest
   was run only to confirm the snapshot is healthy (`59/59`, exit 0) — it does not cover registry symlinks (its only symlink
   case is `case_symlink_out_of_the_lane_is_not_a_citation`, about knowledge).

## VERDICT:

The hypothesis holds only in its first half: the current tool does exit 2 for a missing, directory-shaped, dangling-symlinked
or unreadable registry (R1/R2/R3/R6), so exit 2 is the established unevaluable code for a registry the lane cannot use as a
file — but the current tool exits **0 green** on an out-of-lane registry symlink (R5), because `lane_registry()` has no
realpath containment check, so K12 is a real new behaviour and not a restatement of existing behaviour; the fix must be an
explicit "registry resolves outside the lane -> exit 2" refusal (realpath containment), leaving in-lane registry symlinks
readable, and the counter's K12 expectation of exit 2 is consistent with the tool's reserved-unevaluable contract.
VERDICT: K12 is a genuine gap (current tool exits 0 green on an out-of-lane registry symlink); exit 2 is the contract-consistent
refusal, but it must be added as an explicit containment check rather than inherited from the missing/unreadable-registry precedent.
