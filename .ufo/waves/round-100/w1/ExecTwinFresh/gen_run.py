#!/usr/bin/env python3
"""ExecTwinFresh r100 differential: own generator, twin vs frozen oracle.

Corpus is ours (scenario templates + targeted CC/refusal families);
c100_fresh304.py's generator/code and frozen/*.py sources were not read
for behaviour. Oracle is a black-box peer process (python3 -I -B stdin bytes).
Compared: rc, parsed stdout JSON (key order free, list order significant),
refusal shape (rc 1 + empty stdout + stderr prefix 'invalid_input:'),
and e4 stdout shape (no leading whitespace, at most one trailing \\n).
"""
import json
import os
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
ORACLE = LANE + "/.ufo/waves/round-100/frozen/pos-oracle.py"
TWIN = LANE + "/.ufo/waves/round-100/w1/ExecTwinFresh/twin.py"
WORK = "/fast/scratch/hyaku/kake-r100/ExecTwinFresh"

SEED = 100226
N = 3600

OPAQUE_CHARS = ["!"] + [chr(c) for c in range(0x23, 0x7F)] + [chr(c) for c in range(0x80, 0x100)]
TOKEN_PARTS = ["x-a", "etag", "ETag", "last-modified", "Last-Modified", "cache-control",
               "Cache-Control", "connection", "Connection", "content-length", "keep-alive",
               "TE", "transfer-encoding", "upgrade", "proxy-authenticate", "x-secret",
               "X-Secret", "age", "date", "server", "x-pad", "x-listed", "proxy-authorization",
               "proxy-authentication-info", "proxy-connection"]
LM = "Tue, 01 Jan 2035 00:00:00 GMT"
LM2 = "Wed, 02 Jan 2035 00:00:00 GMT"


def opaque(rnd, k=None):
    k = k if k is not None else rnd.randint(0, 8)
    return "".join(rnd.choice(OPAQUE_CHARS) for _ in range(k))


def stored(id_, received, headers):
    return {"id": id_, "received": received, "headers": headers}


def resp(headers, status=304):
    return {"status": status, "headers": headers}


def inp(stored_list, r_headers, status=304):
    return {"stored": stored_list, "response": resp(r_headers, status)}


