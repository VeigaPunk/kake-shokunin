#!/usr/bin/env python3
import json, sys
US, RS, GS = "\x1f", "\x1e", "\x1c"
T = "!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
def esc(s):
    for raw, enc in (("%", "%25"), (GS, "%1C"), ("\x1d", "%1D"), (RS, "%1E"), (US, "%1F")):
        s = s.replace(raw, enc)
    return s
def tok(s):
    return bool(s) and all(c in T for c in s)
def main():
    try:
        obj = json.load(sys.stdin)
    except Exception:
        print("invalid_input: not JSON", file=sys.stderr); return 1
    if not isinstance(obj, dict):
        print("invalid_input: input must be a JSON object", file=sys.stderr); return 1
    uri = obj.get("uri")
    if not isinstance(uri, str):
        print("invalid_input: uri must be a string", file=sys.stderr); return 1
    headers = obj.get("request_headers")
    if not isinstance(headers, dict):
        print("invalid_input: request_headers must be an object", file=sys.stderr); return 1
    _vn = set(x.strip(" \t").lower() for x in obj.get("vary", "").split(",")) if isinstance(obj.get("vary", ""), str) else set()
    low = {}
    for name, value in headers.items():
        if not isinstance(name, str) or not tok(name):
            print("invalid_input: header name is not a token", file=sys.stderr); return 1
        if not isinstance(value, str):
            print("invalid_input: header value must be a string", file=sys.stderr); return 1
        if "\r" in value or "\n" in value:
            print("invalid_input: header value contains CR or LF", file=sys.stderr); return 1
        k = name.lower()
        if k in low and k in _vn:
            print("invalid_input: duplicate header name", file=sys.stderr); return 1
        low[k] = value
    vary = obj.get("vary", "")
    if not isinstance(vary, str):
        print("invalid_input: vary must be a string", file=sys.stderr); return 1
    names = []
    if vary != "":
        for raw in vary.split(","):
            m = raw.strip(" \t")
            if m == "*":
                print("invalid_input: vary wildcard nominates no field", file=sys.stderr); return 1
            if not tok(m):
                print("invalid_input: vary member is not a token", file=sys.stderr); return 1
            names.append(m.lower())
    if len(set(names)) != len(names):
        print("invalid_input: duplicate vary member", file=sys.stderr); return 1
    parts = []
    for name in sorted(names):
        if name in low:
            parts.append(esc(name) + RS + esc(low[name].strip(" \t")))
        else:
            parts.append(esc(name) + RS + GS)
    key = esc(uri) + ("" if not parts else US + US.join(parts))
    print(json.dumps({"key": key}))
    return 0
raise SystemExit(main())
