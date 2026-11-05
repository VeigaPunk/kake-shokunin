#!/usr/bin/env python3
"""Input generator + differential runner for ExecTwinStale (kake round 98, C2).

Generator is written from stale-contract.md only (no counter code consulted).
Usage: python3 gen.py --count 2400 --seed 98 --work <scratch> --out <seat dir>

Writes into --out:  diff-run.txt, disagreements.jsonl
Writes into --work: inputs.jsonl (every input, base64-free: hex for raw bytes)

Every input runs through twin.py and the counter's oracle as CLIs, identical stdin.
Targeted cases carry expectations hand-derived from the contract; any run that
disagrees with its own expectation is reported with the expectation column.
"""
import argparse
import sys

sys.set_int_max_str_digits(0)  # targeted expectations contain 5000-digit integers
import base64
import concurrent.futures as cf
import json
import pathlib
import random
import subprocess
import sys

LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
ORACLE = LANE / ".ufo/waves/round-98/frozen/pos-oracle.py"
SEAT = pathlib.Path(__file__).resolve().parent
TWIN = SEAT / "twin.py"

# ---------------------------------------------------------------- pools
NAMES = [
    "no-cache", "NO-CACHE", "No-Cache", "no-cach", "no_cache", "no-cache-x",
    "must-revalidate", "Must-Revalidate", "proxy-revalidate", "s-maxage", "S-MAXAGE",
    "stale-while-revalidate", "Stale-While-Revalidate", "STALE-WHILE-REVALIDATE",
    "stale-if-error", "Stale-If-Error", "stale-if-error2",
    "max-age", "MAX-AGE", "max-stale", "min-fresh", "only-if-cached",
    "no-store", "private", "public", "immutable", "x-ext", "x", "",
]
VALUES = [
    None, "0", "1", "5", "10", "12", "59", "100", "599", "600", "1200",
    "2147483647", "2147483648", "2147483649", "4294967296",
    "99999999999999999999", "00012", "000", "0005",
    "5s", "-1", "+5", "1.5", "1e3", "0x10", "abc",
    "\"5\"", "\"\"", "\"a,b\"", "\"x\\\"y\"", "\"5", "5\"", "\" 5\"", "\"no-cache\"",
    "\u0663", "\u00b2", "\u00e9", "\u20ac", "a\\b", "\"a\\\"", "\"\\\"",
    "\x01", "\x7f", "\x80", "\x9f", "\xa0", "\xff", "\u0100",
    "\"a\" x", "x y", "a=b", "5 ", " 5", "\t5",
    "\"" + "9" * 40 + "\"", "9" * 40, "0" * 300 + "5", "9" * 5000,
]
EQ_FORMS = ["=", "=", "=", "=", "= ", " =", " = ", "=\t", "==", "=="]
SEPS = [", ", ",", " , ", ",\t", ",,", ", ,", ",  ", ", \t"]
MUTATE_CHARS = list('"\\,=; \t\x01\x7f\x80\xa0\xff\u0100\u0663\u00b2\u00e9()/@:[]{}?<>\n\r0-+.9x')


def mutate(rng, s):
    op = rng.randrange(3)
    pos = rng.randrange(len(s) + 1)
    ch = rng.choice(MUTATE_CHARS)
    if op == 0:
        return s[:pos] + ch + s[pos:]
    if op == 1 and s:
        p = min(pos, len(s) - 1)
        return s[:p] + s[p + 1:]
    return s[:pos] + ch + s[pos + 1:]


CLEAN_NAMES = [
    "no-cache", "NO-CACHE", "must-revalidate", "proxy-revalidate", "s-maxage",
    "stale-while-revalidate", "Stale-While-Revalidate", "stale-if-error", "STALE-IF-ERROR",
    "max-age", "no-store", "private", "public", "immutable", "x-ext",
]
CLEAN_VALUES = [
    None, "0", "1", "5", "10", "12", "59", "100", "599", "600", "1200",
    "2147483647", "2147483648", "2147483649", "00012", "\"5\"", "\"\"", "\"a,b\"", "\"x\\\"y\"",
]


