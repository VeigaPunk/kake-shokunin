#!/usr/bin/env python3
"""Run a robots_audit.py tool over the round-38 real-run manifests and compare
its report with expectations.json (declared from the public contract text).

usage: run_realrun.py --tool PATH --out DIR [--timeout SECONDS]

Each manifest is run in this directory with `python3 -B <tool> --manifest NAME`,
cwd = this directory, a 20 s cap (contract bound), a fixed minimal environment,
and no network or writes by the harness. One receipt per manifest plus a
summary are written under --out. A receipt records the tool's sha256 (routed
defect 5), its exit code, stdout, stderr, the observed report, the declared
expected report, and the exact differences.

The comparison is exact: exit code, verdict, checksEvaluated, and the multiset
of {check, reason} findings. A tool that reports the right verdict but the wrong
number of evaluated checks, or a fault for the wrong check, is a mismatch.

Exit: 0 when every manifest matches, 1 on any mismatch, 2 when a run could not
be evaluated (tool missing, timeout, unparseable output).
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def finding_key(item):
    if not isinstance(item, dict):
        return ("<non-object>", json.dumps(item, sort_keys=True))
    return (item.get("check"), item.get("reason"))


def compare(expected, observed):
    """Return a list of human-readable differences; empty means match."""
    diffs = []
    for key in ("exit", "verdict", "checksEvaluated"):
        if observed.get(key) != expected[key]:
            diffs.append(f"{key}: expected {expected[key]!r}, observed {observed.get(key)!r}")
    exp_findings = sorted(finding_key(x) for x in expected["findings"])
    got = observed.get("findings")
    if not isinstance(got, list):
        diffs.append(f"findings: expected a list, observed {type(got).__name__}")
        return diffs
    got_findings = sorted(finding_key(x) for x in got)
    if got_findings != exp_findings:
        missing = [f for f in exp_findings if f not in got_findings]
        extra = [f for f in got_findings if f not in exp_findings]
        if missing:
            diffs.append("findings missing: " + json.dumps(missing, ensure_ascii=False))
        if extra:
            diffs.append("findings extra: " + json.dumps(extra, ensure_ascii=False))
        if not missing and not extra:
            diffs.append("findings differ in multiplicity")
    return diffs


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--timeout", type=float, default=20.0)
    args = parser.parse_args(argv)

    tool = os.path.abspath(args.tool)
    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    if not os.path.isfile(tool):
        print(f"run_realrun.py: no tool at {tool}", file=sys.stderr)
        return 2
    tool_sha = sha256_file(tool)

    expectations = json.load(open(os.path.join(HERE, "expectations.json"), encoding="utf-8"))
    manifests = expectations["manifests"]

    env = {
        "PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
        "HOME": os.environ.get("HOME", "/tmp"),
        "TMPDIR": os.environ.get("TMPDIR", "/tmp"),
        "PYTHONDONTWRITEBYTECODE": "1",
        "LANG": "C.UTF-8",
    }

    summary = {"version": 1, "tool": tool, "toolSha256": tool_sha,
               "python": sys.version, "pythonExecutable": sys.executable,
               "timeoutSeconds": args.timeout, "runs": [], "unrunnable": []}
    worst = 0
    for name in sorted(manifests):
        expected = manifests[name]
        manifest_path = os.path.join(HERE, name)
        manifest_sha = sha256_file(manifest_path) if os.path.isfile(manifest_path) else None
        cmd = [sys.executable, "-B", tool, "--manifest", name]
        receipt = {
            "manifest": name,
            "manifestSha256": manifest_sha,
            "tool": tool,
            "toolSha256": tool_sha,
            "command": cmd,
            "cwd": HERE,
            "python": sys.version,
            "pythonExecutable": sys.executable,
            "environment": env,
            "expected": {k: expected[k] for k in ("exit", "verdict", "checksEvaluated", "findings")},
            "expectedBasis": expected["basis"],
        }
        try:
            proc = subprocess.run(cmd, cwd=HERE, env=env, capture_output=True, text=True,
                                  timeout=args.timeout)
        except subprocess.TimeoutExpired as exc:
            receipt.update({"status": "timeout", "matches": False,
                            "stdout": (exc.stdout or b"").decode("utf-8", "replace")
                            if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
                            "stderr": (exc.stderr or b"").decode("utf-8", "replace")
                            if isinstance(exc.stderr, bytes) else (exc.stderr or ""),
                            "diffs": [f"timed out after {args.timeout}s"]})
            summary["unrunnable"].append(name)
            worst = max(worst, 2)
        else:
            observed = {}
            parse_error = None
            try:
                observed = json.loads(proc.stdout)
            except json.JSONDecodeError as exc:
                parse_error = f"stdout is not JSON: {exc}"
            if not isinstance(observed, dict):
                parse_error = parse_error or "stdout JSON is not an object"
            observed = observed if isinstance(observed, dict) else {}
            observed = dict(observed)
            observed["exit"] = proc.returncode
            receipt.update({
                "status": "ran",
                "exit": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "observed": observed,
            })
            if parse_error:
                receipt["matches"] = False
                receipt["diffs"] = [parse_error]
                summary["unrunnable"].append(name)
                worst = max(worst, 2)
            else:
                diffs = compare(expected, observed)
                receipt["matches"] = not diffs
                receipt["diffs"] = diffs
                if diffs:
                    worst = max(worst, 1)
        with open(os.path.join(out, f"receipt-{name.replace('.json', '')}.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        summary["runs"].append({
            "manifest": name,
            "matches": receipt["matches"],
            "exit": receipt.get("exit"),
            "expectedExit": expected["exit"],
            "expectedVerdict": expected["verdict"],
            "observedVerdict": (receipt.get("observed") or {}).get("verdict"),
            "expectedChecksEvaluated": expected["checksEvaluated"],
            "observedChecksEvaluated": (receipt.get("observed") or {}).get("checksEvaluated"),
            "diffs": receipt["diffs"],
        })
        print(f"{name}: matches={receipt['matches']} exit={receipt.get('exit')} "
              f"diffs={len(receipt['diffs'])}", flush=True)

    summary["allMatch"] = worst == 0
    summary["worst"] = worst
    with open(os.path.join(out, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"tool sha256 {tool_sha}: {'all match' if worst == 0 else 'mismatches'}")
    return worst


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
