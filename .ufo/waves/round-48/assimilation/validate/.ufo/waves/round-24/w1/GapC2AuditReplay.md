# C2 audit receipt mutation probe — GapC2AuditReplay

## Verdict

**Coverage gap found (P2, C2 / operability).** Eleven committed cases were exercised: nine malformed audit receipts and two byte-identical acceptance controls. Seven malformed mutants were killed; two survived: `exit: false` substituted for numeric `0`, and `result.pagesChecked: true` substituted for numeric `1`. Both survivors incorrectly returned exit 0 with 12/12 accepted. No case emitted a traceback. No baseline failure occurred.

For each case the same bounded round-23 detector ran on pristine, committed case, and committed restored bytes: **33 detector executions**. Every pristine and restored run exited 0 with 12/12 accepted; all eight watched-file hashes matched the base after every restoration. This is author-side mutation evidence, not an admission or integration decision.

## Findings

### P2 — Python equality accepts boolean substitutions in numeric audit fields

Impacted claim/axis: frozen C2, operability. Expected detector: reject a receipt that does not exactly reproduce the validator process exit and result with exit 1 or 2, and no traceback. `measure_c2.py` documents exact replay at lines 9–12 and compares the parsed receipt with the reproduced object at line 103. Python equality does not distinguish `False` from `0` or `True` from `1`; these cases therefore survive despite changing JSON value types.

Smallest fix: in the maintained `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/receipt_replay.py`, validate numeric audit fields with exact non-boolean types before comparing results: `type(exit) is int` and `type(result.pagesChecked) is int`, then preserve exact receipt/result key and value comparison. Return a normal receipt-validation rejection for a type mismatch. Do not alter either historical round-23 runner, and do not relax the contract to accept booleans. Add both observed cases to the C2 frozen population. This report does not implement or test that fix.

#### `audit-exit-boolean` — survived

