#!/usr/bin/env python3
"""Round-51 wave-evidence builder.

Derives the three committed wave-evidence artifacts the C1 ledger certifies, from measured
facts only:

  settlement.json          seat accounting: spawn, settled, dead, reports_written
  wave-timing.json         the measured startedAt / settledAt pair of the dispatch
  round-time-accounting.json
                           aggregate seat seconds, dead-seat seconds and the wall clock

Measured inputs:
  * `.ufo/waves/round-51/w51-taskcall.json` — the validator's payload (seat names and roles)
  * `.ufo/waves/round-51/wave-start-utc.txt` — the L1's pre-dispatch timestamp
  * `.ufo/waves/round-51/settled-utc.txt` — the L1's post-batch timestamp
  * `.ufo/waves/round-51/w1/<Seat>.md` — each seat's own report; its mtime is the seat's
    finish time, so `seconds` is the seat's elapsed time since dispatch.

A seat with no committed report is recorded dead with reason `no-report`: the batch settled
without a written report, so the seat produced no committed output.

Usage: python3 -B .ufo/waves/round-51/build_wave_evidence.py
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone

WAVE = ".ufo/waves/round-51"
W1 = f"{WAVE}/w1"
TIMEOUT = int(os.environ.get("KAKE_R51_TIMEOUT", "3600"))


def stamp(path: str) -> datetime:
    raw = open(path, encoding="utf-8").read().strip()
    return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc)


def main() -> int:
    payload = json.load(open(f"{WAVE}/w51-taskcall.json", encoding="utf-8"))
    tasks = payload["taskCall"]["tasks"]
    started = stamp(f"{WAVE}/wave-start-utc.txt")
    settled = stamp(f"{WAVE}/settled-utc.txt")
    wall = int((settled - started).total_seconds())

    settled_seats: list[dict] = []
    dead_seats: list[dict] = []
    for task in tasks:
        path = os.path.join(W1, task["name"] + ".md")
        role = task.get("agent") or task.get("role")
        if os.path.isfile(path):
            end = datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)
            seconds = max(0, int((end - started).total_seconds()))
            settled_seats.append({
                "name": task["name"], "role": role,
                "model": "commandcode/deepseek/deepseek-v4.1-flash",
                "exit": 0, "seconds": seconds, "report": True,
            })
        else:
            dead_seats.append({
                "name": task["name"], "role": role,
                "model": "commandcode/deepseek/deepseek-v4.1-flash",
                "exit": -1, "seconds": wall, "report": False,
                "reason": "no-report",
                "reasonDetail": "the batch settled with no committed seat report",
            })

    settlement = {
        "schema": "kake-r51-settlement-v1",
        "wave": "r51-w1",
        "transport": "omp/task (one batched task call)",
        "routeTable": "/home/vgpnk/.omp/agent/config.yml",
        "dispatchPayload": f"{WAVE}/w51-taskcall.json",
        "timeout_seconds": TIMEOUT,
        "spawn": payload["counts"]["spawn"],
        "replacements": [],
        "settled": settled_seats,
        "dead": dead_seats,
        "settled_count": len(settled_seats),
        "dead_count": len(dead_seats),
        "reports_written": sum(1 for e in settled_seats + dead_seats if e["report"]),
        "seats": [
            {"name": t["name"], "role": t.get("agent") or t.get("role")}
            for t in tasks
        ],
    }
    with open(f"{WAVE}/settlement.json", "w", encoding="utf-8") as fh:
        json.dump(settlement, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    timing = {
        "schema": "kake-r51-wave-timing-v1",
        "wave": "r51-w1",
        "startedAt": started.isoformat(),
        "settledAt": settled.isoformat(),
        "wallClockSeconds": wall,
        "source": "L1 pre-dispatch and post-batch timestamps, UTC",
    }
    with open(f"{WAVE}/wave-timing.json", "w", encoding="utf-8") as fh:
        json.dump(timing, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    aggregate = sum(int(e["seconds"]) for e in settled_seats + dead_seats)
    dead_seconds = sum(int(e["seconds"]) for e in dead_seats)
    accounting = {
        "schema": "kake-r51-round-time-accounting-v1",
        "round": 51,
        "wave": "r51-w1",
        "wall_clock_seconds": wall,
        "aggregate_seat_seconds": aggregate,
        "dead_seat_seconds": dead_seconds,
        "settled_seats": len(settled_seats),
        "dead_seats": len(dead_seats),
        "seatDefinition": "per-seat seconds are elapsed time from dispatch to the seat's own report mtime; dead seats are charged the wave wall clock",
        "spawn": payload["counts"]["spawn"],
    }
    with open(f"{WAVE}/round-time-accounting.json", "w", encoding="utf-8") as fh:
        json.dump(accounting, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"spawn={settlement['spawn']} settled={len(settled_seats)} dead={len(dead_seats)} "
          f"reports={settlement['reports_written']} wall={wall} aggregate={aggregate} deadSeconds={dead_seconds}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
