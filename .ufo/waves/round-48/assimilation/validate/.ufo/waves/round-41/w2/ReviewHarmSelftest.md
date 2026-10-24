# R41 w2 — ReviewHarmSelftest (harm rule, selftest half)

Axes: operability, freshness. Leaf seat, no subagents. Lane repo /home/vgpnk/Projects/shokunin/kake-shokunin; all commands below ran there (cwd), exit codes in brackets.

## What I checked
1. Build selftest = 198/198 PASS.
2. Base tool (8eb121c8) selftest = 188/198 with only `r41_*` red.
3. Selftest diff 8eb121c8 → eae5ae2 removes no line.
4. Byte identity of the two tools under test (guards against testing the wrong bytes).

## Commands and results
- `sha256sum scripts/sitemap_audit.py` [0] → `0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf` = claimed build `0b485431…13edbf`.
- `git show 8eb121c8:scripts/sitemap_audit.py > $SANDBOX/base_sitemap_audit.py` [0]; `sha256sum` → `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e` = claimed base `4de35f8c…1460e`.
- `git rev-parse 8eb121c8 eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6` [0] → full ids match the claims.
- Build: `timeout 900 prlimit --as=4000000000 python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` [0]; output `PASS 198/198`; `grep -n 'FAIL\|COVERAGE'` on the captured output found nothing [1].
- Base: same command with `--tool /fast/scratch/hyaku/kake-r41w2/ReviewHarmSelftest/base_sitemap_audit.py` [1]; `PASS 188/198`; exactly 10 `FAIL` ids, all matching `^FAIL r41` (10/10), non-`r41_` FAILs 0.
- Diff: `git diff --numstat 8eb121c8 eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6 -- scripts/sitemap_audit_selftest.py` [0] → `76  0` (76 added, 0 removed); `grep -c '^-[^-]'` on the full diff → 0 removed content lines. Added lines: 75 non-empty + 1 empty = 76, consistent with numstat (the empty added line is invisible to both `^+[^+]` and `^-[^-]` greps).
- Tree identity: `git status --porcelain -- scripts/` → empty; `git diff eae5ae2 --stat -- scripts/` → empty. Working-tree scripts are byte-identical to the build commit, so both runs used the build's selftest fixture set (the item's specified design: one selftest, two tools). HEAD is 2653b629 (later commit), but scripts/ matches eae5ae2 exactly and is clean.

## FAIL ids on base (all 10, all `r41_*`)
r41_manifest_url_c0_interior, r41_loc_path_space, r41_loc_path_pipe, r41_loc_path_caret,
r41_loc_path_brace, r41_loc_path_del, r41_loc_fragment_second_hash, r41_loc_path_bracket,
r41_loc_bad_percent_triplet, r41_loc_userinfo_second_at.
Consistent with the scorecard's round-41 build section ("base `PASS 188/198`, the ten red fixtures all
`r41_*`"; the port-letter parity guard green on both — not contradicted by anything observed here).

## Verdicts per checked statement
- Build selftest 198/198 at sha `0b485431…`: **holds**.
- Base 188/198 with only `r41_*` red (10 ids, listed above): **holds**.
- Selftest diff removes no line: **holds** (numstat `76 0`; zero `-` content lines).

## Findings
None at any severity. No defect observed in the checked surface.

## Residual risk / gaps (not failures)
- This item covers the selftest half only; the round-39 real-run byte-equality half (`fd985a41…`) was not re-run here.
- Selftest exit-1 on base is by design (red new fixtures); no COVERAGE FAIL appeared in either run, so the fixture set is self-consistent.
- Sandbox artifacts (both raw outputs, extracted base tool): `/fast/scratch/hyaku/kake-r41w2/ReviewHarmSelftest/`.
- Tooling directive: nothing installed — python3/git already present sufficed; no pacman/uv/npx/cargo/npm activity.
