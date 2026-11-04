"""Differential harness for scripts/stored_reuse.py (round-91 C2, seat ExecReuseTool).

Compares the candidate's evaluate() against the frozen counter's reference()
(``c91_reuse.py``, frozen bytes) over: the counter's 45 hand cases, its seeded
generated population (seed 91091, n=120), 20000 fuzzed inputs (valid and
malformed), and Age/max-age boundary sweeps. Acceptance-class and output
equality must hold everywhere; refusal reason texts are not compared.

Usage: python3 -B diff-harness.py [path/to/stored_reuse.py]
Default candidate path: <lane>/scripts/stored_reuse.py.
Exit 0 iff zero mismatches. The frozen counter is never modified.
"""
import importlib.util
import json
import random
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
COUNTER = LANE + "/.ufo/waves/round-91/c91_reuse.py"
TOOL = sys.argv[1] if len(sys.argv) > 1 else LANE + "/scripts/stored_reuse.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


counter = load("c91", COUNTER)
tool = load("sr", TOOL)

mismatches = 0
checked = 0


def compare(inp, tag):
    global mismatches, checked
    checked += 1
    try:
        e = counter.reference(inp)
        er = None
    except counter.Invalid as exc:
        e, er = None, str(exc)
    try:
        g = tool.evaluate(inp)
        gr = None
    except tool.InvalidInput as exc:
        g, gr = None, str(exc)
    if (e is None) != (g is None) or (e is not None and e != g):
        mismatches += 1
        print("MISMATCH", tag)
        print("  input :", json.dumps(inp, sort_keys=True)[:500])
        print("  ref   :", e, er)
        print("  tool  :", g, gr)


cases = counter.hand_cases()
for name, inp, expected in cases:
    compare(inp, "hand:" + name)

gen = counter.generate(91091, 120)
for i, inp in enumerate(gen):
    compare(inp, "gen%d" % i)

rng = random.Random(4242)
NAMES = ["Date", "Age", "Expires", "Cache-Control", "cache-control", "Vary", "X-A", "x-a", ""]
VALUES = ["1000000", "999000", "0", "-5", "abc", "", " 12 ", "1e3", "12.0",
          "9999999999999999999999", "*", "* , Accept", "Accept, *", "a\rb", "a\nb", "a\tb"]
CC = ["max-age=60", "max-age=abc", 'max-age="60"', "s-maxage=10", "min-fresh=5",
      "no-cache", "no-store", "must-revalidate", "proxy-revalidate", "private",
      "foo", "foo=bar", "max-stale", "max-stale=5", "max-stale=abc", "",
      "MAX-AGE=30", "max-age = 60", ",,", "max-age=60, max-age=60", "max-age=0",
      "only-if-cached", "s-maxage=0, max-age=1"]


def rand_cc():
    return ", ".join(rng.choice(CC) for _ in range(rng.randrange(0, 4)))


def rand_headers():
    h = {}
    for _ in range(rng.randrange(0, 4)):
        pick = rng.choice(NAMES)
        v = rand_cc() if pick in ("Cache-Control", "cache-control") else rng.choice(VALUES)
        h[pick] = v
    return h


def rand_input():
    inp = {"stored": {"status": rng.choice([200, 203, 301, 404, 500, 99, 600, True, "200", None]),
                      "headers": rand_headers()},
           "request": {"method": rng.choice(["GET", "HEAD", "POST", "get", "", 5, None]),
                       "headers": rand_headers()},
           "now": rng.choice([0, 999999, 1000000, 1000030, 1001000, -1, 1.5, True])}
    if rng.random() < 0.5:
        inp["shared"] = rng.choice([True, False, "yes", 1, None])
    if rng.random() < 0.1:
        inp[rng.choice(["extra", "Stored", "now "])] = 1
    return inp


for i in range(20000):
    compare(rand_input(), "fuzz%d" % i)

for age in range(-2, 9):
    for ma in (0, 1, 5, 60):
        for off in (-1, 0, 1, 5, 61):
            inp = {"stored": {"status": 200,
                              "headers": {"Date": "1000",
                                          "Cache-Control": "max-age=%d" % ma}},
                   "request": {"method": "GET", "headers": {}},
                   "now": max(0, 1000 + off)}
            compare(inp, "bnd%d" % age)
            inp["stored"]["headers"]["Age"] = str(age)
            compare(inp, "bnd-age%d" % age)

print("tool=%s" % TOOL)
print("checked=%d mismatches=%d" % (checked, mismatches))
sys.exit(1 if mismatches else 0)
