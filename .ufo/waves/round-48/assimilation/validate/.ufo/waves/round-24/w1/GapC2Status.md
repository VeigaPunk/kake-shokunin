## Verdict

Author-side C2 gap audit; owned axis: **operability**. **Nine executed cases: six malformed receipts killed, one malformed receipt survived, and two acceptance controls held.** No case was inconclusive. The survivor is a stored HTML page labeled HTTP 204.

The pristine frozen revision accepted **12/12** (exit 0). Every restored replay accepted **12/12** (exit 0), with no traceback. Across all 19 bounded detector invocations, stderr was empty and the last stdout line was exactly `}`. This is a historical-runner coverage finding, not independent admission or an integrated fix.

## Findings

### P2 — `status-204-page` survives despite an impossible response body

**Impacted claim/axis:** C2 / operability: malformed-receipt rejection.

**Smallest mutation:** change only `status: 200` to `status: 204` on line 10 of `/tmp/kake-r24-GapC2Status-clone/.ufo/waves/round-23/live/ds4cc-primary/fetch.json`. Leave the original 76,159-byte `page.html`, its SHA-256, `bytes`, valid media type, timestamp, and clean canonical audit unchanged. The mutant therefore exercises status/body consistency rather than a broken audit or digest.

**Expected detector:** the historical C2 replay should reject this receipt with exit 1 or 2 and no Python traceback under HTTP response semantics. [RFC 9110 §15.3.5](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.3.5) says: “A 204 response is terminated by the end of the header section; it cannot contain content or trailers.” The historical docstring's shorthand “served (2xx text/html)” is broader than that semantic rule; this discrepancy is the identified gap, not a failure of the existing numeric range check.