def cc_case(rnd):
    # Mixed-case qualified names, token/quoted/empty-quoted, extensions,
    # empty elements, malformed forms, controls, non-ASCII, semicolons,
    # commas inside quoted strings, escapes, OWS placement.
    name = rnd.choice(["no-cache", "NO-CACHE", "No-Cache", "nO-cAcHe", "private",
                       "PRIVATE", "Private", "pRiVaTe"])
    ext = rnd.choice(["x-no-cache", "no-cachex", "x-private", "privatex",
                      "my-no-cache-tag", "noprivte"])
    arg = rnd.choice(["x", "abc", "a-b", "", "0", "a,b", "f", "!#$", "é", "a b"])
    qarg = '"%s"' % arg
    form = rnd.choice([
        "%s=%s", "%s=%s", "%s=%s",  # token / quoted / empty-quoted mix (arg may be "")
        "%s=%s", "%s", "%s", "%s",
        "%s=,%s=x", ",%s=%s", "%s=%s,", "%s=%s,,", "%s =%s", "%s= %s",
        "%s\t=%s", "%s=\t%s", ' %s=%s', '%s=%s ', "\t%s=%s\t",
        "max-age=5, %s=%s", "%s=%s, max-age=1", "max-age=1,,%s=%s",
        "%s=%s;z=1", "%s=%s; ", "%s;", "%s %s", "%s=\"unclosed",
        "x=%s, %s=%s", "%s=%s, ", ", %s=%s", "%s=\"a,b\"", "%s=\"a\\\"b\"",
        "%s=\"a\\\\\"", "%s=\"a\x01b\"", "%s=\"a\x7fb\"", "%s=\"é\"",
        "%s=\"a\tb\"", "%s=a\x7fb", "%s=é", "é=%s", "no-cache\x01=%s",
        "%s=%s\r", "%s=%s\n", "%s=%s\x00", "%s=\"a\n\"", "%s=\"a\"x",
        "%s==%s", "=x", "%s=", "%s= ", '"%s"=%s', "%s='x'", "%s=*",
        "%s=^", "%s=x y", "%s=x,,y", " , , ", "", " ", ",", ",,",
        "private", "no-cache", "public", "max-age=60", "must-revalidate",
        "no-cache=abc", "No-Cache=\"s\"", "private=\"\"", "PRIVATE=z",
        "private=", 'private=""', "no-cachex=1", 'x-no-cache="a"',
        "foo-private=\"a\"", "NO-CACHEX=\"1\"",
    ])
    args = {"%s": None}  # placeholder; built below
    # Build the value.
    if form == "%s":
        cc = rnd.choice([name, ext, "private", "no-cache"])
    elif form == "%s=%s":
        cc = ("no-cache=%s" if rnd.random() < 0.5 else "private=%s") % (
            rnd.choice([arg, qarg, chr(34)+chr(34), chr(34)+"a,b"+chr(34), "é", ""]))
    elif form == "%s=%s," or form == "%s=%s,,":
        cc = (name + "=" + rnd.choice([arg, qarg]) + form[-2:])
    elif form in ("%s =%s", "%s= %s", "%s\t=%s", "%s=\t%s",
                  ' %s=%s', '%s=%s ', "\t%s=%s\t"):
        cc = form % (name, rnd.choice([arg, qarg]))
        if "%s =%s" in form or "%s= %s" in form or "\t" in form:
            pass
        else:
            cc = form % (name, qarg) if "%s=%s" in form else form % name
    elif form == "%s=%s":
        cc = name + "=" + rnd.choice([arg, qarg])
    else:
        # Generic fill: name/ext + arg/qarg into remaining placeholders.
        pool = [name, ext, arg, qarg, "1", "x"]
        vals = []
        tmp = form
        i = 0
        while "%s" in tmp:
            tmp = tmp.replace("%s", pool[i % len(pool)], 1)
            i += 1
        cc = tmp
    # Wrap: 304 carries either an etag match (update path) or nothing.
    mode = rnd.random()
    if mode < 0.5:
        op = opaque(rnd, 3)
        headers = {"etag": '"%s"' % op, "cache-control": cc}
        st = [stored("s0", rnd.choice([0, 1, 7]), {"etag": '"%s"' % op, "x-a": " 1 "})]
        return inp(st, headers), "cc"
    elif mode < 0.8:
        return inp([], {"cache-control": cc}), "cc-empty"
    else:
        headers = {"cache-control": cc, "age": rnd.choice(["0", " 5 ", "\t9\t"])}
        st = [stored("s0", 2, {"x-a": "v"})]
        return inp(st, headers), "cc-novalidator"


def sc_strong(rnd):
    op = opaque(rnd)
    n = rnd.randint(0, 4)
    st = []
    for i in range(n):
        kind = rnd.choice(["match", "match", "match-weak", "other", "other-weak",
                           "case-variant", "no-etag", "bare"])
        h = {"content-type": "text/html"}
        if kind == "match":
            h["etag"] = '"%s"' % op
        elif kind == "match-weak":
            h["etag"] = 'W/"%s"' % op
        elif kind == "other":
            h["etag"] = '"%s"' % opaque(rnd)
        elif kind == "other-weak":
            h["etag"] = 'W/"%s"' % opaque(rnd)
        elif kind == "case-variant":
            h["etag"] = '"%s"' % (op.upper() if rnd.random() < 0.5 else op.lower())
        elif kind == "no-etag":
            h["last-modified"] = LM
        st.append(stored("s%d" % i, rnd.choice([0, 1, 5, -3, 10**30 + i, 2**70]), h))
    h304 = {"etag": '"%s"' % op}
    if rnd.random() < 0.3:
        h304["last-modified"] = LM
    if rnd.random() < 0.2:
        h304["x-fresh"] = "yes"
    return inp(st, h304), "strong"


