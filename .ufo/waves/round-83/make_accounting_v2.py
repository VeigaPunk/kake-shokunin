#!/usr/bin/env python3
"""Round-83 wave accounting v2 — spec/results populations, per-seat UTF-8 bytes, attack share.

    make_accounting_v2.py --spec <w1-spec.json> --results <w1-results.json> \
                          --out <w1-accounting.json>
    make_accounting_v2.py --selftest [--work <dir>]

v2 supersedes round-82's `make_accounting.py` (`kake-wave-accounting/v1`). Every v1 key is
re-derived by the same rules, so a v1 consumer keeps reading the same numbers; v2 adds:

  * `supersedes` — the format id v2 extends.
  * `bytes_basis` — always `"utf-8"`: an output's size is `len(output.encode("utf-8"))`, never
    `len(output)` (code points). A 150-character row of two-byte characters is 300 bytes.
  * `seats` — one row per results row: `name`, `role` (from the spec item), `output_bytes`.
  * `rows_skipped` — results rows dropped before derivation (not an object, or no string name);
    a clean results file reads 0.

`settled_names` is sorted in v2 (v1 kept results order) so two derivations of the same population
compare equal without a shared ordering convention. `substantive_names` keeps results order, as in
v1, so that key reproduces byte-for-byte.

A seat is `settled` when its output is non-empty. It is `substantive` when it carries at least
`SUBSTANTIVE_BYTES` (200) bytes of output — a progress line is not a deliverable. Attack roles are
the run-15 directive's {reviewer, critic, mutation-tester, labrat}; a row whose name is absent from
the spec counts as role `""` (non-attack), exactly as the round-83 C1 counter derives it.

Writes nothing but `--out`. Exit 0 written, 2 bad input, 64 usage. `--selftest` builds its
fixtures under `--work` (else `tempfile.mkdtemp`, which honours `TMPDIR`), removes the directory it
created, prints `selftest: N/N passed`, and exits 0 iff every check passes.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable, Iterable

SCHEMA = "kake-wave-accounting/v2"
SUPERSEDES = "kake-wave-accounting/v1"
ATTACK_ROLES = ("reviewer", "critic", "mutation-tester", "labrat")
SUBSTANTIVE_BYTES = 200
BYTES_BASIS = "utf-8"


def digest(path: str | os.PathLike[str]) -> str:
    with open(path, "rb") as stream:
        return hashlib.sha256(stream.read()).hexdigest()


def utf8_len(output: object) -> int:
    """Byte length of an output under UTF-8; anything that is not a string is 0 bytes."""
    return len(output.encode("utf-8")) if isinstance(output, str) else 0


def load(path: str) -> Any:
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)


def build_record(spec: Any, results: Any, spec_sha256: str, results_sha256: str
                 ) -> tuple[dict[str, Any] | None, str]:
    """Derive the accounting record; `(record, "")` or `(None, reason)`."""
    if not isinstance(spec, dict) or not isinstance(results, dict):
        return None, "spec and results must be JSON objects"
    items = spec.get("items")
    rows = results.get("results")
    if not isinstance(items, list):
        return None, "spec.items is not a list"
    if not isinstance(rows, list):
        return None, "results.results is not a list"
    roles: dict[str, str] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            return None, f"spec.items[{index}] is not an object"
        name, role = item.get("name"), item.get("role")
        if not isinstance(name, str) or not isinstance(role, str):
            return None, f"spec.items[{index}] lacks a string name/role"
        roles[name] = role
    settled: list[str] = []
    substantive: list[str] = []
    seats: list[dict[str, Any]] = []
    skipped = 0
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not isinstance(row.get("name"), str):
            skipped += 1
            continue
        name = row["name"]
        output = row.get("output") or ""
        if not isinstance(output, str):
            return None, f"results.results[{index}] output is not a string"
        try:
            size = utf8_len(output)
        except UnicodeEncodeError as exc:
            return None, f"results.results[{index}] output is not UTF-8 encodable: {exc}"
        seats.append({"name": name, "role": roles.get(name, ""), "output_bytes": size})
        if size > 0:
            settled.append(name)
        if size >= SUBSTANTIVE_BYTES:
            substantive.append(name)
    settled_attack = [name for name in settled if roles.get(name) in ATTACK_ROLES]
    substantive_attack = [name for name in substantive if roles.get(name) in ATTACK_ROLES]
    requested = len(items)
    requested_attack = sum(1 for item in items if item["role"] in ATTACK_ROLES)
    record: dict[str, Any] = {
        "schema": SCHEMA,
        "supersedes": SUPERSEDES,
        "lane": results.get("lane", "kake"),
        "round": results.get("round"),
        "wave": results.get("wave"),
        "attack_roles": list(ATTACK_ROLES),
        "substantive_floor_bytes": SUBSTANTIVE_BYTES,
        "bytes_basis": BYTES_BASIS,
        "requested": requested,
        "requested_attack": requested_attack,
        "requested_share": round(requested_attack / requested, 4) if requested else 0.0,
        "settled": len(settled),
        "settled_names": sorted(settled),
        "settled_attack": len(settled_attack),
        "settled_share": round(len(settled_attack) / len(settled), 4) if settled else 0.0,
        "substantive": len(substantive),
        "substantive_names": substantive,
        "substantive_attack": len(substantive_attack),
        "substantive_share": (round(len(substantive_attack) / len(substantive), 4)
                              if substantive else 0.0),
        "empty_output": sorted(set(roles) - set(settled)),
        "seats": seats,
        "rows_skipped": skipped,
        "spec_sha256": spec_sha256,
        "results_sha256": results_sha256,
    }
    return record, ""


def _invoke(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = main(argv)
    return code, out.getvalue(), err.getvalue()


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _run_fixture(base: Path, slug: str, spec: Any, results: Any, *,
                 raw_results: str | None = None, write_results: bool = True
                 ) -> tuple[Path, Path, Path, dict[str, Any] | None, int, str]:
    root = base / slug
    root.mkdir()
    spec_path = root / "spec.json"
    results_path = root / "results.json"
    out_path = root / "accounting.json"
    _write_json(spec_path, spec)
    if raw_results is not None:
        results_path.write_text(raw_results, encoding="utf-8")
    elif write_results:
        _write_json(results_path, results)
    code, _stdout, stderr = _invoke(["--spec", str(spec_path), "--results", str(results_path),
                                     "--out", str(out_path)])
    record = None
    if out_path.is_file():
        try:
            record = json.loads(out_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            record = None
    return spec_path, results_path, out_path, record, code, stderr


def _spec(*items: tuple[str, str]) -> dict[str, Any]:
    return {"wave": "w1", "items": [{"name": name, "role": role} for name, role in items]}


def _results(*rows: tuple[str, str]) -> dict[str, Any]:
    return {"lane": "kake", "round": 83, "wave": "w1",
            "results": [{"name": name, "output": output} for name, output in rows]}


def _check_empty_row(base: Path) -> tuple[bool, str]:
    _, _, _, record, code, stderr = _run_fixture(
        base, "empty-row", _spec(("Alfa", "executor"), ("Bravo", "scribe")),
        _results(("Alfa", ""), ("Bravo", "x" * 300)))
    if code != 0 or record is None:
        return False, f"exit={code} stderr={stderr.strip()[:120]}"
    seats = {row["name"]: row["output_bytes"] for row in record.get("seats", [])}
    ok = (record.get("settled") == 1 and record.get("settled_names") == ["Bravo"]
          and record.get("settled_share") == 0.0 and seats.get("Alfa") == 0
          and seats.get("Bravo") == 300)
    return ok, f"settled={record.get('settled')} names={record.get('settled_names')} seats={seats}"


def _check_floor_199(base: Path) -> tuple[bool, str]:
    _, _, _, record, code, stderr = _run_fixture(
        base, "floor-199", _spec(("Alfa", "executor")), _results(("Alfa", "x" * 199)))
    if code != 0 or record is None:
        return False, f"exit={code} stderr={stderr.strip()[:120]}"
    ok = (record.get("settled") == 1 and record.get("substantive") == 0
          and record.get("seats") == [{"name": "Alfa", "role": "executor",
                                       "output_bytes": 199}])
    return ok, f"settled={record.get('settled')} substantive={record.get('substantive')}"


def _check_floor_200(base: Path) -> tuple[bool, str]:
    _, _, _, record, code, stderr = _run_fixture(
        base, "floor-200", _spec(("Alfa", "executor")), _results(("Alfa", "x" * 200)))
    if code != 0 or record is None:
        return False, f"exit={code} stderr={stderr.strip()[:120]}"
    ok = (record.get("settled") == 1 and record.get("substantive") == 1
          and record["seats"][0]["output_bytes"] == 200)
    return ok, f"substantive={record.get('substantive')}"


def _check_utf8_bytes(base: Path) -> tuple[bool, str]:
    output = "\u00e9" * 150  # 150 code points, 300 UTF-8 bytes
    _, _, _, record, code, stderr = _run_fixture(
        base, "utf8-bytes", _spec(("Alfa", "critic")), _results(("Alfa", output)))
    if code != 0 or record is None:
        return False, f"exit={code} stderr={stderr.strip()[:120]}"
    size = record["seats"][0]["output_bytes"]
    ok = (len(output) == 150 and size == 300 and size != len(output)
          and record.get("settled_attack") == 1 and record.get("substantive") == 1)
    return ok, f"chars={len(output)} output_bytes={size} settled_attack={record.get('settled_attack')}"


def _check_attack_share(base: Path) -> tuple[bool, str]:
    _, _, _, record, code, stderr = _run_fixture(
        base, "attack-share",
        _spec(("Rev", "reviewer"), ("Cri", "critic"), ("Exec", "executor"), ("Scribe", "scribe")),
        _results(("Rev", "x" * 300), ("Cri", ""), ("Exec", "x" * 300), ("Scribe", "x" * 300)))
    if code != 0 or record is None:
        return False, f"exit={code} stderr={stderr.strip()[:120]}"
    ok = (record.get("requested") == 4 and record.get("requested_attack") == 2
          and record.get("requested_share") == 0.5 and record.get("settled") == 3
          and record.get("settled_attack") == 1 and record.get("settled_share") == 0.3333)
    return ok, (f"requested={record.get('requested')}/{record.get('requested_attack')} "
                f"settled={record.get('settled')}/{record.get('settled_attack')} "
                f"share={record.get('settled_share')}")


def _check_sorted_names(base: Path) -> tuple[bool, str]:
    _, _, _, record, code, stderr = _run_fixture(
        base, "sorted-names",
        _spec(("Zulu", "scribe"), ("Mike", "scribe"), ("Alfa", "scribe")),
        _results(("Zulu", "x" * 300), ("Mike", "x" * 300), ("Alfa", "x" * 300)))
    if code != 0 or record is None:
        return False, f"exit={code} stderr={stderr.strip()[:120]}"
    names = record.get("settled_names")
    ok = names == ["Alfa", "Mike", "Zulu"] and names != ["Zulu", "Mike", "Alfa"]
    return ok, f"settled_names={names}"


def _check_seats_shape(base: Path) -> tuple[bool, str]:
    _, _, _, record, code, stderr = _run_fixture(
        base, "seats-shape",
        _spec(("Alfa", "reviewer"), ("Bravo", "executor"), ("Charlie", "critic")),
        _results(("Alfa", "x" * 300), ("Bravo", ""), ("Charlie", "x" * 250)))
    if code != 0 or record is None:
        return False, f"exit={code} stderr={stderr.strip()[:120]}"
    seats = record.get("seats", [])
    rows_ok = (len(seats) == 3
               and all(set(row) == {"name", "role", "output_bytes"} for row in seats)
               and [(row["name"], row["role"]) for row in seats]
               == [("Alfa", "reviewer"), ("Bravo", "executor"), ("Charlie", "critic")])
    ok = (rows_ok and record.get("bytes_basis") == "utf-8" and record.get("schema") == SCHEMA
          and record.get("rows_skipped") == 0
          and record.get("spec_sha256") and record.get("results_sha256"))
    return ok, f"seats={len(seats)} bytes_basis={record.get('bytes_basis')!r}"


def _check_missing_results(base: Path) -> tuple[bool, str]:
    _, results_path, out_path, record, code, stderr = _run_fixture(
        base, "missing-results", _spec(("Alfa", "executor")), None, write_results=False)
    ok = code == 2 and record is None and not out_path.exists() and "error:" in stderr
    return ok, f"exit={code} out_written={out_path.exists()} stderr={stderr.strip()[:120]}"


def _check_malformed_results(base: Path) -> tuple[bool, str]:
    _, _, out_path, record, code, stderr = _run_fixture(
        base, "malformed-results", _spec(("Alfa", "executor")), None, raw_results="{not json")
    ok = code == 2 and record is None and not out_path.exists() and "error:" in stderr
    return ok, f"exit={code} out_written={out_path.exists()}"


def _check_writes_only_out(base: Path) -> tuple[bool, str]:
    spec_path, results_path, out_path, record, code, _stderr = _run_fixture(
        base, "writes-only-out", _spec(("Alfa", "executor")), _results(("Alfa", "x" * 300)))
    listing = sorted(path.name for path in out_path.parent.iterdir())
    ok = (code == 0 and record is not None
          and listing == ["accounting.json", "results.json", "spec.json"])
    return ok, f"listing={listing}"


def _check_deterministic(base: Path) -> tuple[bool, str]:
    root = base / "deterministic"
    root.mkdir()
    spec_path = root / "spec.json"
    results_path = root / "results.json"
    _write_json(spec_path, _spec(("Alfa", "reviewer"), ("Bravo", "executor")))
    _write_json(results_path, _results(("Alfa", "x" * 300), ("Bravo", "y" * 199)))
    first, second = root / "a.json", root / "b.json"
    code_a, _, _ = _invoke(["--spec", str(spec_path), "--results", str(results_path),
                            "--out", str(first)])
    code_b, _, _ = _invoke(["--spec", str(spec_path), "--results", str(results_path),
                            "--out", str(second)])
    ok = (code_a == 0 and code_b == 0 and first.read_bytes() == second.read_bytes())
    return ok, f"exit={code_a}/{code_b} identical={first.read_bytes() == second.read_bytes()}"


def _check_usage_exit_64(base: Path) -> tuple[bool, str]:
    code, _stdout, stderr = _invoke(["--spec", "only-a-spec.json"])
    ok = code == 64 and "required" in stderr
    return ok, f"exit={code} stderr={stderr.strip()[:120]}"


def _check_help_exit_0(base: Path) -> tuple[bool, str]:
    code, stdout, _stderr = _invoke(["--help"])
    ok = code == 0 and "make_accounting_v2" in stdout
    return ok, f"exit={code}"


CHECKS: tuple[tuple[str, Callable[[Path], tuple[bool, str]]], ...] = (
    ("empty-row-unsettled", _check_empty_row),
    ("floor-199-settled-not-substantive", _check_floor_199),
    ("floor-200-substantive", _check_floor_200),
    ("non-ascii-counts-utf8-bytes", _check_utf8_bytes),
    ("attack-share-arithmetic", _check_attack_share),
    ("settled-names-sorted", _check_sorted_names),
    ("seats-one-per-row", _check_seats_shape),
    ("missing-results-exit-2", _check_missing_results),
    ("malformed-results-exit-2", _check_malformed_results),
    ("writes-only-out", _check_writes_only_out),
    ("deterministic-bytes", _check_deterministic),
    ("usage-exit-64", _check_usage_exit_64),
    ("help-exit-0", _check_help_exit_0),
)


def selftest(work: str | None) -> int:
    parent = None
    if work:
        parent = Path(work).expanduser()
        parent.mkdir(parents=True, exist_ok=True)
    root = Path(tempfile.mkdtemp(prefix="c83-accounting-selftest-",
                                 dir=None if parent is None else str(parent)))
    passed = 0
    try:
        for name, check in CHECKS:
            try:
                ok, detail = check(root)
            except Exception as exc:  # a crashing check is a failing check, never a pass
                ok, detail = False, f"raised {type(exc).__name__}: {exc}"
            print(f"{'ok  ' if ok else 'FAIL'} {name}" + (f"  [{detail}]" if detail else ""))
            passed += 1 if ok else 0
        print(f"selftest: {passed}/{len(CHECKS)} passed")
        return 0 if passed == len(CHECKS) else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="make_accounting_v2.py",
        description="kake wave accounting v2 (UTF-8 per-seat bytes).")
    parser.add_argument("--spec")
    parser.add_argument("--results")
    parser.add_argument("--out")
    parser.add_argument("--work", help="fixture base for --selftest (default: TMPDIR)")
    parser.add_argument("--selftest", action="store_true",
                        help="build synthetic fixtures, assert the rulings, exit 0 iff all pass")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    if args.selftest:
        return selftest(args.work)
    missing = [flag for flag, value in (("--spec", args.spec), ("--results", args.results),
                                        ("--out", args.out)) if not value]
    if missing:
        print(f"error: {', '.join(missing)} required (or --selftest)", file=sys.stderr)
        return 64
    try:
        spec = load(args.spec)
        results = load(args.results)
        spec_sha256 = digest(args.spec)
        results_sha256 = digest(args.results)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    record, error = build_record(spec, results, spec_sha256, results_sha256)
    if record is None:
        print(f"error: {error}", file=sys.stderr)
        return 2
    try:
        with open(args.out, "w", encoding="utf-8") as stream:
            json.dump(record, stream, indent=1)
            stream.write("\n")
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    settled_bytes = sum(row["output_bytes"] for row in record["seats"] if row["output_bytes"])
    print(f"requested={record['requested']} requested_attack={record['requested_attack']} "
          f"requested_share={record['requested_share']}")
    print(f"settled={record['settled']} settled_attack={record['settled_attack']} "
          f"settled_share={record['settled_share']} settled_bytes={settled_bytes}")
    print(f"substantive={record['substantive']} substantive_attack={record['substantive_attack']} "
          f"substantive_share={record['substantive_share']}")
    print(f"empty_output={','.join(record['empty_output']) or '-'}")
    print(f"bytes_basis={record['bytes_basis']} seats={len(record['seats'])} "
          f"rows_skipped={record['rows_skipped']} out={args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
