## Verdict

**Six assigned malformed-receipt mutants killed; zero survived; zero inconclusive.** The pristine round-23 C1 detector accepted 17/17 units (exit 0). Each independently committed one-field mutation was rejected (exit 1, 16/17 units accepted), with empty stderr and no Python traceback. After every probe the receipt was restored byte-for-byte, committed, and the identical detector again accepted 17/17 (exit 0).

Owned axis challenged: **operability**, round-24 claim **C2**, using the historical C1 receipt replay. Freshness content was not changed. These are pre-existing rejection controls, not newly discovered acceptance/crash gaps. This author-side probe makes no independent admission or integration claim.

## Findings

**P3 — informational regression-retention finding, not a production defect.** The assigned verdict/correction/reason checks already hold at the frozen revision. Impacted claim/axis: C2 / operability. Smallest fix: none to the historical runner; preserve these exact rejection behaviors in the maintained replay and retain the exercised cases as negative controls. In particular, do not silently case-fold/trim verdict values, coerce an array into a verdict, or coerce an integer into correction text.

### Exact observed results

The diagnostics below quote the complete `problems` string from the sole failing unit in each stdout document. Every mutant returned exit 1, `accepted: 16`, `total: 17`, `stderr: ""`, and the exact last stdout line `}`. No other unit failed.

| Case / commit message | Receipt claim | Exact diagnostic | Verdict |
|---|---|---|---|
| `verdict-lowercase-hold` | `drift-detection:c1` | `claim c1: verdict 'hold'` | killed |
| `verdict-stale-trailing-space` | `drift-detection:c4` | `claim c4: verdict 'STALE '` | killed |
| `verdict-array-hold` | `drift-detection:c1` | `claim 0: missing field` | killed |
| `stale-missing-correction` | `drift-detection:c4` | `claim c4: STALE without correction` | killed |
| `unverifiable-empty-reason` | `fleet-registry:c2` | `claim c2: UNVERIFIABLE without reason` | killed |
| `stale-integer-correction` | `drift-detection:c4` | `claim c4: STALE without correction` | killed |

### Contract and RFC basis

