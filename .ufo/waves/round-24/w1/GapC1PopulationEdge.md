## Verdict

**C2 / operability: parser-boundary gaps reproduced on the C1 side.** Ten file-level cases were each committed directly on frozen base `f7de3ab4e9f030a15a857a5a08631bd8e690f436`, measured with the historical round-23 C1 runner, and restored byte-for-byte in a second committed revision. Every per-case pristine and restored run accepted **17/17**, exit **0**, with no traceback. There are **4 killed reject cases**, **4 surviving accepted reject cases**, **1 surviving crash**, and **1 held acceptance control**. None was inconclusive.

The four accepted survivors are three non-JSON numeric spellings plus one conflicting-duplicate-name case. The duplicate-name rejection is a proposed receipt-integrity policy, **not an RFC 8259 MUST**; it must not be conflated with the three grammar violations. The 5,000-digit integer is valid JSON syntax but triggers an uncaught implementation-limit exception, which violates round-24's clean-rejection requirement.

Author-side audit only: no admission, integration, shipping, production change, or maintained-replay verification is claimed. This report is the only lane file written.

## Findings

### P1 — A 5,000-digit integer crashes replay instead of rejecting cleanly

Impacted claim/axis: C2 / operability. A single extra `edgeProbe` member contains a 5,000-digit positive decimal integer. The historical runner only catches `json.JSONDecodeError` at lines 47–50; Python 3.14.8 instead raises `ValueError` at its 4,300-digit integer-conversion limit. Exit 1 **with a traceback is not a killed mutant** under C2.

Smallest fix: in the maintained `scripts/receipt_replay.py`, catch the integer-limit `ValueError` at the JSON-load boundary and return an ordinary receipt validation failure. Keep the safety limit; do not globally disable it. RFC 8259 §§6 and 9 permit implementation numeric limits but do not require a traceback.

Exact command:

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision da57c1f1d6e25757b1001468129de4d3c72e014f
```

Exact stdout: empty (zero bytes). Exact stderr:

```text
Traceback (most recent call last):
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py", line 126, in <module>
    raise SystemExit(main())
                     ~~~~^^
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py", line 115, in main
    problems, verdicts = check_unit(args.root, revision, unit)
                         ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py", line 48, in check_unit
    receipt = json.loads(raw)
  File "/usr/lib/python3.14/json/__init__.py", line 352, in loads
    return _default_decoder.decode(s)
           ~~~~~~~~~~~~~~~~~~~~~~~^^^
  File "/usr/lib/python3.14/json/decoder.py", line 345, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.14/json/decoder.py", line 361, in raw_decode
    obj, end = self.scan_once(s, idx)
               ~~~~~~~~~~~~~~^^^^^^^^
ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits; use sys.set_int_max_str_digits() to increase the limit
```

### P2 — Non-finite numeric tokens are accepted anywhere in the object

Impacted claim/axis: C2 / operability. Adding only `"edgeProbe": NaN`, `"edgeProbe": Infinity`, or `"edgeProbe": -Infinity` leaves the required receipt fields untouched. All three cases exit 0 and accept 17/17. RFC 8259 §6 explicitly says numeric values such as Infinity and NaN are not permitted. RFC 8259 §9 allows a general-purpose parser to accept extensions; the stricter round-24 malformed-receipt rejection contract is why these extensions must be disabled for receipt validation.

Smallest fix: reject `parse_constant` tokens during JSON decoding, including in otherwise ignored metadata, and route that rejection through the normal validation-failure result. No unrelated extra-field ban is needed. Exact commands and verbatim output excerpts appear below; complete streams are preserved in the hashed result artifacts.

### P3 — Conflicting duplicate names silently use the last value

Impacted claim/axis: C2 / operability, **policy-strengthening candidate**. Inserting `"unit": "wrong-unit"` immediately before the original valid `unit` accepts 17/17. Inserting the same bad member immediately after it rejects with `unit/path mismatch`. Thus the documented population-match check observes the last value rather than detecting the ambiguity.

RFC 8259 §4 says names **SHOULD** be unique and explicitly documents last-wins, erroring, and all-pairs implementations; duplicate names are not categorically excluded by its grammar. The round-23 docstring does not explicitly prohibit duplicate names. Consequently `expect: reject` for the bad-first case is an explicitly recommended, unambiguous-evidence policy, not a claim that round 23 violated an RFC MUST. The bad-last case is independently rejectable by the documented unit-match requirement.

Smallest proposed fix, if this stricter receipt policy is frozen: decode with an object-pairs hook that rejects repeated decoded names at any depth; report an ordinary validation problem. Do not silently alter the contract to treat this recommendation as pre-existing normative evidence.

### Commands, mutations and exact observed output

Runner: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py`. Receipt: `.ufo/waves/round-23/receipts/drift-detection.json`. Each case replaces only this receipt in the isolated clone; all other measured files are from the frozen base.

Output blocks below quote **exact, noncontiguous selected stdout lines**, not a reconstructed full JSON result. The complete stdout/stderr for pristine, mutated and restored runs are in each `.result.json`. `stdoutTail` is literally `}` for every JSON-emitting run and empty for the crash; acceptance and the target's problems, not this last line, determine the verdict.

#### receipt-invalid-json-truncated

Expected: **reject**. Observed: exit **1**, traceback **false**, accepted **16/17**. Verdict: **killed**.

Mutation revision: `db69e6d35236c0f62510a6438cb2d5816b764ae3`. Input length: 5209 bytes.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision db69e6d35236c0f62510a6438cb2d5816b764ae3
```


```text
 "accepted": 16,
 "total": 17,
    "receipt is not JSON: Expecting ',' delimiter: line 91 column 1 (char 5207)"
```

Exact stderr: empty.

#### receipt-array-not-object

Expected: **reject**. Observed: exit **1**, traceback **false**, accepted **16/17**. Verdict: **killed**.

Mutation revision: `edd14d8944f472694519da40dbb34a7e4c9bdc9b`. Input length: 5212 bytes.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision edd14d8944f472694519da40dbb34a7e4c9bdc9b
```


```text
 "accepted": 16,
 "total": 17,
    "receipt is not an object"
```

Exact stderr: empty.

#### receipt-utf8-bom

Expected: **reject**. Observed: exit **1**, traceback **false**, accepted **16/17**. Verdict: **killed**.

Mutation revision: `f857e2f47cc59e0c0f2d6b7f06c2545117fa5c9d`. Input length: 5212 bytes.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision f857e2f47cc59e0c0f2d6b7f06c2545117fa5c9d
```


```text
 "accepted": 16,
 "total": 17,
    "receipt is not JSON: Unexpected UTF-8 BOM (decode using utf-8-sig): line 1 column 1 (char 0)"
```

Exact stderr: empty.

#### receipt-nan-token

Expected: **reject**. Observed: exit **0**, traceback **false**, accepted **17/17**. Verdict: **survived-accepted**.

Mutation revision: `265ffb797235d71c32dfd3c721197617aed1b3f5`. Input length: 5228 bytes.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision 265ffb797235d71c32dfd3c721197617aed1b3f5
```


```text
 "accepted": 17,
 "total": 17,
```

Exact stderr: empty.

#### receipt-infinity-token

Expected: **reject**. Observed: exit **0**, traceback **false**, accepted **17/17**. Verdict: **survived-accepted**.

