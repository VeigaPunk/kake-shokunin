## Verdict

C1 freshness, C2 operability, the validator selftest, the frozen matrix, live snapshots, and the archived domain page are distinct evidence classes; none substitutes for another. At candidate `4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc`, the named counters report C1 `0/17` and C2 `0/12` because the candidate revision has no required receipts. The current validator selftest passes and a direct current matrix run reports `32/32`, but the frozen replay currently cannot evaluate because a pinned input digest differs. Those test results do not satisfy either round-23 receipt population.

**One bounded move:** in the C2 handoff, report receipt/replay coverage separately from policy outcome counts—`clean`, `failed-policy`, `could-not-evaluate`, and `not-served`—without changing the frozen C2 acceptance semantics. Keep C1's claim-level receipt count separate. This improves **operability** by preventing “receipt accepted” from being read as “canonical policy passed”; it does not weaken **freshness**, because no C2 snapshot or round-22 artifact is counted as a C1 historical-claim observation. **Risk:** an aggregate receipt count can still be mistaken for policy success or independently attested GETs unless the four outcomes and producer-reported provenance remain visible. No code or contract edit is proposed here.

## Findings

### P1 — The round-23 receipt populations are not satisfied at the candidate

**Exact commands:**

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc
```

**Exact observed output (selected fields; every unit/surface row has the stated missing-receipt problem):**

```json
C1: {"accepted": 0, "revision": "4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc", "total": 17}
C1 first row: {"unit": "drift-detection", "pass": false, "problems": ["receipt missing"]}
C1 exit: 1

C2: {"accepted": 0, "revision": "4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc", "total": 12, "validatorSha256": "d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac"}
C2 first row: {"id": "ds4cc-primary", "pass": false, "problems": ["fetch.json or audit.json missing"], "verdict": null}
C2 exit: 1
```

**Impacted claims/axes:** C1/freshness requires claim receipts for 16 historical knowledge entries plus the property map; C2/operability requires committed snapshots and audit receipts for 12 surfaces. The frozen contract says so at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/contract.json:7-26`. The C1 population identifies its 17 units at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/c1-population.json:4-73`; C2 defines its 12 URL population at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/c2-population.json:4-79`. Both measurement scripts select files with `git show <revision>:...`, not the working tree: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py:34-44,101-118` and `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py:31-46,92-108`.

A live snapshot in the working tree is not enough to satisfy the measured candidate: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live/charter-ghp/fetch.json:1-12` records a GET, status 200 and a body digest, while `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live/charter-ghp/audit.json:1-8` records `clean`; the candidate counter still reports that its committed `fetch.json`/`audit.json` are missing. Smallest correction is to keep these axes separate and measure only after the corresponding C1 receipts and C2 per-surface artifacts are in the selected revision. This report does not claim admission or independently verified closure.

### P1 — Direct tests pass, but current frozen replay does not verify the current candidate

**Exact commands and observed output:**

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py --selftest
```

Output excerpt: `"name": "body_svg_after_head" ... "ok": true`, `"name": "body_math_after_head" ... "ok": true`, `"name": "body_void_selfclose" ... "ok": true`, and `"passed": true`. The implementation returns the clean selftest exit on that result (`/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py:904-968`). These are isolated local fixtures, not a network observation.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --json
```

Observed stdout prefix: `{"selection": "all", "accepted": 32, "total": 32, "executed": 32, "discrepancies": 0, "toolMissing": false, ...}`. The matrix's fixed case names are at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py:17-51`; it compares each run's exit and finding IDs to `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/cases.json` at `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py:257-294`. Its 32 frozen cases do not include the newer `body_svg_after_head`, `body_math_after_head`, or `body_void_selfclose` selftest cases (`/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py:815-821`), so neither suite substitutes for the other.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/replay.py --root /home/vgpnk/Projects/shokunin/kake-shokunin
```

Exact stdout: `{"verdict": "could-not-evaluate", "id": "snapshot_tampered", "error": "snapshot member digest mismatch"}`; exit `2`. The replay verifies every frozen member before invoking the matrix (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/replay.py:41-60`). The current validator hash is `d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac`; the frozen inputs map in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/frozen/expected.json:74` pins the repository file `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py` at `5de32200ea409349659180ab93d02d273c113008596d93834da94ef1c04a1c15`. Thus the direct 32/32 result is a current functional matrix run, but the frozen replay result is not current proof of the frozen input set. The smallest safe correction is to label the replay result as unavailable for this changed validator snapshot; any new digest baseline belongs to its authorized owner/round.

**Impact:** C2-related operability evidence is limited to the direct matrix's selected offline cases; this replay does not close C2 or C1. `/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:394-414` defines `canonical-audit` as a named-static-policy gate and calls the matrix/replay helpers evidence tools, not additional domain gates.

### P2 — C2 receipt acceptance is not synonymous with policy success or an independently proved GET

**Source inspection:** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py:36-39,42-84,102-108`.

