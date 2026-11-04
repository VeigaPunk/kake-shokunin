#!/usr/bin/env python3
"""Round-84 C2 counter: policy-header value semantics re-derive (kake).

Runs the frozen tool `scripts/policy_value_class.py` over the two committed
captures and over the two synthetic control pairs, and decides the predicate
frozen in `.ufo/waves/round-84/contract.md` §C2. The counter verifies every
receipt itself before trusting any tool output, and compares each control
pair's changed policy headers against
`.ufo/waves/round-84/policy-expectations.json`.

Usage:
  c84_policy_values.py --root <tree> [--revision <rev>] [--work <dir>]
  c84_policy_values.py --selftest

Exit: 0 met, 1 not met, 2 unevaluable, 64 usage. Offline: no socket call.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

TOOL = "scripts/policy_value_class.py"
REAL_A = ".ufo/waves/round-81/capture"
REAL_B = ".ufo/waves/round-82/capture"
CONTROL = ".ufo/waves/round-84/capture-control"
DECLARED = ".ufo/waves/round-81/capture-expectations.json"
EXPECTATIONS = ".ufo/waves/round-84/policy-expectations.json"
RECORD = ".ufo/waves/round-84/controls/tool-real-pair.txt"

SURFACE_KEYS = ("changed", "reordered", "numeric_parameter", "directive_added",
                "directive_removed", "directive_changed", "header_added",
                "header_removed", "unclassified")
CHANGE_RE = re.compile(r"^change surface=(\S+) header=(\S+) class=(\S+)$")
OFFLINE_IMPORT = re.compile(r"^\s*(?:import|from)\s+(socket|urllib|requests|http\.client)\b",
                            re.MULTILINE)


def export(root: Path, revision: str, work: Path) -> Path:
    target = work / "export"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    proc = subprocess.run(["git", "-C", str(root), "archive", "--format=tar", revision],
                          capture_output=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"git archive {revision} failed: "
                           f"{proc.stderr.decode('utf-8', 'replace').strip()}")
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as archive:
        archive.extractall(target)
    return target


def receipt_ok(directory: Path) -> bool:
    receipt_path = directory / "response.json"
    if not receipt_path.is_file():
        return False
    try:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    body_path = directory / str(receipt.get("bodyFile") or "body.bin")
    if not body_path.is_file():
        return False
    body = body_path.read_bytes()
    if receipt.get("method") != "GET":
        return False
    status = receipt.get("status")
    if not isinstance(status, int) or not 100 <= status <= 599:
        return False
    if receipt.get("bytes") != len(body):
        return False
    if receipt.get("sha256") != hashlib.sha256(body).hexdigest():
        return False
    return receipt.get("truncated") is False


def run_tool(tree: Path, a: str, b: str, work: Path) -> tuple[int, str]:
    tool = tree / TOOL
    if not tool.is_file():
        return 127, ""
    proc = subprocess.run([sys.executable, "-B", str(tool), "--a", str(tree / a),
                           "--b", str(tree / b), "--declared", str(tree / DECLARED)],
                          capture_output=True, text=True, check=False,
                          env={"TMPDIR": str(work), "PATH": "/usr/bin:/bin"})
    return proc.returncode, proc.stdout


def kv(line: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for token in line.split():
        if "=" in token:
            key, value = token.split("=", 1)
            fields[key] = value
    return fields


def parse(stdout: str) -> dict | None:
    changes: dict[tuple[str, str], str] = {}
    surfaces: dict[str, dict[str, str]] = {}
    summary: dict[str, str] | None = None
    for line in stdout.splitlines():
        if line.startswith("change "):
            match = CHANGE_RE.match(line)
            if not match:
                return None
            changes[(match.group(1), match.group(2))] = match.group(3)
        elif line.startswith("surface="):
            fields = kv(line)
            surfaces[fields.get("surface", "")] = fields
        elif line.startswith("summary "):
            summary = kv(line)
    if summary is None:
        return None
    for key in SURFACE_KEYS:
        if key not in summary:
            return None
    return {"changes": changes, "surfaces": surfaces, "summary": summary}


def mismatches(observed: dict[tuple[str, str], str],
               expected: dict[str, dict[str, str]]) -> int:
    wanted = {(surface, header): cls for surface, table in expected.items()
              for header, cls in table.items()}
    return len(set(wanted.items()) ^ set(observed.items()))


def offline(tool_text: str) -> bool:
    text = tool_text
    match = re.search(r'^""".*?"""', text, re.DOTALL)
    if match:
        text = text[:match.start()] + text[match.end():]
    return OFFLINE_IMPORT.search(text) is None


def tool_selftest(tree: Path, work: Path) -> bool:
    tool = tree / TOOL
    if not tool.is_file():
        return False
    work.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run([sys.executable, "-B", str(tool), "--selftest", "--work", str(work)],
                          capture_output=True, text=True, check=False, env={"PATH": "/usr/bin:/bin"})
    return proc.returncode == 0


def evaluate(tree: Path, work: Path, label: str = "worktree") -> int:
    flags: dict[str, int | str] = {}
    try:
        declared_doc = json.loads((tree / DECLARED).read_text(encoding="utf-8"))
        expectations = json.loads((tree / EXPECTATIONS).read_text(encoding="utf-8"))
        declared = [str(item["id"]) for item in declared_doc["surfaces"]]
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        print("fault: cannot read the declared surfaces or the frozen expectations", file=sys.stderr)
        return 2
    flags["declared"] = len(declared)
    flags["surfaces_a"] = sum(1 for sid in declared if (tree / REAL_A / sid).is_dir())
    flags["surfaces_b"] = sum(1 for sid in declared if (tree / REAL_B / sid).is_dir())

    receipts = [(REAL_A, sid) for sid in declared] + [(REAL_B, sid) for sid in declared]
    for pair in ("control", "equivalent"):
        for side in ("a", "b"):
            receipts += [(f"{CONTROL}/{pair}/{side}", sid) for sid in declared]
    flags["receipts_ok"] = int(all(receipt_ok(tree / base / sid) for base, sid in receipts))

    tool_file = tree / TOOL
    tool_text = tool_file.read_text(encoding="utf-8") if tool_file.is_file() else ""
    flags["tool_absent"] = int(not tool_file.is_file())
    flags["tool_offline"] = int(bool(tool_text) and offline(tool_text))

    real_rc, real_out = run_tool(tree, REAL_A, REAL_B, work)
    parsed = parse(real_out) if real_rc == 0 else None
    flags["real_changed"] = int(parsed["summary"]["changed"]) if parsed else -1
    flags["real_verdict"] = parsed["summary"]["verdict"] if parsed else "tool-unevaluable"

    control_rc, control_out = run_tool(tree, f"{CONTROL}/control/a", f"{CONTROL}/control/b", work)
    control = parse(control_out) if control_rc == 0 else None
    flags["ctl_changed"] = int(control["summary"]["changed"]) if control else -1
    flags["ctl_verdict"] = control["summary"]["verdict"] if control else "tool-unevaluable"
    flags["ctl_mismatch"] = (mismatches(control["changes"], expectations.get("control", {}))
                             if control else -1)

    eq_rc, eq_out = run_tool(tree, f"{CONTROL}/equivalent/a", f"{CONTROL}/equivalent/b", work)
    eq = parse(eq_out) if eq_rc == 0 else None
    flags["eq_changed"] = int(eq["summary"]["changed"]) if eq else -1
    flags["eq_verdict"] = eq["summary"]["verdict"] if eq else "tool-unevaluable"
    flags["eq_mismatch"] = (mismatches(eq["changes"], expectations.get("equivalent", {}))
                            if eq else -1)

    record_path = tree / RECORD
    record = record_path.read_text(encoding="utf-8") if record_path.is_file() else None
    flags["record_equal"] = int(record is not None and
                                record.rstrip("\n") == real_out.rstrip("\n"))
    _second_rc, second_out = run_tool(tree, REAL_A, REAL_B, work)
    flags["determinism"] = int(real_rc == 0 and second_out == real_out)
    flags["selftest_ok"] = int(tool_selftest(tree, work / "tool-selftest"))
    flags["counter_selftest_ok"] = int(selfcheck())

    met = (
        flags["declared"] == 3
        and flags["surfaces_a"] == 3 and flags["surfaces_b"] == 3
        and flags["receipts_ok"] == 1
        and flags["real_changed"] == 0 and flags["real_verdict"] == "policy-unchanged"
        and flags["ctl_changed"] == 3 and flags["ctl_mismatch"] == 0
        and flags["ctl_verdict"] == "policy-changed"
        and flags["eq_changed"] == 1 and flags["eq_mismatch"] == 0
        and flags["eq_verdict"] == "policy-rewritten-equivalent"
        and flags["record_equal"] == 1 and flags["determinism"] == 1
        and flags["tool_offline"] == 1 and flags["selftest_ok"] == 1
        and flags["counter_selftest_ok"] == 1
    )
    order = ("declared", "surfaces_a", "surfaces_b", "receipts_ok", "real_changed",
             "real_verdict", "ctl_changed", "ctl_mismatch", "ctl_verdict", "eq_changed",
             "eq_mismatch", "eq_verdict", "record_equal", "determinism", "tool_offline",
             "selftest_ok", "counter_selftest_ok")
    rendered = " ".join(f"{key}={flags[key]}" for key in order if key in flags)
    print(f"C2v1 revision={label} {rendered} met={'true' if met else 'false'}")
    return 0 if met else 1


# ------------------------------------------------------------------ self-check

CANARY = """change surface=s1 header=cache-control class=numeric_parameter
change surface=s1 header=referrer-policy class=reordered
surface=s1 changed=2 reordered=1 numeric_parameter=1 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-changed
summary surfaces=1 changed=2 reordered=1 numeric_parameter=1 directive_added=0 directive_removed=0 directive_changed=0 header_added=0 header_removed=0 unclassified=0 verdict=policy-changed
"""


def selfcheck() -> bool:
    parsed = parse(CANARY)
    if parsed is None:
        return False
    if parsed["summary"]["verdict"] != "policy-changed":
        return False
    if mismatches(parsed["changes"], {"s1": {"cache-control": "numeric_parameter",
                                             "referrer-policy": "reordered"}}) != 0:
        return False
    if mismatches(parsed["changes"], {"s1": {"cache-control": "reordered"}}) != 3:
        return False
    return True


def selftest() -> int:
    checks = [("canary-parses", selfcheck()),
              ("offline-detects-socket", not offline("import socket\n")),
              ("offline-accepts-clean", offline('"""doc"""\nimport json\n')),
              ("change-regex-rejects-junk", CHANGE_RE.match("change surface=") is None)]
    passed = sum(1 for _n, ok in checks if ok)
    for name, ok in checks:
        print(("ok   " if ok else "FAIL ") + name)
    print(f"selftest: {passed}/{len(checks)} passed")
    return 0 if passed == len(checks) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path)
    parser.add_argument("--revision")
    parser.add_argument("--work", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    if not args.root:
        parser.print_usage(sys.stderr)
        return 64
    root = args.root.resolve()
    if not root.is_dir():
        print(f"fault: not a directory: {root}", file=sys.stderr)
        return 2
    work = args.work or Path(tempfile.mkdtemp(dir=None, prefix="c84-c2-"))
    work.mkdir(parents=True, exist_ok=True)
    try:
        if args.revision:
            if not (root / ".git").exists():
                print("fault: --revision needs a git checkout", file=sys.stderr)
                return 2
            tree = export(root, args.revision, work)
            (work / "run").mkdir(parents=True, exist_ok=True)
            return evaluate(tree, work / "run", args.revision)
        return evaluate(root, work / "run")
    finally:
        if args.work is None:
            shutil.rmtree(work, ignore_errors=True)



if __name__ == "__main__":
    raise SystemExit(main())
