#!/usr/bin/env python3
"""H4 harm probe (kake r42 wave 1): generalize the round-41 closure probe.

Usage:
  python3 -B h4_probe.py --tool-file <cand.py> --base-file <base40.py> \
      --seed N --out <receipt.json> [--count 20000] [--sitemaps <dir>]

Method (a direct generalization of /fast/scratch/hyaku/kake-r42/shared/closure-probe/
probe.py, sha256 01498b1b60d343f0eabb5ec5f342a3c358a56ce6c994b432a35aa2ec2f91a0b5,
which is the round-41 closure's probe script):

  * values: 0-3 random mutations (insertion at any position including the ends,
    deletion, duplication) of the real <loc> values of the retained sitemaps;
    inserted units: ASCII 0x00-0x7F, broken percent units ("%", "%4", "%zz",
    "%41"), delimiters ("@", "#", "?", ":", "//"), "[", "]", "e-acute", ":99999".
  * tools: each side's _parse_url imported from its own file (importlib).
  * oracle: vendored abnf 2.9.1 rfc3986.Rule("URI").parse_all (wheel sha256
    cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917) plus
    http(s) scheme and a non-empty host.
  * class: the closure's own out-of-class rule (non-ASCII, a "[" in the
    authority/host slot, or a port above 65535); "in-class" values are the
    only ones counted for oracleDisagree.

Reported measures:
  validReject   base accepts AND oracle accepts AND candidate rejects
  newAccept     base rejects AND candidate accepts
  oracleDisagree (in-class only, as the closure defined it) candidate vs oracle
  plus counts (n, inClass, outOfClass) and the base's own in-class
  oracle disagreements (the closure's base-vs-oracle number).

Exit 0: receipt written. Exit 2: cannot evaluate (bad arguments, wheel sha
mismatch, missing tool/base attribute, no loc values).
"""

import argparse
import hashlib
import importlib.util
import json
import os
import random
import re
import sys

ORACLE_WHEEL = ("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-41/oracle/"
                "abnf-2.9.1-py3-none-any.whl")   # L1: lane copy, same sha256 as the scratch copy
ORACLE_WHEEL_SHA256 = "cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917"
DEFAULT_SITEMAPS = ("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/"
                     "round-41/realrun/sitemaps/")

MAX_EXAMPLES = 5


def fail(msg):
    sys.stderr.write("h4_probe: %s\n" % msg)
    raise SystemExit(2)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_tool(path, name):
    if not os.path.isfile(path):
        fail("tool file not found: %s" % path)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail("cannot import %s" % path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, "_parse_url", None)
    if fn is None:
        fail("%s has no _parse_url" % path)
    return fn


def load_oracle():
    if not os.path.isfile(ORACLE_WHEEL):
        fail("oracle wheel not found: %s" % ORACLE_WHEEL)
    got = sha256_file(ORACLE_WHEEL)
    if got != ORACLE_WHEEL_SHA256:
        fail("oracle wheel sha256 mismatch: %s != %s" % (got, ORACLE_WHEEL_SHA256))
    sys.path.insert(0, ORACLE_WHEEL)
    try:
        from abnf.grammars import rfc3986
        from abnf.parser import ParseError
    except Exception as exc:                      # pragma: no cover - env fault
        fail("cannot import abnf from vendored wheel: %r" % (exc,))
    return rfc3986.Rule("URI"), ParseError


def oracle(value, URI, ParseError):
    """Closure oracle: RFC 3986 URI parse, http(s) scheme, non-empty host."""
    try:
        URI.parse_all(value)
    except ParseError:
        return False
    m = re.match(r"([A-Za-z][A-Za-z0-9+.\-]*)://([^/?#]*)", value)
    if not m or m.group(1).lower() not in ("http", "https"):
        return False
    auth = m.group(2).rsplit("@", 1)[-1]
    host = auth[: auth.rfind("]") + 1] if auth.startswith("[") else auth.split(":")[0]
    return bool(host)


def out_of_class(value):
    """The round-41 closure's class rule, verbatim."""
    if "[" in value.split("/", 3)[2] if value.count("/") >= 2 else False:
        return True
    if any(ord(c) > 0x7F for c in value):
        return True
    m = re.match(r"[A-Za-z][A-Za-z0-9+.\-]*://(?:[^/?#@]*@)?[^/?#:]*:(\d+)", value)
    return bool(m and len(m.group(1)) and int(m.group(1)) > 65535)


def read_locs(directory):
    locs = []
    names = sorted(n for n in os.listdir(directory) if n.endswith(".xml"))
    for name in names:
        with open(os.path.join(directory, name), encoding="utf-8") as fh:
            locs += re.findall(r"<loc>([^<]+)</loc>", fh.read())
    return [l.strip().replace("&amp;", "&") for l in locs]


