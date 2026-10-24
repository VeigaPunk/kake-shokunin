#!/usr/bin/env python3
"""L1 private reference for kake round-37 C1 (offline robots.txt expectation audit).

Written from the public C1 contract only. ABLATE (env KAKE_ABLATE, comma list) switches off one
rule at a time; each ablation name is listed in ABLATIONS with the bullet it belongs to.
"""
from __future__ import annotations

import json
import os
import re
import stat
import sys
from urllib.parse import urlsplit

ABL = {"b_other"}
LIMIT = 512000
MAX_MANIFEST = 64 * 1024 * 1024
UNRESERVED = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")
HEX = set("0123456789abcdefABCDEF")
UA_RE = re.compile(r"[A-Za-z_-]+")


def parse(data: bytes):
    if "b_limit" not in ABL:
        data = data[:LIMIT]
    if data.startswith(b"\xef\xbb\xbf") and "b_bom" not in ABL:
        data = data[3:]
    text = data.decode("utf-8", "replace")
    if "b_cr" in ABL:
        lines = text.split("\n")
    else:
        lines = re.split(r"\r\n|\r|\n", text)
    groups = []
    cur = None
    last_ua = False
    for line in lines:
        if "b_comment" not in ABL:
            i = line.find("#")
            if i >= 0:
                line = line[:i]
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip(" \t")
        if "b_keycase" not in ABL:
            key = key.lower()
        value = value.strip(" \t")
        if key == "user-agent":
            if cur is None or not last_ua or "c_consecutive" in ABL:
                cur = {"agents": [], "rules": []}
                groups.append(cur)
            cur["agents"].append(value)
            last_ua = True
        elif key in ("allow", "disallow"):
            if cur is None:
                if "b_orphan" in ABL:
                    cur = {"agents": ["*"], "rules": []}
                    groups.append(cur)
                else:
                    continue
            cur["rules"].append((key, value))
            last_ua = False
        else:
            if "b_other" in ABL:
                last_ua = False
                cur = None
            continue
    return groups


def select(groups, ua):
    if "c_uacase" in ABL:
        matched = [g for g in groups if ua in g["agents"]]
    else:
        u = ua.lower()
        matched = [g for g in groups if any(a.lower() == u for a in g["agents"])]
    if "c_merge" in ABL and matched:
        matched = matched[:1]
    if not matched and "c_star" not in ABL:
        matched = [g for g in groups if "*" in g["agents"]]
        if "c_merge" in ABL and matched:
            matched = matched[:1]
    rules = []
    for g in matched:
        rules.extend(g["rules"])
    return rules


def normalize(s: str) -> str:
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "%" and i + 2 < len(s) and s[i + 1] in HEX and s[i + 2] in HEX:
            b = int(s[i + 1:i + 3], 16)
            if chr(b) in UNRESERVED and "e_unreserved" not in ABL:
                out.append(chr(b))
            elif "e_hexcase" in ABL:
                out.append(s[i:i + 3])
            else:
                out.append("%" + s[i + 1:i + 3].upper())
            i += 3
            continue
        if ord(ch) > 127 and "e_nonascii" not in ABL:
            out.append("".join("%%%02X" % b for b in ch.encode("utf-8")))
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def matches(pat: str, path: str) -> bool:
    anchored = pat.endswith("$") and "d_dollar" not in ABL
    body = pat[:-1] if anchored else pat
    if "d_star" in ABL:
        rx = re.escape(body)
    else:
        rx = ".*".join(re.escape(p) for p in body.split("*"))
    return re.match(rx + ("\\Z" if anchored else ""), path, re.S) is not None


def path_to_match(url: str) -> str:
    p = urlsplit(url)
    path = p.path
    if not path and "f_emptypath" not in ABL:
        path = "/"
    if p.query and "f_query" not in ABL:
        path += "?" + p.query
    if "f_fragment" in ABL and p.fragment:
        path += "#" + p.fragment
    return path


def decide(rules, path: str) -> bool:
    npath = normalize(path)
    if npath == "/robots.txt" and "f_robots" not in ABL:
        return True
    best = None
    for kind, pat in rules:
        if pat == "" and "d_empty" not in ABL:
            continue
        npat = normalize(pat)
        if not matches(npat, npath):
            continue
        length = len(npat)
        if "d_longest" in ABL:
            if best is None:
                best = (length, kind)
            continue
        if "d_tie" in ABL:
            if best is None or length > best[0] or (length == best[0] and kind == "disallow"):
                best = (length, kind)
        elif best is None or length > best[0] or (length == best[0] and kind == "allow"):
            best = (length, kind)
    return best is None or best[1] == "allow"


