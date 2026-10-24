#!/usr/bin/env python3
"""Fail if a control receipt was committed after wave-1 build dispatch."""
from datetime import datetime
import os
from pathlib import Path
import subprocess
import sys


def parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if parsed.utcoffset() is None:
        raise ValueError("timestamp must include a UTC offset")
    return parsed


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: timeline_check.py REPO WAVE_DIR RECEIPT_REPO_PATH", file=sys.stderr)
        return 2

    repo = Path(sys.argv[1])
    wave = Path(sys.argv[2])
    receipt = sys.argv[3]
    try:
        dispatched = parse_time((wave / "w1-dispatched-at.txt").read_text())
        env = os.environ.copy()
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
            env.pop(key, None)
        result = subprocess.run(
            ["git", "-C", str(repo), "log", "--diff-filter=A", "-1", "--format=%cI", "--", receipt],
            check=False,
            capture_output=True,
            text=True,
            env=env,
            timeout=10,
        )
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
            return 2
        committed_text = result.stdout.strip()
        if not committed_text:
            print(f"receipt has no add commit in repository history: {receipt}", file=sys.stderr)
            return 2
        committed = parse_time(committed_text)
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        print(f"timeline-check error: {error}", file=sys.stderr)
        return 2

    delta = int((dispatched - committed).total_seconds())
    print(f"receipt_added_at={committed.isoformat()}")
    print(f"w1_dispatched_at={dispatched.isoformat()}")
    print(f"dispatch_minus_receipt_seconds={delta}")
    if committed <= dispatched:
        print("PASS: control receipt was committed before build dispatch")
        return 0
    print("FAIL: control receipt was committed after build dispatch")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