def sc_weak(rnd):
    op = opaque(rnd)
    lm_variants = [LM, "  " + LM, LM + "\t", " \t" + LM + " ", LM2]
    mode = rnd.choice(["etag-only", "lm-only", "both"])
    h304 = {}
    if mode in ("etag-only", "both"):
        h304["etag"] = 'W/"%s"' % op
    if mode in ("lm-only", "both"):
        h304["last-modified"] = rnd.choice(lm_variants[:4])
    n = rnd.randint(0, 4)
    st = []
    for i in range(n):
        h = {"content-type": "text/css"}
        kind = rnd.choice(["etag", "etag", "lm", "both", "strong-same-opaque",
                           "neither", "lm-spaces", "extra"])
        if kind in ("etag", "both", "strong-same-opaque", "extra"):
            h["etag"] = '"%s"' % op if kind == "strong-same-opaque" else (
                'W/"%s"' % op if rnd.random() < 0.7 else '"%s"' % op)
        if kind in ("lm", "both", "lm-spaces", "extra"):
            h["last-modified"] = rnd.choice(lm_variants)
        st.append(stored("s%d" % i, rnd.choice([0, 2, 2, 7, -1, 10**40, 10**40]), h))
    if n >= 2 and rnd.random() < 0.35:
        same = rnd.choice([3, 10**40])
        if mode == "etag-only":
            st = [stored("t0", same, {"etag": 'W/"%s"' % op}),
                  stored("t1", same, {"etag": '"%s"' % op})]
        elif mode == "lm-only":
            st = [stored("t0", same, {"last-modified": LM}),
                  stored("t1", same, {"last-modified": " " + LM + "\t"})]
        else:
            st = [stored("t0", same, {"etag": 'W/"%s"' % op, "last-modified": LM}),
                  stored("t1", same, {"etag": '"%s"' % op, "last-modified": LM})]
        return inp(st, h304), "weak-tie-corresponding"
    if n >= 2 and rnd.random() < 0.25:
        st = [stored("u0", 5, {"etag": 'W/"%s"' % op}),
              stored("u1", 5, {"etag": 'W/"%s"' % opaque(rnd)}),
              stored("u2", 9, {"etag": 'W/"%s"' % op})]
        return inp(st, h304), "weak-tie-off"
    return inp(st, h304), "weak-" + mode


def sc_novalidator(rnd):
    n = rnd.choice([0, 1, 1, 2, 3])
    st = []
    for i in range(n):
        h = {}
        kind = rnd.choice(["bare", "bare", "etag", "lm", "both"])
        if kind in ("etag", "both"):
            h["etag"] = ('W/"%s"' if rnd.random() < 0.5 else '"%s"') % opaque(rnd)
        if kind in ("lm", "both"):
            h["last-modified"] = "Mon, 02 Jan 2034 00:00:00 GMT"
        st.append(stored("s%d" % i, rnd.randint(-5, 9), h))
    return inp(st, {"x-note": "n"}), "no-validator"


def sc_update_fields(rnd):
    op = opaque(rnd)
    st_headers = {"content-type": "text/html", "cache-control": "max-age=60",
                  "x-listed": "stored-kept", "x-unlisted": "stored-old",
                  "Content-Length": "99", "KEEP-ALIVE": "timeout=5",
                  "Proxy-Authorization": "Basic z", "Proxy-Authenticate": "Basic q",
                  "Proxy-Authentication-Info": "x=\"y\"", "x-overwrite": "old",
                  "connection": "x-hop", "x-hop": "stored-hop",
                  "te": "trailers", "transfer-encoding": "chunked",
                  "upgrade": "h2c", "proxy-connection": "keep-alive",
                  "Age": " 3 ", "x-sp": "  v  "}
    h304 = {"etag": '"%s"' % op, "Content-Length": "5", "x-unlisted": "new",
            "X-Overwrite": "new", "x-listed": "conn-dropped",
            "age": rnd.choice(["0", " 5 ", "\t9\t"]), "x-p": "  w  "}
    conn_kind = rnd.choice(["plain", "ows", "excluded", "nonexcl", "empty-members",
                            "mixedcase", "obs-member", "self", "dup", "empty",
                            "spaces-only", "quoted", "semispace"])
    conn = {"plain": "x-listed", "ows": "x-listed , X-Secret",
            "excluded": ",".join(["keep-alive", "te", "upgrade", "proxy-connection",
                                  "transfer-encoding", "proxy-authenticate",
                                  "proxy-authentication-info", "content-length"]),
            "nonexcl": "x-unlisted, server", "empty-members": ",,x-listed,,",
            "mixedcase": "X-LISTED", "obs-member": "x-listed, s%ccret" % 0xe9,
            "self": "connection", "dup": "x-listed, x-listed", "empty": "",
            "spaces-only": "  \t ", "quoted": '"x-listed"',
            "semispace": "x-listed ; x-listed", "nonascii": "x-listed, cafe\u00e9"}[conn_kind]
    if conn is not None:
        h304["connection"] = conn
    if rnd.random() < 0.2:
        h304["keep-alive"] = "timeout=9"
        h304["tE"] = "trailers"
        h304["Transfer-Encoding"] = "chunked"
        h304["Proxy-Authenticate"] = 'Basic realm="x"'
    st = [stored("only", rnd.choice([0, 9, -4]), st_headers)]
    if rnd.random() < 0.3:
        st.append(stored("shadow", 99, {"etag": '"%s"' % op, "x-shadow": "1"}))
    return inp(st, h304), "update-" + conn_kind


