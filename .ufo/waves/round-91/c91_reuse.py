#!/usr/bin/env python3
"""Round-91 C2 counter: stored-response reuse decision conformance (contract v1).

Frozen before data (`.ufo/waves/round-91/freeze.md`). Reads committed bytes at
--revision, scores the candidate against `.ufo/waves/round-91/c2-contract.md`
(45 clause-tagged hand cases + a seeded generated population decided by this
file's own reference) and requires every frozen forgery subject to be refused.

Successor requirements this counter implements (round-90 routed defect R90-A, gate
shape): the population pins and the case labels live in this file and in
`frozen/c2-population.sha256` only, are never written into any directory a scored
subject can reach (each subject runs with cwd set to a fresh empty directory and
receives exactly one JSON object on stdin), the pins are checked against the frozen
file digest named below, and the hand-case input digests are checked against the
candidate's own source (`anti_table`) so a lookup table is refused.

met <=> candidate present
      AND population digest-ok
      AND anti_table ok
      AND hand cases all decided as declared
      AND generated cases all decided as the reference decides
      AND every forgery subject refused (scored met=false).

Output line 1:
  C2v91 revision=<sha> candidate=present|absent hand=H/H generated=G/G
        forgeries_refused=F/F anti_table=ok|hit population=ok|drift seed=<n> met=true|false
line 2: JSON detail. Exit 0 iff met; 2 on reference/case drift; 1 otherwise.
Scratch: --work (required); everything created beneath it and removed.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

BASE = "5b20af16661040f383e9e84f85b838619857cb14"
CANDIDATE = "scripts/stored_reuse.py"
PINS_FILE = ".ufo/waves/round-91/frozen/c2-population.sha256"
PINS_SHA = "033b6103303d33690c4a6d02b04df36ba86b3b4f1d1e18aa5e267cb9b95084c8"
FORGERIES = [
    ".ufo/waves/round-91/frozen/neg-pin-reader.py",
    ".ufo/waves/round-91/frozen/neg-allowlist.py",
    ".ufo/waves/round-91/frozen/neg-blanket-refuse.py",
    ".ufo/waves/round-91/frozen/neg-blanket-admit.py",
    ".ufo/waves/round-91/frozen/neg-hash-table.py",
]
CACHEABLE = (200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501)
DELTA = ("max-age", "s-maxage", "min-fresh")
KEYS_OUT = {"decision", "freshness_lifetime", "current_age"}


class Invalid(Exception):
    pass


def ascii_lower(s):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in s)


def parse_cc(value):
    out = {}
    for raw in value.split(","):
        d = raw.strip(" \t")
        if not d:
            raise Invalid("empty directive")
        name, sep, arg = d.partition("=")
        name = ascii_lower(name.strip(" \t"))
        if not name:
            raise Invalid("empty directive name")
        if sep:
            arg = arg.strip(" \t")
            quoted = len(arg) >= 2 and arg[0] == '"' and arg[-1] == '"'
            if quoted:
                arg = arg[1:-1]
            if name in DELTA or name == "max-stale":
                if quoted:
                    raise Invalid("quoted delta-seconds")
                if not re.fullmatch(r"[0-9]+", arg):
                    raise Invalid("bad delta-seconds")
                val = int(arg)
            else:
                val = arg
        else:
            val = None
        if name in out and out[name] != val:
            raise Invalid("duplicate directive")
        out[name] = val
    return out


def read_headers(obj):
    if not isinstance(obj, dict):
        raise Invalid("headers must be an object")
    out = {}
    for k, v in obj.items():
        if not isinstance(k, str) or not isinstance(v, str):
            raise Invalid("header name and value must be strings")
        if not k:
            raise Invalid("empty header name")
        lk = ascii_lower(k)
        if lk in out:
            raise Invalid("duplicate header name")
        if "\r" in v or "\n" in v or "\0" in v:
            raise Invalid("control character in value")
        out[lk] = v.strip(" \t")
    return out


def as_int(name, value, allow_negative=False):
    if not re.fullmatch(r"-?[0-9]+", value):
        raise Invalid("%s must be an integer" % name)
    n = int(value)
    if not allow_negative and n < 0:
        raise Invalid("%s must be nonnegative" % name)
    return n


def reference(inp):
    if not isinstance(inp, dict):
        raise Invalid("input must be an object")
    if set(inp) - {"stored", "request", "now", "shared"}:
        raise Invalid("unknown input key")
    for k in ("stored", "request", "now"):
        if k not in inp:
            raise Invalid("missing %s" % k)
    stored, request, now = inp["stored"], inp["request"], inp["now"]
    if not isinstance(stored, dict) or not isinstance(request, dict):
        raise Invalid("stored and request must be objects")
    if set(stored) - {"status", "headers"} or set(request) - {"method", "headers"}:
        raise Invalid("unknown stored/request key")
    if "status" not in stored:
        raise Invalid("missing status")
    status = stored["status"]
    if not isinstance(status, int) or isinstance(status, bool) or not 100 <= status <= 599:
        raise Invalid("status must be an integer 100..599")
    if "method" not in request:
        raise Invalid("missing method")
    method = request["method"]
    if not isinstance(method, str) or not method:
        raise Invalid("method must be a nonempty string")
    if not isinstance(now, int) or isinstance(now, bool) or now < 0:
        raise Invalid("now must be a nonnegative integer")
    shared = inp.get("shared", False)
    if not isinstance(shared, bool):
        raise Invalid("shared must be a boolean")
    sh = read_headers(stored.get("headers", {}))
    rh = read_headers(request.get("headers", {}))
    scc = parse_cc(sh["cache-control"]) if "cache-control" in sh else {}
    rcc = parse_cc(rh["cache-control"]) if "cache-control" in rh else {}
    # clause 5-9: validation and lifetime first
    if "date" not in sh:
        raise Invalid("missing Date")
    date = as_int("Date", sh["date"], allow_negative=True)
    age_h = as_int("Age", sh["age"]) if "age" in sh else 0
    expires = as_int("Expires", sh["expires"], allow_negative=True) if "expires" in sh else None
    current_age = max(0, age_h) + max(0, now - date)
    if shared and "s-maxage" in scc:
        lifetime = scc["s-maxage"]
    elif "max-age" in scc:
        lifetime = scc["max-age"]
    elif expires is not None:
        lifetime = expires - date
    else:
        lifetime = None
    # clause 10
    vary = sh.get("vary")
    star = vary is not None and any(m.strip(" \t") == "*" for m in vary.split(","))
    if (method not in ("GET", "HEAD") or status not in CACHEABLE
            or "no-store" in scc or "no-store" in rcc
            or ("private" in scc and shared) or star):
        return {"decision": "not-storable", "freshness_lifetime": None, "current_age": None}
    # clauses 11-19
    if lifetime is None:
        decision = "heuristic-undecided"
    elif "no-cache" in rcc:
        decision = "revalidate"
    elif "no-cache" in scc:
        decision = "revalidate"
    elif "max-age" in rcc and current_age > rcc["max-age"]:
        decision = "revalidate"
    elif "min-fresh" in rcc and lifetime - current_age < rcc["min-fresh"]:
        decision = "revalidate"
    elif current_age < lifetime:
        decision = "reuse"
    elif "must-revalidate" in scc or ("proxy-revalidate" in scc and shared):
        decision = "must-revalidate-fail"
    elif "max-stale" in rcc and (rcc["max-stale"] is None
                                 or current_age - lifetime <= rcc["max-stale"]):
        decision = "serve-stale"
    else:
        decision = "revalidate"
    # clause 20
    if "only-if-cached" in rcc and decision not in ("reuse", "not-storable"):
        decision = "only-if-cached-miss"
    return {"decision": decision, "freshness_lifetime": lifetime, "current_age": current_age}


def H(name, stored_cc, method, now, *, status=200, request_cc=None, shared=False,
      date=1000000, age=None, expires=None, vary=None, decision=None,
      lifetime=None, ageout=None):
    headers = {"Date": str(date)}
    if age is not None:
        headers["Age"] = str(age)
    if stored_cc:
        headers["Cache-Control"] = stored_cc
    if expires is not None:
        headers["Expires"] = str(expires)
    if vary is not None:
        headers["Vary"] = vary
    req = {"method": method, "headers": {}}
    if request_cc:
        req["headers"]["Cache-Control"] = request_cc
    inp = {"stored": {"status": status, "headers": headers}, "request": req,
           "now": now, "shared": shared}
    return (name, inp, {"decision": decision, "freshness_lifetime": lifetime,
                        "current_age": ageout})


def R(name, inp):
    return (name, inp, None)


def hand_cases():
    c = []
    c.append(H("fresh-max-age", "max-age=60", "GET", 1000030, decision="reuse", lifetime=60, ageout=30))
    c.append(H("stale-boundary", "max-age=60", "GET", 1000060, decision="revalidate", lifetime=60, ageout=60))
    c.append(H("stale-max-stale-ok", "max-age=60", "GET", 1000065, request_cc="max-stale=10",
               decision="serve-stale", lifetime=60, ageout=65))
    c.append(H("stale-max-stale-too-old", "max-age=60", "GET", 1000071, request_cc="max-stale=10",
               decision="revalidate", lifetime=60, ageout=71))
    c.append(H("max-stale-unbounded", "max-age=60", "GET", 1001000, request_cc="max-stale",
               decision="serve-stale", lifetime=60, ageout=1000))
    c.append(H("must-revalidate-stale", "max-age=60, must-revalidate", "GET", 1000061,
               request_cc="max-stale", decision="must-revalidate-fail", lifetime=60, ageout=61))
    c.append(H("proxy-revalidate-shared", "max-age=60, proxy-revalidate", "GET", 1000061,
               request_cc="max-stale=100", shared=True, decision="must-revalidate-fail",
               lifetime=60, ageout=61))
    c.append(H("proxy-revalidate-private", "max-age=60, proxy-revalidate", "GET", 1000061,
               request_cc="max-stale=100", decision="serve-stale", lifetime=60, ageout=61))
    c.append(H("s-maxage-shared", "max-age=10, s-maxage=100", "GET", 1000050, shared=True,
               decision="reuse", lifetime=100, ageout=50))
    c.append(H("s-maxage-ignored-private", "max-age=10, s-maxage=100", "GET", 1000050,
               decision="revalidate", lifetime=10, ageout=50))
    c.append(H("expires-lifetime", None, "GET", 1000100, expires=1000120, decision="reuse",
               lifetime=120, ageout=100))
    c.append(H("expires-negative", None, "GET", 1000000, expires=999900,
               decision="revalidate", lifetime=-100, ageout=0))
    c.append(H("no-lifetime", None, "GET", 1000010, decision="heuristic-undecided",
               lifetime=None, ageout=10))
    c.append(H("request-no-cache", "max-age=60", "GET", 1000030, request_cc="no-cache",
               decision="revalidate", lifetime=60, ageout=30))
    c.append(H("stored-no-cache", "no-cache, max-age=60", "GET", 1000030,
               decision="revalidate", lifetime=60, ageout=30))
    c.append(H("request-max-age", "max-age=60", "GET", 1000030, request_cc="max-age=10",
               decision="revalidate", lifetime=60, ageout=30))
    c.append(H("request-max-age-equal", "max-age=60", "GET", 1000030, request_cc="max-age=30",
               decision="reuse", lifetime=60, ageout=30))
    c.append(H("min-fresh-short", "max-age=60", "GET", 1000030, request_cc="min-fresh=40",
               decision="revalidate", lifetime=60, ageout=30))
    c.append(H("min-fresh-exact", "max-age=60", "GET", 1000030, request_cc="min-fresh=30",
               decision="reuse", lifetime=60, ageout=30))
    c.append(H("only-if-cached-stale", "max-age=60", "GET", 1000060, request_cc="only-if-cached",
               decision="only-if-cached-miss", lifetime=60, ageout=60))
    c.append(H("only-if-cached-fresh", "max-age=60", "GET", 1000030, request_cc="only-if-cached",
               decision="reuse", lifetime=60, ageout=30))
    c.append(H("not-storable-method", "max-age=60", "POST", 1000030, decision="not-storable"))
    c.append(H("not-storable-status", "max-age=60", "GET", 1000030, status=500,
               decision="not-storable"))
    c.append(H("not-storable-no-store", "no-store, max-age=60", "GET", 1000030,
               decision="not-storable"))
    c.append(H("not-storable-request-no-store", "max-age=60", "GET", 1000030,
               request_cc="no-store", decision="not-storable"))
    c.append(H("not-storable-private-shared", "private, max-age=60", "GET", 1000030,
               shared=True, decision="not-storable"))
    c.append(H("private-private", "private, max-age=60", "GET", 1000030, decision="reuse",
               lifetime=60, ageout=30))
    c.append(H("not-storable-vary-star", "max-age=60", "GET", 1000030, vary="*",
               decision="not-storable"))
    c.append(H("vary-named", "max-age=60", "GET", 1000030, vary="Accept", decision="reuse",
               lifetime=60, ageout=30))
    c.append(H("age-header", "max-age=60", "GET", 1000010, age=40, decision="reuse",
               lifetime=60, ageout=50))
    c.append(H("age-future-date", "max-age=60", "GET", 1000000, date=1000100, age=5,
               decision="reuse", lifetime=60, ageout=5))
    c.append(H("head-method", "max-age=60", "HEAD", 1000030, decision="reuse", lifetime=60, ageout=30))
    c.append(H("unknown-directive-ignored", "max-age=60, foo=bar", "GET", 1000030,
               decision="reuse", lifetime=60, ageout=30))
    c.append(H("must-revalidate-fresh", "max-age=60, must-revalidate", "GET", 1000030,
               decision="reuse", lifetime=60, ageout=30))
    c.append(H("max-age-beats-expires", "max-age=60", "GET", 1000030, expires=1000120,
               decision="reuse", lifetime=60, ageout=30))
    c.append(H("only-if-cached-not-storable", "max-age=60", "POST", 1000030,
               request_cc="only-if-cached", decision="not-storable"))
    # refusals
    c.append(R("refuse-quoted-delta", {"stored": {"status": 200, "headers": {
        "Date": "1000000", "Cache-Control": 'max-age="60"'}},
        "request": {"method": "GET", "headers": {}}, "now": 1000030}))
    c.append(R("refuse-duplicate-header-name", {"stored": {"status": 200, "headers": {
        "Date": "1000000", "Cache-Control": "max-age=60", "cache-control": "max-age=30"}},
        "request": {"method": "GET", "headers": {}}, "now": 1000030}))
    c.append(R("refuse-cr-value", {"stored": {"status": 200, "headers": {
        "Date": "1000000", "Cache-Control": "max-age=60", "X-Note": "a\rb"}},
        "request": {"method": "GET", "headers": {}}, "now": 1000030}))
    c.append(R("refuse-missing-date", {"stored": {"status": 200, "headers": {
        "Cache-Control": "max-age=60"}},
        "request": {"method": "GET", "headers": {}}, "now": 1000030}))
    c.append(R("refuse-negative-now", {"stored": {"status": 200, "headers": {
        "Date": "1000000", "Cache-Control": "max-age=60"}},
        "request": {"method": "GET", "headers": {}}, "now": -1}))
    c.append(R("refuse-unknown-key", {"stored": {"status": 200, "headers": {
        "Date": "1000000", "Cache-Control": "max-age=60"}},
        "request": {"method": "GET", "headers": {}}, "now": 1000030, "extra": 1}))
    c.append(R("refuse-string-status", {"stored": {"status": "200", "headers": {
        "Date": "1000000", "Cache-Control": "max-age=60"}},
        "request": {"method": "GET", "headers": {}}, "now": 1000030}))
    c.append(R("refuse-duplicate-directive", {"stored": {"status": 200, "headers": {
        "Date": "1000000", "Cache-Control": "max-age=60, max-age=30"}},
        "request": {"method": "GET", "headers": {}}, "now": 1000030}))
    c.append(R("refuse-negative-age", {"stored": {"status": 200, "headers": {
        "Date": "1000000", "Age": "-1", "Cache-Control": "max-age=60"}},
        "request": {"method": "GET", "headers": {}}, "now": 1000030}))
    return c


def generate(seed, n):
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        status = rng.choice([200, 200, 200, 203, 301, 404, 500])
        date = rng.randrange(900000, 1100000)
        age = rng.choice([0, 0, 5, 30, 60, 120])
        now = date + rng.randrange(-30, 400)
        if now < 0:
            now = 0
        method = rng.choice(["GET", "GET", "GET", "HEAD", "POST"])
        scc = []
        if rng.random() < 0.6:
            scc.append("max-age=%d" % rng.choice([0, 10, 30, 60, 120]))
        if rng.random() < 0.25:
            scc.append("s-maxage=%d" % rng.choice([10, 50, 100]))
        for name, p in (("no-cache", 0.15), ("no-store", 0.08), ("must-revalidate", 0.15),
                        ("proxy-revalidate", 0.08), ("private", 0.08)):
            if rng.random() < p:
                scc.append(name)
        rcc = []
        for name, p in (("no-cache", 0.2), ("no-store", 0.1), ("only-if-cached", 0.08)):
            if rng.random() < p:
                rcc.append(name)
        if rng.random() < 0.2:
            rcc.append("max-age=%d" % rng.choice([0, 10, 30, 60]))
        if rng.random() < 0.2:
            rcc.append("min-fresh=%d" % rng.choice([0, 10, 30, 60]))
        if rng.random() < 0.2:
            rcc.append(rng.choice(["max-stale", "max-stale=0", "max-stale=10", "max-stale=60"]))
        headers = {"Date": str(date)}
        if age:
            headers["Age"] = str(age)
        if scc:
            headers["Cache-Control"] = ", ".join(scc)
        if rng.random() < 0.12:
            headers["Expires"] = str(date + rng.choice([-60, 0, 60, 300]))
        if rng.random() < 0.08:
            headers["Vary"] = rng.choice(["*", "Accept", "Accept, Accept-Language"])
        req = {"method": method, "headers": {}}
        if rcc:
            req["headers"]["Cache-Control"] = ", ".join(rcc)
        out.append({"stored": {"status": status, "headers": headers}, "request": req,
                    "now": now, "shared": rng.random() < 0.3})
    return out


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def extract(root, rev, paths, dest):
    p = git(root, "archive", "--format=tar", rev, "--", *paths)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode(errors="replace"))
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
        tf.extractall(dest, filter="data")


def score_subject(path, cases, gen_expected, work, timeout=60):
    """Run one subject over every case. Returns (hand_ok, gen_ok, errors, failures)."""
    failures = []
    errors = []
    hand_ok = gen_ok = 0
    idx = 0
    for i, (name, inp, expected) in enumerate(cases):
        idx += 1
        ok, why = run_one(path, inp, expected, work, timeout)
        if why.startswith("error:"):
            errors.append("%s %s" % (name, why))
        elif ok:
            hand_ok += 1
        else:
            failures.append("%s %s" % (name, why))
    for i, (inp, expected) in enumerate(gen_expected):
        ok, why = run_one(path, inp, expected, work, timeout)
        if why.startswith("error:"):
            errors.append("gen%d %s" % (i, why))
        elif ok:
            gen_ok += 1
        else:
            failures.append("gen%d %s" % (i, why))
    return hand_ok, gen_ok, errors, failures


def run_one(path, inp, expected, work, timeout):
    d = tempfile.mkdtemp(prefix="s-", dir=work)
    payload = json.dumps(inp).encode()
    try:
        p = subprocess.run([sys.executable, "-B", path], input=payload, cwd=d,
                           capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, "error: timeout"
    except OSError as exc:
        return False, "error: %s" % exc
    finally:
        shutil.rmtree(d, ignore_errors=True)
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace")
    if expected is None:
        if p.returncode != 1:
            return False, "expected refusal, rc=%d" % p.returncode
        if out.strip():
            return False, "refusal wrote stdout"
        if not err.startswith("invalid_input:"):
            return False, "refusal stderr prefix"
        return True, "ok"
    if p.returncode != 0:
        return False, "expected success, rc=%d %s" % (p.returncode, err.strip()[:120])
    try:
        got = json.loads(out)
    except ValueError:
        return False, "stdout not JSON"
    if not isinstance(got, dict) or set(got) != KEYS_OUT:
        return False, "output keys %s" % (sorted(got) if isinstance(got, dict) else type(got).__name__)
    for k in KEYS_OUT:
        if got[k] != expected[k] or type(got[k]) is not type(expected[k]):
            return False, "%s=%r want %r" % (k, got[k], expected[k])
    return True, "ok"


def selftest():
    cases = hand_cases()
    bad = []
    for name, inp, expected in cases:
        try:
            got = reference(inp)
        except Invalid:
            if expected is not None:
                bad.append("%s: reference refused, case expects %s" % (name, expected["decision"]))
            continue
        if expected is None:
            bad.append("%s: reference decided, case expects refusal" % name)
            continue
        if got != expected:
            bad.append("%s: reference %r != case %r" % (name, got, expected))
    gen = generate(91091, 120)
    decisions = set()
    for inp in gen:
        try:
            decisions.add(reference(inp)["decision"])
        except Invalid as exc:
            bad.append("generator produced an invalid input: %s" % exc)
    if len(decisions) < 5:
        bad.append("generator covers only %d decisions: %s" % (len(decisions), sorted(decisions)))
    for line in bad:
        print("selftest FAIL %s" % line)
    print("selftest %d/%d hand cases, %d generated, %d decisions"
          % (len(cases) - len(bad), len(cases), len(gen), len(decisions)))
    return 0 if not bad else 2


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--candidate", default=CANDIDATE)
    ap.add_argument("--seed", type=int)
    ap.add_argument("--generated", type=int, default=120)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.root and a.revision and a.work):
        ap.error("--root, --revision and --work are required unless --selftest")
    root = os.path.realpath(a.root)
    rev = git(root, "rev-parse", "%s^{commit}" % a.revision).stdout.decode().strip()
    if not rev:
        print("C2v91 revision=? unresolved")
        return 2
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c91r-", dir=a.work)
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1, 2 ** 31)
    detail = {}
    try:
        # reference self-check before any candidate is scored
        cases = hand_cases()
        for name, inp, expected in cases:
            try:
                got = reference(inp)
            except Invalid:
                if expected is not None:
                    print("C2v91 reference drift on %s: refused, case expects %s"
                          % (name, expected["decision"]))
                    return 2
                continue
            if expected is None or got != expected:
                print("C2v91 reference drift on %s: %r" % (name, got))
                return 2
        gen_expected = [(inp, reference(inp)) for inp in generate(seed, a.generated)]
        tree = os.path.join(work, "tree")
        os.mkdir(tree)
        cand_present = git(root, "cat-file", "-e", "%s:%s" % (rev, a.candidate)).returncode == 0
        if not cand_present:
            print("C2v91 revision=%s candidate=absent hand=0/%d generated=0/%d forgeries_refused=0/%d "
                  "anti_table=n/a population=n/a seed=%d met=false"
                  % (rev, len(cases), a.generated, len(FORGERIES), seed))
            print(json.dumps({"reason": "candidate absent"}, sort_keys=True))
            return 1
        extract(root, rev, [a.candidate] + FORGERIES + [PINS_FILE], tree)
        pins = {}
        with open(os.path.join(tree, PINS_FILE)) as fh:
            for line in fh:
                h, _, p = line.strip().partition("  ")
                if p:
                    pins[p] = h
        drift = [p for p in FORGERIES if pins.get(p) != sha_file(os.path.join(tree, p))]
        pins_ok = (not drift) and sha_file(os.path.join(tree, PINS_FILE)) == PINS_SHA
        detail["population_drift"] = drift
        detail["pins_digest"] = sha_file(os.path.join(tree, PINS_FILE))
        cand_path = os.path.join(tree, a.candidate)
        src = open(cand_path, "rb").read().decode("utf-8", "replace")
        hits = []
        for name, inp, _ in cases:
            if sha_bytes(json.dumps(inp, sort_keys=True).encode())[:16] in src:
                hits.append("digest:" + name)
        for p in FORGERIES:
            stem = os.path.splitext(os.path.basename(p))[0]
            if stem in src:
                hits.append("stem:" + stem)
        detail["anti_table_hits"] = hits
        hand_ok, gen_ok, errors, failures = score_subject(cand_path, cases, gen_expected, work)
        refused = 0
        forgery_detail = {}
        for p in FORGERIES:
            fp = os.path.join(tree, p)
            h_ok, g_ok, errs, fails = score_subject(fp, cases, gen_expected, work)
            admitted = (h_ok == len(cases) and g_ok == a.generated and not errs)
            forgery_detail[p] = {"hand": h_ok, "generated": g_ok, "errors": len(errs),
                                 "admitted": admitted}
            if not admitted:
                refused += 1
        detail.update({"hand_failures": failures[:12], "errors": errors[:12],
                       "forgeries": forgery_detail,
                       "candidate_sha256": sha_file(cand_path)})
        met = (not drift and pins_ok and not hits and hand_ok == len(cases)
               and gen_ok == a.generated and refused == len(FORGERIES))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("C2v91 revision=%s candidate=present hand=%d/%d generated=%d/%d forgeries_refused=%d/%d "
          "anti_table=%s population=%s seed=%d met=%s"
          % (rev, hand_ok, len(cases), gen_ok, a.generated, refused, len(FORGERIES),
             "hit" if hits else "ok", "ok" if (pins_ok and not drift) else "drift", seed,
             str(met).lower()))
    print(json.dumps(detail, sort_keys=True))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