def rand_cc_clean(rng):
    """Well-formed Cache-Control with occasional valid-but-odd spacing; few refusals."""
    k = rng.choice([0, 1, 1, 2, 2, 3, 4, 5])
    parts = []
    for _ in range(k):
        name = rng.choice(CLEAN_NAMES)
        val = rng.choice(CLEAN_VALUES)
        parts.append(name if val is None else name + "=" + val)
    s = ""
    for i, p in enumerate(parts):
        if i:
            s += rng.choice([", ", ",", " , ", ",\t"])
        s += p
    return s


def rand_cc(rng):
    """Dirty generator: deliberately malformed and odd tokens."""
    k = rng.choice([0, 1, 1, 2, 2, 3, 4, 5, 6])
    parts = []
    for _ in range(k):
        name = rng.choice(NAMES)
        if rng.random() < 0.40:
            el = name
        else:
            el = name + rng.choice(EQ_FORMS) + (rng.choice(VALUES) or "")
        if rng.random() < 0.08:
            el += rng.choice([" ", "\t", "  ", ""])
        if rng.random() < 0.05:
            el = rng.choice([" ", "\t"]) + el
        parts.append(el)
    s = ""
    for i, p in enumerate(parts):
        if i:
            s += rng.choice(SEPS)
        s += p
    if rng.random() < 0.05:
        s = rng.choice([",", " ,", ",,x", "", " ", "\t"]) + s
    if rng.random() < 0.05:
        s += rng.choice([",", " ,", "  ", ", "])
    if rng.random() < 0.06:
        s = mutate(rng, s)
    return s


def digit_tokens(s):
    out, cur = [], ""
    for ch in s:
        if ch in "0123456789":
            cur += ch
        elif cur:
            out.append(int(cur[:30]))
            cur = ""
    if cur:
        out.append(int(cur[:30]))
    return out


def rand_age_pair(rng, rcc):
    lifetime = rng.choice([0, 1, 2, 5, 10, 59, 60, 600, 1200, 1800, 3600, 86400,
                           2147483647, 2147483648, 2147483649, 10 ** 12])
    roll = rng.random()
    if roll < 0.35:
        candidates = digit_tokens(rcc)
        if candidates:
            d = rng.choice(candidates) + rng.choice([-1, 0, 0, 1])
        else:
            d = rng.randint(-3, 3)
    elif roll < 0.85:
        d = rng.randint(-3, 3)
    else:
        d = rng.choice([10 ** rng.randint(1, 30), 2147483648, 2147483649, 4294967296])
    age = max(0, lifetime + d)
    if rng.random() < 0.02:
        age = 10 ** rng.randint(1, 40)
    return lifetime, age


def maybe_bad(rng, value, choices):
    if rng.random() < 0.04:
        return rng.choice(choices)
    return value


def rand_obj(rng):
    dirty = rng.random() < 0.35
    make = rand_cc if dirty else rand_cc_clean
    rcc = make(rng)
    qcc = make(rng) if rng.random() < 0.55 else ""
    lifetime, age = rand_age_pair(rng, rcc)
    lifetime = maybe_bad(rng, lifetime, [True, False, 600.0, "600", None, -1, 1.5, [600], 2 ** 70])
    age = maybe_bad(rng, age, [True, 1.0, "600", None, -5, 0.5, {"a": 1}])
    event = rng.choices(["request", "error", "Request", "error ", "", "retry", None],
                        weights=[45, 45, 2, 2, 2, 2, 2])[0]
    obj = {"response_cc": rcc, "freshness_lifetime": lifetime, "current_age": age, "event": event}
    if rng.random() < 0.7:
        obj["request_cc"] = qcc
    if event == "error":
        err = rng.choice([500, 502, 503, 504, 500, 502, 503, 504, 501, 505, 499, 400, 404,
                          599, 600, 99, 100, 200, 300, "network", "network", "Network",
                          "timeout", None, True, 500.0, "500"])
        obj["error"] = err
    elif rng.random() < 0.08:
        obj["error"] = rng.choice([None, 500, "network", False])
    if rng.random() < 0.4:
        obj["shared"] = rng.choice([True, False, True, False, None, "true", 1])
    if rng.random() < 0.04:
        del obj[rng.choice(["response_cc", "freshness_lifetime", "current_age", "event"])]
    if rng.random() < 0.03:
        obj[rng.choice(["foo", "Event", "cache_control", "stale"])] = rng.choice([1, "x", None])
    if rng.random() < 0.02:
        obj["response_cc"] = rng.choice([None, 5, ["max-age=5"], True])
    if rng.random() < 0.02:
        obj["request_cc"] = rng.choice([None, 5, False])
    return obj


