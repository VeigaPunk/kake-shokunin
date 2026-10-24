# ReviewScorecardLog35 — SCORECARD round-35 sections and LOG round 35 vs receipts

Attacked: every number, hash and revision in SCORECARD.md round-35 sections (capability row line 196; declared claims 1357-1429; controls 1431-1456; C2 counter version 2 1458-1495; measured results 1497-1525) and LOG.md round 35 (1460-1479) at the target revision, against the receipt files.

Method: lane files at 7deacc4 and HEAD (0d52173) are identical for SCORECARD.md and LOG.md (`git diff 7deacc4 HEAD --stat` touches only `w2`/spec files, no SCORECARD/LOG change). All checks read-only in the lane; counter re-runs in a sandbox clone (`/fast/scratch/hyaku/kake-r35/w2/ReviewScorecardLog35/clone3`, `git clone -q`, checked out at HEAD; TMPDIR under sandbox).

Re-runs (sealed counter, key-revision 4c6be2bd), all byte-for-byte identical to the committed receipts (JSON equality) and to stated exit codes:
- `python3 -B .ufo/waves/round-35/sealed_count.py c1 --root . --revision 16a6b8b8 --key-revision 4c6be2bd` → met false, passed 14/24, exit 1
- `... c2 --revision 16a6b8b8 ...` → met false, probes 0/12, exit 1
- `... c1 --revision b1cbbc39 ...` → met true, 24/24, exit 0
- `... c2 --revision b1cbbc39 ...` → met false, exit 1
- `... c1 --revision 95abec21 ...` → met true, 24/24, exit 0
- `... c2 --revision 95abec21 ...` → met true, probes 12/12, words 1388, copiedShare 0.0, goodCites S078 S079 S080 S082 S083 S084 S085 S086, exit 0
- `... c1|c2 --revision 4c6be2bd ...` → refused, "key visible at the measured revision", exit 2 (matches `verification/c1-at-4c6be2bd.json`)
- `python3 -B ...sealed_count_v1.py c2 --revision 95abec21 --key-revision 4c6be2bd` → met true, words 1298, exit 0

