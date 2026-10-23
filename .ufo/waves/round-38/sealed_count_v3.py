#!/usr/bin/env python3
"""Round-38 sealed counter v3 for C2 (robots_audit round-38 contract: JSON numbers, URL characters,
normalized implicit /robots.txt allow; separation from a stdlib-delegating reader). C2 is the
redesign of round-38 C1, withdrawn before any build under its own declared rule; the v2 counter
(`sealed_count.py`, predicate `passed >= 19 of 20 sealed cases`) stays C1's rule of record.

Frozen predicate (the same sentence in SCORECARD "Round 38 — C2 declared", in this code and in
every receipt's `predicate` field):

    met: passed >= 20 of 20 sealed cases

Changes from v2: the target is every case; the key adds checks (one per excluded ASCII URL
character, and (c)/(d)/(k) checks); a finding whose check is a string that is not one of this run's
fresh ids never matches an expected check (v2 let a tool echo an original id, round-38 control
call MutCounterV2 F1); a missing --tool-file gives exit 2 with a JSON receipt (F2); a run whose
expectation carries `checksEvaluated` also requires the report's integer `checksEvaluated` to equal
it (round-38 control call CtlBaseWrapper: v2 ignored the count). PREDICATE carries the declared
sentence verbatim, `met:` included (CriticPredicate).

Adapted from the round-37 counter (`.ufo/waves/round-37/sealed_count.py`, which stays the rule of
record for round 37's C1): same jail, same fresh-id and fresh-file-name materialization, same
pin-and-refuse rules, same judge. One change: a run may carry `rawTemplate`, manifest text written
byte for byte (so it can hold literals such as NaN that JSON cannot carry), in which every
`@ID:<name>@` token becomes a fresh check id and every `@FILE:<name>@` token the fresh name of that
robots file; expected findings name ids by the same tokens.

The 20 cases were written by the L1 before this file and before any build. Until the reveal
commit they live outside the lane; this file pins their sha256, so they cannot change after the
declaration. The builder of the tool never sees them. A revision that already contains the key
file cannot be measured (exit 2), so nothing measured can be a copy of the key.

Usage:
  python3 -B sealed_count.py --root ROOT --revision REV (--key-revision KREV | --key-file PATH)
  python3 -B sealed_count.py --root ROOT --tool-file PATH (--key-revision KREV | --key-file PATH)

The tool at REV (or the file named by --tool-file, used to score the L1's private reference, its
ablations and control tools; receipts say which) runs once per run as
`python3 -B <tool> --manifest <manifest>` in a bubblewrap jail that sees only /usr and the scratch
directory, with a clean environment and a 20 s timeout. A run passes when the exit code, the
report's `verdict`, `checksEvaluated` (where the case states it) and the multiset of findings
projected on (check, reason) equal the sealed expectation. Other fields are not compared.

Exit 0 when met, 1 when not met, 2 when it cannot evaluate (unresolved revision, key sha256
mismatch, key visible at REV, no bwrap).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

KEY_PATH = ".ufo/waves/round-38/sealed/cases_v3.json"
KEY_SHA256 = "749ef6a65de67f09abffad33fa6d7efcb1e7f1515b1d2fa51a93ff9977b63aa6"
TOOL = "scripts/robots_audit.py"
CASES = 20
TARGET = 20
PREDICATE = "met: passed >= 20 of 20 sealed cases"
TIMEOUT = 20


def _env() -> dict[str, str]:
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=_env())


def resolve(root: str, revision: str) -> str | None:
    proc = git(root, "rev-parse", "--verify", "--quiet", f"{revision}^{{commit}}")
    return proc.stdout.decode().strip() if proc.returncode == 0 else None


def show(root: str, revision: str, path: str) -> bytes | None:
    proc = git(root, "show", f"{revision}:{path}")
    return proc.stdout if proc.returncode == 0 else None


def load_key(args: argparse.Namespace) -> tuple[dict | None, str]:
    if args.key_file:
        data = Path(args.key_file).read_bytes()
    else:
        krev = resolve(args.root, args.key_revision)
        data = show(args.root, krev, KEY_PATH) if krev else None
        if data is None:
            return None, "key not found at key revision"
    digest = hashlib.sha256(data).hexdigest()
    if digest != KEY_SHA256:
        return None, f"key sha256 {digest} != pinned {KEY_SHA256}"
    return json.loads(data), "ok"


def project(findings: list, idmap: dict | None) -> list:
    """Project findings on (check, reason). With an id map (observed findings), a string check
    that is not a fresh id of this run becomes an unmatched marker; None (expected findings)
    keeps checks as written."""
    rows = []
    for f in findings:
        if not isinstance(f, dict):
            rows.append(("<non-object>",))
            continue
        check = f.get("check")
        if idmap is not None:
            try:
                check = idmap[check] if check in idmap else (["<not-a-fresh-id>", check] if check is not None else None)
            except TypeError:
                check = ["<unhashable>", repr(check)]
        rows.append((json.dumps(check), str(f.get("reason"))))
    return sorted(rows)


def materialize(run: dict, work: Path) -> tuple[Path, dict]:
    """Write one run under `work` with fresh ids and file names; return manifest path, id map."""
    names = {}
    for rel, body in run["files"].items():
        data = base64.b64decode(body["b64"])
        fresh = uuid.uuid4().hex
        base = rel.rsplit("/", 1)[-1]
        if rel.startswith("../"):
            (work.parent / fresh).write_bytes(data)
        else:
            (work / fresh).write_bytes(data)
        names[base] = fresh
    idmap: dict = {}
    if "rawTemplate" in run:
        text = run["rawTemplate"]
        for token in sorted(set(re.findall(r"@ID:[A-Za-z0-9_]+@", text))):
            idmap[token] = "c" + uuid.uuid4().hex[:12]
            text = text.replace(token, idmap[token])
        for token in sorted(set(re.findall(r"@FILE:[^@]+@", text))):
            text = text.replace(token, names[token[6:-1]])
        mpath = work / f"m{uuid.uuid4().hex[:8]}.json"
        mpath.write_bytes(text.encode("utf-8"))
        return mpath, idmap
    if "raw" in run:
        mpath = work / f"m{uuid.uuid4().hex[:8]}.json"
        mpath.write_bytes(base64.b64decode(run["raw"]["b64"]))
        return mpath, idmap
    manifest = run["manifest"]
    if isinstance(manifest, dict) and isinstance(manifest.get("checks"), list):
        checks = []
        for c in manifest["checks"]:
            if isinstance(c, dict):
                c = dict(c)
                if isinstance(c.get("id"), str) and c["id"]:
                    c["id"] = idmap.setdefault(c["id"], "c" + uuid.uuid4().hex[:12])
                r = c.get("robots")
                if isinstance(r, str):
                    head, _, tail = r.rpartition("/")
                    if tail in names:
                        c["robots"] = (head + "/" if _ else "") + names[tail]
            checks.append(c)
        manifest = dict(manifest, checks=checks)
    mpath = work / f"m{uuid.uuid4().hex[:8]}.json"
    mpath.write_text(json.dumps(manifest), encoding="utf-8")
    return mpath, idmap


def judge(run: dict, proc: subprocess.CompletedProcess | None, idmap: dict) -> bool:
    exp = run["expect"]
    if proc is None or proc.returncode != exp["exit"]:
        return False
    try:
        report = json.loads(proc.stdout)
    except (ValueError, RecursionError):
        return False
    if not isinstance(report, dict) or report.get("verdict") != exp["verdict"]:
        return False
    if "checksEvaluated" in exp and (type(report.get("checksEvaluated")) is not int
                                     or report["checksEvaluated"] != exp["checksEvaluated"]):
        return False
    findings = report.get("findings")
    if not isinstance(findings, list):
        return False
    inverse = {v: k for k, v in idmap.items()}
    observed = project(findings, inverse)
    expected = project(exp["findings"], None)
    return observed == expected


def jail(scratch: str, work: Path) -> list[str]:
    """The tool runs in a bubblewrap jail that sees only /usr and the scratch directory (the
    current run, the tool file). No /home, no other /fast path, no network, its own pid
    namespace, so it cannot read the key file, the lane repository or this counter's command
    line. Each run's directory is removed after the run."""
    return ["bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64",
            "/lib64", "--symlink", "usr/bin", "/bin", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
            "--bind", scratch, scratch, "--chdir", str(work), "--unshare-all", "--die-with-parent",
            "--clearenv", "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", scratch,
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "PYTHONDONTWRITEBYTECODE", "1"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--revision")
    src.add_argument("--tool-file")
    keysrc = ap.add_mutually_exclusive_group(required=True)
    keysrc.add_argument("--key-revision")
    keysrc.add_argument("--key-file")
    args = ap.parse_args()
    out: dict = {"claim": "C2", "predicate": PREDICATE, "counterSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    rev = None
    if args.revision:
        rev = resolve(args.root, args.revision)
        if rev is None:
            out["error"] = "unresolved revision"
            print(json.dumps(out, indent=1))
            return 2
        out["revision"] = rev
        if show(args.root, rev, KEY_PATH) is not None:
            out["error"] = "key visible at the measured revision"
            print(json.dumps(out, indent=1))
            return 2
        tool = show(args.root, rev, TOOL)
    else:
        out["toolFile"] = args.tool_file
        try:
            tool = Path(args.tool_file).read_bytes()
        except OSError as exc:
            out["error"] = f"tool file unreadable: {exc}"
            print(json.dumps(out, indent=1))
            return 2
    if shutil.which("bwrap") is None or not Path("/usr/bin/python3").is_file():
        out["error"] = "bwrap or /usr/bin/python3 missing: the tool cannot be jailed"
        print(json.dumps(out, indent=1))
        return 2
    key, why = load_key(args)
    if key is None:
        out["error"] = why
        print(json.dumps(out, indent=1))
        return 2
    rows = []
    with tempfile.TemporaryDirectory(prefix="kake-r38-c2-") as scratch:
        tool_path = None
        if tool is not None:
            tool_path = Path(scratch) / f"t{uuid.uuid4().hex}.py"
            tool_path.write_bytes(tool)
        for case in key["cases"]:
            ok = tool_path is not None
            for run in case["runs"]:
                if not ok:
                    break
                proc, idmap = None, {}
                case_dir = Path(scratch) / uuid.uuid4().hex
                case_dir.mkdir()
                work = case_dir / uuid.uuid4().hex
                work.mkdir()
                mpath, idmap = materialize(run, work)
                try:
                    proc = subprocess.run(jail(scratch, work) + ["/usr/bin/python3", "-B", str(tool_path),
                                          "--manifest", str(mpath)], cwd=work, capture_output=True,
                                          timeout=TIMEOUT, env={})
                    proc.stdout = proc.stdout.decode("utf-8", "replace")
                except subprocess.TimeoutExpired:
                    proc = None
                ok = judge(run, proc, idmap)
                shutil.rmtree(case_dir, ignore_errors=True)
            rows.append({"id": case["id"], "passed": bool(ok)})
    passed = sum(r["passed"] for r in rows)
    met = len(rows) == CASES and passed >= TARGET
    out.update({"toolPresent": tool is not None,
                "toolSha256": hashlib.sha256(tool).hexdigest() if tool is not None else None,
                "cases": len(rows), "passed": passed, "target": TARGET, "met": met, "perCase": rows})
    print(json.dumps(out, indent=1))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