- Application authority: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py:2-19` documents the exact verdict set, required STALE correction, required UNVERIFIABLE reason, and exit semantics. The corresponding checks are at lines 69-92: required fields must be nonempty strings; verdict membership is exact; STALE correction must be a nonempty string occurring verbatim in the section; an empty UNVERIFIABLE reason is rejected.
- [RFC 8259 §§2–3, 5–7](https://www.rfc-editor.org/rfc/rfc8259#section-3) distinguishes JSON strings, arrays, and numbers. All six fixtures remain syntactically valid JSON; rejection is receipt-schema/semantic rejection, not JSON syntax rejection. A space inside a string is not insignificant whitespace outside JSON tokens.
- [RFC 3339 §5.6](https://www.rfc-editor.org/rfc/rfc3339#section-5.6) governs timestamps, not verdict spelling or correction types. No timestamp was changed. The legacy `observedAt: "2026-10-21"` remained exactly as committed; this probe makes no claim that this full-date is an RFC 3339 date-time.
- [RFC 9110 §8.3.1](https://www.rfc-editor.org/rfc/rfc9110#section-8.3.1) makes media type/subtype tokens case-insensitive; that rule does not apply to this application verdict enumeration. No HTTP/media-type field was changed or tested here.

### Exercised C2 malformed-case array

Indices in `jsonPath` are zero-based. Each object below represents exactly one operation against the frozen committed receipt. STALE tests use an already-STALE claim; the empty-reason test uses an already-UNVERIFIABLE claim, so neither hides a second mutation.

```json
[
  {
    "id": "verdict-lowercase-hold",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": [
      "claims",
      0,
      "verdict"
    ],
    "value": "hold",
    "expect": "reject",
    "why": "The runner's documented verdict set is exactly HOLD/STALE/UNVERIFIABLE, so lowercase hold is outside the receipt contract.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "verdict-stale-trailing-space",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": [
      "claims",
      3,
      "verdict"
    ],
    "value": "STALE ",
    "expect": "reject",
    "why": "The runner's documented verdict set does not include STALE followed by a space; whitespace inside a JSON string is data, not the insignificant token whitespace of RFC 8259 section 2.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "verdict-array-hold",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": [
      "claims",
      0,
      "verdict"
    ],
    "value": [
      "HOLD"
    ],
    "expect": "reject",
    "why": "RFC 8259 sections 3 and 5 distinguish an array from a string, and the receipt contract requires verdict to be a nonempty string in HOLD/STALE/UNVERIFIABLE.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "stale-missing-correction",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "delete",
    "jsonPath": [
      "claims",
      3,
      "correction"
    ],
    "expect": "reject",
    "why": "The runner's documented contract requires every STALE claim to include correction text that appears verbatim in the unit's round-23 section.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "unverifiable-empty-reason",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fleet-registry.json",
    "op": "set",
    "jsonPath": [
      "claims",
      1,
      "reason"
    ],
    "value": "",
    "expect": "reject",
    "why": "The runner's documented contract requires a reason for UNVERIFIABLE, and an empty string supplies no reason.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "stale-integer-correction",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/drift-detection.json",
    "op": "set",
    "jsonPath": [
      "claims",
      3,
      "correction"
    ],
    "value": 42,
    "expect": "reject",
    "why": "RFC 8259 sections 3 and 6 distinguish a number from correction text, and the receipt contract requires a nonempty STALE correction that occurs verbatim in the round-23 section.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  }
]
```

### Exact detector commands

Each command was executed through Python `subprocess.run` with a 60-second timeout, captured stdout/stderr, and no timeout fired. The executable runner was always the lane's unchanged round-23 runner, not a copy of the new maintained implementation.

```text
# pristine; exit=0; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision f7de3ab4e9f030a15a857a5a08631bd8e690f436
# verdict-lowercase-hold; exit=1; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision fda08b590ea3be2d60369266526c6807fe02e350
# verdict-lowercase-hold-restored; exit=0; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision b92d481925bff480622c17fa4ba9baf374609029
# verdict-stale-trailing-space; exit=1; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision 06f831b20e863044c1a2b72857d2161ab9bf9bab
# verdict-stale-trailing-space-restored; exit=0; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision cf1447fa1a6e9a4cc6ff64e2dd0e421bbc7564c4
# verdict-array-hold; exit=1; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision 40faaed333bf98144ef3c39253e667db11315070
# verdict-array-hold-restored; exit=0; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision d49f3427fdf3c4950b87e058c44c1f950359cddf
# stale-missing-correction; exit=1; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision 431a353c12644651fb2be3863bb3a1a127efa941
# stale-missing-correction-restored; exit=0; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision e59132c454c775d02bb0cdf81faaadc9c5e23c61
# unverifiable-empty-reason; exit=1; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision 78bda9bcf3ea1d0268a7a07fce60a5b5cccc68e7
# unverifiable-empty-reason-restored; exit=0; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision 1d2216ce0bac7fdd9abb4c319833dac3c9c726d1
# stale-integer-correction; exit=1; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision 7084e37643d4694fa22b0fe7f3aaeaabe1fe8e04
# stale-integer-correction-restored; exit=0; traceback=false; stderr=""
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1VerdictSet-vbiL/clone --revision dea5d7b404a1390cfe753aace08df95649a2e0e9
```

## Checked and held

### Isolation and commit evidence

- Scratch root: `/tmp/kake-r24-GapC1VerdictSet-vbiL`.
- Clone: `/tmp/kake-r24-GapC1VerdictSet-vbiL/clone`; source: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
- Actual clone command: `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-GapC1VerdictSet-vbiL/clone`.
- Observed initial clone HEAD: `f7de3ab4e9f030a15a857a5a08631bd8e690f436`. The clone was explicitly detached at that revision before probing and returned to it after every restoration, including the final probe.
- Each mutant was made by one surgical receipt edit and committed in the clone. Its parent is the frozen base; each restoration was the inverse edit, committed separately, and replayed before detaching at the base for the next case.
- Every mutation and restoration commit used `GIT_COMMITTER_DATE=2026-10-21T12:00:00Z` and `GIT_AUTHOR_DATE=2026-10-21T12:00:00Z`. Signing and hooks were disabled only for those scratch-clone commit commands. No lane Git/jj/index state was changed.

| Case | Mutant commit | Restored commit | Mutant receipt SHA-256 |
|---|---|---|---|
| `verdict-lowercase-hold` | `fda08b590ea3be2d60369266526c6807fe02e350` | `b92d481925bff480622c17fa4ba9baf374609029` | `a612674cf87f16fdbfa1c48b34e918e527470b6a54ec79063cfe20c8268e2811` |
| `verdict-stale-trailing-space` | `06f831b20e863044c1a2b72857d2161ab9bf9bab` | `cf1447fa1a6e9a4cc6ff64e2dd0e421bbc7564c4` | `ba6488c7d4ac5332e118c196dec9091f89ca8757f869ed3eb7621dde70e2edef` |
| `verdict-array-hold` | `40faaed333bf98144ef3c39253e667db11315070` | `d49f3427fdf3c4950b87e058c44c1f950359cddf` | `c8dbac33803dbb2cc23591ef3a2fc48c37b0b9a0a657c30ec32ac58e0593c13c` |
| `stale-missing-correction` | `431a353c12644651fb2be3863bb3a1a127efa941` | `e59132c454c775d02bb0cdf81faaadc9c5e23c61` | `79ac6feb4ed654eba0d22cb30072cc6548f5baeb33851c06abd49a71b24a0c2f` |
| `unverifiable-empty-reason` | `78bda9bcf3ea1d0268a7a07fce60a5b5cccc68e7` | `1d2216ce0bac7fdd9abb4c319833dac3c9c726d1` | `2e1e475df86b8b0b62a63489d6fdff9d9aa3a56678da293fa97adcc5c6150ebf` |
| `stale-integer-correction` | `7084e37643d4694fa22b0fe7f3aaeaabe1fe8e04` | `dea5d7b404a1390cfe753aace08df95649a2e0e9` | `cf97014f53c67a0bd702fd12c63e6bdec8fe3875368c241a418a83ecf414488f` |

The pristine and restored hashes below apply to every corresponding row above; all five drift-detection restorations and the fleet-registry restoration also compared equal to the base receipt bytes, not merely semantically equivalent JSON.

| Absolute receipt path | Before SHA-256 | After/restored SHA-256 |
|---|---|---|
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/clone/.ufo/waves/round-23/receipts/drift-detection.json` | `212fa028494dbeba1725932901d9cd21abe020512f7320f626bc418732d0a8f8` | `212fa028494dbeba1725932901d9cd21abe020512f7320f626bc418732d0a8f8` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/clone/.ufo/waves/round-23/receipts/fleet-registry.json` | `0f43d815b90c4be058d9305c5e648bdd6f475bd4acebc2b0463b29f5a71f6dc6` | `0f43d815b90c4be058d9305c5e648bdd6f475bd4acebc2b0463b29f5a71f6dc6` |

Final worktree/restoration hash command and exact output:

```text
sha256sum /tmp/kake-r24-GapC1VerdictSet-vbiL/clone/.ufo/waves/round-23/receipts/drift-detection.json /tmp/kake-r24-GapC1VerdictSet-vbiL/clone/.ufo/waves/round-23/receipts/fleet-registry.json /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py
212fa028494dbeba1725932901d9cd21abe020512f7320f626bc418732d0a8f8  /tmp/kake-r24-GapC1VerdictSet-vbiL/clone/.ufo/waves/round-23/receipts/drift-detection.json
0f43d815b90c4be058d9305c5e648bdd6f475bd4acebc2b0463b29f5a71f6dc6  /tmp/kake-r24-GapC1VerdictSet-vbiL/clone/.ufo/waves/round-23/receipts/fleet-registry.json
c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py
```

The runner SHA-256 before the first mutation was also `c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5`.

### Retained evidence artifacts

Each `*.output.json` contains the exact argv, exit status, full stdout string, full stderr string, traceback flag and last stdout line, without output abbreviation. `evidence.json` records commit argv/output, revision and receipt hashes; `cases.json` is the same six-case array above.

| Absolute path | SHA-256 |
|---|---|
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/cases.json` | `7299e8a391dbda3ca08cfe80ba05d528d06aed774f95d18f2fd76afad30aa768` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/evidence.json` | `417143ba243fdf56c8a25fed6c44a22d346eef2c1e77b3c75de9604b0a0eb01a` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/pristine.output.json` | `569f8136db9680f02ac1d896aa75fbf082fa86483201c25d8c580557ce1ab6bd` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/verdict-lowercase-hold.output.json` | `0105b117ea73e7ec3ccb47abe43c9dc4fa487b996afc05ecc7760e940654b663` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/verdict-lowercase-hold-restored.output.json` | `542b3175d29967c57b8e15e87d04193b67ae4bf1155c9b71619b5027d275d840` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/verdict-stale-trailing-space.output.json` | `918c8a309dc7dabe88c09d973d29d7d88c1b85fc2cea191b4d420bcc562b5007` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/verdict-stale-trailing-space-restored.output.json` | `1ac9aa262bc02292ca6c2e035238974d040ee252154e180c808b07fd0f9e715f` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/verdict-array-hold.output.json` | `56f32d5ab0288a4f80c89bb927f048efb2f01b4d22c55d467f1ee65ac1a3ca5c` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/verdict-array-hold-restored.output.json` | `24a748847b876d932682a11000b6b2f69dcda6970c25f4f70a5e9477ee65daf3` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/stale-missing-correction.output.json` | `52da1f1a592cdead5c245cbf1d25e376982e7fc5c2246b67327196af6c524254` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/stale-missing-correction-restored.output.json` | `ea81b02ebe14d8005a6e7f0022424415508fcf7ea4832663e1457e1556d8378a` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/unverifiable-empty-reason.output.json` | `352750ca8b0c6254393d7c3f5fde8d761db8a8fe6eeedd0537aaec799ba10392` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/unverifiable-empty-reason-restored.output.json` | `ce086adfa36b096172d64ab45532abca3cddf988602c1a33972b1195a1fbfc1e` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/stale-integer-correction.output.json` | `4c769e246dc92c333855eaef0e89bb8503f30e9052b53a8b87ea683e5352cbf1` |
| `/tmp/kake-r24-GapC1VerdictSet-vbiL/stale-integer-correction-restored.output.json` | `ede1d249c7a45c6708664cd65fbc74ce644cbb4ad22d9f7d82f7992f65200764` |

### Tools

No tool was installed or upgraded. Used the pre-existing `Python 3.14.8` and `git version 2.56.0` (exact version outputs observed). Required operator rules and the frozen round-24 contract were read before writing; pacman and host services were untouched.

## Limits

- Exactly six assigned mutations were exercised, plus one pristine and six restored replay runs (13 detector invocations). This does not establish rejection of every malformed receipt or general RFC conformance.
- The maintained `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/receipt_replay.py`, round-23 C2 runner, builds, linters, formatters and broad test suites were not invoked. This report therefore does not claim they passed.
- No original observation was re-fetched or authenticated. The only web access was read-only public RFC documentation; no publishing, account operation, secret access, domain-tree mutation or other runtime was performed.
- Only this report was written in the lane. All altered receipts, commits and retained raw probe artifacts are confined to the named scratch directory. No production change, docs change outside this requested report, integration, admission judgment or subagent dispatch was performed.
