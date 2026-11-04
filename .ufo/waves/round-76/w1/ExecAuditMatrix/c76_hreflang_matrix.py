#!/usr/bin/env python3
"""c76_hreflang_matrix.py -- frozen contract C2 case matrix and its counter.

Runs a candidate offline hreflang audit tool over the frozen case set from
contract C2 (kake round 76) inside an isolated fixture tree per case, compares
the observed (exit, finding-id set) with the case's frozen expected verdict,
and runs the four frozen degenerate constants to prove the matrix can fail
them.

Usage:
    python3 c76_hreflang_matrix.py --root . --tool PATH --revision REV \
        --work DIR [--cases DIR] [--consts DIR] [--min-decided N]
        [--timeout SECONDS]

Case schema (one JSON file per case, see cases/):
    {"name": str, "decided": bool, "derivation": str,
     "manifest": {"version": 1, "pages": [{"id","file","url"}]},
     "files": {relative path: str | {"b64": str}},
     "expected": {"exit": int, "ids": [str]},
     "note": str            # required when decided is false
     "actual": {"exit": int, "ids": [str]}   # selftest fixtures only
    }

Verdict predicate. A case is correct when the tool, invoked as

    <tool> --manifest <fixture>/manifest.json --root <fixture> --json

with cwd and TMPDIR inside its own run directory, emits a parseable JSON report
whose `findings` list carries exactly the expected finding-id set (order and
multiplicity ignored) and exits with the expected code. `hreflang_external_target`
is the contract's informational id: it is excluded from the compared set on
both sides (it is not a policy finding and the contract does not say whether a
run reports it). An undecided case is excluded from decided/correct/wrong and
counted only in `undecided`.

Constants. Four degenerate drop-in tools under consts/ are run over every
decided case. `constants_failed=K/T` counts the constants that fail at least
one decided case. A constant that passes every decided case means the matrix
cannot distinguish it from a correct tool: that is a matrix defect, reported
as `matrix_defect=true`, and `met` is false in that run.

met = (wrong == 0) and (decided >= --min-decided) and
      (constants_failed == number of constants) and (not matrix_defect)

Exit 0 when met, 1 otherwise; 64 on usage.
"""

import argparse
import base64
import collections
import hashlib
import json
import os
import shutil
import subprocess
import sys


class UsageError(Exception):
    pass


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_cases(case_files):
    digest = hashlib.sha256()
    for path in sorted(case_files):
        digest.update(os.path.basename(path).encode("utf-8"))
        digest.update(b"\0")
        with open(path, "rb") as handle:
            digest.update(handle.read())
        digest.update(b"\0")
    return digest.hexdigest()


def finding_id(row):
    if isinstance(row, dict):
        for key in ("id", "finding", "code"):
            value = row.get(key)
            if isinstance(value, str):
                return value
        return None
    if isinstance(row, str):
        return row
    return None


def observed_report(stdout, manifest_page_count, process_exit):
    """Validate the A16 report object and return its observed verdict.

    Amendment A16: a tool that prints nothing must not be scored as clean, so
    the matrix requires a parseable JSON object carrying `version`, `pages`
    (count equal to the manifest's page count), `findings`, `counts` and
    `exit`. Finding ids are compared as a multiset.
    """
    record = {"ok": False, "error": "", "exit_field": None,
              "ids": collections.Counter(), "pages": None}
    try:
        report = json.loads(stdout)
    except (ValueError, TypeError):
        record["error"] = "stdout is not JSON"
        return record
    if not isinstance(report, dict):
        record["error"] = "report is not a JSON object"
        return record
    missing = [key for key in ("version", "pages", "findings", "counts", "exit")
               if key not in report]
    if missing:
        record["error"] = "report lacks %s" % ",".join(missing)
        return record
    pages = report["pages"]
    if isinstance(pages, bool):
        record["error"] = "pages is a bool"
        return record
    if isinstance(pages, list):
        pages_count = len(pages)
    elif isinstance(pages, int):
        pages_count = pages
    else:
        record["error"] = "pages is neither a count nor a list"
        return record
    record["pages"] = pages_count
    if pages_count != manifest_page_count:
        record["error"] = "pages=%d but manifest has %d" % (
            pages_count, manifest_page_count)
        return record
    if not isinstance(report["findings"], list):
        record["error"] = "findings is not a list"
        return record
    if not isinstance(report["counts"], dict):
        record["error"] = "counts is not an object"
        return record
    if not isinstance(report["exit"], int) or isinstance(report["exit"], bool):
        record["error"] = "exit is not an int"
        return record
    if report["exit"] != process_exit:
        record["error"] = "report exit=%r but process exit=%r" % (
            report["exit"], process_exit)
        return record
    ids = collections.Counter()
    for row in report["findings"]:
        value = finding_id(row)
        if value is not None:
            ids[value] += 1
    record["ok"] = True
    record["exit_field"] = report["exit"]
    record["ids"] = ids
    return record