def sc_lm_ws(rnd):
    v304 = rnd.choice([LM, " " + LM, LM + "\t", " \t" + LM + "  "])
    variants = [LM, " " + LM, LM + "\t", LM + "  ",
                " \t" + LM + " \t", LM + " x", LM.replace("GMT", "UTC"),
                LM.replace("Tue,  ", "Tue, ")]
    st = [stored("w%d" % i, i, {"last-modified": v, "x-idx": str(i)})
          for i, v in enumerate(variants)]
    return inp(st, {"last-modified": v304}), "lm-whitespace"


def sc_multi_strong(rnd):
    op = opaque(rnd)
    st = [stored("m%d" % i, i, {"etag": '"%s"' % op, "x-order": str(i)})
          for i in range(rnd.randint(2, 4))]
    st.append(stored("weak", 99, {"etag": 'W/"%s"' % op}))
    st.append(stored("off", 50, {"etag": '"%s"' % opaque(rnd)}))
    rnd.shuffle(st)
    return inp(st, {"etag": '"%s"' % op}), "multi-strong"


def sc_refusal(rnd):
    kind = rnd.choice(["json", "nonobject", "topkeys", "respkeys", "status", "storedtype",
                       "elemtype", "id", "recv", "hdrobj", "name", "casedup", "valtype",
                       "crnul", "etag304", "etagstored", "obsname", "rawbytes"])
    base = [stored("s0", 1, {"etag": '"a"', "x-a": "1"})]

    def wrap(st, rh):
        return {"stored": st, "response": {"status": 304, "headers": rh}}

    if kind == "rawbytes":
        payload = rnd.choice([
            b"\xff\xfe", b"\xc3\x28", b"\x80", b"\xc3\xa9", b"not json", b"", b"{",
            b"\xef\xbb\xbf{\"stored\":[],\"response\":{\"status\":304,\"headers\":{}}}",
            b'{"stored":[],"response":{"status":304,"headers":{}}} extra',
            b'{"stored":[],"response":{"status":304,"headers":{}}}\n',
            b'{"stored":[],"response":{"status":304,"headers":{}}}\x00',
            b'  {"stored":[],"response":{"status":304,"headers":{}}}  ',
            b'\x00', b'\x1f\x8b', b'{"stored":\xff}',
        ])
        return ("BYTES", payload), "refusal-rawbytes"
    if kind == "json":
        return ("RAW", rnd.choice(["", "{", "not json", '{"stored":', "[1,2", '{"a":1,}'])), "refusal-json"
    if kind == "nonobject":
        return rnd.choice([[], "x", 5, None, True, [base]]), "refusal-nonobject"
    if kind == "topkeys":
        return (rnd.choice([{"stored": []}, {"response": resp({})},
                {"stored": [], "response": resp({}), "extra": 1}, {}])), "refusal-topkeys"
    if kind == "respkeys":
        return (rnd.choice([{"stored": [], "response": {"status": 304}},
                {"stored": [], "response": {"headers": {}}},
                {"stored": [], "response": {"status": 304, "headers": {}, "x": 1}}])), "refusal-respkeys"
    if kind == "status":
        return ({"stored": [], "response": {"status": rnd.choice(
            [200, 305, "304", 304.0, True, False, None, [304], 30.4]), "headers": {}}}), "refusal-status"
    if kind == "storedtype":
        return (rnd.choice([{"stored": {}, "response": resp({})},
                {"stored": "x", "response": resp({})}, {"stored": 5, "response": resp({})},
                {"stored": None, "response": resp({})}] )), "refusal-storedtype"
    if kind == "elemtype":
        e = rnd.choice([5, "x", None, [], {"id": "a"}, {"id": "a", "received": 1},
                        {"received": 1, "headers": {}}, {"id": "a", "headers": {}, "x": 2}])
        return ({"stored": [e], "response": resp({})}, "refusal-elemtype")
    if kind == "id":
        return (rnd.choice([
            {"stored": [stored("", 1, {})], "response": resp({})},
            {"stored": [stored(5, 1, {})], "response": resp({})},
            {"stored": [stored(None, 1, {})], "response": resp({})},
            {"stored": [stored(True, 1, {})], "response": resp({})},
            {"stored": [stored("a", 1, {}), stored("a", 2, {})], "response": resp({})},
            {"stored": [stored(" ", 1, {})], "response": resp({})},
            {"stored": [stored("a b", 1, {})], "response": resp({})}] )), "refusal-id"
    if kind == "recv":
        return ({"stored": [stored("s0", rnd.choice(
            [True, False, 1.5, "3", None, [1], {}, 304.0, 2**53 + 0.5]), {})],
            "response": resp({})}, "refusal-received")
    if kind == "hdrobj":
        return (rnd.choice([
            {"stored": [], "response": {"status": 304, "headers": []}},
            {"stored": [], "response": {"status": 304, "headers": "x"}},
            {"stored": [], "response": {"status": 304, "headers": 5}},
            {"stored": [], "response": {"status": 304, "headers": True}},
            {"stored": [stored("s0", 1, [])], "response": resp({})},
            {"stored": [stored("s0", 1, None)], "response": resp({})}] )), "refusal-hdrobj"
    if kind == "name":
        nm = rnd.choice(["", "bad name", "bad@name", "a(b)", 'q"uote', "a\tb", "a:b",
                         "a,b", "a/b", "a?b", "a=b", "[x]", "{x}", "x\x7f", "é", "a b"])
        if rnd.random() < 0.5:
            return ({"stored": [], "response": resp({nm: "v"})}, "refusal-name-304")
        return ({"stored": [stored("s0", 1, {nm: "v"})], "response": resp({})}, "refusal-name-stored")
    if kind == "obsname":
        nm = rnd.choice(["%cetag" % 0xe9, "a%cb" % 0x80, "%c" % 0xff])
        return ({"stored": [], "response": resp({nm: "v"})}, "refusal-obsname")
    if kind == "casedup":
        pair = rnd.choice([("ETag", "etag"), ("X-A", "x-a"),
                           ("Last-Modified", "LAST-MODIFIED"), ("Connection", "CoNnEcTiOn")])
        if rnd.random() < 0.5:
            return ({"stored": [], "response": resp({pair[0]: "v", pair[1]: "w"})}, "refusal-casedup-304")
        return ({"stored": [stored("s0", 1, {pair[0]: "v", pair[1]: "w"})],
                 "response": resp({})}, "refusal-casedup-stored")
    if kind == "valtype":
        v = rnd.choice([5, None, True, [], {}, 1.0])
        if rnd.random() < 0.5:
            return ({"stored": [], "response": resp({"x-a": v})}, "refusal-valtype-304")
        return ({"stored": [stored("s0", 1, {"x-a": v})], "response": resp({})}, "refusal-valtype-stored")
    if kind == "crnul":
        v = rnd.choice(["a\rb", "a\nb", "a\x00b", "\r", "\n", "x\x00", "a\rb\x00c"])
        if rnd.random() < 0.5:
            return ({"stored": [], "response": resp({"x-a": v})}, "refusal-crnul-304")
        return ({"stored": [stored("s0", 1, {"x-a": v})], "response": resp({})}, "refusal-crnul-stored")
    if kind == "etag304":
        ev = rnd.choice(["abc", 'w/"a"', "W/", '"a', 'a"', '"a" x', '"a"b', '"a b"', '"a\tb"',
                         '""""', '"', "W", "w/", '"a" , "b"', '"a"x', 'W/ "a"', '"%c"' % 0x7f,
                         '"unclosed', ["a"], '"%c"' % 0x20, ' W/  ', 'W/"a" ', '"é"',
                         '"%s"' % opaque(rnd) + '"', '"\x80"', '"a\\"'])
        return ({"stored": [], "response": resp({"etag": ev})}, "refusal-etag304")
    if kind == "etagstored":
        ev = rnd.choice(["abc", 'w/"a"', '"a b"', '"%c"' % 0x7f, '"a" tail', ["a"], 5,
                         '"%s" "' % opaque(rnd), '"bad', 'W/"x"', '"é"'])
        return ({"stored": [stored("s0", 1, {"etag": ev})],
                 "response": resp({"x-note": "n"})}, "refusal-etagstored")
    raise AssertionError(kind)


