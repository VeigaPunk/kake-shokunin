#!/usr/bin/env python3
"""ExecTwinFresh differential driver: seeded scenario+refusal corpus -> twin vs oracle.

Corpus construction is ours (scenario templates + targeted refusals + token-pool
fuzz); the counter's generator was not read. Compares exit code, parsed stdout
objects (key order free, list order significant) and refusal shape
(empty stdout + stderr prefix "invalid_input:"), never refusal reason text.
"""
import json
import os
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
ORACLE = LANE + "/.ufo/waves/round-99/frozen/pos-oracle.py"
TWIN = LANE + "/.ufo/waves/round-99/w1/ExecTwinFresh/twin.py"
WORK = "/fast/scratch/hyaku/kake-r99/ExecTwinFresh"

SEED = 99226
N = 2400

# opaque alphabet: `!`, #..~ (no space 0x20, no quote 0x22, no DEL 0x7f), obs-text
OPAQUE_CHARS = ["!"] + [chr(c) for c in range(0x23, 0x7F)] + [chr(c) for c in range(0x80, 0x100)]
TOKEN_PARTS = ["x-a", "etag", "ETag", "last-modified", "Last-Modified", "cache-control",
               "Cache-Control", "connection", "Connection", "content-length", "keep-alive",
               "TE", "transfer-encoding", "upgrade", "proxy-authenticate", "x-secret",
               "X-Secret", "age", "date", "server", "x-pad", "x-listed"]


def opaque(rnd, k=None):
    k = k if k is not None else rnd.randint(0, 8)
    return "".join(rnd.choice(OPAQUE_CHARS) for _ in range(k))


def etag(rnd, weak=False, op=None):
    return ('W/"%s"' if weak else '"%s"') % (op if op is not None else opaque(rnd))


def stored(id_, received, headers):
    return {"id": id_, "received": received, "headers": headers}


def resp(headers, status=304):
    return {"status": status, "headers": headers}


def inp(stored_list, r_headers, status=304):
    return {"stored": stored_list, "response": resp(r_headers, status)}


# ---------------- scenario classes (each returns (input, tag)) ----------------

def sc_strong(rnd):
    op = opaque(rnd)
    others = [opaque(rnd) for _ in range(rnd.randint(0, 2))]
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
            h["etag"] = '"%s"' % (others[rnd.randrange(len(others))] if others else opaque(rnd))
        elif kind == "other-weak":
            h["etag"] = 'W/"%s"' % (others[rnd.randrange(len(others))] if others else opaque(rnd))
        elif kind == "case-variant":
            # char-for-char means case-sensitive: probe upper/lower variants
            h["etag"] = '"%s"' % (op.upper() if rnd.random() < 0.5 else op.lower())
        elif kind == "no-etag":
            h["last-modified"] = "Tue, 01 Jan 2035 00:00:00 GMT"
        st.append(stored("s%d" % i, rnd.choice([0, 1, 5, -3, 10**30 + i, 2**70]), h))
    h304 = {"etag": '"%s"' % op}
    if rnd.random() < 0.3:
        h304["last-modified"] = "Tue, 01 Jan 2035 00:00:00 GMT"  # ignored for selection
    if rnd.random() < 0.2:
        h304["x-fresh"] = "yes"
    return inp(st, h304), "strong"