def load_cases(cases_dir):
    if not os.path.isdir(cases_dir):
        raise UsageError("cases dir not found: %s" % cases_dir)
    paths = sorted(
        os.path.join(cases_dir, name)
        for name in os.listdir(cases_dir)
        if name.endswith(".json")
    )
    if not paths:
        raise UsageError("no case files in %s" % cases_dir)
    cases = []
    names = set()
    for path in paths:
        try:
            with open(path, "rb") as handle:
                row = json.loads(handle.read().decode("utf-8"))
        except (OSError, ValueError, UnicodeDecodeError) as exc:
            raise UsageError("unreadable case %s: %s" % (path, exc))
        if not isinstance(row, dict):
            raise UsageError("case %s is not an object" % path)
        for key in ("name", "decided", "manifest", "files", "expected"):
            if key not in row:
                raise UsageError("case %s lacks %r" % (path, key))
        if not isinstance(row["name"], str) or not row["name"]:
            raise UsageError("case %s has a bad name" % path)
        if row["name"] in names:
            raise UsageError("duplicate case name %r" % row["name"])
        names.add(row["name"])
        if not isinstance(row["decided"], bool):
            raise UsageError("case %s: decided must be a bool" % path)
        if not row["decided"] and not row.get("note"):
            raise UsageError("undecided case %s must carry a note" % path)
        expected = row["expected"]
        if not isinstance(expected, dict):
            raise UsageError("case %s: expected must be an object" % path)
        if not isinstance(expected.get("exit"), int):
            raise UsageError("case %s: expected.exit must be an int" % path)
        if not isinstance(expected.get("ids"), list):
            raise UsageError("case %s: expected.ids must be a list" % path)
        if not all(isinstance(item, str) for item in expected["ids"]):
            raise UsageError("case %s: expected.ids must be strings" % path)
        if not isinstance(row["files"], dict):
            raise UsageError("case %s: files must be an object" % path)
        if not isinstance(row["manifest"], dict):
            raise UsageError("case %s: manifest must be an object" % path)
        row["_path"] = path
        cases.append(row)
    return paths, cases


def write_fixture(case, fixture_dir):
    if os.path.exists(fixture_dir):
        shutil.rmtree(fixture_dir)
    os.makedirs(fixture_dir)
    for name, content in sorted(case["files"].items()):
        target = os.path.join(fixture_dir, name)
        parent = os.path.dirname(target)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent)
        if isinstance(content, dict) and "symlink" in content:
            os.symlink(content["symlink"], target)
        elif isinstance(content, dict) and content.get("dir"):
            os.makedirs(target, exist_ok=True)
        else:
            if isinstance(content, dict) and "b64" in content:
                payload = base64.b64decode(content["b64"])
            else:
                payload = str(content).encode("utf-8")
            with open(target, "wb") as handle:
                handle.write(payload)
    with open(os.path.join(fixture_dir, "manifest.json"), "w",
              encoding="utf-8") as handle:
        json.dump(case["manifest"], handle, indent=1, sort_keys=True)
    if "actual" in case:
        with open(os.path.join(fixture_dir, "actual.json"), "w",
                  encoding="utf-8") as handle:
            json.dump(case["actual"], handle, indent=1, sort_keys=True)


