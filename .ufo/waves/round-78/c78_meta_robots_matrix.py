#!/usr/bin/env python3
"""c78_meta_robots_matrix.py -- frozen C3 case matrix and its counter.

Contract: round-78 C3 + contract-amendment-1.md (A1..A5) +
contract-amendment-2.md (B1..B6).

Predicate (amendment 2 B5):

    met <=> cases == <frozen count> and decided == <frozen count>
            and correct == <frozen count> and constants_failed == 4
            and selftest_ok

`cases` is taken from the frozen case-id list FROZEN_CASE_IDS, never from a
directory count; the --cases directory must hold exactly those ids (missing or
extra ids are named findings and force met=false).

Interface (amendment 2 B1/B2): the manifest handed to the tool carries no
`expect` -- {"schema","agents","checks":[{id,path,url}]}.  With --json the tool
prints one JSON object:

    {"version":1,"checks":[{"id","effective":[...],"findings":[...]}]}

or, on an input/check fault, {"version":1,"error":"<code>"} with exit 2.

Comparison (B3): a normal case is correct iff the tool's exit code, its sorted
`effective` list and its sorted `findings` list all equal the case's
expect.json.  An exit-2 case is correct iff the exit is 2 and the report's
`error` equals expect.json's `error`.

Selftest (B5): the tool's own --selftest is run from the same revision blob; it
must exit 0 and print a final `selftest: P/T passed` line with P == T >= 40.

Invocation:

    python3 -B .ufo/waves/round-78/c78_meta_robots_matrix.py --root . \
        --tool-revision <rev> --cases .ufo/waves/round-78/cases \
        --consts .ufo/waves/round-78/consts --work <scratch>

The tool blob is extracted with `git show <rev>:scripts/meta_robots_audit.py`;
the working-tree copy is never executed for a receipt.

Exit: 0 met, 1 measured defect, 2 unevaluable (tool absent at the revision or
unreadable cases/consts), 64 usage.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

TOOL_PATH = "scripts/meta_robots_audit.py"
CASE_FILES = ("expect.json", "manifest.json", "page.html")

# Amendment 3 C1 corrects amendment 2's stale 34-count literal to 36.
FROZEN_CASE_IDS = (
    "g01_absent_tag", "g02_noindex", "g03_none_expansion", "g04_all_default",
    "g05_index_follow_one", "g06_conflicting_noindex",
    "g07_conflicting_nofollow", "g08_max_snippet_two",
    "g09_max_image_preview_two", "g10_max_video_no_limit",
    "g11_max_snippet_invalid", "g12a_unavailable_datetime",
    "g12b_unavailable_date", "g12c_unavailable_rfc822",
    "g13_unavailable_invalid", "g14_uppercase", "g15_empty_content",
    "g16_unknown_directive", "g17_googlebot_ignored",
    "g18_googlebot_with_agents", "g19_body_tag_respected",
    "g21_self_closing", "g22_single_quotes", "g23_noarchive_ignored",
    "g24_trailing_comma", "g25_nosnippet_dominates",
    "g26_max_snippet_zero_video_minus_one", "g27_indexifembedded",
    "g28_within_content_conflict", "g29_max_image_preview_none",
    "g30_max_snippet_minus_one", "g31_missing_content",
    "g32_nocache_ignored", "g33_lowercase_t_z",
    "g34_missing_file_exit2", "g35_duplicate_id_exit2",
)
DECLARED_CASE_COUNT = 36
SELFTEST_RE = re.compile(r"^selftest:\s*(\d+)/(\d+)\s+passed\s*$")


class UsageError(Exception):
    pass


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def digest_cases(cases_dir, names):
    digest = hashlib.sha256()
    for name in names:
        for member in CASE_FILES:
            path = os.path.join(cases_dir, name, member)
            digest.update(name.encode("utf-8"))
            digest.update(b"/")
            digest.update(member.encode("utf-8"))
            digest.update(b"\0")
            if os.path.isfile(path):
                with open(path, "rb") as handle:
                    digest.update(handle.read())
            digest.update(b"\0")
    return digest.hexdigest()


def git(root, args):
    try:
        proc = subprocess.run(
            ["git", "-C", root] + args, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=120)
    except OSError as exc:
        return {"rc": 127, "out": b"", "err": str(exc).encode()}
    except subprocess.TimeoutExpired:
        return {"rc": 124, "out": b"", "err": b"git timed out"}
    return {"rc": proc.returncode, "out": proc.stdout, "err": proc.stderr}


def reset_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.unlink(path)
    os.makedirs(path)


def extract_tool(root, revision, work):
    spec = "%s:%s" % (revision, TOOL_PATH)
    show = git(root, ["show", spec])
    blob = git(root, ["rev-parse", spec])
    if show["rc"] != 0:
        return {"ok": False, "rc": show["rc"],
                "error": show["err"].decode("utf-8", "replace").strip()[:400],
                "blob": None, "sha256": None, "path": None, "bytes": 0}
    target = os.path.join(work, "tool")
    reset_dir(target)
    path = os.path.join(target, "meta_robots_audit.py")
    with open(path, "wb") as handle:
        handle.write(show["out"])
    return {"ok": True, "rc": 0, "error": "",
            "blob": blob["out"].decode("utf-8", "replace").strip() or None,
            "sha256": sha256_file(path), "path": path,
            "bytes": len(show["out"])}


def load_json(path):
    try:
        with open(path, "rb") as handle:
            return json.loads(handle.read().decode("utf-8")), None
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        return None, str(exc)


def load_cases(cases_dir):
    if not os.path.isdir(cases_dir):
        raise UsageError("cases dir not found: %s" % cases_dir)
    present = sorted(name for name in os.listdir(cases_dir)
                     if os.path.isdir(os.path.join(cases_dir, name)))
    missing = [name for name in FROZEN_CASE_IDS if name not in present]
    extra = [name for name in present if name not in FROZEN_CASE_IDS]
    cases = []
    for name in FROZEN_CASE_IDS:
        case_dir = os.path.join(cases_dir, name)
        reasons = []
        record = {"name": name, "dir": case_dir, "decided": False,
                  "reason": "", "check_id": name, "exit": None,
                  "effective": None, "findings": None, "error": None}
        if not os.path.isdir(case_dir):
            record["reason"] = "case directory missing"
            cases.append(record)
            continue
        manifest, manifest_error = load_json(
            os.path.join(case_dir, "manifest.json"))
        expect, expect_error = load_json(os.path.join(case_dir, "expect.json"))
        if manifest_error:
            reasons.append("manifest: %s" % manifest_error)
        if expect_error:
            reasons.append("expect: %s" % expect_error)
        if isinstance(manifest, dict):
            if manifest.get("schema") != "kake-meta-robots-manifest/v1":
                reasons.append("manifest schema")
            checks = manifest.get("checks")
            if not isinstance(checks, list):
                reasons.append("manifest checks")
        elif manifest is not None:
            reasons.append("manifest is not an object")
        if isinstance(expect, dict):
            record["exit"] = expect.get("exit")
            if not isinstance(record["exit"], int) or isinstance(
                    record["exit"], bool):
                reasons.append("expect.exit is not an int")
                record["exit"] = None
            elif record["exit"] == 2:
                if not isinstance(expect.get("error"), str):
                    reasons.append("exit-2 case lacks expect.error")
                else:
                    record["error"] = expect["error"]
            else:
                for key in ("effective", "findings"):
                    value = expect.get(key)
                    if not (isinstance(value, list)
                            and all(isinstance(item, str) for item in value)):
                        reasons.append("expect.%s is not a string list" % key)
                if not reasons:
                    record["effective"] = sorted(expect["effective"])
                    record["findings"] = sorted(expect["findings"])
                    checks = manifest.get("checks", []) if isinstance(
                        manifest, dict) else []
                    if not (len(checks) == 1 and isinstance(checks[0], dict)
                            and checks[0].get("id") == name
                            and isinstance(checks[0].get("path"), str)):
                        reasons.append(
                            "manifest must carry exactly one check with this id")
                    else:
                        page = os.path.join(case_dir, checks[0]["path"])
                        if not os.path.isfile(page):
                            reasons.append("page.html missing")
        elif expect is not None:
            reasons.append("expect.json is not an object")
        record["decided"] = not reasons
        record["reason"] = "; ".join(reasons)
        cases.append(record)
    return cases, missing, extra


def run_tool(tool, case_dir, run_dir, timeout, extra_args=()):
    reset_dir(run_dir)
    tmp_dir = os.path.join(run_dir, "tmp")
    os.makedirs(tmp_dir)
    env = dict(os.environ)
    env["TMPDIR"] = tmp_dir
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    argv = [sys.executable, "-B", tool] + list(extra_args)
    try:
        proc = subprocess.run(
            argv, cwd=run_dir, env=env, timeout=timeout,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.TimeoutExpired:
        return {"exit": None, "stdout": b"", "stderr": b"timeout"}
    except OSError as exc:
        return {"exit": None, "stdout": b"", "stderr": str(exc).encode()}
    return {"exit": proc.returncode, "stdout": proc.stdout,
            "stderr": proc.stderr}


def audit_case(tool, case, run_dir, timeout):
    # Only page payload and an unlabelled manifest cross the oracle boundary.
    parent = os.path.dirname(os.path.dirname(os.path.dirname(run_dir)))
    source = os.path.join(parent, "inputs", os.urandom(16).hex())
    os.makedirs(source)
    manifest, error = load_json(os.path.join(case["dir"], "manifest.json"))
    if error:
        raise UsageError(error)
    for check in manifest["checks"]:
        check["id"] = "check"
        check["url"] = "https://example.test/page"
        check.pop("expect", None)
    with open(os.path.join(source, "manifest.json"), "w", encoding="utf-8") as handle:
        json.dump(manifest, handle)
    page = os.path.join(case["dir"], "page.html")
    if os.path.isfile(page):
        shutil.copyfile(page, os.path.join(source, "page.html"))
    try:
        return run_tool(
            tool, source, run_dir, timeout,
            extra_args=["--manifest", os.path.join(source, "manifest.json"),
                        "--root", source, "--json"])
    finally:
        shutil.rmtree(source)


def parse_report(stdout):
    try:
        report = json.loads(stdout.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    return report if isinstance(report, dict) else None


def judge(case, result):
    if result["exit"] is None:
        return {"correct": False, "observed": None,
                "reason": "no exit: %s"
                          % result["stderr"].decode("utf-8", "replace")[-160:]}
    report = parse_report(result["stdout"])
    if report is None:
        return {"correct": False, "observed": None,
                "reason": "unparseable report: %s"
                          % result["stderr"].decode("utf-8", "replace")[-160:]}
    if case["exit"] == 2:
        observed = {"exit": result["exit"], "error": report.get("error"),
                    "version": report.get("version")}
        if result["exit"] != 2:
            return {"correct": False, "observed": observed,
                    "reason": "exit %s != 2" % result["exit"]}
        if report.get("error") != case["error"]:
            return {"correct": False, "observed": observed,
                    "reason": "error %r != %r"
                              % (report.get("error"), case["error"])}
        return {"correct": True, "observed": observed, "reason": ""}
    checks = report.get("checks")
    observed = {"exit": result["exit"], "version": report.get("version"),
                "checks": checks if isinstance(checks, list) else None}
    if result["exit"] != case["exit"]:
        return {"correct": False, "observed": observed,
                "reason": "exit %s != %s" % (result["exit"], case["exit"])}
    if report.get("version") != 1:
        return {"correct": False, "observed": observed,
                "reason": "version %r != 1" % report.get("version")}
    if not (isinstance(checks, list) and len(checks) == 1
            and isinstance(checks[0], dict)):
        return {"correct": False, "observed": observed,
                "reason": "report must carry exactly one check"}
    row = checks[0]
    if row.get("id") != case["check_id"]:
        return {"correct": False, "observed": observed,
                "reason": "check id %r != %r"
                          % (row.get("id"), case["check_id"])}
    effective = row.get("effective")
    findings = row.get("findings")
    if effective != case["effective"]:
        return {"correct": False, "observed": observed,
                "reason": "effective %s != %s"
                          % (json.dumps(effective), json.dumps(
                              case["effective"]))}
    if findings != case["findings"]:
        return {"correct": False, "observed": observed,
                "reason": "findings %s != %s"
                          % (json.dumps(findings), json.dumps(
                              case["findings"]))}
    return {"correct": True, "observed": observed, "reason": ""}


def run_cases(tool, cases, work, label, timeout):
    records = []
    for case in cases:
        if not case["decided"]:
            records.append({"name": case["name"], "decided": False,
                            "correct": False, "reason": case["reason"],
                            "observed": None})
            continue
        run_dir = os.path.join(work, "runs", label, os.urandom(16).hex())
        result = audit_case(tool, case, run_dir, timeout)
        verdict = judge(dict(case, check_id="check"), result)
        records.append({"name": case["name"], "decided": True,
                        "correct": verdict["correct"],
                        "reason": verdict["reason"],
                        "observed": verdict["observed"]})
    return records


def tally(records):
    decided = [row for row in records if row["decided"]]
    return {"cases": len(records), "decided": len(decided),
            "correct": sum(1 for row in decided if row["correct"]),
            "wrong": sum(1 for row in decided if not row["correct"])}


def discover_constants(consts_dir):
    if not os.path.isdir(consts_dir):
        raise UsageError("consts dir not found: %s" % consts_dir)
    paths = sorted(os.path.join(consts_dir, name)
                   for name in os.listdir(consts_dir) if name.endswith(".py"))
    if not paths:
        raise UsageError("no constants under %s" % consts_dir)
    return paths


def run_tool_selftest(tool, work, timeout):
    run_dir = os.path.join(work, "tool-selftest")
    result = run_tool(tool, run_dir, run_dir, timeout,
                      extra_args=["--selftest"])
    text = result["stdout"].decode("utf-8", "replace")
    passed = total = None
    lines = text.strip().splitlines()
    match = SELFTEST_RE.fullmatch(lines[-1]) if lines else None
    if match:
        passed, total = int(match.group(1)), int(match.group(2))
    ok = (result["exit"] == 0 and passed is not None and passed == total
          and total >= 40)
    return {"ok": ok, "exit": result["exit"], "passed": passed,
            "total": total,
            "tail": text.strip().splitlines()[-3:] if text.strip() else []}


def predicate(verdicts, constants_failed, selftest_ok):
    return (verdicts["cases"] == DECLARED_CASE_COUNT
            and verdicts["decided"] == DECLARED_CASE_COUNT
            and verdicts["correct"] == DECLARED_CASE_COUNT
            and constants_failed == 4
            and selftest_ok)


def prepare_work(work, root):
    work = os.path.abspath(work)
    if work in ("/", os.path.expanduser("~")) or root.startswith(work + os.sep):
        raise UsageError("refusing to use %r as --work" % work)
    os.makedirs(work, exist_ok=True)
    return work


def run_matrix(opts):
    root = os.path.abspath(opts.root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cases_dir = os.path.abspath(opts.cases or os.path.join(script_dir, "cases"))
    consts_dir = os.path.abspath(opts.consts or os.path.join(
        script_dir, "consts"))
    work = prepare_work(opts.work, root)
    cases, missing, extra = load_cases(cases_dir)
    constants = discover_constants(consts_dir)
    revision = opts.tool_revision
    tool = extract_tool(root, revision, work)
    cases_hash = digest_cases(cases_dir, list(FROZEN_CASE_IDS))
    if not tool["ok"]:
        print("C3v1 revision=%s cases=%d decided=0 correct=0 wrong=0 "
              "constants_failed=0/%d met=false"
              % (revision, len(FROZEN_CASE_IDS), len(constants)))
        print("tool_absent rc=%d error=%s" % (tool["rc"], tool["error"] or "-"))
        print("cases_sha256=%s" % cases_hash)
        return 2
    records = run_cases(tool["path"], cases, work, "tool", opts.timeout)
    verdicts = tally(records)
    const_records = []
    for path in constants:
        name = os.path.basename(path)
        rows = run_cases(path, cases, work, "const-" + name, opts.timeout)
        failed = sorted(row["name"] for row in rows
                        if row["decided"] and not row["correct"])
        const_records.append({"name": name, "failed": failed,
                              "tally": tally(rows)})
    constants_failed = sum(1 for row in const_records if row["failed"])
    selftest = run_tool_selftest(tool["path"], work, opts.timeout)
    adversary = os.path.join(script_dir, "w1", "ExecC3Matrix",
                             "echo_sibling_expect.py")
    sibling_rows = run_cases(adversary, cases, work, "sibling-label", opts.timeout)
    sibling_failed = any(row["decided"] and not row["correct"]
                         for row in sibling_rows)
    print("sibling_expect_control_failed=%s" % str(sibling_failed).lower())
    met = (predicate(verdicts, constants_failed, selftest["ok"])
           and not missing and not extra and sibling_failed)
    print("C3v1 revision=%s cases=%d decided=%d correct=%d wrong=%d "
          "constants_failed=%d/%d met=%s"
          % (revision, verdicts["cases"], verdicts["decided"],
             verdicts["correct"], verdicts["wrong"], constants_failed,
             len(const_records), "true" if met else "false"))
    print("selftest_ok=%s selftest=%s/%s selftest_exit=%s selftest_tail=%s"
          % ("true" if selftest["ok"] else "false",
             selftest["passed"], selftest["total"], selftest["exit"],
             json.dumps(selftest["tail"])))
    print("case_set frozen=%d declared=%d missing=%s extra=%s"
          % (len(FROZEN_CASE_IDS), DECLARED_CASE_COUNT,
             json.dumps(missing), json.dumps(extra)))
    if missing or extra:
        print("finding case_set_mismatch")
    print("tool_blob=%s tool_sha256=%s tool_bytes=%d cases_sha256=%s"
          % (tool["blob"] or "-", tool["sha256"] or "-", tool["bytes"],
             cases_hash))
    for row in records:
        if not row["decided"]:
            print("case %s verdict=undecided reason=%s"
                  % (row["name"], row["reason"]))
            continue
        print("case %s verdict=%s%s"
              % (row["name"], "correct" if row["correct"] else "wrong",
                 "" if row["correct"] else " reason=%s" % row["reason"]))
    for row in const_records:
        print("const %s failed=%d/%d first=%s passes_all=%s"
              % (row["name"], len(row["failed"]), row["tally"]["decided"],
                 json.dumps(row["failed"][:4]),
                 "no" if row["failed"] else "yes"))
    return 0 if met else 1


def selftest(work):
    os.makedirs(work, exist_ok=True)
    checks = []

    def check(name, got, want):
        checks.append({"name": name, "ok": got == want, "got": got,
                       "want": want})

    def judge_one(case, report, process_exit):
        result = {"exit": process_exit,
                  "stdout": json.dumps(report).encode("utf-8"), "stderr": b""}
        return judge(case, result)["correct"]

    def normal(effective, findings):
        return {"exit": 0 if not findings else 1, "check_id": "c",
                "effective": sorted(effective), "findings": sorted(findings),
                "error": None}

    def report_of(effective, findings):
        return {"version": 1, "checks": [{"id": "c",
                                          "effective": list(effective),
                                          "findings": list(findings)}]}

    base = normal(["follow", "index"], [])
    check("clean-correct", judge_one(base, report_of(["follow", "index"], []),
                                     0), True)
    finding = normal([], ["meta_robots_invalid_value"])
    check("finding-correct",
          judge_one(finding,
                    report_of([], ["meta_robots_invalid_value"]), 1), True)
    check("wrong-effective-only",
          judge_one(base, report_of(["noindex"], []), 0), False)
    check("wrong-findings-only",
          judge_one(normal([], ["meta_robots_invalid_value"]),
                    report_of([], []), 1), False)
    check("wrong-exit",
          judge_one(base, report_of(["follow", "index"], []), 1), False)
    check("unparseable-stdout",
          judge(base, {"exit": 0, "stdout": b"not json",
                       "stderr": b""})["correct"], False)
    fault = {"exit": 2, "check_id": "c", "effective": None, "findings": None,
             "error": "missing_file"}
    check("fault-correct",
          judge_one(fault, {"version": 1, "error": "missing_file"}, 2), True)
    check("fault-wrong-code",
          judge_one(fault, {"version": 1, "error": "bad_manifest"}, 2), False)
    check("fault-wrong-exit",
          judge_one(fault, {"version": 1, "error": "missing_file"}, 0), False)
    check("wrong-version",
          judge_one(base, {"version": 2, "checks": [{
              "id": "c", "effective": ["follow", "index"], "findings": []}]},
                    0), False)
    check("wrong-check-id",
          judge_one(base, {"version": 1, "checks": [{
              "id": "x", "effective": ["follow", "index"], "findings": []}]},
                    0), False)
    good = {"cases": DECLARED_CASE_COUNT, "decided": DECLARED_CASE_COUNT,
            "correct": DECLARED_CASE_COUNT, "wrong": 0}
    check("predicate-met", predicate(good, 4, True), True)
    check("predicate-selftest-false", predicate(good, 4, False), False)
    check("predicate-constants", predicate(good, 3, True), False)
    check("predicate-undecided",
          predicate({"cases": DECLARED_CASE_COUNT,
                     "decided": DECLARED_CASE_COUNT - 1,
                     "correct": DECLARED_CASE_COUNT - 1, "wrong": 0},
                    4, True), False)
    fixture = os.path.join(work, "missing-frozen-id")
    reset_dir(fixture)
    try:
        for name in FROZEN_CASE_IDS:
            directory = os.path.join(fixture, name)
            os.makedirs(directory)
            with open(os.path.join(directory, "page.html"), "w") as handle:
                handle.write("<html><head></head><body></body></html>")
            with open(os.path.join(directory, "manifest.json"), "w") as handle:
                json.dump({"schema": "kake-meta-robots-manifest/v1",
                           "checks": [{"id": name, "path": "page.html",
                                       "url": "https://example.test/page"}]}, handle)
            with open(os.path.join(directory, "expect.json"), "w") as handle:
                json.dump({"exit": 0, "effective": ["follow", "index"],
                           "findings": []}, handle)
        shutil.rmtree(os.path.join(fixture, "g16_unknown_directive"))
        population, missing, extra = load_cases(fixture)
        verdicts = {"cases": len(population),
                    "decided": sum(row["decided"] for row in population),
                    "correct": sum(row["decided"] for row in population),
                    "wrong": 0}
        finding = "case_set_mismatch" if missing or extra else None
        met = predicate(verdicts, 4, True) and not missing and not extra
        check("integration-missing-frozen-id",
              (finding, met, missing),
              ("case_set_mismatch", False, ["g16_unknown_directive"]))
    finally:
        shutil.rmtree(fixture)
    failed = [row for row in checks if not row["ok"]]
    for row in failed:
        print("selftest FAIL %s got=%r want=%r"
              % (row["name"], row["got"], row["want"]))
    print("C3v1 selftest cases=%d passed=%d failed=%d"
          % (len(checks), len(checks) - len(failed), len(failed)))
    return 0 if not failed else 1


def main(argv):
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--tool-revision", default=None)
    parser.add_argument("--cases", default=None)
    parser.add_argument("--consts", default=None)
    parser.add_argument("--work", required=True)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--selftest", action="store_true")
    try:
        opts = parser.parse_args(argv)
    except SystemExit:
        return 64
    try:
        if opts.selftest:
            return selftest(opts.work)
        if not opts.tool_revision:
            raise UsageError("--tool-revision is required")
        return run_matrix(opts)
    except UsageError as exc:
        print("usage: %s" % exc, file=sys.stderr)
        return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
