#!/usr/bin/env python3
"""Hand-written shape validator for the round-37 C1 manifest.

Implements only the manifest/check faults of the C1 contract (bullet (f) and the
manifest part of bullet (g)); it never parses robots rules and never decides an
access result, so it is not a robots tool. With --evidence it additionally
asserts that each check's quoted justifying lines exist verbatim in the recorded
body at the stated line numbers.

usage: validate_manifest.py PATH [--evidence]
exit 0 shape ok, 1 faults found, 2 could not read
"""
import json
import os
import re
import sys

PRODUCT_TOKEN = re.compile(r"^[A-Za-z_-]+$")


def lines_of(path):
    data = open(path, "rb").read()
    if data.startswith(b"\xef\xbb\xbf"):
        data = data[3:]
    text = data.decode("utf-8", "replace")
    out, cur, i = [], [], 0
    while i < len(text):
        ch = text[i]
        if ch == "\r":
            out.append("".join(cur)); cur = []
            if i + 1 < len(text) and text[i + 1] == "\n":
                i += 1
        elif ch == "\n":
            out.append("".join(cur)); cur = []
        else:
            cur.append(ch)
        i += 1
    if cur:
        out.append("".join(cur))
    return out


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def status_ok(v):
    return is_int(v) and (200 <= v <= 299 or 400 <= v <= 499 or 500 <= v <= 599)


def url_ok(u):
    if not isinstance(u, str):
        return False
    m = re.match(r"^(https?)://([^/?#]+)", u)
    if not m:
        return False
    authority = m.group(2)
    host = authority.rsplit("@", 1)[-1]
    if host.startswith("["):
        host = host[: host.find("]") + 1] if "]" in host else ""
    else:
        host = host.split(":", 1)[0]
    return bool(host)


def check(manifest_path, with_evidence):
    faults = []
    try:
        raw = open(manifest_path, "rb").read()
    except OSError as exc:
        print(json.dumps({"manifest": manifest_path, "faults": [f"unreadable: {exc}"]}, indent=2))
        return 2
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(json.dumps({"manifest": manifest_path, "faults": [f"not UTF-8: {exc}"]}, indent=2))
        return 1
    try:
        doc = json.loads(text)
    except json.JSONDecodeError as exc:
        print(json.dumps({"manifest": manifest_path, "faults": [f"not JSON: {exc}"]}, indent=2))
        return 1
    if not isinstance(doc, dict):
        faults.append("manifest is not an object")
        print(json.dumps({"manifest": manifest_path, "faults": faults}, indent=2)); return 1
    if not (is_int(doc.get("version")) and doc.get("version") == 1):
        faults.append("version is not the integer 1")
    checks = doc.get("checks")
    if not isinstance(checks, list):
        faults.append("checks is not a list")
        print(json.dumps({"manifest": manifest_path, "faults": faults}, indent=2)); return 1

    base = os.path.realpath(os.path.dirname(os.path.abspath(manifest_path)))
    seen = set()
    stats = {"checks": len(checks), "allow": 0, "disallow": 0, "quotes": 0, "hosts": {}}
    for idx, chk in enumerate(checks):
        where = f"checks[{idx}]"
        if not isinstance(chk, dict):
            faults.append(f"{where}: not an object"); continue
        cid = chk.get("id")
        if not (isinstance(cid, str) and cid):
            faults.append(f"{where}: id missing or not a non-empty string"); cid = None
        elif cid in seen:
            faults.append(f"{where}: id {cid!r} repeated")
        else:
            seen.add(cid)
        if not status_ok(chk.get("robotsStatus")):
            faults.append(f"{where}: robotsStatus {chk.get('robotsStatus')!r} outside 200-299/400-499/500-599")
        ua = chk.get("userAgent")
        if not (isinstance(ua, str) and PRODUCT_TOKEN.match(ua)):
            faults.append(f"{where}: userAgent {ua!r} is not a product token")
        if not url_ok(chk.get("url")):
            faults.append(f"{where}: url {chk.get('url')!r} is not an absolute http(s) URL with a host")
        expect = chk.get("expect")
        if expect not in ("allow", "disallow"):
            faults.append(f"{where}: expect {expect!r} is not 'allow' or 'disallow'")
        else:
            stats[expect] += 1
        if status_ok(chk.get("robotsStatus")) and 200 <= chk["robotsStatus"] <= 299:
            rp = chk.get("robots")
            if not (isinstance(rp, str) and rp):
                faults.append(f"{where}: robots missing for a 2xx status")
            elif os.path.isabs(rp) or rp.startswith("\\"):
                faults.append(f"{where}: robots {rp!r} is absolute")
            else:
                target = os.path.realpath(os.path.join(base, rp))
                if not (target == base or target.startswith(base + os.sep)):
                    faults.append(f"{where}: robots {rp!r} escapes the manifest directory")
                elif not os.path.isfile(target):
                    faults.append(f"{where}: robots {rp!r} is not a regular file")
                else:
                    stats["hosts"][rp] = stats["hosts"].get(rp, 0) + 1
        if with_evidence:
            ev = chk.get("evidence")
            if not isinstance(ev, dict) or not isinstance(ev.get("quotes"), list) or not ev["quotes"]:
                faults.append(f"{where}: no quoted justifying line")
                continue
            rp = chk.get("robots")
            path = os.path.realpath(os.path.join(base, rp)) if isinstance(rp, str) else None
            if not path or not os.path.isfile(path):
                faults.append(f"{where}: evidence has no readable robots body"); continue
            body_lines = lines_of(path)
            for q in ev["quotes"]:
                ln, qt = q.get("line"), q.get("text")
                if not is_int(ln) or not isinstance(qt, str):
                    faults.append(f"{where}: malformed quote {q!r}"); continue
                if not (1 <= ln <= len(body_lines)):
                    faults.append(f"{where}: quote line {ln} outside {rp}")
                elif body_lines[ln - 1] != qt:
                    faults.append(f"{where}: quote does not match {rp}:{ln}")
                else:
                    stats["quotes"] += 1

    report = {"manifest": manifest_path, "version": doc.get("version"), "faults": faults, "stats": stats}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not faults else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: validate_manifest.py PATH [--evidence]", file=sys.stderr)
        sys.exit(2)
    sys.exit(check(sys.argv[1], "--evidence" in sys.argv[2:]))
