# SelftestFixtureDrift — round 29, wave 2 (falsify), axis: operability

Target: committed scripts/fixtures/base-path at 7697990cbca20291f3b0367b8ff4220e93b38b03 versus frozen .ufo/waves/round-29/c2-matrix.json.
Sandbox: /fast/scratch/hyaku/kake-r29/w2/SelftestFixtureDrift/ (clone/ at 7697990; compare.py sha256 d74aae8e…; regen/; work/; tuples.tsv).
Installs or updates: none. Tools: Python 3.14.8 stdlib, git 2.56.0, diff, cmp, grep, sha256sum.
Lane touched read-only (cmp, diff -r, read, git --no-optional-locks ls-files and rev-parse). Only this report is written in the lane.

## Verdict
- HOLDS for committed bytes. Committed fixtures equal the frozen matrix: 30/30 case dirs, 87/87 files byte-identical, 30/30 expected.json tuples equal. No extra or missing case.
- LIMIT TO STATE for the committed selftest gate: it passes a tree with a case removed (P5) and passes byte-only fixture edits (P1, P6, P7).
- DRIFT OUTSIDE COMMIT (lane working tree): 14 untracked case dirs, and the working-tree selftest and audit scripts differ from 7697990. See F3.

## Commands and exit codes
1. git clone -q <lane> && git checkout -q 7697990… → exit 0; HEAD 7697990cbca20291f3b0367b8ff4220e93b38b03.
2. git ls-tree -r HEAD -- scripts/fixtures/base-path | wc -l → 87, all mode 100644. find … ! -type f ! -type d → 0 (no symlinks). git diff --stat HEAD -- fixtures → empty, exit 0.
3. Matrix freeze: blob 0687433ecd7cd14eb90287121f82a99074503b84 at d18bbf3 (declared, +588), 98dbab2 (fixtures added, 87 files) and 7697990. git diff --stat 98dbab2 7697990 -- matrix fixtures → empty, exit 0. Matrix sha256 75c08f641a31356d0f3446d9e6e435c44ee02bc4cf49102904e2466dbac2e84a.
4. python3 -B compare.py --write-regen --table tuples.tsv --self-check → exit 0. Output: committed files=87, committed case dirs=30, matrix ids unique=True count=30, "EQUAL".
5. diff -r regen/scripts/fixtures/base-path clone/scripts/fixtures/base-path → exit 0 (independent cross-check).
6. python3 -B scripts/base_path_selftest.py (clone) → exit 0; "30/30 clean".
7. Lane scripts run from copies (lane-scripts/): on committed fixtures → exit 0, 30/30; on lane fixture copy (44 dirs) → exit 0, 44/44.

## Perturbation checks (comparator vs committed selftest on copies)
- P1 comment appended to K1 index.html: comparator byte drift; selftest 30/30 (miss).
- P2 D1 expected exit 1→2: bytes and tuple drift; selftest 29/30 fail.
- P3 I5 reason renamed: bytes and tuple drift; selftest 29/30 fail.
- P4 extra dir X1 (no manifest): extra dir flagged; selftest 30/31 fail (fails on malformed input, not on the extra itself).
- P5 U1 dir removed: missing dir flagged; selftest 29/29 clean (miss).
- P6 I8 trailing newline removed: byte drift; selftest 30/30 (miss).
- P7 D11 sub/page.html href→HREF: byte drift; selftest 30/30 (miss).
- P8 D14 findings reversed: byte drift, tuple equal (multiset); selftest 30/30 (by design).

## Tuple table (committed expected.json equals matrix; full rows in sandbox tuples.tsv)
K1–K7: exit 0, clean, no findings. D1–D14: exit 1, failed-policy, outside_base_path (D10 ×2, D14 ×4). I1–I4, I6–I8: exit 2, input_invalid. I5: exit 2, page_outside_base_path. U1: exit 64, verdict null. Kinds: control 7, defect 14, input 8, usage 1.

## Findings (ranked)
F1 (limit, operability). The committed selftest has no case-count floor. case_dirs comes from iterdir (scripts/base_path_selftest.py:256-258), and "30" appears nowhere. P5 passes 29/29. The lane copy with 44 dirs passes 44/44.
F2 (limit, operability). The committed selftest compares exit, verdict and reason tuples only (matrix:14, "comparison"). Fixture bytes are not gated (P1, P6, P7). This matches its docstring; only a regeneration compare such as compare.py catches them.
F3 (drift in lane working tree, outside commit 7697990).
  a. 14 untracked case dirs X01–X14: git --no-optional-locks ls-files --others --exclude-standard → 42 files; tracked fixture files 87; diff -r against the commit → exit 1, only "Only in" lines for X01–X14. Not in the frozen matrix.
  b. Lane scripts/base_path_selftest.py differs from commit (cmp exit 1, 12-line diff). FINDING_KEYS adds "page" and "resolved" (lane:53), and pagesChecked/referencesChecked count checks (lane:212-217). Inert for the frozen 30 (grep for these keys in committed fixtures: exit 1). Active for X09 and X14 only.
  c. Lane scripts/base_path_audit.py differs (cmp exit 1, 7-line diff) in the --help text only (lane:127-149). No behaviour change seen.
  The lane's own scripts would report 44/44 on the lane tree, not 30/30. The L1 decides which tree counts toward the round. The commit bytes hold.

## Not verified
- Whether the X01–X14 expectations are correct. That belongs to the tool-behaviour seats.
- The C2 counter (c2_matrix_count.py) was not run; it is not my item.
- Mode bits checked only through ls-tree (100644). No ACL or xattr checks.
- X-file mtimes read as about 4 minutes old at check time, so the lane set may still change.