Statement list (support = receipt + code + re-run; all yes):
1. Base `16a6b8b8144f4d6e6187e9ecbb4fb5f4528b911a` — yes, object exists, receipts at it.
2. C1 before (passed 14 at 16a6b8b8 and bd14096a) — yes (`c1-at-16a6b8b8.json`, `c1-at-bd14096a.json`, re-run).
3. C1 after (24/24 at b1cbbc39 and 95abec21) — yes (`c1-at-b1cbbc39.json`, `c1-at-95abec21.json`, re-run).
4. C1 contract split "24 sealed cases (12 on the round-34 rules, 12 on the three repairs)" — yes: case groups R1 (4, og_url_multiple), R2 (5, template/svg/math suppression), R3 (3, page_unreadable continue) = 12 repair; G (12) = round-34 rules; per-case expectations match contract bullets (a)-(c).
5. C2 before (met false, probes 0/12 at 16a6b8b8, bd14096a, b1cbbc39) — yes.
6. C2 after at 95abec21 (entry present, 1388 <= 1500 words, copiedShare 0.0 <= 0.25, nine pinned texts intact, 8 >= 3 good cites S078-S099, probes 12/12 >= 9) — yes.
7. Selftest 45/45 at b1cbbc39 — yes (`verification/selftest-link-preview-at-b1cbbc39.txt`: cases 45, passed 45, failed 0, exit 0).
8. Round-34 matrix 28/28 at b1cbbc39 — yes (`c1r34-matrix-at-b1cbbc39.json`: 28/28, byKind 6/6+13/13+7/7+2/2, toolSha 1a8b2724…).
9. Controls pre-build at 318561ef (v1): C1 base/declaration/lookup dcef39b5/constant 14/14/7/7 of 24; C2 base/declaration/hollow 0cce15f0 probes 0; junk probes 0 (entry,size,copied,cites pass); keyword probes 3; transcript probes 8, copiedShare 0.9951; no control meets target — yes, every row matches `control-*.json` + `.exit` (all 1), and control commits exist in bundles (`retained/r35-control-*.bundle` heads 5f767534, 04848219, e5263d41, ae9fb361, c2e38e5d; round-34 bundles hold dcef39b5, 0cce15f0).
10. Version-2 section: v1 sha256 `c4d58dae…49ef` / v2 `1b4d9d59…469b` — yes (sealed_count_v1.py c4d58da…; sealed_count.py 1b4d9d59…; file at 81d9fd74 = v1); pins unchanged between versions (C1_KEY_SHA256 a861dccd…, C2_KEY_SHA256 111bceea… identical in both).
11. v1 critic bundles score 8 and 6 probes with other conditions passing — yes (`control-c2-critic-dilute-comment.json` probes 8, copied 0.0376; `control-c2-critic-zwsp-hiddenrows.json` probes 6, copied 0.0043; cites/size/entry true both); "one probe short of met" — yes (8 < 9).
12. Version-2 semantics implemented as described (comments + Unicode format chars removed; `[a-z0-9]+` words, cap 2200; cites = first `## Registry` section, fence-safe, id retained in `sources/receipts.json` with URL in row source cell, row mined dated 2026-10-22, used-by entry) — yes, `sealed_count.py` lines 197-281.
13. Every control rescored under v2 — yes (`control-v2-*.json`: C1 14/14/7/7; C2 base/declaration/hollow 0; junk probes 0 cites 1; keyword 3; transcript 8/0.9951; critic dilute 8/0.9781/cites 0; critic zwsp 8/0.9781/cites 0; reworded 6/0.0733/cites S078 S082 S083); new reworded bundle + critic bundles retained — yes.
14. Measured table, v1-at-95abec21 (met true, 12/12, 1298 words), reveal refusal exit 2, separability at b1cbbc39 (C1 24, C2 met false) — yes.
15. Landing provenance: repair patch sha256 `7e463fa7…3a13` applied byte-for-byte — yes: in sandbox, `git apply evidence/w1-tools/patch.diff` onto `16a6b8b8` tool (base blob cccc3a17…) yields tool sha 1a8b27243a00cede… = b1cbbc39 blob = receipt toolSha. Entry sha `0b5ac7e8…c397` landed unedited — yes: entry blob at 95abec21 and HEAD both 0b5ac7e8… (receipt entrySha256).
16. C2 rows S078-S087 "8 mined, 2 rejected", S006 re-opened used-by, S074 correction note, SKILL registry row fd0d53b2, dcef39b5 correction by append — yes (SOURCES.md rows S078 mined..S087 rejected; S006 used-by includes the entry; SOURCES.md:174 S074 note; SKILL.md:1035 gate registry; lessons/round-35.md:100 correction; criterion receipts `criterion-registry-row-at-fd0d53b2.txt` PASS, `at-318561ef.txt` FAIL, `criterion-control-description-r35-correction.txt` PASS, `r34-row4.txt` FAIL, `prebuild-leak-r34-c2…` FAIL — three checks shown able to fail).
17. Reveal commit adds only sealed keys + `l1-reference-patch-not-landed.diff`; it applies to the base tool and yields a different blob (99770908… vs landed 1a8b272…) — yes, "not landed" holds.

Findings by severity: none — no number, hash, revision or capability-row statement in the round-35 sections was found unsupported. All numeric claims reproduce from receipts and independent re-runs.

Notes (not findings): (i) control table "transcript … (1296 words)" vs receipt `words` 1303 — already reconciled in wave-1 `w1/ReviewControlReceipts.md:45-46` (body 1296 + 7-word title/header = 1303 descriptor; not a threshold claim). (ii) Pre-declaration sealing "outside the lane, mode 0700" and "neither seat read the keys" are process claims not independently auditable from repo state; the counter's exit-2 refusal on any revision holding a key and the absence of any sealed-key path in lane history before 4c6be2b (git log --all -- sealed/) are consistent with them. (iii) The "20-line reference patch" is a 64-line diff file; ~20 are substantive +/- lines (descriptor).

Residual risk / verification gaps: no live network checks (none claimed: C2 is offline-structural); entry-truth and row-truth read remains owed to the closure (disclosed limit); I did not re-verify every receipt's `.exit` file beyond checks (all consistent with JSON `met`/exit contract).