def sc_fuzz(rnd):
    n = rnd.randint(0, 3)
    st = []
    for i in range(n):
        h = {}
        for _ in range(rnd.randint(0, 3)):
            h[rnd.choice(TOKEN_PARTS + ["x%d" % rnd.randrange(100)])] = rnd.choice(
                ["v", "  v  ", "ok", opaque(rnd),
                 ('W/"%s"' if rnd.random() < 0.5 else '"%s"') % opaque(rnd), LM])
        st.append(stored("f%d" % i, rnd.choice([0, 1, -1, 2**65, rnd.randint(-9, 9)]), h))
    h304 = {}
    for _ in range(rnd.randint(0, 4)):
        h304[rnd.choice(TOKEN_PARTS + ["x%d" % rnd.randrange(100)])] = rnd.choice(
            ["v", ('W/"%s"' if rnd.random() < 0.5 else '"%s"') % opaque(rnd), LM,
             opaque(rnd), "keep-alive, x-pad", "5", "chunked", "max-age=1, no-cache=z",
             "no-cache", "x-no-cache=1", ",,"])
    return inp(st, h304), "fuzz"


BUILDERS = [(cc_case, 0.40), (sc_strong, 0.12), (sc_weak, 0.12), (sc_novalidator, 0.06),
            (sc_update_fields, 0.10), (sc_lm_ws, 0.04), (sc_multi_strong, 0.03),
            (sc_refusal, 0.08), (sc_fuzz, 0.05)]


