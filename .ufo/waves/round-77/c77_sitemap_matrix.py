#!/usr/bin/env python3
"""C2 measurement instrument: the frozen container/format matrix (round 77).

Rule of record: .ufo/waves/round-77/contract.md, claim C2.

Usage (the frozen counting form):

  python3 -B .ufo/waves/round-77/c77_sitemap_matrix.py --root . \
      --tool scripts/sitemap_audit.py --revision <full-hash> \
      --cases .ufo/waves/round-77/cases --consts .ufo/waves/round-77/consts \
      --work <scratch>

It runs one tool over the 20 frozen cases and over the 4 degenerate constants,
and prints exactly one line:

  C2 revision=<rev> cases=<n> decided=<n> correct=<n> wrong=<n> constants_failed=<k>/4 met=<true|false>

with `met <=> cases == decided and wrong == 0 and constants_failed == 4`.
Exit 0 when met, 1 when not met, 64 on usage error, 2 when the instrument
cannot evaluate (a case population that is not the frozen 20 ids, a constants
directory that does not hold exactly 4 tools, or a git extraction failure).

A case is *decided* when the tool exits with a code and prints one JSON
document whose `checks` list can be read.  It is *correct* when the exit code
equals `expect.json`'s `exit` and, for exit 0/1, the set of finding ids
(`findings[].code`) equals `expect.json`'s `findings` with no check at status
"error".  For exit 2 (the contract's "input fault", amendment A9) a check must
be at status "error", no finding id may be reported, and the set of `error`
codes must equal `expect.json`'s `findings`, which every exit-2 case names
(g03 `gzip_invalid`, amendment A6; d01 `format_unsupported`).  An exit-2
expectation that names no code is refused (exit 2, no line).  A case that is
decided but not correct is *wrong*; an undecided case is neither, so it makes
`cases == decided` false.

A constant *fails* a case when that case is not correct for it, or is
undecided.  A constant is counted in `constants_failed` when it fails at least
one case.

`--tool-revision <hash>` extracts `scripts/sitemap_audit.py` from that
committed revision into `--work` with `git show` and measures those bytes.
`--selftest` exercises this counter itself on fixtures it builds under
`--work`, including a case whose expectation is deliberately wrong and a
constant that must survive; it prints `selftest <passed>/<total> passed`.
"""

import argparse
import json
import os
import re
import subprocess
import sys

FROZEN_CASE_IDS = frozenset(
    (
        "g01", "g02", "g03", "g04",
        "t01", "t02", "t03", "t04", "t05", "t06", "t07",
        "r01", "r02", "r03", "r04",
        "a01", "a02", "a03",
        "s01",
        "d01",
    )
)

CONSTANT_COUNT = 4
EXIT_MET = 0
EXIT_NOT_MET = 1
EXIT_CANNOT = 2
EXIT_USAGE = 64

LINE_RE = re.compile(
    r"\AC2 revision=(?P<revision>\S+) cases=(?P<cases>\d+) decided=(?P<decided>\d+) "
    r"correct=(?P<correct>\d+) wrong=(?P<wrong>\d+) constants_failed=(?P<failed>\d+)/4 "
    r"met=(?P<met>true|false)\Z"
)


class CannotEvaluate(Exception):
    """The instrument refuses to measure: its own inputs are not the frozen ones."""


# --------------------------------------------------------------------------
# Files
# --------------------------------------------------------------------------

def read_json(path):
    with open(path, "rb") as handle:
        return json.loads(handle.read().decode("utf-8"))


def load_expect(case_dir):
    document = read_json(os.path.join(case_dir, "expect.json"))
    exit_code = document["exit"]
    findings = document["findings"]
    if type(exit_code) is not int or exit_code not in (0, 1, 2):
        raise ValueError("%s: exit must be 0, 1 or 2" % case_dir)
    if not isinstance(findings, list) or not all(isinstance(item, str) and item for item in findings):
        raise ValueError("%s: findings must be a list of ids" % case_dir)
    if exit_code == 2 and not findings:
        raise ValueError("%s: an exit-2 case must name its input-fault error code" % case_dir)
    return exit_code, sorted(set(findings))


