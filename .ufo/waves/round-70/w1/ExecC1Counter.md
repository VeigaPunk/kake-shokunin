# ExecC1Counter — kake round-70 W1

Seat: executor. Base revision: e5f6fd9e4c243d092160bc74e8bea24256087173.
Frozen predicate implemented verbatim: C1 met iff the counter prints `unannotated=0` and exits 0.

## Deliverables (.ufo/waves/round-70/w1/ExecC1Counter/)
- `c70_pointer_audit.py` (final lane path `.ufo/waves/round-70/c70_pointer_audit.py`), sha256
  `3e4958fc1a2971c418ff42317ea6fe204e3c312353c37f7a85d71d37ae45a43e`, 328 lines.
- `patch.diff`: `add -N` + `git diff` at the clone; `git apply --check` exit 0 on a clean base
  clone, and the applied file sha256 equals the delivered file.
- `selftest.txt`, `base-run.txt`, `base-run-lane.txt`, `after-sim.txt` — exercised receipts below.

## Behaviour
- Committed bytes only: `git -C <root> show <revision>:SCORECARD.md`. Every git call is list-form
  `subprocess.run(['git','-C',root,...])`; no shell=True, no shell interpolation.
- Population: the three frozen regexes, deduplicated by token, first occurrence line kept.
- Dangling: repo -> `git cat-file -e <rev>:<path>` nonzero; home/tmp -> `os.path.lexists` on the
  expanded path (home) or the literal path (tmp).
- Annotation: section `## Pointer calibration (round 70)` to the next level-1/2 heading; a row with
  leading spaces and one pipe stripped, spaces stripped, full-string equality is the only
  annotator; prefix/substring never annotates; rows inside HTML comments are not rows.
- Output: `pointers=N dangling=D annotated=A unannotated=U met=true|false`, then one
  `<class> <status> line=<n> token=<token>` per dangling token; exit 0 iff U==0, 1 else, 2 on usage/IO.
- `--selftest --work <dir>`: one fixture repo under work (`init -q`, toplevel assertion, commits
  `-c user.name=fx -c user.email=fx@fixture`), cases (a)-(e); temp dirs only via `mkdtemp(dir=work)`.

## Exercised verification (only these ran)
1. Selftest: `python3 -B <clone>/.ufo/waves/round-70/c70_pointer_audit.py --selftest --work <S>/work`
   -> cases a-e ok, `selftest 5/5`, exit 0 (`selftest.txt`). Case (d) prints
   `pointers=2 dangling=2 annotated=1 unannotated=1 met=false`, with the full token still
   `tmp unannotated line=3 token=<token>`; the prefix cell annotates only itself.
2. Base run (do-nothing control): `python3 -B <clone>/.ufo/waves/round-70/c70_pointer_audit.py
   --root <clone> --revision e5f6fd9e...` -> `pointers=348 dangling=19 annotated=0
   unannotated=19 met=false`, exit 1; exact U0 = 19 (`base-run.txt`). With the delivered artifact
   against the lane root the output is byte-identical, exit 1 (`base-run-lane.txt`). Kill rule not hit.
3. Base dangling population (19), class, first line:
   home: `~/Projects/plazir-15-site` (62), `~/DIRMAP.md` (76), `~/projects` (77)
   repo: `.ufo/charter-scribe/ledger.jsonl` (89), `scripts/sources-census.sh` (1583),
   `.ufo/waves/round-39/r38w2-evidence.SHA256S` (2357), `.ufo/waves/round-44/verification/before-v4.json` (3451),
   `.ufo/waves/round-44/verification/after-v5.json` (3456), `.ufo/l0-questions.md` (3750),
   `scripts/hyaku/ufo-wave-policy.json` (4184), `scripts/../.ufo/waves/round-51/c51_wave_ledger.py` (4214)
   tmp: `/tmp/kake-r18` (89), `r17` (90), `r16` (91), `r15` (92), `r14` (93), `r13` (94),
   `r12` (99), `r11` (100), `r10` (101)
4. After-state reachability (scratch-only simulation of the calibration section, not the lane
   after-state): appended bare rows for all 19 in a scratch clone commit (ea736568f7260fe58415929863b6df0c55f3aaa6)
   -> `pointers=348 dangling=19 annotated=19 unannotated=0 met=true`, exit 0 (`after-sim.txt`).
5. Mutation-tester cross-check: MutC1Counter ran this exact sha against five fixture repos and
   reports F1-F5 5/5 killed (prefix, comment, wrong-section, honest, worktree), plus backticked
   cell -> unannotated. It corrected my worktree pre-run with the sharper mutant: SCORECARD
   committed with the repo pointer, target only in the worktree -> `pointers=1 dangling=1
   unannotated=1` exit 1, proving resolution is revision-based. Receipt:
   `.ufo/waves/round-70/w1/MutC1Counter/receipt-counter-fixtures.txt`.

## Findings for integration
- Annotation first cells must be the bare token; backticked or inline-code cells do not annotate
  (strict equality; MutC1Counter reproduced this). Rows inside HTML comments do not annotate.
- Known adjacent, not a claim: a pipe row inside a fenced code block in the section annotates,
  because the frozen rule is syntactic ("line ... after leading spaces and a pipe"). Fixture F7 and
  receipt live with MutC1Counter; the L1 rules on it. I did not alter the frozen rule.
- Three base repo danglers are fleet-root-relative in intent (`scripts/sources-census.sh`,
  `scripts/hyaku/ufo-wave-policy.json`, `.ufo/l0-questions.md`): they exist under
  /home/vgpnk/Projects/shokunin, not at the revision; annotation or rewording is required.
- `scripts/../.ufo/waves/round-51/c51_wave_ledger.py` dangles literally: cat-file does not normalize
  `..`; the normalized path exists at base.
- tmp family: 9 distinct tokens `/tmp/kake-r10/`..`/tmp/kake-r18/` over 11 occurrences (r17 repeats
  at lines 4461, 4478). The contract prose says "12 tokens"; the frozen dedupe rule yields 9.
  Recorded as measured, not reinterpreted.
- Home-class U0 depends on the measuring host HOME (/home/vgpnk).

## Risks / blockers
- None blocking this delivery. The lane after-state does not exist yet (the calibration section is
  C1/L1 work); the tip run must be executed after integration, never inferred from `after-sim.txt`.
- Hand-off: apply `patch.diff`, run `--root <lane> --revision <tip>` and require `unannotated=0`
  exit 0, then run `--selftest` from the integrated file.

## Tooling and scratch
- No tool installed or upgraded; pacman untouched.
- /fast/scratch/hyaku/kake-r70/ExecC1Counter removed on exit. No lane tracked file modified
  (`git status --porcelain` shows only untracked wave files; `git diff -- SCORECARD.md` empty).