**Exact observed code behavior:** the non-served branch accepts a matching `{"verdict":"not-served","status":...}` receipt without an HTML audit (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py:57-62`); a served page is accepted if its stored bytes hash matches and the revision's validator reproduces `audit.json` (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py:63-84`); top-level `pass` is `not problems` (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py:102-108`), not `verdict == "clean"`. The counter reads committed artifacts; it does not issue GETs. The producer does issue GET using `opener.open` and records URL, final URL, status, body digest and timestamp (`/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py:50-81`), then writes the metadata and audit receipt (`/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py:111-129`). Therefore, with complete committed receipts, the counter can reproduce an audit and validate metadata/byte consistency under trust in the producer; it cannot independently attest that the producer made the claimed request.

**Local observation:** `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live-summary.json:2-88` contains 12 outcomes: 1 `clean`, 3 `failed-policy`, 4 `could-not-evaluate` (`html_unsupported`), and 4 `not-served` (404). For example, `charter-ghp` is 200/clean (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live-summary.json:20-24`), while `vault-index-kimi` is 200/failed-policy with `canonical_missing` (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live-summary.json:42-48`). This snapshot summary is a point-in-time observation, not a claim that all 12 policies passed.

**Impacted claim/axis:** C2/operability—`accepted` currently denotes receipt consistency, including auditable negative and unsupported outcomes, not twelve policy-clean pages. The contract after-state requires one committed snapshot and audit receipt per surface (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/contract.json:21-26`), not that all audits be clean. Smallest correction is the bounded move above: preserve receipt coverage semantics, but show policy outcome counts separately and describe `GET` provenance as producer-reported.

### P2 — Counterexample: round-22 evidence was not exclusively synthetic

A broad assertion that round-22 canonical evidence was *only* synthetic fixtures is false. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/domain-snapshot/provenance.json:2-9` records an archived working file from source repository `/home/vgpnk/Projects/ufo-fsd-alpha`, specifically `/home/vgpnk/Projects/ufo-fsd-alpha/docs/charter-ufo-fsd/index.html`, at source commit `31c465f15669f744848bd9f5d56191c5085670f7`, with a SHA-256 checked against that commit's blob; it dates retrieval to 2026-10-20 and explicitly limits scope to a local static-source handoff. Its manifest sets the charter URL and expected canonical (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/domain-snapshot/manifest.json:4-8`). The recorded command in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/domain-integrated.json:3-14` returned exit `0` and stdout `{"findings":[],"pagesChecked":1,"verdict":"clean"}`.

This is evidence about one exact archived source artifact and the named local policy, not evidence that the live site served those bytes, that it remains current, or that Google selected that canonical. That limit is explicit in `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/domain-snapshot/provenance.json:7-9`, `/home/vgpnk/Projects/shokunin/kake-shokunin/PROVINCE.md:52-58`, and `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md:53-56,90-94`.

## Checked and held

| Evidence | Proves | Does not prove |
|---|---|---|
| Current validator selftest (`selftest.passed=true`; `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py:753-968`) | The listed in-code local cases produce their embedded expected exits/findings; includes the recent SVG, MathML and self-closed HTML cases. | Live URL reachability, current deployment, the C1 knowledge claims, or broad HTML5/browser conformance. |
| Current direct round-22 matrix (`32/32`, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/matrix.py:17-51,257-294`) | Current validator output agrees with the 32 named cases' expected exits/finding IDs. | Frozen-input integrity now; current replay exits `2`. It also does not test unlisted cases or any live surface. |
| Round-23 live records (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live-summary.json:2-88`, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live/charter-ghp/fetch.json:1-12`, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live/charter-ghp/audit.json:1-8`) | The local cache contains a point-in-time GET metadata record and a re-audited charter response, plus the listed outcomes for the population. | That these files are in candidate `4d95...` (the measured C2 counter says they are absent there), independent network attestation, or all-pages-clean status. |
| Round-22 archived source page (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/domain-snapshot/provenance.json:2-9`, `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-22/domain-integrated.json:3-14`) | One content-addressed source snapshot was checked against one manifest's static canonical policy at the recorded time. | A live response, present-day source state, HTTP headers/redirects, JS behavior, Google selection, or C1 freshness across 17 units. |
| Round-23 C1 receipts | Only the claim-level live observations and required verdict/correction/reason rows can serve C1; the counter checks base anchors and their round-23 citations (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py:39-90`). | Nothing in the round-22 tests, archive, or C2 page snapshots supplies those claim rows. Candidate currently measures `0/17`. |

The scope boundary is consistent with the corpus: the static preflight entry describes source-backed publisher policy and fixture proof (`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/README.md:42`), while the round-22 frontier leaves live delivery, headers, JS canonicals, Google selection and publication open (`/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/README.md:126-135`). The gate registry also says the canonical matrix/replay are evidence helpers, not additional domain gates (`/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:413-416`), and the freshness-sweep registry warns that offline/skipped checks are not complete publishing proof (`/home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md:208-212`).

## Limits

- No external HTTP request, account operation, publish, or source-tree mutation was performed in this review. Existing `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live/` files are treated as local cache evidence only.
- The candidate counter runs establish missing committed receipt coverage at the specified revision, not independent admission or the truth of any live-site content.
- No claim is made about Google-selected canonicals, redirects/headers beyond the saved producer metadata, JavaScript-rendered canonicals, or publication readiness.
- No tools were installed or updated. Only this report is written in the lane.
