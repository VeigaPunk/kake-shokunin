# SentinelScope — scoped findings (round 96 w1) (2026-11-05T15:45:38-03:00)

Verdict: `SENTINEL refused=28 escaped=F1,F2,F3,F4`

Full report + per-attack receipts: `.ufo/waves/round-96/w1/SentinelScope/sentinel.md` (r01–r18).

- **F1 (HIGH, route to round 97 — defect, not repaired):** frozen `.ufo/waves/round-96/c96_reval.py` crashes
  `NameError: name 'mutants' is not defined` (line 624) on every candidate-present scoring run — the only path
  C2's `candidate=present … met=true` predicate needs. rc=1, empty stdout, no verdict line. Both committed
  controls avoid the path (base-c2 = candidate-absent early return; ctl-c2-selftest = selftest scope, line 511).
  Receipt: `w1/SentinelScope/r08-c2-crash-nameerror.txt`.
- **F2 (LOW, env-boundary):** C1 counter executes `git` resolved from PATH; a shadowed wrapper was executed with
  a clean verdict (precondition: control of the counting process env). Receipt: `r06-c1-path-git-shadow.txt`.
- **F3 (INFO):** sandbox-unaudited: `os.kill(os.getppid(), sig)` (scorer-DoS only), outside `os.listdir`/`os.stat`
  metadata, persistent unaudited `os.chdir` (no content escape — realpath still checks every open). Receipt:
  `r09-sandbox-matrix.json`.
- **F4 (CONFIRMS routed R95-7, C2 side):** no effectful-shadow defense — marker-writing candidate answering
  correctly runs clean (r10/r16); outside-tree effects refused (r12/r13/r14). Counter-level admission formally
  undecidable this round because of F1.

Refused (28 total): all C1 module-shadow vectors (PYTHONPATH, cwd, beside-copy), startup os-shadow,
docstring claim check; sandbox symlink/abs/chdir/fd/open_code/runpy outside-root opens, 5 denied imports, 5
process-creation denials, PYTHONPATH-under--I, parent sandbox-source read; hostile candidates
effect-out/symlink/execv refused at the sandbox layer. Base controls reproduced line-identically (read-only);
lane zero-mutation proven across all scoring runs (porcelain identical, HEAD constant); `resume_continuity_v1`
has no surface here — substituted zero-mutation check performed. Instruments untouched; digests re-verified
after all runs; no tools installed; no sysctls touched; scratch deleted before yield.
