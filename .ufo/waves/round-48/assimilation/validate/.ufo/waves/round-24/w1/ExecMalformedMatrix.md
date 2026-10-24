## Verdict

Implemented the C2 measurement command and a provisional ten-case population in the isolated clone. The old round-23 runner matrix was exercised from the required fixture base; the population records each run's observed exit, traceback flag, and stdout tail. No lane production files, lane index, or lane revision were changed. This is author-side work, not independent admission.

## Findings

### P2 — Frozen round-23 runners accept malformed timestamps and traceback on non-string Content-Type (C2 / operability)

**Exact runner commands:** each command below ran after a `git clone --quiet --no-hardlinks /tmp/kake-r24-ExecMalformedMatrix-60av/clone /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb`, detached checkout at `f7de3ab4e9f030a15a857a5a08631bd8e690f436`, and a per-case `git reset --hard` to that fixture. The case was then committed with `GIT_AUTHOR_DATE=GIT_COMMITTER_DATE=2026-10-21T12:00:00Z` and the fixed identity in the counter. Runner scripts were copied from the fixture revision.

- `/usr/bin/python /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/runners/measure_c1.py --root /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb --revision bd5cb7a78b55c178d5a38cf6c97338aa7288e61a`
- `/usr/bin/python /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/runners/measure_c1.py --root /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb --revision d394daaf215f670d4ffecb63a30c9717c8a26a9e`
- `/usr/bin/python /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/runners/measure_c2.py --root /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb --revision de0f31b6e9fd7ea359ca930ff45a8c6e5431c6a1`
- `/usr/bin/python /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/runners/measure_c2.py --root /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb --revision 8df727d0e068ea20fda3925f3d5eadf29686ebcb`
- `/usr/bin/python /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/runners/measure_c2.py --root /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb --revision d7600e6decc928bfe992ddb25a2e261e4cacaadd`
- `/usr/bin/python /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/runners/measure_c2.py --root /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb --revision 63771eef59304426845e0c93c83eccced82794a1`
- `/usr/bin/python /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/runners/measure_c2.py --root /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb --revision 7357a7f2d42b3e6a43a37e152ebf1472beae63a4`
- `/usr/bin/python /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/runners/measure_c2.py --root /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb --revision f785b62167cd005ba77cf1af1eef4413eced860d`
- `/usr/bin/python /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/runners/measure_c2.py --root /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb --revision a95c7bd2285e6727602907db379f95b5b56103ab`
- `/usr/bin/python /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/runners/measure_c2.py --root /tmp/kake-r24-ExecMalformedMatrix-60av/r23-report-run/sb --revision 82deb5666b8e06230640ad0703c7ee1e4ac6a685`

**Observed output (last stdout/stderr lines, as retained in `r23Observed`):** `c1-observedat-garbage`: exit 0, traceback false, stdout tail `}`; `c1-unmodified-control`: exit 0, traceback false, stdout tail `}`; `c2-future-fetchedat`: exit 0, traceback false, stdout tail `}`; `c2-contenttype-number`: exit 1, traceback true, stdout tail empty, stderr tail `AttributeError: 'int' object has no attribute 'split'`; `c2-contenttype-array`: exit 1, traceback true, stdout tail empty, stderr tail `AttributeError: 'list' object has no attribute 'split'`; `c2-unmodified-control`: exit 0, traceback false, stdout tail `}`; `c2-contenttype-nan-token`: exit 1, traceback true, stdout tail empty, stderr tail `AttributeError: 'float' object has no attribute 'split'`; `c2-contenttype-infinity-token`: exit 1, traceback true, stdout tail empty, stderr tail `AttributeError: 'float' object has no attribute 'split'`; `c2-duplicate-contenttype-key`: exit 1, traceback true, stdout tail empty, stderr tail `AttributeError: 'int' object has no attribute 'split'`; `c2-truncated-fetch-json`: exit 1, traceback false, stdout tail `}`. Classification is 3/10 overall: reject 1/8 and accept 2/2.

**Impacted claim/axis:** C2, operability. **Smallest fix:** the maintained replay runner must reject invalid/future timestamps and invalid receipt JSON/media-type values through validation rather than allowing the round-23 lexical prefix check or calling `.split()` on unchecked values; rejection must not emit a traceback.

The provisional population's ten measured case records are:

