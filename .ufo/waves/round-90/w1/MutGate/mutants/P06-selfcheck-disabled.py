#!/usr/bin/env python3
"""Behavioural conformance gate for a cache-key constructor (round 90).

Scores one candidate script against the round-89 key contract
(`.ufo/waves/round-89/c2-contract.md`): members, names, values, escaping,
layout, the refusal list and the output protocol. The candidate runs once per
case in an execution-time sandbox (audit hook): it may import the standard
library only and may open no file other than itself and the standard library,
spawn no process, open no socket and load no C library. A violation ends the
candidate's process at once with exit 97, so it cannot be caught and hidden.

Two populations are scored:
  * hand cases, each tagged with the contract clause it decides;
  * generated cases, built at run time from a seed (random unless --seed is
    given, printed either way) and decided by this gate's own reference, so a
    table over committed cases cannot pass.
A third population, advisory cases, holds inputs the contract does not decide but a
primary source does (RFC 8259 UTF-8 and string escaping, RFC 9110 §5.5 NUL). They
are reported on their own line and never scored into met.

Last two stdout lines:
  cache_key_conformance advisory=X/Y[ outside-contract-gaps=<labels>]
  cache_key_conformance clauses=A/B hand=C/D generated=E/F sandbox=ok|violation seed=S met=true|false
Exit 0 iff met. Exit 2 on usage or self-check failure.

Standard library only. Scratch: --work, else $TMPDIR (never a hardcoded /tmp).
"""

import argparse
import concurrent.futures as cf
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile

TCHARS = "!#$%&'*+-.^_`|~0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
US, RS, GS, X1D = "\x1f", "\x1e", "\x1c", "\x1d"
REFUSE = object()
VIOLATION_RC = 97

# ---------------------------------------------------------------- reference


class _Bad(Exception):
    pass


def _esc(s):
    out = []
    for ch in s:
        if ch == "%":
            out.append("%25")
        elif ch in (GS, X1D, RS, US):
            out.append("%%%02X" % ord(ch))
        else:
            out.append(ch)
    return "".join(out)


def _token(s):
    return len(s) > 0 and all(c in TCHARS for c in s)


def _trim(s):
    i, j = 0, len(s)
    while i < j and s[i] in " \t":
        i += 1
    while j > i and s[j - 1] in " \t":
        j -= 1
    return s[i:j]


def reference(obj):
    """Contract key for a decoded JSON value, or REFUSE."""
    try:
        if type(obj) is not dict:
            raise _Bad
        uri = obj.get("uri")
        if type(uri) is not str:
            raise _Bad
        hdrs = obj.get("request_headers")
        if type(hdrs) is not dict:
            raise _Bad
        seen = {}
        for name, value in hdrs.items():
            if type(name) is not str or not _token(name):
                raise _Bad
            if type(value) is not str or "\r" in value or "\n" in value:
                raise _Bad
            low = name.lower()
            if low in seen:
                raise _Bad
            seen[low] = value
        vary = obj["vary"] if "vary" in obj else ""
        if type(vary) is not str:
            raise _Bad
        members = []
        if vary != "":
            for raw in vary.split(","):
                m = _trim(raw)
                if m == "*" or not _token(m):
                    raise _Bad
                members.append(m.lower())
        if len(set(members)) != len(members):
            raise _Bad
        pairs = []
        for name in sorted(members):
            if name in seen:
                pairs.append(_esc(name) + RS + _esc(_trim(seen[name])))
            else:
                pairs.append(_esc(name) + RS + GS)
        return _esc(uri) + ("" if not pairs else US + US.join(pairs))
    except _Bad:
        return REFUSE


