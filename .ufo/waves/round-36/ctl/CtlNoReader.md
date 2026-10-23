# CtlNoReader — round-36 pre-freeze control

## Control and axes

Tool: `/fast/scratch/hyaku/kake-r36/controls/CtlNoReader/source_recheck.py`

Axes: content-check discrimination; faithful retained status/redirect/input behavior; key-blind containment.

The deliberately omitted behavior is every final-200 content check, contract bullets (c)–(f). The tool never opens or decodes a body file. It validates body paths by resolution and regular-file metadata only, then treats every valid final-200 check as holding: no `quote_missing`, `unsupported_type`, or `charset_unsupported` is emitted.

The control implements final-status outcomes (a), RFC 3986 redirect resolution and leading-permanent-run findings (b), input validation and per-check continuation (g), and verdict/exit precedence. Resolution retains case, empty queries, and other spelling rather than normalizing beyond RFC 3986 dot-segment removal. Invalid checks receive no other findings. `checksEvaluated` counts valid checks, including the content checks that this control deliberately skips.

How it tries to score: agree on all input/status/redirect findings, and agree on every content check whose correct outcome is clean. It does not key on check IDs, URL words, quote words, names, case labels, or any sealed data. A counter whose content-negative cases are insufficiently numerous could therefore accept it despite the absent reader.

## Expected detector and verdict

Frozen detector named by the declaration: `.ufo/waves/round-36/sealed_count.py`, predicate `met: passed >= 25 of 28 sealed cases`. **Not read or run.** No sealed score or `met` result is claimed.

Expected weakness to probe: whether skipping the entire body-reading operation still reaches the threshold. [INFERENCE] If at least four cases require content-negative findings without an earlier invalid-check outcome, this control cannot meet the predicate.

Local contract discriminator: the first handmade manifest requires `quote_missing`, `unsupported_type`, and `charset_unsupported` under the full contract, hence exit 2 / `could-not-evaluate`. The control instead returns exit 0 / `clean`. Thus the intentional defect is **killed by that local contract discriminator**. The frozen-counter verdict remains **inconclusive/unmeasured**, not a killed or surviving sealed mutant. The four self-tests below assert the intended control behavior, not full-contract conformance.

## Self-test actually run: four handmade manifests

Runtime: Python 3.14.8, standard library only. A bounded Python runner made four anonymous in-memory manifests with `os.memfd_create`, then invoked the actual CLI separately for each:

```text
timeout 10s python3 -B /fast/scratch/hyaku/kake-r36/controls/CtlNoReader/source_recheck.py --manifest /proc/self/fd/<inherited-fd>
```

The runner was itself wrapped in `timeout 60s`. It checked the complete parsed JSON report, actual process exit code, and empty stderr against hand-written expected control outputs. Each manifest descriptor was closed in `finally`; no named fixture files or bytecode caches were created.

For these anonymous manifests, the resolved manifest parent is `/`. Their valid body path was the relative string `fast/scratch/hyaku/kake-r36/controls/CtlNoReader/source_recheck.py`, naming this control's own regular file. No other body was opened. The common quote was `UNWRITTEN_QUOTE_7d4f3f1b_2cc6_4fe8_9a41`, absent from the control source. Unless stated otherwise, checks used URL `https://origin.example/a/b/start?old=1`.

### 1. `all-final-200-content-skipped`

Three checks, each ending in status 200 and naming the control source as body:

- `missing-quote`: `contentType` = `text/plain`.
- `unsupported-type`: `contentType` = `application/octet-stream`.
- `unsupported-charset`: `contentType` = `text/plain; charset=not-a-real-encoding`.

Actual exit **0**, stderr empty:

```json
{"version": 1, "verdict": "clean", "checksEvaluated": 3, "findings": []}
```

### 2. `status-and-leading-permanent-run`

Five checks:

- `permanent-prefix`: 301 `../catalog`, 308 `?edition=2`, 302 `/landing`, then 410. The moved target stops before the temporary hop.
- `temporary-prefix`: 302 `../away`, 308 `/destination`, then 503. No moved finding.
- `other-success`: final 204, therefore `http_error`.
- `empty-query`: URL `HTTPS://Origin.EXAMPLE/a/b?previous=1`, 308 `?`, then 404. Case and the explicit empty query remain in the target.
- `same-scheme-reference`: 301 `https:next`, then 200 with the valid own-file body. Strict RFC 3986 resolution yields `https:next`, not a same-scheme relative-path reinterpretation.

