#!/usr/bin/env python3
"""Write `.ufo/waves/round-81/w1-accounting.json` from the frozen spec and the settled wave.

R80-4's condition (contract §C1) is decided from this record by
`c81_defect_queue.py`: the record must re-derive `attack_roles`, the requested and
settled totals, the attack share and the spec's sha256. A seat whose output is
empty did not do attack work, so it is *not* settled for this count — that is the
round-80 defect this record exists to stop repeating.

    python3 -B .ufo/waves/round-81/make_accounting.py [--root <lane>]
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ATTACK_ROLES = ["reviewer", "critic", "mutation-tester", "labrat"]
WAVE = Path(".ufo/waves/round-81")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    spec_path = root / WAVE / "w1-spec.json"
    results_path = root / WAVE / "w1-results.json"
    spec_bytes = spec_path.read_bytes()
    spec = json.loads(spec_bytes.decode("utf-8"))
    results = json.loads(results_path.read_text(encoding="utf-8"))
    items = spec.get("items") or []
    roles = {i["name"]: i.get("role") for i in items}
    requested_attack = sum(1 for r in roles.values() if r in ATTACK_ROLES)
    settled = [r for r in (results.get("results") or [])
               if isinstance(r, dict) and isinstance(r.get("name"), str)
               and (r.get("output") or "").strip()]
    settled_attack = sum(1 for r in settled if roles.get(r["name"]) in ATTACK_ROLES)
    total = len(settled)
    share = settled_attack / total if total else 0.0
    record = {
        "wave": "w1",
        "round": 81,
        "attack_roles": ATTACK_ROLES,
        "attack_role_source": ("run-15 addendum role list; sentinel is not an attack role "
                              "(round-80 closure R80-4)"),
        "requested_total": len(items),
        "requested_attack": requested_attack,
        "settled_total": total,
        "settled_attack": settled_attack,
        "share": share,
        "settled_definition": "a results row with non-empty output; empty-output seats are not settled",
        "settled_names": sorted(r["name"] for r in settled),
        "empty_output": sorted(r["name"] for r in (results.get("results") or [])
                              if isinstance(r, dict) and not (r.get("output") or "").strip()),
        "spec_sha256": hashlib.sha256(spec_bytes).hexdigest(),
        "floor": 0.25,
        "met": share >= 0.25,
    }
    out = root / WAVE / "w1-accounting.json"
    out.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"requested {requested_attack}/{len(items)} settled {settled_attack}/{total} "
          f"share={share:.3f} met={'true' if record['met'] else 'false'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
