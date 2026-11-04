#!/usr/bin/env python3
"""Classify changed policy-header values in retained captures, without network I/O.

Usage:
  policy_value_class.py --a <capture-dir> --b <capture-dir> --declared <json>
  policy_value_class.py --selftest [--work <dir>]

The sibling classifier owns header classes, canonicalization and receipt checks.
Values use the round-84 frozen comma-separated name[=parameter] grammar, not
individual HTTP fields' richer grammars. Unparseable changed values are decisive.
Exit: 0 printed, 1 unevaluable input, 64 usage.
"""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent))
from header_change_class import POLICY, header_class, canonical, load_surface, declared_surfaces

CLASSES = ("reordered", "numeric_parameter", "directive_added", "directive_removed",
           "directive_changed", "header_added", "header_removed", "unclassified")
VERDICTS = ("policy-unchanged", "policy-rewritten-equivalent", "policy-changed",
            "policy-unclassified")
NAME = re.compile(r"[!#$%&'*+.^_`|~0-9a-z-]+")
NUMBER = re.compile(r"[0-9]+")


def directives(value: str) -> list[tuple[str, str | None]] | None:
    result = []
    for part in value.split(","):
        name, separator, parameter = part.strip().partition("=")
        name = name.strip().lower()
        parameter = parameter.strip().lower()
        if not NAME.fullmatch(name) or (separator and not parameter):
            return None
        result.append((name, parameter if separator else None))
    return result


def value_class(before: str | None, after: str | None) -> str:
    # Presence is a field-level fact; parsing applies when both fields exist.
    if before is None:
        return "header_added"
    if after is None:
        return "header_removed"
    a, b = directives(before), directives(after)
    if a is None or b is None:
        return "unclassified"
    ca, cb = Counter(a), Counter(b)
    if ca == cb:
        return "reordered"
    names_a = {name for name, _ in a}
    names_b = {name for name, _ in b}
    if names_a < names_b:
        return "directive_added"
    if names_b < names_a:
        return "directive_removed"
    removed = list((ca - cb).elements())
    added = list((cb - ca).elements())
    if names_a == names_b and len(removed) == len(added) == 1:
        name_a, parameter_a = removed[0]
        name_b, parameter_b = added[0]
        if (name_a == name_b and parameter_a is not None and parameter_b is not None
                and NUMBER.fullmatch(parameter_a) and NUMBER.fullmatch(parameter_b)):
            return "numeric_parameter"
    return "directive_changed"


def verdict(counts: dict[str, int]) -> str:
    if counts["changed"] == 0:
        return VERDICTS[0]
    if counts["unclassified"]:
        return VERDICTS[3]
    if counts["changed"] == counts["reordered"]:
        return VERDICTS[1]
    return VERDICTS[2]


def classify(a: dict, b: dict) -> tuple[dict[str, str], dict[str, int]]:
    changes = {}
    counts = dict.fromkeys(("changed", *CLASSES), 0)
    for name in sorted(set(a["headers"]) | set(b["headers"])):
        if name not in POLICY or header_class(name) != "policy":
            continue
        before, after = a["headers"].get(name), b["headers"].get(name)
        if before != after:
            category = value_class(before, after)
            changes[name] = category
            counts[category] += 1
            counts["changed"] += 1
    return changes, counts


def render(counts: dict[str, int]) -> str:
    return " ".join(f"{key}={counts[key]}" for key in ("changed", *CLASSES))


def run(a_dir: Path, b_dir: Path, declared_path: Path) -> int:
    declared = declared_surfaces(declared_path)
    if not declared:
        print(f"fault: cannot read declared surfaces from {declared_path}", file=sys.stderr)
        return 1
    rows = []
    changes = []
    totals = dict.fromkeys(("changed", *CLASSES), 0)
    for surface_id, _url in declared:
        a, detail_a = load_surface(a_dir / surface_id)
        b, detail_b = load_surface(b_dir / surface_id)
        if a is None or b is None:
            print(f"fault: surface={surface_id} a=[{detail_a}] b=[{detail_b}]", file=sys.stderr)
            return 1
        changed, counts = classify(a, b)
        changes.extend((surface_id, name, category) for name, category in changed.items())
        rows.append(f"surface={surface_id} {render(counts)} verdict={verdict(counts)}")
        for key in totals:
            totals[key] += counts[key]
    for surface_id, name, category in sorted(changes):
        print(f"change surface={surface_id} header={name} class={category}")
    for row in rows:
        print(row)
    print(f"summary surfaces={len(declared)} {render(totals)} verdict={verdict(totals)}")
    return 0


