# KakeR33.CriticHarmCheck — owned-axis harm, 5777d5af..0a0acfb1

Seat: leaf critic, r33-falsify, judged on operability and freshness. Sandbox clone
/fast/scratch/hyaku/kake-r33/w2/CriticHarmCheck/clone at 0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0;
base worktree .../CriticHarmCheck/base at 5777d5af79cac1ebf9144b348a9d274099e77338. No tools installed.

## Verdict
- Operability: no harm. One documentation line now overstates (finding F1, low).
- Freshness: no harm. No history line was deleted or rewritten, and the S062 pin stays valid.

## Commands (all run in the sandbox; exit codes as observed)
- `git merge-base --is-ancestor 5777d5af 0a0acfb1` gives exit 0. There are five commits, each with one parent (linear; no history rewrite).
- `git diff 5777d5af 0a0acfb1 -- SCORECARD.md | grep -c '^-[^-]'` prints 0 (exit 0). SCORECARD.md is +75/-0, so it is append-only.
- `git diff --stat 5777d5af 0a0acfb1`: 47 files, 4100 insertions, 29 deletions. `git diff ... | grep -c '^-[^-]'` prints 29.
- `git diff --numstat` lines with deletions: only scripts/citing_set_hostile_selftest.py (+23/-6), scripts/citing_set_selftest.py (+87/-22) and P6-commit-before-init/hostile.json (+1/-1). Deletions per commit: bc6c4a8 0, b1752a2 7, e490381 18, 1cf452e 6, 0a0acfb 0.
- Ledgers and docs are all +N/-0: LOG.md +28, corpus/SOURCES.md +2, sitemap-orphan-audit.md +71, QUALITY.md +37, SKILL.md +44, PROVINCE.md +16, corpus/README.md +10. freshness-pins.json is untouched.
- `git diff --stat bc6c4a8 0a0acfb1 -- .ufo/waves/round-33/c1_code_probe.py .ufo/waves/round-33/c2_pin_count.py` is empty, so the frozen counters were not edited after the declaration.
- Runner at tip and at base: `python3 -B scripts/citing_set_selftest.py --root . --tmpdir <sandbox> --json` exits 0 at both, verdict clean, 45 cases, 0 failed.
- Hostile selftest at tip and at base: `python3 -B scripts/citing_set_hostile_selftest.py --root . --tmpdir <sandbox>` exits 0 at both; P1 through P6 all pass, error null.
- Upstream (read-only L1 clone): `git diff --quiet 1fbdb8ed 7fc6aa2f -- render.yaml apps-sdk/Dockerfile apps-sdk/src/server.ts .dockerignore` exits 0, so S062's four files are byte-unchanged at the new pin. The parent of 7fc6aa2f is 1fbdb8ed, and the delta is 12 files with additions only (magga/ plus sitemap.xml +3).

## Deleted-line inventory (29 lines) with judgement
1. hostile.json P6: `"reason_contains": "needs an earlier 'git_init'"` becomes `"reason_code": "setup_commit_before_init"`. The pin moves from message text to a code, as declared for C1. P6 still separates the load-time layer from the apply-time layer (code `setup_commit_without_repo`), and P6 passes at tip. Meaning changes as intended. No harm.
2. hostile selftest: the `CASE_KEYS` line was split to add `reason_code`. The `reason_contains` validator was generalised to both keys; it is now stricter (whitespace-only strings are refused). Two docstring lines were reflowed to add "and its reason_code". The spec-directory listing that silently skipped symlinked or non-directory entries now exits 2 and names them. These are additive or stricter, with no lost check. Side note: no hostile spec at tip uses `reason_contains` any more (`git grep -l reason_contains HEAD -- scripts/fixtures/citing-set-hostile/` finds nothing). The key is supported but no longer exercised.
3. runner docstring: one line about P6 was reworded to add the round-33 `reason_code` sentence. Additive, with no meaning lost.
4. runner `--tmpdir` default: `DEFAULT_TMPDIR` changed to None plus a private `mkdtemp` that is removed afterwards. An explicit `--tmpdir` behaves exactly as before. The gate's `--selftest` delegation and every caller I found pass `--tmpdir` or accept the private default. I did not run the default mode, because it writes under /fast/scratch/hyaku/kake-r27, outside my sandbox.
5. runner `load_case_setup` raise line: `ValueError` becomes `CaseRefusal("setup_commit_before_init", ...)`. `CaseRefusal` subclasses `ValueError`, so `prepare_case`'s `except ValueError` still catches it, and the message fragment is unchanged.
6. `apply_setup` raise: `RuntimeError` becomes `SetupRefusal(...)`, which subclasses `RuntimeError`. The text is unchanged.
7. `prepare_case` setup-failure return: a string becomes `CaseRefusal(code, same text)`, and `run_case` uses `str(setup)`, so the reason text is identical.
8. `read_expected`: 10 lines were moved inside the `try:` (re-indented). The inner `ValueError`s are not `OSError`, so they pass through unchanged, and `OSError` from fstat or read now becomes "expected.json unreadable". This is a repair; no behaviour was lost.
9. `def main` split into `_run` plus a new `main` wrapper: a pure restructure.
10. Fixture-root listing (5 lines): non-directory entries are now refused (exit 2). This is a real behaviour change; see F1.

Rewritten history lines (SCORECARD, LOG, SOURCES, knowledge, lessons, QUALITY, SKILL, PROVINCE): none. The SCORECARD "Corrections and limits found by wave 1" block (SCORECARD.md:1135-1157) is appended under the measured results and says "the declaration stays as landed". It is not a rewrite.

## F1 (operability, low; a fixable documentation defect, not a judged harm)
Counterexample, using copied fixtures in the sandbox:
- With `.keep` added to the fixture root, the base exits 0 (clean) and the tip exits 2 with "fixture directory contains non-directory entries: .keep".
- With a dangling symlink `zz-dangling`, the base exits 1 and names `zz-dangling` as a failed case. The tip exits 2 with the same "non-directory entries: zz-dangling" error.
- Receipts: /fast/scratch/hyaku/kake-r33/w2/CriticHarmCheck/r/{base,clone}-{dotfile,dangling}.json.

No false pass results: both runs are nonzero, and the tip names the entry, so this is the intended round-33 "stray fixture-root entries" repair. However, the unchanged docstring line scripts/citing_set_selftest.py:80-81 (blame 9a7f5be2) still says "a symlink in the fixture directory, dot-named or not (a symlinked case is a failed case ...)". At tip, that holds only for symlinks that resolve to a directory. A dangling symlink or a symlink to a file is now a could-not-evaluate run, and the docstring does not mention the new non-directory refusal. Impacted axis: operability, meaning operator expectations from the docs.

Smallest safe correction: amend lines 80-81 to say that a symlink resolving to a directory is a failed case, and that any non-directory entry (a file, a dotfile, a dangling symlink or a symlink to a file) makes the run could-not-evaluate (exit 2).

## Not verified
- The runner's default (no `--tmpdir`) mode and concurrent default runs (a sibling seat owns these).
- C1 and C2 counter scores at the tip (sibling rerun seats own these).
- Whether 7fc6aa2f is deployed (no owned-site requests were allowed).
