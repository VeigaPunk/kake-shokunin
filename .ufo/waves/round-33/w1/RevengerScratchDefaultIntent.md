# w1 RevengerScratchDefaultIntent — fixed default scratch path in `scripts/citing_set_selftest.py`

Item: why a fixed default scratch path (~line 133) instead of per-run; intentional? would a per-run default break a documented use?
Revision measured: `bc6c4a8d435473f3c30903210be30d9d6e3ef750` (own sandbox clone; lane working tree not read as evidence). Sandbox: `/fast/scratch/hyaku/kake-r33/w1/RevengerScratchDefaultIntent/` (TMPDIR set to its `tmp/`). No tool installs. No subagents.

## Verdict

- `DEFAULT_TMPDIR = "/fast/scratch/hyaku/kake-r27"` sits at `scripts/citing_set_selftest.py:136` at this revision (line 133 at the round-32 tip `285abcad` the lessons cite; three docstring lines inserted above it since). `git log -L 132,140` shows the hunk originates **only** in `ac46a74` (2026-10-21, "round-27: source-ground grouped claim and freeze…"), the file's birth commit. It was never modified in any of the 7 commits to the script; the fixed default is original design, not later drift.
- Intentional parts, with evidence: the value is the round-27 wave scratch root — round-27's committed contract pins it (`.ufo/waves/round-27/contract.json:30`: "Use TMPDIR=/fast/scratch/hyaku/kake-r27"), and the runner itself was authored in the `writer-selftest` worktree under that root (`.ufo/waves/round-27/start-evidence.json:6`). It follows the operator `/fast/scratch/hyaku/` convention, pointedly not `/tmp`, which corpus rules disqualify as evidence scratch (`corpus/lessons/round-22-verifier-spotcheck.md:163-165` "tmpfs paths are not evidence"; `corpus/lessons/round-25.md:177-182`). The location is also documented behavior: `SKILL.md:616` gate row says "selftest scratch below `/fast/scratch/hyaku/kake-r27`". Leftover inspection is *possible* (no post-run cleanup: the only `rmtree` is per-case before copy, `scripts/citing_set_selftest.py:511-513`; case copies and `HOME` persist under `<scratch>/citing-set-selftest/`), but no lesson or SKILL line documents inspecting leftovers as a use [INFERENCE: convenience only].
- "Ceiling path stability" is **not** a reason: `GIT_CEILING_DIRECTORIES` is derived per run, not from the constant — setup git gets the case copy's parent (`scripts/citing_set_selftest.py:442-446`), the gate subprocess gets `<resolved --tmpdir>/citing-set-selftest/cases` (`:703-714`), matching `SKILL.md:847-848`. The only value-sensitivity is `os.pathsep` in the resolved path, refused because Git colon-splits the variable with no escape (`:705-709`; `SKILL.md:885-887`; `.ufo/waves/round-31/a2-w2/CriticGitPins.md:11` "the default tmpdir has no colon"). A per-run `tempfile.mkdtemp()` default yields an equally valid colon-free ceiling on this host.
- The lane itself already classifies the fixed default as a pre-existing harm, not a feature: round-32 routed defect 6 — concurrent `citing_set.py --selftest` runs collide on it, 4/4 false failures at base and tip (`corpus/lessons/round-32-verifier-spotcheck.md:136-141`; `corpus/lessons/round-32.md:67`; root cause in `.ufo/waves/round-32/w1/ExecBenignSuiteTip.md:24,33,37`: fixed per-case paths racing on rmtree/copytree, plus the gate delegation cannot forward `--tmpdir` — the gate parser has no `--tmpdir` option at all, verified by grep over `scripts/citing_set.py`; its `run_selftest` at `:834-873` forwards unknown argv but parse rejects the option upstream). A per-run default would *repair* that documented defect.

## Documented uses a per-run default would change

