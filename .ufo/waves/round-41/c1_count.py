#!/usr/bin/env python3
"""Round-41 C1 counter: does `scripts/sitemap_audit.py` judge `loc` and `sitemapUrl` values the way
the RFC 3986 `URI` grammar (Appendix A, as published in the `abnf` 2.9.1 package) judges them?

Usage (exit 0 met, 1 not met, 2 cannot evaluate; a receipt is written in every case):
  python3 -B .ufo/waves/round-41/c1_count.py --root . --revision <rev> [--seed N] --out <receipt>
  python3 -B .ufo/waves/round-41/c1_count.py --root . --tool-file <path> [--label L] [--seed N] --out <receipt>

Cases are generated per run from the seed (random when not given; recorded in the receipt):
one inserted unit (an ASCII character or a percent sequence) at an interior position of one
component (userinfo, host, port, path, query, fragment) of an otherwise valid http(s) URL whose
other characters are random characters valid in their component (percent triplets included).
`loc` cases use the XML-legal ASCII characters (TAB, LF, CR, U+0020-U+007F) written
raw or as character references at random; `sitemapUrl` cases use U+0000-U+007F. The expected label
of every case comes from the oracle only: valid when the value parses as RFC 3986 `URI`, its scheme
is `http` or `https` (case-insensitive) and it has an authority with a non-empty host (contract
sentence 22). A tool agrees on a `loc` case when it reports `loc_not_absolute` for that entry exactly
when the oracle says invalid, and on a `sitemapUrl` case when that check is an error with
`check_invalid` exactly when the oracle says invalid. No other output is read.

The tool runs once per run in bubblewrap (`/usr`, one case directory and the tool; no network,
private pid namespace, empty environment). Directory, file, mount and id names are random and carry
no case identity or label; labels never leave this process before the tool has exited.
"""
import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import tempfile
import zipfile

PREDICATE = ("met: the tool's judgment of loc and sitemapUrl agrees with the RFC 3986 URI oracle "
             "on 1434 of 1434 generated cases")
CASES = 1434
TOOL_PATH = "scripts/sitemap_audit.py"
HERE = os.path.dirname(os.path.abspath(__file__))
ORACLE_WHEEL = os.path.join(HERE, "oracle", "abnf-2.9.1-py3-none-any.whl")
ORACLE_SHA256 = "cdcac127b3693ded2b00565878d8ed2b96d34b29f0ee199c06d7b40baaf60917"
RUN_TIMEOUT = 600

COMPONENTS = ("userinfo", "host", "port", "path", "query", "fragment")
LOC_UNITS = [chr(9), chr(10), chr(13)] + [chr(c) for c in range(0x20, 0x80)]       # 99
URL_UNITS = [chr(c) for c in range(0x00, 0x80)]                                    # 128
PCT_UNITS = ["%41", "%7e", "%4G", "%G4", "%", "%2"]                                # 6
LOWER = "abcdefghijklmnopqrstuvwxyz"
ALNUM = LOWER + "0123456789"
TLDS = ("com", "net", "org", "example", "test", "io")
UNRESERVED = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~"
SUB_DELIMS = "!$&'()*+,;="
FILL = {"userinfo": UNRESERVED + SUB_DELIMS + ":", "host": UNRESERVED + SUB_DELIMS,
        "path": UNRESERVED + SUB_DELIMS + ":@", "query": UNRESERVED + SUB_DELIMS + ":@/?",
        "fragment": UNRESERVED + SUB_DELIMS + ":@/?"}


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], check=True, capture_output=True).stdout


