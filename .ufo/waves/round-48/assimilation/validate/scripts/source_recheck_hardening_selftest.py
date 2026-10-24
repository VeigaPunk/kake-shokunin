#!/usr/bin/env python3
"""Round-37 hardening self-test for the offline source re-check audit.

Companion to `scripts/source_recheck_selftest.py` (which this file does not edit).  Four carried
round-36 tool defects are pinned here, each with a fixture that is red on the round-36 tool
(`4d5b3d55:scripts/source_recheck.py`) and green on the hardened tool:

  g29  a FIFO manifest must not block forever: exit 2, one input_invalid (check null).
  g30  a 1 GiB manifest must not be read into memory: exit 2, one input_invalid.
  g31  a `/dev/zero` manifest must not be read into memory: exit 2, one input_invalid.
  g32  the body is opened at the resolved path that was validated, not at the unresolved one.

Round 38 adds the two carried read-cap defects (round-37 w2/SentinelHardening.md, defect 1):

  g33  a body larger than the stated 16 MiB cap is one check_invalid for that check, not a read
       into memory and not a truncated quote test: exit 2, one check_invalid, nothing evaluated.
  g34  a 1 GiB body must not be read into memory: exit 2, one check_invalid (base: MemoryError,
       exit 1, no JSON).
  g35  a manifest inside the 64 MiB cap (~60 MiB) whose parse cannot fit the address space is one
       input_invalid with a report, not a MemoryError with no stdout (base: exit 1, no JSON).

Round 39 pins one defect carried from round 38 (SCORECARD.md "Defects carried to round 39"):

  g36  an oversized body on a chain that starts with a permanent hop is one check_invalid, not
       `moved` plus `check_invalid`, and the check is not counted in checksEvaluated (base for
       the fixture: two findings for that check and checksEvaluated 2).

Two page-text fixtures pin the contract (c) amendment implemented with them:

  c-attributed-script         `<script` inside another tag's quoted attribute value opens nothing
  c-attributed-script-real    a genuine script element is still removed after such an attribute

The amendment sentence (round-37, contract (c)):

  "A raw-element start tag counts only where a tag can start, not inside another tag's attribute
   value."

Fixture shape is the shape of `scripts/source_recheck_selftest.py`: a fixture names its contract
sentence, a manifest (or raw bytes), inline body files, an expected exit code, verdict, finding
multiset (projected on (check, reason), plus target for `moved` only) and checksEvaluated; extra
`accept` alternatives are tolerated readings.  Extensions used only by this file: `fifos`,
`links`, `sparse`, `rlimit_as`, `timeout` and `open_expectation` (the paths the tool must and
must not open, read from an strace trace -- the only observable that separates a check-then-open
race from opening the validated path, because both reads return the same bytes when the
filesystem is still).

Usage:
    python3 scripts/source_recheck_hardening_selftest.py [--tool PATH]

Exit 0 only when every fixture passes.
"""