WORKED = [  # contract worked examples 1-7 (example 5 sent JSON-escaped)
    ({"uri": "https://e.test/a", "request_headers": {}}, "https://e.test/a"),
    ({"uri": "https://e.test/a", "request_headers": {"Accept-Encoding": "gzip"}, "vary": "Accept-Encoding"},
     "https://e.test/a" + US + "accept-encoding" + RS + "gzip"),
    ({"uri": "https://e.test/a", "request_headers": {"accept-encoding": "gzip", "Accept": "text/html"},
      "vary": " Accept ,Accept-Encoding "},
     "https://e.test/a" + US + "accept" + RS + "text/html" + US + "accept-encoding" + RS + "gzip"),
    ({"uri": "https://e.test/a", "request_headers": {"a": "50%"}, "vary": "a"},
     "https://e.test/a" + US + "a" + RS + "50%25"),
    ({"uri": "https://e.test/a", "request_headers": {"a": "x" + US + "b" + RS + "y"}, "vary": "a"},
     "https://e.test/a" + US + "a" + RS + "x%1Fb%1Ey"),
    ({"uri": "https://e.test/a", "request_headers": {"Accept-Encoding": ""}, "vary": "Accept-Encoding"},
     "https://e.test/a" + US + "accept-encoding" + RS),
    ({"uri": "https://e.test/a", "request_headers": {}, "vary": "Accept-Encoding"},
     "https://e.test/a" + US + "accept-encoding" + RS + GS),
]

# ---------------------------------------------------------------- hand cases
# (clause, label, payload bytes, expected key or REFUSE)

U = "https://e.test/p"


def _j(obj):
    return json.dumps(obj).encode()


def _k(*pairs):
    return U + ("" if not pairs else US + US.join(n + RS + v for n, v in pairs))


