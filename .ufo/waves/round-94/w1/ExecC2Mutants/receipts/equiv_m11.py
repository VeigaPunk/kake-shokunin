#!/usr/bin/env python3
"""Exhaustive differential check: pos-good base vs mutant M11 decide()."""
import importlib.util
import itertools
import sys

base_path, mut_path = sys.argv[1], sys.argv[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


B = load("base_ev", base_path)
M = load("mut_ev", mut_path)


def run(mod, payload):
    try:
        return ("ok", mod.decide(payload))
    except Exception as exc:  # Bad or any other
        return ("exc", type(exc).__name__, str(exc))


methods = ["GET", "HEAD", "POST", "PUT"]
exists_v = [True, False]
etags = [None, '"a"', 'W/"a"']
lms = [None, 0, 5, 10]
ims_inm = [None, "*", '"a"', 'W/"a"']
dates = [None, 0, 5, 10, -1]
roles = [None, "origin", "cache"]
n = 0
diffs = []
for method, ex, et, lm, im, inm, ims, ius, role in itertools.product(
        methods, exists_v, etags, lms, ims_inm, ims_inm, dates, dates, roles):
    payload = {"method": method,
               "current": {"exists": ex, "etag": et, "last_modified": lm},
               "request": {"if_match": im, "if_none_match": inm,
                           "if_modified_since": ims, "if_unmodified_since": ius}}
    if role is not None:
        payload["role"] = role
    n += 1
    a, b = run(B, payload), run(M, payload)
    if a != b:
        diffs.append((payload, a, b))
print("cases=%d differing=%d" % (n, len(diffs)))
for d in diffs[:5]:
    print("DIFF", d)
