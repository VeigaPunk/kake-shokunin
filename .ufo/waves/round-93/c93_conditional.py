#!/usr/bin/env python3
"""Round-93 C2 counter: conditional request evaluation conformance (contract v1).

Frozen before data (`.ufo/waves/round-93/freeze.md`). Reads committed bytes at
--revision, scores the candidate against `.ufo/waves/round-93/c2-contract.md`
(30 hand cases + a seeded generated population decided by this file's own
reference) and requires every frozen forgery subject to be refused while the
frozen positive control is admitted.

Successor requirements this counter implements (round-92 routed defects R92-4,
R92-5): one hand case per contract clause and per refusal class, a
type-mismatch case for the int/bool clause, and the reference is checked against
the worked cases *before* any candidate is scored, so an oracle/contract drift
exits 2 rather than passing silently. The reference is never reachable from a
scored subject: each subject runs under an audit-hook sandbox that denies `open`
outside the subject's own directory and denies every import outside a frozen
allowlist, so an absolute-path import of this counter is refused by execution,
not by a text check.

met <=> candidate present
      AND population digest-ok (pins file digest and every frozen subject digest)
      AND anti_table ok (no hand-case input digest and no forgery stem in the source)
      AND hand cases all decided as declared
      AND generated cases all decided as the reference decides
      AND every forgery subject refused (scored met=false)
      AND the positive control admitted

Output line 1:
  C2v93 revision=<sha> candidate=present|absent hand=H/H generated=G/G
        forgeries_refused=F/F positive=admitted|refused anti_table=ok|hit
        population=ok|drift seed=<n> met=true|false
line 2: JSON detail. Exit 0 iff met; 2 on reference/case drift; 1 otherwise.
--selftest runs the isolated fixture battery and asserts its own exit code.
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

BASE = "10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5"
CANDIDATE = "scripts/conditional_eval.py"
PINS_FILE = ".ufo/waves/round-93/frozen/c2-population.sha256"
PINS_SHA = "9c45db5c7f7d05f4d9a4930bbd9c84e8d1b75c28b0ebbc9018124bd8b3606869"
POSITIVE = ".ufo/waves/round-93/frozen/pos-good.py"
FORGERIES = [
    ".ufo/waves/round-93/frozen/neg-blanket-200.py",
    ".ufo/waves/round-93/frozen/neg-blanket-304.py",
    ".ufo/waves/round-93/frozen/neg-weak-strong-swap.py",
    ".ufo/waves/round-93/frozen/neg-ignore-precedence.py",
    ".ufo/waves/round-93/frozen/neg-oracle-import.py",
    ".ufo/waves/round-93/frozen/neg-pin-reader.py",
]
TOP_KEYS = {"method", "current", "request", "role"}
CUR_KEYS = {"exists", "etag", "last_modified"}
REQ_KEYS = {"if_match", "if_none_match", "if_modified_since", "if_unmodified_since"}
TCHAR = re.compile(r"[!#$%&'*+\-.^_`|~0-9A-Za-z]+")
ETAGC = set("!") | {chr(c) for c in range(0x23, 0x7F)}


class Invalid(Exception):
    pass


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def parse_etag(s):
    """Clause 3. Returns (weak, opaque)."""
    weak = s.startswith("W/")
    rest = s[2:] if weak else s
    if len(rest) < 2 or rest[0] != '"' or rest[-1] != '"':
        raise Invalid("malformed entity-tag")
    opaque = rest[1:-1]
    for ch in opaque:
        if ch not in ETAGC:
            raise Invalid("malformed entity-tag")
    return weak, opaque


def parse_list(value):
    """Clause 4. Returns '*' or a list of (weak, opaque)."""
    s = value.strip(" \t")
    if s == "*":
        return "*"
    if not s:
        raise Invalid("empty precondition field value")
    out = []
    for part in s.split(","):
        p = part.strip(" \t")
        if not p:
            raise Invalid("empty list member")
        if p == "*":
            raise Invalid('"*" mixed with entity tags')
        out.append(parse_etag(p))
    return out


def strong(a, b):
    return (not a[0]) and (not b[0]) and a[1] == b[1]


def weak(a, b):
    return a[1] == b[1]


def reference(inp, swap=None):
    """swap='comparison' flips the two comparison functions (drift fixture)."""
    if not isinstance(inp, dict):
        raise Invalid("input is not an object")
    if set(inp) - TOP_KEYS:
        raise Invalid("unexpected top-level key")
    for key in ("method", "current", "request"):
        if key not in inp:
            raise Invalid("missing %s" % key)
    method = inp["method"]
    if not isinstance(method, str) or not TCHAR.fullmatch(method):
        raise Invalid("method is not a token")
    cur = inp["current"]
    if not isinstance(cur, dict) or set(cur) != CUR_KEYS:
        raise Invalid("current is not the declared object")
    req = inp["request"]
    if not isinstance(req, dict) or set(req) != REQ_KEYS:
        raise Invalid("request is not the declared object")
    exists = cur["exists"]
    if not isinstance(exists, bool):
        raise Invalid("exists is not a bool")
    etag = cur["etag"]
    if etag is not None and not isinstance(etag, str):
        raise Invalid("etag is neither null nor a string")
    lastmod = cur["last_modified"]
    if lastmod is not None and (not is_int(lastmod) or lastmod < 0):
        raise Invalid("last_modified is neither null nor a non-negative int")
    if not exists and (etag is not None or lastmod is not None):
        raise Invalid("absent representation carries a validator")
    values = {}
    for key in sorted(REQ_KEYS):
        v = req[key]
        if v is None:
            values[key] = None
        elif key in ("if_match", "if_none_match"):
            if not isinstance(v, str):
                raise Invalid("%s is neither null nor a string" % key)
            values[key] = parse_list(v)
        elif not is_int(v) or v < 0:
            raise Invalid("%s is neither null nor a non-negative int" % key)
        else:
            values[key] = v
    role = inp.get("role", "origin")
    if role not in ("origin", "cache"):
        raise Invalid("role is not origin or cache")
    cur_tag = parse_etag(etag) if etag is not None else None

    if swap == "comparison":
        strong_f, weak_f = weak, strong
    else:
        strong_f, weak_f = strong, weak

    im = values["if_match"]
    ius = values["if_unmodified_since"]
    inm = values["if_none_match"]
    ims = values["if_modified_since"]

    def matches(spec, cmp):
        if spec == "*":
            return exists
        if not exists or cur_tag is None:
            return False
        return any(cmp(t, cur_tag) for t in spec)

    if role == "origin":
        if im is not None:
            if not matches(im, strong_f):
                return {"decision": "412", "precondition": "if_match"}
        elif ius is not None and lastmod is not None:
            if not lastmod <= ius:
                return {"decision": "412", "precondition": "if_unmodified_since"}
    if inm is not None:
        if matches(inm, weak_f):
            if method in ("GET", "HEAD"):
                return {"decision": "304", "precondition": "if_none_match"}
            return {"decision": "412", "precondition": "if_none_match"}
    elif ims is not None and method in ("GET", "HEAD") and lastmod is not None:
        if lastmod <= ims:
            return {"decision": "304", "precondition": "if_modified_since"}
    return {"decision": "200", "precondition": None}


def C(name, method, exists, etag, lastmod, req, expected, role=None):
    inp = {"method": method,
           "current": {"exists": exists, "etag": etag, "last_modified": lastmod},
           "request": dict({"if_match": None, "if_none_match": None,
                            "if_modified_since": None, "if_unmodified_since": None},
                           **req)}
    if role is not None:
        inp["role"] = role
    return (name, inp, expected)


def OK(dec, pre=None):
    return {"decision": dec, "precondition": pre}


def hand_cases():
    """30 worked cases. `expected` is the exact output object, or None for a refusal."""
    c = []
    # clause 8 — If-Match, strong comparison (RFC 9110 §8.8.3.2 Table 3)
    c.append(C("ifmatch/exact-match", "PUT", True, '"1"', 500, {"if_match": '"1"'}, OK("200")))
    c.append(C("ifmatch/weak-tag-no-strong-match", "PUT", True, '"1"', 500,
               {"if_match": 'W/"1"'}, OK("412", "if_match")))
    c.append(C("ifmatch/strong-vs-weak-current", "PUT", True, 'W/"1"', 500,
               {"if_match": '"1"'}, OK("412", "if_match")))
    c.append(C("ifmatch/list-second-member", "PUT", True, '"b"', 500,
               {"if_match": '"a", "b"'}, OK("200")))
    c.append(C("ifmatch/star-with-representation", "PUT", True, None, None,
               {"if_match": "*"}, OK("200")))
    c.append(C("ifmatch/star-without-representation", "PUT", False, None, None,
               {"if_match": "*"}, OK("412", "if_match")))
    c.append(C("ifmatch/list-no-member", "DELETE", True, '"z"', 500,
               {"if_match": '"a", "b"'}, OK("412", "if_match")))
    c.append(C("ifmatch/skipped-for-cache", "PUT", True, '"z"', 500,
               {"if_match": '"a"'}, OK("200"), role="cache"))
    # clause 9 — If-Unmodified-Since
    c.append(C("ius/older-modification-passes", "PUT", True, None, 500,
               {"if_unmodified_since": 600}, OK("200")))
    c.append(C("ius/equal-passes", "PUT", True, None, 600,
               {"if_unmodified_since": 600}, OK("200")))
    c.append(C("ius/newer-fails", "PUT", True, None, 700,
               {"if_unmodified_since": 600}, OK("412", "if_unmodified_since")))
    c.append(C("ius/ignored-when-last-modified-absent", "PUT", True, None, None,
               {"if_unmodified_since": 0}, OK("200")))
    c.append(C("ius/ignored-when-if-match-present", "PUT", True, '"1"', 700,
               {"if_match": '"1"', "if_unmodified_since": 600}, OK("200")))
    c.append(C("ius/skipped-for-cache", "PUT", True, None, 700,
               {"if_unmodified_since": 600}, OK("200"), role="cache"))
    # clause 10 — If-None-Match, weak comparison
    c.append(C("inm/match-get", "GET", True, '"1"', 500,
               {"if_none_match": '"1"'}, OK("304", "if_none_match")))
    c.append(C("inm/weak-member-matches-strong-current", "GET", True, '"1"', 500,
               {"if_none_match": 'W/"1"'}, OK("304", "if_none_match")))
    c.append(C("inm/weak-current-matches-strong-member", "GET", True, 'W/"1"', 500,
               {"if_none_match": '"1"'}, OK("304", "if_none_match")))
    c.append(C("inm/both-weak-different", "GET", True, 'W/"1"', 500,
               {"if_none_match": 'W/"2"'}, OK("200")))
    c.append(C("inm/match-post-412", "POST", True, '"1"', 500,
               {"if_none_match": '"1"'}, OK("412", "if_none_match")))
    c.append(C("inm/star-with-representation", "GET", True, '"1"', 500,
               {"if_none_match": "*"}, OK("304", "if_none_match")))
    c.append(C("inm/star-without-representation", "GET", False, None, None,
               {"if_none_match": "*"}, OK("200")))
    c.append(C("inm/no-match", "GET", True, '"1"', 500,
               {"if_none_match": '"2", "3"'}, OK("200")))
    c.append(C("inm/precedes-if-modified-since", "GET", True, '"1"', 500,
               {"if_none_match": '"2"', "if_modified_since": 900}, OK("200")))
    c.append(C("inm/ignored-when-current-etag-absent", "GET", True, None, 500,
               {"if_none_match": '"1"'}, OK("200")))
    # clause 11 — If-Modified-Since
    c.append(C("ims/equal-304", "GET", True, None, 500,
               {"if_modified_since": 500}, OK("304", "if_modified_since")))
    c.append(C("ims/later-value-304", "GET", True, None, 500,
               {"if_modified_since": 900}, OK("304", "if_modified_since")))
    c.append(C("ims/earlier-value-200", "HEAD", True, None, 500,
               {"if_modified_since": 400}, OK("200")))
    c.append(C("ims/ignored-for-post", "POST", True, None, 500,
               {"if_modified_since": 900}, OK("200")))
    c.append(C("ims/ignored-when-last-modified-absent", "GET", True, None, None,
               {"if_modified_since": 900}, OK("200")))
    c.append(C("ims/ignored-when-if-none-match-present", "GET", True, None, 500,
               {"if_none_match": '"9"', "if_modified_since": 900}, OK("200")))
    # clauses 1-4 — refusals
    extra = {"method": "GET",
             "current": {"exists": True, "etag": '"1"', "last_modified": 500},
             "request": {"if_match": None, "if_none_match": None,
                         "if_modified_since": None, "if_unmodified_since": None},
             "role_hint": "origin"}
    c.append(("refuse/unknown-top-key", extra, None))
    c.append(C("refuse/method-not-token", "G ET", True, '"1"', 500, {}, None))
    c.append(C("refuse/exists-not-bool", "GET", 1, '"1"', 500, {}, None))
    c.append(C("refuse/last-modified-bool", "GET", True, '"1"', True, {}, None))
    c.append(C("refuse/etag-unquoted", "GET", True, '"1', 500,
               {"if_none_match": '"1"'}, None))
    c.append(C("refuse/etag-bad-char", "GET", True, '"a b"', 500, {}, None))
    c.append(C("refuse/star-mixed", "GET", True, '"1"', 500,
               {"if_none_match": '*, "1"'}, None))
    c.append(C("refuse/empty-member", "GET", True, '"1"', 500,
               {"if_none_match": '"1", , "2"'}, None))
    c.append(C("refuse/empty-value", "GET", True, '"1"', 500, {"if_match": "  "}, None))
    c.append(C("refuse/absent-with-etag", "GET", False, '"1"', None, {}, None))
    c.append(C("refuse/date-as-string-not-int", "GET", True, None, 500,
               {"if_modified_since": "400"}, None))
    c.append(C("refuse/date-bool", "GET", True, None, 500,
               {"if_unmodified_since": False}, None))
    c.append(C("refuse/negative-date", "GET", True, None, -5, {}, None))
    c.append(C("refuse/role-unknown", "GET", True, '"1"', 500, {}, None, role="proxy"))
    return c


def generate(seed, n):
    rng = random.Random(seed)
    methods = ["GET", "HEAD", "PUT", "POST", "DELETE", "PATCH", "OPTIONS"]
    tags = ['"a"', 'W/"a"', '"b"', 'W/"b"', '"c"']
    out = []
    for _ in range(n):
        exists = rng.random() < 0.8
        etag = rng.choice(tags) if exists and rng.random() < 0.75 else None
        lastmod = (rng.randrange(0, 10 ** 6) if exists and rng.random() < 0.8 else None)
        req = {}
        for key in ("if_match", "if_none_match"):
            r = rng.random()
            if r < 0.30:
                req[key] = "*"
            elif r < 0.70:
                req[key] = ", ".join(rng.choice(tags) for _ in range(rng.randrange(1, 3)))
            else:
                req[key] = None
        for key in ("if_modified_since", "if_unmodified_since"):
            req[key] = rng.randrange(0, 10 ** 6) if rng.random() < 0.35 else None
        inp = {"method": rng.choice(methods),
               "current": {"exists": exists, "etag": etag, "last_modified": lastmod},
               "request": req}
        if rng.random() < 0.4:
            inp["role"] = rng.choice(["origin", "cache"])
        out.append(inp)
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


def reference_selfcheck(cases):
    """Exit 2 on any drift between the reference and a worked case."""
    for name, inp, expected in cases:
        try:
            got = reference(inp)
        except Invalid:
            if expected is not None:
                return "reference drift on %s: refused, case expects %s" % (
                    name, expected["decision"])
            continue
        if expected is None or got != expected:
            return "reference drift on %s: %r" % (name, got)
    return None


def selftest(argv=None):
    """Isolated fixture battery: the reference, a drifted reference, the positive
    control and every forgery are scored, and the exit code is asserted."""
    work = None
    try:
        work = os.path.join(os.environ.get("TMPDIR", "/tmp"), "c93sel-%d" % os.getpid())
        os.makedirs(work, exist_ok=True)
        tree = os.path.join(work, "tree")
        os.mkdir(tree)
        sandbox = os.path.join(work, "sandbox.py")
        with open(sandbox, "w") as fh:
            fh.write(SANDBOX)
        cases = hand_cases()
        drift = reference_selfcheck(cases)
        if drift:
            print("selftest FAIL: %s" % drift)
            return 1
        if reference(cases[0][1], swap="comparison") == cases[0][2] and \
                all(reference(i, swap="comparison") == e for _, i, e in cases if e):
            print("selftest FAIL: drifted reference agrees with every case")
            return 1
        drift_cases = [n for n, i, e in cases
                       if e is not None and reference(i, swap="comparison") != e]
        if not drift_cases:
            print("selftest FAIL: no case distinguishes the drifted reference")
            return 1
        here = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.abspath(os.path.join(here, "..", "..", ".."))
        gen_expected = []
        for inp in generate(93, 40):
            try:
                gen_expected.append((inp, reference(inp)))
            except Invalid:
                continue
        ok = 0
        total = 0
        for rel, want_admitted in [(POSITIVE, True)] + [(f, False) for f in FORGERIES]:
            src = os.path.join(repo_root, rel)
            if not os.path.exists(src):
                print("selftest FAIL: missing fixture %s" % rel)
                return 1
            total += 1
            dest = os.path.join(tree, os.path.basename(rel))
            shutil.copyfile(src, dest)
            h, g, fails = score_subject(work, dest, cases, gen_expected, sandbox)
            admitted = h == len(cases) and g == len(gen_expected) and not fails
            if admitted == want_admitted:
                ok += 1
            else:
                print("selftest FAIL: %s admitted=%s wanted=%s hand=%d/%d gen=%d/%d %s"
                      % (rel, admitted, want_admitted, h, len(cases), g,
                         len(gen_expected), (fails or [""])[0][:160]))
        print("selftest %d/%d fixtures scored as declared; drifted-reference cases=%d"
              % (ok, total, len(drift_cases)))
        return 0 if ok == total else 1
    finally:
        if work:
            shutil.rmtree(work, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--candidate", default=CANDIDATE)
    ap.add_argument("--generated", type=int, default=120)
    ap.add_argument("--seed", type=int, default=93)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.root and a.revision and a.work):
        ap.error("--root, --revision and --work are required")
    root = os.path.realpath(a.root)
    rev = git(root, "rev-parse", "%s^{commit}" % a.revision).stdout.decode().strip()
    if not rev:
        print("C2v93 revision=? unresolved")
        return 2
    seed = a.seed
    os.makedirs(a.work, exist_ok=True)
    work = os.path.join(a.work, "c93c-%d" % os.getpid())
    os.makedirs(work, exist_ok=True)
    detail = {"seed": seed}
    try:
        cases = hand_cases()
        drift = reference_selfcheck(cases)
        if drift:
            print("C2v93 reference drift: %s" % drift)
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
            print("C2v93 revision=%s candidate=absent hand=0/%d generated=0/%d "
                  "forgeries_refused=0/%d positive=refused anti_table=n/a population=n/a "
                  "seed=%d met=false"
                  % (rev, len(cases), a.generated, len(FORGERIES), seed))
            print(json.dumps({"reason": "candidate absent"}, sort_keys=True))
            return 1
        for path in [a.candidate, POSITIVE] + FORGERIES + [PINS_FILE]:
            blob = show(root, rev, path)
            if blob is None:
                print("C2v93 revision=%s population=drift missing=%s met=false"
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
        pinned = FORGERIES + [POSITIVE]
        drift_paths = [p for p in pinned if pins.get(p) != sha_file(os.path.join(tree, p))]
        pins_ok = (not drift_paths) and sha_file(os.path.join(tree, PINS_FILE)) == PINS_SHA
        detail["population_drift"] = drift_paths
        detail["pins_digest"] = sha_file(os.path.join(tree, PINS_FILE))
        cand_path = os.path.join(tree, a.candidate)
        src = open(cand_path, "rb").read().decode("utf-8", "replace")
        hits = []
        for name, inp, _ in cases:
            if sha_bytes(json.dumps(inp, sort_keys=True).encode())[:16] in src:
                hits.append("digest:" + name)
        for p in FORGERIES + [POSITIVE]:
            stem = os.path.splitext(os.path.basename(p))[0]
            if stem in src:
                hits.append("stem:" + stem)
        detail["anti_table_hits"] = hits
        hand_ok, gen_ok, failures = score_subject(work, cand_path, cases, gen_expected,
                                                  sandbox)
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
        pp = os.path.join(tree, POSITIVE)
        ph, pg, pfails = score_subject(work, pp, cases, gen_expected, sandbox)
        positive_ok = (ph == len(cases) and pg == len(gen_expected) and not pfails)
        detail.update({"hand_failures": failures[:12],
                       "forgeries": forgery_detail,
                       "positive": {"hand": ph, "generated": pg,
                                    "admitted": positive_ok,
                                    "first_failure": pfails[0] if pfails else ""},
                       "candidate_sha256": sha_file(cand_path)})
        met = (not drift_paths and pins_ok and not hits and hand_ok == len(cases)
               and gen_ok == len(gen_expected) and refused == len(FORGERIES)
               and positive_ok)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print("C2v93 revision=%s candidate=present hand=%d/%d generated=%d/%d "
          "forgeries_refused=%d/%d positive=%s anti_table=%s population=%s seed=%d met=%s"
          % (rev, hand_ok, len(cases), gen_ok, len(gen_expected), refused, len(FORGERIES),
             "admitted" if positive_ok else "refused", "hit" if hits else "ok",
             "ok" if (pins_ok and not drift_paths) else "drift", seed, str(met).lower()))
    print(json.dumps(detail, sort_keys=True))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
