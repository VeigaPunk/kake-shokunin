## Verdict

Recommend HOLD for the C2 operability claim pending the maintained replay's malformed-receipt validation. The base round-23 runner accepted 12/12 unmodified surfaces, but it also accepted malformed not-served receipts and raised an uncaught traceback for a truthy non-string Content-Type. The two requested not-served invariants themselves behaved correctly in the mutations: a not-served audit on an actual served 200 HTML response was rejected, and a stored `page.html` on a 404 was rejected. The 404 `text/html` no-page control remained accepted.

## Findings

### P1 — Malformed `contentType` values pass the not-served branch

`measure_c2.py:36-39` evaluates status before using `ctype`; for status 404 this short-circuits without validating `contentType`. The upstream replay producer's `live_snapshot.py:172-173` explicitly requires contentType to be a string or null. RFC 9110 §8.3.1 defines media-type syntax as type/subtype; RFC 8259 §3 allows numbers and booleans as JSON values, but does not make them media types. The case-insensitive valid header control is accepted as it should be.

Commands (each case was separately committed in the sandbox clone, then run against that commit):
- `python3 /tmp/kake-r24-GapC2NotServedShape-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2NotServedShape-clone --revision 51b9d465409497099baff9b81a60a83c6e81ceba` — exit 0, stderr empty, stdout tail `}`; exact surface output: `{"id":"charter-kimi","pass":true,"problems":[],"verdict":"not-served"}`.
- `python3 /tmp/kake-r24-GapC2NotServedShape-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2NotServedShape-clone --revision 7073c643e04f02c0408b156c1e030c5e1ddd08f3` — exit 0, stderr empty, stdout tail `}`; exact surface output: `{"id":"charter-kimi","pass":true,"problems":[],"verdict":"not-served"}`.
- `python3 /tmp/kake-r24-GapC2NotServedShape-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2NotServedShape-clone --revision b4d8931f9ee0ecdb8b8582bb070baefb7ff4dab1` — exit 0, stderr empty, stdout tail `}`; exact surface output: `{"id":"charter-kimi","pass":true,"problems":[],"verdict":"not-served"}`.
- Control: `python3 /tmp/kake-r24-GapC2NotServedShape-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2NotServedShape-clone --revision 8bd24b59a199c089efd9b5626ba5367504f5e851` — exit 0, stderr empty, stdout tail `}`; exact surface output: `{"id":"charter-kimi","pass":true,"problems":[],"verdict":"not-served"}`.

Impact: C2 / operability; malformed Content-Type metadata is treated as a passing not-served observation. Smallest fix: validate every non-null contentType's JSON type and media-type grammar before classifying the response, including the non-2xx branch.

### P1 — A not-served audit receipt accepts a floating-point status

RFC 9110 §15 defines status codes as three-digit integers. RFC 8259 §6 allows JSON numbers such as `404.0`, but that value is not an integer status in the receipt contract. Python dictionary equality makes `404.0 == 404`, so the exact receipt comparison at `measure_c2.py:75-77` accepts it.

Command: `python3 /tmp/kake-r24-GapC2NotServedShape-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2NotServedShape-clone --revision f595238d50106da9f21b8c2addf60d601f215331` — exit 0, stderr empty, stdout tail `}`; exact surface output: `{"id":"charter-kimi","pass":true,"problems":[],"verdict":"not-served"}`.

Impact: C2 / operability; malformed audit status values are accepted. Smallest fix: validate audit receipt field types (especially `status` with `type(value) is int`) before comparing values.

### P1 — Malformed `fetchedAt` values pass the not-served path's lexical date check

`measure_c2.py:56-57` checks only `fetchedAt[:10] < "2026-10-21"`. RFC 3339 §5.6 requires a full date-time with a time-offset and defines `date-month` as 01–12. Both the missing-offset timestamp and month 13 pass the runner unchanged.

Commands:
- `python3 /tmp/kake-r24-GapC2NotServedShape-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2NotServedShape-clone --revision 4bb37a1e119e377bf8c7179cb73fb0284b00de48` — exit 0, stderr empty, stdout tail `}`; exact surface output: `{"id":"charter-kimi","pass":true,"problems":[],"verdict":"not-served"}`.
- `python3 /tmp/kake-r24-GapC2NotServedShape-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2NotServedShape-clone --revision 973b6725d679107455eb2ff85e53ff77c7a74cdd` — exit 0, stderr empty, stdout tail `}`; exact surface output: `{"id":"charter-kimi","pass":true,"problems":[],"verdict":"not-served"}`.

Impact: C2 / operability; malformed timestamps count as verified receipts. Smallest fix: parse and validate the complete RFC 3339 date-time, including calendar ranges and offset, before applying the round-date threshold.

### P1 — Truthy non-string Content-Type crashes instead of a clean rejection

The `served()` call at `measure_c2.py:72` reaches `ctype.split(...)` at line 39 for a 200 response and a truthy numeric Content-Type. This produces an uncaught Python exception rather than the C2 contract's rejection with exit 1 or 2 and no traceback.

Command: `python3 /tmp/kake-r24-GapC2NotServedShape-clone/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2NotServedShape-clone --revision 482697d6e99752d55c5f731f38a54e2a96829b8c` — exit 1, stdout empty, traceback true, stderr ends exactly:
`AttributeError: 'int' object has no attribute 'split'`

Impact: C2 / operability; malformed receipts can terminate replay with a traceback. Smallest fix: validate `contentType` before calling `served()` and return a normal validation problem for invalid types.