Mutation revision: `29d7e2f640d0b69eb8c4f127874b8678e33fe755`. Input length: 5233 bytes.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision 29d7e2f640d0b69eb8c4f127874b8678e33fe755
```


```text
 "accepted": 17,
 "total": 17,
```

Exact stderr: empty.

#### receipt-negative-infinity-token

Expected: **reject**. Observed: exit **0**, traceback **false**, accepted **17/17**. Verdict: **survived-accepted**.

Mutation revision: `0d8fc7fbbf89317253db95ede956f06270bf1a7a`. Input length: 5234 bytes.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision 0d8fc7fbbf89317253db95ede956f06270bf1a7a
```


```text
 "accepted": 17,
 "total": 17,
```

Exact stderr: empty.

#### receipt-duplicate-unit-bad-first

Expected: **reject**. Observed: exit **0**, traceback **false**, accepted **17/17**. Verdict: **survived-accepted**.

Mutation revision: `b70c51f4ab28a8b3488a329477dcdad5a758f5e7`. Input length: 5232 bytes.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision b70c51f4ab28a8b3488a329477dcdad5a758f5e7
```


```text
 "accepted": 17,
 "total": 17,
```

Exact stderr: empty.

#### receipt-duplicate-unit-bad-last

Expected: **reject**. Observed: exit **1**, traceback **false**, accepted **16/17**. Verdict: **killed**.

Mutation revision: `25777c339f49c2b6d830ab87c1ee0155a1896d55`. Input length: 5232 bytes.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision 25777c339f49c2b6d830ab87c1ee0155a1896d55
```


```text
 "accepted": 16,
 "total": 17,
    "unit/path mismatch"
```

Exact stderr: empty.

#### receipt-large-integer-1000-digits

Expected: **accept**. Observed: exit **0**, traceback **false**, accepted **17/17**. Verdict: **control-held**.

Mutation revision: `77efc1c0c68465966063abb5476352d09c3939fd`. Input length: 6225 bytes.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision 77efc1c0c68465966063abb5476352d09c3939fd
```


```text
 "accepted": 17,
 "total": 17,
```

Exact stderr: empty.

#### receipt-large-integer-5000-digits

Expected: **reject**. Observed: exit **1**, traceback **true**, accepted **no JSON result**. Verdict: **survived-crash**.

Mutation revision: `da57c1f1d6e25757b1001468129de4d3c72e014f`. Input length: 10225 bytes.

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision da57c1f1d6e25757b1001468129de4d3c72e014f
```


Exact stdout: empty. Exact stderr is quoted in the P1 finding above.

### C2 malformed-case JSON array

**L1-approved raw-file schema extension:** `op: "raw"` and string `value` below mean **replace the entire receipt with `value.encode("utf-8")`**, without adding quotes, parsing, reserializing, or normalizing it; there is no `jsonPath` for this operation. The parent explicitly approved this extension during report completion and stated that `ExecMalformedMatrix` was instructed to support it. The original set/delete schema cannot retain these byte-level cases, and `op: "set", jsonPath: []` would incorrectly JSON-encode a quoted string. The approved raw operation preserves invalid syntax, a leading BOM, non-finite tokens, duplicate members and over-limit integers. The exact hashed `.receipt` fixtures remain the authoritative measured bytes. Population-adapter implementation is outside this audit and was not independently exercised here.

All ten entries below were actually run. The BOM's `expect: reject` preserves an allowed strict-parser policy: RFC 8259 §8.1 permits, but does not require, ignoring it. The 1,000-digit integer is an acceptance control in otherwise unconstrained metadata; the 5,000-digit integer selects clean rejection under the observed interpreter limit, rather than claiming that the integer's grammar is invalid.