def sc_weak(rnd):
    op = opaque(rnd)
    lm = "Tue, 01 Jan 2035 00:00:00 GMT"
    lm_variants = [lm, "  " + lm, lm + "\t", " \t" + lm + " ", lm.replace("01", "02")]
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
                           "neither", "lm-spaces", "extra-validators"])
        if kind in ("etag", "both", "strong-same-opaque", "extra-validators"):
            if kind == "strong-same-opaque":
                h["etag"] = '"%s"' % op          # strong stored matches weakly
            else:
                h["etag"] = 'W/"%s"' % op if rnd.random() < 0.7 else '"%s"' % op
        if kind in ("lm", "both", "lm-spaces", "extra-validators"):
            h["last-modified"] = rnd.choice(lm_variants)
        if kind == "neither":
            h["x-only"] = "1"
        st.append(stored("s%d" % i, rnd.choice([0, 2, 2, 7, -1, 10**40, 10**40]), h))
    tag = "weak-" + mode
    # targeted: ties among corresponding (LC3) vs ties off-correspondence
    if n >= 2 and rnd.random() < 0.35:
        same_recv = rnd.choice([3, 10**40])
        if mode == "etag-only":
            st = [stored("t0", same_recv, {"etag": 'W/"%s"' % op}),
                  stored("t1", same_recv, {"etag": '"%s"' % op})]
        elif mode == "lm-only":
            st = [stored("t0", same_recv, {"last-modified": lm}),
                  stored("t1", same_recv, {"last-modified": " " + lm + "\t"})]
        else:
            st = [stored("t0", same_recv, {"etag": 'W/"%s"' % op, "last-modified": lm}),
                  stored("t1", same_recv, {"etag": '"%s"' % op, "last-modified": lm})]
        tag = "weak-tie-corresponding"
    elif n >= 2 and rnd.random() < 0.25:
        st = [stored("u0", 5, {"etag": 'W/"%s"' % op}),
              stored("u1", 5, {"etag": 'W/"%s"' % opaque(rnd)}),
              stored("u2", 9, {"etag": 'W/"%s"' % op})]
        tag = "weak-tie-off"
    return inp(st, h304), tag


def sc_novalidator(rnd):
    n = rnd.choice([0, 1, 1, 2, 3])
    st = []
    for i in range(n):
        h = {}
        kind = rnd.choice(["bare", "bare", "etag", "lm", "both"])
        if kind in ("etag", "both"):
            h["etag"] = etag(rnd, weak=rnd.random() < 0.5)
        if kind in ("lm", "both"):
            h["last-modified"] = "Mon, 02 Jan 2034 00:00:00 GMT"
        st.append(stored("s%d" % i, rnd.randint(-5, 9), h))
    return inp(st, {"x-note": "n"}), "no-validator"


def sc_update_fields(rnd):
    op = opaque(rnd)
    st_headers = {"content-type": "text/html", "cache-control": "max-age=60",
                  "x-listed": "stored-kept", "x-unlisted": "stored-old",
                  "Content-Length": "99", "KEEP-ALIVE": "timeout=5",
                  "Proxy-Authorization": "Basic z", "x-overwrite": "old"}
    h304 = {"etag": '"%s"' % op,
            "Content-Length": "5",
            "x-unlisted": "new",
            "X-Overwrite": "new",
            "x-listed": "conn-dropped",
            "age": "0"}
    conn_kind = rnd.choice(["plain", "ows", "excluded", "nonexcluded", "empty-members",
                            "mixedcase", "obs-member", "self", "dup"])
    conn = {"plain": "x-listed",
            "ows": "x-listed , X-Secret",
            "excluded": ",".join(["keep-alive", "te", "upgrade", "proxy-connection",
                                  "transfer-encoding", "proxy-authenticate",
                                  "proxy-authentication-info", "content-length"]),
            "nonexcluded": "x-unlisted, server",
            "empty-members": ",,x-listed,,",
            "mixedcase": "X-LISTED",
            "obs-member": "x-listed, s%ccret" % 0xe9,
            "self": "connection",
            "dup": "x-listed, x-listed"}[conn_kind]
    if conn is not None:
        h304["connection"] = conn
    if rnd.random() < 0.25:
        h304["Cache-Control"] = rnd.choice(
            ["max-age=60", "no-cache", "private", "no-cache=x",
             'no-cache="f"', 'max-age=5, private="g"', 'NO-CACHE="x"', 'Private="g"'])
    if rnd.random() < 0.2:
        h304["keep-alive"] = "timeout=9"
        h304["tE"] = "trailers"
        h304["Transfer-Encoding"] = "chunked"
        h304["Upgrade"] = "h2c"
        h304["Proxy-Authenticate"] = 'Basic realm="x"'
        h304["Proxy-Authentication-Info"] = "next"
    if rnd.random() < 0.15:
        h304["Authentication-Info"] = "ok"   # NOT on the never-copy list
    # stored response identified via strong etag always -> update path
    st = [stored("only", rnd.choice([0, 9, -4]), st_headers)]
    if rnd.random() < 0.3:
        st.append(stored("shadow", 99, {"etag": '"%s"' % op, "x-shadow": "1"}))
    return inp(st, h304), "update-" + conn_kind


