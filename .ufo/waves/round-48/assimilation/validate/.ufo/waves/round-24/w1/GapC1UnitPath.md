## Verdict

No actionable unit/path identity defect found in the six tested C1 receipt mutations. The frozen round-23 runner enforces exact population identity: all six altered receipts were rejected with exit 1, without a Python traceback; each run accepted the other 16 of 17 units. The unmodified base passed 17/17. This is author-side probe evidence, not independent admission.

## Findings

None (P0–P3). The tested identity violations were already rejected by the round-23 runner; no fix is indicated for this scope.

## Checked and held

Sandbox: `/tmp/kake-r24-GapC1UnitPath-clone`, cloned with `git clone --no-hardlinks` from the lane. Its observed initial HEAD was `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. Each test started from that base in its own worktree, changed only `.ufo/waves/round-23/receipts/drift-detection.json`, was committed with `GIT_AUTHOR_DATE=GIT_COMMITTER_DATE=2026-10-21T12:00:00Z`, and was measured with the round-23 `measure_c1.py` runner. Every measurement command was `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1UnitPath-clone --revision <revision>`.

| Case | Revision | Exact observed result excerpt |
|---|---|---|
| wrong-unit | `b9ce15dd13db7a8112f344974f279fe8eedb44dc` | exit 1; traceback false; stdout contained `"accepted": 16,`, `"total": 17,`, `"pass": false,`, `"problems": ["unit/path mismatch"]`; stdout tail `}`; stderr empty. |
| path-dotdot | `9fd5acce350eb5befdff5738ba6d3af9c54da071` | exit 1; traceback false; stdout contained `"accepted": 16,`, `"total": 17,`, `"pass": false,`, `"problems": ["unit/path mismatch"]`; stdout tail `}`; stderr empty. |
| path-list | `11ced7bd9d8a73120d50652f89ffb0ecffaa4b31` | exit 1; traceback false; stdout contained `"accepted": 16,`, `"total": 17,`, `"pass": false,`, `"problems": ["unit/path mismatch"]`; stdout tail `}`; stderr empty. |
| unit-missing | `ba7eaf6a4c297ee41abf05f04c95dfe5f702171c` | exit 1; traceback false; stdout contained `"accepted": 16,`, `"total": 17,`, `"pass": false,`, `"problems": ["unit/path mismatch"]`; stdout tail `}`; stderr empty. |
| unit-trailing-space | `a294a4e4231e5ca897ee879df2537c191bc652df` | exit 1; traceback false; stdout contained `"accepted": 16,`, `"total": 17,`, `"pass": false,`, `"problems": ["unit/path mismatch"]`; stdout tail `}`; stderr empty. |
| path-trailing-space | `470101a49d25f587fecb0b46bfa16c3f554e0aba` | exit 1; traceback false; stdout contained `"accepted": 16,`, `"total": 17,`, `"pass": false,`, `"problems": ["unit/path mismatch"]`; stdout tail `}`; stderr empty. |

The runner docstring says each receipt's `unit` and `path` must match the population; implementation compares those fields directly and emits `unit/path mismatch` when they do not. The `../` spelling was `corpus/knowledge/../knowledge/drift-detection.md`; it is not equal to the population's exact path. RFC 8259 §5/§7 makes JSON arrays and strings valid JSON values, but does not make the array or altered string satisfy the runner's field-identity contract. The trailing spaces were inside the unit/path string values, not insignificant JSON whitespace.

Baseline command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1UnitPath-clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436`. Exact result excerpts: `"accepted": 17,`, `"total": 17,`, and the drift-detection row had `"pass": true,` and `"problems": []`.

RFC 3339 §5.6 and RFC 9110 §8.3.1 do not determine these unit/path identity cases; they concern timestamp and media-type syntax, respectively. RFC 8259 was used only for the JSON-type/string distinctions above.

Cases applied to the committed receipts and measured at the listed revisions:

```json
[
  {
    "id": "wrong-unit",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": ["unit"],
    "value": "fleet-registry",
    "expect": "reject",
    "why": "The documented C1 receipt contract requires unit to equal the population unit, so this mismatch must reject.",
    "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "path-dotdot",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": ["path"],
    "value": "corpus/knowledge/../knowledge/drift-detection.md",
    "expect": "reject",
    "why": "The documented C1 receipt contract requires the exact population path; RFC 8259 §7 treats this as a valid string but does not normalize its value.",
    "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "path-list",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": ["path"],
    "value": ["corpus/knowledge/drift-detection.md"],
    "expect": "reject",
    "why": "RFC 8259 §5 permits arrays as JSON values, but the documented C1 receipt contract requires path to match the population's string value.",
    "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "unit-missing",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "delete",
    "jsonPath": ["unit"],
    "expect": "reject",
    "why": "The documented C1 receipt contract requires the receipt unit to match the population unit, and an omitted member cannot match.",
    "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "unit-trailing-space",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": ["unit"],
    "value": "drift-detection ",
    "expect": "reject",
    "why": "The unit string's trailing space is valid JSON under RFC 8259 §7 but differs from the exact population identity required by the runner.",
    "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}
  },
  {
    "id": "path-trailing-space",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": ["path"],
    "value": "corpus/knowledge/drift-detection.md ",
    "expect": "reject",
    "why": "The path string's trailing space is valid JSON under RFC 8259 §7 but differs from the exact population identity required by the runner.",
    "r23Observed": {"exit": 1, "traceback": false, "stdoutTail": "}"}
  }
]
```

## Limits

This audit covers only the listed C1 identity mutations in round-23 `measure_c1.py`, not the separate C1 timestamp/claims checks, C2 `measure_c2.py` behavior, or maintained round-24 `scripts/receipt_replay.py`. No tools were installed or updated.