## Checked and held

- Read the frozen contract at `.ufo/waves/round-24/contract.json` and the round-23 runner and producer. Round-24 `c2-population.json` was not present in the lane at audit time, so the mutations used the frozen round-23 population that the round-23 runner itself requires.
- Lane HEAD and clone-observed HEAD were both `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. The clone's baseline replay was exit 0, accepted 12/12, no traceback. The clone was reset to that base after all cases. The round-23 runner SHA-256 was `91134d27af6c48f8e8bd6e604e533396f6d9c3542d1285ec1e3901f6358e5653`; its hash matched the lane file and recorded round-23 result.
- Each mutation was committed independently with both `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE` set to `2026-10-21T12:00:00Z`, then replayed at that committed revision.
- The `not-served-audit-on-served-200` mutation was rejected at commit `d13a6951ba83857664d79c22eeaa678401e08fcd`, exit 1, no traceback; output problem: `audit.json {'error': None, 'exit': None, 'status': 200, 'verdict': 'not-served'} != reproduced {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}}`.
- The stored-page mutation was rejected at commit `712a7bb77622b6cae77e08318e24cf6052f4ab57`, exit 1, no traceback; output problem: `page.html stored for a non-served response`.
- RFC sources consulted: [RFC 3339 §5.6](https://www.rfc-editor.org/rfc/rfc3339.html#section-5.6), [RFC 9110 §8.3.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.3.1) and [§15](https://www.rfc-editor.org/rfc/rfc9110.html#section-15), [RFC 8259 §§3 and 6](https://www.rfc-editor.org/rfc/rfc8259.html#section-3).
- No tools were installed or updated. The `lsp` device was not mounted (`read xd://lsp` returned `No such tool`); no LSP semantic queries were available. No build, lint, formatter, or selftest was run.

C2 malformed-case array below contains only the ten mutations actually committed and replayed. For file-level `page.html` creation, `jsonPath: []` denotes the file contents; JSON receipt mutations use `jsonPath` as root-relative keys.

```json
[
  {
    "id": "not-served-audit-on-served-200",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/audit.json",
    "op": "set",
    "jsonPath": [],
    "value": {"verdict": "not-served", "status": 200, "exit": null, "error": null},
    "expect": "reject",
    "why": "The runner contract requires a 2xx text/html fetch to have the reproduced audit result, not a not-served receipt; RFC 9110 §8.3.1 defines text/html as a media type.",
    "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "not-served-404-page-html-stored",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/page.html",
    "op": "set",
    "jsonPath": [],
    "value": "<!doctype html><html><body>unexpected stored page</body></html>\n",
    "expect": "reject",
    "why": "The runner's documented not-served branch requires that page.html not be stored for a non-2xx text/html fetch.",
    "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "not-served-404-case-insensitive-html-control",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": "TEXT/HTML; CHARSET=UTF-8",
    "expect": "accept",
    "why": "RFC 9110 §8.3.1 treats media type type/subtype tokens case-insensitively; the 404 status remains non-served regardless.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "not-served-404-numeric-content-type",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": 5,
    "expect": "reject",
    "why": "The producer's reaudit contract accepts contentType only as a string or null; a number is not an RFC 9110 §8.3.1 media type, though valid as an RFC 8259 JSON number.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "not-served-404-boolean-content-type",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": false,
    "expect": "reject",
    "why": "The producer's reaudit contract permits contentType only as a string or null; false is a JSON boolean, not an RFC 9110 §8.3.1 media type.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "served-200-truthy-numeric-content-type",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": 5,
    "expect": "reject",
    "why": "The producer's reaudit contract permits contentType only as a string or null; a truthy number must be rejected cleanly rather than passed to media-type parsing.",
    "r23Observed": {"exit": 1, "traceback": true, "stdoutTail": ""}
  },
  {
    "id": "not-served-404-invalid-media-type-string",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["contentType"],
    "value": "text html",
    "expect": "reject",
    "why": "RFC 9110 §8.3.1 media-type grammar requires type slash subtype; this malformed Content-Type must not pass as an ordinary not-served receipt.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "not-served-audit-float-status",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/audit.json",
    "op": "set",
    "jsonPath": ["status"],
    "value": 404.0,
    "expect": "reject",
    "why": "RFC 9110 §15 defines status-code as a three-digit integer; RFC 8259 permits this JSON number spelling, but the audit receipt status must remain an integer.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "not-served-fetched-at-missing-offset",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["fetchedAt"],
    "value": "2026-10-21T06:33:20",
    "expect": "reject",
    "why": "RFC 3339 §5.6 requires full-time to include a time-offset (Z or plus/minus HH:MM); this timestamp is not a complete date-time.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "not-served-fetched-at-invalid-month",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": ["fetchedAt"],
    "value": "2026-13-21T06:33:20Z",
    "expect": "reject",
    "why": "RFC 3339 §5.6 defines date-month as 01-12; lexical prefix comparison accepts this invalid month.",
    "r23Observed": {"exit": 0, "traceback": false, "stdoutTail": "}"}
  }
]
```

## Limits

This audit measures only the round-23 replay against the requested malformed not-served variants at base `f7de3ab4e9f030a15a857a5a08631bd8e690f436`; it does not establish the behavior of the not-yet-present round-24 population or the maintained round-24 replay. All mutations and commits were confined to `/tmp/kake-r24-GapC2NotServedShape-clone`; the clone ended at the base revision. No lane production files were changed; this report is the only lane write.