def sc_lm_whitespace(rnd):
    lm_core = "Tue, 01 Jan 2035 00:00:00 GMT"
    v304 = rnd.choice([lm_core, " " + lm_core, lm_core + "\t", " \t" + lm_core + "  "])
    st = []
    for i, v in enumerate([lm_core, " " + lm_core, lm_core + "\t", lm_core + "  ",
                           " \t" + lm_core + " \t", lm_core + " x", lm_core.replace("GMT", "UTC"),
                           lm_core.replace("  ", " ") if "  " in lm_core else lm_core + "\t\t"]):
        st.append(stored("w%d" % i, i, {"last-modified": v, "x-idx": str(i)}))
    return inp(st, {"last-modified": v304}), "lm-whitespace"


# ---------------- refusal class ----------------

def sc_refusal(rnd):
    kind = rnd.choice(["json", "nonobject", "topkeys", "respkeys", "status", "storedtype",
                       "elemtype", "id", "recv", "hdrobj", "name", "casedup", "valtype",
                       "crnul", "etag304", "etagstored", "lc6", "obsname"])
    base_st = [stored("s0", 1, {"etag": '"a"', "x-a": "1"})]

    def wrap(st, rh):
        return {"stored": st, "response": {"status": 304, "headers": rh}}

    if kind == "json":
        raw = rnd.choice(["", "{", "not json", '{"stored":', "[1,2", '{"a":1,}'])
        return ("RAW", raw), "refusal-json"
    if kind == "nonobject":
        doc = rnd.choice([[], "x", 5, None, True, [base_st]])
        return doc, "refusal-nonobject"
    if kind == "topkeys":
        doc = rnd.choice([{"stored": []},
                          {"response": resp({})},
                          {"stored": [], "response": resp({}), "extra": 1},
                          {}])
        return doc, "refusal-topkeys"
    if kind == "respkeys":
        doc = rnd.choice([{"stored": [], "response": {"status": 304}},
                          {"stored": [], "response": {"headers": {}}},
                          {"stored": [], "response": {"status": 304, "headers": {}, "x": 1}}])
        return doc, "refusal-respkeys"
    if kind == "status":
        s = rnd.choice([200, 305, "304", 304.0, True, False, None, [304], {"s": 304}, 30.4])
        return {"stored": [], "response": {"status": s, "headers": {}}}, "refusal-status"
    if kind == "storedtype":
        doc = rnd.choice([{"stored": {}, "response": resp({})},
                          {"stored": "x", "response": resp({})},
                          {"stored": 5, "response": resp({})},
                          {"stored": None, "response": resp({})}])
        return doc, "refusal-storedtype"
    if kind == "elemtype":
        e = rnd.choice([5, "x", None, [], {"id": "a"}, {"id": "a", "received": 1},
                        {"received": 1, "headers": {}}, {"id": "a", "headers": {}, "x": 2}])
        return {"stored": [e], "response": resp({})}, "refusal-elemtype"
    if kind == "id":
        doc = rnd.choice([
            {"stored": [stored("", 1, {})], "response": resp({})},
            {"stored": [stored(5, 1, {})], "response": resp({})},
            {"stored": [stored(None, 1, {})], "response": resp({})},
            {"stored": [stored(True, 1, {})], "response": resp({})},
            {"stored": [stored("a", 1, {}), stored("a", 2, {})], "response": resp({})},
            {"stored": [stored("a b", 1, {})], "response": resp({})},   # valid (non-empty str)
        ])
        return doc, "refusal-id"
    if kind == "recv":
        r = rnd.choice([True, False, 1.5, "3", None, [1], {}, 304.0, 2**53 + 0.5])
        return {"stored": [stored("s0", r, {})], "response": resp({})}, "refusal-received"
    if kind == "hdrobj":
        doc = rnd.choice([
            {"stored": [], "response": {"status": 304, "headers": []}},
            {"stored": [], "response": {"status": 304, "headers": "x"}},
            {"stored": [], "response": {"status": 304, "headers": 5}},
            {"stored": [], "response": {"status": 304, "headers": True}},
            {"stored": [stored("s0", 1, [])], "response": resp({})},
            {"stored": [stored("s0", 1, None)], "response": resp({})},
        ])
        return doc, "refusal-hdrobj"
    if kind == "name":
        nm = rnd.choice(["", "bad name", "bad@name", "a(b)", 'q"uote', "a\tb", "a:b",
                         "a,b", "a/b", "a?b", "a=b", "[x]", "{x}", "x\x7f"])
        where = rnd.random()
        if where < 0.5:
            return {"stored": [], "response": resp({nm: "v"})}, "refusal-name-304"
        return {"stored": [stored("s0", 1, {nm: "v"})], "response": resp({})}, "refusal-name-stored"
    if kind == "obsname":
        nm = rnd.choice(["%cetag" % 0xe9, "a%cb" % 0x80, "%c" % 0xff])
        return {"stored": [], "response": resp({nm: "v"})}, "refusal-obsname"
    if kind == "casedup":
        pair = rnd.choice([("ETag", "etag"), ("X-A", "x-a"), ("Last-Modified", "LAST-MODIFIED"),
                           ("Connection", "CoNnEcTiOn")])
        if rnd.random() < 0.5:
            return {"stored": [], "response": resp({pair[0]: "v", pair[1]: "w"})}, "refusal-casedup-304"
        return {"stored": [stored("s0", 1, {pair[0]: "v", pair[1]: "w"})],
                "response": resp({})}, "refusal-casedup-stored"
    if kind == "valtype":
        v = rnd.choice([5, None, True, [], {}, 1.0])
        if rnd.random() < 0.5:
            return {"stored": [], "response": resp({"x-a": v})}, "refusal-valtype-304"
        return {"stored": [stored("s0", 1, {"x-a": v})], "response": resp({})}, "refusal-valtype-stored"
    if kind == "crnul":
        v = rnd.choice(["a\rb", "a\nb", "a\x00b", "\r", "\n", "x\x00"])
        if rnd.random() < 0.5:
            return {"stored": [], "response": resp({"x-a": v})}, "refusal-crnul-304"
        return {"stored": [stored("s0", 1, {"x-a": v})], "response": resp({})}, "refusal-crnul-stored"
    if kind == "etag304":
        ev = rnd.choice(["abc", 'w/"a"', "W/", '"a', 'a"', '"a" x', '"a"b', '"a b"', '"a\tb"',
                         '""""', '"', "W", "w/", '"a" , "b"', '"a"x', 'W/ "a"', '"%c"' % 0x7f,
                         '"unclosed', ["a"], '"%c"' % 0x20, ' W/  ', 'W/"a" ' + " ",
                         '"%s"' % opaque(rnd) + '"'])
        return {"stored": [], "response": resp({"etag": ev})}, "refusal-etag304"
    if kind == "etagstored":
        ev = rnd.choice(["abc", 'w/"a"', '"a b"', '"%c"' % 0x7f, '"a" tail', ["a"], 5,
                         '"%s" "' % opaque(rnd)])
        return {"stored": [stored("s0", 1, {"etag": ev})],
                "response": resp({"x-note": "n"})}, "refusal-etagstored"
    if kind == "lc6":
        cc = rnd.choice(['no-cache="x"', 'private="g"', 'max-age=5, no-cache="f"',
                         'NO-CACHE="x"', 'Private="g"', 'no-cache="x', 'private="',
                         "no-cache=", "private", "no-cache"])
        if rnd.random() < 0.15:
            # LC6 governs the 304 only: stored qualified cc must be ACCEPTED
            return {"stored": [stored("s0", 1, {"cache-control": 'no-cache="x"',
                                                "etag": '"%s"' % opaque(rnd)})],
                    "response": resp({"etag": '"%s"' % opaque(rnd)})}, "lc6-stored-only"
        return {"stored": base_st, "response": resp({"etag": '"%s"' % opaque(rnd),
                                                     "cache-control": cc})}, "refusal-lc6"
    raise AssertionError(kind)