import argparse
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
DEFAULT_TOOL = HERE / "source_recheck.py"
MIN_FIXTURES = 6
TIMEOUT_SECONDS = 60
MEMORY_LIMIT = 512 * 1024 * 1024
# Round-38: the tool's stated body cap, and a manifest just under the 64 MiB cap whose flat
# array of small objects cannot fit MEMORY_LIMIT during json.loads (~7.9M dicts, >1 GiB).
BODY_CAP = 16 * 1024 * 1024
NEAR_CAP_MANIFEST = (
    b'{"version": 1, "checks": [], "junk": ['
    + b'{"a":1},' * ((60 * 1024 * 1024) // 8)
    + b'{"a":1}]}'
)
NON_REDIRECT_LOCATION = "/final"
URL = "https://example.test/page"
QUOTE = "VISIBLE"

HOPS = '[{"status": 200, "location": "/final"}]'
CONTRACT = {
    "g": (
        '(g) Input faults. "An unreadable or non-JSON manifest, a non-object, version other '
        'than 1, or checks not a list: one input_invalid finding with check null, nothing '
        'evaluated. A check that breaks any manifest rule above (including a body path that is '
        'absolute, escapes the manifest directory, or is missing or not a regular file): one '
        'check_invalid finding for it ... and no other finding for it."'
    ),
    "g-open": (
        '(g) "It reads only the manifest and the body files it names; no network, no writes." '
        'Round-37 hardening: the body is opened at the path that was validated (the resolved '
        'one), so no check-then-open race re-resolves a symlink.'
    ),
    "body-cap": (
        'Round-38 repair carried from round-37 (g) reads: "A body larger than the stated cap '
        '(16 MiB) is an input fault for that check: one check_invalid finding, nothing counted '
        'as evaluated." No body, however large, is read into memory or reported as a crash, and '
        'a manifest inside the 64 MiB cap whose JSON parse cannot fit the address space is an '
        'unreadable manifest: one input_invalid with check null.'
    ),
    "body-cap-moved": (
        '(g) "A check that breaks any manifest rule above ...: one check_invalid finding for it '
        '... and no other finding for it; the other checks are still evaluated and their '
        'findings reported. checksEvaluated counts the checks that are not check_invalid." '
        'Round-39: a body over the stated 16 MiB cap is that input fault even when the chain '
        'starts with a permanent hop, so the check gets no moved finding and is not counted.'
    ),
    "c": (
        '(c) HTML text. "the contents of script, style and template elements removed (start tag '
        'to the next end tag of the same name, ASCII case-insensitive)" -- with the round-37 '
        'amendment: "A raw-element start tag counts only where a tag can start, not inside '
        "another tag's attribute value.\""
    ),
}

FIXTURES = []


def add(name, contract, manifest=None, raw=None, argv=None, exit_code=0, verdict="clean",
        findings=(), evaluated=None, files=None, fifos=None, links=None, sparse=None,
        rlimit_as=None, timeout=None, open_expectation=None, accept=None):
    """Register one fixture (shape of scripts/source_recheck_selftest.py)."""
    files = dict(files or {})
    manifest = extract_body_files(manifest, files)
    FIXTURES.append({
        "name": name,
        "contract": contract,
        "manifest": manifest,
        "raw": raw,
        "argv": argv,
        "exit": exit_code,
        "verdict": verdict,
        "findings": list(findings),
        "evaluated": evaluated,
        "files": files,
        "fifos": list(fifos or ()),
        "links": dict(links or {}),
        "sparse": dict(sparse or {}),
        "rlimit_as": rlimit_as,
        "timeout": timeout or TIMEOUT_SECONDS,
        "open_expectation": open_expectation,
        "accept": list(accept or []),
    })


def extract_body_files(manifest, files):
    """Move inline body bytes out of the manifest into `files` (as the round-36 harness does)."""
    if not isinstance(manifest, dict):
        return manifest
    checks = manifest.get("checks")
    if not isinstance(checks, list):
        return manifest
    for check in checks:
        if not isinstance(check, dict):
            continue
        for key in [k for k in check if k.endswith(".html") and isinstance(check[k], bytes)]:
            files[key] = check.pop(key)
    return manifest


def alt(exit_code, verdict=None, findings=(), evaluated=None):
    return {"exit": exit_code, "verdict": verdict, "findings": list(findings),
            "evaluated": evaluated}


def chk(cid="k1", quote=QUOTE, hops=None, **extra):
    check = {
        "id": cid,
        "url": URL,
        "quote": quote,
        "hops": [{"status": 200}] if hops is None else hops,
    }
    check.update(extra)
    return check


def mf(checks):
    return {"version": 1, "checks": checks}


def f(check, reason, target=None):
    return {"check": check, "reason": reason, "target": target}


def page(body):
    return {"body.html": body}


def build_fixtures():
    invalid = ([f(None, "input_invalid")], 2, "could-not-evaluate")
    add("g29-fifo-manifest", CONTRACT["g"], argv=["--manifest", "{fifo}"],
        fifos=["manifest.fifo"], exit_code=invalid[1], verdict=invalid[2],
        findings=invalid[0], evaluated=0, timeout=10)
    add("g30-huge-manifest", CONTRACT["g"], argv=["--manifest", "{sparse:huge.json}"],
        sparse={"huge.json": 1024 * 1024 * 1024}, exit_code=invalid[1],
        verdict=invalid[2], findings=invalid[0], evaluated=0,
        rlimit_as=MEMORY_LIMIT, timeout=30)
    add("g31-device-manifest", CONTRACT["g"], argv=["--manifest", "/dev/zero"],
        exit_code=invalid[1], verdict=invalid[2], findings=invalid[0], evaluated=0,
        rlimit_as=MEMORY_LIMIT, timeout=30)

    add("c-attributed-script",
        CONTRACT["c"],
        manifest=mf([chk(quote="VISIBLE-TEXT", contentType="text/html",
                         body="body.html")]),
        files=page(b'<p title="see <script> note">VISIBLE-TEXT</p>'
                   b'<script>hidden();</script><p>TAIL</p>'),
        evaluated=1)
    add("c-attributed-script-real",
        CONTRACT["c"],
        manifest=mf([
            chk("k1", quote="LINK-TEXT", contentType="text/html", body="body.html"),
            chk("k2", quote="bad()", contentType="text/html", body="body.html"),
        ]),
        files=page(b'<a href="/x" data-label="a <script> b">LINK-TEXT</a>'
                   b'<script>bad()</script><p>AFTER</p>'),
        exit_code=1, verdict="failed-policy",
        findings=[f("k2", "quote_missing")], evaluated=2)

    add("g32-body-open-resolved", CONTRACT["g-open"],
        manifest=mf([chk(quote="HELLO", contentType="text/html", body="body.html")]),
        files={"real-body.html": b"<p>HELLO</p>"},
        links={"body.html": "real-body.html"},
        evaluated=1,
        open_expectation={"must_include": ["real-body.html"],
                          "must_exclude": ["body.html"]})

    # Round-38: carried read-cap defects. A body over the stated cap is one check_invalid for
    # that check; no body is read into memory; a near-cap manifest that cannot be parsed in the
    # address space is one input_invalid with a report.
    # Round-39 decides what this file left unpinned: contract (g) says checksEvaluated "counts
    # the checks that are not check_invalid", so an evaluate-time check_invalid (unreadable or
    # oversized body) is not counted; g33/g34 now pin 0 and g36 pins the moved finding.
    add("g33-body-over-cap", CONTRACT["body-cap"],
        manifest=mf([chk(quote=QUOTE, contentType="text/html", body="body.html")]),
        files={"body.html": b"<p>" + b"A" * (BODY_CAP + 1) + b"</p>"},
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0)
    add("g34-body-1g", CONTRACT["body-cap"],
        manifest=mf([chk(quote=QUOTE, contentType="text/html", body="body.bin")]),
        sparse={"body.bin": 1024 * 1024 * 1024},
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("k1", "check_invalid")], evaluated=0,
        rlimit_as=MEMORY_LIMIT, timeout=30)
    # Round-39: a body over the cap is an input fault for that check, so contract (g)'s "no
    # other finding for it" also drops the moved finding of a leading permanent run, and
    # checksEvaluated counts the other check only.
    add("g36-body-over-cap-with-moved", CONTRACT["body-cap-moved"],
        manifest=mf([
            chk("kbad", quote=QUOTE, contentType="text/html", body="big.html",
                hops=[{"status": 301, "location": "/final"},
                      {"status": 200, "location": NON_REDIRECT_LOCATION}]),
            chk("kgood", quote=QUOTE, contentType="text/html", body="small.html"),
        ]),
        files={"big.html": b"<p>" + b"A" * (BODY_CAP + 1) + b"</p>",
               "small.html": b"<p>VISIBLE</p>"},
        exit_code=2, verdict="could-not-evaluate",
        findings=[f("kbad", "check_invalid")], evaluated=1)
    add("g35-near-cap-manifest", CONTRACT["body-cap"], raw=NEAR_CAP_MANIFEST,
        exit_code=2, verdict="could-not-evaluate",
        findings=[f(None, "input_invalid")], evaluated=0,
        rlimit_as=MEMORY_LIMIT, timeout=60,
        accept=[alt(0, "clean", evaluated=0)])


