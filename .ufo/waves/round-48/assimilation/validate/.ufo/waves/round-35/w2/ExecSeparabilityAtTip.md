# C1/C2 separability at the tip

Axes attacked: operability (C1) and freshness (C2).

## Variants
- Both variants were based on `95abec210c35eb17abffc16f8d39dbc6c6825fc5`, the parent of reveal `4c6be2bdec5630166c4013e53c226b1119ec63cc`, not lane tip `7deacc4629c1d05a34fb919d8095e99efc7b712f`. Per assignment, I used 95ab because the tip contains the revealed key; the counter refuses to score a revision containing a key.
- A: `2d9b1e2dcfbc3427860a608eefaeb3b7fdcf947a`; only `scripts/link_preview_audit.py` restored from `318561ef` (counter-reported `toolSha256=cccc3a17256aa4387a57e55b039257f8b3a3d0a9f34dd925f62f4c73bd33a4db`).
- B: `c468ba7d8a2655bd3ed925026bf8bdba286b2de2`; removed `corpus/knowledge/security-txt-publishing.md` and rows S078–S087 from `corpus/SOURCES.md`. Other 95ab content, including S006's used-by cell, was left unchanged.
- Both commits have 95ab as parent. Sandbox: `/fast/scratch/hyaku/kake-r35/w2/ExecSeparabilityAtTip/`.

## Four sealed scores
Each ran from the named worktree after `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r35/w2/ExecSeparabilityAtTip/tmp`, under `timeout 120s`; the printed `exit=` and process exit code agreed.

1. A-C1, cwd `.../A`: `timeout 120s python3 -B .ufo/waves/round-35/sealed_count.py c1 --root . --revision 2d9b1e2 --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc` — exit 1. Output: `met=false`, `passed=14/24`, target 22; revision `2d9b1e2dcfbc3427860a608eefaeb3b7fdcf947a`, counter SHA-256 `1b4d9d590b70f82c72e257006b77dc7232c43d7ccf1e5df51e892da2efb3469b`.
2. A-C2, cwd `.../A`: `timeout 120s python3 -B .ufo/waves/round-35/sealed_count.py c2 --root . --revision 2d9b1e2 --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc` — exit 0. Output: `met=true`, `probesPassed=12/12`, 1388 words, `copiedShare=0.0`, good cites S078 S079 S080 S082 S083 S084 S085 S086; entry SHA-256 `0b5ac7e83a622045a3c1a528e25c042ecb400b46309a09660ac0b500e6c0c397`.
3. B-C1, cwd `.../B`: `timeout 120s python3 -B .ufo/waves/round-35/sealed_count.py c1 --root . --revision c468ba7 --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc` — exit 0. Output: `met=true`, `passed=24/24`, target 22; revision `c468ba7d8a2655bd3ed925026bf8bdba286b2de2`, tool SHA-256 `1a8b27243a00cede1b93f8d3e95201476c75b70a3bcaa59a7e51f2220e5f5ef4`, counter SHA-256 as above.
4. B-C2, cwd `.../B`: `timeout 120s python3 -B .ufo/waves/round-35/sealed_count.py c2 --root . --revision c468ba7 --key-revision 4c6be2bdec5630166c4013e53c226b1119ec63cc` — exit 1. Output: `met=false`, `probesPassed=0/12`, 0 words, `copiedShare=1.0`, `entrySha256=null`, no good cites; revision `c468ba7d8a2655bd3ed925026bf8bdba286b2de2`.

Observed cross-results are orthogonal: A loses C1 while retaining C2; B retains C1 while losing C2. The counter SHA was v2 (`1b4d9d59…f3469b`) in all runs. No sealed key contents were read.

## Evidence, risks, blockers
- Contract/axes/targets and key-visibility refusal: `SCORECARD.md:1357-1377`; counter contract and refusal: `.ufo/waves/round-35/sealed_count.py:14-39,55-82`.
- Existing results and reveal reference: `SCORECARD.md:1497-1510`.
- Risk: these are deliberately 95ab-based variants, not A/B commits based on 7de; they establish separability only for the tested pre-reveal base. No other checks, builds, linters, or tests were run. No tools installed or updated. No blocker to the four requested scores.
- Lane changes: this report only. A/B implementation commits and working files remain in the sandbox listed above.
