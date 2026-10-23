#!/usr/bin/env python3
"""Round-36 criterion: a counter version bump may not move a scored constant or predicate silently.

Mined from the round-35 closure, routed defect 2 ("Do not loosen a counter in a version bump that a
control forced for other reasons"): version 2 of that round's counter raised `C2_MAX_WORDS` from 1500
to 2200 with no control forcing it, and nothing in the tree recorded the move. This check compares
two counter files and reports every scored difference:

  constants    every module-level UPPER_CASE assignment (targets, thresholds, caps, key pins,
               tool paths, case counts and the timeouts that decide a run).
  predicate    every module-level string constant whose value reads as a predicate (PREDICATE and
               any lowercase equivalent: a comparison, "at least", "passed", "met:"), the
               `Declared target:` / `met:` sentences of the module docstring (the frozen predicate
               as declared), and every string literal inside the functions that decide a case
               (`judge`, `project` and `*_judge`): those literals name the fields and verdict
               labels the judge compares, so a changed label is a weakened predicate.

Exit 0 when both files carry the same constants, pins and predicate; 1 when any differs (each
difference printed with its name, category, old and new value); 2 on a usage, read or parse error.

Usage:
  python3 -B version_bump_check.py OLD.py NEW.py [--list]

`--list` also prints the full inventory both files were compared on, for audit.
"""
import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path

UPPER = re.compile(r"^[A-Z][A-Z0-9_]*$")
PREDICATE_WORDS = re.compile(r">=|<=|==|!=|\bat least\b|\bpassed\b|\bmet\b")
DOC_PREDICATE = re.compile(r"^\s*(?:`?met`?\s*:|Declared target:)")
JUDGE_FUNCS = re.compile(r"^(?:judge|project|.*_judge)$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(node: ast.AST) -> str:
    """A stable text for a constant's value: literal value when it is one, source otherwise."""
    try:
        value = ast.literal_eval(node)
    except (ValueError, SyntaxError, TypeError, MemoryError, RecursionError):
        return re.sub(r"\s+", " ", ast.unparse(node)).strip()
    return json.dumps(value, sort_keys=True, default=repr)


def category(name: str, label: str = "") -> str:
    if label in {"predicate-literal", "met-expression"} or name.startswith("__doc__"):
        return "predicate"
    tokens = set(name.upper().split("_"))
    if "PREDICATE" in tokens or name.upper() == "PREDICATE":
        return "predicate"
    if tokens & {"SHA", "SHA256", "HASH", "PIN", "PINS", "DIGEST"}:
        return "pin"
    if tokens & {"TARGET", "TARGETS", "GOAL"}:
        return "target"
    if tokens & {"MAX", "CAP", "CEILING", "WORDS", "SHINGLE", "SIZE"}:
        return "cap"
    if tokens & {"MIN", "FLOOR", "THRESHOLD", "LIMIT", "CASES", "PROBES", "COUNT", "N", "TIMEOUT"}:
        return "threshold"
    return "constant"


def judge_literals(tree: ast.AST) -> set[str]:
    """String literals inside the functions that decide a case (the judge vocabulary)."""
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and JUDGE_FUNCS.match(node.name):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                    found.add(f"{node.name}:{sub.value}")
    return found


def met_expressions(tree: ast.Module) -> dict[str, str]:
    """The expressions that compute the `met` verdict: an assignment to `met` (or `*_met`) and a
    dict entry keyed `"met"`. A loosened `passed >= TARGET - 5` shows up here, not in a constant."""
    found: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and (target.id == "met" or target.id.endswith("_met")):
                    found[target.id] = re.sub(r"\s+", " ", ast.unparse(node.value)).strip()
        elif isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and key.value == "met":
                    text = re.sub(r"\s+", " ", ast.unparse(value)).strip()
                    found["dict[met]"] = text
    return found


def doc_predicates(tree: ast.Module) -> dict[str, str]:
    doc = ast.get_docstring(tree) or ""
    out: dict[str, str] = {}
    for i, line in enumerate(doc.splitlines()):
        if DOC_PREDICATE.search(line):
            out[f"__doc__[{i}]"] = re.sub(r"\s+", " ", line).strip()
    return out


def scan(path: Path) -> dict[str, dict[str, str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    consts: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        else:
            continue
        for target in targets:
            if not isinstance(target, ast.Name):
                continue
            name = target.id
            literal = canonical(value)
            if UPPER.match(name):
                consts[name] = literal
            elif isinstance(value, ast.Constant) and isinstance(value.value, str) and PREDICATE_WORDS.search(value.value):
                # a string constant that names a predicate without upper-case naming
                consts[name] = literal
    consts.update(doc_predicates(tree))
    return {"constants": consts,
            "predicate": {k: "present" for k in sorted(judge_literals(tree))},
            "met": met_expressions(tree)}


def compare(old: dict[str, str], new: dict[str, str], label: str) -> list[str]:
    lines: list[str] = []
    for name in sorted(set(old) | set(new)):
        if name not in new:
            lines.append(f"REMOVED  [{category(name, label)}] {label} {name}: {old[name]!r}")
        elif name not in old:
            lines.append(f"ADDED    [{category(name, label)}] {label} {name}: {new[name]!r}")
        elif old[name] != new[name]:
            lines.append(f"CHANGED  [{category(name, label)}] {label} {name}: {old[name]!r} -> {new[name]!r}")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare the scored constants and predicate of two counters.")
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--list", action="store_true", help="print the compared inventory first")
    a = ap.parse_args()
    paths = [Path(a.old), Path(a.new)]
    for p in paths:
        if not p.is_file():
            print(f"cannot read {p}", file=sys.stderr)
            return 2
    try:
        scans = [scan(p) for p in paths]
    except SyntaxError as exc:
        print(f"cannot parse: {exc}", file=sys.stderr)
        return 2
    print(f"old {paths[0]} sha256 {sha256(paths[0])}")
    print(f"new {paths[1]} sha256 {sha256(paths[1])}")
    if a.list:
        for p, s in zip(paths, scans):
            print(f"-- inventory {p}")
            for name, value in sorted(s["constants"].items()):
                print(f"   const     {name} = {value}")
            for name in sorted(s["predicate"]):
                print(f"   predicate {name}")
            for name, value in sorted(s["met"].items()):
                print(f"   met       {name} = {value}")
    diffs = (compare(scans[0]["constants"], scans[1]["constants"], "constant")
             + compare(scans[0]["predicate"], scans[1]["predicate"], "predicate-literal")
             + compare(scans[0]["met"], scans[1]["met"], "met-expression"))
    n_const = len(set(scans[0]["constants"]) | set(scans[1]["constants"]))
    n_pred = len(set(scans[0]["predicate"]) | set(scans[1]["predicate"]))
    print(f"compared {n_const} constants (module-level UPPER_CASE plus docstring predicate lines), "
          f"{n_pred} judge predicate literals and {len(scans[0]['met'])} met expressions")
    if not diffs:
        print("verdict: SAME - no target, threshold, cap, pin or predicate differs")
        return 0
    print(f"differences: {len(diffs)}")
    for line in diffs:
        print(line)
    cats = sorted({re.search(r"\[([^\]]+)\]", line).group(1) for line in diffs})
    print(f"verdict: DIFFERENT - {', '.join(cats)} {'differ' if len(cats) > 1 else 'differs'}; a scored control must be named for each")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # `| head`: the verdict was already written
        sys.exit(0)