build_fixtures()


def tool_environment():
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.setdefault("LC_ALL", "C.UTF-8")
    return env


def project(findings):
    """Project findings on (check, reason), plus target for `moved` only."""
    rows = []
    if not isinstance(findings, list):
        raise ValueError("findings is not a list")
    for item in findings:
        if not isinstance(item, dict):
            rows.append(("<non-object>",))
            continue
        reason = item.get("reason")
        check = item.get("check")
        if reason == "moved":
            rows.append((json.dumps(check), str(reason), json.dumps(item.get("target"))))
        else:
            rows.append((json.dumps(check), str(reason)))
    return sorted(rows)


def expected_projection(findings):
    rows = []
    for item in findings:
        if item["reason"] == "moved":
            rows.append((json.dumps(item["check"]), item["reason"], json.dumps(item["target"])))
        else:
            rows.append((json.dumps(item["check"]), item["reason"]))
    return sorted(rows)


def snapshot(root):
    return {str(path.relative_to(root)) for path in root.rglob("*")}


def materialize(fixture, work):
    case_dir = work / fixture["name"]
    case_dir.mkdir(parents=True, exist_ok=True)
    for rel, data in fixture["files"].items():
        target = (case_dir / rel).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for rel, size in fixture["sparse"].items():
        with open(case_dir / rel, "wb") as handle:
            handle.truncate(size)
    for rel, target in fixture["links"].items():
        link = case_dir / rel
        link.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(target, link)
    for rel in fixture["fifos"]:
        os.mkfifo(case_dir / rel)
    manifest_path = case_dir / "manifest.json"
    if fixture["raw"] is not None:
        manifest_path.write_bytes(fixture["raw"])
    elif fixture["manifest"] is not None:
        manifest_path.write_text(json.dumps(fixture["manifest"]), encoding="utf-8")
    return case_dir, manifest_path


