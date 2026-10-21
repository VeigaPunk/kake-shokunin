# GapC1HeadingIds — round-24 C2 audit, C1 heading/id boundary

## Verdict

**Scoped audit complete; no production defect exposed in these sampled checks.** Nine committed receipt cases matched the round-23 runner contract: six rejected (exit 1, no traceback) and three accepted controls (exit 0). The unmodified admitted revision was accepted at **17/17** units. A single deliberate section-boundary mutant was **killed**: the detector caught its false acceptance of citations that precede the heading. Exact original bytes were restored after every fixture and after the runner mutation.

Owned axis: **operability**, for round-24 claim C2 / milestone `r24-build`; this is author-side evidence, not independent admission or integration. No freshness reconciliation, publishing, or upstream mutation was attempted.

- Frozen contract read first: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-24/contract.json`.
- Isolated clone: `/tmp/kake-r24-GapC1HeadingIds-MfFE/clone`; `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r24-GapC1HeadingIds-MfFE/clone` observed HEAD `f7de3ab4e9f030a15a857a5a08631bd8e690f436`, then explicitly detached at that same frozen revision.
- All case receipts: `/tmp/kake-r24-GapC1HeadingIds-MfFE/clone/.ufo/waves/round-23/receipts/fire-journal-codes.json`; companion unit fixtures: `/tmp/kake-r24-GapC1HeadingIds-MfFE/clone/corpus/knowledge/fire-journal-codes.md`.
- Every case and exact-byte restoration was committed with `GIT_AUTHOR_DATE=2026-10-21T12:00:00Z` and `GIT_COMMITTER_DATE=2026-10-21T12:00:00Z`.
- Final restored clone HEAD: `9461a35c7266a6368c29a9cf76ebc9e6aba19868`. The case commits remain in this clone history.

## Findings

### P3 — keep the heading boundary as a regression sentinel; no historical-runner fix indicated

Impacted claim/axis: **C2 / operability**. The real runner correctly rejected duplicate ids, unmatched bracket/LF ids, both directions of the c1/c11 citation boundary, and a valid heading positioned after all citations. The smallest plausible defect was deleting only `[position:]` from the section assignment in an isolated exact copy of the historical runner:

```text
file: /tmp/kake-r24-GapC1HeadingIds-MfFE/measure_c1.py:65
pristine:     section = current[position:] if position >= 0 else ""
mutated:      section = current if position >= 0 else ""
```

Expected detector: reject the `heading-id-citations-before-heading` fixture with exit 1 or 2 and no traceback, while retaining all other expected outcomes. The bounded detector checked the same ten committed revisions (one pristine control plus nine cases) against pristine, mutated, and restored runner bytes.

Exact command, unchanged for all three passes:

```text
python3 /tmp/kake-r24-GapC1HeadingIds-MfFE/heading_detector.py --runner /tmp/kake-r24-GapC1HeadingIds-MfFE/measure_c1.py --manifest /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-cases.json --root /tmp/kake-r24-GapC1HeadingIds-MfFE/clone
```

Exact detector summaries emitted by the probe recorder:

```text
{"detectorExit": 0, "failures": [], "falseAccepts": [], "falseRejects": [], "passed": 10, "runnerSha256": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5", "stage": "pristine", "total": 10}
{"detectorExit": 1, "failures": ["heading-id-citations-before-heading"], "falseAccepts": ["heading-id-citations-before-heading"], "falseRejects": [], "passed": 9, "runnerSha256": "e05341dd5cd0159ed26e26252ea6feb1e4ccb34ffcdcb133ff560e46ecf23d78", "stage": "mutated", "total": 10}
{"detectorExit": 0, "failures": [], "falseAccepts": [], "falseRejects": [], "passed": 10, "runnerSha256": "c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5", "stage": "restored", "total": 10}
```

The mutant changed only the before-heading fixture from historical-runner exit 1 / accepted 16/17 / six citation diagnostics to exit 0 / accepted 17/17 / no diagnostics. Its detector exited 1. **Verdict: killed**, not inconclusive: the pristine detector first passed all ten expectations and the restored detector passed them again.

Smallest fix: **none to the byte-frozen historical runner**. Preserve the existing heading-relative slice, complete `[unit:id]` match and exact-equality duplicate check when maintaining replay; do not add an undocumented id grammar to turn the accepted bracket/LF controls into failures.

### P3 — companion unit fixtures are required for five cases

The required case schema expresses receipt JSON operations, not Markdown edits. The four receipt-only cases below can be replayed directly against the frozen base. Five additional cases have real, committed companion Markdown fixtures; the same receipt JSON operation by itself is **not** the case that was exercised. In particular, importing the three fixture-dependent accept controls as receipt-only mutations would incorrectly reject them. The heading-order and short-prefix rejection fixtures change `observedAt` only to a valid same-day timestamp so that a receipt is committed alongside the Markdown fixture; that timestamp is not their rejection cause.

Smallest handling: under the frozen JSON-only population schema, use only the four receipt-only cases as freeze candidates and keep the five companion-dependent cases as separate counter-fixture evidence at their named commits. ExecReceiptReplay confirmed that the replay reads committed unit fixtures, but expressing them in the population would require an explicit schema extension; this report neither assumes nor requests that extension. Do not silently flatten them or change their expected outcomes. This is a representation/coverage limit, not a new receipt contract.

### Case commands and observed outcomes

Each command below is the actual historical runner invocation, with a 120-second per-process bound in the recorder. All had empty stderr and `traceback=false`; each stdout ended with the literal last line `}`. Full, unabridged stdout/stderr, commands, fixture notes, before/after hashes and restoration runs are in the per-case evidence JSON files listed below.

| Case | Expected | Actual exit | Accepted units | Exact diagnostic JSON string values / empty problems |
|---|---|---:|---:|---|
| `heading-id-duplicate` | reject | 1 | 16/17 | `["claim c1: duplicate id"]` |
| `heading-id-close-bracket-uncited` | reject | 1 | 16/17 | `["claim c1]: not cited in round-23 section"]` |
| `heading-id-newline-uncited` | reject | 1 | 16/17 | `["claim c1\n: not cited in round-23 section"]` |
| `heading-id-c11-not-c1` | reject | 1 | 16/17 | `["claim c11: not cited in round-23 section"]` |
| `heading-id-c1-c11-distinct-control` | accept | 0 | 17/17 | `[]` |
| `heading-id-c1-not-c11` | reject | 1 | 16/17 | `["claim c1: not cited in round-23 section"]` |
| `heading-id-close-bracket-cited-control` | accept | 0 | 17/17 | `[]` |
| `heading-id-newline-cited-control` | accept | 0 | 17/17 | `[]` |
| `heading-id-citations-before-heading` | reject | 1 | 16/17 | `["claim c1: not cited in round-23 section", "claim c2: not cited in round-23 section", "claim c3: not cited in round-23 section", "claim c4: not cited in round-23 section", "claim c5: not cited in round-23 section", "claim c6: not cited in round-23 section"]` |

Exact invocations:

```text
# heading-id-duplicate
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1HeadingIds-MfFE/clone --revision 1493b393b3564f851662d4988f57485d4449c94a
# heading-id-close-bracket-uncited
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1HeadingIds-MfFE/clone --revision 757947f9f4a513c370e6e3ade80797cecc9f8bf4
# heading-id-newline-uncited
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1HeadingIds-MfFE/clone --revision 004820dbf80a6efee0db546e69d81617f2e040da
# heading-id-c11-not-c1
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1HeadingIds-MfFE/clone --revision 281c286f7948f8b15b42cdfb1accace3dcf1e0a3
# heading-id-c1-c11-distinct-control
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1HeadingIds-MfFE/clone --revision c93698639a569e6799120f1bf5b636ef259e4ee9
# heading-id-c1-not-c11
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1HeadingIds-MfFE/clone --revision de5234fb91a12378258ae14378a6c44f7c5814f5
# heading-id-close-bracket-cited-control
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1HeadingIds-MfFE/clone --revision bcd42b3ee6187b31976788269f827cde8baa0b06
# heading-id-newline-cited-control
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1HeadingIds-MfFE/clone --revision aff2e42e70ea67352c7750434f4954ff02f202c8
# heading-id-citations-before-heading
python3 /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py --root /tmp/kake-r24-GapC1HeadingIds-MfFE/clone --revision 821ae1b2f1214ad297d8fab4e3ec031bfb672335
```

### Committed companion-fixture definitions

- **`heading-id-c1-c11-distinct-control`**, commit `c93698639a569e6799120f1bf5b636ef259e4ee9`: Companion unit fixture: replace the single [fire-journal-codes:c2] token at original line 83 with [fire-journal-codes:c11]; leave [fire-journal-codes:c1] at line 82 intact. This control requires the companion fixture, not a receipt-only replay.
- **`heading-id-c1-not-c11`**, commit `de5234fb91a12378258ae14378a6c44f7c5814f5`: Companion unit fixture: replace the single [fire-journal-codes:c1] token at original line 82 with [fire-journal-codes:c11], leaving all receipt claim ids and all other citations intact. The receipt change is only a valid same-day RFC 3339 section 5.6 timestamp to commit a receipt together with this fixture; it is not the rejection cause.
- **`heading-id-close-bracket-cited-control`**, commit `bcd42b3ee6187b31976788269f827cde8baa0b06`: Companion unit fixture: replace the single [fire-journal-codes:c1] at original line 82 with [fire-journal-codes:c1]]. No identifier grammar prohibiting ] is documented.
- **`heading-id-newline-cited-control`**, commit `aff2e42e70ea67352c7750434f4954ff02f202c8`: Companion unit fixture: replace [fire-journal-codes:c1] at original line 82 with the bytes [fire-journal-codes:c1 followed by LF then ]; leave the remainder of the row after ]. The JSON id contains the escape \n, not a raw unescaped control byte.
- **`heading-id-citations-before-heading`**, commit `821ae1b2f1214ad297d8fab4e3ec031bfb672335`: Companion unit fixture: move only original line 78, ## Live re-verification — round 23 (2026-10-21), to after original line 87; all six exact citations remain earlier in the file. Receipt observedAt is changed only to an RFC 3339 section 5.6 same-day timestamp to commit a receipt alongside the fixture.

### C2 malformed-case array

All nine objects below describe cases actually run. Cases whose `why` starts with “With the committed companion unit fixture” are counter-fixture evidence only under the current frozen schema: they require the committed fixture described above and MUST NOT be imported as receipt-only population mutations. The remaining four objects are directly replayable freeze candidates.

```json
[
  {
    "id": "heading-id-duplicate",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": [
      "claims",
      1,
      "id"
    ],
    "value": "c1",
    "expect": "reject",
    "why": "The runner requires claim ids to be unique (measure_c1.py:68-75); RFC 8259 section 5 permits repeated array values but does not override this receipt-level uniqueness rule.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "heading-id-close-bracket-uncited",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": [
      "claims",
      0,
      "id"
    ],
    "value": "c1]",
    "expect": "reject",
    "why": "RFC 8259 section 7 permits ] in a string, but the documented literal citation becomes [fire-journal-codes:c1]] and that exact token is not present after the heading.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "heading-id-newline-uncited",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": [
      "claims",
      0,
      "id"
    ],
    "value": "c1\n",
    "expect": "reject",
    "why": "RFC 8259 section 7 permits an escaped LF in a string, but the documented literal citation includes that decoded LF and does not occur after the heading.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "heading-id-c11-not-c1",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": [
      "claims",
      0,
      "id"
    ],
    "value": "c11",
    "expect": "reject",
    "why": "The contract requires the complete [unit:id] literal, so the existing [fire-journal-codes:c1] cannot satisfy id c11; RFC 8259 section 8.3 compares decoded strings rather than prefixes.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "heading-id-c1-c11-distinct-control",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": [
      "claims",
      1,
      "id"
    ],
    "value": "c11",
    "expect": "accept",
    "why": "With the committed companion unit fixture, the documented uniqueness check is exact equality and both distinct ids have complete citations after the heading; RFC 8259 section 8.3 gives no basis for treating c1 and c11 as equal.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "heading-id-c1-not-c11",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": [
      "observedAt"
    ],
    "value": "2026-10-21T12:00:00Z",
    "expect": "reject",
    "why": "With the committed companion unit fixture, the complete [unit:id] requirement prevents [fire-journal-codes:c11] from satisfying c1 even though c1 is a prefix of c11; the valid same-day observedAt change is not the rejection cause.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "heading-id-close-bracket-cited-control",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": [
      "claims",
      0,
      "id"
    ],
    "value": "c1]",
    "expect": "accept",
    "why": "With the committed companion unit fixture, the contract permits any nonblank string id with its exact citation, and RFC 8259 section 7 permits ]; this companion fixture supplies the complete [fire-journal-codes:c1]] token.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "heading-id-newline-cited-control",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": [
      "claims",
      0,
      "id"
    ],
    "value": "c1\n",
    "expect": "accept",
    "why": "With the committed companion unit fixture, rFC 8259 section 7 allows escaped LF in a string and the runner documents raw literal citation matching, not a single-line or Markdown-rendered id grammar; the companion contains that exact decoded-LF token.",
    "r23Observed": {
      "exit": 0,
      "traceback": false,
      "stdoutTail": "}"
    }
  },
  {
    "id": "heading-id-citations-before-heading",
    "target": "c1",
    "file": ".ufo/waves/round-23/receipts/fire-journal-codes.json",
    "op": "set",
    "jsonPath": [
      "observedAt"
    ],
    "value": "2026-10-21T12:00:00Z",
    "expect": "reject",
    "why": "With the committed companion unit fixture moving the heading below all citations, the runner docstring requires rejection because every [unit:id] must follow the heading; the valid same-day observedAt change is not the rejection cause.",
    "r23Observed": {
      "exit": 1,
      "traceback": false,
      "stdoutTail": "}"
    }
  }
]
```

## Checked and held

- `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py:2-19` documents nonempty claims, exact citation text and placement after the heading; `:68-75` enforces unique ids; `:83-84` checks the complete token. The existing historical duplicate-id mutation fixture also treats duplicates as invalid. Duplicate claim-id values are an application-level rule, **not** RFC 8259’s rule about object member names.
- [RFC 8259 §7](https://www.rfc-editor.org/rfc/rfc8259#section-7): `]` is legal inside a JSON string and LF is legal when escaped as `\n`; the decoded LF is then part of the id. These probes used valid escaped LF, not invalid raw LF inside JSON quotation marks. The documented contract has no prohibition on either character. Exact-citation controls therefore expect acceptance.
- [RFC 8259 §8.3](https://www.rfc-editor.org/rfc/rfc8259#section-8.3): string equality uses decoded code units, not prefix equality. Distinct `c1` and `c11` with their own exact tokens remained accepted.
- [RFC 3339 §5.6](https://www.rfc-editor.org/rfc/rfc3339#section-5.6) specifies date-time grammar, and [RFC 9110 §8.3.1](https://www.rfc-editor.org/rfc/rfc9110#section-8.3.1) specifies HTTP media types; neither defines claim-id syntax or Markdown heading semantics. No timestamp/media-type acceptance rule was invented for this heading/id audit. The two companion fixtures that change `observedAt` use `2026-10-21T12:00:00Z`, a syntactically valid date-time.
- Pristine admitted revision: historical C1 runner exit 0, accepted 17/17; verdict totals HOLD 79, STALE 55, UNVERIFIABLE 42. After **each of the nine cases**, the same historical runner on the exact-byte restoration commit returned exit 0, accepted 17/17, with no traceback.

### Restoration evidence

Each case’s receipt and unit file returned to these original hashes. The runner copy was restored from the original captured bytes in `finally`; no mutated runner remains. Final observed `sha256sum` output:

```text
c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5  /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/measure_c1.py
c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5  /tmp/kake-r24-GapC1HeadingIds-MfFE/clone/.ufo/waves/round-23/measure_c1.py
ffc9b3a44ee84ed827f3badc697f0ae5c8be007a50de3cafc2ccd23617697daf  /tmp/kake-r24-GapC1HeadingIds-MfFE/clone/.ufo/waves/round-23/c1-population.json
17722509b0589b30d3ba279ef40edaaba9f6763854f7b89dc393a61fed86830e  /tmp/kake-r24-GapC1HeadingIds-MfFE/clone/.ufo/waves/round-23/receipts/fire-journal-codes.json
7e74cb6346300b1b3a242d1a1c14c72f7932956f6f5a29055c78e6e26503a503  /tmp/kake-r24-GapC1HeadingIds-MfFE/clone/corpus/knowledge/fire-journal-codes.md
c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5  /tmp/kake-r24-GapC1HeadingIds-MfFE/measure_c1.py
```

| Case | Mutated receipt SHA-256 | Mutated unit SHA-256 | Exact restoration commit |
|---|---|---|---|
| `heading-id-duplicate` | `0d24f3649369f11b490d66c69f04bac7cdce2ec711d49743ed2c07cb9a9edbe0` | `7e74cb6346300b1b3a242d1a1c14c72f7932956f6f5a29055c78e6e26503a503` | `cace26f2af90856ed80e89f36d6defdb0450726a` |
| `heading-id-close-bracket-uncited` | `3161329f0d6e4caa9fc5063cb481f7b0718d47257430c2740a05d03988ee87a2` | `7e74cb6346300b1b3a242d1a1c14c72f7932956f6f5a29055c78e6e26503a503` | `53d6d05919db057964fa2fe8097a18164275ff43` |
| `heading-id-newline-uncited` | `5002e5c9abc6297e91c0c5216240fe06394922ce0d292f6a2f92ff48ad3168c8` | `7e74cb6346300b1b3a242d1a1c14c72f7932956f6f5a29055c78e6e26503a503` | `5b5999f9f2a5372dde349c0d11cfb9292512cca1` |
| `heading-id-c11-not-c1` | `886492999681e7fd157efcb41520e1d50bb17bd737aac60d630dad4b3f3b9df1` | `7e74cb6346300b1b3a242d1a1c14c72f7932956f6f5a29055c78e6e26503a503` | `8b3b708185a3036a23ea8e36b4e8a8a91a866c87` |
| `heading-id-c1-c11-distinct-control` | `3d5f59d1e6b9e217109c4b8c84c229d3a135cce39660c4f7caa04db120f13d2a` | `bd6a7fccf24459bcc8296d80d42778ffe2cc40d6103d6d265cbd0d2f2508a581` | `624cb9649597a12c38c91912779f227d2514b183` |
| `heading-id-c1-not-c11` | `0ec44451c78cb28f05442c8246ad00bb320b8a83a0f000f696d2bb78c3f877dc` | `ac3d9d074caef35569317c898337226892151bc892e4446a3918b57f916bd5d8` | `d6e3c95578ffcd6ac8b0032be9ecdfa99cd4708f` |
| `heading-id-close-bracket-cited-control` | `3161329f0d6e4caa9fc5063cb481f7b0718d47257430c2740a05d03988ee87a2` | `499b0f032440651491cd428d09e5d5607812eff888e70fa29ba90c1313758e6b` | `81e22e98281bae19731953a236c12995c6d69b99` |
| `heading-id-newline-cited-control` | `5002e5c9abc6297e91c0c5216240fe06394922ce0d292f6a2f92ff48ad3168c8` | `deb8009011471f9a1de40015b84f02e633e9e39f53d25877a105acbd47c29d08` | `549957b5c3d67373f2b7840efb854e736e08b78e` |
| `heading-id-citations-before-heading` | `0ec44451c78cb28f05442c8246ad00bb320b8a83a0f000f696d2bb78c3f877dc` | `9a20c51fb8c3e2bb926cffe7e17771ce9ab7e484bdd21e599dcd100aa00548f8` | `9461a35c7266a6368c29a9cf76ebc9e6aba19868` |

The mutant runner SHA-256 was `e05341dd5cd0159ed26e26252ea6feb1e4ccb34ffcdcb133ff560e46ecf23d78`; pristine/restored SHA-256 was `c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5`. Receipt before/after SHA-256 was `17722509b0589b30d3ba279ef40edaaba9f6763854f7b89dc393a61fed86830e`; unit before/after SHA-256 was `7e74cb6346300b1b3a242d1a1c14c72f7932956f6f5a29055c78e6e26503a503`.

### Retained investigation artifacts

All paths below are absolute; each line is an observed SHA-256 followed by its artifact path. The clone contains the committed receipt/unit fixture bytes. `heading-cases.json` maps every case to its committed revision and companion fixture; each per-case JSON retains the full original runner output and its restoration output. `detector-*.json` retains the full ten-case output for the named runner-byte stage.

```text
a0e9096ca5382c7ce98c92d567c14f325dabc52a470b00a254bfd8b584606c6c  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading_detector.py
aa72f5de89dc09f3aa254ff8b07fa5f8e2b50cecc57a09f25c0286a3892eb25e  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-cases.json
a42cba4fb912f1e3f1f93ea4f019f5c640a88e3ca0160856fc926267baf46c17  /tmp/kake-r24-GapC1HeadingIds-MfFE/malformed-cases.json
c217d2760d4bcb3e66bc8f19dfd41077a3cb774b0310e1e9c47099c46ef8bdc5  /tmp/kake-r24-GapC1HeadingIds-MfFE/measure_c1.py
cfb450c68cfb7ef60b1f897102a62c48a3a79dabe8135e33b46885ae1a701941  /tmp/kake-r24-GapC1HeadingIds-MfFE/probe-evidence.json
eed7df4447bb1573e96ad270b0b29f9f3668e9bac40a21da214b13978fb3aae5  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-id-duplicate.json
4d0c840fbdf594da33b2a376ba977514f086df21c3a52d85ecc306ecafdfa638  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-id-close-bracket-uncited.json
7976306b3729a42b21658923fd160c8d2e10d7868f1e4574321f92dddded7682  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-id-newline-uncited.json
ab9d6ed46a44dadaf3a5674485f9b546288e21127e891dda61b26dc091e9f41b  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-id-c11-not-c1.json
905fa87ecd51819c09bbc2dbce25d45be4c6ef7a27589428edb698d880ffc8a5  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-id-c1-c11-distinct-control.json
16a586d3891c153d90326d3ae95f758cefe18144ada7ca9c1c19c08bca2f4910  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-id-c1-not-c11.json
23588f6b5a8895de5b38543967408ae5f9ec82957da292bb8d4372ac0b7bf7c1  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-id-close-bracket-cited-control.json
ba0c625b4599ded0a8c2a83aa57553d53ff6130ee028ebdec4540e3384c01d1c  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-id-newline-cited-control.json
26b9b2915a186803f72efcd84841837185afc9bf059e9994766efaef17e7d515  /tmp/kake-r24-GapC1HeadingIds-MfFE/heading-id-citations-before-heading.json
ad48ef985772cd08c543a110e49a38859d35516ee0913a94c8df14bf2434bc69  /tmp/kake-r24-GapC1HeadingIds-MfFE/detector-pristine.json
f1f0f8887b37d2b7c02ebebe34ddfcfcc772fa8265302ac22d7abf9cccdef3c1  /tmp/kake-r24-GapC1HeadingIds-MfFE/detector-mutated.json
d2af4a7e4c36dad060fb9d50774892a29231cb191923cd81eb45c7beca4053ed  /tmp/kake-r24-GapC1HeadingIds-MfFE/detector-restored.json
```

Additional checksum manifests: `/tmp/kake-r24-GapC1HeadingIds-MfFE/artifact-hashes.txt` and `/tmp/kake-r24-GapC1HeadingIds-MfFE/restoration-hashes.txt`.

## Limits

- This is a scoped nine-case audit and one plausible section-boundary mutation probe, not exhaustive receipt validation or independent admission. It establishes only the exercised heading/id behavior.
- Five cases require their companion unit-file fixtures and cannot be reproduced from the receipt-only operation alone. The report keeps that boundary explicit; no frozen population or maintained production script was edited.
- No builds, lint, formatters, network probes of domain surfaces, installation, publishing, source-tree writes, or additional runtimes were invoked. Only targeted Python CLI probes, Git commits in the isolated clone, read-only RFC GETs, and checksums were used. No subagents were spawned.
- Existing tools: Python `3.14.8`, Git `2.56.0`. Tools installed/upgraded: **none**. The host-wide pacman pause was respected.
- The lane was read-only except for this assigned report; historical round-23 runners and receipts, production files, lane/fleet Git state, sibling lanes, domain trees and configuration were not modified.
