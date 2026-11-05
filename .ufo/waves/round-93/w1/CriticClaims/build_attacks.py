#!/usr/bin/env python3
"""CriticClaims r93: build the C2 attack subjects used against
.ufo/waves/round-93/c93_conditional.py. Writes them into the directory given as
argv[1]. The frozen counter is imported (read-only) to derive the exact case
population; nothing frozen is modified.

Subjects
  A_cache_lazy.py     full decision logic, but If-Match/If-Unmodified-Since are
                      validated only in the origin role -> clause 6 violated,
                      no frozen case distinguishes it.
  B_lookup.py         no evaluation logic at all: a dict from the sorted-JSON
                      input to the expected answer for all 44 hand + 120
                      generated cases; 200 for anything else.
  C_crash_refusal.py  correct on valid input; malformed input raises (traceback,
                      no `invalid_input:` line) -> clause 4/6 refusal form
                      violated, still counted as "refused".
  D_hand_only.py      the 44 hand answers as a table, 200 elsewhere.
  E_no_validation.py  correct decision order, no clause 1-4 validation.
  F1_import.py        `import c93_conditional` (oracle import).
  F2_open.py          open the counter by absolute path.
  F3_shell.py         import subprocess / os.system.
  G_copied_oracle.py  the counter's own reference() copied verbatim into the
                      subject.
"""

import importlib.util
import json
import os
import sys

COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-93/c93_conditional.py"
OUT = sys.argv[1]


