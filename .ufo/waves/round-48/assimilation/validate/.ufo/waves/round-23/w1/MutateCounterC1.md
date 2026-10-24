## Verdict

**Freshness / r23-build: all six deliberately bad receipt cases were rejected by pristine bytes; five of six single-guard mutants were killed, one survived, zero were inconclusive.**

The surviving mutant disables only the explicit missing-heading check. It still rejects the heading-less receipt through the citation-in-section check. This is an acceptance-oracle coverage/equivalence finding, not evidence that pristine code accepts an invalid receipt. Every mutant was restored before the next mutation; the same detector was run on pristine, each mutated state, and each restored state.

Author-side scoped mutation evidence only; no independent admission, integration, deployment, or contract change.

- Read-only lane counter: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py`.
- Isolated clone: `/tmp/kake-r23-MutateCounterC1-ZrEA/clone` (created with `git clone --no-hardlinks`).
- Observed clone HEAD before fixtures: `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`.
- Frozen base for anchors: `b5d599e19bead54b96f589444e9ec64cdf67c28a`.
- Synthetic all-valid control commit: `c45356b2db67b95d42277689c1684f138fefb20a`.
- Deliberately bad probe commit: `53f36e8a4687f021f2f2a2a7f782f57497151e28` (parent is the all-valid control).
- Full commands, exact stdout/stderr, return codes and hashes: `/tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/runs.json`.
- Detector committed in the probe at `/tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py`; SHA-256 `4af8ff987f4e0c58cc150f256002ff5bf55098852037ab56938f8fa4e4d95679`.

## Findings

### P3 — dropping the explicit heading guard survives the rejection-only oracle

**Mutant:** `/tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py:64`, replacing `if position < 0:` with `if False:`. No other source line changed in that mutant.

**Expected detector:** valid revision exits 0 and accepts 17/17; bad revision exits 1, rejects each of the six named bad units, and accepts exactly the other 11. The detector checks individual unit acceptance, not merely aggregate exit status, and does not require diagnostic equality. Each counter invocation has a 30-second timeout.

**Exact executed detector command:**

```bash
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/mutant-drop-heading.json
```

**Observed output:** detector exit `0`; counter exits `0` for the good revision and `1` for the bad revision; accepted counts `17` and `11`; `falseAccepts` is empty; detector verdict is `SURVIVED`. Exact stdout follows:

```text
{"badAccepted": 11, "badExit": 1, "counterSha256": "8e86b0fbfd8c97c6bdf7303f48051504b50063ea776b87840c2ab8fef5113dbe", "detectorPass": true, "falseAccepts": [], "fixtures": {"anchor-absent-at-base": {"problems": ["claim c1: anchor not in unit at base"], "rejected": true, "unit": "fire-journal-codes"}, "duplicate-ids": {"problems": ["claim c1: duplicate id"], "rejected": true, "unit": "ghp-subpath-spotcheck"}, "missing-heading": {"problems": ["claim c1: not cited in round-23 section", "claim c2: not cited in round-23 section", "claim c3: not cited in round-23 section"], "rejected": true, "unit": "drift-detection"}, "observedAt-2026-10-20": {"problems": ["observedAt missing or before 2026-10-21"], "rejected": true, "unit": "keeper-timer-inert"}, "stale-correction-absent-in-section": {"problems": ["claim c1: correction not in round-23 section"], "rejected": true, "unit": "fleet-registry"}, "wrong-unit": {"problems": ["unit/path mismatch"], "rejected": true, "unit": "free-read-verbs"}}, "goodAccepted": 17, "goodExit": 0, "positiveControl": true, "unrelatedUnitsAccepted": true, "verdict": "SURVIVED", "wellFormedBadResult": true}
```

The pristine missing-heading case reports `"round-23 heading missing in unit file"` plus three `"claim cN: not cited in round-23 section"` problems. The mutant removes only the first diagnostic; all three citation failures remain. Specifically, no heading makes `section` empty, nonempty claims require nonempty ids, and their citation tokens cannot occur in an empty section.

**Impacted claim/axis:** C1 freshness, specifically sensitivity of an acceptance/rejection detector to deleting the explicit heading diagnostic. No false acceptance was observed for this mutant.

**Smallest fix:** no production or contract relaxation. If the explicit diagnostic itself must be mutation-detected, assert the missing-heading diagnostic for this case in addition to rejection. Under the assigned behavior-only oracle, retain this survivor as redundant with the citation guard; do not describe it as a killed behavioral mutant.

### Baseline bad-receipt observations

All 17 units have three synthetic claims in the positive control. Six units have one deliberate defect each in the probe revision; the missing-heading and correction-placement defects are in the receipt-associated unit file. All 17 receipt JSON files remain committed under the clone receipt directory. These fixtures explicitly say they are synthetic and are not live re-verification receipts.

Receipt directory: `/tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/receipts`.

| Bad case | Unit | Deliberate defect | Exact pristine problem output |
|---|---|---|---|
| missing-heading | drift-detection | Required heading removed from the unit; all three citation tokens remain. | `round-23 heading missing in unit file`<br>`claim c1: not cited in round-23 section`<br>`claim c2: not cited in round-23 section`<br>`claim c3: not cited in round-23 section` |
| anchor-absent-at-base | fire-journal-codes | Only c1 anchor replaced with `MUTATION-ONLY-NOT-IN-BASE: fire-journal-codes-anchor-absent-2026-10-21`. | `claim c1: anchor not in unit at base` |
| stale-correction-absent-in-section | fleet-registry | c1 remains STALE with nonempty correction in receipt; identical correction moved before the required heading in the unit. | `claim c1: correction not in round-23 section` |
| wrong-unit | free-read-verbs | Receipt unit changed to `wrong-unit-for-mutation-probe`; path and citations remain correct. | `unit/path mismatch` |
| duplicate-ids | ghp-subpath-spotcheck | Second claim id changed from c2 to c1; c1 citation already present. | `claim c1: duplicate id` |
| observedAt-2026-10-20 | keeper-timer-inert | Receipt observedAt changed from 2026-10-21 to 2026-10-20. | `observedAt missing or before 2026-10-21` |

### Mutant outcomes

Each guard was independently replaced with `if False:` (or `elif False:` for correction placement), followed by an exact one-line restoration. The good control accepted 17/17 with exit 0 in every run. All bad-revision counter invocations exited 1, including killed mutants: **using exit status alone would have missed all five false acceptances.**

| Mutant / original line | Bad accepted | False-accepted case | Detector exit | Verdict |
|---|---:|---|---:|---|
| mutant-drop-heading / 64 | 11/17 | none | 0 | SURVIVED |
| mutant-drop-base-anchor / 79 | 12/17 | anchor-absent-at-base | 1 | KILLED |
| mutant-drop-stale-section / 87 | 12/17 | stale-correction-absent-in-section | 1 | KILLED |
| mutant-drop-unit-path / 51 | 12/17 | wrong-unit | 1 | KILLED |
| mutant-drop-duplicate-id / 71 | 12/17 | duplicate-ids | 1 | KILLED |
| mutant-drop-observed-at / 53 | 12/17 | observedAt-2026-10-20 | 1 | KILLED |

Exact source mutations (only one pair active at a time):

```diff
--- /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py
+++ /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py (each independent mutant)
@@ line 64: mutant-drop-heading @@
-    if position < 0:
+    if False:
@@ line 79: mutant-drop-base-anchor @@
-        if claim["anchor"] not in base_text:
+        if False:
@@ line 87: mutant-drop-stale-section @@
-            elif correction not in section:
+            elif False:
@@ line 51: mutant-drop-unit-path @@
-    if receipt.get("unit") != unit["unit"] or receipt.get("path") != unit["path"]:
+    if False:
@@ line 71: mutant-drop-duplicate-id @@
-        if claim["id"] in seen:
+        if False:
@@ line 53: mutant-drop-observed-at @@
-    if not isinstance(receipt.get("observedAt"), str) or receipt["observedAt"][:10] < "2026-10-21":
+    if False:
```

## Checked and held

**Explicitly exercised detector commands:** each command below invokes exactly the same committed detector and the same good/bad commit pair. Its log contains both full underlying counter commands, full counter output and stderr.

```bash
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/pristine.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/mutant-drop-heading.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/restored-drop-heading.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/mutant-drop-base-anchor.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/restored-drop-base-anchor.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/mutant-drop-stale-section.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/restored-drop-stale-section.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/mutant-drop-unit-path.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/restored-drop-unit-path.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/mutant-drop-duplicate-id.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/restored-drop-duplicate-id.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/mutant-drop-observed-at.json
python3 /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/detect_c1.py --root /tmp/kake-r23-MutateCounterC1-ZrEA/clone --counter /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py --good c45356b2db67b95d42277689c1684f138fefb20a --bad 53f36e8a4687f021f2f2a2a7f782f57497151e28 --log /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe/restored-drop-observed-at.json
```

**Actual detector results:**

| Run / log basename | Detector exit | Good counter (exit, accepted) | Bad counter (exit, accepted) |
|---|---:|---|---|
| pristine.json | 0 | 0, 17/17 | 1, 11/17 |
| mutant-drop-heading.json | 0 | 0, 17/17 | 1, 11/17 |
| restored-drop-heading.json | 0 | 0, 17/17 | 1, 11/17 |
| mutant-drop-base-anchor.json | 1 | 0, 17/17 | 1, 12/17 |
| restored-drop-base-anchor.json | 0 | 0, 17/17 | 1, 11/17 |
| mutant-drop-stale-section.json | 1 | 0, 17/17 | 1, 12/17 |
| restored-drop-stale-section.json | 0 | 0, 17/17 | 1, 11/17 |
| mutant-drop-unit-path.json | 1 | 0, 17/17 | 1, 12/17 |
| restored-drop-unit-path.json | 0 | 0, 17/17 | 1, 11/17 |
| mutant-drop-duplicate-id.json | 1 | 0, 17/17 | 1, 12/17 |
| restored-drop-duplicate-id.json | 0 | 0, 17/17 | 1, 11/17 |
| mutant-drop-observed-at.json | 1 | 0, 17/17 | 1, 12/17 |
| restored-drop-observed-at.json | 0 | 0, 17/17 | 1, 11/17 |

All log files are under `/tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/mutation-probe`; all counter and detector stderr strings were exactly empty (`""`).

**Before/mutated/restored SHA-256 evidence:** the before digest for the first mutant is the pristine run; each subsequent before state is the preceding restored run. All six restores were exercised, not inferred.

| Mutant | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 |
|---|---|---|---|
| mutant-drop-heading | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` | `8e86b0fbfd8c97c6bdf7303f48051504b50063ea776b87840c2ab8fef5113dbe` | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` |
| mutant-drop-base-anchor | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` | `d9b37a869f8ad2c6cc0232ab77c13d289d0f737e125657b393a50d7c75560099` | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` |
| mutant-drop-stale-section | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` | `677295aa63938f6f2ca2da76516098c4d0db0161f3d87a3a172a8676434cb6ee` | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` |
| mutant-drop-unit-path | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` | `d54c3d4f2bd8cf8bd39102f7538025c52f34c752334d4a6afef19329e8057c15` | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` |
| mutant-drop-duplicate-id | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` | `2559fa8b933a2d47d2ae3171865d79eaa7216d35137cb7ac5912cd7d3859e67e` | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` |
| mutant-drop-observed-at | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` | `fd3104aa5f4b4678b081c82cf1093c8a5fa465ce7cf03d7497e9c0194ebdbd3e` | `89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe` |