```json
[
  {
    "id": "c1-observedat-garbage",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-10-21garbage",
    "expect": "reject",
    "why": "RFC 3339 section 5.6 requires a complete date-time rather than a date prefix followed by arbitrary text.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c1-unmodified-control",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": ["observedAt"],
    "value": "2026-10-21",
    "expect": "accept",
    "why": "The existing date-only receipt is a control for preserving acceptance of the unmodified round-23 fixture.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c2-future-fetchedat",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": ["fetchedAt"],
    "value": "2099-01-01T00:00:00Z",
    "expect": "reject",
    "why": "A well-formed RFC 3339 timestamp in the future cannot establish an observation made at the measurement time.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c2-contenttype-number",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "replace",
    "replace": {"old": "\"text/html; charset=utf-8\"", "new": "200"},
    "expect": "reject",
    "why": "RFC 9110 section 8.3 defines Content-Type as a media-type string, not a number.",
    "r23Observed": {"exit": 1, "traceback": true, "stdoutTail": ""}
  },
  {
    "id": "c2-contenttype-array",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": ["text/html"],
    "expect": "reject",
    "why": "RFC 9110 section 8.3 defines Content-Type as a media-type string, not an array.",
    "r23Observed": {"exit": 1, "traceback": true, "stdoutTail": ""}
  },
  {
    "id": "c2-unmodified-control",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": ["fetchedAt"],
    "value": "2026-10-21T06:33:03Z",
    "expect": "accept",
    "why": "The existing fetch receipt is a control for preserving acceptance of the unmodified round-23 fixture.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "c2-contenttype-nan-token",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "raw",
    "value": "{\n \"bytes\": 76159,\n \"contentType\": NaN,\n \"error\": null,\n \"fetchedAt\": \"2026-10-21T06:33:03Z\",\n \"finalUrl\": \"https://ds4cc.com/\",\n \"method\": \"GET\",\n \"redirects\": [],\n \"sha256\": \"ccb3f46eda1ce3270df1e3373d49c4034025c4f475a6999142279e03b00b2bb8\",\n \"status\": 200,\n \"truncated\": false,\n \"url\": \"https://ds4cc.com/\"\n}\n",
    "expect": "reject",
    "why": "RFC 8259 sections 6 and 9 exclude NaN from JSON numbers and a receipt parser must reject the non-JSON token without crashing.",
    "r23Observed": {"exit": 1, "traceback": true, "stdoutTail": ""}
  },
  {
    "id": "c2-contenttype-infinity-token",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "raw",
    "value": "{\n \"bytes\": 76159,\n \"contentType\": Infinity,\n \"error\": null,\n \"fetchedAt\": \"2026-10-21T06:33:03Z\",\n \"finalUrl\": \"https://ds4cc.com/\",\n \"method\": \"GET\",\n \"redirects\": [],\n \"sha256\": \"ccb3f46eda1ce3270df1e3373d49c4034025c4f475a6999142279e03b00b2bb8\",\n \"status\": 200,\n \"truncated\": false,\n \"url\": \"https://ds4cc.com/\"\n}\n",
    "expect": "reject",
    "why": "RFC 8259 sections 6 and 9 exclude Infinity from JSON numbers and a receipt parser must reject the non-JSON token without crashing.",
    "r23Observed": {"exit": 1, "traceback": true, "stdoutTail": ""}
  },
  {
    "id": "c2-duplicate-contenttype-key",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "raw",
    "value": "{\n \"bytes\": 76159,\n \"contentType\": \"text/html; charset=utf-8\",\n \"contentType\": 200,\n \"error\": null,\n \"fetchedAt\": \"2026-10-21T06:33:03Z\",\n \"finalUrl\": \"https://ds4cc.com/\",\n \"method\": \"GET\",\n \"redirects\": [],\n \"sha256\": \"ccb3f46eda1ce3270df1e3373d49c4034025c4f475a6999142279e03b00b2bb8\",\n \"status\": 200,\n \"truncated\": false,\n \"url\": \"https://ds4cc.com/\"\n}\n",
    "expect": "reject",
    "why": "RFC 8259 section 4 says object names SHOULD be unique; duplicate receipt keys make the selected value ambiguous and must not be accepted as a valid measurement.",
    "r23Observed": {"exit": 1, "traceback": true, "stdoutTail": ""}
  },
  {
    "id": "c2-truncated-fetch-json",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "raw",
    "value": "{\n \"bytes\": 76159,\n \"contentType\": \"text/html; charset=utf-8\",\n \"error\": null,\n \"fetchedAt\": \"2026-10-21T06:33:03Z\",\n \"finalUrl\": \"https://ds4cc.com/\",\n \"method\": \"GET\",\n \"redirects\": [],\n \"sha256\": \"ccb3f46eda1ce3270df1e3373d49c4034025c4f475a6999142279e03b00b2bb8\",\n \"status\": 200,\n \"truncated\": false,\n \"url\": \"https://ds4cc.com/\"\n",
    "expect": "reject",
    "why": "A truncated fetch receipt does not satisfy JSON syntax or provide a complete observation object.",
    "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}
  }
]
```

## Checked and held

- The source clone was observed at HEAD `f7de3ab4e9f030a15a857a5a08631bd8e690f436`; the requested files remain uncommitted in that clone.
- Counter: `/tmp/kake-r24-ExecMalformedMatrix-60av/clone/.ufo/waves/round-24/measure_c2.py` — SHA-256 `5b5687789e20202f2cfd20a76f3e2ad0928a655445a44ded8d1bce2efae5733d`.
- Population: `/tmp/kake-r24-ExecMalformedMatrix-60av/clone/.ufo/waves/round-24/c2-population.json` — SHA-256 `de4d371fb641ea97c2428a815dd99100d3ccb7cc8ef177f9180e2f265c270d1e`; this digest is the value to copy into the placeholder when L1 freezes the unchanged file.
- The counter implements revision-pinned population loading, runner selection at `REV`, isolated no-hardlinks sandboxing, per-case hard reset and fixed-identity/date commits, set/delete mutation preserving detected indentation, plus exact-text `raw` and single-match `replace` mutations. It records stdout/stderr tails and classifies reject/accept exactly as requested; `--json` emits structured results.
- The matrix executed the round-23 C1/C2 runner code sourced from `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. The round-23 runners themselves were not changed.
- No tools were installed or updated.

## Limits

- `POPULATION_SHA256` is intentionally `L1_FILL_ON_FREEZE`; the L1 must replace that placeholder with the reported population digest when freezing. The digest check is bypassed only while that exact placeholder remains.
- The new counter's full `--root/--revision` CLI was not run against a committed R24 population revision; the requested actual R23 mutation matrix was run through the counter's case mutation/runner-dispatch helpers. The L1's integrated gate should execute the CLI against the frozen revision.
- The report block records provisional test cases and their historical R23 observations, not final admission evidence for C2.
