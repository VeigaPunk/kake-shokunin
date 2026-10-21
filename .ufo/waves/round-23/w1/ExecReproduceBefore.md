## Verdict

PASS for the scoped reproduction: the script was written in the isolated clone at `/tmp/kake-r23-ExecReproduceBefore-7hK2/clone/.ufo/waves/round-23/routed/reproduce-r22-before.sh` (observed clone HEAD `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`). It reconstructed both runners from `c0fd6d5`, ran both named probes, and matched their committed before-fix verdicts. This is reproduction evidence only, not independent admission or a claim that round-23 C1/C2 passed.

## Findings

### P3 — Historical before-fix verdicts reproduced (operability)

- Exact command: `/tmp/kake-r23-ExecReproduceBefore-7hK2/clone/.ufo/waves/round-23/routed/reproduce-r22-before.sh`
- Exact observed output:

```json
{
  "all_matched": true,
  "counter_probe": {
    "actual_passed": false,
    "actual_rejected": {
      "CE1_stub_matrix": false,
      "CE2_unvalidated_baseline": false,
      "CE3_self_consistent_stub": false
    },
    "expected_passed": false,
    "expected_rejected": {
      "CE1_stub_matrix": false,
      "CE2_unvalidated_baseline": false,
      "CE3_self_consistent_stub": false
    },
    "matched": true,
    "process_exit": 1
  },
  "defect_probe": {
    "actual": {
      "met": 2,
      "passed": false,
      "total": 8
    },
    "expected": {
      "met": 2,
      "passed": false,
      "total": 8
    },
    "matched": true,
    "process_exit": 1
  },
  "source_revision": "c0fd6d5"
}
```

- Impacted claim/axis: operability; confirms the historical before-fix probe results are reproducible from the named Git revision.
- Smallest fix: none; all requested compared values match the committed receipts.

## Checked and held

- Clone: `/tmp/kake-r23-ExecReproduceBefore-7hK2/clone`; observed HEAD `4e7dd1d4e52dcbdce249dd3dbc8485bc4e23cf4b`.
- Script: `/tmp/kake-r23-ExecReproduceBefore-7hK2/clone/.ufo/waves/round-23/routed/reproduce-r22-before.sh`.
- Recreated source SHA-256 values: `canonical_audit.py` = `35433e5077af77efa843014b00901b16878b334bb85ab73b4412aa8b705918e7`; `measure.py` = `329f45b67b3610c5ac132ef53f3428ad8dc9c2dd065ec0a96834a08b71ab9c49`.
- Script, inline:

```bash
#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
repo_root="$(git -C "$script_dir" rev-parse --show-toplevel)"
tmp="$(mktemp -d /tmp/kake-r23-ExecReproduceBefore-XXXXXX)"
trap 'rm -rf -- "$tmp"' EXIT

git -C "$repo_root" show c0fd6d5:scripts/canonical_audit.py > "$tmp/canonical_audit_c0fd6d5.py"
git -C "$repo_root" show c0fd6d5:.ufo/waves/round-22/measure.py > "$tmp/measure_c0fd6d5.py"

set +e
python3 -B "$repo_root/.ufo/waves/round-22/postfix/defect-probe.py" \
  --validator "$tmp/canonical_audit_c0fd6d5.py" > "$tmp/defect-actual.json"
defect_exit=$?
python3 -B "$repo_root/.ufo/waves/round-22/postfix/counter-probe.py" \
  --lane "$repo_root" --measure "$tmp/measure_c0fd6d5.py" > "$tmp/counter-actual.json"
counter_exit=$?
set -e

python3 - "$repo_root" "$tmp/defect-actual.json" "$tmp/counter-actual.json" \
  "$defect_exit" "$counter_exit" <<'PY'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
defect = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
counter = json.loads(pathlib.Path(sys.argv[3]).read_text(encoding="utf-8"))
defect_exit, counter_exit = map(int, sys.argv[4:6])
postfix = root / ".ufo/waves/round-22/postfix"
defect_before = json.loads((postfix / "defect-probe-before.json").read_text(encoding="utf-8"))
counter_before = json.loads((postfix / "counter-probe-before.json").read_text(encoding="utf-8"))

expected_defect = {key: defect_before[key] for key in ("met", "total", "passed")}
actual_defect = {key: defect[key] for key in ("met", "total", "passed")}
defect_match = actual_defect == expected_defect and defect_exit == 1

expected_rejected = {
    key: counter_before[key]["rejected"]
    for key in ("CE1_stub_matrix", "CE2_unvalidated_baseline", "CE3_self_consistent_stub")
}
actual_rejected = {
    key: counter[key]["rejected"]
    for key in expected_rejected
}
counter_match = (
    actual_rejected == expected_rejected
    and counter["passed"] == counter_before["passed"]
    and counter_exit == 1
)

print(json.dumps({
    "source_revision": "c0fd6d5",
    "defect_probe": {
        "expected": expected_defect,
        "actual": actual_defect,
        "process_exit": defect_exit,
        "matched": defect_match,
    },
    "counter_probe": {
        "expected_rejected": expected_rejected,
        "actual_rejected": actual_rejected,
        "expected_passed": counter_before["passed"],
        "actual_passed": counter["passed"],
        "process_exit": counter_exit,
        "matched": counter_match,
    },
    "all_matched": defect_match and counter_match,
}, ensure_ascii=False, indent=2, sort_keys=True))

if not (defect_match and counter_match):
    raise SystemExit(1)
PY
```

- Only the requested targeted reproduction and runner digest commands were run. No dependencies were installed. No production files in the lane were edited; this report is the only lane file written.

## Limits

This confirms the historical baseline is reproducible from `c0fd6d5` and agrees with the committed `-before.json` fields: defect probe `met=2/8`, and CE1–CE3 `rejected=false`. It does not verify any round-23 live surface, build/lint/test the project, or claim integration/admission. The reproduction script remains in the `/tmp` clone; its complete source is included above for integration.