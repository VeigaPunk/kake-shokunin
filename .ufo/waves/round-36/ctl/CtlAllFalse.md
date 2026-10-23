# CtlAllFalse — pre-freeze all-negative control

Control: `/fast/scratch/hyaku/kake-r36/controls/CtlAllFalse/source_recheck.py`

Contract source: read-only `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 3555f63f:SCORECARD.md`, section “Round 36 — declared claims”. Frozen predicate: `met: passed >= 25 of 28 sealed cases`. No sealed measurement was run or observed.

## Axes and skipped work

- **Freshness (claimed axis):** no evidence-dependent source re-check happens. The tool never opens, stats, resolves, or otherwise inspects a body; it ignores status, redirects, media types, charset, HTML, normalization, quote contents, and per-check validity.
- **Operability (interface only):** Python stdlib, `--manifest PATH`, one JSON report for an accepted invocation, and exit codes 0/1/2/64. This is not evidence that the real auditing capability exists.

The control validates only the manifest envelope and copies each usable check id into exactly one `quote_missing` finding, with null target. Every nonempty checks list produces `failed-policy`, exit 1; an empty list is `clean`, exit 0. Unreadable/invalid manifests or invalid envelopes produce `input_invalid`, `could-not-evaluate`, exit 2. Wrong CLI shape exits 64 with usage on stderr. Malformed individual checks still receive `quote_missing` (null check id when necessary), deliberately skipping their required validation.

## Scoring attack and counterexample

The control tries to win if most cases expect blanket negative answers, or if negative verdicts conceal wrong finding reasons. It uses no lookup table, check-id pattern, URL/quote keyword heuristic, directory label, or body filename. [INFERENCE] Exact multiset comparison plus positive/heterogeneous cases should reject this approach; its actual score remains unknown to this seat.

The strongest exercised counterexample is a valid check ending in HTTP 404: the public contract requires one `gone`, but this control returns one `quote_missing`. Both exit 1, so comparing verdict/exit alone cannot distinguish them. The second fixture also shows missing body paths being incorrectly treated as evaluated quote failures rather than `check_invalid`.

If this control meets the frozen predicate, the fixable defect is insufficient discrimination in the counter, not a newly implemented capability. Smallest safe correction: preserve exact per-check reason comparison and ensure enough valid status/redirect, positive-match, and input-fault cases differ from blanket `quote_missing` that this control cannot reach 25. No counter defect is claimed without L1 measurement, and no admission, saturation, or canonical Rust judgment is made here.

## Self-test actually run

Existing interpreter: Python **3.14.8**. Four hand-made JSON manifests were passed through anonymous pipes to the CLI (`--manifest /proc/self/fd/3`); no fixture files were written. For each invocation the harness loaded the control source, installed a Python audit hook rejecting every subsequent file open except the manifest pipe, then executed its `__main__` path with the CLI arguments. Each run recorded exactly one allowed manifest open and no attempted body open. The hook did not implement any audit rule for the control.

Hand-made inputs:

```json
{"version":1,"checks":[{"id":"case-a","url":"https://example.invalid/source","quote":"retained text","hops":[{"status":404,"location":""}]}]}
```

```json
{"version":1,"checks":[{"id":"case-b","url":"https://example.invalid/plain","quote":"needle","hops":[{"status":200,"location":""}],"contentType":"text/plain","body":"never-opened.body"},{"id":"case-c","url":"https://example.invalid/binary","quote":"needle","hops":[{"status":200,"location":""}],"contentType":"application/octet-stream","body":"never-opened.bin"}]}
```

```json
{"version":1,"checks":[]}
```

```json
{"version":2,"checks":[]}
```

Observed stdout and process exits:

```text
404_all_negative: exit 1
{"version":1,"verdict":"failed-policy","checksEvaluated":1,"findings":[{"check":"case-a","reason":"quote_missing","target":null}]}
two_unopened_bodies: exit 1
{"version":1,"verdict":"failed-policy","checksEvaluated":2,"findings":[{"check":"case-b","reason":"quote_missing","target":null},{"check":"case-c","reason":"quote_missing","target":null}]}
empty_manifest: exit 0
{"version":1,"verdict":"clean","checksEvaluated":0,"findings":[]}
invalid_version: exit 2
{"version":1,"verdict":"could-not-evaluate","checksEvaluated":0,"findings":[{"check":null,"reason":"input_invalid","target":null}]}
```

Each stdout object and exit code was asserted against the intended control behavior. Whitespace/key order above is normalized for readability. All four open-audit records were `{"opened":["/proc/self/fd/3"]}`. Additional usage check: `python3 -B source_recheck.py --manifest` returned 64, empty stdout, stderr `usage: source_recheck.py --manifest PATH`.

```text
PASS: 4 hand-made manifests; 1 usage check; 0 body opens; 0 fixture files written
selftest_exit=0
```

These tests verify the deliberate shortcut and CLI, not compliance with the real source-audit rules. No other verification was run.

## Key-blindness tree listing

Actual output of `timeout --kill-after=1s 10s ls -la /fast/scratch/hyaku/kake-r36/controls/CtlAllFalse/`:

```text
total 4
drwxr-xr-x 2 vgpnk vgpnk   31 Oct 22 22:23 .
drwxr-xr-x 4 vgpnk vgpnk   49 Oct 22 22:23 ..
-rwxr-xr-x 1 vgpnk vgpnk 1634 Oct 22 22:23 source_recheck.py
```

## Compliance

I complied with key blindness: I never listed, read, searched, or statted anything under `/fast/scratch/hyaku/kake-r36/` except my own `controls/CtlAllFalse/` directory. I never read `.ufo/waves/round-36/verification/`, the counter, a sealed case, or a key, and never searched for them. The only lane/fleet Git command was read-only `git show`; there were no git/jj writes, sandbox clones, network calls, or runtime orchestration. Exactly two deliverable files were written: this report and the control. Test manifests stayed in anonymous pipes. All started subprocesses were timeout-capped at 10–60 seconds, completed, and left no background process tree. No tools were installed or updated; no pacman transaction was attempted.