def sc_fuzz(rnd):
    n = rnd.randint(0, 3)
    st = []
    for i in range(n):
        h = {}
        for _ in range(rnd.randint(0, 3)):
            h[rnd.choice(TOKEN_PARTS + ["x%d" % rnd.randrange(100)])] = rnd.choice(
                ["v", "  v  ", "a\rb" if rnd.random() < 0.03 else "ok",
                 opaque(rnd), etag(rnd, rnd.random() < 0.5), "Tue, 01 Jan 2035 00:00:00 GMT"])
        st.append(stored("f%d" % i, rnd.choice([0, 1, -1, 2**65, rnd.randint(-9, 9)]), h))
    h304 = {}
    for _ in range(rnd.randint(0, 4)):
        name = rnd.choice(TOKEN_PARTS + ["x%d" % rnd.randrange(100)])
        val = rnd.choice(["v", etag(rnd, rnd.random() < 0.5), "Tue, 01 Jan 2035 00:00:00 GMT",
                          opaque(rnd), "keep-alive, x-pad", "5", "chunked"])
        h304[name] = val
    return inp(st, h304), "fuzz"


def sc_multi_strong(rnd):
    # multiple matching strong etags: update lists every match in input order
    op = opaque(rnd)
    st = [stored("m%d" % i, i, {"etag": '"%s"' % op, "x-order": str(i)}) for i in range(rnd.randint(2, 4))]
    st.append(stored("weak", 99, {"etag": 'W/"%s"' % op}))
    st.append(stored("off", 50, {"etag": '"%s"' % opaque(rnd)}))
    rnd.shuffle(st)
    return inp(st, {"etag": '"%s"' % op}), "multi-strong"