def discover_cases(cases_root):
    case_ids = []
    for name in sorted(os.listdir(cases_root)):
        case_dir = os.path.join(cases_root, name)
        if not os.path.isdir(case_dir):
            continue
        if not os.path.isfile(os.path.join(case_dir, "manifest.json")):
            continue
        if not os.path.isfile(os.path.join(case_dir, "expect.json")):
            continue
        case_ids.append(name)
    return case_ids


def discover_constants(consts_root):
    paths = []
    for name in sorted(os.listdir(consts_root)):
        if not name.endswith(".py"):
            continue
        path = os.path.join(consts_root, name)
        if os.path.isfile(path):
            paths.append(path)
    return paths


# --------------------------------------------------------------------------
# One tool run
# --------------------------------------------------------------------------

def _python():
    return sys.executable or "python3"


def observe(tool_path, case_dir, work, timeout, env_extra=None):
    """Run the tool on one case; return a decided/undecided observation."""
    manifest = os.path.join(case_dir, "manifest.json")
    env = dict(os.environ)
    env.pop("C2_REAL_TOOL", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if env_extra:
        env.update(env_extra)
    try:
        completed = subprocess.run(
            [_python(), "-B", tool_path, "--manifest", manifest],
            cwd=work,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"decided": False, "reason": "timeout after %ss" % timeout, "exit": None}
    except OSError as error:
        return {"decided": False, "reason": "could not run: %s" % error, "exit": None}
    try:
        document = json.loads(completed.stdout.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return {"decided": False, "reason": "stdout is not one JSON document", "exit": completed.returncode}
    if not isinstance(document, dict) or not isinstance(document.get("checks"), list):
        return {"decided": False, "reason": "output has no checks list", "exit": completed.returncode}
    ids = set()
    finding_ids = set()
    error_ids = set()
    error_present = False
    for check in document["checks"]:
        if not isinstance(check, dict):
            return {"decided": False, "reason": "a check is not an object", "exit": completed.returncode}
        if check.get("status") == "error":
            error_present = True
            code = check.get("error")
            if not isinstance(code, str) or not code:
                return {"decided": False, "reason": "an error check names no code", "exit": completed.returncode}
            ids.add(code)
            error_ids.add(code)
        findings = check.get("findings")
        if not isinstance(findings, list):
            return {"decided": False, "reason": "a check has no findings list", "exit": completed.returncode}
        for finding in findings:
            if not isinstance(finding, dict):
                return {"decided": False, "reason": "a finding is not an object", "exit": completed.returncode}
            code = finding.get("code")
            if not isinstance(code, str) or not code:
                return {"decided": False, "reason": "a finding names no code", "exit": completed.returncode}
            ids.add(code)
            finding_ids.add(code)
    return {
        "decided": True,
        "exit": completed.returncode,
        "ids": sorted(ids),
        "finding_ids": sorted(finding_ids),
        "error_ids": sorted(error_ids),
        "error_present": error_present,
        "stderr": completed.stderr.decode("utf-8", "replace").strip(),
    }


def judge(expect, observed):
    """True when correct, False when wrong, None when undecided.

    Exit 0/1: the finding-id set equals the expectation and no check is at
    status "error".  Exit 2 (the contract's "input fault", amendment A9): a
    check is at status "error", no finding id is reported, and the error-code
    set equals the expectation (g03 `gzip_invalid`, d01 `format_unsupported`).
    """
    if not observed["decided"]:
        return None
    expected_exit, expected_ids = expect
    if expected_exit == 2:
        return (
            observed["exit"] == 2
            and observed["error_present"]
            and not observed["finding_ids"]
            and observed["error_ids"] == expected_ids
        )
    return (
        observed["exit"] == expected_exit
        and not observed["error_present"]
        and observed["finding_ids"] == expected_ids
    )


# --------------------------------------------------------------------------
# Case sets and constants
# --------------------------------------------------------------------------

def run_case_set(tool_path, cases_root, work, timeout, env_extra=None, required_ids=None):
    case_ids = discover_cases(cases_root)
    if required_ids is not None and set(case_ids) != set(required_ids):
        missing = sorted(set(required_ids) - set(case_ids))
        extra = sorted(set(case_ids) - set(required_ids))
        raise CannotEvaluate(
            "case population is not the frozen 20 ids: missing=%s extra=%s" % (missing, extra)
        )
    results = []
    for case_id in case_ids:
        case_dir = os.path.join(cases_root, case_id)
        expect = load_expect(case_dir)
        observed = observe(tool_path, case_dir, work, timeout, env_extra)
        results.append(
            {
                "id": case_id,
                "expect": {"exit": expect[0], "findings": expect[1]},
                "observed": observed,
                "verdict": judge(expect, observed),
            }
        )
    return results


def run_constants(consts_root, cases_root, work, timeout, measured_tool, required_ids=None):
    paths = discover_constants(consts_root)
    if len(paths) != CONSTANT_COUNT:
        raise CannotEvaluate(
            "constants directory holds %d python tools, expected %d: %s"
            % (len(paths), CONSTANT_COUNT, [os.path.basename(path) for path in paths])
        )
    entries = []
    for path in paths:
        results = run_case_set(
            path,
            cases_root,
            work,
            timeout,
            env_extra={"C2_REAL_TOOL": measured_tool},
            required_ids=required_ids,
        )
        failed = [result["id"] for result in results if result["verdict"] is not True]
        entries.append({"name": os.path.basename(path), "results": results, "failed": failed})
    return entries


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------

def tally(results):
    decided = sum(1 for result in results if result["verdict"] is not None)
    correct = sum(1 for result in results if result["verdict"] is True)
    wrong = sum(1 for result in results if result["verdict"] is False)
    assert correct + wrong == decided
    return decided, correct, wrong


def frozen_line(revision, results, constants):
    decided, correct, wrong = tally(results)
    constants_failed = sum(1 for entry in constants if entry["failed"])
    met = len(results) == decided and wrong == 0 and constants_failed == CONSTANT_COUNT
    line = (
        "C2 revision=%s cases=%d decided=%d correct=%d wrong=%d constants_failed=%d/4 met=%s"
        % (revision, len(results), decided, correct, wrong, constants_failed, "true" if met else "false")
    )
    return line, met, constants_failed


def emit_detail(results, constants):
    for result in results:
        observed = result["observed"]
        if observed["decided"]:
            verdict = {True: "correct", False: "wrong", None: "undecided"}[result["verdict"]]
            sys.stderr.write(
                "case %s expect_exit=%d expect_findings=%s observed_exit=%d observed_findings=%s observed_error=%s verdict=%s\n"
                % (
                    result["id"],
                    result["expect"]["exit"],
                    ",".join(result["expect"]["findings"]) or "-",
                    observed["exit"],
                    ",".join(observed["finding_ids"]) or "-",
                    ",".join(observed["error_ids"]) or "-",
                    verdict,
                )
            )
        else:
            sys.stderr.write(
                "case %s expect_exit=%d expect_findings=%s observed=undecided (%s)\n"
                % (
                    result["id"],
                    result["expect"]["exit"],
                    ",".join(result["expect"]["findings"]) or "-",
                    observed["reason"],
                )
            )
    for entry in constants:
        sys.stderr.write(
            "const %s failed=%d ids=%s\n"
            % (entry["name"], len(entry["failed"]), ",".join(entry["failed"]) or "-")
        )


def receipt_document(revision, tool, line, met, results, constants):
    return {
        "version": 1,
        "revision": revision,
        "tool": tool,
        "line": line,
        "met": met,
        "cases": [
            {
                "id": result["id"],
                "expect": result["expect"],
                "observed": result["observed"],
                "verdict": result["verdict"],
            }
            for result in results
        ],
        "constants": [
            {"name": entry["name"], "failed": entry["failed"], "cases": len(entry["results"])}
            for entry in constants
        ],
    }


# --------------------------------------------------------------------------
# Selftest
# --------------------------------------------------------------------------

SELFTEST_TABLE = {
    "s01": (0, []),
    "s02": (1, ["alpha"]),
    "s03": (2, ["beta"]),
    "s04": (0, []),
    "s05": (1, ["gamma"]),
    "s06": (0, []),
    "s07": (1, ["alpha"]),
    "s08": (0, []),
}

ORACLE = '''#!/usr/bin/env python3
import json, sys
TABLE = %r
def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    document = json.loads(open(argv[2], "rb").read().decode("utf-8"))
    ident = document["checks"][0]["id"]
    if ident not in TABLE:
        return 3
    exit_code, ids = TABLE[ident]
    if exit_code == 2:
        check = {"id": ident, "status": "error", "error": ids[0] if ids else "input_invalid", "findings": []}
    elif ids:
        check = {"id": ident, "status": "findings", "error": None,
                 "findings": [{"code": code, "entry": 1} for code in ids]}
    else:
        check = {"id": ident, "status": "clean", "error": None, "findings": []}
    verdict = "could-not-evaluate" if exit_code == 2 else ("failed-policy" if ids else "clean")
    sys.stdout.write(json.dumps({"version": 1, "verdict": verdict, "checks": [check]}) + "\\n")
    return exit_code
if __name__ == "__main__":
    sys.exit(main(sys.argv))
''' % (SELFTEST_TABLE,)

CRASH = '''#!/usr/bin/env python3
import sys
sys.stderr.write("boom\\n")
sys.exit(3)
'''

EXIT2_CLEAN = '''#!/usr/bin/env python3
import json, sys
sys.stdout.write(json.dumps({"version": 1, "verdict": "could-not-evaluate",
    "checks": [{"id": "x", "status": "clean", "error": None, "findings": []}]}) + "\\n")
sys.exit(2)
'''

CONST_ALWAYS_CLEAN = '''#!/usr/bin/env python3
import json, sys
sys.stdout.write(json.dumps({"version": 1, "verdict": "clean",
    "checks": [{"id": "x", "status": "clean", "error": None, "findings": []}]}) + "\\n")
sys.exit(0)
'''

ERROR_ONLY = '''#!/usr/bin/env python3
import json, sys
print(json.dumps({"version": 1, "verdict": "could-not-evaluate",
    "checks": [{"id": "x", "status": "error", "error": "gzip_corrupt", "findings": []}]}))
sys.exit(2)
'''

ERROR_AND_FINDING = '''#!/usr/bin/env python3
import json, sys
print(json.dumps({"version": 1, "verdict": "could-not-evaluate",
    "checks": [{"id": "x", "status": "error", "error": "gzip_invalid",
                "findings": [{"code": "too_large", "entry": None}]}]}))
sys.exit(2)
'''

ERROR_PINNED = '''#!/usr/bin/env python3
import json, sys
print(json.dumps({"version": 1, "verdict": "could-not-evaluate",
    "checks": [{"id": "x", "status": "error", "error": "gzip_invalid", "findings": []}]}))
sys.exit(2)
'''

CONST_EVERY_ID = '''#!/usr/bin/env python3
import json, sys
sys.stdout.write(json.dumps({"version": 1, "verdict": "failed-policy",
    "checks": [{"id": "x", "status": "findings", "error": None,
                "findings": [{"code": "wrong_id", "entry": 1}]}]}) + "\\n")
sys.exit(1)
'''

CONST_EMPTY = '''#!/usr/bin/env python3
import json, sys
sys.stdout.write(json.dumps({"version": 1, "verdict": "failed-policy",
    "checks": [{"id": "x", "status": "clean", "error": None, "findings": []}]}) + "\\n")
sys.exit(1)
'''

CONST_WRONG_EXIT = '''#!/usr/bin/env python3
import json, sys
sys.stdout.write(json.dumps({"version": 1, "verdict": "clean",
    "checks": [{"id": "x", "status": "clean", "error": None, "findings": []}]}) + "\\n")
sys.exit(1)
'''

CONST_SURVIVES = ORACLE  # a constant that decides every fixture correctly

MIRROR_EMPTY_FINDINGS = '''#!/usr/bin/env python3
import json, os, subprocess, sys
tool = os.environ.get("C2_REAL_TOOL")
if not tool:
    sys.exit(64)
done = subprocess.run([sys.executable, "-B", tool] + sys.argv[1:], capture_output=True)
try:
    document = json.loads(done.stdout.decode("utf-8"))
except (UnicodeDecodeError, ValueError):
    sys.exit(done.returncode)
checks = []
for check in document.get("checks", []):
    status = check.get("status")
    checks.append({"id": check.get("id"), "status": status if status == "error" else "clean",
                   "error": check.get("error") if status == "error" else None, "findings": []})
verdict = "could-not-evaluate" if any(item["status"] == "error" for item in checks) else "clean"
print(json.dumps({"version": 1, "verdict": verdict, "checks": checks}))
sys.exit(done.returncode)
'''


def _write(path, text, mode=0o644):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    os.chmod(path, mode)


def _write_fixture_case(case_dir, case_id, expect):
    os.makedirs(case_dir)
    _write(os.path.join(case_dir, "sitemap.txt"), "https://example.com/one\n")
    _write(
        os.path.join(case_dir, "manifest.json"),
        json.dumps(
            {
                "version": 1,
                "checks": [
                    {"id": case_id, "file": "sitemap.txt", "sitemapUrl": "https://example.com/sitemap.txt"}
                ],
            },
            indent=2,
        )
        + "\n",
    )
    _write(os.path.join(case_dir, "expect.json"), json.dumps(expect, indent=2) + "\n")


def _build_selftest_fixtures(work):
    root = os.path.join(work, "selftest")
    if os.path.isdir(root):
        import shutil

        shutil.rmtree(root)
    cases_root = os.path.join(root, "cases")
    tools_root = os.path.join(root, "tools")
    consts_fail = os.path.join(root, "consts-fail")
    consts_survive = os.path.join(root, "consts-survive")
    for path in (cases_root, tools_root, consts_fail, consts_survive):
        os.makedirs(path)
    for case_id, (exit_code, findings) in SELFTEST_TABLE.items():
        _write_fixture_case(
            os.path.join(cases_root, case_id), case_id, {"exit": exit_code, "findings": findings}
        )
    _write(os.path.join(tools_root, "oracle.py"), ORACLE, 0o755)
    _write(os.path.join(tools_root, "crash.py"), CRASH, 0o755)
    _write(os.path.join(tools_root, "exit2_clean.py"), EXIT2_CLEAN, 0o755)
    _write(os.path.join(consts_fail, "always_clean.py"), CONST_ALWAYS_CLEAN, 0o755)
    _write(os.path.join(consts_fail, "every_id.py"), CONST_EVERY_ID, 0o755)
    _write(os.path.join(consts_fail, "empty.py"), CONST_EMPTY, 0o755)
    _write(os.path.join(consts_fail, "wrong_exit.py"), CONST_WRONG_EXIT, 0o755)
    for name in ("always_clean.py", "every_id.py", "empty.py"):
        source = {
            "always_clean.py": CONST_ALWAYS_CLEAN,
            "every_id.py": CONST_EVERY_ID,
            "empty.py": CONST_EMPTY,
        }[name]
        _write(os.path.join(consts_survive, name), source, 0o755)
    _write(os.path.join(consts_survive, "survivor.py"), CONST_SURVIVES, 0o755)
    return {
        "root": root,
        "cases": cases_root,
        "tools": tools_root,
        "consts_fail": consts_fail,
        "consts_survive": consts_survive,
    }


def selftest(work, timeout):
    fixtures = _build_selftest_fixtures(work)
    checks = []

    def check(name, condition, detail=""):
        checks.append((name, bool(condition), detail))

    oracle = os.path.join(fixtures["tools"], "oracle.py")
    results = run_case_set(oracle, fixtures["cases"], work, timeout)
    constants = run_constants(fixtures["consts_fail"], fixtures["cases"], work, timeout, oracle)
    line, met, constants_failed = frozen_line("selftest", results, constants)
    decided, correct, wrong = tally(results)
    check("line-shape", LINE_RE.match(line) is not None, line)
    check("eight-cases", len(results) == 8 and decided == 8, "cases=%d decided=%d" % (len(results), decided))
    check("all-correct", correct == 8 and wrong == 0, "correct=%d wrong=%d" % (correct, wrong))
    check("four-constants-fail", constants_failed == 4, "constants_failed=%d" % constants_failed)
    check("met-true", met is True, line)

    constants = run_constants(fixtures["consts_survive"], fixtures["cases"], work, timeout, oracle)
    line, met, constants_failed = frozen_line("selftest", results, constants)
    survivors = [entry["name"] for entry in constants if not entry["failed"]]
    check(
        "surviving-constant-not-counted",
        constants_failed == 3 and survivors == ["survivor.py"] and met is False,
        "constants_failed=%d survivors=%s" % (constants_failed, survivors),
    )

    # The decisive kill: a tool whose exits are all right and whose finding
    # lists are empty must still be reported failed, on exactly the cases
    # whose expected finding set is non-empty.
    mirror = os.path.join(fixtures["tools"], "mirror_empty_findings.py")
    _write(mirror, MIRROR_EMPTY_FINDINGS, 0o755)
    results = run_case_set(mirror, fixtures["cases"], work, timeout, env_extra={"C2_REAL_TOOL": oracle})
    failed = [result["id"] for result in results if result["verdict"] is not True]
    check(
        "empty-findings-constant-killed",
        failed == ["s02", "s05", "s07"],
        "failed=%s" % (failed,),
    )

    # A fixture whose expectation is deliberately wrong: s02 expects clean.
    s02_expect = os.path.join(fixtures["cases"], "s02", "expect.json")
    _write(s02_expect, json.dumps({"exit": 0, "findings": []}, indent=2) + "\n")
    results = run_case_set(oracle, fixtures["cases"], work, timeout)
    line, met, constants_failed = frozen_line("selftest", results, constants)
    wrong_ids = [result["id"] for result in results if result["verdict"] is False]
    check(
        "wrong-expected-fixture-reported",
        wrong_ids == ["s02"] and met is False,
        "wrong=%s" % (wrong_ids,),
    )

    crash = os.path.join(fixtures["tools"], "crash.py")
    results = run_case_set(crash, fixtures["cases"], work, timeout)
    decided, correct, wrong = tally(results)
    line, met, _ = frozen_line("selftest", results, constants)
    check(
        "crashing-tool-undecided",
        decided == 0 and wrong == 0 and met is False,
        "decided=%d met=%s" % (decided, met),
    )

    exit2_clean = os.path.join(fixtures["tools"], "exit2_clean.py")
    results = run_case_set(exit2_clean, fixtures["cases"], work, timeout)
    wrong_ids = [result["id"] for result in results if result["verdict"] is False]
    check(
        "exit-two-needs-error-status",
        "s03" in wrong_ids,
        "wrong=%s" % (wrong_ids,),
    )

    # Exit-2 expectations name their input-fault code (amendment A6/A9), the
    # code is pinned, and a mixed error-plus-finding verdict is wrong.
    error_only = os.path.join(fixtures["tools"], "error_only.py")
    _write(error_only, ERROR_ONLY, 0o755)

    no_code_root = os.path.join(fixtures["root"], "cases-no-code")
    _write_fixture_case(os.path.join(no_code_root, "s09"), "s09", {"exit": 2, "findings": []})
    refused = False
    try:
        run_case_set(error_only, no_code_root, work, timeout)
    except ValueError:
        refused = True
    check("code-less-exit-two-refused", refused, "no ValueError raised")

    pinned_root = os.path.join(fixtures["root"], "cases-pinned")
    _write_fixture_case(
        os.path.join(pinned_root, "s10"), "s10", {"exit": 2, "findings": ["gzip_invalid"]}
    )
    results = run_case_set(error_only, pinned_root, work, timeout)
    check(
        "wrong-input-fault-code-rejected",
        [result["verdict"] for result in results] == [False],
        "verdicts=%s" % ([result["verdict"] for result in results],),
    )
    pinned = os.path.join(fixtures["tools"], "error_pinned.py")
    _write(pinned, ERROR_PINNED, 0o755)
    results = run_case_set(pinned, pinned_root, work, timeout)
    check(
        "pinned-input-fault-code-accepted",
        [result["verdict"] for result in results] == [True],
        "verdicts=%s" % ([result["verdict"] for result in results],),
    )
    mixed = os.path.join(fixtures["tools"], "error_and_finding.py")
    _write(mixed, ERROR_AND_FINDING, 0o755)
    results = run_case_set(mixed, pinned_root, work, timeout)
    check(
        "mixed-fault-finding-rejected",
        [result["verdict"] for result in results] == [False],
        "verdicts=%s" % ([result["verdict"] for result in results],),
    )

    passed = sum(1 for _, ok, _ in checks if ok)
    for name, ok, detail in checks:
        sys.stdout.write("selftest %s %s%s\n" % ("ok" if ok else "FAIL", name, "" if ok else " (%s)" % detail))
    sys.stdout.write("selftest %d/%d passed\n" % (passed, len(checks)))
    return 0 if passed == len(checks) else 1


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def resolve(root, value):
    if os.path.isabs(value):
        return value
    return os.path.abspath(os.path.join(root, value))


def main(argv):
    parser = argparse.ArgumentParser(description="C2 container/format matrix (round 77)")
    parser.add_argument("--root", default=".")
    parser.add_argument("--tool", default=None)
    parser.add_argument("--tool-revision", default=None)
    parser.add_argument("--revision", default=None)
    parser.add_argument("--cases", default=".ufo/waves/round-77/cases")
    parser.add_argument("--consts", default=".ufo/waves/round-77/consts")
    parser.add_argument("--work", default=None)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--json-out", default=None)
    options = parser.parse_args(argv[1:])

    if options.work is None:
        sys.stderr.write("c77_sitemap_matrix: --work is required\n")
        return EXIT_USAGE
    work = os.path.abspath(options.work)
    os.makedirs(work, exist_ok=True)
    if options.selftest:
        return selftest(work, options.timeout)

    root = os.path.abspath(options.root)
    if (options.tool is None) == (options.tool_revision is None):
        sys.stderr.write("c77_sitemap_matrix: pass exactly one of --tool or --tool-revision\n")
        return EXIT_USAGE
    try:
        if options.tool_revision is not None:
            revision = options.revision or options.tool_revision
            tool_path = os.path.join(work, "tool-%s.py" % options.tool_revision[:16])
            completed = subprocess.run(
                ["git", "-C", root, "show", "%s:scripts/sitemap_audit.py" % options.tool_revision],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if completed.returncode != 0:
                raise CannotEvaluate(
                    "git show %s:scripts/sitemap_audit.py failed: %s"
                    % (options.tool_revision, completed.stderr.decode("utf-8", "replace").strip())
                )
            with open(tool_path, "wb") as handle:
                handle.write(completed.stdout)
        else:
            tool_path = resolve(root, options.tool)
            if not os.path.isfile(tool_path):
                raise CannotEvaluate("tool not found: %s" % tool_path)
            revision = options.revision or "worktree"
        cases_root = resolve(root, options.cases)
        consts_root = resolve(root, options.consts)
        results = run_case_set(
            tool_path, cases_root, work, options.timeout, required_ids=FROZEN_CASE_IDS
        )
        constants = run_constants(
            consts_root, cases_root, work, options.timeout, tool_path, required_ids=FROZEN_CASE_IDS
        )
    except CannotEvaluate as error:
        sys.stderr.write("c77_sitemap_matrix: cannot evaluate: %s\n" % error)
        return EXIT_CANNOT
    except (OSError, ValueError) as error:
        sys.stderr.write("c77_sitemap_matrix: cannot evaluate: %s\n" % error)
        return EXIT_CANNOT

    line, met, _ = frozen_line(revision, results, constants)
    if options.verbose:
        emit_detail(results, constants)
    if options.json_out:
        with open(options.json_out, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(receipt_document(revision, tool_path, line, met, results, constants), indent=2) + "\n")
    sys.stdout.write(line + "\n")
    return EXIT_MET if met else EXIT_NOT_MET


if __name__ == "__main__":
    sys.exit(main(sys.argv))
