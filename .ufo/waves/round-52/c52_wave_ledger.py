#!/usr/bin/env python3
"""Round-52 wave-evidence ledger — hardened C1 counter (operability).

Supersedes `.ufo/waves/round-51/c51_wave_ledger.py` (round-51 claim instrument).
It certifies the same three ledger checks over committed bytes (git show / git
ls-tree only; no worktree reads, no network), plus the vacuity floor the
round-51 residual wave proved was missing (ResidualSettlement: M1-M12 reachable
at 907790c).

Predicate (frozen in `.ufo/waves/round-52/contract.json` before any data):

    met: ledger_checks_passed == 3 of 3

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable (malformed or
exception), 64 usage error.

New guards (all as L1/L2/L3 sub-conditions, each falsifiable):
  L1a spawn floor      — spawn > 0, and settlement seats list equals the payload
                          tasks (name+role, ordered), and the grant's `seats=N`
                          equals spawn and the payload seat count.
  L1b coverage floor    — reports_written == len(settled) == spawn; dead seats are
                          [] unless each dead seat carries a classified reason and
                          a consistent duration (no unclassified free pass).
  L1c report pinning    — every seat marked reported has exactly one committed
                          report file whose blob is non-empty and has a unique
                          sha256 across reports.
  L2  deterministic     — duplicate probe receipts for one alias must agree on
                          httpStatus; a used route needs a committed receipt with
                          integer httpStatus, ok:true and a body excerpt.
  L3  labelled LOG      — LOG.md must name the wall clock via a labelled token
                          (`wall clock **N** s` or `wall_clock_seconds=N`), not a
                          bare substring.
  Exit-code contract     — unevaluable evidence (exceptions, malformed JSON) exits
                          2, never 1; absent evidence counts as a miss (exit 1).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
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

SELFTEST_DIR = ".ufo/waves/round-52/selftest/ledger"


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


def _blob_sha256(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8", "surrogatepass")).hexdigest()


def check_l1(root: str, rev: str) -> tuple[str, list[str], dict]:
    notes: list[str] = []
    settlement = show_json(root, rev, SETTLEMENT)
    taskcall = show_json(root, rev, TASKCALL)
    if settlement is None:
        return "fail", ["settlement receipt absent at the measured revision"], {}
    if taskcall is None:
        return "fail", ["dispatch payload absent at the measured revision"], {}
    tasks = taskcall.get("taskCall", {}).get("tasks", [])
    payload_spawn = taskcall.get("counts", {}).get("spawn")
    spawn = settlement.get("spawn")
    seats = settlement.get("settled", []) + settlement.get("dead", [])
    settled = settlement.get("settled", [])
    dead = settlement.get("dead", [])
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

    # L1a — vacuity floor
    if not isinstance(spawn, int) or spawn <= 0:
        notes.append(f"vacuity: settlement spawn {spawn} is not > 0")
    try:
        expected_seats = [
            {"name": t["name"], "role": t.get("agent")} for t in tasks
        ]
        actual_seats = [
            {"name": s.get("name"), "role": s.get("role")} for s in seats
        ]
        if actual_seats != expected_seats:
            notes.append("vacuity: settlement seats list != payload task list (name+role, ordered)")
    except (TypeError, KeyError):
        notes.append("vacuity: settlement seats list is not comparable to the payload tasks")
    declared = settlement.get("seats")
    if not isinstance(declared, list) or not declared:
        notes.append("vacuity: settlement carries no non-empty seats list")
    else:
        declared_pairs = [
            {"name": s.get("name"), "role": s.get("role")} for s in declared
        ]
        roster_pairs = [
            {"name": s.get("name"), "role": s.get("role")} for s in seats
        ]
        if declared_pairs != roster_pairs:
            notes.append("vacuity: settlement seats list != settled + dead roster")
    grant = show(root, rev, GRANT)
    m = re.search(r"seats=(\d+)", grant or "")
    if m is None:
        notes.append("vacuity: wave grant file does not carry a seats= figure")
    else:
        grant_seats = int(m.group(1))
        if grant_seats != spawn or grant_seats != len(tasks):
            notes.append(
                f"vacuity: grant seats={grant_seats} != spawn {spawn} != payload {len(tasks)}"
            )

    # L1b — coverage floor
    if settlement.get("settled_count", 0) + settlement.get("dead_count", 0) != len(seats):
        notes.append("settled_count + dead_count != settled + dead entries")
    if len(seats) != spawn:
        notes.append(
            f"coverage: settled + dead {len(seats)} != spawn {spawn}"
        )
    if settlement.get("reports_written") != len(settled):
        notes.append(
            f"coverage: reports_written {settlement.get('reports_written')} != settled {len(settled)}"
        )
    if settlement.get("reports_written") != len(committed):
        notes.append(
            f"coverage: reports_written {settlement.get('reports_written')} != committed files {len(committed)}"
        )
    if dead:
        for seat in dead:
            reason = str(seat.get("reason", ""))
            secs = seat.get("seconds")
            if not reason or not isinstance(secs, int) or secs < 0:
                notes.append(
                    f"dead seat {seat.get('name')} lacks a classified reason or non-negative integer seconds"
                )
            elif reason.startswith("timeout-") and secs != int(settlement.get("timeout_seconds", 0)):
                notes.append(f"dead seat {seat.get('name')} reason {reason} but {secs}s != timeout")
            elif reason.startswith("exit-") and secs > int(settlement.get("timeout_seconds", 0)):
                notes.append(f"dead seat {seat.get('name')} ran longer than its timeout")
            elif not (reason.startswith("timeout-") or reason.startswith("exit-")):
                notes.append(f"dead seat {seat.get('name')} carries unclassified reason {reason!r}")

    # L1c — report pinning
    if reported != committed:
        missing = sorted(set(reported) - set(committed))
        extra = sorted(set(committed) - set(reported))
        if missing:
            notes.append(f"seats marked with a report but no committed file: {missing}")
        if extra:
            notes.append(f"committed report files for unknown seats: {extra}")
    digests: set[str] = set()
    for name in reported:
        blob = show(root, rev, f"{REPORT_DIR}/{name}.md")
        if blob is None:
            notes.append(f"report body unreadable for seat {name}")
            continue
        if not blob.strip():
            notes.append(f"vacuity: report body for {name} is empty")
            continue
        d = _blob_sha256(blob)
        if d in digests:
            notes.append(f"vacuity: report digest for {name} duplicates another report")
        digests.add(d)
    return ("fail" if notes else "pass"), notes, facts


def check_l2(root: str, rev: str) -> tuple[str, list[str], dict]:
    notes: list[str] = []
    route_map = show_json(root, rev, ROUTE_MAP)
    if route_map is None:
        return "fail", ["route map absent at the measured revision"], {}
    roles = route_map.get("roles", {})
    if not roles:
        return "fail", ["route map carries no role bindings"], {}
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
        if alias in receipts:
            if receipts[alias].get("httpStatus") != receipt.get("httpStatus"):
                notes.append(
                    f"conflicting probe receipts for alias {alias} ("
                    f"{receipts[alias].get('httpStatus')} vs {receipt.get('httpStatus')})"
                )
            continue
        receipts[alias] = receipt
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
        elif receipt.get("ok") is True and not (200 <= status < 300):
            notes.append(
                f"probe receipt for {alias} claims ok with httpStatus {status}"
            )
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
    return ("fail" if notes else "pass"), notes, facts


def check_l3(root: str, rev: str) -> tuple[str, list[str], dict]:
    notes: list[str] = []
    settlement = show_json(root, rev, SETTLEMENT)
    timing = show_json(root, rev, TIMING)
    accounting = show_json(root, rev, ACCOUNTING)
    log_text = show(root, rev, LOG)
    if settlement is None:
        return "fail", ["settlement receipt absent at the measured revision"], {}
    if timing is None:
        return "fail", ["wave timing bytes absent at the measured revision"], {}
    if accounting is None:
        return "fail", ["round time accounting artifact absent at the measured revision"], {}
    if log_text is None:
        return "fail", ["LOG.md absent at the measured revision"], {}
    seats = settlement.get("settled", []) + settlement.get("dead", [])
    try:
        aggregate = sum(int(e.get("seconds", 0)) for e in seats)
    except (TypeError, ValueError):
        return "unevaluable", ["settlement seat seconds are not integers"], {}
    try:
        dead_seconds = sum(int(e.get("seconds", 0)) for e in settlement.get("dead", []))
    except (TypeError, ValueError):
        return "unevaluable", ["dead-seat seconds are not integers"], {}
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
        carried = timing.get("wallClockSeconds")
        if carried != wall:
            notes.append(f"wave timing wallClockSeconds {carried} != re-derived {wall}")
        if wall > 0:
            labelled = (
                re.search(rf"wall clock[: ]+\*{{0,2}}{wall}\*{{0,2}}\s+s", log_text)
                or re.search(rf"wall_clock_seconds={wall}\b", log_text)
            )
            if not labelled:
                notes.append(f"LOG.md does not name the labelled wall-clock token {wall}")
            # Vacuity floor: a wave that took wall>0 seconds cannot have every
            # seat charge 0 seconds; zero durations are placeholders, not data.
            if aggregate == 0:
                notes.append(
                    f"vacuity: every seat charges 0 s while the wave wall clock is {wall} s"
                )
            for seat in seats:
                secs = int(seat.get("seconds", 0))
                if secs <= 0:
                    notes.append(
                        f"vacuity: seat {seat.get('name')} charges {secs} s in a {wall} s wave"
                    )
                elif secs > wall:
                    notes.append(
                        f"seat {seat.get('name')} charges {secs} s longer than the {wall} s wave"
                    )
    if accounting.get("aggregate_seat_seconds") != aggregate:
        notes.append(
            f"time accounting aggregate {accounting.get('aggregate_seat_seconds')} != {aggregate}"
        )
    if accounting.get("dead_seat_seconds") != dead_seconds:
        notes.append(
            f"time accounting dead-seat seconds {accounting.get('dead_seat_seconds')} != {dead_seconds}"
        )
    roster = {
        "spawn": settlement.get("spawn"),
        "settled_seats": len(settlement.get("settled", [])),
        "dead_seats": len(settlement.get("dead", [])),
    }
    for field, expected in roster.items():
        if accounting.get(field) != expected:
            notes.append(
                f"time accounting {field} {accounting.get(field)} != settlement {expected}"
            )
    grant = show(root, rev, GRANT)
    if grant is None:
        notes.append("wave grant file absent at the measured revision")
    elif "granted lane=kake" not in grant:
        notes.append("wave grant file does not carry a kake grant line")
    return ("fail" if notes else "pass"), notes, facts


def run_checks(root: str, rev: str) -> tuple[int, list[dict]]:
    results = []
    for label, fn in (("L1", check_l1), ("L2", check_l2), ("L3", check_l3)):
        try:
            state, notes, facts = fn(root, rev)
        except Exception as exc:  # noqa: BLE001 — unevaluable evidence exits 2
            state, notes, facts = "unevaluable", [f"exception: {exc}"], {}
        results.append({"check": label, "state": state, "notes": notes, "facts": facts})
    if any(r["state"] == "unevaluable" for r in results):
        return 2, results
    if all(r["state"] == "pass" for r in results):
        return 0, results
    return 1, results
def _selftest_repo(fixture_dir: str, files: dict[str, str], commit_msg: str) -> None:
    """Build a small git repo from a files dict (sandbox only, never the lane)."""
    subprocess.run(["git", "init", "-q", fixture_dir], check=True)
    for rel, content in files.items():
        path = f"{fixture_dir}/{rel}"
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    subprocess.run(["git", "-C", fixture_dir, "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", fixture_dir, "-c", "user.email=selftest@local", "-c",
         "user.name=selftest", "commit", "-q", "-m", commit_msg],
        check=True,
    )


def _selftest_fixture_files() -> dict[str, dict[str, str]]:
    """Return {fixture_name: {repo_relative_path: content}} for each fixture."""
    base_files: dict[str, str] = {}
    # Harvest the real r51 wave evidence from the committed tree.
    import os
    root = os.getcwd()
    rev = "907790c78008819fc95c988431188f90b81f0d5f"
    for rel in (SETTLEMENT, TASKCALL, ROUTE_MAP, TIMING, ACCOUNTING, GRANT, LOG):
        raw = show(root, rev, rel)
        if raw is None:
            raise SystemExit(f"selftest: missing r51 evidence {rel}")
        base_files[rel] = raw
    for p in list_paths(root, rev, REPORT_DIR):
        if p.endswith(".md"):
            raw = show(root, rev, p)
            if raw is None:
                raise SystemExit(f"selftest: missing r51 report {p}")
            base_files[p] = raw
    for p in list_paths(root, rev, PROBE_DIR):
        if p.endswith(".json"):
            raw = show(root, rev, p)
            if raw is None:
                raise SystemExit(f"selftest: missing r51 probe {p}")
            base_files[p] = raw
    fixtures: dict[str, dict[str, str]] = {"pass": dict(base_files)}

    def clone(mutate) -> dict[str, str]:
        files = dict(base_files)
        mutate(files)
        return files

    def j(names):
        return json.dumps(names, ensure_ascii=False, indent=1)

    def load(rel):
        return json.loads(base_files[rel])

    # 1 empty wave
    def f_empty(files):
        settle = load(SETTLEMENT)
        settle["spawn"] = 0
        settle["settled"] = []
        settle["dead"] = []
        settle["settled_count"] = 0
        settle["dead_count"] = 0
        settle["reports_written"] = 0
        settle["seats"] = []
        files[SETTLEMENT] = j(settle)
        tc = load(TASKCALL)
        tc["taskCall"]["tasks"] = []
        tc["counts"]["spawn"] = 0
        files[TASKCALL] = j(tc)
        for p in list(files):
            if p.startswith(REPORT_DIR) and p.endswith(".md"):
                del files[p]
        files[GRANT] = files[GRANT].replace("seats=48", "seats=0")
    fixtures["fail_spawn0"] = clone(f_empty)

    # 2 phantom seats (settlement names not in payload)
    def f_phantom(files):
        settle = load(SETTLEMENT)
        for e in settle["settled"]:
            e["name"] = "Phantom" + e["name"]
        settle["seats"] = [{"name": e["name"], "role": e["role"]} for e in settle["settled"]]
        files[SETTLEMENT] = j(settle)
    fixtures["fail_phantom"] = clone(f_phantom)

    # 3 zero-byte reports
    def f_zerobyte(files):
        for p in list(files):
            if p.startswith(REPORT_DIR) and p.endswith(".md"):
                files[p] = ""
    fixtures["fail_zerobyte"] = clone(f_zerobyte)

    # 4 48 seats / 0 reports
    def f_noreports(files):
        settle = load(SETTLEMENT)
        for e in settle["settled"]:
            e["report"] = False
        settle["reports_written"] = 0
        settle["seats"] = [{"name": e["name"], "role": e["role"]} for e in settle["settled"]]
        files[SETTLEMENT] = j(settle)
        for p in list(files):
            if p.startswith(REPORT_DIR) and p.endswith(".md"):
                del files[p]
    fixtures["fail_48of0"] = clone(f_noreports)

    # 5 multiset collapse: duplicate name, 49 entries, 48 files
    def f_multiset(files):
        settle = load(SETTLEMENT)
        settle["settled"].append(dict(settle["settled"][0]))
        settle["settled_count"] = len(settle["settled"])
        settle["seats"] = [{"name": e["name"], "role": e["role"]} for e in settle["settled"]]
        files[SETTLEMENT] = j(settle)
    fixtures["fail_multiset"] = clone(f_multiset)

    # 6 LOG token deleted
    def f_logtoken(files):
        files[LOG] = files[LOG].replace("wall clock **897 s**", "elapsed 897 s")
    fixtures["fail_logtoken"] = clone(f_logtoken)

    # 7 time tautology
    def f_tauto(files):
        settle = load(SETTLEMENT)
        for e in settle["settled"]:
            e["seconds"] = 0
        files[SETTLEMENT] = j(settle)
        acct = load(ACCOUNTING)
        acct["aggregate_seat_seconds"] = 0
        files[ACCOUNTING] = j(acct)
    fixtures["fail_timetautology"] = clone(f_tauto)

    # 8 seats field renamed
    def f_seatsrename(files):
        settle = load(SETTLEMENT)
        settle["Unused00"] = settle.pop("seats")
        files[SETTLEMENT] = j(settle)
    fixtures["fail_seatsrename"] = clone(f_seatsrename)

    # 9 47-of-48 delivery
    def f_47of48(files):
        settle = load(SETTLEMENT)
        name = settle["settled"].pop()["name"]
        settle["settled_count"] = len(settle["settled"])
        settle["dead"] = [{"name": name, "reason": "no-report", "seconds": 5, "exit": -1}]
        settle["dead_count"] = 1
        settle["seats"] = [{"name": e["name"], "role": e.get("role")} for e in settle["settled"] + settle["dead"]]
        files[SETTLEMENT] = j(settle)
        for p in list(files):
            if p.endswith(f"/{name}.md"):
                del files[p]
    fixtures["fail_47of48"] = clone(f_47of48)

    # 10 grant drift
    def f_grant(files):
        files[GRANT] = files[GRANT].replace("seats=48", "seats=1")
    fixtures["fail_grant"] = clone(f_grant)

    # 11 missing name key
    def f_noname(files):
        settle = load(SETTLEMENT)
        del settle["settled"][0]["name"]
        files[SETTLEMENT] = j(settle)
    fixtures["fail_namekey"] = clone(f_noname)

    # 12 duplicate digests
    def f_dupdigest(files):
        reports = [p for p in files if p.startswith(REPORT_DIR) and p.endswith(".md")]
        if reports:
            files[reports[1]] = files[reports[0]]
    fixtures["fail_dupdigest"] = clone(f_dupdigest)

    def probe_json(files):
        return next(
            p for p in files
            if p.startswith(PROBE_DIR) and p.endswith(".json") and "commandcode" in p
        )

    # 13 duplicate probe receipts that disagree on status
    def f_statusconflict(files):
        path = probe_json(files)
        receipt = json.loads(files[path])
        receipt["httpStatus"] = 204
        files[path.replace(".json", "-dup.json")] = j(receipt)
    fixtures["fail_statusconflict"] = clone(f_statusconflict)

    # 14 ok claimed on a non-2xx status
    def f_statusok(files):
        path = probe_json(files)
        receipt = json.loads(files[path])
        receipt["httpStatus"] = 500
        files[path] = j(receipt)
    fixtures["fail_statusok"] = clone(f_statusok)

    # 15 wave timing carries a wall clock it does not derive
    def f_timingcarry(files):
        timing = load(TIMING)
        timing["wallClockSeconds"] = int(timing.get("wallClockSeconds", 0)) + 60
        files[TIMING] = j(timing)
    fixtures["fail_timingcarry"] = clone(f_timingcarry)

    # 16 seat role drifts from the dispatch payload
    def f_roledrift(files):
        settle = load(SETTLEMENT)
        drift = settle["seats"][0]["name"]
        settle["seats"][0]["role"] = "reviewer"
        for seat in settle["settled"]:
            if seat["name"] == drift:
                seat["role"] = "reviewer"
        files[SETTLEMENT] = j(settle)
    fixtures["fail_roledrift"] = clone(f_roledrift)

    # 17 dead seat with an unclassified reason (receipts otherwise agree)
    def f_deadreason(files):
        settle = load(SETTLEMENT)
        seat = settle["settled"].pop()
        settle["dead"] = [{
            "name": seat["name"], "role": seat.get("role"),
            "reason": "mystery", "seconds": 5, "exit": -1,
        }]
        settle["settled_count"] = len(settle["settled"])
        settle["dead_count"] = 1
        settle["reports_written"] = len(settle["settled"])
        settle["seats"] = [
            {"name": e["name"], "role": e.get("role")}
            for e in settle["settled"] + settle["dead"]
        ]
        files[SETTLEMENT] = j(settle)
        files.pop(f"{REPORT_DIR}/{seat['name']}.md", None)
        acct = load(ACCOUNTING)
        acct["aggregate_seat_seconds"] = (
            acct["aggregate_seat_seconds"] - int(seat["seconds"]) + 5
        )
        acct["dead_seat_seconds"] = 5
        acct["settled_seats"] = len(settle["settled"])
        acct["dead_seats"] = 1
        files[ACCOUNTING] = j(acct)
    fixtures["fail_deadreason"] = clone(f_deadreason)

    # 18 accounting roster drifts from the settlement
    def f_acctroster(files):
        acct = load(ACCOUNTING)
        acct["spawn"] = 47
        files[ACCOUNTING] = j(acct)
    fixtures["fail_acctroster"] = clone(f_acctroster)
    return fixtures


def selftest() -> int:
    import os
    import shutil
    fixtures = _selftest_fixture_files()
    passed = 0
    total = len(fixtures)
    failures: list[str] = []
    for name, files in fixtures.items():
        work = f"{SELFTEST_DIR}/work/{name}"
        if os.path.exists(work):
            shutil.rmtree(work)
        _selftest_repo(work, files, f"fixture {name}")
        rev = subprocess.run(
            ["git", "-C", work, "rev-parse", "HEAD"],
            stdout=subprocess.PIPE, text=True, check=True,
        ).stdout.strip()
        code, results = run_checks(work, rev)
        if name == "pass":
            ok = code == 0
        elif name == "fail_namekey":
            ok = code == 2
        else:
            ok = code == 1
        if ok:
            passed += 1
        else:
            failures.append(f"{name}: expected {'0' if name=='pass' else ('2' if name=='fail_namekey' else '1')}, got {code}")
            for r in results:
                if r["notes"]:
                    failures.append(f"    {r['check']}: {' | '.join(r['notes'][:2])}")
    shutil.rmtree(f"{SELFTEST_DIR}/work", ignore_errors=True)
    print(f"c52 ledger selftest: {passed}/{total}")
    for line in failures:
        print("  FAIL", line)
    return 0 if passed == total else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Round-52 wave-evidence ledger (C1)")
    parser.add_argument("--root", default=".")
    parser.add_argument("--revision", default=None)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not args.revision:
        parser.error("--revision is required unless --selftest is used")
    code, results = run_checks(args.root, args.revision)
    passed = sum(1 for r in results if r["state"] == "pass")
    if args.json:
        body = {
            "schema": "kake-r52-c1-wave-ledger-v1",
            "predicate": PREDICATE,
            "revision": args.revision,
            "checks": {r["check"]: {"passed": r["state"] == "pass", "notes": r["notes"], "facts": r["facts"]} for r in results},
            "ledger_checks_passed": passed,
            "met": code == 0,
        }
        print(json.dumps(body, indent=1))
    else:
        print(f"C1 ledger {passed}/3 met={'True' if code == 0 else 'False'}  ({PREDICATE})")
        for r in results:
            state = r["state"].upper()
            print(f"  {r['check']} {state}")
            for note in r["notes"]:
                print(f"    - {note}")
        print(f"  revision: {args.revision}")
    print("EXIT=" + str(code) if not args.json else f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