def load():
    spec = importlib.util.spec_from_file_location("c93", COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


HEAD = '''import json, re, sys

def out(dec, pre=None):
    sys.stdout.write(json.dumps({"decision": dec, "precondition": pre}) + "\\n")
    sys.exit(0)

def bad(msg):
    sys.stderr.write("invalid_input: %s\\n" % msg)
    sys.exit(1)

inp = json.loads(sys.stdin.read())
'''

BODY = r'''
class Invalid(Exception):
    pass

def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)

TCHAR = re.compile(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+")
ETAGC = set("!") | {chr(c) for c in range(0x23, 0x7F)}

def parse_etag(s):
    weak = s.startswith("W/")
    rest = s[2:] if weak else s
    if len(rest) < 2 or rest[0] != '"' or rest[-1] != '"':
        raise Invalid("malformed entity-tag")
    for ch in rest[1:-1]:
        if ch not in ETAGC:
            raise Invalid("malformed entity-tag")
    return weak, rest[1:-1]

def parse_list(value):
    s = value.strip(" \t")
    if s == "*":
        return "*"
    if not s:
        raise Invalid("empty value")
    out = []
    for part in s.split(","):
        p = part.strip(" \t")
        if not p:
            raise Invalid("empty member")
        if p == "*":
            raise Invalid("star mixed")
        out.append(parse_etag(p))
    return out

def strong(a, b):
    return (not a[0]) and (not b[0]) and a[1] == b[1]

def weak(a, b):
    return a[1] == b[1]
'''

DECIDE = r'''
method = inp["method"]
cur = inp["current"]
req = inp["request"]
role = inp.get("role", "origin")
exists = cur["exists"]
cur_tag = parse_etag(cur["etag"]) if cur["etag"] is not None else None
lastmod = cur["last_modified"]
im = parse_list(req["if_match"]) if req["if_match"] is not None else None
inm = parse_list(req["if_none_match"]) if req["if_none_match"] is not None else None
ims = req["if_modified_since"]
ius = req["if_unmodified_since"]

def matches(spec, cmp):
    if spec == "*":
        return exists
    if not exists or cur_tag is None:
        return False
    return any(cmp(t, cur_tag) for t in spec)

if role == "origin":
    if im is not None:
        if not matches(im, strong):
            out("412", "if_match")
    elif ius is not None and lastmod is not None:
        if not lastmod <= ius:
            out("412", "if_unmodified_since")
if inm is not None:
    if matches(inm, weak):
        out("304" if method in ("GET", "HEAD") else "412", "if_none_match")
elif ims is not None and method in ("GET", "HEAD") and lastmod is not None:
    if lastmod <= ims:
        out("304", "if_modified_since")
out("200", None)
'''

A_CACHE_LAZY = HEAD + BODY + r'''
method = inp["method"]
cur = inp["current"]
req = inp["request"]
role = inp.get("role", "origin")
exists = cur["exists"]
cur_tag = parse_etag(cur["etag"]) if cur["etag"] is not None else None
lastmod = cur["last_modified"]
inm = parse_list(req["if_none_match"]) if req["if_none_match"] is not None else None
ims = req["if_modified_since"]

def matches(spec, cmp):
    if spec == "*":
        return exists
    if not exists or cur_tag is None:
        return False
    return any(cmp(t, cur_tag) for t in spec)

if role == "origin":
    # defect: If-Match / If-Unmodified-Since are parsed only here, so a cache
    # role input with a malformed field is decided instead of refused (clause 6)
    im = parse_list(req["if_match"]) if req["if_match"] is not None else None
    ius = req["if_unmodified_since"]
    if im is not None:
        if not matches(im, strong):
            out("412", "if_match")
    elif ius is not None and lastmod is not None:
        if not lastmod <= ius:
            out("412", "if_unmodified_since")
if inm is not None:
    if matches(inm, weak):
        out("304" if method in ("GET", "HEAD") else "412", "if_none_match")
elif ims is not None and method in ("GET", "HEAD") and lastmod is not None:
    if lastmod <= ims:
        out("304", "if_modified_since")
out("200", None)
'''

C_CRASH = HEAD + BODY + DECIDE.replace("def bad", "def _unused_bad")
E_NO_VALIDATION = HEAD + r'''
method = inp["method"]
cur = inp["current"]
req = inp["request"]
role = inp.get("role", "origin")
exists = cur["exists"]
etag = cur["etag"]
lastmod = cur["last_modified"]
def tag(s):
    try:
        w = s.startswith("W/")
        r = s[2:] if w else s
        return (w, r[1:-1])
    except Exception:
        return (False, s)
def lst(v):
    if v is None:
        return None
    s = v.strip()
    if s == "*":
        return "*"
    return [tag(p.strip()) for p in s.split(",") if p.strip()]
cur_tag = tag(etag) if etag is not None else None
im, inm = lst(req["if_match"]), lst(req["if_none_match"])
ims, ius = req["if_modified_since"], req["if_unmodified_since"]
def matches(spec, cmp):
    if spec == "*":
        return exists
    if not exists or cur_tag is None:
        return False
    return any(cmp(t, cur_tag) for t in spec)
def strong(a, b):
    return (not a[0]) and (not b[0]) and a[1] == b[1]
def weak(a, b):
    return a[1] == b[1]
if role == "origin":
    if im is not None:
        if not matches(im, strong):
            out("412", "if_match")
    elif ius is not None and lastmod is not None:
        if not lastmod <= ius:
            out("412", "if_unmodified_since")
if inm is not None:
    if matches(inm, weak):
        out("304" if method in ("GET", "HEAD") else "412", "if_none_match")
elif ims is not None and method in ("GET", "HEAD") and lastmod is not None:
    if lastmod <= ims:
        out("304", "if_modified_since")
out("200", None)
'''

F1 = 'import c93_conditional\nprint(c93_conditional.reference({}))\n'
F2 = ('f = open("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/'
      'round-93/c93_conditional.py")\nprint(len(f.read()))\n')
F3 = 'import subprocess\nprint(subprocess.run(["true"]).returncode)\n'


def main():
    m = load()
    os.makedirs(OUT, exist_ok=True)
    cases = m.hand_cases()
    gen = []
    for inp in m.generate(93, 120):
        try:
            gen.append((inp, m.reference(inp)))
        except m.Invalid:
            continue
    table = {}
    for _, inp, exp in cases:
        table[json.dumps(inp, sort_keys=True)] = exp
    for inp, exp in gen:
        table[json.dumps(inp, sort_keys=True)] = exp
    hand_only = {json.dumps(inp, sort_keys=True): exp for _, inp, exp in cases
                 if exp is not None}
    files = {
        "A_cache_lazy.py": A_CACHE_LAZY,
        "C_crash_refusal.py": C_CRASH,
        "E_no_validation.py": E_NO_VALIDATION,
        "F1_import.py": F1,
        "F2_open.py": F2,
        "F3_shell.py": F3,
        "B_lookup.py": HEAD + "TABLE = " + json.dumps(table, sort_keys=True) + "\n"
                      "k = json.dumps(inp, sort_keys=True)\n"
                      "if k in TABLE:\n"
                      "    e = TABLE[k]\n"
                      "    out(e['decision'], e['precondition'])\n"
                      "out('200', None)\n",
        "D_hand_only.py": HEAD + "TABLE = " + json.dumps(hand_only, sort_keys=True) + "\n"
                          "k = json.dumps(inp, sort_keys=True)\n"
                          "if k in TABLE:\n"
                          "    e = TABLE[k]\n"
                          "    out(e['decision'], e['precondition'])\n"
                          "out('200', None)\n",
    }
    # G: the counter's own reference, copied verbatim
    src = open(COUNTER, encoding="utf-8").read()
    start = src.index("TOP_KEYS = {")
    end = src.index("\n\ndef C(")
    files["G_copied_oracle.py"] = (
        "import json, re, sys\n" + src[start:end] + "\n"
        "try:\n"
        "    inp = json.loads(sys.stdin.read())\n"
        "    sys.stdout.write(json.dumps(reference(inp)) + '\\n')\n"
        "except Invalid as e:\n"
        "    sys.stderr.write('invalid_input: %s\\n' % e)\n"
        "    sys.exit(1)\n")
    for name, text in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(text)
    print("wrote %d subjects to %s (hand=%d generated=%d)"
          % (len(files), OUT, len(cases), len(gen)))


if __name__ == "__main__":
    main()
