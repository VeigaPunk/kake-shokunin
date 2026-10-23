# Round 38 wave 2 — ReviewHarm

Axes: operability and freshness. Attack: no-harm for base `af43a50fa399881eead9381d835b78a015e277a6` → tip `adab4c7e9ec2178657395f49346f18800ff4796f`, specifically the requested docs/corpus diff, all `scripts/*selftest*.py`, and round-36/37 rule-of-record counters.

## Verdict

- Targeted documentation/corpus edits remove no substantive prior content: **holds**. `git diff --numstat … -- SCORECARD.md SKILL.md PROVINCE.md LOG.md SHONEN.md corpus/` (exit 0): 9 files, 470 insertions, 4 deletions; `SHONEN.md` unchanged. The four deletions are two in-place SCORECARD row rewrites, S034's expanded `used-by`, and the knowledge-entry source header rewrite. The SCORECARD rows now say round-37 C1 is **not admitted** (`SCORECARD.md:198,2010`); the new lesson says C1 withdrawn and C2 is admitted for measurement, not as a fix (`corpus/lessons/round-38.md:10-21,63-74`).
- Prior operability instruments survive base→tip: **holds**. Both current round-36 and round-37 counters return 28/28 on each revision; all 7 selftests exit 0 on each revision, with the robots selftest expanded 137→194 and source-recheck hardening 6→9.
- Freshness prose is locally scoped and dated: **holds within this review scope**. The new source rows/lesson are dated 2026-10-23, state SHA pins and scope limits, and reject S101 as the contract source (`corpus/SOURCES.md:106-109`; `corpus/lessons/round-38.md:25-59`). External URLs were not independently re-fetched.
- No actionable finding in scope.

## Commands and results

`git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --numstat af43a50fa399881eead9381d835b78a015e277a6 adab4c7e9ec2178657395f49346f18800ff4796f -- SCORECARD.md SKILL.md PROVINCE.md LOG.md SHONEN.md corpus/` → exit 0. Reviewed the actual hunks with the same refs and path filter using `git diff --unified=1` → exit 0. No `lsp` device was mounted (`read xd://lsp`: “No such tool”; only ast_edit/debug mounted), so no references/definition/diagnostics requests were available; text search was not used as semantic proof.

In both sandbox clones, ran each `scripts/*selftest*.py` under `prlimit --as=4000000000 -- timeout 900 python3 -B`, after `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE`; `citing_set_selftest.py` also received `--tmpdir "$TMPDIR/citing-set"`, and `citing_set_hostile_selftest.py` received `--root "$PWD" --tmpdir "$TMPDIR/hostile"`. Logs (stdout+stderr) are in `/fast/scratch/hyaku/kake-r38w2/ReviewHarm/logs/{base,tip}/`.

| Selftest | Base exit/output (log SHA-256) | Tip exit/output (log SHA-256) |
|---|---|---|
| `base_path_selftest.py` | 0; 45/45; `f22b7337a6c8683467d29b53e8c994c78844d39abf1233e74ed49c2464d47d5a` | 0; 45/45; `f6a3ec355dff70426c41d9d221c22e20ea7b2171d4c1b14c7f8a9b00656c4a6f` |
| `citing_set_hostile_selftest.py` | 0; `passed:true`; `573cf7c3904feef460c3401f6d44ef3ac315a03b7f4b5c0e8aea1bd993c4a03f` | 0; `passed:true`; `eb547428487f88a8498ffd2bdc860e6495b6cde9e755f48a77b5e00582ad5f71` |
| `citing_set_selftest.py` | 0; 45 cases, 0 failed; `0f7b025098ee2a333d1d8bd0b0379280665418896c424e314160f59c30f5f366` | 0; 45 cases, 0 failed; `5810aa3285e3b9f8c6791e5f916d8ffed913b57aa2229e3330a2e3c83f307f6c` |
| `link_preview_selftest.py` | 0; 46/46; `eda0b75a930d6b61382e14e510e5196b4a8b2e6925337d82339828ff091c46aa` | 0; 46/46; `5796956b233d2a8ca485503bd4405478992011b8ee49300f7fdb7aa9a2d0045a` |
| `robots_audit_selftest.py` | 0; 137/137; `d2e0bcc4b42d8efb91fe8f4eae25de31d58512c11a55a674e07cf0b49961af1e` | 0; 194/194; `5a8b65f4b650ea3c68f79baca445aa11d8d44d5a9513824e0e2befee36252aea` |
| `source_recheck_hardening_selftest.py` | 0; 6/6; `6c1ed0b2d64087376080ce9186fba2d41d9472ac69b197d3ed3e18944dbc6bf4` | 0; 9/9; `a64f213a6126e489441997eae7e54b5697736d440e3bba35e85ea8104cce10e5` |
| `source_recheck_selftest.py` | 0; 106/106; `e238e8d66d3fe19ad97846a531088befd28fd3614057cc67a4a651c77f8e6355` | 0; 106/106; `b713aa80a0c2b1d0a7db35243737a0c72510e509faff960e5aa1bece0f339293` |

Counters ran from each clone with the same 4-GiB address-space limit and 900-s timeout:
- Round 36: `python3 -B .ufo/waves/round-36/sealed_count.py --root . --tool-file scripts/source_recheck.py --key-revision fd1fb723` → exit 0, 28/28, met true at base (tool SHA `4f8adbc23d314bbae9280190a83a2f985bfddb22d94b6135b133222818d47179`) and tip (tool SHA `6629d8000ac661ef7340137dc026cbdcc79ab0c81d845ed499376b4c1b0f9c6b`). Counter SHA `88ec59140258ce759107b7472fdd07a005b7c1bb8b3ba5218347e4518342ff8e`.
- Round 37: `python3 -B .ufo/waves/round-37/sealed_count.py --root . --tool-file scripts/robots_audit.py --key-revision 424aa248` → exit 0, 28/28, met true at base (tool SHA `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`) and tip (tool SHA `f4d057c4afac885b998de404da8c19f2d5d0a4d754a9d539e49b07d3f36baace`). Counter SHA `2ebb39b585e2a35f16ff71397f2fb22477a7a3c0e95da4415a26b0430b0cf0e3`.

Verification notes: an extra, superseded round-36 v2 counter attempt exited 2 because it pins the old key SHA (`a690…`), while the current v3 counter/key pin is `44c948…` (`.ufo/waves/round-36/sealed_count_v2.py:28-32`; current `sealed_count.py:34-41,60-65`); the current v3 result above is the rule-of-record run. The first exploratory hostile-selftest call omitted required `--root/--tmpdir` and exited 2; corrected calls above passed. One earlier citing-set invocation used its hardcoded default temp root `/fast/scratch/hyaku/kake-r27`; code removes that temp in `finally` (`scripts/citing_set_selftest.py:824-831`), and the observed temp path no longer exists. All final reruns used only the assigned sandbox TMPDIRs. No tools installed.