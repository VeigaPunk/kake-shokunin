# ExecC1Data53

Claim C1 data for three members. Method: shared clone detached at base `97cdc122379711c2b02a8970752c8782da3ac81d`;
each counter run `python3 -B <path> --root . --revision <rev>` with `GIT_*` scrubbed (env -i, PATH+HOME+TMPDIR only),
TMPDIR scratch, timeout 1800. Raw outputs: `ExecC1Data53.files/out/<counter>-<rev8>.txt` (16 runs).

## MEMBERS:

### `.ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py`
- Measured rev: `fd91527a286086c1f4e6d4f44f715a907f041b5d` — source line: report `/.ufo/reports/round-53/kake.md` L23
  "**Freshness claim — measured on the source-row commit `fd91527a286086c1f4e6d4f44f715a907f041b5d`**"; SCORECARD round-53
  section names only base `3994101d`. Spotcheck `corpus/lessons/round-53-verifier-spotcheck.md` L5: base `3994101d`, after `189ba6d1`.
- Registered: SKILL.md L213, Kind cell literally `gate` => label **live** under the C1 rule.
- exit@base (97cdc122): **1** (`gate-truth 2/7 met=False`). Matches contract's L1 probe.
- exit@measured (fd91527a): **1** (`gate-truth 2/7 met=False`; L1/L2/L3/R1/R2 fail).
- Ever green? Ran 6 revisions: `3994101d` (round-52 tip, receipt's own run) 1, `fd91527a` 1, `189ba6d1` (r53 tip) 1,
  `a631cc02` 1, `5826682b` (r54 tip) 1, `97cdc122` 1 — every real tree `2/7 met=False`. The only green is the selftest's
  in-memory `pass_corrected` fixture (mutated copies, never committed). Honest label: **never-met**, pin `fd91527a`.
- Verdict-map error in the existing row: it claims `64=usage`; the code uses stock argparse (exits 2 on usage). Real map: 0/1/2.

### `.ufo/waves/round-54/c54_ops_debt.py`
- Measured rev: `a631cc0246b97f2a949d61186c7466468faf94d6` — SCORECARD L4282-84 "measured commit
  `a631cc0246b97f2a949d61186c7466468faf94d6`"; report `/.ufo/reports/round-54/kake.md` L30 "After `a631cc02...` ...
  uncovered=0 ... exit 0".
- Registered: **unregistered** at base (no SKILL.md row; matches contract's 12-member unregistered list).
- exit@base (97cdc122): **0** (`registry=present manifest=present uncovered=0`).
- exit@measured (a631cc02): **0** (same line). Also green at parent `a0a4fd48` and r54 tip `5826682b`; **1** at r54 base
  `68228b2d` (`registry=absent manifest=absent uncovered=7`, reproduces `controls/base-c2-ops-debt.txt`).
- Ever green: yes. Honest label: **live**.
- Fragility (for L1/w2): its `registry_row_ok` requires the c53 row's Kind cell to equal literal `gate`; relabelling c53
  to `never met` turns this counter red (`registry=absent`) unless the counter is adjusted too. Coupling is inside the
  counter, not in SKILL.md.

### `.ufo/waves/round-54/c54_s374_calib.py`
- Measured rev: `a631cc0246b97f2a949d61186c7466468faf94d6` — same source lines as above (SCORECARD L4288 counting command;
  kake.md L25 "After `a631cc02...` `mismatches=0 met=True`, exit 0").
- Registered: **unregistered** at base.
- exit@base (97cdc122): **0** (`mismatches=0 met=True`).
- exit@measured (a631cc02): **0**. Green at parent `a0a4fd48` and tip `5826682b`; **1** at r54 base `68228b2d`
  (`mismatches=1`, reproduces `controls/base-c1-s374.txt`). Correction commit `8e408e00` is an ancestor of `a0a4fd48`.
- Ever green: yes. Honest label: **live**.

## ROWS:
- `.ufo/waves/round-60/w1/ExecC1Data53.files/rows.md` — three complete 8-cell rows in SKILL.md format:
  - c53 replacement row: Kind `gate (never met: red at its round-53 measured revision fd91527a286086c1f4e6d4f44f715a907f041b5d, ...)`;
    verdict map corrected to real exits `0=`/`1=`/`2=` (no `64`); selftest `--selftest` (17 fixtures).
  - c54_ops_debt new row: Kind `gate (live; ...)`; `0=`/`1=`/`2=`/`64=` (UsageParser); self-test `none (no selftest mode)`.
  - c54_s374_calib new row: Kind `gate (live; ...)`; `0=`/`1=`/`2=`/`64=`; selftest `--selftest` (9 fixtures).
  All entry commands are the counters' real CLIs (`python3 -B <path> --root . --revision <commit>`); no `|` inside cells.

## NOTES:
- c53 label consequence: `live` + exit 1 at base is the contract's `live_not_green` mismatch; the honest relabel is
  `never met` (pin `fd91527a`), NOT `historical` — it never printed green on a committed tree. Pin ancestry verified:
  fd91527a, 189ba6d1, a631cc02, 5826682b are all ancestors of 97cdc122.
- Applying the c53 relabel row changes `c54_ops_debt.py` from green to red (the Kind-literal coupling above): the L1 must
  either keep c53's row verbatim elsewhere for that check, patch c54_ops_debt, or accept it turning red and relabel it
  accordingly. Flagged, not resolved — resolving it is a c54 counter change, outside my write scope.
- c53's checks L1/L2/L3/R1/R2 fail at every committed revision because they read `corpus/lessons/round-52.md` and
  `corpus/SOURCES.md` at the revision; round 53 never landed the corrected bytes the selftest fixture fabricates.
- No tools installed; no pacman run. No build/lint/test verification beyond the counter runs above (parent owns the
  post-integration gate). Scratch `/fast/scratch/hyaku/kake-r60/ExecC1Data53/` deleted after copying cited outputs.

VERDICT: c53_gate_truth.py = never-met (red 1 at base, measured rev fd91527a, and 4 more revs; pin fd91527a); c54_ops_debt.py and c54_s374_calib.py = live (green 0 at base and at measured a631cc02); three drafted 8-cell rows in ExecC1Data53.files/rows.md.
