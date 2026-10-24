# ReviewQualityCriteria34 — QUALITY.md "Round-34 criteria" (a)–(d) at 24a1647

Target: `corpus/QUALITY.md:606-675` at `24a16474ee73e20453f3e1be9d2f33573c5196d9`, read in a
sandbox clone `/fast/scratch/hyaku/kake-r34/w2/ReviewQualityCriteria34/clone` (checkout `24a1647`,
probe commits `bc0ef0b` synthetic lessons, tag `probe-lookup` fetched from the retained bundle).

## Per-criterion verdicts

### (a) Cited artifact resolves from committed lane bytes — PASS
- Pointers resolve: routed item 2 is verbatim at
  `corpus/lessons/round-33-verifier-spotcheck.md:192-196`; all three retained paths absent at
  `d08d8de` (`git cat-file -e` exit 128, observed for bundle AND both diffs) and present at
  `a2fe31b` (exit 0). Receipt `verification/criterion-retained-path-d08d8de-vs-a2fe31b.txt`
  records exactly this for the bundle; I re-verified both `.diff` files myself.
- sha256 text claims verified: bundle `6ff6c403…77c00`, dedup `28fd9adf…7d6e`, alt
  `daeaa738…0ce6e`; `git bundle list-heads` → `489714be413c936a6d98188a80fce016c0b52ef7` on
  `refs/tags/r33-c1-counterexample`. Commit objects are NOT lane-resident (`git cat-file -t
  489714be` in lane → "could not get object info"); they resolve only via `git bundle`, which
  the criterion's "makes bytes reachable, not proved" limit covers.
- Check = `git cat-file -e` per cited path; the receipt is the failing+passing run pair.
- Consistent with the round-20 byte-identical-append rule (`QUALITY.md:35-36`): (a) restates it.
- Nit: receipt demonstrates the fail/pass pair for one of three named paths.

### (b) Gate records a screened reject with reason — PARTIAL FAIL on check strength
- Pointers resolve: spotcheck:197-198 verbatim; `corpus/lessons/round-33.md:25-37` is `## Gate`
  with two `admit` rows (:31, :32) and `grep -c reject` = 0 — verified; `SCORECARD.md:1203`
  names S071/S072 "opened and screened for rejection".
- Named check exists at `.ufo/waves/round-34/criteria/gate_reject_check.py`; receipts exist and
  reproduce identically (re-ran): exit 1 `NO MATCH` on round-33 at `93359ff`; exit 0 `MATCH
  corpus/lessons/round-29.md:56` on round-29 at `a2fe31b2`.
- Round-34's own Gate (`corpus/lessons/round-34.md:38-42`) satisfies the criterion: four
  reject rows with located quotes and reasons.
- DEFECT B1 (medium): the criterion requires the check "to fail … a reject with no located
  reason" and Reject-lists "a status word or the verdict again". The check only tests a
  non-empty reason. On sandbox probe commit `bc0ef0b`: decision `reject, tier C, kind docs,
  status rejected` → exit 0 (MATCH); bullet `**rejected**: rejected` → exit 0. A bare `reject`
  correctly gives exit 1. So the verdict-again/status-word shape passes — the check's own
  limit admits "a present reason is not a true reason", but the criterion's Reject clause
  enumerates exactly this shape. Evidence: `gate_reject_check.py:85-94` (`has_reason` returns
  true on any non-empty tail).
- DEFECT B2 (minor): "(its docstring states the exit contract)" — the docstring
  (`gate_reject_check.py:2`) is one line and states no exit contract; exits 0/1/2 exist only
  in code (:153-171). Compare `receipt_presence_check.py`/`lookup_control_check.py`, whose
  docstrings do state contracts.

### (c) Every cited run ships a committed receipt — PASS
- Pointers resolve: spotcheck:199-201 verbatim; quoted line verified at
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kake.md:62`
  ("`93359ff`: 4/4 (run, not committed)"); `git diff 3abfc44 93359ff --stat -- scripts/` is
  empty (0 lines) — "harmless" claim verified; `corpus/QUALITY.md:450-460` is the round-30
  named-revision-receipt bullet it extends — verified.
- Check exists at `.ufo/waves/round-34/criteria/receipt_presence_check.py`; receipt
  `criterion-receipt-presence-r33-report.txt` says `unreceipted hashes: 93359ff` exit 1 —
  reproduced identically. Failing run shown; can fail.
- Nits: no committed exit-0 receipt is cited (only a wave-1 report); docstring matches receipt
  `revision` by prefix while text says "equals".
- Residual: no `.ufo/reports/round-34/` report exists at `24a1647`, and no file in the landed
  tree names `24a1647` as a measured revision — so (c) is not violated by this round, but also
  untested against this round's own report.

### (d) Counter scores lookup control below full score — PASS
- Pointers resolve: "round-34 mistake row 4" = `corpus/lessons/round-34.md` `## Mistakes` row 4
  (line 68, lookup-table row); both control bundles present, heads `lookup-c1`→`dcef39b5`,
  `hollow-c2`→`0cce15f`.
- Check exists; receipt `criterion-lookup-control-c1-dcef39b.txt` (exit 1, score 28/28, verdict
  FAIL) reproduced byte-identically after `git fetch` of the bundle into the clone (control
  objects are not lane-resident — same bundle-only reachability as (a), consistent).
- Can fail — the cited receipt IS the failing run. No earlier criterion contradicts: the
  round-33 hollow-control bullet (`QUALITY.md:590-604`) requires only a hollow commit below
  after-value; (d) adds the lookup class and ordering as a superset.
- Residual (not a contradiction, worth noting): applied to round 34 itself, (d)'s Reject list
  ("counter that materializes cases under directory names equal to case ids next to a
  published matrix") describes the landed `c1_matrix_count.py` — the criterion grounds this as
  mistake row 4 rather than claiming compliance, and the "run before the counter is frozen"
  clause postdates the frozen counter.

## Commands run (all in sandbox clone unless noted)
- `git cat-file -e <rev>:<path>` ×6 → 128 at `d08d8de`, 0 at `a2fe31b` (all three paths)
- `python3 -B .ufo/waves/round-34/criteria/gate_reject_check.py --repo . --rev 93359ff --lesson
  corpus/lessons/round-33.md` → 1; same on `a2fe31b2`/`round-29.md` → 0; on probe `bc0ef0b`
  synthetic lessons → 1 (bare reject), 0 (status-word reason), 0 (verdict-again reason)
- `python3 -B .ufo/waves/round-34/criteria/receipt_presence_check.py --report <fleet r33
  kake.md> --repo . --rev 93359ff --round 33` → 1 `unreceipted hashes: 93359ff`
- `git fetch <bundle> refs/heads/lookup-c1:refs/tags/probe-lookup` then `lookup_control_check.py
  --counter .ufo/waves/round-34/c1_matrix_count.py --repo . --control dcef39b5f…` → 1 (28/28)
- `sha256sum retained/*`, `git bundle list-heads` ×3, `git -C <lane> cat-file -t` (read-only)

## Not verified / limits
- C2 counter not probed against `0cce15f0` with `lookup_control_check.py` (receipt exists only
  for C1); C2 hollow receipt is `c2-at-critic-hollow-0cce15f.json` from the counter itself.
- No full-text contradiction scan beyond Gate/sandbox/receipt/counter terms across rounds 21–33;
  none of the round-31 wave-2 corrections conflict.
- Lane mutations: none except this report; probe commit/tag confined to sandbox clone.

Report: .ufo/waves/round-34/w2/ReviewQualityCriteria34.md
Tools installed: none.