def load_oracle():
    data = open(ORACLE_WHEEL, "rb").read()
    if hashlib.sha256(data).hexdigest() != ORACLE_SHA256:
        raise RuntimeError("oracle wheel sha256 mismatch")
    zipfile.ZipFile(ORACLE_WHEEL).testzip()
    sys.path.insert(0, ORACLE_WHEEL)
    from abnf.grammars import rfc3986
    from abnf import ParseError
    rule = rfc3986.Rule("URI")

    def find(node, name):
        if node.name == name:
            return node
        for child in node.children:
            hit = find(child, name)
            if hit is not None:
                return hit
        return None

    def valid(value):
        try:
            node = rule.parse_all(value)
        except ParseError:
            return False
        scheme = find(node, "scheme")
        if scheme is None or scheme.value.lower() not in ("http", "https"):
            return False
        authority = find(node, "authority")
        if authority is None:
            return False
        host = find(authority, "host")
        return host is not None and host.value != ""

    return valid


def tok(rng, lo=4, hi=8):
    return rng.choice(LOWER) + "".join(rng.choice(ALNUM) for _ in range(rng.randint(lo, hi) - 1))


def fill(rng, comp, lo=4, hi=10):
    """Random text that is valid in `comp` (RFC 3986): two letters or digits, then characters of
    the component's repertoire and percent-encoded triplets."""
    out = [rng.choice(ALNUM), rng.choice(ALNUM)]
    for _ in range(rng.randint(lo, hi) - 2):
        roll = rng.random()
        if roll < 0.1:
            out.append("%" + "".join(rng.choice("0123456789ABCDEFabcdef") for _ in range(2)))
        elif roll < 0.55:
            out.append(rng.choice(FILL[comp]))
        else:
            out.append(rng.choice(ALNUM))
    return "".join(out)


def insert(rng, text, unit):
    i = rng.randint(1, len(text) - 1)
    return text[:i] + unit + text[i:]


def make_url(rng, target, unit):
    """An http(s) URL with `unit` inserted at an interior position of component `target`."""
    scheme = rng.choice(("http", "https", "HTTP", "Https"))
    userinfo = None
    if target == "userinfo" or rng.random() < 0.1:
        first = fill(rng, "host")
        if target == "userinfo":
            first = insert(rng, first, unit)
        userinfo = first + (":" + fill(rng, "userinfo") if rng.random() < 0.5 else "")
    roll = rng.random()
    if target == "host" or roll < 0.8:
        label = fill(rng, "host")
        if target == "host":
            label = insert(rng, label, unit)
        host = label + "." + rng.choice(TLDS)
    elif roll < 0.9:
        host = "192.0.2." + str(rng.randint(1, 254))
    else:
        host = "[2001:db8::" + format(rng.randint(1, 0xffff), "x") + "]"
    port = None
    if target == "port" or rng.random() < 0.1:
        port = str(rng.randint(10, 99))
        if target == "port":
            port = insert(rng, port, unit)
    segments = [fill(rng, "path") for _ in range(rng.randint(1, 3))]
    if target == "path":
        k = rng.randrange(len(segments))
        segments[k] = insert(rng, segments[k], unit)
    query = None
    if target == "query" or rng.random() < 0.4:
        query = fill(rng, "query")
        if target == "query":
            query = insert(rng, query, unit)
    fragment = None
    if target == "fragment" or rng.random() < 0.2:
        fragment = fill(rng, "fragment")
        if target == "fragment":
            fragment = insert(rng, fragment, unit)
    url = scheme + "://" + (userinfo + "@" if userinfo is not None else "") + host
    url += (":" + port if port is not None else "") + "/" + "/".join(segments)
    url += ("?" + query if query is not None else "") + ("#" + fragment if fragment is not None else "")
    return url


def xml_text(rng, value):
    out = []
    for ch in value:
        if ch in "&<>\"'" or ord(ch) < 0x20 or ord(ch) == 0x7F or (not ch.isalnum() and rng.random() < 0.3):
            out.append(("&#%d;" % ord(ch)) if rng.random() < 0.5 else ("&#x%X;" % ord(ch)))
        else:
            out.append(ch)
    return "".join(out)


