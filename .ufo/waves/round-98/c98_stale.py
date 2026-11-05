#!/usr/bin/env python3
"""c98_stale.py — round-98 C2 counter (kake): stale-serving extensions, contract v1.

Scores the candidate `scripts/stale_extensions.py` read from COMMITTED bytes
at --revision (/usr/bin/git, GIT_NO_REPLACE_OBJECTS=1) against
`.ufo/waves/round-98/stale-contract.md`:

  hand       HAND cases below; expectations written by hand from RFC 5861 /
             RFC 9111 and the contract (clause tag per case), not derived
             from the oracle.
  generated  N cases from a seeded grammar (default N=240); expectation by
             the counter's own oracle `decide()`. Malformed / out-of-contract
             inputs are part of the population and are scored as refusals.
             Default seed = int(sha256(<revision commit id>)[:8], 16), so the
             set is unknown until the scored commit exists; --seed overrides.

The candidate runs once per case: `python3 -I -B <copy>` with cwd and HOME
in a fresh dir under --work, env reduced to PATH/LC_ALL, stdin the case JSON,
10 s timeout. A decided case passes iff exit 0, stdout parses to an object
whose keys are exactly {decision, staleness} and equals the expectation. A
refusal case passes iff exit 1, stdout empty, stderr starts `invalid_input:`.

Line 1: `candidate=<present sha256=..|absent> hand=h/H generated=g/G
refusals=r/R seed=S met=<true|false>`. Exit 0 met (hand=H/H and
generated=G/G), 1 not met / absent, 2 setup error. Line 2: JSON failures
(first 40). `--selftest`: oracle vs every hand expectation, plus grammar
sanity (both decided and refused cases generated for the default N).
`--candidate-file PATH` scores a file outside git (controls / attack seats
only; the claim is scored only from --revision).
Known limit (declared before data): the candidate is not sandboxed beyond
-I and a scratch cwd; a candidate that opens this counter's source and
re-implements the oracle from it is not detected (carried R97-5).
"""
import argparse, hashlib, json, os, random, shutil, subprocess, sys, tempfile