def encode_obj(rng, obj):
    ensure_ascii = rng.random() < 0.5
    text = json.dumps(obj, ensure_ascii=ensure_ascii, allow_nan=True)
    roll = rng.random()
    if roll < 0.035:
        cut = rng.randrange(1, max(2, len(text)))
        return text[:cut].encode("utf-8", "surrogatepass")
    if roll < 0.05:
        return ("\n\t " + text + rng.choice(["", "\n", "\r\n", " x", "}", "  \n\n"])).encode("utf-8", "surrogatepass")
    if roll < 0.06:
        return ("[" + text + "]").encode("utf-8", "surrogatepass")
    if roll < 0.065:
        return b"\xff" + text.encode("utf-8")
    if roll < 0.07:
        return ("\ufeff" + text).encode("utf-8", "surrogatepass")
    if roll < 0.075:
        return text.replace('"event"', '"event":"request","event"', 1).encode("utf-8", "surrogatepass")
    if roll < 0.08:
        return text.replace("600", "1E2", 1).encode("utf-8", "surrogatepass")
    if roll < 0.082:
        return text.replace("600", "00600", 1).encode("utf-8", "surrogatepass")
    if roll < 0.084:
        return text.replace('"response_cc"', '"\\u0072esponse_cc"', 1).encode("utf-8", "surrogatepass")
    return text.encode("utf-8", "surrogatepass")


# ---------------------------------------------------------------- targeted cases
def C(resp, ev="request", L=600, A=0, req=None, err=None, shared=None, drop=(), extra=None):
    o = {"response_cc": resp, "freshness_lifetime": L, "current_age": A, "event": ev}
    if req is not None:
        o["request_cc"] = req
    if err is not None:
        o["error"] = err
    if shared is not None:
        o["shared"] = shared
    for k in drop:
        o.pop(k, None)
    if extra:
        o.update(extra)
    return json.dumps(o)


REFUSE = ("refused",)


def D(decision, staleness):
    return ("decided", decision, staleness)


