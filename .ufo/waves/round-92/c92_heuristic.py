#!/usr/bin/env python3
"""Round-92 C2 counter: heuristic freshness decision conformance (contract v1).

Frozen before data (`.ufo/waves/round-92/freeze.md`). Reads committed bytes at
--revision, scores the candidate against `.ufo/waves/round-92/c2-contract.md`
(28 hand cases + a seeded generated population decided by this file's own
reference) and requires every frozen forgery subject to be refused.

Successor requirements this counter implements (round-91 routed defects R91-2,
K91-6): the reference is never reachable from a scored subject — each subject runs
under an audit-hook sandbox that denies `open` outside the subject's own directory
and denies every import outside a frozen allowlist, so an absolute-path import of
this counter (`frozen/neg-oracle-import.py`) is refused by execution, not by a
text check; the anti-table conjunct is exercised by a frozen subject rather than
being an unfalsified assertion; and the population pins are checked against the
frozen pins-file digest named below.

met <=> candidate present
      AND population digest-ok (pins file digest and every forgery digest)
      AND anti_table ok (no hand-case input digest and no forgery stem in the source)
      AND hand cases all decided as declared
      AND generated cases all decided as the reference decides
      AND every forgery subject refused (scored met=false).

Output line 1:
  C2v92 revision=<sha> candidate=present|absent hand=H/H generated=G/G
        forgeries_refused=F/F anti_table=ok|hit population=ok|drift seed=<n> met=true|false
line 2: JSON detail. Exit 0 iff met; 2 on reference/case drift; 1 otherwise.
Scratch: --work (required); everything created beneath it and removed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys

BASE = "e143faff1b86aad172dd87696da900c70347b8b2"
CANDIDATE = "scripts/heuristic_freshness.py"
PINS_FILE = ".ufo/waves/round-92/frozen/c2-population.sha256"
PINS_SHA = "b780fa2457d619951dd81db6edfa0d3c540e0b6cf7a381b73b555df3ff7cec76"
FORGERIES = [
    ".ufo/waves/round-92/frozen/neg-blanket-admit.py",
    ".ufo/waves/round-92/frozen/neg-blanket-refuse.py",
    ".ufo/waves/round-92/frozen/neg-status-table.py",
    ".ufo/waves/round-92/frozen/neg-pin-reader.py",
    ".ufo/waves/round-92/frozen/neg-oracle-import.py",
]
HEURISTICALLY_CACHEABLE = (200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501)
KEYS_OUT = {"decision", "lifetime", "heuristic"}
TOP_KEYS = {"stored", "now", "shared"}
DELTA = ("max-age", "s-maxage")


class Invalid(Exception):
    pass


def ascii_lower(s):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in s)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def parse_cc(value):
    """Clause 4. Returns {name: arg-or-None}."""
    out = {}
    for raw in value.split(","):
        d = raw.strip(" \t")
        if not d:
            raise Invalid("empty Cache-Control directive")
        name, sep, arg = d.partition("=")
        name = ascii_lower(name.strip(" \t"))
        if not name:
            raise Invalid("empty Cache-Control directive name")
        if sep:
            arg = arg.strip(" \t")
            if len(arg) >= 2 and arg[0] == '"' and arg[-1] == '"':
                arg = arg[1:-1]
            if name in DELTA and not re.fullmatch(r"[0-9]+", arg):
                raise Invalid("delta-seconds argument is not a bare non-negative integer")
        else:
            arg = None
        if name in out and out[name] != arg:
            raise Invalid("conflicting Cache-Control directive %s" % name)
        out[name] = arg
    return out


def norm_headers(raw):
    """Clauses 1-3."""
    if not isinstance(raw, dict):
        raise Invalid("headers is not an object")
    seen = {}
    out = {}
    for name, value in raw.items():
        if not isinstance(name, str) or not isinstance(value, str):
            raise Invalid("header name or value is not a string")
        if any(c in value for c in "\r\n\0"):
            raise Invalid("header value contains CR, LF or NUL")
        low = ascii_lower(name)
        if low in seen:
            raise Invalid("duplicate header name")
        seen[low] = name
        out[low] = value.strip(" \t")
    return out


def delta(headers, name):
    v = headers.get(name)
    if v is None:
        return None
    if not re.fullmatch(r"[0-9]+", v):
        raise Invalid("%s is not a decimal integer" % name)
    return int(v)


def reference(inp):
    if not isinstance(inp, dict):
        raise Invalid("input is not an object")
    if set(inp) - TOP_KEYS:
        raise Invalid("unexpected top-level key")
    stored = inp.get("stored")
    if not isinstance(stored, dict) or set(stored) - {"status", "headers"}:
        raise Invalid("stored is not the declared object")
    status = stored.get("status")
    if not is_int(status) or not 100 <= status <= 599:
        raise Invalid("status is not an int in 100..599")
    now = inp.get("now")
    if not is_int(now) or now < 0:
        raise Invalid("now is not a non-negative int")
    shared = inp.get("shared", False)
    if not isinstance(shared, bool):
        raise Invalid("shared is not a bool")
    headers = norm_headers(stored.get("headers", {}))
    cc = parse_cc(headers["cache-control"]) if "cache-control" in headers else {}
    if "date" not in headers:
        raise Invalid("Date is absent")
    if not re.fullmatch(r"[0-9]+", headers["date"]):
        raise Invalid("Date is not a decimal integer")
    date = int(headers["date"])
    expires = delta(headers, "expires")
    lastmod = delta(headers, "last-modified")
    smaxage = None
    if "s-maxage" in cc:
        if not re.fullmatch(r"[0-9]+", cc["s-maxage"] or ""):
            raise Invalid("s-maxage is not a decimal integer")
        smaxage = int(cc["s-maxage"])
    maxage = None
    if "max-age" in cc:
        if not re.fullmatch(r"[0-9]+", cc["max-age"] or ""):
            raise Invalid("max-age is not a decimal integer")
        maxage = int(cc["max-age"])

    # clause 9: not-storable
    vary_star = False
    if "vary" in headers:
        vary_star = any(m.strip(" \t") == "*" for m in headers["vary"].split(","))
    if ("no-store" in cc or ("private" in cc and shared) or vary_star):
        return {"decision": "not-storable", "lifetime": None, "heuristic": False}

    # clause 10: explicit
    if shared and smaxage is not None:
        return {"decision": "explicit", "lifetime": smaxage, "heuristic": False}
    if maxage is not None:
        return {"decision": "explicit", "lifetime": maxage, "heuristic": False}
    if expires is not None:
        return {"decision": "explicit", "lifetime": expires - date, "heuristic": False}

    # clause 11: heuristically cacheable
    if status not in HEURISTICALLY_CACHEABLE and "public" not in cc:
        return {"decision": "not-heuristically-cacheable", "lifetime": None,
                "heuristic": False}

    # clause 12 / 13
    if lastmod is not None and lastmod <= date:
        return {"decision": "heuristic",
                "lifetime": min((date - lastmod) // 10, 86400), "heuristic": True}
    return {"decision": "heuristic-undecided", "lifetime": None, "heuristic": False}


def H(name, status, headers, expected, now=1000000, shared=None):
    inp = {"stored": {"status": status, "headers": headers}, "now": now}
    if shared is not None:
        inp["shared"] = shared
    return (name, inp, expected)


def hand_cases():
    """28 worked cases. `expected` is the exact output object, or None for a refusal."""
    C = []
    # clause 10 — explicit wins, heuristics never used
    C.append(H("explicit/max-age", 200, {"Date": "1000000", "Cache-Control": "max-age=600",
                                         "Last-Modified": "900000"},
               {"decision": "explicit", "lifetime": 600, "heuristic": False}))
    C.append(H("explicit/s-maxage-shared", 200,
               {"Date": "1000000", "Cache-Control": "s-maxage=120, max-age=600"},
               {"decision": "explicit", "lifetime": 120, "heuristic": False}, shared=True))
    C.append(H("explicit/s-maxage-ignored-private", 200,
               {"Date": "1000000", "Cache-Control": "s-maxage=120, max-age=600"},
               {"decision": "explicit", "lifetime": 600, "heuristic": False}, shared=False))
    C.append(H("explicit/expires-minus-date", 200,
               {"Date": "1000000", "Expires": "1000300", "Last-Modified": "900000"},
               {"decision": "explicit", "lifetime": 300, "heuristic": False}))
    C.append(H("explicit/expires-before-date-negative", 200,
               {"Date": "1000000", "Expires": "999900"},
               {"decision": "explicit", "lifetime": -100, "heuristic": False}))
    C.append(H("explicit/max-age-beats-expires", 200,
               {"Date": "1000000", "Expires": "1000300", "Cache-Control": "max-age=5"},
               {"decision": "explicit", "lifetime": 5, "heuristic": False}))
    # clause 12 — heuristic arithmetic and its boundaries
    C.append(H("heuristic/ten-percent", 200,
               {"Date": "1000000", "Last-Modified": "990000"},
               {"decision": "heuristic", "lifetime": 1000, "heuristic": True}))
    C.append(H("heuristic/floor", 200,
               {"Date": "1000000", "Last-Modified": "999989"},
               {"decision": "heuristic", "lifetime": 1, "heuristic": True}))
    C.append(H("heuristic/floor-below-one", 200,
               {"Date": "1000000", "Last-Modified": "999999"},
               {"decision": "heuristic", "lifetime": 0, "heuristic": True}))
    C.append(H("heuristic/equal-timestamps", 200,
               {"Date": "1000000", "Last-Modified": "1000000"},
               {"decision": "heuristic", "lifetime": 0, "heuristic": True}))
    C.append(H("heuristic/cap-86400", 200,
               {"Date": "1000000", "Last-Modified": "100000"},
               {"decision": "heuristic", "lifetime": 86400, "heuristic": True}))
    C.append(H("heuristic/cap-exact-boundary", 200,
               {"Date": "1864000", "Last-Modified": "1000000"},
               {"decision": "heuristic", "lifetime": 86400, "heuristic": True}))
    C.append(H("heuristic/just-below-cap", 200,
               {"Date": "1863999", "Last-Modified": "1000000"},
               {"decision": "heuristic", "lifetime": 86399, "heuristic": True}))
    # clause 11 — the cacheability gate
    C.append(H("gate/404-heuristically-cacheable", 404,
               {"Date": "1000000", "Last-Modified": "990000"},
               {"decision": "heuristic", "lifetime": 1000, "heuristic": True}))
    C.append(H("gate/500-not-cacheable", 500,
               {"Date": "1000000", "Last-Modified": "990000"},
               {"decision": "not-heuristically-cacheable", "lifetime": None,
                "heuristic": False}))
    C.append(H("gate/500-public-overrides", 500,
               {"Date": "1000000", "Cache-Control": "public", "Last-Modified": "990000"},
               {"decision": "heuristic", "lifetime": 1000, "heuristic": True}))
    C.append(H("gate/200-no-last-modified", 200, {"Date": "1000000"},
               {"decision": "heuristic-undecided", "lifetime": None, "heuristic": False}))
    C.append(H("gate/last-modified-after-date", 200,
               {"Date": "1000000", "Last-Modified": "1000001"},
               {"decision": "heuristic-undecided", "lifetime": None, "heuristic": False}))
    # clause 9 — not-storable
    C.append(H("store/no-store", 200,
               {"Date": "1000000", "Cache-Control": "no-store", "Last-Modified": "990000"},
               {"decision": "not-storable", "lifetime": None, "heuristic": False}))
    C.append(H("store/private-shared", 200,
               {"Date": "1000000", "Cache-Control": "private", "Last-Modified": "990000"},
               {"decision": "not-storable", "lifetime": None, "heuristic": False},
               shared=True))
    C.append(H("store/private-not-shared", 200,
               {"Date": "1000000", "Cache-Control": "private", "Last-Modified": "990000"},
               {"decision": "heuristic", "lifetime": 1000, "heuristic": True}, shared=False))
    C.append(H("store/vary-star", 200,
               {"Date": "1000000", "Vary": "Accept-Encoding, *", "Last-Modified": "990000"},
               {"decision": "not-storable", "lifetime": None, "heuristic": False}))
    C.append(H("store/vary-members-not-star", 200,
               {"Date": "1000000", "Vary": "Accept-Encoding, User-Agent",
                "Last-Modified": "990000"},
               {"decision": "heuristic", "lifetime": 1000, "heuristic": True}))
    # clause 1-7 — refusals
    C.append(H("refuse/date-absent", 200, {"Last-Modified": "990000"}, None))
    C.append(H("refuse/date-non-integer", 200, {"Date": "1e6"}, None))
    C.append(H("refuse/duplicate-header-name", 200,
               {"Date": "1000000", "date": "1000000"}, None))
    C.append(H("refuse/delta-seconds-signed", 200,
               {"Date": "1000000", "Cache-Control": "max-age=+5"}, None))
    C.append(H("refuse/empty-directive", 200,
               {"Date": "1000000", "Cache-Control": "max-age=5, "}, None))
    return C


def generate(seed, n):
    rng = random.Random(seed)
    statuses = [200, 203, 204, 206, 300, 301, 308, 404, 405, 410, 414, 501, 500, 502, 403]
    out = []
    for _ in range(n):
        date = rng.randrange(0, 2 * 10 ** 9)
        headers = {"Date": str(date)}
        if rng.random() < 0.55:
            headers["Last-Modified"] = str(date - rng.randrange(-5, 2 * 10 ** 6))
        if rng.random() < 0.30:
            headers["Expires"] = str(date + rng.randrange(-100, 10 ** 6))
        cc = []
        if rng.random() < 0.30:
            cc.append("max-age=%d" % rng.randrange(0, 10 ** 5))
        if rng.random() < 0.20:
            cc.append("s-maxage=%d" % rng.randrange(0, 10 ** 5))
        if rng.random() < 0.12:
            cc.append(rng.choice(["public", "no-store", "private", "no-cache",
                                  "must-revalidate", "immutable"]))
        if rng.random() < 0.12:
            cc.append("foo=bar")
        if cc:
            headers["Cache-Control"] = ", ".join(cc)
        if rng.random() < 0.10:
            headers["Vary"] = rng.choice(["Accept-Encoding", "*", "User-Agent, *"])
        if rng.random() < 0.10:
            headers["Age"] = str(rng.randrange(0, 10 ** 5))
        out.append({"stored": {"status": rng.choice(statuses), "headers": headers},
                    "now": rng.randrange(0, 2 * 10 ** 9),
                    "shared": rng.random() < 0.5})
    return out


SANDBOX = r'''
import importlib.machinery, importlib.util, json, os, pkgutil, runpy, sys

subject = sys.argv[1]
root = os.path.dirname(os.path.abspath(subject))
allowed = set("""json sys os re math collections functools itertools decimal fractions
typing dataclasses enum string unicodedata operator copy bisect heapq array struct textwrap
pprint numbers abc contextlib weakref types warnings traceback linecache tokenize token keyword
builtins codecs encodings io errno stat posixpath genericpath time datetime hashlib random
binascii base64 runpy importlib importlib.machinery importlib.util pkgutil zipimport marshal
_collections_abc _io""".split())
prefixes = tuple(p for p in {sys.prefix, sys.base_prefix, os.path.dirname(os.__file__)} if p)


def hook(event, args):
    if event == "open":
        p = args[0]
        if isinstance(p, (bytes, bytearray)):
            p = p.decode("utf-8", "replace")
        if isinstance(p, int):
            return
        if not isinstance(p, str):
            return
        ap = os.path.abspath(p)
        if ap == os.path.abspath(subject) or ap.startswith(root + os.sep):
            return
        if ap.startswith(prefixes):
            return
        raise PermissionError("sandbox: open outside the subject tree: %s" % ap)
    elif event == "import":
        name = args[0]
        if name.split(".")[0] not in allowed:
            raise PermissionError("sandbox: import denied: %s" % name)
    elif event in ("os.system", "subprocess.Popen", "os.spawn", "os.posix_spawn"):
        raise PermissionError("sandbox: process creation denied: %s" % event)


sys.addaudithook(hook)
sys.argv = [subject]
sys.path[:] = [root]
runpy.run_path(subject, run_name="__main__")
'''


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, "rb") as fh:
        return sha_bytes(fh.read())


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True)


def show(root, rev, path):
    p = git(root, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def run_subject(work, path, inp, sandbox):
    payload = json.dumps(inp, sort_keys=True).encode()
    try:
        p = subprocess.run([sys.executable, "-B", sandbox, path], input=payload,
                           capture_output=True, timeout=60, cwd=work,
                           env={"PATH": "/usr/bin:/bin", "HOME": work})
    except subprocess.TimeoutExpired:
        return None, "timeout"
    out = p.stdout.decode("utf-8", "replace")
    err = p.stderr.decode("utf-8", "replace").strip()
    if p.returncode == 0:
        if not out.strip():
            return None, "empty stdout"
        try:
            return json.loads(out), None
        except ValueError:
            return None, "non-JSON stdout"
    return None, "rc=%d %s" % (p.returncode, err[:120])


def score_subject(work, path, cases, gen_expected, sandbox):
    hand_ok = 0
    failures = []
    for name, inp, expected in cases:
        got, why = run_subject(work, path, inp, sandbox)
        if expected is None:
            if got is None:
                hand_ok += 1
            else:
                failures.append("%s: expected refusal, got %r" % (name, got))
            continue
        if got == expected:
            hand_ok += 1
        else:
            failures.append("%s: expected %r got %r%s" % (
                name, expected, got, "" if why is None else " (%s)" % why))
    gen_ok = 0
    for inp, expected in gen_expected:
        got, why = run_subject(work, path, inp, sandbox)
        if got == expected:
            gen_ok += 1
        elif len(failures) < 40:
            failures.append("generated: expected %r got %r%s" % (
                expected, got, "" if why is None else " (%s)" % why))
    return hand_ok, gen_ok, failures


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--candidate", default=CANDIDATE)
    ap.add_argument("--generated", type=int, default=120)
    ap.add_argument("--seed", type=int, default=92)
    a = ap.parse_args(argv)
    if not (a.root and a.revision and a.work):
        ap.error("--root, --revision and --work are required")
    root = os.path.realpath(a.root)
    rev = git(root, "rev-parse", "%s^{commit}" % a.revision).stdout.decode().strip()
    if not rev:
        print("C2v92 revision=? unresolved")
        return 2
    seed = a.seed
    os.makedirs(a.work, exist_ok=True)
    work = os.path.join(a.work, "c92h-%d" % os.getpid())
    os.makedirs(work, exist_ok=True)
    detail = {"seed": seed}
    try:
        # reference self-check before any candidate is scored
        cases = hand_cases()
        for name, inp, expected in cases:
            try:
                got = reference(inp)
            except Invalid:
                if expected is not None:
                    print("C2v92 reference drift on %s: refused, case expects %s"
                          % (name, expected["decision"]))
                    return 2
                continue
            if expected is None or got != expected:
                print("C2v92 reference drift on %s: %r" % (name, got))
                return 2
        gen_expected = []
        for inp in generate(seed, a.generated):
            try:
                gen_expected.append((inp, reference(inp)))
            except Invalid:
                continue
        tree = os.path.join(work, "tree")
        os.mkdir(tree)
        sandbox = os.path.join(work, "sandbox.py")
        with open(sandbox, "w") as fh:
            fh.write(SANDBOX)
        cand_present = git(root, "cat-file", "-e", "%s:%s" % (rev, a.candidate)).returncode == 0
        if not cand_present:
            print("C2v92 revision=%s candidate=absent hand=0/%d generated=0/%d "
                  "forgeries_refused=0/%d anti_table=n/a population=n/a seed=%d met=false"
                  % (rev, len(cases), a.generated, len(FORGERIES), seed))
            print(json.dumps({"reason": "candidate absent"}, sort_keys=True))
            return 1
        for path in [a.candidate] + FORGERIES + [PINS_FILE]:
            blob = show(root, rev, path)
            if blob is None:
                print("C2v92 revision=%s population=drift missing=%s met=false"
                      % (rev, path))
                print(json.dumps({"reason": "missing " + path}, sort_keys=True))
                return 1
            dest = os.path.join(tree, path)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as fh:
                fh.write(blob)
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
        hand_ok, gen_ok, failures = score_subject(work, cand_path, cases, gen_expected, sandbox)
        refused = 0
        forgery_detail = {}
        for p in FORGERIES:
            fp = os.path.join(tree, p)
            h_ok, g_ok, fails = score_subject(work, fp, cases, gen_expected, sandbox)
            admitted = (h_ok == len(cases) and g_ok == len(gen_expected) and not fails)
            forgery_detail[p] = {"hand": h_ok, "generated": g_ok, "admitted": admitted,
                                 "first_failure": fails[0] if fails else ""}
            if not admitted:
                refused += 1
        detail.update({"hand_failures": failures[:12],
                       "forgeries": forgery_detail,
                       "candidate_sha256": sha_file(cand_path)})
        met = (not drift and pins_ok and not hits and hand_ok == len(cases)
               and gen_ok == len(gen_expected) and refused == len(FORGERIES))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("C2v92 revision=%s candidate=present hand=%d/%d generated=%d/%d "
          "forgeries_refused=%d/%d anti_table=%s population=%s seed=%d met=%s"
          % (rev, hand_ok, len(cases), gen_ok, len(gen_expected), refused, len(FORGERIES),
             "hit" if hits else "ok", "ok" if (pins_ok and not drift) else "drift", seed,
             str(met).lower()))
    print(json.dumps(detail, sort_keys=True))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
