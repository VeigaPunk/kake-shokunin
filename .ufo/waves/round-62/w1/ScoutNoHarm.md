# ScoutNoHarm — affected-file safeguards

## Observed scope

The frozen C1 counter `.ufo/waves/round-62/c62_calibration.py:9-17,31-43` reads exactly five committed blobs: `corpus/lessons/round-61-verifier-spotcheck.md`, `corpus/knowledge/response-header-expectations.md`, `corpus/QUALITY.md`, `corpus/lessons/round-62.md`, and `corpus/SOURCES.md`. It derives the disagreement count from S432+Disagree lines, correction from the exact substantive quote plus `S432 §3.6` and `Round-62 correction`, criterion from `substantive located quote` plus a pointer to the verifier spot-check, lesson gate from its declared tokens, and source-row presence from `| S432 |`. Only the source row, not every registry status cell or the knowledge entry's cited-source coverage, is counter-observed.

The extant disputed row is `corpus/lessons/round-61-verifier-spotcheck.md:30-36`; line 33 says Admit / Disagree, and lines 36-46 preserve the harm and route the correction. Keep these bytes and the row: the contract explicitly says not to mark it rejected. The cited S432 sentence is in `corpus/knowledge/response-header-expectations.md` current lines 71-87, where lines 77-80 are the generic lead-ins; the contract identifies the substantive §3.6 quote as `response header can be used to require checking of a response’s Content-Type header against the destination of a request`, located in retained `.ufo/waves/round-61/sources/S432.html:6151-6154`. `corpus/QUALITY.md:7-29` defines an append-only criterion history; its lines 28-29 specifically require append/supersede rather than erase earlier criteria. The round-62 contract also requires recording mistake and criterion in `corpus/lessons/round-62.md`, and its counter checks that lesson gate. `corpus/SOURCES.md` holds the source row; preserve the admitted S432 status per contract.

Coverage/score context: `PROVINCE.md:32-36` already locates response-header expectations in Frontier and explicitly limits them to record-bound audit, not universal policy or live cleanliness. `SCORECARD.md:3-7,15-19` declares calibration owned at score 2 and depth/coverage/adjacency outside scored ownership. No scorecard or province edit is required by frozen C1; extra scope must not be promoted to another claim (contract lines 11, 17-19).

## Read-only checks to detect unintended changes

Use the immutable base `c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13`; do not modify/run the frozen counter as an edit target. First confirm any measurement revision is the already-approved committed revision, then review the complete committed diff limited to the five counter inputs plus `PROVINCE.md` and `SCORECARD.md`:

```sh
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --stat c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 <measured-rev> -- corpus/SOURCES.md corpus/QUALITY.md corpus/knowledge/response-header-expectations.md corpus/lessons/round-61-verifier-spotcheck.md corpus/lessons/round-62.md PROVINCE.md SCORECARD.md
git -C /home/vgpnk/Projects/shokunin/kake-shokunin diff --find-renames --unified=3 c341a7a47b7ad91b2d3c3fd04adab72cd92ccb13 <measured-rev> -- corpus/SOURCES.md corpus/QUALITY.md corpus/knowledge/response-header-expectations.md corpus/lessons/round-61-verifier-spotcheck.md corpus/lessons/round-62.md PROVINCE.md SCORECARD.md
```

Inspect for: (a) S432's original registry row/status/used-by/recheck fields untouched; no new rejected status or replacement row; (b) round-61 verifier record byte-identical; (c) original knowledge and QUALITY content retained, with only intended correction/criterion additions; (d) no changes to PROVINCE coverage classification or SCORECARD score, evidence pointers, owned axes, or move history. Since the counter proves only that an S432 row exists, separately compare the whole SOURCES row and historical spot-check against base, not merely its `source_row=1` output. Append-only checks can compare base blobs to candidate with the exact authorized additions removed; use `git show <rev>:<path>` for committed blobs rather than worktree content.

Frozen result reference: contract line 15 records the pre-wave census command/output (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` -> `kake\tok\t.../corpus/SOURCES.md`, exit 0; 16 W04 duplicate-URL warnings, no row edits justified); line 19 names the only C1 counter and base control. After integration, preserve that base-control receipt and compare the committed after-state receipt to the frozen predicate; do not rerun or reinterpret a score as evidence that unrelated source-status, coverage-map, or score state stayed unchanged. No checks were run by this scout.

## Evidence commands

Commands used for this read-only report:

```sh
# Read via repository tools: contract.md lines 7, 15, 19; c62_calibration.py lines 9-17, 31-43;
# QUALITY.md lines 7-29; response-header-expectations.md lines 71-87;
# round-61-verifier-spotcheck.md lines 30-46; PROVINCE.md lines 32-36;
# SCORECARD.md lines 3-7, 15-19.
```

No source, counter, criterion, score, or score receipt was changed or executed.