def build_corpus():
    rnd = random.Random(SEED)
    corpus = []
    for i in range(N):
        x = rnd.random()
        acc = 0.0
        for builder, w in BUILDERS:
            acc += w
            if x < acc:
                doc, tag = builder(rnd)
                break
        else:
            doc, tag = sc_fuzz(rnd)
        corpus.append((i, doc, tag))
    return corpus


def norm(proc):
    if proc.returncode == 0:
        try:
            return ("OK", json.loads(proc.stdout.decode("utf-8")))
        except Exception as exc:
            return ("BADJSON", "%s:%s" % (exc.__class__.__name__, repr(proc.stdout[:120])))
    out_empty = proc.stdout == b""
    pref = proc.stderr.decode("utf-8", "replace").startswith("invalid_input:")
    return ("ERR", out_empty and pref)


def shape_ok(parsed):
    if parsed is None or parsed[0] != "OK":
        return False
    obj = parsed[1]
    return (isinstance(obj, dict) and set(obj) == {"decision", "rule", "updated"}
            and obj["decision"] in ("update", "must-not-update", "no-update")
            and obj["rule"] in ("strong", "weak", "no-validator")
            and isinstance(obj["updated"], list)
            and all(isinstance(u, dict) and set(u) == {"id", "headers"} for u in obj["updated"]))