BUILDERS = [(sc_strong, 0.20), (sc_weak, 0.20), (sc_novalidator, 0.10),
            (sc_update_fields, 0.15), (sc_lm_whitespace, 0.05),
            (sc_multi_strong, 0.05), (sc_refusal, 0.15), (sc_fuzz, 0.10)]


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


# ---------------- differential execution ----------------

def norm(proc):
    if proc.returncode == 0:
        try:
            return ("OK", json.loads(proc.stdout.decode("utf-8")))
        except Exception as exc:
            return ("BADJSON", "%s:%s" % (exc.__class__.__name__, proc.stdout[:120]))
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


def run_one(case):
    i, doc, tag = case
    if isinstance(doc, tuple) and doc[0] == "RAW":
        payload = doc[1].encode("utf-8")
    else:
        payload = json.dumps(doc, ensure_ascii=True).encode("utf-8")
    env = dict(os.environ)
    env["TMPDIR"] = WORK
    t = subprocess.run([sys.executable, "-B", TWIN], input=payload,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=WORK, env=env)
    o = subprocess.run([sys.executable, "-B", ORACLE], input=payload,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=WORK, env=env)
    tn, on = norm(t), norm(o)
    if t.returncode == 1 or o.returncode == 1:
        agree = (t.returncode == o.returncode == 1) and tn == ("ERR", True) and on == ("ERR", True)
    else:
        agree = (t.returncode == o.returncode == 0) and tn == on and shape_ok(tn)
    return {"i": i, "tag": tag,
            "input": payload.decode("utf-8", "backslashreplace"),
            "twin_rc": t.returncode, "twin": tn,
            "twin_err": t.stderr.decode("utf-8", "replace")[:200],
            "oracle_rc": o.returncode, "oracle": on,
            "oracle_err": o.stderr.decode("utf-8", "replace")[:200],
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
                fh.write("TWIN rc=%s %s err=%s\n" % (r["twin_rc"], json.dumps(r["twin"], ensure_ascii=True)[:400], r["twin_err"].strip()[:120]))
                fh.write("ORAC rc=%s %s err=%s\n" % (r["oracle_rc"], json.dumps(r["oracle"], ensure_ascii=True)[:400], r["oracle_err"].strip()[:120]))

    tags = {}
    for r in results:
        tags[r["tag"]] = tags.get(r["tag"], 0) + 1
    print("inputs=%d disagreements=%d groups=%d" % (len(results), len(dis), len(groups)))
    print("tag-histogram:", json.dumps(tags, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
