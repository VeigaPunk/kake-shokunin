#!/usr/bin/env python3
"""Compose CriticClaims C2 escape candidates from the frozen oracle skeleton."""
import os

CAND = "/fast/scratch/hyaku/kake-r99/CriticClaims/cand"
os.makedirs(CAND, exist_ok=True)

HEAD = '''import json, re, sys
TCHAR = re.compile(r"^[!#$%&'*+\\-.^_`|~0-9A-Za-z]+$")
HOP = {'keep-alive', 'proxy-connection', 'te', 'transfer-encoding', 'upgrade'}
PROXY = {'proxy-authenticate', 'proxy-authentication-info', 'proxy-authorization'}


class Refuse(Exception):
    pass


def _is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _headers(h):
    if not isinstance(h, dict):
        raise Refuse("headers not an object")
    out = {}
    for k, v in h.items():
        if not isinstance(k, str) or not TCHAR.match(k):
            raise Refuse("invalid header name")
        lk = k.lower()
        if lk in out:
            raise Refuse("case-duplicate header name")
        if not isinstance(v, str):
            raise Refuse("non-string header value")
        if any(c in v for c in "\\r\\n\\x00"):
            raise Refuse("CR/LF/NUL in value")
        out[lk] = v
    return out


def _etag(v):
    """Return (weak, opaque) or raise."""
    s = v.strip(" \\t")
    weak = False
    if s.startswith("W/"):
        weak = True
        s = s[2:]
    if len(s) < 2 or s[0] != '"' or s[-1] != '"':
        raise Refuse("malformed etag")
    op = s[1:-1]
    for ch in op:
        o = ord(ch)
        if not (o == 0x21 or 0x23 <= o <= 0x7E or 0x80 <= o <= 0xFF):
            raise Refuse("malformed etag")
    return weak, op
'''

REF = '''

def reference(inp):
    if not isinstance(inp, dict) or set(inp) != {"stored", "response"}:
        raise Refuse("top-level keys")
    resp = inp["response"]
    if not isinstance(resp, dict) or set(resp) != {"status", "headers"}:
        raise Refuse("response keys")
    if not _is_int(resp["status"]) or resp["status"] != 304:
        raise Refuse("status not 304")
    rh = _headers(resp["headers"])
    stored = inp["stored"]
    if not isinstance(stored, list):
        raise Refuse("stored not a list")
    ids = set()
    norm = []
    for el in stored:
        if not isinstance(el, dict) or set(el) != {"id", "received", "headers"}:
            raise Refuse("stored element keys")
        if not isinstance(el["id"], str) or el["id"] == "" or el["id"] in ids:
            raise Refuse("bad id")
        ids.add(el["id"])
        if not _is_int(el["received"]):
            raise Refuse("received not integer")
        sh = _headers(el["headers"])
        et = _etag(sh["etag"]) if "etag" in sh else None
        lm = sh["last-modified"].strip(" \\t") if "last-modified" in sh else None
        norm.append((el["id"], el["received"], sh, et, lm))
    ret = _etag(rh["etag"]) if "etag" in rh else None
    rlm = rh["last-modified"].strip(" \\t") if "last-modified" in rh else None
    cc = rh.get("cache-control", "")
    if 'no-cache="' in cc.lower() or 'private="' in cc.lower():
        raise Refuse("qualified cache-control outside contract")
    if ret is not None and not ret[0]:
        rule = "strong"
        sel = [n for n in norm if n[3] is not None and not n[3][0] and n[3][1] == ret[1]]
        dec_none = "must-not-update"
    elif ret is not None or rlm is not None:
        rule = "weak"
        corr = []
        for n in norm:
            ok = True
            if ret is not None:
                ok = ok and n[3] is not None and n[3][1] == ret[1]
            if rlm is not None:
                ok = ok and n[4] is not None and n[4] == rlm
            if ok:
                corr.append(n)
        sel = []
        if corr:
            top = max(n[1] for n in corr)
            best = [n for n in corr if n[1] == top]
            if len(best) > 1:
                raise Refuse("ambiguous most recent")
            sel = best
        dec_none = "no-update"
    else:
        rule = "no-validator"
        sel = [norm[0]] if len(norm) == 1 and norm[0][3] is None and norm[0][4] is None else []
        dec_none = "no-update"
    excl = {"content-length", "connection"} | HOP | PROXY
    if "connection" in rh:
        for m in rh["connection"].split(","):
            m = m.strip(" \\t").lower()
            if m:
                excl.add(m)
    upd = []
    for n in sel:
        h = dict(n[2])
        for k, v in rh.items():
            if k not in excl:
                h[k] = v
        upd.append({"id": n[0], "headers": h})
    return {"decision": "update" if upd else dec_none, "rule": rule, "updated": upd}
'''

