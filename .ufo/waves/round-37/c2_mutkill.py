#!/usr/bin/env python3
"""Round-37 counter for C2 (operability: the fixture set of `scripts/source_recheck_selftest.py`).

Frozen predicate (the same sentence in SCORECARD "Round 37 — declared claims", in this code and
in every receipt's `predicate` field):

    met: killed >= 32 of 32 round-36 tool mutants

The 32 mutants are round-36 wave-2 `MutTool`'s single-point mutants of the measured tool
(`4d5b3d55:scripts/source_recheck.py`, sha256 577b2d7d…0d48), copied byte-exact into
`.ufo/waves/round-37/c2/mutants/` with MutTool's manifest (each mutant's sha256 is checked
against it; the manifest itself is pinned below).

The counter never runs the selftest's own runner, so the selftest cannot recognize a mutant by
its hash, name or text: it only reads the selftest's fixture DATA. At REV it extracts
`scripts/source_recheck_selftest.py`, imports it inside a bubblewrap jail that sees only /usr and
a scratch directory holding that one file, and dumps its `FIXTURES` list. Then it runs every
fixture itself (a frozen copy of the round-36 selftest judgment, `judge` below: exit code among
the accepted ones; for shape fixtures and exits other than 64 one JSON object with version 1,
a findings list, the verdict, the findings projected on (check, reason) plus target for `moved`,
and checksEvaluated when the fixture names it; no file written) against:

  E1  the measured round-36 tool  `4d5b3d55:scripts/source_recheck.py`
  E2  the round-36 independent blind implementation
      `1a16b8e3:.ufo/waves/round-36/retained/independent/selftest-seat-reference.py`
  M01..M32  the mutants

A fixture is valid when it passes on both E1 and E2 (so a fixture whose expectation is junk, or
encodes one implementation's reading the other does not share, counts for nothing). A mutant is
killed when at least one valid fixture fails on it. Every tool runs in the jail with a clean
environment and a 60 s timeout per fixture.

Usage:  python3 -B c2_mutkill.py --root ROOT --revision REV [--jobs N]
Exit 0 when met, 1 when not met, 2 when it cannot evaluate.
"""
from __future__ import annotations

import argparse
import base64
import concurrent.futures as cf
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

PREDICATE = "killed >= 32 of 32 round-36 tool mutants"
TARGET = 32
MUTANTS = 32
SELFTEST = "scripts/source_recheck_selftest.py"
MUTDIR = ".ufo/waves/round-37/c2/mutants"
MANIFEST_SHA256 = "9300ad38e992a95381f8526379b71125c585dc43d1b833d739c771c45134dbd4"
E1 = ("4d5b3d550748e5b52af31646b74c1aa435942bde", "scripts/source_recheck.py",
      "577b2d7d028964e06152f5a7b792141e586045eaa8ec9262ee7f416ba5510d48")
E2 = ("1a16b8e3faebcd24718c2cde6bf0c04b4c09cc59",
      ".ufo/waves/round-36/retained/independent/selftest-seat-reference.py",
      "a5176feed87d9cd10d04b14f6fce3ef947f0266796ceb4778ece8ccbc0dd221f")
TIMEOUT = 60

DUMPER = r'''
import base64, importlib.util, json, sys
spec = importlib.util.spec_from_file_location("kake_selftest_under_count", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
sys.argv = [sys.argv[1]]
spec.loader.exec_module(mod)
fx = getattr(mod, "FIXTURES", None)
if not fx and hasattr(mod, "build_fixtures"):
    mod.build_fixtures()
    fx = mod.FIXTURES
def enc(o):
    if isinstance(o, (bytes, bytearray)):
        return {"__b64__": base64.b64encode(bytes(o)).decode()}
    if isinstance(o, dict):
        return {str(k): enc(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [enc(v) for v in o]
    return o
print(json.dumps({"fixtures": enc(list(fx)), "reasons": list(getattr(mod, "REASONS", ()))}))
'''


def dec(o):
    if isinstance(o, dict):
        if set(o) == {"__b64__"}:
            return base64.b64decode(o["__b64__"])
        return {k: dec(v) for k, v in o.items()}
    if isinstance(o, list):
        return [dec(v) for v in o]
    return o


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