def generate(rng, valid):
    specs = [("loc", comp, unit) for comp in COMPONENTS for unit in LOC_UNITS + PCT_UNITS]
    specs += [("sitemapUrl", comp, unit) for comp in COMPONENTS for unit in URL_UNITS + PCT_UNITS]
    cases = []
    for field, comp, unit in specs:
        value = make_url(rng, comp, unit)
        cases.append({"field": field, "component": comp, "unit": unit, "value": value,
                      "valid": valid(value)})
    rng.shuffle(cases)
    return cases


def layout(rng, cases, cd):
    """Write the manifest and sitemap files; return (manifest name, plan) where plan maps each case
    to (check index, entry index or None)."""
    def name():
        return "%x" % rng.getrandbits(64)

    used = set()

    def fresh_id():
        while True:
            v = tok(rng, 6, 12)
            if v not in used:
                used.add(v)
                return v

    def urlset(values):
        body = "".join("<url><loc>%s</loc></url>" % xml_text(rng, v) for v in values)
        return ('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % body)

    shared = name() + ".xml"
    shared_host = tok(rng) + ".com"
    with open(os.path.join(cd, shared), "w", encoding="utf-8") as fh:
        fh.write(urlset(["https://%s/%s/%s" % (shared_host, tok(rng), tok(rng))]))
    checks = []
    plan = [None] * len(cases)
    loc_idx = [i for i, c in enumerate(cases) if c["field"] == "loc"]
    groups = []
    while loc_idx:
        n = rng.randint(20, 60)
        groups.append(loc_idx[:n])
        loc_idx = loc_idx[n:]
    url_idx = [i for i, c in enumerate(cases) if c["field"] == "sitemapUrl"]
    items = [("g", g) for g in groups] + [("u", i) for i in url_idx]
    rng.shuffle(items)
    for kind, payload in items:
        if kind == "g":
            fname = name() + ".xml"
            with open(os.path.join(cd, fname), "w", encoding="utf-8") as fh:
                fh.write(urlset([cases[i]["value"] for i in payload]))
            host = tok(rng) + "." + rng.choice(TLDS)
            checks.append({"id": fresh_id(), "file": fname,
                           "sitemapUrl": "https://%s/%s/sitemap.xml" % (host, tok(rng))})
            for k, i in enumerate(payload, 1):
                plan[i] = (len(checks) - 1, k)
        else:
            checks.append({"id": fresh_id(), "file": shared, "sitemapUrl": cases[payload]["value"]})
            plan[payload] = (len(checks) - 1, None)
    mname = name() + ".json"
    with open(os.path.join(cd, mname), "w", encoding="utf-8") as fh:
        json.dump({"version": 1, "checks": checks}, fh)
    return mname, plan


def sandbox_argv(cd, work, tool, tname, mname):
    return ["bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/lib", "/lib",
            "--symlink", "usr/lib64", "/lib64", "--symlink", "usr/bin", "/bin",
            "--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
            "--ro-bind", cd, work, "--ro-bind", tool, tname, "--chdir", work,
            "--unshare-all", "--die-with-parent", "--new-session", "--clearenv",
            "--setenv", "PATH", "/usr/bin", "--setenv", "LANG", "C.UTF-8",
            "/usr/bin/python3", "-B", tname, "--manifest", work + "/" + mname]


def judge(cases, plan, stdout):
    try:
        doc = json.loads(stdout)
        items = doc["checks"]
        if not isinstance(items, list):
            raise ValueError("checks not a list")
    except Exception as ex:
        return [False] * len(cases), "output unreadable: %s" % str(ex)[:200]
    out = []
    for case, (ci, entry) in zip(cases, plan):
        try:
            item = items[ci]
            if entry is None:
                said_invalid = item.get("status") == "error" and item.get("error") == "check_invalid"
            else:
                said_invalid = any(isinstance(f, dict) and f.get("code") == "loc_not_absolute"
                                   and f.get("entry") == entry for f in (item.get("findings") or []))
            out.append(said_invalid == (not case["valid"]))
        except Exception:
            out.append(False)
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--revision")
    src.add_argument("--tool-file")
    ap.add_argument("--label", default="")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--out")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(6), "big")
    rec = {"predicate": PREDICATE, "cases": CASES, "passed": None, "met": False, "revision": None,
           "toolFile": a.tool_file, "label": a.label, "seed": seed,
           "counterSha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
           "oracleSha256": ORACLE_SHA256, "toolSha256": None, "toolExit": None, "byField": {},
           "byComponent": {}, "oracleInvalid": None, "note": None, "misses": []}

    def finish(code):
        s = json.dumps(rec, indent=1)
        if a.out:
            with open(a.out, "w") as fh:
                fh.write(s + "\n")
        print(json.dumps({k: rec[k] for k in ("label", "revision", "passed", "cases", "byField",
                                              "met", "note")}))
        sys.exit(code)

    try:
        valid = load_oracle()
    except Exception as ex:
        rec["note"] = "cannot evaluate: oracle: %s" % ex
        finish(2)
    if subprocess.run(["sh", "-c", "command -v bwrap"], capture_output=True).returncode != 0:
        rec["note"] = "cannot evaluate: bwrap missing"
        finish(2)
    if a.revision:
        try:
            rev = git(root, "rev-parse", "--verify", "%s^{commit}" % a.revision).decode().strip()
        except Exception as ex:
            rec["note"] = "cannot evaluate: revision: %s" % ex
            finish(2)
        rec["revision"] = rev
        try:
            data = git(root, "show", "%s:%s" % (rev, TOOL_PATH))
        except subprocess.CalledProcessError:
            data = None
    else:
        try:
            data = open(a.tool_file, "rb").read()
        except OSError:
            data = None
    rng = random.Random(seed)
    cases = generate(rng, valid)
    if len(cases) != CASES:
        rec["note"] = "cannot evaluate: generated %d cases" % len(cases)
        finish(2)
    rec["oracleInvalid"] = sum(1 for c in cases if not c["valid"])
    if data is None:
        agree, why = [False] * len(cases), "tool absent"
    else:
        rec["toolSha256"] = hashlib.sha256(data).hexdigest()
        with tempfile.TemporaryDirectory(prefix="%x-" % rng.getrandbits(32)) as td:
            cd = os.path.join(td, "%x" % rng.getrandbits(48))
            os.makedirs(cd)
            tool = os.path.join(td, "%x.py" % rng.getrandbits(48))
            with open(tool, "wb") as fh:
                fh.write(data)
            mname, plan = layout(rng, cases, cd)
            work = "/%x" % rng.getrandbits(40)
            tname = "/%x/%x.py" % (rng.getrandbits(40), rng.getrandbits(40))
            try:
                p = subprocess.run(sandbox_argv(cd, work, tool, tname, mname), cwd=td,
                                   capture_output=True, timeout=RUN_TIMEOUT)
                rec["toolExit"] = p.returncode
                agree, why = judge(cases, plan, p.stdout.decode("utf-8", "replace"))
            except subprocess.TimeoutExpired:
                agree, why = [False] * len(cases), "timeout"
    rec["note"] = why
    rec["passed"] = sum(agree)
    for key, bucket in (("field", rec["byField"]), ("component", rec["byComponent"])):
        for case, ok in zip(cases, agree):
            b = bucket.setdefault(case[key], [0, 0])
            b[0] += ok
            b[1] += 1
    rec["byField"] = {k: "%d/%d" % tuple(v) for k, v in sorted(rec["byField"].items())}
    rec["byComponent"] = {k: "%d/%d" % tuple(v) for k, v in sorted(rec["byComponent"].items())}
    rec["misses"] = [{"field": c["field"], "component": c["component"], "unit": c["unit"],
                      "value": c["value"], "oracleValid": c["valid"]}
                     for c, ok in zip(cases, agree) if not ok][:200]
    rec["met"] = len(agree) == CASES and rec["passed"] == CASES
    finish(0 if rec["met"] else 1)


if __name__ == "__main__":
    main()
