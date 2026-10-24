# C2 gap audit: error / truncated flags

## Verdict

**P2 coverage finding on C2 / operability:** the historical round-23 detector accepted six malformed flag receipts. Of ten expected-reject cases, four were killed and six survived; both expected-accept controls held. No case was inconclusive and no run emitted a Python traceback. A survivor is a detector-coverage finding, not an admission decision or permission to relax the claim.

The single defect family probed is implicit defaulting/truthiness of receipt flags instead of explicit presence and JSON type/value checks. Each non-control changed or removed exactly one member of one committed `fetch.json`; neither `audit.json` nor `page.html` was changed. The existing served `ds4cc-primary` and not-served `charter-kimi` receipts exercise both branches without constructing a substitute receipt.

- Owned axis exercised: **operability**. The frozen freshness axis was not measured by this probe.
- Pristine detector: exit **0**, accepted **12/12**.
- Mutants: **4 killed / 6 survived**; controls: **2 held**.
- Restored detector after every case: exit **0**, accepted **12/12**, exact original receipt hashes and original full Git tree.
- Author-side evidence only; no production fix, integration, shipment, or independent admission is claimed.

## Findings

### P2 — missing / mistyped flags can remain accepted, particularly on the not-served branch

Impacted claim/axis: round-24 **C2 / operability**, structural/semantic receipt rejection.

Observed survivors:

- Served HTML: deleting `error`, setting `truncated` to numeric `0`, or deleting `truncated` each retained exit 0 and 12/12 accepted; `ds4cc-primary` remained `clean` with an empty problems list.
- Existing HTTP 404 not-served receipt: `error: 0`, `error: ""`, or `truncated: "false"` each retained exit 0 and 12/12 accepted; `charter-kimi` remained `not-served` with an empty problems list.

The historical implementation is the cause: `served()` uses `fetch.get("error") is None` but the global usable-response check uses truthiness of `fetch.get("error")`; `truncated` is only checked for truthiness inside `served()`. An omitted key therefore defaults to a success-like value, numeric zero aliases false, and a 404 status short-circuits served classification before truncated's type matters.

Smallest fix for the maintained replay implementation: before either classification branch, require the `error` member to be present and exactly JSON null for a usable HTTP response, and require the `truncated` member to be present and a JSON boolean (in Python, an exact bool type check, not numeric equality/truthiness). For served HTML, require that boolean to be false. Reject violations with exit 1 or 2 and a diagnostic rather than a traceback. Keep the round-23 runners byte-intact. No fix was applied here.

### Expectation basis and standards boundary

The expectations do not come from Python truthiness and do not assert that these inputs are invalid JSON syntax:

- Frozen source `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py:7-15` documents usable committed GET receipts and matching served/not-served storage; lines 36-39 explicitly require null error for served HTML, and lines 58-59 reject fetch errors.
- At the frozen revision, `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/live_snapshot.py:77-99` emits `error` as null or a nonempty diagnostic string and always emits `truncated` as the boolean comparison `len(body) > MAX_BODY`.
- `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/knowledge/static-canonical-preflight.md:125-136,155` says the counter reproduces captures and that missing or altered capture data is input error, not not-served.
- [RFC 8259 §3](https://www.rfc-editor.org/rfc/rfc8259.html#section-3) distinguishes null, booleans, strings and numbers; [§4](https://www.rfc-editor.org/rfc/rfc8259.html#section-4) defines object members; [§6](https://www.rfc-editor.org/rfc/rfc8259.html#section-6) and [§7](https://www.rfc-editor.org/rfc/rfc8259.html#section-7) distinguish numeric flags and the empty/string-false values from their null/boolean counterparts. The RFC itself does **not** prescribe these application member names or require their presence. **[INFERENCE]** The required-member/type expectations follow from the lane's producer representation plus its missing/altered-capture rule; this is not a new RFC-imposed receipt schema.
- [RFC 3339 §5.6](https://www.rfc-editor.org/rfc/rfc3339.html#section-5.6) and [RFC 9110 §8.3.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.3.1) were read. They constrain the unchanged timestamp and media-type fields, not the error/truncated JSON types; neither supplies a reason to coerce flag values. This probe makes no timestamp/media-type coverage claim.

### Executed C2 malformed-case array

Only actually committed and replayed cases appear below. The null and boolean-false controls already equalled the original values; they used intentional empty commits and remained byte-identical. `stdoutTail` really is just `}` because the runner pretty-prints JSON. For deletion cases `value` is omitted, as it is unused by `op: delete`.

```json
[
  {
    "id": "error-null-control",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "error"
    ],
    "expect": "accept",
    "why": "The committed usable HTTP response records error:null, the no-error value required by served() and emitted by live_snapshot.py; RFC 8259 section 3 defines null distinctly from strings and numbers.",
    "value": null,
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "error-empty-string",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "error"
    ],
    "expect": "reject",
    "why": "served() requires error to be JSON null for the stored 2xx HTML body, and the empty string is a distinct JSON string rather than null under RFC 8259 sections 3 and 7.",
    "value": "",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "error-zero",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "error"
    ],
    "expect": "reject",
    "why": "The stored successful HTML response requires error:null rather than a numeric flag; RFC 8259 sections 3 and 6 make the number 0 distinct from null and an error string.",
    "value": 0,
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "error-key-missing",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "delete",
    "jsonPath": [
      "error"
    ],
    "expect": "reject",
    "why": "The snapshot producer always emits the error member and the handoff says missing capture data is input error; RFC 8259 section 4 does not equate an omitted object member with an explicit null value.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "truncated-false-control",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "truncated"
    ],
    "expect": "accept",
    "why": "The committed full HTML snapshot records the JSON boolean false produced by len(body)>MAX_BODY, with matching body digest and audit; RFC 8259 section 3 defines false as a boolean literal.",
    "value": false,
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "truncated-string-false",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "truncated"
    ],
    "expect": "reject",
    "why": "truncated is the producer boolean cap flag and a stored full HTML body requires false, not the truthy JSON string \"false\"; RFC 8259 sections 3 and 7 distinguish these types.",
    "value": "false",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "truncated-zero",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "truncated"
    ],
    "expect": "reject",
    "why": "The producer emits a boolean truncated flag, so numeric 0 is malformed even though Python treats it like false; RFC 8259 sections 3 and 6 distinguish boolean false from a number.",
    "value": 0,
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "truncated-one",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "set",
    "jsonPath": [
      "truncated"
    ],
    "expect": "reject",
    "why": "Numeric 1 is not the producer boolean truncated flag under RFC 8259 sections 3 and 6, and treating it as true is inconsistent with the stored full HTML page and served audit.",
    "value": 1,
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "truncated-key-missing",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/fetch.json",
    "op": "delete",
    "jsonPath": [
      "truncated"
    ],
    "expect": "reject",
    "why": "The snapshot producer always records whether its body cap truncated the response and the handoff calls missing capture data input error; RFC 8259 section 4 does not supply an omitted member with boolean false.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "error-zero-not-served",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": [
      "error"
    ],
    "expect": "reject",
    "why": "The producer records null for this usable 404 HTTP response or a diagnostic string for a fetch error, never a number; RFC 8259 sections 3 and 6 distinguish numeric 0 from either permitted representation.",
    "value": 0,
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "truncated-string-not-served",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": [
      "truncated"
    ],
    "expect": "reject",
    "why": "The producer emits a JSON boolean cap flag for every response including 404, and RFC 8259 sections 3 and 7 distinguish the string \"false\" from that boolean even when no page is stored.",
    "value": "false",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "error-empty-not-served",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/charter-kimi/fetch.json",
    "op": "set",
    "jsonPath": [
      "error"
    ],
    "expect": "reject",
    "why": "This completed 404 response uses error:null and producer errors are nonempty diagnostics, so the empty string must not alias null in replay; RFC 8259 sections 3 and 7 keep strings distinct from null.",
    "value": "",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  }
]
```

### Exact commands and observed output

All commands below used the same historical runner and a 120-second outer subprocess bound. Its canonical-audit children retain the historical 60-second bound. Environment was `GIT_AUTHOR_DATE=2026-10-21T12:00:00Z`, `GIT_COMMITTER_DATE=2026-10-21T12:00:00Z`, `PYTHONDONTWRITEBYTECODE=1`, and `TMPDIR=/tmp/kake-r24-GapC2ErrorTruncated-U4Kw`. The fixed dates affect commits, not receipt observation fields.

For every run below, stderr was exactly the empty string and stdout's final line was exactly `}`. Full, unabridged stdout/stderr and subprocess commands are retained in the hash-listed evidence files. The quoted blocks below are exact contiguous target-row excerpts of that stdout; acceptance counts are decoded from that same captured output.

#### error-null-control

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision ed58dfda01daf2f46d7a5b26be2ece6df792a77f`

Expected **accept**; observed exit **0**, accepted **12/12**, traceback **false**; verdict **control-held**.

```text
  {
   "id": "ds4cc-primary",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
```

#### error-empty-string

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision bf9c75a50d2de0838bdf4c52a5a32d684adb2f69`

Expected **reject**; observed exit **1**, accepted **11/12**, traceback **false**; verdict **killed**.

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

#### error-zero

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision de4653292bf9f5a9c6552f7d4a02ff82a1e04e0c`

Expected **reject**; observed exit **1**, accepted **11/12**, traceback **false**; verdict **killed**.

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

#### error-key-missing

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision 6aa048bca8b1508fafd10ab8301026f550eeb77b`

Expected **reject**; observed exit **0**, accepted **12/12**, traceback **false**; verdict **survived**.

```text
  {
   "id": "ds4cc-primary",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
```

#### truncated-false-control

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision b38e63b4a344e294660832a040d9483c4c860e1d`

Expected **accept**; observed exit **0**, accepted **12/12**, traceback **false**; verdict **control-held**.

```text
  {
   "id": "ds4cc-primary",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
```

#### truncated-string-false

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision 9be6ed00b32ed732eea460bee817cbd383ef5689`

Expected **reject**; observed exit **1**, accepted **11/12**, traceback **false**; verdict **killed**.

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

#### truncated-zero

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision 25bf5b3da41b7fd4ac6f1292f68a16e64b81c876`

Expected **reject**; observed exit **0**, accepted **12/12**, traceback **false**; verdict **survived**.

```text
  {
   "id": "ds4cc-primary",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
```

#### truncated-one

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision b305132188053e04b52a05f1f49fe22411e58fbc`

Expected **reject**; observed exit **1**, accepted **11/12**, traceback **false**; verdict **killed**.

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

#### truncated-key-missing

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision d901c1c38ab7c273641e32036a3021bef67f4116`

Expected **reject**; observed exit **0**, accepted **12/12**, traceback **false**; verdict **survived**.

```text
  {
   "id": "ds4cc-primary",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
```

#### error-zero-not-served

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision afab9af79ee62fff782a3c58ea6313e2a3de75e4`

Expected **reject**; observed exit **0**, accepted **12/12**, traceback **false**; verdict **survived**.

```text
  {
   "id": "charter-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  }
```

#### truncated-string-not-served

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision 4062155728f73248ebde53aea1d1d85e807be305`

Expected **reject**; observed exit **0**, accepted **12/12**, traceback **false**; verdict **survived**.

```text
  {
   "id": "charter-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  }
```

#### error-empty-not-served

Command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision d13c87175162f3c2f5daf877e9bc958b91203413`

Expected **reject**; observed exit **0**, accepted **12/12**, traceback **false**; verdict **survived**.

```text
  {
   "id": "charter-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  }
```

## Checked and held

### Clone, pristine detector and commit discipline

Clone command: `git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone`. Observed initial clone HEAD and explicit detached frozen HEAD were both `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. All probe/restoration commits descend from that revision; a restoration commit returns the entire tree to the frozen tree before the next case. No lane Git/index state was changed.

Pristine command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436`

Observed exit 0, stderr `""`, no traceback; exact opening stdout lines:

```text
{
 "accepted": 12,
 "revision": "f7de3ab4e9f030a15a857a5a08631bd8e690f436",
 "surfaces": [
```

Commit command pattern, with the actual arguments recorded per case in evidence: `git -C /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone -c 'user.name=KakeR24 GapC2ErrorTruncated' -c user.email=kake-r24-gap-c2-error-truncated@localhost -c commit.gpgsign=false -c core.hooksPath=/dev/null commit --quiet --allow-empty -m 'r24 flag probe <case-id> mutated'` (and `restored` for the paired exact-byte restoration). Each was preceded by `git add -- <absolute fetch.json path>` in this clone only.

Recorded date inspection: `git -C /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone log '--format=%H %cI %aI' f7de3ab4e9f030a15a857a5a08631bd8e690f436..HEAD`; all 24 rows reported both dates exactly `2026-10-21T12:00:00Z`. Exact stdout:

```text
2e91a03c7a5bb7a298a5a806fe90d266fd4b8e49 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
d13c87175162f3c2f5daf877e9bc958b91203413 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
87428b0bac2620a0cd0e3ad65787f5a3405e8de2 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
4062155728f73248ebde53aea1d1d85e807be305 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
c6150bd1ef9390fa5663cc222cea557e163558e1 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
afab9af79ee62fff782a3c58ea6313e2a3de75e4 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
f75667c5a7afe222010e6a4ab21738041528b6e5 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
d901c1c38ab7c273641e32036a3021bef67f4116 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
eaffd6faacc6b1d6ec02fe51bcc9c3ea0b8e460b 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
b305132188053e04b52a05f1f49fe22411e58fbc 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
ea95693e10962fcaae217b630b8a2ae303e0a94e 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
25bf5b3da41b7fd4ac6f1292f68a16e64b81c876 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
5de96da78ae6733b5ce0953f8744afcff45c7d47 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
9be6ed00b32ed732eea460bee817cbd383ef5689 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
8675d37ace269e154098abf627064ad9a795c548 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
b38e63b4a344e294660832a040d9483c4c860e1d 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
700c8a2869ff18712b3efcc37df2de9b5a756bcd 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
6aa048bca8b1508fafd10ab8301026f550eeb77b 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
b1421d41276c891034f50db189b39194099cb0f1 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
de4653292bf9f5a9c6552f7d4a02ff82a1e04e0c 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
3a6708be78543b333e98ea793d539df6e69cc92e 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
bf9c75a50d2de0838bdf4c52a5a32d684adb2f69 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
0e06b345f61ba06e0f4e15ee867531b95998ec9c 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
ed58dfda01daf2f46d7a5b26be2ece6df792a77f 2026-10-21T12:00:00Z 2026-10-21T12:00:00Z
```

### Exact restoration evidence

The receipt was restored through an unconditional `finally` path before the restored commit and detector run. Every committed mutant digest matched its corresponding worktree digest. The shared before/restored digests were:

- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone/.ufo/waves/round-23/live/ds4cc-primary/fetch.json`: `a860e0a3eba641411850f52c112ee127bc96cd050bfa7ac1024c911d7f1a9f3c`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone/.ufo/waves/round-23/live/charter-kimi/fetch.json`: `cbca8a945fb106ebbfbc72a01ed1a0c41b5b74276e51c0ec471cdb48af17cb71`

Every restored full Git tree was `ba4a40e4604c1f207f23deeb68c117409b76be70` (the frozen base tree), not merely an equivalent parsed JSON object.

| Case | Mutated receipt SHA-256 | Restored commit | Restored exit / accepted |
|---|---|---|---|
| error-null-control | `a860e0a3eba641411850f52c112ee127bc96cd050bfa7ac1024c911d7f1a9f3c` | `0e06b345f61ba06e0f4e15ee867531b95998ec9c` | 0 / 12/12 |
| error-empty-string | `2c652a4b0c9207df3119e6b7177af70143bfde3a3f1b56a7abd0492048f4020c` | `3a6708be78543b333e98ea793d539df6e69cc92e` | 0 / 12/12 |
| error-zero | `378a5f5b494f838feab34f56a48472a7aa802ff2b93f778f0e7e5518b07d8ad0` | `b1421d41276c891034f50db189b39194099cb0f1` | 0 / 12/12 |
| error-key-missing | `b4eeabd0bceb22938c71979ea846473cb13fc0000ea81593fb7e1f658ac785a9` | `700c8a2869ff18712b3efcc37df2de9b5a756bcd` | 0 / 12/12 |
| truncated-false-control | `a860e0a3eba641411850f52c112ee127bc96cd050bfa7ac1024c911d7f1a9f3c` | `8675d37ace269e154098abf627064ad9a795c548` | 0 / 12/12 |
| truncated-string-false | `c3f8456ed88839bb152478833e2d35916eb9140be6065ecaf2149e60d83cbe88` | `5de96da78ae6733b5ce0953f8744afcff45c7d47` | 0 / 12/12 |
| truncated-zero | `3efd5911b041cac806611f29fa0c3b20cb9810e4b2e4a66b7b270d2ea7a7fa6a` | `ea95693e10962fcaae217b630b8a2ae303e0a94e` | 0 / 12/12 |
| truncated-one | `268521c7103c5686bac9616ea9cc8b843656092c0703fe1ad6ab8146d27bf869` | `eaffd6faacc6b1d6ec02fe51bcc9c3ea0b8e460b` | 0 / 12/12 |
| truncated-key-missing | `61ab18aa6489dfa19f625ff46fd3b96aabba3293ca537a4244feef57c34aa503` | `f75667c5a7afe222010e6a4ab21738041528b6e5` | 0 / 12/12 |
| error-zero-not-served | `2495db70fba96e92dfc2b2bb4b75e51d09b65bab2e0684f8b9853c3b117f1a9b` | `c6150bd1ef9390fa5663cc222cea557e163558e1` | 0 / 12/12 |
| truncated-string-not-served | `4217d1dd459b610bed9511e9049408b0b9806d3c9695e58502985fca2411f221` | `87428b0bac2620a0cd0e3ad65787f5a3405e8de2` | 0 / 12/12 |
| error-empty-not-served | `11b906ac10fbd77f6e58dea57464c9f4cb8ff9306ff730e33528ff825470fd72` | `2e91a03c7a5bb7a298a5a806fe90d266fd4b8e49` | 0 / 12/12 |

Final restored command: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone --revision 2e91a03c7a5bb7a298a5a806fe90d266fd4b8e49`. Observed exit 0, stderr `""`, no traceback; exact opening stdout lines:

```text
{
 "accepted": 12,
 "revision": "2e91a03c7a5bb7a298a5a806fe90d266fd4b8e49",
 "surfaces": [
```

The four killed cases (`error-empty-string`, `error-zero`, `truncated-string-false`, `truncated-one`) each failed the served receipt with these exact messages, rather than a type-specific flag diagnostic:

```text
    "page.html stored for a non-served response",
    "non-served surface lacks a matching not-served receipt"
```

This is branch-consistency coverage, not evidence that flag schema validation already exists. Both unmodified controls and all twelve exact-byte restorations remained accepted.

### Protected bytes

Before/after SHA-256 values were equal for all of these paths (captured with `sha256sum <absolute path>`):

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py`: `91134d27af6c48f8e8bd6e604e533396f6d9c3542d1285ec1e3901f6358e5653`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone/.ufo/waves/round-23/measure_c2.py`: `91134d27af6c48f8e8bd6e604e533396f6d9c3542d1285ec1e3901f6358e5653`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone/scripts/live_snapshot.py`: `3638891d4107a57b5d3c919da41a33f3a0c97d15db257d1e9070e00f3b462a20`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone/scripts/canonical_audit.py`: `23638a87dba90f151bc65ed220983ab948989a5dfadf64f62469ceeabe45d0a4`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone/.ufo/waves/round-23/live/ds4cc-primary/audit.json`: `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone/.ufo/waves/round-23/live/ds4cc-primary/page.html`: `ccb3f46eda1ce3270df1e3373d49c4034025c4f475a6999142279e03b00b2bb8`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/clone/.ufo/waves/round-23/live/charter-kimi/audit.json`: `26f5b2a199bcb26624bf04804264903ff40a063184f19c84e9578d840de707cb`

### Retained evidence artifacts

The JSON files contain actual outputs, commit IDs, hashes, restoration results and exact invoked subprocess commands; no raw output was reconstructed from predictions. All scratch artifacts remain under the isolated workspace. `evidence.json` combines the entire probe; `cases.json` contains exactly the report array.

- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/baseline.json` — SHA-256 `37e35d65398301793623e497e2c6acece9d2815804417dc3af3713d3b36d766d`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/error-null-control.json` — SHA-256 `8d127be982f0849a421202cc3d786980f7f9c2c77e0ee354e035fba2d49bb909`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/error-empty-string.json` — SHA-256 `f97f86ea3f9d72dd1092fcb330dd97304ab7217f69431d4627ba5627e5dd8a30`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/error-zero.json` — SHA-256 `8a1f343ca377588773d5293a6977d4a6563b037225986821fbf955fbbc4dd1c3`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/error-key-missing.json` — SHA-256 `0ae03ee8133b2ebcee3c2d6fd4d87958cc7b1330e47a6ee055bfe809dbc55324`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/truncated-false-control.json` — SHA-256 `b85998e949b5f67196e7363feb10935a97bb45e22b55e9c078626370a7ce992d`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/truncated-string-false.json` — SHA-256 `35b86838c42a3447cd1aa42a4e2b6a65f619758259269381416000cf31fc87a7`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/truncated-zero.json` — SHA-256 `91d889de2d141b5fcf06c5b63c7854a06d6572b559e0c826d4f6cf09ee70254f`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/truncated-one.json` — SHA-256 `8fa1838ef7324c0461a98400a32b80e32111c1c3036c5477d4e5a380857df42b`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/truncated-key-missing.json` — SHA-256 `c212cf76412ad4f90a4ea116e444d521549e5783b47636bd4c1a1410d27296bb`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/error-zero-not-served.json` — SHA-256 `d041db09750b81fb49de9d568da42c5659449c7077458ada83c600b1ae72b52e`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/truncated-string-not-served.json` — SHA-256 `0ab56260b0ca74ee732e7a041fc94a81f97d9040aa3534aeb9234bae108d427f`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/error-empty-not-served.json` — SHA-256 `26abcef4727f07e60fd9ed0dd2960797f8224cff9acc247a998625314c209532`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/evidence.json` — SHA-256 `b7a5e7d5745a644b7fcea02219e77186eb71d073eeb81944d8826731ffc14479`
- `/tmp/kake-r24-GapC2ErrorTruncated-U4Kw/cases.json` — SHA-256 `bcd7b9c0db61df437cee9b81a839bef0bc2be6031a3fcc86373ad59d951f2514`

## Limits

- Only the twelve cases listed were exercised; there were 25 bounded detector invocations: one pristine baseline, twelve committed cases, twelve restored commits. No unrun value/branch combination is claimed covered.
- No new `page.html`/`audit.json` rewrite was needed: the existing 404 receipt exposes the not-served branch independently. No relabelled 2xx-not-served fixture, duplicate-key JSON, timestamp mutation, media-type mutation, or non-string top-level receipt was tested here.
- These are valid JSON texts with lane-schema/semantic defects; RFC 8259 alone does not make an empty string, numeric zero, or an omitted member syntactically invalid. Required-key and explicit-null expectations are grounded in the producer and handoff above.
- No live property was fetched or authenticated. The only external reads were public RFC documentation. No domain source tree was modified.
- The maintained `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/receipt_replay.py` was not edited or exercised. No production source, historical runner, audit/body, fleet state, or sibling file was edited. The only lane write is this assigned report.
- No builds, lint, formatters, broad suite, or other runtime were invoked; only Python's named replay detector and its historical canonical-audit children, Git and SHA-256 evidence commands were used. No subagents were spawned.
- Tool installations/updates: **none**. No pacman transaction, service restart, or host configuration change was performed.