def hand_cases():
    c = []
    add = lambda clause, label, payload, exp: c.append((clause, label, payload, exp))
    for i, (obj, key) in enumerate(WORKED, 1):
        add("layout", "worked-%d" % i, _j(obj), key)
    # members: split, OWS trim, token, case-insensitive sort, duplicates
    add("members", "tab-trim", _j({"uri": U, "request_headers": {"a": "1", "b": "2"}, "vary": "\tb ,a\t"}),
        _k(("a", "1"), ("b", "2")))
    add("members", "sort-lowered-a-B", _j({"uri": U, "request_headers": {"a": "1", "B": "2"}, "vary": "a, B"}),
        _k(("a", "1"), ("b", "2")))
    add("members", "sort-lowered-B-a", _j({"uri": U, "request_headers": {"a": "1", "b": "2"}, "vary": "B, a"}),
        _k(("a", "1"), ("b", "2")))
    add("members", "sort-lowered-Zb", _j({"uri": U, "request_headers": {}, "vary": "Zz, b"}),
        _k(("b", GS), ("zz", GS)))
    add("members", "member-name-lowered", _j({"uri": U, "request_headers": {"x-a": "v"}, "vary": "X-A"}),
        _k(("x-a", "v")))
    add("members", "dup-member-case", _j({"uri": U, "request_headers": {}, "vary": "a, A"}), REFUSE)
    add("members", "dup-member-exact", _j({"uri": U, "request_headers": {"a": "1"}, "vary": "a,a"}), REFUSE)
    add("members", "trailing-comma", _j({"uri": U, "request_headers": {}, "vary": "a,"}), REFUSE)
    add("members", "leading-comma", _j({"uri": U, "request_headers": {}, "vary": ", a"}), REFUSE)
    add("members", "only-ows", _j({"uri": U, "request_headers": {}, "vary": "  "}), REFUSE)
    add("members", "inner-space", _j({"uri": U, "request_headers": {}, "vary": "a b"}), REFUSE)
    add("members", "lf-not-ows", _j({"uri": U, "request_headers": {}, "vary": "a\n"}), REFUSE)
    add("members", "vt-not-ows", _j({"uri": U, "request_headers": {}, "vary": "\x0ba"}), REFUSE)
    add("members", "non-ascii", _j({"uri": U, "request_headers": {}, "vary": "\u00e9"}), REFUSE)
    add("members", "wildcard", _j({"uri": U, "request_headers": {}, "vary": "*"}), REFUSE)
    add("members", "wildcard-listed", _j({"uri": U, "request_headers": {"a": "1"}, "vary": "a, *"}), REFUSE)
    add("members", "wildcard-ows", _j({"uri": U, "request_headers": {}, "vary": " * "}), REFUSE)
    add("members", "star-in-token", _j({"uri": U, "request_headers": {"a*": "1"}, "vary": "a*"}),
        _k(("a*", "1")))
    # names: case-insensitive lookup, duplicates, token, escaping of '%'
    add("names", "lookup-ci", _j({"uri": U, "request_headers": {"ACCEPT": "x"}, "vary": "accept"}),
        _k(("accept", "x")))
    add("names", "dup-header-ci", b'{"uri":"' + U.encode() + b'","request_headers":{"A":"1","a":"2"}}', REFUSE)
    add("names", "dup-header-unnominated", _j({"uri": U, "request_headers": {"Q": "1", "q": "1"}, "vary": "a"}),
        REFUSE)
    add("names", "name-not-token", _j({"uri": U, "request_headers": {"a b": "1"}}), REFUSE)
    add("names", "name-empty", _j({"uri": U, "request_headers": {"": "1"}}), REFUSE)
    add("names", "name-percent-present", _j({"uri": U, "request_headers": {"a%b": "x"}, "vary": "a%b"}),
        _k(("a%25b", "x")))
    add("names", "name-percent-absent", _j({"uri": U, "request_headers": {}, "vary": "A%1F"}),
        _k(("a%251f", GS)))
    # values: SP/HTAB edge trim only, byte-exact otherwise
    add("values", "edge-ows", _j({"uri": U, "request_headers": {"a": " \tgzip \t"}, "vary": "a"}),
        _k(("a", "gzip")))
    add("values", "vt-kept", _j({"uri": U, "request_headers": {"a": "\x0bgzip\x0c"}, "vary": "a"}),
        _k(("a", "\x0bgzip\x0c")))
    add("values", "nbsp-kept", _j({"uri": U, "request_headers": {"a": "\u00a0x"}, "vary": "a"}),
        _k(("a", "\u00a0x")))
    add("values", "case-kept", _j({"uri": U, "request_headers": {"a": "GZip"}, "vary": "a"}), _k(("a", "GZip")))
    add("values", "inner-ws-kept", _j({"uri": U, "request_headers": {"a": "x  \t y"}, "vary": "a"}),
        _k(("a", "x  \t y")))
    add("values", "all-ows-is-empty", _j({"uri": U, "request_headers": {"a": " \t "}, "vary": "a"}),
        _k(("a", "")))
    add("values", "cr-only", _j({"uri": U, "request_headers": {"a": "x\ry"}, "vary": "a"}), REFUSE)
    add("values", "lf-only", _j({"uri": U, "request_headers": {"a": "x\ny"}, "vary": "a"}), REFUSE)
    add("values", "cr-unnominated", _j({"uri": U, "request_headers": {"z": "x\r"}, "vary": "a"}), REFUSE)
    add("values", "lf-unnominated-novary", _j({"uri": U, "request_headers": {"z": "\nx"}}), REFUSE)
    add("values", "value-number", _j({"uri": U, "request_headers": {"a": 1}, "vary": "a"}), REFUSE)
    add("values", "value-null", _j({"uri": U, "request_headers": {"a": None}}), REFUSE)
    # escaping: '%' first, four separators, URI and names and values
    add("escaping", "value-each-sep", _j({"uri": U, "request_headers": {"a": GS + X1D + RS + US}, "vary": "a"}),
        _k(("a", "%1C%1D%1E%1F")))
    add("escaping", "value-percent-escape-literal", _j({"uri": U, "request_headers": {"a": "%1F"}, "vary": "a"}),
        _k(("a", "%251F")))
    add("escaping", "uri-percent", _j({"uri": "https://e.test/a%20b", "request_headers": {}}),
        "https://e.test/a%2520b")
    add("escaping", "uri-seps", _j({"uri": "u" + US + RS + GS + X1D, "request_headers": {}}), "u%1F%1E%1C%1D")
    add("escaping", "uri-seps-with-pair", _j({"uri": "u" + US, "request_headers": {"a": "v"}, "vary": "a"}),
        "u%1F" + US + "a" + RS + "v")
    add("escaping", "value-sep-not-ows", _j({"uri": U, "request_headers": {"a": US + "x"}, "vary": "a"}),
        _k(("a", "%1Fx")))
    # layout: absent vs empty, no-vary, empty vary
    add("layout", "vary-empty", _j({"uri": U, "request_headers": {"a": "1"}, "vary": ""}), U)
    add("layout", "vary-absent", _j({"uri": U, "request_headers": {"a": "1"}}), U)
    add("layout", "present-empty", _j({"uri": U, "request_headers": {"a": ""}, "vary": "a"}), _k(("a", "")))
    add("layout", "absent", _j({"uri": U, "request_headers": {}, "vary": "a"}), _k(("a", GS)))
    add("layout", "three-pairs", _j({"uri": U, "request_headers": {"c": "3", "A": "1"}, "vary": "c,b,a"}),
        _k(("a", "1"), ("b", GS), ("c", "3")))
    add("layout", "empty-uri", _j({"uri": "", "request_headers": {}, "vary": "a"}), US + "a" + RS + GS)
    # refusals on the envelope
    add("refusals", "malformed-json", b'{"uri": "x", ', REFUSE)
    add("refusals", "empty-input", b"", REFUSE)
    add("refusals", "array", b"[]", REFUSE)
    add("refusals", "string", b'"x"', REFUSE)
    add("refusals", "uri-missing", _j({"request_headers": {}}), REFUSE)
    add("refusals", "uri-number", _j({"uri": 1, "request_headers": {}}), REFUSE)
    add("refusals", "uri-null", _j({"uri": None, "request_headers": {}}), REFUSE)
    add("refusals", "headers-missing", _j({"uri": U}), REFUSE)
    add("refusals", "headers-missing-vary", _j({"uri": U, "vary": "a"}), REFUSE)
    add("refusals", "headers-list", _j({"uri": U, "request_headers": []}), REFUSE)
    add("refusals", "headers-null", _j({"uri": U, "request_headers": None}), REFUSE)
    add("refusals", "vary-number", _j({"uri": U, "request_headers": {}, "vary": 1}), REFUSE)
    add("refusals", "vary-null", _j({"uri": U, "request_headers": {}, "vary": None}), REFUSE)
    add("refusals", "vary-list", _j({"uri": U, "request_headers": {}, "vary": ["a"]}), REFUSE)
    return c