```json
[
  {
    "id": "receipt-invalid-json-truncated",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "raw",
    "value": "{\n \"unit\": \"drift-detection\",\n \"path\": \"corpus/knowledge/drift-detection.md\",\n \"observedAt\": \"2026-10-21\",\n \"claims\": [\n  {\n   \"id\": \"c1\",\n   \"anchor\": \"the webzites and plazir source trees remain absent after the 2026-10-12 prune.\",\n   \"claim\": \"The documented webzites and plazir-15-site source trees are absent locally.\",\n   \"surface\": \"/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site\",\n   \"method\": \"test -e\",\n   \"observation\": \"absent /home/vgpnk/Projects/webzites\\nabsent /home/vgpnk/Projects/plazir-15-site\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c2\",\n   \"anchor\": \"`ufo-fsd.kimi.pro`\\n  is a 612B React shell\",\n   \"claim\": \"GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.\",\n   \"surface\": \"GET https://ufo-fsd.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\\\"root\\\"></div>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c3\",\n   \"anchor\": \"GET it, don't HEAD (HEAD\u2192403).\",\n   \"claim\": \"HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.\",\n   \"surface\": \"HEAD https://ufo-fsd.kimi.pro\",\n   \"method\": \"HEAD\",\n   \"observation\": \"http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c4\",\n   \"anchor\": \"`plazir27.kimi.pro` returns 200 with a 5,995B\\n  preview-404 body (x-fc-request-id, Function-Compute ingress).\",\n   \"claim\": \"The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.\",\n   \"surface\": \"GET https://plazir27.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.\",\n   \"verdict\": \"STALE\",\n   \"correction\": \"As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c5\",\n   \"anchor\": \"canonical = `veigapunk.github.io/lucario/` (live)\",\n   \"claim\": \"The cited canonical GitHub Pages Lucario URL still serves the page.\",\n   \"surface\": \"GET https://veigapunk.github.io/lucario/\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario<span>.</span></h1>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c6\",\n   \"anchor\": \"plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path\",\n   \"claim\": \"Both explicitly named dead-slot Kimi pages still return HTTP 404.\",\n   \"surface\": \"GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page\",\n   \"method\": \"GET\",\n   \"observation\": \"https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c7\",\n   \"anchor\": \"**8** (incl. `/tetris/`,\",\n   \"claim\": \"The r16 live Plazir sitemap contained eight locations including tetris.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/sitemap.xml\",\n   \"method\": \"GET\",\n   \"observation\": \"200; 7 loc entries; tetris absent from sitemap although tetris/ returns 200\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.\"\n  },\n  {\n   \"id\": \"c8\",\n   \"anchor\": \"| `snake/index.html` `og:url` | 0 hits\",\n   \"claim\": \"The r16 live snake page had no og:url and speedrun had a Plazir self-canonical.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/\",\n   \"method\": \"GET\",\n   \"observation\": \"snake 200 og:url https://veigapunk.github.io/plazir-15-site/snake/; speedrun 200 canonical https://ds4cc.com/speedrun/\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.\"\n  }\n ]\n\n",
    "expect": "reject",
    "why": "RFC 8259 \u00a74 requires an object end delimiter; the documented C1 receipt must be a JSON object.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "receipt-array-not-object",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "raw",
    "value": "[{\n \"unit\": \"drift-detection\",\n \"path\": \"corpus/knowledge/drift-detection.md\",\n \"observedAt\": \"2026-10-21\",\n \"claims\": [\n  {\n   \"id\": \"c1\",\n   \"anchor\": \"the webzites and plazir source trees remain absent after the 2026-10-12 prune.\",\n   \"claim\": \"The documented webzites and plazir-15-site source trees are absent locally.\",\n   \"surface\": \"/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site\",\n   \"method\": \"test -e\",\n   \"observation\": \"absent /home/vgpnk/Projects/webzites\\nabsent /home/vgpnk/Projects/plazir-15-site\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c2\",\n   \"anchor\": \"`ufo-fsd.kimi.pro`\\n  is a 612B React shell\",\n   \"claim\": \"GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.\",\n   \"surface\": \"GET https://ufo-fsd.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\\\"root\\\"></div>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c3\",\n   \"anchor\": \"GET it, don't HEAD (HEAD\u2192403).\",\n   \"claim\": \"HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.\",\n   \"surface\": \"HEAD https://ufo-fsd.kimi.pro\",\n   \"method\": \"HEAD\",\n   \"observation\": \"http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c4\",\n   \"anchor\": \"`plazir27.kimi.pro` returns 200 with a 5,995B\\n  preview-404 body (x-fc-request-id, Function-Compute ingress).\",\n   \"claim\": \"The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.\",\n   \"surface\": \"GET https://plazir27.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.\",\n   \"verdict\": \"STALE\",\n   \"correction\": \"As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c5\",\n   \"anchor\": \"canonical = `veigapunk.github.io/lucario/` (live)\",\n   \"claim\": \"The cited canonical GitHub Pages Lucario URL still serves the page.\",\n   \"surface\": \"GET https://veigapunk.github.io/lucario/\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario<span>.</span></h1>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c6\",\n   \"anchor\": \"plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path\",\n   \"claim\": \"Both explicitly named dead-slot Kimi pages still return HTTP 404.\",\n   \"surface\": \"GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page\",\n   \"method\": \"GET\",\n   \"observation\": \"https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c7\",\n   \"anchor\": \"**8** (incl. `/tetris/`,\",\n   \"claim\": \"The r16 live Plazir sitemap contained eight locations including tetris.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/sitemap.xml\",\n   \"method\": \"GET\",\n   \"observation\": \"200; 7 loc entries; tetris absent from sitemap although tetris/ returns 200\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.\"\n  },\n  {\n   \"id\": \"c8\",\n   \"anchor\": \"| `snake/index.html` `og:url` | 0 hits\",\n   \"claim\": \"The r16 live snake page had no og:url and speedrun had a Plazir self-canonical.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/\",\n   \"method\": \"GET\",\n   \"observation\": \"snake 200 og:url https://veigapunk.github.io/plazir-15-site/snake/; speedrun 200 canonical https://ds4cc.com/speedrun/\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.\"\n  }\n ]\n}]\n",
    "expect": "reject",
    "why": "RFC 8259 \u00a75 permits arrays as JSON, but measure_c1.py lines 8 and 51\u201352 explicitly require a receipt object.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "receipt-utf8-bom",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "raw",
    "value": "\ufeff{\n \"unit\": \"drift-detection\",\n \"path\": \"corpus/knowledge/drift-detection.md\",\n \"observedAt\": \"2026-10-21\",\n \"claims\": [\n  {\n   \"id\": \"c1\",\n   \"anchor\": \"the webzites and plazir source trees remain absent after the 2026-10-12 prune.\",\n   \"claim\": \"The documented webzites and plazir-15-site source trees are absent locally.\",\n   \"surface\": \"/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site\",\n   \"method\": \"test -e\",\n   \"observation\": \"absent /home/vgpnk/Projects/webzites\\nabsent /home/vgpnk/Projects/plazir-15-site\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c2\",\n   \"anchor\": \"`ufo-fsd.kimi.pro`\\n  is a 612B React shell\",\n   \"claim\": \"GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.\",\n   \"surface\": \"GET https://ufo-fsd.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\\\"root\\\"></div>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c3\",\n   \"anchor\": \"GET it, don't HEAD (HEAD\u2192403).\",\n   \"claim\": \"HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.\",\n   \"surface\": \"HEAD https://ufo-fsd.kimi.pro\",\n   \"method\": \"HEAD\",\n   \"observation\": \"http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c4\",\n   \"anchor\": \"`plazir27.kimi.pro` returns 200 with a 5,995B\\n  preview-404 body (x-fc-request-id, Function-Compute ingress).\",\n   \"claim\": \"The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.\",\n   \"surface\": \"GET https://plazir27.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.\",\n   \"verdict\": \"STALE\",\n   \"correction\": \"As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c5\",\n   \"anchor\": \"canonical = `veigapunk.github.io/lucario/` (live)\",\n   \"claim\": \"The cited canonical GitHub Pages Lucario URL still serves the page.\",\n   \"surface\": \"GET https://veigapunk.github.io/lucario/\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario<span>.</span></h1>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c6\",\n   \"anchor\": \"plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path\",\n   \"claim\": \"Both explicitly named dead-slot Kimi pages still return HTTP 404.\",\n   \"surface\": \"GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page\",\n   \"method\": \"GET\",\n   \"observation\": \"https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c7\",\n   \"anchor\": \"**8** (incl. `/tetris/`,\",\n   \"claim\": \"The r16 live Plazir sitemap contained eight locations including tetris.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/sitemap.xml\",\n   \"method\": \"GET\",\n   \"observation\": \"200; 7 loc entries; tetris absent from sitemap although tetris/ returns 200\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.\"\n  },\n  {\n   \"id\": \"c8\",\n   \"anchor\": \"| `snake/index.html` `og:url` | 0 hits\",\n   \"claim\": \"The r16 live snake page had no og:url and speedrun had a Plazir self-canonical.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/\",\n   \"method\": \"GET\",\n   \"observation\": \"snake 200 og:url https://veigapunk.github.io/plazir-15-site/snake/; speedrun 200 canonical https://ds4cc.com/speedrun/\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.\"\n  }\n ]\n}",
    "expect": "reject",
    "why": "RFC 8259 \u00a78.1 permits a parser to ignore a BOM but does not require it; preserving the current strict UTF-8 JSON-text rejection is allowed.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "receipt-nan-token",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "raw",
    "value": "{\n \"edgeProbe\": NaN,\n \"unit\": \"drift-detection\",\n \"path\": \"corpus/knowledge/drift-detection.md\",\n \"observedAt\": \"2026-10-21\",\n \"claims\": [\n  {\n   \"id\": \"c1\",\n   \"anchor\": \"the webzites and plazir source trees remain absent after the 2026-10-12 prune.\",\n   \"claim\": \"The documented webzites and plazir-15-site source trees are absent locally.\",\n   \"surface\": \"/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site\",\n   \"method\": \"test -e\",\n   \"observation\": \"absent /home/vgpnk/Projects/webzites\\nabsent /home/vgpnk/Projects/plazir-15-site\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c2\",\n   \"anchor\": \"`ufo-fsd.kimi.pro`\\n  is a 612B React shell\",\n   \"claim\": \"GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.\",\n   \"surface\": \"GET https://ufo-fsd.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\\\"root\\\"></div>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c3\",\n   \"anchor\": \"GET it, don't HEAD (HEAD\u2192403).\",\n   \"claim\": \"HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.\",\n   \"surface\": \"HEAD https://ufo-fsd.kimi.pro\",\n   \"method\": \"HEAD\",\n   \"observation\": \"http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c4\",\n   \"anchor\": \"`plazir27.kimi.pro` returns 200 with a 5,995B\\n  preview-404 body (x-fc-request-id, Function-Compute ingress).\",\n   \"claim\": \"The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.\",\n   \"surface\": \"GET https://plazir27.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.\",\n   \"verdict\": \"STALE\",\n   \"correction\": \"As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c5\",\n   \"anchor\": \"canonical = `veigapunk.github.io/lucario/` (live)\",\n   \"claim\": \"The cited canonical GitHub Pages Lucario URL still serves the page.\",\n   \"surface\": \"GET https://veigapunk.github.io/lucario/\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario<span>.</span></h1>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c6\",\n   \"anchor\": \"plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path\",\n   \"claim\": \"Both explicitly named dead-slot Kimi pages still return HTTP 404.\",\n   \"surface\": \"GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page\",\n   \"method\": \"GET\",\n   \"observation\": \"https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c7\",\n   \"anchor\": \"**8** (incl. `/tetris/`,\",\n   \"claim\": \"The r16 live Plazir sitemap contained eight locations including tetris.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/sitemap.xml\",\n   \"method\": \"GET\",\n   \"observation\": \"200; 7 loc entries; tetris absent from sitemap although tetris/ returns 200\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.\"\n  },\n  {\n   \"id\": \"c8\",\n   \"anchor\": \"| `snake/index.html` `og:url` | 0 hits\",\n   \"claim\": \"The r16 live snake page had no og:url and speedrun had a Plazir self-canonical.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/\",\n   \"method\": \"GET\",\n   \"observation\": \"snake 200 og:url https://veigapunk.github.io/plazir-15-site/snake/; speedrun 200 canonical https://ds4cc.com/speedrun/\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.\"\n  }\n ]\n}",
    "expect": "reject",
    "why": "RFC 8259 \u00a76 forbids the NaN numeric token, even in an otherwise ignored extension member.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "receipt-infinity-token",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "raw",
    "value": "{\n \"edgeProbe\": Infinity,\n \"unit\": \"drift-detection\",\n \"path\": \"corpus/knowledge/drift-detection.md\",\n \"observedAt\": \"2026-10-21\",\n \"claims\": [\n  {\n   \"id\": \"c1\",\n   \"anchor\": \"the webzites and plazir source trees remain absent after the 2026-10-12 prune.\",\n   \"claim\": \"The documented webzites and plazir-15-site source trees are absent locally.\",\n   \"surface\": \"/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site\",\n   \"method\": \"test -e\",\n   \"observation\": \"absent /home/vgpnk/Projects/webzites\\nabsent /home/vgpnk/Projects/plazir-15-site\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c2\",\n   \"anchor\": \"`ufo-fsd.kimi.pro`\\n  is a 612B React shell\",\n   \"claim\": \"GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.\",\n   \"surface\": \"GET https://ufo-fsd.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\\\"root\\\"></div>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c3\",\n   \"anchor\": \"GET it, don't HEAD (HEAD\u2192403).\",\n   \"claim\": \"HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.\",\n   \"surface\": \"HEAD https://ufo-fsd.kimi.pro\",\n   \"method\": \"HEAD\",\n   \"observation\": \"http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c4\",\n   \"anchor\": \"`plazir27.kimi.pro` returns 200 with a 5,995B\\n  preview-404 body (x-fc-request-id, Function-Compute ingress).\",\n   \"claim\": \"The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.\",\n   \"surface\": \"GET https://plazir27.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.\",\n   \"verdict\": \"STALE\",\n   \"correction\": \"As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c5\",\n   \"anchor\": \"canonical = `veigapunk.github.io/lucario/` (live)\",\n   \"claim\": \"The cited canonical GitHub Pages Lucario URL still serves the page.\",\n   \"surface\": \"GET https://veigapunk.github.io/lucario/\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario<span>.</span></h1>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c6\",\n   \"anchor\": \"plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path\",\n   \"claim\": \"Both explicitly named dead-slot Kimi pages still return HTTP 404.\",\n   \"surface\": \"GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page\",\n   \"method\": \"GET\",\n   \"observation\": \"https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c7\",\n   \"anchor\": \"**8** (incl. `/tetris/`,\",\n   \"claim\": \"The r16 live Plazir sitemap contained eight locations including tetris.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/sitemap.xml\",\n   \"method\": \"GET\",\n   \"observation\": \"200; 7 loc entries; tetris absent from sitemap although tetris/ returns 200\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.\"\n  },\n  {\n   \"id\": \"c8\",\n   \"anchor\": \"| `snake/index.html` `og:url` | 0 hits\",\n   \"claim\": \"The r16 live snake page had no og:url and speedrun had a Plazir self-canonical.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/\",\n   \"method\": \"GET\",\n   \"observation\": \"snake 200 og:url https://veigapunk.github.io/plazir-15-site/snake/; speedrun 200 canonical https://ds4cc.com/speedrun/\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.\"\n  }\n ]\n}",
    "expect": "reject",
    "why": "RFC 8259 \u00a76 forbids the Infinity numeric token, even in an otherwise ignored extension member.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "receipt-negative-infinity-token",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "raw",
    "value": "{\n \"edgeProbe\": -Infinity,\n \"unit\": \"drift-detection\",\n \"path\": \"corpus/knowledge/drift-detection.md\",\n \"observedAt\": \"2026-10-21\",\n \"claims\": [\n  {\n   \"id\": \"c1\",\n   \"anchor\": \"the webzites and plazir source trees remain absent after the 2026-10-12 prune.\",\n   \"claim\": \"The documented webzites and plazir-15-site source trees are absent locally.\",\n   \"surface\": \"/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site\",\n   \"method\": \"test -e\",\n   \"observation\": \"absent /home/vgpnk/Projects/webzites\\nabsent /home/vgpnk/Projects/plazir-15-site\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c2\",\n   \"anchor\": \"`ufo-fsd.kimi.pro`\\n  is a 612B React shell\",\n   \"claim\": \"GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.\",\n   \"surface\": \"GET https://ufo-fsd.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\\\"root\\\"></div>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c3\",\n   \"anchor\": \"GET it, don't HEAD (HEAD\u2192403).\",\n   \"claim\": \"HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.\",\n   \"surface\": \"HEAD https://ufo-fsd.kimi.pro\",\n   \"method\": \"HEAD\",\n   \"observation\": \"http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c4\",\n   \"anchor\": \"`plazir27.kimi.pro` returns 200 with a 5,995B\\n  preview-404 body (x-fc-request-id, Function-Compute ingress).\",\n   \"claim\": \"The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.\",\n   \"surface\": \"GET https://plazir27.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.\",\n   \"verdict\": \"STALE\",\n   \"correction\": \"As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c5\",\n   \"anchor\": \"canonical = `veigapunk.github.io/lucario/` (live)\",\n   \"claim\": \"The cited canonical GitHub Pages Lucario URL still serves the page.\",\n   \"surface\": \"GET https://veigapunk.github.io/lucario/\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario<span>.</span></h1>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c6\",\n   \"anchor\": \"plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path\",\n   \"claim\": \"Both explicitly named dead-slot Kimi pages still return HTTP 404.\",\n   \"surface\": \"GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page\",\n   \"method\": \"GET\",\n   \"observation\": \"https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c7\",\n   \"anchor\": \"**8** (incl. `/tetris/`,\",\n   \"claim\": \"The r16 live Plazir sitemap contained eight locations including tetris.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/sitemap.xml\",\n   \"method\": \"GET\",\n   \"observation\": \"200; 7 loc entries; tetris absent from sitemap although tetris/ returns 200\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.\"\n  },\n  {\n   \"id\": \"c8\",\n   \"anchor\": \"| `snake/index.html` `og:url` | 0 hits\",\n   \"claim\": \"The r16 live snake page had no og:url and speedrun had a Plazir self-canonical.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/\",\n   \"method\": \"GET\",\n   \"observation\": \"snake 200 og:url https://veigapunk.github.io/plazir-15-site/snake/; speedrun 200 canonical https://ds4cc.com/speedrun/\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.\"\n  }\n ]\n}",
    "expect": "reject",
    "why": "RFC 8259 \u00a76 forbids the -Infinity numeric token, even in an otherwise ignored extension member.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "receipt-duplicate-unit-bad-first",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "raw",
    "value": "{\n \"unit\": \"wrong-unit\",\n \"unit\": \"drift-detection\",\n \"path\": \"corpus/knowledge/drift-detection.md\",\n \"observedAt\": \"2026-10-21\",\n \"claims\": [\n  {\n   \"id\": \"c1\",\n   \"anchor\": \"the webzites and plazir source trees remain absent after the 2026-10-12 prune.\",\n   \"claim\": \"The documented webzites and plazir-15-site source trees are absent locally.\",\n   \"surface\": \"/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site\",\n   \"method\": \"test -e\",\n   \"observation\": \"absent /home/vgpnk/Projects/webzites\\nabsent /home/vgpnk/Projects/plazir-15-site\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c2\",\n   \"anchor\": \"`ufo-fsd.kimi.pro`\\n  is a 612B React shell\",\n   \"claim\": \"GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.\",\n   \"surface\": \"GET https://ufo-fsd.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\\\"root\\\"></div>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c3\",\n   \"anchor\": \"GET it, don't HEAD (HEAD\u2192403).\",\n   \"claim\": \"HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.\",\n   \"surface\": \"HEAD https://ufo-fsd.kimi.pro\",\n   \"method\": \"HEAD\",\n   \"observation\": \"http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c4\",\n   \"anchor\": \"`plazir27.kimi.pro` returns 200 with a 5,995B\\n  preview-404 body (x-fc-request-id, Function-Compute ingress).\",\n   \"claim\": \"The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.\",\n   \"surface\": \"GET https://plazir27.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.\",\n   \"verdict\": \"STALE\",\n   \"correction\": \"As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c5\",\n   \"anchor\": \"canonical = `veigapunk.github.io/lucario/` (live)\",\n   \"claim\": \"The cited canonical GitHub Pages Lucario URL still serves the page.\",\n   \"surface\": \"GET https://veigapunk.github.io/lucario/\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario<span>.</span></h1>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c6\",\n   \"anchor\": \"plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path\",\n   \"claim\": \"Both explicitly named dead-slot Kimi pages still return HTTP 404.\",\n   \"surface\": \"GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page\",\n   \"method\": \"GET\",\n   \"observation\": \"https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c7\",\n   \"anchor\": \"**8** (incl. `/tetris/`,\",\n   \"claim\": \"The r16 live Plazir sitemap contained eight locations including tetris.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/sitemap.xml\",\n   \"method\": \"GET\",\n   \"observation\": \"200; 7 loc entries; tetris absent from sitemap although tetris/ returns 200\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.\"\n  },\n  {\n   \"id\": \"c8\",\n   \"anchor\": \"| `snake/index.html` `og:url` | 0 hits\",\n   \"claim\": \"The r16 live snake page had no og:url and speedrun had a Plazir self-canonical.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/\",\n   \"method\": \"GET\",\n   \"observation\": \"snake 200 og:url https://veigapunk.github.io/plazir-15-site/snake/; speedrun 200 canonical https://ds4cc.com/speedrun/\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.\"\n  }\n ]\n}",
    "expect": "reject",
    "why": "RFC 8259 \u00a74 recommends unique names; rejecting conflicting unit members is the proposed unambiguous-evidence policy, not an RFC MUST.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "receipt-duplicate-unit-bad-last",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "raw",
    "value": "{\n \"unit\": \"drift-detection\",\n \"unit\": \"wrong-unit\",\n \"path\": \"corpus/knowledge/drift-detection.md\",\n \"observedAt\": \"2026-10-21\",\n \"claims\": [\n  {\n   \"id\": \"c1\",\n   \"anchor\": \"the webzites and plazir source trees remain absent after the 2026-10-12 prune.\",\n   \"claim\": \"The documented webzites and plazir-15-site source trees are absent locally.\",\n   \"surface\": \"/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site\",\n   \"method\": \"test -e\",\n   \"observation\": \"absent /home/vgpnk/Projects/webzites\\nabsent /home/vgpnk/Projects/plazir-15-site\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c2\",\n   \"anchor\": \"`ufo-fsd.kimi.pro`\\n  is a 612B React shell\",\n   \"claim\": \"GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.\",\n   \"surface\": \"GET https://ufo-fsd.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\\\"root\\\"></div>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c3\",\n   \"anchor\": \"GET it, don't HEAD (HEAD\u2192403).\",\n   \"claim\": \"HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.\",\n   \"surface\": \"HEAD https://ufo-fsd.kimi.pro\",\n   \"method\": \"HEAD\",\n   \"observation\": \"http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c4\",\n   \"anchor\": \"`plazir27.kimi.pro` returns 200 with a 5,995B\\n  preview-404 body (x-fc-request-id, Function-Compute ingress).\",\n   \"claim\": \"The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.\",\n   \"surface\": \"GET https://plazir27.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.\",\n   \"verdict\": \"STALE\",\n   \"correction\": \"As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c5\",\n   \"anchor\": \"canonical = `veigapunk.github.io/lucario/` (live)\",\n   \"claim\": \"The cited canonical GitHub Pages Lucario URL still serves the page.\",\n   \"surface\": \"GET https://veigapunk.github.io/lucario/\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario<span>.</span></h1>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c6\",\n   \"anchor\": \"plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path\",\n   \"claim\": \"Both explicitly named dead-slot Kimi pages still return HTTP 404.\",\n   \"surface\": \"GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page\",\n   \"method\": \"GET\",\n   \"observation\": \"https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c7\",\n   \"anchor\": \"**8** (incl. `/tetris/`,\",\n   \"claim\": \"The r16 live Plazir sitemap contained eight locations including tetris.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/sitemap.xml\",\n   \"method\": \"GET\",\n   \"observation\": \"200; 7 loc entries; tetris absent from sitemap although tetris/ returns 200\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.\"\n  },\n  {\n   \"id\": \"c8\",\n   \"anchor\": \"| `snake/index.html` `og:url` | 0 hits\",\n   \"claim\": \"The r16 live snake page had no og:url and speedrun had a Plazir self-canonical.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/\",\n   \"method\": \"GET\",\n   \"observation\": \"snake 200 og:url https://veigapunk.github.io/plazir-15-site/snake/; speedrun 200 canonical https://ds4cc.com/speedrun/\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.\"\n  }\n ]\n}",
    "expect": "reject",
    "why": "RFC 8259 \u00a74 recommends unique names and the final unit value violates the documented unit/population match.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "receipt-large-integer-1000-digits",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "raw",
    "value": "{\n \"edgeProbe\": 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999,\n \"unit\": \"drift-detection\",\n \"path\": \"corpus/knowledge/drift-detection.md\",\n \"observedAt\": \"2026-10-21\",\n \"claims\": [\n  {\n   \"id\": \"c1\",\n   \"anchor\": \"the webzites and plazir source trees remain absent after the 2026-10-12 prune.\",\n   \"claim\": \"The documented webzites and plazir-15-site source trees are absent locally.\",\n   \"surface\": \"/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site\",\n   \"method\": \"test -e\",\n   \"observation\": \"absent /home/vgpnk/Projects/webzites\\nabsent /home/vgpnk/Projects/plazir-15-site\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c2\",\n   \"anchor\": \"`ufo-fsd.kimi.pro`\\n  is a 612B React shell\",\n   \"claim\": \"GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.\",\n   \"surface\": \"GET https://ufo-fsd.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\\\"root\\\"></div>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c3\",\n   \"anchor\": \"GET it, don't HEAD (HEAD\u2192403).\",\n   \"claim\": \"HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.\",\n   \"surface\": \"HEAD https://ufo-fsd.kimi.pro\",\n   \"method\": \"HEAD\",\n   \"observation\": \"http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c4\",\n   \"anchor\": \"`plazir27.kimi.pro` returns 200 with a 5,995B\\n  preview-404 body (x-fc-request-id, Function-Compute ingress).\",\n   \"claim\": \"The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.\",\n   \"surface\": \"GET https://plazir27.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.\",\n   \"verdict\": \"STALE\",\n   \"correction\": \"As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c5\",\n   \"anchor\": \"canonical = `veigapunk.github.io/lucario/` (live)\",\n   \"claim\": \"The cited canonical GitHub Pages Lucario URL still serves the page.\",\n   \"surface\": \"GET https://veigapunk.github.io/lucario/\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario<span>.</span></h1>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c6\",\n   \"anchor\": \"plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path\",\n   \"claim\": \"Both explicitly named dead-slot Kimi pages still return HTTP 404.\",\n   \"surface\": \"GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page\",\n   \"method\": \"GET\",\n   \"observation\": \"https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c7\",\n   \"anchor\": \"**8** (incl. `/tetris/`,\",\n   \"claim\": \"The r16 live Plazir sitemap contained eight locations including tetris.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/sitemap.xml\",\n   \"method\": \"GET\",\n   \"observation\": \"200; 7 loc entries; tetris absent from sitemap although tetris/ returns 200\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.\"\n  },\n  {\n   \"id\": \"c8\",\n   \"anchor\": \"| `snake/index.html` `og:url` | 0 hits\",\n   \"claim\": \"The r16 live snake page had no og:url and speedrun had a Plazir self-canonical.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/\",\n   \"method\": \"GET\",\n   \"observation\": \"snake 200 og:url https://veigapunk.github.io/plazir-15-site/snake/; speedrun 200 canonical https://ds4cc.com/speedrun/\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.\"\n  }\n ]\n}",
    "expect": "accept",
    "why": "RFC 8259 \u00a7\u00a76 and 9 allow this integer, it is below the observed 4300-digit parser limit, and the C1 contract does not constrain extra metadata.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "receipt-large-integer-5000-digits",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "raw",
    "value": "{\n \"edgeProbe\": 99999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999,\n \"unit\": \"drift-detection\",\n \"path\": \"corpus/knowledge/drift-detection.md\",\n \"observedAt\": \"2026-10-21\",\n \"claims\": [\n  {\n   \"id\": \"c1\",\n   \"anchor\": \"the webzites and plazir source trees remain absent after the 2026-10-12 prune.\",\n   \"claim\": \"The documented webzites and plazir-15-site source trees are absent locally.\",\n   \"surface\": \"/home/vgpnk/Projects/webzites; /home/vgpnk/Projects/plazir-15-site\",\n   \"method\": \"test -e\",\n   \"observation\": \"absent /home/vgpnk/Projects/webzites\\nabsent /home/vgpnk/Projects/plazir-15-site\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c2\",\n   \"anchor\": \"`ufo-fsd.kimi.pro`\\n  is a 612B React shell\",\n   \"claim\": \"GET of ufo-fsd.kimi.pro still serves the cited 612-byte React-shell HTML.\",\n   \"surface\": \"GET https://ufo-fsd.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://ufo-fsd.kimi.pro/ size_download=612 content_type=text/html; charset=utf-8; body includes <title>DS4CC</title>, /assets/index-Bw9NLFv4.js and <div id=\\\"root\\\"></div>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c3\",\n   \"anchor\": \"GET it, don't HEAD (HEAD\u2192403).\",\n   \"claim\": \"HEAD of ufo-fsd.kimi.pro still returns 403, so GET is required to inspect the page.\",\n   \"surface\": \"HEAD https://ufo-fsd.kimi.pro\",\n   \"method\": \"HEAD\",\n   \"observation\": \"http_code=403 url=https://ufo-fsd.kimi.pro/ content_type=application/json; charset=utf-8\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c4\",\n   \"anchor\": \"`plazir27.kimi.pro` returns 200 with a 5,995B\\n  preview-404 body (x-fc-request-id, Function-Compute ingress).\",\n   \"claim\": \"The current preview-404 response uses the cited Function-Compute ingress and x-fc-request-id header.\",\n   \"surface\": \"GET https://plazir27.kimi.pro\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://statics.kimi.ai/pages/preview-404-en.html size_download=5995 content_type=text/html; headers show HTTP/2 302 with location https://statics.kimi.ai/pages/preview-404-en.html and server cloudflare, then HTTP/2 200 with server Byte-nginx, content-length 5995, x-request-id d006fefde588a635fd54dbba470aa211; body title is 404.\",\n   \"verdict\": \"STALE\",\n   \"correction\": \"As of 2026-10-21, GET https://plazir27.kimi.pro returns HTTP/2 302 to https://statics.kimi.ai/pages/preview-404-en.html and then HTTP/2 200 from Byte-nginx with a 5,995-byte HTML page titled 404 carrying x-request-id (not observed x-fc-request-id), so the old Function-Compute ingress label is not supported by this response.\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c5\",\n   \"anchor\": \"canonical = `veigapunk.github.io/lucario/` (live)\",\n   \"claim\": \"The cited canonical GitHub Pages Lucario URL still serves the page.\",\n   \"surface\": \"GET https://veigapunk.github.io/lucario/\",\n   \"method\": \"GET\",\n   \"observation\": \"http_code=200 url=https://veigapunk.github.io/lucario/ size_download=3435 content_type=text/html; charset=utf-8; body includes <title>lucario</title> and <h1>lucario<span>.</span></h1>.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c6\",\n   \"anchor\": \"plazir15.kimi.page / charter-ufo-fsd.kimi.page | 404 dead slots, RECREATE path\",\n   \"claim\": \"Both explicitly named dead-slot Kimi pages still return HTTP 404.\",\n   \"surface\": \"GET https://plazir15.kimi.page; GET https://charter-ufo-fsd.kimi.page\",\n   \"method\": \"GET\",\n   \"observation\": \"https://plazir15.kimi.page: http_code=404 url=https://plazir15.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8. https://charter-ufo-fsd.kimi.page: http_code=404 url=https://charter-ufo-fsd.kimi.page/ size_download=13409 content_type=text/html; charset=utf-8.\",\n   \"verdict\": \"HOLD\",\n   \"seat\": \"ReverifyDriftDetection\"\n  },\n  {\n   \"id\": \"c7\",\n   \"anchor\": \"**8** (incl. `/tetris/`,\",\n   \"claim\": \"The r16 live Plazir sitemap contained eight locations including tetris.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/sitemap.xml\",\n   \"method\": \"GET\",\n   \"observation\": \"200; 7 loc entries; tetris absent from sitemap although tetris/ returns 200\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, the live Plazir sitemap lists seven locations and omits tetris; tetris/ still returns 200, so the r16 eight-loc count and 103-vs-102 cross-source arithmetic remain dated history, not current totals.\"\n  },\n  {\n   \"id\": \"c8\",\n   \"anchor\": \"| `snake/index.html` `og:url` | 0 hits\",\n   \"claim\": \"The r16 live snake page had no og:url and speedrun had a Plazir self-canonical.\",\n   \"surface\": \"https://veigapunk.github.io/plazir-15-site/snake/index.html; https://veigapunk.github.io/plazir-15-site/speedrun/\",\n   \"method\": \"GET\",\n   \"observation\": \"snake 200 og:url https://veigapunk.github.io/plazir-15-site/snake/; speedrun 200 canonical https://ds4cc.com/speedrun/\",\n   \"verdict\": \"STALE\",\n   \"seat\": \"w2/HoldDriftDetection\",\n   \"correction\": \"As of 2026-10-21, live snake/index.html has one og:url to the Plazir snake URL and speedrun/ declares https://ds4cc.com/speedrun/ canonical; the absent checkout prevents a current source-vs-live synchronization verdict.\"\n  }\n ]\n}",
    "expect": "reject",
    "why": "RFC 8259 \u00a7\u00a76 and 9 permit numeric limits; the observed 4300-digit implementation limit may reject 5000 digits but C2 requires exit 1 or 2 without traceback.",
    "r23Observed": {
      "exit": 1,
      "traceback": true,
      "stdoutTail": ""
    }
  }
]
```