GIT = "/usr/bin/git"
GENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", LC_ALL="C")
CAND = "scripts/stale_extensions.py"
CLAMP = 2147483648
TCHAR = set("!#$%&'*+-.^_`|~0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
OUT_REQ = {"max-age", "max-stale", "min-fresh", "only-if-cached"}
ERRS = (500, 502, 503, 504, "network")


class Refuse(Exception):
    pass


# ---------------------------------------------------------------- oracle
def _qd_ok(ch):
    o = ord(ch)
    return ch in "\t " or o == 0x21 or 0x23 <= o <= 0x5B or 0x5D <= o <= 0x7E or 0x80 <= o <= 0xFF


def _qp_ok(ch):
    o = ord(ch)
    return ch in "\t " or 0x21 <= o <= 0x7E or 0x80 <= o <= 0xFF


def parse_cc(s):
    elems, cur, i, inq = [], "", 0, False
    while i < len(s):
        ch = s[i]
        if inq:
            cur += ch
            if ch == "\\":
                if i + 1 >= len(s):
                    raise Refuse("dangling backslash")
                cur += s[i + 1]
                i += 2
                continue
            if ch == '"':
                inq = False
            i += 1
            continue
        if ch == '"':
            inq = True
        if ch == ",":
            elems.append(cur); cur = ""; i += 1; continue
        cur += ch; i += 1
    if inq:
        raise Refuse("unterminated quoted-string")
    elems.append(cur)
    out = {}
    for e in elems:
        e = e.strip(" \t")
        if not e:
            continue
        j = 0
        while j < len(e) and e[j] in TCHAR:
            j += 1
        name = e[:j]
        if not name:
            raise Refuse("bad directive name")
        rest = e[j:]
        val = None
        if rest:
            if rest[0] != "=" or len(rest) == 1:
                raise Refuse("bad directive syntax")
            v = rest[1:]
            if v[0] == '"':
                k, body = 1, ""
                while True:
                    if k >= len(v):
                        raise Refuse("unterminated quoted-string")
                    c = v[k]
                    if c == '"':
                        break
                    if c == "\\":
                        if k + 1 >= len(v) or not _qp_ok(v[k + 1]):
                            raise Refuse("bad quoted-pair")
                        body += v[k + 1]; k += 2; continue
                    if not _qd_ok(c):
                        raise Refuse("bad qdtext")
                    body += c; k += 1
                if k != len(v) - 1:
                    raise Refuse("text after quoted-string")
                val = ("q", body)
            else:
                if not all(c in TCHAR for c in v):
                    raise Refuse("bad token value")
                val = ("t", v)
        n = name.lower()
        if n not in out:
            out[n] = val
    return out


def delta(d, name):
    if name not in d:
        return None
    v = d[name]
    if v is None or v[0] != "t" or not v[1].isdigit() or not v[1].isascii():
        return None
    return min(int(v[1]), CLAMP)


def _int(x):
    return isinstance(x, int) and not isinstance(x, bool) and x >= 0


def decide(inp):
    if not isinstance(inp, dict):
        raise Refuse("not an object")
    allowed = {"response_cc", "request_cc", "freshness_lifetime", "current_age", "event", "error", "shared"}
    if set(inp) - allowed:
        raise Refuse("unknown key")
    for k in ("response_cc", "freshness_lifetime", "current_age", "event"):
        if k not in inp:
            raise Refuse("missing " + k)
    rc_s, qc_s = inp["response_cc"], inp.get("request_cc", "")
    if not isinstance(rc_s, str) or not isinstance(qc_s, str):
        raise Refuse("cc not string")
    L, A = inp["freshness_lifetime"], inp["current_age"]
    if not _int(L) or not _int(A):
        raise Refuse("bad integer")
    ev = inp["event"]
    if ev not in ("request", "error"):
        raise Refuse("bad event")
    sh = inp.get("shared", False)
    if not isinstance(sh, bool):
        raise Refuse("bad shared")
    err = inp.get("error", None)
    if ev == "request":
        if err is not None:
            raise Refuse("error on request event")
    else:
        if err is None:
            raise Refuse("missing error")
        if err != "network" and not (isinstance(err, int) and not isinstance(err, bool) and 100 <= err <= 599):
            raise Refuse("bad error")
    for s in (rc_s, qc_s):
        if any(ord(c) > 0xFF or (ord(c) < 0x20 and c != "\t") or ord(c) == 0x7F for c in s):
            raise Refuse("bad character")
    rc, qc = parse_cc(rc_s), parse_cc(qc_s)
    if set(qc) & OUT_REQ:
        raise Refuse("request directive outside contract")
    st = max(0, A - L)
    if ev == "error" and err not in ERRS:
        return {"decision": "not-an-error", "staleness": st}
    if A < L and "no-cache" not in rc and "no-cache" not in qc:
        return {"decision": "fresh", "staleness": st}
    prohibited = ("no-cache" in rc or "must-revalidate" in rc or "no-cache" in qc or
                  (sh and ("proxy-revalidate" in rc or "s-maxage" in rc)))
    if ev == "request":
        w = delta(rc, "stale-while-revalidate")
        ok = not prohibited and w is not None and st <= w
        return {"decision": "serve-stale-revalidate" if ok else "revalidate", "staleness": st}
    e = delta(qc, "stale-if-error")
    if e is None:
        e = delta(rc, "stale-if-error")
    ok = not prohibited and e is not None and st <= e
    return {"decision": "serve-stale-error" if ok else "error-through", "staleness": st}


def expect(inp):
    try:
        return decide(inp)
    except Refuse:
        return "REFUSE"


# ---------------------------------------------------------------- hand cases
def C(rc, L, A, ev="request", err=None, qc=None, shared=None, **extra):
    d = {"response_cc": rc, "freshness_lifetime": L, "current_age": A, "event": ev}
    if err is not None:
        d["error"] = err
    if qc is not None:
        d["request_cc"] = qc
    if shared is not None:
        d["shared"] = shared
    d.update(extra)
    return d


SW = "max-age=600, stale-while-revalidate=30"
SE = "max-age=600, stale-if-error=1200"
R = "REFUSE"
HAND = [
    ("H01", "5861§3.1 inside window", C(SW, 600, 615), ("serve-stale-revalidate", 15)),
    ("H02", "5861§3.1 boundary inclusive", C(SW, 600, 630), ("serve-stale-revalidate", 30)),
    ("H03", "5861§3 past window", C(SW, 600, 631), ("revalidate", 31)),
    ("H04", "9111§4.2 fresh", C(SW, 600, 599), ("fresh", 0)),
    ("H05", "9111§4.2 age==lifetime is stale", C(SW, 600, 600), ("serve-stale-revalidate", 0)),
    ("H06", "5861§4.1 example 900", C(SE, 600, 900, "error", 500), ("serve-stale-error", 300)),
    ("H07", "5861§4.1 age 1800 boundary", C(SE, 600, 1800, "error", 500), ("serve-stale-error", 1200)),
    ("H08", "5861§4.1 age > 1800 writes error through", C(SE, 600, 1801, "error", 500), ("error-through", 1201)),
    ("H09", "5861§4 502", C(SE, 600, 900, "error", 502), ("serve-stale-error", 300)),
    ("H10", "5861§4 503", C(SE, 600, 900, "error", 503), ("serve-stale-error", 300)),
    ("H11", "5861§4 504", C(SE, 600, 900, "error", 504), ("serve-stale-error", 300)),
    ("H12", "5861§1 network failure", C(SE, 600, 900, "error", "network"), ("serve-stale-error", 300)),
    ("H13", "5861§4 404 not an error", C(SE, 600, 900, "error", 404), ("not-an-error", 300)),
    ("H14", "5861§4 501 not listed", C(SE, 600, 900, "error", 501), ("not-an-error", 300)),
    ("H15", "5861§4 429 not listed", C(SE, 600, 900, "error", 429), ("not-an-error", 300)),
    ("H16", "5861§3 swr does not cover errors", C(SW, 600, 615, "error", 500), ("error-through", 15)),
    ("H17", "5861§4 sie does not cover plain requests", C(SE, 600, 900), ("revalidate", 300)),
    ("H18", "5861§4 request scope narrower", C(SE, 600, 900, "error", 500, qc="stale-if-error=60"), ("error-through", 300)),
    ("H19", "5861§4 request scope wider", C("max-age=600, stale-if-error=10", 600, 900, "error", 500, qc="stale-if-error=600"), ("serve-stale-error", 300)),
    ("H20", "5861§4 request-only sie", C("max-age=600", 600, 900, "error", 503, qc="stale-if-error=300"), ("serve-stale-error", 300)),
    ("H21", "9111§5.2.2.2 must-revalidate blocks sie", C(SE + ", must-revalidate", 600, 900, "error", 500), ("error-through", 300)),
    ("H22", "9111§5.2.2.2 must-revalidate blocks swr", C("must-revalidate, " + SW, 600, 615), ("revalidate", 15)),
    ("H23", "9111§5.2.2.4 no-cache response, fresh age", C("no-cache, " + SW, 600, 10), ("revalidate", 0)),
    ("H24", "9111§5.2.2.4 no-cache response on error", C("no-cache, " + SE, 600, 10, "error", 500), ("error-through", 0)),
    ("H25", "9111§5.2.1.4 no-cache request, fresh age", C(SW, 600, 10, qc="no-cache"), ("revalidate", 0)),
    ("H26", "9111§5.2.2.8 proxy-revalidate shared", C(SW + ", proxy-revalidate", 600, 615, shared=True), ("revalidate", 15)),
    ("H27", "9111§5.2.2.8 proxy-revalidate private cache", C(SW + ", proxy-revalidate", 600, 615, shared=False), ("serve-stale-revalidate", 15)),
    ("H28", "9111§5.2.2.10 s-maxage shared", C(SE + ", s-maxage=600", 600, 900, "error", 500, shared=True), ("error-through", 300)),
    ("H29", "9111§5.2.2.10 s-maxage private cache", C(SE + ", s-maxage=600", 600, 900, "error", 500, shared=False), ("serve-stale-error", 300)),
    ("H30", "contract 4 quoted value absent", C('max-age=600, stale-while-revalidate="30"', 600, 615), ("revalidate", 15)),
    ("H31", "contract 4 non-digit value absent", C("max-age=600, stale-while-revalidate=abc", 600, 615), ("revalidate", 15)),
    ("H32", "contract 4 negative value absent", C("max-age=600, stale-while-revalidate=-1", 600, 615), ("revalidate", 15)),
    ("H33", "9111§4.2.1 first occurrence", C("stale-while-revalidate=5, stale-while-revalidate=60", 600, 630), ("revalidate", 30)),
    ("H34", "contract 3 case-insensitive name", C("Max-Age=600, STALE-WHILE-REVALIDATE=30", 600, 615), ("serve-stale-revalidate", 15)),
    ("H35", "9111§1.2.2 clamp", C("stale-while-revalidate=99999999999", 0, 1000000000), ("serve-stale-revalidate", 1000000000)),
    ("H36", "5861§3 request swr ignored", C("max-age=600", 600, 615, qc="stale-while-revalidate=60"), ("revalidate", 15)),
    ("H37", "contract rule 2 fresh on error", C(SE, 600, 100, "error", 500), ("fresh", 0)),
    ("H38", "no directives zero lifetime", C("", 0, 0), ("revalidate", 0)),
    ("H39", "contract input: error on request", C(SW, 600, 615, "request", 500), R),
    ("H40", "contract input: missing error", C(SE, 600, 900, "error"), R),
    ("H41", "contract input: negative age", C(SW, 600, -1), R),
    ("H42", "contract input: boolean age", C(SW, 600, True), R),
    ("H43", "contract input: float lifetime", C(SW, 600.0, 615), R),
    ("H44", "contract 2 whitespace around =", C("max-age = 600", 600, 615), R),
    ("H45", "contract 2 empty value", C("stale-if-error=", 600, 900, "error", 500), R),
    ("H46", "contract 2 unterminated quote", C('foo="bar, max-age=600', 600, 615), R),
    ("H47", "contract 5 max-stale out of contract", C(SW, 600, 615, qc="max-stale"), R),
    ("H48", "contract input: unknown key", C(SW, 600, 615, extra_key=1), R),
    ("H49", "5861§4 200 is not an error", C(SE, 600, 900, "error", 200), ("not-an-error", 300)),
    ("H50", "contract input: status 99", C(SE, 600, 900, "error", 99), R),
    ("H51", "contract input: error string", C(SE, 600, 900, "error", "timeout"), R),
    ("H52", "contract 1 comma inside quotes", C('foo="a, stale-while-revalidate=30", max-age=600', 600, 615), ("revalidate", 15)),
    ("H53", "contract 4 qualified no-cache conservative", C('no-cache="set-cookie", stale-while-revalidate=30', 600, 615), ("revalidate", 15)),
    ("H54", "contract 1 empty list elements", C(", ,stale-while-revalidate=30,,", 600, 615), ("serve-stale-revalidate", 15)),
    ("H55", "contract 4 zero window at age==lifetime", C("stale-while-revalidate=0", 600, 600), ("serve-stale-revalidate", 0)),
    ("H56", "contract 5 no-store ignored", C("no-store, " + SW, 600, 615), ("serve-stale-revalidate", 15)),
    ("H57", "contract 1 HTAB OWS", C("max-age=600,\tstale-while-revalidate=30", 600, 615), ("serve-stale-revalidate", 15)),
    ("H58", "contract 4 request sie invalid falls back", C(SE, 600, 900, "error", 500, qc='stale-if-error="5"'), ("serve-stale-error", 300)),
    ("H59", "contract input: shared not boolean", C(SW, 600, 615, shared="yes"), R),
    ("H60", "contract 2 text after quoted-string", C('foo="a"b, ' + SW, 600, 615), R),
]


# ---------------------------------------------------------------- generator
def gen_case(rng):
    def dv():
        return rng.choice(["0", "5", "30", "60", "300", "600", "1200", "3600", "99999999999",
                           '"30"', "abc", "-1", "1.5", str(rng.randint(0, 2000))])

    def cc(pool, n):
        parts = []
        for _ in range(n):
            p = rng.choice(pool)
            if callable(p):
                p = p()
            if rng.random() < 0.2:
                p = p.upper() if rng.random() < 0.5 else p.title()
            parts.append(p)
        sep = rng.choice([", ", ",", " , ", ",\t"])
        return sep.join(parts)

    resp_pool = [lambda: "max-age=" + str(rng.randint(0, 900)),
                 lambda: "stale-while-revalidate=" + dv(),
                 lambda: "stale-if-error=" + dv(),
                 "must-revalidate", "proxy-revalidate", "no-cache", "public", "private", "no-store",
                 lambda: "s-maxage=" + str(rng.randint(0, 900)), "foo", 'ext="a, b"', 'no-cache="set-cookie"']
    req_pool = [lambda: "stale-if-error=" + dv(), "no-cache", lambda: "stale-while-revalidate=" + dv(),
                "x-ext", "no-transform"]
    L = rng.choice([0, 1, 60, 300, 600, rng.randint(0, 1200)])
    A = max(0, L + rng.choice([-50, -1, 0, 1, 15, 30, 31, 60, 299, 300, 301, 1200, 1201, rng.randint(-100, 2500)]))
    ev = rng.choice(["request", "error"])
    d = {"response_cc": cc(resp_pool, rng.randint(0, 4)), "freshness_lifetime": L,
         "current_age": A, "event": ev}
    if rng.random() < 0.6:
        d["request_cc"] = cc(req_pool, rng.randint(0, 2))
    if rng.random() < 0.6:
        d["shared"] = rng.random() < 0.5
    if ev == "error":
        d["error"] = rng.choice([500, 502, 503, 504, "network", 404, 501, 429, 200, 304])
    if rng.random() < 0.15:  # malformed / out-of-contract population
        k = rng.randint(0, 9)
        if k == 0: d["current_age"] = -rng.randint(1, 9)
        elif k == 1: d["freshness_lifetime"] = rng.choice([True, 1.0, "600"])
        elif k == 2: d["event"] = rng.choice(["stale", "", None])
        elif k == 3: d["error"] = rng.choice([99, 600, "timeout", True]) if ev == "error" else 500
        elif k == 4: d["response_cc"] += rng.choice([", max-age = 5", ", stale-if-error=", ', x="open'])
        elif k == 5: d["request_cc"] = rng.choice(["max-stale", "min-fresh=5", "only-if-cached", "max-age=0"])
        elif k == 6: d["bogus"] = 1
        elif k == 7: d.pop(rng.choice(["response_cc", "freshness_lifetime", "current_age", "event"]))
        elif k == 8: d["shared"] = rng.choice(["true", 1, None])
        else: d["response_cc"] += ', y="a"b'
    return d


def generate(seed, n):
    rng = random.Random(seed)
    return [gen_case(rng) for _ in range(n)]


# ---------------------------------------------------------------- runner
def run_one(cand, case, work):
    d = tempfile.mkdtemp(prefix="c", dir=work)
    try:
        p = subprocess.run([sys.executable, "-I", "-B", cand], input=json.dumps(case).encode(),
                           capture_output=True, cwd=d, timeout=10,
                           env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": d})
        return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        return "timeout", "", ""
    finally:
        shutil.rmtree(d, ignore_errors=True)


def judge(rcode, out, err, want):
    if want == "REFUSE":
        return rcode == 1 and out == "" and err.startswith("invalid_input:")
    if rcode != 0:
        return False
    try:
        o = json.loads(out)
    except ValueError:
        return False
    return isinstance(o, dict) and set(o) == {"decision", "staleness"} and \
        o == {"decision": want[0], "staleness": want[1]} and type(o["staleness"]) is int


def norm(e):
    return e if e == "REFUSE" else (e["decision"], e["staleness"])


def selftest(n):
    ok = 0
    for hid, tag, inp, want in HAND:
        got = norm(expect(inp))
        if got == want:
            ok += 1
        else:
            print(f"FAIL {hid} {tag}: want={want} got={got}")
    cases = generate(98, n)
    ref = sum(1 for c in cases if expect(c) == "REFUSE")
    dec = {norm(expect(c))[0] for c in cases if expect(c) != "REFUSE"}
    g_ok = ref > 0 and len(dec) == 6
    print(f"hand-oracle {ok}/{len(HAND)} generated-refusals={ref}/{n} decisions={sorted(dec)}")
    print(f"selftest {'ok' if ok == len(HAND) and g_ok else 'FAIL'}")
    return 0 if ok == len(HAND) and g_ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root"); ap.add_argument("--revision"); ap.add_argument("--work")
    ap.add_argument("--seed", type=int); ap.add_argument("--generated", type=int, default=240)
    ap.add_argument("--candidate-file"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.generated)
    if not a.work or not (a.candidate_file or (a.root and a.revision)):
        print("usage: --work and (--root --revision | --candidate-file)", file=sys.stderr)
        return 2
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c98stale-", dir=a.work)
    try:
        seed_src = "file"
        if a.candidate_file:
            data = open(a.candidate_file, "rb").read()
        else:
            p = subprocess.run([GIT, "-C", a.root, "rev-parse", "--verify", a.revision + "^{commit}"],
                               capture_output=True, env=GENV)
            if p.returncode:
                print("setup-error bad revision"); return 2
            rev = p.stdout.decode().strip(); seed_src = rev
            p = subprocess.run([GIT, "-C", a.root, "show", f"{rev}:{CAND}"], capture_output=True, env=GENV)
            if p.returncode:
                print(f"candidate=absent hand=0/{len(HAND)} generated=0/{a.generated} refusals=0/0 "
                      f"seed=- met=false revision={rev}")
                return 1
            data = p.stdout
        seed = a.seed if a.seed is not None else int(hashlib.sha256(seed_src.encode()).hexdigest()[:8], 16)
        cand = os.path.join(work, "cand.py")
        open(cand, "wb").write(data)
        sha = hashlib.sha256(data).hexdigest()
        fails, h_ok = [], 0
        for hid, tag, inp, want in HAND:
            r = run_one(cand, inp, work)
            if judge(*r, want):
                h_ok += 1
            else:
                fails.append({"id": hid, "tag": tag, "want": want, "rc": r[0], "out": r[1][:120], "err": r[2][:120]})
        gens = generate(seed, a.generated)
        g_ok = r_ok = r_n = 0
        for i, inp in enumerate(gens):
            want = norm(expect(inp))
            r_n += want == "REFUSE"
            r = run_one(cand, inp, work)
            if judge(*r, want):
                g_ok += 1
                r_ok += want == "REFUSE"
            else:
                fails.append({"id": f"G{i:03d}", "input": inp, "want": want, "rc": r[0],
                              "out": r[1][:120], "err": r[2][:120]})
        met = h_ok == len(HAND) and g_ok == len(gens)
        print(f"candidate=present sha256={sha} hand={h_ok}/{len(HAND)} generated={g_ok}/{len(gens)} "
              f"refusals={r_ok}/{r_n} seed={seed} met={'true' if met else 'false'}"
              + (f" revision={seed_src}" if not a.candidate_file else " source=candidate-file"))
        try:
            print(json.dumps(fails[:40], ensure_ascii=False, default=str))
        except BrokenPipeError:
            pass
        return 0 if met else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
