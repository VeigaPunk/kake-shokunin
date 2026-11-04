#!/usr/bin/env python3
"""Round-79 C2 counter — frozen X-Robots-Tag case matrix (kake, operability capability).

Runs a same-CLI `scripts/x_robots_tag_audit.py` over the frozen case set and compares, per
case, the exit code, the report's global finding-id list and every check's `directives`,
`effective` and `bots` sets against the oracle in `expect/expect.json` (kept outside the case
directories; each manifest is copied to scratch first, so the tool receives payloads only).

Frozen predicate (contract §C2):

    met <=> decided == cases AND wrong == 0 AND constants_failed == 4/4 AND selftest_ok

Then runs four degenerate constants over the same cases; each must fail at least one case.

Exit: 0 met, 1 not met, 2 unevaluable input, 64 usage. Read-only outside --work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL_REL = "scripts/x_robots_tag_audit.py"
REPORT_SCHEMA = "x-robots-tag-report/v1"


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run_tool(tool: Path, manifest: Path) -> tuple[int, str, str]:
    p = subprocess.run([sys.executable, "-B", str(tool), "--manifest", str(manifest), "--json"],
                       capture_output=True, text=True, timeout=120)
    return p.returncode, p.stdout, p.stderr


def parse_report(stdout: str):
    try:
        doc = json.loads(stdout.strip())
    except json.JSONDecodeError:
        return None
    if not isinstance(doc, dict) or doc.get("schema") != REPORT_SCHEMA:
        return None
    return doc


def compare(exp: dict, report: dict, code: int) -> tuple[bool, str]:
    if "error" in exp:
        if exp["exit"] != code:
            return False, f"error-exit:{code}!={exp['exit']}"
        got = (report.get("error") or {}).get("id")
        return (got == exp["error"], "" if got == exp["error"] else f"error-id:{got}!={exp['error']}")
    if code != exp["exit"]:
        return False, f"exit:{code}!={exp['exit']}"
    got_findings = sorted(set(report.get("findings") or []))
    if got_findings != exp["findings"]:
        return False, f"findings:{got_findings}!={exp['findings']}"
    checks = {}
    for c in report.get("checks") or []:
        if isinstance(c, dict) and isinstance(c.get("id"), str):
            checks[c["id"]] = c
    if len(checks) != len(exp["checks"]):
        return False, f"checks:{len(checks)}!={len(exp['checks'])}"
    for cid, want in exp["checks"].items():
        got = checks.get(cid)
        if got is None:
            return False, f"missing-check:{cid}"
        for field in ("directives", "effective"):
            if sorted(got.get(field) or []) != want[field]:
                return False, f"{field}:{cid}:{sorted(got.get(field) or [])}!={want[field]}"
        gb = got.get("bots") or {}
        if not isinstance(gb, dict) or {k: sorted(v) for k, v in gb.items()} != want["bots"]:
            return False, f"bots:{cid}"
    return True, ""


def run_cases(tool: Path, cases: list[tuple[str, Path]], expect: dict, work: Path) -> dict:
    inputs = work / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    out = {"cases": len(cases), "decided": 0, "correct": 0, "wrong": 0, "undecided": 0,
           "details": []}
    for cid, manifest in cases:
        dst = inputs / f"{cid}.json"
        shutil.copyfile(manifest, dst)
        code, stdout, _ = run_tool(tool, dst)
        report = parse_report(stdout)
        if report is None:
            out["undecided"] += 1
            out["details"].append((cid, "undecided", "no parseable report"))
            continue
        out["decided"] += 1
        ok, why = compare(expect[cid], report, code)
        if ok:
            out["correct"] += 1
        else:
            out["wrong"] += 1
            out["details"].append((cid, "wrong", why))
    return out


def selftest(work: Path) -> tuple[bool, list[str]]:
    base = work / "selftest"
    cases_dir = base / "cases"
    tools_dir = base / "tools"
    cases_dir.mkdir(parents=True, exist_ok=True)
    tools_dir.mkdir(parents=True, exist_ok=True)
    checks: list[tuple[str, bool, str]] = []
    expect = {"s1": {"exit": 0, "findings": [],
                     "checks": {"s1": {"directives": ["noindex"], "effective": ["noindex"], "bots": {}}}},
              "s2": {"exit": 1, "findings": ["xrt_empty_rule"],
                     "checks": {"s2": {"directives": [], "effective": [], "bots": {}}}},
              "s3": {"exit": 2, "error": "xrt_input_schema"}}
    cases = []
    for cid, payload in [("s1", {"schema": "x-robots-tag-manifest/v1", "checks": []}),
                         ("s2", {"schema": "x-robots-tag-manifest/v1", "checks": []}),
                         ("s3", {"schema": "x-robots-tag-manifest/v1", "checks": []})]:
        d = cases_dir / cid
        d.mkdir(parents=True, exist_ok=True)
        (d / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
        cases.append((cid, d / "manifest.json"))

    header = "import json,sys\n"
    good = header + (
        "a=sys.argv.index('--manifest'); cid=sys.argv[a+1].split('/')[-1][:-5]\n"
        "R={'s1':{'schema':'x-robots-tag-report/v1','checks':[{'id':'s1','directives':['noindex'],'effective':['noindex'],'bots':{}}],'findings':[],'exit':0},"
        "'s2':{'schema':'x-robots-tag-report/v1','checks':[{'id':'s2','directives':[],'effective':[],'bots':{}}],'findings':['xrt_empty_rule'],'exit':1},"
        "'s3':{'schema':'x-robots-tag-report/v1','error':{'id':'xrt_input_schema','detail':'x'},'exit':2}}\n"
        "print(json.dumps(R[cid], sort_keys=True))\nsys.exit(R[cid]['exit'])\n")
    variants = {
        "good": good,
        "bad-findings": header + (
            "a=sys.argv.index('--manifest'); cid=sys.argv[a+1].split('/')[-1][:-5]\n"
            "print(json.dumps({'schema':'x-robots-tag-report/v1','checks':[],'findings':['xrt_extra'],'exit':0}))\n"
            "sys.exit(0)\n"),
        "bad-effective": header + (
            "a=sys.argv.index('--manifest'); cid=sys.argv[a+1].split('/')[-1][:-5]\n"
            "print(json.dumps({'schema':'x-robots-tag-report/v1','checks':[{'id':cid,'directives':['noindex'],'effective':[],'bots':{}}],'findings':[],'exit':0}))\n"
            "sys.exit(0)\n"),
        "bad-exit": header + (
            "a=sys.argv.index('--manifest'); cid=sys.argv[a+1].split('/')[-1][:-5]\n"
            "print(json.dumps({'schema':'x-robots-tag-report/v1','checks':[{'id':cid,'directives':['noindex'],'effective':['noindex'],'bots':{}}],'findings':[],'exit':0}))\n"
            "sys.exit(0)\n"),
        "unparseable": header + "print('not json')\nsys.exit(0)\n",
    }
    paths = {}
    for name, src in variants.items():
        p = tools_dir / f"{name}.py"
        p.write_text(src, encoding="utf-8")
        paths[name] = p

    good_res = run_cases(paths["good"], cases, expect, base / "w-good")
    checks.append(("good-decided", good_res["decided"] == 3, str(good_res)))
    checks.append(("good-correct", good_res["correct"] == 3 and good_res["wrong"] == 0, str(good_res)))
    for name, needle in [("bad-findings", "findings"), ("bad-effective", "effective"),
                         ("bad-exit", "exit")]:
        r = run_cases(paths[name], cases, expect, base / f"w-{name}")
        got = any(why.startswith(needle) for _, _, why in r["details"])
        checks.append((f"{name}-wrong", r["wrong"] >= 1 and got, str(r["details"])))
    r = run_cases(paths["unparseable"], cases, expect, base / "w-unparseable")
    checks.append(("unparseable-undecided", r["undecided"] == 3, str(r)))
    failed_bad = 0
    for cid, m in cases:
        r = run_cases(paths["bad-findings"], [(cid, m)], expect, base / "w-const-bad")
        if r["wrong"] or r["undecided"]:
            failed_bad += 1
    checks.append(("const-good-fails-none", good_res["wrong"] == 0 and good_res["undecided"] == 0,
                   str(good_res)))
    checks.append(("const-bad-fails-all", failed_bad == 3, str(failed_bad)))
    bad = [f"{n}: {d}" for n, ok, d in checks if not ok]
    for n, ok, _ in checks:
        print(f"  {'ok' if ok else 'FAIL'} {n}")
    return not bad, bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--tool")
    ap.add_argument("--tool-revision")
    ap.add_argument("--cases", default=str(HERE / "cases"))
    ap.add_argument("--expect", default=str(HERE / "expect" / "expect.json"))
    ap.add_argument("--consts", default=str(HERE / "consts"))
    ap.add_argument("--work")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--consts-only", action="store_true",
                    help="control mode: run the degenerate constants over the frozen cases only")
    a = ap.parse_args()
    if not (a.consts_only or a.selftest) and (a.tool is None) == (a.tool_revision is None):
        print("usage: exactly one of --tool / --tool-revision is required", file=sys.stderr)
        return 64
    work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="kake-c79-"))
    work.mkdir(parents=True, exist_ok=True)
    owned = a.work is None
    try:
        if a.selftest:
            ok, bad = selftest(work)
            print(f"selftest: {'PASS' if ok else 'FAIL'}")
            return 0 if ok else 1
        cases_path = Path(a.cases)
        consts_path = Path(a.consts)
        expect_doc = json.loads(Path(a.expect).read_text(encoding="utf-8"))
        if expect_doc.get("schema") != "xrt-expect/v1":
            print("unevaluable: expect file schema")
            print("exit=2")
            return 2
        expect = expect_doc["cases"]
        case_dirs = sorted(p for p in cases_path.iterdir() if p.is_dir())
        cases = [(p.name, p / "manifest.json") for p in case_dirs if (p / "manifest.json").exists()]
        if not cases or set(expect) != {c for c, _ in cases}:
            print("unevaluable: case set and oracle disagree")
            print("exit=2")
            return 2
        if a.consts_only:
            constants = sorted(consts_path.glob("*.py"))
            failed = 0
            for const in constants:
                r = run_cases(const, cases, expect, work / f"const-{const.stem}")
                hit = r["wrong"] > 0 or r["undecided"] > 0
                failed += 1 if hit else 0
                print(f"const {const.name} failures={r['wrong']} undecided={r['undecided']} "
                      f"total={len(cases)} {'failed' if hit else 'PASSED'}")
            ok = failed == len(constants) and len(constants) == 4
            print(f"ctl constants_failed={failed}/{len(constants)} cases={len(cases)}")
            print(f"exit={0 if ok else 1}")
            return 0 if ok else 1
        if a.tool_revision:
            p = subprocess.run(["git", "-C", a.root, "show", f"{a.tool_revision}:{TOOL_REL}"],
                               capture_output=True)
            if p.returncode != 0:
                print(f"TOOL_ABSENT rc={p.returncode} error={p.stderr.decode().strip()}")
                print("exit=2")
                return 2
            tool = work / "tool.py"
            tool.write_bytes(p.stdout)
            label = a.tool_revision
        else:
            tool = Path(a.tool).resolve()
            if not tool.exists():
                print(f"TOOL_ABSENT path={tool}")
                print("exit=2")
                return 2
            label = "worktree"
        tool_bytes = tool.read_bytes()
        res = run_cases(tool, cases, expect, work)
        constants = sorted(consts_path.glob("*.py"))
        failed = 0
        const_detail = []
        for const in constants:
            r = run_cases(const, cases, expect, work / f"const-{const.stem}")
            hit = r["wrong"] > 0 or r["undecided"] > 0
            failed += 1 if hit else 0
            const_detail.append(f"{const.name}:{'failed' if hit else 'PASSED'}")
        st_ok, _ = selftest(work)
        cases_sha = sha256("|".join(f"{cid}:{sha256((p).read_bytes())}" for cid, p in cases).encode())
        met = (res["decided"] == len(cases) and res["wrong"] == 0 and res["undecided"] == 0
               and failed == len(constants) and len(constants) == 4 and st_ok)
        code = 0 if met else 1
        if a.json:
            print(json.dumps({"schema": "kake-r79-c2-xrt-matrix-v1", "revision": label,
                              "tool_sha256": sha256(tool_bytes), "tool_bytes": len(tool_bytes),
                              "cases": len(cases), **{k: res[k] for k in
                                                      ("decided", "correct", "wrong", "undecided")},
                              "constants_failed": f"{failed}/{len(constants)}",
                              "constants": const_detail, "selftest_ok": st_ok,
                              "cases_sha256": cases_sha, "met": met, "exit": code}, indent=1))
        else:
            for cid, kind, why in res["details"]:
                print(f"  {kind.upper()} {cid} {why}")
            print(f"  constants: {' '.join(const_detail)}")
            print(f"C2v1 revision={label} tool_sha256={sha256(tool_bytes)} "
                  f"tool_bytes={len(tool_bytes)} cases={len(cases)} decided={res['decided']} "
                  f"correct={res['correct']} wrong={res['wrong']} undecided={res['undecided']} "
                  f"constants_failed={failed}/{len(constants)} "
                  f"selftest_ok={'true' if st_ok else 'false'} cases_sha256={cases_sha} "
                  f"met={'true' if met else 'false'}")
            print(f"exit={code}")
        return code
    finally:
        if owned:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