## Checked and held

### Isolation and immutable baseline

Exact clone/setup commands (all writes remained below the fresh scratch directory except this scoped report):

```sh
mktemp -d /tmp/kake-r24-GapC1PopulationEdge-XXXX
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone
git -C /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone rev-parse HEAD
git -C /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone switch --detach f7de3ab4e9f030a15a857a5a08631bd8e690f436
```

Observed clone HEAD: `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. There were no lane Git mutations, source-tree changes, remote fetches, sibling changes, builds, linters, formatters, or subagent dispatches.

Every mutation commit's parent is the frozen base. Exact commit metadata (`%H`, `%P`, `%aI`, `%cI`) is preserved in its result artifact. Commit subprocess environment was:

```text
GIT_AUTHOR_NAME=kake-shokunin
GIT_AUTHOR_EMAIL=kake@shokunin.local
GIT_COMMITTER_NAME=kake-shokunin
GIT_COMMITTER_EMAIL=kake@shokunin.local
GIT_AUTHOR_DATE=2026-10-21T12:00:00Z
GIT_COMMITTER_DATE=2026-10-21T12:00:00Z
```

For each case, the exact command pattern was the following, with `<id>` replaced by that case's ID; `write` performed the whole-file byte replacement from its raw `value`:

```sh
git -C /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone -c core.hooksPath=/dev/null -c commit.gpgsign=false switch --detach f7de3ab4e9f030a15a857a5a08631bd8e690f436
git -C /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone -c core.hooksPath=/dev/null -c commit.gpgsign=false add -- .ufo/waves/round-23/receipts/drift-detection.json
git -C /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone -c core.hooksPath=/dev/null -c commit.gpgsign=false commit -m 'r24 probe <id>' -- .ufo/waves/round-23/receipts/drift-detection.json
```

After measuring the mutant, a `finally` block restored the original UTF-8 file through `write`, staged only that receipt and committed with message `r24 restore <id>` using the same fixed environment. The detector was then invoked with that restoration commit. The next mutation began again at the frozen base, not at the previous mutant.

### Pristine and restored detector held

Exact pristine command (run once initially and again before each mutation):

```sh
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1PopulationEdge-nUEx/clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436
```

Exact selected pristine stdout lines:

```text
 "accepted": 17,
 "claimVerdicts": {
  "HOLD": 79,
  "STALE": 55,
  "UNVERIFIABLE": 42
 },
 "total": 17,
