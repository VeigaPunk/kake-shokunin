## Verdict

**Operability / C2, r24-build: 12 isolated one-point mutants probed; 4 killed, 8 survived, 0 inconclusive. Two survivors are behaviorally equivalent slice deletions, leaving six non-equivalent coverage findings.** This is author-side mutation evidence, not independent admission.

The unchanged round-23 detector passed all 28 cases on the pristine frozen revision and after each of the 12 exact-byte restorations. Its eight surviving mutant runs also passed all 28 cases. The four killed runs exited 1. No baseline failure was credited as a kill.

The maintained replay selftest should distinguish the six non-equivalent survivors: missing timestamp string guards in both counters, missing HTML comparison, missing lower HTTP-status bound, missing `error is None` classification guard, and missing truncation guard. It cannot behaviorally kill the two equivalent `[:10]` deletions; those must not become impossible acceptance criteria.

## Findings

### P2 — timestamp type guards can disappear without the detector noticing

Impacted claim/axis: C2 / operability. Source locations:

- C1: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py:55`.
- C2: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py:56`.

M05 deleted `not isinstance(receipt.get("observedAt"), str) or `; M06 deleted `not isinstance(fetch.get("fetchedAt"), str) or `. Each mutant exited 0 with all 28 detector cases passing and empty stderr. The existing timestamp negative cases only supply the string `2026-10-20`; they do not exercise missing/non-string timestamp values.

Smallest selftest improvement: exercise missing and non-string timestamps for each replay target, requiring rejection with exit 1 or 2, valid diagnostic output, and no Python traceback. Retain positive boundary controls. These proposed additions were not run here; their ability to kill M05/M06 is [INFERENCE] from the changed expression, not an additional measured case result.

### P2 — HTML, lower-status, error and truncation guards are unexercised