Exact command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision ddfc96c5699b59823d9e33d987542e4c886db1c3
```

Actual exit: `0`; stderr: `''` (empty); traceback: `false`. Exact complete stdout:

```text
{
 "accepted": 12,
 "revision": "ddfc96c5699b59823d9e33d987542e4c886db1c3",
 "surfaces": [
  {
   "id": "ds4cc-primary",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
  {
   "id": "plazir15-ghp",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
  {
   "id": "charter-ghp",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
  {
   "id": "ds4cc-kimi",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "burnerchrome-kimi",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "vault-index-kimi",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "plazir27-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  },
  {
   "id": "ufo-fsd-kimi-pro",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "lucario-ghp",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "lucario-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  },
  {
   "id": "plazir15-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  },
  {
   "id": "charter-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  }
 ],
 "total": 12,
 "validatorSha256": "23638a87dba90f151bc65ed220983ab948989a5dfadf64f62469ceeabe45d0a4"
}
```

#### `audit-pagecount-boolean` — survived

Exact command:

```text
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 02b211e4c179189b072b8ffc3c9028b34c4a89b0
```

Actual exit: `0`; stderr: `''` (empty); traceback: `false`. Exact complete stdout:

```text
{
 "accepted": 12,
 "revision": "02b211e4c179189b072b8ffc3c9028b34c4a89b0",
 "surfaces": [
  {
   "id": "ds4cc-primary",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
  {
   "id": "plazir15-ghp",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
  {
   "id": "charter-ghp",
   "pass": true,
   "problems": [],
   "verdict": "clean"
  },
  {
   "id": "ds4cc-kimi",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "burnerchrome-kimi",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "vault-index-kimi",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "plazir27-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  },
  {
   "id": "ufo-fsd-kimi-pro",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "lucario-ghp",
   "pass": true,
   "problems": [],
   "verdict": "failed-policy"
  },
  {
   "id": "lucario-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  },
  {
   "id": "plazir15-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  },
  {
   "id": "charter-kimi",
   "pass": true,
   "problems": [],
   "verdict": "not-served"
  }
 ],
 "total": 12,
 "validatorSha256": "23638a87dba90f151bc65ed220983ab948989a5dfadf64f62469ceeabe45d0a4"
}
```

### Contract and RFC basis

- Local exact-replay rule: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py:2-15`, with the equality checks at lines 75–77 and 100–105. Served receipts must match both process exit and result; non-served receipts must match `{verdict: "not-served", status: fetch.status, exit: null, error: null}`.
- Validator output contract: `/tmp/kake-r24-GapC2AuditReplay-clone/scripts/canonical_audit.py:113-115,752-770` documents the result keys and numeric process exits and produces numeric page counts.
- [RFC 8259 §3](https://www.rfc-editor.org/rfc/rfc8259.html#section-3), [§6](https://www.rfc-editor.org/rfc/rfc8259.html#section-6), and [§7](https://www.rfc-editor.org/rfc/rfc8259.html#section-7) distinguish boolean, numeric, and string JSON values. The boolean and string mutants are syntactically valid JSON, but invalid under exact replay. [§4](https://www.rfc-editor.org/rfc/rfc8259.html#section-4) allows extra object members in JSON generally; their rejection here follows the documented local receipt contract, not a claim that JSON forbids them.
- [RFC 3339 §5.6](https://www.rfc-editor.org/rfc/rfc3339.html#section-5.6) and [RFC 9110 §8.3.1](https://www.rfc-editor.org/rfc/rfc9110.html#section-8.3.1) were read. This scoped probe leaves `fetchedAt` and `contentType` intact: `2026-10-21T06:33:03Z` / `2026-10-21T06:33:17Z`, and `text/html; charset=utf-8`. Their grammars do not authorize audit fields with different types or a 503 audit status paired with a 404 fetch. No timestamp/media-type mutation was added under this audit-only assignment.

### Executed C2 case population

Exactly the following eleven cases ran. `stdoutTail` is literally `}` because the runner pretty-prints its JSON; it is not substituted with a semantic summary. Controls are identity `set` operations and were committed with `--allow-empty` while retaining exact baseline receipt bytes.

```json
[
  {
    "id": "audit-verdict-mismatch",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/audit.json",
    "op": "set",
    "jsonPath": [
      "result",
      "verdict"
    ],
    "value": "failed-policy",
    "expect": "reject",
    "why": "The served receipt must reproduce canonical_audit.py result exactly (round-23 measure_c2.py lines 9-12); the unmodified page reproduces clean, not failed-policy.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "audit-exit-string",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/audit.json",
    "op": "set",
    "jsonPath": [
      "exit"
    ],
    "value": "0",
    "expect": "reject",
    "why": "The served receipt must reproduce the numeric process exit exactly; RFC 8259 sections 3, 6 and 7 distinguish a string from a number.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "audit-extra-top-key",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/audit.json",
    "op": "set",
    "jsonPath": [
      "unexpected"
    ],
    "value": true,
    "expect": "reject",
    "why": "An extra top-level member violates the documented exact served-receipt replay, although it remains valid JSON under RFC 8259 section 4.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "audit-extra-result-key",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/audit.json",
    "op": "set",
    "jsonPath": [
      "result",
      "unexpected"
    ],
    "value": true,
    "expect": "reject",
    "why": "An extra result member violates exact reproduction of the validator result; RFC 8259 section 4 permits arbitrary object members but does not override the local receipt contract.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "audit-result-missing",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/audit.json",
    "op": "delete",
    "jsonPath": [
      "result"
    ],
    "expect": "reject",
    "why": "The served receipt must contain both the reproduced exit and result (round-23 measure_c2.py lines 9-12), so an absent result is not a matching receipt.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "notserved-audit-status-mismatch",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/lucario-kimi/audit.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": 503,
    "expect": "reject",
    "why": "The not-served receipt must carry fetch.status exactly (round-23 measure_c2.py lines 13-14), which remains 404 rather than 503.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "audit-exit-boolean",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/audit.json",
    "op": "set",
    "jsonPath": [
      "exit"
    ],
    "value": false,
    "expect": "reject",
    "why": "A boolean false is not the reproduced numeric exit 0 under the exact replay contract and the distinct JSON value types in RFC 8259 section 3.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "audit-pagecount-boolean",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/audit.json",
    "op": "set",
    "jsonPath": [
      "result",
      "pagesChecked"
    ],
    "value": true,
    "expect": "reject",
    "why": "A boolean true is not the reproduced numeric pagesChecked value 1 under exact result replay and the distinct JSON value types in RFC 8259 section 3.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "notserved-audit-verdict-mismatch",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/lucario-kimi/audit.json",
    "op": "set",
    "jsonPath": [
      "verdict"
    ],
    "value": "clean",
    "expect": "reject",
    "why": "A 404 response without page.html requires the documented not-served audit verdict, not a clean canonical-policy result (round-23 measure_c2.py lines 13-14).",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "audit-served-unchanged-control",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/ds4cc-primary/audit.json",
    "op": "set",
    "jsonPath": [
      "exit"
    ],
    "value": 0,
    "expect": "accept",
    "why": "This identity set retains the committed served audit byte-for-byte, including its numeric exit and exactly reproduced result.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "audit-notserved-unchanged-control",
    "target": "c2",
    "file": ".ufo/waves/round-23/live/lucario-kimi/audit.json",
    "op": "set",
    "jsonPath": [
      "status"
    ],
    "value": 404,
    "expect": "accept",
    "why": "This identity set retains the committed not-served audit byte-for-byte, matching the numeric 404 fetch status with no page.html.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  }
]
```

## Checked and held

### Isolation, execution and bounds

- Axis under challenge: **operability**. Protected axis/bounds: historical evidence integrity; no source-tree, publishing, or fleet changes. Read `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/contract.json` first.
- Scratch creation command: `mktemp -d /tmp/kake-r24-GapC2AuditReplay-XXXX`; observed output: `/tmp/kake-r24-GapC2AuditReplay-y5BD`.
- Clone command: `git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-GapC2AuditReplay-clone`. Exact clone output: `Cloning into '/tmp/kake-r24-GapC2AuditReplay-clone'...` followed by `done.`. Observed clone HEAD and pinned checkout HEAD both: `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. Checkout command: `git -C /tmp/kake-r24-GapC2AuditReplay-clone checkout --detach f7de3ab4e9f030a15a857a5a08631bd8e690f436`.
- Each case branch starts directly at the frozen base using `git -C /tmp/kake-r24-GapC2AuditReplay-clone switch -c GapC2AuditReplay/<id> f7de3ab4e9f030a15a857a5a08631bd8e690f436`; only the named audit.json is changed. Every mutated commit is a direct child of the base, followed by its restoration commit. No fetch.json, page.html, manifest, validator, population, or runner edit was needed.
- Commit command form: `git -C /tmp/kake-r24-GapC2AuditReplay-clone add -- <case.file>` then `git -C /tmp/kake-r24-GapC2AuditReplay-clone commit --allow-empty -m "probe <id>: mutated receipt"` (and equivalently `restored receipt`). Both author and committer identities are `KakeR24.GapC2AuditReplay <gap-c2-audit-replay@local.invalid>`; `GIT_AUTHOR_DATE=2026-10-21T12:00:00Z` and **`GIT_COMMITTER_DATE=2026-10-21T12:00:00Z`**.
- Every runner subprocess used `python3`, `PYTHONDONTWRITEBYTECODE=1`, capture of stdout/stderr, and a 90-second outer timeout. The historical runner retains its own 60-second timeout per canonical validator subprocess. No timeout occurred.
- Tools observed: `git version 2.56.0`; `Python 3.14.8`. **No tool install/update**, package transaction, host service change, subagent dispatch, other runtime, build, lint, formatter, or network request to a property occurred. Web access was read-only RFC documentation.

### Actual case outcomes

Every row: pristine `exit=0, accepted=12/12`; restored `exit=0, accepted=12/12`. All 33 stderr streams were empty and all 33 traceback flags were false.

| Case | Expected | Actual exit | Accepted | Verdict |
|---|---|---:|---:|---|
| `audit-verdict-mismatch` | reject | 1 | 11/12 | killed |
| `audit-exit-string` | reject | 1 | 11/12 | killed |
| `audit-extra-top-key` | reject | 1 | 11/12 | killed |
| `audit-extra-result-key` | reject | 1 | 11/12 | killed |
| `audit-result-missing` | reject | 1 | 11/12 | killed |
| `notserved-audit-status-mismatch` | reject | 1 | 11/12 | killed |
| `audit-exit-boolean` | reject | 0 | 12/12 | survived |
| `audit-pagecount-boolean` | reject | 0 | 12/12 | survived |
| `notserved-audit-verdict-mismatch` | reject | 1 | 11/12 | killed |
| `audit-served-unchanged-control` | accept | 0 | 12/12 | control held |
| `audit-notserved-unchanged-control` | accept | 0 | 12/12 | control held |

Exact observed problem field values for each killed mutant (all seven returned exit 1):

- `audit-verdict-mismatch`: `audit.json {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'failed-policy'}} != reproduced {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}}`
- `audit-exit-string`: `audit.json {'exit': '0', 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}} != reproduced {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}}`
- `audit-extra-top-key`: `audit.json {'unexpected': True, 'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}} != reproduced {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}}`
- `audit-extra-result-key`: `audit.json {'exit': 0, 'result': {'unexpected': True, 'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}} != reproduced {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}}`
- `audit-result-missing`: `audit.json {'exit': 0} != reproduced {'exit': 0, 'result': {'findings': [], 'pagesChecked': 1, 'verdict': 'clean'}}`
- `notserved-audit-status-mismatch`: `non-served surface lacks a matching not-served receipt`
- `notserved-audit-verdict-mismatch`: `non-served surface lacks a matching not-served receipt`

### Exact commands and retained revisions

All pristine commands used the frozen base and the same absolute runner/root shown above. Complete exact commands, full stdout, empty stderr, exit, traceback flags and per-stage hashes are retained in the raw artifacts below. These are the exact mutated and restored commands, without revision placeholders:

- `audit-verdict-mismatch`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 0e44c2ab75f7c25b0aeea0e498268d079cf5c6d1`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 347e08dc143c1b9be78b6d655893338a87884f6a`
- `audit-exit-string`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision e2321b1ece74c8451e5c1005c69b1377033b8199`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision eaee7c5be88d0420993b60e2b663f679bd2d33b2`
- `audit-extra-top-key`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 89f8386eb8a8b63bff8f416e4586a1f34601ce00`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 4661f28339edf11ac06505b518adb401a8eaa338`
- `audit-extra-result-key`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 435bbf4e38726ecd20edd2626c887a2b3bcdf4c5`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 5cec44fb2fb832fe870e9b50879663fdb4fbfc20`
- `audit-result-missing`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 6a37e162f8950d6ffb2222684afd10b172c39a42`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 7b2940bab6b1d029ecc861e2626623f948732525`
- `notserved-audit-status-mismatch`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision e29b53253c85324de2156325c8ac311f963dec5d`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision b6b3f2233147458aad78487a55ef9ba2e6488cb6`
- `audit-exit-boolean`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision ddfc96c5699b59823d9e33d987542e4c886db1c3`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 74471e9889e40eb2947c9eca58b963197eff8b82`
- `audit-pagecount-boolean`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 02b211e4c179189b072b8ffc3c9028b34c4a89b0`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision b0c4394d78e609dce85d4e49ee0db4d578d6e533`
- `notserved-audit-verdict-mismatch`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 076c988f1fb2535bb5f5d962486b889327a11409`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 049ce3f0641fada5084e267bc456233ff8f629cf`
- `audit-served-unchanged-control`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 9ed730f88c412d40b05f24baf1436ec41293881d`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 9234240ba08bce1cba7d17264416face2bd572e3`
- `audit-notserved-unchanged-control`
  - mutated: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 948bcc6aaeb7bb7418dfc12867f95c6851e51aa0`
  - restored: `python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c2.py --root /tmp/kake-r24-GapC2AuditReplay-clone --revision 13a807550c9bf5f3f59f9ad803419659dc4e16b2`

### Before / mutant / restored SHA-256

Paths are the absolute audit paths in the clone. **S** = `/tmp/kake-r24-GapC2AuditReplay-clone/.ufo/waves/round-23/live/ds4cc-primary/audit.json`; **N** = `/tmp/kake-r24-GapC2AuditReplay-clone/.ufo/waves/round-23/live/lucario-kimi/audit.json`. S pristine/restored SHA-256 is `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75`; N pristine/restored SHA-256 is `26f5b2a199bcb26624bf04804264903ff40a063184f19c84e9578d840de707cb`. Neither baseline audit has a trailing newline; restoration writes the original exact bytes.

| Case | Path | Before SHA-256 | Case SHA-256 | Restored SHA-256 |
|---|---|---|---|---|
| `audit-verdict-mismatch` | S | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` | `bbc8ffe1ecad4f7d52d49813c9deaf5dcfb79b8439f1520cf3733d4f804bea76` | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` |
| `audit-exit-string` | S | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` | `ba3c98d89bc45fbc09b78e8e36a6e9ca2f257d29f70676bc717a983cedce214d` | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` |
| `audit-extra-top-key` | S | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` | `09124ca99ba2428135b3e0c148fc4adc0b5bb18209357b6adcbe901f23e98258` | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` |
| `audit-extra-result-key` | S | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` | `d4c39a11f42f195fb969f5c789370769469cda6da44163592cd1775d6ee356ad` | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` |
| `audit-result-missing` | S | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` | `482cba2cbfa7582bd0668d446d49197edc860a8b6e1814df6eefd69858dd5be2` | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` |
| `notserved-audit-status-mismatch` | N | `26f5b2a199bcb26624bf04804264903ff40a063184f19c84e9578d840de707cb` | `2f6c53fa34969ad434ceda7413502f23e84bdefc999943a11b08f62e8bbb0907` | `26f5b2a199bcb26624bf04804264903ff40a063184f19c84e9578d840de707cb` |
| `audit-exit-boolean` | S | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` | `82832f3610270a1d532c39b4cf643d00d5a0e3c923e8edff7754f82bb606d5b8` | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` |
| `audit-pagecount-boolean` | S | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` | `528f2396b2984702a4fca018d6f0ea9ebc00e2a22189aad27e8ef0774e14eed9` | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` |
| `notserved-audit-verdict-mismatch` | N | `26f5b2a199bcb26624bf04804264903ff40a063184f19c84e9578d840de707cb` | `f1bd196f21ec5b940d1dd3951273a76ddedc5c7013d363cc9a6873452191cfcd` | `26f5b2a199bcb26624bf04804264903ff40a063184f19c84e9578d840de707cb` |
| `audit-served-unchanged-control` | S | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` | `9265346ed4990b6b91b99adf97bf2ec94bde0abadc688ac46168644f73927c75` |
| `audit-notserved-unchanged-control` | N | `26f5b2a199bcb26624bf04804264903ff40a063184f19c84e9578d840de707cb` | `26f5b2a199bcb26624bf04804264903ff40a063184f19c84e9578d840de707cb` | `26f5b2a199bcb26624bf04804264903ff40a063184f19c84e9578d840de707cb` |

Additional unchanged watched artifacts (each matched this base SHA-256 in all 33 records):

- `/tmp/kake-r24-GapC2AuditReplay-clone/.ufo/waves/round-23/live/ds4cc-primary/fetch.json` — `a860e0a3eba641411850f52c112ee127bc96cd050bfa7ac1024c911d7f1a9f3c`
- `/tmp/kake-r24-GapC2AuditReplay-clone/.ufo/waves/round-23/live/ds4cc-primary/page.html` — `ccb3f46eda1ce3270df1e3373d49c4034025c4f475a6999142279e03b00b2bb8`
- `/tmp/kake-r24-GapC2AuditReplay-clone/.ufo/waves/round-23/live/lucario-kimi/fetch.json` — `47519fe7eb2102898529f8c940fbf5e2936ad9c4cd868ac795725faa6a671550`
- `/tmp/kake-r24-GapC2AuditReplay-clone/.ufo/waves/round-23/measure_c1.py` — `c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5`
- `/tmp/kake-r24-GapC2AuditReplay-clone/.ufo/waves/round-23/measure_c2.py` — `91134d27af6c48f8e8bd6e604e533396f6d9c3542d1285ec1e3901f6358e5653`
- `/tmp/kake-r24-GapC2AuditReplay-clone/scripts/canonical_audit.py` — `23638a87dba90f151bc65ed220983ab948989a5dfadf64f62469ceeabe45d0a4`

The final clone HEAD is the restored unchanged-control commit `13a807550c9bf5f3f59f9ad803419659dc4e16b2`. Every listed case branch retains its mutant and restoration commits. The final detector run accepted all 12/12 surfaces. The lane runners were never written; their initial SHA-256 values matched the cloned base values listed above.

### Raw output artifacts

Artifacts contain observations, not new production code. All paths below are absolute; SHA-256 hashes commit their exact bytes. Each individual log holds the full detector stdout/stderr as JSON strings rather than a truncated transcript.

- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-verdict-mismatch-pristine.json` — `b980dc9fad5a4eb99b4b1351ff03a5f87eaccb7f4f0ed14c3c0265e99ff95e95`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-verdict-mismatch-mutated.json` — `fed7295d5a3d0a4d40ab44d1b1e43a9cd90082df6035de901ad85f4b53f4955e`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-verdict-mismatch-restored.json` — `a563090252c5ad6ed9076474513ecea59a6c41d169461cc287e7d16044396507`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-exit-string-pristine.json` — `f4e17cffe5fe295afcbd7c3c33efd39f7f9b016784d3238f9df0867163fa617f`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-exit-string-mutated.json` — `1d844be83cb0a67c81782ab1200be27644aae8c6fc15112db4ec6ddbb40cd693`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-exit-string-restored.json` — `a8fcc773a60c3ad920af4ce7a0bc17d22406b0b425a9f14cd8f3e2b7d6f09788`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-extra-top-key-pristine.json` — `4101344dcdef0a67ec198d2f78226c0103715e55bc46e1ad8ca0bce633fff979`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-extra-top-key-mutated.json` — `85eb075d7f63d60954cdf0658ef2aba47d3f2d3f749650612022529a040fa53c`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-extra-top-key-restored.json` — `f46d857cb6e1c572e4a232f93a6819fb081a3149829d128a00cc39e2771d7bed`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-extra-result-key-pristine.json` — `2145151532385457964a9ce5fab1eabd3ad8028a9ff9bc431442c40659a2c38d`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-extra-result-key-mutated.json` — `170caac645c7d371937eac4af78047e02d85d151dc3a19ebff15c3fb7df28e96`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-extra-result-key-restored.json` — `cb2da8e99d53892e4d22f267d11cda231f3ef0a6b7cac8d9b1c868f0281eb154`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-result-missing-pristine.json` — `5ad017f4c7067d07edbd3e40e58f0055e0d053a00e77d773224cdd0912988ac8`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-result-missing-mutated.json` — `3eaa157a1d45acb2809c4e4f96dadfc91a307f3b3e41e850bb888bcd6c57c4cd`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-result-missing-restored.json` — `5cc00c2459fbeb19c6cf41a3b7bcef97f85eb626e90930370dff5c70202dd856`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/notserved-audit-status-mismatch-pristine.json` — `b5dc334aacbd5b65f5fd66404160c6b41d8ea3971a79aca40f17e24113fccaae`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/notserved-audit-status-mismatch-mutated.json` — `347039fb4317873a7d83bb63fc7a3f7d1693d288e1404f1b686fa7424d945a88`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/notserved-audit-status-mismatch-restored.json` — `92484aab60ddff5653dafb0737154032c29f83b287f72fbc34f3cda0c3b83bc9`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-exit-boolean-pristine.json` — `0247652d8e51317c698590b61a5431f49c498140b0dc617ae070eae8489164c3`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-exit-boolean-mutated.json` — `a43fc3b4d502205d3e0ed115543cb2a7e4ed506c5774ee78f9f9232697b31aad`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-exit-boolean-restored.json` — `f2d7bb4722812beb91e8ff74c55707e84c3fdbee365fc44ca4f65c35a923e87b`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-pagecount-boolean-pristine.json` — `24b6643ef907bf3ced02bde8b88435feb2770887283613f45269885125929cc9`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-pagecount-boolean-mutated.json` — `82dba49922e6ae14c4dac0bd17d13c26e62ed3f5838281b9dc343617a6c8546f`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-pagecount-boolean-restored.json` — `b5503fc7587a40ab9e849c0d5842a7237078e6418ca0fb9e6612e387ace2b5bd`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/notserved-audit-verdict-mismatch-pristine.json` — `0a57242eb3672ccbaaccfb82ab08e034ec803642f06c993e5d8a41de276bbd76`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/notserved-audit-verdict-mismatch-mutated.json` — `73a0f5bd23007a833c2316d4f421f78af2b7b152dd0cfd858900c96703b1e034`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/notserved-audit-verdict-mismatch-restored.json` — `fc04da1560c5e588abfaae320bd5522ebb05be7a840053aa19743073301ed4f9`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-served-unchanged-control-pristine.json` — `1553e62acc19b6ccf5f6983db6b04ed0623606585e1da60cf52d3389aa14d22d`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-served-unchanged-control-mutated.json` — `b3a74420b3d51bccd676768c2141a76fe7787534107d727b99e97f129bbb2336`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-served-unchanged-control-restored.json` — `f71edb979762d234059b3ea2e31b053c1c38104bbb943a91cb481a30ebc4d4c4`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-notserved-unchanged-control-pristine.json` — `207953f5c2eb766aa27371085a2eea9a07fabad20f0d57928f31c995d36a0e7c`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-notserved-unchanged-control-mutated.json` — `e0b4cf8ca8cea29c000886e641a692b1b37f7336aaa8daff956dfaa3566ad0d2`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/audit-notserved-unchanged-control-restored.json` — `720575eb071d8c746f3b879907df4c5616010aa4dff55cd636d73578eb50a131`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/cases.json` — `8c4cb991b87d13bce6b4df2618fccbe05c09e2af7cb321c0c4329e4596d28e55`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/probe-results.json` — `02170a6fe72ba0fefd98d384fc2b4e7b2ecda0c1c53ed82733eb6e269ac76050`
- `/tmp/kake-r24-GapC2AuditReplay-y5BD/artifacts.sha256` — `8b426fcdb5e095c12b2e56b9b2e4af2eee5518e1ca63beecc43199ab113c995a` (checksum listing of all 35 preceding artifacts).

## Limits

- This scoped probe tests committed audit receipt replay at the frozen round-23 base only. It does not authenticate the original HTTP observations, test current live services, exercise C1, or evaluate the round-24 maintained implementation.
- A surviving mutant is a detector coverage finding, not permission to change the exact-replay contract. The maintained-script fix and freezing/integration decisions remain with L1. No independent admission is claimed.
- Only this report was written in the lane. All commits, altered receipts, restored receipts and raw artifacts are in the isolated `/tmp` clone/scratch. No git/jj mutation was run in the lane or fleet repository.
- An internal tooling issue unrelated to the receipt detector was reported through `xd://report_issue`: `read` parsed the documented inline selector in `xd://eval/helpers:1-190` as an unknown topic; a subsequent unselected documentation read succeeded. This did not affect any probe result.
