# Round 97 — seat MutReval (mutation probe of the C2 successor's new clauses)

Deliverables: `w1/MutReval/mutants.tsv` (per-mutant table), `w1/MutReval/mut.md` (method, commands, rc, results),
`w1/MutReval/mut-m1.py`…`mut-m7.py` (mutant sources), `w1/MutReval/receipt-*.txt` (every run's rc, argv,
stdout, stderr), `w1/MutReval/receipt-jobs.json` and `receipt-runner.py` (the job list and runner).

## Scope and bounds
- Target: `c97_reval.py` (sha256 `f3895a32…`, verified before and after). Read-only; no LANE byte written.
- Mutants built in a scratch clone of LANE at tip `9e27ce0b…`; fixtures in scratch clones; scratch removed after copying receipts.
- No tool installed or upgraded (python 3.14.8, git 2.56.0 from the host).
- Kill rule: killed iff `--selftest` fails OR the output line differs from the frozen counter on the lane tip OR on the
  table-in-candidate-slot clone (`cf9ea193…`). Supplementary fixtures are reported separately and are not in the rule.

## Result
- Frozen baselines: selftest rc=0 `8/8 … 14/14 … anti_table=ok`; lane tip rc=0 `met=true` (`hand=37/37 generated=104/104
  heldout=56/56 forgeries_refused=7/7 … population=ok`); table clone rc=1 `heldout=20/58 … met=false`.
- Official: **killed 3/8** (M1 drop held-out conjunct → table clone `met=true`; M2 constant seed → `heldout` totals differ on tip
  and table clone; M3 fixtures without held-out → `forgeries_refused=6/7` on tip and table clone).
- Official survivors: M4a (pins at HEAD), M4b (pins from working tree), M5 (drop LOOKUP_SHA check), M6 (anti-table canonical-only),
  M7 (GIT from PATH, equivalent).
- Selftest rc=0 for all eight mutants: the selftest does not exercise the held-out conjunct, the pin reads, the LOOKUP_SHA check,
  or the widened anti-table, so it is blind to every successor clause probed here.
- Supplementary (outside the kill rule), each distinguishing the mutant from the frozen counter: M4a on a HEAD-changed pin
  (rc2 drift vs rc0), M4b on a working-tree-changed pin (rc2 drift vs rc0), M5 on a comment-changed frozen lookup table
  (rc2 drift vs rc0 with full line), M6 on a candidate carrying a minified-form needle (anti_table=ok met=true vs hit met=false).

## Findings the round must record (routed to L1; no repair made)
1. **Coverage survivors (M4a, M4b, M5, M6).** The frozen fixture population (positive control, six round-96 forgeries, lookup
   table, the frozen controls) does not exercise: pins read at the scored revision rather than HEAD or the working tree (R96-1
   committed-bytes clause); the LOOKUP_SHA digest pin on the forgery itself; or the minified/digest-encoding needles of the
   widened anti-table (R96-2). Each clause is correct by reading and by supplementary probe, but no frozen receipt shows it bites.
   The round should record these as unexercised clauses; the counter stays frozen per the round-95 Amendment-A rule.
2. **M2 kill is by total only.** The constant-seed mutant changes held-out totals (56→57 on tip) but decides every case
   identically on the tip. The commit-derived seed clause therefore has no verdict-level kill in the frozen set [INFERENCE:
   a candidate that memorizes the constant-seed inputs would pass heldout on a constant seed; not run].
3. **Reference-refused inputs are silently skipped in generated and held-out scoring (measured).** `generate()` yields inputs
   the reference refuses (`validation response without a stored validator`); `main()` drops them via `except Invalid: continue`.
   Measured skips: seed 97: 16/120; seed 9797: 3/60; tip seed `int(9e27ce0b…[:15],16)`: 4/60; table-clone seed: 2/60.
   The C6 refusal class is scored on generated/held-out only by the single hand case `refuse/status-without-validator`.
   The printed `generated=104/104` and `heldout=56/56` therefore hide these skips. [INFERENCE from code: a candidate that
   constructs or updates on those inputs would not be penalized by generated or held-out scoring.]
4. **M7 is an equivalent mutant on this host.** `GIT = "git"` resolves through the child environment's PATH (`/usr/bin:/bin`).
   With a failing shim first on the outer PATH, frozen and mutant outputs are identical (`receipt-F-tip-shim.txt`,
   `receipt-m7-tip-shim.txt`, no `SHIM-GIT-USED`). The `/usr/bin/git` pin is defense-in-depth with no observable effect.
5. **Stale docstring.** `c97_reval.py` docstring still says "every forgery subject refused (6/6)" and "the six forgeries";
   `FORGERIES` lists seven. `HELDOUT = 60` is labeled as the held-out count, but the printed totals are 53–58 by design of finding 3.
   Documentation drift only; the frozen bytes are not to be edited.
6. **LANE tree state (observed, not touched).** `git -C LANE status --porcelain` at the time of my reads shows ` M SKILL.md` and
   untracked `controls/census-before.txt`, `controls/repair-c1.txt`, `controls/repair-c2.txt`, `w1-dispatch.json`. The freeze
   says controls were committed before the freeze; `repair-c1.txt` and `repair-c2.txt` are not in a commit. L1 should confirm
   which receipts are committed evidence.
7. **Scratch incident.** ConnectorScope-23 reported an `rm -rf` of the round parent scratch directory, which removed this seat's
   clones mid-run. I recreated the clones from LANE and re-ran; every run in the receipts postdates the recreation.

## Observed C2 line at the lane tip (context only; not a re-scoring)
`C2v97 revision=9e27ce0b… candidate=present hand=37/37 generated=104/104 heldout=56/56 forgeries_refused=7/7 positive=admitted
mutants=14/14 survivors=none anti_table=ok population=ok seed=97 met=true`, rc=0. Candidate sha256 at tip is `192b3bf7…`, matching the freeze.

MUT-REVAL killed=3/8 survivors=M4a-pins-at-HEAD,M4b-pins-working-tree,M5-drop-lookup-pin,M6-antitable-canonical-only,M7-git-from-PATH
