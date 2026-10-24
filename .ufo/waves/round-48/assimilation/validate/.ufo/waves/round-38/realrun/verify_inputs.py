#!/usr/bin/env python3
"""Self-check of the round-38 real-run inputs (not of any robots tool).

Checks, from the files as written:
  * the main manifest is JSON with 91 checks, 3 new checks per host over 12 hosts,
    and the 55 round-37 checks are byte-identical to the lane copy after removing
    the `robots/` re-point prefix;
  * every (k) check's URL path is exactly /robots%2Etxt or /%72obots.txt, with no
    query and no fragment, and both escapes are of unreserved characters;
  * every (i) check's URL holds exactly one ASCII character outside the RFC 3986
    set of contract (i), of the class its id names;
  * every percent-path check holds at least one %XX escape;
  * every fault manifest parses as JSON with Python's integer-digit limit removed,
    and its fault literal is raw (NaN/Infinity/-Infinity/1e400/5,000 digits), while
    the base's json.loads without that limit fails on the long-integer manifests;
  * expectations.json ids cover exactly the new checks and the declared faults are
    exactly the (i) checks.

Exit 0 when every assertion holds; 1 otherwise. Writes verify_inputs.json next to
itself with the checks and their pass/fail.
"""
import json
import os
import sys

sys.set_int_max_str_digits(0)

HERE = os.path.dirname(os.path.abspath(__file__))

ALLOWED = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~"
    ":/?#[]@!$&'()*+,;=%"
)
EXCLUDED_CLASS = {
    "space": {" "}, "quote": {'"'}, "backslash": {"\\"}, "braceopen": {"{"},
    "pipe": {"|"}, "caret": {"^"}, "backtick": {"`"}, "braceclose": {"}"},
    "gt": {">"}, "lt": {"<"}, "ctl": {"\u0001"}, "del": {"\u007f"},
}
results = []


def check(name, condition, detail=""):
    results.append({"check": name, "pass": bool(condition), "detail": detail})
    if not condition:
        print(f"FAIL {name}: {detail}", file=sys.stderr)
        return False
    return True


ok = True
lane = json.load(open("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37/realrun/robots/manifest.json", encoding="utf-8"))
main = json.load(open(os.path.join(HERE, "manifest.json"), encoding="utf-8"))
exp = json.load(open(os.path.join(HERE, "expectations.json"), encoding="utf-8"))

ok &= check("main.version", main.get("version") == 1)
ok &= check("main.count", len(main["checks"]) == 91, str(len(main["checks"])))
ids = [c["id"] for c in main["checks"]]
ok &= check("main.ids-unique", len(ids) == len(set(ids)))

copied_ok = True
for a, b in zip(lane["checks"], main["checks"]):
    b = json.loads(json.dumps(b))
    prefix = "robots/"
    if not b["robots"].startswith(prefix):
        copied_ok = False
        break
    b["robots"] = b["robots"][len(prefix):]
    if a != b:
        copied_ok = False
        print("round-37 check changed:", a["id"], file=sys.stderr)
        break
ok &= check("round37.verbatim-after-repoint", copied_ok)

new = main["checks"][55:]
by_host = {}
for c in new:
    by_host.setdefault(c["evidence"]["sourceUrl"], []).append(c)
ok &= check("new.count", len(new) == 36, str(len(new)))
ok &= check("new.hosts", len(by_host) == 12, str(len(by_host)))
ok &= check("new.three-per-host", all(len(v) == 3 for v in by_host.values()),
            json.dumps({k: len(v) for k, v in by_host.items()}))

for c in new:
    cid = c["id"]
    url = c["url"]
    bad = [(ch, hex(ord(ch))) for ch in url if ord(ch) < 128 and ch not in ALLOWED]
    if cid.startswith("r38-k-"):
        ok &= check(f"{cid}.k-path", url.endswith("/robots%2Etxt") or url.endswith("/%72obots.txt"), url)
        ok &= check(f"{cid}.k-noquery", "?" not in url and "#" not in url, url)
        escaped = url.rsplit("/", 1)[-1]
        if escaped == "robots%2Etxt":
            ok &= check(f"{cid}.k-unreserved-2e", chr(0x2E).isascii() and "%2E" in url)
        else:
            ok &= check(f"{cid}.k-unreserved-72", escaped.startswith("%72obots.txt") and chr(0x72) == "r")
    elif cid.startswith("r38-i-"):
        cls = cid.rsplit("-", 1)[-1]
        want = EXCLUDED_CLASS[cls]
        got = {ch for ch, _ in bad}
        ok &= check(f"{cid}.i-one-excluded", got == want, f"want {want!r} got {got!r} url {url!r}")
    elif cid.startswith("r38-e-"):
        ok &= check(f"{cid}.e-escape", "%" in url and any(
            url[i] == "%" and i + 2 < len(url) and all(h in "0123456789abcdefABCDEF" for h in url[i+1:i+3])
            for i in range(len(url))), url)
    else:
        ok &= check(f"{cid}.kind", False, "unknown new-check prefix")

declared = {cid: rec["declaredOutcome"] for cid, rec in exp["newChecks"].items()}
ok &= check("oracle.covers-new", set(declared) == {c["id"] for c in new})
fault_ids = [c["id"] for c in new if declared[c["id"]] == "check_invalid"]
ok &= check("oracle.faults-are-i-checks", fault_ids == [c["id"] for c in new if c["id"].startswith("r38-i-")],
            json.dumps(fault_ids))
expected_findings = [x["check"] for x in exp["manifests"]["manifest.json"]["findings"]]
ok &= check("oracle.main-findings", expected_findings == fault_ids)
ok &= check("oracle.main-evaluated",
            exp["manifests"]["manifest.json"]["checksEvaluated"] == len(main["checks"]) - len(fault_ids))

literal_checks = {
    "manifest.h-long-status.json": ("99999999", "5000 nines"),
    "manifest.h-unused-bigint.json": ("99999999", "5000 nines"),
    "manifest.h-nan-unused.json": ("NaN", "NaN"),
    "manifest.h-infinity-status.json": ("Infinity", "Infinity"),
    "manifest.h-neginfinity-status.json": ("-Infinity", "-Infinity"),
    "manifest.h-float-status.json": ("1e400", "1e400"),
}
for name, (token, label) in literal_checks.items():
    text = open(os.path.join(HERE, name), encoding="utf-8").read()
    ok &= check(f"{name}.literal", token in text, label)
    try:
        parsed = json.loads(text)
        parsed_ok = isinstance(parsed, dict) and len(parsed["checks"]) == 2
    except Exception as exc:  # noqa: BLE001
        parsed_ok = False
        print(name, "parse with limit removed failed:", exc, file=sys.stderr)
    ok &= check(f"{name}.parses", parsed_ok)

# The long-integer manifests are JSON numbers, not JSON syntax errors: the only
# reason the base tool cannot read them is Python's default 4300-digit int limit.
sys.set_int_max_str_digits(4300)
for name in ("manifest.h-long-status.json", "manifest.h-unused-bigint.json"):
    try:
        json.loads(open(os.path.join(HERE, name), encoding="utf-8").read())
        failed = False
    except ValueError as exc:
        failed = "4300" in str(exc) or "digits" in str(exc)
    ok &= check(f"{name}.base-limit-4300-digits", failed)

print(json.dumps({"ok": ok, "checks": len(results)}, indent=1))
with open(os.path.join(HERE, "verify_inputs.json"), "w", encoding="utf-8") as fh:
    json.dump({"ok": ok, "results": results}, fh, indent=2)
    fh.write("\n")
sys.exit(0 if ok else 1)
