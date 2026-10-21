# GapC2ContentType — C2 audit, media-type axis (round 24, author-side)

Base `f7de3ab4e9f030a15a857a5a08631bd8e690f436` · owned axis: **operability** · sandbox `/tmp/kake-r24-GapC2ContentType-i9gc/clone`.

## Verdict

Twelve committed content-type cases were exercised against the round-23 runner. Of seven cases that should be rejected as malformed receipt values, four raised an uncaught Python traceback and three were accepted as a valid `not-served` receipt. Five acceptance controls held: JSON `null` as the producer's absent-header representation, case-insensitive HTML media type, a trailing empty parameter, leading HTTP whitespace, and a syntactically valid non-HTML subtype. The frozen base itself accepted 12/12.

This is author-side C2 evidence only; it does not claim independent admission or an integrated fix.

## Findings

### P2 — Truthy non-string `contentType` crashes the historical replay

**Impacted claim/axis:** C2 / operability — malformed receipts must exit 1 or 2 without a traceback.

**Exact runner command for each case:** `python3 /tmp/kake-r24-GapC2ContentType-i9gc/clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ContentType-i9gc/clone --revision HEAD`.

**Observed:** `contentType` values `200`, `[200]`, `{"type":"text/html"}`, and `true` each exited 1 with empty stdout and an uncaught `AttributeError` on `ctype.split(";")`. Exact final stderr lines were `AttributeError: 'int' object has no attribute 'split'`, `AttributeError: 'list' object has no attribute 'split'`, `AttributeError: 'dict' object has no attribute 'split'`, and `AttributeError: 'bool' object has no attribute 'split'`, respectively. These are error exits, but violate the required no-traceback behavior.

**Smallest fix:** in maintained `scripts/receipt_replay.py`, validate `contentType`'s receipt shape before `served()`; preserve `null` as the producer's representation for an absent header, accept strings only after media-type validation, and return a normal rejection for other JSON types. Do not change the archived round-23 runners.

### P2 — Falsey invalid values and a comma-combined field are accepted

**Impacted claim/axis:** C2 / operability — malformed receipt rejection.

**Observed:** on the coherent `charter-kimi` 200/not-served fixture, `false`, `""`, and `"text/html, text/plain"` each exited 0 with `accepted: 12`, and the exact affected-surface fields were `"id": "charter-kimi"`, `"pass": true`, `"problems": []`, `"verdict": "not-served"`. `false` and the empty string are silently treated as absent by `fetch.get("contentType") or ""`; the comma value is silently classified as non-HTML. Additional exploratory committed probes with empty `[]` and `{}` also exited 0 with 12/12 accepted, for the same falsey short-circuit. In every accepted run, the literal stdout tail was `}`.

**Expected basis:** RFC 8259 §3 permits these JSON values but distinguishes arrays, objects, booleans, strings, and `null`; JSON validity does not make a value a valid Content-Type field. RFC 9110 §8.3 defines `Content-Type = media-type`, and §8.3.1 defines `media-type = type "/" subtype parameters`; an empty string is not a media type, and a comma-separated value is not one media type (Content-Type is a singleton field). `null` is different: the current `live_snapshot.py:172-173` receipt shape explicitly permits string or null, and RFC 9110 §8.3 permits an absent Content-Type field; the null case is therefore retained as an acceptance control. `text/htmlx` is a valid, distinct subtype, not malformed HTML. RFC 9110 §5.5 requires field parsing to exclude allowed leading whitespace before evaluation, so the leading-space control is valid. Its §5.6.6 grammar permits empty trailing parameters, so `text/html;` is also a valid acceptance control.

**Smallest fix:** validate non-null string values against the Content-Type media-type grammar before deciding `served` versus `not-served`; do not use general Python truthiness as a type/absence test. Keep syntactically valid non-HTML media types (including `text/htmlx`) on the not-served path.

### Executed C2 malformed-case array

Every object below was applied to a committed round-23 receipt and the historical runner was run at that case's commit. `stdoutTail` is the literal final stdout line; traceback details are recorded above because crash cases emitted no stdout.

