#!/usr/bin/env python3
"""Build the round-84 frozen control pairs for the policy-value classifier.

Frozen at the round-84 freeze, before the tool `scripts/policy_value_class.py`
existed and before any seat ran. The pairs are synthetic by construction: each
side is a copy of the round-81 capture (`.ufo/waves/round-81/capture`) whose
retained bodies and digests are untouched; only the header list (and the
receipt's `headerCount`) is edited.

  capture-control/control/a     capture A + Referrer-Policy seeded on the sitemap
  capture-control/control/b     a + the three expected changes
  capture-control/equivalent/a  same as control/a
  capture-control/equivalent/b  a + the order-only rewrite only

Usage: python3 -B build_control_pairs.py --root <lane-tree>
Exit 0 written, 1 input fault, 64 usage.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

SOURCE_CAPTURE = Path(".ufo/waves/round-81/capture")
TARGET = Path(".ufo/waves/round-84/capture-control")
EXPECTATIONS = Path(".ufo/waves/round-84/policy-expectations.json")

SEED = {("ds4cc-sitemap"): ("referrer-policy", "no-referrer, strict-origin")}
CONTROL_B = [
    ("ds4cc-primary", "cache-control", "max-age=60"),
    ("ds4cc-robots", "x-frame-options", "SAMEORIGIN"),
    ("ds4cc-sitemap", "referrer-policy", "strict-origin, no-referrer"),
]
EQUIVALENT_B = [
    ("ds4cc-sitemap", "referrer-policy", "strict-origin, no-referrer"),
]


def receipt_path(tree: Path, surface: str) -> Path:
    return tree / surface / "response.json"


def set_header(tree: Path, surface: str, name: str, value: str) -> None:
    path = receipt_path(tree, surface)
    document = json.loads(path.read_text(encoding="utf-8"))
    headers = document["headers"]
    lowered = name.lower()
    for item in headers:
        if str(item.get("name", "")).strip().lower() == lowered:
            item["value"] = value
            break
    else:
        headers.append({"name": name, "value": value})
    document["headerCount"] = len(headers)
    path.write_text(json.dumps(document, indent=1), encoding="utf-8")


def build_side(tree: Path) -> None:
    for surface, (name, value) in SEED.items():
        set_header(tree, surface, name, value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", required=True, type=Path)
    args = parser.parse_args(argv)
    root: Path = args.root.resolve()
    source = root / SOURCE_CAPTURE
    if not source.is_dir():
        print(f"fault: no capture at {source}", file=sys.stderr)
        return 1
    target = root / TARGET
    if target.exists():
        shutil.rmtree(target)

    for pair in ("control", "equivalent"):
        a_tree = target / pair / "a"
        b_tree = target / pair / "b"
        shutil.copytree(source, a_tree)
        build_side(a_tree)
        shutil.copytree(a_tree, b_tree)

    for surface, name, value in CONTROL_B:
        set_header(target / "control" / "b", surface, name, value)
    for surface, name, value in EQUIVALENT_B:
        set_header(target / "equivalent" / "b", surface, name, value)

    expectations = {
        "_note": "Round-84 C2 frozen control expectations. The counter compares every changed "
                 "policy header in each pair against this table; a mismatch reopens the claim.",
        "surfaces": ["ds4cc-primary", "ds4cc-robots", "ds4cc-sitemap"],
        "control": {
            "ds4cc-primary": {"cache-control": "numeric_parameter"},
            "ds4cc-robots": {"x-frame-options": "header_added"},
            "ds4cc-sitemap": {"referrer-policy": "reordered"},
        },
        "equivalent": {
            "ds4cc-sitemap": {"referrer-policy": "reordered"},
        },
        "verdicts": {"control": "policy-changed", "equivalent": "policy-rewritten-equivalent"},
    }
    (root / EXPECTATIONS).write_text(json.dumps(expectations, indent=1) + "\n", encoding="utf-8")

    surfaces = 0
    for pair in ("control", "equivalent"):
        for side in ("a", "b"):
            surfaces += sum(1 for item in (target / pair / side).iterdir() if item.is_dir())
    print(f"built pair=control surfaces=3 built_pair=equivalent surfaces=3 receipts={surfaces}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