def emit(verdict, evaluated, findings):
    print(json.dumps({"version": 1, "verdict": verdict, "checksEvaluated": evaluated, "findings": findings}))
    return {"clean": 0, "failed-policy": 1, "could-not-evaluate": 2}[verdict]


def main(argv):
    if len(argv) != 2 or argv[0] != "--manifest":
        print("usage: robots_audit.py --manifest PATH", file=sys.stderr)
        return 64
    mpath = argv[1]
    try:
        st = os.stat(mpath)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_MANIFEST:
            raise ValueError
        with open(mpath, "rb") as fh:
            m = json.loads(fh.read().decode("utf-8"))
    except (OSError, ValueError, RecursionError):
        return emit("could-not-evaluate", 0, [{"check": None, "reason": "input_invalid"}])
    if (not isinstance(m, dict) or not (type(m.get("version")) is int and m.get("version") == 1 or "g_version" in ABL)
            or not (isinstance(m.get("checks"), list) or "g_checklist" in ABL)):
        return emit("could-not-evaluate", 0, [{"check": None, "reason": "input_invalid"}])
    base = os.path.realpath(os.path.dirname(os.path.abspath(mpath)))
    findings = []
    evaluated = 0
    seen = set()
    for c in (m["checks"] if isinstance(m["checks"], list) else []):
        cid = c.get("id") if isinstance(c, dict) and isinstance(c.get("id"), str) and c.get("id") else None
        bad = cid is None
        if cid is not None:
            if cid in seen and "f_dup" not in ABL:
                bad = True
            seen.add(cid)
        rules = None
        if not bad:
            status = c.get("robotsStatus")
            ua = c.get("userAgent")
            url = c.get("url")
            expect = c.get("expect")
            if type(status) is not int or not (200 <= status <= 599) or (300 <= status <= 399 and "f_3xx" not in ABL):
                bad = True
            elif not isinstance(ua, str) or not (UA_RE.fullmatch(ua) or ("f_ua" in ABL and ua)):
                bad = True
            elif expect not in ("allow", "disallow") and not ("f_expect" in ABL and isinstance(expect, str)):
                bad = True
            elif not isinstance(url, str):
                bad = True
            else:
                try:
                    p = urlsplit(url)
                    if (p.scheme not in ("http", "https") and "f_scheme" not in ABL) or not p.hostname:
                        bad = True
                except ValueError:
                    bad = True
        if (not bad and 200 <= status <= 299) or (not bad and "a_4xx" in ABL and 400 <= status <= 499) \
                or (not bad and "a_5xx" in ABL and 500 <= status <= 599):
            rel = c.get("robots")
            if not isinstance(rel, str) or not rel or os.path.isabs(rel):
                bad = True
            else:
                full = os.path.join(base, rel)
                real = os.path.realpath(full)
                if ("f_escape" not in ABL and not real.startswith(base + os.sep)) or not os.path.isfile(real):
                    bad = True
                else:
                    try:
                        with open(real, "rb") as fh:
                            data = fh.read(LIMIT if "b_limit" not in ABL else -1)
                        rules = select(parse(data), ua)
                    except OSError:
                        bad = True
        if bad:
            findings.append({"check": cid, "reason": "check_invalid"})
            continue
        evaluated += 1
        path = path_to_match(url)
        if 200 <= status <= 299 or rules is not None:
            allowed = decide(rules, path)
        elif 400 <= status <= 499:
            allowed = True
        else:
            allowed = False
        if "a_2xx" in ABL and status != 200 and 200 <= status <= 299:
            allowed = True
        if expect not in ("allow", "disallow"):
            expect = "allow"
        if expect == "allow" and not allowed:
            findings.append({"check": cid, "reason": "blocked"})
        elif expect == "disallow" and allowed:
            findings.append({"check": cid, "reason": "exposed"})
    if any(f["reason"] in ("input_invalid", "check_invalid") for f in findings):
        v = "could-not-evaluate"
    elif findings:
        v = "failed-policy"
    else:
        v = "clean"
    return emit(v, evaluated, findings)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
