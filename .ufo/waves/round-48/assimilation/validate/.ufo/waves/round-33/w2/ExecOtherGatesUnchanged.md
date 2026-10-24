# Round 33 W2 — other-gate comparison

Axes: operability and freshness. Compared archive exports of base `5777d5af79cac1ebf9144b348a9d274099e77338` and tip `0a0acfb1b2e74494ccc591e317f6a4c3e048f2a0`, both under `/fast/scratch/hyaku/kake-r33/w2/ExecOtherGatesUnchanged/{base,tip}`. Commands ran in their respective export roots; retained batch set `TMPDIR` to `/fast/scratch/hyaku/kake-r33/w2/ExecOtherGatesUnchanged/tmp/{base,tip}` and captured stdout/stderr plus an explicit exit line.

| Command | Base | Tip | Comparison / explanation |
|---|---|---|---|
| `python3 -B scripts/canonical_audit.py --selftest` | exit 0; `passed: true` | exit 0; `passed: true` | Exact receipts identical (cmp exit 0). |
| `python3 -B scripts/base_path_selftest.py` | exit 0; clean, 45/45 | exit 0; clean, 45/45 | Only tool/fixture absolute paths differ because exports have different roots; all remaining output matches. |
| `python3 -B scripts/citing_set.py --help` | exit 0 | exit 0 | Help output identical (cmp exit 0). |
| `node scripts/freshness-sweep.mjs --offline` | exit 1; `77 files · 597 occurrences`; 1 drift | exit 1; `78 files · 600 occurrences`; 1 drift | Same verdict and drift: missing `~/Projects/shokunin/.ufo/waves/round-29/w2/FieldsAndCounts.md`, unannotated at `corpus/lessons/round-29.md:102`. Tip adds `corpus/lessons/round-33.md`: relative-form cites 1266→1287 and set-delta files +21→+22. Other reported counts remain resolve 22, declaredAbsent 63, drift 1, unresolved 10; citation base 96, missSet 64. Export root strings differ. |
| `node scripts/corpus-contract.mjs --help` | exit 0 | exit 0 | Help output identical (cmp exit 0). |
| `node scripts/corpus-contract.mjs` (documented default check) | exit 0; 0 findings, 27 knowledge entries, 27 lane lessons, 17 skipped, 0 errors | exit 0; 0 findings, 27 knowledge entries, 28 lane lessons, 17 skipped, 0 errors | The only count change is the new round-33 lesson. |

Conclusion: no change in the canonical, base-path, citing-set CLI-help, or corpus-contract help results. Corpus contract remains clean; its lesson count rises as expected. Freshness keeps the same exit/verdict, not a pass: the pre-existing unannotated miss remains. Offline mode explicitly skips armed remote checks (`complete=false`); history is suspended for its pin-declared missing source, so this run makes no remote-freshness claim.

Evidence: outputs and comparisons are retained under `/fast/scratch/hyaku/kake-r33/w2/ExecOtherGatesUnchanged/evidence/`. Receipts: base/tip `canonical-audit.txt:1-2`, `base-path-selftest.txt:5-10,59-60`, `citing-set-help.txt:1-17`, `freshness-offline.txt:5-8,70-83`, `corpus-contract-help.txt:1-21`, and `corpus-contract-check.txt:20-21`. Comparisons: `comparison/canonical-cmp.txt:1`, `citing-set-help-cmp.txt:1`, `corpus-help-cmp.txt:1`, `base-path.diff:6-13`, `freshness-offline.diff:10-29`, `corpus-check.diff:14-17`. Hash ledger: `SHA256SUMS.txt:1-18`, SHA-256 `7744c7700707c0dd3fd5aa370d22e7c04b86e6047e93baaedf7a5536db31415c`.

Risk note: a preliminary pass preceded the retained batch and ran with ambient `TMPDIR` unset. `canonical_audit.py --selftest` uses `tempfile.TemporaryDirectory` (`scripts/canonical_audit.py:944`); that preliminary invocation returned 0, but its temp location was not recorded. The retained canonical results were rerun with sandbox `TMPDIR`. No live network requests or tool installs were made.