TARGETED = [
    # (label, raw_text, expectation)
    ("baseline-swr-boundary-inclusive", C("max-age=600, stale-while-revalidate=1200", L=600, A=1800), D("serve-stale-revalidate", 1200)),
    ("swr-just-over", C("stale-while-revalidate=1200", L=600, A=1801), D("revalidate", 1201)),
    ("swr-zero-at-equality", C("stale-while-revalidate=0", L=600, A=600), D("serve-stale-revalidate", 0)),
    ("fresh-one-below", C("stale-while-revalidate=5", L=600, A=599), D("fresh", 0)),
    ("request-no-cache-prohibits-fresh-age", C("stale-while-revalidate=100", L=600, A=5, req="no-cache"), D("revalidate", 0)),
    ("resp-no-cache-qualified", C('no-cache="Set-Cookie", stale-while-revalidate=100', L=600, A=650), D("revalidate", 50)),
    ("must-revalidate-prohibits", C("must-revalidate, stale-while-revalidate=100", L=600, A=650), D("revalidate", 50)),
    ("proxy-revalidate-shared", C("proxy-revalidate, stale-while-revalidate=100", L=600, A=650, shared=True), D("revalidate", 50)),
    ("proxy-revalidate-private", C("proxy-revalidate, stale-while-revalidate=100", L=600, A=650, shared=False), D("serve-stale-revalidate", 50)),
    ("s-maxage-shared", C("s-maxage=10, stale-while-revalidate=100", L=600, A=650, shared=True), D("revalidate", 50)),
    ("s-maxage-private", C("s-maxage=10, stale-while-revalidate=100", L=600, A=650, shared=False), D("serve-stale-revalidate", 50)),
    ("req-no-cache-with-swr", C("stale-while-revalidate=100", L=600, A=650, req="no-cache"), D("revalidate", 50)),
    ("req-max-age-refused", C("stale-while-revalidate=100", L=600, A=650, req="max-age=0"), REFUSE),
    ("req-MAX-AGE-upper-refused", C("stale-while-revalidate=100", L=600, A=650, req="MAX-AGE=0"), REFUSE),
    ("req-max-stale-refused", C("x", L=600, A=650, req="max-stale"), REFUSE),
    ("req-min-fresh-refused", C("x", L=600, A=650, req="min-fresh=3"), REFUSE),
    ("req-only-if-cached-refused", C("x", L=600, A=650, req="only-if-cached"), REFUSE),
    ("req-swr-ignored", C("", L=600, A=650, req="stale-while-revalidate=100"), D("revalidate", 50)),
    ("req-no-store-ignored", C("no-store, stale-while-revalidate=100", L=600, A=650, req="no-store, private"), D("serve-stale-revalidate", 50)),
    ("swr-quoted-absent", C('stale-while-revalidate="100"', L=600, A=650), D("revalidate", 50)),
    ("swr-first-occurrence-wins-high", C("stale-while-revalidate=100, stale-while-revalidate=5", L=600, A=650), D("serve-stale-revalidate", 50)),
    ("swr-first-occurrence-wins-low", C("stale-while-revalidate=5, stale-while-revalidate=100", L=600, A=650), D("revalidate", 50)),
    ("swr-first-quoted-then-valid", C('stale-while-revalidate="5", stale-while-revalidate=100', L=600, A=650), D("revalidate", 50)),
    ("swr-case-insensitive", C("STALE-WHILE-REVALIDATE=100", L=600, A=650), D("serve-stale-revalidate", 50)),
    ("swr-leading-zeros", C("stale-while-revalidate=00012", L=600, A=612), D("serve-stale-revalidate", 12)),
    ("swr-clamp-at-cap", C("stale-while-revalidate=2147483649", L=0, A=2147483648), D("serve-stale-revalidate", 2147483648)),
    ("swr-clamp-over-cap", C("stale-while-revalidate=2147483649", L=0, A=2147483649), D("revalidate", 2147483649)),
    ("swr-huge-clamped", C("stale-while-revalidate=" + "9" * 5000, L=0, A=2147483649), D("revalidate", 2147483649)),
    ("swr-huge-clamped-inside", C("stale-while-revalidate=" + "9" * 5000, L=0, A=2147483648), D("serve-stale-revalidate", 2147483648)),
    ("swr-non-digit-absent", C("stale-while-revalidate=5s", L=600, A=650), D("revalidate", 50)),
    ("swr-plus-absent", C("stale-while-revalidate=+5", L=600, A=650), D("revalidate", 50)),
    ("swr-no-value-absent", C("stale-while-revalidate", L=600, A=650), D("revalidate", 50)),
    ("swr-empty-value-refused", C("stale-while-revalidate=", L=600, A=650), REFUSE),
    ("swr-arabic-digit-refused", C("stale-while-revalidate=\u0663", L=600, A=650), REFUSE),
    ("swr-superscript-two-refused", C("stale-while-revalidate=\u00b2", L=600, A=650), REFUSE),
    ("space-around-equals-refused", C("max-age = 5", L=600, A=650), REFUSE),
    ("space-in-name-refused", C("a b", L=600, A=650), REFUSE),
    ("quoted-escape-ok", C('x="a\\"b"', L=10, A=0), D("fresh", 0)),
    ("unterminated-quote-refused", C('x="unterminated', L=10, A=0), REFUSE),
    ("text-after-quote-refused", C('x="a" y', L=10, A=0), REFUSE),
    ("quoted-comma-not-split", C('x="a,b", stale-while-revalidate=5', L=0, A=10), D("revalidate", 10)),
    ("lone-equals-refused", C("=5", L=10, A=0), REFUSE),
    ("comma-only-ok", C(",", L=10, A=0), D("fresh", 0)),
    ("blank-element-skipped", C(" , \t, stale-while-revalidate=100 ,", L=600, A=650), D("serve-stale-revalidate", 50)),
    ("ctl-outside-refused", C("x\u0001", L=10, A=0), REFUSE),
    ("del-refused", C("x\u007f", L=10, A=0), REFUSE),
    ("c1-inside-quotes-allowed", C('x="\u0080"', L=10, A=0), D("fresh", 0)),
    ("c1-outside-refused", C("x\u0080", L=10, A=0), REFUSE),
    ("above-ff-inside-quotes-refused", C('x="\u0100"', L=10, A=0), REFUSE),
    ("error-500-no-directives", C("stale-while-revalidate=100", ev="error", L=600, A=650, err=500), D("error-through", 50)),
    ("error-500-resp-sie", C("stale-if-error=100", ev="error", L=600, A=650, err=500), D("serve-stale-error", 50)),
    ("error-network-resp-sie", C("stale-if-error=100", ev="error", L=600, A=650, err="network"), D("serve-stale-error", 50)),
    ("error-404-not-an-error", C("stale-if-error=100", ev="error", L=600, A=650, err=404), D("not-an-error", 50)),
    ("error-501-not-an-error", C("stale-if-error=100", ev="error", L=600, A=650, err=501), D("not-an-error", 50)),
    ("error-100-not-an-error", C("", ev="error", L=600, A=650, err=100), D("not-an-error", 50)),
    ("error-599-not-an-error", C("", ev="error", L=600, A=650, err=599), D("not-an-error", 50)),
    ("error-503-counts", C("stale-if-error=50", ev="error", L=600, A=650, err=503), D("serve-stale-error", 50)),
    ("error-504-counts", C("stale-if-error=50", ev="error", L=600, A=650, err=504), D("serve-stale-error", 50)),
    ("error-502-serves", C("stale-if-error=50", ev="error", L=600, A=650, err=502), D("serve-stale-error", 50)),
    ("error-99-refused", C("", ev="error", L=600, A=650, err=99), REFUSE),
    ("error-600-refused", C("", ev="error", L=600, A=650, err=600), REFUSE),
    ("error-bool-refused", C("", ev="error", L=600, A=650, err=True), REFUSE),
    ("error-float-refused", C("", ev="error", L=600, A=650, err=500.0), REFUSE),
    ("error-string-500-refused", C("", ev="error", L=600, A=650, err="500"), REFUSE),
    ("error-missing-refused", C("", ev="error", L=600, A=650, drop=("error",)), REFUSE),
    ("error-null-refused", C("", ev="error", L=600, A=650, extra={"error": None}), REFUSE),
    ("request-with-error-refused", C("", ev="request", L=600, A=650, err=500), REFUSE),
    ("request-with-error-null-ok", C("stale-while-revalidate=100", ev="request", L=600, A=650, extra={"error": None}), D("serve-stale-revalidate", 50)),
    ("req-sie-overrides-resp", C("stale-if-error=100", ev="error", L=600, A=650, err=500, req="stale-if-error=10"), D("error-through", 50)),
    ("req-sie-overrides-bigger", C("stale-if-error=100", ev="error", L=600, A=650, err=500, req="stale-if-error=50"), D("serve-stale-error", 50)),
    ("req-sie-quoted-falls-back", C("stale-if-error=100", ev="error", L=600, A=650, err=500, req='stale-if-error="10"'), D("serve-stale-error", 50)),
    ("req-sie-nonnumeric-falls-back", C("stale-if-error=100", ev="error", L=600, A=650, err=500, req="stale-if-error=x"), D("serve-stale-error", 50)),
    ("req-sie-prohibited-by-shared", C("s-maxage=1, stale-if-error=100", ev="error", L=600, A=650, err=500, shared=True), D("error-through", 50)),
    ("req-no-cache-blocks-error", C("stale-if-error=100", ev="error", L=600, A=650, err=500, req="no-cache"), D("error-through", 50)),
    ("error-fresh-age-serves-fresh", C("stale-if-error=100", ev="error", L=600, A=599, err=500), D("fresh", 0)),
    ("error-fresh-but-req-no-cache", C("stale-if-error=100", ev="error", L=600, A=599, err=500, req="no-cache"), D("error-through", 0)),
    ("error-404-fresh-is-not-an-error", C("", ev="error", L=600, A=599, err=404), D("not-an-error", 0)),
    ("error-sie-zero-boundary", C("stale-if-error=0", ev="error", L=600, A=600, err=500), D("serve-stale-error", 0)),
    ("error-sie-zero-over", C("stale-if-error=0", ev="error", L=600, A=601, err=500), D("error-through", 1)),
    ("resp-no-cache-blocks-error", C("no-cache, stale-if-error=100", ev="error", L=600, A=650, err=500), D("error-through", 50)),
    ("event-capital-refused", C("", ev="Request", L=10, A=0), REFUSE),
    ("event-missing-refused", C("", L=10, A=0, drop=("event",)), REFUSE),
    ("lifetime-float-refused", C("", L=600.0, A=0), REFUSE),
    ("lifetime-true-refused", C("", L=True, A=0), REFUSE),
    ("lifetime-negative-refused", C("", L=-1, A=0), REFUSE),
    ("lifetime-string-refused", C("", L="600", A=0), REFUSE),
    ("age-null-refused", C("", L=10, A=None), REFUSE),
    ("age-exp-float-refused", '{"response_cc":"","freshness_lifetime":1,"current_age":1E2,"event":"request"}', REFUSE),
    ("shared-null-refused", C("", L=10, A=0, shared=None, extra={"shared": None}), REFUSE),
    ("shared-string-refused", C("", L=10, A=0, extra={"shared": "true"}), REFUSE),
    ("unknown-key-refused", C("", L=10, A=0, extra={"foo": 1}), REFUSE),
    ("request-cc-null-refused", C("", L=10, A=0, extra={"request_cc": None}), REFUSE),
    ("response-cc-missing-refused", C("", L=10, A=0, drop=("response_cc",)), REFUSE),
    ("top-array-refused", "[1,2]", REFUSE),
    ("empty-object-refused", "{}", REFUSE),
    ("invalid-json-refused", '{"response_cc":', REFUSE),
    ("trailing-garbage-refused", C("", L=10, A=0) + " x", REFUSE),
    ("trailing-newline-ok", C("", L=10, A=0) + "\n", D("fresh", 0)),
    ("two-objects-refused", C("", L=10, A=0) + C("", L=10, A=0), REFUSE),
    ("duplicate-key-refused", '{"response_cc":"","freshness_lifetime":1,"current_age":0,"event":"request","event":"error"}', REFUSE),
    ("bom-refused", "\ufeff" + C("", L=10, A=0), REFUSE),
    ("nan-refused", '{"response_cc":"","freshness_lifetime":NaN,"current_age":0,"event":"request"}', REFUSE),
    ("big-freshness-int-accepted", '{"response_cc":"","freshness_lifetime":' + "1" + "0" * 4000 + ',"current_age":' + "1" + "0" * 4000 + ',"event":"request"}', D("revalidate", 0)),
    ("big-age-staleness-exact", '{"response_cc":"stale-while-revalidate=5","freshness_lifetime":0,"current_age":' + "7" * 5000 + ',"event":"request"}', D("revalidate", int("7" * 5000))),
    ("swr-leading-zeros-5000", C("stale-while-revalidate=" + "0" * 5000 + "5", L=0, A=5), D("serve-stale-revalidate", 5)),
]


