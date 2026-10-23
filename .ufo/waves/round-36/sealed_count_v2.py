#!/usr/bin/env python3
"""Round-36 sealed counter for C1 (source re-check audit, `scripts/source_recheck.py`).

Frozen predicate (the same sentence in SCORECARD "Round 36 — declared claims", in this code and
in every receipt's `predicate` field):

    met: passed >= 25 of 28 sealed cases

The 28 cases were written by the L1 before this file and before any build. Until the reveal
commit they live outside the lane; this file pins their sha256, so they cannot change after the
declaration. The builder of the tool never sees them. A revision that already contains the key
file cannot be measured (exit 2), so nothing measured can be a copy of the key.

Usage:
  python3 -B sealed_count.py --root ROOT --revision REV (--key-revision KREV | --key-file PATH)
  python3 -B sealed_count.py --root ROOT --tool-file PATH (--key-revision KREV | --key-file PATH)

The tool `scripts/source_recheck.py` at REV (or the file named by --tool-file, used only to score
the L1's private reference and its ablations; receipts say which) runs once per case as
`python3 -B <tool> --manifest <manifest>` with a clean environment and a 20 s timeout. Each case is
materialized under a fresh random directory. Every check id is replaced by a fresh random id and
every body file by a fresh random name (no extension) on each run, and the expected findings are
mapped the same way, so no tool can key on ids, file names or labels. A case passes when the exit
code, the report's `verdict` and the multiset of findings projected on (check, reason, target)
equal the sealed expectation; `target` is compared for `moved` findings only (others project to
null). `checksEvaluated` and any other field are not compared.

Version 2 (before any build and before any control seat's tool was scored; version 1 is kept
as `sealed_count_v1.py`): the L1's own review found that a tool run by version 1 could read this
counter's command line through /proc and so learn the key path or key revision, then read the key
from the lane. Version 2 runs the tool in a bubblewrap jail (see `jail`). The cases, the key pin,
the projection, the judge and the predicate are unchanged.

Exit 0 when met, 1 when not met, 2 when it cannot evaluate (unresolved revision, key sha256
mismatch, key visible at REV).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

KEY_PATH = ".ufo/waves/round-36/sealed/cases.json"
KEY_SHA256 = "a690d39e912cf641baa14f101f461e31304ac336c59a41c9689aacf91e02f9ca"
TOOL = "scripts/source_recheck.py"
CASES = 28
TARGET = 25
PREDICATE = "passed >= 25 of 28 sealed cases"
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


def project(findings: list, idmap: dict) -> list:
    rows = []
    for f in findings:
        if not isinstance(f, dict):
            rows.append(("<non-object>",))
            continue
        reason = f.get("reason")
        target = f.get("target") if reason == "moved" else None
        check = f.get("check")
        rows.append((json.dumps(idmap.get(check, check)), str(reason), json.dumps(target)))
    return sorted(rows)


def materialize(case: dict, work: Path) -> tuple[Path, dict]:
    """Write the case under `work` with fresh ids and file names; return manifest path, id map."""
    names = {}
    for rel, body in case["files"].items():
        data = base64.b64decode(body["b64"])
        fresh = uuid.uuid4().hex
        if rel.startswith("../"):
            (work.parent / fresh).write_bytes(data)
            names[rel] = "../" + fresh
        else:
            (work / fresh).write_bytes(data)
            names[rel] = fresh
    idmap = {}
    checks = []
    for c in case["manifest"]["checks"]:
        if isinstance(c, dict):
            c = dict(c)
            if isinstance(c.get("id"), str) and c["id"]:
                idmap[c["id"]] = "c" + uuid.uuid4().hex[:12]
                c["id"] = idmap[c["id"]]
            if isinstance(c.get("body"), str) and c["body"] in names:
                c["body"] = names[c["body"]]
        checks.append(c)
    manifest = dict(case["manifest"], checks=checks)
    mpath = work / f"m{uuid.uuid4().hex[:8]}.json"
    mpath.write_text(json.dumps(manifest), encoding="utf-8")
    return mpath, idmap


def judge(case: dict, proc: subprocess.CompletedProcess | None, idmap: dict) -> bool:
    exp = case["expect"]
    if proc is None or proc.returncode != exp["exit"]:
        return False
    try:
        report = json.loads(proc.stdout)
    except (ValueError, RecursionError):
        return False
    if not isinstance(report, dict) or report.get("verdict") != exp["verdict"]:
        return False
    findings = report.get("findings")
    if not isinstance(findings, list):
        return False
    inverse = {v: k for k, v in idmap.items()}
    observed = project(findings, inverse)
    expected = project(exp["findings"], {})
    return observed == expected


def jail(scratch: str, work: Path) -> list[str]:
    """Version 2: the tool runs in a bubblewrap jail that sees only /usr and the scratch
    directory (its case, the tool file and the escaping body file). No /home, no other
    /fast path, no network, its own pid namespace, so it cannot read the key file, the lane
    repository or this counter's command line (which names the key path or key revision)."""
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
    out: dict = {"claim": "C1", "predicate": PREDICATE, "counterSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
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
        tool = Path(args.tool_file).read_bytes()
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
    with tempfile.TemporaryDirectory(prefix="kake-r36-c1-") as scratch:
        tool_path = None
        if tool is not None:
            tool_path = Path(scratch) / f"t{uuid.uuid4().hex}.py"
            tool_path.write_bytes(tool)
        for case in key["cases"]:
            proc, idmap = None, {}
            if tool_path is not None:
                work = Path(scratch) / uuid.uuid4().hex
                work.mkdir()
                mpath, idmap = materialize(case, work)
                try:
                    proc = subprocess.run(jail(scratch, work) + ["/usr/bin/python3", "-B", str(tool_path),
                                          "--manifest", str(mpath)], cwd=work, capture_output=True,
                                          timeout=TIMEOUT, env={})
                    proc.stdout = proc.stdout.decode("utf-8", "replace")
                except subprocess.TimeoutExpired:
                    proc = None
            rows.append({"id": case["id"], "passed": judge(case, proc, idmap)})
    passed = sum(r["passed"] for r in rows)
    met = len(rows) == CASES and passed >= TARGET
    out.update({"toolPresent": tool is not None,
                "toolSha256": hashlib.sha256(tool).hexdigest() if tool is not None else None,
                "cases": len(rows), "passed": passed, "target": TARGET, "met": met, "perCase": rows})
    print(json.dumps(out, indent=1))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
