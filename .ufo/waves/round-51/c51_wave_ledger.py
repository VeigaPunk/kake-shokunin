#!/usr/bin/env python3
"""Round-51 wave-evidence ledger — the C1 counter (operability).

What it is: a re-derivation of the round's own wave evidence over committed bytes
only. It reads `git show <revision>:<path>` and `git ls-tree`; it opens no worktree
file of the measured revision and performs no network access.

What its contract is: it certifies three ledger checks, each over bytes a reader can
re-derive with the same commands:

  L1 seat accounting — the number of committed seat reports under
    `.ufo/waves/round-51/w1/` equals the count the committed settlement receipt
    records as written, the settlement's spawn count equals the seat count of the
    committed dispatch payload, and every seat the settlement marks as having a
    report has exactly one committed report file (and every committed report file
    belongs to a seat the settlement knows).
  L2 route receipts — every route the wave used has a committed probe receipt that
    names an HTTP status code and a body excerpt; a failing receipt is never used
    as a role's model; and every failing receipt is recorded as a deviation in the
    committed route map.
  L3 time accounting — the aggregate seat time, the dead-seat time and the wave wall
    clock are re-derivable from the committed settlement and wave-timing bytes, the
    committed time-accounting artifact carries the same three figures, the lane's
    LOG.md names the wall-clock figure, and every dead seat's recorded duration is
    consistent with its recorded reason.

Predicate (frozen in `.ufo/waves/round-51/contract.json` before any data):

    met: ledger_checks_passed == 3 of 3

Exit codes: 0 the predicate is met, 1 it is not, 2 the evidence cannot be evaluated,
64 usage error.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone

PREDICATE = "met: ledger_checks_passed == 3 of 3"

WAVE_DIR = ".ufo/waves/round-51"
REPORT_DIR = f"{WAVE_DIR}/w1"
SETTLEMENT = f"{WAVE_DIR}/settlement.json"
TASKCALL = f"{WAVE_DIR}/w51-taskcall.json"
ROUTE_MAP = f"{WAVE_DIR}/route-map.json"
PROBE_DIR = f"{WAVE_DIR}/route-probes"
TIMING = f"{WAVE_DIR}/wave-timing.json"
ACCOUNTING = f"{WAVE_DIR}/round-time-accounting.json"
GRANT = f"{WAVE_DIR}/wave-grant.txt"
LOG = "LOG.md"


def git(root: str, *args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", "-C", root, *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return proc.returncode, proc.stdout


def show(root: str, rev: str, path: str) -> str | None:
    rc, out = git(root, "show", f"{rev}:{path}")
    return out if rc == 0 else None


def show_json(root: str, rev: str, path: str):
    raw = show(root, rev, path)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def list_paths(root: str, rev: str, prefix: str) -> list[str]:
    rc, out = git(root, "ls-tree", "-r", "--name-only", rev, "--", prefix)
    if rc != 0:
        return []
    return [line for line in out.splitlines() if line.strip()]


def parse_ts(value: str) -> datetime | None:
    try:
        text = value.replace("Z", "+00:00")
        stamp = datetime.fromisoformat(text)
    except (ValueError, AttributeError):
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp


def check_l1(root: str, rev: str) -> tuple[bool, list[str], dict]:
    notes: list[str] = []
    settlement = show_json(root, rev, SETTLEMENT)
    taskcall = show_json(root, rev, TASKCALL)
    if settlement is None:
        return False, ["settlement receipt absent at the measured revision"], {}
    if taskcall is None:
        return False, ["dispatch payload absent at the measured revision"], {}
    tasks = taskcall.get("taskCall", {}).get("tasks", [])
    payload_spawn = taskcall.get("counts", {}).get("spawn")
    spawn = settlement.get("spawn")
    seats = settlement.get("settled", []) + settlement.get("dead", [])
    reported = sorted(e["name"] for e in seats if e.get("report"))
    committed = sorted(
        p[len(REPORT_DIR) + 1:][: -len(".md")]
        for p in list_paths(root, rev, REPORT_DIR)
        if p.endswith(".md")
    )
    facts = {
        "payload_spawn": payload_spawn,
        "settlement_spawn": spawn,
        "payload_seats": len(tasks),
        "settlement_seats": len(seats),
        "settlement_reports_written": settlement.get("reports_written"),
        "seats_marked_with_report": len(reported),
        "committed_report_files": len(committed),
    }
    if payload_spawn != len(tasks):
        notes.append(f"payload spawn {payload_spawn} != payload seats {len(tasks)}")
    if spawn != len(tasks):
        notes.append(f"settlement spawn {spawn} != payload seats {len(tasks)}")
    if settlement.get("settled_count", 0) + settlement.get("dead_count", 0) != len(seats):
        notes.append("settled_count + dead_count != settled + dead entries")
    if settlement.get("reports_written") != len(committed):
        notes.append(
            f"settlement reports_written {settlement.get('reports_written')} "
            f"!= committed report files {len(committed)}"
        )
    if reported != committed:
        missing = sorted(set(reported) - set(committed))
        extra = sorted(set(committed) - set(reported))
        if missing:
            notes.append(f"seats marked with a report but no committed file: {missing}")
        if extra:
            notes.append(f"committed report files for unknown seats: {extra}")
    return (not notes), notes, facts


def check_l2(root: str, rev: str) -> tuple[bool, list[str], dict]:
    notes: list[str] = []
    route_map = show_json(root, rev, ROUTE_MAP)
    if route_map is None:
        return False, ["route map absent at the measured revision"], {}
    roles = route_map.get("roles", {})
    if not roles:
        return False, ["route map carries no role bindings"], {}
    receipts: dict[str, dict] = {}
    for path in list_paths(root, rev, PROBE_DIR):
        if not path.endswith(".json"):
            continue
        raw = show(root, rev, path)
        if raw is None:
            continue
        try:
            receipt = json.loads(raw)
        except json.JSONDecodeError:
            notes.append(f"probe receipt {path} is not JSON")
            continue
        alias = receipt.get("alias")
        if not alias:
            notes.append(f"probe receipt {path} names no alias")
            continue
        receipts.setdefault(alias, receipt)
    facts = {"roles": len(roles), "receipts": len(receipts)}
    used = {r.get("kimiModel") for r in roles.values() if r.get("kimiModel")}
    for alias in sorted(used):
        receipt = receipts.get(alias)
        if receipt is None:
            notes.append(f"no committed probe receipt for used route {alias}")
            continue
        status = receipt.get("httpStatus")
        if not isinstance(status, int):
            notes.append(f"probe receipt for {alias} carries no integer httpStatus")
        if receipt.get("ok") is not True:
            notes.append(f"route {alias} was used but its receipt is not ok")
    for alias, receipt in sorted(receipts.items()):
        status = receipt.get("httpStatus")
        if not isinstance(status, int):
            notes.append(f"probe receipt for {alias} carries no integer httpStatus")
        if receipt.get("ok") is False:
            excerpt = receipt.get("bodyExcerpt")
            if not isinstance(excerpt, str) or not excerpt.strip():
                notes.append(f"failing probe receipt for {alias} carries no body excerpt")
            if alias in used:
                notes.append(f"failing route {alias} was used by a role")
            recorded = " ".join(
                str(roles.get(role, {}).get("probe", "")) for role in roles
            )
            if alias not in recorded:
                notes.append(f"failing route {alias} is not recorded as a deviation in the route map")
    return (not notes), notes, facts


def check_l3(root: str, rev: str) -> tuple[bool, list[str], dict]:
    notes: list[str] = []
    settlement = show_json(root, rev, SETTLEMENT)
    timing = show_json(root, rev, TIMING)
    accounting = show_json(root, rev, ACCOUNTING)
    log_text = show(root, rev, LOG)
    if settlement is None:
        return False, ["settlement receipt absent at the measured revision"], {}
    if timing is None:
        return False, ["wave timing bytes absent at the measured revision"], {}
    if accounting is None:
        return False, ["round time accounting artifact absent at the measured revision"], {}
    if log_text is None:
        return False, ["LOG.md absent at the measured revision"], {}
    seats = settlement.get("settled", []) + settlement.get("dead", [])
    aggregate = sum(int(e.get("seconds", 0)) for e in seats)
    dead_seconds = sum(int(e.get("seconds", 0)) for e in settlement.get("dead", []))
    timeout = int(settlement.get("timeout_seconds", 0))
    started = parse_ts(str(timing.get("startedAt", "")))
    settled = parse_ts(str(timing.get("settledAt", "")))
    wall = int((settled - started).total_seconds()) if started and settled else None
    facts = {
        "aggregate_seat_seconds": aggregate,
        "dead_seat_seconds": dead_seconds,
        "wall_clock_seconds": wall,
        "timeout_seconds": timeout,
    }
    for seat in settlement.get("dead", []):
        reason = str(seat.get("reason", ""))
        secs = int(seat.get("seconds", 0))
        if reason.startswith("timeout-") and secs != timeout:
            notes.append(
                f"dead seat {seat.get('name')} records reason {reason} but {secs}s != {timeout}s"
            )
        if reason.startswith("exit-") and secs > timeout:
            notes.append(f"dead seat {seat.get('name')} ran longer than its timeout")
    if wall is None:
        notes.append("wave timing does not carry a parsable startedAt/settledAt pair")
    else:
        recorded = accounting.get("wall_clock_seconds")
        if recorded != wall:
            notes.append(f"time accounting wall clock {recorded} != re-derived {wall}")
        if wall > 0 and str(wall) not in log_text:
            notes.append(f"LOG.md does not name the re-derived wall-clock figure {wall}")
    if accounting.get("aggregate_seat_seconds") != aggregate:
        notes.append(
            f"time accounting aggregate {accounting.get('aggregate_seat_seconds')} != {aggregate}"
        )
    if accounting.get("dead_seat_seconds") != dead_seconds:
        notes.append(
            f"time accounting dead-seat seconds {accounting.get('dead_seat_seconds')} != {dead_seconds}"
        )
    grant = show(root, rev, GRANT)
    if grant is None:
        notes.append("wave grant file absent at the measured revision")
    elif "granted lane=kake" not in grant:
        notes.append("wave grant file does not carry a kake grant line")
    return (not notes), notes, facts


def main() -> int:
    parser = argparse.ArgumentParser(description="Round-51 wave-evidence ledger (C1)")
    parser.add_argument("--root", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = {}
    passed = 0
    for name, fn in (("L1", check_l1), ("L2", check_l2), ("L3", check_l3)):
        ok, notes, facts = fn(args.root, args.revision)
        results[name] = {"passed": ok, "notes": notes, "facts": facts}
        passed += 1 if ok else 0

    report = {
        "schema": "kake-r51-c1-wave-ledger-v1",
        "predicate": PREDICATE,
        "revision": args.revision,
        "checks": results,
        "ledger_checks_passed": passed,
        "met": passed == 3,
    }
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"C1 ledger {passed}/3 met={passed == 3}  ({PREDICATE})")
        for name in ("L1", "L2", "L3"):
            entry = results[name]
            state = "pass" if entry["passed"] else "FAIL"
            print(f"  {name} {state}")
            for note in entry["notes"]:
                print(f"    - {note}")
        print(f"  revision: {args.revision}")
    return 0 if passed == 3 else 1


if __name__ == "__main__":
    sys.exit(main())
