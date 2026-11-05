#!/usr/bin/env python3
"""Round-97 C2 counter: revalidation exchange, contract v1 (successor of c96_reval.py).

Successor changes (routed R96-1, R96-2, R96-3 git pin; frozen in
`.ufo/waves/round-97/freeze.md` before any seat scores):
  * R96-1: main() binds the mutant population (the round-96 counter crashed
    with NameError at line 624 on every candidate-present run).
  * Committed bytes only: the pins file, every pinned fixture, the mutant
    population and base are read at --revision (no HEAD / working-tree
    fallback); git is /usr/bin/git with GIT_NO_REPLACE_OBJECTS=1.
  * R96-2: held-out generated cases whose seed is derived from the scored
    commit id (a candidate cannot table inputs keyed on the hash of the
    commit that contains it); the anti-table also searches raw canonical and
    minified JSON texts, sha256/sha1/md5 hex digests of both forms, their
    alternate-nibble halves and base64/urlsafe-base64 digest encodings.
  * one more frozen forgery: neg-lookup-table.py (answers memorized for
    every hand and fixed-seed generated input; default otherwise).

The round-96 docstring follows; its clauses hold unless amended above.

Frozen before data (`.ufo/waves/round-96/freeze.md`). New decision instrument
over supplied values only (RFC 9111 section 4.3): which precondition header
fields a cache constructs for a stored response (clause C1/C2) and how it
handles the received validation response (clauses C3-C5), with the C6 refusal
classes. Contract: `.ufo/waves/round-96/reval-contract-v1.md`. The candidate
is `scripts/reval_exchange.py` (absent at the round base — the wave builds
it); the positive control and the six forgeries are frozen beside this file;
the mutant population patches the frozen positive-control bytes.

met <=> candidate present
      AND population digest-ok (pins file digest and every pinned fixture)
      AND anti_table ok (no hand-case input digest, no generated-case input
          digest, and no forgery stem in the candidate source — R95-8)
      AND hand cases all decided as declared (contract v1)
      AND generated cases all decided as the reference decides
      AND held-out cases (seed = int(revision[:15], 16)) all decided as the
          reference decides
      AND every forgery subject refused (6/6)
      AND the positive control admitted
      AND every scored mutant killed.

Output line 1:
  C2v97 revision=<sha> candidate=present|absent hand=H/H generated=G/G
        heldout=X/X forgeries_refused=F/7 positive=admitted|refused
        mutants=killed/14 survivors=none|<ids> anti_table=ok|hit
        population=ok|drift seed=97 met=true|false
line 2: JSON detail. Exit 0 iff met; 2 on reference/case/population drift;
1 otherwise.
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

BASE = "36d148f5c60100021304903c30e5663207c72f4f"
CANDIDATE = "scripts/reval_exchange.py"
PINS_FILE = ".ufo/waves/round-96/frozen/c2-population.sha256"
PINS_SHA = "d9c8f96eec5c98565a3c75350d425770efa012b76e5e8151f4daec7d8d50c4e9"
POSITIVE = ".ufo/waves/round-96/frozen/pos-good-reval.py"
FORGERIES = [
    ".ufo/waves/round-96/frozen/neg-blanket-construct.py",
    ".ufo/waves/round-96/frozen/neg-blanket-update.py",
    ".ufo/waves/round-96/frozen/neg-swap-precedence.py",
    ".ufo/waves/round-96/frozen/neg-refuse-all.py",
    ".ufo/waves/round-96/frozen/neg-oracle-import.py",
    ".ufo/waves/round-96/frozen/neg-pin-reader.py",
    ".ufo/waves/round-97/frozen/neg-lookup-table.py",
]
MUTANTS_JSON = ".ufo/waves/round-96/frozen/mutants-reval.json"
MUTANT_BASE = ".ufo/waves/round-96/frozen/pos-good-reval.py"
SEED = 97
GENERATED = 120
HELDOUT = 60
SELFTEST_HELDOUT_SEED = 9797
LOOKUP_SHA = "898df9a2ce5ea7713d3d5c33ada13250a667c490eccbaf642556295ca9c460cc"
GIT = "/usr/bin/git"
TOP_KEYS = {"stored", "received_status"}
STORED_KEYS = {"exists", "etag", "last_modified"}
ETAGC = {chr(0x21)} | {chr(c) for c in range(0x23, 0x7F)} \
    | {chr(c) for c in range(0x80, 0x100)}


class Invalid(Exception):
    pass


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def parse_etag(s):
    weak = s.startswith("W/")
    rest = s[2:] if weak else s
    if len(rest) < 2 or rest[0] != '"' or rest[-1] != '"':
        raise Invalid("malformed entity-tag")
    for ch in rest[1:-1]:
        if ch not in ETAGC:
            raise Invalid("malformed entity-tag")
    return s


def _no_duplicate_keys(pairs):
    seen = set()
    for k, _ in pairs:
        if k in seen:
            raise Invalid("duplicate object key in input document")
        seen.add(k)
    return dict(pairs)


def reference(inp):
    """The contract-v1 reference decision."""
    if not isinstance(inp, dict):
        raise Invalid("input is not an object")
    if set(inp) != TOP_KEYS:
        raise Invalid("unexpected or missing top-level keys")
    stored = inp["stored"]
    if not isinstance(stored, dict) or set(stored) != STORED_KEYS:
        raise Invalid("stored is not the declared object")
    exists = stored["exists"]
    if not isinstance(exists, bool):
        raise Invalid("exists is not a bool")
    etag = stored["etag"]
    if etag is not None:
        if not isinstance(etag, str) or not etag:
            raise Invalid("etag is neither null nor a string")
        parse_etag(etag)
    lm = stored["last_modified"]
    if lm is not None and (not is_int(lm) or lm < 0):
        raise Invalid("last_modified is neither null nor a non-negative int")
    status = inp["received_status"]
    if status is not None:
        if not is_int(status):
            raise Invalid("received_status is neither null nor an int")
        if not 100 <= status <= 599:
            raise Invalid("received_status out of 100..599")
        if status < 200:
            raise Invalid("1xx is interim and never a validation response")
    has_validator = etag is not None or lm is not None
    if exists is False and has_validator:
        raise Invalid("absent representation carries a validator")
    if status is not None and not has_validator:
        raise Invalid("validation response without a stored validator")
    if status is None:
        if not has_validator:
            return {"decision": "cannot-revalidate",
                    "if_none_match": None, "if_modified_since": None}
        return {"decision": "construct",
                "if_none_match": etag,
                "if_modified_since": lm}
    if status == 304:
        return {"decision": "update-stored",
                "if_none_match": None, "if_modified_since": None}
    if 500 <= status <= 599:
        return {"decision": "may-reuse-stored",
                "if_none_match": None, "if_modified_since": None}
    return {"decision": "replace-stored",
            "if_none_match": None, "if_modified_since": None}


def C(name, exists, etag, lastmod, status, expected):
    inp = {"stored": {"exists": exists, "etag": etag, "last_modified": lastmod},
           "received_status": status}
    return (name, inp, expected)


def RAW(name, payload, expected=None):
    return (name, {"__raw__": payload}, expected)


def OK(dec, inm=None, ims=None):
    return {"decision": dec, "if_none_match": inm, "if_modified_since": ims}


def hand_cases():
    """Worked cases; expected None means the subject must refuse."""
    c = []
    # clause C1/C2 — construction
    c.append(C("construct/both-validators", True, '"v1"', 500, None,
               OK("construct", '"v1"', 500)))
    c.append(C("construct/etag-only", True, '"abc"', None, None,
               OK("construct", '"abc"', None)))
    c.append(C("construct/lm-only", True, None, 12345, None,
               OK("construct", None, 12345)))
    c.append(C("construct/weak-etag-verbatim", True, 'W/"v2"', 700, None,
               OK("construct", 'W/"v2"', 700)))
    c.append(C("construct/neither-validator", True, None, None, None,
               OK("cannot-revalidate")))
    c.append(C("construct/etag-zero-lm", True, '"z"', 0, None,
               OK("construct", '"z"', 0)))
    c.append(C("construct/obs-text-etag", True, '"caf\xe9"', None, None,
               OK("construct", '"caf\xe9"', None)))
    # clause C3 — 304
    c.append(C("c304/with-etag", True, '"v1"', 500, 304, OK("update-stored")))
    c.append(C("c304/lm-only", True, None, 500, 304, OK("update-stored")))
    # clause C4 — 5xx
    c.append(C("c5xx/500", True, '"v1"', 500, 500, OK("may-reuse-stored")))
    c.append(C("c5xx/503-lm-only", True, None, 42, 503, OK("may-reuse-stored")))
    c.append(C("c5xx/599-upper-edge", True, '"v"', None, 599,
               OK("may-reuse-stored")))
    # clause C5 — full-response class
    c.append(C("c200/replace", True, '"v1"', 500, 200, OK("replace-stored")))
    c.append(C("c404/replace", True, '"v1"', 500, 404, OK("replace-stored")))
    c.append(C("c410/replace", True, None, 9, 410, OK("replace-stored")))
    c.append(C("c302/replace", True, '"v"', 5, 302, OK("replace-stored")))
    c.append(C("c499/replace-upper-edge", True, '"v"', None, 499,
               OK("replace-stored")))
    # clause C6 — refusals
    c.append(C("refuse/1xx-interim", True, '"v"', 1, 100, None))
    c.append(C("refuse/status-600", True, '"v"', 1, 600, None))
    c.append(C("refuse/status-99", True, '"v"', 1, 99, None))
    c.append(C("refuse/status-not-int", True, '"v"', 1, "304", None))
    c.append(C("refuse/status-bool", True, '"v"', 1, True, None))
    c.append(C("refuse/etag-not-string", True, 5, 1, None, None))
    c.append(C("refuse/etag-unquoted", True, "v1", 1, None, None))
    c.append(C("refuse/etag-quoted-control", True, '"a\x01b"', 1, None, None))
    c.append(C("refuse/lm-negative", True, None, -1, None, None))
    c.append(C("refuse/lm-not-int", True, None, "yesterday", None, None))
    c.append(C("refuse/validators-without-representation", False, '"v"', 1,
               None, None))
    c.append(C("refuse/status-without-validator", True, None, None, 304, None))
    c.append(C("refuse/exists-not-bool", "yes", None, 1, None, None))
    c.append(RAW("refuse/unknown-top-key",
                 b'{"stored": {"exists": true, "etag": null, '
                 b'"last_modified": null}, "received_status": null, '
                 b'"extra": 1}', None))
    c.append(RAW("refuse/missing-stored-key",
                 b'{"stored": {"exists": true, "etag": null}, '
                 b'"received_status": null}', None))
    c.append(RAW("refuse/raw-dup-bytes",
                 b'{"stored": {"exists": true, "etag": null, '
                 b'"last_modified": null}, "received_status": null, '
                 b'"received_status": 304}', None))
    c.append(RAW("refuse/raw-nested-dup",
                 b'{"stored": {"exists": true, "etag": null, '
                 b'"last_modified": 1, "last_modified": 2}, '
                 b'"received_status": null}', None))
    c.append(RAW("refuse/raw-not-json", b'not json at all', None))
    c.append(RAW("refuse/raw-empty", b'', None))
    c.append(RAW("refuse/raw-array", b'[1,2]', None))
    return c


def generate(seed, count):
    rng = random.Random(seed)
    tags = ['"t1"', '"t2"', 'W/"t3"', '"caf\xe94"']
    out = []
    for _ in range(count):
        exists = rng.random() < 0.85
        etag = rng.choice(tags) if exists and rng.random() < 0.7 else None
        lm = (rng.randrange(0, 10 ** 6) if exists and rng.random() < 0.8
              else None)
        status = None
        r = rng.random()
        if r < 0.45:
            status = rng.choice([200, 204, 302, 304, 404, 410, 499, 500, 503,
                                 599])
        inp = {"stored": {"exists": exists, "etag": etag, "last_modified": lm},
               "received_status": status}
        out.append(inp)
    return out


SANDBOX = r'''
import importlib.machinery, importlib.util, json, os, pkgutil, runpy, sys

subject = os.path.realpath(sys.argv[1])
root = os.path.dirname(subject)
allowed = set("""json sys os re math collections functools itertools decimal fractions
typing dataclasses enum string unicodedata operator copy bisect heapq array struct textwrap
pprint numbers abc contextlib weakref types warnings traceback linecache tokenize token keyword
builtins codecs encodings io errno stat posixpath genericpath time datetime hashlib random
binascii base64 runpy importlib importlib.machinery importlib.util pkgutil zipimport marshal
_collections_abc _io""".split())
prefixes = tuple(p for p in {os.path.realpath(sys.prefix),
                             os.path.realpath(sys.base_prefix),
                             os.path.dirname(os.path.realpath(os.__file__))}
                 if p)


def hook(event, args):
    if event == "open":
        p = args[0]
        if isinstance(p, (bytes, bytearray)):
            p = p.decode("utf-8", "replace")
        if isinstance(p, int):
            return
        if not isinstance(p, str):
            return
        ap = os.path.realpath(p)
        if ap == subject or ap.startswith(root + os.sep):
            return
        if ap.startswith(prefixes):
            return
        raise PermissionError("sandbox: open outside the subject tree: %s" % ap)
    elif event == "import":
        name = args[0]
        if name.split(".")[0] not in allowed:
            raise PermissionError("sandbox: import denied: %s" % name)
    elif event in ("os.system", "subprocess.Popen", "os.spawn", "os.posix_spawn",
                   "os.exec", "os.fork"):
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
    env = {"PATH": "/usr/bin:/bin", "GIT_NO_REPLACE_OBJECTS": "1",
           "HOME": os.environ.get("HOME", "/"), "LC_ALL": "C",
           "GIT_CONFIG_NOSYSTEM": "1"}
    return subprocess.run([GIT, "-C", root, *args], capture_output=True,
                          env=env)


def show(root, rev, path):
    p = git(root, "show", "%s:%s" % (rev, path))
    return p.stdout if p.returncode == 0 else None


def run_subject(work, path, inp, sandbox):
    if isinstance(inp, dict) and "__raw__" in inp:
        payload = inp["__raw__"]
    else:
        payload = json.dumps(inp, sort_keys=True).encode()
    try:
        p = subprocess.run([sys.executable, "-I", "-B", sandbox,
                            os.path.realpath(path)], input=payload,
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


def score_subject(work, path, cases, gen_expected, sandbox, gen_limit=None):
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
    gen = gen_expected if gen_limit is None else gen_expected[:gen_limit]
    gen_ok = 0
    for inp, expected in gen:
        got, why = run_subject(work, path, inp, sandbox)
        if got == expected:
            gen_ok += 1
        elif len(failures) < 40:
            failures.append("generated: expected %r got %r%s" % (
                expected, got, "" if why is None else " (%s)" % why))
    return hand_ok, gen_ok, failures, len(gen)


def reference_selfcheck(cases):
    for name, inp, expected in cases:
        if isinstance(inp, dict) and "__raw__" in inp:
            continue
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


def load_mutants(blob):
    data = json.loads(blob.decode("utf-8"))
    if isinstance(data, dict) and "mutants" in data:
        return data["mutants"]
    if isinstance(data, list):
        return data
    raise Invalid("unrecognised mutant population shape")


def mutant_cases(work, sandbox, cases, gen_expected, base_src, mutants, tree):
    killed = []
    survivors = []
    notes = {}
    for m in mutants:
        mid = m["id"]
        find, replace = m["find"], m["replace"]
        if base_src.count(find) != 1:
            return None, None, None, "mutant %s find-string occurs %d times" % (
                mid, base_src.count(find))
        src = base_src.replace(find, replace, 1)
        dest = os.path.join(tree, "mut-%s.py" % mid)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(src)
        h_ok, g_ok, fails, g_total = score_subject(
            work, dest, cases, gen_expected, sandbox, gen_limit=40)
        is_killed = bool(fails)
        (killed if is_killed else survivors).append(mid)
        notes[mid] = {"killed": is_killed,
                      "first_failure": fails[0][:160] if fails else ""}
    return killed, survivors, notes, None


def _forms(inp):
    if isinstance(inp, dict) and "__raw__" in inp:
        return [inp["__raw__"]]
    return [json.dumps(inp, sort_keys=True).encode(),
            json.dumps(inp, sort_keys=True, separators=(",", ":")).encode(),
            json.dumps(inp, sort_keys=True, ensure_ascii=False).encode("utf-8")]


def input_digests(cases, gen_expected):
    """R96-2: needles a memorizing candidate would carry. Raw texts of the
    structured inputs (>= 24 bytes, so short refusal payloads such as `[1,2]`
    are not needles), then digest encodings of every form."""
    import base64
    digs = set()
    inputs = [inp for _, inp, _ in cases] + [inp for inp, _ in gen_expected]
    for inp in inputs:
        for form in _forms(inp):
            if len(form) >= 24:
                digs.add(form.decode("utf-8", "replace"))
            for h in (hashlib.sha256(form), hashlib.sha1(form),
                      hashlib.md5(form)):
                hx = h.hexdigest()
                digs.update({hx, hx[::2], hx[1::2]})
                raw = h.digest()
                for enc in (base64.b64encode(raw), base64.urlsafe_b64encode(raw)):
                    e = enc.decode()
                    digs.update({e, e.rstrip("=")})
    return digs


FORGERY_STEMS = ["neg-blanket-construct", "neg-blanket-update",
                 "neg-swap-precedence", "neg-refuse-all", "neg-oracle-import",
                 "neg-pin-reader", "neg-lookup-table", "pos-good-reval"]


def anti_table(candidate_src, digs):
    """R95-8: full digests of hand AND generated case inputs, plus the
    frozen subject stems (a candidate that names a forgery or the positive
    control is tailoring, not deciding)."""
    hits = []
    for d in digs:
        if d in candidate_src:
            hits.append(d)
    stem_hits = [s for s in FORGERY_STEMS if s in candidate_src]
    return hits, stem_hits


def check_pins(root, pins_blob, rev):
    """Returns drift list. pins file lines: <sha256>  <path>; read at rev."""
    drift = []
    pin_lines = [l for l in pins_blob.decode().splitlines() if l.strip()]
    for line in pin_lines:
        want, _, rel = line.partition("  ")
        rel = rel.strip()
        blob = show(root, "HEAD", rel)
        if blob is None:
            drift.append("missing pinned fixture %s" % rel)
        elif sha_bytes(blob) != want:
            drift.append("digest drift on %s" % rel)
    return drift, len(pin_lines)


def selftest(argv=None):
    base_tmp = None
    try:
        base_tmp = os.path.join(os.environ.get("TMPDIR", "/tmp"),
                                "c97rsel-%d" % os.getpid())
        work = os.path.join(base_tmp, "w")
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
        here = os.path.dirname(os.path.abspath(__file__))
        repo_root = os.path.abspath(os.path.join(here, "..", "..", ".."))
        gen_expected = []
        for inp in generate(SEED, 40):
            try:
                gen_expected.append((inp, reference(inp)))
            except Invalid:
                continue
        heldout = []
        for inp in generate(SELFTEST_HELDOUT_SEED, 30):
            try:
                heldout.append((inp, reference(inp)))
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
            h, g, fails, g_total = score_subject(work, dest, cases,
                                                 gen_expected + heldout, sandbox)
            admitted = h == len(cases) and g == g_total and not fails
            if admitted == want_admitted:
                ok += 1
            else:
                print("selftest FAIL: %s admitted=%s wanted=%s hand=%d/%d "
                      "gen=%d/%d %s"
                      % (rel, admitted, want_admitted, h, len(cases), g,
                         g_total, (fails or [""])[0][:200]))
        mutants = load_mutants(open(os.path.join(repo_root, MUTANTS_JSON),
                                    "rb").read())
        base_src = open(os.path.join(repo_root, MUTANT_BASE), "r",
                        encoding="utf-8").read()
        killed, survivors, notes, mdrift = mutant_cases(
            work, sandbox, cases, gen_expected, base_src, mutants, tree)
        if mdrift:
            print("selftest FAIL: %s" % mdrift)
            return 1
        digs = input_digests(cases, gen_expected)
        pos_src = open(os.path.join(repo_root, POSITIVE), "r",
                       encoding="utf-8").read()
        hits, stem_hits = anti_table(pos_src, digs)
        anti_ok = not hits and not stem_hits
        print("selftest %d/%d fixtures scored as declared; mutants killed "
              "%d/%d survivors=%s; anti_table=%s; generated-vs-reference "
              "seeded cases=%d"
              % (ok, total, len(killed), len(killed) + len(survivors),
                 ",".join(survivors) or "none", "ok" if anti_ok else "hit",
                 len(gen_expected)))
        return 0 if (ok == total and not survivors and anti_ok) else 1
    finally:
        if base_tmp:
            shutil.rmtree(base_tmp, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--work", required=True)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root or ".")
    if a.selftest:
        return selftest()
    if not a.revision:
        print("C2v97 revision=? population=drift met=false")
        print(json.dumps({"error": "--revision required"}))
        return 2
    p = git(root, "rev-parse", "--verify", "%s^{commit}" % a.revision)
    if p.returncode != 0:
        print("C2v97 revision=%s population=drift met=false" % a.revision)
        print(json.dumps({"error": "unresolvable revision"}))
        return 2
    rev = p.stdout.decode().strip()
    pins_blob = show(root, rev, PINS_FILE) or b""
    if sha_bytes(pins_blob) != PINS_SHA:
        print("C2v97 revision=%s population=drift met=false" % rev)
        print(json.dumps({"pins_digest": sha_bytes(pins_blob),
                          "expected": PINS_SHA}, sort_keys=True))
        return 2
    drift, pin_count = check_pins(root, pins_blob, rev)
    b = show(root, rev, FORGERIES[-1])
    if b is None or sha_bytes(b) != LOOKUP_SHA:
        drift.append("digest drift on %s" % FORGERIES[-1])
    if drift:
        print("C2v97 revision=%s population=drift met=false" % rev)
        print(json.dumps({"drift": drift}, sort_keys=True))
        return 2
    cases = hand_cases()
    mutants = load_mutants(show(root, rev, MUTANTS_JSON))
    n_mut = len(mutants)
    candidate = show(root, rev, CANDIDATE)
    if candidate is None:
        print("C2v97 revision=%s candidate=absent hand=0/%d generated=0/%d "
              "heldout=0/%d forgeries_refused=0/%d positive=refused mutants=0/%d "
              "survivors=none anti_table=ok population=ok seed=%d met=false"
              % (rev, len(cases), GENERATED, HELDOUT, len(FORGERIES), n_mut,
                 SEED))
        print(json.dumps({"detail": "candidate absent"}, sort_keys=True))
        return 1
    drift = reference_selfcheck(cases)
    if drift:
        print("C2v97 revision=%s population=drift met=false" % rev)
        print(json.dumps({"drift": drift}, sort_keys=True))
        return 2
    gen_expected = []
    for inp in generate(SEED, GENERATED):
        try:
            gen_expected.append((inp, reference(inp)))
        except Invalid:
            continue
    heldout = []
    for inp in generate(int(rev[:15], 16), HELDOUT):
        try:
            heldout.append((inp, reference(inp)))
        except Invalid:
            continue
    work = os.path.abspath(a.work)
    os.makedirs(work, exist_ok=True)
    tree = os.path.join(work, "tree")
    shutil.rmtree(tree, ignore_errors=True)
    os.makedirs(tree, exist_ok=True)
    sandbox = os.path.join(work, "sandbox.py")
    with open(sandbox, "w") as fh:
        fh.write(SANDBOX)
    src_text = candidate.decode("utf-8", "replace")
    digs = input_digests(cases, gen_expected)
    at_hits, at_stems = anti_table(src_text, digs)
    anti_ok = not at_hits and not at_stems

    dest = os.path.join(tree, "candidate.py")
    with open(dest, "wb") as fh:
        fh.write(candidate)
    h_ok, g_ok, fails, g_total = score_subject(work, dest, cases,
                                               gen_expected, sandbox)
    _, x_ok, x_fails, x_total = score_subject(work, dest, [], heldout, sandbox)
    fails = fails + x_fails

    def score_fixture(rel, want_admitted):
        blob = show(root, rev, rel)
        if blob is None:
            return False, False, ["fixture absent at revision: %s" % rel]
        d = os.path.join(tree, os.path.basename(rel))
        with open(d, "wb") as fh:
            fh.write(blob)
        fh_, g_, fails_, gt = score_subject(work, d, cases,
                                            gen_expected + heldout, sandbox)
        admitted = fh_ == len(cases) and g_ == gt and not fails_
        return admitted == want_admitted, admitted, fails_

    pos_ok, pos_admitted, pos_fails = score_fixture(POSITIVE, True)
    refused = 0
    forge_notes = {}
    for rel in FORGERIES:
        ok_, admitted_, fails_ = score_fixture(rel, False)
        refused += 1 if ok_ else 0
        forge_notes[os.path.basename(rel)] = {
            "refused_ok": ok_, "admitted": admitted_,
            "first": (fails_ or [""])[0][:120]}

    base_src = show(root, rev, MUTANT_BASE).decode("utf-8")
    killed, survivors, notes, mdrift = mutant_cases(
        work, sandbox, cases, gen_expected, base_src, mutants, tree)
    if mdrift:
        print("C2v97 revision=%s population=drift met=false" % rev)
        print(json.dumps({"drift": mdrift}, sort_keys=True))
        return 2

    hand_total = len(cases)
    met = (h_ok == hand_total and g_ok == g_total and x_ok == x_total
           and refused == len(FORGERIES) and pos_admitted and not survivors
           and anti_ok)
    print("C2v97 revision=%s candidate=present hand=%d/%d generated=%d/%d "
          "heldout=%d/%d forgeries_refused=%d/%d positive=%s mutants=%d/%d "
          "survivors=%s anti_table=%s population=ok seed=%d met=%s"
          % (rev, h_ok, hand_total, g_ok, g_total, x_ok, x_total, refused,
             len(FORGERIES),
             "admitted" if pos_admitted else "refused", len(killed),
             len(killed) + len(survivors), ",".join(survivors) or "none",
             "ok" if anti_ok else "hit", SEED, str(met).lower()))
    print(json.dumps({"hand_failures": fails[:10], "forge": forge_notes,
                      "mutants": {k: v for k, v in list(notes.items())[:20]},
                      "anti_hits": sorted(at_hits)[:5], "anti_stems": at_stems,
                      "pins": pin_count}, sort_keys=True))
    shutil.rmtree(tree, ignore_errors=True)
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
