# ReviewHarm — round-40 harm review (operability, freshness)

Seat: KakeR40.ReviewHarm. Repo tip 6d5cd54a54d5098978f0e80eca510aa8f1c0b099, base f171c58b. Read-only git; sandbox /fast/scratch/hyaku/kake-r40res/ReviewHarm/. No tools installed (none needed; jq/jaq 3.1.1 and python3 present).

## Surfaces checked (command / exit)

1. Diff shape: `git -C repo diff --stat f171c58b 6d5cd54…` → 232 files, +60652/-4. `--diff-filter=DR --name-only` → empty (exit 0): no deleted/renamed files. `--numstat` over SCORECARD.md SKILL.md PROVINCE.md corpus/QUALITY.md corpus/README.md corpus/SOURCES.md LOG.md → only additions (LOG +18, SCORECARD +117, SKILL +14, QUALITY +25, SOURCES +6); PROVINCE.md, corpus/README.md absent = unchanged. Whole-repo deletion scan (`awk '$2!="0"'`): the only deletions are 4 lines inside scripts/sitemap_audit.py (+10/-4, tool diff 14 lines: U branch `_ENC_ATTR_RE` value guard at ~67, E NUL→xml_malformed at ~186, R duplicate-id guard at ~334 in `_evaluate_check`). Selftest +67/-0.
2. Other tools: sha256 sweep base-blob vs working tree over all scripts/*.py → only scripts/sitemap_audit.py and scripts/sitemap_audit_selftest.py differ; all other 17 .py identical. robots_audit.py sha256 f4d057c4… unchanged (matches SKILL.md line 1116).
3. Selftests at tip (from repo root, exit 0 both): robots `python3 -B scripts/robots_audit_selftest.py --tool scripts/robots_audit.py` → 204/204 clean; sitemap `python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` → PASS 179/179.
4. Real run: `sha256sum -c .ufo/waves/round-39/verification/realrun/inputs.sha256` → all 7 OK, exit 0. Rebuild at tip from read-only manifest (cwd /fast/scratch/hyaku/kake-r39a3w1/ScoutPublicSitemaps/realrun): `python3 -B <repo>/scripts/sitemap_audit.py --manifest manifest.json` → exit 1 (recorded round-39 build exit `build-565ef4c9.exit` = `exit=1`, identical). `jq -S .` sha256: new fd985a4186… == round-39 build fd985a4186…; canonical diff empty.
5. Tool identity: sha256sum scripts/sitemap_audit.py = 03a8fba4930ad7628a569e7aa30b3ece728fbb6eb3fa4ac7c9a78dfbeb07b22b == L1 reference declared in SCORECARD.md line 2604 and SKILL.md line 1139.
6. Scene cross-check: `.ufo/waves/round-40/verification/w1/*.json` = 76 receipts; `jq -s 'map(select(.met))|length' …` = 27 (exit 0) — matches "27 of 76". Extra 3 files are d1check-{base,ref,mutant}.txt (criteria receipts). `git status --porcelain`: 4 untracked wave artifacts (census-after.txt, resid-dispatch-*, sources/xmlschema11-2.html); no tracked dirty files.

## Verdicts (attacked statement: holds / overstated / wrong)
- "Deletions in the listed docs; --diff-filter=DR empty" — HOLDS (all doc files add-only; no deleted/renamed files).
- "Other tools unchanged except the two sitemap files" — HOLDS (17/19 scripts byte-identical; robots tool hash unchanged and its 204-fixture selftest passes).
- "Selftests at tip run clean" — HOLDS (robots 204/204, sitemap 179/179, both exit 0).
- "Real run at tip reproduces round-39 build" — HOLDS (byte-equal canonical JSON, same exit 1, inputs checksums verified).

## Findings
- No harm found on any surface the round touched: docs additions-only, one tool repair confined to the declared E/U/R branches (4 deleted lines inside it), selftest growth additive, real-run output byte-equal, robots/freshness tooling untouched (freshness-sweep, corpus-contract, source-recheck, citing-set, link-preview, canonical, base-path, live-snapshot, receipt-replay all unchanged bytes). SKILL.md/SCORECARD/QUALITY/SOURCES amendments are additions (SKILL.md:1139-1149 records the new tool hash; QUALITY (o)(q)(r) checks exist under criteria/ with receipts).
- Residual risk: I did not run the criteria checkers (preseal_order_check.py, d1_check.py) or the frozen counter — wave-1/C1-verdict territory, not harm; their check existence is confirmed only. Robots selftest exercised round-38/39 paths, not round-40 code (robots bytes unchanged). The 4 deleted tool lines are part of the declared repair; no behavioral delta observed on the six real-run hosts (repair classes E/U/R unsampled there).