def e4_ok(stdout):
    # e4: no leading whitespace, optionally exactly one trailing \n, nothing else.
    if not stdout or stdout != stdout.lstrip(b" \t"):
        return False
    return stdout.count(b"\n") <= 1 and (b"\n" not in stdout or stdout.endswith(b"\n"))


def run_one(case):
    i, doc, tag = case
    if isinstance(doc, tuple) and doc[0] in ("RAW", "BYTES"):
        payload = doc[1].encode("utf-8") if doc[0] == "RAW" else doc[1]
    else:
        payload = json.dumps(doc, ensure_ascii=True).encode("utf-8")
    env = dict(os.environ)
    env["TMPDIR"] = WORK
    t = subprocess.run([sys.executable, "-I", "-B", TWIN], input=payload,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=WORK, env=env)
    o = subprocess.run([sys.executable, "-I", "-B", ORACLE], input=payload,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=WORK, env=env)
    tn, on = norm(t), norm(o)
    if t.returncode == 1 or o.returncode == 1:
        agree = (t.returncode == o.returncode == 1) and tn == ("ERR", True) and on == ("ERR", True)
    else:
        agree = (t.returncode == o.returncode == 0) and tn == on and shape_ok(tn)
        if agree and (not e4_ok(t.stdout) or not e4_ok(o.stdout)):
            agree = False
    return {"i": i, "tag": tag, "input": payload.decode("utf-8", "backslashreplace"),
            "twin_rc": t.returncode, "twin": tn,
            "twin_err": t.stderr.decode("utf-8", "replace")[:200],
            "twin_out": t.stdout[:500].decode("utf-8", "backslashreplace"),
            "oracle_rc": o.returncode, "oracle": on,
            "oracle_err": o.stderr.decode("utf-8", "replace")[:200],
            "oracle_out": o.stdout[:500].decode("utf-8", "backslashreplace"),
            "agree": agree}


def sig(rec):
    def side(which):
        d = rec[which]
        if d[0] == "OK":
            return (0, d[1].get("decision"), d[1].get("rule"), len(d[1].get("updated", [])))
        return (1 if d[0] == "ERR" else 2, None, None, None)
    return (rec["twin_rc"], rec["oracle_rc"], side("twin"), side("oracle"))


def main():
    corpus = build_corpus()
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(run_one, corpus))
    with open(os.path.join(WORK, "results.jsonl"), "w") as fh:
        for rec in results:
            fh.write(json.dumps(rec, ensure_ascii=True) + "\n")
    dis = [r for r in results if not r["agree"]]
    groups = {}
    for r in dis:
        groups.setdefault(sig(r), []).append(r)
    with open(os.path.join(WORK, "groups.txt"), "w") as fh:
        fh.write("n=%d disagreements=%d groups=%d\n" % (len(results), len(dis), len(groups)))
        for gi, (s, members) in enumerate(sorted(groups.items(), key=lambda kv: -len(kv[1]))):
            fh.write("\n=== GROUP %d  n=%d  sig=%s\n" % (gi, len(members), json.dumps(s)))
            for r in members[:200]:
                fh.write("--- case i=%d tag=%s\n" % (r["i"], r["tag"]))
                fh.write("IN: %s\n" % r["input"])
                fh.write("TWIN rc=%s %s err=%s out=%s\n" % (
                    r["twin_rc"], json.dumps(r["twin"], ensure_ascii=True)[:400],
                    r["twin_err"].strip()[:120], r["twin_out"][:200]))
                fh.write("ORAC rc=%s %s err=%s out=%s\n" % (
                    r["oracle_rc"], json.dumps(r["oracle"], ensure_ascii=True)[:400],
                    r["oracle_err"].strip()[:120], r["oracle_out"][:200]))
    tags = {}
    for r in results:
        tags[r["tag"]] = tags.get(r["tag"], 0) + 1
    print("inputs=%d disagreements=%d groups=%d" % (len(results), len(dis), len(groups)))
    print("tag-histogram:", json.dumps(tags, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
