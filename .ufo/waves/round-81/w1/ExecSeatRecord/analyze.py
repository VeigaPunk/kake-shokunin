#!/usr/bin/env python3
"""ExecSeatRecord scratch: independent analysis of recorder outputs and inputs."""
import hashlib
import json
import pathlib

S = pathlib.Path("/fast/scratch/hyaku/kake-r81/ExecSeatRecord")
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
IGNORED_CANDIDATES = {"status", "exit", "error", "exit_code", "error_text",
                      "status_code", "err", "failure", "ok", "success"}


def jload(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def record_facts(tag, path):
    r = jload(path)
    print(f"== {tag} record {path}")
    print("wave:", r.get("wave"), "| round:", r.get("round"))
    print("seats:", len(r.get("seats", {})))
    print("empty_output:", r.get("empty_output"))
    print("not_settled:", r.get("not_settled"))
    seat_keys = {k for e in r["seats"].values() for k in e}
    print("seat-entry keys:", sorted(seat_keys))
    print("schema_limit:", json.dumps(r.get("schema_limit")))
    return r


def results_facts(tag, path):
    p = pathlib.Path(path)
    if not p.is_file():
        print(f"== {tag} results {path}: ABSENT")
        return None
    d = jload(p)
    rows = d.get("results") or []
    print(f"== {tag} results {path}")
    print("top-level keys:", sorted(d.keys()))
    print("declared seats:", d.get("seats"), "| rows:", len(rows))
    shapes = {}
    union = set()
    for row in rows:
        ks = tuple(sorted(row.keys()))
        shapes[ks] = shapes.get(ks, 0) + 1
        union.update(row.keys())
    print("row key shapes:", {"[" + ",".join(k) + "]": v for k, v in shapes.items()})
    print("row key union:", sorted(union))
    print("ignored-candidate keys present:", sorted(union & IGNORED_CANDIDATES))
    return d


def spec_facts(tag, path):
    d = jload(path)
    items = [i for i in (d.get("items") or []) if isinstance(i, dict)]
    names = [i.get("name") for i in items]
    print(f"== {tag} spec {path}: items={len(items)} names={names}")
    return names


r80 = results_facts("r80", LANE / ".ufo/waves/round-80/w1-results.json")
s80 = spec_facts("r80", LANE / ".ufo/waves/round-80/w1-spec.json")
r79 = results_facts("r79", LANE / ".ufo/waves/round-79/w1-results.json")
s79 = spec_facts("r79", LANE / ".ufo/waves/round-79/w1-spec.json")
r81 = results_facts("r81", LANE / ".ufo/waves/round-81/w1-results.json")
if r81 is not None:
    spec_facts("r81", LANE / ".ufo/waves/round-81/w1-spec.json")

rec80 = record_facts("r80", S / "r80.json")
rec79 = record_facts("r79", S / "r79.json")

# ground truth cross-checks, computed here from raw bytes, not from the recorder
for tag, res, spec_names, rec in (("r80", r80, s80, rec80), ("r79", r79, s79, rec79)):
    if res is None:
        continue
    names = [row["name"] for row in res["results"] if isinstance(row, dict) and isinstance(row.get("name"), str)]
    empty = sorted(n for n, row in zip(names, res["results"]) if not (row.get("output") or "").encode("utf-8").strip())
    missing = sorted(set(spec_names) - set(names))
    print(f"-- {tag} ground truth: rows={len(names)} empty={empty} spec-minus-results={missing}")
    print(f"-- {tag} recorder agreement: empty_ok={rec['empty_output'] == empty} "
          f"not_settled_ok={rec['not_settled'] == missing} seats_ok={set(rec['seats']) == set(names)}")

# byte/digest re-derivation spot check for two r80 seats straight from the results bytes
for seat in ("ScoutSources", "ReviewC1"):
    row = next(r for r in r80["results"] if r["name"] == seat)
    raw = (row.get("output") or "").encode("utf-8")
    ent = rec80["seats"][seat]
    print(f"-- digest {seat}: bytes_ok={ent['output_bytes'] == len(raw)} "
          f"sha_ok={ent['output_sha256'] == hashlib.sha256(raw).hexdigest()} "
          f"status={ent['status']} role={ent['role']} exit={ent['exit']} error={ent['error']!r}")

# class-boundary case records
for key in ("a", "b", "c"):
    rec = jload(S / "cases" / f"{key}-record.json")
    print(f"-- case {key} statuses: " + ", ".join(f"{n}={e['status']}" for n, e in sorted(rec["seats"].items()))
          + f" | empty_output={rec['empty_output']}")

# determinism digests
for name in ("r80.json", "r80-again.json", "r80-reordered-record.json", "r79.json"):
    p = S / name
    if p.is_file():
        b = p.read_bytes()
        print(f"-- sha256 {name}: {hashlib.sha256(b).hexdigest()} ({len(b)} bytes)")