def jail(scratch: str, cwd: Path) -> list[str]:
    return ["bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib", "--symlink", "usr/lib64",
            "/lib64", "--symlink", "usr/bin", "/bin", "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
            "--bind", scratch, scratch, "--chdir", str(cwd), "--unshare-all", "--die-with-parent",
            "--clearenv", "--setenv", "PATH", "/usr/bin", "--setenv", "HOME", scratch,
            "--setenv", "LC_ALL", "C.UTF-8", "--setenv", "PYTHONDONTWRITEBYTECODE", "1"]


def project(findings: list) -> list:
    rows = []
    for item in findings:
        if not isinstance(item, dict):
            rows.append(("<non-object>",))
            continue
        reason = item.get("reason")
        check = item.get("check")
        try:
            json.dumps(check)
        except (TypeError, ValueError):
            check = repr(check)
        if reason == "moved":
            rows.append((json.dumps(check), str(reason), json.dumps(item.get("target"), default=repr)))
        else:
            rows.append((json.dumps(check), str(reason)))
    return sorted(rows)


def snapshot(root: Path) -> set:
    return {str(p.relative_to(root)) for p in root.rglob("*")}


def run_fixture(tool: Path, fx: dict, scratch: str, reasons: list) -> bool:
    """Frozen copy of the round-36 selftest judgment (scripts/source_recheck_selftest.py
    `run_case` at 1a16b8e3), run inside the jail. True when the tool passes the fixture."""
    box = Path(scratch) / uuid.uuid4().hex
    try:
        work = box / "w"
        case_dir = work / "case"
        case_dir.mkdir(parents=True)
        for rel, data in (fx.get("files") or {}).items():
            target = (case_dir / rel).resolve()
            if not str(target).startswith(str(box) + os.sep):
                return False
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data if isinstance(data, bytes) else str(data).encode())
        mpath = case_dir / "manifest.json"
        if fx.get("raw") is not None:
            mpath.write_bytes(fx["raw"] if isinstance(fx["raw"], bytes) else str(fx["raw"]).encode())
        elif fx.get("manifest") is not None:
            mpath.write_text(json.dumps(fx["manifest"]), encoding="utf-8")
        argv = fx.get("argv")
        argv = ["--manifest", str(mpath)] if argv is None else [str(mpath) if a == "{manifest}" else str(a) for a in argv]
        before = snapshot(work)
        try:
            proc = subprocess.run(jail(scratch, case_dir) + ["/usr/bin/python3", "-B", str(tool)] + argv,
                                  cwd=str(case_dir), capture_output=True, timeout=TIMEOUT, env={})
        except subprocess.TimeoutExpired:
            return False
        if snapshot(work) - before:
            return False
        stdout = proc.stdout.decode("utf-8", "replace")
        accepted = [{"exit": fx.get("exit"), "verdict": fx.get("verdict"), "findings": fx.get("findings") or [],
                     "evaluated": fx.get("evaluated")}] + list(fx.get("accept") or [])
        if proc.returncode not in {a.get("exit") for a in accepted}:
            return False
        if not fx.get("shape", True) or proc.returncode == 64:
            return True
        try:
            report = json.loads(stdout)
        except (ValueError, RecursionError):
            return False
        if not isinstance(report, dict) or report.get("version") != 1:
            return False
        findings = report.get("findings")
        if not isinstance(findings, list):
            return False
        for item in findings:
            if not isinstance(item, dict) or not isinstance(item.get("reason"), str) or item["reason"] not in reasons:
                return False
            if item.get("check") is not None and not isinstance(item.get("check"), str):
                return False
            if item.get("target") is not None and not isinstance(item.get("target"), str):
                return False
        got = project(findings)
        for want in accepted:
            if want.get("exit") != proc.returncode:
                continue
            if want.get("verdict") is not None and report.get("verdict") != want["verdict"]:
                continue
            if project(want.get("findings") or []) != got:
                continue
            if want.get("evaluated") is not None and report.get("checksEvaluated") != want["evaluated"]:
                continue
            return True
        return False
    finally:
        shutil.rmtree(box, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()
    out: dict = {"claim": "C2", "predicate": PREDICATE,
                 "counterSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

    def fail(msg: str) -> int:
        out["error"] = msg
        print(json.dumps(out, indent=1))
        return 2

    rev = resolve(args.root, args.revision)
    if rev is None:
        return fail("unresolved revision")
    out["revision"] = rev
    if shutil.which("bwrap") is None or not Path("/usr/bin/python3").is_file():
        return fail("bwrap or /usr/bin/python3 missing")
    selftest = show(args.root, rev, SELFTEST)
    if selftest is None:
        return fail("selftest absent at revision")
    out["selftestSha256"] = hashlib.sha256(selftest).hexdigest()
    mroot = Path(args.root) / MUTDIR
    mbytes = (mroot / "MutTool-manifest.json").read_bytes() if (mroot / "MutTool-manifest.json").is_file() else b""
    if hashlib.sha256(mbytes).hexdigest() != MANIFEST_SHA256:
        return fail("mutant manifest missing or sha256 differs from the pin")
    manifest = json.loads(mbytes)
    tools: dict[str, bytes] = {}
    for name, (r, p, pin) in (("E1", E1), ("E2", E2)):
        data = show(args.root, r, p)
        if data is None or hashlib.sha256(data).hexdigest() != pin:
            return fail(f"{name} missing or sha256 differs")
        tools[name] = data
    for m in manifest["mutants"]:
        data = (mroot / f"{m['id']}.py").read_bytes()
        if hashlib.sha256(data).hexdigest() != m["mutantSha256"]:
            return fail(f"mutant {m['id']} sha256 differs")
        tools[m["id"]] = data
    if len(manifest["mutants"]) != MUTANTS:
        return fail("mutant count differs")
    with tempfile.TemporaryDirectory(prefix="kake-r37-c2-") as scratch:
        dumpdir = Path(scratch) / "dump"
        dumpdir.mkdir()
        sfile = dumpdir / f"s{uuid.uuid4().hex}.py"
        sfile.write_bytes(selftest)
        dfile = dumpdir / "dump.py"
        dfile.write_text(DUMPER, encoding="utf-8")
        try:
            proc = subprocess.run(jail(scratch, dumpdir) + ["/usr/bin/python3", "-B", str(dfile), str(sfile)],
                                  capture_output=True, timeout=300, env={})
            dumped = json.loads(proc.stdout)
        except (subprocess.TimeoutExpired, ValueError):
            return fail("fixture dump failed")
        shutil.rmtree(dumpdir, ignore_errors=True)
        fixtures = dec(dumped["fixtures"])
        reasons = list(dumped.get("reasons") or [])
        tdir = Path(scratch) / "tools"
        tdir.mkdir()
        paths = {}
        for name, data in tools.items():
            paths[name] = tdir / f"t{uuid.uuid4().hex}.py"
            paths[name].write_bytes(data)
        jobs = [(name, i) for name in tools for i in range(len(fixtures))]
        with cf.ThreadPoolExecutor(max_workers=max(1, args.jobs)) as ex:
            res = dict(zip(jobs, ex.map(lambda j: run_fixture(paths[j[0]], fixtures[j[1]], scratch, reasons), jobs)))
    names = [str(f.get("name")) for f in fixtures]
    valid = [i for i in range(len(fixtures)) if res[("E1", i)] and res[("E2", i)]]
    per_mutant = []
    for m in manifest["mutants"]:
        killers = [names[i] for i in valid if not res[(m["id"], i)]]
        per_mutant.append({"id": m["id"], "bullet": m.get("bullet"), "skippedRule": m.get("skippedRule"),
                           "killed": bool(killers), "killers": killers[:8], "killerCount": len(killers)})
    killed = sum(p["killed"] for p in per_mutant)
    met = len(per_mutant) == MUTANTS and killed >= TARGET
    out.update({"fixtures": len(fixtures), "validFixtures": len(valid),
                "failedOnE1": [names[i] for i in range(len(fixtures)) if not res[("E1", i)]],
                "failedOnE2": [names[i] for i in range(len(fixtures)) if not res[("E2", i)]],
                "mutants": len(per_mutant), "killed": killed, "target": TARGET, "met": met,
                "survivors": [p["id"] for p in per_mutant if not p["killed"]], "perMutant": per_mutant})
    print(json.dumps(out, indent=1))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