```

Exit 0; stderr empty. Every restoration produced exit 0, no traceback and 17/17; full individual outputs are retained. The four ordinary reject cases returned 16/17 and no traceback, so truncated JSON, a top-level array, a UTF-8 BOM, and the bad-last duplicate were actually killed. The valid 1,000-digit extra-member control returned 17/17 with no traceback.

### Before / mutant / exact restoration evidence

For **every row**, `beforeSha256`, `restoredSha256`, and the final worktree receipt digest equal:

`212fa028494dbeba1725932901d9cd21abe020512f7320f626bc418732d0a8f8`

The original receipt is 5,209 bytes. Each restoration was additionally compared with the original Git blob for exact byte equality, not merely semantic JSON equality. Per-case mutated digests and both commit IDs:

| Case | Mutation commit | Mutated receipt SHA-256 | Restored commit |
|---|---|---|---|

| receipt-invalid-json-truncated | `db69e6d35236c0f62510a6438cb2d5816b764ae3` | `d359e05fdb5ea0754230fefe7f84f93d17db86342f3ada3080f17561bb9db242` | `eb7585c7afbedbdfc0bc6dfcb7479e48292d5a92` |

| receipt-array-not-object | `edd14d8944f472694519da40dbb34a7e4c9bdc9b` | `f68fbd89edcdd57e2f3dc51918d7d272e0ab05076aadda117eef403042344bb0` | `c2969879f0f0ad5ef2fede88d37578278df70fe6` |

| receipt-utf8-bom | `f857e2f47cc59e0c0f2d6b7f06c2545117fa5c9d` | `f12eab61df50cce6f88a313ffdb053405928382056b70244823e030c0af0cd56` | `39ef7dc0a2d714d45e058a91063d0a207dd81310` |

| receipt-nan-token | `265ffb797235d71c32dfd3c721197617aed1b3f5` | `db14eeb7f0b4432e76bf888988b5b7c026448759c66155727b5b035405813c9f` | `7a6cf5d51e470bde136773ef932cfcdc7aa1b05a` |

| receipt-infinity-token | `29d7e2f640d0b69eb8c4f127874b8678e33fe755` | `56a7d28cacf7e77af2ecca7cb9fa4fa26047459f0efc4ee9cfeceb9e6d829110` | `ab99642f1cbc55070edbc7837c518491ff4c3510` |

| receipt-negative-infinity-token | `0d8fc7fbbf89317253db95ede956f06270bf1a7a` | `7a72502ea0c5a178eb64f4aa922d864d81b840a0a55ceef1edeeb2fec7a99c93` | `973bd1b96e3e918c06449664890a4beceadf5a6b` |

| receipt-duplicate-unit-bad-first | `b70c51f4ab28a8b3488a329477dcdad5a758f5e7` | `84c1728decaf1632094156ea5019c6a5d9d56b199d05e9200192e684aeabed34` | `9e5773c291c698a5b4f510480f617239ca8cd3c7` |

| receipt-duplicate-unit-bad-last | `25777c339f49c2b6d830ab87c1ee0155a1896d55` | `e16d904c5c90d84412c8f29023c9afd64a0099ec66fad057de77399af331351a` | `4dca55f26d93867036e4529f1f75ba6ce7ee246d` |

| receipt-large-integer-1000-digits | `77efc1c0c68465966063abb5476352d09c3939fd` | `ba714db98e261933f05884ac4329d480552589f1f00e45f7b4de0ae7c99f5a0e` | `b96f246327a96444808ea9e240b9fd262a41c051` |

| receipt-large-integer-5000-digits | `da57c1f1d6e25757b1001468129de4d3c72e014f` | `95630e7a9f8f6e39d780706e56f7358466d3fc93c1b4e09887a078071f2c4027` | `cf6d63a9ee396d62665af2272b43ab89f971d2d4` |


Final clone HEAD is restoration commit `cf6d63a9ee396d62665af2272b43ab89f971d2d4`; its detector accepted 17/17, exit 0, no traceback. Historical runner SHA-256 before and after all probes remained `c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5`.

### Preserved artifacts

All paths are absolute. The result artifacts contain exact commands, full stdout/stderr, pristine and restored results, mutation/restoration commit outputs, and fixed-date commit metadata. The fixtures are exact UTF-8 bytes, including the BOM or malformed syntax where applicable.

| Artifact | SHA-256 |
|---|---|

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/baseline.json` | `d58042a1f06ab3dc8e24bce1fba38cc50269d04388843a628232f1fdbd066110` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/input-specs.json` | `1b1ba9d43f046750280eb01aa5c3ba043356819c59490458cf854abb98eadcdb` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/cases.json` | `982808d9c5dbc2211c723a003b26dc2f121ce371d9f6741a3613fedc40d52ecd` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-invalid-json-truncated.receipt` | `d359e05fdb5ea0754230fefe7f84f93d17db86342f3ada3080f17561bb9db242` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-invalid-json-truncated.result.json` | `9516b1354f5ae193f20641fc115776dff0410e6641ff2d698578cfbbaaafb251` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-array-not-object.receipt` | `f68fbd89edcdd57e2f3dc51918d7d272e0ab05076aadda117eef403042344bb0` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-array-not-object.result.json` | `9e1149c7a0262d212940e0dc5ac8ebc1ee30f8282665132858eaca12d0d0087c` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-utf8-bom.receipt` | `f12eab61df50cce6f88a313ffdb053405928382056b70244823e030c0af0cd56` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-utf8-bom.result.json` | `d5fe6d7a258e27973361d32e664e02c9ca4b6b902b0d5ea5e5c5330c890f5384` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-nan-token.receipt` | `db14eeb7f0b4432e76bf888988b5b7c026448759c66155727b5b035405813c9f` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-nan-token.result.json` | `f298bf8760ba43e71d9b174d0909613024290b728d35ba51fcb8e0fe6e6e0949` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-infinity-token.receipt` | `56a7d28cacf7e77af2ecca7cb9fa4fa26047459f0efc4ee9cfeceb9e6d829110` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-infinity-token.result.json` | `289e3875499367b10f4a622ec33e654de88a238bd19115c24574465994e4ee6b` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-negative-infinity-token.receipt` | `7a72502ea0c5a178eb64f4aa922d864d81b840a0a55ceef1edeeb2fec7a99c93` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-negative-infinity-token.result.json` | `209c70afdc110b17529c58931566b91cf4f3344f464794d96ee3c0c987021951` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-duplicate-unit-bad-first.receipt` | `84c1728decaf1632094156ea5019c6a5d9d56b199d05e9200192e684aeabed34` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-duplicate-unit-bad-first.result.json` | `372a23881e7b5f85648e042c19e2db2bad56c6462a866615b7e1e10544f053a5` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-duplicate-unit-bad-last.receipt` | `e16d904c5c90d84412c8f29023c9afd64a0099ec66fad057de77399af331351a` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-duplicate-unit-bad-last.result.json` | `f5e620cc923d0987dda9be3d59bc08f96bb7658569b9c20c4afc2967d8d2a936` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-large-integer-1000-digits.receipt` | `ba714db98e261933f05884ac4329d480552589f1f00e45f7b4de0ae7c99f5a0e` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-large-integer-1000-digits.result.json` | `eefcac550e47414a92d647776f2482427738d891451aaf1fdfa934e7da1e603f` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-large-integer-5000-digits.receipt` | `95630e7a9f8f6e39d780706e56f7358466d3fc93c1b4e09887a078071f2c4027` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/receipt-large-integer-5000-digits.result.json` | `eba31c6a1c5d85e931b5b39e4b09f50303760c280bb98cda0f30440feeec1827` |