def targeted_inputs():
    out = []
    for label, raw, exp in TARGETED:
        out.append({"label": label, "class": "targeted", "raw": raw.encode("utf-8", "surrogatepass"), "expect": exp})
    return out


def random_inputs(rng, count):
    out = []
    for i in range(count):
        obj = rand_obj(rng)
        out.append({"label": "rand-%05d" % i, "class": "random", "raw": encode_obj(rng, obj), "expect": None})
    return out


# ---------------------------------------------------------------- runner
def run_cli(script, data, cwd):
    p = subprocess.run([sys.executable, str(script)], input=data, capture_output=True, cwd=cwd, timeout=30)
    return p.returncode, p.stdout, p.stderr


def classify(rc, out, err):
    if rc == 0:
        if not out.endswith(b"\n") or out.count(b"\n") != 1:
            return ("format-bad", rc, out[:160].decode("utf-8", "replace"))
        try:
            obj = json.loads(out.decode("utf-8"))
        except Exception:
            return ("format-bad", rc, out[:160].decode("utf-8", "replace"))
        if (not isinstance(obj, dict) or set(obj) != {"decision", "staleness"}
                or not isinstance(obj["decision"], str)
                or isinstance(obj["staleness"], bool) or not isinstance(obj["staleness"], int)):
            return ("format-bad", rc, out[:160].decode("utf-8", "replace"))
        return ("decided", obj["decision"], obj["staleness"])
    if rc == 1 and out == b"" and err.startswith(b"invalid_input:"):
        return REFUSE
    return ("unexpected", rc, out[:160].decode("utf-8", "replace"), err[:200].decode("utf-8", "replace"))