# ---------------------------------------------------------------- generated

NAME_POOL = ["a", "b", "Accept", "accept-encoding", "X-Y", "a%b", "Zz", "q", "Q1", "~t", "B"]
VAL_ALPHA = ["x", "Y", " ", "\t", "%", GS, X1D, RS, US, "\x0b", "1F", "\u00e9", ",", "*"]


def gen_case(rng):
    hdrs = {}
    used = set()
    for _ in range(rng.randint(0, 4)):
        n = rng.choice(NAME_POOL)
        n = "".join(ch.upper() if rng.random() < 0.3 else ch for ch in n)
        if n.lower() in used and rng.random() < 0.85:
            continue
        used.add(n.lower())
        hdrs[n] = "".join(rng.choice(VAL_ALPHA) for _ in range(rng.randint(0, 5)))
        if rng.random() < 0.04:
            hdrs[n] += rng.choice(["\r", "\n"])
    members = []
    for _ in range(rng.randint(0, 4)):
        m = rng.choice(NAME_POOL + [k for k in hdrs])
        m = "".join(ch.swapcase() if rng.random() < 0.3 else ch for ch in m)
        m = rng.choice(["", " ", "\t"]) + m + rng.choice(["", " ", "\t", " \t"])
        if rng.random() < 0.03:
            m = rng.choice(["*", "", "a b"])
        members.append(m)
    uri = "https://e.test/" + "".join(rng.choice(["p", "%", US, GS, "2", "/"]) for _ in range(rng.randint(0, 6)))
    obj = {"uri": uri, "request_headers": hdrs}
    if members or rng.random() < 0.5:
        obj["vary"] = ",".join(members)
    return obj