def expand(item, case_dir):
    """Replace the path placeholders in one argv entry."""
    if not isinstance(item, str):
        return item
    if item == "{fifo}":
        return str(case_dir / "manifest.fifo")
    if item.startswith("{sparse:") and item.endswith("}"):
        return str(case_dir / item[len("{sparse:"):-1])
    if item == "{manifest}":
        return str(case_dir / "manifest.json")
    return str(item)


def limit_memory(limit):
    def apply():
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    return apply


def run_case(tool, fixture, work, trace_dir):
    problems = []
    case_dir, manifest_path = materialize(fixture, work)
    argv = fixture["argv"]
    if argv is None:
        argv = ["--manifest", str(manifest_path)]
    else:
        argv = [expand(item, case_dir) for item in argv]
    command = [sys.executable, "-B", str(tool)] + argv
    trace_path = None
    if fixture["open_expectation"] is not None:
        strace = shutil.which("strace")
        if strace is None:
            return ["strace is not available; the opened-path fixture cannot run"]
        trace_path = trace_dir / (fixture["name"] + ".trace")
        command = [strace, "-f", "-q", "-s", "4096", "-e", "trace=openat,open",
                   "-o", str(trace_path)] + command
    before = snapshot(case_dir)
    kwargs = {
        "cwd": str(case_dir),
        "capture_output": True,
        "text": True,
        "timeout": fixture["timeout"],
        "env": tool_environment(),
    }
    if fixture["rlimit_as"] is not None:
        kwargs["preexec_fn"] = limit_memory(fixture["rlimit_as"])
    try:
        proc = subprocess.run(command, **kwargs)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return ["tool could not run: %s" % exc]
    after = snapshot(case_dir)
    written = sorted(after - before)
    if written:
        problems.append("tool wrote files: %s" % ", ".join(written))

    accepted = [{
        "exit": fixture["exit"],
        "verdict": fixture["verdict"],
        "findings": fixture["findings"],
        "evaluated": fixture["evaluated"],
    }]
    accepted.extend(fixture["accept"])
    exit_codes = sorted({item["exit"] for item in accepted})
    if proc.returncode not in exit_codes:
        problems.append("exit mismatch: expected one of %r, observed %r (stderr: %s)"
                        % (exit_codes, proc.returncode, proc.stderr.strip()[:200]))
        return problems

    try:
        report = json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError) as exc:
        problems.append("stdout is not one JSON object: %s" % exc)
        return problems
    if not isinstance(report, dict):
        return problems + ["report is not an object"]
    if report.get("version") != 1:
        problems.append("version mismatch: expected 1, observed %r" % (report.get("version"),))
    mismatches = []
    for want in accepted:
        current = []
        if want["verdict"] is not None and report.get("verdict") != want["verdict"]:
            current.append("verdict: expected %r, observed %r"
                           % (want["verdict"], report.get("verdict")))
        wanted = expected_projection(want["findings"])
        got = project(report.get("findings"))
        if wanted != got:
            current.append("findings: expected %s, observed %s" % (wanted, got))
        if want["evaluated"] is not None and report.get("checksEvaluated") != want["evaluated"]:
            current.append("checksEvaluated: expected %r, observed %r"
                           % (want["evaluated"], report.get("checksEvaluated")))
        if not current:
            mismatches = []
            break
        if not mismatches:
            mismatches = current
    problems.extend(mismatches)

    if not problems and trace_path is not None:
        problems.extend(check_open_paths(trace_path, case_dir, fixture["open_expectation"]))
    return problems