Impacted claim/axis: C2 / operability. Source location: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py:36-39`.

M08 removed the HTML comparison, M09 removed `200 <=`, M11 removed `fetch.get("error") is None`, and M12 removed `not fetch.get("truncated")`. Every mutant exited 0 with all 28 detector cases passing and empty stderr. The served fixture responses are 200 HTML with `error: null` and `truncated: false`; the non-served fixture is 404 HTML. Thus the 404 fixture exercises the upper status bound, not the lower bound or the other three guards.

Smallest selftest improvements, preserving the existing contract rather than broadening it:

- M08: a 200 non-HTML response must not enter HTML canonical replay. A complementary receipt case can keep the otherwise-valid HTML body/audit while changing only the media type and require rejection.
- M09: assert that a 199 HTML response is not served; retain accepted 200 and rejected/non-served 300-boundary controls according to the replay contract.
- M11: assert the serving predicate is false for an otherwise-served response with a non-null error.
- M12: assert the serving predicate is false for an otherwise-served response with `truncated: true`.

These are proposed detector inputs, not exercised receipt-population cases. In particular, the caller already records an error for a truthy `fetch.error` before calling `served()`. Consequently, merely checking the final CLI rejection of an error-bearing receipt might still fail to kill M11. Test the classification behavior if that behavior remains a maintained invariant; do not require a redundant implementation guard if the maintained contract no longer exposes it. The predicted new-case outcomes above are [INFERENCE].

The known non-string `contentType` defect is not an existing guard that can be removed: round 23 has no `isinstance(ctype, str)` check. The unchanged selftest also supplies no non-string content type. This probe does not re-run or newly claim the user-reported crash. The new replay selftest still needs the frozen non-string media-type cases and must reject without traceback.

### P3 — both slice-deletion survivors are equivalent, not killable coverage gaps

M01 and M02 removed `[:10]` from the respective timestamp comparisons. Both survived.

For any string `s` and `d = "2026-10-21"`, `s[:10] < d` and `s < d` have the same Boolean result: a differing prefix determines both comparisons; an equal ten-character prefix makes both comparisons false, regardless of suffix; a shorter string is unchanged by slicing. Non-strings are short-circuited by the retained `isinstance` guard in both versions. Therefore these particular mutants are equivalent for the guarded receipt input, not merely missed by today's fixtures.

Smallest fix: exclude M01/M02 from a behavioral mutation-score denominator. Add the frozen malformed/future timestamp cases to validate the maintained date-time contract, but do not claim such cases can distinguish these two old lexical expressions.

### Exact setup, detector and mutation commands

All work ran from `/tmp/kake-r24-MutateR23CounterSelftest-1yE0`; the only lane write was this report. Scratch creation used:

```sh
mktemp -d /tmp/kake-r24-MutateR23CounterSelftest-XXXX
```

Exact output:

```text
/tmp/kake-r24-MutateR23CounterSelftest-1yE0
```

Clone/frozen-base commands:

```sh
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone && git -C /tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone rev-parse HEAD && git -C /tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone switch --detach f7de3ab4e9f030a15a857a5a08631bd8e690f436
```

Exact observed output:

```text
Cloning into '/tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone'...
done.
f7de3ab4e9f030a15a857a5a08631bd8e690f436
HEAD is now at f7de3ab round-23: record final committed measurements and recovery audit dispositions
```

The observed clone HEAD before detaching was exactly the required frozen revision. The same bounded detector command ran 25 times, with a 300-second outer subprocess timeout and no timeout reached:

```sh
env TMPDIR=/tmp/kake-r24-MutateR23CounterSelftest-1yE0/fixtures GIT_AUTHOR_DATE=2026-10-21T12:00:00Z GIT_COMMITTER_DATE=2026-10-21T12:00:00Z python3 -B /tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone/.ufo/waves/round-23/counter_selftest.py
```

`TMPDIR` kept the detector's disposable fixture clones and audit files inside this seat's scratch directory. The detector itself was never edited. Because it clones its source repository, every mutant was committed **before** invoking it; no result relies on an uncommitted edit being visible to the fixture clone.

Mutation and restoration edits used the surgical edit tool on only the indicated scratch-clone line. For each row, the commit log records the exact commands `git add -f -- <absolute changed script>`, `git -c user.name=Kake\ R24\ mutation\ probe -c user.email=kake-r24-mutation@example.invalid commit --quiet -m 'probe: <row-id>-mutant'` (or `-restored`), and `git rev-parse HEAD`, each with `-C /tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone` and the environment above. These command descriptions are templates; the fully expanded, actually executed commands and their exact stdout/stderr are retained individually in the artifact manifest below.

### Mutants, expected detector and actual output

C1 denotes `/tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone/.ufo/waves/round-23/measure_c1.py`; C2 denotes `/tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone/.ufo/waves/round-23/measure_c2.py`. Each row changes only one expression/term. Exit triples are **pristine / mutant / restored**. The restored run of a row supplies the next row's pristine, byte-identical baseline; the first row uses `00-pristine`.

| ID / artifact row-id | Point mutation | Expected detector | Actual exits | Verdict / exact-output evidence |
|---|---|---|---|---|
| M01 `01-c1-drop-slice` | C1:55, `receipt["observedAt"][:10]` → `receipt["observedAt"]` | No behavioral kill is possible: equivalent | 0 / 0 / 0 | Survived; passed 28/28, stdout success suffix below, stderr empty |
| M02 `02-c2-drop-slice` | C2:56, `fetch["fetchedAt"][:10]` → `fetch["fetchedAt"]` | No behavioral kill is possible: equivalent | 0 / 0 / 0 | Survived; passed 28/28, same success suffix, stderr empty |
| M03 `03-c1-less-equal` | C1:55, `<` → `<=` | C1 valid boundary fixture should fail selftest | 0 / 1 / 0 | Killed by `C1 valid receipts`; accepted 0, expected 17 |
| M04 `04-c2-less-equal` | C2:56, `<` → `<=` | C2 valid boundary fixture should fail selftest | 0 / 1 / 0 | Killed by `C2 valid live receipts`; accepted 0, expected 12 |
| M05 `05-c1-remove-time-type` | C1:55, delete `not isinstance(receipt.get("observedAt"), str) or ` | Non-string/missing timestamp regression should make selftest fail | 0 / 0 / 0 | Survived; passed 28/28, same success suffix, stderr empty |
| M06 `06-c2-remove-time-type` | C2:56, delete `not isinstance(fetch.get("fetchedAt"), str) or ` | Non-string/missing timestamp regression should make selftest fail | 0 / 0 / 0 | Survived; passed 28/28, same success suffix, stderr empty |
| M07 `07-served-remove-status-type` | C2:38, delete `isinstance(status, int) and ` | Existing null-status fixture should make selftest fail | 0 / 1 / 0 | Killed by `C2 invalid status`; counter emitted traceback rather than JSON |
| M08 `08-served-remove-media-type` | C2:39, delete ` and ctype.split(";")[0].strip().lower() == "text/html"` | Non-HTML classification regression should make selftest fail | 0 / 0 / 0 | Survived; passed 28/28, same success suffix, stderr empty |
| M09 `09-served-remove-status-lower` | C2:38, `200 <= status < 300` → `status < 300` | Lower-bound classification regression should make selftest fail | 0 / 0 / 0 | Survived; passed 28/28, same success suffix, stderr empty |
| M10 `10-served-remove-status-upper` | C2:38, `200 <= status < 300` → `200 <= status` | Existing 404 non-served control should make selftest fail | 0 / 1 / 0 | Killed by `C2 valid live receipts`; accepted 11, expected 12 |
| M11 `11-served-remove-error-none` | C2:38, delete ` and fetch.get("error") is None` | Serving-classification regression should make selftest fail, if retained as an invariant | 0 / 0 / 0 | Survived; passed 28/28, same success suffix, stderr empty |
| M12 `12-served-remove-truncated` | C2:39, delete `not fetch.get("truncated") and ` | Truncated classification regression should make selftest fail | 0 / 0 / 0 | Survived; passed 28/28, same success suffix, stderr empty |

For every successful invocation, stdout parsed as 28 cases with every `passed` true and `selftest` equal to `passed`; stderr was exactly empty. An exact stdout suffix present in every successful output is:

```text
], "selftest": "passed"}
```

The full, unabridged stdout/stderr of every invocation is retained, including temporary fixture paths and fixture revision IDs. Exact contiguous stderr prefixes for the three structured failures:

```text
counter_selftest: {"accepted": 0, "case": "C1 valid receipts"
counter_selftest: {"accepted": 0, "case": "C2 valid live receipts"
counter_selftest: {"accepted": 11, "case": "C2 valid live receipts"
```

Exact error strings from those outputs, respectively:

```text
exit 1, expected 0
accepted 0, expected 17
exit 1, expected 0
accepted 0, expected 12
exit 1, expected 0
accepted 11, expected 12
```

M10 additionally emitted the exact error string:

```text
non-served target 'charter-kimi' did not report not-served
```

M07's exact selftest stderr prefix (followed by the captured counter stderr representation) was:

```text
counter_selftest: C2 invalid status: counter emitted invalid JSON: exit=1, stdout='', 
```

The last line of its nested, captured counter stderr was exactly:

```text
TypeError: '<=' not supported between instances of 'int' and 'NoneType'
```

All four failed detector invocations had empty stdout. M07 is a **killed code mutant**, not evidence that a malformed receipt was gracefully rejected: the detector correctly failed on the introduced crash.

## Checked and held

### Restoration evidence

The initial pristine invocation and all 12 restored invocations exited 0, passed 28/28 cases, and had empty stderr. SHA-256 was measured immediately before and after every detector invocation; none of the three script hashes changed during a run.

Pristine and every restored copy shared these exact hashes:

```text
c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5  /tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone/.ufo/waves/round-23/measure_c1.py
91134d27af6c48f8e8bd6e604e533396f6d9c3542d1285ec1e3901f6358e5653  /tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone/.ufo/waves/round-23/measure_c2.py
496b0fdf413eeaa3a24a580d02e625ff751be3db5db9a8ad5b9a5fe478863f84  /tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone/.ufo/waves/round-23/counter_selftest.py
```

Only the named changed script had a mutant hash; the other counter and the detector retained their pristine hashes. The full before/mutant/restored three-file hash sets are recorded per mutant in the mutation manifest.

| Mutant | Changed-script mutant SHA-256 |
|---|---|
| M01 | `4f3f34e0801dc8a4f756ad502d7c18e8c9521874c168bc6e3344f42d5c72111b` |
| M02 | `95e07b47329b92ce43eda40fde5c7f2cf16204039378b75676eaeb222dc7e719` |
| M03 | `44fd7b958fed5691c04e0cc741b5ea13e6f512cf95095087738f3b3c07565eb1` |
| M04 | `4bbb05b8881fdbc9cbedc426c25502c2444339aca985a1d4d6dcc1fe4c7465da` |
| M05 | `d833a7aa20df5ec076849953fa7ba944410bdeea121f0f50f034f9d5a1d00ab2` |
| M06 | `22d3db2114657405ef686f84d821a83411285cc910cc4f87dc82cfbdf0f63d6a` |
| M07 | `b5be419a1c8931146ed9367b178f770570160d266ed3ac6c85d44474d889f35f` |
| M08 | `565e94c0017deecbeaa32177f1ddf1451cb41a512d1d21b71b951a943222b9d4` |
| M09 | `204082258b2030f4f7b9c488bc7b441c4e5ca62914abf2dddff0338fe045da2f` |
| M10 | `19b424da9e21ba1d61ea963ec05511480e1af0d03a6311c055b549a60c6f90cf` |
| M11 | `22ba2ae1c061bc5fed7efab64b7f74774d00a6edbd6454dbd0df416afdfa5e85` |
| M12 | `c140c39001f94ccc2d88add7a98a0dbe2dce9f6d4692a91d5e67e93b975950a9` |

Scratch-clone committed inputs and exact restoration commits:

| Mutant | Mutant HEAD | Restored HEAD |
|---|---|---|
| M01 | `4805c700945fff63710026fdac80bd24dcf6964e` | `d01fb34434edded3cce29f01959a12fe3dbb1b76` |
| M02 | `b912034413552c2de62f89fdc23d6487ab34f1ee` | `5a01f27e5ce246e6b77110b76d5a31f888bf5ff5` |
| M03 | `21617647177e389a837a5ae1fdb8aebc32fd8df5` | `1984f62a04fdd5decb96a7191caeb766c90fc77c` |
| M04 | `8f9e7b9afbcec249c9831a045e69d30d5bdc1118` | `e3b1e8c8c1b6f083d88607b1047622cd9d116a5e` |
| M05 | `24b3ba0caa60ffb83c4d79335a17283176ae5664` | `799b3a4698d8d5550d9ed3dba0bd7e0c6a633bc1` |
| M06 | `0b0e608f827c91e2daa5fc7fa6c0ca70b1d1a3a0` | `5980f2c6b449d5774387281fa1c91a372da127c3` |
| M07 | `16a1bc9a3eec8e75ee5fce0bb5646310b5f12a3f` | `5f51ec749b64a41ef2d81c0172525009cb98413c` |
| M08 | `bb6c96f04b78b69c5f4c4a90325eb6ab4a3d5462` | `95c57ce1e7f2f9850a808803048f898abe476cb2` |
| M09 | `77838fdcc06d63de23253ab71eb0772a19a0fa29` | `269c40334315f5952fc5c12446ba0b9a3ccdacb3` |
| M10 | `e96df6c844dac15d28295aa2a55da300902a9e04` | `3636fc7fec0d9fa2865b81012ad6aa6ea75c5e56` |
| M11 | `73f1ae4dd55175f162af5cc245ae24a11ce17a6b` | `3eba7e15098803a8a5bd50961ef4b061a86abba0` |
| M12 | `ca4ae5c0f7b2ad00ea974ed4892b37766d5df797` | `acdbb3acf84c78696e8d95e98c76add8a5acfcd4` |

The scratch clone ends at `acdbb3acf84c78696e8d95e98c76add8a5acfcd4`, with all three script byte streams restored to their frozen-base hashes. The different HEAD preserves mutation/restoration evidence; no destructive reset was used.

### Exact-output artifacts

Each artifact below is absolute and remains in this seat's isolated scratch directory:

- `/tmp/kake-r24-MutateR23CounterSelftest-1yE0/probe-records.json` — SHA-256 `5e1248b1fa2425a00cbd7386e6c2b6202572f5ef71c4e5db044b5f1697fce40e`. Contains all 25 exact expanded detector commands, input HEADs, return codes, complete stdout/stderr, before/after hashes and parsed case counts.
- `/tmp/kake-r24-MutateR23CounterSelftest-1yE0/mutation-manifest.json` — SHA-256 `2d8c83f09564b2ce154e1f80d1d314fd99ff38c95ba68a128463b7f266bbbc08`. Contains each precise replacement, expected detector, verdict, pristine/mutant/restored run mapping, HEADs and hashes.
- `/tmp/kake-r24-MutateR23CounterSelftest-1yE0/artifact-sha256.txt` — SHA-256 `8fc020a55d818bd880d85db754c7cfb7ca5e1a779b632982a1603af8cf95b881`. Lists absolute paths and SHA-256 for both consolidated artifacts, the three restored scripts, all 75 per-invocation JSON/stdout/stderr files, and all 24 mutation/restoration commit-command logs. This is the complete produced-artifact inventory.

The source-copy paths and their exact restored hashes are listed above. The clone itself remains available at `/tmp/kake-r24-MutateR23CounterSelftest-1yE0/clone` for inspecting any recorded input commit. No helper scripts were created or left behind.

### Tooling and bounds

Exact version-command output:

```text
Python 3.14.8
git version 2.56.0
```

No tools were installed or updated; no pacman transaction, service restart, network request, build, linter or formatter was run. No subagents were dispatched. The lane, fleet, sibling source trees, configuration and indices were not edited; only the assigned report was written in the lane.

## Limits

- This is a targeted mutation probe of the unchanged historical selftest against frozen round-23 counters, not implementation or admission of `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/receipt_replay.py`.
- The 25 detector invocations are the exercised verification. Proposed new selftest inputs above are not counted as run, are not C2 population receipts, and have no fabricated `r23Observed` result.
- The old selftest seeds a date-only C1 timestamp and a full UTC C2 timestamp. Its success does not establish RFC 3339 parsing or future-time rejection. Preserve the frozen contract's actual accepted controls when constructing the maintained selftest rather than inheriting synthetic lexical-test assumptions.
- M11's guard has caller-level overlap; a final rejection-only oracle may not detect its removal. Preserve end-to-end contract behavior, not a particular implementation shape.
- M01/M02 cannot be killed by a behavioral oracle while the rest of their original guarded comparison remains unchanged. The measured score is 4/12 overall, or 4/10 after excluding those two equivalent mutants.
- No independent admission, integration, production change or claim of newly verifying the already-reported malformed timestamp/content-type defects is made.
