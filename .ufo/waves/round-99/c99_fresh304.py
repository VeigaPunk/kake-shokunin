#!/usr/bin/env python3
"""Round-99 C2 counter: 304 freshening contract v1 (.ufo/waves/round-99/fresh304-contract.md).

Scores candidate scripts/freshen_304.py read from COMMITTED bytes at --revision
(git show), or a --candidate-file (controls only). Each case runs the candidate
once: `python3 -I -B <candidate>` in a fresh scratch cwd under --work, stdin =
case JSON, minimal env (PATH, LANG, HOME/TMPDIR = scratch), timeout 10 s.

A case passes when:
  expected decision -> exit 0, stdout is one JSON object equal to the expected
                       object (dict key order ignored; list order scored);
  expected refusal  -> exit 1, stdout empty, stderr starts with `invalid_input:`.

Populations:
  hand      the HAND list below (written from the contract, each tagged with the
            clause it decides); the reference must agree with every hand
            expectation before any candidate runs (exit 2 on drift);
  generated N cases (default 240) from a grammar seeded by --seed or, by
            default, by int(first 8 hex of the scored revision id, 16) -- so a
            table keyed on committed cases cannot pass.

Output line:
  candidate=<absent|present> sha256=<hex> hand=a/b generated=c/d refusals=e/f seed=S met=<bool>
met=true iff candidate present and every hand and generated case passes.
Exit 0 met; 1 not met or candidate absent; 2 could-not-evaluate / usage / drift.
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

CANDIDATE = "scripts/freshen_304.py"
TCHAR = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
HOP = {"keep-alive", "proxy-connection", "te", "transfer-encoding", "upgrade"}
PROXY = {"proxy-authenticate", "proxy-authentication-info", "proxy-authorization"}


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
        if any(c in v for c in "\r\n\x00"):
            raise Refuse("CR/LF/NUL in value")
        out[lk] = v
    return out


def _etag(v):
    """Return (weak, opaque) or raise."""
    s = v.strip(" \t")
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
        lm = sh["last-modified"].strip(" \t") if "last-modified" in sh else None
        norm.append((el["id"], el["received"], sh, et, lm))
    ret = _etag(rh["etag"]) if "etag" in rh else None
    rlm = rh["last-modified"].strip(" \t") if "last-modified" in rh else None
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
            m = m.strip(" \t").lower()
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


def ref_or_refusal(inp):
    try:
        return reference(inp)
    except Refuse:
        return None


def S(i, rec, **h):
    return {"id": i, "received": rec, "headers": {k.replace("_", "-"): v for k, v in h.items()}}


def R(**h):
    return {"status": 304, "headers": {k.replace("_", "-"): v for k, v in h.items()}}


def U(i, **h):
    return {"id": i, "headers": {k.replace("_", "-").lower(): v for k, v in h.items()}}


# (tag, input, expected-object or None for refusal)
HAND = [
    ("strong-1", {"stored": [S("a", 1, ETag='"x"', Cache_Control="max-age=10")], "response": R(ETag='"x"', Cache_Control="max-age=60")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', cache_control="max-age=60")]}),
    ("strong-all-matching", {"stored": [S("a", 1, ETag='"x"'), S("b", 2, ETag='"y"'), S("c", 3, ETag='"x"')], "response": R(ETag='"x"', Expires="E")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', expires="E"), U("c", etag='"x"', expires="E")]}),
    ("strong-none-mustnot", {"stored": [S("a", 1, ETag='"y"')], "response": R(ETag='"x"')},
     {"decision": "must-not-update", "rule": "strong", "updated": []}),
    ("strong-vs-weak-stored", {"stored": [S("a", 1, ETag='W/"x"')], "response": R(ETag='"x"')},
     {"decision": "must-not-update", "rule": "strong", "updated": []}),
    ("strong-ignores-lm", {"stored": [S("a", 1, ETag='"x"', Last_Modified="L1")], "response": R(ETag='"x"', Last_Modified="L2")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', last_modified="L2")]}),
    ("strong-empty-set", {"stored": [], "response": R(ETag='"x"')},
     {"decision": "must-not-update", "rule": "strong", "updated": []}),
    ("strong-case-sensitive", {"stored": [S("a", 1, ETag='"X"')], "response": R(ETag='"x"')},
     {"decision": "must-not-update", "rule": "strong", "updated": []}),
    ("strong-trim", {"stored": [S("a", 1, ETag=' "x" ')], "response": R(ETag='"x"\t')},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"\t')]}),
    ("strong-empty-opaque", {"stored": [S("a", 1, ETag='""')], "response": R(ETag='""')},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='""')]}),
    ("weak-etag-most-recent", {"stored": [S("a", 5, ETag='W/"x"'), S("b", 9, ETag='"x"'), S("c", 7, ETag='W/"x"')], "response": R(ETag='W/"x"')},
     {"decision": "update", "rule": "weak", "updated": [U("b", etag='W/"x"')]}),
    ("weak-etag-none", {"stored": [S("a", 5, ETag='W/"y"')], "response": R(ETag='W/"x"')},
     {"decision": "no-update", "rule": "weak", "updated": []}),
    ("weak-lm-only", {"stored": [S("a", 1, Last_Modified="Mon"), S("b", 2, Last_Modified="Tue")], "response": R(Last_Modified="Mon")},
     {"decision": "update", "rule": "weak", "updated": [U("a", last_modified="Mon")]}),
    ("weak-lm-trim", {"stored": [S("a", 1, Last_Modified=" Mon ")], "response": R(Last_Modified="Mon")},
     {"decision": "update", "rule": "weak", "updated": [U("a", last_modified="Mon")]}),
    ("weak-both-need-both", {"stored": [S("a", 3, ETag='W/"x"'), S("b", 2, ETag='W/"x"', Last_Modified="L")], "response": R(ETag='W/"x"', Last_Modified="L")},
     {"decision": "update", "rule": "weak", "updated": [U("b", etag='W/"x"', last_modified="L")]}),
    ("weak-tie-refused", {"stored": [S("a", 4, ETag='W/"x"'), S("b", 4, ETag='W/"x"')], "response": R(ETag='W/"x"')}, None),
    ("weak-tie-below-top-ok", {"stored": [S("a", 4, ETag='W/"x"'), S("b", 4, ETag='W/"x"'), S("c", 6, ETag='W/"x"')], "response": R(ETag='W/"x"')},
     {"decision": "update", "rule": "weak", "updated": [U("c", etag='W/"x"')]}),
    ("weak-lm-stored-lacks", {"stored": [S("a", 1, ETag='"q"')], "response": R(Last_Modified="L")},
     {"decision": "no-update", "rule": "weak", "updated": []}),
    ("weak-negative-received", {"stored": [S("a", -5, Last_Modified="L"), S("b", -9, Last_Modified="L")], "response": R(Last_Modified="L")},
     {"decision": "update", "rule": "weak", "updated": [U("a", last_modified="L")]}),
    ("noval-single", {"stored": [S("a", 1, Cache_Control="max-age=1")], "response": R(Cache_Control="max-age=99")},
     {"decision": "update", "rule": "no-validator", "updated": [U("a", cache_control="max-age=99")]}),
    ("noval-two", {"stored": [S("a", 1), S("b", 2)], "response": R(Expires="E")},
     {"decision": "no-update", "rule": "no-validator", "updated": []}),
    ("noval-stored-has-etag", {"stored": [S("a", 1, ETag='"x"')], "response": R(Expires="E")},
     {"decision": "no-update", "rule": "no-validator", "updated": []}),
    ("noval-stored-has-lm", {"stored": [S("a", 1, Last_Modified="L")], "response": R()},
     {"decision": "no-update", "rule": "no-validator", "updated": []}),
    ("noval-empty", {"stored": [], "response": R()},
     {"decision": "no-update", "rule": "no-validator", "updated": []}),
    ("upd-content-length", {"stored": [S("a", 1, ETag='"x"', Content_Length="10")], "response": R(ETag='"x"', Content_Length="0")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', content_length="10")]}),
    ("upd-connection-listed", {"stored": [S("a", 1, ETag='"x"', X_Foo="old")], "response": R(ETag='"x"', Connection="X-Foo, , close", X_Foo="new", X_Bar="b")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', x_foo="old", x_bar="b")]}),
    ("upd-hop-fixed", {"stored": [S("a", 1, ETag='"x"')], "response": R(ETag='"x"', Keep_Alive="t", TE="x", Transfer_Encoding="chunked", Upgrade="u", Proxy_Connection="p")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"')]}),
    ("upd-proxy-fields", {"stored": [S("a", 1, ETag='"x"')], "response": R(ETag='"x"', Proxy_Authenticate="B", Proxy_Authentication_Info="i", Proxy_Authorization="z", Vary="x")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', vary="x")]}),
    ("upd-case-merge", {"stored": [S("a", 1, ETag='"x"', CACHE_CONTROL="old")], "response": R(ETag='"x"', cache_control="new")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', cache_control="new")]}),
    ("upd-value-bytes-kept", {"stored": [S("a", 1, ETag='"x"')], "response": R(ETag='"x"', X_V="  spaced\tvalue ")},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"x"', x_v="  spaced\tvalue ")]}),
    ("upd-connection-self-case", {"stored": [S("a", 1)], "response": R(CONNECTION="keep-alive", Date="D")},
     {"decision": "update", "rule": "no-validator", "updated": [U("a", date="D")]}),
    ("upd-obs-text-etag", {"stored": [S("a", 1, ETag='"\u00e9"')], "response": R(ETag='"\u00e9"')},
     {"decision": "update", "rule": "strong", "updated": [U("a", etag='"\u00e9"')]}),
    ("ref-status-200", {"stored": [], "response": {"status": 200, "headers": {}}}, None),
    ("ref-status-bool", {"stored": [], "response": {"status": True, "headers": {}}}, None),
    ("ref-extra-key", {"stored": [], "response": R(), "now": 1}, None),
    ("ref-dup-id", {"stored": [S("a", 1), S("a", 2)], "response": R()}, None),
    ("ref-empty-id", {"stored": [S("", 1)], "response": R()}, None),
    ("ref-received-bool", {"stored": [S("a", True)], "response": R()}, None),
    ("ref-received-float", {"stored": [S("a", 1.0)], "response": R()}, None),
    ("ref-bad-name", {"stored": [], "response": {"status": 304, "headers": {"bad name": "v"}}}, None),
    ("ref-case-dup", {"stored": [], "response": {"status": 304, "headers": {"ETag": '"x"', "etag": '"x"'}}}, None),
    ("ref-crlf", {"stored": [S("a", 1, X="a\r\nb")], "response": R()}, None),
    ("ref-nonstring", {"stored": [], "response": {"status": 304, "headers": {"x": 5}}}, None),
    ("ref-etag-list", {"stored": [], "response": R(ETag='"a", "b"')}, None),
    ("ref-etag-unquoted", {"stored": [S("a", 1, ETag="abc")], "response": R()}, None),
    ("ref-etag-lower-w", {"stored": [], "response": R(ETag='w/"x"')}, None),
    ("ref-etag-dquote-inside", {"stored": [], "response": R(ETag='"a"b"')}, None),
    ("ref-qualified-nocache", {"stored": [S("a", 1)], "response": R(Cache_Control='no-cache="set-cookie"')}, None),
    ("ref-qualified-private", {"stored": [S("a", 1)], "response": R(Cache_Control='max-age=1, PRIVATE="x"')}, None),
    ("ref-stored-not-list", {"stored": {}, "response": R()}, None),
    ("ref-not-object", [], None),
]


def gen_case(rng):
    pool_tags = ['"a"', '"b"', 'W/"a"', 'W/"b"', '""', '"\u00e9"']
    lms = ["L1", "L2", " L1"]
    bad = rng.random() < 0.12
    n = rng.randint(0, 4)
    stored = []
    for k in range(n):
        h = {}
        if rng.random() < 0.6:
            h["ETag" if rng.random() < 0.5 else "etag"] = rng.choice(pool_tags)
        if rng.random() < 0.4:
            h["Last-Modified"] = rng.choice(lms)
        if rng.random() < 0.5:
            h["Content-Length"] = str(rng.randint(0, 99))
        if rng.random() < 0.5:
            h["Cache-Control"] = "max-age=%d" % rng.randint(0, 9)
        if rng.random() < 0.3:
            h["X-Foo"] = "s%d" % k
        stored.append({"id": "s%d" % k, "received": rng.randint(-3, 6), "headers": h})
    rh = {}
    if rng.random() < 0.7:
        rh["ETag"] = rng.choice(pool_tags)
    if rng.random() < 0.4:
        rh["last-modified"] = rng.choice(lms)
    for name in ["Content-Length", "Cache-Control", "X-Foo", "Keep-Alive", "Transfer-Encoding",
                 "Proxy-Authenticate", "Expires", "Upgrade", "TE"]:
        if rng.random() < 0.25:
            rh[name] = "r-%s" % rng.randint(0, 9)
    if rng.random() < 0.25:
        rh["Connection"] = rng.choice(["X-Foo", "close", "expires, ,x-foo", "Cache-Control"])
    inp = {"stored": stored, "response": {"status": 304, "headers": rh}}
    if bad:
        kind = rng.randint(0, 6)
        if kind == 0:
            inp["response"]["status"] = rng.choice([200, 412, "304"])
        elif kind == 1:
            inp["response"]["headers"]["ETag"] = rng.choice(['x', '"a', 'w/"a"', '"a","b"'])
            inp["response"]["headers"].pop("etag", None)
        elif kind == 2 and stored:
            stored[0]["received"] = rng.choice([1.5, True, "1"])
        elif kind == 3 and len(stored) >= 1:
            stored.append({"id": stored[0]["id"], "received": 0, "headers": {}})
        elif kind == 4:
            inp["response"]["headers"]["X-Bad"] = "a\nb"
        elif kind == 5:
            inp["response"]["headers"]["Cache-Control"] = 'no-cache="x"'
        else:
            inp["extra"] = 1
    return inp


def run_candidate(path, inp, work, k):
    d = os.path.join(work, "case-%d" % k)
    os.makedirs(d)
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C.UTF-8", "HOME": d, "TMPDIR": d}
    try:
        r = subprocess.run([sys.executable, "-I", "-B", path], input=json.dumps(inp).encode(),
                           capture_output=True, cwd=d, env=env, timeout=10)
        res = (r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace"))
    except subprocess.TimeoutExpired:
        res = (124, "", "")
    shutil.rmtree(d, ignore_errors=True)
    return res


def judge(expected, res):
    rc, out, err = res
    if expected is None:
        return rc == 1 and out.strip() == "" and err.startswith("invalid_input:")
    if rc != 0:
        return False
    try:
        obj = json.loads(out)
    except ValueError:
        return False
    return obj == expected


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--generated", type=int, default=240)
    ap.add_argument("--candidate-file")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    # reference vs hand expectations (drift check) - always first
    drift = [t for t, inp, exp in HAND if ref_or_refusal(inp) != exp]
    if drift:
        print("could-not-evaluate: reference drift on %s" % ",".join(drift), file=sys.stderr)
        return 2
    if a.selftest:
        rng = random.Random(9999)
        kinds = {}
        for _ in range(2000):
            r = ref_or_refusal(gen_case(rng))
            key = "refusal" if r is None else r["decision"] + "/" + r["rule"]
            kinds[key] = kinds.get(key, 0) + 1
        need = {"refusal", "update/strong", "must-not-update/strong", "update/weak", "no-update/weak",
                "update/no-validator", "no-update/no-validator"}
        ok = need.issubset(kinds)
        print("hand=%d/%d reference agrees; generated classes %s" % (len(HAND), len(HAND), json.dumps(kinds, sort_keys=True)))
        print("selftest %d/2" % (1 + ok))
        return 0 if ok else 1
    if not a.work or (not a.revision and not a.candidate_file):
        print("usage: --work <scratch> and --revision <rev> (or --candidate-file) required", file=sys.stderr)
        return 2
    os.makedirs(a.work, exist_ok=True)
    w = tempfile.mkdtemp(dir=a.work, prefix="c99f-")
    try:
        rev = None
        if a.revision:
            r = subprocess.run(["git", "-C", a.root, "rev-parse", "--verify", a.revision + "^{commit}"], capture_output=True)
            if r.returncode != 0:
                print("could-not-evaluate: unresolvable revision", file=sys.stderr)
                return 2
            rev = r.stdout.decode().strip()
        if a.candidate_file:
            data = open(a.candidate_file, "rb").read()
        else:
            r = subprocess.run(["git", "-C", a.root, "show", "%s:%s" % (rev, CANDIDATE)], capture_output=True)
            if r.returncode != 0:
                print("revision=%s candidate=absent met=false" % rev)
                return 1
            data = r.stdout
        cand = os.path.join(w, "freshen_304.py")
        open(cand, "wb").write(data)
        sha = hashlib.sha256(data).hexdigest()
        seed = a.seed if a.seed is not None else (int(rev[:8], 16) if rev else 99099)
        rng = random.Random(seed)
        gen = [gen_case(rng) for _ in range(a.generated)]
        k = 0
        hp = 0
        fails = []
        refusals_total = refusals_ok = 0
        for t, inp, exp in HAND:
            ok = judge(exp, run_candidate(cand, inp, w, k)); k += 1
            hp += ok
            if exp is None:
                refusals_total += 1; refusals_ok += ok
            if not ok:
                fails.append("hand:" + t)
        gp = 0
        for i, inp in enumerate(gen):
            exp = ref_or_refusal(inp)
            ok = judge(exp, run_candidate(cand, inp, w, k)); k += 1
            gp += ok
            if exp is None:
                refusals_total += 1; refusals_ok += ok
            if not ok:
                fails.append("gen:%d" % i)
        met = hp == len(HAND) and gp == len(gen)
        print("revision=%s candidate=present sha256=%s hand=%d/%d generated=%d/%d refusals=%d/%d seed=%d met=%s"
              % (rev, sha, hp, len(HAND), gp, len(gen), refusals_ok, refusals_total, seed, str(met).lower()))
        for f in fails[:40]:
            print("fail " + f)
        return 0 if met else 1
    finally:
        shutil.rmtree(w, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
