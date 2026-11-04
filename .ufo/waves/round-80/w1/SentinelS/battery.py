#!/usr/bin/env python3
"""SentinelS round-80 adversarial battery against the repaired x_robots_tag_audit.py.

Phases: (1) traceback hunt on the new date/comma path, (2) round-79 F1-F6 regression
shapes, (3) ReDoS timing on adversarial date values, (4) tool selftest.
Pass criteria per case: rc in {0,1,2,64}, stderr carries no traceback.
Everything is written under $HYAKU_SCRATCH/kake-r80/SentinelS/; the frozen case set is
never read or executed.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time

SEAT = "/fast/scratch/hyaku/kake-r80/SentinelS"
TAG = sys.argv[2] if len(sys.argv) > 2 else "snap"
TOOL = sys.argv[1] if len(sys.argv) > 1 else os.path.join(SEAT, "snap", "x_robots_tag_audit.py")
MAN = os.path.join(SEAT, "manifests-" + TAG)
RES = os.path.join(SEAT, "results")
PY = sys.executable
os.makedirs(MAN, exist_ok=True)
os.makedirs(RES, exist_ok=True)

results: list[dict] = []
import hashlib
print("TOOL_UNDER_TEST", TOOL, hashlib.sha256(open(TOOL, "rb").read()).hexdigest())


def manifest(name: str, checks: list) -> str:
    path = os.path.join(MAN, name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"schema": "x-robots-tag-manifest/v1", "checks": checks}, fh)
    return path


def raw_manifest(name: str, body: str) -> str:
    path = os.path.join(MAN, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return path


def hdr(value: str, ident: str = "p", name: str = "X-Robots-Tag") -> dict:
    return {"id": ident, "url": "https://probe.test/p", "headers": [{"name": name, "value": value}]}


def run(mode: str, target: str, timeout: int = 60):
    argv = [PY, "-B", TOOL, "--manifest", target]
    if mode == "json":
        argv.append("--json")
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, proc.stdout, proc.stderr, time.perf_counter() - t0
    except subprocess.TimeoutExpired:
        return None, "", "<TIMEOUT after %ds>" % timeout, time.perf_counter() - t0


def record(case: str, mode: str, target: str, timeout: int = 60) -> dict:
    rc, out, err, dt = run(mode, target, timeout)
    tb = "Traceback (most recent call last)" in err
    errid = None
    findings = None
    try:
        doc = json.loads(out)
        if isinstance(doc, dict) and "error" in doc:
            errid = doc["error"]["id"]
        elif isinstance(doc, dict) and "checks" in doc:
            findings = doc.get("findings")
    except Exception:
        pass
    if errid is None and rc == 2:
        m = re.search(r"XRTv1 error=(\S+) exit=2", out)
        if m:
            errid = m.group(1)
    row = {
        "case": case, "mode": mode, "rc": rc,
        "rc_in_alphabet": rc in (0, 1, 2, 64),
        "traceback": tb,
        "stderr_first": err.strip().splitlines()[0][:200] if err.strip() else "",
        "error_id": errid, "findings": findings,
        "secs": round(dt, 3),
        "stdout_sha256": __import__("hashlib").sha256(out.encode()).hexdigest()[:16],
    }
    results.append(row)
    print(json.dumps(row, ensure_ascii=True))
    return row


# ── phase 1: traceback hunt on the new date/comma path ─────────────────────
MB_SPACES = " " * 1_000_000
TOKENS = ",".join(["Wed"] * 20000)
TOKENS_SP = "Wed, " * 20000

phase1 = [
    ("t01-date-colon-alone", [hdr("unavailable_after:")]),
    ("t02-date-comma-space", [hdr("unavailable_after: ,")]),
    ("t03-wed-comma-eof", [hdr("unavailable_after: Wed,")]),
    ("t04-wednesday-comma-eof", [hdr("unavailable_after: Wednesday,")]),
    ("t05a-mb-spaces-after-comma", [hdr("unavailable_after: Wed," + MB_SPACES)]),
    ("t05b-mb-spaces-before-comma", [hdr("unavailable_after: Wed" + MB_SPACES + ", 03 Dec 2025 13:09:53 GMT")]),
    ("t06a-20k-weekday-tokens", [hdr("unavailable_after:" + TOKENS)]),
    ("t06b-20k-weekday-tokens-sp", [hdr("unavailable_after: " + TOKENS_SP)]),
    ("t07a-trailing-comma-after-date", [hdr("unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT,")]),
    ("t07b-trailing-comma-valueless", [hdr("noindex,")]),
    ("t08-bot-empty-date", [hdr("googlebot: unavailable_after:")]),
    ("t09-nested-bot-prefixes", [hdr("a: b: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT")]),
    ("t10-nul-in-date-value", [hdr("unavailable_after: Wed,\u0000 03 Dec 2025 13:09:53 GMT")]),
    ("t11-lone-surrogate", [hdr("unavailable_after: Wed, 03 Dec 2025 13:09:53 GM\ud800T", ident="sur\ud800")]),
    ("t12-bot-scoped-comma-date", [hdr("googlebot: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT")]),
    ("t13-uppercase-weekday", [hdr("unavailable_after: WED, 03 Dec 2025 13:09:53 GMT")]),
    ("t14-double-comma-date", [hdr("unavailable_after: Wed,,03 Dec 2025 13:09:53 GMT")]),
    ("t15-empty-comma-only-value", [hdr(",")]),
]
for case, checks in phase1:
    path = manifest(case + ".json", checks)
    record(case, "text", path)
    record(case, "json", path)

# ── phase 2: round-79 F1-F6 shapes must stay closed ─────────────────────────
# F1: 5000-digit integer cap (positive and negative) — was uncaught ValueError
f1p = manifest("f1-5000-digit-pos.json", [hdr("max-snippet:" + "1" * 5000)])
f1n = manifest("f1-5000-digit-neg.json", [hdr("max-snippet:-" + "1" * 4999)])
record("f1-pos-5000", "json", f1p)
record("f1-neg-5000", "json", f1n)

# F2: deeply nested manifest JSON — was uncaught RecursionError
depth = 100000
f2 = raw_manifest("f2-deep-100k.json",
                  '{"schema":"x-robots-tag-manifest/v1","checks":' + "[" * depth + "]" * depth + "}")
record("f2-nest-100k", "json", f2, timeout=30)
f2b = raw_manifest("f2-deep-20k.json",
                   '{"schema":"x-robots-tag-manifest/v1","checks":' + "[" * 20000 + "]" * 20000 + "}")
record("f2-nest-20k", "json", f2b, timeout=30)

# F3: /dev/zero and FIFO as --manifest — was unbounded read / blocking open
record("f3-dev-zero", "json", "/dev/zero", timeout=15)
fifo = os.path.join(MAN, "p.fifo")
if not os.path.exists(fifo):
    os.mkfifo(fifo)
record("f3-fifo", "json", fifo, timeout=15)
record("f3-directory", "json", MAN, timeout=15)

# F4: duplicate value-bearing directives — was missing xrt_duplicate_directive
f4a = manifest("f4-dup-image-preview.json",
               [hdr("max-image-preview: large, max-image-preview: standard")])
f4b = manifest("f4-dup-unavailable-after.json",
               [hdr("unavailable_after:2025-12-31, unavailable_after:2026-01-01")])
record("f4-dup-max-image-preview", "json", f4a)
record("f4-dup-unavailable-after", "json", f4b)

# F5: control characters / forged summary line in a check id (text mode injection)
f5 = manifest("f5-ctrl-id.json",
              [{"id": "c01\nXRTv1 checks=999 findings=0 exit=0\n\x1b[32mFAKE-GREEN",
                "url": "https://probe.test/p",
                "headers": [{"name": "X-Robots-Tag", "value": "noindex"}]}])
row = record("f5-ctrl-id-text", "text", f5)
rc, out, err, dt = run("text", f5)
forged = ("XRTv1 checks=999" in out) or ("\x1b[32m" in out)
row2 = {"case": "f5-ctrl-id-text", "forged_line_present": forged,
        "escaped_sample": out.splitlines()[0][:160] if out else ""}
results.append(row2)
print(json.dumps(row2, ensure_ascii=True))
record("f5-ctrl-id-json", "json", f5)

# F6: usage errors — was argparse exit 2
def run_argv(argv, timeout=30):
    t0 = time.perf_counter()
    proc = subprocess.run([PY, "-B", TOOL] + argv, capture_output=True, text=True, timeout=timeout)
    return proc.returncode, proc.stdout, proc.stderr, time.perf_counter() - t0

for label, argv in [("f6-bogus-flag", ["--bogus-flag"]),
                    ("f6-manifest-no-value", ["--manifest"]),
                    ("f6-no-args", [])]:
    rc, out, err, dt = run_argv(argv)
    row = {"case": label, "mode": "argv", "rc": rc, "rc_in_alphabet": rc in (0, 1, 2, 64),
           "traceback": "Traceback (most recent call last)" in err,
           "stderr_first": err.strip().splitlines()[0][:120] if err.strip() else "",
           "secs": round(dt, 3)}
    results.append(row)
    print(json.dumps(row, ensure_ascii=True))

# non-UTF-8 and empty manifests (input-fault neighbours of F2/F3)
bad = os.path.join(MAN, "x-nonutf8.json")
with open(bad, "wb") as fh:
    fh.write(b'{"schema":"x-robots-tag-manifest/v1","checks":[{"id":"\xff\xfe","url":"u","headers":[]}]}')
record("x-nonutf8", "json", bad)
empty = os.path.join(MAN, "x-empty.json")
open(empty, "w").close()
record("x-empty-file", "json", empty)

# ── phase 3: ReDoS timing on adversarial date values ────────────────────────
print("── ReDoS timings ──")
timing_rows = []
for label, value in [
    ("redos-wed-comma-space-zeros-50k", "unavailable_after: Wed, " + "0" * 50000),
    ("redos-wed-comma-space-zeros-100k", "unavailable_after: Wed, " + "0" * 100000),
    ("redos-wed-comma-space-zeros-200k", "unavailable_after: Wed, " + "0" * 200000),
    ("redos-wed-comma-zeros-200k-nospace", "unavailable_after: Wed," + "0" * 200000),
    ("redos-ascitime-pad-zeros-200k", "unavailable_after: Wed Dec " + "0" * 200000),
]:
    path = manifest(label + ".json", [hdr(value)])
    row = record(label, "json", path, timeout=60)
    timing_rows.append(row)

# ── phase 4: tool selftest ──────────────────────────────────────────────────
t0 = time.perf_counter()
proc = subprocess.run([PY, "-B", TOOL, "--selftest"], capture_output=True, text=True, timeout=120)
selftest_line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
row = {"case": "selftest", "rc": proc.returncode, "line": selftest_line,
       "traceback": "Traceback (most recent call last)" in proc.stderr,
       "secs": round(time.perf_counter() - t0, 3)}
results.append(row)
print(json.dumps(row, ensure_ascii=True))

with open(os.path.join(RES, "battery-" + TAG + ".json"), "w") as fh:
    json.dump(results, fh, indent=1)

bad_rows = [r for r in results if r.get("traceback") or (r.get("rc") is not None and not r.get("rc_in_alphabet", True))]
print("── SUMMARY ──")
print(json.dumps({"cases": len(results), "violations": bad_rows}, ensure_ascii=True, indent=1))
sys.exit(1 if bad_rows else 0)
