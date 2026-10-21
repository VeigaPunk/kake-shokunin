# Round 23 wave 2 — MutateGuards

## Verdict

**Counterexample found: guard-regression coverage gap.** Of seven isolated one-line mutants, **six were killed and one survived** the combined prescribed detectors; none was inconclusive. The surviving M3 removes the foreign end-tag mismatch rejection, yet both commands still pass with byte-for-byte baseline stdout. This is a detector-coverage finding, not an admission judgment, proof of a live-page defect, or a falsification of C2's specific 12/12 receipt-reproduction count.

**Axis:** operability (C2). **Milestone:** r23-falsify. No production fix was made and no contract was changed.

| Mutant | Guard | Selftest on mutant | Relaxation probe on mutant | Combined verdict |
| --- | --- | --- | --- | --- |
| M1 | base-after-head check | killed; exit 1; 80/81; [S2](#output-s2) | killed; exit 1; 9/11; [R2](#output-r2) | **killed** |
| M2 | foreign base/head/link token check | killed; exit 1; 79/81; [S3](#output-s3) | survived; exit 0; 11/11; [R1](#output-r1) | **killed** |
| M3 | foreign end-tag mismatch | survived; exit 0; 81/81; [S1](#output-s1) | survived; exit 0; 11/11; [R1](#output-r1) | **survived** |
| M4 | set_cdata_mode override | killed; exit 1; 78/81; [S4](#output-s4) | killed; exit 1; 8/11; [R3](#output-r3) | **killed** |
| M5 | C1-control range | killed; exit 1; 79/81; [S5](#output-s5) | survived; exit 0; 11/11; [R1](#output-r1) | **killed** |
| M6 | duplicate-page check | killed; exit 1; 80/81; [S6](#output-s6) | survived; exit 0; 11/11; [R1](#output-r1) | **killed** |
| M7 | HTML_VOID_ELEMENTS allowance | killed; exit 1; 80/81; [S7](#output-s7) | killed; exit 1; 10/11; [R4](#output-r4) | **killed** |

## Findings

### P2 — M3: deleting foreign end-tag mismatch rejection survives both detectors

- **Impacted claim/axis:** C2 / operability, specifically regression confidence in the fail-closed foreign-content parser boundary at `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py:310-319`.
- **Smallest mutant:** in the foreign-stack mismatch `else` branch, replace `self.unsupported = True` with `pass` at original line 318. All other guards and all tests remain unchanged.
- **Exact commands:** the two commands in [Execution](#execution), run against the M3 bytes identified in the hash ledger.
- **Exact output:** [S1](#output-s1), exit 0, selftest passed 81/81; [R1](#output-r1), exit 0, relaxation probe passed 11/11. Both stderr streams are exactly empty. Full captured stdout is reproduced in the output dictionary, not paraphrased.
- **Expected detector before execution:** both were predicted to survive. The only explicit mismatched-end case also has forbidden foreign base markup and a residual foreign-stack entry. Other rejection paths therefore mask removal of this guard.
- **Smallest fix (recommendation, not applied):** retain the existing production guard and add a mismatched foreign end-tag regression whose foreign stack subsequently closes normally and which contains no base/head/canonical token. [INFERENCE; unrun] A candidate is a valid explicit head/canonical followed by `<body><svg><g></path></g></svg></body>`, expecting exit 2 / `html_unsupported`. Add an analogous non-clean expectation to the relaxation detector if that detector is intended to protect this guard independently. No added test or candidate payload was executed in this assignment.

### P3 — M2: relaxation probe alone does not detect removal of the foreign-token rejection

- **Impacted claim/axis:** C2 / operability, standalone coverage of the guard at `/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/canonical_audit.py:206-210`. The combined detector does kill M2, so this is narrower than the M3 gap.
- **Smallest mutant:** replace the `_foreign_token` condition with `if False:` at original line 209, disabling its base/head/canonical-link rejection without changing foreign-stack handling.
- **Exact commands:** the same two commands in [Execution](#execution), against M2 bytes.
- **Exact output:** [S3](#output-s3), exit 1, 79/81: `body_svg_selfclose_link` changes from expected exit 2 / `html_unsupported` to exit 1 / `canonical_missing`, and `foreignobject_base` changes from expected exit 2 / `html_unsupported` to exit 0 / null finding. [R1](#output-r1) remains exit 0, 11/11, with identical baseline stdout. Both stderr streams are empty.
- **Expected detector before execution:** selftest was predicted to kill and relaxation could survive. The prediction additionally named `foreign_content` as a selftest failure; that specific prediction did not occur. [INFERENCE from the unchanged parser] Its unclosed ordinary foreign `link` leaves another rejection path active. This does not alter the observed two failing cases or combined verdict.
- **Smallest fix (recommendation, not applied):** port the already-killing self-closing foreignObject/base selftest shape into the relaxation attacks. Its current foreign base payloads use a non-self-closing base, allowing unrelated stack/mismatch rejection to satisfy the broad “not clean” expectation.

## Checked and held

- Exactly the requested seven mutants were applied, one at a time, in the isolated clone. Each changed one original source line. No two mutants overlapped.
- Both named commands ran on pristine, mutated, and restored bytes for every mutant: **42 detector invocations**, comprising 21 selftests and 21 relaxation probes. Every invocation completed; no timeout, baseline failure, or restored-byte failure occurred.
- Every one of the seven pristine phases and seven restored phases returned selftest exit 0 (81/81) and relaxation exit 0 (11/11). All pristine/restored stdout matched S1/R1 byte for byte.
- M1, M2, M4, M5, M6, and M7 were killed by selftest. The relaxation probe independently killed M1, M4, and M7. Its lack of C1-control and duplicate-manifest coverage is outside its documented body-markup purpose; it is not treated here as a defect in those production guards.
- Exact original source bytes were restored in a `finally` path after each mutated phase, then the same detectors were run again. Every restored source hash equals the original hash below. Hashes immediately before and after every detector pair also matched, showing those detector runs did not modify the validator.
- The relaxation detector file was never mutated; its final checksum remains the initial checksum below. No selftest, probe, fixture, manifest contract, live receipt, or production source was edited in the lane. The only lane write is this requested report.

## Execution

- Frozen candidate: `5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd`.
- Scratch root: `/tmp/kake-r23w2-MutateGuards-HBeu`. Clone: `/tmp/kake-r23w2-MutateGuards-HBeu/clone`.
- Exact clone/checkout command (completed successfully):

```sh
git clone --no-hardlinks --no-checkout /home/vgpnk/Projects/shokunin/kake-shokunin /tmp/kake-r23w2-MutateGuards-HBeu/clone && git -C /tmp/kake-r23w2-MutateGuards-HBeu/clone checkout --detach 5e5afb9e4d8ee18831b9b35b35e8a34e47aceecd
```

- Checkout stdout/stderr as delivered by the command tool (combined display):

```text
Cloning into '/tmp/kake-r23w2-MutateGuards-HBeu/clone'...
done.
HEAD is now at 5e5afb9 round-23: counter selftest removes every heading copy; add all-UNVERIFIABLE and non-GET cases
```

- Working directory for every detector: `/tmp/kake-r23w2-MutateGuards-HBeu/clone`. Pre-existing interpreter: `Python 3.14.8`.
- Environment added consistently to every phase: `TMPDIR=/tmp/kake-r23w2-MutateGuards-HBeu` and `PYTHONDONTWRITEBYTECODE=1`; other inherited variables were unchanged. Temporary detector fixtures stayed beneath the assigned scratch root. Each outer command had a 90-second deadline.
- Exact detector commands, unchanged in all phases:

```sh
python3 /tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py --selftest
python3 /tmp/kake-r23w2-MutateGuards-HBeu/clone/.ufo/waves/round-23/relaxation_probe.py --validator /tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py
```

The two read-only detector processes were launched concurrently inside each stable-byte phase; mutations and restorations were serialized. All following case failure blocks are exact JSON record values selected from the captured selftest/probe stdout, not replacements for the full exact stdout dictionary.

## Per-mutant expectations and observed outputs

### M1 — base-after-head check

Original line 289 in `/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py`; one-line change:

```diff
-        if tag in {"head", "base"}:
+        if tag == "head":
```

**Expectation recorded before any detector ran:** selftest kills body_base; relaxation kills body_base and body_base_selfclose, because body base is no longer rejected.

**Observed:** killed.

- `selftest`: exit 1; passed `false`; exact full stdout [S2](#output-s2); stderr empty. Selected failing records:

```json
[
  {
    "actual": {
      "exit": 0,
      "id": null
    },
    "expected": {
      "exit": 2,
      "id": "html_unsupported"
    },
    "name": "body_base",
    "ok": false
  }
]
```

- `relaxation`: exit 1; passed `false`; exact full stdout [R2](#output-r2); stderr empty. Selected failing records:

```json
[
  {
    "case": "body_base",
    "expect": "not clean",
    "exit": 0,
    "verdict": "clean",
    "ok": false
  },
  {
    "case": "body_base_selfclose",
    "expect": "not clean",
    "exit": 0,
    "verdict": "clean",
    "ok": false
  }
]
```

### M2 — foreign base/head/link token check

Original line 209 in `/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py`; one-line change:

```diff
-        if tag in {"base", "head"} or (tag == "link" and is_canonical_relation(attrs_first_wins(attrs))):
+        if False:
```

**Expectation recorded before any detector ran:** selftest kills foreign_content, body_svg_selfclose_link and foreignobject_base; relaxation may survive because its non-self-closing foreign base payloads independently leave unmatched foreign-stack elements.

**Observed:** killed.

- `selftest`: exit 1; passed `false`; exact full stdout [S3](#output-s3); stderr empty. Selected failing records:

```json
[
  {
    "actual": {
      "exit": 1,
      "id": "canonical_missing"
    },
    "expected": {
      "exit": 2,
      "id": "html_unsupported"
    },
    "name": "body_svg_selfclose_link",
    "ok": false
  },
  {
    "actual": {
      "exit": 0,
      "id": null
    },
    "expected": {
      "exit": 2,
      "id": "html_unsupported"
    },
    "name": "foreignobject_base",
    "ok": false
  }
]
```

- `relaxation`: exit 0; passed `true`; exact full stdout [R1](#output-r1); stderr empty. Selected failing records:

```json
[]
```

### M3 — foreign end-tag mismatch

Original line 318 in `/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py`; one-line change:

```diff
-                self.unsupported = True
+                pass
```

**Expectation recorded before any detector ran:** both detectors survive: the existing mismatched-end base case also encounters a forbidden foreign base and leaves an unclosed foreign stack, masking omission of the mismatch rejection.

**Observed:** survived.

- `selftest`: exit 0; passed `true`; exact full stdout [S1](#output-s1); stderr empty. Selected failing records:

```json
[]
```

- `relaxation`: exit 0; passed `true`; exact full stdout [R1](#output-r1); stderr empty. Selected failing records:

```json
[]
```

### M4 — set_cdata_mode override

Original line 202 in `/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py`; one-line change:

```diff
-        if self.foreign_stack:
+        if False:
```

**Expectation recorded before any detector ran:** both detectors kill svg_title_hidden_base, svg_style_hidden_base and svg_script_hidden_base: inherited HTML CDATA hides the base markup.

**Observed:** killed.

- `selftest`: exit 1; passed `false`; exact full stdout [S4](#output-s4); stderr empty. Selected failing records:

```json
[
  {
    "actual": {
      "exit": 0,
      "id": null
    },
    "expected": {
      "exit": 2,
      "id": "html_unsupported"
    },
    "name": "svg_title_hidden_base",
    "ok": false
  },
  {
    "actual": {
      "exit": 0,
      "id": null
    },
    "expected": {
      "exit": 2,
      "id": "html_unsupported"
    },
    "name": "svg_style_hidden_base",
    "ok": false
  },
  {
    "actual": {
      "exit": 0,
      "id": null
    },
    "expected": {
      "exit": 2,
      "id": "html_unsupported"
    },
    "name": "svg_script_hidden_base",
    "ok": false
  }
]
```

- `relaxation`: exit 1; passed `false`; exact full stdout [R3](#output-r3); stderr empty. Selected failing records:

```json
[
  {
    "case": "svg_title_hidden_base",
    "expect": "not clean",
    "exit": 0,
    "verdict": "clean",
    "ok": false
  },
  {
    "case": "svg_style_hidden_base",
    "expect": "not clean",
    "exit": 0,
    "verdict": "clean",
    "ok": false
  },
  {
    "case": "svg_script_hidden_base",
    "expect": "not clean",
    "exit": 0,
    "verdict": "clean",
    "ok": false
  }
]
```

### M5 — C1-control range

Original line 476 in `/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py`; one-line change:

```diff
-    if "\\" in raw or any(ord(ch) <= 0x20 or 0x7F <= ord(ch) <= 0x9F for ch in raw):
+    if "\\" in raw or any(ord(ch) <= 0x20 or ord(ch) == 0x7F for ch in raw):
```

**Expectation recorded before any detector ran:** selftest kills href_c1_control_path and href_c1_control_query; relaxation survives because none of its cases exercises C1 controls.

**Observed:** killed.

- `selftest`: exit 1; passed `false`; exact full stdout [S5](#output-s5); stderr empty. Selected failing records:

```json
[
  {
    "actual": {
      "exit": 0,
      "id": null
    },
    "expected": {
      "exit": 1,
      "id": "canonical_url_invalid"
    },
    "name": "href_c1_control_path",
    "ok": false
  },
  {
    "actual": {
      "exit": 1,
      "id": "canonical_mismatch"
    },
    "expected": {
      "exit": 1,
      "id": "canonical_url_invalid"
    },
    "name": "href_c1_control_query",
    "ok": false
  }
]
```

- `relaxation`: exit 0; passed `true`; exact full stdout [R1](#output-r1); stderr empty. Selected failing records:

```json
[]
```

### M6 — duplicate-page check

Original line 699 in `/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py`; one-line change:

```diff
-        if any(page["url"] == seen["url"] or page["file"] == seen["file"] for seen in normalized_pages):
+        if False and any(page["url"] == seen["url"] or page["file"] == seen["file"] for seen in normalized_pages):
```

**Expectation recorded before any detector ran:** selftest kills duplicate_pages; relaxation survives because it supplies one-page manifests only.

**Observed:** killed.

- `selftest`: exit 1; passed `false`; exact full stdout [S6](#output-s6); stderr empty. Selected failing records:

```json
[
  {
    "actual": {
      "exit": 0,
      "id": null
    },
    "expected": {
      "exit": 2,
      "id": "input_invalid"
    },
    "name": "duplicate_pages",
    "ok": false
  }
]
```

- `relaxation`: exit 0; passed `true`; exact full stdout [R1](#output-r1); stderr empty. Selected failing records:

```json
[]
```

### M7 — HTML_VOID_ELEMENTS allowance

Original line 305 in `/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py`; one-line change:

```diff
-        if tag not in HEAD_VOID_ELEMENTS and not (self._after_head() and tag in HTML_VOID_ELEMENTS):
+        if tag not in HEAD_VOID_ELEMENTS:
```

**Expectation recorded before any detector ran:** selftest kills body_void_selfclose; relaxation kills control_void_selfclose because accepted body void self-closing syntax is now rejected.

**Observed:** killed.

- `selftest`: exit 1; passed `false`; exact full stdout [S7](#output-s7); stderr empty. Selected failing records:

```json
[
  {
    "actual": {
      "exit": 2,
      "id": "html_unsupported"
    },
    "expected": {
      "exit": 0,
      "id": null
    },
    "name": "body_void_selfclose",
    "ok": false
  }
]
```

- `relaxation`: exit 1; passed `false`; exact full stdout [R4](#output-r4); stderr empty. Selected failing records:

```json
[
  {
    "case": "control_void_selfclose",
    "expect": "clean",
    "exit": 2,
    "verdict": "could-not-evaluate",
    "ok": false
  }
]
```

## Before / mutated / restored hashes

Original validator SHA-256 (**B**, 50,616 bytes): `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387`. Every pristine source hash and every restored source hash below equals B.

Relaxation probe SHA-256, initial and final: `b435251eda266b8d817486d7ceb9f385ec07f905a56d5a2aa177e7a7d47cf6ef`.

| Mutant | Pristine SHA-256 | Mutated SHA-256 | Restored SHA-256 |
| --- | --- | --- | --- |
| M1 | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` | `80504748f990cc9f4a3a0337abaeb531e904167cae6ba537082685a5168bb7a8` | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` |
| M2 | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` | `c7553eb7db69072e951f53b139217d67550fd8832f49f7cca4fce1392a243ca5` | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` |
| M3 | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` | `85657c9a7cdd751b7fa1caa8a679dd714331ba63525d47eaa429639df53899c0` | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` |
| M4 | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` | `6607887b965d226211b25409cceec59c4be0777ee029361de81b639e66b397e6` | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` |
| M5 | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` | `2cf6fa8ea7588c1660cea71a37e7a561072400b117a0edc1da92b5e45c83f612` | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` |
| M6 | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` | `164a74410c3e3cffa470b5a98d670eeb3555867ea4b248eb17438c31039fb670` | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` |
| M7 | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` | `05a398dcedba026a0774cc9cdf94cfc0bf3294a0bc167074a25d916647c48dae` | `062ccc4db6ab506ecb274ac0da4e4c4e9041462562e23cc586a0168cc8e44387` |

## Phase-by-phase detector ledger

Each row records an actual execution pair. S/R output IDs reference exact captured bytes in the dictionary below; repeated IDs mean identical stdout, stderr, and exit status, not omitted runs. “B” is the full original validator hash above. Mutated hashes are listed in full in the preceding ledger.

| Mutant | Phase | Source hash before = after | Selftest exit / exact output | Relaxation exit / exact output |
| --- | --- | --- | --- | --- |
| M1 | pristine | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M1 | mutated | M1 mutated | 1 / [S2](#output-s2) | 1 / [R2](#output-r2) |
| M1 | restored | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M2 | pristine | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M2 | mutated | M2 mutated | 1 / [S3](#output-s3) | 0 / [R1](#output-r1) |
| M2 | restored | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M3 | pristine | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M3 | mutated | M3 mutated | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M3 | restored | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M4 | pristine | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M4 | mutated | M4 mutated | 1 / [S4](#output-s4) | 1 / [R3](#output-r3) |
| M4 | restored | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M5 | pristine | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M5 | mutated | M5 mutated | 1 / [S5](#output-s5) | 0 / [R1](#output-r1) |
| M5 | restored | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M6 | pristine | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M6 | mutated | M6 mutated | 1 / [S6](#output-s6) | 0 / [R1](#output-r1) |
| M6 | restored | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M7 | pristine | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |
| M7 | mutated | M7 mutated | 1 / [S7](#output-s7) | 1 / [R4](#output-r4) |
| M7 | restored | B | 0 / [S1](#output-s1) | 0 / [R1](#output-r1) |

## Limits

- Leaf mutation probe only: no subagent dispatch, runtime admission/judgment, integration, production changes, builds, lint, formatters, live HTTP probes, or system/service operations. Neither C1 nor C2 measurement counters were run; no 17/17 or 12/12 remeasurement is claimed.
- A killed mutant demonstrates sensitivity to this particular one-line defect, not exhaustive parser correctness. A surviving mutant is a coverage finding, not permission to relax the documented boundary. The recommended additional regression inputs were not run.
- The C1-control-range guard refers to Unicode C1 control characters; it is not claim C1 (freshness). Its mutation results are classified solely on operability.
- Pristine source capture through the raw ranged reader omitted its final LF. Before any detector execution, one LF was restored to the captured text and its SHA-256 was required to match the independently observed original checksum. Every later restoration matched that checksum. The raw-reader discrepancy was reported through the tool issue channel; it did not cause a detector failure or an inconclusive mutant.
- **Tool installs/updates:** none. Used pre-existing `Python 3.14.8`, Git, sha256sum, wc, and mktemp. No pacman transaction or other installation channel was used.
- Scratch evidence retained at `/tmp/kake-r23w2-MutateGuards-HBeu`: `expectations.json` records expectations fixed before testing; each `M<n>-pristine.json`, `M<n>-mutated.json`, and `M<n>-restored.json` contains exact captured stdout/stderr, exit status, commands, working directory, output hashes, and source before/after hashes. The report below embeds every unique detector output, so it does not depend on scratch retention to preserve exact stdout.

## Exact output dictionary

These are complete stdout streams captured from the named detector commands, without reformatting or truncation. Each code block includes the stdout stream's final LF. Every stderr stream was exactly zero bytes (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). IDs also carry exit status, stdout byte count, and SHA-256. Identical outputs are deduplicated; all 42 individual command results are mapped by the phase ledger.

<a id="output-s1"></a>

### S1 — selftest

Exit: `0`. Stdout: `11106` bytes. SHA-256: `9459f427aa3d5b6f5a1d4392fabaf3f578f832734c014931b3caa52d38234abf`. Stderr: exactly empty.

```json
{"selftest": {"cases": [{"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "absolute_match", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "selfclosing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "title_text_decoy", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_same_dir", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_parent", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "root_relative", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "scheme_relative", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority_four", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "first_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "second_base_ignored", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "empty_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_token_list", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_uppercase", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "attr_uppercase", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "rel_non_ascii_separator", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "duplicate_attrs_first_wins", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "entity_href", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "query_preserved", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "empty_query_delimiter", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "relative_empty_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "missing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_same", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_different", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_absent", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_empty", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_ascii_whitespace", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "invalid_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "javascript_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "data_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "fragment_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "empty_fragment", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_host", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_query", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_invalid", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "comment_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "script_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "template_decoy", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "template_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "noscript_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreign_content", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_svg_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_math_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_void_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_selfclose_link", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_svg", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_nonvoid_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_unclosed", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_svg_then_body_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreignobject_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_head_breakout_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_mismatched_end_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_title_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_style_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_script_hidden_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "svg_title_text_clean", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "processing_instruction", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "missing_head", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_body_child", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_traversal", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_parent", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "fifo_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_symlink", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "manifest_dir_caller_prefix", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "empty_manifest", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "duplicate_pages", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_mode", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_unknown_flag", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_manifest_path", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_conflicting_modes", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_json_with_selftest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_abbreviated_manifest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_repeated_manifest", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "cli_help", "ok": true}], "passed": true}, "tool": "canonical_audit.py"}
```

<a id="output-r1"></a>

### R1 — relaxation

Exit: `0`. Stdout: `1578` bytes. SHA-256: `ce749d35097a17a3a5e5775875a8b84acff244314927c8860289e09cad0c6436`. Stderr: exactly empty.

```json
{
 "validator": "/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py",
 "passed": true,
 "met": 11,
 "total": 11,
 "cases": [
  {
   "case": "body_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "body_base_selfclose",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "foreignobject_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_head_breakout_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_mismatched_end_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_title_hidden_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_style_hidden_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_script_hidden_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "math_annotation_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "control_body_svg",
   "expect": "clean",
   "exit": 0,
   "verdict": "clean",
   "ok": true
  },
  {
   "case": "control_void_selfclose",
   "expect": "clean",
   "exit": 0,
   "verdict": "clean",
   "ok": true
  }
 ]
}
```

<a id="output-s2"></a>

### S2 — selftest

Exit: `1`. Stdout: `11094` bytes. SHA-256: `b8c5666e8a64a43bb8f3b5d6ae5e753473e36ba1c22f229f046aa7ca70eaff12`. Stderr: exactly empty.

```json
{"selftest": {"cases": [{"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "absolute_match", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "selfclosing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "title_text_decoy", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_same_dir", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_parent", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "root_relative", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "scheme_relative", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority_four", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "first_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "second_base_ignored", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "empty_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_token_list", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_uppercase", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "attr_uppercase", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "rel_non_ascii_separator", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "duplicate_attrs_first_wins", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "entity_href", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "query_preserved", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "empty_query_delimiter", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "relative_empty_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "missing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_same", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_different", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_absent", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_empty", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_ascii_whitespace", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "invalid_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "javascript_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "data_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "fragment_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "empty_fragment", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_host", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_query", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_invalid", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "comment_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "script_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "template_decoy", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "template_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "noscript_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreign_content", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_svg_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_math_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_void_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_selfclose_link", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_svg", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_nonvoid_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_unclosed", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_svg_then_body_canonical", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_base", "ok": false}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreignobject_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_head_breakout_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_mismatched_end_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_title_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_style_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_script_hidden_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "svg_title_text_clean", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "processing_instruction", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "missing_head", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_body_child", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_traversal", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_parent", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "fifo_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_symlink", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "manifest_dir_caller_prefix", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "empty_manifest", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "duplicate_pages", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_mode", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_unknown_flag", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_manifest_path", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_conflicting_modes", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_json_with_selftest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_abbreviated_manifest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_repeated_manifest", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "cli_help", "ok": true}], "passed": false}, "tool": "canonical_audit.py"}
```

<a id="output-r2"></a>

### R2 — relaxation

Exit: `1`. Stdout: `1554` bytes. SHA-256: `f01f467fc2bf66e134d1298ea6ec6b44c505ea2a6564f1c2d1f6c9bb52d8d267`. Stderr: exactly empty.

```json
{
 "validator": "/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py",
 "passed": false,
 "met": 9,
 "total": 11,
 "cases": [
  {
   "case": "body_base",
   "expect": "not clean",
   "exit": 0,
   "verdict": "clean",
   "ok": false
  },
  {
   "case": "body_base_selfclose",
   "expect": "not clean",
   "exit": 0,
   "verdict": "clean",
   "ok": false
  },
  {
   "case": "foreignobject_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_head_breakout_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_mismatched_end_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_title_hidden_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_style_hidden_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_script_hidden_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "math_annotation_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "control_body_svg",
   "expect": "clean",
   "exit": 0,
   "verdict": "clean",
   "ok": true
  },
  {
   "case": "control_void_selfclose",
   "expect": "clean",
   "exit": 0,
   "verdict": "clean",
   "ok": true
  }
 ]
}
```

<a id="output-s3"></a>

### S3 — selftest

Exit: `1`. Stdout: `11096` bytes. SHA-256: `35d097e04cca7aa06ae234413ed92ba9b35d7017b0b4a52914af8371d2807858`. Stderr: exactly empty.

```json
{"selftest": {"cases": [{"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "absolute_match", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "selfclosing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "title_text_decoy", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_same_dir", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_parent", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "root_relative", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "scheme_relative", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority_four", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "first_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "second_base_ignored", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "empty_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_token_list", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_uppercase", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "attr_uppercase", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "rel_non_ascii_separator", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "duplicate_attrs_first_wins", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "entity_href", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "query_preserved", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "empty_query_delimiter", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "relative_empty_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "missing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_same", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_different", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_absent", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_empty", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_ascii_whitespace", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "invalid_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "javascript_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "data_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "fragment_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "empty_fragment", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_host", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_query", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_invalid", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "comment_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "script_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "template_decoy", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "template_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "noscript_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreign_content", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_svg_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_math_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_void_selfclose", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_selfclose_link", "ok": false}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_svg", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_nonvoid_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_unclosed", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_svg_then_body_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreignobject_base", "ok": false}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_head_breakout_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_mismatched_end_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_title_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_style_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_script_hidden_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "svg_title_text_clean", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "processing_instruction", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "missing_head", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_body_child", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_traversal", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_parent", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "fifo_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_symlink", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "manifest_dir_caller_prefix", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "empty_manifest", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "duplicate_pages", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_mode", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_unknown_flag", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_manifest_path", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_conflicting_modes", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_json_with_selftest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_abbreviated_manifest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_repeated_manifest", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "cli_help", "ok": true}], "passed": false}, "tool": "canonical_audit.py"}
```

<a id="output-s4"></a>

### S4 — selftest

Exit: `1`. Stdout: `11068` bytes. SHA-256: `a1689e493e1f85ad2b9e2cb254c372400e5d8adc7f22f40ac42504b6e7ece55a`. Stderr: exactly empty.

```json
{"selftest": {"cases": [{"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "absolute_match", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "selfclosing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "title_text_decoy", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_same_dir", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_parent", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "root_relative", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "scheme_relative", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority_four", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "first_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "second_base_ignored", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "empty_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_token_list", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_uppercase", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "attr_uppercase", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "rel_non_ascii_separator", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "duplicate_attrs_first_wins", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "entity_href", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "query_preserved", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "empty_query_delimiter", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "relative_empty_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "missing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_same", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_different", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_absent", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_empty", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_ascii_whitespace", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "invalid_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "javascript_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "data_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "fragment_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "empty_fragment", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_host", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_query", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_invalid", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "comment_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "script_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "template_decoy", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "template_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "noscript_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreign_content", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_svg_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_math_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_void_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_selfclose_link", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_svg", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_nonvoid_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_unclosed", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_svg_then_body_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreignobject_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_head_breakout_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_mismatched_end_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_title_hidden_base", "ok": false}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_style_hidden_base", "ok": false}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_script_hidden_base", "ok": false}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "svg_title_text_clean", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "processing_instruction", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "missing_head", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_body_child", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_traversal", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_parent", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "fifo_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_symlink", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "manifest_dir_caller_prefix", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "empty_manifest", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "duplicate_pages", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_mode", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_unknown_flag", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_manifest_path", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_conflicting_modes", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_json_with_selftest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_abbreviated_manifest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_repeated_manifest", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "cli_help", "ok": true}], "passed": false}, "tool": "canonical_audit.py"}
```

<a id="output-r3"></a>

### R3 — relaxation

Exit: `1`. Stdout: `1542` bytes. SHA-256: `7207e9fdbe2d456a69e6f8148a40cb1851549ec36447c26a80d04083a30d3b12`. Stderr: exactly empty.

```json
{
 "validator": "/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py",
 "passed": false,
 "met": 8,
 "total": 11,
 "cases": [
  {
   "case": "body_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "body_base_selfclose",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "foreignobject_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_head_breakout_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_mismatched_end_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_title_hidden_base",
   "expect": "not clean",
   "exit": 0,
   "verdict": "clean",
   "ok": false
  },
  {
   "case": "svg_style_hidden_base",
   "expect": "not clean",
   "exit": 0,
   "verdict": "clean",
   "ok": false
  },
  {
   "case": "svg_script_hidden_base",
   "expect": "not clean",
   "exit": 0,
   "verdict": "clean",
   "ok": false
  },
  {
   "case": "math_annotation_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "control_body_svg",
   "expect": "clean",
   "exit": 0,
   "verdict": "clean",
   "ok": true
  },
  {
   "case": "control_void_selfclose",
   "expect": "clean",
   "exit": 0,
   "verdict": "clean",
   "ok": true
  }
 ]
}
```

<a id="output-s5"></a>

### S5 — selftest

Exit: `1`. Stdout: `11087` bytes. SHA-256: `9f872cc6d6142c346c4f741b87aa534006c4e97a212d42e196ab9be990aa6621`. Stderr: exactly empty.

```json
{"selftest": {"cases": [{"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "absolute_match", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "selfclosing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "title_text_decoy", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_same_dir", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_parent", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "root_relative", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "scheme_relative", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority_four", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "first_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "second_base_ignored", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "empty_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_token_list", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_uppercase", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "attr_uppercase", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "rel_non_ascii_separator", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "duplicate_attrs_first_wins", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "entity_href", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "query_preserved", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "empty_query_delimiter", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "relative_empty_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "missing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_same", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_different", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_absent", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_empty", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_ascii_whitespace", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_path", "ok": false}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_query", "ok": false}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "invalid_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "javascript_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "data_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "fragment_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "empty_fragment", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_host", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_query", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_invalid", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "comment_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "script_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "template_decoy", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "template_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "noscript_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreign_content", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_svg_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_math_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_void_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_selfclose_link", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_svg", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_nonvoid_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_unclosed", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_svg_then_body_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreignobject_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_head_breakout_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_mismatched_end_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_title_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_style_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_script_hidden_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "svg_title_text_clean", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "processing_instruction", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "missing_head", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_body_child", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_traversal", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_parent", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "fifo_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_symlink", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "manifest_dir_caller_prefix", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "empty_manifest", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "duplicate_pages", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_mode", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_unknown_flag", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_manifest_path", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_conflicting_modes", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_json_with_selftest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_abbreviated_manifest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_repeated_manifest", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "cli_help", "ok": true}], "passed": false}, "tool": "canonical_audit.py"}
```

<a id="output-s6"></a>

### S6 — selftest

Exit: `1`. Stdout: `11097` bytes. SHA-256: `566e201d71479980da197dbe39a277ad23d4cbea24cd2bb4559a4b5686039bd1`. Stderr: exactly empty.

```json
{"selftest": {"cases": [{"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "absolute_match", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "selfclosing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "title_text_decoy", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_same_dir", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_parent", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "root_relative", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "scheme_relative", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority_four", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "first_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "second_base_ignored", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "empty_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_token_list", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_uppercase", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "attr_uppercase", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "rel_non_ascii_separator", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "duplicate_attrs_first_wins", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "entity_href", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "query_preserved", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "empty_query_delimiter", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "relative_empty_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "missing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_same", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_different", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_absent", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_empty", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_ascii_whitespace", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "invalid_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "javascript_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "data_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "fragment_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "empty_fragment", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_host", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_query", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_invalid", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "comment_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "script_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "template_decoy", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "template_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "noscript_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreign_content", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_svg_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_math_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_void_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_selfclose_link", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_svg", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_nonvoid_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_unclosed", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_svg_then_body_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreignobject_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_head_breakout_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_mismatched_end_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_title_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_style_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_script_hidden_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "svg_title_text_clean", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "processing_instruction", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "missing_head", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_body_child", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_traversal", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_parent", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "fifo_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_symlink", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "manifest_dir_caller_prefix", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "empty_manifest", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "duplicate_pages", "ok": false}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_mode", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_unknown_flag", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_manifest_path", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_conflicting_modes", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_json_with_selftest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_abbreviated_manifest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_repeated_manifest", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "cli_help", "ok": true}], "passed": false}, "tool": "canonical_audit.py"}
```

<a id="output-s7"></a>

### S7 — selftest

Exit: `1`. Stdout: `11122` bytes. SHA-256: `42c5c137b67e6cd44ab11ce9ccbb3ab1ac19839060443c29e8f773812e36b61b`. Stderr: exactly empty.

```json
{"selftest": {"cases": [{"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "absolute_match", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "selfclosing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "title_text_decoy", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_same_dir", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "relative_parent", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "root_relative", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "scheme_relative", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "network_path_empty_authority_four", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "first_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "second_base_ignored", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "empty_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_token_list", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "rel_uppercase", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "attr_uppercase", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "rel_non_ascii_separator", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "duplicate_attrs_first_wins", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "entity_href", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "query_preserved", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "empty_query_delimiter", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "relative_empty_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "missing_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_same", "ok": true}, {"actual": {"exit": 1, "id": "canonical_multiple"}, "expected": {"exit": 1, "id": "canonical_multiple"}, "name": "duplicate_different", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_link", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_absent", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_empty", "ok": true}, {"actual": {"exit": 1, "id": "canonical_href_missing"}, "expected": {"exit": 1, "id": "canonical_href_missing"}, "name": "href_ascii_whitespace", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "href_c1_control_query", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "invalid_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "javascript_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_url_invalid"}, "expected": {"exit": 1, "id": "canonical_url_invalid"}, "name": "data_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "fragment_url", "ok": true}, {"actual": {"exit": 1, "id": "canonical_fragment"}, "expected": {"exit": 1, "id": "canonical_fragment"}, "name": "empty_fragment", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_host", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_path", "ok": true}, {"actual": {"exit": 1, "id": "canonical_mismatch"}, "expected": {"exit": 1, "id": "canonical_mismatch"}, "name": "wrong_query", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_invalid", "ok": true}, {"actual": {"exit": 1, "id": "base_url_invalid"}, "expected": {"exit": 1, "id": "base_url_invalid"}, "name": "base_empty_authority", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "comment_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "script_decoy", "ok": true}, {"actual": {"exit": 1, "id": "canonical_missing"}, "expected": {"exit": 1, "id": "canonical_missing"}, "name": "template_decoy", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "template_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "noscript_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreign_content", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_svg_after_head", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "body_math_after_head", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 0, "id": null}, "name": "body_void_selfclose", "ok": false}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_selfclose_link", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_svg", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_nonvoid_selfclose", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_svg_unclosed", "ok": true}, {"actual": {"exit": 1, "id": "canonical_outside_head"}, "expected": {"exit": 1, "id": "canonical_outside_head"}, "name": "body_svg_then_body_canonical", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "body_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "foreignobject_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_head_breakout_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_mismatched_end_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_title_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_style_hidden_base", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "svg_script_hidden_base", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "svg_title_text_clean", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "processing_instruction", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "missing_head", "ok": true}, {"actual": {"exit": 2, "id": "html_unsupported"}, "expected": {"exit": 2, "id": "html_unsupported"}, "name": "head_body_child", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_traversal", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "symlink_parent", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "fifo_html", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "manifest_symlink", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "manifest_dir_caller_prefix", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "empty_manifest", "ok": true}, {"actual": {"exit": 2, "id": "input_invalid"}, "expected": {"exit": 2, "id": "input_invalid"}, "name": "duplicate_pages", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_mode", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_unknown_flag", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_missing_manifest_path", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_conflicting_modes", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_json_with_selftest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_abbreviated_manifest", "ok": true}, {"actual": {"exit": 64, "id": "usage_json"}, "expected": {"exit": 64, "id": "usage_json"}, "name": "cli_repeated_manifest", "ok": true}, {"actual": {"exit": 0, "id": null}, "expected": {"exit": 0, "id": null}, "name": "cli_help", "ok": true}], "passed": false}, "tool": "canonical_audit.py"}
```

<a id="output-r4"></a>

### R4 — relaxation

Exit: `1`. Stdout: `1593` bytes. SHA-256: `a6e383135890f5ebc5d7c1a0caca7725b393e4a2e0bcb85dd2e5b32bb0bbb012`. Stderr: exactly empty.

```json
{
 "validator": "/tmp/kake-r23w2-MutateGuards-HBeu/clone/scripts/canonical_audit.py",
 "passed": false,
 "met": 10,
 "total": 11,
 "cases": [
  {
   "case": "body_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "body_base_selfclose",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "foreignobject_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_head_breakout_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_mismatched_end_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_title_hidden_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_style_hidden_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "svg_script_hidden_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "math_annotation_base",
   "expect": "not clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": true
  },
  {
   "case": "control_body_svg",
   "expect": "clean",
   "exit": 0,
   "verdict": "clean",
   "ok": true
  },
  {
   "case": "control_void_selfclose",
   "expect": "clean",
   "exit": 2,
   "verdict": "could-not-evaluate",
   "ok": false
  }
 ]
}
```