```json
[
  {
    "id": "ctype-int-200",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": 200,
    "expect": "reject",
    "why": "RFC 9110 §8.3 requires a media-type field value, while RFC 8259 §3 makes 200 a JSON number rather than a string.",
    "r23Observed": {"exit": 1, "traceback": true, "stdoutTail": ""}
  },
  {
    "id": "ctype-list",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": [200],
    "expect": "reject",
    "why": "RFC 8259 §3 distinguishes arrays from strings, and an array cannot satisfy RFC 9110 §8.3.1's media-type grammar.",
    "r23Observed": {"exit": 1, "traceback": true, "stdoutTail": ""}
  },
  {
    "id": "ctype-dict",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": {"type": "text/html"},
    "expect": "reject",
    "why": "RFC 8259 §3 distinguishes objects from strings, and an object cannot satisfy RFC 9110 §8.3.1's media-type grammar.",
    "r23Observed": {"exit": 1, "traceback": true, "stdoutTail": ""}
  },
  {
    "id": "ctype-true",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": true,
    "expect": "reject",
    "why": "RFC 8259 §3 distinguishes a boolean from a string, and true cannot satisfy RFC 9110 §8.3.1's media-type grammar.",
    "r23Observed": {"exit": 1, "traceback": true, "stdoutTail": ""}
  },
  {
    "id": "ctype-false",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": false,
    "expect": "reject",
    "why": "The lane receipt shape permits a string or absent-header null, not false, and RFC 9110 §8.3 requires a media-type field value when Content-Type is present.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "ctype-null-absent",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": null,
    "expect": "accept",
    "why": "The lane producer permits null for an absent Content-Type and RFC 9110 §8.3 permits the field to be absent, so this is a valid non-served control.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "ctype-empty-string",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": "",
    "expect": "reject",
    "why": "An explicitly present empty string is not RFC 9110 §8.3.1's required type slash subtype media-type, unlike an absent field represented as null.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "ctype-uppercase-html",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": "TEXT/HTML; charset=utf-8",
    "expect": "accept",
    "why": "RFC 9110 §8.3.1 makes type and subtype tokens case-insensitive, so this is a valid text/html served-response control.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "ctype-trailing-semicolon",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": "text/html;",
    "expect": "accept",
    "why": "RFC 9110 §5.6.6 permits empty trailing parameters, so text/html; is valid media-type syntax for this served-response control.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "ctype-htmlx",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": "text/htmlx",
    "expect": "accept",
    "why": "text/htmlx is a syntactically valid distinct subtype under RFC 9110 §8.3.1 and should be accepted as a valid not-served response.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "ctype-leading-ows",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": " text/html",
    "expect": "accept",
    "why": "RFC 9110 §5.5 requires allowed leading field whitespace to be excluded before evaluating the field value, yielding valid text/html.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "ctype-comma-list",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": "text/html, text/plain",
    "expect": "reject",
    "why": "RFC 9110 §8.3 defines Content-Type as a singleton media-type field, whose §8.3.1 grammar does not admit a comma-separated list.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  }
]
```

## Checked and held

- Clone command: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-GapC2ContentType-i9gc/clone`; observed initial HEAD was exactly `f7de3ab4e9f030a15a857a5a08631bd8e690f436`.
- Frozen-base invocation: `python3 /tmp/kake-r24-GapC2ContentType-i9gc/clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ContentType-i9gc/clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436` → exit 0, `accepted: 12`, `total: 12`, every surface passed.
- Each reported case was committed with author and committer dates fixed at `2026-10-21T12:00:00Z`, then run at its commit using the command above with `--revision HEAD`. Per-case revisions and observed outcomes:

| Case | Revision | Observed |
|---|---|---|
| `ctype-int-200` | `e84c74f825912324c3c01540d6983b972b84e6e7` | exit 1; traceback; int `.split` AttributeError |
| `ctype-list` | `a57c0342bb0278568ab4f9aba099dfdd7a3d1ea6` | exit 1; traceback; list `.split` AttributeError |
| `ctype-dict` | `91fac3750bca4d47b26d11b43534e3991e97dc54` | exit 1; traceback; dict `.split` AttributeError |
| `ctype-true` | `f03f1fac526fd4c105d6377c41c1cc289e2b62ca` | exit 1; traceback; bool `.split` AttributeError |
| `ctype-false` | `c17d81c9c3ed7498e7fea53a8424b4b43c20562c` | exit 0; accepted 12/12; `charter-kimi` not-served |
| `ctype-null-absent` | `cdf69e3767c32c1ac7e89fd8422f506e688f2561` | exit 0; accepted 12/12; `charter-kimi` not-served |
| `ctype-empty-string` | `6a09c2c90dca5a3f1116c2b7a3dc14e4850f5c6d` | exit 0; accepted 12/12; `charter-kimi` not-served |
| `ctype-uppercase-html` | `020959c05f34bd121fe27fd99b5b821122ec5826` | exit 0; accepted 12/12; `ds4cc-primary` clean |
| `ctype-trailing-semicolon` | `3299a928b2cb73d243e52ce5df176e73df6cf823` | exit 0; accepted 12/12; `ds4cc-primary` clean |
| `ctype-htmlx` | `a7e2c136e23d41014dc9211bdccc89dfbcb3a16f` | exit 0; accepted 12/12; `charter-kimi` not-served |
| `ctype-leading-ows` | `87bbeb2aab67114d7fef1fb2f71ff74e52c33941` | exit 0; accepted 12/12; `ds4cc-primary` clean |
| `ctype-comma-list` | `bb9a84a084192c7376e2bd240c7fb9d257fa8fac` | exit 0; accepted 12/12; `charter-kimi` not-served |

- For the `charter-kimi` cases, the initial numeric-case commit also changed `status` and `audit.json.status` from 404 to 200 so the exercised response remained a coherent no-page not-served receipt while the truthy invalid values reached `served()`. No `page.html` existed for this surface. Later cases changed only `contentType`; all other surfaces were retained from the frozen base. The three positive HTML controls mutated only `ds4cc-primary.fetch.json` and retained its original page/audit.
- RFC 3339 §5.6 was not exercised on this media-type axis; timestamp bytes were unchanged. The round-24 `c2-population.json` path was absent when checked, so these are author-side candidate cases for L1 integration, not an assertion that a frozen round-24 population already contains them.
- No tool installs or updates were needed.

## Limits

- Only the historical round-23 C2 replay was measured; no implementation file or round-24 population was changed by this seat.
- The report's JSON array contains 12 cases; the empty-array and empty-object probes are separately disclosed in Findings as supplementary exploratory evidence and are not additional case objects.
- This measures receipt parsing and branch behavior only; it does not authenticate or re-observe any network response.