def run_tool(tool, fixture_dir, run_dir, timeout):
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir)
    os.makedirs(os.path.join(run_dir, "tmp"))
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(run_dir, "tmp")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    argv = [
        sys.executable, tool,
        "--manifest", os.path.join(fixture_dir, "manifest.json"),
        "--root", fixture_dir,
        "--json",
    ]
    try:
        proc = subprocess.run(
            argv, cwd=run_dir, env=env, timeout=timeout,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
    except subprocess.TimeoutExpired:
        return {"exit": None, "stdout": b"", "stderr": b"timeout",
                "timed_out": True}
    except OSError as exc:
        return {"exit": None, "stdout": b"", "stderr": str(exc).encode(),
                "timed_out": False}
    return {"exit": proc.returncode, "stdout": proc.stdout,
            "stderr": proc.stderr, "timed_out": False}


def evaluate_case(case, tool, work, index, timeout):
    fixture = os.path.join(work, "fixtures", "%02d-%s" % (index, case["name"]))
    run_dir = os.path.join(work, "runs", "%02d-%s" % (index, case["name"]))
    write_fixture(case, fixture)
    result = run_tool(tool, fixture, run_dir, timeout)
    manifest_pages = case["manifest"].get("pages")
    manifest_count = len(manifest_pages) if isinstance(manifest_pages, list) else 0
    observed = observed_report(
        result["stdout"].decode("utf-8", "replace"), manifest_count,
        result["exit"])
    expected = case["expected"]
    expected_ids = collections.Counter(expected["ids"])
    record = {
        "name": case["name"],
        "decided": case["decided"],
        "expected_exit": expected["exit"],
        "expected_ids": sorted(expected_ids.elements()),
        "observed_exit": result["exit"],
        "observed_ids": sorted(observed["ids"].elements()),
        "pages": observed["pages"],
        "manifest_pages": manifest_count,
        "json": observed["ok"],
        "shape_error": observed["error"],
        "exit_field": observed["exit_field"],
        "timed_out": result["timed_out"],
        "stderr_tail": result["stderr"].decode("utf-8", "replace")[-400:],
    }
    if not case["decided"]:
        record["verdict"] = "undecided"
    elif (result["exit"] == expected["exit"] and observed["ok"]
          and observed["ids"] == expected_ids):
        record["verdict"] = "correct"
    else:
        record["verdict"] = "wrong"
    return record


def run_cases(cases, tool, work, timeout):
    records = []
    for index, case in enumerate(cases):
        records.append(evaluate_case(case, tool, work, index, timeout))
    return records


def tally(records):
    decided = [row for row in records if row["decided"]]
    return {
        "cases": len(records),
        "decided": len(decided),
        "correct": sum(1 for row in decided if row["verdict"] == "correct"),
        "wrong": sum(1 for row in decided if row["verdict"] == "wrong"),
        "undecided": sum(1 for row in records if not row["decided"]),
    }


def discover_constants(consts_dir):
    if not os.path.isdir(consts_dir):
        raise UsageError("consts dir not found: %s" % consts_dir)
    paths = sorted(
        os.path.join(consts_dir, name)
        for name in os.listdir(consts_dir)
        if name.endswith(".py") and name.startswith("const_")
    )
    if not paths:
        raise UsageError("no const_*.py in %s" % consts_dir)
    return paths


def run_constants(consts, cases, work, timeout):
    results = []
    for index, path in enumerate(consts):
        sub = os.path.join(work, "consts", "%02d-%s" % (
            index, os.path.splitext(os.path.basename(path))[0]))
        records = run_cases(cases, path, sub, timeout)
        verdicts = tally(records)
        failed_cases = sorted(
            row["name"] for row in records
            if row["decided"] and row["verdict"] == "wrong")
        results.append({
            "name": os.path.basename(path),
            "path": path,
            "tally": verdicts,
            "failures": len(failed_cases),
            "first_failed": failed_cases[:3],
            "passes_all": verdicts["wrong"] == 0 and verdicts["decided"] > 0,
        })
    return results


def emit_run(tool, cases_hash, records, constants, revision_note, min_decided):
    verdicts = tally(records)
    constants_failed = sum(1 for row in constants if row["failures"] > 0)
    matrix_defect = any(row["passes_all"] for row in constants)
    met = (
        verdicts["wrong"] == 0
        and verdicts["decided"] >= min_decided
        and constants_failed == len(constants)
        and not matrix_defect
        and verdicts["decided"] > 0
    )
    print("tool=%s" % os.path.abspath(tool))
    print("tool_sha256=%s" % sha256_file(tool))
    print("cases_sha256=%s" % cases_hash)
    print(revision_note)
    for row in records:
        print(
            "case %s expected=exit%d ids=%s observed=exit%s ids=%s "
            "pages=%s/%s json=%s verdict=%s%s"
            % (row["name"], row["expected_exit"],
               json.dumps(row["expected_ids"]), row["observed_exit"],
               json.dumps(row["observed_ids"]),
               row["pages"] if row["pages"] is not None else "-",
               row["manifest_pages"],
               "ok" if row["json"] else "bad", row["verdict"],
               "" if row["json"] else " shape=%s" % (row["shape_error"] or "?")))
    for row in constants:
        print("constant %s failed=%d/%d first=%s passes_all=%s"
              % (row["name"], row["failures"], verdicts["decided"],
                 json.dumps(row["first_failed"]),
                 "yes" if row["passes_all"] else "no"))
    if matrix_defect:
        print("matrix_defect=true constants_pass_all=%s"
              % json.dumps([row["name"] for row in constants
                            if row["passes_all"]]))
    print(
        "cases=%d decided=%d correct=%d wrong=%d undecided=%d "
        "constants_failed=%d/%d met=%s"
        % (verdicts["cases"], verdicts["decided"], verdicts["correct"],
           verdicts["wrong"], verdicts["undecided"], constants_failed,
           len(constants), "true" if met else "false"))
    return met, verdicts


def prepare_work(work):
    if not work or os.path.abspath(work) in ("/", os.path.expanduser("~")):
        raise UsageError("refusing to use %r as --work" % work)
    if os.path.exists(work):
        shutil.rmtree(work)
    os.makedirs(work)


def revision_note(root, revision):
    note = "revision=%s" % (revision or "-")
    if revision:
        try:
            proc = subprocess.run(
                ["git", "-C", root, "cat-file", "-e", revision + "^{commit}"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
            ok = proc.returncode == 0
        except (OSError, subprocess.TimeoutExpired):
            ok = False
        note += " revision_ok=%s" % ("yes" if ok else "no")
    try:
        proc = subprocess.run(
            ["git", "-C", root, "rev-parse", "HEAD"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        head = proc.stdout.decode("utf-8", "replace").strip() or "-"
    except (OSError, subprocess.TimeoutExpired):
        head = "-"
    note += " head=%s" % head
    return note


# --------------------------------------------------------------- selftest
SELFTEST_STUB = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
root = args[args.index("--root") + 1] if "--root" in args else "."
mode = %r
with open(os.path.join(root, "actual.json"), "r", encoding="utf-8") as fh:
    actual = json.load(fh)
with open(os.path.join(root, "manifest.json"), "r", encoding="utf-8") as fh:
    manifest = json.load(fh)
ids = list(actual["ids"])
code = int(actual["exit"])
if mode == "wrong":
    ids = []
    code = 0 if code != 0 else 1
elif mode == "exit_flip":
    code = 0 if code != 0 else 1
elif mode == "extra_id":
    if "hreflang_nonreciprocal" not in ids:
        ids.append("hreflang_nonreciprocal")
elif mode == "missing_id":
    ids = ids[:-1]
print(json.dumps({"version": 1, "pages": len(manifest.get("pages", [])),
                  "findings": [{"id": item} for item in ids],
                  "counts": {}, "exit": code}))
sys.exit(code)
'''

SELFTEST_NOOP = r'''#!/usr/bin/env python3
import sys
sys.exit(0)
'''

SELFTEST_ALWAYS_CLEAN = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
root = args[args.index("--root") + 1] if "--root" in args else "."
with open(os.path.join(root, "manifest.json"), "r", encoding="utf-8") as fh:
    manifest = json.load(fh)
print(json.dumps({"version": 1, "pages": len(manifest.get("pages", [])),
                  "findings": [], "counts": {}, "exit": 0}))
sys.exit(0)
'''

SELFTEST_MUTATOR = r'''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
root = args[args.index("--root") + 1] if "--root" in args else "."
with open(os.path.join(root, "page.html"), "r", encoding="utf-8") as fh:
    text = fh.read()
with open(os.path.join(root, "manifest.json"), "r", encoding="utf-8") as fh:
    manifest = json.load(fh)
ids = ["hreflang_invalid_tag"] if "BAD" in text else []
code = 1 if ids else 0
with open(os.path.join(root, "page.html"), "a", encoding="utf-8") as fh:
    fh.write("BAD")
print(json.dumps({"version": 1, "pages": len(manifest.get("pages", [])),
                  "findings": [{"id": item} for item in ids],
                  "counts": {}, "exit": code}))
sys.exit(code)
'''


def selftest_case(name, decided, manifest, files, exit_code, ids, actual=None,
                  note=None):
    row = {
        "name": name,
        "decided": decided,
        "derivation": "selftest fixture",
        "manifest": manifest,
        "files": files,
        "expected": {"exit": exit_code, "ids": sorted(ids)},
    }
    if actual is not None:
        row["actual"] = {"exit": actual[0], "ids": sorted(actual[1])}
    if note:
        row["note"] = note
    return row


def write_case_dir(path, cases):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    for row in cases:
        with open(os.path.join(path, row["name"] + ".json"), "w",
                  encoding="utf-8") as handle:
            json.dump(row, handle, indent=1, sort_keys=True)


def selftest(work):
    base = os.path.join(work, "selftest")
    if os.path.exists(base):
        shutil.rmtree(base)
    os.makedirs(os.path.join(base, "tools"))
    tools = {}
    for mode in ("actual", "wrong", "exit_flip", "extra_id", "missing_id"):
        path = os.path.join(base, "tools", "stub_%s.py" % mode)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(SELFTEST_STUB % mode)
        tools[mode] = path
    noop = os.path.join(base, "tools", "const_noop.py")
    with open(noop, "w", encoding="utf-8") as handle:
        handle.write(SELFTEST_NOOP)
    always_clean = os.path.join(base, "tools", "const_always_clean.py")
    with open(always_clean, "w", encoding="utf-8") as handle:
        handle.write(SELFTEST_ALWAYS_CLEAN)
    mutator = os.path.join(base, "tools", "stub_mutator.py")
    with open(mutator, "w", encoding="utf-8") as handle:
        handle.write(SELFTEST_MUTATOR)

    manifest_a = {"version": 1, "pages": [
        {"id": "a", "file": "a.html", "url": "https://alpha.example/a"}]}
    manifest_ab = {"version": 1, "pages": [
        {"id": "a", "file": "a.html", "url": "https://alpha.example/a"},
        {"id": "b", "file": "b.html", "url": "https://beta.example/b"}]}
    truth = [
        selftest_case("clean", True, manifest_a, {"a.html": "<html></html>"},
                      0, [], actual=(0, [])),
        selftest_case("policy", True, manifest_a, {"a.html": "<html></html>"},
                      1, ["hreflang_invalid_tag"],
                      actual=(1, ["hreflang_invalid_tag"])),
        selftest_case("fault", True, manifest_ab, {"a.html": "<html></html>"},
                      2, ["input_unreadable"], actual=(2, ["input_unreadable"])),
        selftest_case("multi", True, manifest_ab,
                      {"a.html": "<html></html>", "b.html": "<html></html>"},
                      1, ["hreflang_nonreciprocal", "hreflang_self_missing"],
                      actual=(1, ["hreflang_nonreciprocal",
                                  "hreflang_self_missing"])),
    ]
    truth_dir = os.path.join(base, "cases-truth")
    write_case_dir(truth_dir, truth)

    checks = []

    def record(label, ok, detail):
        checks.append((label, bool(ok), detail))

    paths, cases = load_cases(truth_dir)
    run_work = os.path.join(base, "run-truth")
    prepare_work(run_work)
    records = run_cases(cases, tools["actual"], run_work, 30)
    verdicts = tally(records)
    record("truth-set-correct",
           verdicts["decided"] == 4 and verdicts["correct"] == 4
           and verdicts["wrong"] == 0,
           json.dumps(verdicts))

    for mode in ("wrong", "exit_flip", "extra_id", "missing_id"):
        run_work = os.path.join(base, "run-" + mode)
        prepare_work(run_work)
        records = run_cases(cases, tools[mode], run_work, 30)
        verdicts = tally(records)
        record("%s-detected" % mode.replace("_", "-"),
               verdicts["wrong"] >= 1, json.dumps(verdicts))

    # a deliberately wrong expected verdict must be a wrong case, not a pass
    wrong_expected = [dict(row) for row in truth]
    wrong_expected[1] = dict(wrong_expected[1])
    wrong_expected[1]["expected"] = {"exit": 0, "ids": []}
    wrong_dir = os.path.join(base, "cases-wrong-expected")
    write_case_dir(wrong_dir, wrong_expected)
    paths, cases = load_cases(wrong_dir)
    run_work = os.path.join(base, "run-wrong-expected")
    prepare_work(run_work)
    records = run_cases(cases, tools["actual"], run_work, 30)
    verdicts = tally(records)
    record("deliberately-wrong-expected-detected",
           verdicts["wrong"] >= 1 and verdicts["correct"] == 3,
           json.dumps(verdicts))

    # undecided cases are excluded, never counted as passes
    undecided = [dict(row) for row in truth]
    undecided[3] = dict(undecided[3])
    undecided[3]["decided"] = False
    undecided[3]["note"] = "selftest undecided"
    undecided_dir = os.path.join(base, "cases-undecided")
    write_case_dir(undecided_dir, undecided)
    paths, cases = load_cases(undecided_dir)
    run_work = os.path.join(base, "run-undecided")
    prepare_work(run_work)
    records = run_cases(cases, tools["actual"], run_work, 30)
    verdicts = tally(records)
    excluded = [row for row in records if not row["decided"]]
    record("undecided-excluded",
           verdicts["undecided"] == 1 and verdicts["decided"] == 3
           and verdicts["correct"] == 3
           and excluded and excluded[0]["verdict"] == "undecided",
           json.dumps(verdicts))

    # a constant that fails a policy case is not a matrix defect ...
    paths, truth_cases = load_cases(truth_dir)
    run_work = os.path.join(base, "run-noop-truth")
    prepare_work(run_work)
    consts = run_constants([noop], truth_cases, run_work, 30)
    failures = consts[0]["failures"]
    defect = consts[0]["passes_all"]
    record("constant-fails-policy-case", failures >= 1 and not defect,
           "failed=%d passes_all=%s" % (failures, defect))

    # ... and a constant that passes every case is a matrix defect
    clean_only = [selftest_case("clean-%d" % i, True, manifest_a,
                                {"a.html": "<html></html>"}, 0, [])
                  for i in range(2)]
    clean_dir = os.path.join(base, "cases-clean-only")
    write_case_dir(clean_dir, clean_only)
    paths, clean_cases = load_cases(clean_dir)
    run_work = os.path.join(base, "run-noop-clean")
    prepare_work(run_work)
    consts = run_constants([always_clean], clean_cases, run_work, 30)
    record("all-pass-constant-is-matrix-defect",
           consts[0]["passes_all"] and consts[0]["failures"] == 0,
           "passes_all=%s failed=%d" % (consts[0]["passes_all"],
                                        consts[0]["failures"]))

    # fixture isolation: a tool that mutates its own tree must not leak
    mut_cases = [
        selftest_case("iso-1", True, manifest_a,
                      {"page.html": "<html>good</html>"}, 0, [],
                      actual=(0, [])),
        selftest_case("iso-2", True, manifest_a,
                      {"page.html": "<html>good</html>"}, 0, [],
                      actual=(0, [])),
    ]
    for row in mut_cases:
        row["manifest"] = {"version": 1, "pages": [
            {"id": "a", "file": "page.html", "url": "https://alpha.example/a"}]}
    mut_dir = os.path.join(base, "cases-isolation")
    write_case_dir(mut_dir, mut_cases)
    paths, mut_loaded = load_cases(mut_dir)
    run_work = os.path.join(base, "run-isolation")
    prepare_work(run_work)
    records = run_cases(mut_loaded, mutator, run_work, 30)
    verdicts = tally(records)
    record("fixture-isolation",
           verdicts["correct"] == 2 and verdicts["wrong"] == 0,
           json.dumps(verdicts))

    # determinism: the same scenario twice yields the same summary
    paths, det_cases = load_cases(truth_dir)
    run_a = os.path.join(base, "run-det-a")
    run_b = os.path.join(base, "run-det-b")
    prepare_work(run_a)
    prepare_work(run_b)
    left = tally(run_cases(det_cases, tools["actual"], run_a, 30))
    right = tally(run_cases(det_cases, tools["actual"], run_b, 30))
    record("determinism", left == right, json.dumps([left, right]))

    passed = sum(1 for _label, ok, _detail in checks if ok)
    for label, ok, detail in checks:
        print("selftest-%s %s %s" % (label, "ok" if ok else "FAIL", detail))
    print("selftest %d/%d passed" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


# ------------------------------------------------------------------- main
def main(argv=None):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--root", default=".")
    parser.add_argument("--tool")
    parser.add_argument("--revision", default="")
    parser.add_argument("--work")
    parser.add_argument("--cases")
    parser.add_argument("--consts")
    parser.add_argument("--min-decided", type=int, default=24)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--selftest", action="store_true")
    try:
        args, extra = parser.parse_known_args(argv)
    except SystemExit:
        return 64
    if extra:
        sys.stderr.write("unrecognized arguments: %s\n" % " ".join(extra))
        return 64
    if not args.work:
        sys.stderr.write("--work is required\n")
        return 64
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cases_dir = args.cases or os.path.join(script_dir, "cases")
    consts_dir = args.consts or os.path.join(script_dir, "consts")
    try:
        prepare_work(args.work)
        if args.selftest:
            return selftest(args.work)
        if not args.tool:
            sys.stderr.write("--tool is required\n")
            return 64
        tool = args.tool
        if not os.path.isabs(tool):
            tool = os.path.join(os.path.abspath(args.root), tool)
        if not os.path.isfile(tool):
            sys.stderr.write("tool not found: %s\n" % tool)
            return 64
        case_paths, cases = load_cases(cases_dir)
        consts = discover_constants(consts_dir)
        cases_hash = sha256_cases(case_paths)
        records = run_cases(cases, tool, args.work, args.timeout)
        constants = run_constants(
            consts, cases, args.work, args.timeout)
        met, _verdicts = emit_run(
            tool, cases_hash, records, constants,
            revision_note(os.path.abspath(args.root), args.revision),
            args.min_decided)
    except UsageError as exc:
        sys.stderr.write("%s\n" % exc)
        return 64
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