MAIN = '''

def main():
    try:
        inp = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        out = reference(inp)
    except (Refuse, ValueError, UnicodeDecodeError, KeyError, TypeError, AttributeError) as e:
        sys.stderr.write("invalid_input: %s\\n" % e)
        return 1
    sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

# e1: strip stored hop-by-hop/proxy/connection fields from the updated map (contract never
# excludes stored fields; only 304 fields are excepted). Untested: stored maps never carry them.
e1 = HEAD + REF.replace(
    "    upd = []\n    for n in sel:\n        h = dict(n[2])\n",
    "    upd = []\n    for n in sel:\n        h = dict(n[2])\n"
    "        for sk in list(h):\n"
    "            if sk == \"connection\" or sk in HOP or sk in PROXY:\n"
    "                del h[sk]\n") + MAIN

# e2: lazy stored-ETag parsing; malformed stored ETags escape refusal when the 304 carries
# Last-Modified only (weak rule never reads stored ETags then).
e2 = HEAD + REF.replace(
    '        et = _etag(sh["etag"]) if "etag" in sh else None\n        lm = sh["last-modified"].strip(" \\t") if "last-modified" in sh else None\n        norm.append((el["id"], el["received"], sh, et, lm))',
    '        lm = sh["last-modified"].strip(" \\t") if "last-modified" in sh else None\n        norm.append((el["id"], el["received"], sh, None, lm))'
).replace(
    '    ret = _etag(rh["etag"]) if "etag" in rh else None',
    '    etmem = {}\n'
    '    def get_et(n):\n'
    '        if n[0] not in etmem:\n'
    '            etmem[n[0]] = _etag(n[2]["etag"]) if "etag" in n[2] else None\n'
    '        return etmem[n[0]]\n'
    '    ret = _etag(rh["etag"]) if "etag" in rh else None'
).replace(
    '        sel = [n for n in norm if n[3] is not None and not n[3][0] and n[3][1] == ret[1]]',
    '        sel = [n for n in norm if get_et(n) is not None and not get_et(n)[0] and get_et(n)[1] == ret[1]]'
).replace(
    '                ok = ok and n[3] is not None and n[3][1] == ret[1]',
    '                ok = ok and get_et(n) is not None and get_et(n)[1] == ret[1]'
).replace(
    '        sel = [norm[0]] if len(norm) == 1 and norm[0][3] is None and norm[0][4] is None else []',
    '        sel = [norm[0]] if len(norm) == 1 and get_et(norm[0]) is None and norm[0][4] is None else []'
) + MAIN

# e3: Last-Modified trimmed of spaces only (contract: spaces AND tabs) — generator and hand
# cases only ever pad with spaces.
e3 = (HEAD + REF
      .replace('lm = sh["last-modified"].strip(" \\t")', 'lm = sh["last-modified"].strip(" ")')
      .replace('rlm = rh["last-modified"].strip(" \\t")', 'rlm = rh["last-modified"].strip(" ")')
      ) + MAIN

# e4: refusal prints a newline on stdout (contract: nothing on stdout; judge strips).
e4 = HEAD + REF + '''
def main():
    try:
        inp = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        out = reference(inp)
    except (Refuse, ValueError, UnicodeDecodeError, KeyError, TypeError, AttributeError) as e:
        sys.stdout.write("\\n")
        sys.stderr.write("invalid_input: %s\\n" % e)
        return 1
    sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

# e5: unparseable JSON crashes with a traceback (contract: invalid_input refusal); scored
# inputs are always valid JSON, so this never surfaces.
e5 = HEAD + REF + '''
def main():
    inp = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    try:
        out = reference(inp)
    except (Refuse, ValueError, UnicodeDecodeError, KeyError, TypeError, AttributeError) as e:
        sys.stderr.write("invalid_input: %s\\n" % e)
        return 1
    sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

# e6: also excludes the 304's Age field from the copy (LC5: no other field is excluded).
e6 = HEAD + REF.replace(
    '    excl = {"content-length", "connection"} | HOP | PROXY',
    '    excl = {"content-length", "connection", "age"} | HOP | PROXY') + MAIN

# honest-strict: contract-honouring candidate that additionally refuses JSON objects carrying
# case-insensitive duplicate keys (contract silent; reference last-wins). Direction-B probe:
# expected to PASS the counter too (no scored input exercises it) -> no false negative found.
strict = HEAD + REF + '''

def _pairs(pairs):
    seen = set()
    for k, _ in pairs:
        lk = k.lower() if isinstance(k, str) else k
        if lk in seen:
            raise ValueError("duplicate object key in input")
        seen.add(lk)
    return dict(pairs)


def main():
    try:
        inp = json.loads(sys.stdin.buffer.read().decode("utf-8"), object_pairs_hook=_pairs)
        out = reference(inp)
    except (Refuse, ValueError, UnicodeDecodeError, KeyError, TypeError, AttributeError) as e:
        sys.stderr.write("invalid_input: %s\\n" % e)
        return 1
    sys.stdout.write(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''

for name, body in [("e1-storedhopstrip", e1), ("e2-lazyetag", e2), ("e3-lmspacetrim", e3),
                   ("e4-wsstdout", e4), ("e5-badjsoncrash", e5), ("e6-ageexcl", e6),
                   ("honest-strict", strict)]:
    with open(os.path.join(CAND, name + ".py"), "w") as f:
        f.write(body)
    print("wrote", name, len(body))
