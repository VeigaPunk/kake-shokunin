# MutationDropReport — round-51 wave 1 (seat `MutationDropReport`, mutation-tester)

**Assigned mutant:** drop one committed seat report file from the C1 wave-evidence fixture and re-run the L1 check.
**Verdict: KILLED.** L1 rejected the mutant with two notes; the whole ledger fell to 2/3, exit 1.
**Pristine control passes 3/3, exit 0.** Restoration is byte-identical and the detector returns to 3/3.

## Axes named

- Operability: does the C1 ledger actually detect a per-seat output that vanished, rather than restate its own inputs?
- Mechanism integrity: is the detector's pass/fail derived from committed bytes, not the worktree?

## Fixture (built in `/tmp`, lane untouched)

Scratch repo `/tmp/kake51-mutdrop-2`, `git init` fresh, no copy of the lane's `.git`:

- `.ufo/waves/round-51/c51_wave_ledger.py` — copied byte-for-byte from the lane (`cp -p`).
- `w51-taskcall.json` — `counts.spawn = 2`, `taskCall.tasks = [{name: Alpha}, {name: Beta}]`.
- `settlement.json` — `spawn 2`, `settled_count 2`, `dead_count 0`, `reports_written 2`,
  `timeout_seconds 3600`, both seats `report: true` (10 s and 20 s), `dead: []`.
- `w1/Alpha.md`, `w1/Beta.md` — the two seat reports (no `swarm-registry.json`, so the `.md` filter is exercised as in the real wave).
- `route-map.json` — one role `scout` with `kimiModel "route-ok"`; probe prose names both `route-ok` (HTTP 200) and the deviation `route-bad` (HTTP 500).
- `route-probes/route-ok.json` — `{alias: route-ok, httpStatus: 200, ok: true}`;
  `route-probes/route-bad.json` — `{alias: route-bad, httpStatus: 500, ok: false, bodyExcerpt: "upstream 500"}`, bound to no role.
- `wave-timing.json` — `startedAt 2026-10-25T00:00:00Z`, `settledAt 2026-10-25T00:01:40Z` (wall = 100 s).
- `round-time-accounting.json` — `wall_clock_seconds 100`, `aggregate_seat_seconds 30`, `dead_seat_seconds 0`.
- `LOG.md` — names the wall-clock figure `100`.
- `wave-grant.txt` — `granted lane=kake wave=r51-w1 seats=2`.

Command (identical for every run below):

```
python3 -B .ufo/waves/round-51/c51_wave_ledger.py --root /tmp/kake51-mutdrop-2 --revision <commit>
```

## 1. Baseline (pristine bytes)

Revision `68d388e14f9821deb5898265a6a3c68d82b53fe3`.

```
C1 ledger 3/3 met=True  (met: ledger_checks_passed == 3 of 3)
  L1 pass
  L2 pass
  L3 pass
EXIT=0
```

A baseline failure would have been inconclusive; there was none, so the mutant is scorable.

## 2. Mutant — delete one seat report file

```
sha256 .ufo/waves/round-51/w1/Beta.md before = 3ae5df978cbd2895286d3e5a66edda5f1a687b00fa41b42b17e0107004de4eb4
git rm .ufo/waves/round-51/w1/Beta.md && git commit   -> ede2b7fa8449ade8933193113c36c7209a01c54f
```

`w1/` now holds `Alpha.md` only. Detector output, verbatim:

```
C1 ledger 2/3 met=False  (met: ledger_checks_passed == 3 of 3)
  L1 FAIL
    - settlement reports_written 2 != committed report files 1
    - seats marked with a report but no committed file: ['Beta']
  L2 pass
  L3 pass
  revision: ede2b7fa8449ade8933193113c36c7209a01c54f
EXIT=1
```

**Exact notes:**

1. `settlement reports_written 2 != committed report files 1`
2. `seats marked with a report but no committed file: ['Beta']`

**Exit code: 1** (L1 failed, so `ledger_checks_passed` = 2 and `met=False`).

Both halves of the L1 condition fired independently: the aggregate count equality
(`reports_written` vs the committed `.md` count under `w1/`) and the per-seat name equality
(`reported` vs `committed`, scoped to `ls-tree -r` at the revision). The mutant was **rejected**;
the L1 guard is not broken for this defect.

## 3. Restoration

```
git revert --no-edit --no-commit HEAD ; git commit  -> adeeeb86d32c96f89d4ddf9f9bc7a5ab9d678e26
sha256 .ufo/waves/round-51/w1/Beta.md after  = 3ae5df978cbd2895286d3e5a66edda5f1a687b00fa41b42b17e0107004de4eb4
git diff 68d388e1..adeeeb86 -- .ufo/waves/round-51/w1/Beta.md   -> empty
```

Restored bytes are identical to the pristine bytes (same sha256, empty diff). Detector at the
restored revision:

```
C1 ledger 3/3 met=True  (met: ledger_checks_passed == 3 of 3)
  L1 pass
  L2 pass
  L3 pass
EXIT=0
```

So the kill is attributable to the mutation alone, not to scratch-repo drift.

## 4. Coverage finding (not exercised, advice only)

L1 compares `settlement.reports_written` and each seat's `report` flag against the committed
`w1/` tree. `build_wave_evidence.py:51-60,84` derives those very fields from
`os.path.isfile(W1/<seat>.md)` over the same tree — `settled` vs `dead` and `reports_written`
are computed from the file set L1 later counts. [INFERENCE] A *coordinated* substitution — drop
`Beta.md` **and** re-author `settlement.json` so `Beta` moves to `dead` with `report: false`
(or `reports_written` becomes 1) — would satisfy L1's equalities, because both sides of the
comparison are authored from the same observation by the same builder. L1 therefore certifies
that settlement and the file tree agree, not that either is independent of the builder.
This probe was **not run** (out of the assigned scope) and is a coverage observation, not a
change to the contract or a request to alter C1.

## 5. Lane-state observation at dispatch

`git status --short` in the lane shows `.ufo/waves/round-51/route-map.json`, `route-probes/`,
`w1/`, `w51-taskcall.json`, `wave-grant.txt`, `wave-start-utc.txt` untracked and no
`settlement.json` / `wave-timing.json` / `round-time-accounting.json` on disk yet. The lane tip
`9d13768` therefore legitimately scores 0/3 for C1 — the wave evidence is not committed, which
matches the declared dispatch state. No lane bytes were read from a worktree-only path for the
verdict above; every detector run used `--revision` against committed objects.

## 6. Bounds and tooling

- Wrote exactly one file in the lane: this report. Scratch confined to `/tmp/kake51-mutdrop-2`.
- Read-only git used only: `log`, `status`, `rev-parse`, `show`/`ls-tree` (via the counter), `diff`.
- No `git add`/`commit`/`checkout`/`reset`/`push`, no `jj` mutation, in the lane. All commits cited above are in the `/tmp` scratch repo.
- No files under `considerthese/`, `.ufo/waves/round-46/residual/`, or `round-48/.../validate/` were touched.
- No tools installed or upgraded; nothing to record under the tooling directive.
- Files I could not read: none — `c51_wave_ledger.py` (ranges 1-32, 33-152, 152-265, 245-297) and
  `build_wave_evidence.py` (44-100) were read in full coverage of the paths I cite.