def main(argv=None):
    ap = argparse.ArgumentParser(description="H4 harm probe (round-42 wave 1)")
    ap.add_argument("--tool-file", required=True, help="candidate tool (.py)")
    ap.add_argument("--base-file", required=True, help="round-40 base tool (.py)")
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out", required=True, help="receipt JSON path")
    ap.add_argument("--count", type=int, default=20000,
                    help="number of mutated values (default 20000, the closure's count)")
    ap.add_argument("--sitemaps", default=DEFAULT_SITEMAPS)
    args = ap.parse_args(argv)

    URI, ParseError = load_oracle()
    cand_parse = load_tool(args.tool_file, "h4_cand_tool")
    base_parse = load_tool(args.base_file, "h4_base_tool")
    if not os.path.isdir(args.sitemaps):
        fail("sitemaps dir not found: %s" % args.sitemaps)
    locs = read_locs(args.sitemaps)
    if not locs:
        fail("no <loc> values under %s" % args.sitemaps)

    rng = random.Random(args.seed)
    ALPHA = ([chr(c) for c in range(0x00, 0x80)]
             + ["%", "%4", "%zz", "%41", "@", "#", "?", ":", "//", "[", "]", "é",
                ":99999"])

    stats = {
        "n": 0,
        "inClass": 0,
        "outOfClass": 0,
        "validReject": 0,
        "newAccept": 0,
        "oracleDisagree": 0,
        "oracleDisagreeAcceptInvalid": 0,
        "oracleDisagreeRejectValid": 0,
        "baseOracleDisagree": 0,
        "baseOracleDisagreeAcceptInvalid": 0,
        "baseOracleDisagreeRejectValid": 0,
        "candidateAcceptsBaseRejects": 0,
        "candidateRejectsBaseAccepts": 0,
        "outOfClassChanged": 0,
    }
    examples = {}

    def note(key, value):
        bucket = examples.setdefault(key, [])
        if len(bucket) < MAX_EXAMPLES:
            bucket.append(repr(value))

    for _ in range(args.count):
        v = rng.choice(locs)
        for _ in range(rng.choice([0, 1, 1, 2, 3])):
            op = rng.random()
            p = rng.randint(0, len(v))
            if op < 0.7:
                v = v[:p] + rng.choice(ALPHA) + v[p:]
            elif op < 0.9 and len(v) > 1:
                v = v[:p] + v[p + 1:]
            else:
                v = v[:p] + v[p:p + 3] + v[p:]
        stats["n"] += 1
        b = base_parse(v) is not None
        c = cand_parse(v) is not None
        if out_of_class(v):
            stats["outOfClass"] += 1
            if b != c:
                stats["outOfClassChanged"] += 1
                o = oracle(v, URI, ParseError)
                key = "outOfClass_base%d_cand%d_oracle%d" % (b, c, o)
                stats[key] = stats.get(key, 0) + 1
                note(key, v)
            continue
        stats["inClass"] += 1
        o = oracle(v, URI, ParseError)
        if b != o:
            stats["baseOracleDisagree"] += 1
            if b:
                stats["baseOracleDisagreeAcceptInvalid"] += 1
            else:
                stats["baseOracleDisagreeRejectValid"] += 1
            note("baseOracleDisagree_acceptInvalid" if b else
                 "baseOracleDisagree_rejectValid", v)
        if c != o:
            stats["oracleDisagree"] += 1
            if c:
                stats["oracleDisagreeAcceptInvalid"] += 1
            else:
                stats["oracleDisagreeRejectValid"] += 1
            note("oracleDisagree_acceptInvalid" if c else
                 "oracleDisagree_rejectValid", v)
        if b and o and not c:
            stats["validReject"] += 1
            note("validReject", v)
        if not b and c:
            stats["newAccept"] += 1
            note("newAccept", v)
        if c and not b:
            stats["candidateAcceptsBaseRejects"] += 1
        if b and not c:
            stats["candidateRejectsBaseAccepts"] += 1

    receipt = {
        "probe": "h4_probe",
        "wave": "r42-w1",
        "seed": args.seed,
        "count": args.count,
        "toolFile": args.tool_file,
        "toolSha256": sha256_file(args.tool_file),
        "baseFile": args.base_file,
        "baseSha256": sha256_file(args.base_file),
        "sitemaps": args.sitemaps,
        "oracleWheel": ORACLE_WHEEL,
        "oracleWheelSha256": ORACLE_WHEEL_SHA256,
        "locs": len(locs),
        "counts": stats,
        "examples": examples,
    }
    out = os.path.abspath(args.out)
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({"out": out, "counts": stats}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
