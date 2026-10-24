## Verdict

**Conclusive author-side C2 operability mutation probe; not independent admission.**

- Captured all 12 public surfaces with the requested read-only snapshot command, committed the snapshot in an isolated no-hardlinks clone, and measured **12/12 accepted, counter exit 0**.
- Committed five separate tampered variants, each directly derived from that passing baseline. The pristine counter rejected **all five**, each with **11/12 accepted, exit 1**, and exactly the intended `ds4cc-primary` failure.
- Applied **one counter mutant**, removing only the GET-method clause from the URL/method gate. The requested baseline-plus-five-tamper detector **SURVIVED** this mutant: all six detector cases still passed and their complete counter stdout SHA-256 values were unchanged.
- An additional method-only metadata witness **KILLED** that same mutant: pristine rejected HEAD-labelled metadata; mutant accepted it; exact restoration rejected it again. This is a **coverage gap in the five-tamper detector, not a demonstrated defect in the pristine counter**.
- Restored the exact original counter and baseline snapshot bytes. No production code, lane Git state, domain tree, publishing surface, or sibling file was modified. The only lane write is this report.

## Findings

### P2 — The five requested negative cases do not protect the GET-method clause

**Impacted claim/axis:** C2 / operability. The counter's receipt contract requires the population URL **and** method GET. A wrong-URL case covers only one side of that combined predicate.

**Counter mutant M1:** `/tmp/kake-r23-MutateCounterC2-dLpp/clone/.ufo/waves/round-23/measure_c2.py:52`:

```diff
-    if fetch.get("url") != surface["url"] or fetch.get("method") != "GET":
+    if fetch.get("url") != surface["url"]:
```

The unchanged following line still reports `fetch url/method does not match population GET`. No other counter behavior was changed. The detector executes this working-tree counter against fixed committed receipt revisions; the receipt variants themselves retain the original committed counter and validator.

**Expected detector:** baseline must return 0 with 12 accepted; each of the five requested receipt variants must return 1 with 11 accepted and only its intended single diagnostic. The same bounded detector was run on pristine, mutated, and restored counter bytes. It also requires total 12 and empty stderr, so a crash or unrelated rejection cannot masquerade as a killed receipt mutant.

**Exact primary-detector commands, in execution order:**

```sh
python3 /tmp/kake-r23-MutateCounterC2-dLpp/detect_counter.py --out /tmp/kake-r23-MutateCounterC2-dLpp/pristine.json
python3 /tmp/kake-r23-MutateCounterC2-dLpp/detect_counter.py --out /tmp/kake-r23-MutateCounterC2-dLpp/mutated.json
python3 /tmp/kake-r23-MutateCounterC2-dLpp/detect_counter.py --out /tmp/kake-r23-MutateCounterC2-dLpp/restored.json
```

Each command exited 0. Exact final stdout lines, respectively:

```text
{"counterSha256": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c", "detector": "PASS", "evidence": "/tmp/kake-r23-MutateCounterC2-dLpp/pristine.json"}
{"counterSha256": "1be045e1c8594ca60a9af857d4265c2e36b0ad36c59060cc2e05db62e54a2e7b", "detector": "PASS", "evidence": "/tmp/kake-r23-MutateCounterC2-dLpp/mutated.json"}
{"counterSha256": "ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c", "detector": "PASS", "evidence": "/tmp/kake-r23-MutateCounterC2-dLpp/restored.json"}
```

**Discriminating witness:** commit `c358d459a9247af78ac44025e02f66e473e910c0` changes only the existing live snapshot's metadata from `"method": "GET"` to `"method": "HEAD"`. It does not send a HEAD request or fetch any additional URL.

Exact witness commands, run at each of the same three counter states:

```sh
python3 /tmp/kake-r23-MutateCounterC2-dLpp/detect_counter.py --method-witness --out /tmp/kake-r23-MutateCounterC2-dLpp/pristine-method.json
python3 /tmp/kake-r23-MutateCounterC2-dLpp/detect_counter.py --method-witness --out /tmp/kake-r23-MutateCounterC2-dLpp/mutated-method.json
python3 /tmp/kake-r23-MutateCounterC2-dLpp/detect_counter.py --method-witness --out /tmp/kake-r23-MutateCounterC2-dLpp/restored-method.json
```

Exact case stdout, respectively:

```text
{"accepted": 11, "case": "method-HEAD", "detectorCase": "PASS", "failed": [{"id": "ds4cc-primary", "pass": false, "problems": ["fetch url/method does not match population GET"], "verdict": "clean"}], "returncode": 1, "revision": "c358d459a9247af78ac44025e02f66e473e910c0", "stdoutSha256": "43224d674a532acbb4aae06478a262ac8a8fbfc1b010235ebcff195d07294e78", "total": 12}
{"accepted": 12, "case": "method-HEAD", "detectorCase": "FAIL", "failed": [], "returncode": 0, "revision": "c358d459a9247af78ac44025e02f66e473e910c0", "stdoutSha256": "a5a73e5caac1bd46391c1bf76a217143741b135774887af2a480e680d7fb857c", "total": 12}
{"accepted": 11, "case": "method-HEAD", "detectorCase": "PASS", "failed": [{"id": "ds4cc-primary", "pass": false, "problems": ["fetch url/method does not match population GET"], "verdict": "clean"}], "returncode": 1, "revision": "c358d459a9247af78ac44025e02f66e473e910c0", "stdoutSha256": "43224d674a532acbb4aae06478a262ac8a8fbfc1b010235ebcff195d07294e78", "total": 12}
```

The witness detector exited **0 / 1 / 0**; the underlying counter exited **1 / 0 / 1**. Thus the witness kills M1, with no baseline failure and no inconclusive result.

**Smallest fix:** add this method-only committed receipt case to the permanent behavioral detector, expecting counter exit 1 and the existing URL/method diagnostic. Keep the production GET clause and frozen contract unchanged. No production or permanent-test edit was made by this probe.

## Checked and held

### Isolation and provenance

Exact clone command:

```sh
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r23-MutateCounterC2-dLpp/clone
git -C /tmp/kake-r23-MutateCounterC2-dLpp/clone rev-parse HEAD
```

Observed initial clone HEAD:

```text
4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b
```

The clone was then explicitly pinned, without changing the lane, to the assigned candidate:

```sh
git -C /tmp/kake-r23-MutateCounterC2-dLpp/clone switch --detach 4d95d2e9a7fa41735b064ebfd92ce1a25e84b0cc
```

Observed output:

```text
HEAD is now at 4d95d2e round-23: evaluate body-only SVG/MathML and void self-closing tags; read-only live snapshot tool
```

The lane producer, cloned candidate producer, counter, and validator were fingerprinted before the probe. Lane and pinned-clone source hashes matched:

| Input | SHA-256 |
| --- | --- |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py` | `ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c` |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py` | `0475a3c4540ebb97054e48b67736ed9589dc91d1baba65cc8610ad61682d71cc` |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py` | `d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac` |
| `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/c2-population.json` | `ac58c80fda73cae194fcc75bf56f62b19ea5443048ddf822fcee8d08e7c75d98` |

### Live baseline

Exact command, working directory `/tmp/kake-r23-MutateCounterC2-dLpp/clone`:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py --population /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/c2-population.json --out /tmp/kake-r23-MutateCounterC2-dLpp/clone/.ufo/waves/round-23/live
```

It completed successfully. Its observed surface data were:

| Surface | Status | Verdict | Findings |
| --- | --- | --- | --- |
| ds4cc-primary | 200 | clean | [] |
| plazir15-ghp | 200 | clean | [] |
| charter-ghp | 200 | clean | [] |
| ds4cc-kimi | 200 | failed-policy | canonical_missing |
| burnerchrome-kimi | 200 | failed-policy | canonical_missing |
| vault-index-kimi | 200 | failed-policy | canonical_missing |
| plazir27-kimi | 404 | not-served | [] |
| ufo-fsd-kimi-pro | 200 | failed-policy | canonical_missing |
| lucario-ghp | 200 | failed-policy | canonical_missing |
| lucario-kimi | 404 | not-served | [] |
| plazir15-kimi | 404 | not-served | [] |
| charter-kimi | 404 | not-served | [] |

The chosen served target recorded `"fetchedAt": "2026-10-21T06:57:47Z"`, `"bytes": 76159`, `"status": 200`, `"method": "GET"`, and `"contentType": "text/html; charset=utf-8"`.

Exact baseline commit command:

```sh
git -C /tmp/kake-r23-MutateCounterC2-dLpp/clone add -f /tmp/kake-r23-MutateCounterC2-dLpp/clone/.ufo/waves/round-23/live
git -C /tmp/kake-r23-MutateCounterC2-dLpp/clone -c core.hooksPath=/dev/null -c commit.gpgsign=false -c user.name=MutateCounterC2 -c user.email=mutatecounterc2@invalid commit -m 'probe: commit live C2 baseline snapshots'
git -C /tmp/kake-r23-MutateCounterC2-dLpp/clone rev-parse HEAD
```

Observed commit: `f581c3aacab3a63ff594a3dd8420dd15d0c71c85` (40 files).

Exact first baseline measurement:

```sh
python3 /tmp/kake-r23-MutateCounterC2-dLpp/clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r23-MutateCounterC2-dLpp/clone --revision f581c3aacab3a63ff594a3dd8420dd15d0c71c85
```

Counter exited **0**, with exact output fields `"accepted": 12`, `"total": 12`, and `"validatorSha256": "d8acf75062ab61006a5fdf786d04deb0d54d0d15f19e11be09a80b57aa74ecac"`; every surface had `"pass": true` and `"problems": []`. Acceptance is reproducible receipt acceptance, **not** a claim that all pages have clean canonical policy: five honestly reproduced receipts are `failed-policy`, and four are `not-served`.

### Committed receipt mutants

All mutations below affect only `/tmp/kake-r23-MutateCounterC2-dLpp/clone/.ufo/waves/round-23/live/ds4cc-primary/`. Each commit has the clean live baseline as its parent; none accumulates a prior tamper. The clone was switched back to the committed baseline between variants and before the counter mutation.

| Case | Exact change | Committed revision | Counter result in pristine / M1 / restored |
| --- | --- | --- | --- |
| edited-page | Append `<!-- mutation probe: altered committed page bytes -->` to served bytes without changing the fetch digest | `504da68a44749344203adbc5f53708da194b8990` | 1, 11/12 / 1, 11/12 / 1, 11/12 |
| edited-audit | Change `pagesChecked` from 1 to 2, preserving `verdict: clean` | `8880874095216c5f22e3359199746dc9d177920d` | 1, 11/12 / 1, 11/12 / 1, 11/12 |
| served-relabelled-not-served | Replace the audit with `{"error":null,"exit":null,"status":200,"verdict":"not-served"}`, retaining the served fetch metadata and page bytes | `53eb4c0f595936d4cac6d72093d2289fd1c80f9e` | 1, 11/12 / 1, 11/12 / 1, 11/12 |
| wrong-url | Change only metadata `url` to `https://example.invalid/`; no request to that URL | `ed80e048995ffc9ab1dc0b2584eb7910cf167c46` | 1, 11/12 / 1, 11/12 / 1, 11/12 |
| stale-fetchedAt | Change `2026-10-21T06:57:47Z` to `2026-10-20T06:57:47Z` | `d6759677bc9c2b037f5f8dfd463fa944f3e09357` | 1, 11/12 / 1, 11/12 / 1, 11/12 |

Exact observed diagnostic strings, in table order; these were identical in all three counter states:

```text
page.html missing or digest differs from fetch.sha256
audit.json {'exit': 0, 'result': {'findings': [], 'pagesChecked': 2, 'verdict': 'clean'}} != reproduced {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}}
audit.json {'error': None, 'exit': None, 'status': 200, 'verdict': 'not-served'} != reproduced {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}}
fetch url/method does not match population GET
fetchedAt missing or before 2026-10-21
```

Complete counter stdout hashes in pristine, M1, and restored runs were identical for every primary-detector case:

| Case | SHA-256 of exact counter stdout |
| --- | --- |
| baseline | `c096f7f2449853ba855b7dbaa4109c15d362f1bbb6ed34f98310732311615dfd` |
| edited-page | `9e70362184dec670c01a45f102e59a1e4e40e7a7e76be1838127a41733bf1148` |
| edited-audit | `5566ae529b2f482457753eec96aa2660490dc48e5e6584e0fc8b6bfacc8fa5b6` |
| served-relabelled-not-served | `cacaeefcf49c6d87b793c5c76a6141cafd4f4913ea60858b9de3b2649370d99b` |
| wrong-url | `419bc24257e7a7b5491759ac33581a2dea2705671fbd3f79159225e3c77c007a` |
| stale-fetchedAt | `da10c107a330777c8b2b60a6e4e9346547dae4adbad28a9c81faf0e199b10294` |

### Byte restoration evidence

Counter SHA-256, before / mutated / restored:

```text
ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c
1be045e1c8594ca60a9af857d4265c2e36b0ad36c59060cc2e05db62e54a2e7b
ec7c246f61fa8d03242115a31aba651e57f3a115377d49c11acb7e48dd721e4c
```

Original committed snapshot hashes equal the final restored working-tree hashes:

| Restored absolute path | Original = restored SHA-256 |
| --- | --- |
| `/tmp/kake-r23-MutateCounterC2-dLpp/clone/.ufo/waves/round-23/live/ds4cc-primary/page.html` | `ccb3f46eda1ce3270df1e3373d49c4034025c4f475a6999142279e03b00b2bb8` |
| `/tmp/kake-r23-MutateCounterC2-dLpp/clone/.ufo/waves/round-23/live/ds4cc-primary/audit.json` | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` |
| `/tmp/kake-r23-MutateCounterC2-dLpp/clone/.ufo/waves/round-23/live/ds4cc-primary/fetch.json` | `3efd970611cf108cddfc26666ff7f58b8e871e87c9ae5ae31a220e91dcfbe1b1` |

Tampered byte hashes, read from the actual committed variants:

| Case | Tampered SHA-256 |
| --- | --- |
| edited-page | `890487d7cf46ff5e7fd0ac721536de78a384f3d4dc145075c7e154a08b9120b7` |
| edited-audit | `63b594ae724edd78925c78375f9ffdf5619c7518ef50086c940211ed7c0629c4` |
| served-relabelled-not-served | `a405ed9e28fc62d27d3ad0d9a54e2aae5b9d34f8afa4dfb9330eb4288935a8a9` |
| wrong-url | `9e8883188b3be1f2f4cfb99737f53105b1024d8f834e57fa4678b647364976f3` |
| stale-fetchedAt | `00a2e39c1e3158c9ae637cad95893f252d439210530d5a3afc540a5958921c81` |
| method-HEAD witness | `08869552089e8b78bf5c093257872b9525306ce2b141ee9a45b441bcd3724516` |

Restoration was performed immediately after both mutant runs, including the witness's intentional detector exit 1, before running the identical restored detector and witness. The clone remains at the committed live baseline. Snapshot variants are retained by clone-only `refs/heads/probe/` refs.

### Retained evidence

All raw counter stdout, stderr, full per-case commands, return codes, summaries, and counter hashes are recorded in:

- `/tmp/kake-r23-MutateCounterC2-dLpp/pristine.json`
- `/tmp/kake-r23-MutateCounterC2-dLpp/mutated.json`
- `/tmp/kake-r23-MutateCounterC2-dLpp/restored.json`
- `/tmp/kake-r23-MutateCounterC2-dLpp/pristine-method.json`
- `/tmp/kake-r23-MutateCounterC2-dLpp/mutated-method.json`
- `/tmp/kake-r23-MutateCounterC2-dLpp/restored-method.json`

The exact detector is `/tmp/kake-r23-MutateCounterC2-dLpp/detect_counter.py`. Per-variant before/tampered/restored byte hashes are `/tmp/kake-r23-MutateCounterC2-dLpp/hash-evidence.json`. All detector evidence is scratch-only; no detector or mutant was integrated into the lane.

## Limits

- This is one scoped mutation probe, not an independent admission, integration, policy repair, or exhaustive counter audit. Only the five requested negative cases and one method-only discriminating witness were exercised.
- The served-to-not-served case relabels the audit while retaining the original successful fetch and page. It does not fabricate matching 404 metadata, rewrite an entire provenance chain, or establish resistance to every possible coordinated forgery.
- Network activity was limited to the requested producer's public read-only GETs and its redirects. No auth, cookies, forms, POST, publishing, deploy, account, DNS, Kimi chat, upstream source edit, or service action was performed.
- The snapshot is evidence of bytes served at fetch time, not a future guarantee or search-engine canonical decision. Canonical-policy failures were reproduced, not repaired.
- No builds, lint, formatters, broad test suites, additional agent runtimes, or subagents were invoked.
- The first attempt to submit the snapshot command with asynchronous execution was not launched: `Background job limit reached (100). Wait for running jobs to finish or cancel one.` The synchronous invocation then completed in 20.43 seconds. This scheduling refusal was not a failed behavioral baseline.
- Tools used were already installed: exact version output `Python 3.14.8` and `git version 2.56.0`. No tools were installed or updated; no pacman transaction occurred.
