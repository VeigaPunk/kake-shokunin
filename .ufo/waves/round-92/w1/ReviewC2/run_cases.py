#!/usr/bin/env python3
"""ReviewC2 runner: executes every case in cases.json against the C2 candidate.

One fresh `python3 -B scripts/heuristic_freshness.py` process per case (stdin/stdout).
Never imports or reads the candidate source; observes the protocol only.
Writes runs.jsonl (full detail) and agreement.txt (human summary).
"""
import json
import subprocess
import sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
HERE = Path(__file__).resolve().parent
CANDIDATE = LANE / "scripts" / "heuristic_freshness.py"


def expected_refusal_ok(proc) -> tuple[bool, str]:
    if proc.returncode != 1:
        return False, f"exit={proc.returncode} (want 1)"
    if proc.stdout != b"":
        return False, f"stdout={proc.stdout[:80]!r} (want empty)"
    err = proc.stderr.decode("utf-8", "replace")
    if not err.startswith("invalid_input:"):
        return False, f"stderr={err[:80]!r} (want 'invalid_input:' prefix)"
    return True, "refused"


def expected_decision_ok(proc, want: dict) -> tuple[bool, str]:
    if proc.returncode != 0:
        return False, f"exit={proc.returncode} stderr={proc.stderr[:80]!r} (want exit 0)"
    if proc.stderr != b"":
        return False, f"stderr={proc.stderr[:80]!r} (want empty)"
    try:
        got = json.loads(proc.stdout.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return False, f"stdout={proc.stdout[:80]!r} not JSON: {exc}"
    if set(got) != {"decision", "lifetime", "heuristic"}:
        return False, f"keys={sorted(got)} (want exactly decision/lifetime/heuristic)"
    if got != want:
        return False, f"got={got} want={want}"
    return True, f"agreed {got}"


def main() -> int:
    if not CANDIDATE.exists():
        print(f"CANDIDATE ABSENT: {CANDIDATE}", file=sys.stderr)
        return 2
    cases = json.loads((HERE / "cases.json").read_text())["cases"]
    rows = []
    for case in cases:
        stdin = json.dumps(case["input"], ensure_ascii=False).encode("utf-8")
        proc = subprocess.run(
            ["python3", "-B", str(CANDIDATE)],
            input=stdin, capture_output=True, cwd=str(LANE), timeout=30,
        )
        if case["expected"].get("refusal"):
            ok, detail = expected_refusal_ok(proc)
        else:
            ok, detail = expected_decision_ok(proc, case["expected"])
        rows.append({
            "id": case["id"], "clause": case["clause"], "note": case.get("note", ""),
            "ok": ok, "detail": detail,
            "exit": proc.returncode,
            "stdout": proc.stdout.decode("utf-8", "replace"),
            "stderr": proc.stderr.decode("utf-8", "replace"),
        })
    (HERE / "runs.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    )
    total = len(rows)
    agree = sum(1 for r in rows if r["ok"])
    lines = [
        f"candidate: scripts/heuristic_freshness.py",
        f"cases: {total}  agree: {agree}  disagree: {total - agree}",
        "",
    ]
    for r in rows:
        mark = "ok       " if r["ok"] else "DISAGREE "
        lines.append(f"{mark} {r['id']:>4} clause {str(r['clause']):>5}  {r['detail']}")
    (HERE / "agreement.txt").write_text("\n".join(lines) + "\n")
    print(f"cases={total} agree={agree} disagree={total - agree}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
