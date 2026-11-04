#!/usr/bin/env python3
"""ExecSeatRecord scratch: build the three class-boundary fixture results files."""
import json
import pathlib

S = pathlib.Path("/fast/scratch/hyaku/kake-r81/ExecSeatRecord")
cases = S / "cases"
cases.mkdir(parents=True, exist_ok=True)

spec = {"wave": "kake-r81-w1", "items": [
    {"name": "SeatA", "role": "scout", "item": "x"},
    {"name": "SeatB", "role": "executor", "item": "x"},
    {"name": "SeatC", "role": "critic", "item": "x"},
]}
(cases / "spec.json").write_text(json.dumps(spec, indent=1) + "\n", encoding="utf-8")

base_rows = [
    {"name": "SeatA", "agent": "scout", "output": "x"},
    {"name": "SeatB", "agent": "executor", "output": "x"},
    {"name": "SeatC", "agent": "critic", "output": "x"},
]
variants = {
    "a": [dict(r) for r in base_rows],
    "b": [dict(r) for r in base_rows[:2]] + [{"name": "SeatC", "agent": "critic", "output": ""}],
    "c": [dict(r) for r in base_rows[:2]] + [{"name": "SeatC", "agent": "critic", "output": "   \n"}],
}
for key, rows in variants.items():
    doc = {"lane": "kake", "round": 81, "wave": "w1", "results": rows}
    (cases / f"{key}-results.json").write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
print("cases written:", sorted(p.name for p in cases.iterdir()))
