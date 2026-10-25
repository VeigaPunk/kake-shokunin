#!/usr/bin/env python3
"""Round-52 gate-registry completeness counter (C1, routed defect r51-1).

Round 51's two counters had no registry row, no self-test and no frozen baseline, so
PROTOCOL §Gate graded them non-conformant as gates. This counter decides whether the
round-52 SKILL.md registry rows and their frozen baselines actually exist, over
committed bytes only (`git show`; no worktree reads, no network):

  * each of the two instruments has a registry row with all eight cells
    (name, kind, entry command, verdict map, self-test, pinned values, write scope,
    owner), naming the counter script and offering a `--selftest` mode;
  * each counter script hashes to its `baselines.json` pin, and every pinned input
    blob hashes to its pin;
  * each committed self-test receipt hashes to its pin and reports exit 0.

Predicate (frozen in `.ufo/waves/round-52/contract.json` before any data):

    met: registry_rows == 2 AND selftest_receipts == 2

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable (missing or malformed
pin/receipt bytes, exception), 64 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

PREDICATE = "met: registry_rows == 2 AND selftest_receipts == 2"
REGISTRY_HOME = "SKILL.md"
BASELINES = ".ufo/waves/round-52/baselines.json"
CONTROL = ".ufo/waves/round-52/control"
SELFTEST_DIR = ".ufo/waves/round-52/selftest/registry"

TARGETS = {
    "wave-evidence-ledger": ".ufo/waves/round-52/c52_wave_ledger.py",
    "quote-truth-counter": ".ufo/waves/round-52/c52_quote_truth.py",
}


def git(root: str, *args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", "-C", root, *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return proc.returncode, proc.stdout


def show(root: str, rev: str, path: str) -> str | None:
    rc, out = git(root, "show", f"{rev}:{path}")
    return out if rc == 0 else None


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def registry_rows(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) != 10:  # 8 content cells, empty edges
            continue
        name = cells[1]
        if not name or name == "Name" or set(name) <= {"-"}:
            continue
        rows[name] = cells[1:-1]
    return rows


def exit_line(text: str) -> str | None:
    for line in reversed(text.splitlines()):
        if line.strip().upper().startswith("EXIT="):
            return line.strip()
    return None


def run_checks(root: str, rev: str) -> tuple[int, list[dict]]:
    results: list[dict] = []

    def add(check: str, notes: list[str], facts: dict | None = None) -> None:
        results.append({
            "check": check,
            "state": "pass" if not notes else "fail",
            "notes": notes,
            "facts": facts or {},
        })

    try:
        registry_text = show(root, rev, REGISTRY_HOME)
        if registry_text is None:
            return 2, [{
                "check": "registry_home",
                "state": "unevaluable",
                "notes": [f"{REGISTRY_HOME} unreadable at the measured revision"],
                "facts": {},
            }]
        rows = registry_rows(registry_text)
        pin_text = show(root, rev, BASELINES)
        if pin_text is None:
            return 2, [{
                "check": "baselines",
                "state": "unevaluable",
                "notes": [f"{BASELINES} absent at the measured revision"],
                "facts": {},
            }]
        try:
            pins = json.loads(pin_text).get("counters", {})
        except json.JSONDecodeError:
            return 2, [{
                "check": "baselines",
                "state": "unevaluable",
                "notes": [f"{BASELINES} is not JSON"],
                "facts": {},
            }]

        registry_notes: list[str] = []
        receipt_notes: list[str] = []
        pin_notes: list[str] = []
        registry_hits = 0
        receipt_hits = 0
        for name, script in TARGETS.items():
            row = rows.get(name)
            if row is None:
                registry_notes.append(f"{name}: no registry row in {REGISTRY_HOME}")
            else:
                registry_hits += 1
                if len(row) != 8 or any(not cell for cell in row):
                    registry_notes.append(f"{name}: registry row does not carry 8 non-empty cells")
                    row = None
            pin = pins.get(name)
            if pin is None:
                pin_notes.append(f"{name}: no baseline entry")
                continue
            if pin.get("script") != script:
                pin_notes.append(f"{name}: baseline names script {pin.get('script')!r}, expected {script!r}")
            script_blob = show(root, rev, script)
            if script_blob is None:
                pin_notes.append(f"{name}: counter script {script} absent at the measured revision")
            elif pin.get("scriptSha256") != sha(script_blob):
                pin_notes.append(f"{name}: counter sha256 does not match the pinned baseline")
            for path, digest in sorted(pin.get("inputs", {}).items()):
                blob = show(root, rev, path)
                if blob is None:
                    pin_notes.append(f"{name}: pinned input {path} absent at the measured revision")
                elif sha(blob) != digest:
                    pin_notes.append(f"{name}: pinned input {path} does not hash to its pin")
            if row is not None:
                if script not in row[2]:
                    registry_notes.append(f"{name}: entry command does not name {script}")
                if "--selftest" not in row[4] or script not in row[4]:
                    registry_notes.append(f"{name}: self-test cell does not offer `{script} --selftest`")
                if row[5].strip() in ("", "—"):
                    registry_notes.append(f"{name}: pinned-values cell is empty")
                if row[7] != "kake":
                    registry_notes.append(f"{name}: owner cell is {row[7]!r}, expected 'kake'")
            for receipt in pin.get("receipts", []):
                path = receipt.get("path")
                blob = show(root, rev, path) if path else None
                if blob is None:
                    receipt_notes.append(f"{name}: selftest receipt {path} absent")
                    continue
                if sha(blob) != receipt.get("sha256"):
                    receipt_notes.append(f"{name}: selftest receipt {path} does not hash to its pin")
                    continue
                line = exit_line(blob)
                if line != receipt.get("exit"):
                    receipt_notes.append(
                        f"{name}: selftest receipt {path} exits {line!r}, pinned {receipt.get('exit')!r}"
                    )
                    continue
                if line != "EXIT=0":
                    receipt_notes.append(f"{name}: selftest receipt {path} is not a clean run")
                    continue
                receipt_hits += 1

        add("registry_rows", registry_notes, {"rows": registry_hits})
        add("frozen_baselines", pin_notes)
        add("selftest_receipts", receipt_notes, {"receipts": receipt_hits})
    except Exception as exc:
        return 2, results + [{
            "check": "exception",
            "state": "unevaluable",
            "notes": [f"{type(exc).__name__}: {exc}"],
            "facts": {},
        }]

    if any(r["state"] == "unevaluable" for r in results):
        return 2, results
    met = (
        results[0]["facts"].get("rows") == 2
        and results[2]["facts"].get("receipts") == 2
        and all(r["state"] == "pass" for r in results)
    )
    return (0 if met else 1), results


def _repo(fixture_dir: str, files: dict[str, str]) -> str:
    os.makedirs(fixture_dir, exist_ok=True)
    subprocess.run(["git", "init", "-q", fixture_dir], check=True)
    for path, content in files.items():
        target = os.path.join(fixture_dir, path)
        os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(content)
    subprocess.run(["git", "-C", fixture_dir, "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", fixture_dir, "-c", "user.email=selftest@local", "-c",
         "user.name=selftest", "commit", "-q", "-m", "fixture"],
        check=True,
    )
    rc, out = git(fixture_dir, "rev-parse", "HEAD")
    return out.strip()


def selftest() -> int:
    rev = os.environ.get("KAKE_R52_SELFTEST_REV")
    if not rev:
        rc, out = git(os.getcwd(), "rev-parse", "HEAD")
        if rc != 0:
            print("selftest: cannot resolve HEAD", file=sys.stderr)
            return 2
        rev = out.strip()
    root = os.getcwd()
    pins_text = show(root, rev, BASELINES)
    skills_text = show(root, rev, REGISTRY_HOME)
    if pins_text is None or skills_text is None:
        print("selftest: missing SKILL.md or baselines at HEAD", file=sys.stderr)
        return 2
    pins = json.loads(pins_text)
    base: dict[str, str] = {REGISTRY_HOME: skills_text, BASELINES: pins_text}
    for name, pin in pins.get("counters", {}).items():
        script = show(root, rev, pin["script"])
        if script is not None:
            base[pin["script"]] = script
        for path in pin.get("inputs", {}):
            blob = show(root, rev, path)
            if blob is not None:
                base[path] = blob
        for receipt in pin.get("receipts", []):
            blob = show(root, rev, receipt["path"])
            if blob is not None:
                base[receipt["path"]] = blob

    def clone(mutate) -> dict[str, str]:
        files = dict(base)
        mutate(files)
        return files

    def row_of(name: str) -> str:
        for line in base[REGISTRY_HOME].splitlines():
            if line.startswith(f"| {name} |"):
                return line
        raise KeyError(name)

    fixtures: dict[str, dict[str, str]] = {"pass": dict(base)}

    def f_row_missing(files):
        files[REGISTRY_HOME] = files[REGISTRY_HOME].replace(row_of("quote-truth-counter") + "\n", "")

    fixtures["fail_row_missing"] = clone(f_row_missing)

    def f_row_short(files):
        line = row_of("wave-evidence-ledger")
        files[REGISTRY_HOME] = files[REGISTRY_HOME].replace(line, "|".join(line.split("|")[:-2]) + " |")

    fixtures["fail_row_short"] = clone(f_row_short)

    def f_no_selftest_cell(files):
        line = row_of("quote-truth-counter")
        cells = line.split("|")
        cells[5] = " `python3 -B .ufo/waves/round-52/c52_quote_truth.py --root . --revision <commit>` "
        files[REGISTRY_HOME] = files[REGISTRY_HOME].replace(line, "|".join(cells))

    fixtures["fail_no_selftest_cell"] = clone(f_no_selftest_cell)

    def f_script_sha(files):
        data = json.loads(files[BASELINES])
        data["counters"]["wave-evidence-ledger"]["scriptSha256"] = "0" * 64
        files[BASELINES] = json.dumps(data, ensure_ascii=False, indent=1)

    fixtures["fail_script_sha"] = clone(f_script_sha)

    def f_input_sha(files):
        data = json.loads(files[BASELINES])
        key = next(iter(data["counters"]["quote-truth-counter"]["inputs"]))
        data["counters"]["quote-truth-counter"]["inputs"][key] = "1" * 64
        files[BASELINES] = json.dumps(data, ensure_ascii=False, indent=1)

    fixtures["fail_input_sha"] = clone(f_input_sha)

    def f_receipt_sha(files):
        data = json.loads(files[BASELINES])
        data["counters"]["quote-truth-counter"]["receipts"][0]["sha256"] = "2" * 64
        files[BASELINES] = json.dumps(data, ensure_ascii=False, indent=1)

    fixtures["fail_receipt_sha"] = clone(f_receipt_sha)

    def f_receipt_exit(files):
        data = json.loads(files[BASELINES])
        receipt = data["counters"]["wave-evidence-ledger"]["receipts"][0]
        path = receipt["path"]
        body = files[path].replace("EXIT=0", "EXIT=1")
        files[path] = body
        receipt["sha256"] = sha(body)

    fixtures["fail_receipt_exit"] = clone(f_receipt_exit)

    def f_missing_receipt(files):
        data = json.loads(files[BASELINES])
        path = data["counters"]["quote-truth-counter"]["receipts"][0]["path"]
        files.pop(path, None)

    fixtures["fail_missing_receipt"] = clone(f_missing_receipt)

    def f_bad_pins(files):
        files[BASELINES] = "{nope"

    fixtures["fail_bad_pins"] = clone(f_bad_pins)

    work_root = os.path.join(root, SELFTEST_DIR, "work")
    if os.path.exists(work_root):
        shutil.rmtree(work_root)
    os.makedirs(work_root, exist_ok=True)
    passed = 0
    total = len(fixtures)
    failures: list[str] = []
    for name in sorted(fixtures):
        work = os.path.join(work_root, name)
        fixture_rev = _repo(work, fixtures[name])
        code, results = run_checks(work, fixture_rev)
        expected = 0 if name == "pass" else (2 if name == "fail_bad_pins" else 1)
        if code == expected:
            passed += 1
        else:
            failures.append(f"{name}: expected {expected}, got {code}")
            for r in results:
                for note in r["notes"][:2]:
                    failures.append(f"    {r['check']}: {note}")
    shutil.rmtree(work_root, ignore_errors=True)
    print(f"c52 registry selftest: {passed}/{total} (fixture revision {rev[:12]})")
    for line in failures:
        print("  FAIL", line)
    return 0 if passed == total else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Round-52 gate-registry completeness counter (C1)")
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
    rows = next((r["facts"].get("rows") for r in results if r["check"] == "registry_rows"), None)
    receipts = next((r["facts"].get("receipts") for r in results if r["check"] == "selftest_receipts"), None)
    if args.json:
        print(json.dumps({
            "schema": "kake-r52-c1-gate-registry-v1",
            "predicate": PREDICATE,
            "revision": args.revision,
            "registry_rows": rows,
            "selftest_receipts": receipts,
            "checks": {r["check"]: {"state": r["state"], "notes": r["notes"], "facts": r["facts"]} for r in results},
            "met": code == 0,
        }, indent=1, ensure_ascii=False))
    else:
        print(f"C1 registry rows={rows} receipts={receipts} met={code == 0}  ({PREDICATE})")
        for r in results:
            print(f"  {r['check']} {r['state'].upper()}")
            for note in r["notes"]:
                print(f"    - {note}")
        print(f"  revision: {args.revision}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