1. `SKILL.md:616` (citing-set gate row): "selftest scratch below `/fast/scratch/hyaku/kake-r27`, no network, no live Git/index/jj writes" — the durable containment statement becomes false; the line must be updated with any default change. This is the only durable corpus text documenting the default location.
2. `.ufo/waves/round-27/contract.json:30` ("Use TMPDIR=/fast/scratch/hyaku/kake-r27") — frozen round-27 contract would no longer describe the runner; historical artifact, annotate rather than rewrite.
3. Predictable leftover path for post-run inspection (`<scratch>/citing-set-selftest/cases/<case>`, `…/home`) — lost with a per-run default, but nowhere documented as a use, and out-of-repo scratch is already ruled non-evidence (round-22 spotcheck :163-165) [INFERENCE that this is convenience only].

## Documented uses a per-run default would NOT break

- `SKILL.md:806`: the documented self-test invocation passes `--tmpdir <dir>` explicitly.
- Round-30/31/33 counters: all pass explicit `--tmpdir` — `.ufo/waves/round-30/w1/ReviewC1Before.md:59` ("The counter passes --tmpdir, so this does not affect C1"); `.ufo/waves/round-33/c1_code_probe.py:145,150`; hostile selftest requires `--tmpdir` (`scripts/citing_set_hostile_selftest.py:229`, explicit at `:198`).
- `SKILL.md:636` (`git_name_selftest.py … --tmpdir /fast/scratch/hyaku/kake-r27`): explicit flag, unaffected; confirms the path is the round-27 convention.
- Hostile `tmpdir_in_victim` specs (P3/P6): probe ceiling behavior relative to whatever tmpdir is given; independent of the default value.
- Would be *fixed*, not broken: concurrent `citing_set.py --selftest` false failures (routed defect 6) and cross-run `HOME` residue under `<scratch>/citing-set-selftest/home` (`scripts/citing_set_selftest.py:205-216`).

## Commands and exits (all in sandbox clone at bc6c4a8d; GIT_* env unset per bounds)

1. `git clone -q <lane> clone && git -C clone checkout -q bc6c4a8d…` → HEAD echo `bc6c4a8d…` — exit 0.
2. `git blame -L 115,160 -- scripts/citing_set_selftest.py` → line 136 `DEFAULT_TMPDIR` last touched by `ac46a74` (2026-10-21) — exit 0.
3. `git log --follow --pretty='%h %ad %s' -- scripts/citing_set_selftest.py` → 7 commits `ac46a74`…`df31d30`; birth `ac46a74` — exit 0.
4. `git log -L 132,140:scripts/citing_set_selftest.py` → single commit `ac46a74` (new-file hunk) — exit 0.
5. `git grep -n -E 'kake-r27|DEFAULT_TMPDIR|--tmpdir' -- scripts SKILL.md .ufo/waves/round-33 corpus/knowledge` → anchors cited above — exit 0.
6. `git grep -n 'kake-r27' | wc -l` → 383 hits, all under `.ufo/waves/round-27` except `SKILL.md:616,636`, the runner `:136`, and wave-28/30/31/32 receipts that *quote* it — exit 0. No fixture, expected.json or hostile spec embeds the literal path.
7. `git grep -n -E 'def child_env|GIT_CEILING_DIRECTORIES|shutil.rmtree|os.pathsep in str|cases_root = '` → runner lines 205/215/442-446/512/703-714 — exit 0.
8. `git grep -n -E 'selftest|tmpdir' -- scripts/citing_set.py` → no `--tmpdir` option in the gate parser; delegation at `:830,834-873,883-884` — exit 0.

## Not verified

- Did not execute the selftest or any gate/counter (read-only item; no run receipts produced).
- Whether the round-33 C1 repair (L1 in flight) changes this default is out of scope here; my lines refer to `bc6c4a8d`.
- Did not check whether `tempfile.mkdtemp()` output could ever contain `os.pathsep` on other platforms (Linux `TMPDIR` semantics only).