def selftest(work: Path) -> int:
    cases = (
        ("reordered", "public, max-age=600", "max-age=600, public"),
        ("numeric_parameter", "public, max-age=600", "public, max-age=60"),
        ("directive_added", "public", "public, immutable"),
        ("directive_removed", "public, immutable", "public"),
        ("directive_changed", "mode=one", "mode=two"),
        ("header_added", None, "public"),
        ("header_removed", "public", None),
        ("unclassified", "public", "bad directive"),
        ("directive_changed", "public", "private"),
        ("directive_changed", "mode", "mode=one"),
        ("directive_changed", "a=1, b=2", "a=3, b=4"),
        ("reordered", "public, public, max-age=1", "public, max-age=1, public"),
    )
    work.mkdir(parents=True, exist_ok=True)
    # A unique child keeps repeated runs from overwriting callers' fixtures.
    with tempfile.TemporaryDirectory(prefix="policy-selftest-", dir=work) as temporary:
        root = Path(temporary)
        declared = root / "declared.json"
        declared.write_text(json.dumps({"surfaces": [{"id": "s1", "url": "https://example.test/"}]}),
                            encoding="utf-8")
        results = []
        for index, (expected, before, after) in enumerate(cases):
            pair = root / str(index)
            for side, value in (("a", before), ("b", after)):
                directory = pair / side / "s1"
                directory.mkdir(parents=True)
                body = b"policy fixture\n"
                (directory / "body.bin").write_bytes(body)
                headers = ([] if value is None else [{"name": "Cache-Control", "value": value}])
                receipt = {"method": "GET", "status": 200, "bodyFile": "body.bin",
                           "bytes": len(body), "sha256": hashlib.sha256(body).hexdigest(),
                           "truncated": False, "headers": headers}
                (directory / "response.json").write_text(json.dumps(receipt), encoding="utf-8")
            a, _ = load_surface(pair / "a" / "s1")
            b, _ = load_surface(pair / "b" / "s1")
            observed, counts = classify(a, b)
            expected_verdict = ("policy-rewritten-equivalent" if expected == "reordered" else
                                "policy-unclassified" if expected == "unclassified" else "policy-changed")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = run(pair / "a", pair / "b", declared)
            expected_output = (f"change surface=s1 header=cache-control class={expected}\n"
                               f"surface=s1 {render(counts)} verdict={expected_verdict}\n"
                               f"summary surfaces=1 {render(counts)} verdict={expected_verdict}\n")
            results.append(observed == {"cache-control": expected} and counts["changed"] == 1
                           and code == 0 and stdout.getvalue() == expected_output)
        results.append(canonical([{"name": "CACHE-Control", "value": "public"},
                                  {"name": "cache-control", "value": "max-age=1"}])
                       == {"cache-control": "public, max-age=1"})
        results.append(verdict(dict.fromkeys(("changed", *CLASSES), 0)) == "policy-unchanged")
        # The last pair is otherwise valid: reject a single retained-body fault.
        (pair / "b" / "s1" / "body.bin").write_bytes(b"corrupt")
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = run(pair / "a", pair / "b", declared)
        results.append(code == 1 and not stdout.getvalue() and "fault:" in stderr.getvalue())
    passed = sum(results)
    print(f"selftest: {passed}/{len(results)} passed")
    return 0 if all(results) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0], allow_abbrev=False)
    parser.add_argument("--a")
    parser.add_argument("--b")
    parser.add_argument("--declared")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--work")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    if ((args.selftest and any((args.a, args.b, args.declared)))
            or (not args.selftest and (args.work or not all((args.a, args.b, args.declared))))):
        parser.print_usage(sys.stderr)
        return 64
    try:
        if args.selftest:
            if args.work:
                return selftest(Path(args.work))
            with tempfile.TemporaryDirectory(prefix="policy-selftest-") as temporary:
                return selftest(Path(temporary))
        return run(Path(args.a), Path(args.b), Path(args.declared))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(f"fault: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