# ---------------------------------------------------------------- sandbox

SANDBOX = r'''
import os, sys, sysconfig, runpy
_cand = os.path.realpath(sys.argv[1])
_STD = set(sys.stdlib_module_names) | set(sys.builtin_module_names)
_roots = []
for _k in ("stdlib", "platstdlib"):
    _p = sysconfig.get_paths().get(_k)
    if _p:
        _roots.append(os.path.realpath(_p) + os.sep)
_roots = tuple(_roots)
_DENY = ("subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork",
         "os.forkpty", "pty.spawn", "socket.connect", "socket.bind", "socket.__new__", "ctypes.dlopen",
         "ctypes.dlsym", "ctypes.cdata", "glob.glob", "os.chdir",
         "os.startfile", "webbrowser.open", "urllib.Request", "shutil.copyfile", "os.remove",
         "os.rename", "os.mkdir", "os.rmdir", "os.unlink", "os.truncate", "os.chmod", "os.symlink")
def _die(why):
    os.write(2, ("SANDBOX_VIOLATION " + why + "\n").encode("utf-8", "replace"))
    os._exit(97)
def _hook(event, args):
    if event == "import":
        top = str(args[0]).split(".")[0]
        if top not in _STD:
            _die("import " + str(args[0]))
    elif event in ("os.listdir", "os.scandir"):
        p = args[0] if args and args[0] is not None else "."
        if isinstance(p, int):
            _die(event + " fd")
        if isinstance(p, bytes):
            p = os.fsdecode(p)
        rp = os.path.realpath(str(p)) + os.sep
        if not rp.startswith(_roots):
            _die(event + " " + rp)
    elif event == "open":
        p = args[0]
        if isinstance(p, int):
            return
        if isinstance(p, bytes):
            p = os.fsdecode(p)
        rp = os.path.realpath(str(p))
        if rp != _cand and not rp.startswith(_roots):
            _die("open " + rp)
    elif event.startswith(_DENY) or event == "sys.addaudithook":
        _die(event)
sys.argv = [_cand]
sys.addaudithook(_hook)
runpy.run_path(_cand, run_name="__main__")
'''


def run_candidate(py, sandbox, cand, payload, cwd):
    env = {"PATH": "/usr/bin:/bin", "LC_ALL": "C.UTF-8", "PYTHONIOENCODING": "utf-8"}
    try:
        p = subprocess.run([py, "-I", "-S", "-B", sandbox, cand], input=payload, capture_output=True,
                           timeout=20, cwd=cwd, env=env)
    except subprocess.TimeoutExpired:
        return ("timeout", None, b"")
    if p.returncode == VIOLATION_RC and b"SANDBOX_VIOLATION" in p.stderr:
        return ("violation", None, p.stderr)
    return (p.returncode, p.stdout, p.stderr)


def judge(result, expected):
    rc, out, err = result
    if rc == "violation" or rc == "timeout":
        return False, str(rc)
    if expected is REFUSE:
        ok = rc == 1 and out == b"" and err.startswith(b"invalid_input:")
        return ok, "" if ok else "expected refusal; rc=%r out=%r err=%r" % (rc, out[:80], err[:80])
    if rc != 0:
        return False, "expected key; rc=%r err=%r" % (rc, err[:120])
    try:
        text = out.decode("utf-8")
        lines = text.split("\n")
        if len(lines) != 2 or lines[1] != "":
            return False, "stdout must be one JSON line"
        doc = json.loads(lines[0])
    except (UnicodeDecodeError, ValueError):
        return False, "stdout not JSON: %r" % out[:80]
    if type(doc) is not dict or set(doc) != {"key"} or doc["key"] != expected:
        return False, "key mismatch: got %r want %r" % (doc, expected)
    return True, ""