**Exact command:**

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 2cac052a281132ebdb500588705ee5e06fdad7f8
```

**Observed:** exit 0, accepted 12/12, traceback false, stderr `""`. Exact affected-surface stdout excerpt:

```text
  {
   "id": "ds4cc-primary",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
```

**Verdict:** survived. Baseline and restored bytes both passed, so this is not a baseline-failure inference.

**Smallest fix:** in the maintained `scripts/receipt_replay.py`, add a structural/semantic validation problem for a status-204 receipt that stores response content (`page.html`, or a positive recorded body length) before accepting canonical replay. Preserve the strict integer/range guard and archived round-23 runners. Merely replaying the page's canonical audit cannot detect the contradictory HTTP status. No implementation or contract change was made by this leaf.

### Contract and standards basis for expectations

- Historical runner: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py:7-15` documents the served/non-served branches; lines 36-39 use `200 <= status < 300`; lines 58-59 require `type(status) is int` and the inclusive range 100–599. The exact-int requirement is the local receipt contract, not a claim that JSON itself has separate integer and floating-point primitive types.
- [RFC 8259 §3](https://www.rfc-editor.org/rfc/rfc8259.html#section-3) distinguishes booleans, strings and numbers. [§6](https://www.rfc-editor.org/rfc/rfc8259.html#section-6) permits a fractional representation such as `200.0`; rejecting it here preserves the runner's explicit application-level exact-int requirement. It is **not** invalid JSON. No coercion is implied by the JSON standard.
- [RFC 9110 §15](https://www.rfc-editor.org/rfc/rfc9110.html#section-15) defines a three-digit integer code within 100–599 inclusive, 1xx as informational, 2xx as successful, and 3xx as redirection. It requires treating unrecognized codes as the x00 code of their class. Thus `299` is an acceptance control, while `199`/`300` with the retained served-page artifacts violate the documented branch contract. The latter cases do not claim that all `300` responses are malformed HTTP.
- [RFC 9110 §8.3.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.3.1) supplies the media-type grammar; unchanged `text/html; charset=utf-8` is valid. [RFC 3339 §5.6](https://www.rfc-editor.org/rfc/rfc3339.html#section-5.6) supplies the timestamp grammar; unchanged `2026-10-21T06:33:03Z` is well-formed. Neither field was mutated in this scoped status audit, and no new timestamp/media-type coverage is claimed.

### Executed C2 malformed-case array

Every object below corresponds to an actual committed sandbox snapshot and an actual run of the historical runner. The retained original `audit.json`/`page.html` are intentional for all page-status cases. The `status-200-control` set operation is byte-identical to the original field, recorded in an explicit empty control commit. `stdoutTail` is literally the final output line, so detailed failure information is recorded separately below and in the evidence bundle.

```json
[
  {
    "id": "status-boolean-true",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": true,
    "expect": "reject",
    "why": "The historical receipt contract requires type(status) is int; RFC 8259 §3 distinguishes true from a number, and RFC 9110 §15 requires a three-digit integer status code.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "status-float-200",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": 200.0,
    "expect": "reject",
    "why": "The historical runner requires type(status) is int rather than coercing a floating-point value; RFC 8259 §6 permits 200.0 as JSON but does not require this application to accept that receipt representation.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "status-string-200",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": "200",
    "expect": "reject",
    "why": "The historical receipt contract requires an integer status without string coercion; RFC 8259 §3 distinguishes strings from numbers and RFC 9110 §15 describes an integer status code.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "status-199-page",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": 199,
    "expect": "reject",
    "why": "The runner documents stored page.html only for 2xx text/html responses, while RFC 9110 §15 classifies 199 as informational rather than a final served response.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "status-300-page",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": 300,
    "expect": "reject",
    "why": "The runner documents stored page.html only for 2xx text/html responses, and RFC 9110 §15 classifies 300 as redirection rather than 2xx success.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "status-204-page",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": 204,
    "expect": "reject",
    "why": "The unchanged receipt claims a 76159-byte page body, but RFC 9110 §15.3.5 says a 204 response cannot contain content or trailers, despite the historical runner’s broader 2xx text/html shorthand.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "status-negative",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": -1,
    "expect": "reject",
    "why": "RFC 9110 §15 limits valid HTTP status codes to 100 through 599 inclusive, so -1 cannot record a usable HTTP response.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "status-200-control",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": 200,
    "expect": "accept",
    "why": "This is the unmodified positive control: the original 200 text/html page, matching digest and audit satisfy the documented served-response branch and RFC 9110 §15.3.1.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "status-299-control",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": 299,
    "expect": "accept",
    "why": "The integer 299 remains inside the documented 2xx served-response range, and RFC 9110 §15 requires treating an unrecognized status as the x00 status of its class.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  }
]
```

## Checked and held

### Isolation, commits, and actual outcomes

Clone command actually run:

```text
git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-GapC2Status-clone
git -C /tmp/kake-r24-GapC2Status-clone rev-parse HEAD
git -C /tmp/kake-r24-GapC2Status-clone switch --detach f7de3ab4e9f030a15a857a5a08631bd8e690f436
```

Observed clone HEAD: `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. Every subsequent case snapshot descends from that revision through exact restoration commits; no cumulative receipt mutations were carried into the next case. Only the one `fetch.json` status line was changed. `audit.json` and `page.html` never changed.

All 17 sandbox commits used `GIT_COMMITTER_DATE=2026-10-21T12:00:00Z` and `GIT_AUTHOR_DATE=2026-10-21T12:00:00Z`. Actual commit argv, fixed environment, stdout and full commit identities are preserved in the evidence bundle. Hooks and commit signing were explicitly disabled for these isolated scratch commits.

| Case | JSON value | Expect | Exit | Accepted | Probe verdict | Case revision | Restored revision |
|---|---|---|---:|---:|---|---|---|
| `status-boolean-true` | `true` | reject | 1 | 11/12 | killed | `2101baba55bf77d8c050e7a20f45a2d495085f09` | `8b94c5ea53d22906d02fb7ec490ce57a373c764d` |
| `status-float-200` | `200.0` | reject | 1 | 11/12 | killed | `ec18c3f88e45ad549e3a5c59b018875169b5201b` | `1bf50d256d3760bab8366e0fe1d0a6ada0053b51` |
| `status-string-200` | `"200"` | reject | 1 | 11/12 | killed | `fc3059abfe53cdbd2fada0539c34c3b96baf08b6` | `784b2aea71dcb22fc77d84e0f14b41fce4eda540` |
| `status-199-page` | `199` | reject | 1 | 11/12 | killed | `2dc6f86cc340e0e3fabeedc47562fe6df49821fb` | `156754ae2bd2a9da0c30ae48ecbb0680b12cc7ad` |
| `status-300-page` | `300` | reject | 1 | 11/12 | killed | `f0fec68ced03dce2f7a2748bdd717883bfb65b65` | `506af7bd6178c19281bc96fcf50fe8aed65cf0f8` |
| `status-204-page` | `204` | reject | 0 | 12/12 | survived | `2cac052a281132ebdb500588705ee5e06fdad7f8` | `487b916e0c5c9138351ed67a54bbc959904f5086` |
| `status-negative` | `-1` | reject | 1 | 11/12 | killed | `a16d6036b180545915fa17ba00b0984f654972e7` | `fd82fad1ee54a2bf3b406e74d3d1f2c0f4934582` |
| `status-200-control` | `200` | accept | 0 | 12/12 | control held | `6dcc1dddc5657fb81f8d2d36c4afe9ad07d4eb15` | `6dcc1dddc5657fb81f8d2d36c4afe9ad07d4eb15` |
| `status-299-control` | `299` | accept | 0 | 12/12 | control held | `93d6af4d34f7bdfbcb2f7121061b2265892e60e2` | `5cb760084dc3e02b986311130e159ea2aece696b` |

`true`, `200.0`, `"200"`, and `-1` each produced the following exact affected-surface stdout excerpt (the strict usable-response guard held):

```text
  {
   "id": "ds4cc-primary",
   "pass": false,
   "problems": [
    "fetch did not record a usable HTTP response",
    "page.html stored for a non-served response",
    "non-served surface lacks a matching not-served receipt"
   ],
   "verdict": "not-served"
  },
```

`199` and `300` each produced the following exact affected-surface stdout excerpt (the served-range boundaries held):

```text
  {
   "id": "ds4cc-primary",
   "pass": false,
   "problems": [
    "page.html stored for a non-served response",
    "non-served surface lacks a matching not-served receipt"
   ],
   "verdict": "not-served"
  },
```

The pristine run, both acceptance controls (`200`, `299`) and every restored run produced the same clean affected-surface row shown for the survivor above, with accepted 12/12 and exit 0. `true` being a Python `int` subclass did not create acceptance: the top-level validator already uses the exact-type guard, and `true` also lies outside the HTTP range.

### Before/after hashes and byte-exact restoration

Before **every** case and after **every** restoration, fetch SHA-256 was:

```text
a860e0a3eba641411850f52c112ee127bc96cd050bfa7ac1024c911d7f1a9f3c
```

Mutated/control fetch SHA-256 values actually observed by `sha256sum`:

| Case | SHA-256 at the case snapshot |
|---|---|
| `status-boolean-true` | `bae9d396a2421b5aef681d81717c6e60c7b7ff99f290203372e43e885e2d4d52` |
| `status-float-200` | `09978322598ff5e9c713af96e1628a45d0be1dfcd457dca29d81ac2856f5eb6a` |
| `status-string-200` | `e6876a71702792fd87706652c54f0be500064f32bab5503871dcd736ea586437` |
| `status-199-page` | `66d4653534ae56b164e5ba7b2cdad9d5c75a4fa8c5101dd4f1c58bf6b7c3981c` |
| `status-300-page` | `04456e72df0bc3c59e1d7db2e4d5395db9533626fec3a558fdb37b82e1cda7d0` |
| `status-204-page` | `9e481d19d618b6b25a8a9382d1015fcb3f02467c1cca68a38bf793e065ee8dea` |
| `status-negative` | `4844c2eae5949f2f8b1d84749970ef77c6f47cec3d48a0b5fa5f88c3bdc9ef8f` |
| `status-200-control` | `a860e0a3eba641411850f52c112ee127bc96cd050bfa7ac1024c911d7f1a9f3c` |
| `status-299-control` | `85f5c9278cc287ae3224e9baec98b37915b7fd4a12628e94b43a7e1531cf7398` |

The following hashes held in all 19 detector records (absolute input paths are stored in each record):

```text
9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75  /tmp/kake-r24-GapC2Status-clone/.ufo/waves/round-23/live/ds4cc-primary/audit.json
ccb3f46eda1ce3270df1e3373d49c4034025c4f475a6999142279e03b00b2bb8  /tmp/kake-r24-GapC2Status-clone/.ufo/waves/round-23/live/ds4cc-primary/page.html
91134d27af6c48f8e8bd6e604e533396f6d9c3542d1285ec1e3901f6358e5653  /tmp/kake-r24-GapC2Status-clone/.ufo/waves/round-23/measure_c2.py
91134d27af6c48f8e8bd6e604e533396f6d9c3542d1285ec1e3901f6358e5653  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py
```

Final clone HEAD: `fd82fad1ee54a2bf3b406e74d3d1f2c0f4934582`. Exact committed-tree restoration command:

```text
git -C /tmp/kake-r24-GapC2Status-clone rev-parse 'f7de3ab4e9f030a15a857a5a08631bd8e690f436^{tree}' 'fd82fad1ee54a2bf3b406e74d3d1f2c0f4934582^{tree}'
```

Exact output, exit 0:

```text
ba4a40e4604c1f207f23deeb68c117409b76be70
ba4a40e4604c1f207f23deeb68c117409b76be70
```

Thus the final committed clone tree equals the frozen base tree, not just a reconstructed JSON value. Final restored behavioral replay also accepted 12/12 with exit 0 and no traceback.

### Exact detector commands and retained output

Each invocation was bounded to 120 seconds, used the same absolute historical runner and isolated clone, and recorded complete stdout/stderr without alteration. These are the actual commands (labels identify their raw JSON records):

```text
pristine:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436
status-200-control:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 6dcc1dddc5657fb81f8d2d36c4afe9ad07d4eb15
restored-status-200-control:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 6dcc1dddc5657fb81f8d2d36c4afe9ad07d4eb15
status-boolean-true:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 2101baba55bf77d8c050e7a20f45a2d495085f09
restored-status-boolean-true:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 8b94c5ea53d22906d02fb7ec490ce57a373c764d
status-float-200:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision ec18c3f88e45ad549e3a5c59b018875169b5201b
restored-status-float-200:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 1bf50d256d3760bab8366e0fe1d0a6ada0053b51
status-string-200:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision fc3059abfe53cdbd2fada0539c34c3b96baf08b6
restored-status-string-200:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 784b2aea71dcb22fc77d84e0f14b41fce4eda540
status-199-page:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 2dc6f86cc340e0e3fabeedc47562fe6df49821fb
restored-status-199-page:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 156754ae2bd2a9da0c30ae48ecbb0680b12cc7ad
status-299-control:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 93d6af4d34f7bdfbcb2f7121061b2265892e60e2
restored-status-299-control:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 5cb760084dc3e02b986311130e159ea2aece696b
status-300-page:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision f0fec68ced03dce2f7a2748bdd717883bfb65b65
restored-status-300-page:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 506af7bd6178c19281bc96fcf50fe8aed65cf0f8
status-204-page:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 2cac052a281132ebdb500588705ee5e06fdad7f8
restored-status-204-page:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision 487b916e0c5c9138351ed67a54bbc959904f5086
status-negative:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision a16d6036b180545915fa17ba00b0984f654972e7
restored-status-negative:
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2Status-clone --revision fd82fad1ee54a2bf3b406e74d3d1f2c0f4934582
```

Complete run and commit evidence: `/tmp/kake-r24-GapC2Status-RkfJ/probe-evidence.json`. The separately importable case array is `/tmp/kake-r24-GapC2Status-RkfJ/cases.json`. The bundle includes the unmodified baseline, nine case outputs, nine restored outputs, all commit evidence, exact hash results and tree restoration evidence.

Absolute-path SHA-256 inventory for every produced scratch evidence file:

```text
5675f7ae5ce4a6b885836d59997f192919906b89b662370a777c8f2205ac1968  /tmp/kake-r24-GapC2Status-RkfJ/versions.json
135d876432eae1509f8f2d93308c57faee759bee25ab9c360950b32759f439c0  /tmp/kake-r24-GapC2Status-RkfJ/pristine.json
22c1c97e1963a8a5d10510a11d2a99e57df6f7c2802f3b0f85003e57b3c3be75  /tmp/kake-r24-GapC2Status-RkfJ/status-200-control.json
e8517e0d547673af4279885a243989f98ffe1702c7f477448ca1ded603494aef  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-200-control.json
2ce8f00aa2e2f6216d9c9fca87dfe2af9948d62b49c73620f41f49b7236176e4  /tmp/kake-r24-GapC2Status-RkfJ/status-boolean-true.json
a1a751289bcfaa02326a53c8e4d554cf4c7e292f6eb4f925d2f7e8beecfb9b46  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-boolean-true.json
e1d77ffcea890f1379b760da12813cf33b620981c3b42808fcfb560c9ac00d45  /tmp/kake-r24-GapC2Status-RkfJ/status-float-200.json
fa98f9c166ad4d4c53efbad1712a49c71e973d37d6f8c91b8eaf55c41c902dc2  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-float-200.json
234e2a705e8d4e0b8ee5cb3155a752946e110134cac33f0f6a456ba6cd3d137d  /tmp/kake-r24-GapC2Status-RkfJ/status-string-200.json
2a208364b06f12599a728a34391dae3f5b0b8c5537116c9a52d1f50a94f687ca  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-string-200.json
52096ca21870588c2cc9ef57c20f895a09a68f4a5512be340985d5b37871ed89  /tmp/kake-r24-GapC2Status-RkfJ/status-199-page.json
60d2f7494fd871a5fce27392ef84a0563e8ab3e1e9012321967ac429541fdf4b  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-199-page.json
b8ad588374d68729f9831fbb4e305fc9d339a73bacf6a3b72d51691a5102a1aa  /tmp/kake-r24-GapC2Status-RkfJ/status-299-control.json
14fedd67654511a5dda0b88e39518ab3de9014dfd24c54220499d71ca0c96942  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-299-control.json
c6f198d93f99a17d097bd8aee386a3f45c233caf40796549ca8c80a227c89ff9  /tmp/kake-r24-GapC2Status-RkfJ/status-300-page.json
6f664e02ac1bbfd0ac76aedc682231b65f913f080a7b6ca4bc5df757de4b51eb  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-300-page.json
af4595e19f456c90f07709597041f48e4697e7a6c1a560686fc5a1c4df2d3d0c  /tmp/kake-r24-GapC2Status-RkfJ/status-204-page.json
7f7c9efa56e20a839384920202bb2a9a0be1ef13ba8ef9811feabae4f850ef15  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-204-page.json
ed5f9eeb70673110dfd9fb5fdd8500504a513880e02f50a44567aa3ec6349a70  /tmp/kake-r24-GapC2Status-RkfJ/status-negative.json
7b0f6ee2a878c8c5ab717605ae2f5eff777feb679b814117c5c48e44e4270aa7  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-negative.json
0676d709ca95856898719902854f72f05d468b13ff4ee773f4d9d534e56d25c9  /tmp/kake-r24-GapC2Status-RkfJ/status-200-control-commit.json
4a302145d831e8ff194fe435a538c568d9bcc8a75728b237a92cd8c97c3f447c  /tmp/kake-r24-GapC2Status-RkfJ/status-boolean-true-commit.json
09ed58cfa2298b918e30aa5ae8ae077d189b8e81a533f5872f262624650665e4  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-boolean-true-commit.json
af76674908d9df71553415d08bcc97002ea0479800cc9eeb34fb118d15097fef  /tmp/kake-r24-GapC2Status-RkfJ/status-float-200-commit.json
d5637843ea001fe37110de1813679fe5bf1121737e3d151ad29feff0a4fbad8d  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-float-200-commit.json
57a3fd964578565be891db021c1bd167fc97d9dbcb3e0733f43823ae38540e42  /tmp/kake-r24-GapC2Status-RkfJ/status-string-200-commit.json
5fdb8399f16a8a682f72a69b8537e65f7fafb83d8dccdfc8015ad50dcc96558e  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-string-200-commit.json
84b2b729457a081fd8993ac352c18899b02a2e91ec0ee96bff6e4993917c4885  /tmp/kake-r24-GapC2Status-RkfJ/status-199-page-commit.json
01ae9dcac077bfc3a5c2fb017ccb742b3e2441f072d817b05c3ac117800bd49c  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-199-page-commit.json
c65c76216c99c367ea4492d81006d9890927f63a32380bd234ca4fe12d5c303c  /tmp/kake-r24-GapC2Status-RkfJ/status-299-control-commit.json
142d1b452acbc3dbf0c85854a0abfd0a7a11771ebe0c4235d40320baadac1b0b  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-299-control-commit.json
4a1634132e05345075598e899b056ef78059f97d0b61a7551c8fd4f99a232186  /tmp/kake-r24-GapC2Status-RkfJ/status-300-page-commit.json
e105c262814ff5ae5e68c5f513347d8f4d40d7f158db699b735a65e32d3dc7a9  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-300-page-commit.json
7691639c93001db45bc76506799d2fe4eeba38601240319d55271bfe6c2617aa  /tmp/kake-r24-GapC2Status-RkfJ/status-204-page-commit.json
b52a5f355cf0812e860c51c2844a863ab27ddae8ce4390702e98aed80cf3a8d4  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-204-page-commit.json
7a890a064a6122a5b5caf95643ef899eabb13000eff54941feee46b38919f4a1  /tmp/kake-r24-GapC2Status-RkfJ/status-negative-commit.json
7cda2edc9dd4915cac05528833fa2e905bf27dcd9d3bc3638ecfbe2805991ff4  /tmp/kake-r24-GapC2Status-RkfJ/restored-status-negative-commit.json
ed5db652258a007142733e139b004eba641b1e962506a615380adc5d182e78d4  /tmp/kake-r24-GapC2Status-RkfJ/cases.json
71a6e18a20460711d0708d328a1fb9a732a7789cf6ba60ab6b8addb62cc0c65f  /tmp/kake-r24-GapC2Status-RkfJ/restoration.json
57c128ca0390aa5ce244bbd1ee593b5eca714a1a0c459db2c7291034436ddcf8  /tmp/kake-r24-GapC2Status-RkfJ/probe-evidence.json
ea83d9dbfbca8629dc5987473f10984dc2a98e54d6b72f3cca1419b7dafa7fe3  /tmp/kake-r24-GapC2Status-RkfJ/artifacts.sha256
```

## Limits

- Author-side, historical-runner audit only. No lane production file, historical runner, source-domain tree, index, fleet state, or sibling scratch copy was modified. The only lane write is this requested report. L1 remains sole integration writer and admission owner.
- No new replay implementation was executed, reviewed for acceptance, or integrated here. The status-204 finding must not be relabeled accepted merely to make coverage pass; the maintained replayer and its frozen population are the planner's integration surface.
- Focus was exactly the requested status typing, served-range boundaries, 204-with-page contradiction and a negative code. No no-page 204 control, exhaustive HTTP status semantics, malformed timestamps, media-type variants, redirects, or other receipt fields were probed in this assignment. A well-formed stored receipt still does not authenticate a past network observation.
- No builds, lint, formatters, live website requests, runtime substitutions, or subagents were used. Public read-only RFC documentation was the only web access.
- Existing tools used: `Python 3.14.8` and `git version 2.56.0`. No tools were installed or upgraded; no pacman transaction or host service change was attempted.