def show(data):
    text = data.decode("utf-8", "backslashreplace")
    return text if len(text) <= 260 else text[:260] + "...(+%d)" % (len(text) - 260)


def fmt_cls(c):
    return json.dumps(c, ensure_ascii=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=2400)
    ap.add_argument("--seed", type=int, default=98)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", default=str(SEAT))
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    work = pathlib.Path(args.work).resolve()
    outdir = pathlib.Path(args.out).resolve()
    work.mkdir(parents=True, exist_ok=True)
    outdir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)

    inputs = targeted_inputs() + random_inputs(rng, args.count)
    with (work / "inputs.jsonl").open("w") as fh:
        for it in inputs:
            fh.write(json.dumps({"label": it["label"], "class": it["class"],
                                 "b64": base64.b64encode(it["raw"]).decode()}) + "\n")

    cwd = str(work)

    def one(it):
        t = run_cli(TWIN, it["raw"], cwd)
        o = run_cli(ORACLE, it["raw"], cwd)
        return it, t, o

    with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(one, inputs))

    counts = {"n": 0, "match": 0, "disagree": 0, "twin_decided": 0, "twin_refused": 0,
              "twin_internal": 0, "expect_fail_twin": 0, "expect_fail_oracle": 0,
              "targeted": 0, "random": 0}
    disagreements = []
    lines = []
    for it, (trc, tout, terr), (orc, oout, oerr) in results:
        counts["n"] += 1
        counts[it["class"]] += 1
        tc = classify(trc, tout, terr)
        oc = classify(orc, oout, oerr)
        if trc == 2:
            counts["twin_internal"] += 1
        if tc[0] == "decided":
            counts["twin_decided"] += 1
            counts["dec:" + tc[1]] = counts.get("dec:" + tc[1], 0) + 1
        elif tc == REFUSE:
            counts["twin_refused"] += 1
        exp_note = ""
        if it["expect"] is not None:
            if tc != it["expect"]:
                counts["expect_fail_twin"] += 1
                exp_note += " TWIN!=EXPECT"
            if oc != it["expect"]:
                counts["expect_fail_oracle"] += 1
                exp_note += " ORACLE!=EXPECT"
        same = tc == oc
        if same:
            counts["match"] += 1
        else:
            counts["disagree"] += 1
            disagreements.append({"label": it["label"], "input": show(it["raw"]),
                                  "twin": tc, "twin_rc": trc, "oracle": oc, "oracle_rc": orc,
                                  "expect": it["expect"]})
        lines.append("%s | %s | twin=%s rc=%d | oracle=%s rc=%d | %s%s" % (
            it["label"], it["class"], fmt_cls(tc), trc, fmt_cls(oc), orc,
            "MATCH" if same else "DISAGREE", exp_note))
        lines.append("    input: " + json.dumps(show(it["raw"])))

    with (outdir / "disagreements.jsonl").open("w") as fh:
        for d in disagreements:
            fh.write(json.dumps(d) + "\n")

    header = [
        "# EXEC-TWIN diff-run (ExecTwinStale, kake round 98, C2)",
        "# python3 %s --count %d --seed %d --work <scratch> --out <seat>" % (
            pathlib.Path(__file__).name, args.count, args.seed),
        "# python: " + sys.version.split()[0],
        "# twin:   " + str(TWIN),
        "# oracle: " + str(ORACLE) + " (counter CLI; run as subprocess, code not read)",
        "# inputs: %d total (targeted %d, random %d)" % (counts["n"], counts["targeted"], counts["random"]),
        "# twin decided=%d refused=%d internal_errors=%d" % (
            counts["twin_decided"], counts["twin_refused"], counts["twin_internal"]),
        "# match=%d disagree=%d" % (counts["match"], counts["disagree"]),
        "# expectation failures: twin=%d oracle=%d" % (counts["expect_fail_twin"], counts["expect_fail_oracle"]),
        "# twin decision coverage: " + ", ".join(
            "%s=%d" % (k[4:], v) for k, v in sorted(counts.items()) if k.startswith("dec:")),
        "",
    ]
    (outdir / "diff-run.txt").write_text("\n".join(header + lines) + "\n")

    print("\n".join(header))
    print("disagreements written: %d" % len(disagreements))
    return 0


if __name__ == "__main__":
    sys.exit(main())