Final actual restoration output:

```text
counter_matches_initial_clone_git_blob=true
all_restored_summaries_equal_pristine=true
```

All six restored detector stdout/stderr/exit triples also match the pristine observation byte-for-byte: `true` (comparison of captured outputs, no additional counter invocation).

Final actual `sha256sum` output for counter bytes:

```text
89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe  /tmp/kake-r23-MutateCounterC1-ZrEA/clone/.ufo/waves/round-23/measure_c1.py
89564ca584a45aa6c9082c2bb02995f535aa0a11df7bc8275ecb2d75b81839fe  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py
```

Frozen population SHA-256: `ffc9b3a44ee84ed827f3badc697f0ae5c8be007a50de3cafc2ccd23617697daf`. The population was never edited.

## Limits

- This is a structural freshness-counter mutation probe, not live HTTP re-verification of any C1 historical claim. Synthetic control receipts are not admission evidence and must not be integrated as real receipts.
- The six assigned cases are covered. Receipt path mismatch alone, missing correction field, malformed/future date formats, unknown verdicts, missing fields, malformed JSON, UNVERIFIABLE reason handling, and population tampering were not separately mutation-tested here.
- The wrong-unit mutant disables the existing combined unit/path guard, but the bad fixture changes only unit. The STALE fixture retains a nonempty correction and places it before the heading, specifically testing section placement rather than correction presence.
- The survivor changes a diagnostic without changing acceptance for the assigned case. This probe does not establish every other heading-related parser behavior.
- All source/index/commit mutations occurred only inside the isolated clone. The lane received only this scoped report. Counter bytes were restored exactly; synthetic commits and raw logs are deliberately retained in the scratch clone for reproduction, not offered for integration.
- No subagents, other agent runtime, HTTP requests, publish/deploy actions, builds, linters, formatters or unrelated test suites were invoked.
- No tool was installed or upgraded. Existing `python3` reported exactly `Python 3.14.8`; Git and sha256sum were existing tools. No pacman transaction or service restart was attempted.
- No independent admission or shipping judgment is asserted.