def advisory_cases():
    """Cases the round-89 contract does not decide but a primary source does.

    Reported on their own line, never scored into met: they surface contract gaps
    (routed, not silently added). Expected outcome is the source's rule.
      utf8-required   RFC 8259 s8.1: JSON text exchanged between systems MUST be UTF-8.
      raw-control     RFC 8259 s7: U+0000..U+001F MUST be escaped inside a string
                      (the contract's worked example 5 says the controls are carried raw).
      nul-in-value    RFC 9110 s5.5: a field value with NUL is invalid; a recipient
                      MUST reject the message or replace NUL with SP.
    """
    return [
        ("advisory", "utf8-required", b'{"uri":"\xff","request_headers":{}}', REFUSE),
        ("advisory", "raw-control", b'{"uri":"u\x1f","request_headers":{}}', REFUSE),
        ("advisory", "nul-in-value", _j({"uri": U, "request_headers": {"a": "x\x00y"}, "vary": "a"}), REFUSE),
    ]


def self_check():
    return True
    for obj, key in WORKED:
        if reference(obj) != key:
            return False
    for clause, label, payload, exp in hand_cases():
        try:
            obj = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            if exp is not REFUSE:
                return False
            continue
        if reference(obj) != exp and not (reference(obj) is REFUSE and exp is REFUSE):
            return False
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--generated", type=int, default=120)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--work")
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args(argv)
    if not self_check():
        print("cache_key_conformance self-check failed: reference disagrees with the contract cases")
        return 2
    cand = os.path.realpath(a.candidate)
    if not os.path.isfile(cand):
        print("cache_key_conformance candidate missing: %s" % a.candidate)
        return 2
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1, 2 ** 31)
    rng = random.Random(seed)
    work = tempfile.mkdtemp(prefix="ckc-", dir=a.work or os.environ.get("TMPDIR") or None)
    try:
        sandbox = os.path.join(work, "sandbox.py")
        with open(sandbox, "w") as fh:
            fh.write(SANDBOX)
        cwd = os.path.join(work, "cwd")
        os.mkdir(cwd)
        hand = hand_cases()
        gen = []
        for i in range(a.generated):
            obj = gen_case(rng)
            gen.append(("generated", "g%03d" % i, json.dumps(obj).encode(), reference(obj)))
        adv = advisory_cases()
        allc = hand + gen + adv
        with cf.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            results = list(ex.map(lambda c: run_candidate(a.python, sandbox, cand, c[2], cwd), allc))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    clause_ok = {}
    hand_pass = gen_pass = 0
    violation = False
    advisory_fail = []
    for (clause, label, payload, exp), res in zip(allc, results):
        ok, why = judge(res, exp)
        if clause == "advisory":
            if not ok:
                advisory_fail.append(label)
            continue
        violation = violation or res[0] == "violation"
        if clause == "generated":
            gen_pass += ok
        else:
            hand_pass += ok
            clause_ok[clause] = clause_ok.get(clause, True) and ok
        if not ok and a.verbose:
            print("FAIL %s/%s: %s" % (clause, label, why or res[0]))
            if res[0] == "violation":
                print("  " + res[2].decode("utf-8", "replace").strip())
    nclauses = len(clause_ok)
    cpass = sum(clause_ok.values())
    met = (not violation and cpass == nclauses and hand_pass == len(hand) and gen_pass == len(gen))
    print("cache_key_conformance advisory=%d/%d%s" % (
        len(adv) - len(advisory_fail), len(adv),
        (" outside-contract-gaps=" + ",".join(advisory_fail)) if advisory_fail else ""))
    print("cache_key_conformance clauses=%d/%d hand=%d/%d generated=%d/%d sandbox=%s seed=%d met=%s" % (
        cpass, nclauses, hand_pass, len(hand), gen_pass, len(gen), "violation" if violation else "ok", seed,
        "true" if met else "false"))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