def check_open_paths(trace_path, case_dir, expectation):
    """Assert which paths inside the case directory the tool opened."""
    prefix = str(case_dir) + os.sep
    opened = set()
    try:
        text = trace_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return ["cannot read strace trace: %s" % exc]
    for line in text.splitlines():
        if prefix not in line:
            continue
        start = line.find(prefix)
        rest = line[start + len(prefix):]
        name = rest.split('"')[0].split("\\")[0]
        opened.add(name)
    problems = []
    for name in expectation["must_include"]:
        if name not in opened:
            problems.append("tool did not open %r (opened: %s)" % (name, sorted(opened)))
    for name in expectation["must_exclude"]:
        if name in opened:
            problems.append("tool opened the unresolved path %r (opened: %s)"
                            % (name, sorted(opened)))
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="source re-check audit hardening self-test")
    parser.add_argument("--tool", default=str(DEFAULT_TOOL), help="tool under test")
    parser.add_argument("--list", action="store_true", help="list fixture names and exit")
    args = parser.parse_args(argv)

    if args.list:
        try:
            for fixture in FIXTURES:
                print("%s\t%s" % (fixture["name"], fixture["contract"][:40]))
        except BrokenPipeError:
            pass
        return 0

    tool = Path(args.tool).resolve()
    summary = {
        "selftest": "kake-r37-source-recheck-hardening-selftest",
        "tool": str(tool),
        "cases": len(FIXTURES),
        "passed": 0,
        "failed": 0,
        "passedOverTotal": "0/%d" % len(FIXTURES),
        "verdict": "clean",
        "failures": [],
    }
    if len(FIXTURES) < MIN_FIXTURES:
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None,
                                "reasons": ["only %d fixtures; expected at least %d"
                                            % (len(FIXTURES), MIN_FIXTURES)]}]
        print(json.dumps(summary, sort_keys=True))
        return 2
    if not tool.is_file():
        summary["verdict"] = "could-not-evaluate"
        summary["failed"] = 1
        summary["failures"] = [{"case": None, "reasons": ["tool not found: %s" % tool]}]
        print(json.dumps(summary, sort_keys=True))
        return 2

    work = Path(tempfile.mkdtemp(prefix="kake-r37-hardening-"))
    trace_dir = Path(tempfile.mkdtemp(prefix="kake-r37-hardening-traces-"))
    try:
        for fixture in FIXTURES:
            problems = run_case(tool, fixture, work, trace_dir)
            if problems:
                summary["failures"].append({
                    "case": fixture["name"],
                    "contract": fixture["contract"],
                    "reasons": problems,
                })
            else:
                summary["passed"] += 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(trace_dir, ignore_errors=True)

    summary["failed"] = summary["cases"] - summary["passed"]
    summary["passedOverTotal"] = "%d/%d" % (summary["passed"], summary["cases"])
    if summary["failed"]:
        summary["verdict"] = "failed"
    print(json.dumps(summary, sort_keys=True))
    if summary["failed"]:
        for item in summary["failures"]:
            print("FAIL %s" % item["case"], file=sys.stderr)
            for reason in item["reasons"]:
                print("  - %s" % reason, file=sys.stderr)
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
