#!/usr/bin/env python3
"""Independent reading of .ufo/waves/round-89/c2-contract.md (ReviewGate, round 90).
Written from the contract text only. Env knobs (for variant probes):
  MODE env is not available under the gate (env is scrubbed), so variants are separate files."""
import json, sys

TCHAR = set("!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
US, RS, GS = "\u001f", "\u001e", "\u001c"
SEP = {"\u001c": "%1C", "\u001d": "%1D", "\u001e": "%1E", "\u001f": "%1F", "%": "%25"}

class Refuse(Exception):
    pass

def tok(s):
    return s != "" and all(c in TCHAR for c in s)

def ows(s):
    return s.strip(" \t")

def esc(s):
    return "".join(SEP.get(c, c) for c in s)

def lower_ascii(s):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in s)

def key(obj):
    if not isinstance(obj, dict):
        raise Refuse("not an object")
    if "uri" not in obj or not isinstance(obj["uri"], str):
        raise Refuse("uri")
    if "request_headers" not in obj or not isinstance(obj["request_headers"], dict):
        raise Refuse("request_headers")
    hdr = {}
    for n, v in obj["request_headers"].items():
        if not isinstance(n, str) or not tok(n):
            raise Refuse("name")
        if not isinstance(v, str) or "\r" in v or "\n" in v:
            raise Refuse("value")
        ln = lower_ascii(n)
        if ln in hdr:
            raise Refuse("dup header")
        hdr[ln] = v
    vary = obj.get("vary", "")
    if not isinstance(vary, str):
        raise Refuse("vary type")
    mem = []
    if vary != "":
        for m in vary.split(","):
            m = ows(m)
            if m == "*":
                raise Refuse("wildcard")
            if not tok(m):
                raise Refuse("member")
            m = lower_ascii(m)
            if m in mem:
                raise Refuse("dup member")
            mem.append(m)
    mem.sort()
    if not mem:
        return esc(obj["uri"])
    parts = [esc(n) + RS + (esc(ows(hdr[n])) if n in hdr else GS) for n in mem]
    return esc(obj["uri"]) + US + US.join(parts)

class _Dup(dict):
    pass

def main(raw_ok=True, tb=False, newline=True):
    data = sys.stdin.buffer.read()
    try:
        try:
            text = data.decode("utf-8")
            obj = json.loads(text, strict=not raw_ok, object_pairs_hook=lambda ps: _Dup(ps) if len({k for k, _ in ps}) != len(ps) else dict(ps))
        except ValueError:
            raise Refuse("not JSON")
        if isinstance(obj, dict) and isinstance(obj.get("request_headers"), _Dup):
            raise Refuse("dup header (exact)")
        k = key(obj)
    except Refuse as e:
        sys.stderr.write("invalid_input: %s\n" % e)
        if tb:
            import traceback; traceback.print_stack(file=sys.stderr)
        return 1
    out = json.dumps({"key": k})
    sys.stdout.write(out + ("\n" if newline else ""))
    return 0

if __name__ == "__main__":
    sys.exit(main())
