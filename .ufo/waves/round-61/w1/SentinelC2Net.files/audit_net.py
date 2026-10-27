#!/usr/bin/env python3
"""SentinelC2Net: static network-surface audit of response_snapshot.py + receipt validation."""
from __future__ import annotations
import ast, hashlib, json, os, re, sys

TOOL = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/response_snapshot.py"
CAP = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/capture"
POP = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-23/live"
REQUIRED = ["finalUrl", "headers", "sha256", "bytes", "fetchedAt", "userAgent"]

def static(path):
    src = open(path, encoding="utf-8").read()
    out = {}
    tree = ast.parse(src)
    consts = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try: consts[node.targets[0].id] = ast.literal_eval(node.value)
            except Exception: pass
    out["consts"] = {k: v for k, v in consts.items() if isinstance(v, (int, str, float, bool))}
    # method literals
    methods = set(re.findall(r'method\s*=\s*["\']([A-Z]+)["\']', src))
    out["http_method_literals"] = sorted(methods)
    out["has_post_literal"] = bool(re.search(r'["\'](POST|PUT|PATCH|DELETE)["\']', src))
    out["data_kwarg"] = bool(re.search(r'\bdata\s*=', src))
    out["cookie_tokens"] = sorted(set(re.findall(r'(?i)cookie[a-z_-]*', src)))
    out["cookiejar_import"] = "cookiejar" in src
    out["auth_tokens"] = sorted(set(re.findall(r'(?i)\b(authorization|bearer|token|password|secret|api[_-]?key)\b', src)))
    out["user_agent_round61"] = bool(re.search(r'round61', src, re.I))
    out["write_calls"] = sorted(set(re.findall(r'\b(os\.open|os\.mkdir|os\.makedirs|open\()', src)))
    out["fd_relative_writes"] = bool(re.search(r'dir_fd\s*=', src))
    out["no_follow"] = "O_NOFOLLOW" in src
    out["tmpdir"] = bool(re.search(r'TMPDIR|tempfile|mkdtemp', src))
    out["offswitch"] = sorted(set(re.findall(r'add_argument\(\s*"(--[a-z-]+)"', src)))
    out["env_reads"] = sorted(set(re.findall(r'environ(?:\.get)?\(?\s*\[?"([A-Z_]+)"|environ\.get\(\s*"([A-Z_]+)"', src)))
    out["method_assignments"] = sorted(set(re.findall(r'method\s*=\s*([A-Za-z_"\']+)', src)))
    out["lines"] = len(src.splitlines())
    out["sha"] = hashlib.sha256(src.encode()).hexdigest()
    return out

def receipts(cap):
    res = {"dirs": [], "ok": 0, "bad": 0, "rows": [], "secret_hits": [], "body_files": []}
    if not os.path.isdir(cap):
        res["missing"] = cap
        return res
    for name in sorted(os.listdir(cap)):
        d = os.path.join(cap, name)
        if not os.path.isdir(d):
            continue
        res["dirs"].append(name)
        row = {"id": name, "file": "response.json", "parse": "MISSING", "keys": "-", "status": None,
               "finalUrl": None, "hdr_n": None, "bytes": None, "sha": "-", "ua": None, "fetchedAt": None}
        p = os.path.join(d, "response.json")
        if not os.path.exists(p):
            res["bad"] += 1; res["rows"].append(row); continue
        try:
            v = json.load(open(p, encoding="utf-8"))
            row["parse"] = "ok"
        except Exception as e:
            row["parse"] = f"INVALID: {type(e).__name__}"; res["bad"] += 1; res["rows"].append(row); continue
        if not isinstance(v, dict):
            row["parse"] = "NOT-OBJECT"; res["bad"] += 1; res["rows"].append(row); continue
        missing = [k for k in REQUIRED if k not in v]
        row["keys"] = "all" if not missing else "miss:" + ",".join(missing)
        st = v.get("status")
        row["status"] = st
        row["finalUrl"] = v.get("finalUrl")
        h = v.get("headers")
        row["hdr_n"] = len(h) if isinstance(h, list) else (type(h).__name__ if h is not None else None)
        row["bytes"] = v.get("bytes")
        row["sha"] = (str(v.get("sha256"))[:12] + "…") if v.get("sha256") else None
        row["ua"] = v.get("userAgent")
        row["fetchedAt"] = v.get("fetchedAt")
        # header structure: list of {"name","value"} or pairs
        hdr_ok = isinstance(h, list) and all(
            (isinstance(x, dict) and "name" in x and "value" in x) or (isinstance(x, (list, tuple)) and len(x) == 2)
            for x in h)
        row["hdr_shape"] = "ok" if hdr_ok else "BAD"
        if isinstance(h, list):
            names = [((x.get("name") if isinstance(x, dict) else x[0]) or "") for x in h if hdr_ok]
            for i, nm in enumerate(names):
                low = str(nm).lower()
                if low in ("set-cookie", "cookie", "authorization", "proxy-authorization"):
                    val = (h[i].get("value") if isinstance(h[i], dict) else h[i][1])
                    res["secret_hits"].append({"id": name, "header": nm, "len": len(str(val))})
        body = os.path.join(d, "body.bin")
        alt = [f for f in ("body.bin", "body", "page.html", "body.txt") if os.path.exists(os.path.join(d, f))]
        if alt:
            bp = os.path.join(d, alt[0])
            b = open(bp, "rb").read()
            good = (len(b) == v.get("bytes") and hashlib.sha256(b).hexdigest() == v.get("sha256"))
            row["body"] = f"{alt[0]}:{'MATCH' if good else 'MISMATCH'}"
            res["body_files"].append({"id": name, "file": alt[0], "match": good})
        else:
            row["body"] = "no-body-file"
        ok = (row["keys"] == "all" and row["hdr_shape"] == "ok" and isinstance(st, int)
              and v.get("userAgent") and "round61" in str(v.get("userAgent")).lower()
              and str(v.get("fetchedAt", "")).startswith("2026-10-27"))
        row["verdict"] = "OK" if ok else "PROBLEM"
        res["ok" if ok else "bad"] += 1
        res["rows"].append(row)
    return res

if __name__ == "__main__":
    if not os.path.exists(TOOL):
        print(json.dumps({"tool": "ABSENT"}, indent=1)); sys.exit(0)
    print(json.dumps({"static": static(TOOL), "receipts": receipts(CAP), "tool_sha": hashlib.sha256(open(TOOL,'rb').read()).hexdigest()}, indent=1))