| `/tmp/kake-r24-GapC1PopulationEdge-nUEx/manifest.json` | `4067c1d4afbbc22eb09a3c35fd180bc0bbbd9e6633f8ec028e253460abe366a9` |

## Limits

- This is a bounded audit of the **C1 receipt-file parsing boundary** using one committed populated receipt. It does not exercise the C2 network fetch schema or authenticate original network observations, and it does not verify the maintained replacement script.
- Ten mutated executions, ten per-case pristine executions, ten restored executions, and one initial pristine execution were run. The population was never changed; no baseline failed.
- The integer-limit observation is interpreter-specific: existing Python **3.14.8** reports a **4,300-digit** limit. An interpreter configured differently might accept 5,000 digits. RFC 8259 permits a numeric limit; a conforming control below this observed limit was run to distinguish legal large numbers from non-JSON tokens.
- The receipt's historical `observedAt: "2026-10-21"` was preserved. [RFC 3339 §5.6](https://www.rfc-editor.org/rfc/rfc3339#section-5.6) defines `full-date` separately from `date-time = full-date "T" full-time`; this probe does not assert that the historical date-only field is an RFC 3339 date-time, nor tighten that separate contract at the expense of frozen controls.
- [RFC 9110 §8.3.1](https://www.rfc-editor.org/rfc/rfc9110#section-8.3.1) defines HTTP `type/subtype` media types. This C1 receipt has no media-type field under test; no acceptance decision here rests on that unrelated grammar.
- Opened primary JSON authority: [RFC 8259 §§2–6, 8.1, 9](https://www.rfc-editor.org/rfc/rfc8259). §4 uniqueness is SHOULD-level and §8.1 BOM ignoring is MAY-level. These policy distinctions are explicit above; they are not silently upgraded to MUST-level defects.
- The parent approved `op: raw` with exact UTF-8 file text in `value` as a schema extension; ordinary set/delete JSON-path semantics cannot preserve these byte-level cases. The emitted array uses that approved operation, not an invented set-at-root convention. The adapter itself was not exercised by this audit.
- Existing tools used: Python **3.14.8**, Git **2.56.0**, and `sha256sum`. **No tools were installed or updated**; no pacman transaction or host-service restart was attempted.
- No independent round admission is claimed. The L1 integration writer decides which policy-strengthening candidates enter the frozen malformed-case population.
