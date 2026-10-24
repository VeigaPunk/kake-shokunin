#!/usr/bin/env python3
"""Round-33 criterion check: a hostile spec that pins WHICH LAYER refused must
name a structured refusal code, not message text.

Reads committed bytes at a Git revision (never the working tree).

Checks, all five must hold:
  S1 specs    every hostile spec case carrying ``reason_contains`` also carries
              a non-empty ``reason_code``
  S2 schema   the hostile selftest accepts ``reason_code`` in its case-key set
  S3 compare  the hostile selftest reads ``reason_code`` from a case (so the key
              is graded, not merely tolerated)
  S4 emit     the runner reports a per-case ``code`` (dict key / row assignment)
  S5 literal  every ``reason_code`` value named in a spec appears as a literal
              in the runner source (a typo or never-emitted code is caught)

Exit: 0 all met, 1 any unmet, 2 could not evaluate.
"""
import argparse
import ast
import json
import re
import subprocess
import sys

SPEC_ROOT = "scripts/fixtures/"
SPEC_NAME = "hostile.json"
HOSTILE_SELFTEST = "scripts/citing_set_hostile_selftest.py"
RUNNER = "scripts/citing_set_selftest.py"


def git_show(root, rev, path):
    done = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)],
                          capture_output=True)
    if done.returncode != 0:
        raise CouldNotEvaluate("git show %s:%s failed: %s"
                               % (rev, path, done.stderr.decode("utf-8", "replace").strip()))
    return done.stdout


def git_ls(root, rev, path):
    done = subprocess.run(["git", "-C", root, "ls-tree", "-r", "--name-only", rev, "--", path],
                          capture_output=True)
    if done.returncode != 0:
        raise CouldNotEvaluate("git ls-tree %s -- %s failed" % (rev, path))
    return [line for line in done.stdout.decode("utf-8", "replace").splitlines() if line]


class CouldNotEvaluate(Exception):
    pass


def spec_paths(root, rev):
    return sorted(p for p in git_ls(root, rev, SPEC_ROOT)
                  if p.rsplit("/", 1)[-1] == SPEC_NAME)


def load_specs(root, rev):
    specs = []
    for path in spec_paths(root, rev):
        try:
            doc = json.loads(git_show(root, rev, path).decode("utf-8"))
        except ValueError as exc:
            raise CouldNotEvaluate("%s is not JSON: %s" % (path, exc))
        if not isinstance(doc, dict) or not isinstance(doc.get("cases"), list):
            raise CouldNotEvaluate("%s has no cases list" % path)
        for case in doc["cases"]:
            if isinstance(case, dict):
                specs.append((path, case))
    return specs


def case_keys(src):
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "CASE_KEYS" for t in node.targets):
            return {n.value for n in ast.walk(node.value)
                    if isinstance(n, ast.Constant) and isinstance(n.value, str)}, node.value
    return set(), None


def compares_reason_code(src):
    """True when the selftest compares a code value with == or !=, not merely
    validates the key's type. Validation alone (isinstance, membership) is not
    grading, so it does not satisfy this check."""
    tree = ast.parse(src)
    token = re.compile(r"(?:^|[^A-Za-z])code(?:[A-Z_]|$)")
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            operands = [node.left] + list(node.comparators)
            if any(isinstance(op, (ast.Eq, ast.NotEq)) for op in node.ops) \
                    and any(token.search(ast.unparse(part)) for part in operands
                            if not isinstance(part, ast.Constant)):
                return True
    return False


def reports_code(src):
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict) and any(
                isinstance(k, ast.Constant) and k.value == "code" for k in node.keys):
            return True
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Subscript) and isinstance(target.slice, ast.Constant) \
                        and target.slice.value == "code":
                    return True
    return False


def main(argv=None):
    parser = argparse.ArgumentParser(prog="criterion_check.py")
    parser.add_argument("--root", required=True, help="Git repository holding the lane paths")
    parser.add_argument("--rev", required=True, help="revision whose committed bytes are graded")
    args = parser.parse_args(argv)

    checks = []

    def record(ident, met, detail):
        checks.append({"id": ident, "met": bool(met), "detail": detail})

    try:
        specs = load_specs(args.root, args.rev)
        selftest_src = git_show(args.root, args.rev, HOSTILE_SELFTEST).decode("utf-8")
        runner_src = git_show(args.root, args.rev, RUNNER).decode("utf-8")
        keys, _keys_node = case_keys(selftest_src)
        coded = compares_reason_code(selftest_src)
        emits = reports_code(runner_src)
    except (CouldNotEvaluate, SyntaxError) as exc:
        print(json.dumps({"schema": "kake-r33-refusal-code-criterion/1", "revision": args.rev,
                          "passed": False, "error": str(exc)}, indent=1))
        return 2

    violations = ["%s case %r" % (path, case.get("name"))
                  for path, case in specs
                  if case.get("reason_contains") and not (isinstance(case.get("reason_code"), str)
                                                          and case["reason_code"])]
    record("S1_specs_name_code",
           not violations,
           {"cases": len(specs),
            "reason_contains_cases": sum(1 for _, c in specs if c.get("reason_contains")),
            "violations": violations})

    record("S2_schema_accepts_code", "reason_code" in keys,
           {"case_keys": sorted(keys)})

    record("S3_selftest_compares_code", coded,
           {"comparison_involving_code": coded})

    record("S4_runner_emits_code", emits, {"per_case_code_field": emits})

    named = sorted({case["reason_code"] for _, case in specs
                    if isinstance(case.get("reason_code"), str) and case["reason_code"]})
    literals = {node.value for node in ast.walk(ast.parse(runner_src))
                if isinstance(node, ast.Constant) and isinstance(node.value, str)}
    missing = [code for code in named if code not in literals]
    record("S5_code_literal_in_runner", not missing,
           {"named_codes": named, "absent_from_runner": missing})

    met = sum(1 for c in checks if c["met"])
    out = {"schema": "kake-r33-refusal-code-criterion/1",
           "revision": args.rev,
           "checks": checks,
           "met": met,
           "total": len(checks),
           "passed": met == len(checks)}
    print(json.dumps(out, indent=1))
    return 0 if out["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