Actual exit **1**, stderr empty:

```json
{"version": 1, "verdict": "failed-policy", "checksEvaluated": 5, "findings": [{"check": "permanent-prefix", "reason": "moved", "target": "https://origin.example/a/catalog?edition=2"}, {"check": "permanent-prefix", "reason": "gone", "target": null}, {"check": "temporary-prefix", "reason": "http_error", "target": null}, {"check": "other-success", "reason": "http_error", "target": null}, {"check": "empty-query", "reason": "moved", "target": "HTTPS://Origin.EXAMPLE/a/b?"}, {"check": "empty-query", "reason": "gone", "target": null}, {"check": "same-scheme-reference", "reason": "moved", "target": "https:next"}]}
```

### 3. `invalid-checks-do-not-stop-neighbors`

Eight entries: JSON null; `bad-quote` with an empty quote; `bad-chain` ending in 301; `bad-location` with a numeric redirect location; `absolute-body` naming `/dev/null` (rejected lexically); `missing-body` naming `absent-handmade-body` inside this control directory; `directory-body` naming this control directory itself; and valid `still-evaluated` ending in 404. Only the last is evaluated.

Actual exit **2**, stderr empty:

```json
{"version": 1, "verdict": "could-not-evaluate", "checksEvaluated": 1, "findings": [{"check": null, "reason": "check_invalid", "target": null}, {"check": "bad-quote", "reason": "check_invalid", "target": null}, {"check": "bad-chain", "reason": "check_invalid", "target": null}, {"check": "bad-location", "reason": "check_invalid", "target": null}, {"check": "absolute-body", "reason": "check_invalid", "target": null}, {"check": "missing-body", "reason": "check_invalid", "target": null}, {"check": "directory-body", "reason": "check_invalid", "target": null}, {"check": "still-evaluated", "reason": "gone", "target": null}]}
```

### 4. `manifest-checks-not-a-list`

Input: `{"version": 1, "checks": "not-a-list"}`.

Actual exit **2**, stderr empty:

```json
{"version": 1, "verdict": "could-not-evaluate", "checksEvaluated": 0, "findings": [{"check": null, "reason": "input_invalid", "target": null}]}
```

Actual runner summary:

```text
SELFTEST 4/4 passed
EXIT 0
```

## Byte preservation / restoration evidence

This assignment creates a standalone control; no pristine lane implementation was supplied or modified, so no pristine/mutated/restored implementation triplet is claimed. There was nothing to restore in the lane or in a sibling source. The newly written control remained byte-identical through the bounded probes:

```text
SHA-256 before: b5e9f6b12082f64fb4497219a86982cfa19fe6eee63e1b472f09680f73918f6b
SHA-256 after:  b5e9f6b12082f64fb4497219a86982cfa19fe6eee63e1b472f09680f73918f6b
```

Both hashes were actual `timeout 10s sha256sum` outputs for the tool. All spawned test/CLI processes exited, anonymous descriptors were closed, and no background job/service was started.

## Key-blindness tree listing

Actual command: `timeout 10s ls -la /fast/scratch/hyaku/kake-r36/controls/CtlNoReader/`; exit 0:

```text
total 8
drwxr-xr-x 2 vgpnk vgpnk   31 Oct 22 22:24 .
drwxr-xr-x 7 vgpnk vgpnk  109 Oct 22 22:25 ..
-rwxr-xr-x 1 vgpnk vgpnk 7878 Oct 22 22:24 source_recheck.py
```

## Compliance

- Complied with key blindness: no listing, reading, searching, or stat targeting any other directory/file under `/fast/scratch/hyaku/kake-r36/`; no sealed cases sought anywhere. The required own-directory listing is above.
- Never read `.ufo/waves/round-36/verification/`, the frozen counter, or any sealed key. Only public declaration bytes were obtained with read-only `git show 3555f63f:SCORECARD.md`.
- No network; no git/jj writes; no sibling source changes; no installs or upgrades. Read `/home/vgpnk/.omp/agent/RULES.md` first. Existing Python 3.14.8 was sufficient; pacman was not invoked.
- Every explicitly spawned command was timeout-bounded at 60 seconds or less. Test subprocess environments had `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed. No process tree was left running.
- Exactly two named deliverable files written: this report and the control tool. No scaffolding or named test fixtures remain.

Report: .ufo/waves/round-36/ctl/CtlNoReader.md
